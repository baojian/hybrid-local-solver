"""I4-D families + exact output-measure statistics."""
import math, random, sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
import zoo
from amglib import GModel, VecMeter, amg_local, push_c, cheb_local, direct_local


# ---------------- extra families ----------------
def fast_grid(w, h):
    adj = {}
    for y in range(h):
        for x in range(w):
            u = y * w + x
            nb = []
            if x: nb.append(u - 1)
            if x + 1 < w: nb.append(u + 1)
            if y: nb.append(u - w)
            if y + 1 < h: nb.append(u + w)
            adj[u] = sorted(nb)
    return adj, (h // 2) * w + w // 2


def fast_grid3(w):
    adj = {}
    for z in range(w):
        for y in range(w):
            for x in range(w):
                u = (z * w + y) * w + x
                nb = []
                if x: nb.append(u - 1)
                if x + 1 < w: nb.append(u + 1)
                if y: nb.append(u - w)
                if y + 1 < w: nb.append(u + w)
                if z: nb.append(u - w * w)
                if z + 1 < w: nb.append(u + w * w)
                adj[u] = sorted(nb)
    c = w // 2
    return adj, (c * w + c) * w + c


def rrt(n, sd=7):
    rng = random.Random(sd)
    adj = {i: [] for i in range(n)}
    for i in range(1, n):
        p = rng.randrange(i)
        adj[i].append(p); adj[p].append(i)
    return {u: sorted(v) for u, v in adj.items()}, 0


def comb(B, T):
    """backbone b_0..b_{B-1}; each carries a pendant path of T vertices."""
    edges = [(i, i + 1) for i in range(B - 1)]
    nid = B
    for i in range(B):
        prev = i
        for _ in range(T):
            edges.append((prev, nid)); prev = nid; nid += 1
    return zoo._sym(edges, nid), 0


def hidden_hub(pre, M, tail=0):
    """seed - v1 - ... - v_pre - HUB(M leaves).  S_eps = the short path;
    the hub is a *boundary* vertex of unbounded degree."""
    edges = [(i, i + 1) for i in range(pre)]
    hub = pre
    nid = pre + 1
    for _ in range(M):
        edges.append((hub, nid)); nid += 1
    return zoo._sym(edges, nid), 0


def ball_trap(L, M, at=None):
    """path 0..L-1 (seed at 0) with a CLIQUE of size M attached at vertex `at`
    through a single edge.  vol(S_eps) stays path-sized; any BFS-BALL method
    that reaches depth `at`+1 pays M^2."""
    if at is None:
        at = L // 2
    edges = [(i, i + 1) for i in range(L - 1)]
    base = L
    for i in range(M):
        for j in range(i + 1, M):
            edges.append((base + i, base + j))
    edges.append((at, base))
    return zoo._sym(edges, base + M), 0


def powerlaw_tree(n, gamma=2.2, sd=11):
    """preferential-attachment-like tree with heavy tail (BA m=1)."""
    rng = random.Random(sd)
    adj = {i: [] for i in range(n)}
    targets = [0]
    for i in range(1, n):
        p = targets[rng.randrange(len(targets))]
        adj[i].append(p); adj[p].append(i)
        targets.append(p); targets.append(i)
    return {u: sorted(v) for u, v in adj.items()}, 0


# ---------------- exact output measure ----------------
def exact_u(model, how="lu"):
    """u = pi/d, computed exactly (sparse LU) or to machine tol by CG."""
    if how == "lu":
        x0 = spla.spsolve(model.Q.tocsc(), model.b)
    else:
        x0, _ = spla.cg(model.Q, model.b, rtol=1e-13, atol=1e-18,
                        maxiter=200000)
        rr = float(np.max(np.abs(model.Q @ x0 - model.b) / model.sqd))
        model.cg_resid = rr
    model._x0 = x0
    pi = x0 * model.sqd
    return x0, pi / model.d


def out_stats(model, eps, u=None):
    """Everything about the OUTPUT: S_eps, its volume, its boundary."""
    if u is None:
        _, u = exact_u(model)
    S = np.flatnonzero(u > eps)
    n = model.n
    inS = np.zeros(n, bool); inS[S] = True
    volS = float(model.d[S].sum())
    # outer boundary ring
    if S.size:
        nb = np.concatenate([model.indices[model.indptr[v]:model.indptr[v + 1]]
                             for v in S])
        nb = np.unique(nb)
        B = nb[~inS[nb]]
    else:
        B = np.array([], dtype=np.int64)
    volB = float(model.d[B].sum())
    # is the support clipped by the finite graph?  (max u on the graph rim)
    return dict(nS=int(S.size), volS=volS, nB=int(B.size), volB=volB,
                sumpi=float((u * model.d).sum()), umax=float(u.max()),
                volS_eps=volS * eps, nS_eps=S.size * eps,
                volB_eps=volB * eps)
