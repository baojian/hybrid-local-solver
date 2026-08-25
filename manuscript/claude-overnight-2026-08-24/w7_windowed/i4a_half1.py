"""I4-A HALF 1: face-aligned retraction cap -- exact verification.

Runs the safeguarded AESP-CD recurrence in EXACT Fractions under two caps
  base : r = min(beta d_t, Delta * 1)            (engine.py, w = 1)
  face : r = min(beta d_t, Delta_w * w^(k))      (i3g_core, w = inverse iter.)
and evaluates, at every stage and exactly:
  S1  safety invariant of the recovered theorem (7 flags)
  C5  L-E in the FULL-graph geometry   ||P_1 r||_D <= beta ||P_1 d||_D
  C5F L-E in the FACE geometry         ||P_w r||_{D_S} <= beta ||P_w d||_{D_S}
  C10 low-mode floor, full geometry    L_t >= (1-q) L_{t-1} > 0
  C10F low-mode floor, face geometry   L^w_t >= (1-q) L^w_{t-1} > 0
  C11 monotone certificate             d_t >= 0, e_t >= 0
  C15 correction census                N / C(clean) / P(partial) / F(full)
  J_T exact (only correcting stages can have gamma > 1)
"""
import sys, json, math, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, star_graph, complete_graph
from i3g_core import run_exact, face_w_exact

SAFEKEYS = ('pos_den', 'pos_w', 'mono_d', 'ell_ge_x', 'ell_le_xs',
            'e_ge_0', 'en_ge_0')


def analyse(I, T, mode, k=8, wcache=None, kdiag=8):
    n = I.n
    d, Qt, q, be, al, kap, mu = I.d, I.Qt, I.q, I.beta, I.alpha, I.kappa, I.mu
    vol = sum(d)
    xs = I.xstar
    recs = run_exact(I, T, mode=mode, k=k)
    if wcache is None:
        wcache = {}
    out = dict(mode=mode, k=k, T=len(recs),
               word=''.join(r['cls'] for r in recs),
               safe={kk: [0, 0] for kk in SAFEKEYS}, abort=False)
    ck = {kk: [0, 0] for kk in ('C5_full', 'C5_face', 'C10_full', 'C10_face',
                                'C11_mono')}
    worst = dict(C5_full=0.0, C5_face=0.0, C10_full=None, C10_face=None)
    Sstar = tuple(sorted(I.Sstar))
    tface = None
    Lprev = Lwprev = None
    Jt = Fr(0)
    gam = []
    corr = []
    for r in recs:
        for kk in SAFEKEYS:
            ck_ = out['safe'][kk]
            ck_[1] += 1
            ck_[0] += bool(r['safe'][kk])
        if r.get('ABORT'):
            out['abort'] = True
        t, S, x = r['t'], r['S'], r['x']
        if tface is None and tuple(i for i in range(n) if x[i] > 0) == Sstar:
            tface = t
        post = (tface is not None and t > tface)
        e = [xs[i] - x[i] for i in range(n)]
        dt, rr = r['dh'], r['rh']
        ck['C11_mono'][1] += 1
        ck['C11_mono'][0] += (all(v >= 0 for v in dt) and all(v >= 0 for v in e))
        # ---- full-graph low mode
        L = sum(d[i] * e[i] for i in range(n)) / vol
        if Lprev is not None and Lprev > 0:
            ok = (L >= (1 - q) * Lprev) and L > 0
            ck['C10_full'][1] += 1; ck['C10_full'][0] += ok
            if post:
                ck.setdefault('C10_full_post', [0, 0])
                ck['C10_full_post'][1] += 1; ck['C10_full_post'][0] += ok
            rt = float(L / Lprev)
            worst['C10_full'] = rt if worst['C10_full'] is None \
                else min(worst['C10_full'], rt)
        Lprev = L
        # ---- face low mode (running face S)
        if S:
            key = S
            key = (S, kdiag)
            if key not in wcache:
                wcache[key] = face_w_exact(Qt, d, I.adj, list(S), k=kdiag)
            wS = wcache[key][0]
            nw = sum(d[i] * wS[i] * wS[i] for i in S)
            Lw = sum(d[i] * e[i] * wS[i] for i in S) / nw
            if Lwprev is not None and Lwprev > 0:
                ok = (Lw >= (1 - q) * Lwprev) and Lw > 0
                ck['C10_face'][1] += 1; ck['C10_face'][0] += ok
                if post:
                    ck.setdefault('C10_face_post', [0, 0])
                    ck['C10_face_post'][1] += 1; ck['C10_face_post'][0] += ok
                rt = float(Lw / Lwprev)
                worst['C10_face'] = rt if worst['C10_face'] is None \
                    else min(worst['C10_face'], rt)
            Lwprev = Lw
        # ---- L-E only meaningful at correcting stages (r == 0 otherwise)
        if r['Delta'] > 0:
            corr.append((t, r['cls'], post))
            # full geometry: P_1 u = u - <u,1>_D/vol
            def pfull(u):
                m = sum(d[i] * u[i] for i in range(n)) / vol
                return [u[i] - m for i in range(n)]
            pr, pd = pfull(rr), pfull(dt)
            nr = sum(d[i] * pr[i] ** 2 for i in range(n))
            nd = sum(d[i] * pd[i] ** 2 for i in range(n))
            ok = nr <= be * be * nd
            ck['C5_full'][1] += 1; ck['C5_full'][0] += ok
            if nd > 0:
                worst['C5_full'] = max(worst['C5_full'],
                                       float(nr / (be * be * nd)))
            # face geometry: P_w u = u - <u,w>_{D_S}/<w,w>_{D_S} * w on S
            wS = wcache[(S, kdiag)][0]
            nw = sum(d[i] * wS[i] * wS[i] for i in S)
            def pface(u):
                c = sum(d[i] * u[i] * wS[i] for i in S) / nw
                return {i: u[i] - c * wS[i] for i in S}
            pr, pd = pface(rr), pface(dt)
            nr = sum(d[i] * pr[i] ** 2 for i in S)
            nd = sum(d[i] * pd[i] ** 2 for i in S)
            ok = nr <= be * be * nd
            ck['C5_face'][1] += 1; ck['C5_face'][0] += ok
            if nd > 0:
                worst['C5_face'] = max(worst['C5_face'],
                                       float(nr / (be * be * nd)))
            # exact gamma at this stage (N stages have Dfin = 0 => gamma = 1)
            zmx = [-e[i] + (1 / q - 1) * dt[i] for i in range(n)]
            cq = (1 + q) / q
            Dfin = -2 * cq * I.dotD(rr, zmx) + cq ** 2 * I.dotD(rr, rr)
            p = I.obstacle_solve(I.ct, kap, x, warm=I.Sstar)
            pmx = [p[i] - x[i] for i in range(n)]
            gapE = (I.Fval(p) - I.Fval(xs)) + kap / 2 * I.dotD(pmx, pmx)
            Phi = gapE + mu / 2 * I.dotD(zmx, zmx)
            g = (1 + mu * Dfin / (2 * Phi)) if Phi > 0 else Fr(1)
            if g > 1:
                gam.append((t, float(g), post))
    out['checks'] = ck
    out['worst'] = worst
    out['ncorr'] = len(corr)
    out['corr'] = corr
    out['last_corr'] = corr[-1][0] if corr else None
    out['tface'] = tface
    out['ncorr_post'] = sum(1 for c in corr if c[2])
    out['census'] = {c: out['word'].count(c) for c in 'NCPF'}
    out['J_T'] = sum(math.log(g) for _, g, _p in gam)
    out['J_post'] = sum(math.log(g) for _, g, p in gam if p)
    out['gam'] = gam
    out['infl_events'] = len(gam)
    return out, wcache


def line(o):
    ck = o['checks']
    return ("%-5s T=%-4d ncorr=%-3d last=%-5s N/C/P/F=%d/%d/%d/%d  "
            "C5full %d/%d(w=%.4g) C5face %d/%d(w=%.4g)  "
            "C10full %d/%d(post %s) C10face %d/%d(post %s)  J=%.5f (%d ev) tF=%s safe=%s"
            % (o['mode'], o['T'], o['ncorr'], o['last_corr'],
               o['census']['N'], o['census']['C'], o['census']['P'],
               o['census']['F'],
               ck['C5_full'][0], ck['C5_full'][1], o['worst']['C5_full'],
               ck['C5_face'][0], ck['C5_face'][1], o['worst']['C5_face'],
               ck['C10_full'][0], ck['C10_full'][1],
               '%d/%d' % tuple(ck.get('C10_full_post', [0, 0])),
               ck['C10_face'][0], ck['C10_face'][1],
               '%d/%d' % tuple(ck.get('C10_face_post', [0, 0])),
               o['J_T'], o['infl_events'], o['tface'],
               all(a == b for a, b in o['safe'].values())))


if __name__ == '__main__':
    t0 = time.time()
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    results = {}

    def do(name, adj, seed, q, rho, T, modes=(('base', 0), ('face', 8))):
        I = Inst(adj, seed, q, rho)
        print("\n=== %s  n=%d |S*|=%d  q=%s rho=%s alpha=%s ===" %
              (name, I.n, len(I.Sstar), q, rho, I.alpha))
        wc = {}
        rr = {}
        for (m, k) in modes:
            o, wc = analyse(I, T, m, k=k, wcache=wc, kdiag=8)
            tag = m if m == 'base' else 'face%d' % k
            o['tag'] = tag
            print("  " + line(o))
            rr[tag] = o
        results[name] = dict(n=I.n, nS=len(I.Sstar), q=str(q), rho=str(rho),
                             runs={t: {kk: v for kk, v in o.items()
                                       if kk not in ('corr',)}
                                   for t, o in rr.items()})
        return rr

    # ---------------- P24 tuned: the sharpest known proper-face stress cell
    do('P24 tuned', path_graph(24), [Fr(1)] + [Fr(0)] * 23, Fr(1, 32),
       Fr(65, 4096), T, modes=(('base', 0), ('face', 2), ('face', 8)))

    json.dump(results, open('/home/claude/work/overnight/w7_windowed/'
                            'i4a_half1_p24.json', 'w'), indent=1, default=str)
    print("\n[%.1fs]" % (time.time() - t0))
