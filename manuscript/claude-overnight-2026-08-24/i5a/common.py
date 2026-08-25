"""I5-A: manuscript spider verification. Shared machinery.

Conventions = manuscript sections/cf_push_two_stage_analysis.tex:
  H = I - c_a A D^{-1},  c_a=(1-a)/(1+a), g_a=2a/(1+a),  H pi = g_a e_seed
  push at u, relax w:  z_u += w*sigma; r_u -= w*sigma; r_nb += c_a*w*sigma/d_u
  Phase I: w=1, active  r_u >= g_a*tau*d_u          (one-sided)
  Phase II: w=wstar=2(1+a)/(1+sqrt a)^2, active |r_u| >= g_a*eps*d_u
  work: d_u per executed push. lambda = (1-sqrt a)/(1+sqrt a).
Semantic scale u_i = pi_i/d_i; output z valid iff max_i |pi_i - z_i|/d_i <= eps.
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from collections import deque

import sys
sys.path.insert(0, "/home/claude/work/overnight/lib")


# ---------------- parameters ----------------

def pars(alpha):
    a = float(alpha)
    t = math.sqrt(a)
    lam = (1 - t) / (1 + t)
    c = (1 - a) / (1 + a)
    g = 2 * a / (1 + a)
    wstar = 2 * (1 + a) / (1 + t) ** 2
    return t, lam, c, g, wstar


def spider_scales(alpha, theta):
    """L_sp, M, L=M+1 per eq:cf-spider-scales."""
    t, lam, c, g, wstar = pars(alpha)
    Lsp = math.log(1 / theta) / (-math.log(lam))
    M = int(math.floor(Lsp / 2))
    return Lsp, M, M + 1


def u0_closed(alpha, k, L):
    """Exact center value u0 = pi_v/d_v of the center-seeded k-arm spider,
    equal arms of length L:  u0 = (sqrt a / k) * (1+lam^{2L})/(1-lam^{2L})
                                = (sqrt a / k) * coth(L * (-log lam))."""
    t, lam, c, g, wstar = pars(alpha)
    z = lam ** (2 * L)
    return (t / k) * (1 + z) / (1 - z)


def arm_profile_closed(alpha, k, L):
    """u_j for j=1..L (center-seeded equal-arm spider)."""
    t, lam, c, g, wstar = pars(alpha)
    u0 = u0_closed(alpha, k, L)
    den = 1 + lam ** (2 * L)
    return u0, [u0 * (lam ** j + lam ** (2 * L - j)) / den for j in range(1, L + 1)]


# ---------------- instance builders (ordered adjacency) ----------------

def build_spider(k, L, pendant=False):
    """Center 0; arm a occupies ids 1+a*L .. (a+1)*L (depth 1..L).
    Center adjacency ordered by arms; arm vertices [inward, outward].
    pendant=True: extra vertex p = 1+k*L attached to center (appended LAST
    in center's adjacency list).
    Returns adj (list of lists, ordered), pos map id->('c'|'p'|(arm,depth))."""
    n = 1 + k * L + (1 if pendant else 0)
    adj = [[] for _ in range(n)]
    pos = {0: 'c'}
    for a in range(k):
        first = 1 + a * L
        adj[0].append(first)
        for j in range(1, L + 1):
            vid = a * L + j
            pos[vid] = (a, j)
            inward = 0 if j == 1 else vid - 1
            adj[vid].append(inward)
            if j < L:
                adj[vid].append(vid + 1)
    if pendant:
        p = 1 + k * L
        adj[0].append(p)
        adj[p].append(0)
        pos[p] = 'p'
    return adj, pos


def solve_pi(adj, alpha, seed):
    """Exact pi by sparse solve of H pi = g e_seed (float)."""
    n = len(adj)
    t, lam, c, g, wstar = pars(alpha)
    d = np.array([len(a) for a in adj], float)
    rows, cols, vals = [], [], []
    for u in range(n):
        rows.append(u); cols.append(u); vals.append(1.0)
        for w in adj[u]:
            rows.append(u); cols.append(w); vals.append(-c / d[w])
    H = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
    rhs = np.zeros(n); rhs[seed] = g
    pi = spla.spsolve(H.tocsc(), rhs)
    return pi, d


# ---------------- literal two-phase CF-Push FIFO ----------------

def cf_push_fifo(adj, alpha, seed, eps, tau, log_pushes=False, max_push=10**8):
    """Literal alg:cf-push with the manuscript's FIFO convention.
    Returns dict with W1, W2, n1, n2, z, r, pushes (optional list of
    (vertex, residual-before) for Phase II)."""
    n = len(adj)
    t, lam, c, g, wstar = pars(alpha)
    d = [len(a) for a in adj]
    z = [0.0] * n
    r = [0.0] * n
    r[seed] = g

    pushes = [] if log_pushes else None

    def run_phase(omega, thr_of, signed):
        W = 0; cnt = 0
        q = deque(); inq = [False] * n

        def act(u):
            return (abs(r[u]) if signed else r[u]) >= thr_of(u)
        for u in range(n):
            if act(u):
                q.append(u); inq[u] = True
        while q:
            u = q.popleft(); inq[u] = False
            if not act(u):
                continue  # stale entry, skipped, free
            sig = r[u]
            if pushes is not None and signed:
                pushes.append((u, sig))
            W += d[u]; cnt += 1
            if cnt > max_push:
                raise RuntimeError("push budget exceeded")
            z[u] += omega * sig
            r[u] -= omega * sig
            f = c * omega * sig / d[u]
            for w in adj[u]:
                r[w] += f
                if not inq[w] and act(w):
                    q.append(w); inq[w] = True
            if not inq[u] and act(u):
                q.append(u); inq[u] = True
        return W, cnt

    W1, n1 = run_phase(1.0, lambda u: g * tau * d[u], signed=False)
    W2, n2 = run_phase(wstar, lambda u: g * eps * d[u], signed=True)
    # termination check
    viol = max(abs(r[u]) / (g * eps * d[u]) for u in range(n))
    assert viol < 1.0 + 1e-9, ("certificate not met at exit", viol)
    return dict(W1=W1, W2=W2, n1=n1, n2=n2, z=np.array(z), r=np.array(r),
                pushes=pushes)


def semantic_err(z, pi, d):
    return float(np.max(np.abs(np.asarray(z) - pi) / d))


def cert_gap(adj, alpha, z, seed, eps):
    """max_u |r_u|/(g*eps*d_u) for r = g e_seed - H z."""
    n = len(adj)
    t, lam, c, g, wstar = pars(alpha)
    d = np.array([len(a) for a in adj], float)
    r = -np.asarray(z, float).copy()
    # r = g e_seed - (z - c A D^{-1} z)
    ad = np.zeros(n)
    zz = np.asarray(z, float)
    for u in range(n):
        s = 0.0
        for w in adj[u]:
            s += zz[w] / d[w]
        ad[u] = s
    r = -(zz - c * ad)
    r[seed] += g
    return float(np.max(np.abs(r) / (g * eps * d))), r
