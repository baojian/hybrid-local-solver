"""cert.py -- production (e') certificate: profile-localized supersolution.

Repo semantics (lib/model.py):  Q = (1+a)/2 I - (1-a)/2 D^-1/2 A D^-1/2,
b = a D^-1/2 s, pi = D^1/2 x0, err(x_hat) = ||D^-1/2 (x_hat - x0)||_inf.

Push scale: H pi = ga s, H = I - c A D^-1, c=(1-a)/(1+a), ga=2a/(1+a);
r = ga s - H pi_hat;  psi = |r|/d;  theta = ||psi||_inf.
Exact identity:  D^-1/2(Q x_hat - b) = -((1+a)/2) D^-1 r.

TIER 0 (repo rule):  err <= theta/(1-c)   (worst-case sharp, I4-F Lemma 1).

TIER 1, certificate (e'):  let G = (I-cP)^-1 psi (P = D^-1 A row-stochastic).
Then err <= ||G||_inf, with EQUALITY when r is one-signed, and max G is
attained on T = supp(psi) (discrete maximum principle, I4-F Thm 2).
Localize: pick ANY Omega >= T, put the pessimistic exterior value
E = theta/(1-c) (a global upper bound on G) outside, and solve on Omega

    d_i Ghat_i - c sum_{j~i, j in Omega} Ghat_j = d_i psi_i + c |N(i)\Omega| E.

(I - cP)|Omega is a nonsingular M-matrix => Ghat >= G on Omega
(comparison principle), hence

    err <= max_{j in T} Ghat_j        -- SOUND for every K, every graph.

Self-consistent exterior upgrade ('sc'):  for any exterior u, the walk from u
must take >= 1 step to enter Omega before it can touch T, so by the strong
Markov property  Ehat := sup_ext G <= c * max_{ring} G, ring = {i in Omega
with an exterior neighbor}.  E enters the local system LINEARLY:
Ghat(E) = G0 + E*h with (D-cA)|O G0 = d psi, (D-cA)|O h = c*nout, and
h <= c < 1 entrywise (h_i = E_i[c^{tau_ext}] with exterior frozen at 1).
True G obeys G|O <= G0 + Ehat*h and Ehat <= c*max_ring(G0 + Ehat*h), so
Ehat is below the least fixed point  E* = max_{j in ring} c*G0_j/(1-c*h_j)
of the monotone c*max-affine map (contraction factor c*max h <= c^2 < 1).
Solving with E* is therefore SOUND, costs one extra solve with the same
factorization, and removes the log(1/alpha) radius penalty of the
pessimistic exterior (i5f radius theory: pessimistic needs
lam^K <= tau*sqrt(alpha); sc needs only lam^{2K} <~ tau).

ONLY the profile version is implemented.  The support version A(T) is a trap:
round-off inflates supp r and drives the bound to 1 (I4-F sec 6).

Charging: vol(Omega) adjacency reads, solver work (LU factor flops counted as
sum_j nnz(L_j)^2, or CG sweeps * nnz), one repair pass nnz for iterative
solves, |T| output reads.  All reported in the result and optionally pushed
into a campaign meter.
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# global soundness ledger (every assert_sound call is recorded)
SOUND_CHECKS = 0
VIOLATIONS = []


# ---------------------------------------------------------------- helpers --
def push_consts(alpha):
    c = (1.0 - alpha) / (1.0 + alpha)
    ga = 2.0 * alpha / (1.0 + alpha)
    return c, ga


def _csr(model):
    A = model.A.tocsr()
    return A, A.indptr, A.indices


def push_residual(model, x_hat):
    """r = ga s - H pihat in the push scale; pihat = D^1/2 x_hat."""
    c, ga = push_consts(model.alpha)
    pih = model.sqd * x_hat
    r = -(pih - c * (model.A @ (pih / model.d)))
    s = getattr(model, "s", None)
    if s is not None:
        r += ga * s
    else:
        r[model.seed] += ga
    return r


def K_schedule(alpha, tau=0.5, pessimistic=True):
    """Radius schedule.  Escape rate on the worst (1-D) geometry:
    lambda = (1-sqrt(a))/(1+sqrt(a)),  ln(1/lambda) = 2 artanh(sqrt(a)).
    Pessimistic-exterior inflation of the certified A is ~ lambda^K * O(1)
    ABSOLUTE, so to sit within (1+tau) of the K=inf bound whose scale is
    sqrt(alpha) we need lambda^K <= tau*sqrt(alpha):
        K = ceil( (ln(1/tau) + 0.5 ln(1/alpha)) / (2 artanh sqrt(alpha)) )
    i.e. the corrected Theta(log(1/alpha)/sqrt(alpha)) form (i5b).  With the
    self-consistent exterior the log(1/alpha) term drops:
        K = ceil( ln(1/tau)-ish / (2 artanh sqrt(alpha)) ) + O(1).
    """
    sa = math.sqrt(min(max(alpha, 1e-300), 1.0))
    rate = 2.0 * math.atanh(min(sa, 1 - 1e-12))
    if pessimistic:
        num = math.log(1.0 / tau) + 0.5 * math.log(1.0 / alpha)
    else:
        num = math.log(1.0 / tau) + 1.0
    return max(1, int(math.ceil(num / rate)))


def _grow_ball(indptr, indices, start, K, inO, cap):
    """BFS ball of radius K from `start` (bool mask inO updated in place).
    Returns list of frontier arrays; stops at cap vertices."""
    frontier = start
    for _ in range(K):
        if frontier.size == 0:
            break
        nb = np.unique(np.concatenate(
            [indices[indptr[v]:indptr[v + 1]] for v in frontier]))
        nb = nb[~inO[nb]]
        if nb.size == 0:
            break
        if int(inO.sum()) + nb.size > cap:
            inO[nb[:max(0, cap - int(inO.sum()))]] = True
            break
        inO[nb] = True
        frontier = nb
    return inO


# ------------------------------------------------------------ the product --
def certify_eprime(model, x_hat, K=None, tau=0.5, exterior="sc",
                   omega="ball", sc_rounds=3, solver="auto", cap=300000,
                   meter=None, r=None, hi_frac=0.90, K_lo_frac=0.25,
                   eps_target=None):
    """Certified semantic error bound for an arbitrary iterate x_hat.

    Returns dict with:
      err_bound   -- SOUND upper bound on ||D^-1/2(x_hat - x0)||_inf
      err_tier0   -- the repo-rule bound theta/(1-c) for comparison
      theta, K, nOmega, volOmega, nnz
      cost        -- dict(reads=vol(Omega) [+|T| discovery],
                          solve=charged solver work, total=...)
    exterior: 'pessimistic' (theta/(1-c)) or 'sc' (self-consistent, sound,
              removes the log(1/alpha) radius term; sc_rounds extra solves).
    omega:    'ball'      -> Omega = B_K(T)
              'multiscale'-> Omega = B_K(T_hi) U B_{K_lo}(T), T_hi = smallest
                             set carrying hi_frac of the psi d-mass.
    solver:   'splu' | 'cg' | 'auto'.  CG results are repaired to a sound
              supersolution by the row-sum bound on the inner residual.
    If meter is given, reads are charged as meter.scan_idx/scan and solver
    work as meter.resp.
    """
    alpha = model.alpha
    c, ga = push_consts(alpha)
    A, indptr, indices = _csr(model)
    n = model.n
    if r is None:
        r = push_residual(model, x_hat)
    psi = np.abs(r) / model.d
    theta = float(psi.max())
    tier0 = theta / (1.0 - c)
    if theta <= 0.0:
        return dict(err_bound=0.0, err_tier0=0.0, theta=0.0, K=0, nOmega=0,
                    volOmega=0.0, nnz=0, cost=dict(reads=0.0, solve=0.0,
                                                   total=0.0))
    # profile support with the discarded-dust correction (I4-F caveat 3):
    # dropped entries are absorbed into theta_dust and added to the bound.
    keep = psi > 1e-12 * theta
    theta_dust = float(psi[~keep].max()) if (~keep).any() else 0.0
    T = np.flatnonzero(keep)
    if K is None:
        K = K_schedule(alpha, tau, pessimistic=(exterior == "pessimistic"))
    inO = np.zeros(n, bool)
    if omega == "multiscale":
        # T_hi: smallest psi-set carrying hi_frac of sum d*psi
        w = model.d[T] * psi[T]
        o = np.argsort(psi[T])[::-1]
        cw = np.cumsum(w[o])
        khi = int(np.searchsorted(cw, hi_frac * cw[-1])) + 1
        Thi = T[o[:khi]]
        inO[T] = True
        _grow_ball(indptr, indices, T, max(1, int(K * K_lo_frac)), inO, cap)
        _grow_ball(indptr, indices, Thi, K, inO, cap)
    else:
        inO[T] = True
        _grow_ball(indptr, indices, T, K, inO, cap)
    O = np.flatnonzero(inO)
    volO = float(model.d[O].sum())
    if meter is not None:
        if hasattr(meter, "scan_idx"):
            meter.scan_idx(O)
        else:
            for u in O:
                meter.scan(int(u))
    # local system  (D - cA)|O  Ghat = d*psi|O + c*nout*E
    KO = (sp.diags(model.d[O]) - c * A[O][:, O]).tocsc()
    nout = model.d[O] - np.asarray(A[O][:, O].sum(axis=1)).ravel()
    ring = nout > 0
    nnz = int(KO.nnz)
    base = model.d[O] * psi[O]
    # solver policy: LU only on small windows where fill is affordable;
    # otherwise CG at MODERATE tolerance with the sound residual-repair
    # slack  Ghat := max(g,0) + ||rhs - K g||_{inf,1/d}/(1-c)
    # (row-sum bound (I-cP_loc)^{-1} 1 <= 1/(1-c); sound for ANY inexact g).
    # The slack is refined only until it stops mattering for the verdict.
    use_splu = (solver == "splu") or (solver == "auto" and O.size <= 8000)
    solve_charge = 0.0
    slack_goal = (0.1 * eps_target) if eps_target else None

    def _solve(rhs):
        nonlocal solve_charge
        if use_splu:
            if not hasattr(_solve, "lu"):
                _solve.lu = spla.splu(KO, permc_spec="MMD_AT_PLUS_A",
                                      diag_pivot_thresh=0.0,
                                      options=dict(SymmetricMode=True))
                Lm = _solve.lu.L.tocsc()
                cnt = np.diff(Lm.indptr).astype(float)
                _solve.ffl = float(np.sum(cnt ** 2))
                _solve.snz = 2.0 * float(Lm.nnz + _solve.lu.U.nnz)
                solve_charge += _solve.ffl
            solve_charge += _solve.snz
            g = _solve.lu.solve(rhs)
            rho = rhs - KO @ g
            solve_charge += nnz
            slack = float(np.max(np.abs(rho) / model.d[O])) / (1.0 - c)
            return np.maximum(g, 0.0) + slack
        g = np.zeros(O.size)
        rt = 3e-2
        for _ in range(6):
            it = [0]

            def cb(_):
                it[0] += 1
            g, info = spla.cg(KO, rhs, x0=g, rtol=rt, atol=0.0,
                              maxiter=100000, callback=cb)
            solve_charge += (it[0] + 2.0) * nnz
            rho = rhs - KO @ g
            slack = float(np.max(np.abs(rho) / model.d[O])) / (1.0 - c)
            gpos = np.maximum(g, 0.0)
            # refine only while the slack could change the verdict
            ref = float(gpos[np.isin(O, T)].max()) if T.size else 0.0
            goal = max(slack_goal or 0.0, 0.05 * ref)
            if slack <= max(goal, 1e-300) or rt <= 1e-12:
                break
            rt = max(rt * 1e-2, 1e-12)
        return gpos + slack

    Emax = theta / (1.0 - c)
    inT = np.isin(O, T)
    rounds = 0
    if exterior == "sc" and ring.any():
        # exact linear self-consistent exterior: Ghat(E) = G0 + E*h,
        # E* = least fixed point of E -> c*max_ring(G0 + E*h)  (h <= c < 1).
        G0 = _solve(base)
        h = _solve(c * nout)
        h = np.minimum(h, c)          # provable cap, guards fp round-off
        den = 1.0 - c * h[ring]
        E = float(np.max(c * G0[ring] / den))
        E = min(E, Emax)
        Gh = G0 + E * h
        rounds = 1
    else:
        E = Emax
        Gh = _solve(base + c * nout * E)
    bound = float(Gh[inT].max()) + theta_dust / (1.0 - c)
    bound = min(bound, tier0)
    if meter is not None and hasattr(meter, "resp"):
        meter.resp(solve_charge)
    cost = dict(reads=volO, solve=float(solve_charge),
                total=volO + float(solve_charge))
    return dict(err_bound=bound, err_tier0=tier0, theta=theta, K=int(K),
                nOmega=int(O.size), volOmega=volO, nnz=nnz, sc_rounds=rounds,
                cost=cost)


def certify_tier0(model, x_hat, r=None):
    """The repo rule's certified bound, in the same semantic units."""
    c, _ = push_consts(model.alpha)
    if r is None:
        r = push_residual(model, x_hat)
    theta = float(np.max(np.abs(r) / model.d))
    return theta / (1.0 - c)


def assert_sound(model, x_hat, out, x0=None, tag=""):
    """Compare a certificate output against the exact solve.  Any violation
    is recorded in VIOLATIONS and raised.  Returns true error."""
    global SOUND_CHECKS
    if x0 is None:
        x0 = model.solve_exact()
    err = float(np.max(np.abs(x_hat - x0) / model.sqd))
    SOUND_CHECKS += 1
    if out["err_bound"] < err * (1.0 - 1e-9):
        VIOLATIONS.append((tag, err, out["err_bound"]))
        raise AssertionError(
            f"(e') SOUNDNESS VIOLATION [{tag}]: bound {out['err_bound']:.6e}"
            f" < true err {err:.6e}")
    return err
