"""I7-B phase 3: the doubled-orthant relaxation.

Variables (u, w) >= 0 in R^n x R^n (overlap allowed), y := u - w, but the
clip vector is taken as ym := w (>= true (y)_- on overlaps).  h eliminated
(sup over free h in closed form).  Define

  PsiRel(u, w) = |M P w|^2 + 2<M^2 P w, P(u-w)> - <P(u-w), M(m0-M) P(u-w)>
                 + nu^2 <l', S^{-1} l'>,
  l' = M(m0-M) P(u-w) - M^2 P w .

On disjoint (u,w) with u = y_+, w = y_- this equals sup_h Psi(y, h).
Claim to test:  PsiRel <= 0 on the doubled orthant  (=> free C9 everywhere).
This is copositivity of the 2n x 2n matrix B with [u;w]^T B [u;w] = PsiRel.
"""
import sys, time, json
import numpy as np
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import (GenInst, hypercube, petersen, cycle,
                        complete_bipartite, rook, cocktail, circulant)
from i7b_hunt import build

def big_B(ctx):
    """2n x 2n symmetric matrix of PsiRel on (u, w)."""
    n, d, P, M, nu = ctx['n'], ctx['d'], ctx['P'], ctx['M'], ctx['nu']
    D = ctx['D']
    A = ctx['A']          # M(m0-M)
    Sinv = ctx['Sinv']
    # linear maps of (u, w): z = P u - P w ; wP = P w
    Zu, Zw, Wm = P, -P, P
    T1u, T1w = 0*M, M @ P                    # M P w
    T2w = M @ (M @ P)                        # M^2 P w
    # PsiRel = |T1 w|^2 + 2<T2 w, z> - <z, A z> + nu^2 <l', Sinv l'>
    # as block form; build via stacking
    Lu = A @ P                                # part of l' from u
    Lw = -A @ P - T2w                         # from w  (z has -P w)
    B = np.zeros((2 * n, 2 * n))
    # |T1w|^2_D
    B[n:, n:] += T1w.T @ D @ T1w
    # 2<T2 w, z>_D = 2 w^T T2w^T D (P u - P w)
    Cross = T2w.T @ D @ P
    B[n:, :n] += Cross
    B[:n, n:] += Cross.T
    B[n:, n:] += -(Cross + Cross.T)
    # -<z, A z>_D with z = P(u - w)
    AzP = P.T @ D @ (A @ P)
    B[:n, :n] += -AzP
    B[n:, n:] += -AzP
    B[:n, n:] += AzP
    B[n:, :n] += AzP.T
    # + nu^2 l'^T D Sinv l',  l' = Lu u + Lw w
    K = D @ Sinv
    B[:n, :n] += (nu ** 2) * (Lu.T @ K @ Lu)
    B[:n, n:] += (nu ** 2) * (Lu.T @ K @ Lw)
    B[n:, :n] += (nu ** 2) * (Lw.T @ K @ Lu)
    B[n:, n:] += (nu ** 2) * (Lw.T @ K @ Lw)
    return 0.5 * (B + B.T)

def orthant_max(B, iters=6000, restarts=200, rng=None):
    """max s^T B s over s >= 0, |s| = 1 by projected power/gradient ascent."""
    rng = rng or np.random.default_rng(11)
    N = B.shape[0]
    best = (-np.inf, None)
    for r in range(restarts):
        s = np.abs(rng.standard_normal(N)) if r else np.ones(N)
        s /= np.linalg.norm(s)
        step = 0.5
        val = s @ B @ s
        for it in range(iters // 10):
            g = 2 * (B @ s)
            s2 = np.maximum(s + step * (g - s * (g @ s)), 0.0)
            nn = np.linalg.norm(s2)
            if nn == 0:
                break
            s2 /= nn
            v2 = s2 @ B @ s2
            if v2 > val + 1e-16:
                s, val = s2, v2
                step = min(step * 1.3, 2.0)
            else:
                step *= 0.5
                if step < 1e-10:
                    break
        if val > best[0]:
            best = (val, s.copy())
    return best

def check_graph(name, adj, q):
    ctx = build(adj, q)
    B = big_B(ctx)
    val, s = orthant_max(B)
    n = ctx['n']
    print('%-16s  orthant max of PsiRel = %+.4e' % (name, val))
    if val > 1e-10:
        u, w = s[:n], s[n:]
        ov = np.minimum(u, w)
        print('     VIOLATION cand.: overlap |min(u,w)|=%.3e  u=%s w=%s' %
              (np.linalg.norm(ov), np.round(u, 3), np.round(w, 3)))
    return val, s, B, ctx

if __name__ == '__main__':
    out = {}
    for name, adj, q in [
            ('C6 q=1/10', cycle(6), '1/10'),
            ('C6 q=1/4(eq)', cycle(6), '1/4'),
            ('Pet q=1/10', petersen(), '1/10'),
            ('Pet q=1/3(eq)', petersen(), '1/3'),
            ('Q4 q=1/10', hypercube(4), '1/10'),
            ('Q4 q=1/4(eq)', hypercube(4), '1/4'),
            ('Q3 q=1/10', hypercube(3), '1/10'),
            ('K33 q=1/10', complete_bipartite(3, 3), '1/10'),
            ('C8 q=1/10', cycle(8), '1/10'),
            ('C10 q=1/20', cycle(10), '1/20'),
            ('C12 q=1/20', cycle(12), '1/20'),
            ('Q5 q=1/10', hypercube(5), '1/10'),
    ]:
        val, s, B, ctx = check_graph(name, adj, q)
        out[name] = float(val)
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i7b_relax.json', 'w'), indent=1)
