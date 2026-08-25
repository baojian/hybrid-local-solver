"""I5-C runner: exact batteries for face-calibrated momentum.

Per run it verifies, ALL EXACT unless labelled:
  S     7+1 safety flags at every stage (incl. face_eq: S_t = supp x_t)
  CHAIN face chain is monotone (S_{t-1} subset S_t); #changes <= |S*|
  OD    per-face overdamping certificate kappa/(kappa+ub) >= 1-qr^2 (asserted
        in face_mom; re-checked here) and interlacing lo > alpha on proper
        faces (certified strictness)
  C5f   L-E, face geometry, with the STAGE's beta_t   (at r != 0 stages)
  C10f  face low-mode floor  L^w_t >= (1-qr_t) L^w_{t-1} > 0  (same-face
        stages; reported post-lock and overall; also vs global 1-q)
  ABS   absorption: last stage with r != 0 (t_abs-1), last with Delta > 0;
        gamma_t = 1 exactly beyond (r = 0 => Dfin = 0 => gamma = 1)
  J_T   exact estimate-sequence inflation (global-q certificate, as i2c/i4a)
  SPEED first t with ||x*-x_t||_D^2 <= eps * ||x*||_D^2, eps in 1e-4/8/12
  RETUNE at face-change stages: exact gamma (=1 if r=0) and the
        face-Lyapunov jump Phi^new/Phi^old at the same state (Measured-style
        formula, exact arithmetic)
  C3f/C9f (optional) post-lock face N-linearity e_{t+1}=Mm_S ta_t and
        V-decay V_{t+1} <= (1-qr)^2 V_t with the face operator
"""
import sys, json, math, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, star_graph, complete_graph, _gauss
from i3g_core import face_w_exact
from i5c_core import run_i5c, face_mom, lemma_identity_checks

SAFEKEYS = ('pos_den', 'pos_w', 'mono_d', 'ell_ge_x', 'ell_le_xs',
            'e_ge_0', 'en_ge_0', 'face_eq')
EPS = (Fr(1, 10**4), Fr(1, 10**8), Fr(1, 10**12))


def analyse5(I, T, variant, k=8, wcache=None, beta_fix=None, qr_fix=None,
             c9=False):
    n = I.n
    d, Qt, q, al, kap, mu = I.d, I.Qt, I.q, I.alpha, I.kappa, I.mu
    xs = I.xstar
    recs = run_i5c(I, T, variant=variant, k=k, beta_fix=beta_fix,
                   qr_fix=qr_fix)
    if wcache is None:
        wcache = {}
    out = dict(variant=variant, T=len(recs),
               word=''.join(r['cls'] for r in recs),
               safe={kk: [0, 0] for kk in SAFEKEYS}, abort=False)
    ck = {kk: [0, 0] for kk in
          ('C5_face', 'C10_face_q', 'C10_face_qr', 'C11_mono', 'chain',
           'interlace', 'overdamp')}
    worst = dict(C5_face=0.0, C10_face_q=None, C10_face_qr=None)
    Sstar = tuple(sorted(I.Sstar))
    e2_0 = I.dotD(xs, xs)
    tface = None
    Lwprev = None
    Sprev = None
    gam = []
    corr = []       # stages with Delta > 0
    rnzs = []       # stages with r != 0
    changes = []
    speed = {str(e): None for e in EPS}
    faces = []
    qr_by_face = {}
    for r in recs:
        for kk in SAFEKEYS:
            c = out['safe'][kk]
            c[1] += 1
            c[0] += bool(r['safe'][kk])
        if r.get('ABORT'):
            out['abort'] = True
        t, S, x = r['t'], r['S'], r['x']
        qr, be = r['qr'], r['beta']
        if S and (not faces or faces[-1][1] != S):
            faces.append((t, S))
            if qr is not None:
                qr_by_face[S] = qr
        if tface is None and tuple(i for i in range(n) if x[i] > 0) == Sstar:
            tface = t
        post = (tface is not None and t > tface)
        e = [xs[i] - x[i] for i in range(n)]
        e2 = I.dotD(e, e)
        for eps in EPS:
            if speed[str(eps)] is None and e2 <= eps * e2_0:
                speed[str(eps)] = t
        dt, rr = r['dh'], r['rh']
        ck['C11_mono'][1] += 1
        ck['C11_mono'][0] += (all(v >= 0 for v in dt) and
                              all(v >= 0 for v in e))
        # ---- chain monotone
        if Sprev is not None:
            ck['chain'][1] += 1
            ck['chain'][0] += set(Sprev) <= set(S)
            if S != Sprev:
                changes.append(t)
        # ---- per-face certificates (once per new face)
        if S and (len(faces) and faces[-1][0] == t):
            lo, hi = r['cw']
            if lo is not None:
                ck['interlace'][1] += 1
                ck['interlace'][0] += (lo > al if S != tuple(range(n))
                                       else lo == al) or set(S) == set(range(n))
                if qr is not None:
                    ck['overdamp'][1] += 1
                    ck['overdamp'][0] += (kap / (kap + hi) >= 1 - qr * qr)
        # ---- face low-mode floor (same-face consecutive stages only)
        if S:
            key = (S, k)
            if key not in wcache:
                wcache[key] = face_w_exact(Qt, d, I.adj, list(S), k=k)
            wS = wcache[key][0]
            nw = sum(d[i] * wS[i] * wS[i] for i in S)
            Lw = sum(d[i] * e[i] * wS[i] for i in S) / nw
            if Lwprev is not None and S == Sprev and Lwprev > 0:
                okq = (Lw >= (1 - q) * Lwprev) and Lw > 0
                qq = qr if qr is not None else q
                okr = (Lw >= (1 - qq) * Lwprev) and Lw > 0
                for nm, ok in (('C10_face_q', okq), ('C10_face_qr', okr)):
                    ck[nm][1] += 1
                    ck[nm][0] += ok
                    if post:
                        ck.setdefault(nm + '_post', [0, 0])
                        ck[nm + '_post'][1] += 1
                        ck[nm + '_post'][0] += ok
                rt = float(Lw / Lwprev)
                for nm in ('C10_face_q', 'C10_face_qr'):
                    worst[nm] = rt if worst[nm] is None else min(worst[nm], rt)
            Lwprev = Lw
        if r['Delta'] > 0:
            corr.append((t, r['cls'], post))
        # ---- diagnostics only where a real retraction happened
        if r['rnz']:
            rnzs.append(t)
            wS = wcache[(S, k)][0]
            nw = sum(d[i] * wS[i] * wS[i] for i in S)

            def pface(u):
                c = sum(d[i] * u[i] * wS[i] for i in S) / nw
                return {i: u[i] - c * wS[i] for i in S}
            pr, pd = pface(rr), pface(dt)
            nr = sum(d[i] * pr[i] ** 2 for i in S)
            nd = sum(d[i] * pd[i] ** 2 for i in S)
            ok = nr <= be * be * nd
            ck['C5_face'][1] += 1
            ck['C5_face'][0] += ok
            if nd > 0:
                worst['C5_face'] = max(worst['C5_face'],
                                       float(nr / (be * be * nd)))
            # exact global-q gamma
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
        Sprev = S
    # ---- retune jumps at face changes (state-based Phi with (qr,beta) pairs)
    retune = []
    for t in changes:
        r = recs[t]
        if r['qr'] is None or t == 0:
            continue
        Sold = recs[t - 1]['S']
        qro, qrn = recs[t - 1]['qr'], r['qr']
        if qro is None or qro == qrn:
            continue
        x, dt = r['x'], r['dh']
        e = [xs[i] - x[i] for i in range(n)]
        p = I.obstacle_solve(I.ct, kap, x, warm=I.Sstar)
        pmx = [p[i] - x[i] for i in range(n)]
        gapE = (I.Fval(p) - I.Fval(xs)) + kap / 2 * I.dotD(pmx, pmx)

        def phiP(qq):
            if qq >= 1:
                z = [-e[i] for i in range(n)]
            else:
                z = [-e[i] + (1 / qq - 1) * dt[i] for i in range(n)]
            aR = qq * qq / (1 + qq * qq)
            muP = kap * aR / (aR + kap)
            return gapE + muP / 2 * I.dotD(z, z)
        Pn, Po = phiP(qrn), phiP(qro)
        retune.append(dict(t=t, qr_old=float(qro), qr_new=float(qrn),
                           jump=float(Pn / Po) if Po > 0 else None,
                           gamma_here=1.0 if not r['rnz'] else None,
                           rnz=r['rnz'], gapE_pos=gapE > 0))
    # ---- optional post-lock face C3/C9
    c9res = None
    if c9 and tface is not None:
        Sl = Sstar
        idx = list(Sl)
        m = len(idx)
        Qs = [[Qt[i][j] for j in idx] for i in idx]
        ds = [d[i] for i in idx]
        H = [[Qs[a][b] + (kap * ds[a] if a == b else 0) for b in range(m)]
             for a in range(m)]

        def MmS(u):
            return _gauss([row[:] for row in H], [kap * ds[a] * u[a]
                                                  for a in range(m)])
        c9res = dict(C3=[0, 0], C9=[0, 0], Vpos=[0, 0], worstV=None)
        ts = [t for t in range(tface + 1, len(recs) - 1)]
        ts = [t for t in ts if t <= tface + 80 or t % 20 == 0 or
              t >= len(recs) - 5]
        Vprev = {}
        for t in ts:
            r = recs[t]
            if r['S'] != Sl or recs[t + 1]['S'] != Sl:
                continue
            be_t = r['beta']
            qr_t = r['qr'] if r['qr'] is not None else q
            e_m = [xs[i] - recs[t - 1]['x'][i] for i in idx] \
                if t - 1 >= 0 else None
            e_t = [xs[i] - r['x'][i] for i in idx]
            e_n = [xs[i] - r['xn'][i] for i in idx]
            if r['cls'] == 'N' and e_m is not None:
                ta = [(1 + be_t) * e_t[a] - be_t * e_m[a] for a in range(m)]
                pred = MmS(ta)
                c9res['C3'][1] += 1
                c9res['C3'][0] += (pred == e_n)

            def Vform(u, v):
                Mv = MmS(v)
                return (sum(ds[a] * u[a] * u[a] for a in range(m))
                        - (1 + be_t) * sum(ds[a] * u[a] * Mv[a]
                                           for a in range(m))
                        + be_t * sum(ds[a] * Mv[a] * Mv[a] for a in range(m)))
            if e_m is not None:
                # project out the w-mode?  K_n V uses the FULL vector minus
                # mean; here we use the full face vectors (the w-mode is
                # overdamped => its V_k can be negative; record Vpos to see)
                V = Vform(e_n, e_t)
                Vp = Vform(e_t, e_m)
                c9res['Vpos'][1] += 1
                c9res['Vpos'][0] += (V >= 0)
                if Vp > 0:
                    c9res['C9'][1] += 1
                    ok = V <= (1 - qr_t) ** 2 * Vp
                    c9res['C9'][0] += ok
                    rt = float(V / Vp)
                    c9res['worstV'] = rt if c9res['worstV'] is None \
                        else max(c9res['worstV'], rt)
    out['checks'] = ck
    out['worst'] = worst
    out['ncorr'] = len(corr)
    out['n_rnz'] = len(rnzs)
    out['last_corr'] = corr[-1][0] if corr else None
    out['last_rnz'] = rnzs[-1] if rnzs else None
    out['tface'] = tface
    out['census'] = {c: out['word'].count(c) for c in 'NCPF'}
    out['J_T'] = sum(math.log(g) for _, g, _p in gam)
    out['infl_events'] = len(gam)
    out['gam'] = gam
    out['speed'] = speed
    out['nfaces'] = len(faces)
    out['nchanges'] = len(changes)
    out['changes'] = changes
    out['qr_final'] = float(recs[-1]['qr']) if recs[-1]['qr'] is not None \
        else None
    out['beta_final'] = float(recs[-1]['beta'])
    out['retune'] = retune
    out['retune_logsum'] = sum(max(0.0, math.log(rj['jump']))
                               for rj in retune if rj['jump'])
    out['c9'] = c9res
    return out, wcache


def line5(o):
    ck = o['checks']

    def f(nm):
        a, b = ck[nm]
        return '%d/%d' % (a, b)
    sp = o['speed']
    return ("%-6s T=%-4d corr(D>0)=%-3d r!=0:%-3d lastD=%-5s lastR=%-5s "
            "N/C/P/F=%d/%d/%d/%d C5f %s(w=%.4g) C10f[q] %s C10f[qr] %s "
            "(post %s | %s) chain %s intl %s od %s J=%.5f(%dev) "
            "tF=%s nface=%d chg=%d rt+=%.4f b_end=%.4f "
            "t@1e-4/8/12=%s/%s/%s safe=%s"
            % (o['variant'], o['T'], o['ncorr'], o['n_rnz'],
               o['last_corr'], o['last_rnz'],
               o['census']['N'], o['census']['C'], o['census']['P'],
               o['census']['F'], f('C5_face'), o['worst']['C5_face'],
               f('C10_face_q'), f('C10_face_qr'),
               '%d/%d' % tuple(ck.get('C10_face_q_post', [0, 0])),
               '%d/%d' % tuple(ck.get('C10_face_qr_post', [0, 0])),
               f('chain'), f('interlace'), f('overdamp'),
               o['J_T'], o['infl_events'], o['tface'], o['nfaces'],
               o['nchanges'], o['retune_logsum'], o['beta_final'],
               sp[str(EPS[0])], sp[str(EPS[1])], sp[str(EPS[2])],
               all(a == b for a, b in o['safe'].values())))
