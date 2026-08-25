"""Float mirror of engine.py with error-coordinate mode + rescaling.

Startup runs in x-coordinates (obstacle solves, supports grow monotonically).
Once supp(x_t) == S* and solves interior, switches to error coordinates on the
face S*: the recurrence and every diagnostic are homogeneous (deg 1 / deg 2)
in (e_{t-1}, e_t), so we rescale when errors get tiny and track log-scale.
gamma_t, correction word, and per-window log-contractions are scale-free.
"""
import numpy as np
import math

class FInst:
    def __init__(self, adj, seed, q, rho, alpha=None):
        self.adj = adj
        self.n = n = len(adj)
        self.d = np.array([len(adj[i]) for i in range(n)], float)
        self.q = q = float(q)
        self.alpha = float(alpha) if alpha is not None else q * q / (1 + q * q)
        al = self.alpha
        self.rho = rho = float(rho)
        self.kappa = 1 - 2 * al
        self.beta = (1 - q) / (1 + q)
        self.mu = self.kappa * al / (al + self.kappa)
        A = np.zeros((n, n))
        for i in range(n):
            for j in adj[i]:
                A[i, j] = 1.0
        self.Qt = np.diag((1 + al) / 2 * self.d) - (1 - al) / 2 * A
        self.s = np.array(seed, float)
        self.ct = al * self.s - al * rho * self.d
        self.xstar = self.obstacle_solve(self.ct, 0.0, np.zeros(n))
        self.Sstar = np.where(self.xstar > 1e-300)[0]

    def obstacle_solve(self, ct, kap, ellh, warm=None):
        n = self.n
        rhs = ct + kap * self.d * ellh
        P = set(np.where(rhs > 0)[0]) if warm is None else set(warm)
        if not P:
            P = set(np.where(rhs > 0)[0])
        H = self.Qt + kap * np.diag(self.d)
        for _ in range(4 * n + 8):
            idx = np.array(sorted(P), int)
            xs = np.linalg.solve(H[np.ix_(idx, idx)], rhs[idx])
            neg = idx[xs < 0]
            if len(neg):
                P -= set(neg.tolist()); continue
            x = np.zeros(n); x[idx] = xs
            g = H @ x - rhs
            viol = [i for i in range(n) if i not in P and g[i] < -1e-14]
            if not viol:
                return x
            P |= set(viol)
        raise RuntimeError("active set stalled")

    def run(self, T, bankA=None, keep_arrays=False):
        """Returns dict of per-stage lists: cls, gamma, logPhi, logEQ, loge2,
        Delta_rel (Delta scaled), J cumulative."""
        n = self.n
        q, al, be, kap, mu = self.q, self.alpha, self.beta, self.kappa, self.mu
        S = self.Sstar
        QtS = self.Qt[np.ix_(S, S)]
        dS = self.d[S]
        HS = QtS + kap * np.diag(dS)
        xsS = self.xstar[S]
        cls, gams, logPhi, logEQ, loge2, Js, Psis = [], [], [], [], [], [], []
        xm = np.zeros(n); x = np.zeros(n)
        mode = 'x'
        em = e = None       # errors on face (hat), scaled
        lsc = 0.0           # log scale: true = scaled * exp(lsc)
        J = 0.0
        EQ_prev_log = None
        for t in range(T):
            if mode == 'x':
                dh = x - xm
                ah = x + be * dh
                suppa = ah > 1e-300
                Delta = 0.0
                if suppa.any():
                    zt = self.ct - self.Qt @ ah
                    m = np.where(suppa, -zt / (al * self.d), -np.inf)
                    Delta = max(0.0, m.max())
                rh = np.minimum(be * dh, Delta)
                c = 'N' if Delta <= 0 else (
                    'F' if Delta >= (be * dh).max() - 1e-300 else 'P')
                ellh = ah - rh
                eloc = self.xstar - x
                dloc = dh
                # diagnostics in x mode
                zmx = -eloc + (1 / q - 1) * dloc
                cq = (1 + q) / q
                Dfin = -2 * cq * np.sum(self.d * rh * zmx) + \
                    cq**2 * np.sum(self.d * rh * rh)
                p = self.obstacle_solve(self.ct, kap, x, warm=S.tolist())
                ep = self.xstar - p
                pmx = p - x
                gapE = 0.5 * ep @ self.Qt @ ep + \
                    kap / 2 * np.sum(self.d * pmx * pmx)
                Phi = gapE + mu / 2 * np.sum(self.d * zmx * zmx)
                EQ = eloc @ self.Qt @ eloc
                e2 = np.sum(self.d * eloc * eloc)
                gam = 1 + mu * Dfin / (2 * Phi) if Phi > 0 else 1.0
                lp = math.log(Phi) if Phi > 0 else -np.inf
                lq_ = math.log(EQ) if EQ > 0 else -np.inf
                le = math.log(e2) if e2 > 0 else -np.inf
                xn = self.obstacle_solve(self.ct, kap, ellh)
                xm, x = x, xn
                # switch?
                if (set(np.where(x > 0)[0]) == set(S.tolist())
                        and set(np.where(xm > 0)[0]) == set(S.tolist())):
                    mode = 'e'
                    em = (self.xstar - xm)[S].copy()
                    e = (self.xstar - x)[S].copy()
                    lsc = 0.0
            else:
                dh = em - e                      # d_t (hat, face)
                ta = (1 + be) * e - be * em      # trial error
                zt = QtS @ ta                    # = ct - Qt a on face
                Delta = max(0.0, (-zt / (al * dS)).max())
                bd = be * dh
                rh = np.minimum(bd, Delta)
                c = 'N' if Delta <= 0 else (
                    'F' if Delta >= bd.max() - 1e-300 else 'P')
                zmx = -e + (1 / q - 1) * dh
                cq = (1 + q) / q
                Dfin = (-2 * cq * np.sum(dS * rh * zmx) +
                        cq**2 * np.sum(dS * rh * rh))
                ep = np.linalg.solve(HS, kap * dS * e)
                emep = e - ep
                gapE = 0.5 * ep @ QtS @ ep + \
                    kap / 2 * np.sum(dS * emep * emep)
                Phi = gapE + mu / 2 * np.sum(dS * zmx * zmx)
                EQ = e @ QtS @ e
                e2 = np.sum(dS * e * e)
                gam = 1 + mu * Dfin / (2 * Phi) if Phi > 0 else 1.0
                lp = math.log(Phi) + 2 * lsc if Phi > 0 else -np.inf
                lq_ = math.log(EQ) + 2 * lsc if EQ > 0 else -np.inf
                le = math.log(e2) + 2 * lsc if e2 > 0 else -np.inf
                en = np.linalg.solve(HS, kap * dS * (ta + rh))
                em, e = e, en
                sc = np.abs(e).max()
                if sc < 1e-120 and sc > 0:
                    em /= sc; e /= sc; lsc += math.log(sc)
            if gam > 1:
                J += math.log(gam)
            cls.append(c); gams.append(gam); logPhi.append(lp)
            logEQ.append(lq_); loge2.append(le); Js.append(J)
            if bankA is not None:
                if EQ_prev_log is not None and lp > -np.inf:
                    # Psi = Phi + (A/q) EQ_{t-1}: log-sum-exp
                    a1, a2 = lp, math.log(bankA / q) + EQ_prev_log
                    m_ = max(a1, a2)
                    Psis.append(m_ + math.log(math.exp(a1 - m_) +
                                              math.exp(a2 - m_)))
                else:
                    Psis.append(None)
            EQ_prev_log = lq_
        res = dict(cls=''.join(cls), gamma=gams, logPhi=logPhi, logEQ=logEQ,
                   loge2=loge2, J=Js)
        if bankA is not None:
            res['logPsi'] = Psis
        return res


def window_table(res, q, w=None):
    """Per-window inflation vs contraction. Windows [j*w,(j+1)*w)."""
    if w is None:
        w = math.ceil(1 / q)
    T = len(res['J'])
    rows = []
    nw = T // w
    for j in range(nw):
        a, b = j * w, (j + 1) * w
        infl = res['J'][b - 1] - (res['J'][a - 1] if a else 0.0)
        dPhi = res['logPhi'][a] - res['logPhi'][b - 1] if \
            (res['logPhi'][a] > -np.inf and res['logPhi'][b - 1] > -np.inf) \
            else float('nan')
        de2 = res['loge2'][a] - res['loge2'][b - 1]
        ncorr = sum(1 for cch in res['cls'][a:b] if cch != 'N')
        rows.append(dict(j=j, t0=a, infl=infl, qw=q * w, dlogPhi=dPhi,
                         dloge2=de2, ncorr=ncorr,
                         ratio=infl / (q * w)))
    return rows


def tail_slope(res, q, frac=0.5):
    """LS fit J_T ~ slope * qT + B over the last frac of the horizon."""
    J = np.array(res['J']); T = len(J)
    t0 = int(T * (1 - frac))
    xs = q * np.arange(T)[t0:]
    ys = J[t0:]
    A = np.vstack([xs, np.ones_like(xs)]).T
    sol, *_ = np.linalg.lstsq(A, ys, rcond=None)
    return sol[0], sol[1]
