"""I7-B phase 2: maximize Psi over FREE (y, h) — h eliminated in closed form.

Psi*(y) = C0(y) + nu^2 <l'(y), S^{-1} l'(y)>_D
  C0 = |M P ym|^2 + 2<M^2 P ym, Py> - <Py, M(m0-M) Py>
  l' = M(m0-M) P y - M^2 P ym ,   ym = (-y)_+
  S  = nu^2 m0 M + beta (m0 - 2M + M^2)   (PD on 1^perp in class)

sup_{y,h} Psi <= 0  <=>  C9 holds at EVERY stage for ANY cap Delta and ANY
(h, hm) — the fully unconditional form.  Per sign-pattern S (= supp ym),
Psi* is an explicit quadratic form Q_S; the global sign question is
  max_S  max_{y in cone(S)} y^T Q_S y  vs  0.
Strategy: (1) enumerate patterns (n<=10) / orbit-reps+random (n=16);
lam_max(Q_S) <= 0 for all S => proven NSD on the whole space (no cone
needed).  (2) else check top eigvecs against cones + projected ascent.
"""
import sys, time, itertools, json
import numpy as np
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import (GenInst, hypercube, petersen, cycle,
                        complete_bipartite, rook, cocktail, circulant)

def build(adj, q):
    n = len(adj)
    I = GenInst(adj, [Fr(1, n)] * n, Fr(q), Fr(1, 8 * n * n))
    d = np.array([float(x) for x in I.d]); vol = d.sum()
    M = np.array([[float(x) for x in row] for row in I.Mm])
    m0, be = float(I.m0), float(I.beta)
    qf = float(I.q); nu = qf / (1 + qf)
    D = np.diag(d)
    P = np.eye(n) - np.outer(np.ones(n), d) / vol      # P u = u - meanD(u) 1
    MP = M @ P
    M2P = M @ MP
    A_mmM = M @ (m0 * np.eye(n) - M)                   # M(m0-M)
    G = m0 * np.eye(n) - 2 * M + M @ M                 # Gslack operator
    S = nu * nu * m0 * M + be * G                      # on 1^perp PD
    # S^{-1} restricted to 1^perp: regularize on span{1}
    S_reg = S + np.outer(np.ones(n), d) / vol
    Sinv = np.linalg.inv(S_reg)
    return dict(n=n, I=I, d=d, vol=vol, M=M, m0=m0, be=be, nu=nu, P=P,
                MP=MP, M2P=M2P, A=A_mmM, S=S, Sinv=Sinv, D=D)

def psi_star(ctx, y):
    d, P, M, nu = ctx['d'], ctx['P'], ctx['M'], ctx['nu']
    ym = np.maximum(-y, 0.0)
    Py, Pym = P @ y, P @ ym
    MPym = M @ Pym
    M2Pym = M @ MPym
    Az = ctx['A'] @ Py
    C0 = (d * MPym) @ MPym + 2 * (d * M2Pym) @ Py - (d * Az) @ Py
    lp = Az - M2Pym
    return C0 + nu * nu * (d * lp) @ (ctx['Sinv'] @ lp)

def QS_matrix(ctx, Sset):
    """Symmetric matrix B (standard metric embedded with D) with
    y^T B y = Psi*_S(y) for y in pattern-S cone."""
    n, d, P, M, nu = ctx['n'], ctx['d'], ctx['P'], ctx['M'], ctx['nu']
    R = np.zeros((n, n))
    for i in Sset:
        R[i, i] = -1.0
    PR = P @ R
    T1 = M @ PR                      # MPym = T1 y
    T2 = M @ T1                      # M2Pym
    Az = ctx['A'] @ P                # M(m0-M)P
    D = ctx['D']
    B = T1.T @ D @ T1 \
        + T2.T @ D @ P + P.T @ D @ T2 \
        - P.T @ D @ Az
    L = Az - T2                      # l' = L y
    B = B + nu * nu * (L.T @ D @ ctx['Sinv'] @ L)
    return 0.5 * (B + B.T)

def analyse_graph(name, adj, q, max_patterns=None, rng=None, npat_rand=4000):
    ctx = build(adj, q)
    n = ctx['n']
    worst = (-np.inf, None, None)
    n_pos = 0
    patterns = None
    if n <= 12:
        patterns = [frozenset(s) for r in range(n + 1)
                    for s in itertools.combinations(range(n), r)]
    else:
        rng = rng or np.random.default_rng(7)
        pats = set()
        # structured: singletons, pairs, spheres around 0, complements
        for i in range(n):
            pats.add(frozenset([i]))
            pats.add(frozenset(range(n)) - frozenset([i]))
        for i in range(n):
            for j in adj[i]:
                pats.add(frozenset([i, j]))
        while len(pats) < npat_rand:
            k = rng.integers(1, n)
            pats.add(frozenset(rng.choice(n, size=k, replace=False).tolist()))
        patterns = list(pats)
    t0 = time.time()
    for Sset in patterns:
        B = QS_matrix(ctx, Sset)
        ev, V = np.linalg.eigh(B)
        lm = ev[-1]
        if lm > worst[0]:
            worst = (lm, Sset, V[:, -1].copy())
        if lm > 1e-11:
            n_pos += 1
    lm, Sw, vw = worst
    print('%-14s n=%d q=%s  patterns=%d  max lam_max(Q_S) = %+.3e  '
          '(#patterns with lam_max>0: %d)  [%.1fs]' %
          (name, n, q, len(patterns), lm, n_pos, time.time() - t0))
    # cone check + direct ascent regardless
    best = (-np.inf, None)
    rng = rng or np.random.default_rng(3)
    starts = [rng.standard_normal(n) for _ in range(400)]
    if vw is not None:
        starts += [vw, -vw]
    # structured starts: (H-K) pair bumps, distance profiles
    for i in range(min(n, 6)):
        e = np.zeros(n); e[i] = 1.0
        for j in adj[i]:
            for tau in (0.2, 1.0, 5.0):
                v = e.copy(); v[j] = -tau
                starts.append(v)
                starts.append(-v)
    f = lambda y: psi_star(ctx, y)
    for y0 in starts:
        y = y0 / np.linalg.norm(y0)
        val = f(y)
        step = 0.3
        for it in range(300):
            g = num_grad(f, y)
            g = g - y * (g @ y)
            y2 = y + step * g
            y2 /= np.linalg.norm(y2)
            v2 = f(y2)
            if v2 > val + 1e-15:
                y, val = y2, v2
                step = min(step * 1.25, 1.0)
            else:
                step *= 0.5
                if step < 1e-9:
                    break
        if val > best[0]:
            best = (val, y.copy())
    print('     direct ascent: max Psi* on sphere = %+.4e' % best[0])
    return dict(name=name, lam_max=float(lm), pat=sorted(Sw), npos=n_pos,
                ascent=float(best[0]),
                y_best=best[1].tolist() if best[1] is not None else None)

def num_grad(f, y, h=1e-7):
    g = np.zeros_like(y)
    f0 = f(y)
    for i in range(len(y)):
        y2 = y.copy(); y2[i] += h
        g[i] = (f(y2) - f0) / h
    return g

if __name__ == '__main__':
    res = []
    for name, adj, q in [
            ('C6 q=1/10', cycle(6), '1/10'),
            ('C6 q=1/4(eq)', cycle(6), '1/4'),
            ('Pet q=1/10', petersen(), '1/10'),
            ('Pet q=1/4', petersen(), '1/4'),
            ('Pet q=1/3(eq)', petersen(), '1/3'),
            ('Q4 q=1/10', hypercube(4), '1/10'),
            ('Q4 q=1/4(eq)', hypercube(4), '1/4'),
    ]:
        res.append(analyse_graph(name, adj, q))
    json.dump(res, open('/home/claude/work/overnight/w7_windowed/'
                        'i7b_hunt.json', 'w'), indent=1)
