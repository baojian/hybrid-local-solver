"""I3-G / I4-A: FACE-ALIGNED retraction cap for the safeguarded AESP-CD recurrence.

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

---------------------------------------------------------------------------
I4-A AUDIT of the recovered theorem (all four gaps checked, see
findings/i4a_face_and_class.md S2).  The statement is CORRECT as written; the
induction it lives inside needs three standing hypotheses that the docstring
leaves implicit and that are added here:

  (H-mono)  d_t = x_t - x_{t-1} >= 0 and 0 <= x_t <= x*  (induction hypothesis
            at stage t; used in (i) and (ii)).
  (H-Mmat)  kappa = 1 - 2 alpha >= 0, so Qt + kappa D is also a nonsingular
            M-matrix and the obstacle LCP is monotone in its right-hand side;
            this is what turns "ell_t <= x*" into "x_{t+1} <= x*".
  (H-pos)   w > 0 on S and Qt_S w > 0 componentwise.

  Gap check 1 (case (iii) direction).  ell_i <= x*_i  <=>  ta_i + r_i >= 0,
  and r_i is a MIN, so both branches must be handled -- they are, (ii) and
  (iii) are exactly the two branches.  Nothing is proved in the wrong
  direction.
  Gap check 2 (Qt_S^{-1} >= 0).  Qt has diag d_i(1+alpha)/2 > 0, offdiag
  -(1-alpha)/2 <= 0, row sum of |offdiag| = d_i(1-alpha)/2 < diag for
  alpha > 0: strictly diagonally dominant Z-matrix => nonsingular M-matrix;
  every principal submatrix inherits this.  Correct.
  Gap check 3 (supersolution).  (Qt + kappa D)x* - (ct + kappa D x*) =
  Qt x* - ct >= 0 with equality on supp(x*): x* solves the obstacle LCP with
  rhs ct + kappa D x* >= ct + kappa D ell_t, and M-matrix LCPs are monotone in
  the rhs, so x_{t+1} <= x*.  Correct.
  Gap check 4 (a_t >= 0).  Needed for "ta_j = x*_j off S" and for supp(a) to
  be the whole support of d_t; it follows from (H-mono).  Correct.

CERTIFIED RATIONAL w WITHOUT EIGENSOLVERS.  (H-pos) is not an assumption to be
checked after the fact: take any y > 0 and set w := Qt_S^{-1} y.  Then
Qt_S w = y > 0 by construction and w > 0 because Qt_S^{-1} > 0 (irreducible
M-matrix).  Choosing y = D_S w_prev makes this ONE step of inverse iteration
for M_S = D_S^{-1}Qt_S:

    w^(0) = 1                       (= the baseline cap, exactly)
    w^(k) = normalize( Qt_S^{-1} D_S w^(k-1) )   ->  Perron vector of M_S,
                                                    rate (alpha_S/lam_2^S)^k.

Every w^(k), k >= 1, satisfies (H-pos) EXACTLY in Fractions with no eigenvalue
computation and no error analysis, and Collatz-Wielandt gives certified
rational two-sided bounds
    min_i (Qt_S w)_i/(d_i w_i)  <=  alpha_S  <=  max_i (Qt_S w)_i/(d_i w_i).
Rounding w to a bounded denominator is allowed provided Qt_S w > 0 is
re-verified exactly afterwards (cheap); we do that and fall back to the
unrounded w if it fails.
"""
import sys, math
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import _gauss


# --------------------------------------------------------------- components
def components(adj, S):
    Sset = set(S); seen = set(); comps = []
    for s0 in sorted(S):
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


# ------------------------------------------------ certified rational Perron
def face_w_exact(Qt, d, adj, S, k=8, den=10**14):
    """Exact-Fraction cap direction on the face S.

    k = 0 returns w == 1 (the BASELINE cap).  k >= 1 returns
    normalize((Qt_S^{-1} D_S)^k 1) per connected component of S, rounded to
    denominator `den` only if Qt_S w > 0 survives the rounding.

    Returns (w, den_vec, cw_lo, cw_hi) with
      den_vec[i] = (Qt_S w)_i  (> 0, certified exactly),
      cw_lo <= alpha_S <= cw_hi  (Collatz-Wielandt, per component minimum/max).
    """
    w = {}
    lo = hi = None
    for comp in components(adj, S):
        m = len(comp)
        wc = [Fr(1)] * m
        Qs = [[Qt[i][j] for j in comp] for i in comp]
        dc = [d[i] for i in comp]
        for _ in range(k):
            y = [dc[t] * wc[t] for t in range(m)]
            wc = _gauss([row[:] for row in Qs], y)
            mx = max(wc)
            wc = [v / mx for v in wc]
        if k >= 1 and den:
            wr = [v.limit_denominator(den) for v in wc]
            if all(v > 0 for v in wr):
                ok = all(sum(Qs[a][b] * wr[b] for b in range(m)) > 0
                         for a in range(m))
                if ok:
                    wc = wr
        for t, i in enumerate(comp):
            w[i] = wc[t]
        # Collatz-Wielandt bracket for alpha_S on this component
        for a in range(m):
            num = sum(Qs[a][b] * wc[b] for b in range(m))
            r = num / (dc[a] * wc[a])
            lo = r if lo is None else min(lo, r)
            hi = r if hi is None else max(hi, r)
    dv = {}
    for i in S:
        dv[i] = sum(Qt[i][j] * w[j] for j in S)
    return w, dv, lo, hi


# ------------------------------------------------------------------ exact run
def run_exact(I, T, mode='base', k=8, den=10**14, stop_on_unsafe=True):
    """Exact Fraction run of the (possibly face-aligned) recurrence.

    mode='base'  -> w = 1 (bit-identical to engine.Inst.run)
    mode='face'  -> w = w^(k), the certified inverse-iteration face vector.

    Records per stage: cls, Delta, S, w, cap, r, ell, x_t, x_{t+1}, and the
    four safety flags of the theorem.  Caches w per distinct face S.
    """
    n = I.n
    q, al, be, kap = I.q, I.alpha, I.beta, I.kappa
    d, Qt, ct, xs = I.d, I.Qt, I.ct, I.xstar
    xm = [Fr(0)] * n
    x = [Fr(0)] * n
    cache = {}
    out = []
    for t in range(T):
        dh = [x[i] - xm[i] for i in range(n)]
        ah = [x[i] + be * dh[i] for i in range(n)]
        S = tuple(i for i in range(n) if ah[i] > 0)
        Delta = Fr(0)
        w = {}
        dv = {}
        cwlo = cwhi = None
        if S:
            if mode == 'base':
                w = {i: Fr(1) for i in S}
                dv = {i: al * d[i] for i in S}
                cwlo = cwhi = al
            else:
                key = S
                if key not in cache:
                    cache[key] = face_w_exact(Qt, d, I.adj, list(S), k=k,
                                              den=den)
                w, dv, cwlo, cwhi = cache[key]
            for i in S:
                zt = ct[i] - sum(Qt[i][j] * ah[j] for j in S)
                if zt < 0:
                    cand = -zt / dv[i]
                    if cand > Delta:
                        Delta = cand
        cap = [Delta * w.get(i, Fr(0)) for i in range(n)]
        rh = [min(be * dh[i], cap[i]) for i in range(n)]
        ellh = [ah[i] - rh[i] for i in range(n)]
        if Delta == 0:
            cls = 'N'
        elif all(cap[i] >= be * dh[i] for i in range(n)):
            cls = 'F'
        elif all(cap[i] <= be * dh[i] for i in range(n)):
            cls = 'C'          # "clean": r = Delta*w exactly (P_w r = 0)
        else:
            cls = 'P'
        xn = I.obstacle_solve(ct, kap, ellh, warm=S or None)
        safe = dict(
            pos_den=all(dv[i] > 0 for i in S),
            pos_w=all(w[i] > 0 for i in S),
            mono_d=all(v >= 0 for v in dh),
            ell_ge_x=all(ellh[i] >= x[i] for i in range(n)),
            ell_le_xs=all(ellh[i] <= xs[i] for i in range(n)),
            e_ge_0=all(xs[i] >= x[i] for i in range(n)),
            en_ge_0=all(xs[i] >= xn[i] for i in range(n)),
        )
        rec = dict(t=t, cls=cls, Delta=Delta, S=S, x=x[:], xn=xn[:],
                   dh=dh, ah=ah, rh=rh, ell=ellh, cap=cap,
                   w=[w.get(i, Fr(0)) for i in range(n)], safe=safe,
                   cw=(cwlo, cwhi))
        out.append(rec)
        if stop_on_unsafe and not all(safe.values()):
            rec['ABORT'] = True
            break
        xm, x = x, xn
    return out
