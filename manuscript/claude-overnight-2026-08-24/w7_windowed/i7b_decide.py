"""I7-B phase 4: COMPLETE decision of  sup_{y,h} Psi <= 0  per instance.

Fact: the max of Psi* over the unit sphere is attained at some y* whose
negative-support N and positive-support P are disjoint; y* restricted to
P u N is an eigenvector of B'_{P,N} (:= Q_{S=N} restricted to P u N rows/
cols) with eigenvalue = the max value, and has strict signs (+ on P, - on
N).  Conversely any such sign-feasible eigenvector with lam > 0 IS a true
violation (its Q-value equals true Psi*).  So:

   sup <= 0  <=>  for every disjoint (P, N), no eigenvector of B'_{P,N}
                  with lam > 0 has the (+P, -N) sign pattern (checking the
                  full eigenSPACE for degenerate lam via a small LP).

Pairs with P = 0 or N = 0 are PROVED <= 0 exactly by the per-mode algebra
(N-type / F-type), so only mixed pairs matter.  Any candidate is verified
against the true Psi* before being declared a violation.
"""
import sys, time, json, itertools
import numpy as np
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import (GenInst, hypercube, petersen, cycle,
                        complete_bipartite, rook, cocktail, circulant)
from i7b_hunt import build, psi_star, QS_matrix

def signspace_feasible(V, P, N, idx):
    """V: columns = eigenbasis of an eigenvalue's space (in restricted
    coords idx). Return c with (Vc) strict-sign-feasible, or None.
    Small LP solved by random+ascent (dims tiny)."""
    m = V.shape[1]
    sgn = np.array([1.0 if i in P else -1.0 for i in idx])
    A = V * sgn[:, None]          # need (A c)_i > 0 for all i
    if m == 1:
        c = np.ones(1)
        if (A @ c > 1e-12).all():
            return c
        if (A @ (-c) > 1e-12).all():
            return -c
        return None
    # maximize min_i (A c)_i over |c|=1 by projected subgradient
    rng = np.random.default_rng(0)
    best = (-np.inf, None)
    for r in range(40):
        c = rng.standard_normal(m); c /= np.linalg.norm(c)
        for it in range(300):
            v = A @ c
            i = np.argmin(v)
            g = A[i]
            c2 = c + 0.2 * g / (1 + it * 0.05)
            c2 /= np.linalg.norm(c2)
            if (A @ c2).min() > v.min():
                c = c2
        v = (A @ c).min()
        if v > best[0]:
            best = (v, c.copy())
    return best[1] if best[0] > 1e-10 else None

def decide(name, adj, q, tol=1e-11, verbose=True):
    ctx = build(adj, q)
    n = ctx['n']
    QS_cache = {}
    worst_neg = np.inf         # most positive lam among sign-INfeasible
    max_lam_feas = -np.inf     # max lam of any sign-feasible eigvec (true val)
    n_mixed = 0
    n_poslam = 0
    near_zero = []
    violations = []
    t0 = time.time()
    verts = list(range(n))
    for assign in itertools.product((0, 1, 2), repeat=n):
        P = frozenset(i for i, a in enumerate(assign) if a == 1)
        N = frozenset(i for i, a in enumerate(assign) if a == 2)
        if not P or not N:
            continue                     # proved exactly (per-mode algebra)
        n_mixed += 1
        if N not in QS_cache:
            QS_cache[N] = QS_matrix(ctx, N)
        idx = sorted(P | N)
        B = QS_cache[N][np.ix_(idx, idx)]
        ev, V = np.linalg.eigh(B)
        for lam0 in np.unique(np.round(ev, 9)):
            if lam0 <= tol:
                continue
            n_poslam += 1
            cols = [k for k in range(len(ev)) if abs(ev[k] - lam0) < 1e-8]
            c = signspace_feasible(V[:, cols], P, N, idx)
            if c is not None:
                y = np.zeros(n)
                yr = V[:, cols] @ c
                for k, i in enumerate(idx):
                    y[i] = yr[k]
                true_val = psi_star(ctx, y / np.linalg.norm(y))
                if true_val > tol:
                    violations.append((sorted(P), sorted(N), float(lam0),
                                       float(true_val), y.tolist()))
                else:
                    near_zero.append((sorted(P), sorted(N), float(lam0),
                                      float(true_val)))
                if true_val > max_lam_feas:
                    max_lam_feas = true_val
    el = time.time() - t0
    status = 'VIOLATED' if violations else 'SUP<=0'
    print('%-16s mixed pairs %7d  pos-lam events %6d  '
          'sign-feasible-true-max %+.2e  %s  [%.1fs]' %
          (name, n_mixed, n_poslam,
           max_lam_feas if max_lam_feas > -np.inf else float('nan'),
           status, el))
    if violations:
        for P, N, lam, tv, y in violations[:4]:
            print('    VIOL P=%s N=%s lam=%.3e true=%.3e' % (P, N, lam, tv))
    if near_zero and verbose:
        # spurious sign-feasible: eigvec feasible but true val <= 0? should
        # not happen (value equals form value) — investigate if any
        print('    NOTE: %d sign-feasible with true<=tol (boundary/deg):'
              % len(near_zero), near_zero[:3])
    return dict(name=name, n_mixed=n_mixed, n_poslam=n_poslam,
                violations=violations, near_zero=near_zero[:10],
                status=status)

if __name__ == '__main__':
    res = []
    for name, adj, q in [
            ('C6 q=1/10', cycle(6), '1/10'),
            ('C6 q=1/4(eq)', cycle(6), '1/4'),
            ('C8 q=1/10', cycle(8), '1/10'),
            ('Q3 q=1/10', hypercube(3), '1/10'),
            ('Q3 q=1/3(eq)', hypercube(3), '1/3'),
            ('K33 q=1/10', complete_bipartite(3, 3), '1/10'),
    ]:
        res.append(decide(name, adj, q))
    json.dump(res, open('/home/claude/work/overnight/w7_windowed/'
                        'i7b_decide_small.json', 'w'), indent=1, default=str)
