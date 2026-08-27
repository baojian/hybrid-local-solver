"""I7-B phase 6: adversarial sweep over graph families.

Per graph: exact (H-K) and (H-K1) kernel censuses, float mu2 -> in-class q,
then the PSI decision (complete pair enumeration n<=12, sampled pairs +
ascent for larger), plus a reachable-stage TK hunt (exact recurrence) on
graphs failing (H-K).

  (H-K)  : 4 vol ((3D-A)^{-1} D)^2_{ij} <= d_j   (i != j)   [Mm^2 kernel]
  (H-K1) : 2 vol ((3D-A)^{-1})_{ij}    <= 1      (i != j)   [Mm  kernel]
"""
import sys, time, json, itertools
import numpy as np
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import (GenInst, hypercube, petersen, cycle, circulant,
                        complete_bipartite, rook, cocktail, connected, _mk)
from i7b_hunt import build, psi_star, QS_matrix
from i7b_decide import signspace_feasible
from i7b_tk import tk_of, psi_terms

def kneser(m, k):
    from itertools import combinations
    Vs = list(combinations(range(m), k))
    n = len(Vs)
    E = [(i, j) for i in range(n) for j in range(i + 1, n)
         if not set(Vs[i]) & set(Vs[j])]
    return _mk(n, E)

def paley(p):
    QR = set((x * x) % p for x in range(1, p))
    return _mk(p, [(i, j) for i in range(p) for j in range(i + 1, p)
                   if (j - i) % p in QR or (i - j) % p in QR])

def shrikhande():
    # Cayley graph on Z4 x Z4 with S = {+-(1,0), +-(0,1), +-(1,1)}
    S = [(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)]
    idx = lambda a, b: 4 * a + b
    E = []
    for a in range(4):
        for b in range(4):
            for da, db in S:
                E.append((idx(a, b), idx((a + da) % 4, (b + db) % 4)))
    return _mk(16, [(u, v) for u, v in E if u < v])

def rand_regular(n, r, seed):
    rng = np.random.default_rng(seed)
    for att in range(600):
        stubs = np.repeat(np.arange(n), r)
        rng.shuffle(stubs)
        E = set()
        ok = True
        for k in range(0, len(stubs), 2):
            u, v = int(stubs[k]), int(stubs[k + 1])
            if u == v or (min(u, v), max(u, v)) in E:
                ok = False; break
            E.add((min(u, v), max(u, v)))
        if ok:
            adj = _mk(n, list(E))
            if connected(adj):
                return adj
    return None

# ---------------------------------------------------------- kernel censuses
def kernel_census(adj):
    n = len(adj)
    d = [Fr(len(adj[i])) for i in range(n)]
    vol = sum(d)
    T = [[Fr(3) * d[i] if i == j else Fr(0) for j in range(n)]
         for i in range(n)]
    for i in range(n):
        for j in adj[i]:
            T[i][j] -= 1
    # invert T exactly
    A = [row[:] + [Fr(1) if k == i else Fr(0) for k in range(n)]
         for i, row in enumerate(T)]
    m = n
    for c in range(m):
        p = next(r for r in range(c, m) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(m):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [A[r][k] - f * A[c][k] for k in range(2 * m)]
    Tinv = [row[m:] for row in A]
    hk1 = max(2 * vol * Tinv[i][j] for i in range(n) for j in range(n)
              if i != j)
    Nm = [[Tinv[i][j] * d[j] for j in range(n)] for i in range(n)]
    # (N^2)_{ij} needed only to find the max ratio: compute full product
    worst = Fr(0)
    for i in range(n):
        row = [sum(Nm[i][k] * Nm[k][j] for k in range(n)) for j in range(n)]
        for j in range(n):
            if i != j:
                worst = max(worst, 4 * vol * row[j] / d[j])
    return float(hk1), float(worst)

def mu2_float(adj):
    n = len(adj)
    d = np.array([len(a) for a in adj], float)
    L = np.diag(d)
    for i in range(n):
        for j in adj[i]:
            L[i, j] -= 1
    Dm = np.diag(1 / np.sqrt(d))
    ev = np.linalg.eigvalsh(Dm @ L @ Dm)
    return ev[1], ev[-1]

QCAND = [Fr(1, k) for k in (4, 5, 6, 8, 10, 12, 16, 20, 25, 30, 40, 50, 64,
                            80, 100)]

def pick_q(mu2):
    for q in QCAND:
        if 2 * float(q) <= mu2 * 0.999:
            return q
    return None

# ------------------------------------------------------------- PSI decision
def decide_pairs(ctx, adj, pairs_iter, npairs_label, tol=1e-11):
    n = ctx['n']
    QS_cache = {}
    n_mixed = n_poslam = 0
    violations, near = [], []
    for P, N in pairs_iter:
        if not P or not N:
            continue
        n_mixed += 1
        key = N
        if key not in QS_cache:
            if len(QS_cache) > 250000:
                QS_cache.clear()
            QS_cache[key] = QS_matrix(ctx, N)
        idx = sorted(P | N)
        B = QS_cache[key][np.ix_(idx, idx)]
        ev, V = np.linalg.eigh(B)
        if ev[-1] <= tol:
            continue
        pos = [k for k in range(len(ev)) if ev[k] > tol]
        used = set()
        for k in pos:
            if k in used:
                continue
            cols = [j for j in pos if abs(ev[j] - ev[k]) < 1e-8]
            used.update(cols)
            n_poslam += 1
            c = signspace_feasible(V[:, cols], P, N, idx)
            if c is not None:
                y = np.zeros(n)
                yr = V[:, cols] @ c
                for kk, i in enumerate(idx):
                    y[i] = yr[kk]
                tv = psi_star(ctx, y / np.linalg.norm(y))
                (violations if tv > tol else near).append(
                    (sorted(P), sorted(N), float(ev[k]), float(tv)))
    return n_mixed, n_poslam, violations, near

def all_pairs(n):
    for assign in itertools.product((0, 1, 2), repeat=n):
        yield (frozenset(i for i, a in enumerate(assign) if a == 1),
               frozenset(i for i, a in enumerate(assign) if a == 2))

def sampled_pairs(n, adj, count, rng):
    yield from ()
    # structured: adjacent pairs, stars, spheres
    for i in range(n):
        Nb = frozenset(adj[i])
        yield frozenset([i]), Nb
        yield Nb, frozenset([i])
        for j in adj[i]:
            yield frozenset([i]), frozenset([j])
    for _ in range(count):
        a = rng.integers(0, 3, size=n)
        yield (frozenset(np.flatnonzero(a == 1).tolist()),
               frozenset(np.flatnonzero(a == 2).tolist()))

def ascent_max(ctx, adj, restarts=250):
    n = ctx['n']
    rng = np.random.default_rng(17)
    best = -np.inf
    f = lambda y: psi_star(ctx, y)
    starts = [rng.standard_normal(n) for _ in range(restarts)]
    for i in range(min(n, 8)):
        e = np.zeros(n); e[i] = 1
        for j in adj[i][:3]:
            v = e.copy(); v[j] = -1
            starts += [v, -v]
    for y0 in starts:
        y = y0 / np.linalg.norm(y0)
        val, step = f(y), 0.3
        for it in range(220):
            g = np.zeros(n); f0 = f(y)
            for i in range(n):
                y2 = y.copy(); y2[i] += 1e-7
                g[i] = (f(y2) - f0) / 1e-7
            g -= y * (g @ y)
            y2 = y + step * g
            y2 /= np.linalg.norm(y2)
            v2 = f(y2)
            if v2 > val + 1e-15:
                y, val = y2, v2
                step = min(step * 1.25, 1.0)
            else:
                step *= 0.5
                if step < 1e-9:
                    break
        best = max(best, val)
    return best

def reachable_tk_hunt(adj, q, T=16):
    """Run exact recurrences (3 seeds); record min TK and max Psi at
    correcting stages (exact sign via Fractions)."""
    n = len(adj)
    dmax = max(len(a) for a in adj)
    out = []
    seeds = [[Fr(1, n)] * n,
             [Fr(1, 2)] + [Fr(1, 2 * (n - 1))] * (n - 1),
             [Fr(2, 3)] + [Fr(1, 3 * (n - 1))] * (n - 1)]
    minTK, maxPsi, ncorr = None, None, 0
    for s in seeds:
        rho = min(s) / (2 * dmax)
        I = GenInst(adj, s, q, rho)
        if not (I.H0 and I.interior):
            continue
        try:
            recs, xs = I.run(T, diag=False)
        except AssertionError:
            continue
        d, vol, be = I.d, I.vol, I.beta
        from i7b_tk import proj
        E = [[I.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
        for t in range(1, T - 1):
            rec = recs[t]
            if rec['cls'] == 'N':
                continue
            ncorr += 1
            y = [be * rec['dt'][i] - rec['Delta'] for i in range(n)]
            h = proj(d, vol, E[t + 1])
            tk = tk_of(I, y)
            _, _, Psi = psi_terms(I, y, h)
            minTK = tk if minTK is None else min(minTK, tk)
            maxPsi = Psi if maxPsi is None else max(maxPsi, Psi)
    return (ncorr, None if minTK is None else float(minTK),
            None if maxPsi is None else float(maxPsi))

def sweep_one(name, adj, force_q=None, do_kernel=True, tkhunt=False):
    n = len(adj)
    t0 = time.time()
    mu2, mumax = mu2_float(adj)
    q = force_q or pick_q(mu2)
    if q is None:
        print('%-18s n=%3d mu2=%.4f  NO in-class q in candidate list' %
              (name, n, mu2))
        return None
    hk1 = hk = None
    if do_kernel:
        hk1, hk = kernel_census(adj)
    ctx = build(adj, str(q))
    mode, viol, near, nm, npl = None, [], [], 0, 0
    if n <= 12:
        nm, npl, viol, near = decide_pairs(ctx, adj, all_pairs(n), 'all')
        mode = 'complete(3^%d)' % n
    else:
        rng = np.random.default_rng(23)
        cnt = 120000 if n <= 20 else 30000
        nm, npl, viol, near = decide_pairs(
            ctx, adj, sampled_pairs(n, adj, cnt, rng), 'sampled')
        mode = 'sampled(%d)' % nm
    asc = ascent_max(ctx, adj, restarts=120 if n <= 20 else 50)
    tk = None
    if tkhunt:
        tk = reachable_tk_hunt(adj, q)
    status = 'VIOLATED' if viol else 'SUP<=0'
    print('%-18s n=%3d mu2=%.4f q=%-5s HK1=%.3f HK=%.3f  %s %s '
          'poslam=%d asc=%+.1e %s tk=%s [%.0fs]' %
          (name, n, mu2, q, hk1 if hk1 is not None else float('nan'),
           hk if hk is not None else float('nan'), mode, status, npl, asc,
           '' if not viol else 'VIOL!', tk, time.time() - t0))
    return dict(name=name, n=n, mu2=float(mu2), q=str(q), hk1=hk1, hk=hk,
                mode=mode, status=status, n_poslam=npl, ascent=float(asc),
                violations=viol[:5], tkhunt=tk)

if __name__ == '__main__':
    res = []
    jobs = []
    for nn in (8, 10, 12, 14, 16):
        jobs.append(('Circ%d(1,2)' % nn, circulant(nn, (1, 2)), None,
                     True, nn <= 14))
    jobs += [
        ('Q5', hypercube(5), None, True, True),
        ('Q6', hypercube(6), None, True, False),
        ('Kneser(6,2)', kneser(6, 2), None, True, True),
        ('Kneser(7,3)', kneser(7, 3), None, True, False),
        ('Paley13', paley(13), None, True, True),
        ('Paley17', paley(17), None, True, False),
        ('Shrikhande', shrikhande(), None, True, True),
        ('T(5)=compl(Pet)', _mk(10, [(i, j) for i in range(10)
                    for j in range(i + 1, 10)
                    if j not in petersen()[i]]), None, True, True),
        ('RR(12,3)', rand_regular(12, 3, 5), None, True, True),
        ('RR(14,4)', rand_regular(14, 4, 7), None, True, True),
        ('RR(16,3)', rand_regular(16, 3, 11), None, True, True),
        ('RR(18,4)', rand_regular(18, 4, 13), None, True, False),
        ('RR(20,3)', rand_regular(20, 3, 17), None, True, False),
        ('C14', cycle(14), None, True, True),
        ('C16', cycle(16), None, True, False),
    ]
    for name, adj, fq, dk, th in jobs:
        if adj is None:
            print('%-18s generation failed' % name); continue
        try:
            r = sweep_one(name, adj, fq, dk, th)
            if r:
                res.append(r)
        except Exception as ex:
            print('%-18s EXC %s' % (name, ex))
    json.dump(res, open('/home/claude/work/overnight/w7_windowed/'
                        'i7b_sweep.json', 'w'), indent=1, default=str)
    print('saved i7b_sweep.json')
