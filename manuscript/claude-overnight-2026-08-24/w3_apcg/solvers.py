"""W3: randomized accelerated proximal coordinate descent (APCG, Lin-Lu-Xiao
2014, strongly-convex constant-parameter variant) for RPPR, restricted to a
fixed support set S, plus baselines (uniform / Gauss-Southwell prox-CD, ISTA).

Work model: every sampled/selected coordinate i charges d_i via meter.scan
(INCLUDING zero prox updates).  Periodic stopping checks charge meter.rec.

APCG efficient form (all L_i = c = (1+alpha)/2 equal, uniform sampling):
  sigma = strong convexity wrt ||.||_L = alpha / c = 2*alpha/(1+alpha)
  a = sqrt(sigma)/n (constant),  r = (1-a)/(1+a)
  y_k  = (x_k + a z_k)/(1+a)
  zhat = (a x_k + z_k)/(1+a);  z_{k+1} = zhat + Delta e_i,
     Delta from prox: z_{k+1,i} = soft(zhat_i - grad_i f(y_k)/(n a c),
                                       lam_i/(n a c))
  x_{k+1} = y_k + n a Delta e_i        (algebraic simplification of the
            paper's step 4; verified against the unsimplified form)
Two-accumulator ("lazy") representation:  p = (x+z)/2,  m = (x-z)/2 = phi*Mh:
  y_i = p_i + r*phi*Mh_i ;  zhat_i = p_i - r*phi*Mh_i
  p_i    += (n a + 1)/2 * Delta
  Mh_i   += (n a - 1)/2 * Delta / (r*phi) ;  phi <- r*phi
so one iteration touches only i and its neighbors: O(d_i) true cost.
"""
import math
import os
import sys

import numpy as np
import scipy.sparse.linalg as spla

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "lib"))
from model import Model            # noqa: E402
from meter import Meter            # noqa: E402


# ---------------------------------------------------------------- ground truth

def exact_support_solver(model, rho, max_rounds=100000):
    """Active-set exact RPPR solver: monotone growth from the violating seeds,
    exact restricted linear solves, removal guard.  Returns (xstar, S_list)."""
    n = model.n
    lam = model.alpha * rho * model.sqd
    b = model.b
    Q = model.Q.tocsr()
    S = {int(i) for i in np.nonzero(model.s)[0] if b[i] > lam[i]}
    if not S:
        return np.zeros(n), []
    for _ in range(max_rounds):
        Sl = sorted(S)
        QSS = Q[Sl][:, Sl].tocsc()
        rhs = b[Sl] - lam[Sl]
        xS = spla.spsolve(QSS, rhs)
        if np.min(xS) <= 0:
            S = {g for g, v in zip(Sl, xS) if v > 0}
            if not S:
                return np.zeros(n), []
            continue
        x = np.zeros(n)
        x[Sl] = xS
        grad = Q @ x - b
        out = np.ones(n, bool)
        out[Sl] = False
        violm = out & (grad < -lam - 1e-12 * model.alpha * rho)
        if not violm.any():
            resid_in = np.max(np.abs(grad[Sl] + lam[Sl]) / model.sqd[Sl])
            assert resid_in < 1e-6 * model.alpha * rho + 1e-15, resid_in
            return x, Sl
        S |= {int(j) for j in np.nonzero(violm)[0]}
    raise RuntimeError("active set did not settle")


# ---------------------------------------------------------- restricted problem

class Restricted:
    """RPPR problem restricted to support S (global node ids).  Hot-loop
    friendly python lists + numpy views for vectorized checks."""

    def __init__(self, model, rho, S, xstar=None, Fstar=None, boundary=False):
        self.model = model
        self.rho = float(rho)
        self.S = [int(g) for g in S]
        self.n = n = len(self.S)
        gl = {g: k for k, g in enumerate(self.S)}
        self.gl = gl
        al = model.alpha
        self.c = (1.0 + al) / 2.0
        off = -(1.0 - al) / 2.0
        self.nbr, self.deg, self.b, self.lam, self.sqd = [], [], [], [], []
        for g in self.S:
            di = model.d[g]
            self.deg.append(int(di))
            self.b.append(float(model.b[g]))
            self.lam.append(al * self.rho * math.sqrt(di))
            self.sqd.append(math.sqrt(di))
            row = []
            for h in model.adj[g]:
                if h in gl:
                    row.append((gl[h], off / math.sqrt(di * model.d[h])))
            self.nbr.append(row)
        self.vol = int(sum(self.deg))
        self.sigma = 2.0 * al / (1.0 + al)      # strong convexity wrt ||.||_L
        self.arho = al * self.rho
        self.QSS = model.Q.tocsr()[self.S][:, self.S]
        self.bv = model.b[self.S]
        self.lamv = np.array(self.lam)
        self.sqdv = np.array(self.sqd)
        self.xstar = xstar
        self.Fstar = Fstar
        self.h0 = max(0.0, float(np.max(self.bv / self.sqdv)) - self.arho)
        if boundary:
            Bset = {}
            for g in self.S:
                for h in model.adj[g]:
                    if h not in gl:
                        Bset.setdefault(h, []).append(
                            (gl[g], off / math.sqrt(model.d[g] * model.d[h])))
            self.Bnodes = sorted(Bset)
            self.Brows = [Bset[j] for j in self.Bnodes]
            self.Bb = [float(model.b[j]) for j in self.Bnodes]
            self.Blam = [al * self.rho * math.sqrt(model.d[j])
                         for j in self.Bnodes]
            self.Bsqd = [math.sqrt(model.d[j]) for j in self.Bnodes]
            self.Bdeg = [int(model.d[j]) for j in self.Bnodes]

    def eval(self, x):
        """Return (h, sym, F).  h = one-sided KKT excess; sym = full KKT
        residual (both in the D^{-1/2}-scaled metric)."""
        grad = self.QSS @ x - self.bv
        h = max(0.0, float(np.max(-grad / self.sqdv)) - self.arho)
        r1 = np.abs(grad + np.sign(x) * self.lamv)
        r0 = np.maximum(np.abs(grad) - self.lamv, 0.0)
        sym = float(np.max(np.where(x != 0.0, r1, r0) / self.sqdv))
        F = 0.5 * float(x @ grad) - 0.5 * float(x @ self.bv) \
            + float(self.lamv @ np.abs(x))
        return h, sym, F

    def boundary_violators(self, x, meter):
        """Safe-gate admission test on the boundary of S.  Charges d_j per
        boundary node examined."""
        out = []
        for t, j in enumerate(self.Bnodes):
            g = -self.Bb[t]
            for (i, q) in self.Brows[t]:
                g += q * x[i]
            meter.rec(self.Bdeg[t])
            if -g / self.Bsqd[t] - self.arho > 0.0:
                out.append(j)
        return out

    def err_vs_star(self, x):
        if self.xstar is None:
            return None
        return float(np.max(np.abs(x - self.xstar) / self.sqdv))


# ------------------------------------------------------------------- solvers

def _soft(u, t):
    if u > t:
        return u - t
    if u < -t:
        return u + t
    return 0.0


def apcg_run(R, meter, rng, delta=0.1, sigma=None, max_iter=None,
             check_every=None, x0=None, boundary=False, want_sym=True,
             flush_at=1e-120, traj_cap=4000, state=None):
    """Lazy APCG on the restricted problem.  Stops when the one-sided KKT
    excess h <= delta*alpha*rho (records W, iters at that crossing) and, if
    want_sym, continues until the full KKT residual also crosses."""
    n = R.n
    if sigma is None:
        sigma = R.sigma
    a = math.sqrt(sigma) / n
    na = n * a
    r = (1.0 - a) / (1.0 + a)
    cp = 0.5 * (na + 1.0)
    cm = 0.5 * (na - 1.0)
    tstep = 1.0 / (na * R.c)
    if max_iter is None:
        max_iter = int(60.0 * n / math.sqrt(sigma)) + 40 * n
    if check_every is None:
        check_every = n
    if state is not None:
        p, Mh, phi = state
        assert len(p) == n and len(Mh) == n
    else:
        p = [0.0] * n if x0 is None else [float(v) for v in x0]
        Mh = [0.0] * n
        phi = 1.0
    b, lam, nbr, c, Sg = R.b, R.lam, R.nbr, R.c, R.S
    target = delta * R.arho
    it_h = W_h = it_sym = W_sym = None
    traj = []
    k = 0
    status = "cap"
    while k < max_iter:
        i = rng.randrange(n)
        rphi = r * phi
        pi_ = p[i]
        mi = Mh[i]
        yi = pi_ + rphi * mi
        g = c * yi - b[i]
        for (j, q) in nbr[i]:
            g += q * (p[j] + rphi * Mh[j])
        zh = pi_ - rphi * mi
        u = zh - tstep * g
        thr = tstep * lam[i]
        if u > thr:
            zn = u - thr
        elif u < -thr:
            zn = u + thr
        else:
            zn = 0.0
        dlt = zn - zh
        phi = rphi
        if dlt != 0.0:
            p[i] = pi_ + cp * dlt
            Mh[i] = mi + cm * dlt / phi
        meter.scan(Sg[i])
        k += 1
        if phi < flush_at:
            for t in range(n):
                Mh[t] *= phi
            phi = 1.0
            meter.rec(n)
        if k % check_every == 0:
            x = np.asarray(p) + phi * np.asarray(Mh)
            meter.rec(R.vol + n)
            h, sym, F = R.eval(x)
            if len(traj) < traj_cap:
                traj.append((k, meter.total(), h, sym,
                             None if R.Fstar is None else F - R.Fstar))
            if boundary:
                adm = R.boundary_violators(x, meter)
                if adm:
                    return dict(status="admit", x=x, admit=adm, iters=k,
                                it_h=it_h, W_h=W_h, traj=traj,
                                state=(p, Mh, phi))
            if it_h is None and h <= target:
                it_h, W_h = k, meter.total()
            if want_sym and it_sym is None and sym <= target:
                it_sym, W_sym = k, meter.total()
            if it_h is not None and ((not want_sym) or it_sym is not None):
                status = "ok"
                break
    x = np.asarray(p) + phi * np.asarray(Mh)
    meter.rec(n)
    return dict(status=status, x=x, iters=k, it_h=it_h, W_h=W_h,
                it_sym=it_sym, W_sym=W_sym, traj=traj)


def apcg_reference(R, rng, iters, sigma=None):
    """Textbook full-vector APCG with the UNSIMPLIFIED paper step 4
    (x_{k+1} = y + n*a*(z+ - z) + (sigma/n)*(z - y)).  For verification of
    the lazy implementation (same rng => identical sampling sequence)."""
    n = R.n
    if sigma is None:
        sigma = R.sigma
    a = math.sqrt(sigma) / n
    na = n * a
    Qd = R.QSS.toarray()
    x = np.zeros(n)
    z = np.zeros(n)
    for _ in range(iters):
        i = rng.randrange(n)
        y = (x + a * z) / (1.0 + a)
        gi = float(Qd[i] @ y) - R.bv[i]
        zh = (1.0 - a) * z + a * y
        u = zh[i] - gi / (na * R.c)
        thr = R.lam[i] / (na * R.c)
        zi = _soft(u, thr)
        zp = zh.copy()
        zp[i] = zi
        xp = y + na * (zp - z) + (sigma / n) * (z - y)
        x, z = xp, zp
    return x


def cd_run(R, meter, rng=None, rule="uniform", delta=0.1, max_iter=None,
           check_every=None, want_sym=True, traj_cap=4000):
    """Baseline prox coordinate descent (exact coordinate minimization, since
    the coordinate Lipschitz constant is exact).  rule in {uniform, gs}.
    Maintains the full gradient (d_i update cost, matching the d_i charge).
    GS picks argmax of the one-sided KKT excess score."""
    n = R.n
    gs = (rule == "gs")
    x = [0.0] * n
    g = [-v for v in R.b]
    b, lam, nbr, c, Sg, sqd = R.b, R.lam, R.nbr, R.c, R.S, R.sqd
    arho = R.arho
    target = delta * arho
    score = np.array([-gi / s - arho for gi, s in zip(g, sqd)])
    if max_iter is None:
        lg = max(1.0, math.log(max(R.h0 / target, 2.0)))
        max_iter = int(8.0 * n / R.sigma * lg) + 200 * n
    if check_every is None:
        check_every = n
    it_h = W_h = it_sym = W_sym = None
    traj = []
    k = 0
    status = "cap"
    while k < max_iter:
        if gs:
            i = int(np.argmax(score))
            if it_h is None and score[i] <= target:
                it_h, W_h = k, meter.total()
        else:
            i = rng.randrange(n)
        gi = g[i]
        u = x[i] - gi / c
        thr = lam[i] / c
        xn = _soft(u, thr)
        dx = xn - x[i]
        meter.scan(Sg[i])
        k += 1
        if dx != 0.0:
            x[i] = xn
            gi += c * dx
            g[i] = gi
            if gs:
                score[i] = -gi / sqd[i] - arho
            for (j, q) in nbr[i]:
                gj = g[j] + q * dx
                g[j] = gj
                if gs:
                    score[j] = -gj / sqd[j] - arho
        if k % check_every == 0:
            xa = np.asarray(x)
            ga = np.asarray(g)
            meter.rec(2 * n)
            h = max(0.0, float(np.max(-ga / R.sqdv)) - arho)
            r1 = np.abs(ga + np.sign(xa) * R.lamv)
            r0 = np.maximum(np.abs(ga) - R.lamv, 0.0)
            sym = float(np.max(np.where(xa != 0.0, r1, r0) / R.sqdv))
            if len(traj) < traj_cap:
                F = 0.5 * float(xa @ ga) - 0.5 * float(xa @ R.bv) \
                    + float(R.lamv @ np.abs(xa))
                traj.append((k, meter.total(), h, sym,
                             None if R.Fstar is None else F - R.Fstar))
            if it_h is None and h <= target:
                it_h, W_h = k, meter.total()
            if want_sym and it_sym is None and sym <= target:
                it_sym, W_sym = k, meter.total()
            if it_h is not None and ((not want_sym) or it_sym is not None):
                status = "ok"
                break
    return dict(status=status, x=np.asarray(x), iters=k, it_h=it_h, W_h=W_h,
                it_sym=it_sym, W_sym=W_sym, traj=traj)


def ista_run(R, meter, delta=0.1, max_iter=None, traj_cap=4000):
    """Full ISTA restricted to S, charged vol(S) per iteration."""
    n = R.n
    target = delta * R.arho
    if max_iter is None:
        lg = max(1.0, math.log(max(R.h0 / target, 2.0)))
        max_iter = int(8.0 / R.model.alpha * lg) + 2000
    x = np.zeros(n)
    it_h = W_h = it_sym = W_sym = None
    traj = []
    status = "cap"
    k = 0
    while k < max_iter:
        grad = R.QSS @ x - R.bv
        meter.rec(R.vol)
        h = max(0.0, float(np.max(-grad / R.sqdv)) - R.arho)
        r1 = np.abs(grad + np.sign(x) * R.lamv)
        r0 = np.maximum(np.abs(grad) - R.lamv, 0.0)
        sym = float(np.max(np.where(x != 0.0, r1, r0) / R.sqdv))
        if len(traj) < traj_cap and k % 8 == 0:
            F = 0.5 * float(x @ grad) - 0.5 * float(x @ R.bv) \
                + float(R.lamv @ np.abs(x))
            traj.append((k, meter.total(), h, sym,
                         None if R.Fstar is None else F - R.Fstar))
        if it_h is None and h <= target:
            it_h, W_h = k, meter.total()
        if it_sym is None and sym <= target:
            it_sym, W_sym = k, meter.total()
        if it_h is not None and it_sym is not None:
            status = "ok"
            break
        u = x - grad
        x = np.sign(u) * np.maximum(np.abs(u) - R.lamv, 0.0)
        k += 1
    return dict(status=status, x=x, iters=k, it_h=it_h, W_h=W_h,
                it_sym=it_sym, W_sym=W_sym, traj=traj)


def fit_exponent(alphas, Ws):
    """Fit p in W ~ alpha^{-p}; returns (p, residual max abs dev in log2)."""
    la = np.log2(np.asarray(alphas, float))
    lw = np.log2(np.asarray(Ws, float))
    A = np.vstack([-la, np.ones_like(la)]).T
    coef, *_ = np.linalg.lstsq(A, lw, rcond=None)
    resid = lw - A @ coef
    return float(coef[0]), float(np.max(np.abs(resid)))
