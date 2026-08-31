"""I6-B step 1: a battery of GENUINELY PARTIAL correction stages on K_n.

Families tuned to produce P stages (Delta strictly inside (be*min d, be*max d)):
  * kblock(n,k,w): k-coordinate heavy block seed  (K8 pulse = kblock(8,1,.558))
  * pulse perturbations: n=8-ish, w near .558, rho near the (H0) edge, q varied
  * 3-level seeds
  * vpulse(cv): high-eigenvector pulse seeds
All exact (Fractions).  For each P stage record exact energies, clip data,
margins of the OLD certified bound (knproof2 C17) and the NEW one (C9').

NEW C9' chain (proved in i6b_c9_closure.md; verified in i6b_sanity.py):
  V_{t+1} = VF + mh^2*E,  VF = s(1-mh)|h|^2,  E = |phih|^2-(1-be)<phih,h>
  E <= -|phih|^2 + 2*be*<phih,co>  <= be^2|co|^2
  => V_{t+1} <= VF + mh^2 be^2 |co|^2 <= (1-q)^2 V_t   iff  g>=0 (q<=1/2)
Margin law:  V_{t+1}/((1-q)^2 V_t) <= max(theta_F, mh/m0),
  theta_F = mh(1-mh)/(m0-mh).
"""
import sys, math, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from kn_modal import KnModal

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def sqrt_ub(X):
    if X <= 0:
        return Fr(0)
    S = 10 ** 20
    r = math.isqrt(X.numerator * S * S * X.denominator) // X.denominator + 1
    return Fr(r, S)

def analyze_cell(name, n, seed, q, rho, T, alpha=None):
    """Run one K_n cell; return (summary, list of P-stage records)."""
    try:
        K = KnModal(n, seed, q, rho, alpha=alpha)
    except AssertionError:
        return None, []
    if not (K.fullsupp and K.ctil_pos):
        return None, []
    al, kap, be, lam = K.alpha, K.kappa, K.beta, K.lam_h
    p, s, m0, mh = K.p, K.s, K.m0, K.mh
    qq = K.q
    nu = qq / (1 + qq)
    g = m0 - mh * (2 - mh)
    thF = mh * (1 - mh) / (m0 - mh)
    law = max(thF, mh / m0)
    try:
        recs, xs = K.run(T)
    except AssertionError:
        return None, []
    E_ = [[K.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    def split(v):
        m = sum(v) / n
        return m, [v[i] - m for i in range(n)]
    word = ''.join(r['cls'] for r in recs)
    prec = []
    idfail = 0
    for t in range(1, T - 1):
        rec = recs[t]
        if rec['cls'] != 'P':
            continue
        Delta, dt = rec['Delta'], rec['dt']
        Lm, hm = split(E_[t]); L, h = split(E_[t + 1]); Ln, hn = split(E_[t + 2])
        phi = [max(be * dt[i] - Delta, Fr(0)) for i in range(n)]
        _, phih = split(phi)
        co = [hm[i] - (1 + be) / (2 * be) * h[i] for i in range(n)]
        X2, H2, m2v = dot(co, co), dot(h, h), dot(phih, phih)
        V = dot(h, h) - p * dot(h, hm) + s * dot(hm, hm)
        Vn = dot(hn, hn) - p * dot(hn, h) + s * dot(h, h)
        VF = s * (1 - mh) * H2
        Ev = m2v - (1 - be) * dot(phih, h)
        # exact identity re-check
        if Vn != VF + mh * mh * Ev:
            idfail += 1
        # OLD certificate (knproof2 C17 formula)
        _, dh = split(dt)
        ta = [(1 + be) * h[i] - be * hm[i] for i in range(n)]  # tah
        A = sqrt_ub(dot(ta, ta))
        mnd = min(dt); eps = Delta - be * mnd
        Ku = min(be * sqrt_ub(dot(dh, dh)), sqrt_ub(Fr(n) * eps * eps / 4))
        H = sqrt_ub(H2)
        Uold = mh * mh * (A + Ku) ** 2 + p * mh * (A + Ku) * H + s * H * H
        # NEW certificates
        U1 = VF + mh * mh * be * be * X2                       # proof bound
        U2 = VF + mh * mh * (2 * be * sqrt_ub(X2 * m2v) - m2v) # at actual |phih|
        tgt = (1 - qq) ** 2 * V
        nclip = sum(1 for i in range(n) if be * dt[i] > Delta)
        mxd, rng = max(dt), max(dt) - min(dt)
        lampos = float((Delta - be * mnd) / (be * rng)) if rng > 0 else None
        cvh = float(dot(phih, h)) / (math.sqrt(float(m2v)) * math.sqrt(float(H2))) \
            if m2v > 0 and H2 > 0 else 0.0
        prec.append(dict(
            cell=name, n=n, q=str(qq), rho=str(rho), t=t, word=word[:t + 2],
            nclip=nclip, fclip=nclip / n, lampos=lampos,
            V=str(V), Vn=str(Vn),
            ratio=float(Vn / V) if V > 0 else None,
            rr_true=float(Vn / tgt) if V > 0 else None,
            m_old=float(Uold / tgt) if V > 0 else None,
            m_new1=float(U1 / tgt) if V > 0 else None,
            m_new2=float(U2 / tgt) if V > 0 else None,
            law=float(law), thF=float(thF), mh_m0=float(mh / m0),
            X2_over_V=float(s * X2 / V) if V > 0 else None,
            H2_over_V=float((1 - mh / m0) * H2 / V) if V > 0 else None,
            cos_phih_h=cvh,
            cov_phi_h_sign=(1 if dot(phih, h) > 0 else (-1 if dot(phih, h) < 0 else 0)),
            E_neg=bool(Ev <= 0),
            ok_old=bool(Uold <= tgt), ok_new1=bool(U1 <= tgt),
            ok_new2=bool(U2 <= tgt), ok_true=bool(Vn <= tgt)))
    summ = dict(cell=name, n=n, q=str(qq), word=word,
                nP=word.count('P'), nF=word.count('F'),
                nC=sum(1 for t in range(1, T - 1)
                       if recs[t]['cls'] not in 'NPF'), idfail=idfail)
    return summ, prec

# ------------------------------------------------------------ seed families
def kblock(n, k, w):
    return [Fr(w).limit_denominator(10 ** 6) / k] * k + \
           [(1 - Fr(w).limit_denominator(10 ** 6)) / (n - k)] * (n - k)

def three_level(n, w1, k2, w2):
    w1, w2 = Fr(w1).limit_denominator(10 ** 6), Fr(w2).limit_denominator(10 ** 6)
    rest = (1 - w1 - w2) / (n - 1 - k2)
    return [w1] + [w2 / k2] * k2 + [rest] * (n - 1 - k2)

def vpulse(n, q, cv):
    al = q * q / (1 + q * q)
    lam = al + (1 - al) * Fr(n, 2 * (n - 1))
    v = [Fr(1)] + [Fr(-1, n - 1)] * (n - 1)
    sd = [(1 + (al + cv * q * q * lam * v[i]) / al) / (2 * n) for i in range(n)]
    return sd if all(x > 0 for x in sd) and sum(sd) == 1 else None

if __name__ == '__main__':
    t0 = time.time()
    cells = []
    # (a) kblock scan
    for n in (4, 6, 8, 12, 16, 24):
        for q in (Fr(1, 4), Fr(1, 6), Fr(1, 10), Fr(1, 20), Fr(1, 50)):
            for k in sorted({1, 2, n // 4, n // 2} - {0}):
                for w in ('0.35', '0.5', '0.65', '0.8'):
                    if Fr(w) <= Fr(k, n):
                        continue
                    sd = kblock(n, k, Fr(w))
                    for fr, tag in ((Fr(9, 10), 'e'), (Fr(99, 100), 'x')):
                        cells.append(('K%d q=%s kb(%d,%s)%s' % (n, q, k, w, tag),
                                      n, sd, q, fr * min(sd) / (n - 1), 22, None))
    # (b) K8-pulse perturbations
    for q, alp in ((Fr(1, 8), None), (Fr(1, 10), Fr(1, 101)), (Fr(1, 12), None),
                   (Fr(1, 16), None)):
        for w in ('0.50', '0.54', '0.558', '0.57', '0.62', '0.70'):
            sd = kblock(8, 1, Fr(w))
            for rho in (Fr(1, 90), Fr(1, 112), Fr(1, 150), Fr(1, 200)):
                cells.append(('K8pul q=%s w=%s r=%s' % (q, w, rho), 8, sd, q,
                              rho, 20, alp))
    # (c) 3-level
    for n in (8, 12, 16):
        for q in (Fr(1, 10), Fr(1, 20)):
            for (w1, k2, w2) in (('0.5', 2, '0.3'), ('0.4', 3, '0.4'),
                                 ('0.6', 2, '0.25'), ('0.45', n // 2 - 1, '0.35')):
                sd = three_level(n, w1, k2, w2)
                if min(sd) <= 0:
                    continue
                for fr in (Fr(9, 10), Fr(99, 100)):
                    cells.append(('K%d q=%s 3lv(%s,%d,%s)' % (n, q, w1, k2, w2),
                                  n, sd, q, fr * min(sd) / (n - 1), 22, None))
    # (d) vpulse big-cv
    for n in (8, 16, 32):
        for q in (Fr(1, 10), Fr(1, 20), Fr(1, 50)):
            for cv in (12, 40, 100, 300):
                sd = vpulse(n, q, cv)
                if sd is None:
                    continue
                for fr in (Fr(1, 2), Fr(9, 10)):
                    cells.append(('K%d q=%s vp%d f=%s' % (n, q, cv, fr), n, sd,
                                  q, fr * min(sd) / (n - 1), 22, None))

    allP, sums = [], []
    for (nm, n, sd, q, rho, T, alp) in cells:
        summ, prec = analyze_cell(nm, n, sd, q, rho, T, alpha=alp)
        if summ:
            sums.append(summ)
            allP.extend(prec)
    nid = sum(s['idfail'] for s in sums)
    print('cells run: %d  (of %d);  identity failures: %d' %
          (len(sums), len(cells), nid))
    print('P stages found: %d   (cells with >=1 P: %d)' %
          (len(allP), sum(1 for s in sums if s['nP'] > 0)))
    print('F stages: %d   CC stages: %d' %
          (sum(s['nF'] for s in sums), sum(s['nC'] for s in sums)))
    if allP:
        import statistics as st
        mo = [r['m_old'] for r in allP if r['m_old'] is not None]
        m1 = [r['m_new1'] for r in allP]
        m2 = [r['m_new2'] for r in allP]
        rt = [r['rr_true'] for r in allP]
        law = [r['law'] for r in allP]
        print('\nMARGIN SUMMARY over %d P stages' % len(allP))
        print('  true  V+/((1-q)^2 V): max %.4f  mean %.4f' % (max(rt), st.mean(rt)))
        print('  OLD cert margin     : max %.4f  mean %.4f  #>1 (FAIL): %d' %
              (max(mo), st.mean(mo), sum(1 for x in mo if x > 1)))
        print('  NEW U1 (proof bound): max %.4f  mean %.4f  #>1: %d' %
              (max(m1), st.mean(m1), sum(1 for x in m1 if x > 1)))
        print('  NEW U2 (actual m)   : max %.4f  mean %.4f  #>1: %d' %
              (max(m2), st.mean(m2), sum(1 for x in m2 if x > 1)))
        print('  law max(thF,mh/m0)  : max %.4f   (U1<=law: %d/%d)' %
              (max(law), sum(1 for r in allP if r['m_new1'] <= r['law'] + 1e-15),
               len(allP)))
        viol = [r for r in allP if not r['ok_new1']]
        print('  C9-prime violations: %d' % len(viol))
        worst = max(allP, key=lambda r: r['m_new1'])
        print('  worst NEW-U1 stage: %s t=%d  m_new1=%.4f law=%.4f nclip=%d/%d'
              % (worst['cell'], worst['t'], worst['m_new1'], worst['law'],
                 worst['nclip'], worst['n']))
        wo = max(allP, key=lambda r: r['m_old'])
        print('  worst OLD stage   : %s t=%d  m_old=%.4f (true %.4f)'
              % (wo['cell'], wo['t'], wo['m_old'], wo['rr_true']))
    json.dump(dict(summaries=sums, pstages=allP),
              open('/home/claude/work/overnight/w7_windowed/i6b_pbattery.json',
                   'w'), indent=1, default=str)
    print('\n[%.1fs] saved i6b_pbattery.json' % (time.time() - t0))
