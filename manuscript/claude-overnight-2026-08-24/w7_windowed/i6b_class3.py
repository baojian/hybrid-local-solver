"""I4-A HALF 2: the  mu_2 >= 2q  CLASS THEOREM for general connected graphs.

Everything below is EXACT rational arithmetic (Fractions).  No eigenvector is
ever computed: the whole modal chain is rewritten with the rational operator

      Mm := kappa (kappa D + Qt)^{-1} D            (= "m(M)", D-self-adjoint)
      P_op := (1+beta) Mm ,   S_op := beta Mm

whose eigenvalues on the k-th normalized-Laplacian mode are exactly
m_k = kappa/(kappa+lam_k), p_k = m_k(1+beta), s_k = m_k beta.  Hence the
Lyapunov form

      V(u,v) := <u,u>_D - <u, P_op v>_D + <v, S_op v>_D
              = sum_k [ h_k^2 - p_k h_k h_k^- + s_k (h_k^-)^2 ]

is computable in Fractions and is *automatically* the per-mode sum with each
mode's own (p_k, s_k).  Likewise the exact N-stage decay identity is

      V(h_{t+1}, h_t) = VS(h_t, h_{t-1}),
      VS(u,v) := <u,S_op u>_D - <u, S_op P_op v>_D + <v, S_op S_op v>_D
               = sum_k s_k V_k ,

which gives  V_{t+1} <= s_2 V_t  with no eigen-decomposition at all.

Spectral constants are CERTIFIED by exact rational positive-definiteness tests
(LDL^T with rational pivots), not by floating eigensolvers:
   mu_2 > theta   <=>   L - theta D + ((theta+1)/vol) d d^T  is PD
   mu_max < theta <=>   theta D - L                          is PD
(the first identity: on d^perp the added rank-one vanishes, on span{1} it
contributes vol > 0).
"""
import sys, json, math, time, itertools
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import complete_graph, path_graph, star_graph, _gauss

KEYS = ('C1_master', 'C2_Fcollapse', 'C3_Nlinear', 'C4_Vdecay', 'C5_oscil',
        'C6_trigger', 'C7_defect', 'C8_philb', 'C9_Vcontract', 'C10_lowfloor',
        'C11_monotone', 'C12_struct', 'C13_absorb', 'C14_Rgeom',
        'C15_corrclass', 'C16_Fcontract', 'C17_Pcert', 'C9s_corr',
        'S1_cauchy', 'S2_lyaplb', 'S3_trigimp')


# ------------------------------------------------------------------ graphs
def _mk(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if v not in adj[u]:
            adj[u].append(v); adj[v].append(u)
    return [sorted(a) for a in adj]


def complete_bipartite(a, b):
    return _mk(a + b, [(i, a + j) for i in range(a) for j in range(b)])


def hypercube(k):
    n = 1 << k
    return _mk(n, [(i, i ^ (1 << b)) for i in range(n) for b in range(k)
                   if i < (i ^ (1 << b))])


def petersen():
    E = [(i, (i + 1) % 5) for i in range(5)] + \
        [(i, 5 + i) for i in range(5)] + \
        [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    return _mk(10, E)


def rook(m):                      # K_m [] K_m, SRG(m^2, 2m-2, m-2, 2)
    E = []
    for r in range(m):
        for c1 in range(m):
            for c2 in range(c1 + 1, m):
                E.append((r * m + c1, r * m + c2))
                E.append((c1 * m + r, c2 * m + r))
    return _mk(m * m, E)


def cocktail(m):                  # K_{2m} minus a perfect matching
    E = [(i, j) for i in range(2 * m) for j in range(i + 1, 2 * m)
         if j != i + m or i >= m]
    return _mk(2 * m, E)


def cycle(n):
    return _mk(n, [(i, (i + 1) % n) for i in range(n)])


def circulant(n, offs):
    return _mk(n, [(i, (i + o) % n) for i in range(n) for o in offs])


def er_dense(n, p, rs):
    st = rs
    E = []
    for i in range(n):
        for j in range(i + 1, n):
            st = (1103515245 * st + 12345) % (1 << 31)
            if (st >> 8) % 1000 < int(p * 1000):
                E.append((i, j))
    adj = _mk(n, E)
    return adj if all(adj[i] for i in range(n)) else None


def connected(adj):
    n = len(adj); seen = {0}; st = [0]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); st.append(v)
    return len(seen) == n


# ------------------------------------------------ certified rational spectra
def _pd(Mrows):
    """Exact rational LDL^T without pivoting: True iff M is symmetric PD."""
    n = len(Mrows)
    A = [row[:] for row in Mrows]
    for k in range(n):
        if A[k][k] <= 0:
            return False
        piv = A[k][k]
        for i in range(k + 1, n):
            f = A[i][k] / piv
            if f == 0:
                continue
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return True


def mu2_gt(adj, theta):
    n = len(adj)
    d = [Fr(len(adj[i])) for i in range(n)]
    vol = sum(d)
    c = (theta + 1) / vol
    M = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = d[i] - theta * d[i]
        for j in adj[i]:
            M[i][j] -= 1
    for i in range(n):
        for j in range(n):
            M[i][j] += c * d[i] * d[j]
    return _pd(M)


def mumax_lt(adj, theta):
    n = len(adj)
    M = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = theta * Fr(len(adj[i])) - Fr(len(adj[i]))
        for j in adj[i]:
            M[i][j] += 1
    return _pd(M)


def bracket(pred, lo, hi, iters=26):
    """pred(x) monotone True below the root; returns (lo, hi) with
    pred(lo) True, pred(hi) False, hi-lo <= (hi0-lo0)/2^iters."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if pred(mid):
            lo = mid
        else:
            hi = mid
    return lo, hi


def spectral_bracket(adj, iters=26):
    """Certified rational (mu2_lo, mu2_hi, mumax_lo, mumax_hi)."""
    l2, h2 = bracket(lambda th: mu2_gt(adj, th), Fr(0), Fr(2), iters)
    lM, hM = bracket(lambda th: not mumax_lt(adj, th), Fr(0), Fr(2), iters)
    return l2, h2, lM, hM


# ------------------------------------------------------- exact interior engine
class GenInst:
    """Exact general-graph instance under (H0): ct > 0, so x* is interior and
    every obstacle solve degenerates to the SAME linear solve with
    H = Qt + kappa D.  H^{-1} is formed once, exactly; positivity of every
    iterate is asserted so the linear branch is certified."""

    def __init__(self, adj, seed, q, rho, mu2=None, mumax=None):
        self.adj = adj
        self.n = n = len(adj)
        self.d = d = [Fr(len(adj[i])) for i in range(n)]
        self.vol = sum(d)
        self.dmin = min(d)
        self.q = q = Fr(q)
        self.alpha = al = q * q / (1 + q * q)
        self.rho = rho = Fr(rho)
        self.kappa = kap = 1 - 2 * al
        self.beta = be = (1 - q) / (1 + q)
        self.mu = kap * al / (al + kap)
        a2, c2 = (1 - al) / 2, (1 + al) / 2
        self.Qt = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            self.Qt[i][i] = c2 * d[i]
            for j in adj[i]:
                self.Qt[i][j] -= a2
        self.s = [Fr(x) for x in seed]
        assert sum(self.s) == 1
        self.ct = [al * self.s[i] - al * rho * d[i] for i in range(n)]
        self.H0 = all(c > 0 for c in self.ct)            # hypothesis (H0)
        # exact inverses
        self.Qinv = self._inv(self.Qt)
        self.Hinv = self._inv([[self.Qt[i][j] + (kap * d[i] if i == j else 0)
                                for j in range(n)] for i in range(n)])
        self.xstar = self._mv(self.Qinv, self.ct)
        self.interior = all(v > 0 for v in self.xstar)
        # Mm = kappa Hinv D  (rational, D-self-adjoint)
        self.Mm = [[kap * self.Hinv[i][j] * d[j] for j in range(n)]
                   for i in range(n)]
        # spectral constants (certified rational bounds)
        self.mu2 = mu2
        self.mumax = mumax
        self.m0 = kap / (kap + al)

    def _inv(self, A):
        n = self.n
        cols = []
        for k in range(n):
            e = [Fr(1) if i == k else Fr(0) for i in range(n)]
            cols.append(_gauss([r[:] for r in A], e))
        return [[cols[j][i] for j in range(n)] for i in range(n)]

    def _mv(self, A, u):
        n = self.n
        return [sum(A[i][j] * u[j] for j in range(n)) for i in range(n)]

    def Qtv(self, u):
        return self._mv(self.Qt, u)

    def Mmv(self, u):
        return self._mv(self.Mm, u)

    def dotD(self, u, v):
        return sum(self.d[i] * u[i] * v[i] for i in range(self.n))

    def Fval(self, u):
        Qu = self.Qtv(u)
        return Fr(1, 2) * sum(u[i] * Qu[i] for i in range(self.n)) - \
            sum(self.ct[i] * u[i] for i in range(self.n))

    def solveH(self, g):
        return self._mv(self.Hinv, g)

    def run(self, T, diag=True):
        n, al, be, kap, mu, q = (self.n, self.alpha, self.beta, self.kappa,
                                 self.mu, self.q)
        d, ct = self.d, self.ct
        xm = [Fr(0)] * n; x = [Fr(0)] * n
        Fstar = self.Fval(self.xstar)
        cq = (1 + q) / q
        recs, xs = [], [xm[:], x[:]]
        for t in range(T):
            dt = [x[i] - xm[i] for i in range(n)]
            a = [x[i] + be * dt[i] for i in range(n)]
            supp = [i for i in range(n) if a[i] > 0]
            Qta = self.Qtv(a)
            Delta = Fr(0)
            for i in supp:
                z = ct[i] - Qta[i]
                if z < 0:
                    Delta = max(Delta, -z / (al * d[i]))
            r = [min(be * dt[i], Delta) for i in range(n)]
            ell = [a[i] - r[i] for i in range(n)]
            mn = min((be * dt[i] for i in range(n)), default=Fr(0))
            mx = max((be * dt[i] for i in range(n)), default=Fr(0))
            cls = 'N' if Delta == 0 else ('F' if Delta >= mx else
                                          ('C' if Delta <= mn else 'P'))
            ta = [self.xstar[i] - a[i] for i in range(n)]
            rec = dict(t=t, cls=cls, Delta=Delta, r=r, ell=ell, dt=dt, ta=ta,
                       supp=tuple(supp))
            if diag:
                e = [self.xstar[i] - x[i] for i in range(n)]
                zmx = [-e[i] + (1 / q - 1) * dt[i] for i in range(n)]
                Dfin = -2 * cq * self.dotD(r, zmx) + cq ** 2 * self.dotD(r, r)
                pr = self.solveH([ct[i] + kap * d[i] * x[i] for i in range(n)])
                if t >= 1 and any(v <= 0 for v in pr):
                    raise AssertionError('prox left the interior at t=%d' % t)
                pmx = [pr[i] - x[i] for i in range(n)]
                gapE = (self.Fval(pr) - Fstar) + kap / 2 * self.dotD(pmx, pmx)
                Phi = gapE + mu / 2 * self.dotD(zmx, zmx)
                rec.update(Phi=Phi, Dfin=Dfin, e2=self.dotD(e, e))
                rec['gamma'] = (1 + mu * Dfin / (2 * Phi)) if Phi > 0 else Fr(1)
            xn = self.solveH([ct[i] + kap * d[i] * ell[i] for i in range(n)])
            if t >= 1 and any(v <= 0 for v in xn):
                raise AssertionError('iterate left the interior at t=%d' % t)
            recs.append(rec)
            xm, x = x, xn
            xs.append(x[:])
        return recs, xs


def sqrt_ub(X):
    if X == 0:
        return Fr(0)
    S = 10 ** 20
    r = math.isqrt(X.numerator * S * S * X.denominator) // X.denominator + 1
    u = Fr(r, S)
    assert u * u >= X
    return u


# ------------------------------------------------------------- the predicates
def analyse(name, adj, seed, q, rho, T, brk=None, mu2_exact=None):
    n = len(adj)
    I = GenInst(adj, seed, q, rho)
    al, be, kap, mu, d = I.alpha, I.beta, I.kappa, I.mu, I.d
    vol, dmin, m0 = I.vol, I.dmin, I.m0
    aq = (1 - q) / q
    if brk is None:
        brk = spectral_bracket(adj)
    mu2_lo, mu2_hi, muM_lo, muM_hi = brk
    if mu2_exact is not None:
        assert mu2_lo <= mu2_exact <= mu2_hi, (name, mu2_lo, mu2_exact, mu2_hi)
        mu2_lo = mu2_hi = mu2_exact
    # certified: lam2 >= lam2_lo, lamMax <= lamM_hi
    lam2_lo = al + (1 - al) * mu2_lo / 2
    lamM_hi = al + (1 - al) * muM_hi / 2
    m2_ub = kap / (kap + lam2_lo)          # >= m_2
    m2_lb = kap / (kap + al + (1 - al) * mu2_hi / 2)   # <= m_2
    s2_ub = m2_ub * be                     # >= s_2
    mM_lb = kap / (kap + lamM_hi)          # <= m_n
    smin_lb = mM_lb * be                   # <= s_n
    C_gen = (1 + be) ** 2 + be * be / smin_lb          # >= C_ta of every mode
    dn_gen = (1 - m2_ub / m0) / 2                      # <= dn of every mode
    wh2 = dmin * (al * be / lamM_hi) ** 2              # <= true constant
    res = dict(name=name, n=n, q=str(q), rho=str(rho), T=T,
               mu2_lo=str(mu2_lo), mu2_hi=str(mu2_hi), twoq=str(2 * q),
               in_class=bool(mu2_lo >= 2 * q), H0=I.H0, interior=I.interior,
               dmin=str(dmin), muM_hi=str(muM_hi),
               checks={k: [0, 0] for k in KEYS}, fails=[])
    ck = res['checks']

    def tick(k, ok, info=''):
        ck[k][1] += 1
        if ok:
            ck[k][0] += 1
        elif len(res['fails']) < 24:
            res['fails'].append((k, info))

    # ---- instance-level structure -----------------------------------------
    tick('C12_struct', connected(adj) and m0 == 1 - q * q and
         s2_ub <= (1 - q) ** 2 and (m2_ub * (1 + be)) ** 2 < 4 * s2_ub,
         's2=%s' % s2_ub)
    tick('C16_Fcontract', s2_ub * (2 - m2_ub) <= (1 - q) ** 2,
         'ratio=%.6f' % float(s2_ub * (2 - m2_ub) / (1 - q) ** 2))
    res['C16_ratio'] = float(s2_ub * (2 - m2_ub) / (1 - q) ** 2)
    res['C16_pred_mu2_ge_2q'] = bool(mu2_lo >= 2 * q)
    res['C16_agree'] = bool((s2_ub * (2 - m2_ub) <= (1 - q) ** 2) ==
                            (mu2_lo >= 2 * q))
    if not (I.H0 and I.interior):
        res['skipped'] = 'H0/interior violated'
        return res, None, I
    recs, xs = I.run(T)
    word = ''.join(r['cls'] for r in recs)
    res['word'] = word

    def split(u):                       # D-orthogonal low/high split
        L = sum(d[i] * u[i] for i in range(n)) / vol
        return L, [u[i] - L for i in range(n)]

    def Vform(u, v):                    # <u,u>_D - <u,P_op v>_D + <v,S_op v>_D
        Mv = I.Mmv(v)
        return I.dotD(u, u) - (1 + be) * I.dotD(u, Mv) + be * I.dotD(v, Mv)

    def VSform(u, v):                   # = sum_k s_k V_k
        # S_op = be Mm, P_op = (1+be) Mm, Mm D-self-adjoint:
        #   <u,S_op u>_D      = be <u, Mm u>_D
        #   <u,S_op P_op v>_D = be(1+be) <Mm u, Mm v>_D
        #   <v,S_op S_op v>_D = be^2 <Mm v, Mm v>_D
        Mu, Mv = I.Mmv(u), I.Mmv(v)
        return (be * I.dotD(u, Mu) - be * (1 + be) * I.dotD(Mu, Mv)
                + be * be * I.dotD(Mv, Mv))

    E = [[I.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    Vs, Ls, Ws = {}, {}, {}
    for t in range(1, len(xs) - 1):
        Lm, hm = split(E[t]); L, h = split(E[t + 1])
        Vs[t] = Vform(h, hm)
        Ws[t] = I.dotD(h, h) + be * I.dotD(hm, I.Mmv(hm))
        Ls[t] = (Lm, L)
    t_abs = None
    mxa = None
    for t in range(1, T - 1):
        em, e, en = E[t], E[t + 1], E[t + 2]
        Lm, hm = split(em); L, h = split(e); Ln, hn = split(en)
        rec = recs[t]
        r, ell, dt, ta = rec['r'], rec['ell'], rec['dt'], rec['ta']
        Delta, cls = rec['Delta'], rec['cls']
        # C1 master identity
        Qen = I.Qtv(en)
        tick('C1_master', all(Qen[i] + kap * d[i] * en[i] ==
                              kap * d[i] * (I.xstar[i] - ell[i])
                              for i in range(n)))
        Mme = I.Mmv(e)
        if cls == 'F':
            tick('C2_Fcollapse', ell == xs[t + 1] and en == Mme)
        if cls == 'N':
            tick('C3_Nlinear', all(v == 0 for v in r) and en == I.Mmv(ta))
        if cls in ('N', 'C'):
            # clean stages have P_h r = 0, so the HIGH recurrence is the N one
            tick('C4_Vdecay', Vs[t + 1] == VSform(h, hm),
                 't=%d cls=%s' % (t, cls))
        # C5 L-E, D-weighted, full-graph geometry (interior face => w = 1)
        _, rh = split(r); _, dh = split(dt)
        tick('C5_oscil', I.dotD(rh, rh) <= be * be * I.dotD(dh, dh))
        # C6 trigger characterisation  al*Delta = max_i [-(M ta)_i]_+
        Qta = I.Qtv(ta)
        mm = max(max((-Qta[i] / d[i] for i in range(n)), default=Fr(0)), Fr(0))
        tick('C6_trigger', mm == al * Delta)
        # C7/C8
        e2m = I.dotD(em, em); e2 = I.dotD(e, e)
        tick('C7_defect', rec['Dfin'] <= aq * (e2m - e2))
        tick('C8_philb', 2 * rec['Phi'] >= mu * e2)
        # C9 closing
        V, Vn = Vs[t], Vs[t + 1]
        if V > 0:
            tick('C9_Vcontract', Vn <= (1 - q) ** 2 * V,
                 't=%d cls=%s ratio=%.6f' % (t, cls, float(Vn / V)))
            rt = Vn / V
            mxa = rt if mxa is None else max(mxa, rt)
            if cls in ('N', 'C'):
                tick('C14_Rgeom', Vn <= s2_ub * V, 't=%d %s' % (t, cls))
        else:
            tick('C9_Vcontract', Vn <= 0)
        # C10 / C11
        tick('C10_lowfloor', L >= (1 - q) * Lm and L > 0)
        tick('C11_monotone', all(v >= 0 for v in dt) and all(v >= 0 for v in e))
        # C15 census + REPAIRED C17'/C9s from the clip identity (I6-B):
        #   V_{t+1} = VF + |Mm phih|^2 - (1-be)<Mm h, Mm phih>,
        #   VF = be<h,Mm(I-Mm)h>,  phih = P(be*d - Delta)_+,
        #   co = hm - ((1+be)/(2be))h,  vh = be*co + nu*h,  nu = q/(1+q).
        # Route A (valid iff TK := <Mm phih, Mm(vh-phih)> >= 0, proved
        #   under (H-K)):  V_{t+1} <= VF - |Mm phih|^2 + 2be<Mm phih,Mm co>
        #                          <= VF + be^2 |Mm co|^2.
        # Route B (unconditional): V_{t+1} <= VF + m2lb^2*(-|phih|^2)
        #   + 2be*m2ub^2*|co||phih| + (1-be)*sqrt(spread_h*spread_phi).
        if cls != 'N':
            tick('C15_corrclass', True, '')    # census only (I6-B)
            res.setdefault('corrclass', []).append(cls)
            nu = q / (1 + q)
            phiv = [max(be * dt[i] - Delta, Fr(0)) for i in range(n)]
            _, phih = split(phiv)
            co = [hm[i] - (1 + be) / (2 * be) * h[i] for i in range(n)]
            Mh, Mphi, Mco = I.Mmv(h), I.Mmv(phih), I.Mmv(co)
            H2 = I.dotD(h, h); m2v = I.dotD(phih, phih)
            X2 = I.dotD(co, co)
            MH2 = I.dotD(Mh, Mh); Mm2v = I.dotD(Mphi, Mphi)
            MX2 = I.dotD(Mco, Mco)
            VF = be * (I.dotD(h, Mh) - MH2)
            tgt = (1 - q) ** 2 * V
            vh = [be * co[i] + nu * h[i] for i in range(n)]
            TK = I.dotD(Mphi, I.Mmv(vh)) - Mm2v
            UApr = VF + be * be * MX2
            okA = bool(TK >= 0 and UApr <= tgt)
            tick('C9s_corr', TK >= 0 and Vs[t + 1] <= UApr,
                 't=%d cls=%s TK>=0:%s' % (t, cls, bool(TK >= 0)))
            if cls == 'P':
                UAex = VF - Mm2v + 2 * be * I.dotD(Mphi, Mco)
                sph = max(m2_ub * m2_ub * H2 - MH2, Fr(0))
                spp = max(m2_ub * m2_ub * m2v - Mm2v, Fr(0))
                UB = VF - m2_lb * m2_lb * m2v + \
                    2 * be * m2_ub * m2_ub * sqrt_ub(X2 * m2v) + \
                    (1 - be) * sqrt_ub(sph * spp)
                okAe = bool(TK >= 0 and UAex <= tgt)
                okB = bool(UB <= tgt)
                tick('C17_Pcert', okAe or okB,
                     't=%d A:%s B:%s' % (t, okAe, okB))
                res.setdefault('Pcert_ratio', []).append(
                    (float(UAex / tgt) if V else None,
                     float(UB / tgt) if V else None, bool(TK >= 0)))
        # ---- S1/S2/S3: the three steps of the general absorption certificate
        _, tah = split(ta)
        tick('S1_cauchy', I.dotD(tah, tah) <= C_gen * Ws[t],
             't=%d' % t)
        tick('S2_lyaplb', dn_gen * Ws[t] <= V, 't=%d' % t)
        prem = (L >= (1 - q) * Lm and Lm > 0 and
                C_gen * V <= dn_gen * wh2 * Lm * Lm)
        if prem:
            tick('S3_trigimp', Delta == 0, 't=%d Delta=%s' % (t, Delta))
            if t_abs is None:
                t_abs = t
    res['maxVratio'] = float(mxa) if mxa is not None else None
    res['t_abs'] = t_abs
    res['ncorr'] = sum(1 for c in word if c != 'N')
    res['census'] = {c: word.count(c) for c in 'NCPF'}
    if t_abs is not None:
        suffix_N = all(c == 'N' for c in word[t_abs:])
        frozen = all(recs[t]['gamma'] <= 1 for t in range(t_abs, T))
        tick('C13_absorb', suffix_N and frozen,
             'sufN=%s frozen=%s' % (suffix_N, frozen))
        res['J_pre_abs'] = sum(math.log(recs[t]['gamma'])
                               for t in range(t_abs) if recs[t]['gamma'] > 1)
    else:
        tick('C13_absorb', False, 'certificate did not fire in T=%d' % T)
    res['J_total'] = sum(math.log(r['gamma']) for r in recs
                         if r.get('gamma', 1) > 1)
    return res, recs, I


# ------------------------------------------------------------------- battery
def seeds_for(n, dmax, kind):
    if kind == 'unif':
        s = [Fr(1, n)] * n
    elif kind == 'skew':
        s = [Fr(1, 2)] + [Fr(1, 2 * (n - 1))] * (n - 1)
    else:
        ws = [Fr(((7 * i * i + 3 * i + 5) % 11) + 3) for i in range(n)]
        S = sum(ws); s = [w / S for w in ws]
    rho = min(s) / (2 * dmax)
    return s, rho


CASES = []


def add(nm, adj, q, mu2=None, T=None, kinds=('unif', 'skew', 'prand')):
    if adj is None or not connected(adj):
        return
    dmax = max(len(a) for a in adj)
    n = len(adj)
    q = Fr(q)
    T = T or (26 if q <= Fr(1, 10) else 18)
    for k in kinds:
        s, rho = seeds_for(n, dmax, k)
        CASES.append(('%s %s q=%s' % (nm, k, q), adj, s, q, rho, T, mu2))


# ---- in class: mu_2 >= 2q, exact rational mu_2 --------------------------
add('K33', complete_bipartite(3, 3), Fr(1, 10), Fr(1))
add('K24', complete_bipartite(2, 4), Fr(1, 10), Fr(1))
add('K25', complete_bipartite(2, 5), Fr(1, 4), Fr(1))
add('Q3', hypercube(3), Fr(1, 10), Fr(2, 3))
add('Q3', hypercube(3), Fr(1, 4), Fr(2, 3))
add('Q3-eq', hypercube(3), Fr(1, 3), Fr(2, 3))          # mu_2 == 2q exactly
add('Q4', hypercube(4), Fr(1, 10), Fr(1, 2), T=22)
add('Q4-eq', hypercube(4), Fr(1, 4), Fr(1, 2), T=18)    # mu_2 == 2q exactly
add('Pet', petersen(), Fr(1, 10), Fr(2, 3))
add('Pet', petersen(), Fr(1, 4), Fr(2, 3))
add('Rook3', rook(3), Fr(1, 10), Fr(3, 4))
add('Cock4', cocktail(4), Fr(1, 10), Fr(1))
add('Cock3', cocktail(3), Fr(1, 4), Fr(1))
add('C6', cycle(6), Fr(1, 10), Fr(1, 2))
add('C6-eq', cycle(6), Fr(1, 4), Fr(1, 2))              # mu_2 == 2q exactly
add('C4', cycle(4), Fr(1, 10), Fr(1))
add('K8', complete_graph(8), Fr(1, 10), Fr(8, 7))       # K_n regression
add('K5', complete_graph(5), Fr(1, 4), Fr(5, 4))
# ---- in class, irrational mu_2: certified bracket only ------------------
add('Circ12(1,2,3)', circulant(12, (1, 2, 3)), Fr(1, 20), None, T=30)
add('ER12p70', er_dense(12, 0.70, 12345), Fr(1, 20), None, T=30,
    kinds=('unif', 'prand'))
add('ER14p60', er_dense(14, 0.60, 777), Fr(1, 20), None, T=30,
    kinds=('unif', 'prand'))
# ---- boundary: just BELOW the threshold  mu_2 < 2q ----------------------
add('Q4-below', hypercube(4), Fr(1, 4) + Fr(1, 200), Fr(1, 2), T=18)
add('Q3-below', hypercube(3), Fr(1, 3) + Fr(1, 300), Fr(2, 3), T=18)
add('C6-below', cycle(6), Fr(1, 4) + Fr(1, 200), Fr(1, 2), T=18)
add('Pet-below', petersen(), Fr(1, 3) + Fr(1, 300), Fr(2, 3), T=18)
add('P8-below', path_graph(8), Fr(1, 10), None, T=26)
add('C12-below', cycle(12), Fr(1, 10), None, T=26)
add('S8-below', star_graph(8), Fr(1, 10), Fr(1), T=26)


if __name__ == '__main__':
    t0 = time.time()
    out = []
    agg = {k: [0, 0] for k in KEYS}
    aggIn = {k: [0, 0] for k in KEYS}
    brkcache = {}
    # reuse the certified spectral brackets computed by i4a_half2 (by name)
    try:
        _old = {r['name']: r for r in json.load(
            open('/home/claude/work/overnight/w7_windowed/i4a_half2.json'))}
    except Exception:
        _old = {}
    print('=== I6-B: class battery rerun with repaired C17 (exact) ===')
    hdr = ('%-26s %3s %-9s %-9s %-5s %-6s %5s %-7s %6s' %
           ('case', 'n', 'mu2_lo', '2q', 'class', 'word', 't_abs', 'C16', 'J'))
    print(hdr)
    for (nm, adj, seed, q, rho, T, mu2) in CASES:
        key = id(adj)
        if key not in brkcache:
            if nm in _old and 'mu2_lo' in _old[nm]:
                o = _old[nm]
                brkcache[key] = (Fr(o['mu2_lo']), Fr(o['mu2_hi']), Fr(0),
                                 Fr(o['muM_hi']))
            else:
                brkcache[key] = spectral_bracket(adj)
        try:
            res, recs, I = analyse(nm, adj, seed, q, rho, T,
                                   brk=brkcache[key], mu2_exact=mu2)
        except AssertionError as ex:
            print('%-26s EXIT %s' % (nm, ex)); continue
        out.append(res)
        for k in KEYS:
            agg[k][0] += res['checks'][k][0]; agg[k][1] += res['checks'][k][1]
            if res['in_class']:
                aggIn[k][0] += res['checks'][k][0]
                aggIn[k][1] += res['checks'][k][1]
        print('%-26s %3d %-9.6f %-9.6f %-5s %-6s %5s %-7s %6.4f' %
              (res['name'], res['n'], float(Fr(res['mu2_lo'])),
               float(Fr(res['twoq'])), 'IN' if res['in_class'] else 'out',
               res.get('word', '-')[:6], res.get('t_abs'),
               'ok' if res['checks']['C16_Fcontract'][0] else 'FAIL',
               res.get('J_total', 0.0)))
    print('\n--- aggregate over ALL %d instances / IN-CLASS only ---' % len(out))
    for k in KEYS:
        a, b = agg[k]; c, e = aggIn[k]
        print('  %-15s all %6d/%-6d %-4s   in-class %6d/%-6d %s' %
              (k, a, b, 'PASS' if a == b else 'FAIL', c, e,
               'PASS' if c == e else 'FAIL'))
    inc = [r for r in out if r['in_class']]
    outc = [r for r in out if not r['in_class']]
    print('\nin-class %d, out-of-class %d' % (len(inc), len(outc)))
    print('absorption fired: in-class %d/%d, out-of-class %d/%d' %
          (sum(1 for r in inc if r.get('t_abs') is not None), len(inc),
           sum(1 for r in outc if r.get('t_abs') is not None), len(outc)))
    if inc:
        print('max t_abs in class: %s ; max J_total in class: %.5f (%s)' %
              (max(r.get('t_abs') or -1 for r in inc),
               max(r.get('J_total', 0) for r in inc),
               max(inc, key=lambda r: r.get('J_total', 0))['name']))
        print('worst C9 V-ratio in class: %.6f' %
              max(r['maxVratio'] for r in inc if r.get('maxVratio')))
    print('\nC16 agreement with the mu_2>=2q predicate: %d/%d' %
          (sum(1 for r in out if r['C16_agree']), len(out)))
    bad = [r for r in out if r['fails']]
    print('instances with a failed predicate: %d' % len(bad))
    for r in bad[:14]:
        print('   %-26s %s' % (r['name'], r['fails'][:3]))
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i6b_class3.json', 'w'), indent=1, default=str)
    print('\n[%.1fs] saved i6b_class3.json' % (time.time() - t0))
