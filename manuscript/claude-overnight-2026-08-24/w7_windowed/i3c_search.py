"""I3-C: mass violation hunt for the named Perron-truncation inequality.

Setting (project coordinates).
  Hat coords xh = D^{-1/2} x ;  Qt = D^{1/2} Q D^{1/2} ;  M := D^{-1} Qt.
  M is D-self-adjoint,  M 1 = alpha 1  (slow mode = CONSTANTS in hat coords).
  Back in x-coords the same operator is Q (plain-symmetric) and the slow
  eigenvector is v = D^{1/2} 1  (v_i = sqrt(d_i)),  Q v = alpha v.
  The engine's retraction is  rh_i = min(beta dh_i, Delta)  in HAT coords,
  i.e.  r_i = min(beta d_i, Delta v_i)  in x-coords  ==>  cap = Delta*v.

Variants tested (all with u >= 0, Delta > 0):
  V1  NAMED : P = I - v v^T/|v|^2 (Euclidean, x-coords), cap Delta*v.
              == D-orth projector onto 1^perp_D with ||.||_D in hat coords.
  V2  MISALIGNED CAP : same P/norm but cap Delta*1 (x-coords) -- what the
              i2c note feared.
  V3  WRONG PROJECTOR: cap Delta*v but P0 = I - 11^T/n, Euclidean.
  V4  Q-WEIGHTED NORM: cap Delta*v, projector P, but norm ||.||_Q.
  V5  D-WEIGHTED-in-x norm: cap Delta*v, projector P, norm ||.||_D (x-coords).
  V6  NAMED with a general coordinatewise 1-Lipschitz phi in w=u/v coords
              (soft-threshold / two-sided clip), P and Euclidean norm.
"""
import numpy as np, json, sys, math, time

rng = np.random.default_rng(20260824)

# ------------------------------------------------------------------ graphs
def adj_complete(n):
    A = np.ones((n, n)); np.fill_diagonal(A, 0); return A

def adj_path(n):
    A = np.zeros((n, n))
    for i in range(n - 1): A[i, i + 1] = A[i + 1, i] = 1
    return A

def adj_cycle(n):
    A = adj_path(n); A[0, n - 1] = A[n - 1, 0] = 1; return A

def adj_star(n):
    A = np.zeros((n, n)); A[0, 1:] = 1; A[1:, 0] = 1; return A

def adj_tree(n):                      # uniform random labelled tree (Prufer)
    A = np.zeros((n, n))
    if n == 2:
        A[0, 1] = A[1, 0] = 1; return A
    pr = rng.integers(0, n, size=n - 2)
    deg = np.ones(n, int)
    for x in pr: deg[x] += 1
    import heapq
    leaves = [i for i in range(n) if deg[i] == 1]; heapq.heapify(leaves)
    pr = list(pr)
    for x in pr:
        lf = heapq.heappop(leaves)
        A[lf, x] = A[x, lf] = 1
        deg[x] -= 1
        if deg[x] == 1: heapq.heappush(leaves, x)
    u, v = [i for i in range(n) if deg[i] == 1 and A[i].sum() == 0][:2] \
        if False else (heapq.heappop(leaves), heapq.heappop(leaves))
    A[u, v] = A[v, u] = 1
    return A

def adj_er(n, p):
    A = (rng.random((n, n)) < p).astype(float)
    A = np.triu(A, 1); A = A + A.T
    # force connectivity by adding a random spanning path
    perm = rng.permutation(n)
    for i in range(n - 1):
        a, b = perm[i], perm[i + 1]; A[a, b] = A[b, a] = 1
    return A

def adj_regular(n, k):
    # circulant k-regular (k even) or +perfect matching
    A = np.zeros((n, n))
    for s in range(1, k // 2 + 1):
        for i in range(n):
            j = (i + s) % n; A[i, j] = A[j, i] = 1
    if k % 2 == 1 and n % 2 == 0:
        for i in range(n // 2): A[i, i + n // 2] = A[i + n // 2, i] = 1
    return A

def adj_barbell(m):
    n = 2 * m + 1
    A = np.zeros((n, n))
    A[:m, :m] = 1; A[m + 1:, m + 1:] = 1; np.fill_diagonal(A, 0)
    A[m - 1, m] = A[m, m - 1] = 1; A[m, m + 1] = A[m + 1, m] = 1
    return A

def adj_broom(nh, nt):                # star with nh leaves + path of nt
    n = nh + nt + 1; A = np.zeros((n, n))
    for i in range(1, nh + 1): A[0, i] = A[i, 0] = 1
    prev = 0
    for i in range(nh + 1, n):
        A[prev, i] = A[i, prev] = 1; prev = i
    return A

def adj_caterpillar(m, k):            # path of m, each with k pendant leaves
    n = m * (1 + k); A = np.zeros((n, n))
    for i in range(m - 1): A[i, i + 1] = A[i + 1, i] = 1
    idx = m
    for i in range(m):
        for _ in range(k):
            A[i, idx] = A[idx, i] = 1; idx += 1
    return A

def adj_doublestar(a, b):
    n = a + b + 2; A = np.zeros((n, n))
    A[0, 1] = A[1, 0] = 1
    for i in range(2, 2 + a): A[0, i] = A[i, 0] = 1
    for i in range(2 + a, n): A[1, i] = A[i, 1] = 1
    return A

def zoo():
    G = []
    for n in (3, 4, 6, 8, 12, 20):
        G += [('K%d' % n, adj_complete(n)), ('P%d' % n, adj_path(n)),
              ('C%d' % n, adj_cycle(n)), ('S%d' % n, adj_star(n))]
    G += [('P24', adj_path(24)), ('S30', adj_star(30))]
    for m in (4, 6, 8): G.append(('barbell%d' % m, adj_barbell(m)))
    for (a, b) in ((2, 8), (1, 15), (12, 12)): G.append(('dstar%d_%d' % (a, b), adj_doublestar(a, b)))
    for (h, t) in ((10, 6), (20, 3), (3, 20)): G.append(('broom%d_%d' % (h, t), adj_broom(h, t)))
    for (m, k) in ((6, 2), (8, 1), (4, 6)): G.append(('cat%d_%d' % (m, k), adj_caterpillar(m, k)))
    for k in (3, 4, 6): G.append(('reg%d_%d' % (14, k), adj_regular(14, k)))
    for _ in range(30):
        n = int(rng.integers(3, 26)); G.append(('rtree%d' % n, adj_tree(n)))
    for _ in range(30):
        n = int(rng.integers(4, 26)); p = float(rng.uniform(0.08, 0.6))
        G.append(('er%d' % n, adj_er(n, p)))
    return G

# ------------------------------------------------------------------ sampler
def sample_u(n, m, kind):
    if kind == 0:  return rng.random((m, n))
    if kind == 1:  return rng.exponential(1.0, (m, n))
    if kind == 2:  return np.exp(rng.normal(0, 3.0, (m, n)))       # heavy tail
    if kind == 3:  return (rng.random((m, n)) < 0.3) * rng.random((m, n))
    if kind == 4:  return np.abs(rng.normal(0, 1, (m, n))) ** 4
    if kind == 5:  return rng.integers(0, 4, (m, n)).astype(float)  # ties
    return rng.random((m, n))

def run(nsamp_per_graph=6000, out=None):
    graphs = zoo()
    worst = {k: (1e18, None) for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6')}
    ratios = {k: 0.0 for k in worst}                # worst  ||P phi(u)||/||P u||
    counts = {k: [0, 0] for k in worst}             # [violations, tested]
    alpha_list = [1e-4, 1e-2, 0.1]
    tot = 0
    for gi, (name, A) in enumerate(graphs):
        n = A.shape[0]
        d = A.sum(1)
        if d.min() <= 0: continue
        v = np.sqrt(d)                              # Perron vector of Q
        vol = d.sum()
        nv2 = vol                                   # |v|^2 = sum d_i
        one = np.ones(n)
        # Q in x-coords, for V4
        Dm12 = 1.0 / v
        Lsym = np.eye(n) - (Dm12[:, None] * A * Dm12[None, :])
        for kind in range(6):
            m = nsamp_per_graph // 6
            U = sample_u(n, m, kind)
            W = U / v                                # w = u/v
            # Delta sampling: mix of quantiles of w and uniform
            mode = rng.integers(0, 3, m)
            qs = rng.random(m)
            Wsort = np.sort(W, axis=1)
            idx = np.clip((qs * n).astype(int), 0, n - 1)
            Dl = Wsort[np.arange(m), idx] * (0.5 + rng.random(m))
            Du = W.max(1) * rng.random(m)
            Dm = W.min(1) + (W.max(1) - W.min(1)) * rng.random(m)
            Delta = np.where(mode == 0, Dl, np.where(mode == 1, Du, Dm))
            Delta = np.maximum(Delta, 1e-14)
            # ---- V1 named
            Z = np.minimum(U, Delta[:, None] * v[None, :])
            def PE(X, vec, nrm2):                    # Euclidean proj orth vec
                c = (X @ vec) / nrm2
                return X - c[:, None] * vec[None, :]
            pu = PE(U, v, nv2); pz = PE(Z, v, nv2)
            a = np.sqrt((pu ** 2).sum(1)); b = np.sqrt((pz ** 2).sum(1))
            gap = a - b
            k = 'V1'; counts[k][1] += m; counts[k][0] += int((gap < -1e-12 * np.maximum(a, 1)).sum())
            j = int(np.argmin(gap))
            if gap[j] < worst[k][0]: worst[k] = (float(gap[j]), (name, kind, j, float(a[j]), float(b[j])))
            rr = np.where(a > 1e-14, b / np.maximum(a, 1e-300), 0.0)
            ratios[k] = max(ratios[k], float(rr.max()))
            # ---- V2 misaligned cap (Delta*1 in x-coords)
            Z2 = np.minimum(U, Delta[:, None] * one[None, :] * v.mean())
            pz2 = PE(Z2, v, nv2); b2 = np.sqrt((pz2 ** 2).sum(1))
            k = 'V2'; g2 = a - b2
            counts[k][1] += m; counts[k][0] += int((g2 < -1e-12 * np.maximum(a, 1)).sum())
            j = int(np.argmin(g2))
            if g2[j] < worst[k][0]: worst[k] = (float(g2[j]), (name, kind, j, float(a[j]), float(b2[j])))
            rr = np.where(a > 1e-14, b2 / np.maximum(a, 1e-300), 0.0)
            ratios[k] = max(ratios[k], float(rr.max()))
            # ---- V3 wrong (plain) projector, correct cap
            pu3 = PE(U, one, float(n)); pz3 = PE(Z, one, float(n))
            a3 = np.sqrt((pu3 ** 2).sum(1)); b3 = np.sqrt((pz3 ** 2).sum(1))
            k = 'V3'; g3 = a3 - b3
            counts[k][1] += m; counts[k][0] += int((g3 < -1e-12 * np.maximum(a3, 1)).sum())
            j = int(np.argmin(g3))
            if g3[j] < worst[k][0]: worst[k] = (float(g3[j]), (name, kind, j, float(a3[j]), float(b3[j])))
            rr = np.where(a3 > 1e-14, b3 / np.maximum(a3, 1e-300), 0.0)
            ratios[k] = max(ratios[k], float(rr.max()))
            # ---- V4 Q-weighted norm (worst over alphas)
            for al in alpha_list:
                Qm = al * np.eye(n) + (1 - al) / 2 * Lsym
                qa = np.einsum('ij,jk,ik->i', pu, Qm, pu)
                qb = np.einsum('ij,jk,ik->i', pz, Qm, pz)
                qa = np.sqrt(np.maximum(qa, 0)); qb = np.sqrt(np.maximum(qb, 0))
                k = 'V4'; g4 = qa - qb
                counts[k][1] += m; counts[k][0] += int((g4 < -1e-12 * np.maximum(qa, 1)).sum())
                j = int(np.argmin(g4))
                if g4[j] < worst[k][0]:
                    worst[k] = (float(g4[j]), (name, kind, j, float(qa[j]), float(qb[j]), al))
                rr = np.where(qa > 1e-14, qb / np.maximum(qa, 1e-300), 0.0)
                ratios[k] = max(ratios[k], float(rr.max()))
            # ---- V5 D-weighted-in-x norm with correct P and cap
            da = np.sqrt((pu ** 2 * d[None, :]).sum(1))
            db = np.sqrt((pz ** 2 * d[None, :]).sum(1))
            k = 'V5'; g5 = da - db
            counts[k][1] += m; counts[k][0] += int((g5 < -1e-12 * np.maximum(da, 1)).sum())
            j = int(np.argmin(g5))
            if g5[j] < worst[k][0]: worst[k] = (float(g5[j]), (name, kind, j, float(da[j]), float(db[j])))
            rr = np.where(da > 1e-14, db / np.maximum(da, 1e-300), 0.0)
            ratios[k] = max(ratios[k], float(rr.max()))
            # ---- V6 general 1-Lipschitz phi in w coords: two-sided clip + soft-thr
            lo = Delta * rng.random(m); hi = lo + (W.max(1) - lo) * rng.random(m)
            thr = Delta * rng.random(m)
            W6 = np.where(rng.random(m)[:, None] < 0.5,
                          np.clip(W, lo[:, None], hi[:, None]),
                          np.sign(W) * np.maximum(np.abs(W) - thr[:, None], 0))
            Z6 = W6 * v[None, :]
            pz6 = PE(Z6, v, nv2); b6 = np.sqrt((pz6 ** 2).sum(1))
            k = 'V6'; g6 = a - b6
            counts[k][1] += m; counts[k][0] += int((g6 < -1e-11 * np.maximum(a, 1)).sum())
            j = int(np.argmin(g6))
            if g6[j] < worst[k][0]: worst[k] = (float(g6[j]), (name, kind, j, float(a[j]), float(b6[j])))
            rr = np.where(a > 1e-14, b6 / np.maximum(a, 1e-300), 0.0)
            ratios[k] = max(ratios[k], float(rr.max()))
            tot += m
    return dict(worst={k: (w[0], w[1]) for k, w in worst.items()},
                ratios=ratios, counts=counts, total=tot,
                ngraphs=len(graphs))

if __name__ == '__main__':
    t0 = time.time()
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    agg = None
    for _ in range(reps):
        r = run()
        if agg is None: agg = r
        else:
            for k in r['ratios']:
                if r['worst'][k][0] < agg['worst'][k][0]: agg['worst'][k] = r['worst'][k]
                agg['ratios'][k] = max(agg['ratios'][k], r['ratios'][k])
                agg['counts'][k][0] += r['counts'][k][0]
                agg['counts'][k][1] += r['counts'][k][1]
            agg['total'] += r['total']
    print("graphs=%d  samples/variant=%d  (%.1fs)" %
          (agg['ngraphs'], agg['counts']['V1'][1], time.time() - t0))
    lab = {'V1': 'NAMED  P=I-vv^T/|v|^2, Euclid, cap D*v',
           'V2': 'cap Delta*1 (misaligned)              ',
           'V3': 'plain projector I-11^T/n              ',
           'V4': 'Q-weighted norm                       ',
           'V5': 'D-weighted-in-x norm                  ',
           'V6': 'general 1-Lipschitz phi in w=u/v      '}
    for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6'):
        c = agg['counts'][k]
        print("  %-4s %s viol=%8d/%9d  min(||Pu||-||Pz||)=%+.3e  max ratio=%.6f"
              % (k, lab[k], c[0], c[1], agg['worst'][k][0], agg['ratios'][k]))
        print("        worst at %s" % (agg['worst'][k][1],))
    json.dump(agg, open('/home/claude/work/overnight/w7_windowed/i3c_search.json', 'w'),
              indent=1, default=str)
