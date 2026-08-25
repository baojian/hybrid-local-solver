"""I2-D / T1: the output-map class  out = p + M r.

Admissible class O_B:  M >= 0, one-hop-local (M_uw = 0 unless w in N[u]),
column sums 1^T M <= B 1^T.   Members: M=0 (B=0), M=beta I (B=beta),
one Jacobi/Neumann smoothing step M_J = alpha(1+a) I + a alpha A D^{-1}
(B = alpha(2-alpha)), M = I (B=1).

Feasibility question (an LP, exactly a transportation problem):
   does there exist M in O_B with   pi_u - p_u - (M r)_u <= eps d_u  for all u?
By LP duality / Gale-Hoffman this is feasible iff for EVERY S subset V
   sum_{u in S} [ pr(r)_u - eps d_u ]_+  <=  B * r(N[S]).
We solve the LP directly (single run, and with an M shared across two runs).
"""
import math
import os
import sys

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'w1_monotone_lb'))
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))
from gpush import GP, pr_matrix, pr_vec            # noqa: E402
import zoo                                          # noqa: E402


def var_index(adj):
    """Variables M_uw for w in N[u]; return (index dict, count)."""
    idx = {}
    k = 0
    for u in range(len(adj)):
        for w in [u] + list(adj[u]):
            idx[(u, w)] = k
            k += 1
    return idx, k


def feasible(adj, runs, eps, B, tol=1e-9):
    """runs = list of (p, r, pi). Shared M. Returns (feasible?, slack)."""
    n = len(adj)
    d = np.array([len(adj[u]) for u in range(n)], dtype=float)
    idx, nv = var_index(adj)
    A_ub, b_ub = [], []
    # output constraints, per run:  -(sum_w M_uw r_w) <= -(pi_u - p_u - eps d_u)
    for (p, r, pi) in runs:
        for u in range(n):
            rhs = pi[u] - p[u] - eps * d[u]
            if rhs <= 0:
                continue
            row = np.zeros(nv)
            for w in [u] + list(adj[u]):
                row[idx[(u, w)]] = -r[w]
            A_ub.append(row); b_ub.append(-rhs)
    # column-sum constraints: sum_{u in N[w]} M_uw <= B
    for w in range(n):
        row = np.zeros(nv)
        for u in [w] + list(adj[w]):
            row[idx[(u, w)]] = 1.0
        A_ub.append(row); b_ub.append(B)
    if not A_ub:
        return True, float('inf')
    res = linprog(c=np.zeros(nv), A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(0, None)] * nv, method='highs')
    return bool(res.status == 0), res


def state(adj, alpha, seed, policy, budget, m=None):
    """Run a member policy up to a work budget; return (p, r, pi, W)."""
    st = GP(adj, alpha, seed, center=seed)
    M = pr_matrix(adj, alpha)
    e = np.zeros(st.n); e[seed] = 1.0
    pi = pr_vec(adj, alpha, e, M)
    if policy == 'full_center_first':
        while st.W < budget:
            u = max(range(st.n), key=lambda v: st.r[v] / st.d[v])
            if st.r[u] <= 1e-15:
                break
            if st.W + st.d[u] > budget:
                break
            st.gp(u, st.cap(u)); st.r[u] = 0.0
    elif policy == 'tuned_degstat':
        # deliberately land on a degree-stationary residual r = const * d
        # (the p+r escape) using a single tuned partial push at the seed
        if st.d[seed] > 1 and budget >= st.d[seed]:
            m_ = st.d[seed]
            # solve r_seed/d_seed == r_leaf/d_leaf after gp(seed, eta)
            # star only: (1 - (1+a)eta/2)/m == (1-a)eta/(2m)/1  -> eta = 2/(1+a)... use star formula
            al = alpha
            eta = 1.0 * 2.0 / (1.0 + al) * ((1 + al) / 2.0) * 1.0
            # exact: (1-(1+a)e/2)/m = (1-a)e/(2m) => 1 = (1+a)e/2 + (1-a)e/2 = e
            eta = 1.0
            st.gp(seed, eta)
        while st.W + 1 <= budget:
            u = max(range(st.n), key=lambda v: st.r[v] / st.d[v])
            if st.r[u] <= 1e-15 or st.W + st.d[u] > budget:
                break
            st.gp(u, st.cap(u)); st.r[u] = 0.0
    else:
        raise ValueError(policy)
    return np.array(st.p), np.array(st.r), pi, st.W


def min_work(adj, alpha, seed, eps, B, budgets, policies):
    best = None
    for pol in policies:
        for bud in budgets:
            p, r, pi, W = state(adj, alpha, seed, pol, bud)
            ok, _ = feasible(adj, [(p, r, pi)], eps, B)
            if ok:
                if best is None or W < best[0]:
                    best = (W, pol)
                break
    return best


def main():
    np.set_printoptions(precision=4, suppress=True)
    print('=' * 78)
    print('T1.a  membership of the standard output maps in O_B (column sums)')
    print('=' * 78)
    for alpha in (0.25, 0.0625, 1 / 64):
        a = (1 - alpha) / 2
        print(f'  alpha={alpha:.5f}:  M=0 -> B=0 ; M=beta I -> B=beta ; '
              f'M=I -> B=1 ; Jacobi M_J -> B={alpha*(2-alpha):.5f}')

    print()
    print('=' * 78)
    print('T1.b  star, centre seed: minimum work for which SOME M in O_B works')
    print('      (B=1 escape = the p+r loophole; B<1 must pay the alpha price)')
    print('=' * 78)
    print(f"{'alpha':>9s} {'eps':>9s} {'m':>5s} {'B':>6s} {'minW':>8s} "
          f"{'m':>6s} {'LB(1-B)':>9s} {'minW*a*e':>9s}")
    for alpha in (0.25, 0.0625, 1 / 64):
        for eps in (2.0 ** -6, 2.0 ** -8):
            m = int(math.floor(1.0 / (8.0 * eps)))
            adj, seed = zoo.star(m)
            kap = 4.0 * alpha / (1.0 + alpha) ** 2
            for B in (0.0, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0):
                # LB from the theorem: Psi(T)/Psi(0) <= eps*vol/(1-B)
                ratio = (2 * eps * m) / max(1e-12, 1.0 - B)
                if ratio < 1.0:
                    lb = m * math.log(1.0 / ratio) / (-math.log(1.0 - kap))
                else:
                    lb = 0.0
                buds = sorted(set([m, m + 1, 2 * m, 3 * m, 4 * m, 6 * m, 8 * m,
                                   12 * m, 16 * m, 24 * m, 32 * m, 48 * m,
                                   64 * m, 96 * m, 128 * m, 192 * m, 256 * m,
                                   400 * m, 700 * m, 1200 * m, 2000 * m]))
                best = min_work(adj, alpha, seed, eps, B, buds,
                                ['tuned_degstat', 'full_center_first'])
                mw = best[0] if best else -1
                print(f'{alpha:9.5f} {eps:9.5f} {m:5d} {B:6.2f} {mw:8d} '
                      f'{m:6d} {lb:9.1f} {mw*alpha*eps:9.5f}')

    print()
    print('=' * 78)
    print('T1.c  is the B=1 loophole killed by a SECOND SEED (shared M)?')
    print('      runs: (star, centre seed) and (star, leaf seed), one shared M')
    print('=' * 78)
    print(f"{'alpha':>9s} {'eps':>9s} {'m':>5s} {'B':>6s} "
          f"{'W_c':>7s} {'W_l':>7s} {'shared M feasible?':>20s}")
    for alpha in (0.25, 1 / 64):
        for eps in (2.0 ** -6,):
            m = int(math.floor(1.0 / (8.0 * eps)))
            adj, _ = zoo.star(m)
            for B in (0.5, 0.9, 1.0):
                for mult in (1, 2, 4, 8, 16, 32, 64, 128):
                    pc, rc, pic, Wc = state(adj, alpha, 0, 'tuned_degstat',
                                            mult * m)
                    pl, rl, pil, Wl = state(adj, alpha, 1, 'tuned_degstat',
                                            mult * m)
                    ok, _ = feasible(adj, [(pc, rc, pic), (pl, rl, pil)],
                                     eps, B)
                    if ok:
                        break
                print(f'{alpha:9.5f} {eps:9.5f} {m:5d} {B:6.2f} '
                      f'{Wc:7d} {Wl:7d} {str(ok):>20s}')

    print()
    print('=' * 78)
    print('T1.d  B=1 on graphs of larger diameter (transport obstruction)')
    print('      min work for an admissible M with B=1, vs vol')
    print('=' * 78)
    print(f"{'graph':>16s} {'alpha':>9s} {'eps':>9s} {'vol':>6s} "
          f"{'minW(B=1)':>10s} {'minW(B=.5)':>11s} {'minW/vol':>9s}")
    tests = [('star(32)', zoo.star(32)), ('path(16)', zoo.path(16)),
             ('spider(6,4)', zoo.spider(6, 4)),
             ('caterpillar(10)', zoo.caterpillar(10)),
             ('binary_tree(4)', zoo.binary_tree(4))]
    for name, (adj, seed) in tests:
        vol = sum(len(adj[u]) for u in adj)
        for alpha in (1 / 64,):
            for eps in (2.0 ** -7,):
                buds = sorted(set([1, 2, 4, 8, 16, 32, 48, 64, 96, 128, 192,
                                   256, 384, 512, 768, 1024, 2048, 4096, 8192,
                                   16384, 32768, 65536]))
                b1 = min_work(adj, alpha, seed, eps, 1.0, buds,
                              ['full_center_first'])
                b5 = min_work(adj, alpha, seed, eps, 0.5, buds,
                              ['full_center_first'])
                print(f'{name:>16s} {alpha:9.5f} {eps:9.5f} {vol:6d} '
                      f'{(b1[0] if b1 else -1):10d} '
                      f'{(b5[0] if b5 else -1):11d} '
                      f'{(b1[0] / vol if b1 else -1):9.2f}')


if __name__ == '__main__':
    main()
