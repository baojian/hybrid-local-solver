"""Part 1: exact u_max on the manuscript spider; regime where S_eps is empty.

Claim to verify: u_max = u0 = (sqrt a/k)*coth(2L*artanh(sqrt a)) and
S_eps = {} iff u0 < eps = theta/k, i.e. iff
    sqrt(a) * (1+lam^{2L})/(1-lam^{2L}) < theta,   L = floor(L_sp/2)+1.
"""
import math, sys
from fractions import Fraction
sys.path.insert(0, "/home/claude/work/overnight/i5a")
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w2_spider_info")
from common import pars, spider_scales, u0_closed, arm_profile_closed, \
    build_spider, solve_pi
import formulas as F

print("=" * 78)
print("A. Validate the closed form u0 = (sqrt a/k)(1+lam^2L)/(1-lam^2L)")
print("=" * 78)
# exact Fractions via formulas.spider_u for rational sqrt(alpha)
for alpha in (Fraction(1, 16), Fraction(1, 64), Fraction(1, 256)):
    lam, s = F.lam_of_alpha(alpha)
    for k, L in ((4, 3), (16, 6), (8, 11)):
        u0, arms = F.spider_u(lam, [L] * k)
        zeta = lam ** (2 * L)
        u0_cf = (s / k) * (1 + zeta) / (1 - zeta)
        assert u0 == u0_cf, (alpha, k, L)
        # u_max = u0 (profile decreasing)
        assert all(arms[0][j] < u0 for j in range(L))
        assert all(arms[0][j] > arms[0][j + 1] for j in range(L - 1))
    print(f"  alpha={alpha}: closed form == exact Fractions spider_u; "
          f"profile strictly decreasing from center  OK")

# one direct ExactModel cross-check (independent Gaussian elimination)
alpha = Fraction(1, 64)
u0s, armss = F.spider_u_from_solver(alpha, [6] * 16)
lam, s = F.lam_of_alpha(alpha)
zeta = lam ** 12
assert u0s == (s / 16) * (1 + zeta) / (1 - zeta)
print("  ExactModel (Fraction Gaussian elimination) confirms closed form "
      "at alpha=1/64, k=16, L=6")

print()
print("=" * 78)
print("B. Manuscript instance table:  L = M+1, eps = theta/k  (ratio "
      "u0/eps is k-free)")
print("=" * 78)
for theta in (0.125, 0.0625):
    print(f"\ntheta_sp = {theta}   [bypass tau*k>1 iff sqrt(a)<theta; "
          f"empty iff u0/eps<1]")
    print(f"{'alpha':>8} {'sqrt(a)':>9} {'L_sp':>8} {'M':>4} {'L':>4} "
          f"{'zeta=lam^2L':>12} {'u0/eps':>9} {'bypass':>7} {'S_eps':>9}")
    for j in range(4, 17):
        alpha = 2.0 ** (-j)
        t, lam, c, g, wstar = pars(alpha)
        Lsp, M, L = spider_scales(alpha, theta)
        zeta = lam ** (2 * L)
        ratio = (t / theta) * (1 + zeta) / (1 - zeta)   # = u0/eps
        bypass = t < theta
        print(f"2^-{j:<5} {t:>9.5f} {Lsp:>8.2f} {M:>4} {L:>4} "
              f"{zeta:>12.5f} {ratio:>9.5f} {str(bypass):>7} "
              f"{'EMPTY' if ratio < 1 else 'NONEMPTY':>9}")

print()
print("=" * 78)
print("C. Exact nonempty band inside the theorem's hypotheses "
      "(fine alpha scan)")
print("=" * 78)
for theta in (0.125, 0.0625):
    lo_pred = (theta * (1 - theta) / (1 + theta)) ** 2
    pts = []
    N = 300000
    for i in range(N):
        la = math.log(2 ** -16) + (math.log(0.9 * theta ** 2 * 1.4) -
                                   math.log(2 ** -16)) * i / (N - 1)
        alpha = math.exp(la)
        t = math.sqrt(alpha)
        if not (t < theta):
            continue
        _, M, L = spider_scales(alpha, theta)
        lam = (1 - t) / (1 + t)
        zeta = lam ** (2 * L)
        if (t / theta) * (1 + zeta) / (1 - zeta) >= 1.0:
            pts.append(alpha)
    if pts:
        print(f"theta={theta}: NONEMPTY band = [{min(pts):.6f}, "
              f"{max(pts):.6f}]  (theta^2 = {theta**2:.6f}, "
              f"asympt. lower edge (th(1-th)/(1+th))^2 = {lo_pred:.6f})")
        print(f"   band width ratio max/min = {max(pts)/min(pts):.3f}; "
              f"dyadic alphas inside: "
              f"{[f'2^-{j}' for j in range(3,18) if min(pts) <= 2.0**-j <= max(pts)]}")
    else:
        print(f"theta={theta}: no alpha with bypass AND nonempty")

print()
print("=" * 78)
print("D. Semantic error of z=0 vs eps, and |S_eps| detail, k=64")
print("=" * 78)
theta, k = 0.125, 64
eps = theta / k
for j in (6, 7, 8, 10, 12):
    alpha = 2.0 ** (-j)
    _, M, L = spider_scales(alpha, theta)
    adj, posm = build_spider(k, L)
    pi, d = solve_pi(adj, alpha, 0)
    u = pi / d
    u0, prof = arm_profile_closed(alpha, k, L)
    assert abs(u[0] - u0) < 1e-12 * u0, (u[0], u0)
    S = int((u >= eps).sum())
    print(f"alpha=2^-{j}: L={L} n={len(adj)}  u_max/eps={u.max()/eps:.5f} "
          f"(closed form {u0/eps:.5f})  |S_eps|={S}  "
          f"vol(S_eps)={int(d[u>=eps].sum())}  "
          f"z=0 semantically {'VALID' if u.max() <= eps else 'INVALID'}")
print("\n(k-independence check: same ratios at k=8)")
for j in (7, 10):
    alpha = 2.0 ** (-j)
    _, M, L = spider_scales(alpha, theta)
    print(f"  alpha=2^-{j}: u0/eps = {u0_closed(alpha, 8, L)/(theta/8):.5f}")
