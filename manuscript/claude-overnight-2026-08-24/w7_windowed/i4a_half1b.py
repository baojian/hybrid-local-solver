"""I4-A Half 1 (part b):
 (1) K_n REGRESSION: face-aligned == baseline bit-exactly whenever the active
     face is the whole graph -- and that is a THEOREM, not a measurement:
     Qt 1 = alpha d  =>  Qt^{-1}(D 1) = (1/alpha) 1  =>  w^(k) = 1 for all k.
     Verified bit-exactly on K_n cells and on the general-graph interior cells.
 (2) more PROPER-FACE cells (|S*| < n) exercised under both caps.
 (3) WHY absorption still fails on a proper face: the face-Perron mode is
     itself UNDERDAMPED, because beta is calibrated to alpha, not to
     alpha_S > alpha.  m_S = kap/(kap+alpha_S) < m_0 = 1-q^2  =>  the low-mode
     characteristic polynomial z^2 - m_S(1+beta) z + m_S beta has COMPLEX
     roots of modulus sqrt(m_S beta) < 1-q, so no floor L^w_t >= c L^w_{t-1}
     with c > 0 can hold: L-H is false on proper faces for a reason that has
     nothing to do with L-E.
"""
import sys, json, math, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, star_graph, complete_graph
from i3g_core import run_exact, face_w_exact
from i4a_half1 import analyse, line, SAFEKEYS


def caterpillar5(m=5, k=2):
    n = m + m * k
    adj = [[] for _ in range(n)]

    def ae(a, b):
        adj[a].append(b); adj[b].append(a)
    for i in range(m - 1):
        ae(i, i + 1)
    for i in range(m):
        for j in range(k):
            ae(i, m + i * k + j)
    return [sorted(a) for a in adj]


def bit_identical(I, T, k=8):
    rb = run_exact(I, T, mode='base')
    rf = run_exact(I, T, mode='face', k=k)
    if len(rb) != len(rf):
        return False, 'len'
    for a, b in zip(rb, rf):
        if a['Delta'] != b['Delta'] or a['rh'] != b['rh'] or a['xn'] != b['xn']:
            return False, 't=%d' % a['t']
    return True, 'ok'


def face_report(I, T, k=8):
    """Post-lock face constants: alpha_S bracket, m_S vs m_0, damping."""
    q, al, be, kap = I.q, I.alpha, I.beta, I.kappa
    recs = run_exact(I, T, mode='base')
    S = recs[-1]['S']
    w, dv, lo, hi = face_w_exact(I.Qt, I.d, I.adj, list(S), k=k)
    m0 = kap / (kap + al)
    mS_lo = kap / (kap + hi)          # <= m_S
    mS_hi = kap / (kap + lo)          # >= m_S
    disc_hi = (mS_hi * (1 + be)) ** 2 - 4 * mS_hi * be     # sign of disc
    return dict(nS=len(S), alpha=float(al), alS_lo=float(lo), alS_hi=float(hi),
                ratio=float(lo / al), m0=float(m0), mS_lo=float(mS_lo),
                mS_hi=float(mS_hi), underdamped=bool(disc_hi < 0),
                modulus=float((mS_hi * be) ** Fr(1, 2)) if mS_hi * be > 0
                else 0.0, one_minus_q=float(1 - q),
                spread=float(max(w.values()) / min(w.values())))


if __name__ == '__main__':
    t0 = time.time()
    res = {}
    print("=== (1) regression: face-aligned == baseline when S = V ===")
    reg = []
    cases = [
        ('K8 pulse', complete_graph(8),
         [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7, Fr(1, 10),
         Fr(1, 112), 16),
        ('K2 n=100', complete_graph(2), [Fr(1, 2), Fr(1, 2)], Fr(1, 100),
         Fr(1, 16), 20),
        ('K16 unif', complete_graph(16), [Fr(1, 16)] * 16, Fr(1, 10),
         Fr(1, 480), 14),
        ('K32 unif', complete_graph(32), [Fr(1, 32)] * 32, Fr(1, 100),
         Fr(1, 1984), 10),
        ('K8 skew edge', complete_graph(8),
         [Fr(1, 2)] + [Fr(1, 14)] * 7, Fr(1, 400), Fr(9, 10) * Fr(1, 98), 14),
        ('Q3 skew (gen)', [[1, 2, 4], [0, 3, 5], [0, 3, 6], [1, 2, 7],
                           [0, 5, 6], [1, 4, 7], [2, 4, 7], [3, 5, 6]],
         [Fr(1, 2)] + [Fr(1, 14)] * 7, Fr(1, 10), Fr(1, 336), 16),
    ]
    for (nm, adj, seed, q, rho, T) in cases:
        I = Inst(adj, seed, q, rho)
        ok, why = bit_identical(I, T)
        print("  %-16s n=%-3d |S*|=%-3d  face==base bit-exactly: %-5s (%s)"
              % (nm, I.n, len(I.Sstar), ok, why))
        reg.append(dict(name=nm, n=I.n, nS=len(I.Sstar), identical=bool(ok)))
    res['regression'] = reg

    print("\n=== (2) more PROPER-FACE cells, baseline vs face-aligned ===")
    pf = []
    pcases = [
        ('P16 tuned', path_graph(16), [Fr(1)] + [Fr(0)] * 15, Fr(1, 24),
         Fr(1, 32), 250),
        ('P20 tuned', path_graph(20), [Fr(1)] + [Fr(0)] * 19, Fr(1, 32),
         Fr(7, 256), 250),
        ('P12 tuned', path_graph(12), [Fr(1)] + [Fr(0)] * 11, Fr(1, 20),
         Fr(5, 128), 200),
        ('cat5_2', caterpillar5(), [Fr(1)] + [Fr(0)] * 14, Fr(1, 20),
         Fr(5, 128), 200),
        ('S16 leaf', star_graph(16), [Fr(0), Fr(1)] + [Fr(0)] * 14,
         Fr(1, 20), Fr(5, 128), 150),
    ]
    for (nm, adj, seed, q, rho, T) in pcases:
        I = Inst(adj, seed, q, rho)
        if len(I.Sstar) == I.n:
            print("  %-12s |S*|=n (interior) -- skipped as a proper-face cell"
                  % nm); continue
        print("  -- %s  n=%d |S*|=%d" % (nm, I.n, len(I.Sstar)))
        wc = {}
        row = dict(name=nm, n=I.n, nS=len(I.Sstar))
        for (m, k) in (('base', 0), ('face', 8)):
            o, wc = analyse(I, T, m, k=k, wcache=wc, kdiag=8)
            print("     " + line(o))
            row[m] = {kk: v for kk, v in o.items()
                      if kk in ('checks', 'worst', 'ncorr', 'last_corr',
                                'census', 'J_T', 'tface', 'safe')}
        pf.append(row)
    res['properface'] = pf

    print("\n=== (3) why absorption still fails: face-mode damping ===")
    dm = []
    for (nm, adj, seed, q, rho, T) in [
            ('P24 tuned', path_graph(24), [Fr(1)] + [Fr(0)] * 23, Fr(1, 32),
             Fr(65, 4096), 120)] + pcases:
        I = Inst(adj, seed, q, rho)
        if len(I.Sstar) == I.n:
            continue
        r = face_report(I, T)
        r['name'] = nm
        dm.append(r)
        print("  %-12s |S|=%-3d alpha_S/alpha in [%.4f, %.4f]  m_S in "
              "[%.6f,%.6f] vs m_0=%.6f  underdamped=%s  |root|=%.6f vs "
              "1-q=%.6f  spread(w)=%.2f"
              % (nm, r['nS'], r['ratio'], float(r['alS_hi'] / r['alpha']),
                 r['mS_lo'], r['mS_hi'], r['m0'], r['underdamped'],
                 r['modulus'], r['one_minus_q'], r['spread']))
    res['damping'] = dm
    json.dump(res, open('/home/claude/work/overnight/w7_windowed/'
                        'i4a_half1b.json', 'w'), indent=1, default=str)
    print("\n[%.1fs]" % (time.time() - t0))
