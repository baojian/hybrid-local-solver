"""I2-C: exact MODAL engine for K_n (two eigenvalues => O(n) exact solves).

On K_n, D = (n-1)I and M := D^{-1} Qtilde has exactly two eigenvalues:
   M 1 = alpha 1                      (low mode, span{1})
   M h = lam_h h  for h _|_ 1,   lam_h = alpha + (1-alpha)*n/(2(n-1)).
Every obstacle solve in the recurrence is, on the full face, the linear solve
   (M + kap I) u = g   =>  u_L = g_L/(alpha+kap),  u_h = g_h/(lam_h+kap),
so a stage costs O(n) exact rational ops instead of an n^3 Gaussian solve.
Positivity of every solve is asserted, so the linear branch is certified
(if an assertion fires the face assumption is violated and we bail).

Cross-validated bit-exactly against engine.py (the validated reconstruction).
"""
from fractions import Fraction as Fr
import math


class KnModal:
    def __init__(self, n, seed, q, rho, alpha=None):
        self.n = n
        self.q = q = Fr(q)
        self.alpha = al = Fr(alpha) if alpha is not None else q * q / (1 + q * q)
        assert q * q == al / (1 - al)
        self.rho = rho = Fr(rho)
        self.dd = dd = Fr(n - 1)                      # common degree
        self.kappa = kap = 1 - 2 * al
        self.beta = (1 - q) / (1 + q)
        self.mu = kap * al / (al + kap)
        self.lam_h = al + (1 - al) * Fr(n, 2 * (n - 1))
        self.m0 = kap / (kap + al)
        self.mh = kap / (kap + self.lam_h)
        self.p = self.mh * (1 + self.beta)
        self.s = self.mh * self.beta
        self.seed = [Fr(x) for x in seed]
        assert sum(self.seed) == 1 and all(x > 0 for x in self.seed)
        # ctil_i = al*s_i - al*rho*d_i ;  chat = D^{-1} ctil
        self.ctil = [al * self.seed[i] - al * rho * dd for i in range(n)]
        self.chat = [c / dd for c in self.ctil]
        # x* = M^{-1} chat  (valid iff positive)
        cL = sum(self.chat) / n
        ch = [c - cL for c in self.chat]
        self.xstar = [cL / al + ch[i] / self.lam_h for i in range(n)]
        self.fullsupp = all(v > 0 for v in self.xstar)
        self.ctil_pos = all(c > 0 for c in self.ctil)   # hypothesis (H0)

    # ---- modal linear solve of (M+kap) u = g -------------------------------
    def msolve(self, g, kap):
        n = self.n
        gL = sum(g) / n
        return [gL / (self.alpha + kap) +
                (g[i] - gL) / (self.lam_h + kap) for i in range(n)]

    def Mv(self, u):
        n = self.n
        uL = sum(u) / n
        return [self.alpha * uL + self.lam_h * (u[i] - uL) for i in range(n)]

    def dotD(self, u, v):
        return self.dd * sum(a * b for a, b in zip(u, v))

    def Fval(self, u):        # d*(.5 u'Mu - chat'u)
        Mu = self.Mv(u)
        return self.dd * (Fr(1, 2) * sum(a * b for a, b in zip(u, Mu)) -
                          sum(a * b for a, b in zip(self.chat, u)))

    def run(self, T, diag=True):
        n, al, be, kap, mu, q = (self.n, self.alpha, self.beta, self.kappa,
                                 self.mu, self.q)
        xm = [Fr(0)] * n
        x = [Fr(0)] * n
        Fstar = self.Fval(self.xstar)
        cq = (1 + q) / q
        recs, xs = [], [xm[:], x[:]]      # xs[t+1] = x_t
        for t in range(T):
            dt = [x[i] - xm[i] for i in range(n)]
            a = [x[i] + be * dt[i] for i in range(n)]
            supp = [i for i in range(n) if a[i] > 0]
            ta = [self.xstar[i] - a[i] for i in range(n)]   # x* - a_t
            Mta = self.Mv(ta)
            Delta = Fr(0)
            for i in supp:
                if Mta[i] < 0:
                    Delta = max(Delta, -Mta[i] / al)
            r = [min(be * dt[i], Delta) for i in range(n)]
            ell = [a[i] - r[i] for i in range(n)]
            mx = max((be * dt[i] for i in range(n)), default=Fr(0))
            cls = 'N' if Delta == 0 else ('F' if Delta >= mx else 'P')
            rec = dict(t=t, cls=cls, Delta=Delta, r=r, ell=ell, dt=dt, ta=ta)
            if diag:
                e = [self.xstar[i] - x[i] for i in range(n)]
                zmx = [-e[i] + (1 / q - 1) * dt[i] for i in range(n)]
                Dfin = -2 * cq * self.dotD(r, zmx) + cq ** 2 * self.dotD(r, r)
                g = [self.chat[i] + kap * x[i] for i in range(n)]
                pr = self.msolve(g, kap)
                if any(v <= 0 for v in pr):
                    raise AssertionError("prox left the face at t=%d" % t)
                pmx = [pr[i] - x[i] for i in range(n)]
                gapE = (self.Fval(pr) - Fstar) + kap / 2 * self.dotD(pmx, pmx)
                Phi = gapE + mu / 2 * self.dotD(zmx, zmx)
                rec.update(Phi=Phi, Dfin=Dfin, e2=self.dotD(e, e), gapE=gapE)
                rec['gamma'] = (1 + mu * Dfin / (2 * Phi)) if Phi > 0 else Fr(1)
            g = [self.chat[i] + kap * ell[i] for i in range(n)]
            xn = self.msolve(g, kap)
            if t >= 1 and any(v <= 0 for v in xn):
                raise AssertionError("iterate left the face at t=%d" % t)
            xn = [max(v, Fr(0)) for v in xn]
            recs.append(rec)
            xm, x = x, xn
            xs.append(x[:])
        return recs, xs


def J_of(recs, upto=None):
    J = 0.0
    for r in recs[:upto]:
        g = r.get('gamma', Fr(1))
        if g > 1:
            J += math.log(g)
    return J
