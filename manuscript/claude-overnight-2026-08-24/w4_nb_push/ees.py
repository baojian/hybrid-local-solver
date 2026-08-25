"""W4 - EXPLORE-ELIMINATE-SUBSTITUTE (EES): nonbacktracking / directed-edge
residual propagation realized as elimination on the explored region.

System (degree-scaled push scale, z ~ pi):
    H z = gamma * s,   H = I - c A D^{-1},  c=(1-a)/(1+a), gamma=2a/(1+a)
    row u:  z_u - c * sum_{w~u} z_w / d_w = f_u      (H[u,w] = -c/d_w)
Residual r = gamma*s - H z maintained sparsely (dict).
Certificate: max_u |r_u| / d_u < gamma*eps   <=>   Model.cert_resid < alpha*eps
                                              =>   semantic err <= eps.

EES round:
  EXPLORE   multi-source BFS from violating vertices, gated by the optimistic
            path-worst-case decay rho -> rho*lam per step (lam=(1-sqrt(a))/(1+sqrt(a)))
            and by a per-round doubling depth cap R_cap (geometric expansion).
  ELIMINATE Gaussian elimination on H[S,S] with a degree-<=2-first ordering:
            peels pendant forest (Thomas), contracts degree-2 chains in the
            2-core (exact tridiagonal transfer -> one effective edge), leaving
            a junction core of min-degree >= 3 (size <= 2*betti - 2), solved
            densely (charged m^3 honestly).
  SUBSTITUTE back-substitution in reverse elimination order; z += delta on S,
            r[S] = 0, residual pushed to outside boundary: r_w += c*delta_u/d_u.

Charging (Meter):
  scan(u) per vertex of S per round (repeat rounds -> R_adj: honest re-elimination
  cost); resp per eliminated vertex ~ O(1) and resp(m^3) for the dense core;
  mat per fill cell and m^2 core cells; rec per coefficient write / backsub op /
  boundary pushback / BFS test.
"""
import math
import sys
from collections import deque

sys.path.insert(0, "/home/claude/work/overnight/lib")
import numpy as np
from model import push_params


def solve_region(adj, d, c, S, r, z, meter=None, dense_limit=2500):
    """Exact solve of H[S,S] delta = r[S]; z += delta, r[S]=0, pushback to
    boundary. Returns (core_size, n_elim, fill_cells)."""
    Slist = list(S)
    diag = {u: 1.0 for u in Slist}
    rhs = {u: r.get(u, 0.0) for u in Slist}
    nbr = {u: set() for u in Slist}
    w = {u: {} for u in Slist}
    for u in Slist:
        if meter: meter.scan(u)
        for v in adj[u]:
            if v in S:
                nbr[u].add(v)
                w[u][v] = w[u].get(v, 0.0) - c / d[v]
                if meter: meter.rec(1)

    q = deque(u for u in Slist if len(nbr[u]) <= 2)
    eliminated = set()
    stack = []  # (u, pivot, row=[(x,w_ux)], phi_u)
    fills = 0
    while q:
        u = q.popleft()
        if u in eliminated or len(nbr[u]) > 2:
            continue
        p = diag[u]
        assert p > 1e-14, f"pivot underflow {p}"
        row = [(x, w[u][x]) for x in nbr[u]]
        phi = rhs[u]
        stack.append((u, p, row, phi))
        eliminated.add(u)
        N = [x for x, _ in row]
        for a in N:
            nbr[a].discard(u)
        for a in N:
            wau = w[a].pop(u)
            f = wau / p
            rhs[a] -= f * phi
            for (x, wux) in row:
                if x == a:
                    diag[a] -= f * wux
                else:
                    old = w[a].get(x, 0.0)
                    w[a][x] = old - f * wux
                    if x not in nbr[a]:
                        nbr[a].add(x); nbr[x].add(a)
                        fills += 1
                        if meter: meter.mat(1)
            if meter: meter.resp(1 + len(row))
        for a in N:
            if a not in eliminated and len(nbr[a]) <= 2:
                q.append(a)
        if meter: meter.resp(2)

    core = [u for u in Slist if u not in eliminated]
    m = len(core)
    zloc = {}
    if m:
        if m > dense_limit:
            raise RuntimeError(f"core too big: {m}")
        cidx = {u: i for i, u in enumerate(core)}
        Mat = np.zeros((m, m))
        b = np.zeros(m)
        for u in core:
            Mat[cidx[u], cidx[u]] = diag[u]
            b[cidx[u]] = rhs[u]
            for x, val in w[u].items():
                Mat[cidx[u], cidx[x]] += val
        sol = np.linalg.solve(Mat, b)
        for u in core:
            zloc[u] = sol[cidx[u]]
        if meter:
            meter.resp(m ** 3)
            meter.mat(m * m)
    for (u, p, row, phi) in reversed(stack):
        s_ = 0.0
        for x, val in row:
            s_ += val * zloc[x]
        zloc[u] = (phi - s_) / p
        if meter: meter.rec(1 + len(row))
    # apply
    for u in Slist:
        z[u] += zloc[u]
        r[u] = 0.0
    for u in Slist:
        val = c * zloc[u] / d[u]
        if val != 0.0:
            for vv in adj[u]:
                if vv not in S:
                    r[vv] = r.get(vv, 0.0) + val
                    if meter: meter.rec(1)
    return m, len(stack), fills


def ees(adj, alpha, seed, eps, meter=None, R0=4, max_rounds=200,
        dense_limit=2500, gate_trust=False):
    """Returns dict with z (pi scale, list), S, rounds, per-round history.
    gate_trust=True: no doubling depth cap (pure lam-gate, one-shot expansion;
    exact depth on path-like geometry, may over-explore on branching graphs)."""
    n = len(adj)
    d = [len(adj[u]) for u in range(n)]
    c, gamma = push_params(alpha)
    sa = math.sqrt(alpha)
    lam = (1 - sa) / (1 + sa)
    thr = gamma * eps
    z = [0.0] * n
    r = {seed: gamma}
    S = set()
    R_cap = R0
    hist = []
    for rnd in range(max_rounds):
        viol = [(u, abs(rv)) for u, rv in r.items() if abs(rv) >= thr * d[u]]
        if not viol:
            return dict(z=z, r=r, S=S, rounds=rnd, hist=hist)
        # ---- EXPLORE: lam-gated multi-source BFS, depth cap R_cap ----
        rho = {}
        frontier = []
        for u, a_ in viol:
            rho[u] = max(rho.get(u, 0.0), a_)
        for u in rho:
            S.add(u)
            frontier.append(u)
        depth = 0
        cap = float("inf") if gate_trust else R_cap
        while frontier and depth < cap:
            depth += 1
            nxt = []
            for u in frontier:
                pu = rho[u] * lam
                if pu < thr:      # cannot pass any gate further
                    if meter: meter.rec(1)
                    continue
                for vv in adj[u]:
                    if meter: meter.rec(1)
                    if vv in rho:
                        continue
                    if vv in S or pu >= thr * d[vv]:
                        rho[vv] = pu
                        S.add(vv)
                        nxt.append(vv)
            frontier = nxt
        R_cap *= 2
        # ---- ELIMINATE + SUBSTITUTE ----
        m, ne, fills = solve_region(adj, d, c, S, r, z, meter, dense_limit)
        hist.append(dict(round=rnd, S=len(S), core=m, fills=fills))
    raise RuntimeError("EES: max_rounds exceeded")


def fifo_sor(adj, alpha, seed, eps, omega=None, meter=None, cap=None):
    """FIFO SOR-relaxed push tail (baseline). omega* = 2(1+a)/(1+sqrt(a))^2."""
    n = len(adj)
    d = [len(adj[u]) for u in range(n)]
    c, gamma = push_params(alpha)
    if omega is None:
        omega = 2 * (1 + alpha) / (1 + math.sqrt(alpha)) ** 2
    thr = gamma * eps
    z = [0.0] * n
    r = [0.0] * n
    r[seed] = gamma
    q = deque([seed])
    inq = [False] * n
    inq[seed] = True
    pushes = 0
    while q:
        u = q.popleft()
        inq[u] = False
        if abs(r[u]) < thr * d[u]:
            continue
        pushes += 1
        if cap and pushes > cap:
            return dict(z=z, r=r, pushes=pushes, capped=True)
        if meter: meter.scan(u)
        ru = r[u]
        z[u] += omega * ru
        r[u] = (1 - omega) * ru
        t = c * omega * ru / d[u]
        for v_ in adj[u]:
            r[v_] += t
            if not inq[v_] and abs(r[v_]) >= thr * d[v_]:
                q.append(v_)
                inq[v_] = True
        if not inq[u] and abs(r[u]) >= thr * d[u]:
            q.append(u)
            inq[u] = True
    return dict(z=z, r=r, pushes=pushes, capped=False)


def region_stats(adj, S):
    """(vol, edges, comps, betti) of induced subgraph on S."""
    E = 0
    vol = 0
    for u in S:
        vol += len(adj[u])
        E += sum(1 for v in adj[u] if v in S)
    E //= 2
    seen = set()
    comps = 0
    for u in S:
        if u in seen:
            continue
        comps += 1
        dq = deque([u]); seen.add(u)
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y in S and y not in seen:
                    seen.add(y); dq.append(y)
    betti = E - len(S) + comps
    return vol, E, comps, betti
