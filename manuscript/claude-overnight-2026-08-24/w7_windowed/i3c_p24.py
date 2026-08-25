"""I3-C part 5: P24 tuned-rho long run -- is the C10 (low-mode floor) failure a
FACE effect (support still growing) or a modal effect?  Also: does the D-weighted
L-E (C5D) hold at every stage of the sharpest known stress family, and does the
absorption certificate ever fire?"""
import sys, math, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
import numpy as np
from fengine import FInst
from engine import path_graph

n, q, rho = 24, 1 / 32, 65 / 4096
adj = path_graph(n)
seed = [1.0] + [0.0] * (n - 1)
I = FInst(adj, seed, q=q, rho=rho)
d = I.d; vol = d.sum(); al, be, kap = I.alpha, I.beta, I.kappa
S = I.Sstar
A = np.zeros((n, n))
for i in range(n):
    for j in adj[i]: A[i, j] = 1.0
Dm12 = 1 / np.sqrt(d)
mu = np.sort(np.linalg.eigvalsh(np.eye(n) - Dm12[:, None] * A * Dm12[None, :]))
lam = al + (1 - al) * mu / 2
m_k = kap / (kap + lam); s_k = m_k * be
print("P24 tuned rho=%g q=%g:  |S*|=%d  mu2=%.6f  2q=%.6f  C16 holds: %s"
      % (rho, q, len(S), mu[1], 2 * q, bool(mu[1] >= 2 * q)))
print("  s_2/(1-q)^2 = %.6f   s_2(2-m_2)/(1-q)^2 = %.6f  (C16 needs <=1)"
      % (s_k[1] / (1 - q) ** 2, s_k[1] * (2 - m_k[1]) / (1 - q) ** 2))
print("  number of modes with mu_k < 2q: %d of %d" % (int((mu < 2 * q).sum()), n))

T = 400
xm = np.zeros(n); x = np.zeros(n)
Lprev = None
c10 = [0, 0]; c10_after = [0, 0]; c5 = [0, 0]; c5w = 0.0
tface = None
word = []
first_fail_after = None
rows = []
for t in range(T):
    dt = x - xm
    a = x + be * dt
    sa = np.where(a > 0)[0]
    Delta = 0.0
    if len(sa):
        z = I.ct[sa] - I.Qt[np.ix_(sa, sa)] @ a[sa]
        neg = z < 0
        if neg.any():
            Delta = float(np.max(-z[neg] / (al * d[sa][neg])))
    r = np.minimum(be * dt, Delta)
    ell = a - r
    mx = (be * dt).max() if n else 0.0
    cls = 'N' if Delta == 0 else ('F' if Delta >= mx else 'P')
    word.append(cls)
    # face lock: supp(x) == S* and interior
    if tface is None and set(np.where(x > 0)[0].tolist()) == set(S.tolist()):
        tface = t
    # C5D: D-weighted L-E
    def PD(u):
        return u - (d @ u) / vol
    Pr, Pd = PD(r), PD(dt)
    nr = float(d @ (Pr ** 2)); nd = float(d @ (Pd ** 2))
    c5[1] += 1
    if nr <= be * be * nd + 1e-25: c5[0] += 1
    if nd > 0: c5w = max(c5w, nr / (be * be * nd))
    e = I.xstar - x
    L = float(d @ e) / vol
    if Lprev is not None and Lprev > 0:
        ok = L >= (1 - q) * Lprev - 1e-18 * abs(L)
        c10[1] += 1; c10[0] += ok
        if tface is not None and t > tface:
            c10_after[1] += 1; c10_after[0] += ok
            if not ok and first_fail_after is None: first_fail_after = t
        if t % 40 == 0 or (tface is not None and abs(t - tface) < 3):
            rows.append((t, L, L / Lprev, 1 - q, ok, int((x > 0).sum())))
    Lprev = L
    xn = I.obstacle_solve(I.ct, kap, ell, warm=sa if len(sa) else None)
    xm, x = x, xn
print("\n  face lock t_F (supp(x_t)==S*): %s   (graph eccentricity of the seed "
      "= %d)" % (tface, n - 1))
print("  C5D (D-weighted L-E, ||P r||_D <= beta ||P d||_D): %d/%d  worst ratio %.6f"
      % (c5[0], c5[1], c5w))
print("  C10 low-mode floor over ALL t   : %d/%d" % (c10[0], c10[1]))
print("  C10 low-mode floor for t > t_F  : %d/%d   (first failure after t_F: %s)"
      % (c10_after[0], c10_after[1], first_fail_after))
print("  correction word[0:60] = %s" % ''.join(word[:60]))
print("  #corrections in T=%d: %d ; last at t=%d ; classes: N=%d F=%d P=%d"
      % (T, sum(c != 'N' for c in word),
         max(i for i, c in enumerate(word) if c != 'N'),
         word.count('N'), word.count('F'), word.count('P')))
print("\n    t        L_t          L_t/L_{t-1}   1-q       floor?  |supp x|")
for t, L, rt, oq, ok, ns in rows:
    print("  %4d  %.8e  %.9f  %.9f  %-5s   %2d" % (t, L, rt, oq, ok, ns))
json.dump(dict(tface=int(tface), word=''.join(word), mu2=float(mu[1]), twoq=2 * q,
               nmodes_below=int((mu < 2 * q).sum()), c5w=float(c5w), c5=[int(z) for z in c5], c10=[int(z) for z in c10], c10_after=[int(z) for z in c10_after]),
          open('/home/claude/work/overnight/w7_windowed/i3c_p24.json', 'w'), indent=1)
