"""I2-F: local PPR solvers on 2D (and 3D) grids.

Conventions (lib/model.py):
    Q = (1+a)/2 I - (1-a)/2 D^{-1/2} A D^{-1/2},   b = a D^{-1/2} e_v
    pi = D^{1/2} x,   semantic err = ||D^{-1/2}(x - x*)||_inf
    certificate ||D^{-1/2}(Q x - b)||_inf < a*eps  =>  err < eps.

KEY STRUCTURAL FACT used by the multigrid candidate.  On the interior of a
d-regular lattice (deg = 2D), D^{-1/2} A D^{-1/2} = A/(2D) = I - L/(2D)
(L = graph Laplacian), hence

    Q = a I + (1-a)/(4D) * L        (D = 2 in 2D -> Q = a I + (1-a)/8 L)

i.e. exactly a POSITIVELY SHIFTED discrete Laplacian: alpha is a mass term,
which only *helps* multigrid.  A region Omega strictly inside the grid, with
zero Dirichlet data outside, has Q[Omega,Omega] = a I + beta * L^Dir_Omega,
the textbook 5-point (7-point in 3D) shifted-Poisson operator.  So "global Q
restricted to the explored region" IS a geometric-multigrid problem.

Charging (Meter convention of lib/meter.py):
  * level-0 relaxation / residual: every touched lattice vertex charges d_u
    (= 2D) -> C_adj on first exposure, R_adj afterwards.  A red-black GS
    sweep therefore charges exactly vol(Omega).
  * coarse-level relaxation / residual: 5 (2D) or 7 (3D) flops per coarse
    point -> C_resp  (the coarse levels are *response* operators, not graph
    adjacency: every one of them is charged).
  * restriction  (full weighting)  -> C_resp  9*n_coarse   (27 in 3D)
  * prolongation (bilinear) + correction -> C_resp 3*n_fine (4 in 3D)
  * coarsest exact solve -> C_resp (dense flops), C_mat (its cells)
  * all materialized level arrays -> C_mat (once per region)
Everything above is inside the reported total W = C_adj+R_adj+C_rec+C_resp+
C_mat, so no level of the hierarchy is free.
"""
import ctypes
import math
import os
import sys
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w5_cheb")

_W8 = "/home/claude/work/overnight/w8_regime"
_LIB = ctypes.CDLL(os.path.join(_W8, "libcpush.so"))
_LIB.cpush.restype = ctypes.c_longlong
_LIB.cpush.argtypes = [
    ctypes.c_int,
    np.ctypeslib.ndpointer(np.int32, flags="C_CONTIGUOUS"),
    np.ctypeslib.ndpointer(np.int32, flags="C_CONTIGUOUS"),
    ctypes.c_double, ctypes.c_double, ctypes.c_int,
    np.ctypeslib.ndpointer(np.float64, flags="C_CONTIGUOUS"),
    np.ctypeslib.ndpointer(np.float64, flags="C_CONTIGUOUS"),
    ctypes.POINTER(ctypes.c_longlong), ctypes.POINTER(ctypes.c_longlong),
    np.ctypeslib.ndpointer(np.uint8, flags="C_CONTIGUOUS"),
    np.ctypeslib.ndpointer(np.uint8, flags="C_CONTIGUOUS"),
    np.ctypeslib.ndpointer(np.int32, flags="C_CONTIGUOUS"),
]


# ---------------------------------------------------------------- meter ----

class VecMeter:
    """Identical accounting to lib.meter.Meter, vectorized (scan(u)=d_u)."""

    def __init__(self, dvec):
        self.dv = np.asarray(dvec, float)
        self.seen = np.zeros(self.dv.shape[0], dtype=bool)
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

    def scan_idx(self, idx):
        m = np.zeros(self.dv.shape[0], bool)
        m[idx] = True
        self.scan_mask(m)

    def rec(self, k=1):
        self.C_rec += k

    def resp(self, k=1):
        self.C_resp += k

    def mat(self, k=1):
        self.C_mat += k

    def total(self):
        return (self.C_adj + self.R_adj + self.C_rec + self.C_resp
                + self.C_mat + self.C_emit)

    def vector(self):
        return dict(C_adj=self.C_adj, R_adj=self.R_adj, C_rec=self.C_rec,
                    C_resp=self.C_resp, C_mat=self.C_mat, total=self.total())


# ------------------------------------------------------------ grid model ----

class LatticeModel:
    """Drop-in for lib.model.Model on a w^D lattice with a CENTER seed.
    Builds Q, b, A directly (fast); exposes the same attribute names."""

    def __init__(self, w, alpha, dim=2):
        self.w = w
        self.dim = dim
        self.n = n = w ** dim
        self.alpha = float(alpha)
        shape = (w,) * dim
        self.shape = shape
        # adjacency via offsets
        rows, cols = [], []
        idx = np.arange(n).reshape(shape)
        for ax in range(dim):
            a_ = np.take(idx, np.arange(0, w - 1), axis=ax).ravel()
            b_ = np.take(idx, np.arange(1, w), axis=ax).ravel()
            rows.append(a_); cols.append(b_)
            rows.append(b_); cols.append(a_)
        rows = np.concatenate(rows); cols = np.concatenate(cols)
        self.A = sp.csr_matrix((np.ones(rows.size), (rows, cols)),
                               shape=(n, n))
        self.d = np.asarray(self.A.sum(axis=1)).ravel()
        self.sqd = np.sqrt(self.d)
        Dm12 = sp.diags(1.0 / self.sqd)
        self.N = (Dm12 @ self.A @ Dm12).tocsr()
        a_ = (1 - self.alpha) / 2.0
        c_ = (1 + self.alpha) / 2.0
        self.Q = (sp.identity(n, format="csr") * c_ - a_ * self.N).tocsr()
        ctr = tuple([w // 2] * dim)
        self.seed = int(idx[ctr])
        self.s = np.zeros(n); self.s[self.seed] = 1.0
        self.b = self.alpha * self.s / self.sqd
        self._x0 = None

    def solve_exact(self):
        if self._x0 is None:
            self._x0 = spla.spsolve(self.Q.tocsc(), self.b)
        return self._x0

    def semantic_err(self, x):
        return float(np.max(np.abs(x - self.solve_exact()) / self.sqd))

    def cert_resid(self, x):
        return float(np.max(np.abs(self.Q @ x - self.b) / self.sqd))


def support_stats(model, eps):
    """Semantic output: S_eps = {v : pi_v/d_v >= eps}; its size, volume,
    and max Chebyshev radius from the seed."""
    x0 = model.solve_exact()
    pid = x0 / model.sqd            # = pi_v / d_v
    S = pid >= eps
    w, dim = model.w, model.dim
    idx = np.flatnonzero(S)
    if idx.size == 0:
        return dict(nS=0, volS=0.0, R=0, touches_bd=False)
    coords = np.unravel_index(idx, model.shape)
    ctr = w // 2
    R = int(max(np.max(np.abs(c - ctr)) for c in coords))
    touches = R >= (w // 2) - 1
    return dict(nS=int(idx.size), volS=float(model.d[idx].sum()), R=R,
                touches_bd=bool(touches))


# --------------------------------------------------------------- push ------

def push_c(model, eps):
    """FIFO lazy ACL push at activation threshold eps (bit-identical C port).
    One-sided guarantee err <= eps.  W = C_adj + R_adj."""
    n = model.n
    A = model.A.tocsr()
    indptr = A.indptr.astype(np.int32)
    indices = A.indices.astype(np.int32)
    p = np.zeros(n); r = np.zeros(n)
    seen = np.zeros(n, np.uint8); inq = np.zeros(n, np.uint8)
    queue = np.zeros(n + 1, np.int32)
    wf = ctypes.c_longlong(0); wr = ctypes.c_longlong(0)
    t0 = time.perf_counter()
    npush = _LIB.cpush(n, indptr, indices, model.alpha, eps, model.seed, p, r,
                       ctypes.byref(wf), ctypes.byref(wr), seen, inq, queue)
    return dict(x=p / model.sqd, W=float(wf.value + wr.value),
                C_adj=float(wf.value), R_adj=float(wr.value),
                n_push=int(npush), wall=time.perf_counter() - t0)


# ------------------------------------------------------- Chebyshev ---------

def cheb_local(model, eps, meter, x_init=None, tau_frac=0.25,
               hard_factor=8, max_wall=120.0):
    """Truncated Chebyshev with the FREE MEASURED certificate (W5 cheb_meas),
    optionally warm-started from x_init (push-then-Chebyshev hybrid)."""
    alpha = model.alpha
    theta = (1 + alpha) / 2.0
    delta = (1 - alpha) / 2.0
    sigma = theta / delta
    Q, b, sqd, n = model.Q, model.b, model.sqd, model.n
    seed = model.seed
    target = alpha * eps
    tau = tau_frac * eps
    win = int(math.ceil(2.0 / math.sqrt(alpha))) + 5
    need = max(1.0, alpha / (0.45 * alpha * eps))
    Kc = int(math.ceil(math.acosh(need) / math.acosh(sigma))) + 2
    hard = hard_factor * Kc + 10
    t0 = time.perf_counter()

    x_prev = np.zeros(n) if x_init is None else np.asarray(x_init, float).copy()
    supp = x_prev != 0.0; supp[seed] = True
    meter.scan_mask(supp)
    r = b - Q @ x_prev
    meter.rec(int(supp.sum()))
    cert0 = float(np.max(np.abs(r) / sqd))
    if cert0 < target:
        return dict(x=x_prev, status="cert", iters=0, cert=cert0)
    x = x_prev + r / theta
    meter.rec(1)
    ucoef = 1.0 / sigma
    best = math.inf; last = 1; k = 1
    while True:
        mask = (x != 0.0) & (np.abs(x) < tau * sqd)
        mask[seed] = False
        if mask.any():
            x[mask] = 0.0
        supp = x != 0.0; supp[seed] = True
        meter.scan_mask(supp)
        r = b - Q @ x
        meter.rec(int(supp.sum()))
        cert = float(np.max(np.abs(r) / sqd))
        if cert < target:
            return dict(x=x, status="cert", iters=k, cert=cert)
        if cert < 0.75 * best:
            best = cert; last = k
        elif k - last >= win:
            tau *= 0.25; last = k
        if k >= hard or time.perf_counter() - t0 > max_wall:
            return dict(x=x, status="maxed", iters=k, cert=cert)
        ucoef = 1.0 / (2.0 * sigma - ucoef)
        rho = 2.0 * sigma * ucoef
        xn = rho * (x + r / theta) + (1.0 - rho) * x_prev
        meter.rec(int(np.count_nonzero(xn)))
        x_prev, x = x, xn
        k += 1


# ------------------------------------------------- local geometric MG ------

def ladder(mmax, dim=2):
    """Region side lengths {q*2^k-1}; every one coarsens by m -> (m-1)/2 down
    to a tiny dense level.  q is restricted so the COARSEST level stays tiny
    (<= 16 unknowns in 2D, <= 27 in 3D) -- otherwise its one-off dense factor
    (charged honestly at (2/3)npt^3) dominates the whole V-cycle budget."""
    vals = set()
    for q in ((1, 3, 5) if dim == 2 else (1, 3)):
        k = 1
        while q * 2 ** k - 1 <= mmax:
            v = q * 2 ** k - 1
            if v >= 5 and v % 2 == 1:     # region side must be odd (centred)
                vals.add(v)
            k += 1
    return sorted(vals)


class Region:
    """Square (cube) sub-lattice of side m0 unknowns centred at the seed, with
    the Dirichlet ring just outside.  Levels coarsen m -> (m-1)/2 while m is
    odd and > 3; the last level is solved densely (LU cached per region).
    Arrays are stored PADDED (m_l+2)^D so all stencils are pure slicing and
    the pad IS the Dirichlet zero."""

    def __init__(self, m0, alpha, dim=2):
        self.dim = dim
        self.alpha = float(alpha)
        self.beta = (1 - self.alpha) / (4.0 * dim)     # Q = a I + beta*L
        ms = [int(m0)]
        while ms[-1] > 3 and ms[-1] % 2 == 1:
            ms.append((ms[-1] - 1) // 2)
        self.ms = ms
        self.nlev = len(ms)
        # level-l operator: a I + beta/4^l * L_l  (rediscretisation, H=2^l)
        self.cf = [self.beta / (4.0 ** l) for l in range(self.nlev)]
        self.diag = [self.alpha + 2 * dim * c for c in self.cf]
        self._lu = None
        self._lu_flops = 0.0

    def m(self, l):
        return self.ms[l]

    def npts(self, l):
        return self.ms[l] ** self.dim

    def coarse_lu(self):
        """Dense LU of the coarsest operator, factored once per region."""
        if self._lu is None:
            m = self.ms[-1]
            A = _dense_op(m, self.dim, self.cf[-1], self.diag[-1])
            import scipy.linalg as sla
            self._lu = sla.lu_factor(A)
            npt = m ** self.dim
            self._lu_flops = (2.0 / 3.0) * npt ** 3
        return self._lu


def _nbr_sum(up):
    """Sum of the 2D lattice neighbours for a PADDED array (interior view)."""
    if up.ndim == 2:
        return (up[:-2, 1:-1] + up[2:, 1:-1] + up[1:-1, :-2] + up[1:-1, 2:])
    return (up[:-2, 1:-1, 1:-1] + up[2:, 1:-1, 1:-1]
            + up[1:-1, :-2, 1:-1] + up[1:-1, 2:, 1:-1]
            + up[1:-1, 1:-1, :-2] + up[1:-1, 1:-1, 2:])


def _rb_masks(m, dim):
    if dim == 2:
        i, j = np.indices((m, m))
        par = (i + j) % 2
    else:
        i, j, k = np.indices((m, m, m))
        par = (i + j + k) % 2
    return par == 0, par == 1


def _relax_rb(up, fp, cf, diag, red, black):
    """One red-black Gauss-Seidel sweep in place on the padded array up."""
    for msk in (red, black):
        s = _nbr_sum(up)
        newv = (fp[1:-1, 1:-1] if up.ndim == 2 else fp[1:-1, 1:-1, 1:-1])
        val = (newv + cf * s) / diag
        tgt = up[1:-1, 1:-1] if up.ndim == 2 else up[1:-1, 1:-1, 1:-1]
        tgt[msk] = val[msk]


def _resid(up, fp, cf, diag):
    """r = f - A u on the interior (returns an unpadded array)."""
    inner = up[1:-1, 1:-1] if up.ndim == 2 else up[1:-1, 1:-1, 1:-1]
    finn = fp[1:-1, 1:-1] if up.ndim == 2 else fp[1:-1, 1:-1, 1:-1]
    return finn - (diag * inner - cf * _nbr_sum(up))


def _restrict(rp, mc, dim):
    """Full weighting fine(padded) -> coarse(padded)."""
    out = np.zeros((mc + 2,) * dim)
    if dim == 2:
        c = rp[2::2, 2::2][:mc, :mc]
        e = (rp[1:-1:2, 2::2][:mc, :mc] + rp[3::2, 2::2][:mc, :mc]
             + rp[2::2, 1:-1:2][:mc, :mc] + rp[2::2, 3::2][:mc, :mc])
        d = (rp[1:-1:2, 1:-1:2][:mc, :mc] + rp[3::2, 1:-1:2][:mc, :mc]
             + rp[1:-1:2, 3::2][:mc, :mc] + rp[3::2, 3::2][:mc, :mc])
        out[1:-1, 1:-1] = (4 * c + 2 * e + d) / 16.0
    else:
        acc = np.zeros((mc, mc, mc))
        wts = {0: 8.0, 1: 4.0, 2: 2.0, 3: 1.0}
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for dk in (-1, 0, 1):
                    w = wts[abs(di) + abs(dj) + abs(dk)]
                    acc += w * rp[2 + di::2, 2 + dj::2,
                                  2 + dk::2][:mc, :mc, :mc]
        out[1:-1, 1:-1, 1:-1] = acc / 64.0
    return out


def _prolong(ep, mf, dim):
    """Bilinear/trilinear interpolation coarse(padded) -> fine(padded)."""
    out = np.zeros((mf + 2,) * dim)
    if dim == 2:
        out[0::2, 0::2] = ep
        out[1::2, 0::2] = 0.5 * (ep[:-1, :] + ep[1:, :])
        out[0::2, 1::2] = 0.5 * (ep[:, :-1] + ep[:, 1:])
        out[1::2, 1::2] = 0.25 * (ep[:-1, :-1] + ep[1:, :-1]
                                  + ep[:-1, 1:] + ep[1:, 1:])
    else:
        out[0::2, 0::2, 0::2] = ep
        out[1::2, 0::2, 0::2] = 0.5 * (ep[:-1] + ep[1:])
        out[0::2, 1::2, 0::2] = 0.5 * (ep[:, :-1] + ep[:, 1:])
        out[0::2, 0::2, 1::2] = 0.5 * (ep[:, :, :-1] + ep[:, :, 1:])
        out[1::2, 1::2, 0::2] = 0.25 * (ep[:-1, :-1] + ep[1:, :-1]
                                        + ep[:-1, 1:] + ep[1:, 1:])
        out[1::2, 0::2, 1::2] = 0.25 * (ep[:-1, :, :-1] + ep[1:, :, :-1]
                                        + ep[:-1, :, 1:] + ep[1:, :, 1:])
        out[0::2, 1::2, 1::2] = 0.25 * (ep[:, :-1, :-1] + ep[:, 1:, :-1]
                                        + ep[:, :-1, 1:] + ep[:, 1:, 1:])
        out[1::2, 1::2, 1::2] = 0.125 * (
            ep[:-1, :-1, :-1] + ep[1:, :-1, :-1] + ep[:-1, 1:, :-1]
            + ep[:-1, :-1, 1:] + ep[1:, 1:, :-1] + ep[1:, :-1, 1:]
            + ep[:-1, 1:, 1:] + ep[1:, 1:, 1:])
    return out


def v_cycle(reg, l, up, fp, rbm, charge, nu1=2, nu2=1):
    """Recursive V-cycle at level l (arrays padded).  `charge` is a dict of
    accumulators: 'lev0' counts level-0 vertex touches (charged as graph
    scans by the caller), 'resp' counts every coarse-level flop."""
    dim = reg.dim
    m = reg.m(l)
    cf, dg = reg.cf[l], reg.diag[l]
    stw = 2 * dim + 1
    if l == reg.nlev - 1:
        # exact solve of the coarsest level (dense LU, factored once/region)
        import scipy.linalg as sla
        npt = m ** dim
        lu = reg.coarse_lu()
        finn = (fp[1:-1, 1:-1] if dim == 2 else fp[1:-1, 1:-1, 1:-1])
        sol = sla.lu_solve(lu, finn.ravel())
        inner = (up[1:-1, 1:-1] if dim == 2 else up[1:-1, 1:-1, 1:-1])
        inner[...] = sol.reshape((m,) * dim)
        charge['resp'] += 2.0 * npt ** 2          # triangular solves
        charge['setup'] = reg._lu_flops           # one-off factor flops
        charge['mat'] += npt ** 2
        return
    red, black = rbm[l]
    for _ in range(nu1):
        _relax_rb(up, fp, cf, dg, red, black)
        if l == 0:
            charge['lev0'] += m ** dim
        else:
            charge['resp'] += stw * (m ** dim)
    r = _resid(up, fp, cf, dg)
    if l == 0:
        charge['lev0'] += m ** dim
    else:
        charge['resp'] += stw * (m ** dim)
    rp = np.zeros((m + 2,) * dim)
    if dim == 2:
        rp[1:-1, 1:-1] = r
    else:
        rp[1:-1, 1:-1, 1:-1] = r
    mc = reg.m(l + 1)
    fc = _restrict(rp, mc, dim)
    charge['resp'] += (9 if dim == 2 else 27) * (mc ** dim)
    ec = np.zeros((mc + 2,) * dim)
    v_cycle(reg, l + 1, ec, fc, rbm, charge, nu1, nu2)
    ef = _prolong(ec, m, dim)
    charge['resp'] += (3 if dim == 2 else 4) * (m ** dim)
    up += ef
    for _ in range(nu2):
        _relax_rb(up, fp, cf, dg, red, black)
        if l == 0:
            charge['lev0'] += m ** dim
        else:
            charge['resp'] += stw * (m ** dim)


def _dense_op(m, dim, cf, dg):
    npt = m ** dim
    idx = np.arange(npt).reshape((m,) * dim)
    A = np.eye(npt) * dg
    for ax in range(dim):
        a_ = np.take(idx, np.arange(0, m - 1), axis=ax).ravel()
        b_ = np.take(idx, np.arange(1, m), axis=ax).ravel()
        A[a_, b_] -= cf
        A[b_, a_] -= cf
    return A


def _region_index(model, m):
    """Global index block of the m^D region centred at the seed, plus its
    Dirichlet ring (the immediate outside neighbours)."""
    w, dim = model.w, model.dim
    h = m // 2
    ctr = w // 2
    lo, hi = ctr - h, ctr + h
    if lo < 1 or hi > w - 2:
        return None
    sl = tuple(slice(lo, hi + 1) for _ in range(dim))
    idx = np.arange(model.n).reshape(model.shape)
    core = idx[sl].copy()
    slw = tuple(slice(lo - 1, hi + 2) for _ in range(dim))
    ring = np.setdiff1d(idx[slw].ravel(), core.ravel())
    return dict(m=m, lo=lo, hi=hi, core=core, ring=ring, sl=sl)


def _ring_cert(up, beta, dim):
    """max |r_v|/sqrt(d_v) over the Dirichlet ring dOmega.  For v just
    outside the region, x_v = 0 and (Qx)_v = -beta * sum_{u~v, u in Omega} x_u
    with exactly one such u (face) or none (edge/corner), d_v = 2*dim."""
    inn = up[1:-1, 1:-1] if dim == 2 else up[1:-1, 1:-1, 1:-1]
    faces = []
    for ax in range(dim):
        faces.append(np.take(inn, 0, axis=ax))
        faces.append(np.take(inn, inn.shape[ax] - 1, axis=ax))
    mx = max(float(np.max(np.abs(f))) for f in faces)
    return beta * mx / math.sqrt(2 * dim)


def mg_local(model, eps, meter, m0=None, mmax=None, nu1=2, nu2=1,
             max_cycles=80, stall=0.5, stall_win=2, x_exact=None,
             oracle=False, verbose=False, cert_every=1):
    """LOCAL MULTIGRID: growing square region (ratio ~1.5) + V-cycles,
    self-certified by the MEASURED residual over Omega U dOmega.  All levels,
    all transfers, all coarse solves and all failed region attempts charged."""
    alpha = model.alpha
    dim = model.dim
    target = alpha * eps
    beta = (1 - alpha) / (4.0 * dim)
    if mmax is None:
        mmax = model.w - 3
    cand = [m for m in ladder(mmax, dim) if m0 is None or m >= m0]
    hist = []
    xg = np.zeros(model.n)
    last = None
    for m in cand:
        ri = _region_index(model, m)
        if ri is None:
            break
        reg = Region(m, alpha, dim)
        rbm = [_rb_masks(reg.m(l), dim) for l in range(reg.nlev)]
        meter.mat(sum(reg.npts(l) for l in range(reg.nlev)))   # arrays
        up = np.zeros((m + 2,) * dim)
        fp = np.zeros((m + 2,) * dim)
        fp[tuple([m // 2 + 1] * dim)] = model.b[model.seed]
        core_mask = np.zeros(model.n, bool)
        core_mask[ri["core"].ravel()] = True
        ring_mask = np.zeros(model.n, bool)
        ring_mask[ri["ring"]] = True
        best = math.inf; stall_ct = 0; cyc = 0
        cert = math.inf; semerr = math.inf
        setup_charged = False
        while cyc < max_cycles:
            ch = dict(lev0=0, resp=0.0, mat=0.0, setup=0.0)
            v_cycle(reg, 0, up, fp, rbm, ch, nu1, nu2)
            cyc += 1
            for _ in range(int(round(ch['lev0'] / (m ** dim)))):
                meter.scan_mask(core_mask)        # level-0 sweeps = graph scans
            meter.resp(ch['resp'])
            meter.mat(ch['mat'])
            if not setup_charged and ch.get('setup', 0.0):
                meter.resp(ch['setup']); setup_charged = True
            # ---- measured certificate over Omega U dOmega ----
            meter.scan_mask(core_mask)            # residual pass over Omega
            meter.scan_mask(ring_mask)            # boundary residual
            rin = _resid(up, fp, reg.cf[0], reg.diag[0])
            meter.rec(int(ri["core"].size) + int(ri["ring"].size))
            rc = _ring_cert(up, beta, dim)
            cert = max(float(np.max(np.abs(rin))) / math.sqrt(2 * dim), rc)
            if x_exact is not None:
                xg[:] = 0.0
                inner = (up[1:-1, 1:-1] if dim == 2 else up[1:-1, 1:-1, 1:-1])
                xg[ri["core"].ravel()] = inner.ravel()
                semerr = float(np.max(np.abs(xg - x_exact) / model.sqd))
            ok = (semerr <= eps) if oracle else (cert < target)
            if ok:
                xg[:] = 0.0
                inner = (up[1:-1, 1:-1] if dim == 2 else up[1:-1, 1:-1, 1:-1])
                xg[ri["core"].ravel()] = inner.ravel()
                hist.append(dict(m=m, cycles=cyc, cert=cert, semerr=semerr))
                return dict(x=xg, status="cert", m=m, cycles=cyc, cert=cert,
                            hist=hist, W_final=None,
                            volOmega=float(model.d[core_mask].sum()))
            # EARLY REGION REJECTION: the boundary residual is a floor that no
            # further V-cycling can lower, so once it exceeds the target the
            # region is provably too small -> grow now (1-2 cycles wasted, not
            # a whole stall window).  Not used in oracle mode.
            if (not oracle) and cyc >= 2 and rc >= target:
                break
            if cert < stall * best:
                best = cert; stall_ct = 0
            else:
                stall_ct += 1
                if stall_ct >= stall_win:
                    break
        hist.append(dict(m=m, cycles=cyc, cert=cert, semerr=semerr, grew=True))
        last = (m, core_mask, cyc, cert)
        if verbose:
            print(f"    MG grow m={m} cyc={cyc} cert={cert:.3e} "
                  f"target={target:.3e}")
    m, core_mask, cyc, cert = last if last else (0, np.zeros(model.n, bool),
                                                 0, math.inf)
    return dict(x=xg, status="maxed", m=m, cycles=cyc, cert=cert, hist=hist,
                volOmega=float(model.d[core_mask].sum()))


# ------------------------------------------- nested-dissection elimination --

def _lu_flops(lu):
    """Cholesky-equivalent flop count of a sparse LU: sum_j nnz(L[j:,j])^2."""
    Lm = lu.L.tocsc()
    cnt = np.diff(Lm.indptr).astype(float)
    return float(np.sum(cnt ** 2)), float(Lm.nnz + lu.U.nnz)


def nd_ees(model, eps, meter, m0=None, mmax=None, x_exact=None, oracle=False,
           permc="MMD_AT_PLUS_A"):
    """EXPLORE-ELIMINATE-SUBSTITUTE with a *nested-dissection* (fill-reducing)
    direct solve of Q[Omega,Omega]; same growing region and same measured
    certificate as mg_local.  Charges factor flops + fill + solves."""
    dim = model.dim
    target = model.alpha * eps
    beta = (1 - model.alpha) / (4.0 * dim)
    if mmax is None:
        mmax = model.w - 3
    cand = [m for m in ladder(mmax, dim) if m0 is None or m >= m0]
    xg = np.zeros(model.n)
    hist = []
    last = None
    for m in cand:
        ri = _region_index(model, m)
        if ri is None:
            break
        core = ri["core"].ravel()
        core_mask = np.zeros(model.n, bool); core_mask[core] = True
        ring_mask = np.zeros(model.n, bool); ring_mask[ri["ring"]] = True
        meter.scan_mask(core_mask)                      # explore
        Qs = model.Q[core_mask][:, core_mask].tocsc()
        meter.rec(float(Qs.nnz))                        # assembly
        lu = spla.splu(Qs, permc_spec=permc)
        fl, nz = _lu_flops(lu)
        meter.resp(fl)                                  # factor flops
        meter.mat(nz)                                   # fill cells
        sol = lu.solve(model.b[core_mask])
        meter.resp(2.0 * nz)                            # triangular solves
        xg[:] = 0.0
        xg[core] = sol
        meter.scan_mask(ring_mask)
        up = np.zeros((m + 2,) * dim)
        if dim == 2:
            up[1:-1, 1:-1] = sol.reshape((m, m))
        else:
            up[1:-1, 1:-1, 1:-1] = sol.reshape((m, m, m))
        fp = np.zeros((m + 2,) * dim)
        fp[tuple([m // 2 + 1] * dim)] = model.b[model.seed]
        cf = beta; dg = model.alpha + 2 * dim * beta
        rin = _resid(up, fp, cf, dg)
        meter.rec(int(core.size) + int(ri["ring"].size))
        cert = max(float(np.max(np.abs(rin))) / math.sqrt(2 * dim),
                   _ring_cert(up, beta, dim))
        semerr = (float(np.max(np.abs(xg - x_exact) / model.sqd))
                  if x_exact is not None else math.inf)
        hist.append(dict(m=m, cert=cert, semerr=semerr, flops=fl, nnz=nz))
        last = (m, core_mask, cert)
        ok = (semerr <= eps) if oracle else (cert < target)
        if ok:
            return dict(x=xg.copy(), status="cert", m=m, cert=cert, hist=hist,
                        volOmega=float(model.d[core_mask].sum()))
    m, core_mask, cert = last if last else (0, np.zeros(model.n, bool),
                                            math.inf)
    return dict(x=xg.copy(), status="maxed", m=m, cert=cert, hist=hist,
                volOmega=float(model.d[core_mask].sum()))
