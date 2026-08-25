"""I5-C: post-lock face V-decay with the w-mode PROJECTED OUT (the correct
analogue of the K_n V, which lives on the mean-free subspace).

On the locked face S*, w = certified Perron vector, P_w = D_S-orthogonal
projector onto w^perp.  h := P_w e.  Under an N-cascade e_{t+1} = Mm_S ta_t,
and [Mm_S, P_w] = 0 up to the w-eigenspace, so h obeys the same recurrence.
Check exactly:  V(h_{t+1}, h_t) >= 0  and  V_{t+1} <= (1-qr)^2 V_t,
V(u,v) = <u,u>_D - (1+b)<u, Mm v>_D + b <Mm v, Mm v>_D.
Also the floor with the *lower* CW end (worst-case rate check):
L^w_t / L^w_{t-1} >= 1-qr at every post-lock stage (already in main; here we
print the observed min/max ratio to compare against the overdamped roots).
"""
import sys, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, _gauss
from i3g_core import face_w_exact
from i5c_core import run_i5c

out = {}
for nm, adj, seed, q, rho, T in [
        ('P12 tuned', path_graph(12), [Fr(1)] + [Fr(0)] * 11, Fr(1, 20),
         Fr(5, 128), 200),
        ('P24 tuned', path_graph(24), [Fr(1)] + [Fr(0)] * 23, Fr(1, 32),
         Fr(65, 4096), 240)]:
    t0 = time.time()
    I = Inst(adj, seed, q, rho)
    recs = run_i5c(I, T, variant='fm')
    n = I.n
    d, Qt, kap, xs = I.d, I.Qt, I.kappa, I.xstar
    Sl = tuple(sorted(I.Sstar))
    idx = list(Sl)
    m = len(idx)
    Qs = [[Qt[i][j] for j in idx] for i in idx]
    ds = [d[i] for i in idx]
    H = [[Qs[a][b] + (kap * ds[a] if a == b else 0) for b in range(m)]
         for a in range(m)]
    w, dv, lo, hi = face_w_exact(Qt, d, I.adj, idx, k=8)
    wv = [w[i] for i in idx]
    nw = sum(ds[a] * wv[a] * wv[a] for a in range(m))

    def Pw(u):
        c = sum(ds[a] * u[a] * wv[a] for a in range(m)) / nw
        return [u[a] - c * wv[a] for a in range(m)]

    def MmS(u):
        return _gauss([row[:] for row in H],
                      [kap * ds[a] * u[a] for a in range(m)])
    tface = next(t for t in range(len(recs))
                 if tuple(i for i in range(n) if recs[t]['x'][i] > 0) == Sl)
    r9 = dict(C9=[0, 0], Vpos=[0, 0], worst=None, tface=tface)
    lastN = None
    hprev = None
    Vprev = None
    for t in range(tface + 1, len(recs) - 1):
        r = recs[t]
        if r['S'] != Sl or r['cls'] != 'N':
            hprev = Vprev = None
            continue
        be = r['beta']
        qr = r['qr']
        e_m = [xs[i] - recs[t - 1]['x'][i] for i in idx]
        e_t = [xs[i] - r['x'][i] for i in idx]
        h_m, h_t = Pw(e_m), Pw(e_t)

        def Vform(u, v):
            Mv = MmS(v)
            return (sum(ds[a] * u[a] * u[a] for a in range(m))
                    - (1 + be) * sum(ds[a] * u[a] * Mv[a] for a in range(m))
                    + be * sum(ds[a] * Mv[a] * Mv[a] for a in range(m)))
        V = Vform(h_t, h_m)
        r9['Vpos'][1] += 1
        r9['Vpos'][0] += (V >= 0)
        if Vprev is not None and Vprev > 0:
            r9['C9'][1] += 1
            ok = V <= (1 - qr) ** 2 * Vprev
            r9['C9'][0] += ok
            rt = float(V / Vprev)
            r9['worst'] = rt if r9['worst'] is None else max(r9['worst'], rt)
        Vprev = V
    print("%s: tface=%d  Vpos %d/%d  C9proj %d/%d  worst=%s  [%.0fs]"
          % (nm, tface, *r9['Vpos'], *r9['C9'],
             ('%.6f' % r9['worst']) if r9['worst'] is not None else 'NA',
             time.time() - t0), flush=True)
    out[nm] = r9
json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                    'i5c_c9proj.json', 'w'), indent=1, default=str)
