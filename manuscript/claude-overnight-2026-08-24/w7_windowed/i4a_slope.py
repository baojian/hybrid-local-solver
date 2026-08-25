"""I4-A: long-horizon (float) windowed-slope comparison, baseline vs
face-aligned cap, on the P24 tuned cell (the i2c spec cell:
q = 1/32, rho = 65/4096, |S*| = 23, baseline 91 inflation events to t = 4748,
tail slope 0.1255).  FLOAT, not exact -- the exact runs are in i4a_half1.py.
"""
import sys, math, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
import numpy as np
from fengine import FInst, window_table, tail_slope
from engine import path_graph


def perron_face(Qt, d, S):
    dS = d[S]; Ds = 1 / np.sqrt(dS)
    Qs = Ds[:, None] * Qt[np.ix_(S, S)] * Ds[None, :]
    ev, V = np.linalg.eigh(Qs)
    v = np.abs(V[:, 0])
    w = v / np.sqrt(dS)
    return w / w.max(), float(ev[0])


def run(I, T, mode='base'):
    n, q, al, be, kap, mu = I.n, I.q, I.alpha, I.beta, I.kappa, I.mu
    S = I.Sstar
    QtS = I.Qt[np.ix_(S, S)]; dS = I.d[S]
    HS = QtS + kap * np.diag(dS)
    wS, alS = perron_face(I.Qt, I.d, S)
    denS = QtS @ wS if mode == 'face' else al * dS
    capS = wS if mode == 'face' else np.ones(len(S))
    cache = {}
    cls, gams, Js, logPhi, loge2 = [], [], [], [], []
    xm = np.zeros(n); x = np.zeros(n)
    md = 'x'; em = e = None; lsc = 0.0; J = 0.0
    for t in range(T):
        if md == 'x':
            dh = x - xm; ah = x + be * dh
            sa = np.where(ah > 1e-300)[0]
            Delta = 0.0; cap = np.zeros(n)
            if len(sa):
                key = tuple(sa.tolist())
                if key not in cache:
                    if mode == 'face':
                        w_, _ = perron_face(I.Qt, I.d, sa)
                        cache[key] = (w_, I.Qt[np.ix_(sa, sa)] @ w_)
                    else:
                        cache[key] = (np.ones(len(sa)), al * I.d[sa])
                w_, den_ = cache[key]
                z = I.ct[sa] - I.Qt[np.ix_(sa, sa)] @ ah[sa]
                Delta = max(0.0, float(np.max(-z / den_)))
                cap[sa] = Delta * w_
            rh = np.minimum(be * dh, cap)
            c = ('N' if Delta <= 0 else
                 ('F' if np.all(cap >= be * dh - 1e-300) else
                  ('C' if np.all(cap <= be * dh + 1e-300) else 'P')))
            ellh = ah - rh
            eloc = I.xstar - x
            zmx = -eloc + (1 / q - 1) * dh
            cq = (1 + q) / q
            Dfin = -2 * cq * np.sum(I.d * rh * zmx) + cq ** 2 * np.sum(I.d * rh * rh)
            p = I.obstacle_solve(I.ct, kap, x, warm=S.tolist())
            ep = I.xstar - p; pmx = p - x
            gapE = 0.5 * ep @ I.Qt @ ep + kap / 2 * np.sum(I.d * pmx * pmx)
            Phi = gapE + mu / 2 * np.sum(I.d * zmx * zmx)
            e2 = float(np.sum(I.d * eloc * eloc))
            gam = 1 + mu * Dfin / (2 * Phi) if Phi > 0 else 1.0
            lp = math.log(Phi) if Phi > 0 else -np.inf
            xn = I.obstacle_solve(I.ct, kap, ellh)
            xm, x = x, xn
            if (set(np.where(x > 0)[0]) == set(S.tolist()) and
                    set(np.where(xm > 0)[0]) == set(S.tolist())):
                md = 'e'
                em = (I.xstar - xm)[S].copy(); e = (I.xstar - x)[S].copy()
                lsc = 0.0
            le = math.log(e2) if e2 > 0 else -np.inf
        else:
            dh = em - e
            ta = (1 + be) * e - be * em
            z = QtS @ ta
            Delta = max(0.0, float(np.max(-z / denS)))
            cap = Delta * capS
            bd = be * dh
            rh = np.minimum(bd, cap)
            c = ('N' if Delta <= 0 else
                 ('F' if np.all(cap >= bd - 1e-300) else
                  ('C' if np.all(cap <= bd + 1e-300) else 'P')))
            zmx = -e + (1 / q - 1) * dh
            cq = (1 + q) / q
            Dfin = -2 * cq * np.sum(dS * rh * zmx) + cq ** 2 * np.sum(dS * rh * rh)
            ep = np.linalg.solve(HS, kap * dS * e)
            emep = e - ep
            gapE = 0.5 * ep @ QtS @ ep + kap / 2 * np.sum(dS * emep * emep)
            Phi = gapE + mu / 2 * np.sum(dS * zmx * zmx)
            e2 = float(np.sum(dS * e * e))
            gam = 1 + mu * Dfin / (2 * Phi) if Phi > 0 else 1.0
            lp = math.log(Phi) + 2 * lsc if Phi > 0 else -np.inf
            le = math.log(e2) + 2 * lsc if e2 > 0 else -np.inf
            en = np.linalg.solve(HS, kap * dS * (ta + rh))
            em, e = e, en
            sc = float(np.abs(e).max())
            if 0 < sc < 1e-120:
                em /= sc; e /= sc; lsc += math.log(sc)
        if gam > 1:
            J += math.log(gam)
        cls.append(c); gams.append(gam); Js.append(J)
        logPhi.append(lp); loge2.append(le)
    return dict(cls=''.join(cls), gamma=gams, J=Js, logPhi=logPhi,
                loge2=loge2, alpha_S=alS, ratio_alS=alS / al)


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 4800
    n, q, rho = 24, 1 / 32, 65 / 4096
    I = FInst(path_graph(n), [1.0] + [0.0] * (n - 1), q=q, rho=rho)
    print("P24 tuned  n=%d |S*|=%d q=%g rho=%g  T=%d  (FLOAT)"
          % (n, len(I.Sstar), q, rho, T))
    out = {}
    for mode in ('base', 'face'):
        r = run(I, T, mode)
        sl, B = tail_slope(r, q)
        ev = [t for t in range(T) if r['gamma'][t] > 1]
        nc = sum(1 for c in r['cls'] if c != 'N')
        cen = {c: r['cls'].count(c) for c in 'NCPF'}
        wt = window_table(r, q)
        mx = max((w['ratio'] for w in wt[1:]), default=0.0)
        print("  %-5s  J_T=%8.5f  slope=%.5f  events=%3d last_ev=%4s  "
              "ncorr=%3d last_corr=%4s  N/C/P/F=%d/%d/%d/%d  "
              "max window infl/(qw) j>=1 = %.5f  alpha_S/alpha=%.4f"
              % (mode, r['J'][-1], sl, len(ev),
                 ev[-1] if ev else None, nc,
                 max((t for t, c in enumerate(r['cls']) if c != 'N'),
                     default=None),
                 cen['N'], cen['C'], cen['P'], cen['F'], mx, r['ratio_alS']))
        out[mode] = dict(J=r['J'][-1], slope=float(sl), events=len(ev),
                         last_event=ev[-1] if ev else None, ncorr=nc,
                         census=cen, maxwin=float(mx),
                         ratio_alS=r['ratio_alS'])
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i4a_slope.json', 'w'), indent=1, default=str)
