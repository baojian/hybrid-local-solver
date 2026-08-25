"""I3-C part 6 (decisive): on a PROPER support face S* the relevant operator is
the principal submatrix M_S = D_S^{-1} Qt_S, whose Perron (bottom) eigenvector
v_S is NOT proportional to D_S^{1/2} 1 and whose bottom eigenvalue alpha_S >
alpha.  The engine's retraction caps at Delta * D^{1/2}1 (x-coords), which is
therefore MISALIGNED with v_S.  Consequences tested:
  (F1) how far is v_S from D_S^{1/2}1  (and alpha_S vs alpha)?
  (F2) does the face-aligned L-E  ||P_{v_S} r|| <= beta ||P_{v_S} d||  hold at
       the actual correcting stages of P24?  (the cap is Delta*D^{1/2}1, so this
       is variant V2 = misaligned cap, which is refutable in general)
  (F3) the face's slow-mode contraction factor vs the critical (1-q):
       m_S = kap/(kap+alpha_S); roots of z^2 - m_S(1+beta) z + m_S beta.
"""
import sys, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
import numpy as np
from fengine import FInst
from engine import path_graph, star_graph
from i3c_transfer import caterpillar

def analyse(name, adj, seed, q, rho, T=400):
    n = len(adj)
    I = FInst(adj, seed, q=q, rho=rho)
    d = I.d; al, be, kap = I.alpha, I.beta, I.kappa
    S = np.array(sorted(I.Sstar.tolist()))
    full = (len(S) == n)
    Qt = I.Qt
    # face operator (symmetric version): Qsym_S = D_S^{-1/2} Qt_S D_S^{-1/2}
    dS = d[S]; Ds12 = 1 / np.sqrt(dS)
    QsS = Ds12[:, None] * Qt[np.ix_(S, S)] * Ds12[None, :]
    w, V = np.linalg.eigh(QsS)
    alS = float(w[0]); vS = V[:, 0]
    if vS.sum() < 0: vS = -vS
    vfull = np.sqrt(dS); vfull = vfull / np.linalg.norm(vfull)
    cosang = float(abs(vS @ vfull))
    mS = kap / (kap + alS); m0 = kap / (kap + al)
    # roots of z^2 - m(1+be) z + m be
    def roots(m):
        b_ = m * (1 + be); c_ = m * be
        disc = b_ * b_ - 4 * c_
        if disc >= 0:
            return (b_ + np.sqrt(disc)) / 2, (b_ - np.sqrt(disc)) / 2, disc
        return np.sqrt(c_), np.sqrt(c_), disc
    rS = roots(mS); r0 = roots(m0)
    out = dict(name=name, n=n, nS=len(S), full=bool(full), alpha=al,
               alpha_S=alS, ratio_alS_al=alS / al, cos_vS_vfull=cosang,
               spread_vS=float(vS.max() / vS.min()) if vS.min() > 0 else float('inf'),
               rate_S=float(rS[0]), rate_full=float(r0[0]), one_minus_q=1 - q,
               mS=float(mS), m0=float(m0))
    # ---- (F2) run and test both L-E forms at correcting stages
    xm = np.zeros(n); x = np.zeros(n)
    stats = dict(nc=0, nP=0, ok_full=0, ok_face=0, worst_full=0.0, worst_face=0.0)
    for t in range(T):
        dt = x - xm; a = x + be * dt
        sa = np.where(a > 0)[0]; Delta = 0.0
        if len(sa):
            z = I.ct[sa] - Qt[np.ix_(sa, sa)] @ a[sa]
            neg = z < 0
            if neg.any(): Delta = float(np.max(-z[neg] / (al * d[sa][neg])))
        r = np.minimum(be * dt, Delta); ell = a - r
        mx = (be * dt).max()
        if Delta > 0:
            stats['nc'] += 1
            if Delta < mx: stats['nP'] += 1
            # form A: full-graph Perron  v = D^{1/2}1, projector on ALL nodes
            vf = np.sqrt(d)
            def rat(vec, sub):
                rr = r[sub]; dd_ = dt[sub]; vv = vec / np.linalg.norm(vec)
                # x-coords: u = D^{1/2} * (hat vector)
                ru = np.sqrt(d[sub]) * rr; du = np.sqrt(d[sub]) * dd_
                pr = ru - (ru @ vv) * vv; pd = du - (du @ vv) * vv
                nn = float(pd @ pd)
                return (float(pr @ pr) / (be * be * nn)) if nn > 0 else 0.0
            ra = rat(np.sqrt(d), np.arange(n))
            rb = rat(vS, S)
            stats['ok_full'] += (ra <= 1 + 1e-12)
            stats['ok_face'] += (rb <= 1 + 1e-12)
            stats['worst_full'] = max(stats['worst_full'], ra)
            stats['worst_face'] = max(stats['worst_face'], rb)
        xn = I.obstacle_solve(I.ct, kap, ell, warm=sa if len(sa) else None)
        xm, x = x, xn
    out.update(stats)
    return out

cases = [
    ('P24 tuned (|S*|<n)', path_graph(24), [1.0] + [0.0] * 23, 1 / 32, 65 / 4096),
    ('P24 small rho (full)', path_graph(24), [1.0] + [0.0] * 23, 1 / 32, 1 / 4096),
    ('P12 full', path_graph(12), [1.0] + [0.0] * 11, 1 / 20, 1 / 4000),
    ('P16 tuned', path_graph(16), [1.0] + [0.0] * 15, 1 / 24, 0.0235),
    ('S12 leaf full', star_graph(12), [0.0, 1.0] + [0.0] * 10, 1 / 20, 1 / 800),
    ('cat6_2 full', caterpillar(6, 2), [1.0] + [0.0] * 17, 1 / 20, 1 / 4000),
]
res = []
print("=== face analysis: is the slow direction still D^{1/2}1 ? ===")
print("%-22s %3s %3s %8s %9s %8s %8s %9s %9s" %
      ("case", "n", "|S*|", "aS/a", "cos(vS,v)", "spread", "rate_S", "1-q", "rateFull"))
for nm, adj, sd, q, rho in cases:
    try:
        o = analyse(nm, adj, sd, q, rho)
    except Exception as ex:
        print("  %-22s SKIP %s" % (nm, ex)); continue
    res.append(o)
    print("%-22s %3d %3d %8.3f %9.6f %8.3f %8.6f %9.6f %9.6f" %
          (o['name'], o['n'], o['nS'], o['ratio_alS_al'], o['cos_vS_vfull'],
           o['spread_vS'], o['rate_S'], o['one_minus_q'], o['rate_full']))
print("\n=== L-E at the actual correcting stages (ratio must be <= 1) ===")
print("%-22s %6s %5s %s" % ("case", "#corr", "#P", "full-Perron cap | face-Perron cap"))
for o in res:
    print("%-22s %6d %5d   ok %d/%d worst %.6f  |  ok %d/%d worst %.6f" %
          (o['name'], o['nc'], o['nP'], o['ok_full'], o['nc'], o['worst_full'],
           o['ok_face'], o['nc'], o['worst_face']))
json.dump(res, open('/home/claude/work/overnight/w7_windowed/i3c_face.json', 'w'),
          indent=1, default=float)
