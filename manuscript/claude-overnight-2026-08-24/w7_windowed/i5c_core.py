"""I5-C: FACE-CALIBRATED MOMENTUM, exact.  (Route-B closer attempt.)

Builds on i3g_core (face-aligned cap + certified rational Perron machinery).
New ingredient: per-stage momentum beta_t calibrated to the CURRENT face
S_t = supp(a_t) (= supp(x_t) under the monotone invariant, for any beta_t>=0).

CERTIFIED RATIONAL CALIBRATION (all Fractions, no floats):
  From the Collatz-Wielandt bracket  lo <= alpha_S <= hi := ub  (i3g_core),
  take the UPPER end ub and set
      qr    = smallest k/M  with  (k/M)^2 >= ub/(1-ub)   (M = 1000; qr<=1)
      beta_t = (1-qr)/(1+qr)                              (beta_t = 0 if qr>=1)
  except qr = q (global) when q^2 >= ub/(1-ub), i.e. when ub <= alpha -- which
  by interlacing happens exactly on the full face (then beta_t = beta and the
  variant is bit-identical to the face-aligned cap = baseline there).

WHY THE UPPER END IS THE SAFE DIRECTION (this answers the calibration-direction
question).  Monotone SAFETY does not involve beta at all (audit below), so both
directions are "safe" for the sandwich.  The quantity beta_t controls is
DAMPING of the face low mode: the low-mode polynomial
    z^2 - m_S(1+beta_t) z + m_S beta_t,     m_S = kappa/(kappa+alpha_S),
has real roots (overdamped => a floor exists) iff
    4 beta_t/(1+beta_t)^2 = 1-qr^2 <= m_S   <=>  qr^2 >= alpha_S/(kappa+alpha_S).
An UPPER bound ub >= alpha_S certifies this:
    qr^2 >= ub/(1-ub) >= alpha_S/(1-alpha_S) >= alpha_S/(kappa+alpha_S),
(the last step needs alpha_S >= alpha, i.e. 1-alpha_S <= kappa+alpha_S).
A LOWER bound would give qr below the critical value => underdamped again =>
L-H lost: the lower end is the UNSAFE direction for the fix.
Per-face exact certificate stored in the record:  kappa/(kappa+ub) >= 1-qr^2.

SAFETY-IN-beta AUDIT (of the i3g_core Safety Theorem):
  beta_t appears in the stage-t proof in exactly two places:
   (b1) the definition a_t = x_t + beta_t d_t together with the cap
        r_i = min(beta_t dh_i, Delta_w w_i): the SAME beta_t in both.
        Case (ii) needs r_i = beta_t dh_i => ell_i = x_i; the monotone half
        needs r_i <= beta_t dh_i => ell_i >= x_i.  Both are structural in
        "the same beta_t", not in its value.
   (b2) beta_t >= 0, so that a_t >= x_t >= 0 and, in case (i), a_i = 0 forces
        x_i = beta_t dh_i = 0 (for beta_t = 0 case (i) instead follows from
        (H-mono) directly: a_i = x_i = 0 and dh_i <= x_i = 0).
  Cases (iii) [ta_S + Delta_w w >= 0 via the M-matrix], the supersolution step
  [x_{t+1} <= x* via (H-Mmat)], and (H-pos) do not mention beta_t.  No
  hypothesis couples beta_t to beta_{t-1}.  Hence the theorem holds verbatim
  for any stage-varying beta_t >= 0: SAFETY IS STAGE-LOCAL IN beta.
  One caveat, made explicit: the LOWER half of the induction (d_{t+1} >= 0)
  is the docstring's "hence x_t <= x_{t+1}"; it rests on ell_t >= x_t plus
  prox monotonicity through the subsolution property of x_t -- an invariant of
  the STATE, not of beta_t.  We do not re-derive it here; the engine verifies
  it exactly at every stage (mono_d / e_ge_0 / en_ge_0 flags).
"""
import sys, math
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, _gauss
from i3g_core import face_w_exact, components


def sqrt_ub_frac(X, M=1000):
    """Smallest k/M (k integer) with (k/M)^2 >= X >= 0.  Exact."""
    if X <= 0:
        return Fr(0)
    num, den = X.numerator, X.denominator
    t = num * M * M
    k = math.isqrt(t // den)
    while k * k * den < t:
        k += 1
    r = Fr(k, M)
    assert r * r >= X
    return r


def face_mom(I, ub, M=1000):
    """Certified face-calibrated (qr, beta) from an UPPER bound ub >= alpha_S.

    Guarantee (exact, all branches):  kappa/(kappa+ub) >= 1 - qr^2, hence
    m_S = kappa/(kappa+alpha_S) >= kappa/(kappa+ub) >= 4 beta/(1+beta)^2:
    the face low mode is (at least critically) damped.
    """
    q, kap = I.q, I.kappa
    if ub <= I.alpha:
        # full face (interlacing: ub >= alpha_S >= alpha, equality iff S=V):
        # global momentum, bit-identical to the baseline calibration.
        qr, be = q, I.beta
    elif 1 - ub <= 0:
        qr, be = Fr(1), Fr(0)
    else:
        q2 = ub / (1 - ub)
        qr = q if q * q >= q2 else sqrt_ub_frac(q2, M)
        if qr >= 1:
            qr, be = Fr(1), Fr(0)
        else:
            be = (1 - qr) / (1 + qr)
    # exact overdamping certificate (must hold in every branch)
    assert kap / (kap + ub) >= 1 - qr * qr, "overdamp cert failed"
    return qr, be


def run_i5c(I, T, variant='fm', k=8, den=10**14, M=1000, beta_fix=None,
            qr_fix=None, stop_on_unsafe=True):
    """Exact Fraction run.

    variant: 'base'   w=1 cap, trigger alpha*d, global beta   (engine baseline)
             'face'   face cap w^(k), global beta             (i4a variant)
             'fm'     face cap w^(k), PER-STAGE face-calibrated beta_t
             'fmlock' face cap, CONSTANT beta_fix (oracle: beta of S*)
             'bm'     w=1 cap + trigger alpha*d, per-stage face beta_t
    Returns per-stage records with safety flags, (qr, beta_t), CW bracket,
    overdamping certificate, and face-change marker.
    """
    n = I.n
    q, al, kap = I.q, I.alpha, I.kappa
    d, Qt, ct, xs = I.d, I.Qt, I.ct, I.xstar
    xm = [Fr(0)] * n
    x = [Fr(0)] * n
    wcache = {}     # S -> (w, dv, lo, hi)
    mcache = {}     # S -> (qr, beta)
    out = []
    Sprev = None
    for t in range(T):
        dh = [x[i] - xm[i] for i in range(n)]
        S0 = tuple(i for i in range(n) if x[i] > 0 or dh[i] > 0)
        # ---- momentum for this stage
        if variant in ('base', 'face'):
            qr, be = q, I.beta
        elif variant == 'fmlock':
            qr, be = qr_fix, beta_fix
        else:  # 'fm', 'bm': face-calibrated
            if not S0:
                qr, be = q, I.beta
            else:
                if S0 not in wcache:
                    wcache[S0] = face_w_exact(Qt, d, I.adj, list(S0), k=k,
                                              den=den)
                if S0 not in mcache:
                    mcache[S0] = face_mom(I, wcache[S0][3], M=M)
                qr, be = mcache[S0]
        ah = [x[i] + be * dh[i] for i in range(n)]
        S = tuple(i for i in range(n) if ah[i] > 0)
        # S == S0 whenever the monotone invariant holds (supp(dh) <= supp(x))
        face_ok = (S == S0) or (be == 0 and set(S) <= set(S0))
        # ---- cap direction + trigger denominator
        Delta = Fr(0)
        w, dv = {}, {}
        cwlo = cwhi = None
        if S:
            if variant in ('base', 'bm'):
                w = {i: Fr(1) for i in S}
                dv = {i: al * d[i] for i in S}
                if variant == 'bm' and S in wcache:
                    cwlo, cwhi = wcache[S][2], wcache[S][3]
            else:
                if S not in wcache:
                    wcache[S] = face_w_exact(Qt, d, I.adj, list(S), k=k,
                                             den=den)
                w, dv, cwlo, cwhi = wcache[S]
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
            cls = 'C'
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
            face_eq=face_ok,
        )
        rec = dict(t=t, cls=cls, Delta=Delta, S=S, x=x[:], xn=xn[:],
                   dh=dh, ah=ah, rh=rh, ell=ellh,
                   w=[w.get(i, Fr(0)) for i in range(n)], safe=safe,
                   cw=(cwlo, cwhi), qr=qr, beta=be,
                   change=(Sprev is not None and S != Sprev and t > 0),
                   rnz=any(v != 0 for v in rh))
        out.append(rec)
        if stop_on_unsafe and not all(safe.values()):
            rec['ABORT'] = True
            break
        Sprev = S
        xm, x = x, xn
    return out


# ---------------- exact algebra checks for the lemmas (rational identities)
def lemma_identity_checks(trials=200, seed=7):
    """(ii)  (1-qS^2) - m_S = 2 aS (a - aS) / ((1-aS)(kap+aS))   exactly,
       with qS^2 = aS/(1-aS), m_S = kap/(kap+aS), kap = 1-2a.
       (floor step)  (1+b) - b/(1-qr) = 1/(1+qr)  for b = (1-qr)/(1+qr).
       Both are rational identities; exact check over random rationals plus
       the cross-multiplied algebra in the findings note = proof."""
    import random
    rnd = random.Random(seed)
    ok1 = ok2 = 0
    for _ in range(trials):
        a = Fr(rnd.randint(1, 999), 10**4)          # alpha in (0, .1)
        aS = Fr(rnd.randint(1, 4999), 10**4)        # alpha_S in (0, .5)
        kap = 1 - 2 * a
        qS2 = aS / (1 - aS)
        mS = kap / (kap + aS)
        lhs = (1 - qS2) - mS
        rhs = 2 * aS * (a - aS) / ((1 - aS) * (kap + aS))
        ok1 += (lhs == rhs)
        qr = Fr(rnd.randint(1, 999), 1000)
        b = (1 - qr) / (1 + qr)
        ok2 += ((1 + b) - b / (1 - qr) == Fr(1, 1 + qr))
    return ok1, ok2, trials
