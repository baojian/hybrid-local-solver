"""W5: Truncated (thresholded) Chebyshev iteration for Q x = b with certified
truncation-error control.

Conventions (lib/model.py): Q = (1+a)/2 I - (1-a)/2 N, spec(Q) in [alpha,1],
b = alpha D^{-1/2} e_v.  Semantic err = ||D^{-1/2}(x-x0)||_inf; certificate
||D^{-1/2}(Qx-b)||_inf < alpha*eps  =>  err < eps.

Chebyshev: theta=(1+alpha)/2, delta=(1-alpha)/2, sigma=theta/delta,
t_k = T_k(sigma), residual poly r_k(l) = T_k((theta-l)/delta)/t_k,
iterate  y_{k+1} = rho_k (y_k + (b-Q y_k)/theta) + (1-rho_k) y_{k-1},
rho_k = 2 sigma t_k/t_{k+1} = 2 sigma u_k, u_k = 1/(2 sigma - u_{k-1}),
u_0 = 1/sigma;  starter y_1 = y_0 + (b-Q y_0)/theta.

ERROR PROPAGATION (exact; proved by the Chebyshev 3-term identity):
if truncation removes g_k from y_k (y_k <- y_k - g_k) at steps k=1..K, then
  y_K - x* = r_K(Q)(y_0 - x*) - sum_k (t_k/t_K) U_{K-k}((theta I - Q)/delta) g_k
(U_m = 2nd-kind Chebyshev; proof: v_j = t_j u_j turns the homogeneous
recurrence into v_{j+1} = 2 mu v_j - v_{j-1}, mu=(theta-l)/delta in [-1,1]).
Hence with |U_m| <= m+1 on [-1,1] and t_k/t_K <= 2 lam^{K-k},
  ||Q y_K - b||_2 <= ||r_0||_2/t_K + sum_k 2 (K-k+1) lam^{K-k} ||g_k||_2,
and since ||D^{-1/2} v||_inf <= ||v||_2 (d_i>=1) this certifies the semantic
error.  A_bar(alpha) = max_m 2(m+1) lam^m ~ (2/e)/(2 sqrt(alpha)) is the
uniform-in-horizon amplification of a single injection.
"""
import math
import sys
import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/lib")
from model import Model  # noqa: E402
import zoo  # noqa: E402,F401


def consts(alpha):
    theta = (1 + alpha) / 2.0
    delta = (1 - alpha) / 2.0
    sigma = theta / delta
    ra = math.sqrt(alpha)
    lam = (1 - ra) / (1 + ra)
    return theta, delta, sigma, lam


def A_bar(alpha):
    """max_m 2 (m+1) lam^m : uniform worst-case amplification of one
    unit-2-norm truncation injection into the final 2-norm residual."""
    _, _, _, lam = consts(alpha)
    if lam >= 1.0:
        return 2.0
    m_est = max(1, int(-1.0 / math.log(lam)))
    best = 2.0
    for m in range(0, 6 * m_est + 12):
        w = 2.0 * (m + 1) * lam ** m
        if w > best:
            best = w
    return best


def K_cert(alpha, eps, r0norm2, share=0.45):
    """First K with r0norm2/t_K <= share*alpha*eps (t_K=cosh(K acosh sigma))."""
    _, _, sigma, _ = consts(alpha)
    need = max(1.0, r0norm2 / (share * alpha * eps))
    return int(math.ceil(math.acosh(need) / math.acosh(sigma))) + 2


class VecMeter:
    """Vectorized meter with identical accounting to lib.meter.Meter:
    scan(u) charges d_u; first exposure -> C_adj, repeats -> R_adj."""

    def __init__(self, model):
        self.dv = model.d
        self.seen = np.zeros(model.n, dtype=bool)
        self.C_adj = 0.0
        self.R_adj = 0.0
        self.C_rec = 0.0
        self.C_resp = 0.0
        self.C_mat = 0.0
        self.C_emit = 0.0

    def scan_mask(self, mask):
        new = mask & ~self.seen
        self.C_adj += float(self.dv[new].sum())
        self.R_adj += float(self.dv[mask & self.seen].sum())
        self.seen |= new

    def rec(self, k=1):
        self.C_rec += k

    def resp(self, k=1):
        self.C_resp += k

    def scan_work(self):
        return self.C_adj + self.R_adj

    def total(self):
        return (self.C_adj + self.R_adj + self.C_rec + self.C_resp
                + self.C_mat + self.C_emit)

    def vector(self):
        return dict(C_adj=self.C_adj, R_adj=self.R_adj, C_rec=self.C_rec,
                    C_resp=self.C_resp, total=self.total())


def cheb_sweep(model, eps, mode="none", tau0=0.0, beta=1.0, tau_cap=None,
               K_max=None, x_init=None, meter=None, x_exact=None,
               stop="ledger", allow_step=None, hard_factor=3, record=False):
    """One Chebyshev sweep (no restart).

    mode: 'none' | 'fixed' (tau_k=tau0) | 'decay' (tau_k=tau0*beta^k) |
          'cert' (2-norm-greedy truncation under per-step ledger allowance).
    Truncation: zero coords with |x_i| < tau_k*sqrt(d_i) (fixed/decay), or the
    largest small-|x| prefix with ||g||_2 <= allow_step (cert), always
    restricted to |x_i| < tau_cap*sqrt(d_i) if tau_cap given.
    stop: 'ledger' (analytic 2-norm certificate < alpha*eps),
          'oracle' (semantic err vs x_exact <= eps),
          'cert_oracle' (true cert ||D^{-1/2}(Qx-b)||_inf <= alpha*eps,
          evaluated out-of-band each step, uncharged - baseline stopping),
          'K' (exactly K_max steps).
    Charges meter: per iteration scan_mask over supp(y_k) U {seed} + rec for
    coordinate writes.  Ledger is O(1)/step via geometric running sums.
    """
    alpha = model.alpha
    theta, delta, sigma, lam = consts(alpha)
    Q, b, sqd, n = model.Q, model.b, model.sqd, model.n
    dv = model.d
    seed = int(np.argmax(np.abs(b)))
    target = alpha * eps
    Ab = A_bar(alpha)
    m = meter

    x_prev = np.zeros(n) if x_init is None else np.asarray(x_init, float).copy()
    # ---- starter: y_1 = y_0 + r_0/theta (charged) ----
    supp = (x_prev != 0.0)
    supp[seed] = True
    if m:
        m.scan_mask(supp)
    r0 = b - Q @ x_prev
    r0n2 = float(np.linalg.norm(r0))
    x = x_prev + r0 / theta
    if m:
        m.rec(int(np.count_nonzero(x)))

    if K_max is None:
        K_max = K_cert(alpha, eps, r0n2)
    if allow_step is None and mode == "cert":
        allow_step = 0.45 * target / (Ab * max(1, K_max))
    hard = hard_factor * K_max + 5

    t_prev, t_cur = 1.0, sigma
    ucoef = 1.0 / sigma          # u_0 = t_0/t_1
    Sa = 0.0                     # sum lam^{k-j} ||g_j||
    Sb = 0.0                     # sum (k-j) lam^{k-j} ||g_j||
    k = 1
    status = "maxed"
    vol_hist = [] if record else None
    supp_hist = [] if record else None
    g_hist = [] if record else None
    n_trunc_tot = 0

    while True:
        # ---- ledger shift to index k, then truncate y_k ----
        Sb = lam * (Sb + Sa)
        Sa = lam * Sa
        g2 = 0.0
        if mode != "none":
            if mode in ("fixed", "decay"):
                tk = tau0 * (beta ** k if mode == "decay" else 1.0)
                mask = (x != 0.0) & (np.abs(x) < tk * sqd)
                mask[seed] = False
                cnt = int(np.count_nonzero(mask))
                if cnt:
                    g2 = float(np.linalg.norm(x[mask]))
                    x[mask] = 0.0
                    n_trunc_tot += cnt
            else:  # cert: greedy smallest-|x| prefix with ||g||_2<=allow_step
                if tau_cap is not None:
                    cand = np.flatnonzero((x != 0.0)
                                          & (np.abs(x) < tau_cap * sqd))
                else:
                    cand = np.flatnonzero(x)
                cand = cand[cand != seed]
                if cand.size:
                    v2 = x[cand] ** 2
                    order = np.argsort(v2)
                    cs = np.cumsum(v2[order])
                    cnt = int(np.searchsorted(cs, allow_step ** 2, side="right"))
                    if cnt > 0:
                        idx = cand[order[:cnt]]
                        g2 = float(np.sqrt(cs[cnt - 1]))
                        x[idx] = 0.0
                        n_trunc_tot += cnt
            Sa += g2
        if record:
            g_hist.append(g2)
        # ---- stopping at index k ----
        bound = r0n2 / t_cur + 2.0 * (Sa + Sb)   # >= ||Q y_k - b||_2
        if m:
            m.resp(1)
        done = False
        if stop == "ledger" and bound < target:
            status = "cert"
            done = True
        elif stop == "oracle" and x_exact is not None:
            if float(np.max(np.abs(x - x_exact) / sqd)) <= eps:
                status = "oracle"
                done = True
        elif stop == "cert_oracle":
            cr = float(np.max(np.abs(b - Q @ x) / sqd))
            if cr <= target:
                status = "cert_oracle"
                done = True
        elif stop == "K" and k >= K_max:
            status = "K"
            done = True
        if not done and k >= hard:
            status = "maxed"
            done = True
        if done:
            break
        # ---- step k -> k+1 (charged) ----
        supp = (x != 0.0)
        supp[seed] = True
        if m:
            m.scan_mask(supp)
        if record:
            vol_hist.append(float(dv[supp].sum()))
            supp_hist.append(int(supp.sum()))
        r = b - Q @ x
        ucoef = 1.0 / (2.0 * sigma - ucoef)
        rho = 2.0 * sigma * ucoef
        x_new = rho * (x + r / theta) + (1.0 - rho) * x_prev
        if m:
            m.rec(int(np.count_nonzero(x_new)))
        x_prev, x = x, x_new
        t_prev, t_cur = t_cur, 2.0 * sigma * t_cur - t_prev
        k += 1

    out = dict(x=x, k=k, status=status, bound=bound, K_max=K_max,
               n_trunc=n_trunc_tot, allow_step=allow_step, r0n2=r0n2)
    if record:
        out["vol_hist"] = vol_hist
        out["supp_hist"] = supp_hist
        out["g_hist"] = g_hist
    return out


def cheb_meas(model, eps, meter, tau_frac=0.25, record=False,
              hard_factor=8):
    """Best certified variant: per-iteration MEASURED certificate.
    Every step already computes r_k = b - Q y_k on the charged scan of
    supp(y_k); ||D^{-1/2} r_k||_inf < alpha*eps is a true certificate, free.
    Truncation: semantic threshold |x_i| < tau*sqrt(d_i), tau adaptive
    (start tau_frac*eps, quartered whenever the running-min certificate
    stalls over a window of ceil(2/sqrt(alpha)) steps).  Correctness never
    depends on the truncation ledger; only termination speed does."""
    alpha = model.alpha
    theta, delta, sigma, lam = consts(alpha)
    Q, b, sqd, n = model.Q, model.b, model.sqd, model.n
    dv = model.d
    seed = int(np.argmax(np.abs(b)))
    target = alpha * eps
    tau = tau_frac * eps
    win = int(math.ceil(2.0 / math.sqrt(alpha))) + 5
    Kc = K_cert(alpha, eps, alpha)
    hard = hard_factor * Kc + 10

    x_prev = np.zeros(n)
    supp = x_prev != 0.0
    supp[seed] = True
    meter.scan_mask(supp)
    r = b - Q @ x_prev
    x = x_prev + r / theta
    meter.rec(1)
    ucoef = 1.0 / sigma
    best_cert = math.inf
    last_improve = 1
    k = 1
    vol_hist = [] if record else None
    while True:
        # truncate y_k (semantic threshold)
        mask = (x != 0.0) & (np.abs(x) < tau * sqd)
        mask[seed] = False
        if mask.any():
            x[mask] = 0.0
        supp = x != 0.0
        supp[seed] = True
        meter.scan_mask(supp)
        if record:
            vol_hist.append(float(dv[supp].sum()))
        r = b - Q @ x
        meter.rec(int(supp.sum()))
        cert = float(np.max(np.abs(r) / sqd))
        if cert < target:
            return dict(x=x, status="cert", k=k, iters=k, cert=cert,
                        tau_final=tau, vol_hist=vol_hist)
        if cert < 0.75 * best_cert:
            best_cert = cert
            last_improve = k
        elif k - last_improve >= win:
            tau *= 0.25          # truncation floor reached: back off
            last_improve = k
        if k >= hard:
            return dict(x=x, status="maxed", k=k, iters=k, cert=cert,
                        tau_final=tau, vol_hist=vol_hist)
        ucoef = 1.0 / (2.0 * sigma - ucoef)
        rho = 2.0 * sigma * ucoef
        x_new = rho * (x + r / theta) + (1.0 - rho) * x_prev
        meter.rec(int(np.count_nonzero(x_new)))
        x_prev, x = x, x_new
        k += 1


def cheb_restarted(model, eps, meter, budget_frac=0.25, K0=None,
                   max_iter_factor=6, record=False):
    """Variant (d): restart every K0 = ceil(2/sqrt(alpha)) steps; at each
    restart compute the EXACT residual on supp (charged) -> true certificate
    ||D^{-1/2}(Qx-b)||_inf < alpha*eps stops.  Within a cycle, 'cert'-mode
    truncation with per-step 2-norm allowance tied to the measured residual;
    an adaptive guard damps truncation if a cycle fails to contract."""
    alpha = model.alpha
    theta, delta, sigma, lam = consts(alpha)
    if K0 is None:
        K0 = int(math.ceil(2.0 / math.sqrt(alpha)))
    Ab = A_bar(alpha)
    target = alpha * eps
    n = model.n
    sqd = model.sqd
    seed = int(np.argmax(np.abs(model.b)))
    x = np.zeros(n)
    prevR2 = None
    aggr = 1.0
    total_iters = 0
    Kc = K_cert(alpha, eps, alpha)  # a-priori scale for the cap
    max_cycles = int(math.ceil(max_iter_factor * Kc / K0)) + 8
    vol_hist = [] if record else None
    cert = None
    for c in range(max_cycles):
        suppm = (x != 0.0)
        suppm[seed] = True
        meter.scan_mask(suppm)          # certification scan (charged)
        resid = model.b - model.Q @ x
        meter.rec(int(suppm.sum()))
        cert = float(np.max(np.abs(resid) / sqd))
        R2 = float(np.linalg.norm(resid))
        if cert < target:
            return dict(x=x, status="cert", cycles=c, iters=total_iters,
                        cert=cert, K0=K0, vol_hist=vol_hist)
        if prevR2 is not None and R2 > 0.6 * prevR2:
            aggr *= 0.25
        prevR2 = R2
        allow = budget_frac * max(target, aggr * 0.2 * R2) / (Ab * K0)
        out = cheb_sweep(model, eps, mode="cert", K_max=K0, x_init=x,
                         meter=meter, stop="K", allow_step=allow,
                         record=record)
        if record:
            vol_hist.extend(out["vol_hist"])
        x = out["x"]
        total_iters += out["k"]
    return dict(x=x, status="maxcycles", cycles=max_cycles, iters=total_iters,
                cert=cert, K0=K0, vol_hist=vol_hist)


def push_solve(model, eps_appr, meter, max_sweeps=400_000):
    """Vectorized lazy Jacobi push (batched ACL). Guarantee: final
    ||D^{-1}(pi - p)||_inf <= eps_appr (= our semantic err, mass scale);
    degree-charged work <= 1/(alpha*eps_appr)."""
    alpha = model.alpha
    n = model.n
    a = (1.0 - alpha) / 2.0
    A = model.A
    dv = model.d
    seed = int(np.argmax(model.s))
    p = np.zeros(n)
    r = np.zeros(n)
    r[seed] = 1.0
    thr = eps_appr * dv
    sweeps = 0
    while sweeps < max_sweeps:
        act = r >= thr
        na = int(np.count_nonzero(act))
        if na == 0:
            break
        meter.scan_mask(act)
        xi = np.where(act, r, 0.0)
        p += alpha * xi
        r = r - xi + a * xi + a * (A @ (xi / dv))
        meter.rec(na)
        sweeps += 1
    return dict(x=p / model.sqd, sweeps=sweeps,
                status="done" if sweeps < max_sweeps else "maxed")


def measure_amp(model, K, m_list, sites):
    """Injection amplification of the exact (linear) truncated-recurrence
    propagator: perturb y_{k0} by e_i (k0 = K-m), run the homogeneous
    recurrence to K.  Returns rows with 2-norm and semantic-norm gains and
    the theory envelope (t_k0/t_K)(m+1)."""
    alpha = model.alpha
    theta, delta, sigma, lam = consts(alpha)
    Q = model.Q
    sqd = model.sqd
    # t_k and u_k schedules
    t = [1.0, sigma]
    for k in range(1, K + 1):
        t.append(2.0 * sigma * t[-1] - t[-2])
    rows = []
    for i in sites:
        e = np.zeros(model.n)
        e[i] = 1.0
        for mrem in m_list:
            k0 = K - mrem
            if k0 < 1:
                continue
            u_prev = np.zeros(model.n)
            u = e.copy()
            peak2 = 1.0
            # coefficient index: step producing y_{j+1} uses rho'_j,
            # u_j = t_j/t_{j+1}
            for j in range(k0, K):
                rho = 2.0 * sigma * t[j] / t[j + 1]
                u_new = rho * (u - (Q @ u) / theta) + (1.0 - rho) * u_prev
                u_prev, u = u, u_new
                peak2 = max(peak2, float(np.linalg.norm(u)))
            A2 = float(np.linalg.norm(u))
            Asem = float(np.max(np.abs(u) / sqd)) * sqd[i]
            env = (t[k0] / t[K]) * (mrem + 1)
            rows.append(dict(site=int(i), d_site=int(model.d[i]), m=mrem,
                             k0=k0, A2=A2, Asem=Asem, A2peak=peak2, env=env))
    return rows


def bfs_dist(adj, s):
    from collections import deque
    n = len(adj)
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if dist[w] < 0:
                dist[w] = dist[u] + 1
                q.append(w)
    return dist


def fit_pq(rows, wkey="W_scan"):
    """log W = c + p log(1/alpha) + q log(1/eps) least squares."""
    X = []
    y = []
    for r in rows:
        X.append([1.0, math.log(1.0 / r["alpha"]), math.log(1.0 / r["eps"])])
        y.append(math.log(max(r[wkey], 1.0)))
    X = np.array(X)
    y = np.array(y)
    coef, res, _, _ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    rms = float(np.sqrt(np.mean((pred - y) ** 2)))
    return dict(c=float(coef[0]), p=float(coef[1]), q=float(coef[2]), rms=rms)
