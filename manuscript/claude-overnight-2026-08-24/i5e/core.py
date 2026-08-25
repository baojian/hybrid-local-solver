"""I5-E core: class R_B simulator (block relaxation with signed residual).

Class R_B (decision recorded here): state (z, r), z0 = 0, r = gamma_a e_v - H z,
H = I - c_a A D^{-1}.  Primitive = omega-relaxed EXACT block relaxation on U,
|U| <= B, omega in (0,2]:
    delta = H_UU^{-1} r_U ;  z_U += omega*delta ;  r -= omega * H[:,U] delta.
omega = 1 is block Gauss-Seidel (exact solve given boundary values); omega != 1
IS included in R_B, so R_1 recovers the whole of I4-C's R+- (coordinate case:
H_uu = 1, delta = r_u).  Output z; guarantee max_u |pi_u - z_u|/d_u <= eps
(semantic / oracle stop, as in I4-C).

Charging (both reported):
  W_vol = sum_ops vol(U)                       (adjacency exposure, = I4-C scale)
  W_S1  = sum_ops vol(U) + (|U| + intE(U))     (structured solve: tree/banded U
                                                solves in O(vol_int(U)))
  W_S3  = sum_ops vol(U) + |U|^3               (dense worst-case solve)

Cap quantities:
  tau_v(U) = ((H_sym)_UU^{-1})_vv = ((H_UU)^{-1})_vv   (diagonal similarity)
  cap_a(U, omega) = omega * sqrt(gamma_a * pi_v * tau_v(U))   [exact block op]
  cap_b(U)        = 2 * sqrt(gamma_a * pi_v * tau_v(U))       [any Phi-monotone
                                                               U-supported op]
Identity: tau_v(V) = pi_v / gamma_a  (since pi = gamma_a H^{-1} e_v).
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


def params(alpha):
    return (1.0 - alpha) / (1.0 + alpha), 2.0 * alpha / (1.0 + alpha)


def omega_star(alpha):
    t = math.sqrt(alpha)
    lam = (1 - t) / (1 + t)
    return 1.0 + lam * lam


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
        self.H = (sp.identity(n) - self.c_a * (self.A @ sp.diags(1.0 / self.d))).tocsc()
        self.rhs = np.zeros(n); self.rhs[seed] = self.g_a
        self._pi = None

    @property
    def pi(self):
        if self._pi is None:
            self._pi = spla.spsolve(self.H, self.rhs)
        return self._pi

    def err(self, z):
        return float(np.max(np.abs(self.pi - z) / self.d))

    def phi(self, z):
        e = self.pi - z
        return float(0.5 * e @ (self.H @ e / self.d))

    def HUU(self, U):
        return self.H[np.ix_(U, U)].toarray()

    def tau(self, v, U):
        """tau_v(U) = ((H_UU)^{-1})_vv ; requires v in U."""
        U = np.asarray(U)
        i = int(np.nonzero(U == v)[0][0])
        G = self.HUU(U)
        e = np.zeros(len(U)); e[i] = 1.0
        return float(np.linalg.solve(G, e)[i])

    def int_edges(self, U):
        Uset = set(int(u) for u in U)
        return sum(1 for u in Uset for w in self.adj[u] if w in Uset) // 2

    def S_eps(self, eps):
        return np.nonzero(self.pi / self.d > eps)[0]


class BlockState:
    def __init__(self, prob, track_cap=False):
        self.P = prob
        self.z = np.zeros(prob.n)
        self.r = prob.rhs.copy()
        self.W_vol = 0.0
        self.W_S1 = 0.0
        self.W_S3 = 0.0
        self.nops = 0
        self.nops_v = 0          # ops whose block contains the seed
        self.track_cap = track_cap
        self.max_util_a = 0.0    # max |dz_v| / cap_a over seed ops
        self.max_util_b = 0.0
        self._gpv = prob.g_a * prob.pi[prob.seed]

    def op(self, U, omega=1.0):
        P = self.P
        U = np.asarray(U, dtype=int)
        G = P.HUU(U)
        delta = np.linalg.solve(G, self.r[U])
        v = P.seed
        vin = v in set(int(u) for u in U)
        if self.track_cap and vin:
            i = int(np.nonzero(U == v)[0][0])
            e = np.zeros(len(U)); e[i] = 1.0
            tau = float(np.linalg.solve(G, e)[i])
            dzv = abs(omega * delta[i])
            cap_a = omega * math.sqrt(self._gpv * tau)
            cap_b = 2.0 * math.sqrt(self._gpv * tau)
            if cap_a > 0:
                self.max_util_a = max(self.max_util_a, dzv / cap_a)
                self.max_util_b = max(self.max_util_b, dzv / cap_b)
        full = np.zeros(P.n); full[U] = omega * delta
        self.z[U] += omega * delta
        self.r -= P.H @ full
        volU = float(P.d[U].sum())
        self.W_vol += volU
        self.W_S1 += volU + (len(U) + P.int_edges(U))
        self.W_S3 += volU + float(len(U)) ** 3
        self.nops += 1
        if vin:
            self.nops_v += 1

    def err(self):
        return self.P.err(self.z)
