"""W2: exact closed forms for spider PPR in the degree-normalized scale.

Scale: u_i = pi_i / d_i  (the semantic-accuracy scale: output eps-valid iff
|pi_hat_i - pi_i|/d_i <= eps, i.e. |pi_hat_i/d_i - u_i| <= eps when d matches).
System: (D - c A) u = gamma e_v,  c = (1-alpha)/(1+alpha), gamma = 2a/(1+a).
Path decay root: lambda = (1-sqrt(a))/(1+sqrt(a));  c = 2L/(1+L^2), gamma=1-c.

Spider(k; L_1..L_k): center 0 (seed, degree k), arm a is a path of L_a >= 1
vertices hanging off the center.

Closed forms (derived by transfer/continued fraction, verified here):
  psi(m)  = lam*(1+lam^(2m))/(1+lam^(2m+2))      # u_j/u_{j-1} when m arm
                                                  # vertices remain strictly
                                                  # below j (psi(0)=c: leaf)
  u_0     = gamma / (k - c*sum_a psi(L_a - 1))
  u_j^(a) = u_0*(lam^j + lam^(2*L_a - j)) / (1 + lam^(2*L_a)),  j=1..L_a
  pi: center k*u_0; arm interior 2*u_j; arm end u_{L_a}.
Infinite arms: psi -> lam, u_0 -> gamma/(k(1-c*lam)) = sqrt(a)/k,
  u_j = (sqrt(a)/k) lam^j.
"""
from fractions import Fraction
import sys
sys.path.insert(0, "/home/claude/work/overnight/lib")


def lam_of_alpha(alpha):
    """Exact rational lambda for alpha with rational sqrt (1/16,1/64,1/256...)."""
    a = Fraction(alpha)
    # find rational sqrt
    from math import isqrt
    p, q = a.numerator, a.denominator
    sp, sq = isqrt(p), isqrt(q)
    assert sp * sp == p and sq * sq == q, "alpha must have rational sqrt"
    s = Fraction(sp, sq)
    return (1 - s) / (1 + s), s


def params(lam):
    c = 2 * lam / (1 + lam ** 2)
    gamma = 1 - c
    return c, gamma


def psi(lam, m):
    return lam * (1 + lam ** (2 * m)) / (1 + lam ** (2 * m + 2))


def spider_u(lam, Ls):
    """Exact u values. Returns (u0, [arm profiles], pi_dict builder)."""
    c, gamma = params(lam)
    k = len(Ls)
    u0 = gamma / (k - c * sum(psi(lam, L - 1) for L in Ls))
    arms = []
    for L in Ls:
        denom = 1 + lam ** (2 * L)
        arms.append([u0 * (lam ** j + lam ** (2 * L - j)) / denom
                     for j in range(1, L + 1)])
    return u0, arms


def spider_adj(Ls):
    """Adjacency dict for unequal-arm spider; returns (adj, vid) where
    vid[(a,j)] = vertex id of arm a depth j (center = 0, depth 0)."""
    adj = {0: []}
    vid = {}
    nid = 1
    for a, L in enumerate(Ls):
        prev = 0
        for j in range(1, L + 1):
            adj[nid] = []
            adj[prev].append(nid)
            adj[nid].append(prev)
            vid[(a, j)] = nid
            prev = nid
            nid += 1
    return {u: sorted(vs) for u, vs in adj.items()}, vid


def spider_u_from_solver(alpha, Ls):
    """Ground truth via ExactModel Gaussian elimination (Fractions)."""
    from model import ExactModel
    adj, vid = spider_adj(Ls)
    em = ExactModel(adj, Fraction(alpha), 0)
    pi = em.solve_pi()
    d = [len(adj[u]) for u in range(len(adj))]
    u = [pi[i] / d[i] for i in range(len(adj))]
    u0 = u[0]
    arms = [[u[vid[(a, j)]] for j in range(1, L + 1)]
            for a, L in enumerate(Ls)]
    return u0, arms


def sympy_checks():
    import sympy as sp
    lam, m = sp.symbols('lambda m', positive=True)
    c = 2 * lam / (1 + lam ** 2)
    # 1. psi recursion: psi_m = c/2 / (1 - (c/2) psi_{m-1})?  No: in u-scale
    # interior eq 2u_j = c(u_{j-1}+u_{j+1}) gives, with r_j = u_j/u_{j-1} and
    # m vertices strictly below j:  r = (c/2)... derive: 2 u_j = c u_{j-1} +
    # c u_{j+1} => 2 = c/r_down_prev... use: psi(m) = c / (2 - c*psi(m-1)).
    def psi_expr(mm):
        return lam * (1 + lam ** (2 * mm)) / (1 + lam ** (2 * mm + 2))
    rec_ok = []
    M = sp.symbols('M', positive=True, integer=True)
    lhs = psi_expr(M)
    rhs = c / (2 - c * psi_expr(M - 1))
    rec_ok.append(sp.simplify(lhs - rhs) == 0)
    # 2. psi(0) = c  (leaf boundary u_L = c u_{L-1})
    rec_ok.append(sp.simplify(psi_expr(0) - c) == 0)
    # 3. fixed point psi(inf) = lam solves lam = c/(2 - c*lam)
    rec_ok.append(sp.simplify(lam - c / (2 - c * lam)) == 0)
    # 4. u0 for k infinite arms equals sqrt(alpha)/k with
    #    sqrt(alpha) = (1-lam)/(1+lam), gamma = 1-c
    k = sp.symbols('k', positive=True)
    u0inf = (1 - c) / (k - c * k * lam / k * k)  # placeholder replaced below
    u0inf = (1 - c) / (k * (1 - c * lam))
    rec_ok.append(sp.simplify(u0inf - (1 - lam) / ((1 + lam) * k)) == 0)
    # 5. deviation psi(m) - lam = lam^(2m+1)(1-lam^2)/(1+lam^(2m+2))
    dev = sp.simplify(psi_expr(M) - lam
                      - lam ** (2 * M + 1) * (1 - lam ** 2)
                      / (1 + lam ** (2 * M + 2)))
    rec_ok.append(dev == 0)
    return rec_ok


if __name__ == "__main__":
    print("sympy identity checks:", sympy_checks())
    # exact cross-validation vs ExactModel for the three campaign alphas
    for alpha in (Fraction(1, 16), Fraction(1, 64), Fraction(1, 256)):
        lam, s = lam_of_alpha(alpha)
        for Ls in ([3], [1, 4], [2, 2, 5], [4, 4, 4, 1], [7, 3, 5, 2, 6]):
            u0f, armsf = spider_u(lam, Ls)
            u0s, armss = spider_u_from_solver(alpha, Ls)
            assert u0f == u0s, (alpha, Ls, "center mismatch")
            assert armsf == armss, (alpha, Ls, "arm mismatch")
        print(f"alpha={alpha}  lam={lam}  closed form == ExactModel  "
              f"(all test spiders, exact Fractions)")
        # kernel check: long equal arms ~ sqrt(a)/k * lam^j
        k, L = 3, 40
        u0, arms = spider_u(lam, [L] * k)
        approx = s / k
        print(f"  u0 (k={k}, L={L}) = {float(u0):.10e}   sqrt(a)/k = "
              f"{float(approx):.10e}   ratio-1 = {float(u0/approx-1):.2e}")
