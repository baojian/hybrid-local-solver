"""I4-C core: class R+/- simulator.

State (z, r), r = gamma_a e_v - H z,  H = I - c_a A D^{-1}.
Primitive op(u, omega):  delta = omega * r[u];  z[u] += delta; r[u] -= delta;
                         r[w] += c_a * delta / d_u  for w ~ u.   Work += d_u.
Output z.  Guarantee:  max_u |pi_u - z_u| / d_u <= eps.
Energy Phi(e) = 0.5 e^T D^{-1} H e ;  exact identity
    Phi(e) - Phi(e^+) = [omega(2-omega)/2] * r_u^2 / d_u.
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


def params(alpha):
    c_a = (1.0 - alpha) / (1.0 + alpha)
    g_a = 2.0 * alpha / (1.0 + alpha)
    return c_a, g_a


def omega_star(alpha):
    t = math.sqrt(alpha)
    lam = (1 - t) / (1 + t)
    return 1.0 + lam * lam


def lam_of(alpha):
    t = math.sqrt(alpha)
    return (1 - t) / (1 + t)


class Prob:
    def __init__(self, adj, alpha, seed):
        self.adj = adj
        self.n = n = len(adj)
        self.alpha = float(alpha)
        self.c_a, self.g_a = params(alpha)
        self.d = np.array([len(adj[u]) for u in range(n)], dtype=float)
        self.seed = seed
        rows, cols = [], []
        for u in range(n):
            for w in adj[u]:
                rows.append(u); cols.append(w)
        self.A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
        self.ADinv = (self.A @ sp.diags(1.0 / self.d)).tocsr()
        self.H = (sp.identity(n) - self.c_a * self.ADinv).tocsr()
        self.rhs = np.zeros(n); self.rhs[seed] = self.g_a
        self._pi = None

    @property
    def pi(self):
        if self._pi is None:
            self._pi = spla.spsolve(self.H.tocsc(), self.rhs)
        return self._pi

    def err(self, z):
        return float(np.max(np.abs(self.pi - z) / self.d))

    def phi(self, e):
        return float(0.5 * e @ (self.H @ e / self.d))

    def S_eps(self, eps):
        return np.nonzero(self.pi / self.d > eps)[0]

    def vol_S_eps(self, eps):
        S = self.S_eps(eps)
        return float(self.d[S].sum()), len(S)


class State:
    """Mutable R+/- state with a work meter."""
    def __init__(self, prob):
        self.P = prob
        self.n = prob.n
        self.z = np.zeros(prob.n)
        self.r = prob.rhs.copy()
        self.W = 0.0
        self.nops = 0
        self.nops_at = np.zeros(prob.n, dtype=np.int64)

    def op(self, u, omega):
        P = self.P
        du = P.d[u]
        delta = omega * self.r[u]
        self.z[u] += delta
        self.r[u] -= delta
        add = P.c_a * delta / du
        for w in P.adj[u]:
            self.r[w] += add
        self.W += du
        self.nops += 1
        self.nops_at[u] += 1
        return delta

    def err(self):
        return self.P.err(self.z)

    def phi(self):
        return self.P.phi(self.P.pi - self.z)

    def resid_inf(self):
        return float(np.max(np.abs(self.r) / self.P.d))
