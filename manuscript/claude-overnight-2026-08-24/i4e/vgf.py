"""I4-E  VALUE-GUIDED region growth + incremental factorisation  (SP2).

The one mechanism the campaign lacked: a region rule that admits a vertex
only when its CERTIFIED VALUE lower bound is large (never merely because it
is adjacent), driving an inner solver whose cycle count is alpha-free.

Charging: identical conventions to i3a_amg/amglib.py (VecMeter).
  * admitting v            -> scan_idx([v])   (charges d_v, first exposure)
  * refresh sweep of S     -> scan_idx(S)     (charges vol(S), repeat R_adj)
  * degree query of a ring vertex (Lemma D of I4-D) -> resp(1)
  * factorisation          -> resp(sum col_cnt^2), mat(nnz(L)+nnz(U))
  * triangular solve       -> resp(2*(nnzL+nnzU))
  * heap operation         -> resp(ceil(log2(size+2)))
  * accumulator arithmetic -> rec(1) per pushed edge / per ring test

THE INVARIANT that makes it output-bounded (Lemma V1, see findings):
  ulb[w] <= u_w for every w, at every instant, and a vertex is CERTIFIED-
  admitted only when  Lo(h) = c_a/d_h * sum_{w in S, w~h} ulb[w] >= gate.
  Since Lo(h) <= u_h, every certified-admitted vertex has u_h >= gate,
  hence  vol(S_cert) <= vol({v : u_v >= gate}) < 1/gate   (I4-D Lemma A).
"""
import heapq
import math
import sys
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
from amglib import VecMeter, GModel, _nbrs, build_hierarchy, v_cycle  # noqa


class DQMeter(VecMeter):
    """Lemma D ring: a boundary vertex costs ONE degree query, not d_h."""

    def ring_scan(self, idx):
        k = len(idx)
        if k:
            self.C_resp += float(k)
            self.solve += float(k)


def _lg(k):
    return math.ceil(math.log2(k + 2.0))


def _forest_order(Qc, root=0):
    """If the region induced by Q[S,S] (CSC/CSR, local indices) is a FOREST,
    return (order, parent, pw) rooted at `root`; else None.  O(nnz)."""
    m = Qc.shape[0]
    A = Qc.tocsr()
    ip, ii, dv = A.indptr, A.indices, A.data
    if A.nnz - m > 2 * (m - 1):
        return None
    parent = np.full(m, -1, np.int64)
    pw = np.zeros(m)
    order = np.empty(m, np.int64)
    seen = np.zeros(m, bool)
    k = 0
    for start in range(m):
        s0 = root if start == 0 else start
        if seen[s0]:
            continue
        seen[s0] = True
        order[k] = s0
        k += 1
        head = k - 1
        while head < k:
            v = order[head]
            head += 1
            for t in range(ip[v], ip[v + 1]):
                w = ii[t]
                if w == v:
                    continue
                if seen[w]:
                    if w != parent[v]:
                        return None          # a cycle: not a forest
                    continue
                seen[w] = True
                parent[w] = v
                pw[w] = dv[t]
                order[k] = w
                k += 1
    if k != m:
        return None
    return order, parent, pw


def _region_solve(Qc, rhs, meter, kappa, allow_amg, sqd_S, alpha, tgt,
                  volS, scan0, root=0):
    """Exact solve of Qc x = rhs, charged.  Three routes, chosen by a charged
    O(nnz) structural test:  FOREST -> HSEG-LDL two-pass (I2-B), cost O(|S|);
    low fill -> sparse LDL with MMD; high fill -> SA-AMG on the region."""
    m = Qc.shape[0]
    meter.rec(float(Qc.nnz))                    # structural test
    fo = _forest_order(Qc, root) if m > 1 else None
    if fo is not None:
        order, parent, pw = fo
        A = Qc.tocsr()
        diag = A.diagonal().astype(float).copy()
        f = np.asarray(rhs, float).copy()
        for i in range(m - 1, 0, -1):           # UP pass (eliminate leaves)
            v = order[i]
            p = parent[v]
            if p < 0:
                continue
            c = pw[v] / diag[v]
            diag[p] -= c * pw[v]
            f[p] -= c * f[v]
        meter.resp(4.0 * m)
        x = np.zeros(m)
        for i in range(m):                      # DOWN pass
            v = order[i]
            p = parent[v]
            x[v] = (f[v] - (pw[v] * x[p] if p >= 0 else 0.0)) / diag[v]
        meter.resp(3.0 * m)
        return x, "forest", float(2 * m)
    lu = spla.splu(Qc.tocsc(), permc_spec="MMD_AT_PLUS_A",
                   diag_pivot_thresh=0.0, options=dict(SymmetricMode=True))
    Lm = lu.L.tocsc()
    cnt = np.diff(Lm.indptr).astype(float)
    fac = float(np.sum(cnt ** 2))
    nnzLU = float(Lm.nnz + lu.U.nnz)
    if allow_amg and fac > kappa * float(Qc.nnz) and m > 200:
        meter.rec(float(m))                     # the fill estimate itself
        meter.phase("setup")
        AS = Qc.tocsr()
        lev, _li = build_hierarchy(AS, sqd_S.copy(), meter, scan0,
                                   rho0=2.0 / (1.0 + alpha), vol0=volS)
        meter.phase("solve")
        x = np.zeros(m)
        for _c in range(60):
            v_cycle(lev, 0, x, rhs, meter, scan0)
            scan0(1)
            if float(np.max(np.abs(rhs - AS @ x) / sqd_S)) < 0.05 * tgt:
                break
        return x, "amg", 0.0
    meter.resp(fac)
    meter.mat(nnzLU)
    x = lu.solve(rhs)
    meter.resp(2.0 * nnzLU)
    return x, "ldl", nnzLU


def vgf_local(model, eps, meter, growth=3.0, gate_mode="sound", spec=True,
              x_exact=None, oracle=False, max_rounds=400, wall_cap=60.0,
              max_nnz=3.0e7, inner="auto", fill_kappa=25.0,
              spec_theta=0.1, ext_solve=True, verbose=False):
    """Value-Guided incremental Factorisation.

    gate_mode: 'sound'  -> gate = gamma*eps   (repository certificate, sound)
               'opt'    -> gate = eps         (semantic gate; heuristic, the
                                               same optimism literal push uses)
    spec:      allow value-ordered speculative admission up to the round's
               volume budget (keeps the round count O(log_growth vol)).
    oracle:    stop on the TRUE semantic error (mechanism-cost lower bound).
    """
    n = model.n
    d = model.d
    sqd = model.sqd
    Q = model.Q
    b = model.b
    ip, ii = model.indptr, model.indices
    alpha = model.alpha
    c_a = (1.0 - alpha) / (1.0 + alpha)
    gam = 2.0 * alpha / (1.0 + alpha)
    gate = (gam * eps) if gate_mode == "sound" else eps
    spec_floor = spec_theta * gate
    target = alpha * eps                      # ||D^-1/2 (Qx-b)||_inf target

    inS = np.zeros(n, bool)
    ulb = np.zeros(n)
    Slist = [model.seed]
    inS[model.seed] = True
    meter.scan_idx(np.array([model.seed]))
    volS = float(d[model.seed])
    cert_vol = float(d[model.seed])           # volume of CERTIFIED admissions
    xg = np.zeros(n)
    t0 = time.perf_counter()
    rounds = 0
    nfac = 0
    fill_tot = 0.0
    status = "maxed"
    last = dict(cert=math.inf, volS=volS, nS=1, rounds=0)
    hier = None

    while rounds < max_rounds:
        if time.perf_counter() - t0 > wall_cap:
            status = "cap"
            break
        rounds += 1
        S = np.asarray(Slist, dtype=np.int64)

        # ---------------- (1) EXACT SOLVE on the admitted region ----------
        meter.scan_idx(S)                      # assemble Q[S,S]
        QS = Q[S][:, S].tocsc()

        def scan0(k, _S=S):
            for _ in range(int(round(k))):
                meter.scan_idx(_S)
        try:
            xS, route, fill_tot = _region_solve(
                QS, b[S], meter, fill_kappa, inner in ("auto", "amg"),
                sqd[S], alpha, target, volS, scan0,
                root=int(np.flatnonzero(S == model.seed)[0]))
        except Exception:
            return dict(x=xg, status="fail", **last)
        nfac += 1
        if fill_tot > max_nnz:
            status = "cap"
            xg[:] = 0.0
            xg[S] = xS
            break
        xg[:] = 0.0
        xg[S] = xS
        ulb[S] = np.maximum(ulb[S], xS / sqd[S])
        rin = b[S] - QS @ xS
        meter.rec(float(S.size))
        c_in = float(np.max(np.abs(rin) / sqd[S]))

        # ---------------- (2) RING REFRESH (one push sweep out of S) ------
        # The sweep re-uses the SAME adjacency read that assembled Q[S,S]
        # above (one read of row i yields both its matrix entries and its
        # push into the ring), so it is not charged a second time.
        nb = _nbrs(model, S)
        src = np.repeat(S, (ip[S + 1] - ip[S]).astype(np.int64))
        out = ~inS[nb]
        rnb, rsrc = nb[out], src[out]
        meter.rec(float(rnb.size))
        if rnb.size:
            accv = np.bincount(rnb, weights=ulb[rsrc], minlength=n)
            ring = np.unique(rnb)
            meter.resp(float(ring.size))       # Lemma D degree queries
            meter.rec(float(ring.size))
            Lo = c_a * accv[ring] / d[ring]
            nu = float(Lo.max())
        else:
            ring = np.empty(0, np.int64)
            Lo = np.empty(0)
            nu = 0.0
            accv = np.zeros(n)
        cert = max(c_in, 0.5 * (1.0 + alpha) * nu)
        semerr = (float(np.max(np.abs(xg - x_exact) / sqd))
                  if x_exact is not None else math.inf)
        last = dict(cert=cert, volS=volS, nS=int(S.size), rounds=rounds,
                    cert_vol=cert_vol, nfac=nfac, fill=fill_tot,
                    nu_over_gate=(nu / gate if gate else math.inf),
                    semerr=semerr)
        ok = (semerr <= eps) if oracle else (nu < gate and c_in < target)
        if ok:
            status = "cert"
            break
        if ring.size == 0:
            status = "exhausted"
            break

        # ---------------- (3) VALUE-GUIDED ADMISSION ----------------------
        budget = growth * volS
        acc = {}
        hp = []
        # Seed the priority queue with the CANDIDATES only (violators + the
        # top speculative band), selected in O(|ring|) by a threshold test --
        # not by sorting the whole ring.  I3-B's kinetic gate keeps the rest
        # of the ring out of the queue entirely.
        cand = np.flatnonzero(Lo >= spec_floor)
        meter.rec(float(ring.size))
        for j in cand:
            v = int(ring[j])
            acc[v] = float(accv[v])
            heapq.heappush(hp, (-float(Lo[j]), v))
        meter.resp(float(cand.size) * _lg(cand.size))
        admitted = 0
        newN = []
        while True:
            while hp:
                if volS >= budget and admitted:
                    break
                negLo, v = heapq.heappop(hp)
                meter.resp(_lg(len(hp) + 1))
                if inS[v]:
                    continue
                cur = c_a * acc[v] / d[v]
                if -negLo < cur - 1e-15 * max(cur, 1e-300):
                    continue                    # outdated duplicate
                isviol = cur >= gate
                if (not isviol) and (not spec):
                    break
                if not isviol:
                    # SPECULATION RULE.  Value-guided, floored and budgeted:
                    #   (i) never below theta*gate -> region <= S_{theta*gate}
                    #   (ii) never past the round's volume budget
                    if cur < spec_floor:
                        break                   # heap is ordered by value
                    if d[v] > budget - volS:
                        continue
                # a genuine violator is ALWAYS admitted (it lies inside
                # S_gate, so its volume is charged to the output bound)
                meter.scan_idx(np.array([v]))
                inS[v] = True
                Slist.append(v)
                newN.append(v)
                volS += float(d[v])
                ulb[v] = max(ulb[v], cur)
                if isviol:
                    cert_vol += float(d[v])
                admitted += 1
                nbv = ii[ip[v]:ip[v + 1]]
                meter.rec(float(nbv.size))
                for y in nbv:
                    y = int(y)
                    if inS[y]:
                        continue
                    if y not in acc:
                        acc[y] = 0.0
                        meter.resp(1.0)         # degree query, new ring vertex
                    acc[y] += ulb[v]
                    ny = -c_a * acc[y] / d[y]
                    if ny <= -spec_floor:
                        heapq.heappush(hp, (ny, y))
                        meter.resp(_lg(len(hp)))
            # ---- (3b) EXTENSION SOLVE: exact solve on the NEW vertices only,
            # with the already-solved region frozen as Dirichlet data.  This
            # is the incremental factorisation step: admitted volume is never
            # re-solved, and the resulting values are still LOWER bounds on u
            # (frozen data is itself a lower bound), so admission stays sound.
            if (not newN) or volS >= budget or not ext_solve:
                break
            N = np.asarray(newN, dtype=np.int64)
            newN = []
            QNall = Q[N]
            rhsN = b[N] - QNall @ xg
            meter.rec(float(QNall.nnz))
            QN = QNall[:, N].tocsc()

            def scan0N(k, _N=N):
                for _ in range(int(round(k))):
                    meter.scan_idx(_N)
            try:
                xN, _rt, _fl = _region_solve(
                    QN, rhsN, meter, fill_kappa, inner in ("auto", "amg"),
                    sqd[N], alpha, target, float(d[N].sum()), scan0N, root=0)
            except Exception:
                break
            newu = np.maximum(ulb[N], xN / sqd[N])
            delta = newu - ulb[N]
            ulb[N] = newu
            xg[N] = np.maximum(xg[N], xN)
            moved = N[delta > 0]
            if moved.size == 0:
                break
            # propagate the lift to the ring accumulators (piggyback push)
            for v, dv in zip(moved.tolist(), delta[delta > 0].tolist()):
                nbv = ii[ip[v]:ip[v + 1]]
                meter.rec(float(nbv.size))
                for y in nbv:
                    y = int(y)
                    if inS[y]:
                        continue
                    if y not in acc:
                        acc[y] = 0.0
                        meter.resp(1.0)
                    acc[y] += dv
                    ny = -c_a * acc[y] / d[y]
                    if ny <= -spec_floor:
                        heapq.heappush(hp, (ny, y))
                        meter.resp(_lg(len(hp)))
            if not hp:
                break
        if admitted == 0:
            # progress guarantee: force the top violator in, whatever it costs
            j = int(np.argmax(Lo))
            v = int(ring[j])
            if Lo[j] < gate:
                status = "stalled"
                break
            meter.scan_idx(np.array([v]))
            inS[v] = True
            Slist.append(v)
            volS += float(d[v])
            ulb[v] = max(ulb[v], float(Lo[j]))
            cert_vol += float(d[v])
        if verbose:
            print(f"   r={rounds} |S|={len(Slist)} vol={volS:.0f} "
                  f"cert_vol={cert_vol:.0f} nu/gate={nu/gate:.3g} "
                  f"cert={cert:.3e} tgt={target:.3e} W={meter.total():.4g}")
    return dict(x=xg, status=status, **last)


# ----------------------------------------------------------------- helpers
def out_measure(model, eps, x0=None):
    if x0 is None:
        x0 = model.solve_exact()
    u = x0 * model.sqd / model.d
    S = np.flatnonzero(u > eps)
    volS = float(model.d[S].sum())
    if S.size:
        nb = np.unique(_nbrs(model, S))
        inS = np.zeros(model.n, bool)
        inS[S] = True
        B = nb[~inS[nb]]
    else:
        B = np.empty(0, np.int64)
    return dict(nS=int(S.size), volS=volS, nB=int(B.size),
                volB=float(model.d[B].sum()), u=u, Sset=S)
