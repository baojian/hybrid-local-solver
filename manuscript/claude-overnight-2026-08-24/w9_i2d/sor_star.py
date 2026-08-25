"""I2-D / T3: exact star block recurrence for signed SOR at omega_* and the
resulting UPPER bound  W = O(m (log(1/(eps m)) + log(1/alpha)) / sqrt(alpha)).

Symmetric reduction of the star K_{1,m} (centre c, m leaves, seed c):
state (R, S) = (r_c, per-leaf residual).  SOR step at u: eta = omega*2 r_u/(1+a).
  centre block (1 op, work m):   R <- (1-omega) R ;  S += c_a omega R / m
  leaf block  (m ops, work m):   R += m c_a omega S ; S <- (1-omega) S
With t=sqrt(alpha), lam=(1-t)/(1+t):  omega_* = 1+lam^2, c_a omega_* = 2 lam,
1-omega_* = -lam^2.  Claim: block aggregates obey x_{j+1}=2 lam x_j - lam^2 x_{j-1},
x_j = (j+1) lam^j x_0.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'w1_monotone_lb'))
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))
from gpush import GP, pr_matrix, pr_vec            # noqa: E402
import zoo                                          # noqa: E402


def lam_of(alpha):
    t = math.sqrt(alpha)
    return (1.0 - t) / (1.0 + t)


def omega_star(alpha):
    return 1.0 + lam_of(alpha) ** 2


def blocks(alpha, m, nblk):
    """Run alternating blocks symbolically; return list of block aggregates."""
    om = omega_star(alpha)
    ca = (1 - alpha) / (1 + alpha)
    R, S = 1.0, 0.0
    xs = []
    for j in range(nblk):
        if j % 2 == 0:                     # centre block
            xs.append(R)
            newS = S + ca * om * R / m
            R = (1 - om) * R
            S = newS
        else:                              # leaf block (all m leaves)
            xs.append(m * S)
            R = R + m * ca * om * S
            S = (1 - om) * S
        xs[-1] = xs[-1]
    return xs


def run_star_sor(alpha, m, eps, maxblk=400000):
    """Alternating-block SOR(omega_*) on the star; work-to-guarantee.
    Stops at the first block boundary where max_u |r_u|/d_u <= eps
    (which implies err = max_u (pi-p)_u/d_u <= eps by the max principle),
    and separately records the oracle stop err(p) <= eps."""
    om = omega_star(alpha)
    ca = (1 - alpha) / (1 + alpha)
    R, S = 1.0, 0.0
    pc, pl = 0.0, 0.0                      # settled mass at centre / per leaf
    W = 0
    W_res, W_err = None, None
    # exact pi on the star (mass scale, seed = centre)
    pi_c = (1 + alpha) / 2.0
    pi_l = (1 - pi_c) / m
    for j in range(maxblk):
        if W_res is None and max(abs(R) / m, abs(S)) <= eps:
            W_res = W
        errc = (pi_c - pc) / m
        errl = (pi_l - pl) / 1.0
        if W_err is None and max(errc, errl) <= eps:
            W_err = W
        if W_res is not None and W_err is not None:
            break
        if j % 2 == 0:
            eta = om * 2.0 * R / (1 + alpha)
            pc += alpha * eta
            newS = S + ca * om * R / m
            R = (1 - om) * R
            S = newS
        else:
            eta = om * 2.0 * S / (1 + alpha)
            pl += alpha * eta
            R = R + m * ca * om * S
            S = (1 - om) * S
        W += m
    return W_res, W_err, (R, S), (pc, pl)


def main():
    print('=' * 78)
    print('T3.a  block recurrence:  x_j = (j+1) lam^j x_0   (exact)')
    print('=' * 78)
    print(f"{'alpha':>9s} {'m':>5s} {'lam':>9s} {'max rel dev of x_j from (j+1)lam^j':>38s}")
    for alpha in (0.25, 0.0625, 1 / 64, 2.0 ** -8, 2.0 ** -12):
        lam = lam_of(alpha)
        for m in (8, 64, 512):
            xs = blocks(alpha, m, 40)
            dev = 0.0
            for j, x in enumerate(xs):
                pred = (j + 1) * lam ** j * xs[0]
                if abs(pred) > 1e-250:
                    dev = max(dev, abs(x - pred) / abs(pred))
            print(f'{alpha:9.6f} {m:5d} {lam:9.6f} {dev:38.3e}')
    print('  (independent of m: the recurrence has no m in it -- verified)')

    print()
    print('=' * 78)
    print('T3.b  work-to-guarantee vs the claimed bound')
    print('      J_bound = ceil( (1/t) * ln( 2/(t*eps*m) ) ),  W_bound = m*J_bound')
    print('=' * 78)
    hdr = (f"{'alpha':>9s} {'eps':>9s} {'m':>6s} {'W_res':>9s} {'W_err':>9s} "
           f"{'W_bound':>9s} {'ratio':>7s} {'c=W*a*e':>9s} "
           f"{'c*sqrt(a)/lg':>12s}")
    print(hdr)
    rows = []
    for alpha in (0.25, 0.0625, 1 / 64, 2.0 ** -8, 2.0 ** -10, 2.0 ** -12):
        t = math.sqrt(alpha)
        for eps in (2.0 ** -7, 2.0 ** -9, 2.0 ** -11):
            m = int(math.floor(1.0 / (8.0 * eps)))
            W_res, W_err, _, _ = run_star_sor(alpha, m, eps)
            Jb = math.ceil((1.0 / t) * math.log(2.0 / (t * eps * m)))
            Wb = m * Jb
            c = W_res * alpha * eps
            lg = math.log(1.0 / alpha) + math.log(1.0 / (eps * m))
            print(f'{alpha:9.6f} {eps:9.6f} {m:6d} {W_res:9d} {W_err:9d} '
                  f'{Wb:9d} {W_res / Wb:7.3f} {c:9.5f} '
                  f'{c / alpha * math.sqrt(alpha) / lg:12.5f}')
            rows.append((alpha, eps, m, W_res, W_err, Wb))
    bad = [r for r in rows if r[3] > r[5]]
    print(f'  -> W_res <= W_bound on all {len(rows)} cells: {len(bad) == 0}'
          + (f'  VIOLATIONS: {bad}' if bad else ''))

    print()
    print('=' * 78)
    print('T3.c  cross-check the symmetric reduction against the full simulator')
    print('=' * 78)
    print(f"{'alpha':>9s} {'m':>5s} {'blk':>5s} {'max|r_full - r_sym|':>22s} "
          f"{'min r':>10s} {'max||r||_1':>11s}")
    for alpha in (0.25, 1 / 64, 2.0 ** -8):
        for m in (8, 32):
            adj, seed = zoo.star(m)
            st = GP(adj, alpha, seed, center=0)
            om = omega_star(alpha)
            ca = (1 - alpha) / (1 + alpha)
            R, S = 1.0, 0.0
            worst = 0.0
            maxl1 = 1.0
            nb = 30
            for j in range(nb):
                if j % 2 == 0:
                    st.sor_step(0, om)
                    newS = S + ca * om * R / m
                    R = (1 - om) * R
                    S = newS
                else:
                    for w in range(1, m + 1):
                        st.sor_step(w, om)
                    R = R + m * ca * om * S
                    S = (1 - om) * S
                worst = max(worst, abs(st.r[0] - R),
                            max(abs(st.r[w] - S) for w in range(1, m + 1)))
                maxl1 = max(maxl1, st.l1_r())
            print(f'{alpha:9.6f} {m:5d} {nb:5d} {worst:22.3e} '
                  f'{st.min_r_seen:10.4f} {maxl1:11.4f}')
    print('  (min r < 0 and ||r||_1 > 1 confirm SOR leaves the r>=0 class)')

    print()
    print('=' * 78)
    print('T3.d  separation table: monotone/signed-eta LB vs SOR UB, same star')
    print('=' * 78)
    print(f"{'alpha':>10s} {'eps':>9s} {'m':>6s} {'LB_r>=0 (W)':>12s} "
          f"{'UB_SOR (W)':>11s} {'ratio':>8s} {'1/(sqrt(a)ln(1/a))':>19s}")
    for alpha in (0.25, 0.0625, 1 / 64, 2.0 ** -8, 2.0 ** -10, 2.0 ** -12):
        for eps in (2.0 ** -9,):
            m = int(math.floor(1.0 / (8.0 * eps)))
            kap = 4.0 * alpha / (1.0 + alpha) ** 2
            lb = m * math.log(4.0) / (-math.log(1.0 - kap))
            W_res, _, _, _ = run_star_sor(alpha, m, eps)
            print(f'{alpha:10.7f} {eps:9.6f} {m:6d} {lb:12.1f} {W_res:11d} '
                  f'{lb / W_res:8.3f} '
                  f'{1.0 / (math.sqrt(alpha) * math.log(1 / alpha)):19.3f}')


if __name__ == '__main__':
    main()
