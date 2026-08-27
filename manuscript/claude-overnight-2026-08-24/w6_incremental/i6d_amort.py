"""I6-D: HSEG-LDL re-carve amortization — proof-driven repair (full-walk rule),
thrash adversaries, and the tree-theorem constants.

EXTRACTED SWAP RULE (dyn_ldl2.HDynTree.admit, line 289):
  during the admission walk, at each junction where the chain leaves light
  child path Pk and enters u = Pk.pvert, after own_add(+1):
      fire iff  sz(Pk.top) > 2.0 * sz(h(u))        [strict; HEAVY_FACTOR = 2]
  where h(u) = vertex just below u on u's own path (sz = 0 if u is bottom).
  On fire: u's tail below u is detached into a new light path T, ALL of Pk's
  vertices are spliced onto u's path.  moved = |tail| + |Pk| (path lengths),
  each moved leaf = one set_leaf = O(log) seg-tree nodes.

THE HOLE IN THE SHIPPED CODE: the walk has `elif not changed: break` — when
Pk's float contribution w^2/delta freezes, the walk stops, so own_add and the
heavy check are SKIPPED above the break.  Maintained sizes can then undercount
without bound and the 2-approx invariant is enforced only lazily.  The proof
below needs exact sizes; HDynTreeFW ("full walk") is the repair: sizes and
heavy checks always walk the whole junction chain (O(chain * log) = O(log^2)
per admission, same asymptotics); only the VALUE update stops early (exact:
frozen contribution => a_u unchanged => all higher deltas unchanged), and a
swap un-freezes it (a_u changed).

THEOREM (amortized re-carve, full-walk rule, hysteresis 2, any tree, any
admission order of n leaf-insertions):
    Phi = sum over light edges (u,c) of max(0, 2*sz(c) - sz(h(u))) >= 0.
  * Insertion of x raises Phi by <= 2*Lambda(x) + 2 <= 2*log_{1.5} n + 2,
    since sz(+1) along x's root chain touches +2 per light chain edge (and
    heavy-side +1's only lower terms); Lambda <= log_{1.5} n by the invariant.
  * A swap at u fires with sz(C) >= 2 sz(H) + 1 and releases the (u,C) term
    2 sz(C) - sz(H) >= sz(C) + sz(H) + 1 > |P_C| + |tail| = moved  (the new
    light edge (u, H_top) enters at value 0 since 2 sz(H) < sz(C); all other
    terms can only fall).
  => total moved <= (2 log_{1.5} n + 2) n ~ 3.42 n log2 n, and total re-carve
     cost <= O(moved * log n) = O(n log^2 n), alpha-free.  Combined with the
     proved chain bound: total backend work O((n + Q) log^2 n).
"""
import sys, math, time, json, random
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from model import Model
from meter import Meter
import core, zoo, i2b
import dyn_ldl2
from dyn_ldl2 import HDynTree, HPath
from dyn_ldl import MATC, QRYC

OUT = '/home/claude/work/overnight/w6_incremental/res_i6d.json'


class HDynTreeFW(HDynTree):
    """Full-walk repair: sizes + heavy checks on EVERY junction of every
    admission; value updates freeze exactly as before (and un-freeze after a
    swap).  Also instruments per-admission moved and per-junction swap log."""

    def __init__(self, model, meter, heavy=dyn_ldl2.HEAVY_FACTOR):
        HDynTree.__init__(self, model, meter, heavy)
        self.adm_moved = []           # moved vertices per admission
        self.swap_log = []            # (u, szC, szH, moved) per swap

    def do_swap(self, u, Pc):
        m0 = self.swap_moved
        szC = Pc.tot
        PU = self.paths[self.pathof[u]]
        szH = PU.sz_at(self.posin[u] + 1)
        n = HDynTree.do_swap(self, u, Pc)
        self.swap_log.append((u, int(szC), int(szH),
                              int(self.swap_moved - m0)))
        return n

    def admit(self, v, p):
        m = self.m
        mv0 = self.swap_moved
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
        frozen = False
        while Pk.pvert is not None:
            u = Pk.pvert
            PU = self.paths[self.pathof[u]]
            ku = self.posin[u]
            nodes += PU.own_add(ku, 1)          # size walk: ALWAYS
            if not frozen:
                dt = Pk.delta_top()
                assert dt > 0.0, ('pivot', dt)
                cn = Pk.w2top / dt
                if cn != Pk.contrib:
                    PU.av[ku] += Pk.contrib - cn
                    Pk.contrib = cn
                    nodes += PU.set_leaf(ku)
                else:
                    frozen = True               # value provably frozen above
            if Pk.tot > self.hf * PU.sz_at(ku + 1):     # heavy check: ALWAYS
                nodes += self.do_swap(u, Pk)
                PU = self.paths[self.pathof[u]]
                nodes += PU.set_leaf(self.posin[u])
                frozen = False                  # a_u changed -> values live
            Pk = PU
            lev += 1
        m.resp(nodes * MATC + 4)
        m.mat(nodes * 5 + 4)
        self.levels.append(lev)
        self.admit_nodes.append(nodes)
        self.adm_moved.append(self.swap_moved - mv0)


def replay_cls(model, trace, cls, heavy=dyn_ldl2.HEAVY_FACTOR):
    """dyn_ldl2.replay_hseg with a class parameter + extra outputs."""
    old = dyn_ldl2.HDynTree
    dyn_ldl2.HDynTree = cls
    try:
        d = dyn_ldl2.replay_hseg(model, trace, heavy)
    finally:
        dyn_ldl2.HDynTree = old
    return d


# ---------------------------------------------------------------- structural
def drive(adj, seed, order, cls=HDynTreeFW, alpha=0.25, check_dense=0):
    """Admit `order`; return amortization metrics (no PPR trace needed —
    the re-carve accounting is purely structural)."""
    mo = Model(adj, alpha, seed)
    dt = cls(mo, Meter(adj))
    inS = {seed}
    S = [seed]
    for v in order:
        par = [u for u in adj[v] if u in inS]
        assert len(par) == 1, (v, par)
        dt.admit(v, par[0])
        inS.add(v); S.append(v)
    n = len(S)
    err = 0.0
    if check_dense:
        idx = np.array(S)
        Qs = mo.Q[idx][:, idx].toarray()
        xs = np.linalg.solve(Qs, mo.b[idx])
        for k in range(0, n, max(1, n // check_dense)):
            xq, _ = dt.query_x(S[k], charge=False)
            err = max(err, abs(xq - xs[k]) / max(abs(xs[k]), 1e-300))
    lg = math.log2(max(n, 2))
    am = getattr(dt, 'adm_moved', [0])
    return dict(n=n, swaps=dt.swaps, moved=int(dt.swap_moved),
                mv_n=dt.swap_moved / n, mv_nlog=dt.swap_moved / (n * lg),
                maxadm=int(max(am) if am else 0),
                lev_mean=float(np.mean(dt.levels)),
                lev_max=int(max(dt.levels)), lev_bound=1.71 * lg,
                adm_nodes=int(np.sum(dt.admit_nodes)),
                adm_nlog2=float(np.sum(dt.admit_nodes)) / (n * lg * lg),
                dense_err=err), dt


# thrash(alternating): root junction, two path arms, always extend the light
# arm; fires as often as hysteresis allows.  Schedule simulated exactly.
def thrash_alt(n):
    a, b = 1, 0
    order_side = ['A']                 # first vertex extends root's path
    sim_swaps, sim_moved = 0, 0
    light = 'B'
    while 1 + a + b < n:
        if light == 'B':
            b += 1; order_side.append('B')
            if b > 2 * a:
                sim_swaps += 1; sim_moved += a + b; light = 'A'
        else:
            a += 1; order_side.append('A')
            if a > 2 * b:
                sim_swaps += 1; sim_moved += a + b; light = 'B'
    adj = {0: []}
    nid = 1
    tip = {'A': 0, 'B': 0}
    order = []
    for s in order_side:
        p = tip[s]
        adj[p].append(nid); adj[nid] = [p]
        tip[s] = nid; order.append(nid); nid += 1
    return {u: sorted(vs) for u, vs in adj.items()}, 0, order, sim_swaps, \
        sim_moved


# nested thrash: complete binary arena of junctions (depth kk, inter-junction
# paths of length ps, long tails below); adaptive driver descends the LIGHT
# side at every junction (read off the live carving) and extends that frontier.
def nested_arena(kk=5, ps=4, tail=4000):
    adj = {0: []}
    down = {0: []}
    nid = [1]

    def newv(p):
        v = nid[0]; nid[0] += 1
        adj[p].append(v); adj[v] = [p]
        down[p].append(v); down[v] = []
        return v

    def path(p, L):
        for _ in range(L):
            p = newv(p)
        return p

    junc = set()

    def build(p, lev):
        u = path(p, ps)                # inter-junction path, ends at u
        if lev == 0:
            path(u, tail)              # long tail below the deepest junction
            return
        junc.add(u)
        build(u, lev - 1)
        build(u, lev - 1)

    junc.add(0)
    build(0, kk - 1)
    build(0, kk - 1)
    return {u: sorted(vs) for u, vs in adj.items()}, 0, junc, down


def nested_drive(n_target, kk=5, ps=4, cls=HDynTreeFW):
    adj, seed, junc, down = nested_arena(kk, ps,
                                         tail=max(2 * n_target, 1000))
    mo = Model(adj, 0.25, seed)
    dt = cls(mo, Meter(adj))
    inS = {seed}

    def light_child(u):
        """admitted junction u: the down-child NOT on u's carved path
        (prefer an unstarted side so both sides exist)."""
        P = dt.paths[dt.pathof[u]]
        k = dt.posin[u]
        heavy = P.verts[k + 1] if k + 1 < P.size else None
        cand = [c for c in down[u] if c != heavy]
        if not cand:
            return down[u][0] if down[u] else None
        for c in cand:
            if c not in inS:
                return c
        return cand[0]

    admitted = 0
    stuck = 0
    while admitted < n_target and stuck < 3:
        u = seed
        step_done = False
        while True:
            c = light_child(u) if u in junc else \
                (down[u][0] if down[u] else None)
            if c is None:              # exhausted tail: give up this branch
                stuck += 1
                break
            if c not in inS:
                dt.admit(c, u)
                inS.add(c); admitted += 1
                step_done = True
                stuck = 0
                break
            u = c
        if not step_done and stuck >= 3:
            break
    return dt, admitted


# armed cascade: ladder of k junctions v_1..v_k; the arm at v_i (heavy: it
# is admitted first, as v_i's path continuation) has h_i = ceil(S_i/2), so
# every junction sits within 1 admission of its firing threshold once the
# spine below is fully built; a tip of <= 3 deep admissions then fires ALL k
# junctions (parity), concentrating Theta(n) moved into O(1) admissions.
def cascade(k=10, m0=40):
    S = [0] * (k + 2)
    h = [0] * (k + 2)
    S[k] = m0
    h[k] = (m0 + 1) // 2
    for i in range(k - 1, 0, -1):
        S[i] = 1 + h[i + 1] + S[i + 1]
        h[i] = (S[i] + 1) // 2
    adj = {0: []}
    nid = [1]

    def newv(p):
        v = nid[0]; nid[0] += 1
        adj[p].append(v); adj[v] = [p]
        return v

    order = []

    def path(p, L):
        for _ in range(L):
            p = newv(p); order.append(p)
        return p

    p = 0
    for i in range(1, k + 1):
        vi = newv(p); order.append(vi)            # junction v_i (light path
        path(vi, h[i])                            # under v_{i-1}); arm =
        p = vi                                    # v_i's heavy continuation
    tip = path(p, S[k])                           # tail: light path below v_k
    tips = [newv(tip)]                            # tip admissions (parity)
    for _ in range(2):
        tips.append(newv(tips[-1]))
    adjs = {u: sorted(vs) for u, vs in adj.items()}
    return adjs, 0, order, tips


def run_cascade(k=10, m0=40):
    adjs, seed, order, tips = cascade(k, m0)
    mo = Model(adjs, 0.25, seed)
    dt = HDynTreeFW(mo, Meter(adjs))
    inS = {seed}
    for v in order:
        par = [u for u in adjs[v] if u in inS]
        dt.admit(v, par[0])
        inS.add(v)
    pre_sw, pre_mv = dt.swaps, dt.swap_moved
    tipsw, tipmv, worst = [], [], 0
    for v in tips:
        s0, m0_ = dt.swaps, dt.swap_moved
        par = [u for u in adjs[v] if u in inS]
        dt.admit(v, par[0])
        inS.add(v)
        tipsw.append(dt.swaps - s0)
        tipmv.append(int(dt.swap_moved - m0_))
        worst = max(worst, dt.swap_moved - m0_)
    n = len(inS)
    return dict(n=n, k=k, pre_swaps=pre_sw, pre_moved=int(pre_mv),
                tip_swaps=tipsw, tip_moved=tipmv,
                worst_adm_moved=int(worst), worst_frac_n=worst / n,
                total_mv_n=dt.swap_moved / n)


# random families
def pa_tree(n, seed=1):
    rng = random.Random(seed)
    deg = [1, 1]
    adj = {0: [1], 1: [0]}
    ends = [0, 1]
    for v in range(2, n):
        u = ends[rng.randrange(len(ends))]
        adj[u].append(v); adj[v] = [u]
        ends.append(u); ends.append(v)
    return {u: sorted(vs) for u, vs in adj.items()}, 0


def rleaf_tree(n, seed=1):
    rng = random.Random(seed)
    adj = {0: [1], 1: [0]}
    leaves = [1]
    for v in range(2, n):
        i = rng.randrange(len(leaves))
        u = leaves[i]
        leaves[i] = leaves[-1]; leaves.pop()
        adj[u].append(v); adj[v] = [u]
        leaves.append(v)
    return {u: sorted(vs) for u, vs in adj.items()}, 0


def rand_order(adj, seed, rng):
    inS = {seed}
    front = list(adj[seed])
    out = []
    while front:
        i = rng.randrange(len(front))
        v = front.pop(i)
        if v in inS:
            continue
        inS.add(v); out.append(v)
        front.extend(w for w in adj[v] if w not in inS)
    return out


# ---------------------------------------------------- certificate on trees
def path_end_adversary(alpha, m=50, C=2.0):
    """Tree analog of I5-F's cycle adversary: path ending at distance ell
    beyond the truncation boundary vs a much longer path.  Both are TREES and
    agree on B_K(boundary) for K < ell.  Returns minimal ell with
    err_short/err_long <= C (=> any C-tight K-local certificate on trees
    needs K >= that ell)."""
    lam = (1 - math.sqrt(alpha)) / (1 + math.sqrt(alpha))
    Lmax = int(max(40, 12.0 / math.sqrt(alpha)))
    nlong = m + 6 * Lmax
    padj = {u: sorted({u - 1, u + 1} & set(range(nlong)))
            for u in range(nlong)}
    mo_l = Model(padj, alpha, 0)
    idx = np.arange(m)
    Qs = mo_l.Q[idx][:, idx].toarray()
    xh = np.linalg.solve(Qs, mo_l.b[idx])
    xhat_l = np.zeros(nlong); xhat_l[:m] = xh
    el = mo_l.semantic_err(xhat_l)
    out = []
    ellstar = None
    for ell in sorted(set(int(round(t)) for t in
                          np.geomspace(1, 4 * Lmax, 40))):
        ns = m + ell
        adx = {u: sorted({u - 1, u + 1} & set(range(ns))) for u in range(ns)}
        mo_s = Model(adx, alpha, 0)
        xhat_s = np.zeros(ns); xhat_s[:m] = xh   # same x_hat (same B_K data)
        es = mo_s.semantic_err(xhat_s)
        r = es / el
        out.append((ell, r))
        if r <= C and ellstar is None:
            ellstar = ell
    return dict(alpha=alpha, lam=lam, ellstar=ellstar,
                ellstar_sqrta=(ellstar or -1) * math.sqrt(alpha),
                curve=out[:12])


# ---------------------------------------------------------------- main
def main():
    res = {}
    t0 = time.time()

    print('== 1. FW correctness vs dense solves (small zoo) ==', flush=True)
    ok = []
    adjc, s = i2b.comb(6, 5)
    import test_dyn2 as td
    for tag, (adj, sd, order) in {
        'comb-bfs': (adjc, s, td.bfs_order(adjc, s)),
        'comb-teeth': td.comb_teeth_first(6, 5),
        'rrt120': (lambda a: (a[0], a[1],
                   rand_order(a[0], a[1], random.Random(3))))(i2b.rrt(120, 11)),
        'star40': ({0: list(range(1, 41)),
                    **{i: [0] for i in range(1, 41)}}, 0, list(range(1, 41))),
    }.items():
        for alpha in (0.25, 2.0 ** -8):
            d, dt = drive(adj, sd, order, HDynTreeFW, alpha, check_dense=40)
            ok.append((tag, alpha, d['dense_err']))
            assert d['dense_err'] < 1e-9, (tag, alpha, d['dense_err'])
            print(f"  {tag:12s} a={alpha:.4f} relerr={d['dense_err']:.1e} "
                  f"sw={d['swaps']} mv={d['moved']}", flush=True)
    res['fw_correct'] = [(t, a, float(e)) for t, a, e in ok]

    print('== 2. thrash(alternating), scaling ==', flush=True)
    rows = []
    for n in [2 ** k for k in range(10, 18)]:
        adj, sd, order, ssw, smv = thrash_alt(n)
        d, dt = drive(adj, sd, order)
        d['sim_swaps'], d['sim_moved'] = ssw, smv
        assert dt.swaps == ssw and dt.swap_moved == smv, \
            ('RULE MISMATCH', dt.swaps, ssw, dt.swap_moved, smv)
        rows.append(d)
        print(f"  n={d['n']:7d} sw={d['swaps']:3d} mv/n={d['mv_n']:.3f} "
              f"mv/(n lg n)={d['mv_nlog']:.4f} maxadm={d['maxadm']:6d} "
              f"lev={d['lev_mean']:.2f}/{d['lev_max']} "
              f"adm/(n lg^2)={d['adm_nlog2']:.2f}", flush=True)
    res['thrash_alt'] = rows

    print('== 3. thrash(nested, light-descent adversary), scaling ==',
          flush=True)
    rows = []
    for n in [1000, 2000, 4000, 8000, 16000]:
        dt, adm = nested_drive(n, kk=5, ps=4)
        lg = math.log2(max(adm, 2))
        am = dt.adm_moved
        d = dict(n=adm, swaps=dt.swaps, moved=int(dt.swap_moved),
                 mv_n=dt.swap_moved / adm, mv_nlog=dt.swap_moved / (adm * lg),
                 maxadm=int(max(am)), lev_mean=float(np.mean(dt.levels)),
                 lev_max=int(max(dt.levels)),
                 adm_nlog2=float(np.sum(dt.admit_nodes)) / (adm * lg * lg))
        rows.append(d)
        print(f"  n={adm:6d} sw={d['swaps']:4d} mv/n={d['mv_n']:.3f} "
              f"mv/(n lg n)={d['mv_nlog']:.4f} maxadm={d['maxadm']:6d} "
              f"lev={d['lev_mean']:.2f}/{d['lev_max']} "
              f"adm/(n lg^2)={d['adm_nlog2']:.2f}", flush=True)
    res['thrash_nested'] = rows

    print('== 4. armed cascade (worst single admission) ==', flush=True)
    rows = []
    for k, m0 in [(6, 40), (8, 40), (10, 40), (12, 40)]:
        try:
            d = run_cascade(k, m0)
            rows.append(d)
            print(f"  k={k:2d} n={d['n']:6d} pre_sw={d['pre_swaps']} "
                  f"tip fires/adm={d['tip_swaps']} moved/adm={d['tip_moved']} "
                  f"worst adm moved={d['worst_adm_moved']} "
                  f"(={d['worst_frac_n']:.2f} n)  total mv/n="
                  f"{d['total_mv_n']:.3f}", flush=True)
        except AssertionError as e:
            print(f"  k={k}: build assert {e}", flush=True)
    res['cascade'] = rows

    print('== 5. random tree families (final rule) ==', flush=True)
    rows = []
    for fam, fn in [('rrt', lambda sd: i2b.rrt(4000, sd)),
                    ('pa', lambda sd: pa_tree(4000, sd)),
                    ('rleaf', lambda sd: rleaf_tree(4000, sd))]:
        for sd in (7, 21):
            adj, s0 = fn(sd)
            order = rand_order(adj, s0, random.Random(sd))
            d, _ = drive(adj, s0, order)
            d['family'], d['seed'] = fam, sd
            rows.append(d)
            print(f"  {fam:6s} seed={sd:2d} n={d['n']} sw={d['swaps']:4d} "
                  f"mv/n={d['mv_n']:.3f} maxadm={d['maxadm']:5d} "
                  f"lev={d['lev_mean']:.2f}/{d['lev_max']} "
                  f"(bound {d['lev_bound']:.1f}) "
                  f"adm/(n lg^2)={d['adm_nlog2']:.2f}", flush=True)
    res['random'] = rows

    print('== 6. certificate on trees: path-end adversary ==', flush=True)
    rows = []
    for a in [2.0 ** -4, 2.0 ** -6, 2.0 ** -8, 2.0 ** -10, 2.0 ** -12]:
        d = path_end_adversary(a)
        rows.append(d)
        print(f"  a=2^{int(math.log2(a))}: minimal ell for factor-2 = "
              f"{d['ellstar']}  (ell*sqrt(a) = {d['ellstar_sqrta']:.3f})",
              flush=True)
    res['cert_tree'] = rows

    json.dump(res, open(OUT, 'w'))
    print(f'[{time.time()-t0:.1f}s] structural done -> {OUT}', flush=True)


if __name__ == '__main__':
    main()
