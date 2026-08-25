"""W2 part 1-2: exact sensitivity of spider PPR to one arm's truncation depth,
critical depth j*, and the k*J product ceiling.

Distinguishability predicate (adjacency-probe adversary): two graphs G,G'
sharing the probed portion admit NO common eps-valid output iff some vertex i
common to both has |pi^G_i - pi^{G'}_i| > eps*(d^G_i + d^{G'}_i).
(Interval overlap per coordinate; vertices present in only one graph impose no
joint constraint because the adversary controls unseen vertex ids.)
"""
from fractions import Fraction
import sys
sys.path.insert(0, "/home/claude/work/overnight/w2_spider_info")
from formulas import lam_of_alpha, params, psi, spider_u


def pair_gap(lam, k, LA, LB, Lrest):
    """Spider with k arms; arms 2..k have length Lrest in both graphs.
    Arm 1 has length LA in G_A, LB in G_B (LA < LB).
    Returns (max_ratio, argmax, gaps) where ratio_i = |pi^A_i - pi^B_i| /
    (d^A_i + d^B_i)  -- forced-distinguish at accuracy eps iff max_ratio > eps.
    Common vertices: center, arm1 depths 1..LA, rest arms depths 1..Lrest."""
    uA0, armsA = spider_u(lam, [LA] + [Lrest] * (k - 1))
    uB0, armsB = spider_u(lam, [LB] + [Lrest] * (k - 1))
    best = (Fraction(-1), None)
    gaps = {}

    def upd(tag, piA, piB, dA, dB):
        r = abs(piA - piB) / (dA + dB)
        gaps[tag] = r
        nonlocal best
        if r > best[0]:
            best = (r, tag)

    upd("center", k * uA0, k * uB0, k, k)
    a1A, a1B = armsA[0], armsB[0]
    for j in range(1, LA + 1):
        dA = 1 if j == LA else 2
        dB = 1 if j == LB else 2
        upd(("arm1", j), dA * a1A[j - 1], dB * a1B[j - 1], dA, dB)
    # rest arms identical lengths; gaps only via center shift (tiny) -- check
    rA, rB = armsA[1], armsB[1]
    for j in (1, Lrest):
        d = 1 if j == Lrest else 2
        upd(("rest", j), d * rA[j - 1], d * rB[j - 1], d, d)
    return best[0], best[1], gaps


def table_a_center(alpha):
    """(a) center impedance: one arm truncated at j vs all-infinite baseline.
    Exact Delta u0 and the predicted normalization."""
    lam, s = lam_of_alpha(alpha)
    c, gamma = params(lam)
    k = 8
    R = 400  # effectively infinite
    base0, _ = spider_u(lam, [R] * k)
    print(f"\n(a) center sensitivity, alpha={alpha} (lam={lam}), k={k}, "
          f"baseline all arms L={R}:")
    print("    j    Delta_u0=u0(j)-u0(inf)      Delta_u0 * k^2/(s*lam^2j)")
    for j in [1, 2, 4, 8, 16, 32, 64]:
        u0, _ = spider_u(lam, [j] + [R] * (k - 1))
        d = u0 - base0
        norm = d * k * k / (s * lam ** (2 * j))
        print(f"  {j:4d}   {float(d):+.6e}              {float(norm):.6f}")
    # predicted constant: c*(1+lam^2)/(1+lam^(2j)) /((1-c lam)(1+lam^2)/... )
    pred = c * (1 + lam ** 2) / (1 - lam ** 2) * (1 - c * lam)
    # Delta u0 ~ (gamma/k)*(c/k)(psi_{j-1}-lam)/(1-c lam)^2 ; psi dev formula
    # => norm -> c*(1-lam^2)/lam /(1-c*lam)/k*... print theoretical limit:
    th = gamma * c * (1 - lam ** 2) / lam / (1 - c * lam) ** 2 / k * k  # per k^2 done
    th = gamma * c * (1 - lam ** 2) / lam / (1 - c * lam) ** 2 / s
    print(f"  predicted large-j constant gamma*c*(1-lam^2)/(lam*(1-c*lam)^2*s)"
          f" = {float(th):.6f}")


def table_b_local(alpha):
    """(b) local effect near the truncation point."""
    lam, s = lam_of_alpha(alpha)
    k, R = 8, 400
    j = 24 if alpha <= Fraction(1, 256) else 12
    uA0, armsA = spider_u(lam, [j] + [R] * (k - 1))
    uB0, armsB = spider_u(lam, [R] * k)
    print(f"\n(b) local u-profile near truncation, alpha={alpha}, k={k}, "
          f"arm1 truncated at j={j} vs L={R}:")
    print("    i    u^A_i/u^B_i        1+lam^(2(j-i))   |u^A-u^B| /"
          " ((s/k) lam^(2j-i))")
    for i in [j // 2, j - 4, j - 2, j - 1, j]:
        uu = armsA[0][i - 1] / armsB[0][i - 1]
        pred = 1 + lam ** (2 * (j - i))
        gap = abs(armsA[0][i - 1] - armsB[0][i - 1])
        nrm = gap / ((s / k) * lam ** (2 * j - i))
        print(f"  {i:4d}   {float(uu):.6f}   {float(pred):.6f}   "
              f"{float(nrm):.6f}")


def jstar(lam, s, k, eps, variant="inf", Jcap=2000):
    """Largest j such that (arm1=j) vs (arm1=long) is forced-distinguish at
    accuracy eps.  variant 'inf': LB=Lrest=large; 'yao': LB=Lrest=2j."""
    lo_ok = 0
    j = 1
    last_ok = 0
    while j <= Jcap:
        if variant == "inf":
            R = 4 * j + 200
            m, _, _ = pair_gap(lam, k, j, R, R)
        else:
            m, _, _ = pair_gap(lam, k, j, 2 * j, 2 * j)
        if m > eps:
            last_ok = j
            j += 1
        else:
            break
    return last_ok


def table_c_product(alpha, eps):
    """(c) critical depth and the product k*j*: scan k, find max."""
    lam, s = lam_of_alpha(alpha)
    import math
    print(f"\n(c) alpha={alpha}, eps={eps} (= sqrt(a)/{float(s/eps):.0f}); "
          f"1/eps={float(1/eps):.0f}, 1/(s*eps)={float(1/(s*eps)):.0f}")
    print("    k      j*_inf  j*_yao   k*j*_yao   pred j*~ln(s/(2k*eps))/ln(1/lam)")
    best = (0, None)
    kmax = int(s / eps) + 2
    ks = sorted(set([2, 4] +
                    [max(2, int(kmax * f)) for f in
                     (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.37, 0.45, 0.55,
                      0.7, 0.85, 1.0)]))
    rows = []
    for k in ks:
        ji = jstar(lam, s, k, eps, "inf")
        jy = jstar(lam, s, k, eps, "yao")
        arg = float(s / (2 * k * eps))
        pred = math.log(arg) / math.log(1 / float(lam)) if arg > 1 else 0.0
        rows.append((k, ji, jy, k * jy, pred))
        if k * jy > best[0]:
            best = (k * jy, k)
    for k, ji, jy, prod, pred in rows:
        print(f"  {k:6d}  {ji:5d}  {jy:5d}   {prod:8d}   {pred:8.2f}")
    print(f"  MAX product k*j*_yao = {best[0]}  at k={best[1]}   "
          f"[vs 1/eps = {float(1/eps):.0f}, 1/(s eps) = "
          f"{float(1/(s*eps)):.0f}]   ratio to 1/eps: "
          f"{best[0]*float(eps):.3f}")
    return best


if __name__ == "__main__":
    from fractions import Fraction as F
    for alpha in (F(1, 16), F(1, 64), F(1, 256)):
        table_a_center(alpha)
        table_b_local(alpha)
    results = {}
    for alpha in (F(1, 16), F(1, 64), F(1, 256)):
        lam, s = lam_of_alpha(alpha)
        for div in (64, 512):
            eps = s / div
            results[(alpha, div)] = table_c_product(alpha, eps)
    # fixed absolute eps across alphas
    for alpha in (F(1, 16), F(1, 64), F(1, 256)):
        results[(alpha, 'abs')] = table_c_product(alpha, F(1, 4000))
    print("\nSUMMARY max products (should be ~const/eps, alpha-independent):")
    for key, (prod, kk) in results.items():
        al, div = key
        lam, s = lam_of_alpha(al)
        eps = s / div if div != 'abs' else F(1, 4000)
        print(f"  alpha={al}, eps={eps}: max k*j* = {prod} = "
              f"{prod*float(eps):.3f}/eps = "
              f"{prod*float(s*eps):.4f}/(sqrt(a)*eps)  (k={kk})")
