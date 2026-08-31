"""I6-C Open 1: the maximum principle max_u pi_u/d_u = pi_v/d_v (seed), hence
Phi = max_u pr(e_u)_v / pi_v = 1, always, with strict inequality off the seed.

Checks:
 P1  ratio form: for many (graph, seed, alpha): argmax_u pi_u/d_u == seed,
     unique, and phi_u = (pi_u/d_u)/(pi_v/d_v) <= 1 (float, tol 1e-10).
 P2  reversibility identity pr(e_u)_v = pi_u * d_v / d_u  (ties the two Phi
     readings together; verified entrywise).
 P3  i2d PRODUCT display "Phi = max_u d_u pi_u/(d_v pi_v)": counterexample
     hunt -- expect > 1 for remote low-degree seeds (leaf-seeded star), i.e.
     the i2d second display is a scale slip; the operative (ratio) form is 1.
 P4  exact-rational spot checks (Fraction solve) on 3 small graphs.
 P5  mass ceiling corollary (the Open-2 tool):
     M_S := sum_{u in S_eps} pi_u <= (pi_v/d_v) * vol(S_eps), all instances.

Rerun: cd /home/claude/work/overnight/i6c && python3 open1_maxprinciple.py
"""
import os
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))
import zoo                                                # noqa: E402


def solve_pi(adj, alpha, seed):
    """H pi = gamma e_seed, H = I - c A D^{-1} (dense float)."""
    n = len(adj)
    c = (1 - alpha) / (1 + alpha)
    g = 2 * alpha / (1 + alpha)
    d = np.array([len(adj[u]) for u in range(n)], float)
    H = np.eye(n)
    for u in range(n):
        for w in adj[u]:
            H[u, w] -= c / d[w]
    rhs = np.zeros(n)
    rhs[seed] = g
    return np.linalg.solve(H, rhs), d, H


def solve_pi_exact(adj, alpha_frac, seed):
    """Fraction Gaussian elimination of H pi = gamma e_seed."""
    n = len(adj)
    c = (1 - alpha_frac) / (1 + alpha_frac)
    g = 2 * alpha_frac / (1 + alpha_frac)
    d = [Fraction(len(adj[u])) for u in range(n)]
    M = [[Fraction(0)] * (n + 1) for _ in range(n)]
    for u in range(n):
        M[u][u] = Fraction(1)
        for w in adj[u]:
            M[u][w] -= c / d[w]
    M[seed][n] = g
    for col in range(n):                       # naive elimination, small n
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [M[r][n] for r in range(n)], d


def lollipop(L, npool):
    """Path 0..L-1 (seed 0) attached to cycle of npool vertices."""
    edges = [(i, i + 1) for i in range(L - 1)]
    base = L
    for j in range(npool):
        edges.append((base + j, base + (j + 1) % npool))
    edges.append((L - 1, base))
    return zoo._sym(edges, L + npool), 0


def battery():
    fams = []
    fams.append(('star16_center', *zoo.star(16, True)))
    fams.append(('star16_leaf', *zoo.star(16, False)))
    fams.append(('star64_leaf', *zoo.star(64, False)))
    fams.append(('path24_end', *zoo.path(24, True)))
    fams.append(('path24_mid', *zoo.path(24, False)))
    fams.append(('cycle20', *zoo.cycle(20)))
    fams.append(('spider4x6', *zoo.spider(4, 6)))
    fams.append(('caterpillar10', *zoo.caterpillar(10)))
    fams.append(('theta_3_4_5', *zoo.theta_graph(3, 4, 5)))
    adj, s = zoo.binary_tree(5)
    fams.append(('btree5_root', adj, s))
    fams.append(('btree5_leaf', adj, len(adj) - 1))
    adj, s = zoo.grid(6, 6)
    fams.append(('grid6x6', adj, s))
    fams.append(('grid6x6_corner', adj, 0))
    fams.append(('rreg24_3', *zoo.random_regular(24, 3)))
    fams.append(('decoy_hub', *zoo.decoy_hub(8, 12)))
    fams.append(('complete8', *zoo.complete(8)))
    fams.append(('double_cycle6', *zoo.double_cycle(6)))
    fams.append(('lollipop_32_12', *lollipop(32, 12)))
    return fams


def main():
    alphas = [0.9, 2**-2, 2**-4, 2**-8, 2**-12]
    fams = battery()
    fail = 0
    n_checked = 0
    worst_gap = 0.0          # max over runs of second-largest phi (want < 1)
    prod_max = 0.0           # max product-form 'Phi' seen (P3)
    prod_witness = None
    print(f"P1/P2/P5 battery: {len(fams)} instances x {len(alphas)} alphas")
    for name, adj, seed in fams:
        n = len(adj)
        for alpha in alphas:
            pi, d, H = solve_pi(adj, alpha, seed)
            u_val = pi / d
            n_checked += 1
            # P1 ratio maximum principle
            phi = u_val / u_val[seed]
            am = int(np.argmax(u_val))
            second = np.max(np.delete(phi, seed)) if n > 1 else 0.0
            worst_gap = max(worst_gap, second)
            if am != seed or np.max(phi) > 1 + 1e-10 or second >= 1 - 1e-12:
                fail += 1
                print(f"  P1 FAIL {name} alpha={alpha}: argmax={am} "
                      f"seed={seed} maxphi={np.max(phi):.6g} 2nd={second:.6g}")
            # P2 reversibility: pr(e_u)_v = pi_u d_v/d_u ; pr = g*H^{-1}
            g = 2 * alpha / (1 + alpha)
            Hinv_row_v = np.linalg.solve(H.T, np.eye(n)[seed])  # row v of H^-1
            pr_eu_v = g * Hinv_row_v          # over u: pr(e_u)_v
            rhs = pi * d[seed] / d
            if np.max(np.abs(pr_eu_v - rhs)) > 1e-9:
                fail += 1
                print(f"  P2 FAIL {name} alpha={alpha}: "
                      f"dev={np.max(np.abs(pr_eu_v - rhs)):.3g}")
            # P3 product form
            prodform = np.max(d * pi) / (d[seed] * pi[seed])
            if prodform > prod_max:
                prod_max, prod_witness = prodform, (name, alpha)
            # P5 mass ceiling on S_eps for a few eps
            for eps in (2**-4, 2**-6, 2**-8):
                S = u_val > eps
                if S.any():
                    M_S = float(pi[S].sum())
                    volS = float(d[S].sum())
                    if M_S > u_val[seed] * volS + 1e-12:
                        fail += 1
                        print(f"  P5 FAIL {name} a={alpha} eps={eps}")
    print(f"P1: max off-seed phi over battery = {worst_gap:.12f} (< 1 strict)")
    print(f"P3: product-form max = {prod_max:.3f} at {prod_witness} "
          f"(>1 ==> i2d's 'd_u pi_u' display is a scale slip; ratio form is "
          f"the operative one and equals 1)")

    # P4 exact rational
    print("P4 exact-rational:")
    for name, adj, seed, af in [
            ('star5_leaf', *zoo.star(5, False), Fraction(1, 7)),
            ('path7_end', *zoo.path(7, True), Fraction(1, 5)),
            ('theta_2_3_4', *zoo.theta_graph(2, 3, 4), Fraction(3, 11))]:
        pix, d = solve_pi_exact(adj, af, seed)
        uv = [p / dd for p, dd in zip(pix, d)]
        mx = max(range(len(uv)), key=lambda i: uv[i])
        strict = all(uv[i] < uv[seed] for i in range(len(uv)) if i != seed)
        ok = (mx == seed) and strict
        print(f"  {name} alpha={af}: argmax=seed {mx == seed}, "
              f"strict {strict}  -> {'OK' if ok else 'FAIL'}")
        if not ok:
            fail += 1
    print(f"\nchecked {n_checked} (instance,alpha) cells;  FAILURES: {fail}")
    print("VERDICT: " + ("ALL PASS -- maximum principle holds, Phi = 1, "
                         "strict off seed." if fail == 0 else "FAILURES."))
    return fail


if __name__ == '__main__':
    sys.exit(0 if main() == 0 else 1)
