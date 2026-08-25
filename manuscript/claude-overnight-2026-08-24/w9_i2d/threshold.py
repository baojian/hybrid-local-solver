"""T1 supplement: the exact B-threshold on the star, and whether B=1 one-hop
output maps trivialise the instance at ZERO push work."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'w1_monotone_lb'))
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))
from outmap_lp import feasible, state          # noqa: E402
import zoo                                      # noqa: E402

print('=' * 78)
print('T1.e  sharp B threshold on the centre-seeded star, m = floor(1/(8eps))')
print('  theory: LB non-vacuous iff B < 1 - eps*vol ;')
print('          M = B I witness works iff B >= 1 - eps*vol/(1-alpha)')
print('=' * 78)
print(f"{'alpha':>9s} {'eps':>9s} {'m':>4s} {'eps*vol':>8s} "
      f"{'1-eps*vol':>10s} {'1-ev/(1-a)':>11s} {'B* (LP, W=m)':>13s} "
      f"{'B* (LP, W=0)':>13s}")
for alpha in (0.25, 0.0625, 1 / 64, 2.0 ** -8):
    for eps in (2.0 ** -6, 2.0 ** -8):
        m = int(math.floor(1.0 / (8.0 * eps)))
        adj, seed = zoo.star(m)
        vol = 2 * m
        ev = eps * vol
        # binary search the smallest B for which the LP is feasible, at W=m and W=0
        out = []
        for bud in (m, 0):
        	p, r, pi, W = state(adj, alpha, seed, 'tuned_degstat', bud)
        	lo, hi = 0.0, 4.0
        	for _ in range(40):
        		mid = 0.5 * (lo + hi)
        		ok, _ = feasible(adj, [(p, r, pi)], eps, mid)
        		if ok: hi = mid
        		else:  lo = mid
        	out.append(hi)
        print(f'{alpha:9.5f} {eps:9.5f} {m:4d} {ev:8.4f} {1-ev:10.4f} '
              f'{1-ev/(1-alpha):11.4f} {out[0]:13.4f} {out[1]:13.4f}')

print()
print('=' * 78)
print('T1.f  Gale/Hall dual certificate: worst set S for the star at W=m')
print('  feasible(B) iff for every S:  sum_{u in S}[pr(r)_u - eps d_u]_+ '
      '<= B * r(N[S])')
print('=' * 78)
for alpha in (1 / 64,):
    for eps in (2.0 ** -8,):
        m = int(math.floor(1.0 / (8.0 * eps)))
        adj, seed = zoo.star(m)
        p, r, pi, W = state(adj, alpha, seed, 'tuned_degstat', m)
        d = np.array([len(adj[u]) for u in adj], float)
        dem = np.maximum(pi - p - eps * d, 0.0)
        # on the star only 3 set-types matter: {c}, subsets of leaves, and mixes
        for lab, S in (('{c}', [0]), ('all leaves', list(range(1, m + 1))),
                       ('V', list(range(m + 1))),
                       ('k=1 leaf', [1]), ('k=m/2 leaves',
                                           list(range(1, m // 2 + 1)))):
            NS = set()
            for u in S:
                NS.add(u); NS.update(adj[u])
            need = dem[S].sum(); have = sum(r[w] for w in NS)
            print(f'  alpha={alpha:.5f} eps={eps:.5f} m={m}  S={lab:14s} '
                  f'demand={need:.6f}  r(N[S])={have:.6f}  '
                  f'B_min={need/have:.4f}')
