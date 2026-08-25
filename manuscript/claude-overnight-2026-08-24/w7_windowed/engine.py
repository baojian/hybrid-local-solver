"""W7: model-reconstruction of the safeguarded AESP-CD finite recurrence.

Reconstructed from notes/aesp_cd_l1_rppr sections 02-08, 14, 15 (staged files).
LABEL: model-reconstruction with exact shifted solves (the rounds state exact
shifted solves are valid zero-residual finite outputs on these families).

  Objective F_rho(x) = 0.5<x,Qx> - <b,x> + alpha*rho*||D^{1/2}x||_1,
    Q = alpha I + (1-alpha)/2 L_sym, b = alpha D^{-1/2}s.
  Hat coords xh = D^{-1/2}x keep everything rational:
    Qt = D^{1/2} Q D^{1/2}: diag d_i(1+alpha)/2, offdiag -(1-alpha)/2 A_ij
    ct_i = alpha s_i - alpha rho d_i.  On x>=0: F = .5 xh'Qt xh - ct'xh.
  Params: rational q, alpha = q^2/(1+q^2)  (q = sqrt(alpha/(1-alpha))),
    kappa = 1-2alpha, beta = (1-q)/(1+q), mu_E = kappa*alpha/(alpha+kappa).
  Recurrence (x_{-1}=x_0=0), stage t:
    d_t = x_t - x_{t-1} >= 0 ;  trial a_t = x_t + beta d_t
    zeta(a)_i = c_i - (Q a)_i (lower residual);
    Delta_t = (1/alpha) max_{i in supp(a_t)} [zeta(a)_i]_- / sqrt(d_i)
    retraction (hat): rh_i = min(beta*dh_i, Delta_t);  ell_t = a_t - r_t >= x_t
    x_{t+1} = exact obstacle solve of  min F_rho(z) + kappa/2||z-ell_t||^2
  Correction word: N (Delta=0), F (Delta >= beta*max dh: ell=x_t), P else.
  Diagnostics (sections 14/15):
    z_t = x_t + (1/q-1)(x_t - x_{t-1});
    Dfin_t = -2((1+q)/q)<r_t, z_t - x*> + ((1+q)/q)^2 ||r_t||^2
    Phi_t = [E(x_t)-E(x*)] + (mu_E/2)||z_t - x*||^2,  E = Moreau_kappa env.
    gamma_t = 1 + mu_E*Dfin_t/(2*Phi_t);  J_T = sum_{t<T} log max(1,gamma_t)
    EQ_t = <e_t,Q e_t>;  bank Psi_t^A = Phi_t + (A/q)*EQ_{t-1}.
"""
from fractions import Fraction as Fr
import math

# ---------------- graphs ----------------

def complete_graph(m):
    return [sorted(set(range(m)) - {i}) for i in range(m)]

def path_graph(m):
    return [[j for j in (i - 1, i + 1) if 0 <= j < m] for i in range(m)]

def star_graph(m):  # center 0, m-1 leaves
    return [list(range(1, m))] + [[0] for _ in range(m - 1)]

def disjoint_union(adjs):
    out, off = [], 0
    for a in adjs:
        out += [[v + off for v in nb] for nb in a]
        off += len(a)
    return out

def add_edge(adj, u, v):
    adj = [list(nb) for nb in adj]
    if v not in adj[u]:
        adj[u].append(v); adj[u].sort()
        adj[v].append(u); adj[v].sort()
    return adj

# ---------------- exact rational core ----------------

class Inst:
    """Instance: graph + seed + (q, rho). All Fractions."""
    def __init__(self, adj, seed, q, rho, alpha=None):
        self.adj = adj
        self.n = n = len(adj)
        self.d = [Fr(len(adj[i])) for i in range(n)]
        self.q = q = Fr(q)
        self.alpha = Fr(alpha) if alpha is not None else q * q / (1 + q * q)
        al = self.alpha
        assert q * q == al / (1 - al), "q must equal sqrt(alpha/(1-alpha))"
        self.rho = rho = Fr(rho)
        self.kappa = 1 - 2 * al
        self.beta = (1 - q) / (1 + q)
        self.mu = self.kappa * al / (al + self.kappa)
        # Qt (dense rational), ct
        a = (1 - al) / 2
        c = (1 + al) / 2
        self.Qt = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            self.Qt[i][i] = c * self.d[i]
            for j in adj[i]:
                self.Qt[i][j] -= a
        self.s = [Fr(x) for x in seed]
        assert sum(self.s) == 1 and all(x >= 0 for x in self.s)
        self.ct = [al * self.s[i] - al * rho * self.d[i] for i in range(n)]
        self.xstar = self.obstacle_solve(self.ct, Fr(0), [Fr(0)] * n)
        self.Sstar = [i for i in range(n) if self.xstar[i] > 0]

    # obstacle solve: min .5 xh'(Qt+k D)xh - (ct + k D ellh)'xh  st xh>=0
    def obstacle_solve(self, ct, kap, ellh, warm=None):
        n = self.n
        rhs = [ct[i] + kap * self.d[i] * ellh[i] for i in range(n)]
        P = set(warm) if warm is not None else set(
            i for i in range(n) if rhs[i] > 0)
        if not P:
            P = set(i for i in range(n) if rhs[i] > 0)
        for _ in range(4 * n + 8):
            idx = sorted(P)
            A = [[self.Qt[i][j] + (kap * self.d[i] if i == j else 0)
                  for j in idx] for i in idx]
            b = [rhs[i] for i in idx]
            xs = _gauss(A, b)
            neg = [i for i, v in zip(idx, xs) if v < 0]
            if neg:
                for i in neg:
                    P.discard(i)
                continue
            x = [Fr(0)] * n
            for i, v in zip(idx, xs):
                x[i] = v
            # off-P gradient must be >= 0: (Qt+kD)x - rhs >= 0
            viol = []
            for i in range(n):
                if i in P:
                    continue
                g = -rhs[i]
                for j in idx:
                    g += self.Qt[i][j] * x[j]
                if g < 0:
                    viol.append(i)
            if not viol:
                return x
            P |= set(viol)
        raise RuntimeError("active set did not converge")

    def Fval(self, xh):  # objective on x>=0 (x-units)
        n = self.n
        Qx = [sum(self.Qt[i][j] * xh[j] for j in range(n)) for i in range(n)]
        return Fr(1, 2) * sum(xh[i] * Qx[i] for i in range(n)) - \
            sum(self.ct[i] * xh[i] for i in range(n))

    def dotD(self, u, v):
        return sum(self.d[i] * u[i] * v[i] for i in range(self.n))

    def dotQ(self, u, v):
        n = self.n
        return sum(u[i] * self.Qt[i][j] * v[j]
                   for i in range(n) for j in range(n) if self.Qt[i][j] != 0)

    def run(self, T, bankA=None, collect=True):
        """Exact run for T stages. Returns list of per-stage dicts."""
        n = self.n
        q, al, be, kap, mu = self.q, self.alpha, self.beta, self.kappa, self.mu
        xm = [Fr(0)] * n   # x_{t-1}
        x = [Fr(0)] * n    # x_t
        Fstar = self.Fval(self.xstar)
        out = []
        EQ_prev = None
        for t in range(T):
            dh = [x[i] - xm[i] for i in range(n)]
            ah = [x[i] + be * dh[i] for i in range(n)]
            # residual zeta*sqrt(d) = ct - Qt a  on supp(a)
            supp_a = [i for i in range(n) if ah[i] > 0]
            Delta = Fr(0)
            for i in supp_a:
                zt = self.ct[i] - sum(self.Qt[i][j] * ah[j] for j in supp_a)
                if zt < 0:
                    Delta = max(Delta, -zt / (al * self.d[i]))
            rh = [min(be * dh[i], Delta) for i in range(n)]
            ellh = [ah[i] - rh[i] for i in range(n)]
            mx = max((be * dh[i] for i in range(n)), default=Fr(0))
            cls = 'N' if Delta == 0 else ('F' if Delta >= mx else 'P')
            # diagnostics
            rec = {'t': t, 'cls': cls, 'Delta': Delta,
                   'supp': tuple(i for i in range(n) if x[i] > 0)}
            if collect:
                e = [self.xstar[i] - x[i] for i in range(n)]
                zmx = [-e[i] + (1 / q - 1) * dh[i] for i in range(n)]  # z_t - x*
                cq = (1 + q) / q
                Dfin = -2 * cq * self.dotD(rh, zmx) + cq**2 * self.dotD(rh, rh)
                # envelope gap: prox p(x_t)
                p = self.obstacle_solve(self.ct, kap, x, warm=self.Sstar)
                ep = [self.xstar[i] - p[i] for i in range(n)]
                pmx = [p[i] - x[i] for i in range(n)]
                gapE = (self.Fval(p) - Fstar) + kap / 2 * self.dotD(pmx, pmx)
                Phi = gapE + mu / 2 * self.dotD(zmx, zmx)
                EQ = self.dotQ(e, e)
                rec.update(Phi=Phi, EQ=EQ, e2=self.dotD(e, e), Dfin=Dfin,
                           gapE=gapE)
                rec['gamma'] = (1 + mu * Dfin / (2 * Phi)) if Phi > 0 else Fr(1)
                if bankA is not None and EQ_prev is not None:
                    rec['Psi'] = Phi + Fr(bankA) / q * EQ_prev
                EQ_prev = EQ
            out.append(rec)
            xn = self.obstacle_solve(self.ct, kap, ellh, warm=supp_a or None)
            xm, x = x, xn
        return out


def _gauss(A, b):
    n = len(b)
    A = [row[:] for row in A]
    b = b[:]
    for col in range(n):
        piv = next(i for i in range(col, n) if A[i][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        b[col], b[piv] = b[piv], b[col]
        inv = 1 / A[col][col]
        A[col] = [v * inv for v in A[col]]
        b[col] *= inv
        for i in range(n):
            if i != col and A[i][col] != 0:
                f = A[i][col]
                A[i] = [vi - f * vc for vi, vc in zip(A[i], A[col])]
                b[i] -= f * b[col]
    return b


def Jseq(recs):
    """Cumulative J_T from per-stage records (float)."""
    J, out = 0.0, []
    for r in recs:
        g = float(r['gamma']) if 'gamma' in r else 1.0
        if g > 1:
            J += math.log(g)
        out.append(J)
    return out
