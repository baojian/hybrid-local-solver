"""I4-B -- ONE composed local PPR solver:

    (i)   growth driven by the I3-B KINETIC GATE (push accumulators, no
          boundary adjacency scan ever),
    (ii)  a BALL-TREEWIDTH TRIAGE routing the interior solve to ELIMINATION
          (sparse LU / fill-free tree elimination) or LOCAL AMG (I3-A),
    (iii) certified termination on the semantic target
          ||D^{-1/2}(Qx-b)||_inf < alpha*eps  =>  max_i|pi_i-pi^_i|/d_i < eps.

Every counter maps onto the project's eleven-coordinate resource vector
(ledger.py).  Nothing is uncharged except the reference exact solve used for
verification only.
"""
import heapq
import math
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from ledger import Ledger

import sys
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
from amglib import build_hierarchy, v_cycle          # noqa: E402


# ===========================================================  T R I A G E ===

TRI_ABS_CAP = 3.0e5      # absolute cap on symbolic-elimination ops per test


def triage(nbrs, volS, kappa=8.0, abs_cap=TRI_ABS_CAP):
    """BALL-TREEWIDTH TRIAGE.  `nbrs` = list of python sets, the induced
    adjacency of the active set S in LOCAL indices.

    Step 1 (Euler test, O(|S| + m)):  cyclomatic number  cyc = m - n + c
    via union-find.  cyc == 0  <=>  the region is a FOREST  <=>  the
    seed-rooted elimination order is fill-free  =>  ELIM, no further work.
    (Also: |V(kernel)| <= 2*cyc and tw(S) <= cyc+1, so tiny cyc is already a
    treewidth certificate.)

    Step 2 (budgeted greedy min-degree symbolic elimination): simulate
    elimination, accumulating the exact factor flop count sum_v deg(v)^2.
    Abort the moment it exceeds  budget = min(kappa*vol(S), abs_cap).
    Completing within budget certifies elimination is affordable -> ELIM;
    aborting is a (one-sided) witness of high fill -> AMG.

    Cost model: 1 charged op per union-find step, per degree update and per
    clique-merge insertion -- i.e. the charged cost equals the work actually
    performed, and is bounded by `budget` by construction.
    Returns (route, ops_charged, cyc, fill_flops_or_None).
    """
    n = len(nbrs)
    ops = 0.0
    # ---- step 1: Euler / forest test
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    m = 0
    ncomp = n
    for i in range(n):
        for j in nbrs[i]:
            if j > i:
                m += 1
                ra, rb = find(i), find(j)
                if ra != rb:
                    par[ra] = rb
                    ncomp -= 1
    ops += float(n + 2 * m)
    cyc = m - n + ncomp
    if cyc <= 0:
        return "elim", ops, cyc, float(2 * m)     # forest: fill-free
    # ---- step 2: budgeted min-degree symbolic elimination
    budget = min(kappa * max(volS, 1.0), abs_cap)
    adj = [set(s) for s in nbrs]
    ops += float(n + 2 * m)                        # copy the pattern
    deg = [len(a) for a in adj]
    heap = [(deg[i], i) for i in range(n)]
    heapq.heapify(heap)
    ops += float(n)
    alive = [True] * n
    flops = 0.0
    left = n
    while left and heap:
        d, v = heapq.heappop(heap)
        ops += 1.0
        if not alive[v] or d != deg[v]:
            continue
        alive[v] = False
        left -= 1
        nb = [u for u in adj[v] if alive[u]]
        k = len(nb)
        flops += float((k + 1) * (k + 1))
        ops += float(k * k + k)
        if ops > budget:
            return "amg", ops, cyc, None
        for u in nb:
            au = adj[u]
            au.discard(v)
            for w in nb:
                if w != u and w not in au:
                    au.add(w)
            deg[u] = len(au)
            heapq.heappush(heap, (deg[u], u))
    if flops > budget:
        return "amg", ops, cyc, flops
    return "elim", ops, cyc, flops


# ==========================================================  S O L V E R ====

class Region:
    """Active set S with an incrementally assembled local matrix and the
    kinetic-gate accumulators on the boundary."""

    def __init__(self, model, led):
        self.m = model
        self.led = led
        self.loc = {}          # global -> local
        self.glob = []         # local -> global
        self.nbrs = []         # induced adjacency, local indices (sets)
        self.vals = []         # dict local->Q value (offdiag), local indices
        self.inB = {}          # global boundary vertex -> P_j accumulator
        self.est = {}          # predicted gate value of a boundary vertex
        self.volS = 0.0
        self.crossdeg = 0.0    # sum_{i in S} |N(i)\S|  (gate push width)

    def admit(self, g, est_child=0.0, newq=None):
        """Admit global vertex g.  Charges the first-exposure scan d_g, the
        O(1) accumulator initialisation of every newly discovered boundary
        vertex, and the materialisation of the new matrix row."""
        m, led = self.m, self.led
        led.scan1(g)                           # C_adj += d_g (first exposure)
        led.inS[g] = True
        i = len(self.glob)
        self.loc[g] = i
        self.glob.append(g)
        self.nbrs.append(set())
        self.vals.append({})
        self.volS += float(m.d[g])
        self.inB.pop(g, None)
        self.est.pop(g, None)
        a = (1.0 - m.alpha) / 2.0
        nb = m.indices[m.indptr[g]:m.indptr[g + 1]]
        newb = 0
        for h in nb:
            h = int(h)
            j = self.loc.get(h)
            if j is not None:
                q = -a / (m.sqd[g] * m.sqd[h])
                self.nbrs[i].add(j)
                self.nbrs[j].add(i)
                self.vals[i][j] = q
                self.vals[j][i] = q
                self.crossdeg -= 1.0            # h no longer a cross edge
            else:
                self.crossdeg += 1.0
                if h not in self.inB:
                    self.inB[h] = 0.0
                    # PREDICTED gate value one hop out (a kinetic estimate:
                    # the true value of a just-exposed vertex is identically
                    # zero, because its only S-neighbour still has x = 0).
                    self.est[h] = est_child
                    if newq is not None:
                        newq.append((-est_child, int(h)))
                    newb += 1
        led.ctl(float(newb), "gate")            # O(1) accumulator init  (P3)
        led.mat(float(m.d[g]))                  # materialise the row
        return i

    def matrix(self):
        m = self.m
        n = len(self.glob)
        c = (1.0 + m.alpha) / 2.0
        indptr = np.zeros(n + 1, np.int64)
        cnt = np.array([len(v) + 1 for v in self.vals], np.int64)
        np.cumsum(cnt, out=indptr[1:])
        idx = np.empty(int(indptr[-1]), np.int64)
        dat = np.empty(int(indptr[-1]), float)
        for i in range(n):
            s = indptr[i]
            ks = list(self.vals[i].items())
            idx[s] = i
            dat[s] = c
            for t, (j, q) in enumerate(ks):
                idx[s + 1 + t] = j
                dat[s + 1 + t] = q
        return sp.csr_matrix((dat, idx, indptr), shape=(n, n))


def composed_solve(model, eps, led, gate="push", kappa=8.0, g_batch=1.5,
                   g_tri=4.0, batch=True, max_rounds=400, wall_cap=60.0,
                   amg_cycles=30, x_exact=None, force=None, verbose=False):
    """The composed solver.  gate='push' = kinetic gate (I3-B); gate='pull'
    = same trajectory, boundary residuals recomputed by scanning each
    boundary vertex's adjacency (the classical rescan) -- the exact A/B."""
    m = model
    alpha = m.alpha
    target = alpha * eps
    R = Region(m, led)
    R.admit(m.seed)
    x = np.zeros(0)
    route = None
    tri_vol = 0.0                # vol(S) at the last triage
    solve_vol = 0.0              # vol(S) at the last solve
    rounds = 0
    flips = 0
    hist = []
    t0 = time.perf_counter()
    fac_cells = 0.0
    status = "maxed"
    routes = []
    tri_ops_tot = 0.0
    levels = None
    cur_x = None
    while rounds < max_rounds:
        if time.perf_counter() - t0 > wall_cap:
            status = "cap"
            break
        rounds += 1
        nS = len(R.glob)
        # ---------------- (ii) TRIAGE, on a volume ladder ------------------
        if force is not None:
            new_route, tri_ops, cyc, fill = force, 1.0, -1, None
            led.ctl(1.0, "triage")
        elif route is None or R.volS >= g_tri * tri_vol:
            new_route, tri_ops, cyc, fill = triage(R.nbrs, R.volS, kappa)
            led.ctl(tri_ops, "triage")
            tri_ops_tot += tri_ops
            tri_vol = R.volS
        else:
            led.ctl(1.0, "triage")           # ladder test only
            new_route, tri_ops, cyc, fill = route, 1.0, -1, None
        if route is not None and new_route != route:
            flips += 1
            # DISCARD of accumulated response state: the factor / hierarchy
            # built for the old mechanism is worthless to the new one.
            led.switch_writeoff(fac_cells)
            fac_cells = 0.0
            levels = None
        route = new_route
        routes.append(route)
        # ---------------- interior solve -----------------------------------
        AS = R.matrix()
        led.mat(float(AS.nnz))
        bS = np.zeros(nS)
        if m.seed in R.loc:
            bS[R.loc[m.seed]] = m.b[m.seed]
        xS = np.zeros(nS)
        if cur_x is not None:
            xS[:cur_x.size] = cur_x           # nested-iteration warm start
            led.rec(float(cur_x.size))
        if route == "elim":
            try:
                lu = spla.splu(AS.tocsc(), permc_spec="MMD_AT_PLUS_A",
                               diag_pivot_thresh=0.0,
                               options=dict(SymmetricMode=True))
            except Exception:
                status = "fail"
                break
            Lm = lu.L.tocsc()
            cnts = np.diff(Lm.indptr).astype(float)
            led.resp(float(np.sum(cnts ** 2)))              # factor flops
            fac_cells = float(Lm.nnz + lu.U.nnz)
            led.temp(fac_cells)
            xS = lu.solve(bS)
            led.resp(2.0 * fac_cells)                        # triangular solves
            c_in = 0.0
            led.rec(float(AS.nnz))                           # residual SpMV
            rin = bS - AS @ xS
            c_in = float(np.max(np.abs(rin) / m.sqd[R.glob])) if nS else 0.0
        else:
            led.phase("setup")
            volS = R.volS

            def level0_scan(k, _idx=np.array(R.glob)):
                for _ in range(int(round(k))):
                    led.scan_idx(_idx)

            Bt = m.sqd[np.array(R.glob)].copy()
            levels, linfo = build_hierarchy(AS, Bt, led, level0_scan,
                                            rho0=2.0 / (1.0 + alpha),
                                            vol0=volS)
            fac_cells = float(sum(l["nnz"] for l in levels))
            led.temp(fac_cells)
            led.phase("solve")
            c_in = math.inf
            best = math.inf
            stall = 0
            Bg0 = np.fromiter(R.inB.keys(), np.int64, len(R.inB))
            Xb0 = (m.Q[Bg0][:, np.array(R.glob)].tocsr() if Bg0.size
                   else None)
            for cy in range(amg_cycles):
                v_cycle(levels, 0, xS, bS, led, level0_scan)
                level0_scan(1)
                rin = bS - AS @ xS
                led.rec(float(nS))
                c_in = float(np.max(np.abs(rin) / m.sqd[R.glob]))
                if c_in < 0.5 * target:
                    break
                # EARLY REGION REJECTION, driven by the gate: the boundary
                # residual is a floor no further V-cycling can lower, and the
                # gate reads it for free (one accumulator sweep, no boundary
                # adjacency scan).  If it already exceeds the target, stop and
                # grow instead of polishing an interior that cannot certify.
                if cy >= 2 and Xb0 is not None:
                    led.ctl(float(R.crossdeg), "gate")
                    led.piggy += float(R.crossdeg)
                    cb0 = float(np.max(np.abs(np.asarray(Xb0 @ xS).ravel())
                                       / m.sqd[Bg0]))
                    led.ctl(float(Bg0.size), "cert")
                    if cb0 >= target:
                        break
                if c_in < 0.6 * best:
                    best = c_in
                    stall = 0
                else:
                    stall += 1
                    if stall >= 2:
                        break
        cur_x = xS.copy()
        led.persist(float(3 * nS + AS.nnz + len(R.inB)))
        # ---------------- (i) KINETIC GATE on the boundary -----------------
        Bg = np.fromiter(R.inB.keys(), np.int64, len(R.inB))
        if Bg.size:
            Xb = m.Q[Bg][:, np.array(R.glob)].tocsr()
            pv = np.asarray(Xb @ xS).ravel()
            rb = -pv                            # b_j = 0 for every j not seed
            if gate == "push":
                # PUSH: one accumulator update per cross edge, inside the
                # interior row scan the solver already paid for  (I3-B P1/P2).
                led.ctl(float(R.crossdeg), "gate")
                led.piggy += float(R.crossdeg)
            else:
                # PULL: rescan every boundary vertex's adjacency list.
                led.scan_idx(Bg)
            gv = np.abs(rb) / m.sqd[Bg]
            led.ctl(float(Bg.size), "cert")     # O(1) threshold test each
            c_bd = float(gv.max())
        else:
            gv = np.zeros(0)
            c_bd = 0.0
        led.ctl(float(nS), "cert")              # interior max-reduction
        cert = max(c_in, c_bd)
        hist.append(dict(rd=rounds, route=route, nS=nS, volS=R.volS,
                         cert=cert, c_in=c_in, c_bd=c_bd, cyc=cyc,
                         fill=fill, W=led.W()))
        if verbose:
            print(f"      rd{rounds:3d} {route:5s} nS={nS:7d} vol={R.volS:9.0f} "
                  f"cert={cert:.3e}/{target:.3e} cyc={cyc}")
        if cert < target:
            status = "cert"
            break
        # ---------------- admission -----------------------------------------
        sel = gv > target
        viol = Bg[sel] if Bg.size else np.zeros(0, np.int64)
        if viol.size == 0:
            status = "stuck"
            break
        gvv = gv[sel]
        for t in np.argsort(-gvv):
            R.est[int(viol[t])] = float(gvv[t])
        ca = (1.0 - alpha) / (1.0 + alpha)       # per-hop gate decay
        # the closure queue is seeded with EVERY current boundary vertex,
        # keyed by its measured gate value (free: the gate just read them all)
        newq = [(-float(gv[t]), int(Bg[t])) for t in range(Bg.size)]
        led.ctl(float(Bg.size), "gate")
        for t in np.argsort(-gvv):
            R.admit(int(viol[t]), est_child=ca * float(gvv[t]), newq=newq)
        if batch:
            # GEOMETRIC BATCHING IN THE GATE'S OWN DIRECTION.  Keep admitting
            # the frontier vertices of highest PREDICTED gate until vol(S) has
            # grown by g_batch since the last solve, and never spend more than
            # (g_batch-1)*vol on this closure -- so a single huge hub can
            # never be dragged in by batching alone (decoy_hub).
            budget = (g_batch - 1.0) * max(solve_vol, 1.0)
            spent = 0.0
            heapq.heapify(newq)
            led.ctl(float(len(newq)), "gate")
            while newq and R.volS < g_batch * max(solve_vol, 1.0):
                e, h = heapq.heappop(newq)
                led.ctl(math.log2(len(newq) + 2), "gate")
                if h in R.loc:
                    continue
                dj = float(m.d[h])
                if spent + dj > budget:
                    break
                R.admit(h, est_child=-e * ca, newq=newq)
                spent += dj
        solve_vol = R.volS
    # ---------------- output ------------------------------------------------
    xg = np.zeros(m.n)
    if cur_x is not None and len(R.glob):
        xg[np.array(R.glob)] = cur_x
    nz = int(np.count_nonzero(xg))
    led.emit(float(nz))
    return dict(x=xg, status=status, rounds=rounds, flips=flips,
                routes=routes, hist=hist, nS=len(R.glob), volS=R.volS,
                cert=hist[-1]["cert"] if hist else math.inf,
                tri_ops=tri_ops_tot, nB=len(R.inB),
                wall=time.perf_counter() - t0)


# ===================================================  W Y - S T Y L E  =======

def wy_active(model, eps, led, max_sweeps=400000, wall_cap=25.0,
              g_batch=1.5):
    """WY-style simple active set: grow an active set, solve the interior by
    monotone damped-Jacobi (push-equivalent, unaccelerated) sweeps, find the
    boundary by PULLING (scanning each boundary vertex).  Same certificate."""
    m = model
    alpha = m.alpha
    target = alpha * eps
    R = Region(m, led)
    R.admit(m.seed)
    om = 2.0 / (1.0 + alpha)      # D_Q^{-1}, diag(Q) = (1+alpha)/2
    xS = np.zeros(1)
    t0 = time.perf_counter()
    sweeps = 0
    rounds = 0
    status = "maxed"
    solve_vol = 0.0
    while rounds < 400:
        rounds += 1
        if time.perf_counter() - t0 > wall_cap or sweeps > max_sweeps:
            status = "cap"
            break
        nS = len(R.glob)
        AS = R.matrix()
        led.mat(float(AS.nnz))
        bS = np.zeros(nS)
        if m.seed in R.loc:
            bS[R.loc[m.seed]] = m.b[m.seed]
        y = np.zeros(nS)
        y[:xS.size] = xS
        led.rec(float(xS.size))
        idxS = np.array(R.glob)
        sq = m.sqd[idxS]
        for _ in range(max_sweeps):
            led.scan_idx(idxS)                    # R_int: one row pass
            r = bS - AS @ y
            led.rec(float(nS))
            sweeps += 1
            c_in = float(np.max(np.abs(r) / sq))
            if c_in < 0.5 * target:
                break
            y += om * r
            led.rec(float(nS))
            if sweeps > max_sweeps or time.perf_counter() - t0 > wall_cap:
                break
        xS = y
        Bg = np.fromiter(R.inB.keys(), np.int64, len(R.inB))
        if Bg.size:
            led.scan_idx(Bg)                      # PULL the boundary
            Xb = m.Q[Bg][:, idxS].tocsr()
            gv = np.abs(np.asarray(Xb @ xS).ravel()) / m.sqd[Bg]
            led.ctl(float(Bg.size), "cert")
            c_bd = float(gv.max())
        else:
            gv = np.zeros(0)
            c_bd = 0.0
        led.ctl(float(nS), "cert")
        led.persist(float(3 * nS + AS.nnz + len(R.inB)))
        if max(c_in, c_bd) < target:
            status = "cert"
            break
        viol = Bg[gv > target] if Bg.size else np.zeros(0, np.int64)
        if viol.size == 0:
            status = "stuck"
            break
        for j in viol[np.argsort(-gv[gv > target])]:
            R.admit(int(j))
        budget = (g_batch - 1.0) * max(solve_vol, R.volS / g_batch)
        spent = 0.0
        while R.volS < g_batch * max(solve_vol, 1e-9) and spent < budget:
            Bg2 = np.fromiter(R.inB.keys(), np.int64, len(R.inB))
            if Bg2.size == 0:
                break
            led.scan_idx(Bg2)
            Xb2 = m.Q[Bg2][:, np.array(R.glob)].tocsr()
            gv2 = np.abs(np.asarray(Xb2 @ np.concatenate(
                [xS, np.zeros(len(R.glob) - xS.size)])).ravel()) / m.sqd[Bg2]
            k = int(np.argmax(gv2))
            dj = float(m.d[Bg2[k]])
            if gv2[k] <= 0 or spent + dj > budget:
                break
            R.admit(int(Bg2[k]))
            spent += dj
        solve_vol = R.volS
    xg = np.zeros(m.n)
    if len(R.glob):
        xg[np.array(R.glob)] = xS
    led.emit(float(np.count_nonzero(xg)))
    return dict(x=xg, status=status, rounds=rounds, sweeps=sweeps,
                nS=len(R.glob), volS=R.volS, wall=time.perf_counter() - t0)
