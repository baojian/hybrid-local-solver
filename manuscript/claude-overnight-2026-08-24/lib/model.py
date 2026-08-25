"""Source-aligned PPR/RPPR model for the overnight campaign.

Conventions (manuscript/tex/shared + notes/_shared/problem_definition):
  L_sym = I - D^{-1/2} A D^{-1/2}
  Q     = alpha*I + (1-alpha)/2 * L_sym
        = (1+alpha)/2 * I - (1-alpha)/2 * D^{-1/2} A D^{-1/2}
  b     = alpha * D^{-1/2} s
  x0    = Q^{-1} b            (source-aligned solution)
  pi    = D^{1/2} x0          (lazy PPR vector; sums to 1 for stochastic s)
  semantic error  err(x_hat) = ||D^{-1/2}(x_hat - x0)||_inf
                             = max_i |pi_hat_i - pi_i| / d_i
  certificate     ||D^{-1/2}(Q x_hat - b)||_inf < alpha*eps  =>  err < eps
  RPPR objective  F_rho(x) = 0.5 x'Qx - b'x + alpha*rho*||D^{1/2} x||_1
  Degree-scaled push system (CF-Push scale):
      H pi = gamma_a e_v,  H = I - c_a A D^{-1},
      c_a = (1-alpha)/(1+alpha), gamma_a = 2*alpha/(1+alpha)

Graphs are dicts: {node: sorted list of neighbors}, nodes 0..n-1, simple,
undirected, no isolated vertices.
"""
from fractions import Fraction
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


# ---------- graph plumbing ----------

def degrees(adj):
    return np.array([len(adj[u]) for u in range(len(adj))], dtype=float)


def adjacency_csr(adj):
    n = len(adj)
    rows, cols = [], []
    for u in range(n):
        for v in adj[u]:
            rows.append(u); cols.append(v)
    data = np.ones(len(rows))
    return sp.csr_matrix((data, (rows, cols)), shape=(n, n))


def vol(adj, S):
    return sum(len(adj[u]) for u in S)


# ---------- float model ----------

class Model:
    def __init__(self, adj, alpha, seed):
        """seed: dict {node: mass} or int (single seed)."""
        self.adj = adj
        self.n = n = len(adj)
        self.alpha = float(alpha)
        self.d = degrees(adj)
        self.sqd = np.sqrt(self.d)
        self.A = adjacency_csr(adj)
        Dm12 = sp.diags(1.0 / self.sqd)
        self.N = Dm12 @ self.A @ Dm12          # D^{-1/2} A D^{-1/2}
        a = (1 - self.alpha) / 2.0
        c = (1 + self.alpha) / 2.0
        self.Q = (sp.identity(n) * c - a * self.N).tocsr()
        s = np.zeros(n)
        if isinstance(seed, dict):
            for k, v_ in seed.items():
                s[k] = v_
        else:
            s[seed] = 1.0
        self.s = s
        self.b = self.alpha * s / self.sqd

    def solve_exact(self):
        x0 = spla.spsolve(self.Q.tocsc(), self.b)
        return x0

    def pi(self, x=None):
        if x is None:
            x = self.solve_exact()
        return self.sqd * x

    def semantic_err(self, x_hat, x0=None):
        if x0 is None:
            x0 = self.solve_exact()
        return np.max(np.abs(x_hat - x0) / self.sqd)

    def cert_resid(self, x_hat):
        """||D^{-1/2}(Q x_hat - b)||_inf ; < alpha*eps certifies err < eps."""
        return np.max(np.abs(self.Q @ x_hat - self.b) / self.sqd)

    def grad(self, x):
        return self.Q @ x - self.b

    def F_rho(self, x, rho):
        return 0.5 * x @ (self.Q @ x) - self.b @ x \
            + self.alpha * rho * np.sum(self.sqd * np.abs(x))

    def prox_grad_step(self, x, rho, eta=1.0):
        """ISTA step with step size eta (L=1)."""
        u = x - eta * self.grad(x)
        thr = eta * self.alpha * rho * self.sqd
        return np.sign(u) * np.maximum(np.abs(u) - thr, 0.0)

    def rppr_exact(self, rho, iters=None, tol=1e-14):
        """High-accuracy RPPR solution by ISTA to machine tolerance."""
        x = np.zeros(self.n)
        it = 0
        while True:
            xn = self.prox_grad_step(x, rho)
            if np.max(np.abs(xn - x)) < tol or (iters and it > iters):
                return xn
            x = xn; it += 1
            if it > 2_000_000:
                return x


# ---------- exact (Fraction) model for small graphs ----------

class ExactModel:
    def __init__(self, adj, alpha, seed):
        self.adj = adj
        self.n = n = len(adj)
        self.alpha = Fraction(alpha)
        self.d = [Fraction(len(adj[u])) for u in range(n)]
        a = (1 - self.alpha) / 2
        c = (1 + self.alpha) / 2
        # Q in scaled coordinates: Q_ij = c*delta_ij - a * A_ij/sqrt(di dj).
        # To stay in Q(rationals), work with M = D^{1/2} Q D^{-1/2} acting on
        # z = D^{1/2} x  (the pi scale):  M = c*I - a*A D^{-1}.
        # M z = D^{1/2} b = alpha * s.
        self.M = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            self.M[i][i] = c
            for j in adj[i]:
                self.M[i][j] -= a / self.d[j]
        self.s = [Fraction(0)] * n
        if isinstance(seed, dict):
            for k, v_ in seed.items():
                self.s[k] = Fraction(v_)
        else:
            self.s[seed] = Fraction(1)
        self.rhs = [self.alpha * si for si in self.s]

    def solve_pi(self):
        """Exact pi by Gaussian elimination over Fractions."""
        n = self.n
        M = [row[:] for row in self.M]
        r = self.rhs[:]
        for col in range(n):
            piv = next(i for i in range(col, n) if M[i][col] != 0)
            M[col], M[piv] = M[piv], M[col]
            r[col], r[piv] = r[piv], r[col]
            inv = 1 / M[col][col]
            M[col] = [v * inv for v in M[col]]
            r[col] *= inv
            for i in range(n):
                if i != col and M[i][col] != 0:
                    f = M[i][col]
                    M[i] = [vi - f * vc for vi, vc in zip(M[i], M[col])]
                    r[i] -= f * r[col]
        return r  # pi

    def semantic_err_pi(self, pi_hat, pi=None):
        if pi is None:
            pi = self.solve_pi()
        return max(abs(ph - p) / d for ph, p, d in zip(pi_hat, pi, self.d))


# ---------- degree-scaled push scale (CF-Push / APPR live here) ----------

def push_params(alpha):
    alpha = float(alpha)
    c_a = (1 - alpha) / (1 + alpha)
    g_a = 2 * alpha / (1 + alpha)
    return c_a, g_a


def appr_lazy(adj, alpha, seed, eps_appr, meter=None, order="fifo"):
    """Literal lazy ACL push (manuscript sec 4). Returns p (mass scale).
    Active: r[u] >= eps_appr * d[u]. Charges d_u per push via meter."""
    from collections import deque
    n = len(adj)
    d = [len(adj[u]) for u in range(n)]
    a = (1 - alpha) / 2.0
    p = [0.0] * n
    r = [0.0] * n
    r[seed] = 1.0
    q = deque([seed]); inq = [False] * n; inq[seed] = True
    while q:
        u = q.popleft(); inq[u] = False
        if r[u] < eps_appr * d[u]:
            continue
        xi = r[u]
        if meter: meter.scan(u)
        p[u] += alpha * xi
        r[u] = a * xi
        for w in adj[u]:
            r[w] += a * xi / d[u]
            if not inq[w] and r[w] >= eps_appr * d[w]:
                q.append(w); inq[w] = True
        if not inq[u] and r[u] >= eps_appr * d[u]:
            q.append(u); inq[u] = True
    return p, r
