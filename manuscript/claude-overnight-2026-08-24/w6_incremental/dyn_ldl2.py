"""I2-B: HSEG-LDL — SEG-LDL with genuine dynamic-order maintenance.

SEG-LDL (dyn_ldl.DynTree) carves the growing tree into paths by the rule
"a new vertex extends its parent's path iff the parent is the childless bottom
of that path".  That carving is *admission-order* dependent and the COMB
breaks it: a tooth vertex (degree 2) crosses the admission threshold one round
before the next backbone vertex (degree 3), so the tooth captures the
backbone's path continuation and the backbone is chopped into segments.  The
chain of paths from a deep tooth vertex to the seed then has length
Theta(#backbone segments) instead of 2, and every admission pays that.

HSEG-LDL fixes this by maintaining a *2-approximate heavy path decomposition*
of the current tree under leaf insertions:

  own[i]   = 1 + sum of subtree sizes of the LIGHT children of verts[i]
  sz(verts[i]) = suffix_sum(own, i)   (carried in the SAME segment tree)
  P.tot    = sz(P.top) = size of the subtree hanging at P's top

  ADMIT v under p: extend/create as before, then walk up the chain of paths.
  At each jump the chain enters vertex u = P_k.pvert from its light child
  path P_k; we point-add +1 to own[posin[u]] (P_k's subtree grew) and compare
      sz(P_k.top)  vs  2 * sz(h),   h = the vertex just below u on u's path.
  If P_k's subtree is more than twice the heavy tail's, SWAP:
      - split u's path below u; the old tail becomes a new light child path
        (its light contribution w^2/delta_top is subtracted from a_u),
      - splice P_k's vertices onto u's path (its light contribution is added
        back into a_u), fixing only the junction weight w(u, P_k.top),
      - rebuild both segment trees and Fenwicks, relabel pathof/posin.
  Cost O(#vertices moved), all charged.

  The factor 2 makes swaps self-amortizing: after a swap the winner's subtree
  is > 2x the loser's, so the loser must double before it can win back; every
  vertex therefore moves O(log |S|) times, total re-carve work O(|S| log |S|).
  The same factor keeps the chains short: a light edge (u,c) has
  sz(c) <= 2*sz(heavy(u)) and sz(u) >= sz(c) + sz(heavy(u)) >= 1.5*sz(c), so
  the number of light edges to the root is <= log_{1.5}|S| ~ 1.71*log2|S|.

Everything else (continued-fraction 2x2 segment trees, log2-scaled values,
O(1) delta_top read, O(log) x-query) is inherited from dyn_ldl.PathSeg.
"""
import sys, math
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from meter import Meter
import core
from dyn_ldl import PathSeg, MATC, SLWC, QRYC, ID, _mul, _norm

HEAVY_FACTOR = 2.0


class HPath(PathSeg):
    """PathSeg + a leaf-sum array `osum` carried in the SAME segment tree, so
    subtree sizes survive splices for free, and an O(moved) splice."""
    __slots__ = ('own', 'osum')

    def __init__(self, pid, pvert, w2top):
        PathSeg.__init__(self, pid, pvert, w2top)
        self.own = []
        self.osum = [0, 0]

    # ---- segment-tree maintenance (mat, slw, osum together)
    def set_leaf(self, i):
        c = self.cap
        k = c + i
        live = i < self.size
        self.mat[k] = self._leafmat(i) if live else ID
        self.slw[k] = self.lw[i] if live else 0.0
        self.osum[k] = self.own[i] if live else 0
        n = 1
        k >>= 1
        while k >= 1:
            self.mat[k] = _mul(self.mat[2 * k], self.mat[2 * k + 1])
            self.slw[k] = self.slw[2 * k] + self.slw[2 * k + 1]
            self.osum[k] = self.osum[2 * k] + self.osum[2 * k + 1]
            n += 1
            k >>= 1
        return n

    def _regrow(self, need):
        c = 1
        while c < max(1, need):
            c *= 2
        self.cap = c
        self.mat = [ID] * (2 * c)
        self.slw = [0.0] * (2 * c)
        self.osum = [0] * (2 * c)
        for i in range(self.size):
            self.mat[c + i] = self._leafmat(i)
            self.slw[c + i] = self.lw[i]
            self.osum[c + i] = self.own[i]
        for k in range(c - 1, 0, -1):
            self.mat[k] = _mul(self.mat[2 * k], self.mat[2 * k + 1])
            self.slw[k] = self.slw[2 * k] + self.slw[2 * k + 1]
            self.osum[k] = self.osum[2 * k] + self.osum[2 * k + 1]
        return 2 * c

    def push(self, v, a, wdn2, lw, own):
        n = 0
        self.verts.append(v); self.av.append(a)
        self.wdn2.append(wdn2); self.lw.append(lw); self.own.append(own)
        self.size += 1
        if self.size > self.cap:
            n += self._regrow(self.size)
        else:
            n += self.set_leaf(self.size - 1)
        return n

    def reload(self, verts, av, wdn2, lw, own):
        self.verts, self.av, self.wdn2 = verts, av, wdn2
        self.lw, self.own = lw, own
        self.size = len(verts)
        return self._regrow(self.size) + self.size

    @property
    def tot(self):
        return self.osum[1]

    def own_add(self, i, v):
        self.own[i] += v
        return self.set_leaf(i)

    def range_osum(self, l, r):
        """sum of own over leaves [l, r)."""
        if l >= r:
            return 0, 0
        c = self.cap
        lo, hi = l + c, r + c
        s = 0; n = 0
        while lo < hi:
            if lo & 1:
                s += self.osum[lo]; lo += 1; n += 1
            if hi & 1:
                hi -= 1; s += self.osum[hi]; n += 1
            lo >>= 1; hi >>= 1
        return s, n

    def sz_at(self, i):
        """subtree size of verts[i] (0 past the end)."""
        if i >= self.size:
            return 0
        return self.range_osum(i, self.size)[0]

    def detach_tail(self, k):
        """Remove positions k+1.. ; return their raw arrays. O(tail*log)."""
        t = self.size - (k + 1)
        if t <= 0:
            return None, 0
        raw = (self.verts[k + 1:], self.av[k + 1:], self.wdn2[k + 1:],
               self.lw[k + 1:], self.own[k + 1:])
        del self.verts[k + 1:]; del self.av[k + 1:]; del self.wdn2[k + 1:]
        del self.lw[k + 1:]; del self.own[k + 1:]
        old = self.size
        self.size = k + 1
        n = 0
        for i in range(k + 1, old):
            n += self.set_leaf(i)          # writes ID / 0 (i >= size)
        return raw, n

    def extend_from(self, P):
        """Append every vertex of path P. O(len(P)*log) amortized."""
        n = 0
        for j in range(P.size):
            n += self.push(P.verts[j], P.av[j], P.wdn2[j], P.lw[j], P.own[j])
        return n


class HDynTree:
    """Grow-only seed-rooted tree, implicit LDL^T on 2-approx heavy paths."""

    def __init__(self, model, meter, heavy=HEAVY_FACTOR):
        self.mo = model
        self.m = meter
        self.hf = heavy
        alpha = model.alpha
        self.qdiag = (1 + alpha) / 2.0
        self.beta = (1 - alpha) / 2.0
        self.sqd = model.sqd
        seed = int(np.nonzero(model.s)[0][0])
        self.seed = seed
        self.bs = float(model.b[seed])
        self.parent = {seed: None}
        self.children = {seed: []}
        P = HPath(0, None, 0.0)
        n0 = P.push(seed, self.qdiag, 0.0, 0.0, 1)
        self.paths = [P]
        self.pathof = {seed: 0}
        self.posin = {seed: 0}
        self.nver = 1
        self.levels, self.admit_nodes, self.query_nodes = [], [], []
        self.swaps = 0
        self.swap_moved = 0
        meter.resp(n0 * MATC + 4)
        meter.mat(n0 * 5)

    def w(self, u, v):
        return self.beta / (self.sqd[u] * self.sqd[v])

    # ---------------------------------------------------------- swap
    def do_swap(self, u, Pc):
        """Promote light child path Pc to be u's heavy continuation.
        Cost O((|tail| + |Pc|) log) -- only the vertices that actually move."""
        PU = self.paths[self.pathof[u]]
        k = self.posin[u]
        nodes = 0
        newown_u = PU.own[k] - Pc.tot        # Pc stops being a light child
        na_u = PU.av[k] + Pc.contrib         # ... so add its contrib back
        raw, n1 = PU.detach_tail(k)
        nodes += n1
        ntail = 0
        if raw is not None:
            tv, ta, tw, tl, to = raw
            ntail = len(tv)
            w2t = self.w(u, tv[0]) ** 2
            T = HPath(len(self.paths), u, w2t)
            nodes += T.reload(tv, ta, tw, tl, to)
            self.paths.append(T)
            for j, x in enumerate(tv):
                self.pathof[x] = T.pid
                self.posin[x] = j
            dtt = T.delta_top()
            assert dtt > 0.0
            T.contrib = w2t / dtt
            newown_u += T.tot                # old tail becomes a light child
            na_u -= T.contrib
        PU.av[k] = na_u
        PU.own[k] = newown_u
        PU.wdn2[k] = self.w(u, Pc.verts[0]) ** 2
        nodes += PU.set_leaf(k)
        base = PU.size
        nodes += PU.extend_from(Pc)
        for j in range(Pc.size):
            x = Pc.verts[j]
            self.pathof[x] = PU.pid
            self.posin[x] = base + j
        self.paths[Pc.pid] = None
        self.swaps += 1
        self.swap_moved += ntail + Pc.size
        self.m.resp(nodes * MATC)
        self.m.mat(nodes * 2)
        return nodes

    # ---------------------------------------------------------- admit
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
            nodes += Pp.push(v, self.qdiag, 0.0, math.log2(wv), 1)
            Pk = Pp
        else:
            NP = HPath(len(self.paths), p, wv * wv)
            nodes += NP.push(v, self.qdiag, 0.0, math.log2(wv), 1)
            self.paths.append(NP)
            self.pathof[v] = NP.pid
            self.posin[v] = 0
            NP.contrib = wv * wv / self.qdiag
            i = self.posin[p]
            Pp.av[i] -= NP.contrib
            nodes += Pp.own_add(i, 1)
            Pk = Pp
        lev = 1
        while Pk.pvert is not None:
            u = Pk.pvert
            PU = self.paths[self.pathof[u]]
            ku = self.posin[u]
            nodes += PU.own_add(ku, 1)         # Pk's subtree grew by 1
            dt = Pk.delta_top()
            assert dt > 0.0, ('pivot', dt)
            cn = Pk.w2top / dt
            changed = (cn != Pk.contrib)
            if changed:
                PU.av[ku] += Pk.contrib - cn
                Pk.contrib = cn
                nodes += PU.set_leaf(ku)
            # 2-approximate heavy check
            if Pk.tot > self.hf * PU.sz_at(ku + 1):
                nodes += self.do_swap(u, Pk)
                PU = self.paths[self.pathof[u]]
                nodes += PU.set_leaf(self.posin[u])
                changed = True
            elif not changed:
                break
            Pk = PU
            lev += 1
        m.resp(nodes * MATC + 4)
        m.mat(nodes * 5 + 4)
        self.levels.append(lev)
        self.admit_nodes.append(nodes)

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


def replay_hseg(model, trace, heavy=HEAVY_FACTOR, verbose=False):
    alpha, eps = model.alpha, trace['eps']
    m = Meter(model.adj)
    core.outer_charge(model, trace, m)
    dt = HDynTree(model, m, heavy)
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
    assert verr < 1e-6, ('hseg verr', verr)
    n = len(order)
    m.resp(2 * n); m.mat(n); m.emit(n)
    beta, sqd = dt.beta, model.sqd
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
    lv = dt.levels or [1]
    return dict(meter=m.vector(), verr=float(verr),
                lev_mean=float(np.mean(lv)), lev_max=int(max(lv)),
                admit_nodes_mean=float(np.mean(dt.admit_nodes or [0])),
                admit_nodes_total=int(np.sum(dt.admit_nodes or [0])),
                query_nodes_total=int(np.sum(dt.query_nodes or [0])),
                nqueries=len(dt.query_nodes),
                npaths=sum(1 for p in dt.paths if p is not None),
                swaps=int(dt.swaps), swap_moved=int(dt.swap_moved),
                cert=float(cert), sem=float(sem))
