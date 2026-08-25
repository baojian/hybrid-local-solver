"""I3-C part 4:
 (a) hunt for genuinely-PARTIAL (P) correction stages on NON-REGULAR graphs and
     compare the three L-E forms there (D-weighted vs Q-weighted vs plain);
 (b) exact-rational verification of the C16 threshold equivalence
        s_k (2 - m_k) <= (1-q)^2     <==>     mu_k >= 2q
     (mu_k = normalized-Laplacian eigenvalue, lam_k = alpha+(1-alpha)mu_k/2);
 (c) diagnose the C10 (low-mode floor) failure on the P24 tuned-rho cell.
"""
import sys, math, json, itertools
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
import numpy as np
from engine import Inst, path_graph, star_graph, complete_graph
from i3c_transfer import caterpillar, doublestar, barbell, rtree, rer

rng = np.random.default_rng(4242)

# ---------------------------------------------------------------- (b) first
print("=== (b) EXACT check of  C16  <=>  mu_k >= 2q ===")
bad = 0; tot = 0; eqcases = 0
for qn, qd in [(1, 4), (1, 8), (1, 10), (1, 16), (1, 32), (1, 100), (3, 10),
               (1, 2), (2, 5), (1, 3), (1, 400), (7, 20)]:
    q = Fr(qn, qd); al = q * q / (1 + q * q); kap = 1 - 2 * al
    be = (1 - q) / (1 + q)
    for mn, md in [(0, 1), (1, 1000), (1, 100), (1, 50), (1, 20), (1, 10),
                   (1, 5), (1, 4), (1, 3), (1, 2), (2, 3), (1, 1), (5, 4),
                   (3, 2), (7, 4), (2, 1), (1, 16), (1, 8), (1, 64), (3, 100),
                   (1, 6), (1, 7), (2, 25), (1, 12), (1, 40)]:
        mu = Fr(mn, md)
        lam = al + (1 - al) * mu / 2
        m = kap / (kap + lam); s = m * be
        lhs = s * (2 - m) <= (1 - q) ** 2
        rhs = mu >= 2 * q
        tot += 1
        if lhs != rhs: bad += 1; print("   MISMATCH q=%s mu=%s" % (q, mu))
        if mu == 2 * q: eqcases += 1
        # also the C12 pair
        assert (s <= (1 - q) ** 2) == (lam >= al) == (mu >= 0)
        assert ((m * (1 + be)) ** 2 < 4 * s) == (lam > al) == (mu > 0)
print("   %d/%d exact (q,mu) pairs agree; %d boundary cases mu=2q "
      "(equality both sides)" % (tot - bad, tot, eqcases))
# boundary: verify equality holds exactly at mu = 2q
for qn, qd in [(1, 4), (1, 10), (1, 32), (1, 100)]:
    q = Fr(qn, qd); al = q * q / (1 + q * q); kap = 1 - 2 * al
    be = (1 - q) / (1 + q); mu = 2 * q
    lam = al + (1 - al) * mu / 2; m = kap / (kap + lam); s = m * be
    print("   q=%-7s mu=2q: m_k=%s == 1-q ? %s ;  s(2-m) - (1-q)^2 = %s"
          % (q, m, m == 1 - q, s * (2 - m) - (1 - q) ** 2))

# ---------------------------------------------------------------- (a)
print("\n=== (a) hunt for genuinely-partial (P) stages on non-regular graphs ===")
def graphs():
    G = [('P6', path_graph(6)), ('P8', path_graph(8)), ('S6', star_graph(6)),
         ('S8', star_graph(8)), ('cat3_2', caterpillar(3, 2)),
         ('dstar1_5', doublestar(1, 5)), ('dstar2_4', doublestar(2, 4)),
         ('barbell3', barbell(3))]
    for rs in range(4): G.append(('rtree8_%d' % rs, rtree(8, rs)))
    for rs in range(3): G.append(('rer8_%d' % rs, rer(8, 0.3, rs)))
    return G

def seeds(n, k):
    out = [[Fr(1, n)] * n]
    for i in range(min(n, 3)):
        s = [Fr(0)] * n; s[i] = Fr(1); out.append(s)
    for _ in range(k):
        w = [Fr(int(rng.integers(1, 30))) for _ in range(n)]
        tw = sum(w); out.append([x / tw for x in w])
    return out

found = []
tested = 0
for nm, adj in graphs():
    n = len(adj)
    for sd in seeds(n, 8):
        for rnum, rden in [(1, 200), (1, 400), (1, 800), (3, 1000), (1, 120),
                           (7, 1000)]:
            for q in (Fr(1, 20), Fr(1, 8)):
                rho = Fr(rnum, rden)
                try:
                    I = Inst(adj, sd, q, rho)
                except Exception:
                    continue
                tested += 1
                al, be, kap = I.alpha, I.beta, I.kappa
                d = I.d; vol = sum(d)
                xm = [Fr(0)] * n; x = [Fr(0)] * n
                for t in range(10):
                    dt = [x[i] - xm[i] for i in range(n)]
                    a = [x[i] + be * dt[i] for i in range(n)]
                    sa = [i for i in range(n) if a[i] > 0]
                    Delta = Fr(0)
                    for i in sa:
                        z = I.ct[i] - sum(I.Qt[i][j] * a[j] for j in sa)
                        if z < 0: Delta = max(Delta, -z / (al * d[i]))
                    mx = max((be * dt[i] for i in range(n)), default=Fr(0))
                    mn_ = min((be * dt[i] for i in range(n)), default=Fr(0))
                    if Delta > 0 and Delta < mx:
                        r = [min(be * dt[i], Delta) for i in range(n)]
                        # three L-E forms
                        def PD(u):
                            c = sum(d[i] * u[i] for i in range(n)) / vol
                            return [u[i] - c for i in range(n)]
                        def P0(u):
                            c = sum(u) / n
                            return [u[i] - c for i in range(n)]
                        def nD(u): return sum(d[i] * u[i] ** 2 for i in range(n))
                        def nQ(u): return sum(u[i] * I.Qt[i][j] * u[j]
                                              for i in range(n) for j in range(n)
                                              if I.Qt[i][j])
                        def n2(u): return sum(v * v for v in u)
                        Pr, Pd = PD(r), PD(dt); Zr, Zd = P0(r), P0(dt)
                        rD = nD(Pr) / (be * be * nD(Pd)) if nD(Pd) > 0 else Fr(0)
                        rQ = nQ(Pr) / (be * be * nQ(Pd)) if nQ(Pd) > 0 else Fr(0)
                        r0 = n2(Zr) / (be * be * n2(Zd)) if n2(Zd) > 0 else Fr(0)
                        clean = Delta <= mn_
                        found.append(dict(g=nm, t=t, q=str(q), rho=str(rho),
                                          clean=bool(clean), rD=float(rD),
                                          rQ=float(rQ), r0=float(r0),
                                          dr=float(max(d) / min(d))))
                    r = [min(be * dt[i], Delta) for i in range(n)]
                    ell = [a[i] - r[i] for i in range(n)]
                    try:
                        xn = I.obstacle_solve(I.ct, kap, ell, warm=sa or None)
                    except Exception:
                        break
                    xm, x = x, xn
print("   scanned %d instances; found %d correcting stages with Delta<beta*max d"
      % (tested, len(found)))
gp = [f for f in found if not f['clean']]
print("   of which genuinely partial (Delta > beta*min d): %d" % len(gp))
if found:
    print("   worst ratio  D-weighted : %.6f" % max(f['rD'] for f in found))
    print("   worst ratio  Q-weighted : %.6f" % max(f['rQ'] for f in found))
    print("   worst ratio  plain (K_n): %.6f" % max(f['r0'] for f in found))
    viol0 = [f for f in found if f['r0'] > 1 + 1e-12]
    violD = [f for f in found if f['rD'] > 1 + 1e-12]
    print("   plain-form violations in the recurrence: %d ; D-form: %d"
          % (len(viol0), len(violD)))
    for f in sorted(found, key=lambda z: -z['r0'])[:5]:
        print("     %s t=%d q=%s rho=%s clean=%s dr=%.1f  rD=%.5f rQ=%.5f r0=%.5f"
              % (f['g'], f['t'], f['q'], f['rho'], f['clean'], f['dr'],
                 f['rD'], f['rQ'], f['r0']))

# ---------------------------------------------------------------- (c)
print("\n=== (c) P24 tuned-rho: why C10 (low-mode floor) fails ===")
n = 24; adj = path_graph(n)
I = Inst(adj, [Fr(1)] + [Fr(0)] * (n - 1), Fr(1, 32), Fr(65, 4096))
d = I.d; vol = sum(d); al, be, kap, q = I.alpha, I.beta, I.kappa, I.q
print("   |S*|=%d  x*_23 = %s  (node 23 off support)" % (len(I.Sstar), I.xstar[-1]))
xm = [Fr(0)] * n; x = [Fr(0)] * n
Lprev = None
rows = []
for t in range(22):
    dt = [x[i] - xm[i] for i in range(n)]
    a = [x[i] + be * dt[i] for i in range(n)]
    sa = [i for i in range(n) if a[i] > 0]
    Delta = Fr(0)
    for i in sa:
        z = I.ct[i] - sum(I.Qt[i][j] * a[j] for j in sa)
        if z < 0: Delta = max(Delta, -z / (al * d[i]))
    r = [min(be * dt[i], Delta) for i in range(n)]
    ell = [a[i] - r[i] for i in range(n)]
    e = [I.xstar[i] - x[i] for i in range(n)]
    L = sum(d[i] * e[i] for i in range(n)) / vol
    # restricted to S*: the master identity only holds on the support face
    S = I.Sstar
    LS = sum(d[i] * e[i] for i in S) / sum(d[i] for i in S)
    ok = None if Lprev is None else (L >= (1 - q) * Lprev)
    rows.append((t, float(L), float(LS), ok, len(sa), Delta > 0))
    Lprev = L
    xn = I.obstacle_solve(I.ct, kap, ell, warm=sa or None)
    xm, x = x, xn
print("     t   L_t (all nodes)  L_t|S*      L_t>=(1-q)L_{t-1}  |supp a| corr")
for t, L, LS, ok, ns, c in rows:
    print("    %2d   %.10e  %.10e   %-5s          %2d      %s"
          % (t, L, LS, ok, ns, c))
json.dump(dict(pstages=found[:200], p24=[(t, L, LS, ok) for t, L, LS, ok, _, _ in rows]),
          open('/home/claude/work/overnight/w7_windowed/i3c_pstage.json', 'w'),
          indent=1, default=str)
