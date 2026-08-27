"""I6-B sanity: exact verification of the CLIP IDENTITY and the new C9' chain
on the K8 pulse (the one known genuinely-partial stage) and one grid cell.

Claims to verify at EVERY stage t>=1 (interior face, K_n):
  (I1) ell_t = x_t + phi_t,   phi_i = (be*d_i - Delta)_+
  (I2) h_{t+1} = mh*(h_t - phih),  phih = P_h phi   (P_h = mean-centering)
  (I3) V_{t+1} = VF + mh^2*E,  VF = s(1-mh)|h_t|^2,
       E = |phih|^2 - (1-be)<phih,h_t>
  (I4) (1-q)^2 V_t - VF = be*m0*s*|co|^2 + be*g*|h|^2,
       co = hm - ((1+be)/(2be)) h,  g = m0 - mh(2-mh)
  (I5) V_t = s|co|^2 + (1 - mh/m0)|h|^2
  (I6) be*d = be*dL*1 + be*co + nu*h,  nu = q/(1+q) = (1-be)/2
  (T)  truncation lemma: <P phi, v> >= |P phi|^2,  v := be*co + nu*h
  (B)  E <= -|phih|^2 + 2*be*<phih-dir...>: final E <= be^2 |co|^2
  (C9') V_{t+1} <= VF + mh^2*be^2*|co|^2 <= (1-q)^2 V_t   (needs g>=0, mh<=m0)
"""
import sys
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from kn_modal import KnModal

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def check(name, n, seed, q, rho, T, alpha=None):
    K = KnModal(n, seed, q, rho, alpha=alpha)
    al, kap, be, lam = K.alpha, K.kappa, K.beta, K.lam_h
    p, s, m0, mh = K.p, K.s, K.m0, K.mh
    qq = K.q
    nu = qq / (1 + qq)
    assert nu == (1 - be) / 2
    g = m0 - mh * (2 - mh)
    recs, xs = K.run(T)
    E_ = [[K.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    def split(v):
        m = sum(v) / n
        return m, [v[i] - m for i in range(n)]
    ok = {k: [0, 0] for k in ('I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'T', 'B', 'C9p', 'C9')}
    pstages = []
    for t in range(1, T - 1):
        rec = recs[t]
        Delta = rec['Delta']
        dt, ell = rec['dt'], rec['ell']
        Lm, hm = split(E_[t]); L, h = split(E_[t + 1]); Ln, hn = split(E_[t + 2])
        phi = [max(be * dt[i] - Delta, Fr(0)) for i in range(n)]
        phL, phih = split(phi)
        co = [hm[i] - (1 + be) / (2 * be) * h[i] for i in range(n)]
        X2 = dot(co, co); H2 = dot(h, h)
        V = dot(h, h) - p * dot(h, hm) + s * dot(hm, hm)
        Vn = dot(hn, hn) - p * dot(hn, h) + s * dot(h, h)
        VF = s * (1 - mh) * H2
        Evar = dot(phih, phih) - (1 - be) * dot(phih, h)
        v = [be * co[i] + nu * h[i] for i in range(n)]
        def tick(key, cond):
            ok[key][1] += 1
            if cond: ok[key][0] += 1
            else: print('  FAIL %s at t=%d (%s)' % (key, t, rec['cls']))
        tick('I1', all(ell[i] == xs[t + 1][i] + phi[i] for i in range(n)))
        tick('I2', all((kap + lam) * hn[i] == kap * (h[i] - phih[i]) for i in range(n)))
        tick('I3', Vn == VF + mh * mh * Evar)
        tick('I4', (1 - qq) ** 2 * V - VF == be * m0 * s * X2 + be * g * H2)
        tick('I5', V == s * X2 + (1 - mh / m0) * H2)
        dL, dh = split(dt)
        tick('I6', all(be * dt[i] == be * dL + be * co[i] + nu * h[i] for i in range(n)))
        covv = dot(phih, v)   # = <P phi, v> since v centered? v = be co + nu h centered: yes
        tick('T', covv >= dot(phih, phih))
        # final bound E <= be^2 X^2 via E <= -m^2+2be m X <= be^2 X^2:
        # verify E <= be^2 X2 directly (rational, no sqrt needed on this side)
        tick('B', Evar <= be * be * X2)
        tick('C9p', Vn <= VF + mh * mh * be * be * X2)
        if V > 0:
            tick('C9', Vn <= (1 - qq) ** 2 * V)
        if rec['cls'] == 'P':
            pstages.append((t, float(Vn / V) if V else None,
                            float((VF + mh*mh*be*be*X2) / ((1-qq)**2*V)) if V else None))
    print('%s: word=%s' % (name, ''.join(r['cls'] for r in recs)[:20]))
    for k, (a, b) in ok.items():
        print('   %-4s %d/%d %s' % (k, a, b, 'OK' if a == b else '** FAIL **'))
    if pstages:
        print('   P stages (t, trueV-ratio, newcert-margin):', pstages)
    return ok, pstages

seed = [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7
check('K8 pulse', 8, seed, Fr(1, 10), Fr(1, 112), 14, alpha=Fr(1, 101))
check('K16 vpulse-ish', 16,
      None or [Fr(1, 32)] * 8 + [Fr(3, 32)] * 8, Fr(1, 50), Fr(1, 2 * 16 * 15), 20)
check('K4 skew', 4, [Fr(1, 2), Fr(1, 6), Fr(1, 6), Fr(1, 6)], Fr(1, 4),
      Fr(1, 40), 20)
