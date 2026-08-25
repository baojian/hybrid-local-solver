"""I5-C: long-horizon FLOAT windowed-slope comparison on P24 tuned:
base / face-cap / fm (per-stage face momentum) / fmlock (oracle S* momentum).
FLOAT mirror -- the exact runs are i5c_main.py; the exact word prefix is
cross-checked against this mirror separately.
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


def mom_from_alS(I, alS, M=1000):
    """Float mirror of i5c_core.face_mom (incl. the M-grid ceil)."""
    if alS <= I.alpha:
        return I.q, I.beta
    if alS >= 1:
        return 1.0, 0.0
    q2 = alS / (1 - alS)
    if I.q * I.q >= q2:
        return I.q, I.beta
    qr = math.ceil(math.sqrt(q2) * M) / M
    if qr >= 1:
        return 1.0, 0.0
    return qr, (1 - qr) / (1 + qr)


def run(I, T, mode='base'):
    n, q, al, be0, kap, mu = I.n, I.q, I.alpha, I.beta, I.kappa, I.mu
    S = I.Sstar
    QtS = I.Qt[np.ix_(S, S)]; dS = I.d[S]
    HS = QtS + kap * np.diag(dS)
    wS, alS_star = perron_face(I.Qt, I.d, S)
    qr_lk, be_lk = mom_from_alS(I, alS_star)
    facecap = mode in ('face', 'fm', 'fmlock')
    denS = QtS @ wS if facecap else al * dS
    capS = wS if facecap else np.ones(len(S))
    beS = be_lk if mode in ('fm', 'fmlock') else be0
    cache = {}
    cls, gams, Js, loge2 = [], [], [], []
    xm = np.zeros(n); x = np.zeros(n)
    md = 'x'; em = e = None; lsc = 0.0; J = 0.0
    nchg = 0; Skey_prev = None
    for t in range(T):
        if md == 'x':
            dh = x - xm
            sup = np.where((x > 1e-300) | (dh > 1e-300))[0]
            key = tuple(sup.tolist())
            if key not in cache:
                if len(sup) == 0:
                    cache[key] = (np.ones(0), np.ones(0), q, be0)
                else:
                    if facecap or mode == 'fm':
                        w_, alS = perron_face(I.Qt, I.d, sup)
                    else:
                        w_, alS = np.ones(len(sup)), al
                    if mode == 'fm':
                        qr_, be_ = mom_from_alS(I, alS)
                    elif mode == 'fmlock':
                        qr_, be_ = qr_lk, be_lk
                    else:
                        qr_, be_ = q, be0
                    den_ = (I.Qt[np.ix_(sup, sup)] @ w_ if facecap
                            else al * I.d[sup])
                    cache[key] = (w_, den_, qr_, be_)
            w_, den_, qr_, be = cache[key]
            if Skey_prev is not None and key != Skey_prev:
                nchg += 1
            Skey_prev = key
            ah = x + be * dh
            sa = np.where(ah > 1e-300)[0]
            Delta = 0.0; cap = np.zeros(n)
            if len(sa):
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
            Dfin = -2 * cq * np.sum(I.d * rh * zmx) + \
                cq ** 2 * np.sum(I.d * rh * rh)
            p = I.obstacle_solve(I.ct, kap, x, warm=S.tolist())
            ep = I.xstar - p; pmx = p - x
            gapE = 0.5 * ep @ I.Qt @ ep + kap / 2 * np.sum(I.d * pmx * pmx)
            Phi = gapE + mu / 2 * np.sum(I.d * zmx * zmx)
            gam = 1 + mu * Dfin / (2 * Phi) if Phi > 0 else 1.0
            xn = I.obstacle_solve(I.ct, kap, ellh)
            xm, x = x, xn
            if (set(np.where(x > 0)[0]) == set(S.tolist()) and
                    set(np.where(xm > 0)[0]) == set(S.tolist())):
                md = 'e'
                em = (I.xstar - xm)[S].copy(); e = (I.xstar - x)[S].copy()
                lsc = 0.0
            e2 = float(np.sum(I.d * eloc * eloc))
            le = math.log(e2) if e2 > 0 else -np.inf
        else:
            be = beS if mode in ('fm', 'fmlock') else be0
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
            Dfin = (-2 * cq * np.sum(dS * rh * zmx) +
                    cq ** 2 * np.sum(dS * rh * rh))
            ep = np.linalg.solve(HS, kap * dS * e)
            emep = e - ep
            gapE = 0.5 * ep @ QtS @ ep + kap / 2 * np.sum(dS * emep * emep)
            Phi = gapE + mu / 2 * np.sum(dS * zmx * zmx)
            e2 = float(np.sum(dS * e * e))
            gam = 1 + mu * Dfin / (2 * Phi) if Phi > 0 else 1.0
            le = math.log(e2) + 2 * lsc if e2 > 0 else -np.inf
            en = np.linalg.solve(HS, kap * dS * (ta + rh))
            em, e = e, en
            sc = float(np.abs(e).max())
            if 0 < sc < 1e-120:
                em /= sc; e /= sc; lsc += math.log(sc)
        if gam > 1:
            J += math.log(gam)
        cls.append(c); gams.append(gam); Js.append(J); loge2.append(le)
    return dict(cls=''.join(cls), gamma=gams, J=Js, loge2=loge2,
                logPhi=loge2, nchg=nchg, alpha_S=alS_star,
                qr_lock=qr_lk, be_lock=be_lk)


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 4800
    n, q, rho = 24, 1 / 32, 65 / 4096
    I = FInst(path_graph(n), [1.0] + [0.0] * (n - 1), q=q, rho=rho)
    print("P24 tuned n=%d |S*|=%d q=%g rho=%g T=%d (FLOAT)"
          % (n, len(I.Sstar), q, rho, T), flush=True)
    out = {}
    for mode in ('base', 'face', 'fm', 'fmlock'):
        r = run(I, T, mode)
        sl, B = tail_slope(r, q)
        ev = [t for t in range(T) if r['gamma'][t] > 1]
        nc = sum(1 for c in r['cls'] if c != 'N')
        cen = {c: r['cls'].count(c) for c in 'NCPF'}
        # iteration count to relative e2 <= 1e-8, 1e-16 (log scale)
        le0 = r['loge2'][0]
        t8 = next((t for t, v in enumerate(r['loge2'])
                   if v <= le0 + math.log(1e-8)), None)
        t16 = next((t for t, v in enumerate(r['loge2'])
                    if v <= le0 + math.log(1e-16)), None)
        print("  %-6s J_T=%9.5f slope=%.5f ev=%3d last_ev=%4s ncorr=%4d "
              "last_corr=%4s N/C/P/F=%d/%d/%d/%d nchg=%d t@1e-8=%s t@1e-16=%s"
              % (mode, r['J'][-1], sl, len(ev), ev[-1] if ev else None, nc,
                 max((t for t, c in enumerate(r['cls']) if c != 'N'),
                     default=None), cen['N'], cen['C'], cen['P'], cen['F'],
                 r['nchg'], t8, t16), flush=True)
        out[mode] = dict(J=r['J'][-1], slope=float(sl), events=len(ev),
                         last_event=ev[-1] if ev else None, ncorr=nc,
                         census=cen, nchg=r['nchg'], t8=t8, t16=t16,
                         qr_lock=r['qr_lock'], be_lock=r['be_lock'],
                         word400=r['cls'][:400])
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i5c_slope.json', 'w'), indent=1, default=str)
