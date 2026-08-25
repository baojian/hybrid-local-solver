"""W2 part 3: validation on concrete graphs.

1. Float-model spider pairs at ensemble scale: forced-distinguish predicate
   computed from the actual solved graphs; verify flip at closed-form j*.
2. Uniformity of the (J vs 2J) gap over mixed rest-arm configs (Yao needs it).
3. Gadget variant: leaf-end vs heavy star-sink at the hidden port -- shows
   only a constant-factor change (degree gadgets don't beat the eps*d slack).
4. Explicit theorem-constant check: k=floor(s/(15 eps)), J=ceil(1/(2s)):
   gap >= eps uniformly?  And the resulting probe count.
"""
from fractions import Fraction as F
import sys, random
sys.path.insert(0, "/home/claude/work/overnight/w2_spider_info")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from formulas import lam_of_alpha, params, spider_u, spider_adj
from model import Model, ExactModel
import numpy as np


def graph_pair_maxratio(alpha, LsA, LsB):
    """Forced-distinguish statistic from actual solved graphs (float):
    max over common vertices of |pi^A - pi^B|/(d^A + d^B).
    Common vertices matched by (arm, depth) coordinates."""
    adjA, vidA = spider_adj(LsA)
    adjB, vidB = spider_adj(LsB)
    mA = Model(adjA, float(alpha), 0)
    mB = Model(adjB, float(alpha), 0)
    piA, piB = mA.pi(), mB.pi()
    dA = {v: len(adjA[v]) for v in adjA}
    dB = {v: len(adjB[v]) for v in adjB}
    best, arg = -1.0, None
    r = abs(piA[0] - piB[0]) / (dA[0] + dB[0])
    best, arg = r, "center"
    for (a, j), vA in vidA.items():
        if (a, j) in vidB:
            vB = vidB[(a, j)]
            r = abs(piA[vA] - piB[vB]) / (dA[vA] + dB[vB])
            if r > best:
                best, arg = r, (a, j)
    return best, arg


def part1_threshold_flip():
    alpha = F(1, 256)
    lam, s = lam_of_alpha(alpha)
    eps = s / 512            # = 1/8192
    k, J = 51, 8             # from sensitivity table: j*_yao = 9
    print(f"1. threshold flip on solved graphs: alpha=1/256, eps=1/8192, "
          f"k={k}, rest arms 2J={2*J}")
    print("   arm1 depth j | maxratio/eps (graph) | (closed form) | forced?")
    from sensitivity import pair_gap
    for j in list(range(5, 14)):
        g, arg = graph_pair_maxratio(alpha, [j] + [2 * J] * (k - 1),
                                     [2 * J] * k)
        cf, cfarg, _ = pair_gap(lam, k, j, 2 * J, 2 * J)
        print(f"   {j:4d}      {g/float(eps):10.4f}  {float(cf/eps):10.4f}"
              f"   {'YES' if g > eps else 'no '}   argmax={arg}")


def part2_mixed_rest():
    alpha = F(1, 256)
    lam, s = lam_of_alpha(alpha)
    eps = s / 512
    k, J = 51, 8
    rng = random.Random(7)
    print(f"\n2. gap uniformity over mixed rest configs (k={k}, J={J}, "
          f"pair = arm1 J vs 2J):")
    worst = None
    for trial in range(12):
        rest = [J if rng.random() < 0.5 else 2 * J for _ in range(k - 1)]
        uA0, armsA = spider_u(lam, [J] + rest)
        uB0, armsB = spider_u(lam, [2 * J] + rest)
        # gap at arm1 vertex J-1 (deg 2 in both)
        gap = abs(armsA[0][J - 2] - armsB[0][J - 2])  # u-scale
        ratio = float(gap / (2 * eps))   # threshold |du|>2eps
        if worst is None or ratio < worst:
            worst = ratio
    # extremes
    for tag, rest in (("all-J", [J] * (k - 1)), ("all-2J", [2 * J] * (k - 1))):
        uA0, armsA = spider_u(lam, [J] + rest)
        uB0, armsB = spider_u(lam, [2 * J] + rest)
        gap = abs(armsA[0][J - 2] - armsB[0][J - 2])
        print(f"   rest={tag:7s}: |du_(J-1)|/(2eps) = {float(gap/(2*eps)):.4f}")
    print(f"   min over 12 random mixed configs: {worst:.4f}  (>1 => forced "
          f"for every rest config => Yao per-arm error prob >= 1/2)")
    # lower bound u0 > s/k check
    u0, _ = spider_u(lam, [J] * k)
    print(f"   u0(all-J)*k/s = {float(u0*k/s):.4f}, "
          f"u0(all-2J)*k/s = {float(spider_u(lam,[2*J]*k)[0]*k/s):.4f} (both >1)")


def part3_gadget():
    """Leaf-end vs heavy sink at hidden port p+1; both vs plain continuation.
    Exact, small spider."""
    alpha = F(1, 16)
    lam, s = lam_of_alpha(alpha)
    k, p = 4, 4          # probed to depth p; port at depth p+1
    R = 40
    print(f"\n3. gadget two-sided range at hidden port (alpha=1/16, k={k}, "
          f"port depth {p+1}):")

    def build(variant, D=16):
        # arms 2..k length R; arm1: path to depth p+1 then variant
        adj, vid = spider_adj([p + 1] + [R] * (k - 1))
        port = vid[(0, p + 1)]
        n = len(adj)
        if variant == "leaf":
            pass
        elif variant == "cont":
            adj = {u: list(v) for u, v in adj.items()}
            prev = port
            for t in range(R - p - 1):
                adj[prev] = sorted(adj[prev] + [n])
                adj[n] = [prev]
                prev = n
                n += 1
        elif variant == "sink":
            adj = {u: list(v) for u, v in adj.items()}
            for t in range(D):
                adj[port] = sorted(adj[port] + [n])
                adj[n] = [port]
                n += 1
        return {u: sorted(vv) for u, vv in adj.items()}, vid

    us = {}
    for variant in ("leaf", "cont", "sink"):
        adj, vid = build(variant)
        em = ExactModel(adj, alpha, 0)
        pi = em.solve_pi()
        us[variant] = [pi[vid[(0, j)]] / len(adj[vid[(0, j)]])
                       for j in range(1, p + 1)]
    print("   u at probed depth p (deg-2 vertex), three completions:")
    for v in ("leaf", "cont", "sink"):
        print(f"     {v:5s}: u_p = {float(us[v][p-1]):.6e}")
    gl = us["leaf"][p - 1] - us["cont"][p - 1]
    gs = us["cont"][p - 1] - us["sink"][p - 1]
    print(f"   leaf-vs-cont gap {float(gl):.3e};  cont-vs-sink gap "
          f"{float(gs):.3e};  two-sided/one-sided = "
          f"{float((gl+gs)/gl):.3f}  (constant-factor only)")


def part4_theorem_constants():
    print("\n4. theorem-constant check: k=floor(s/(15 eps)), J=ceil(1/(2s)):")
    from sensitivity import pair_gap
    for alpha in (F(1, 16), F(1, 64), F(1, 256)):
        lam, s = lam_of_alpha(alpha)
        for div in (64, 512, 4096):
            eps = s / div
            k = int(s / (15 * eps))
            if k < 2:
                continue
            J = -(-1 // (2 * s)).__floor__() if False else int(1 / (2 * s)) + (0 if (1 / (2 * s)) == int(1 / (2 * s)) else 1)
            g, arg, _ = pair_gap(lam, k, J, 2 * J, 2 * J)
            probes = k * J + 1
            print(f"   alpha={alpha}, eps=s/{div}: k={k}, J={J}, "
                  f"gap/eps={float(g/eps):7.3f} {'OK' if g > eps else 'FAIL'}"
                  f"  probes>={probes} = {probes*float(eps):.4f}/eps"
                  f" = {probes*float(s*eps):.5f}/(s*eps)")


if __name__ == "__main__":
    part1_threshold_flip()
    part2_mixed_rest()
    part3_gadget()
    part4_theorem_constants()
