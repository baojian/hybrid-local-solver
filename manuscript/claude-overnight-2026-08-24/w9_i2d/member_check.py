"""Re-run the iteration-1 member zoo against the NEW (Psi-potential) bound.
Asserts, on every run:  N_c^+ >= ln(1/rho)/(-ln(1-kappa_+)) and W >= m*that,
with rho = ||r_stop||_1 / 1  (<= eps*vol) and kappa_+ = 4a/(1+a)^2."""
import math, os, random, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'w1_monotone_lb'))
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))
from gpush import run_queue, run_scan, pr_matrix, pr_vec   # noqa: E402
import zoo                                                  # noqa: E402

POLS = [('appr_fifo', dict(kind='q', discipline='fifo')),
        ('appr_lifo', dict(kind='q', discipline='lifo')),
        ('nonlazy',   dict(kind='q', discipline='fifo', lazy=False)),
        ('damped_0.5', dict(kind='q', discipline='fifo', omega=0.5)),
        ('damped_0.9', dict(kind='q', discipline='fifo', omega=0.9)),
        ('greedy',    dict(kind='s', mode='greedy')),
        ('greedy_nonlazy', dict(kind='s', mode='greedy', lazy=False)),
        ('cheap_first', dict(kind='s', mode='cheap_first')),
        ('jacobi',    dict(kind='s', mode='jacobi')),
        ('jacobi_nonlazy', dict(kind='s', mode='jacobi_nonlazy')),
        ('tiny_leaf', dict(kind='s', mode='tiny_leaf')),
        ('rand_v',    dict(kind='s', mode='rand_v')),
        ('rand_xi',   dict(kind='s', mode='rand_xi')),
        ('rand_mix',  dict(kind='s', mode='rand_mix'))]

print(f"{'policy':16s} {'stop':5s} {'min W*a*e':>10s} {'min W/LBnew':>12s} "
      f"{'min Nc/LBnc':>12s} {'runs':>5s}")
worst = {}
nrun = 0
fails = 0
for name, kw in POLS:
    for stop in ('coord', 'l1'):
        rw, rn, cc = 1e18, 1e18, 1e18
        for alpha in (0.25, 0.0625, 1 / 64):
            for eps in (2.0 ** -5, 2.0 ** -6, 2.0 ** -7, 2.0 ** -8, 2.0 ** -9):
                m = int(math.floor(1.0 / (8.0 * eps)))
                if m < 2:
                    continue
                adj, seed = zoo.star(m)
                for sd in (0, 1, 2):
                    rng = random.Random(sd)
                    k = dict(kw); kind = k.pop('kind')
                    if kind == 'q':
                        st = run_queue(adj, alpha, eps, seed, stop=stop,
                                       rng=rng, **k)
                    else:
                        st = run_scan(adj, alpha, eps, seed, stop=stop,
                                      rng=rng, **k)
                    nrun += 1
                    kap = 4.0 * alpha / (1.0 + alpha) ** 2
                    rho = max(st.sum_r, 1e-300)
                    lbN = math.log(1.0 / rho) / (-math.log(1.0 - kap))
                    lbW = m * lbN
                    # count of POSITIVE centre ops: all member ops have eta>0
                    ncp = st.n_center_ops
                    ok = (st.W >= lbW - 1e-6) and (ncp >= lbN - 1e-6)
                    if not ok:
                        fails += 1
                        print('  FAIL', name, stop, alpha, eps, st.W, lbW,
                              ncp, lbN)
                    rw = min(rw, st.W / lbW)
                    rn = min(rn, ncp / lbN)
                    cc = min(cc, st.W * alpha * eps)
                    if 'rand' not in name and 'mix' not in name:
                        break
        print(f'{name:16s} {stop:5s} {cc:10.5f} {rw:12.3f} {rn:12.3f} '
              f'{nrun:5d}')
print(f'\ntotal runs {nrun}, assertion failures {fails}')
print('LB constant (asymptotic):  W >= m*ln(1/(eps*vol))*(1+a)^2/(4a) '
      '-> c = W*a*e >= ln(4)*(1+a)^2/(32) ~= 0.0433')
for alpha in (0.25, 0.0625, 1/64, 2.0**-8):
    kap = 4.0*alpha/(1+alpha)**2
    print(f'   alpha={alpha:.5f}  kappa+={kap:.5f}  '
          f'c_new = ln4/(-ln(1-kappa+))*alpha/8 = '
          f'{math.log(4)/(-math.log(1-kap))*alpha/8:.5f}   '
          f'(iteration-1 proved c = 3/256 = 0.01172)')
