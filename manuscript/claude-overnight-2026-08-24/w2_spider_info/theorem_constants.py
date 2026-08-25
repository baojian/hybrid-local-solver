"""W2: final theorem-constant certification.

Deterministic ensemble: k = floor(s/(C*eps)), J = ceil(cJ/s), arm depths in
{J, 2J}.  Deterministic adversary needs: fixed-rest pair gap
    gap_det := |u_{(a,J-1)}(l_a=J, rest) - u_{(a,J-1)}(l_a=2J, rest)| > 2 eps
for rest = all-2J (the minimizing rest; monotone since u0 > s/k always).

Randomized (Yao) needs interval separation (per-arm dictatorship uniform over
rest configs):
    sep := u0(J, all-2J)*g_J  -  u0(2J, all-J)*g_2J  > 2 eps
where g_L = (lam^(J-1) + lam^(2L-(J-1)))/(1+lam^(2L)) is the arm profile
factor at depth J-1 for arm length L.  If sep > 2 eps then for any output
value at (a, J-1) at most one of l_a in {J,2J} is compatible REGARDLESS of the
rest realization  =>  P(valid | transcript) <= 2^(-#underprobed arms).
"""
from fractions import Fraction as F
import sys
sys.path.insert(0, "/home/claude/work/overnight/w2_spider_info")
from formulas import lam_of_alpha, spider_u


def gJ(lam, J, L):
    return (lam ** (J - 1) + lam ** (2 * L - (J - 1))) / (1 + lam ** (2 * L))


def check(alpha, div, C, cJnum, cJden):
    lam, s = lam_of_alpha(alpha)
    eps = s / div
    k = int(s / (C * eps))          # floor
    if k < 2:
        return None
    Jq = F(cJnum, cJden) / s
    J = int(Jq) + (0 if Jq == int(Jq) else 1)   # ceil(cJ/s)
    # deterministic: rest all-2J
    _, armsA = spider_u(lam, [J] + [2 * J] * (k - 1))
    _, armsB = spider_u(lam, [2 * J] * k)
    gap_det = abs(armsA[0][J - 2] - armsB[0][J - 2]) if J >= 2 else \
        abs(armsA[0][0] - armsB[0][0])
    # yao separation
    u0_J_min = spider_u(lam, [J] + [2 * J] * (k - 1))[0]   # l_a=J, rest all-2J
    u0_2J_max = spider_u(lam, [2 * J] + [J] * (k - 1))[0]  # l_a=2J, rest all-J
    sep = u0_J_min * gJ(lam, J, J) - u0_2J_max * gJ(lam, J, 2 * J)
    probes = k * J + 1
    return dict(k=k, J=J, det=float(gap_det / (2 * eps)),
                yao=float(sep / (2 * eps)), probes=probes,
                per_eps=probes * float(eps))


if __name__ == "__main__":
    for (C, cJn, cJd) in ((15, 1, 2), (25, 1, 2), (25, 1, 1), (40, 1, 1)):
        print(f"\nC={C}, J=ceil({cJn}/{cJd}s): need det>1 and yao>1 "
              f"(ratios to 2eps)")
        ok_all = True
        for alpha in (F(1, 16), F(1, 64), F(1, 256), F(1, 1024)):
            for div in (2 * C, 8 * C, 64 * C, 512 * C):
                r = check(alpha, div, C, cJn, cJd)
                if r is None:
                    continue
                tag = "OK " if r["det"] > 1 and r["yao"] > 1 else "FAIL"
                ok_all &= (tag == "OK ")
                print(f"  a={str(alpha):7s} eps=s/{div:5d}: k={r['k']:5d} "
                      f"J={r['J']:3d} det={r['det']:6.3f} yao={r['yao']:6.3f} "
                      f"{tag} probes={r['probes']:6d} ={r['per_eps']:.4f}/eps")
        print(f"  => {'ALL OK' if ok_all else 'has failures'}")
