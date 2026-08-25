"""W8 contenders under the shared degree-charged Meter convention.

Work accounting (explicit):
  PUSH (APPR, lazy FIFO, lib appr_lazy semantics, C port for speed):
     W_push = C_adj + R_adj: every EXECUTED push of u charges d_u
     (first exposure -> C_adj, repeats -> R_adj). Nothing else charged
     (coordinate updates are O(d_u) and folded into the scan charge,
     exactly as in the campaign's other work packages).
  WY-STYLE ACTIVE SET (grow S by boundary violations; exact restricted
  solve per expansion via scipy splu):
     scans:   joining vertex v charges d_v (C_adj); each round's boundary-
              residual evaluation charges d_u for every frontier vertex
              (member of S with an outside neighbor)  -> C_adj/R_adj.
     C_rec:   assembly/slicing of Q_SS each round charges vol(S).
     C_resp:  factorization charges nnz(L)+nnz(U); the two triangular
              solves charge 2*(nnz(L)+nnz(U)).  (Task convention:
              "factor nnz + solve flops".)
     W_WY = C_adj + R_adj + C_rec + C_resp.
  TARGET ORACLE: W_target = 1/(sqrt(alpha)*eps), charged verbatim.
     (Idealized; for map positioning only.)

Termination / accuracy (both contenders held to the same semantic eps):
  push: activation threshold eps_appr = eps; residual r < eps*d pointwise
        at exit; the ONE-SIDED ACL bound gives semantic err <= eps a
        priori (pi - p = alpha*M^{-1} r, M^{-1} >= 0, M^{-1} d = d/alpha
        with M = D^{1/2} Q D^{-1/2}, so err <= max r_v/d_v < eps).
  WY:   the zero-extended restricted solve x_hat satisfies an exact
        maximum principle: g = pi - pi_hat >= 0 is M-harmonic on S, so
        h = g/d is a strict (a/c)-subaverage on S and
            err = max_{v not in S} pi_v/d_v      (attained OUTSIDE S).
        The boundary certificate cert_v = (a/d_v) * sum_{u in S ~ v}
        pihat_u/d_u is the in-S part of the subaverage identity for the
        just-outside level, so terminating at max cert < tau tracks
        err <= C*tau with C a structure constant of the region outside S
        (C <= c/alpha in the worst case -- pendant-hub traps -- but O(1)
        on path/leaf/grid-like outside structure).  We therefore run
        with tau = eps/2 and VERIFY err <= eps against the exact
        solution on every cell, tightening tau adaptively (work
        accumulates) if the check fails.  Tightenings are recorded; a
        fully self-certified WY needs the Wei-Yang whp estimation
        machinery (or pays the 1/alpha certificate), so measured W_WY is
        the per-instance-verified variant -- stated in findings.
"""
import ctypes
import math
import os
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
_LIB = ctypes.CDLL(os.path.join(HERE, "libcpush.so"))
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


def push_c(model, eps, seed):
    """FIFO lazy ACL push at activation threshold eps (C port of appr_lazy).
    Returns dict with p (mass scale), W split, push count, max r/d."""
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
    npush = _LIB.cpush(n, indptr, indices, model.alpha, eps, seed, p, r,
                       ctypes.byref(wf), ctypes.byref(wr), seen, inq, queue)
    dt = time.perf_counter() - t0
    return dict(p=p, r=r, C_adj=int(wf.value), R_adj=int(wr.value),
                W=int(wf.value + wr.value), n_push=int(npush),
                max_rd=float(np.max(r / model.d)), wall=dt)


def wy_active_set(model, eps, seed, max_rounds=100000, time_guard=180.0,
                  x0=None, tau_factor=0.5, max_tighten=40):
    """WY-style active-set: exact restricted solves, grow by all boundary
    violators of cert_v >= tau (tau = tau_factor*eps), terminate when
    max cert < tau AND (if x0 given) the true semantic error <= eps,
    halving tau otherwise (adaptive tightening, work accumulates)."""
    n = model.n
    alpha = model.alpha
    a = (1.0 - alpha) / 2.0
    d = model.d
    sqd = model.sqd
    Q = model.Q.tocsr()
    A = model.A.tocsr()
    b = model.b

    in_S = np.zeros(n, bool)
    scanned = np.zeros(n, bool)
    out_deg = d.astype(np.int64).copy()   # neighbors outside S (for S members)
    S_list = []
    C_adj = 0
    R_adj = 0
    C_rec = 0
    C_resp = 0

    def bulk_scan(us):
        nonlocal C_adj, R_adj
        if len(us) == 0:
            return
        dv = d[us]
        first = ~scanned[us]
        C_adj += int(dv[first].sum())
        R_adj += int(dv[~first].sum())
        scanned[us] = True

    def join(us):
        nonlocal out_deg
        bulk_scan(us)                       # d_v charge covers set updates
        in_S[us] = True
        for v in us:
            nb = A.indices[A.indptr[v]:A.indptr[v + 1]]
            out_deg[nb] -= 1
            out_deg[v] = d[v].astype(np.int64) - int(in_S[nb].sum())
            S_list.append(int(v))

    join(np.array([seed]))
    t0 = time.perf_counter()
    rounds = 0
    nnz_lu = 0
    status = "ok"
    xS = None
    S = None
    tau = tau_factor * eps
    tightenings = 0
    while True:
        rounds += 1
        S = np.array(S_list, dtype=np.int64)
        volS = int(d[S].sum())
        C_rec += volS                                     # assembly charge
        QSS = Q[S][:, S].tocsc()
        lu = spla.splu(QSS, permc_spec="MMD_AT_PLUS_A")
        nnz_lu = int(lu.L.nnz + lu.U.nnz)
        C_resp += nnz_lu                                  # factor charge
        xS = lu.solve(b[S])
        C_resp += 2 * nnz_lu                              # solve flops
        # boundary certificate:
        # cert_v = (a/d_v) * sum_{u in S ~ v} pihat_u/d_u,  v not in S
        F = S[out_deg[S] > 0]
        bulk_scan(F)                                      # frontier scans
        z = np.zeros(n)
        z[S] = xS / sqd[S]
        cert = a * (A @ z) / d
        cert[in_S] = 0.0
        cmax = float(cert.max()) if n > len(S_list) else 0.0
        if cmax < tau:
            if x0 is not None and len(S_list) < n:
                x_try = np.zeros(n)
                x_try[S] = xS
                err_now = float(np.max(np.abs(x_try - x0) / sqd))
                if err_now > eps and tightenings < max_tighten:
                    tau *= 0.5
                    tightenings += 1
                    continue
                if err_now > eps:
                    status = "tighten-cap"
            break
        viol = np.flatnonzero(~in_S & (cert >= tau))
        join(viol)
        if rounds >= max_rounds:
            status = "round-cap"
            break
        if time.perf_counter() - t0 > time_guard:
            status = "timeout"
            break
    x_hat = np.zeros(n)
    x_hat[S] = xS
    W = C_adj + R_adj + C_rec + C_resp
    return dict(x=x_hat, W=W, C_adj=C_adj, R_adj=R_adj, C_rec=C_rec,
                C_resp=C_resp, rounds=rounds, S_size=len(S_list),
                vol_S=int(d[S].sum()), nnz_lu=nnz_lu, cert=cmax,
                tightenings=tightenings, status=status,
                wall=time.perf_counter() - t0)


def target_oracle(alpha, eps):
    return 1.0 / (math.sqrt(alpha) * eps)


# ---------- graph families (support scales with 1/eps) ----------

def family_params(name, alpha, eps):
    """Return (builder_args, n_est, m_edges) for the sized instance."""
    if name == "star":
        m = max(2, round(1.0 / (4 * eps)))
        return ("star", (m,)), m + 1, m
    if name == "spider":
        k = max(2, round(1.0 / (4 * eps)))
        L = max(1, round(2.0 / math.sqrt(alpha)))
        return ("spider", (k, L)), 1 + k * L, k * L
    if name == "spider2":
        # W2-canonical hard spider: k = sqrt(alpha)/(4 eps) arms keeps the
        # eps-superlevel set ~1/eps and forces depth ~1/sqrt(alpha)
        k = max(2, round(math.sqrt(alpha) / (4 * eps)))
        L = max(1, round(2.0 / math.sqrt(alpha)))
        return ("spider", (k, L)), 1 + k * L, k * L
    if name == "caterpillar":
        m = max(2, round(1.0 / (4 * eps)))
        return ("caterpillar", (m, 1)), 2 * m, 2 * m - 1
    if name == "btree":
        depth = max(2, math.ceil(math.log2(1.0 / eps + 1)) - 1)
        nn = 2 ** (depth + 1) - 1
        return ("btree", (depth,)), nn, nn - 1
    if name == "grid":
        side = max(3, round(math.sqrt(1.0 / (2 * eps))))
        return ("grid", (side, side)), side * side, 2 * side * (side - 1)
    raise ValueError(name)


def build_graph(kind, args):
    import sys
    sys.path.insert(0, os.path.join(HERE, "..", "lib"))
    import zoo
    if kind == "star":
        return zoo.star(*args)          # seed = center
    if kind == "spider":
        return zoo.spider(*args)        # seed = center
    if kind == "caterpillar":
        return zoo.caterpillar(*args)   # seed = backbone end
    if kind == "btree":
        return zoo.binary_tree(*args)   # seed = root
    if kind == "grid":
        return zoo.grid(*args)          # seed = corner
    raise ValueError(kind)
