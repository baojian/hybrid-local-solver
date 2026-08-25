"""I4-F: sharp certificate amplification constant.

Conventions (repo):  Q=(1+a)/2 I - (1-a)/2 D^-1/2 A D^-1/2,  b=a D^-1/2 s,
  pi=D^1/2 x0,  err = max_i |pihat_i-pi_i|/d_i.
Push scale:  H pi = ga s,  H = I - c A D^-1,  c=(1-a)/(1+a), ga=2a/(1+a).
Identity:  D^-1/2 (Q xhat - b) = -((1+a)/2) D^-1 r,  r = ga s - H pihat.
  so  theta_Q := ||D^-1/2(Qxhat-b)||_inf = ((1+a)/2) * theta,  theta=max|r_j|/d_j.
Repo certificate: theta_Q < a*eps  <=>  theta < ga*eps  <=>  theta/(1-c) < eps.
Worst-case amplification (push scale) = 1/(1-c) = 1/ga = (1+a)/(2a).

NORMALISED amplification (task's A):
  A := err / ((1/a) * theta_Q) = err / (theta/(1-c)) = (1-c)*err/theta  in (0,1].
  A=1 <=> certificate exactly right; A<<1 <=> over-charges by 1/A.

SHARP support-conditional constant (this file's theorem):
  for r supported on T,  err <= Ahat(T)*theta/(1-c) with
  Ahat(T) = (1-c) * max_i G_i,  (I - cP)G = 1_T,  P=D^-1 A,
  and Ahat(T) = max_i pi^{(i)}(T)  (PPR mass from i landing in T)
  and the max is attained at some i in T. Sharp: attained by r = theta*d*1_T >= 0.
"""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla, sys, math
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/i4d")
import zoo, fam
from amglib import GModel


def consts(a):
    c = (1 - a) / (1 + a); ga = 2 * a / (1 + a)
    return c, ga


def exact(m):
    if m.n <= 30000:
        x0 = spla.spsolve(m.Q.tocsc(), m.b)
    else:
        x0, _ = spla.cg(m.Q, m.b, rtol=1e-13, atol=1e-20, maxiter=100000)
    return x0, x0 * m.sqd


def resid_push(m, pih):
    """r = ga s - H pihat,  H = I - c A D^-1."""
    c, ga = consts(m.alpha)
    r = -(pih - c * (m.A @ (pih / m.d)))
    r[m.seed] += ga
    return r


def stats(m, pih, pi, tol=0.0):
    r = resid_push(m, pih)
    th = float(np.max(np.abs(r) / m.d))
    err = float(np.max(np.abs(pih - pi) / m.d))
    c, ga = consts(m.alpha)
    T = np.flatnonzero(np.abs(r) > max(tol, 1e-14 * max(th, 1e-300) * m.d.max()))
    A = (1 - c) * err / th if th > 0 else float("nan")
    thQ = (1 + m.alpha) / 2.0 * th
    return dict(theta=th, thetaQ=thQ, err=err, A=A, nT=int(T.size),
                volT=float(m.d[T].sum()), signT=("+" if (r[T] >= -1e-18 * th * m.d[T]).all()
                                                 else ("-" if (r[T] <= 0).all() else "+-")))


def Gvec(m, T):
    """G = (I-cP)^-1 1_T = (D-cA)^-1 (d*1_T).  SPD solve."""
    c, _ = consts(m.alpha)
    K = (sp.diags(m.d) - c * m.A).tocsc()
    rhs = np.zeros(m.n); rhs[T] = m.d[T]
    if m.n <= 30000:
        G = spla.spsolve(K, rhs)
    else:
        G, _ = spla.cg(K, rhs, rtol=1e-12, atol=1e-20, maxiter=100000)
    return G


def Ahat_sharp(m, T):
    c, _ = consts(m.alpha)
    G = Gvec(m, T)
    return (1 - c) * float(G.max()), G


# ---- x_hat producers -------------------------------------------------
def xh_restricted(m, S):
    """exact solve of Q[S,S]; zero-extended. residual lives on the outer ring."""
    QS = m.Q[S][:, S].tocsc()
    xs = spla.spsolve(QS, m.b[S])
    xh = np.zeros(m.n); xh[S] = xs
    return xh * m.sqd


def bfs_shells(m):
    dist = np.full(m.n, -1, np.int64); dist[m.seed] = 0
    fr = np.array([m.seed]); sh = [fr]; r = 0
    while fr.size:
        nb = np.unique(np.concatenate([m.indices[m.indptr[v]:m.indptr[v+1]] for v in fr]))
        nb = nb[dist[nb] < 0]
        if nb.size == 0: break
        dist[nb] = r + 1; sh.append(nb); fr = nb; r += 1
    return sh, dist


def push_run(m, eps_appr):
    """lazy ACL push in the push scale; returns pihat, r, work (degree units)."""
    c, ga = consts(m.alpha)
    n = m.n
    p = np.zeros(n); r = np.zeros(n); r[m.seed] = ga
    W = 0.0
    inq = np.zeros(n, bool)
    from collections import deque
    q = deque()
    if r[m.seed] > eps_appr * m.d[m.seed]:
        q.append(m.seed); inq[m.seed] = True
    while q:
        u = q.popleft(); inq[u] = False
        ru = r[u]
        if ru <= eps_appr * m.d[u]:
            continue
        du = m.d[u]
        W += du
        p[u] += ru
        push = c * ru / du
        r[u] = 0.0
        nb = m.indices[m.indptr[u]:m.indptr[u+1]]
        r[nb] += push
        need = nb[(r[nb] > eps_appr * m.d[nb]) & (~inq[nb])]
        for v in need:
            q.append(int(v)); inq[v] = True
    return p, r, W


def ista_run(m, eps_appr, rho, iters=4000):
    """RPPR/ISTA on F_rho in push scale (proximal grad on x with l1 pen)."""
    a = m.alpha
    Q, b, sqd = m.Q, m.b, m.sqd
    L = (1 + a) / 2.0
    x = np.zeros(m.n)
    lam = a * rho
    for k in range(iters):
        g = Q @ x - b
        y = x - g / L
        thr = lam * sqd / L
        x = np.sign(y) * np.maximum(np.abs(y) - thr, 0.0)
        if k % 50 == 49:
            if float(np.max(np.abs(Q @ x - b) / sqd)) < eps_appr:
                break
    return x * sqd


def cheb_iterate(m, K):
    """K steps of Chebyshev on Qx=b -> signed dense-ish residual (no support)."""
    a = m.alpha; th = (1 + a) / 2.0; de = (1 - a) / 2.0
    Q, b = m.Q, m.b
    x = np.zeros(m.n); xp = np.zeros(m.n)
    r = b - Q @ x
    x = xp + r / th
    for k in range(2, K + 1):
        if k == 2: om = 2.0 / (2 - (de / th) ** 2 * 1.0)
        else: om = 1.0 / (1 - (de / th) ** 2 * om / 4.0)
        r = b - Q @ x
        xn = om * (x + r / th) + (1 - om) * xp
        xp = x; x = xn
    return x * m.sqd


# ---- candidate-certificate evaluators (moved from run2) ----
def neumann_curve_correct(m, T, Ks):
    """G = sum_k c^k P^k 1_T with P = D^-1 A (row-stochastic).  P y = D^-1 (A y)."""
    c, _ = consts(m.alpha)
    y = np.zeros(m.n); y[T] = 1.0
    acc = y.copy()
    cost = float(m.d[T].sum())
    out = {}
    kmax = max(Ks)
    for k in range(1, kmax + 1):
        nz = np.flatnonzero(y > 1e-300)
        cost += float(m.d[nz].sum())
        y = c * ((m.A @ y) / m.d)
        acc += y
        if k in Ks:
            out[k] = ((1 - c) * float(acc.max()) + c ** k, cost)
    return out


def escape_curve(m, T, Ks, cap=40000):
    """(e) localized supersolution: solve (I-cP)Ghat = 1_T on Omega_K = B_K(T)
    with pessimistic exterior Ghat = 1/(1-c).  Comparison principle => Ghat >= G
    on Omega, and max_i G_i is attained inside T subset Omega, so
    Ahat_e = (1-c) max_{i in Omega} Ghat_i  is SOUND.
    Charged cost = vol(Omega_K) reads + nnz of the local solve."""
    c, _ = consts(m.alpha)
    n = m.n
    inO = np.zeros(n, bool); inO[T] = True
    frontier = T
    out = {}
    kmax = max(Ks)
    for k in range(0, kmax + 1):
        if k in Ks:
            O = np.flatnonzero(inO)
            volO = float(m.d[O].sum())
            # (D - cA)[O,O] Ghat_O = d*1_T|_O + c A[O,Oc] * (1/(1-c)) ... in G-scale:
            # row i in O: d_i G_i - c sum_{j~i} G_j = d_i 1_T(i)
            #   -> d_i G_i - c sum_{j in O} A_ij G_j = d_i 1_T(i) + c*(#nb outside)*1/(1-c)
            K = (sp.diags(m.d) - c * m.A).tocsr()
            KO = K[O][:, O].tocsc()
            nout = m.d[O] - np.asarray(m.A[O][:, O].sum(axis=1)).ravel()
            rhs = np.where(np.isin(O, T), m.d[O], 0.0) + c * nout / (1 - c)
            Gh = spla.spsolve(KO, rhs)
            out[k] = ((1 - c) * float(Gh.max()), volO, int(KO.nnz))
        if k == kmax: break
        nb = np.unique(np.concatenate([m.indices[m.indptr[v]:m.indptr[v+1]]
                                       for v in frontier])) if frontier.size else np.array([],dtype=np.int64)
        nb = nb[~inO[nb]]
        if nb.size == 0 or int(inO.sum()) + int(nb.size) > cap:
            break
        inO[nb] = True; frontier = nb
    # fill any un-computed K with the last available (region exhausted / capped)
    if out:
        last = out[max(out)]
        for kk in Ks:
            if kk not in out and kk > max(out):
                out[kk] = last
    return out




def escape_profile(m, r, Ks, cap=60000):
    """(e') PROFILE localized supersolution -- the practical certificate.
    psi = |r|/d >= 0.  G = (I-cP)^-1 psi satisfies err <= max_i G_i, with
    EQUALITY when r has one sign.  max_i G_i is attained on T=supp(psi)
    (maximum principle).  Localize: Omega_K = B_K(T); set Ghat = theta/(1-c)
    outside (a valid global upper bound on G); solve on Omega.  M-matrix
    comparison => Ghat >= G on Omega => Ahat_e = (1-c)*max_{j in T} Ghat_j is SOUND.
    Cost charged: vol(Omega_K) row reads + nnz of the local system."""
    c, _ = consts(m.alpha)
    n = m.n
    psi = np.abs(r) / m.d
    th = float(psi.max())
    T = np.flatnonzero(psi > 1e-14 * th)
    inO = np.zeros(n, bool); inO[T] = True
    frontier = T
    out = {}
    kmax = max(Ks)
    Kmat = (sp.diags(m.d) - c * m.A).tocsr()
    for k in range(0, kmax + 1):
        if k in Ks:
            O = np.flatnonzero(inO)
            volO = float(m.d[O].sum())
            KO = Kmat[O][:, O].tocsc()
            nout = m.d[O] - np.asarray(m.A[O][:, O].sum(axis=1)).ravel()
            rhs = m.d[O] * psi[O] + c * nout * th / (1 - c)
            Gh = spla.spsolve(KO, rhs)
            inT = np.isin(O, T)
            out[k] = ((1 - c) * float(Gh[inT].max()) / th if th > 0 else 0.0,
                      volO, int(KO.nnz))
        if k == kmax: break
        nb = np.unique(np.concatenate([m.indices[m.indptr[v]:m.indptr[v+1]]
                                       for v in frontier])) if frontier.size else np.array([], dtype=np.int64)
        nb = nb[~inO[nb]]
        if nb.size == 0 or int(inO.sum()) + int(nb.size) > cap:
            break
        inO[nb] = True; frontier = nb
    if out:
        last = out[max(out)]
        for kk in Ks:
            if kk not in out and kk > max(out):
                out[kk] = last
    return out
