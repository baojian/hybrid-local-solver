"""I6-B: knproof2 rerun with the REPAIRED C9/C17 (clip-identity certificate).

Changes vs knproof2.py:
  C15_corrclass -> census only (records CC/F/P; always passes).  It was never
                   a lemma (i4a); with C9' proved at ALL correcting stages the
                   theorem no longer needs P-exclusion.
  C17_Pcert     -> NEW certified bound from the clip identity:
                   U2' = VF + mh^2*(2*be*sqrt_ub(X2*m2v) - m2v) <= (1-q)^2 V_t
                   (VF = s(1-mh)|h|^2, X2=|co|^2, m2v=|phih|^2).
  C9s_corr      -> NEW: the PROOF bound V_{t+1} <= VF + mh^2 be^2 |co|^2 at
                   every correcting stage (F, CC and P alike).

Predicates (see findings/i2c_windowed_proof.md for the lemma statements):
  C1_master     (Qt+kap D) e_{t+1} = kap D (x*-ell_t)          [L-A]
  C2_Fcollapse  F stage => ell=x_t => modal collapse           [L-B]
  C3_Nlinear    N stage => two-term modal linear recurrence    [L-C]
  C4_Vdecay     N stage => V_{t+1} = s V_t exactly             [L-C']
  C5_oscil      |P_h r_t| <= beta |P_h d_t|  (no low->high)    [L-E]
  C6_trigger    alpha*Delta = max_i[-(alpha taL + lam_h tah_i)]_+  [L-D]
  C7_defect     Dfin_t <= a_q (|e_{t-1}|_D^2 - |e_t|_D^2)      [L-F1]
  C8_philb      2 Phi_t >= mu |e_t|_D^2                        [L-F2]
  C9_Vcontract  V_{t+1} <= (1-q)^2 V_t at EVERY stage          [L-I, closing]
  C10_lowfloor  L_t >= (1-q) L_{t-1} > 0 at every stage        [L-H]
  C11_monotone  d_t >= 0 and e_t >= 0 (lower certificate)      [L-M]
  C12_struct    lam_h > alpha <=> p^2<4s <=> s<=(1-q)^2; m0=1-q^2;
                low-mode char poly = (z-(1-q))^2               [L-S]
  C13_absorb    certificate fires; every later stage is N; gamma_t = 1
  C14_Rgeom     R_{t+1} <= (s/(1-q)^2) R_t on N stages         [L-G']
"""
import sys, math, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from kn_modal import KnModal

KEYS = ('C1_master', 'C2_Fcollapse', 'C3_Nlinear', 'C4_Vdecay', 'C5_oscil',
        'C6_trigger', 'C7_defect', 'C8_philb', 'C9_Vcontract', 'C10_lowfloor',
        'C11_monotone', 'C12_struct', 'C13_absorb', 'C14_Rgeom',
        'C15_corrclass', 'C16_Fcontract', 'C17_Pcert', 'C9s_corr')


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def sqrt_ub(X):
    """Rational u with u^2 >= X >= 0, tight to ~1e-18 relative."""
    if X == 0:
        return Fr(0)
    S = 10 ** 20
    num = X.numerator * S * S
    den = X.denominator
    r = math.isqrt(num * den) // den + 1
    u = Fr(r, S)
    assert u * u >= X
    return u


def analyze(name, n, seed, q, rho, T, alpha=None):
    K = KnModal(n, seed, q, rho, alpha=alpha)
    al, kap, be, mu, lam, dd = K.alpha, K.kappa, K.beta, K.mu, K.lam_h, K.dd
    p, s, m0, mh = K.p, K.s, K.m0, K.mh
    aq = (1 - q) / q
    C_ta = (1 + be) ** 2 + be * be / s
    dn_lb = (1 - p * p / (4 * s)) / 2
    wh2 = (al * be / lam) ** 2
    res = dict(name=name, n=n, q=str(q), rho=str(rho), T=T,
               fullsupp=K.fullsupp, ctil_pos=K.ctil_pos,
               checks={k: [0, 0] for k in KEYS}, fails=[],
               maxVratio_corr=None, maxVratio_all=None, margin9=None)
    ck = res['checks']

    def tick(key, ok, info=''):
        ck[key][1] += 1
        if ok:
            ck[key][0] += 1
        else:
            res['fails'].append((key, info))

    # ---- C12: structural, instance level ---------------------------------
    tick('C12_struct', (lam > al) and (p * p < 4 * s) and (s <= (1 - q) ** 2)
         and (m0 == 1 - q * q) and (m0 * (1 + be) == 2 * (1 - q))
         and (m0 * be == (1 - q) ** 2), 'lam_h=%s al=%s' % (lam, al))
    # ---- C16: F-stage contraction, instance level: chi(mh) <= (1-q)^2*dn2 -
    chi = mh * mh - p * mh + s
    tick('C16_Fcontract', chi <= (1 - q) ** 2 * (1 - p * p / (4 * s)),
         'chi=%s' % chi)
    res['chi_ratio'] = float(chi / ((1 - q) ** 2 * (1 - p * p / (4 * s))))
    if not (K.fullsupp and K.ctil_pos):
        res['skipped'] = 'x* not interior or ctil not > 0'
        return res, None, K
    recs, xs = K.run(T)                        # xs[t+1] = x_t
    E = [[K.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    word = ''.join(r['cls'] for r in recs)
    res['word'] = word

    def split(v):
        m = sum(v) / n
        return m, [v[i] - m for i in range(n)]

    Vs, Ls, Rs = {}, {}, {}
    for t in range(1, len(xs) - 1):            # e_{t-1}=E[t], e_t=E[t+1]
        Lm, hm = split(E[t]); L, h = split(E[t + 1])
        V = dot(h, h) - p * dot(h, hm) + s * dot(hm, hm)
        Vs[t], Ls[t] = V, L
        Rs[t] = None if L == 0 and Lm == 0 else (C_ta * V, dn_lb * wh2 * Lm * Lm)

    t_abs = None
    mxc, mxa = None, None
    for t in range(1, T - 1):
        em, e, en = E[t], E[t + 1], E[t + 2]
        Lm, hm = split(em); L, h = split(e); Ln, hn = split(en)
        rec = recs[t]
        r, ell, dt, ta = rec['r'], rec['ell'], rec['dt'], rec['ta']
        Delta, cls = rec['Delta'], rec['cls']
        # C1 master identity  (M+kap) e_{t+1} = kap (x* - ell)
        lhs = [K.Mv(en)[i] + kap * en[i] for i in range(n)]
        rhs = [kap * (K.xstar[i] - ell[i]) for i in range(n)]
        tick('C1_master', lhs == rhs)
        if cls == 'F':
            tick('C2_Fcollapse', ell == xs[t + 1] and
                 all((kap + lam) * hn[i] == kap * h[i] for i in range(n)) and
                 (kap + al) * Ln == kap * L)
        if cls == 'N':
            ok = all(v == 0 for v in r) and \
                all((kap + lam) * hn[i] == kap * ((1 + be) * h[i] - be * hm[i])
                    for i in range(n)) and \
                (kap + al) * Ln == kap * ((1 + be) * L - be * Lm)
            tick('C3_Nlinear', ok)
            V, Vn = Vs[t], Vs[t + 1]
            tick('C4_Vdecay', Vn == s * V)
            if Rs[t] and Rs[t + 1] and Rs[t][1] > 0:
                a1, b1 = Rs[t]; a2, b2 = Rs[t + 1]
                tick('C14_Rgeom', a2 * b1 * (1 - q) ** 2 <= s * a1 * b2)
        # C5 oscillation: |P_h r| <= beta |P_h d|
        _, rh = split(r); _, dh = split(dt)
        tick('C5_oscil', dot(rh, rh) <= be * be * dot(dh, dh))
        # C6 trigger characterisation
        Mta = K.Mv(ta)
        tick('C6_trigger', max(max((-v for v in Mta), default=Fr(0)),
                               Fr(0)) / al == Delta)
        # C7/C8 defect + Phi lower bound
        e2m = dd * dot(em, em); e2 = dd * dot(e, e)
        tick('C7_defect', rec['Dfin'] <= aq * (e2m - e2))
        tick('C8_philb', 2 * rec['Phi'] >= mu * e2)
        # C9 V-contraction at EVERY stage
        V, Vn = Vs[t], Vs[t + 1]
        if V > 0:
            tick('C9_Vcontract', Vn <= (1 - q) ** 2 * V,
                 'cls=%s t=%d ratio=%.6f' % (cls, t, float(Vn / V)))
            rt = Vn / V
            mxa = rt if mxa is None else max(mxa, rt)
            if cls != 'N':
                mxc = rt if mxc is None else max(mxc, rt)
        else:
            tick('C9_Vcontract', Vn == 0, 'V=0 but Vn=%s' % Vn)
        # C15 census + REPAIRED C17'/C9s from the clip identity (I6-B)
        if cls != 'N':
            mnd, mxd = min(dt), max(dt)
            clean = Delta <= be * mnd          # r = Delta*1  => P_h r = 0
            full = Delta >= be * mxd           # r = beta*d   => ell = x_t
            res.setdefault('corrclass', []).append(
                'CC' if clean else ('F' if full else 'P'))
            tick('C15_corrclass', True)        # census only (see docstring)
            phi = [max(be * dt[i] - Delta, Fr(0)) for i in range(n)]
            _, phih = split(phi)
            co = [hm[i] - (1 + be) / (2 * be) * h[i] for i in range(n)]
            X2, m2v = dot(co, co), dot(phih, phih)
            VF = s * (1 - mh) * dot(h, h)
            tgt = (1 - q) ** 2 * Vs[t]
            # proof bound at EVERY correcting stage
            tick('C9s_corr', Vs[t + 1] <= VF + mh * mh * be * be * X2,
                 't=%d cls=%s' % (t, cls))
            if not (clean or full):
                U2 = VF + mh * mh * (2 * be * sqrt_ub(X2 * m2v) - m2v)
                tick('C17_Pcert', U2 <= tgt,
                     't=%d U2/tgt=%.4f' % (t, float(U2 / tgt) if tgt else -1))
                res.setdefault('Pcert_ratio', []).append(
                    float(U2 / tgt) if tgt else None)
        # C10 low-mode floor
        tick('C10_lowfloor', L >= (1 - q) * Lm and L > 0)
        # C11 monotone lower certificate
        tick('C11_monotone', all(v >= 0 for v in dt) and all(v >= 0 for v in e))
        # absorption certificate
        if t_abs is None and Rs[t] and Rs[t][0] <= Rs[t][1] and \
                L >= (1 - q) * Lm:
            t_abs = t
    res['maxVratio_corr'] = float(mxc) if mxc is not None else None
    res['maxVratio_all'] = float(mxa) if mxa is not None else None
    res['margin9'] = float((1 - q) ** 2 - mxa) if mxa is not None else None
    res['t_abs'] = t_abs
    res['ncorr'] = sum(1 for c in word if c != 'N')
    if t_abs is not None:
        suffix_N = all(c == 'N' for c in word[t_abs:])
        frozen = all(recs[t]['gamma'] <= 1 for t in range(t_abs, T))
        tick('C13_absorb', suffix_N and frozen,
             'suffixN=%s frozen=%s' % (suffix_N, frozen))
        res['J_pre_abs'] = sum(math.log(recs[t]['gamma'])
                               for t in range(t_abs) if recs[t]['gamma'] > 1)
        res['J_total'] = sum(math.log(r['gamma'])
                             for r in recs if r['gamma'] > 1)
        # a-priori absorption-time bound from the measured contraction factor
        if mxa is not None and mxa < (1 - q) ** 2 and Rs[1] and Rs[1][1] > 0:
            th = float(mxa / (1 - q) ** 2)
            R1 = float(Rs[1][0] / Rs[1][1])
            res['t_abs_bound'] = (1 + math.ceil(math.log(max(R1, 1.0)) /
                                                math.log(1 / th))
                                  if th < 1 else None)
    else:
        tick('C13_absorb', False, 'certificate did not fire in T=%d' % T)
        res['J_total'] = sum(math.log(r['gamma'])
                             for r in recs if r['gamma'] > 1)
    return res, recs, K


# ------------------------------ family grid -------------------------------
def seeds_for(n, q):
    out = {}
    out['unif'] = [Fr(1, n)] * n
    out['skew'] = [Fr(1, 2)] + [Fr(1, 2 * (n - 1))] * (n - 1)
    tot = n * (n + 1) // 2
    out['ramp'] = [Fr(i + 1, tot) for i in range(n)]
    al = q * q / (1 + q * q)
    lam = al + (1 - al) * Fr(n, 2 * (n - 1))
    v = [Fr(1)] + [Fr(-1, n - 1)] * (n - 1)
    cv = 12
    vp = [(1 + (al + cv * q * q * lam * v[i]) / al) / (2 * n) for i in range(n)]
    if all(x > 0 for x in vp) and sum(vp) == 1:
        out['vpulse'] = vp
    # deterministic pseudo-random positive seed
    ws = [Fr(((7 * i * i + 3 * i + 5) % 11) + 1) for i in range(n)]
    S = sum(ws)
    out['prand'] = [w / S for w in ws]
    return out


if __name__ == '__main__':
    t0 = time.time()
    out, agg = [], {k: [0, 0] for k in KEYS}
    Ts = {Fr(1, 10): 26, Fr(1, 100): 44, Fr(1, 400): 90}
    grid = [(n, q, sn, rk) for n in (2, 4, 8, 16, 32)
            for q in (Fr(1, 10), Fr(1, 100), Fr(1, 400))
            for sn in ('unif', 'skew', 'ramp', 'vpulse', 'prand')
            for rk in ('safe', 'edge')]
    for (n, q, sn, rk) in grid:
        sd = seeds_for(n, q)
        if sn not in sd:
            continue
        seed = sd[sn]
        mn = min(seed)
        rho = mn / (2 * (n - 1)) if rk == 'safe' else \
            Fr(9, 10) * mn / (n - 1)
        nm = 'K%d q=1/%d %s/%s' % (n, int(1 / q), sn, rk)
        try:
            res, recs, K = analyze(nm, n, seed, q, rho, Ts[q])
        except AssertionError as ex:
            print('%-30s FACE-EXIT %s' % (nm, ex)); continue
        out.append(res)
        for k in KEYS:
            agg[k][0] += res['checks'][k][0]; agg[k][1] += res['checks'][k][1]
    # published families
    extra = [('K8 pulse (published)', 8,
              [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7, Fr(1, 10),
              Fr(1, 112), 20, Fr(1, 101)),
             ('K2 n=100 (published)', 2, [Fr(1, 2), Fr(1, 2)], Fr(1, 100),
              Fr(1, 16), 30, None)]
    for (nm, n, seed, q, rho, T, al) in extra:
        res, recs, K = analyze(nm, n, seed, q, rho, T, alpha=al)
        out.append(res)
        for k in KEYS:
            agg[k][0] += res['checks'][k][0]; agg[k][1] += res['checks'][k][1]

    print('=== I2-C K_n predicate battery: %d instances, %.1fs ===' %
          (len(out), time.time() - t0))
    for k in KEYS:
        a, b = agg[k]
        print('  %-14s %6d/%-6d %s' % (k, a, b, 'PASS' if a == b else 'FAIL'))
    bad = [r for r in out if r['fails']]
    print('instances with a failure: %d' % len(bad))
    for r in bad[:10]:
        print('  ', r['name'], r['fails'][:3])
    noabs = [r for r in out if r.get('t_abs') is None and 'skipped' not in r]
    print('instances where the absorption certificate did not fire: %d %s' %
          (len(noabs), [r['name'] for r in noabs][:6]))
    sk = [r for r in out if 'skipped' in r]
    print('skipped (non-interior x*): %d' % len(sk))
    live = [r for r in out if r.get('maxVratio_all') is not None]
    if live:
        w = max(live, key=lambda r: r['maxVratio_all'] / (1 - float(Fr(r['q']))) ** 2)
        print('worst C9 cell: %s  maxVratio_all=%.5f  (1-q)^2=%.5f margin=%.5f'
              % (w['name'], w['maxVratio_all'],
                 (1 - float(Fr(w['q']))) ** 2, w['margin9']))
        cc = [r for r in live if r['maxVratio_corr'] is not None]
        if cc:
            wc = max(cc, key=lambda r: r['maxVratio_corr'])
            print('worst correcting-stage V ratio: %s  %.5f (vs (1-q)^2=%.5f)'
                  % (wc['name'], wc['maxVratio_corr'],
                     (1 - float(Fr(wc['q']))) ** 2))
    print('max J_total over grid: %.5f (%s); max t_abs: %s' %
          (max(r.get('J_total', 0) for r in out),
           max(out, key=lambda r: r.get('J_total', 0))['name'],
           max((r.get('t_abs') or -1) for r in out)))
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i6b_knproof3_results.json', 'w'), indent=1, default=str)
    print('saved i6b_knproof3_results.json')
