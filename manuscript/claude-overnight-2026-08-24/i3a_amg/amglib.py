"""I3-A: LOCAL ALGEBRAIC MULTIGRID for PPR on arbitrary graphs.

Conventions (lib/model.py, identical to W1-W8 / I2-F):
    Q = (1+a)/2 I - (1-a)/2 D^{-1/2} A D^{-1/2} = a I + (1-a)/2 L_sym
    b = a D^{-1/2} e_v ,  pi = D^{1/2} x
    semantic err = ||D^{-1/2}(x - x*)||_inf = max_i |pi_i - pi*_i|/d_i
    certificate  ||D^{-1/2}(Qx - b)||_inf < a*eps  =>  err < eps

Q is a POSITIVELY SHIFTED normalized graph Laplacian: SPD M-matrix, spectrum
in [alpha, 1].  That is exactly the class smoothed aggregation is designed
for; alpha is a mass term which only helps.  The near-nullspace of L_sym is
D^{1/2}1, so the level-0 near-nullspace candidate is B = sqrt(d) on the
region.

=========================== CHARGING LEDGER ================================
Everything below is inside W = C_adj + R_adj + C_rec + C_resp + C_mat.

LEVEL 0 (the graph itself).  Any operation that reads adjacency of a vertex
set M charges sum_{u in M} d_u (first exposure -> C_adj, repeats -> R_adj):
  * incremental BFS exploration of the region and of its boundary ring
  * assembly of Q[S,S] and of the cross block Q[dS,S]
  * strength-of-connection pass at level 0
  * EACH aggregation round at level 0 (MIS rounds + 2 assignment rounds)
  * EACH smoothing sweep at level 0 (Jacobi sweep touches u and its nbrs)
  * EACH residual evaluation at level 0
  * the certificate pass over S and over dS
LEVELS >= 1 (pure response operators - nothing is free):
  * strength pass:            nnz(A_l)                        -> C_resp
  * aggregation:              (#rounds) * nnz(S_l)            -> C_resp
  * tentative prolongator:    n_l + nnz(T_l)                  -> C_resp
  * spectral radius estimate: (n_power) * nnz(A_l)            -> C_resp
  * prolongator smoothing:    exact spmm multiply-add count for (D^-1 A_l) T
                              + nnz(P_l) axpy                 -> C_resp
  * Galerkin RAP:             exact spmm counts for A_l @ P_l and
                              P_l^T @ (A_l P_l)               -> C_resp
  * every V-cycle smoothing sweep / residual: nnz(A_l)        -> C_resp
  * restriction / prolongation: nnz(P_l) each                 -> C_resp
  * coarsest dense LU:  (2/3) n_c^3 once, 2 n_c^2 per solve   -> C_resp
MATERIALISATION: nnz(A_l) + nnz(P_l) + n_l arrays per level, n_c^2 for the
dense coarse factor                                           -> C_mat
COORDINATE WRITES: certificate maxima, vector updates          -> C_rec
ALL FAILED REGION ATTEMPTS ARE CHARGED IN FULL.
============================================================================
"""
import ctypes
import math
import os
import sys
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import scipy.linalg as sla

sys.path.insert(0, "/home/claude/work/overnight/lib")

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
    """Identical accounting to lib.meter.Meter, vectorized (scan(u) = d_u)."""

    def __init__(self, dvec):
        self.dv = np.asarray(dvec, float)
        self.seen = np.zeros(self.dv.shape[0], dtype=bool)
        self.C_adj = 0.0
        self.R_adj = 0.0
        self.C_rec = 0.0
        self.C_resp = 0.0
        self.C_mat = 0.0
        # split of C_resp into SETUP vs SOLVE (AMG's crux)
        self.setup = 0.0
        self.solve = 0.0
        self.agg = 0.0        # charged aggregation work (vectorized MIS)
        self.agg_seq = 0.0    # what a sequential Vanek 3-pass would cost
        self._phase = "solve"

    def phase(self, p):
        self._phase = p

    def scan_idx(self, idx):
        if len(idx) == 0:
            return
        new = ~self.seen[idx]
        w_new = float(self.dv[idx[new]].sum())
        w_old = float(self.dv[idx[~new]].sum())
        self.C_adj += w_new
        self.R_adj += w_old
        self.seen[idx] = True
        if self._phase == "setup":
            self.setup += w_new + w_old
        else:
            self.solve += w_new + w_old

    def rec(self, k=1):
        self.C_rec += k
        if self._phase == "setup":
            self.setup += k
        else:
            self.solve += k

    def resp(self, k=1):
        self.C_resp += k
        if self._phase == "setup":
            self.setup += k
        else:
            self.solve += k

    def mat(self, k=1):
        self.C_mat += k
        if self._phase == "setup":
            self.setup += k
        else:
            self.solve += k

    def total(self):
        return (self.C_adj + self.R_adj + self.C_rec + self.C_resp
                + self.C_mat)

    def vector(self):
        return dict(C_adj=self.C_adj, R_adj=self.R_adj, C_rec=self.C_rec,
                    C_resp=self.C_resp, C_mat=self.C_mat,
                    setup=self.setup, solve=self.solve, total=self.total(),
                    agg=self.agg, agg_seq=self.agg_seq,
                    total_seq=self.total() - self.agg + self.agg_seq)


# ---------------------------------------------------------------- model ----

class GModel:
    """Fast CSR PPR model for an arbitrary adjacency dict."""

    def __init__(self, adj, alpha, seed):
        self.n = n = len(adj)
        self.alpha = float(alpha)
        self.seed = int(seed)
        indptr = np.zeros(n + 1, np.int64)
        for u in range(n):
            indptr[u + 1] = indptr[u] + len(adj[u])
        indices = np.empty(indptr[-1], np.int64)
        for u in range(n):
            indices[indptr[u]:indptr[u + 1]] = adj[u]
        self.indptr = indptr
        self.indices = indices
        self.d = np.diff(indptr).astype(float)
        self.sqd = np.sqrt(self.d)
        self.A = sp.csr_matrix((np.ones(len(indices)), indices, indptr),
                               shape=(n, n))
        a = (1 - self.alpha) / 2.0
        c = (1 + self.alpha) / 2.0
        Dm12 = sp.diags(1.0 / self.sqd)
        self.Q = (sp.identity(n) * c - a * (Dm12 @ self.A @ Dm12)).tocsr()
        self.b = np.zeros(n)
        self.b[self.seed] = self.alpha / self.sqd[self.seed]
        self._x0 = None

    def solve_exact(self):
        if self._x0 is None:
            if self.n <= 8000:
                self._x0 = spla.spsolve(self.Q.tocsc(), self.b)
            else:
                x, info = spla.cg(self.Q, self.b, rtol=1e-14, atol=0.0,
                                  maxiter=20000)
                self._x0 = x
        return self._x0

    def semantic_err(self, x):
        return float(np.max(np.abs(x - self.solve_exact()) / self.sqd))

    def cert_resid(self, x):
        return float(np.max(np.abs(self.Q @ x - self.b) / self.sqd))


def support_stats(model, eps):
    x0 = model.solve_exact()
    pid = x0 / model.sqd
    idx = np.flatnonzero(pid >= eps)
    if idx.size == 0:
        return dict(nS=0, volS=0.0, R=0)
    # exact BFS radius of the support
    dist = bfs_dist(model, idx)
    return dict(nS=int(idx.size), volS=float(model.d[idx].sum()),
                R=int(dist))


def bfs_dist(model, targets):
    """max BFS distance from seed to any target (uncharged; diagnostics)."""
    n = model.n
    tset = np.zeros(n, bool)
    tset[targets] = True
    seen = np.zeros(n, bool)
    seen[model.seed] = True
    frontier = np.array([model.seed])
    r = 0
    left = int(tset.sum()) - int(tset[model.seed])
    while frontier.size and left > 0:
        nb = np.concatenate([model.indices[model.indptr[u]:model.indptr[u + 1]]
                             for u in frontier])
        nb = np.unique(nb)
        nb = nb[~seen[nb]]
        seen[nb] = True
        r += 1
        left -= int(tset[nb].sum())
        frontier = nb
    return r


# --------------------------------------------------------- exploration -----

class Explorer:
    """Incremental BFS ball around the seed.  Charges d_u for every vertex the
    first time its adjacency is read; boundary vertices are charged too."""

    def __init__(self, model, meter):
        self.m = model
        self.meter = meter
        self.dist = np.full(model.n, -1, np.int32)
        self.dist[model.seed] = 0
        self.order = [np.array([model.seed])]
        self.r = 0
        self.scanned = np.zeros(model.n, bool)
        self.cumvol = [float(model.d[model.seed])]

    def grow_to(self, R):
        """Ensure BFS shells up to distance R are known.  Returns False if the
        graph is exhausted before R."""
        while self.r < R:
            fr = self.order[-1]
            if fr.size == 0:
                return False
            idx = fr[~self.scanned[fr]]
            if idx.size:
                self.meter.scan_idx(idx)
                self.scanned[idx] = True
            nb = _nbrs(self.m, fr)
            nb = nb[self.dist[nb] < 0]
            nb = np.unique(nb)
            self.dist[nb] = self.r + 1
            self.order.append(nb)
            self.cumvol.append(self.cumvol[-1] +
                               float(self.m.d[nb].sum()) if nb.size
                               else self.cumvol[-1])
            self.r += 1
        return True

    def ball(self, R):
        R = min(R, self.r)
        return np.concatenate(self.order[:R + 1])

    def ballvol(self, R):
        return self.cumvol[min(R, self.r)]


def _nbrs(model, idx):
    if idx.size == 0:
        return np.empty(0, np.int64)
    ip, ii = model.indptr, model.indices
    lens = (ip[idx + 1] - ip[idx]).astype(np.int64)
    tot = int(lens.sum())
    if tot == 0:
        return np.empty(0, np.int64)
    starts = np.repeat(ip[idx], lens)
    base = np.repeat(np.cumsum(lens) - lens, lens)
    return ii[starts + (np.arange(tot) - base)]


# ----------------------------------------------------- SA-AMG hierarchy ----

def _spmm_flops(A, B):
    """Exact multiply-add count for the sparse product A @ B (SMMP)."""
    rc = np.diff(B.indptr).astype(float)
    return float(rc[A.indices].sum())


def strength(A, theta=0.25):
    """Row-max normalized strength, symmetrized:  |A_ij| >= theta*max_k|A_ik|
    (k != i).  On level 0 this is exactly the classical Ruge-Stuben rule for
    the M-matrix Q.  Returns a symmetric boolean CSR (no diagonal)."""
    Ac = A.tocoo()
    m = Ac.row != Ac.col
    r, c, v = Ac.row[m], Ac.col[m], np.abs(Ac.data[m])
    rowmax = np.zeros(A.shape[0])
    np.maximum.at(rowmax, r, v)
    keep = v >= theta * rowmax[r]
    r, c = r[keep], c[keep]
    S = sp.csr_matrix((np.ones(r.size), (r, c)), shape=A.shape)
    S = S + S.T
    S.data[:] = 1.0
    return S.tocsr()


def aggregate_mis(S, rng):
    """Distance-2 maximal independent set aggregation (vectorized Luby).
    Returns (agg, n_agg, rounds).  rounds is charged."""
    n = S.shape[0]
    Sc = S.tocoo()
    r, c = Sc.row, Sc.col
    prio = rng.random(n)
    state = np.zeros(n, np.int8)          # 0 undecided, 1 root, -1 covered
    rounds = 0
    while True:
        und = state == 0
        if not und.any():
            break
        rounds += 1
        p = np.where(und, prio, -1.0)
        m1 = np.full(n, -1.0)
        np.maximum.at(m1, r, p[c])
        m1 = np.maximum(m1, p)
        m2 = np.full(n, -1.0)
        np.maximum.at(m2, r, m1[c])
        m2 = np.maximum(m2, m1)
        newroots = und & (p >= m2) & (p > 0)
        if not newroots.any():
            state[und] = 1              # isolated leftovers become roots
            break
        state[newroots] = 1
        # everything within distance 2 of a new root is covered
        cov = np.zeros(n, bool)
        cov[newroots] = True
        c1 = np.zeros(n, bool)
        np.logical_or.at(c1, r, cov[c])
        cov2 = cov | c1
        c2 = np.zeros(n, bool)
        np.logical_or.at(c2, r, cov2[c])
        cov = cov2 | c2
        state[cov & (state == 0)] = -1
        if rounds > 40:
            state[state == 0] = 1
            break
    roots = np.flatnonzero(state == 1)
    agg = np.full(n, -1, np.int64)
    agg[roots] = np.arange(roots.size)
    # two propagation rounds (distance <= 2 from a root)
    for _ in range(2):
        cand = np.full(n, -1, np.int64)
        has = agg >= 0
        src = np.where(has[c], agg[c], np.iinfo(np.int64).max)
        best = np.full(n, np.iinfo(np.int64).max)
        np.minimum.at(best, r, src)
        upd = (agg < 0) & (best < np.iinfo(np.int64).max)
        agg[upd] = best[upd]
    left = agg < 0
    if left.any():                       # isolated vertices: singletons
        k = roots.size
        agg[left] = k + np.arange(int(left.sum()))
    return agg, int(agg.max()) + 1, rounds + 2


def build_hierarchy(A0, B0, meter, level0_scan, theta=0.25, npower=12,
                    max_coarse=60, max_levels=14, rng=None, smooth=True,
                    rho0=None, vol0=0.0):
    """Smoothed-aggregation hierarchy on A0.  Every operation charged.
    `level0_scan(k)` charges k full graph-scan passes over the region."""
    rng = rng or np.random.default_rng(0)
    levels = []
    A = A0.tocsr()
    B = B0.copy()
    info = []
    lev = 0
    while True:
        n_l = A.shape[0]
        nnzA = float(A.nnz)
        if n_l <= max_coarse or lev >= max_levels - 1:
            break
        # --- strength of connection
        if lev == 0:
            level0_scan(1)
        else:
            meter.resp(nnzA)
        S = strength(A, theta)
        # --- aggregation
        agg, nagg, rounds = aggregate_mis(S, rng)
        unit = float(vol0) if lev == 0 else float(S.nnz)
        meter.agg += rounds * unit
        meter.agg_seq += 3.0 * unit
        if lev == 0:
            level0_scan(rounds)
        else:
            meter.resp(rounds * float(S.nnz))
        if nagg >= 0.9 * n_l or nagg == 0:
            break                        # coarsening stalled
        # --- tentative prolongator (one near-nullspace vector)
        Tcol = agg
        norms = np.zeros(nagg)
        np.add.at(norms, agg, B * B)
        norms = np.sqrt(np.maximum(norms, 1e-300))
        Tdata = B / norms[agg]
        T = sp.csr_matrix((Tdata, Tcol, np.arange(n_l + 1)),
                          shape=(n_l, nagg))
        Bc = norms
        meter.resp(3.0 * n_l) if lev else meter.rec(3.0 * n_l)
        # --- spectral radius of D^-1 A_l.
        # LEVEL 0 IS FREE AND RIGOROUS: diag(Q) = (1+a)/2 uniformly and
        # spec(Q) subset [a,1] (Cauchy interlacing keeps that for Q[S,S]), so
        # rho(D^-1 Q_SS) <= 2/(1+a) EXACTLY -- no estimation, no scan, and the
        # weighted-Jacobi smoother is then provably convergent with
        # spec(I - om D^-1 Q) subset [-1/3, 1-(4/3)a] for om = 4/(3 rho).
        dg = A.diagonal().copy()
        dg[dg == 0] = 1.0
        Dinv = sp.diags(1.0 / dg)
        DA = (Dinv @ A).tocsr()
        if lev == 0 and rho0 is not None:
            rho = rho0
        else:
            v = rng.standard_normal(n_l)
            rho = 1.0
            for _ in range(npower):
                w = DA @ v
                nw = np.linalg.norm(w)
                if nw == 0:
                    break
                rho = max(rho, nw / np.linalg.norm(v))
                v = w / nw
            rho = 1.25 * max(rho, 1e-12)      # safety: power iter. is a
            meter.resp(npower * nnzA)         # lower bound on rho
        # --- prolongator smoothing  P = (I - (4/(3 rho)) D^-1 A) T
        if smooth:
            om = 4.0 / (3.0 * rho)
            fl = _spmm_flops(DA, T)
            P = (T - om * (DA @ T)).tocsr()
            P.eliminate_zeros()
            if lev == 0:
                meter.rec(fl + float(P.nnz))
            else:
                meter.resp(fl + float(P.nnz))
        else:
            P = T
        # --- Galerkin RAP
        AP = (A @ P).tocsr()
        f1 = _spmm_flops(A, P)
        Pt = P.T.tocsr()
        f2 = _spmm_flops(Pt, AP)
        Ac = (Pt @ AP).tocsr()
        if lev == 0:
            meter.rec(f1 + f2)
        else:
            meter.resp(f1 + f2)
        meter.mat(float(P.nnz) + float(Ac.nnz) + 2.0 * n_l)
        levels.append(dict(A=A, P=P, Pt=Pt, n=n_l, nnz=nnzA, rho=rho,
                           dinv=1.0 / dg, om=(4.0 / (3.0 * rho))))
        info.append(dict(lev=lev, n=n_l, nnz=int(nnzA), nagg=int(nagg),
                         nnzP=int(P.nnz), nnzAc=int(Ac.nnz),
                         cop=float(Ac.nnz) / max(nnzA, 1.0)))
        A, B = Ac, Bc
        lev += 1
    # --- coarsest level: sparse LU with a fill-reducing ordering, charged at
    #     sum_j nnz(L[:,j])^2 factor flops + 2*nnz(L+U) per solve.
    nc = A.shape[0]
    if nc <= 3:
        lu = ("dense", sla.lu_factor(A.toarray()))
        meter.resp((2.0 / 3.0) * nc ** 3)
        meter.mat(float(nc) ** 2)
        solve_nnz = float(nc) ** 2
    else:
        slu = spla.splu(A.tocsc(), permc_spec="MMD_AT_PLUS_A",
                        diag_pivot_thresh=0.0,
                        options=dict(SymmetricMode=True))
        Lm = slu.L.tocsc()
        cntl = np.diff(Lm.indptr).astype(float)
        meter.resp(float(np.sum(cntl ** 2)))
        meter.mat(float(Lm.nnz + slu.U.nnz))
        solve_nnz = float(Lm.nnz + slu.U.nnz)
        lu = ("sparse", slu)
    dgc = A.diagonal().copy()
    dgc[dgc == 0] = 1.0
    levels.append(dict(A=A, P=None, Pt=None, n=nc, nnz=float(A.nnz),
                       lu=lu, dinv=1.0 / dgc, om=None, solve_nnz=solve_nnz))
    info.append(dict(lev=lev, n=int(nc), nnz=int(A.nnz), coarse=True))
    return levels, info


def _jacobi(A, x, f, dinv, om, k):
    for _ in range(k):
        x += om * dinv * (f - A @ x)
    return x


def v_cycle(levels, l, x, f, meter, level0_scan, nu1=2, nu2=2):
    L = levels[l]
    if L["P"] is None:
        kind, fac = L["lu"]
        x[:] = (sla.lu_solve(fac, f) if kind == "dense" else fac.solve(f))
        meter.resp(2.0 * L["solve_nnz"])
        return x
    A, dinv, om = L["A"], L["dinv"], L["om"]
    if l == 0:
        level0_scan(nu1 + 1 + nu2)          # nu1 pre + residual + nu2 post
    else:
        meter.resp((nu1 + 1 + nu2) * L["nnz"])
    _jacobi(A, x, f, dinv, om, nu1)
    r = f - A @ x
    fc = L["Pt"] @ r
    meter.resp(float(L["P"].nnz))
    xc = np.zeros(fc.shape[0])
    v_cycle(levels, l + 1, xc, fc, meter, level0_scan, nu1, nu2)
    x += L["P"] @ xc
    meter.resp(float(L["P"].nnz))
    _jacobi(A, x, f, dinv, om, nu2)
    return x


# ------------------------------------------------------------ local AMG ----

def radius_ladder(rmax, ratio=1.3):
    out, r = [], 1
    while r <= rmax:
        out.append(r)
        r = max(r + 1, int(math.ceil(ratio * r)))
    return out


def amg_local(model, eps, meter, nu1=2, nu2=2, max_cycles=40, rmax=None,
              x_exact=None, oracle=False, theta=0.25, max_coarse=40,
              stall=0.6, stall_win=2, verbose=False, warm=True,
              smooth=True, rseed=0, wall_cap=240.0, grow=1.5):
    """LOCAL ALGEBRAIC MULTIGRID.  Growing BFS ball region + SA V-cycles,
    self-certified by the MEASURED residual over Omega U dOmega.  Every level,
    transfer, aggregation pass, RAP, coarse solve and every failed region
    attempt is charged."""
    alpha = model.alpha
    target = alpha * eps
    rng = np.random.default_rng(rseed)
    ex = Explorer(model, meter)
    if rmax is None:
        rmax = model.n
    Q, sqd, b = model.Q, model.sqd, model.b
    xg = np.zeros(model.n)
    hist = []
    last = None
    t_start = time.perf_counter()
    R = 0
    volprev = 0.0
    exhausted = False
    tot_cycles = 0
    attempts = 0
    allrates = []
    while True:
        if time.perf_counter() - t_start > wall_cap:
            break
        # VOLUME-DRIVEN LADDER: add BFS shells one at a time until the ball's
        # volume has grown by >= `grow` since the last attempted region.  This
        # bounds the final over-shoot by `grow` on families whose balls grow
        # polynomially (grids) AND exponentially (trees, expanders); a purely
        # geometric radius ladder over-shoots trees by 2^(0.3 R).
        while True:
            R += 1
            if not ex.grow_to(R + 1):
                exhausted = True
                R = min(R, ex.r)
                break
            if ex.ballvol(R) >= grow * volprev:
                break
        meter.phase("setup")
        S = ex.ball(R)
        if S.size == 0:
            break
        volprev = float(model.d[S].sum())
        bd = ex.ball(R + 1)
        bd = np.setdiff1d(bd, S, assume_unique=False)
        if bd.size:
            meter.scan_idx(bd)                 # boundary ring scan
        meter.scan_idx(S)                      # assemble Q[S,S]
        AS = Q[S][:, S].tocsr()
        Bt = sqd[S].copy()
        fS = b[S].copy()
        volS = float(model.d[S].sum())

        def level0_scan(k, _S=S):
            for _ in range(int(round(k))):
                meter.scan_idx(_S)

        levels, linfo = build_hierarchy(AS, Bt, meter, level0_scan,
                                        theta=theta, max_coarse=max_coarse,
                                        rng=rng, smooth=smooth,
                                        rho0=2.0 / (1.0 + alpha), vol0=volS)
        # cross block for the boundary residual
        Xb = Q[bd][:, S].tocsr() if bd.size else None
        meter.phase("solve")
        xS = np.zeros(S.size)
        if warm and xg.any():
            # NESTED ITERATION: reuse the previous (smaller) region's iterate.
            xS[:] = xg[S]
            meter.rec(float(S.size))
        cyc = 0
        best = math.inf
        stall_ct = 0
        rates = []          # V-cycle rates on the INTERIOR residual only
        r0 = 1.0
        prev = None
        cert = math.inf
        semerr = math.inf
        while cyc < max_cycles:
            v_cycle(levels, 0, xS, fS, meter, level0_scan, nu1, nu2)
            cyc += 1
            tot_cycles += 1
            # ---- measured certificate over Omega U dOmega ----
            level0_scan(1)                                   # residual on S
            rin = fS - AS @ xS
            c_in = float(np.max(np.abs(rin) / sqd[S]))
            if bd.size:
                meter.scan_idx(bd)
                rb = -(Xb @ xS)
                c_bd = float(np.max(np.abs(rb) / sqd[bd]))
            else:
                c_bd = 0.0
            meter.rec(float(S.size + bd.size))
            cert = max(c_in, c_bd)
            # V-cycle contraction rate measured on the INTERIOR residual (the
            # boundary residual is a region floor, not a cycle property).
            if cyc == 1:
                r0 = c_in
            if prev is not None and prev > 1e-12 * max(r0, 1e-300):
                rates.append(c_in / prev)      # discard machine-noise ratios
            prev = c_in
            if x_exact is not None:
                xg[:] = 0.0
                xg[S] = xS
                semerr = float(np.max(np.abs(xg - x_exact) / sqd))
            ok = (semerr <= eps) if oracle else (cert < target)
            if ok:
                xg[:] = 0.0
                xg[S] = xS
                hist.append(dict(R=R, cycles=cyc, cert=cert, semerr=semerr,
                                 c_in=c_in, c_bd=c_bd, volOmega=volS,
                                 levels=linfo, rates=rates))
                allrates += rates
                return dict(x=xg, status="cert", R=R, cycles=cyc, cert=cert,
                            semerr=semerr, hist=hist, volOmega=volS,
                            nOmega=int(S.size), levels=linfo,
                            rate=float(np.median(rates)) if rates else None,
                            allrate=(float(np.median(allrates)) if allrates
                                     else None),
                            rmax_rate=(float(np.max(allrates)) if allrates
                                       else None),
                            tot_cycles=tot_cycles, attempts=attempts + 1,
                            nlev=len(levels))
            # EARLY REGION REJECTION: the boundary residual is a floor no
            # further V-cycling can lower.
            if (not oracle) and cyc >= 3 and c_bd >= target:
                break
            if cert < stall * best:
                best = cert
                stall_ct = 0
            else:
                stall_ct += 1
                if stall_ct >= stall_win:
                    break
        hist.append(dict(R=R, cycles=cyc, cert=cert, semerr=semerr,
                         volOmega=volS, levels=linfo, rates=rates, grew=True))
        attempts += 1
        allrates += rates
        last = dict(R=R, cycles=cyc, cert=cert, volOmega=volS, levels=linfo,
                    rates=rates, nOmega=int(S.size), nlev=len(levels),
                    tot_cycles=tot_cycles, attempts=attempts,
                    allrate=float(np.median(allrates)) if allrates else None,
                    rmax_rate=float(np.max(allrates)) if allrates else None)
        if warm:
            xg[:] = 0.0
            xg[S] = xS
        if exhausted or S.size >= model.n:
            break
        if verbose:
            print(f"    AMG grow R={R} n={S.size} cyc={cyc} "
                  f"cert={cert:.3e} tgt={target:.3e} "
                  f"rate={np.median(rates) if rates else float('nan'):.3f}")
    if last is None:
        last = dict(R=0, cycles=0, cert=math.inf, volOmega=0.0, levels=[],
                    rates=[], nOmega=0, nlev=0, tot_cycles=0, attempts=0,
                    allrate=None, rmax_rate=None)
    return dict(x=xg, status="maxed", hist=hist,
                rate=(float(np.median(last["rates"])) if last["rates"]
                      else None), **{k: v for k, v in last.items()
                                     if k != "rates"})


# ------------------------------------------------- baselines ---------------

def push_c(model, eps):
    n = model.n
    A = model.A.tocsr()
    indptr = A.indptr.astype(np.int32)
    indices = A.indices.astype(np.int32)
    p = np.zeros(n)
    r = np.zeros(n)
    seen = np.zeros(n, np.uint8)
    inq = np.zeros(n, np.uint8)
    queue = np.zeros(n + 1, np.int32)
    wf = ctypes.c_longlong(0)
    wr = ctypes.c_longlong(0)
    t0 = time.perf_counter()
    npush = _LIB.cpush(n, indptr, indices, model.alpha, eps, model.seed, p, r,
                       ctypes.byref(wf), ctypes.byref(wr), seen, inq, queue)
    return dict(x=p / model.sqd, W=float(wf.value + wr.value),
                C_adj=float(wf.value), R_adj=float(wr.value),
                n_push=int(npush), wall=time.perf_counter() - t0)


def cheb_local(model, eps, meter, tau_frac=0.25, hard_factor=8,
               max_wall=90.0):
    """W5 truncated Chebyshev with the free measured certificate."""
    alpha = model.alpha
    theta = (1 + alpha) / 2.0
    delta = (1 - alpha) / 2.0
    sigma = theta / delta
    Q, b, sqd, n = model.Q, model.b, model.sqd, model.n
    seed = model.seed
    tgt = alpha * eps
    tau = tau_frac * eps
    win = int(math.ceil(2.0 / math.sqrt(alpha))) + 5
    need = max(1.0, 1.0 / (0.45 * eps))
    Kc = int(math.ceil(math.acosh(need) / math.acosh(sigma))) + 2
    hard = hard_factor * Kc + 10
    t0 = time.perf_counter()
    x_prev = np.zeros(n)
    supp = np.zeros(n, bool)
    supp[seed] = True
    meter.scan_idx(np.flatnonzero(supp))
    r = b - Q @ x_prev
    meter.rec(int(supp.sum()))
    if float(np.max(np.abs(r) / sqd)) < tgt:
        return dict(x=x_prev, status="cert", iters=0)
    x = x_prev + r / theta
    meter.rec(1)
    ucoef = 1.0 / sigma
    best = math.inf
    last = 1
    k = 1
    while True:
        mask = (x != 0.0) & (np.abs(x) < tau * sqd)
        mask[seed] = False
        if mask.any():
            x[mask] = 0.0
        supp = x != 0.0
        supp[seed] = True
        meter.scan_idx(np.flatnonzero(supp))
        r = b - Q @ x
        meter.rec(int(supp.sum()))
        cert = float(np.max(np.abs(r) / sqd))
        if cert < tgt:
            return dict(x=x, status="cert", iters=k)
        if cert < 0.75 * best:
            best = cert
            last = k
        elif k - last >= win:
            tau *= 0.25
            last = k
        if k >= hard or time.perf_counter() - t0 > max_wall:
            return dict(x=x, status="maxed", iters=k)
        ucoef = 1.0 / (2.0 * sigma - ucoef)
        rho = 2.0 * sigma * ucoef
        xn = rho * (x + r / theta) + (1.0 - rho) * x_prev
        meter.rec(int(np.count_nonzero(xn)))
        x_prev, x = x, xn
        k += 1


def direct_local(model, eps, meter, rmax=None, max_nnz=4e7, wall_cap=90.0):
    """EXPLORE + exact sparse-LU (fill-reducing) solve of Q[S,S] on the same
    growing ball, same measured certificate.  Generalizes I2-F's ND-EES and
    stands in for the elimination line (EES / HSEG-LDL) on every family."""
    alpha = model.alpha
    tgt = alpha * eps
    ex = Explorer(model, meter)
    Q, sqd, b = model.Q, model.sqd, model.b
    xg = np.zeros(model.n)
    if rmax is None:
        rmax = model.n
    last = None
    t0w = time.perf_counter()
    R = 0
    volprev = 0.0
    exhausted = False
    while True:
        if time.perf_counter() - t0w > wall_cap:
            return dict(x=xg, status="cap", **(last or dict(
                R=0, cert=math.inf, volOmega=0.0, nOmega=0)))
        while True:
            R += 1
            if not ex.grow_to(R + 1):
                exhausted = True
                R = min(R, ex.r)
                break
            if ex.ballvol(R) >= 1.5 * volprev:
                break
        S = ex.ball(R)
        if S.size == 0:
            break
        volprev = float(model.d[S].sum())
        bd = np.setdiff1d(ex.ball(R + 1), S)
        if bd.size:
            meter.scan_idx(bd)
        meter.scan_idx(S)
        AS = Q[S][:, S].tocsc()
        try:
            lu = spla.splu(AS, permc_spec="MMD_AT_PLUS_A",
                           diag_pivot_thresh=0.0,
                           options=dict(SymmetricMode=True))
        except Exception:
            return dict(x=xg, status="fail", R=R, volOmega=0.0)
        Lm = lu.L.tocsc()
        cnt = np.diff(Lm.indptr).astype(float)
        meter.resp(float(np.sum(cnt ** 2)))
        meter.mat(float(Lm.nnz + lu.U.nnz))
        xS = lu.solve(b[S])
        meter.resp(2.0 * float(Lm.nnz + lu.U.nnz))
        meter.scan_idx(S)
        rin = b[S] - AS @ xS
        c_in = float(np.max(np.abs(rin) / sqd[S]))
        if bd.size:
            meter.scan_idx(bd)
            c_bd = float(np.max(np.abs(-(Q[bd][:, S] @ xS)) / sqd[bd]))
        else:
            c_bd = 0.0
        meter.rec(float(S.size + bd.size))
        cert = max(c_in, c_bd)
        volS = float(model.d[S].sum())
        last = dict(R=R, cert=cert, volOmega=volS, nOmega=int(S.size))
        if cert < tgt:
            xg[S] = xS
            return dict(x=xg, status="cert", **last)
        if float(Lm.nnz) > max_nnz:
            return dict(x=xg, status="cap", **last)
        if exhausted or S.size >= model.n:
            break
    return dict(x=xg, status="maxed", **(last or dict(R=0, cert=math.inf,
                                                      volOmega=0.0, nOmega=0)))
