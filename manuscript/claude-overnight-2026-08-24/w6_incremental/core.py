"""W6 — warm-started / incremental active-set solving for local PPR.

Outer loop (unregularized ACL eps target, Wei--Yang style batch admission):
  S_0 = supp(s).  Solve Q_SS x_S = b_S.  Boundary residual at w in N(S)\\S:
      r_w = b_w - (Q x)_w = beta * sum_{u in S~w} x_u / (sqd_u sqd_w),  beta=(1-alpha)/2
  Admission gate:  r_w / sqd_w >= GAMMA * alpha * eps   (GAMMA=0.5)
  Inner solves to scaled-inf residual <= TOL_IN * alpha * eps  (TOL_IN=0.10)
  => on termination  ||D^{-1/2}(Q x - b)||_inf <= max(TOL_IN, GAMMA)*alpha*eps
     < alpha*eps, which certifies semantic error < eps.  Asserted every run
     against Model.solve_exact.

Backends (all replay the SAME exact trace; each has its own Meter):
  COLD-LU     fresh scipy splu per round; charge C_resp += nnz(L)+nnz(U)
              (stated proxy for factor+solve flops), C_mat += |S| per round.
  CG-COLD     CG from x0=0 per round; charge (nnz(Q_SS)+6|S|) per iteration.
              (diag(Q) is the constant (1+alpha)/2, so Jacobi = identity.)
  CG-WARM     CG warm-started from previous round's own iterate (zero-padded).
  INC-LDL     incremental up-looking LDL^T in ADMISSION order.  Appending a
              vertex touches only the sparse-triangular-solve reach of its
              admitted neighbours (charged per touched nonzero); forward solve
              z is append-only; the per-round gate does a partial backward
              solve on the reverse closure D(F) of the frontier (charged).
              On endpoint paths this IS the note's Thm 7 recurrence.
  ORACLE-SDD  idealized nearly-linear solver: per round charge
              cvol(S_t)*plog(cvol(S_t)) + per-round boundary rescans.
  ORACLE-INC  conj:aggregate ideal: plog(cvol(S*)) * (cvol(S*) +
              cvol(boundary-ever \\ S*) + E)  -- each vertex/edge and boundary
              key charged once, polylog amortization.
  plog(x) = log2(2+x).

Outer ledger charged identically to every non-oracle backend: admission scan
of each new vertex (C_adj, first exposure), per-round rescan of the frontier
adjacency (R_adj repeats) + C_rec per boundary-edge residual op.
"""
import sys, time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

sys.path.insert(0, '/home/claude/work/overnight/lib')
from model import Model, vol
from meter import Meter

GAMMA = 0.5
TOL_IN = 0.10
CG_CAP = 20000


def cvol(adj, U):
    return sum(1 + len(adj[u]) for u in U)


def plog(x):
    return np.log2(2.0 + x)


# ---------------------------------------------------------------- trace

def grow_trace(model, eps, keep_Q=True):
    """Grow the active set with exact per-round solves. Returns trace dict."""
    adj, alpha = model.adj, model.alpha
    beta = (1 - alpha) / 2.0
    sqd = model.sqd
    thr = GAMMA * alpha * eps
    seed_supp = [int(v) for v in np.nonzero(model.s)[0]]
    pos, order = {}, []
    S = set()
    out = {}
    frontier = set()

    def admit(v):
        pos[v] = len(order); order.append(v); S.add(v)
        cnt = 0
        for w in adj[v]:
            if w in S:
                out[w] -= 1
                if out[w] == 0:
                    frontier.discard(w)
            else:
                cnt += 1
        out[v] = cnt
        if cnt > 0:
            frontier.add(v)

    for v in seed_supp:
        admit(v)

    rounds = []
    while True:
        idx = np.array(order)
        Qs = model.Q[idx][:, idx].tocsc()
        bS = model.b[idx]
        if len(order) == 1:
            x = bS / Qs[0, 0]
            nnzLU = 1
        else:
            lu = spla.splu(Qs)
            x = lu.solve(bS)
            nnzLU = int(lu.L.nnz + lu.U.nnz)
        F = sorted(frontier)
        rb = {}
        bedges = 0
        for u in F:
            xu = x[pos[u]]
            for w in adj[u]:
                if w not in S:
                    bedges += 1
                    rb[w] = rb.get(w, 0.0) + beta * xu / (sqd[u] * sqd[w])
        viol = sorted(w for w, r in rb.items() if r / sqd[w] >= thr)
        rounds.append(dict(
            n=len(order), F=list(F), T=list(viol), x=x.copy(),
            nnzLU=nnzLU, nnzQ=int(Qs.nnz), bedges=bedges,
            Qs=Qs.tocsr() if keep_Q else None,
            bS=bS, volS=int(sum(len(adj[u]) for u in order)),
            ncand=len(rb)))
        if not viol:
            break
        for v in viol:
            admit(v)

    xfull = np.zeros(model.n)
    xfull[np.array(order)] = rounds[-1]['x']
    x0 = getattr(model, '_x0_cache', None)
    if x0 is None:
        x0 = model.solve_exact()
        model._x0_cache = x0
    cert = model.cert_resid(xfull)
    sem = model.semantic_err(xfull, x0)
    assert cert < alpha * eps, (cert, alpha * eps)
    assert sem <= eps, (sem, eps)
    Sset = set(order)
    bound_ever = set()
    for r in rounds:
        for u in r['F']:
            for w in adj[u]:
                if w not in Sset:
                    bound_ever.add(w)
    return dict(order=order, pos=pos, rounds=rounds, x0=x0,
                cert=cert, sem=sem, S=Sset, bound_ever=bound_ever,
                eps=eps, alpha=alpha)


# ---------------------------------------------------------------- outer ledger

def outer_charge(model, trace, meter):
    adj = model.adj
    for v in trace['order']:
        meter.scan(v)                      # admission exposure (C_adj first)
    for r in trace['rounds']:
        for u in r['F']:
            meter.scan(u)                  # per-round boundary rescan (R_adj)
        meter.rec(r['bedges'] + r['ncand'])


# ---------------------------------------------------------------- backends

def replay_cold_lu(model, trace):
    m = Meter(model.adj); outer_charge(model, trace, m)
    for r in trace['rounds']:
        m.resp(r['nnzLU'])
        m.mat(r['n'])
    return dict(meter=m.vector())


def _cg(Q, b, x0, sqd_S, tol_abs, cap=CG_CAP):
    x = x0.copy()
    r = b - Q @ x
    r0s = float(np.max(np.abs(r) / sqd_S))
    if r0s <= tol_abs:
        return x, 0, r0s, False
    p = r.copy()
    rs = float(r @ r)
    it = 0
    while it < cap:
        Ap = Q @ p
        a = rs / float(p @ Ap)
        x += a * p
        r -= a * Ap
        it += 1
        if float(np.max(np.abs(r) / sqd_S)) <= tol_abs:
            return x, it, r0s, False
        rs2 = float(r @ r)
        p = r + (rs2 / rs) * p
        rs = rs2
    return x, it, r0s, True


def replay_cg(model, trace, warm):
    alpha, eps = model.alpha, trace['eps']
    tol = TOL_IN * alpha * eps
    m = Meter(model.adj); outer_charge(model, trace, m)
    idx = np.array(trace['order'])
    sqd_all = model.sqd[idx]
    prev = None
    percall = []
    capped = False
    for t, r in enumerate(trace['rounds']):
        n = r['n']
        Q = r['Qs']
        b = r['bS']
        sqd_S = sqd_all[:n]
        if warm and prev is not None:
            x0 = np.zeros(n); x0[:len(prev)] = prev
        else:
            x0 = np.zeros(n)
        x, it, r0s, cap = _cg(Q, b, x0, sqd_S, tol)
        capped = capped or cap
        m.resp((r['nnzQ'] + 6 * n) * max(it, 1))
        m.mat(n)
        xt = r['x']
        xprev_pad = np.zeros(n)
        if t > 0:
            xp = trace['rounds'][t - 1]['x']
            xprev_pad[:len(xp)] = xp
        rel_inc = float(np.linalg.norm(xt - xprev_pad) /
                        max(np.linalg.norm(xt), 1e-300))
        percall.append((it, r0s, rel_inc))
        prev = x
    # final x must itself satisfy the certificate; if the interior tolerance
    # was too loose for the boundary margin, tighten the FINAL solve only
    # (recharged honestly) and record it.
    retries = 0
    while True:
        xfull = np.zeros(model.n)
        xfull[idx] = prev
        cert = model.cert_resid(xfull)
        sem = model.semantic_err(xfull, trace['x0'])
        if cert < alpha * eps and sem <= eps:
            break
        retries += 1
        assert retries <= 4, ('cg cert', warm, cert, alpha * eps, sem, eps)
        r = trace['rounds'][-1]
        n = r['n']
        tol = tol / 5.0 ** retries
        x, it, r0s, cap = _cg(r['Qs'], r['bS'], prev.copy(),
                              sqd_all[:n], tol)
        m.resp((r['nnzQ'] + 6 * n) * max(it, 1))
        prev = x
    return dict(meter=m.vector(), iters=[p[0] for p in percall],
                r0=[p[1] for p in percall], rel_inc=[p[2] for p in percall],
                capped=capped, cert=float(cert), sem=float(sem))


class IncLDL:
    """Incremental up-looking LDL^T, admission order. Charges touched entries."""
    def __init__(self, model, meter):
        self.mo = model
        self.m = meter
        self.rows = []      # rows[i]: dict j->L_ij  (j<i)
        self.cols = []      # cols[j]: ascending list of i with L_ij != 0
        self.dv = []        # pivots
        self.z = []         # forward solve L z = b
        self.append_cost = []

    def append(self, v, nbr_pos, qdiag, qvals, bval):
        c0 = self.m.C_resp
        mpos = len(self.dv)
        qd = {p: qvals[k] for k, p in enumerate(nbr_pos)}
        # symbolic reach: DFS from nbr_pos along cols edges j -> i (i>j)
        seen = set(nbr_pos)
        stack = list(nbr_pos)
        while stack:
            j = stack.pop()
            for i in self.cols[j]:
                if i not in seen:
                    seen.add(i); stack.append(i)
        reach = sorted(seen)
        y = {}
        for i in reach:
            yi = qd.get(i, 0.0)
            ri = self.rows[i]
            self.m.resp(1 + len(ri))
            for j, lij in ri.items():
                yj = y.get(j)
                if yj is not None:
                    yi -= lij * yj
            y[i] = yi
        row = {}
        dm = qdiag
        zc = bval
        for i, yi in y.items():
            li = yi / self.dv[i]
            if li != 0.0:
                row[i] = li
                self.cols[i].append(mpos)
                dm -= yi * li
                zc -= li * self.z[i]
                self.m.resp(3); self.m.mat(1)
        assert dm > 0
        self.rows.append(row)
        self.cols.append([])
        self.dv.append(dm)
        self.z.append(zc)
        self.m.resp(2); self.m.mat(2)
        self.append_cost.append(self.m.C_resp - c0)

    def gate_x(self, F_pos, charge=True):
        """x at frontier positions via partial backward solve on the reverse
        closure D(F) = closure of F under j -> cols[j]."""
        seen = set(F_pos)
        stack = list(F_pos)
        while stack:
            j = stack.pop()
            for k in self.cols[j]:
                if k not in seen:
                    seen.add(k); stack.append(k)
        D = sorted(seen, reverse=True)
        x = {}
        cost = 0
        for j in D:
            xj = self.z[j] / self.dv[j]
            cost += 1 + len(self.cols[j])
            for k in self.cols[j]:
                xj -= self.rows[k][j] * x[k]
            x[j] = xj
        if charge:
            self.m.resp(cost)
        return x, cost, len(D)

    def finalize(self):
        n = len(self.dv)
        allpos = list(range(n))
        x, cost, _ = self.gate_x(allpos, charge=True)
        self.m.mat(n); self.m.emit(n)
        return np.array([x[j] for j in range(n)])


def replay_inc_ldl(model, trace, cap=3e8):
    alpha, eps = model.alpha, trace['eps']
    m = Meter(model.adj); outer_charge(model, trace, m)
    inc = IncLDL(model, m)
    order, pos = trace['order'], trace['pos']
    adj = model.adj
    Q = model.Q
    gate_costs, gate_D, lazy_costs = [], [], []
    lazy_miss = 0
    admitted = 0
    prevT = None
    verr = 0.0
    for t, r in enumerate(trace['rounds']):
        # append this round's new vertices (round t solves S with n=r['n'])
        while admitted < r['n']:
            v = order[admitted]
            nb = [pos[w] for w in adj[v] if w in pos and pos[w] < admitted]
            qrow = Q[v]
            qd = {}
            for k, w in zip(qrow.indices, qrow.data):
                qd[k] = w
            qvals = [qd[order[p]] for p in nb]
            inc.append(v, nb, qd[v], qvals, model.b[v])
            admitted += 1
        F_pos = [pos[u] for u in r['F']]
        xF, cost, Dsz = inc.gate_x(F_pos)
        gate_costs.append(cost); gate_D.append(Dsz)
        # verify against trace
        xt = r['x']
        if F_pos:
            verr = max(verr, max(abs(xF[p] - xt[p]) for p in F_pos))
        # lazy ledger: frontier near last batch only
        if prevT is None:
            lazy_costs.append(cost)
        else:
            near = set(prevT)
            for v in prevT:
                near.update(adj[v])
            Frec = [p for u, p in zip(r['F'], F_pos) if u in near]
            _, lcost, _ = inc.gate_x(Frec, charge=False) if Frec else ({}, 0, 0)
            lazy_costs.append(lcost)
            # would lazy have found this batch? every admitted vertex needs
            # a violating parent inside Frec
            Sset = trace['S']
            for w in r['T']:
                par = [u for u in adj[w] if u in pos and pos[u] < r['n']]
                if not any(u in near for u in par):
                    lazy_miss += 1
                    break
        prevT = r['T']
        if m.C_resp > cap:
            return dict(capped=True, meter=m.vector())
    xfin = inc.finalize()
    xt = trace['rounds'][-1]['x']
    verr = max(verr, float(np.max(np.abs(xfin - xt))))
    assert verr < 1e-7 * max(1.0, float(np.max(np.abs(xt)))), verr
    xfull = np.zeros(model.n)
    xfull[np.array(order)] = xfin
    cert = model.cert_resid(xfull)
    sem = model.semantic_err(xfull, trace['x0'])
    assert cert < alpha * eps and sem <= eps, (cert, sem)
    # lazy total = per-round local gates + one final full pass + misses*full
    full_final = gate_costs[-1]
    lazy_total = sum(lazy_costs) + full_final + lazy_miss * full_final
    return dict(meter=m.vector(), capped=False,
                append_total=int(sum(inc.append_cost)),
                append_mean=float(np.mean(inc.append_cost)),
                append_max=int(max(inc.append_cost)),
                nnzL=int(sum(len(rw) for rw in inc.rows)),
                gate_total=int(sum(gate_costs)),
                gate_mean=float(np.mean(gate_costs)),
                gate_maxD=int(max(gate_D)),
                lazy_gate_total=int(lazy_total),
                lazy_miss=int(lazy_miss), verr=float(verr))


def is_tree(adj):
    return sum(len(adj[u]) for u in adj) == 2 * (len(adj) - 1)


def replay_tree_inc(model, trace, tol=1e-8):
    """Tree-DP incremental backend (trees only): seed-rooted elimination
    messages delta_u (leaves-first pivots), gains g_u = -Q_{u,p}/delta_u,
    x_u = g_u * x_parent, x_root = b_root / delta_root.  Admission of v under
    parent p: O(1) local init + upward delta-update along the path p->root
    TRUNCATED when the relative pivot change < tol; then downward x-refresh
    from the topmost changed vertex, PRUNED when the relative x change < tol.
    Gate charge: boundary tests only at frontier vertices touched by the
    descent; a round whose admitted batch has a parent that was NOT touched
    forces a charged full pass (counted).  Every charge goes to C_resp;
    stored writes to C_mat.  Verified against the exact trace each round."""
    alpha, eps = model.alpha, trace['eps']
    adj = model.adj
    m = Meter(adj); outer_charge(model, trace, m)
    order, pos = trace['order'], trace['pos']
    Q = model.Q
    beta = (1 - alpha) / 2.0
    sqd = model.sqd
    root = order[0]
    parent, children = {root: None}, {root: []}
    delta, gain, xv, contrib = {}, {}, {}, {}
    delta[root] = float(Q[root, root])
    contrib[root] = {}
    xv[root] = model.b[root] / delta[root]
    m.resp(2); m.mat(2)
    admitted = 1
    stats = dict(up_steps=[], down_steps=[], full_passes=0, touched=[])
    verr = 0.0

    def descend(u):
        """truncated x-refresh below u (u's x already updated); returns
        (#steps, set of touched vertices)."""
        steps = 0
        touched = {u}
        stack = [u]
        while stack:
            w = stack.pop()
            for c in children[w]:
                newx = gain[c] * xv[w]
                steps += 1
                if abs(newx - xv[c]) > tol * max(newx, 1e-300):
                    xv[c] = newx
                    touched.add(c)
                    stack.append(c)
        m.resp(steps); m.mat(len(touched))
        return steps, touched

    depth = {root: 0}
    for t, r in enumerate(trace['rounds']):
        touched_round = set()
        up_r = down_r = 0
        tops = {}
        while admitted < r['n']:
            v = order[admitted]; admitted += 1
            par = [u for u in adj[v] if u in parent]
            assert len(par) == 1
            p = par[0]
            parent[v] = p; children[v] = []; children[p].append(v)
            depth[v] = depth[p] + 1
            delta[v] = float(Q[v, v])
            gain[v] = beta / (sqd[v] * sqd[p]) / delta[v]
            contrib[v] = {}
            xv[v] = gain[v] * xv[p]
            m.resp(4); m.mat(4)
            # upward delta path (truncated)
            c = v
            u = p
            top = v
            while u is not None:
                edge2 = (beta / (sqd[u] * sqd[c])) ** 2
                newc = edge2 / delta[c]
                old = contrib[u].get(c, 0.0)
                nd = delta[u] - (newc - old)
                up_r += 1
                m.resp(3)
                if abs(nd - delta[u]) <= tol * delta[u]:
                    break
                contrib[u][c] = newc
                delta[u] = nd
                if parent[u] is not None:
                    gain[u] = beta / (sqd[u] * sqd[parent[u]]) / delta[u]
                top = u
                c, u = u, parent[u]
                m.mat(2)
            tops[top] = depth[top]
        # ONE downward refresh per round: from each topmost changed vertex,
        # shallowest first (deeper tops prune immediately if already fresh)
        for top in sorted(tops, key=tops.get):
            if top == root or parent[top] is None:
                xv[root] = model.b[root] / delta[root]
                start = root
            else:
                nx = gain[top] * xv[parent[top]]
                if abs(nx - xv[top]) <= tol * max(nx, 1e-300) \
                        and top in touched_round:
                    continue
                xv[top] = nx
                start = top
            m.resp(1)
            ds, tch = descend(start)
            down_r += ds
            touched_round |= tch
        # gate: test boundary neighbours of touched frontier vertices
        Fset = set(r['F'])
        touchedF = [u for u in touched_round if u in Fset]
        m.resp(sum(len(adj[u]) for u in touchedF))
        # coverage: does the next batch's parents lie in touched frontier?
        if r['T']:
            ok = True
            for w in r['T']:
                pars = [u for u in adj[w] if u in parent]
                if not any(u in touched_round for u in pars):
                    ok = False; break
            if not ok or t == 0:
                stats['full_passes'] += 1
                m.resp(sum(len(adj[u]) for u in r['F']) + r['n'])
        else:
            # termination round: one charged full exact pass
            stats['full_passes'] += 1
            m.resp(sum(len(adj[u]) for u in r['F']) + r['n'])
        stats['up_steps'].append(up_r)
        stats['down_steps'].append(down_r)
        stats['touched'].append(len(touched_round))
        # verify frontier x against exact trace
        xt = r['x']
        if r['F']:
            e = max(abs(xv[u] - xt[pos[u]]) /
                    max(abs(xt[pos[u]]), 1e-300) for u in r['F'])
            verr = max(verr, e)
    assert verr < 2e-2, verr   # frontier staleness; decisions replayed exact,
    # final output recomputed exactly and certified below
    # finalize: exact full recompute (charged), then certify
    n = len(order)
    m.resp(2 * n); m.mat(n); m.emit(n)
    return _tree_inc_finish(model, trace, m, stats, verr, parent, children,
                            beta, sqd)


def _tree_inc_finish(model, trace, m, stats, verr, parent, children,
                     beta, sqd):
    """Exact final recompute (uncharged beyond the finalize charge already
    added): rebuild deltas leaves-first, then x root-down; certify."""
    alpha, eps = model.alpha, trace['eps']
    Q = model.Q
    order, pos = trace['order'], trace['pos']
    root = order[0]
    # leaves-first exact deltas via reverse admission order
    dexact = {}
    for v in reversed(order):
        dv = float(Q[v, v])
        for c in children[v]:
            dv -= (beta / (sqd[v] * sqd[c])) ** 2 / dexact[c]
        dexact[v] = dv
    xex = {root: model.b[root] / dexact[root]}
    for v in order[1:]:
        p = parent[v]
        xex[v] = beta / (sqd[v] * sqd[p]) / dexact[v] * xex[p]
    xfin = np.zeros(model.n)
    for v in order:
        xfin[v] = xex[v]
    cert = model.cert_resid(xfin)
    sem = model.semantic_err(xfin, trace['x0'])
    assert cert < alpha * eps and sem <= eps, (cert, sem)
    xt = trace['rounds'][-1]['x']
    fe = float(np.max(np.abs(xfin[np.array(order)] - xt)))
    assert fe < 1e-8 * max(1.0, float(np.max(np.abs(xt)))), fe
    return dict(meter=m.vector(), verr=float(verr),
                up_total=int(np.sum(stats['up_steps'])),
                up_mean=float(np.mean(stats['up_steps'])),
                down_total=int(np.sum(stats['down_steps'])),
                down_mean=float(np.mean(stats['down_steps'])),
                touched_mean=float(np.mean(stats['touched'])),
                full_passes=int(stats['full_passes']))


def oracle_ledgers(model, trace):
    adj = model.adj
    sdd = 0.0
    for r in trace['rounds']:
        cv = sum(1 + len(adj[u]) for u in trace['order'][:r['n']])
        sdd += cv * plog(cv)
        sdd += sum(1 + len(adj[u]) for u in r['F'])       # boundary rescan
    S = trace['S']
    cvS = cvol(adj, S)
    cvB = sum(1 + len(adj[w]) for w in trace['bound_ever'])
    E = sum(1 for r in trace['rounds'] if r['T'])
    inc = plog(cvS) * (cvS + cvB + E)
    return dict(sdd=float(sdd), inc=float(inc))


# ---------------------------------------------------------------- config run

def run_config(model, eps,
               backends=('cold', 'cgc', 'cgw', 'inc', 'tree', 'oracle'),
               sub=400):
    t0 = time.time()
    trace = grow_trace(model, eps)
    adj = model.adj
    rounds = trace['rounds']
    E = sum(1 for r in rounds if r['T'])
    Ts = [len(r['T']) for r in rounds if r['T']]
    rec = dict(
        eps=eps, alpha=model.alpha, n=model.n,
        E=E, nrounds=len(rounds), S=len(trace['S']),
        volS=rounds[-1]['volS'], cvolS=cvol(adj, trace['S']),
        meanT=float(np.mean(Ts)) if Ts else 0.0,
        maxT=int(max(Ts)) if Ts else 0,
        meanF=float(np.mean([len(r['F']) for r in rounds])),
        maxF=int(max(len(r['F']) for r in rounds)),
        sum_volSt=int(sum(r['volS'] for r in rounds)),
        cert=float(trace['cert']), sem=float(trace['sem']),
        backends={})
    B = rec['backends']
    if 'cold' in backends:
        B['COLD-LU'] = replay_cold_lu(model, trace)
    if 'cgc' in backends:
        B['CG-COLD'] = replay_cg(model, trace, warm=False)
    if 'cgw' in backends:
        B['CG-WARM'] = replay_cg(model, trace, warm=True)
    if 'inc' in backends:
        B['INC-LDL'] = replay_inc_ldl(model, trace)
    if 'tree' in backends and is_tree(model.adj):
        B['TREE-INC'] = replay_tree_inc(model, trace)
    if 'oracle' in backends:
        om = Meter(adj); outer_charge(model, trace, om)
        ol = oracle_ledgers(model, trace)
        B['ORACLE-SDD'] = dict(meter=dict(total=ol['sdd']), solve=ol['sdd'])
        B['ORACLE-INC'] = dict(meter=dict(total=ol['inc']), solve=ol['inc'])
        rec['outer_total'] = om.total()
        rec['outer'] = om.vector()
    # subsample per-round arrays for JSON
    for k in ('CG-COLD', 'CG-WARM'):
        if k in B and 'iters' in B[k]:
            arr = B[k]
            L = len(arr['iters'])
            step = max(1, L // sub)
            for f in ('iters', 'r0', 'rel_inc'):
                arr[f] = arr[f][::step]
            arr['stride'] = step
    rec['wall'] = time.time() - t0
    return rec


def total_of(bdict):
    return bdict['meter']['total']
