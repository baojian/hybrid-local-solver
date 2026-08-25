"""W1: generalized one-hop push simulator (class M and signed non-members).

Canonical operation gp(u, eta) in mass scale (lazy operator, a=(1-alpha)/2):
    r[u] -= (1+alpha)/2 * eta
    r[w] += (1-alpha)/(2 d_u) * eta   for each neighbor w of u
    p[u] += alpha * eta
charged work d_u per operation.

Every one-hop invariant-preserving update is gp(u, eta) for some eta
(characterization lemma in findings/w1_monotone_lb.md):
    lazy ACL push amount xi     -> eta = xi          (needs xi <= r[u])
    non-lazy / CF push amount xi-> eta = 2*xi/(1+alpha)   (removal = xi)
    damped omega (lazy)         -> eta = omega * r[u]
    GS-SOR over-relax omega     -> eta = omega * 2*r[u]/(1+alpha)  (omega>1
                                   drives r[u] negative: leaves class M)
Class M membership == every op satisfies eta <= 2 r[u]/(1+alpha) (r stays >=0).

Invariant preserved by EVERY gp op regardless of sign: p + pr(r) = pi, where
pr(r) = alpha * (cI - a A D^{-1})^{-1} r  (mass scale), c=(1+alpha)/2.
"""
import math
import random
import numpy as np

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from zoo import star  # noqa: E402


# ---------- exact quantities on any graph ----------

def pr_matrix(adj, alpha):
    """Dense M = cI - a A D^{-1} (mass scale); pr(r) = alpha M^{-1} r."""
    n = len(adj)
    a = (1 - alpha) / 2.0
    c = (1 + alpha) / 2.0
    M = np.zeros((n, n))
    for i in range(n):
        M[i, i] = c
        for j in adj[i]:
            M[i, j] -= a / len(adj[j])
    return M


def pr_vec(adj, alpha, rvec, M=None):
    if M is None:
        M = pr_matrix(adj, alpha)
    return alpha * np.linalg.solve(M, np.asarray(rvec, dtype=float))


# ---------- simulator ----------

class GP:
    def __init__(self, adj, alpha, seed, center=None):
        self.adj = adj
        self.n = n = len(adj)
        self.alpha = alpha
        self.d = [len(adj[u]) for u in range(n)]
        self.vol = sum(self.d)
        self.p = [0.0] * n
        self.r = [0.0] * n
        self.r[seed] = 1.0
        self.seed = seed
        self.center = center            # for star bookkeeping
        # ledgers
        self.sum_p = 0.0
        self.sum_r = 1.0                # signed sums (exact identities)
        self.W = 0                      # charged work sum d_u
        self.ops = 0
        self.Z = 0.0                    # sum of eta (signed)
        self.Zc = 0.0                   # sum of eta at center
        self.ZL = 0.0                   # sum of eta at leaves
        self.n_center_ops = 0
        self.max_eta_center = 0.0
        self.min_r_seen = 0.0           # most negative coordinate ever
        self.max_l1_seen = 1.0          # max of ||r||_1 over time (exact recompute is O(n); track approx via signed bound updates)
        self._mass_err = 0.0

    def cap(self, u):
        """Max eta keeping r[u] >= 0 (class-M cap)."""
        return 2.0 * self.r[u] / (1.0 + self.alpha)

    def gp(self, u, eta):
        al = self.alpha
        self.r[u] -= 0.5 * (1 + al) * eta
        spread = 0.5 * (1 - al) * eta / self.d[u]
        for w in self.adj[u]:
            self.r[w] += spread
        self.p[u] += al * eta
        self.sum_p += al * eta
        self.sum_r -= al * eta
        self.W += self.d[u]
        self.ops += 1
        self.Z += eta
        if u == self.center:
            self.Zc += eta
            self.n_center_ops += 1
            if eta > self.max_eta_center:
                self.max_eta_center = eta
        else:
            self.ZL += eta
        if self.r[u] < self.min_r_seen:
            self.min_r_seen = self.r[u]

    # convenience wrappers -------------------------------------------------
    def push_lazy(self, u, xi):
        """ACL lazy push, amount xi <= r[u] (eta = xi)."""
        self.gp(u, xi)

    def push_nonlazy_full(self, u):
        """Full non-lazy push: removal = r[u], eta = 2 r[u]/(1+alpha)."""
        self.gp(u, self.cap(u))
        self.r[u] = 0.0  # kill float dust

    def sor_step(self, u, omega):
        """GS-SOR coordinate step: eta = omega * cap(u). omega>1 => signed."""
        self.gp(u, omega * self.cap(u))

    # checks ---------------------------------------------------------------
    def l1_r(self):
        return sum(abs(x) for x in self.r)

    def mass_check(self):
        e1 = abs(sum(self.p) + sum(self.r) - 1.0)
        e2 = abs(self.sum_p + self.sum_r - 1.0)
        e3 = abs(self.sum_p - self.alpha * self.Z)
        return max(e1, e2, e3)

    def invariant_err(self, M=None):
        """max |p + pr(r) - pi| (pi computed from same M)."""
        M = pr_matrix(self.adj, self.alpha) if M is None else M
        e = np.zeros(self.n); e[self.seed] = 1.0
        pi = pr_vec(self.adj, self.alpha, e, M)
        rec = np.array(self.p) + pr_vec(self.adj, self.alpha, self.r, M)
        return float(np.max(np.abs(rec - pi))), pi

    def err_sem(self, pi, beta=0.0):
        """Semantic degree-normalized error of output p + beta*r."""
        out = np.array(self.p) + beta * np.array(self.r)
        return float(np.max(np.abs(pi - out) / np.array(self.d, dtype=float)))


# ---------- policies (members of class M) ----------
# Each returns the GP state at stop.  stop in {'coord','l1'}:
#   'coord': all r[u] < eps*d_u   (standard APPR rule; implies l1 <= eps*vol)
#   'l1'   : sum r <= eps*vol     (weakest legal stop for the class)

OP_CAP = 4_000_000


def _stopped(st, eps, stop):
    if stop == 'l1':
        return st.sum_r <= eps * st.vol * (1 + 1e-13)
    return False  # 'coord' handled by empty active structure


def _active(st, u, eps):
    return st.r[u] >= eps * st.d[u]


def run_queue(adj, alpha, eps, seed, discipline='fifo', stop='coord',
              omega=1.0, lazy=True, rng=None):
    """FIFO/LIFO full or damped pushes."""
    st = GP(adj, alpha, seed, center=seed)
    from collections import deque
    q = deque([seed]); inq = [False] * st.n; inq[seed] = True
    while q and st.ops < OP_CAP:
        if _stopped(st, eps, stop):
            break
        u = q.popleft() if discipline == 'fifo' else q.pop()
        inq[u] = False
        if not _active(st, u, eps):
            continue
        if lazy:
            st.push_lazy(u, omega * st.r[u])
        else:
            st.gp(u, omega * st.cap(u))
        for w in list(adj[u]) + [u]:
            if not inq[w] and _active(st, w, eps):
                q.append(w); inq[w] = True
    return st


def run_scan(adj, alpha, eps, seed, mode='greedy', stop='coord', rng=None,
             lazy=True):
    """Policies that rescan all vertices each op (n is small).
    mode: greedy (max r/d), rand_v, rand_xi, cheap_first, tiny_leaf,
          rand_mix."""
    st = GP(adj, alpha, seed, center=seed)
    rng = rng or random.Random(0)
    while st.ops < OP_CAP:
        if _stopped(st, eps, stop):
            break
        act = [u for u in range(st.n) if _active(st, u, eps)]
        if not act:
            break
        if mode == 'greedy':
            u = max(act, key=lambda v: st.r[v] / st.d[v])
            st.push_lazy(u, st.r[u]) if lazy else st.push_nonlazy_full(u)
        elif mode == 'rand_v':
            u = rng.choice(act)
            st.push_lazy(u, st.r[u]) if lazy else st.push_nonlazy_full(u)
        elif mode == 'rand_xi':
            u = rng.choice(act)
            st.push_lazy(u, rng.uniform(1e-9, 1.0) * st.r[u])
        elif mode == 'rand_mix':
            u = rng.choice(act)
            w = rng.uniform(0.05, 1.0)
            if rng.random() < 0.5:
                st.push_lazy(u, w * st.r[u])
            else:
                st.gp(u, w * st.cap(u))
        elif mode == 'cheap_first':
            leaves = [u for u in act if u != st.center]
            u = leaves[0] if leaves else st.center
            st.push_nonlazy_full(u)
        elif mode in ('jacobi', 'jacobi_nonlazy'):
            # variant (v): simultaneous batched full pushes on the active
            # snapshot; each op stays feasible (removal <= snapshot <= r).
            snap = st.r[:]
            for u in act:
                if _stopped(st, eps, stop):
                    break
                if mode == 'jacobi':
                    st.push_lazy(u, snap[u])
                else:
                    st.gp(u, 2.0 * snap[u] / (1.0 + st.alpha))
        elif mode == 'tiny_leaf':
            leaves = [u for u in act if u != st.center]
            if leaves:
                u = max(leaves, key=lambda v: st.r[v])
                st.push_lazy(u, min(st.r[u], eps / 10.0))
            else:
                st.push_lazy(st.center, st.r[st.center])
        else:
            raise ValueError(mode)
    return st


# ---------- non-member: signed GS-SOR sweeps ----------

def run_sor(adj, alpha, eps, seed, omega, target='err', skip_tol=0.0):
    """Sweep order: center then all leaves. Oracle stop:
       target='err': stop when semantic err(p) <= eps (checked per sweep).
       Records first sweep where l1(r) <= eps*vol too (may never happen)."""
    st = GP(adj, alpha, seed, center=seed)
    M = pr_matrix(adj, alpha)
    e = np.zeros(st.n); e[seed] = 1.0
    pi = pr_vec(adj, alpha, e, M)
    order = [seed] + [u for u in range(st.n) if u != seed]
    W_at_l1 = None
    sweeps = 0
    while sweeps < 200000:
        for u in order:
            if abs(st.r[u]) > skip_tol:
                st.sor_step(u, omega)
        sweeps += 1
        st.max_l1_seen = max(st.max_l1_seen, st.l1_r())
        if W_at_l1 is None and st.l1_r() <= eps * st.vol:
            W_at_l1 = st.W
        if st.err_sem(pi) <= eps:
            break
    st.sweeps = sweeps
    st.W_at_l1 = W_at_l1
    st.pi = pi
    return st


def omega_opt(alpha):
    ca = (1 - alpha) / (1 + alpha)
    return 2.0 / (1.0 + math.sqrt(1.0 - ca * ca))
