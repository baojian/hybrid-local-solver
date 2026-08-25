"""Part 4 (task 2c): what does the CERTIFICATE |r| < g*eps*d itself require?

(i) LP: minimum support radius R of an arm-symmetric z with
    |g*e_v - H z| <= 0.999 * g*eps*d pointwise, support in ball(R).
(ii) support statistics of the omega=1 push run (APPR at eps) that meets
     the certificate.
Instance: manuscript spider, theta=1/8, k=64, eps=theta/k, L=M+1.
"""
import math, sys
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, "/home/claude/work/overnight/i5a")
from common import pars, spider_scales, build_spider, solve_pi, cf_push_fifo

theta, k = 0.125, 64
eps = theta / k
SL = 0.999


def feasible(alpha, L, R):
    """LP feasibility: symmetric z supported on {center} U depths 1..R."""
    t, lam, c, g, wstar = pars(alpha)
    nv = R + 1                       # z_0 .. z_R
    A, b = [], []

    def row(coeffs, bound):
        v = np.zeros(nv)
        for i, co in coeffs:
            if 0 <= i <= R:
                v[i] += co
        A.append(v); b.append(bound)
        A.append(-v); b.append(bound)

    # center: g - [z0 - c*k*z1/2] in [-g*theta*SL, g*theta*SL]
    # -> |z0 - c*k/2*z1 - g| <= SL*g*theta
    v = np.zeros(nv); v[0] = 1.0
    if R >= 1:
        v[1] = -c * k / 2.0
    A.append(v); b.append(g + SL * g * theta)
    A.append(-v); b.append(-g + SL * g * theta)
    # depth 1 (exists since L>=1): threshold 2*g*eps (interior; L>=2 always)
    row([(1, 1.0), (0, -c / k), (2, -c / 2.0)], SL * 2 * g * eps)
    # depths 2..min(R+1, L)
    for jj in range(2, min(R + 1, L - 1) + 1):
        row([(jj, 1.0), (jj - 1, -c / 2.0), (jj + 1, -c / 2.0)],
            SL * 2 * g * eps)
    # leaf row (depth L): (Hz)_L = z_L - c/2 z_{L-1}, threshold g*eps*1
    if R + 1 >= L:
        row([(L, 1.0), (L - 1, -c / 2.0)], SL * g * eps)
    res = linprog(np.zeros(nv), A_ub=np.vstack(A), b_ub=np.array(b),
                  bounds=[(None, None)] * nv, method="highs")
    return res.status == 0, res.x if res.status == 0 else None


def check_full(alpha, L, R, x):
    """Rebuild the full symmetric z and verify the true certificate."""
    adj, posm = build_spider(k, L)
    z = np.zeros(len(adj))
    z[0] = x[0]
    for a in range(k):
        for jj in range(1, min(R, L) + 1):
            z[a * L + jj] = x[jj]
    t, lam, c, g, wstar = pars(alpha)
    d = np.array([len(aa) for aa in adj], float)
    ad = np.zeros(len(adj))
    for u in range(len(adj)):
        ad[u] = sum(z[w] / d[w] for w in adj[u])
    r = -(z - c * ad); r[0] += g
    return float(np.max(np.abs(r) / (g * eps * d)))


print(f"{'alpha':>7} {'L':>4} {'R_min':>6} {'R_min/L':>8} "
      f"{'vol(ball R)':>11} {'vol*sqa*e':>10} {'true cert@Rmin':>14} "
      f"{'feas@Rmin-1':>11}")
for j in (6, 7, 8, 9, 10, 11, 12):
    alpha = 2.0 ** (-j)
    t, lam, c, g, wstar = pars(alpha)
    _, M, L = spider_scales(alpha, theta)
    lo, hi = 0, L               # feasibility at R=L guaranteed (z=pi)
    okL, xL = feasible(alpha, L, L)
    assert okL
    while lo < hi:
        mid = (lo + hi) // 2
        ok, _ = feasible(alpha, L, mid)
        if ok:
            hi = mid
        else:
            lo = mid + 1
    Rmin = lo
    ok, x = feasible(alpha, L, Rmin)
    tc = check_full(alpha, L, Rmin, x)
    fem1 = feasible(alpha, L, Rmin - 1)[0] if Rmin > 0 else None
    volR = k + 2 * k * min(Rmin, L) - (k if Rmin >= L else 0)
    print(f"2^-{j:<4} {L:>4} {Rmin:>6} {Rmin/L:>8.3f} {volR:>11} "
          f"{volR*t*eps:>10.4f} {tc:>14.4f} {str(fem1):>11}")

print("\nSupport of the omega=1 (APPR at eps) certificate-meeting run:")
print(f"{'alpha':>7} {'nnz(z)':>7} {'n':>7} {'vol(supp)':>10} "
      f"{'vol(G)':>7} {'maxdepth/L':>10} {'W':>7} {'W*sqa*e':>8}")
for j in (6, 8, 10, 12):
    alpha = 2.0 ** (-j)
    t, lam, c, g, wstar = pars(alpha)
    _, M, L = spider_scales(alpha, theta)
    adj, posm = build_spider(k, L)
    res = cf_push_fifo(adj, alpha, 0, eps, eps)   # omega=1 to final cert
    z = res['z']
    d = np.array([len(a) for a in adj], float)
    supp = z != 0
    md = max((posm[i][1] for i in np.where(supp)[0] if posm[i] != 'c'),
             default=0)
    print(f"2^-{j:<4} {int(supp.sum()):>7} {len(adj):>7} "
          f"{int(d[supp].sum()):>10} {int(d.sum()):>7} {md/L:>10.3f} "
          f"{res['W1']:>7} {res['W1']*t*eps:>8.4f}")
