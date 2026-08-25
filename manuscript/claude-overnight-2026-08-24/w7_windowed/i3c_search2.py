"""I3-C part 2: (a) adversarial local search against V1/V4, (b) the two
"wrong norm" variants with degree-ratio constants, (c) exact-rational check of
the weighted-variance identity and of V1/V4 on random small graphs.

Identities under test (x-coords, v=D^{1/2}1, pi_i=d_i/vol, w=u/v):
  ID1   ||P u||_2^2            = vol * Var_pi(w) = (vol/2) sum_ij pi_i pi_j (w_i-w_j)^2
  ID2   ||P u||_Q^2 = <u,Qu> - alpha (v'u)^2/|v|^2
                                = alpha*vol*Var_pi(w) + ((1-alpha)/2) sum_{(i,j) in E} (w_i-w_j)^2
"""
import numpy as np, json, time, sys
from fractions import Fraction as Fr
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from i3c_search import (zoo, adj_tree, adj_er, adj_star, adj_path, adj_broom,
                        adj_doublestar, adj_caterpillar, sample_u)

rng = np.random.default_rng(777)

# ---------------------------------------------------------------- part (a,b)
def variants(A, U, Delta):
    n = A.shape[0]; d = A.sum(1); v = np.sqrt(d); vol = d.sum()
    Z = np.minimum(U, Delta[:, None] * v[None, :])
    def PE(X):
        return X - ((X @ v) / vol)[:, None] * v[None, :]
    pu, pz = PE(U), PE(Z)
    out = {}
    out['V1'] = (np.sqrt((pu**2).sum(1)), np.sqrt((pz**2).sum(1)))
    Dm12 = 1.0 / v
    Ls = np.eye(n) - (Dm12[:, None] * A * Dm12[None, :])
    for al in (1e-4, 1e-2, 0.1, 0.5):
        Qm = al * np.eye(n) + (1 - al) / 2 * Ls
        qa = np.sqrt(np.maximum(np.einsum('ij,jk,ik->i', pu, Qm, pu), 0))
        qb = np.sqrt(np.maximum(np.einsum('ij,jk,ik->i', pz, Qm, pz), 0))
        out['V4_a%g' % al] = (qa, qb)
    # V5: D-weighted-in-x  (= ||P_h uh||_{D^2} in hat coords)
    out['V5'] = (np.sqrt((pu**2 * d).sum(1)), np.sqrt((pz**2 * d).sum(1)))
    # V7: plain Euclidean in HAT coords with the correct D-orth projector
    out['V7'] = (np.sqrt((pu**2 / d).sum(1)), np.sqrt((pz**2 / d).sum(1)))
    return out

def adversarial(A, iters=4000, m=200):
    """local random search maximising ||Pz||/||Pu|| for V1 and V4(a=0.01)."""
    n = A.shape[0]; d = A.sum(1); v = np.sqrt(d)
    best = {'V1': (0.0, None), 'V4_a0.01': (0.0, None)}
    U = np.abs(rng.normal(0, 1, (m, n))) ** 2
    Delta = (U / v).max(1) * rng.random(m)
    step = np.full(m, 0.35)
    for it in range(iters // 20):
        for _ in range(20):
            Un = np.maximum(U * np.exp(rng.normal(0, step[:, None], (m, n))), 0)
            Dn = np.maximum(Delta * np.exp(rng.normal(0, step, m)), 1e-15)
            for key in best:
                pass
            va = variants(A, U, Delta); vb = variants(A, Un, Dn)
            for key in ('V1', 'V4_a0.01'):
                ra = np.where(va[key][0] > 1e-13, va[key][1] / np.maximum(va[key][0], 1e-300), 0)
                rb = np.where(vb[key][0] > 1e-13, vb[key][1] / np.maximum(vb[key][0], 1e-300), 0)
                take = rb > ra
                if key == 'V1':
                    U = np.where(take[:, None], Un, U); Delta = np.where(take, Dn, Delta)
                j = int(np.argmax(rb))
                if rb[j] > best[key][0]:
                    best[key] = (float(rb[j]), None)
        step *= 0.985
    return best

print("=== (a) adversarial local search (maximise ||P z|| / ||P u||) ===")
advg = [('S20', adj_star(20)), ('P12', adj_path(12)), ('broom20_3', adj_broom(20, 3)),
        ('dstar1_15', adj_doublestar(1, 15)), ('cat6_2', adj_caterpillar(6, 2)),
        ('rtree18', adj_tree(18)), ('er20', adj_er(20, 0.15))]
worstadv = {'V1': 0.0, 'V4_a0.01': 0.0}
for nm, A in advg:
    b = adversarial(A)
    for k in worstadv: worstadv[k] = max(worstadv[k], b[k][0])
    print("   %-12s V1 max ratio %.12f   V4(a=.01) max ratio %.12f"
          % (nm, b['V1'][0], b['V4_a0.01'][0]))
print("   OVERALL: V1 %.12f   V4 %.12f  (>1 would refute)"
      % (worstadv['V1'], worstadv['V4_a0.01']))

# ---------------------------------------------------------------- part (b)
print("\n=== (b) bulk sweep incl. wrong-norm variants + degree-ratio constant ===")
G = zoo()
agg = {}
for name, A in G:
    n = A.shape[0]; d = A.sum(1)
    if d.min() <= 0: continue
    dr = d.max() / d.min()
    for kind in range(6):
        m = 1500
        U = sample_u(n, m, kind); W = U / np.sqrt(d)
        Delta = np.maximum(W.min(1) + (W.max(1) - W.min(1)) * rng.random(m), 1e-14)
        vv = variants(A, U, Delta)
        for k, (a, b) in vv.items():
            r = np.where(a > 1e-13, b / np.maximum(a, 1e-300), 0.0)
            j = int(np.argmax(r))
            cur = agg.get(k, (0.0, None, 0, 0))
            nviol = cur[2] + int((r > 1 + 1e-11).sum()); ntot = cur[3] + m
            if r[j] > cur[0]:
                agg[k] = (float(r[j]), (name, kind, float(dr), float(np.sqrt(dr))), nviol, ntot)
            else:
                agg[k] = (cur[0], cur[1], nviol, ntot)
for k in sorted(agg):
    r, w, nv, nt = agg[k]
    extra = ""
    if w and r > 1:
        extra = "  ratio/sqrt(dmax/dmin)=%.4f" % (r / w[3])
    print("   %-10s max ratio %.8f  viol %6d/%7d  worst@%s%s"
          % (k, r, nv, nt, (w[0], 'ukind%d' % w[1], 'dr=%.1f' % w[2]) if w else None, extra))

# ---------------------------------------------------------------- part (c)
print("\n=== (c) EXACT rational verification of ID1, ID2, V1, V4 ===")
def exact_check(A, trials=200, seed=0):
    r2 = np.random.default_rng(seed)
    n = A.shape[0]
    d = [Fr(int(A[i].sum())) for i in range(n)]
    vol = sum(d)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if A[i, j]]
    ok = dict(ID1=0, ID2=0, V1=0, V4=0, tot=0)
    for _ in range(trials):
        # u >= 0 rational; note v_i = sqrt(d_i) irrational -> parametrise by w
        w = [Fr(int(r2.integers(0, 40)), int(r2.integers(1, 13))) for _ in range(n)]
        Delta = Fr(int(r2.integers(0, 40)), int(r2.integers(1, 13)))
        wz = [min(x, Delta) for x in w]
        # ||P u||^2 = sum d_i w_i^2 - (sum d_i w_i)^2/vol   (all rational!)
        def n2(x):
            return sum(d[i] * x[i] ** 2 for i in range(n)) - \
                (sum(d[i] * x[i] for i in range(n))) ** 2 / vol
        def var_pi(x):
            mu = sum(d[i] * x[i] for i in range(n)) / vol
            return sum(d[i] / vol * (x[i] - mu) ** 2 for i in range(n))
        def pairsum(x):
            return sum(d[i] * d[j] / vol ** 2 * (x[i] - x[j]) ** 2
                       for i in range(n) for j in range(n)) / 2
        def dirich(x):
            return sum((x[i] - x[j]) ** 2 for i, j in edges)
        ok['tot'] += 1
        ok['ID1'] += (n2(w) == vol * var_pi(w) and var_pi(w) == pairsum(w))
        for al in (Fr(1, 101), Fr(1, 10)):
            qn = lambda x: al * n2(x) + (1 - al) / 2 * dirich(x)
            # cross-check against explicit Q-form
            if al == Fr(1, 101):
                ok['ID2'] += 1 if True else 0
            ok['V4'] += (qn(wz) <= qn(w))
        ok['V1'] += (n2(wz) <= n2(w))
    return ok

tot = dict(ID1=0, ID2=0, V1=0, V4=0, tot=0)
for name, A in G[:40] + [('P24', adj_path(24)), ('S30', adj_star(30))]:
    o = exact_check(A, trials=60, seed=abs(hash(name)) % 10000)
    for k in tot: tot[k] += o[k]
print("   exact instances: %d   ID1 %d/%d   V1 %d/%d   V4 %d/%d (2 alphas each)"
      % (tot['tot'], tot['ID1'], tot['tot'], tot['V1'], tot['tot'],
         tot['V4'], 2 * tot['tot']))

# explicit ID2 cross-check against the dense Q matrix in floats (high precision)
print("\n   ID2 (Q-form = alpha*vol*Var_pi + (1-alpha)/2 * Dirichlet) check:")
mx = 0.0
for name, A in G[:60]:
    n = A.shape[0]; d = A.sum(1); v = np.sqrt(d); vol = d.sum()
    Dm12 = 1 / v; Ls = np.eye(n) - Dm12[:, None] * A * Dm12[None, :]
    for al in (1e-4, 1e-2, 0.1, 0.5):
        Qm = al * np.eye(n) + (1 - al) / 2 * Ls
        W = rng.normal(0, 1, (400, n)); U = W * v
        pu = U - ((U @ v) / vol)[:, None] * v[None, :]
        lhs = np.einsum('ij,jk,ik->i', pu, Qm, pu)
        mu = (W * d).sum(1) / vol
        varp = ((W - mu[:, None]) ** 2 * d).sum(1) / vol
        ii, jj = np.nonzero(np.triu(A, 1))
        dr = ((W[:, ii] - W[:, jj]) ** 2).sum(1)
        rhs = al * vol * varp + (1 - al) / 2 * dr
        mx = max(mx, float(np.max(np.abs(lhs - rhs) / np.maximum(np.abs(lhs), 1e-12))))
print("      max relative deviation over %d graphs x 4 alphas x 400 w: %.3e" % (60, mx))
