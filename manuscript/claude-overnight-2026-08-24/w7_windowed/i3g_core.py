"""I3-G: FACE-ALIGNED retraction cap for the safeguarded AESP-CD recurrence.

Baseline (engine.py:155-156), hat coords xh = D^{-1/2}x:
    zeta(a)_i = ct_i - (Qt a)_i          (lower residual on supp(a))
    Delta     = max_{i in supp a} [ -zeta_i / (alpha d_i) ]_+
    rh_i      = min(beta dh_i, Delta)                     cap = Delta * 1
  In x-coordinates the cap is Delta * D^{1/2}1, and 1 is the Perron vector of
  the FULL operator M = D^{-1}Qt (M 1 = alpha 1, since Qt 1 = alpha d).

Face-aligned variant.  Let S = supp(a_t) be the current active face,
M_S = D_S^{-1} Qt_S, and w = w_S > 0 its (blockwise) Perron vector in hat
coordinates, M_S w = alpha_S w.  Cap along w instead of along 1:
    Delta_w = max_{i in S} [ -zeta_i / (Qt_S w)_i ]_+
    rh_i    = min(beta dh_i, Delta_w * w_i)               cap = Delta_w * w
  ( w = 1  =>  (Qt 1)_i = alpha d_i  =>  EXACTLY the baseline. )

SAFETY THEOREM (exact; holds for ANY w > 0 supported on S with Qt_S w > 0,
not only the Perron vector -- so w may be a *rational approximation* and the
whole algorithm stays exactly implementable in Fractions):

  Let ta = x* - a_t, ell = a_t - r, r_i = min(beta dh_i, Delta_w w_i).
  (i)   off supp(a): a_i = 0 with x_i,dh_i >= 0 forces x_i = dh_i = 0, so
        r_i = 0 and ell_i = 0 <= x*_i.
  (ii)  coords where the cap does NOT bind: r_i = beta dh_i, ell_i = x_i <= x*.
  (iii) coords where it binds: need ta_i + Delta_w w_i >= 0.  For i in S,
          (Qt_S ta_S)_i >= (Qt ta)_i >= zeta(a)_i
        (the first step because ta_j = x*_j >= 0 off S and Qt_ij <= 0; the
        second because (Qt x*)_i >= ct_i always, with equality on supp(x*)).
        Hence (Qt_S (ta_S + Delta_w w))_i >= zeta_i + Delta_w (Qt_S w)_i >= 0
        by the definition of Delta_w.  Qt_S is a nonsingular M-matrix
        (principal submatrix of the strictly diagonally dominant Z-matrix Qt),
        so Qt_S^{-1} >= 0 and ta_S + Delta_w w >= 0.
  => ell_t <= x* componentwise; x* is then a supersolution of the obstacle
     problem defining x_{t+1}, so x_{t+1} <= x* (e_{t+1} >= 0).  And
     r_i <= beta dh_i gives ell_t >= x_t, the monotone half.        [QED]

So the safeguard's invariant is preserved for EVERY positive cap direction, as
long as the trigger is recalibrated by (Qt_S w) instead of alpha*d.  The
baseline's alpha*d is the w = 1 instance of that rule.
"""
import sys, math
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
import numpy as np


# ------------------------------------------------------------------ Perron
def _components(adj, S):
    Sset = set(S); seen = set(); comps = []
    for s0 in S:
        if s0 in seen:
            continue
        stack = [s0]; comp = []
        seen.add(s0)
        while stack:
            u = stack.pop(); comp.append(u)
            for v in adj[u]:
                if v in Sset and v not in seen:
                    seen.add(v); stack.append(v)
        comps.append(sorted(comp))
    return comps


def perron_face(Qtf, df, adj, S):
    """Float Perron vector w (HAT coords) of M_S = D_S^{-1}Qt_S, blockwise,
    normalised max=1 per connected component.  Returns (w_dict, alpha_S_min)."""
    w = {}
    als = []
    for comp in _components(adj, S):
        idx = np.array(comp, int)
        ds = df[idx]
        Q = Qtf[np.ix_(idx, idx)]
        Ds = 1.0 / np.sqrt(ds)
        Qs = Ds[:, None] * Q * Ds[None, :]
        ev, V = np.linalg.eigh(Qs)
        v = V[:, 0]
        if v.sum() < 0:
            v = -v
        v = np.abs(v)                       # Perron: strictly positive
        wc = v / np.sqrt(ds)
        wc = wc / wc.max()
        for k, i in enumerate(comp):
            w[i] = float(wc[k])
        als.append(float(ev[0]))
    return w, (min(als) if als else 0.0)


def rationalise(w, den=10**9):
    return {i: Fr(v).limit_denominator(den) for i, v in w.items()}


# ------------------------------------------------------------------ caps
def cap_vector(mode, I, S, adj, exact):
    """Return (w, denom) where w[i] is the cap direction on S (hat coords) and
    denom[i] = (Qt_S w)_i > 0 is the trigger normaliser.  mode:
      'base' : w = 1        (denom = alpha*d, the engine's rule)
      'face' : w = Perron(M_S)
    """
    if mode == 'base':
        w = {i: (Fr(1) if exact else 1.0) for i in S}
    else:
        if exact:
            Qtf = np.array([[float(I.Qt[i][j]) for j in range(I.n)]
                            for i in range(I.n)])
            df = np.array([float(x) for x in I.d])
        else:
            Qtf, df = I.Qt, I.d
        wf, _ = perron_face(Qtf, df, adj, S)
        w = rationalise(wf) if exact else wf
    Q = I.Qt
    den = {}
    for i in S:
        if exact:
            den[i] = sum(Q[i][j] * w[j] for j in S)
        else:
            den[i] = float(sum(Q[i][j] * w[j] for j in S))
    return w, den


# ------------------------------------------------------------------ exact run
def run_exact(I, adj, T, mode='base', collect=True):
    """Exact Fraction run of the (possibly face-aligned) recurrence.
    Returns per-stage dicts with the full state so predicates can be checked."""
    n = I.n
    q, al, be, kap, mu = I.q, I.alpha, I.beta, I.kappa, I.mu
    d = I.d
    xm = [Fr(0)] * n
    x = [Fr(0)] * n
    Fstar = I.Fval(I.xstar)
    out = []
    for t in range(T):
        dh = [x[i] - xm[i] for i in range(n)]
        ah = [x[i] + be * dh[i] for i in range(n)]
        S = [i for i in range(n) if ah[i] > 0]
        Delta = Fr(0)
        w = {}; den = {}
        capok = True
        if S:
            w, den = cap_vector(mode, I, S, adj, exact=True)
            if any(den[i] <= 0 for i in S) or any(w[i] <= 0 for i in S):
                capok = False
                w = {i: Fr(1) for i in S}
                den = {i: al * d[i] for i in S}
            for i in S:
                zt = I.ct[i] - sum(I.Qt[i][j] * ah[j] for j in S)
                if zt < 0:
                    cand = -zt / den[i]
                    if cand > Delta:
                        Delta = cand
        cap = [Delta * w.get(i, Fr(0)) for i in range(n)]
        rh = [min(be * dh[i], cap[i]) for i in range(n)]
        ellh = [ah[i] - rh[i] for i in range(n)]
        # class: N / F (cap dominates everywhere => ell = x_t) / P
        if Delta == 0:
            cls = 'N'
        elif all(cap[i] >= be * dh[i] for i in range(n)):
            cls = 'F'
        else:
            cls = 'P'
        rec = dict(t=t, cls=cls, Delta=Delta, x=x[:], xm=xm[:], dh=dh, ah=ah,
                   rh=rh, ell=ellh, S=tuple(S), w=[w.get(i, Fr(0)) for i in range(n)],
                   capok=capok, cap=cap)
        if collect:
            e = [I.xstar[i] - x[i] for i in range(n)]
            zmx = [-e[i] + (1 / q - 1) * dh[i] for i in range(n)]
            cq = (1 + q) / q
            Dfin = -2 * cq * I.dotD(rh, zmx) + cq**2 * I.dotD(rh, rh)
            p = I.obstacle_solve(I.ct, kap, x, warm=I.Sstar)
            pmx = [p[i] - x[i] for i in range(n)]
            gapE = (I.Fval(p) - Fstar) + kap / 2 * I.dotD(pmx, pmx)
            Phi = gapE + mu / 2 * I.dotD(zmx, zmx)
            rec['Phi'] = Phi
            rec['Dfin'] = Dfin
            rec['EQ'] = I.dotQ(e, e)
            rec['gamma'] = (1 + mu * Dfin / (2 * Phi)) if Phi > 0 else Fr(1)
        xn = I.obstacle_solve(I.ct, kap, ellh, warm=S or None)
        rec['xn'] = xn[:]
        out.append(rec)
        xm, x = x, xn
    return out


