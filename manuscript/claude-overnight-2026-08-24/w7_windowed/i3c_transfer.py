"""I3-C part 3: transfer of the C1-C17 chain to GENERAL graphs.

All checks in the engine's HAT coordinates (xh = D^{-1/2}x), where
   M := D^{-1} Qt  is D-self-adjoint,  M 1 = alpha 1  (slow mode = constants),
   P u := u - (<u,1>_D/vol) 1   (D-orthogonal projector onto 1^perp_D),
   ||u||_D^2 = sum_i d_i u_i^2 ,      <u,v>_Q = u' Qt v.
The engine's retraction rh_i = min(beta dh_i, Delta) is truncation at a
CONSTANT level in these coordinates -- i.e. exactly min(u, Delta*v) in
x-coordinates with v = D^{1/2}1.  Predicates tested EXACTLY (Fractions):
  C1  master identity on the interior face
  C2  F-collapse (ell_t = x_t)
  C5D NEW L-E, D-norm      ||P r||_D   <= beta ||P d||_D
  C5Q NEW L-E, Q-norm      ||P r||_Q   <= beta ||P d||_Q
  C5p OLD (K_n) L-E, plain ||P0 r||_2  <= beta ||P0 d||_2, P0 = I - 11'/n
  C6  trigger identity
  C10 low-mode floor  L_t >= (1-q) L_{t-1} > 0
  C11 monotone d_t >= 0, e_t >= 0
Numeric/analytic: C12 (s_k<=(1-q)^2 iff lam_k>=alpha; p_k^2<4s_k iff lam_k>alpha),
  C16 (s_k(2-m_k)<=(1-q)^2  <=>  mu_k >= 2q), C4 aggregated V-decay.
"""
import sys, math, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
import numpy as np
from engine import Inst, path_graph, star_graph, complete_graph, add_edge

# ------------------------------------------------------------------ graphs
def caterpillar(m, k):
    n = m * (1 + k); adj = [[] for _ in range(n)]
    def ae(a, b): adj[a].append(b); adj[b].append(a)
    for i in range(m - 1): ae(i, i + 1)
    idx = m
    for i in range(m):
        for _ in range(k): ae(i, idx); idx += 1
    return [sorted(a) for a in adj]

def doublestar(a, b):
    n = a + b + 2; adj = [[] for _ in range(n)]
    def ae(u, v): adj[u].append(v); adj[v].append(u)
    ae(0, 1)
    for i in range(2, 2 + a): ae(0, i)
    for i in range(2 + a, n): ae(1, i)
    return [sorted(x) for x in adj]

def barbell(m):
    n = 2 * m + 1; adj = [[] for _ in range(n)]
    def ae(u, v): adj[u].append(v); adj[v].append(u)
    for i in range(m):
        for j in range(i + 1, m): ae(i, j)
    for i in range(m + 1, n):
        for j in range(i + 1, n): ae(i, j)
    ae(m - 1, m); ae(m, m + 1)
    return [sorted(x) for x in adj]

def rtree(n, rs):
    rg = np.random.default_rng(rs); adj = [[] for _ in range(n)]
    for i in range(1, n):
        p = int(rg.integers(0, i)); adj[i].append(p); adj[p].append(i)
    return [sorted(a) for a in adj]

def rer(n, p, rs):
    rg = np.random.default_rng(rs); adj = [[] for _ in range(n)]
    for i in range(n - 1):
        adj[i].append(i + 1); adj[i + 1].append(i)
    for i in range(n):
        for j in range(i + 2, n):
            if rg.random() < p: adj[i].append(j); adj[j].append(i)
    return [sorted(set(a)) for a in adj]

# ------------------------------------------------------------------ harness
def check(name, adj, seed, q, rho, T, alpha=None):
    I = Inst(adj, seed, q, rho, alpha=alpha)
    n, al, be, kap, mu = I.n, I.alpha, I.beta, I.kappa, I.mu
    d, vol = I.d, sum(I.d)
    one = [Fr(1)] * n
    def dotD(u, w): return sum(d[i] * u[i] * w[i] for i in range(n))
    def dotQ(u, w): return sum(u[i] * I.Qt[i][j] * w[j]
                               for i in range(n) for j in range(n) if I.Qt[i][j])
    def P(u):
        c = dotD(u, one) / vol
        return [u[i] - c for i in range(n)]
    def P0(u):
        c = sum(u) / n
        return [u[i] - c for i in range(n)]
    def Mv(u):
        return [sum(I.Qt[i][j] * u[j] for j in range(n)) / d[i] for i in range(n)]
    ck = {k: [0, 0] for k in ('C1', 'C2', 'C5D', 'C5Q', 'C5p', 'C6', 'C10', 'C11')}
    fails = {}
    worst = {'C5D': Fr(0), 'C5Q': Fr(0), 'C5p': Fr(0)}
    # replay
    xm = [Fr(0)] * n; x = [Fr(0)] * n
    word = []; Ls = []; ncorr = 0
    prevL = None
    for t in range(T):
        dt = [x[i] - xm[i] for i in range(n)]
        a = [x[i] + be * dt[i] for i in range(n)]
        supp_a = [i for i in range(n) if a[i] > 0]
        Delta = Fr(0)
        for i in supp_a:
            zt = I.ct[i] - sum(I.Qt[i][j] * a[j] for j in supp_a)
            if zt < 0: Delta = max(Delta, -zt / (al * d[i]))
        r = [min(be * dt[i], Delta) for i in range(n)]
        ell = [a[i] - r[i] for i in range(n)]
        mx = max((be * dt[i] for i in range(n)), default=Fr(0))
        cls = 'N' if Delta == 0 else ('F' if Delta >= mx else 'P')
        word.append(cls)
        if Delta > 0: ncorr += 1
        e = [I.xstar[i] - x[i] for i in range(n)]
        xn = I.obstacle_solve(I.ct, kap, ell, warm=supp_a or None)
        en = [I.xstar[i] - xn[i] for i in range(n)]
        def tick(k, ok, info=None):
            ck[k][1] += 1
            if ok: ck[k][0] += 1
            elif k not in fails: fails[k] = (t, info)
        if t >= 1:
            # C1 master identity (interior face only)
            if all(v > 0 for v in xn) and all(v > 0 for v in I.xstar):
                lhs = [sum(I.Qt[i][j] * en[j] for j in range(n)) + kap * d[i] * en[i]
                       for i in range(n)]
                rhs = [kap * d[i] * (I.xstar[i] - ell[i]) for i in range(n)]
                tick('C1', lhs == rhs)
            if cls == 'F': tick('C2', ell == x)
            # ---- the NEW L-E in three norms
            Pr, Pd = P(r), P(dt)
            nr, nd = dotD(Pr, Pr), dotD(Pd, Pd)
            tick('C5D', nr <= be * be * nd, (float(nr), float(be * be * nd)))
            if nd > 0: worst['C5D'] = max(worst['C5D'], nr / (be * be * nd))
            qr, qd = dotQ(Pr, Pr), dotQ(Pd, Pd)
            tick('C5Q', qr <= be * be * qd, (float(qr), float(be * be * qd)))
            if qd > 0: worst['C5Q'] = max(worst['C5Q'], qr / (be * be * qd))
            P0r, P0d = P0(r), P0(dt)
            n0r = sum(v * v for v in P0r); n0d = sum(v * v for v in P0d)
            tick('C5p', n0r <= be * be * n0d, (float(n0r), float(be * be * n0d)))
            if n0d > 0: worst['C5p'] = max(worst['C5p'], n0r / (be * be * n0d))
            # C6 trigger
            ta = [I.xstar[i] - a[i] for i in range(n)]
            Mta = Mv(ta)
            Dm = max([-Mta[i] for i in supp_a] + [Fr(0)]) / al
            tick('C6', Dm == Delta)
            # C10 low floor, C11 monotone
            L = dotD(e, one) / vol
            if prevL is not None:
                tick('C10', L >= (1 - I.q) * prevL and L > 0, (float(L), float(prevL)))
            prevL = L
            tick('C11', all(v >= 0 for v in dt) and all(v >= 0 for v in e))
        xm, x = x, xn
    # ---------- spectral predicates (numeric) ----------
    A = np.zeros((n, n))
    for i in range(n):
        for j in adj[i]: A[i, j] = 1.0
    dd = A.sum(1); Dm12 = 1 / np.sqrt(dd)
    Ls_ = np.eye(n) - Dm12[:, None] * A * Dm12[None, :]
    mu_ = np.sort(np.linalg.eigvalsh(Ls_))
    fal, fq = float(al), float(I.q)
    lam = fal + (1 - fal) * mu_ / 2
    fk, fb = float(kap), float(be)
    m_k = fk / (fk + lam); s_k = m_k * fb; p_k = m_k * (1 + fb)
    hi = slice(1, n)
    C12a = bool(np.all(s_k[hi] <= (1 - fq) ** 2 + 1e-14))
    C12b = bool(np.all(p_k[hi] ** 2 < 4 * s_k[hi]))
    C16 = bool(np.all(s_k[hi] * (2 - m_k[hi]) <= (1 - fq) ** 2 + 1e-14))
    C16pred = bool(mu_[1] >= 2 * fq - 1e-12)
    return dict(name=name, n=n, q=str(I.q), rho=str(I.rho), nS=len(I.Sstar),
                fullsupp=bool(len(I.Sstar) == n),
                dratio=float(dd.max() / dd.min()), mu2=float(mu_[1]),
                twoq=2 * fq, word=''.join(word), ncorr=ncorr,
                checks={k: v for k, v in ck.items()},
                fails={k: str(v) for k, v in fails.items()},
                worstC5D=float(worst['C5D']), worstC5Q=float(worst['C5Q']),
                worstC5p=float(worst['C5p']),
                C12_s_le=C12a, C12_underd=C12b, C16=C16, C16_pred=C16pred,
                s2_over=float(s_k[1] / (1 - fq) ** 2))

def line(r):
    st = []
    for k in ('C1', 'C2', 'C5D', 'C5Q', 'C5p', 'C6', 'C10', 'C11'):
        a, b = r['checks'][k]
        st.append("%s %d/%d%s" % (k, a, b, "" if a == b else "*FAIL*"))
    print("  %-14s n=%2d dr=%5.1f |S*|=%2d mu2=%.4f 2q=%.4f word=%s" %
          (r['name'], r['n'], r['dratio'], r['nS'], r['mu2'], r['twoq'],
           r['word'][:18]))
    print("      " + "  ".join(st))
    print("      worst ratios: C5D=%.4f C5Q=%.4f C5p=%.4f | C12 s<=(1-q)^2 %s, "
          "underdamped %s | C16 %s (pred mu2>=2q: %s) s2/(1-q)^2=%.4f" %
          (r['worstC5D'], r['worstC5Q'], r['worstC5p'], r['C12_s_le'],
           r['C12_underd'], r['C16'], r['C16_pred'], r['s2_over']))
    if r['fails']: print("      FAILS:", r['fails'])

if __name__ == '__main__':
    out = []
    T = 22
    cases = []
    def unif(n): return [Fr(1, n)] * n
    def ep(n): return [Fr(1)] + [Fr(0)] * (n - 1)
    cases.append(('P8 unif', path_graph(8), unif(8), Fr(1, 20), Fr(1, 200)))
    cases.append(('P12 endpt', path_graph(12), ep(12), Fr(1, 20), Fr(1, 400)))
    cases.append(('S8 unif', star_graph(8), unif(8), Fr(1, 20), Fr(1, 400)))
    cases.append(('S12 center', star_graph(12), [Fr(1)] + [Fr(0)] * 11, Fr(1, 20), Fr(1, 800)))
    cases.append(('S12 leaf', star_graph(12), [Fr(0)] + [Fr(1)] + [Fr(0)] * 10, Fr(1, 20), Fr(1, 800)))
    cases.append(('cat6_2', caterpillar(6, 2), unif(18), Fr(1, 20), Fr(1, 400)))
    cases.append(('cat4_3', caterpillar(4, 3), ep(16), Fr(1, 20), Fr(1, 400)))
    cases.append(('dstar2_8', doublestar(2, 8), unif(12), Fr(1, 20), Fr(1, 400)))
    cases.append(('dstar1_9', doublestar(1, 9), [Fr(1)] + [Fr(0)] * 11, Fr(1, 20), Fr(1, 500)))
    cases.append(('barbell4', barbell(4), unif(9), Fr(1, 20), Fr(1, 300)))
    cases.append(('K6 unif', complete_graph(6), unif(6), Fr(1, 20), Fr(1, 200)))
    for rs in (1, 2, 3, 4):
        cases.append(('rtree10_%d' % rs, rtree(10, rs), unif(10), Fr(1, 20), Fr(1, 400)))
    for rs in (1, 2, 3):
        cases.append(('rer10_%d' % rs, rer(10, 0.25, rs), unif(10), Fr(1, 20), Fr(1, 300)))
    # P24 tuned-rho stress cell (the sharpest known case) - exact, T=22
    cases.append(('P24 tuned', path_graph(24), ep(24), Fr(1, 32), Fr(65, 4096)))
    # a low-degree/high-degree extreme: broom
    br = [[] for _ in range(16)]
    def ae(u, v): br[u].append(v); br[v].append(u)
    for i in range(1, 11): ae(0, i)
    prev = 0
    for i in range(11, 16): ae(prev, i); prev = i
    cases.append(('broom10_5', [sorted(a) for a in br], unif(16), Fr(1, 20), Fr(1, 500)))
    print("=== exact predicate transfer on general graphs (T=%d) ===" % T)
    for nm, adj, sd, q, rho in cases:
        try:
            r = check(nm, adj, sd, q, rho, T)
        except Exception as ex:
            print("  %-14s SKIP (%s)" % (nm, ex)); continue
        out.append(r); line(r)
    # aggregate
    agg = {}
    for r in out:
        for k, (a, b) in r['checks'].items():
            p, q_ = agg.get(k, (0, 0)); agg[k] = (p + a, q_ + b)
    print("\n=== AGGREGATE over %d general-graph instances ===" % len(out))
    for k in ('C1', 'C2', 'C5D', 'C5Q', 'C5p', 'C6', 'C10', 'C11'):
        a, b = agg[k]
        print("   %-4s %5d/%5d  %s" % (k, a, b, "PASS" if a == b else
                                       "FAIL (%d)" % (b - a)))
    print("   worst C5D ratio over all: %.6f" % max(r['worstC5D'] for r in out))
    print("   worst C5Q ratio over all: %.6f" % max(r['worstC5Q'] for r in out))
    print("   worst C5p ratio over all: %.6f  <-- old K_n form" %
          max(r['worstC5p'] for r in out))
    print("   C12 s<=(1-q)^2: %d/%d ; underdamped: %d/%d ; C16: %d/%d ; "
          "C16<=>mu2>=2q agreement: %d/%d" %
          (sum(r['C12_s_le'] for r in out), len(out),
           sum(r['C12_underd'] for r in out), len(out),
           sum(r['C16'] for r in out), len(out),
           sum(r['C16'] == r['C16_pred'] for r in out), len(out)))
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/i3c_transfer.json', 'w'),
              indent=1, default=str)
