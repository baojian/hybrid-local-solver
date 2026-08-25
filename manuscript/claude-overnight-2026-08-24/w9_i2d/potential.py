"""I2-D / T2: the settling potential Psi and the signed-eta (r>=0) lower bound.

Psi_c(r) := <phi, r>,  phi^T := e_c^T M_op^{-1} = (1/alpha) * (pr^T e_c)^T,
i.e. phi_u = pr(e_u)_c / alpha = (d_u/(alpha d_c)) * pr(e_c)_u   (reversibility).

Key exact identity (any graph, any sign of eta):
    gp(u, eta)  =>  Delta Psi_c = -eta * [u == c].
So Psi_c is invariant under every operation NOT based at c, and strictly
decreases only at positive c-based operations.  On the star with c = center,
phi = (1, c_a, ..., c_a)/phi_c-normalisation, i.e. Psi ∝ r_c + c_a * sum_L r.

Verifies:
  (P1) the identity, on the graph zoo, for random signed sequences;
  (P2) phi >= 0, phi_c = max phi (needed for the tail bound);
  (P3) the multiplicative step bound |Delta Psi| <= kappa * Psi at c-ops;
  (P4) the resulting count N_c^+ >= ln(4)/(-ln(1-kappa)) on real runs and on
       the pump adversary.
"""
import math
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'w1_monotone_lb'))
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))
from gpush import GP, pr_matrix, pr_vec            # noqa: E402
import zoo                                          # noqa: E402


def phi_vec(adj, alpha, c):
    """phi_u = pr(e_u)_c / alpha  ==  row c of M_op^{-1}."""
    M = pr_matrix(adj, alpha)
    e = np.zeros(len(adj)); e[c] = 1.0
    return np.linalg.solve(M.T, e)          # (M^{-T} e_c) = row c of M^{-1}


def psi(phi, r):
    return float(np.dot(phi, np.asarray(r, dtype=float)))


def check_identity(adj, alpha, seed, c, nops=200, rng=None, signed=True):
    """Random legal-ish sequence (r>=0 enforced); check Delta Psi = -eta*[u==c]."""
    rng = rng or random.Random(0)
    phi = phi_vec(adj, alpha, c)
    st = GP(adj, alpha, seed, center=c)
    worst = 0.0
    worst_rel = 0.0
    for _ in range(nops):
        cand = [u for u in range(st.n) if st.r[u] > 1e-14]
        if not cand:
            break
        u = rng.choice(cand)
        capp = 2.0 * st.r[u] / (1.0 + alpha)          # eta > 0 feasibility
        if signed and rng.random() < 0.45:
            # negative eta: need r[w] >= (1-alpha)|eta|/(2 d_u) for all w~u
            mn = min(st.r[w] for w in adj[u])
            capn = 2.0 * mn * st.d[u] / (1.0 - alpha)
            eta = -rng.uniform(0.0, 1.0) * capn
        else:
            eta = rng.uniform(0.0, 1.0) * capp
        before = psi(phi, st.r)
        st.gp(u, eta)
        after = psi(phi, st.r)
        pred = -eta if u == c else 0.0
        err = abs((after - before) - pred)
        worst = max(worst, err)
        worst_rel = max(worst_rel, err / max(1e-30, abs(eta)))
        assert min(st.r) > -1e-11, 'r went negative'
    return worst, worst_rel, phi, st


def main():
    print('=' * 74)
    print('P1/P2  Psi identity  Delta Psi = -eta*[u==c]   (signed eta, r>=0)')
    print('=' * 74)
    graphs = [
        ('star(8)',       zoo.star(8)[0],            0),
        ('star(40)',      zoo.star(40)[0],           0),
        ('path(9)',       zoo.path(9)[0],            0),
        ('spider(4,3)',   zoo.spider(4, 3)[0],       0),
        ('caterpillar6',  zoo.caterpillar(6)[0],     0),
        ('theta(2,3,4)',  zoo.theta_graph(2, 3, 4)[0], 0),
        ('binary_tree3',  zoo.binary_tree(3)[0],     0),
        ('grid(4,4)',     zoo.grid(4, 4)[0],         0),
        ('complete(6)',   zoo.complete(6)[0],        0),
        ('rand_reg(10,3)', zoo.random_regular(10, 3)[0], 0),
    ]
    print(f"{'graph':16s} {'alpha':>8s} {'max|dPsi-pred|':>15s} {'rel':>10s} "
          f"{'phi>=0':>7s} {'phi_c=max':>10s}")
    allok = True
    for name, adj, c in graphs:
        for alpha in (0.25, 0.0625, 1.0 / 64):
            w, wr, phi, st = check_identity(adj, alpha, c, c, nops=300,
                                            rng=random.Random(hash(name) % 999))
            pos = bool(np.all(phi >= -1e-14))
            cmax = bool(abs(phi[c] - phi.max()) < 1e-12)
            allok &= pos and (w < 1e-10)
            print(f'{name:16s} {alpha:8.4f} {w:15.3e} {wr:10.2e} '
                  f'{str(pos):>7s} {str(cmax):>10s}')
    print(f'  -> identity holds everywhere: {allok}')

    print()
    print('=' * 74)
    print('P3  kappa bound at c-ops:  0 <= -dPsi/Psi <= kappa = 2/((1+a)phi_c)')
    print('    (star closed form: phi_c = (1+a)/(2a)*... , kappa_+ = 4a/(1+a)^2)')
    print('=' * 74)
    print(f"{'graph':16s} {'alpha':>8s} {'phi_c':>10s} {'2/((1+a)phi_c)':>15s} "
          f"{'max obs -dPsi/Psi':>18s}")
    for name, adj, c in graphs[:6]:
        for alpha in (0.25, 0.0625, 1.0 / 64):
            phi = phi_vec(adj, alpha, c)
            kappa = 2.0 / ((1 + alpha) * phi[c])
            # observed worst relative decrease over random signed runs
            rng = random.Random(7)
            obs = 0.0
            for _ in range(6):
                st = GP(adj, alpha, c, center=c)
                for _ in range(150):
                    cand = [u for u in range(st.n) if st.r[u] > 1e-14]
                    if not cand:
                        break
                    u = rng.choice(cand)
                    if rng.random() < 0.45 and min(st.r[w] for w in adj[u]) > 1e-14:
                        mn = min(st.r[w] for w in adj[u])
                        eta = -rng.uniform(0, 1) * 2.0 * mn * st.d[u] / (1 - alpha)
                    else:
                        eta = rng.uniform(0, 1) * 2.0 * st.r[u] / (1 + alpha)
                    P0 = psi(phi, st.r)
                    st.gp(u, eta)
                    P1 = psi(phi, st.r)
                    if P0 > 1e-14:
                        obs = max(obs, (P0 - P1) / P0)
            flag = 'OK' if obs <= kappa + 1e-9 else '**VIOLATION**'
            print(f'{name:16s} {alpha:8.4f} {phi[c]:10.4f} {kappa:15.6f} '
                  f'{obs:18.6f}  {flag}')

    print()
    print('=' * 74)
    print('P4  star: N_c^+ >= ln(1/(4 eps vol / phi-normalised)) / (-ln(1-kappa))')
    print('    signed-eta pump adversary must still pay the c-ops')
    print('=' * 74)
    from gpush import pr_matrix as _pm
    print(f"{'alpha':>8s} {'eps':>10s} {'m':>5s} {'kappa+':>9s} "
          f"{'LB N_c+':>9s} {'LB W':>11s} {'pump K':>7s} {'obs N_c+':>9s} "
          f"{'obs W':>9s} {'ok':>4s}")
    for alpha in (0.25, 0.0625, 1.0 / 64, 2.0 ** -8):
        for eps in (2.0 ** -7, 2.0 ** -9):
            m = int(math.floor(1.0 / (8.0 * eps)))
            adj, seed = zoo.star(m)
            kap = 4.0 * alpha / (1.0 + alpha) ** 2
            lbN = math.log(4.0) / (-math.log(1.0 - kap))
            lbW = m * lbN
            for K in (1, 4, 16):
                st = GP(adj, alpha, 0, center=0)
                # phase 1: pump ||r||_1 to K (leaf-antis then centre-anti)
                guard = 0
                while st.sum_r < K and guard < 20000:
                    guard += 1
                    rc = st.r[0]
                    if rc > 1e-13:
                        for w in range(1, st.n):
                            st.gp(w, -2.0 * (rc / m) / (1 - alpha))
                    mn = min(st.r[w] for w in range(1, st.n))
                    if mn > 1e-13:
                        st.gp(0, -2.0 * m * mn / (1 - alpha))
                    else:
                        break
                npos_c = 0
                # phase 2: solve, full pushes, coord stop
                guard = 0
                while guard < 400000:
                    guard += 1
                    act = [u for u in range(st.n) if st.r[u] >= eps * st.d[u]]
                    if not act:
                        break
                    if 0 in act:
                        st.gp(0, st.cap(0)); st.r[0] = 0.0; npos_c += 1
                    for w in act:
                        if w != 0 and st.r[w] >= eps:
                            st.gp(w, st.cap(w)); st.r[w] = 0.0
                assert st.min_r_seen > -1e-9
                M = _pm(adj, alpha)
                e = np.zeros(st.n); e[0] = 1.0
                pi = pr_vec(adj, alpha, e, M)
                err = st.err_sem(pi)
                ok = (err <= eps * (1 + 1e-9)) and (npos_c >= lbN - 1e-9) \
                    and (st.W >= lbW - 1e-9)
                print(f'{alpha:8.5f} {eps:10.5f} {m:5d} {kap:9.5f} '
                      f'{lbN:9.2f} {lbW:11.1f} {K:7d} {npos_c:9d} '
                      f'{st.W:9d} {str(ok):>4s}')


if __name__ == '__main__':
    main()
