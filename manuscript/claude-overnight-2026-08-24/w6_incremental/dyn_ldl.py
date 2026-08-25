"""I2-B: SEG-LDL — dynamic-order incremental LDL^T on trees, via path-carved
continued-fraction segment trees (heavy-path / top-tree style, design (b)).

Why: the fill-free elimination orders of a tree are exactly the leaf-pruning
orders toward some root.  INC-LDL pins root = newest vertex (appends O(1) on
paths, quadratic fill on branching); TREE-INC pins root = seed (fill-free
always, but each admission renormalizes pivots along the leaf->seed path:
Theta(min(depth, 1/sqrt(alpha))) value-propagation, and no relative-tolerance
truncation can save it because the per-step contraction is 1 - c*sqrt(alpha)).
SEG-LDL keeps the seed-rooted order but stores the factorization IMPLICITLY:

  The tree is carved into vertex-disjoint paths (top..bottom).  Vertex u on a
  path has reduced diagonal  a_u = Q_uu - sum_{light children c} w_c^2/delta_c
  where delta_c is the impedance (Schur pivot) of c's hanging path-subtree and
  w_uv = -Q_uv = beta/(sqd_u sqd_v) > 0.  Along one path with vertices
  v_1..v_k (top..bottom), trailing minors obey
     phi_i = a_i phi_{i+1} - w_{i+1}^2 phi_{i+2},   phi_{k+1}=1, phi_{k+2}=0,
  i.e. (phi_i, phi_{i+1})^T = N_i (phi_{i+1}, phi_{i+2})^T with
     N_i = [[a_i, -w_{i+1}^2], [1, 0]]   (w_{k+1} = 0 for the bottom vertex).
  A balanced segment tree over the path stores ordered products of the N_i
  (normalized 2x2 matrices + log2 scale) and prefix sums of log2 w_i.  Then
     delta_top = phi_1/phi_2            (root aggregate, O(1) to read),
     x_{v_m}   = x_ext * (prod_{j<=m} w_j) * phi_{m+1}/phi_1   (O(log) query),
  where x_ext = x at the path's parent vertex (b_s replaces x_ext * w_1 on the
  root path; seed = top of the root path).  These are the standard tridiagonal
  inverse/cofactor identities; positivity of all minors (SPD M-matrix) makes
  the normalized products forward-stable, and every quantity is carried in
  log2 scale so nothing under/overflows.

  ADMIT leaf v under p:  if p is the childless bottom of its path, v extends
  that path (2 leaf updates, O(log)); otherwise v starts a new one-vertex path
  hanging as a light child of p (one leaf update at p).  Either way the
  path-top impedance changes, which changes one light contribution at the
  parent vertex of that path: one leaf update per path-level up to the root.
  Per-admission work = O(L * log) segment-tree nodes, L = #paths on the
  root chain.  NO truncation, NO value propagation: exact maintenance.

  QUERY x_u (gate): walk the path chain top-down, chaining x_ext through the
  O(log) closed-form evaluation on each path: O(L * log).

  LEVEL CONTROL: carving keeps L <= (#light edges on the root chain).  On
  path/caterpillar/spider/comb L <= 2 by construction; on btree/random trees
  L <= depth.  If an admission sees L > Lmax(n) = max(8, 2 log2 n + 6), the
  whole structure is rebuilt with a true heavy-light decomposition of the
  current tree (charged; heavy paths give L <= log2 n).  A link-cut-tree
  variant would make this worst-case O(log) amortized (see findings).

Charging (Meter): every touched segment-tree node costs MATC resp units
(2x2 multiply ~12 flops + normalization) + 5 mat writes; scalar log-weight
node ops SLWC; vector applications in queries QRYC per node.  Admissions,
propagation, queries, rebuilds and the final exact recompute are all charged.
Also here: replay_inc_ldl_capped (memory-safe INC-LDL for the comb) and
reroot_ledger (idealized cost of design (a) re-rooting, a lower-bound ledger).
"""
import sys, math
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from meter import Meter
import core

MATC = 16
SLWC = 2
QRYC = 10
ID = (1.0, 0.0, 0.0, 1.0, 0.0)


def _norm(m00, m01, m10, m11, e):
    s = max(abs(m00), abs(m01), abs(m10), abs(m11))
    ee = math.frexp(s)[1]
    if -2 <= ee <= 2:
        return (m00, m01, m10, m11, e)
    f = math.ldexp(1.0, -ee)
    return (m00 * f, m01 * f, m10 * f, m11 * f, e + ee)


def _mul(A, B):
    a00, a01, a10, a11, ae = A
    b00, b01, b10, b11, be = B
    return _norm(a00 * b00 + a01 * b10, a00 * b01 + a01 * b11,
                 a10 * b00 + a11 * b10, a10 * b01 + a11 * b11, ae + be)


class PathSeg:
    """One carved path, top..bottom, with an ordered-product segment tree."""
    __slots__ = ('cap', 'size', 'mat', 'slw', 'av', 'wdn2', 'lw',
                 'verts', 'pvert', 'contrib', 'w2top', 'pid')

    def __init__(self, pid, pvert, w2top):
        self.pid = pid
        self.pvert = pvert          # parent vertex id (None for root path)
        self.w2top = w2top          # w(top, pvert)^2 (0.0 for root path)
        self.contrib = 0.0          # last w2top/delta_top pushed into parent
        self.cap = 1
        self.size = 0
        self.mat = [ID, ID]
        self.slw = [0.0, 0.0]
        self.av, self.wdn2, self.lw, self.verts = [], [], [], []

    # -- leaf matrix from raws
    def _leafmat(self, i):
        return _norm(self.av[i], -self.wdn2[i], 1.0, 0.0, 0.0)

    def set_leaf(self, i):
        """Recompute leaf i and pull up. Returns touched node count."""
        c = self.cap
        k = c + i
        self.mat[k] = self._leafmat(i)
        self.slw[k] = self.lw[i]
        n = 1
        k >>= 1
        while k >= 1:
            self.mat[k] = _mul(self.mat[2 * k], self.mat[2 * k + 1])
            self.slw[k] = self.slw[2 * k] + self.slw[2 * k + 1]
            n += 1
            k >>= 1
        return n

    def append(self, v, a, wdn2, lw):
        """Append vertex at bottom. Returns touched node count (incl regrow)."""
        n = 0
        if self.size == self.cap:
            self.cap *= 2
            c = self.cap
            self.mat = [ID] * (2 * c)
            self.slw = [0.0] * (2 * c)
            for i in range(self.size):
                self.mat[c + i] = self._leafmat(i)
                self.slw[c + i] = self.lw[i]
            for k in range(c - 1, 0, -1):
                self.mat[k] = _mul(self.mat[2 * k], self.mat[2 * k + 1])
                self.slw[k] = self.slw[2 * k] + self.slw[2 * k + 1]
            n += 2 * c
        self.verts.append(v)
        self.av.append(a)
        self.wdn2.append(wdn2)
        self.lw.append(lw)
        i = self.size
        self.size += 1
        n += self.set_leaf(i)
        return n

    def delta_top(self):
        m = self.mat[1]
        assert m[2] != 0.0
        return m[0] / m[2]          # phi_1/phi_2, scale cancels

    def suffix_colvec(self, l):
        """(v0, v1, e, nodes): (N_l..N_{size-1})(1,0)^T with log2 scale e."""
        if l >= self.size:
            return 1.0, 0.0, 0.0, 0
        c = self.cap
        lo, hi = l + c, self.size + c
        L, R = [], []
        while lo < hi:
            if lo & 1:
                L.append(lo); lo += 1
            if hi & 1:
                hi -= 1; R.append(hi)
            lo >>= 1; hi >>= 1
        nodes = L + R[::-1]
        v0, v1, e = 1.0, 0.0, 0.0
        for nd in reversed(nodes):
            m00, m01, m10, m11, me = self.mat[nd]
            v0, v1 = m00 * v0 + m01 * v1, m10 * v0 + m11 * v1
            e += me
            s = max(abs(v0), abs(v1))
            ee = math.frexp(s)[1]
            if not (-2 <= ee <= 2):
                f = math.ldexp(1.0, -ee)
                v0 *= f; v1 *= f; e += ee
        return v0, v1, e, len(nodes)

    def slw_prefix(self, r):
        """sum of lw over leaves [0, r); returns (sum, nodes)."""
        c = self.cap
        lo, hi = c, r + c
        s = 0.0
        n = 0
        while lo < hi:
            if lo & 1:
                s += self.slw[lo]; lo += 1; n += 1
            if hi & 1:
                hi -= 1; s += self.slw[hi]; n += 1
            lo >>= 1; hi >>= 1
        return s, n

    def x_at(self, pos, logsrc, src_is_b):
        """log2 x of verts[pos] given log2 x_ext (or log2 b_s on the root
        path).  Everything stays in log2 so deep chains cannot underflow.
        Returns (log2 x, nodes)."""
        rm = self.mat[1]
        phi1, e1 = rm[0], rm[4]
        assert phi1 > 0.0
        if pos + 1 >= self.size:
            s0, es, nq = 1.0, 0.0, 0
        else:
            s0, _s1, es, nq = self.suffix_colvec(pos + 1)
        assert s0 > 0.0
        slws, ns = self.slw_prefix(pos + 1)
        if src_is_b:
            slws -= self.lw[0]      # root path: no w_1 factor, b_s instead
        logx = logsrc + slws + (math.log2(s0) + es) \
            - (math.log2(phi1) + e1)
        return logx, nq + ns + 2


class DynTree:
    """Grow-only seed-rooted tree with path-carved implicit LDL^T."""

    def __init__(self, model, meter):
        self.mo = model
        self.m = meter
        alpha = model.alpha
        self.qdiag = (1 + alpha) / 2.0
        self.beta = (1 - alpha) / 2.0
        self.sqd = model.sqd
        seed = int(np.nonzero(model.s)[0][0])
        self.seed = seed
        self.bs = float(model.b[seed])
        self.parent = {seed: None}
        self.children = {seed: []}
        P = PathSeg(0, None, 0.0)
        n0 = P.append(seed, self.qdiag, 0.0, 0.0)
        self.paths = [P]
        self.pathof = {seed: 0}
        self.posin = {seed: 0}
        self.nver = 1
        self.levels = []
        self.admit_nodes = []
        self.query_nodes = []
        self.rebuilds = 0
        self.rebuild_nodes = 0
        meter.resp(n0 * MATC + 4)
        meter.mat(n0 * 5)

    def w(self, u, v):
        return self.beta / (self.sqd[u] * self.sqd[v])

    def Lmax(self):
        return max(8, int(2 * math.log2(self.nver + 2)) + 6)

    def admit(self, v, p):
        m = self.m
        nodes = 0
        wv = self.w(v, p)
        self.parent[v] = p
        self.children[v] = []
        Pp = self.paths[self.pathof[p]]
        extend = (self.posin[p] == Pp.size - 1) and not self.children[p]
        self.children[p].append(v)
        self.nver += 1
        if extend:
            i = self.posin[p]
            Pp.wdn2[i] = wv * wv
            nodes += Pp.set_leaf(i)
            self.pathof[v] = Pp.pid
            self.posin[v] = Pp.size
            nodes += Pp.append(v, self.qdiag, 0.0, math.log2(wv))
            start = Pp
            lev = 1
        else:
            NP = PathSeg(len(self.paths), p, wv * wv)
            nodes += NP.append(v, self.qdiag, 0.0, math.log2(wv))
            self.paths.append(NP)
            self.pathof[v] = NP.pid
            self.posin[v] = 0
            NP.contrib = wv * wv / self.qdiag
            i = self.posin[p]
            Pp.av[i] -= NP.contrib
            nodes += Pp.set_leaf(i)
            start = Pp
            lev = 2
        Pk = start
        while Pk.pvert is not None:
            dt = Pk.delta_top()
            assert dt > 0.0, ('pivot', dt)
            cn = Pk.w2top / dt
            if cn == Pk.contrib:
                break
            u = Pk.pvert
            PU = self.paths[self.pathof[u]]
            PU.av[self.posin[u]] += Pk.contrib - cn
            Pk.contrib = cn
            nodes += PU.set_leaf(self.posin[u])
            Pk = PU
            lev += 1
        m.resp(nodes * MATC + 4)
        m.mat(nodes * 5 + 4)
        self.levels.append(lev)
        self.admit_nodes.append(nodes)
        if lev > self.Lmax():
            self.full_rebuild()

    def query_x(self, u, charge=True):
        chain = []
        pid, pos = self.pathof[u], self.posin[u]
        while True:
            chain.append((pid, pos))
            pv = self.paths[pid].pvert
            if pv is None:
                break
            pid, pos = self.pathof[pv], self.posin[pv]
        src = math.log2(self.bs)
        nodes = 0
        first = True
        for pid, pos in reversed(chain):
            src, nq = self.paths[pid].x_at(pos, src, first)
            first = False
            nodes += nq
        if charge:
            self.m.resp(nodes * QRYC)
        self.query_nodes.append(nodes)
        return (2.0 ** src if src > -1000.0 else 0.0), len(chain)

    def full_rebuild(self):
        """True HLD of the current tree; rebuild everything. Charged."""
        seed = self.seed
        bfs = [seed]
        for u in bfs:
            bfs.extend(self.children[u])
        size = {u: 1 for u in bfs}
        for u in reversed(bfs):
            for c in self.children[u]:
                size[u] += size[c]
        heavy = {}
        for u in bfs:
            if self.children[u]:
                heavy[u] = max(self.children[u], key=lambda c: size[c])
        newpaths = []
        depth_top = []
        depth = {seed: 0}
        for u in bfs:
            for c in self.children[u]:
                depth[c] = depth[u] + 1
        for u in bfs:
            p = self.parent[u]
            if p is None or heavy.get(p) != u:
                verts = [u]
                w = u
                while w in heavy:
                    w = heavy[w]
                    verts.append(w)
                newpaths.append((u, p, verts))
                depth_top.append(depth[u])
        order = sorted(range(len(newpaths)), key=lambda i: -depth_top[i])
        self.paths = [None] * len(newpaths)
        av = {u: self.qdiag for u in bfs}
        nodes = 0
        newid = {i: k for k, i in enumerate(order)}
        for i in order:
            top, pv, verts = newpaths[i]
            w2t = 0.0 if pv is None else self.w(top, pv) ** 2
            P = PathSeg(newid[i], pv, w2t)
            for j, u in enumerate(verts):
                if j + 1 < len(verts):
                    wd = self.w(verts[j + 1], u)
                else:
                    wd = 0.0
                lw = 0.0 if self.parent[u] is None \
                    else math.log2(self.w(u, self.parent[u]))
                nodes += P.append(u, av[u], wd * wd, lw)
                self.pathof[u] = newid[i]
                self.posin[u] = j
            self.paths[newid[i]] = P
            if pv is not None:
                d = P.delta_top()
                assert d > 0.0
                P.contrib = w2t / d
                av[pv] -= P.contrib
        # av of parents changed after their paths were built? No: paths are
        # built deepest-top-first, so every light contribution lands in av[pv]
        # BEFORE pv's own path is built (depth[pv] < depth[top]).
        self.rebuilds += 1
        self.rebuild_nodes += nodes
        self.m.resp(nodes * MATC + self.nver)
        self.m.mat(nodes * 5)


def replay_seg_ldl(model, trace, verbose=False):
    alpha, eps = model.alpha, trace['eps']
    m = Meter(model.adj)
    core.outer_charge(model, trace, m)
    dt = DynTree(model, m)
    order, pos = trace['order'], trace['pos']
    adj = model.adj
    admitted = 1
    verr = 0.0
    for r in trace['rounds']:
        while admitted < r['n']:
            v = order[admitted]
            admitted += 1
            par = [u for u in adj[v] if u in dt.parent]
            assert len(par) == 1, (v, par)
            dt.admit(v, par[0])
        xt = r['x']
        for u in r['F']:
            xu, lev = dt.query_x(u)
            xe = xt[pos[u]]
            verr = max(verr, abs(xu - xe) / max(abs(xe), 1e-300))
    assert verr < 1e-6, ('seg verr', verr)
    # finalize: one exact leaves-first delta pass + root-down x pass, charged
    n = len(order)
    m.resp(2 * n); m.mat(n); m.emit(n)
    Q = model.Q
    beta = dt.beta
    sqd = model.sqd
    dex = {}
    for v in reversed(order):
        dv = dt.qdiag
        for c in dt.children[v]:
            dv -= (beta / (sqd[v] * sqd[c])) ** 2 / dex[c]
        dex[v] = dv
    root = order[0]
    xex = {root: model.b[root] / dex[root]}
    for v in order[1:]:
        p = dt.parent[v]
        xex[v] = beta / (sqd[v] * sqd[p]) / dex[v] * xex[p]
    xfin = np.zeros(model.n)
    for v in order:
        xfin[v] = xex[v]
    cert = model.cert_resid(xfin)
    sem = model.semantic_err(xfin, trace['x0'])
    assert cert < alpha * eps and sem <= eps, (cert, sem)
    fe = float(np.max(np.abs(xfin[np.array(order)] - trace['rounds'][-1]['x'])))
    assert fe < 1e-8 * max(1.0, float(np.max(np.abs(trace['rounds'][-1]['x'])))), fe
    return dict(meter=m.vector(), verr=float(verr),
                lev_mean=float(np.mean(dt.levels)) if dt.levels else 1.0,
                lev_max=int(max(dt.levels)) if dt.levels else 1,
                admit_nodes_mean=float(np.mean(dt.admit_nodes)) if dt.admit_nodes else 0.0,
                admit_nodes_max=int(max(dt.admit_nodes)) if dt.admit_nodes else 0,
                admit_nodes_total=int(np.sum(dt.admit_nodes)) if dt.admit_nodes else 0,
                query_nodes_total=int(np.sum(dt.query_nodes)) if dt.query_nodes else 0,
                nqueries=len(dt.query_nodes),
                npaths=len(dt.paths), rebuilds=dt.rebuilds,
                rebuild_nodes=int(dt.rebuild_nodes),
                cert=float(cert), sem=float(sem))


# ------------------------------------------------------------------ INC-LDL
# memory-safe capped replay (comb fill blows past RAM otherwise)

def replay_inc_ldl_capped(model, trace, nnzcap=4e6, respcap=6e8):
    alpha, eps = model.alpha, trace['eps']
    m = Meter(model.adj)
    core.outer_charge(model, trace, m)
    inc = core.IncLDL(model, m)
    order, pos = trace['order'], trace['pos']
    adj = model.adj
    Q = model.Q
    admitted = 0
    nnzL = 0
    gate_total = 0
    for t, r in enumerate(trace['rounds']):
        while admitted < r['n']:
            v = order[admitted]
            nb = [pos[w] for w in adj[v] if w in pos and pos[w] < admitted]
            qrow = Q[v]
            qd = {k: w for k, w in zip(qrow.indices, qrow.data)}
            qvals = [qd[order[p]] for p in nb]
            inc.append(v, nb, qd[v], qvals, model.b[v])
            admitted += 1
            nnzL += len(inc.rows[-1])
            if nnzL > nnzcap or m.C_resp > respcap:
                return dict(capped=True, meter=m.vector(), nnzL=int(nnzL),
                            admitted=int(admitted), n_target=len(order),
                            frac=admitted / len(order))
        F_pos = [pos[u] for u in r['F']]
        _xF, cost, _D = inc.gate_x(F_pos)
        gate_total += cost
        if m.C_resp > respcap:
            return dict(capped=True, meter=m.vector(), nnzL=int(nnzL),
                        admitted=int(admitted), n_target=len(order),
                        frac=admitted / len(order))
    xfin = inc.finalize()
    xt = trace['rounds'][-1]['x']
    verr = float(np.max(np.abs(xfin - xt)))
    assert verr < 1e-7 * max(1.0, float(np.max(np.abs(xt)))), verr
    xfull = np.zeros(model.n)
    xfull[np.array(order)] = xfin
    cert = model.cert_resid(xfull)
    sem = model.semantic_err(xfull, trace['x0'])
    assert cert < alpha * eps and sem <= eps, (cert, sem)
    return dict(capped=False, meter=m.vector(), nnzL=int(nnzL),
                gate_total=int(gate_total),
                append_total=int(sum(inc.append_cost)),
                cert=float(cert), sem=float(sem))


# ------------------------------------------------------------------ REROOT
# idealized ledger for design (a): per admission, re-eliminate the tree path
# from the previous root to the new vertex (cost = path length); batches are
# toured in Euler order of the final admission tree (near-optimal ordering).
# This is a LOWER-BOUND-flavoured ledger (O(1) per re-eliminated vertex, free
# gates), so if IT scales badly, design (a) is dead.

def reroot_ledger(model, trace):
    order = trace['order']
    adj = model.adj
    parent, depth = {order[0]: None}, {order[0]: 0}
    children = {order[0]: []}
    for v in order[1:]:
        par = [u for u in adj[v] if u in parent]
        parent[v] = par[0]
        depth[v] = depth[par[0]] + 1
        children[v] = []
        children[par[0]].append(v)
    euler = {}
    stack = [order[0]]
    t = 0
    while stack:
        u = stack.pop()
        euler[u] = t; t += 1
        for c in reversed(children[u]):
            stack.append(c)

    def dist(a, b):
        d = 0
        while depth[a] > depth[b]:
            a = parent[a]; d += 1
        while depth[b] > depth[a]:
            b = parent[b]; d += 1
        while a != b:
            a = parent[a]; b = parent[b]; d += 2
        return d

    W = 0
    prev = order[0]
    per_round = []
    for r in trace['rounds']:
        if not r['T']:
            continue
        batch = sorted(r['T'], key=lambda v: euler[v])
        w0 = W
        for v in batch:
            W += dist(prev, v) + 1
            prev = v
        per_round.append(W - w0)
    return dict(W=int(W), per_round_mean=float(np.mean(per_round)) if per_round else 0.0,
                per_round_max=int(max(per_round)) if per_round else 0)
