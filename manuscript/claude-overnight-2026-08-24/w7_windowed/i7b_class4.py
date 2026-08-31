"""I7-B phase 8: class battery rerun extended with the master-form checks.

Per stage t >= 1 (exact rationals):
  C9M_id : Psi_master(y_t, h_t) == V_{t+1} - (1-q)^2 V_t   (identity)
  C9M_neg: Psi_master <= 0                                  (= C9, restated)
  C9F    : sup_h Psi(y_t, h) <= 0  with h* = nu S^{-1} l'   (free-h version:
           even the adversarial h could not break C9 at this stage's y)
C9F is checked in class only (S PD needs mu_2 >= 2q).
"""
import sys, time, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import GenInst, CASES, spectral_bracket
from i7b_tk import proj, dotD

def exact_solve(Arows, brhs):
    n = len(Arows)
    M = [row[:] + [brhs[i]] for i, row in enumerate(Arows)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [M[r][t] - f * M[c][t] for t in range(n + 1)]
    return [M[i][n] for i in range(n)]

def run_case(nm, adj, seed, q, rho, T, mu2b):
    n = len(adj)
    I = GenInst(adj, seed, q, rho)
    if not (I.H0 and I.interior):
        return None
    d, vol, be, m0 = I.d, I.vol, I.beta, I.m0
    qq = I.q
    nu = qq / (1 + qq)
    in_class = mu2b >= 2 * qq
    recs, xs = I.run(T, diag=False)
    E = [[I.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    M = I.Mm
    def Mv(u): return I.Mmv(u)
    def Vf(u, v):
        Mvv = Mv(v)
        return dotD(d, u, u) - (1 + be) * dotD(d, u, Mvv) + be * dotD(d, v, Mvv)
    def psi_master(y, h):
        z = proj(d, vol, y)
        b = [z[i] - nu * h[i] for i in range(n)]
        ym = [max(-v, Fr(0)) for v in y]
        w = proj(d, vol, ym)
        bw = [b[i] + w[i] for i in range(n)]
        Mbw, Mb, Mh = Mv(bw), Mv(b), Mv(h)
        return (dotD(d, Mbw, Mbw) - m0 * dotD(d, b, Mb)
                - nu * nu * dotD(d, Mh, Mh)
                - be * (m0 * dotD(d, h, h) - 2 * dotD(d, h, Mh)
                        + dotD(d, Mh, Mh)))
    # exact S-solve setup (for C9F): S = nu^2 m0 M + be(m0 I - 2M + M^2)
    M2 = [[sum(M[i][k] * M[k][j] for k in range(n)) for j in range(n)]
          for i in range(n)]
    S = [[nu * nu * m0 * M[i][j]
          + be * ((m0 if i == j else 0) - 2 * M[i][j] + M2[i][j])
          + d[j] / vol for j in range(n)] for i in range(n)]
    cnt = {k: [0, 0] for k in ('C9M_id', 'C9M_neg', 'C9F')}
    for t in range(1, T - 1):
        rec = recs[t]
        h = proj(d, vol, E[t + 1])
        hm = proj(d, vol, E[t])
        y = [be * rec['dt'][i] - rec['Delta'] for i in range(n)]
        Psi = psi_master(y, h)
        V, Vn = Vf(h, hm), Vf(proj(d, vol, E[t + 2]), h)
        cnt['C9M_id'][1] += 1
        cnt['C9M_id'][0] += (Psi == Vn - (1 - qq) ** 2 * V)
        if in_class:
            cnt['C9M_neg'][1] += 1
            cnt['C9M_neg'][0] += (Psi <= 0)
            # C9F: h* = nu S^{-1} l',  l' = M(m0-M) z - M^2 P y_-
            z = proj(d, vol, y)
            ym = [max(-v, Fr(0)) for v in y]
            w = proj(d, vol, ym)
            Mz = Mv(z)
            MMz = Mv(Mz)
            lp = [m0 * Mz[i] - MMz[i] - Mv(Mv(w))[i] for i in range(n)]
            hs = exact_solve(S, [nu * l for l in lp])
            hs = proj(d, vol, hs)
            PsiF = psi_master(y, hs)
            cnt['C9F'][1] += 1
            cnt['C9F'][0] += (PsiF <= 0 and PsiF >= Psi)
    return dict(name=nm, in_class=in_class, cnt=cnt,
                word=''.join(r['cls'] for r in recs))

if __name__ == '__main__':
    t0 = time.time()
    agg = {k: [0, 0] for k in ('C9M_id', 'C9M_neg', 'C9F')}
    brkcache = {}
    try:
        _old = {r['name']: r for r in json.load(
            open('/home/claude/work/overnight/w7_windowed/i4a_half2.json'))}
    except Exception:
        _old = {}
    out = []
    nin = 0
    for (nm, adj, seed, q, rho, T, mu2) in CASES:
        key = id(adj)
        if key not in brkcache:
            if mu2 is not None:
                brkcache[key] = mu2
            elif nm in _old and 'mu2_lo' in _old[nm]:
                brkcache[key] = Fr(_old[nm]['mu2_lo'])
            else:
                brkcache[key] = spectral_bracket(adj)[0]
        try:
            r = run_case(nm, adj, seed, q, rho, T, brkcache[key])
        except AssertionError:
            continue
        if r is None:
            continue
        out.append(r)
        nin += r['in_class']
        for k in agg:
            agg[k][0] += r['cnt'][k][0]
            agg[k][1] += r['cnt'][k][1]
        bad = [k for k in agg if r['cnt'][k][0] != r['cnt'][k][1]]
        if bad:
            print('  %-24s FAIL %s %s' % (r['name'], bad,
                                          {k: r['cnt'][k] for k in bad}))
    print('=== I7-B extended class battery: %d instances (%d in class) ===' %
          (len(out), nin))
    for k in agg:
        a, b = agg[k]
        print('  %-8s %5d/%-5d %s' % (k, a, b, 'PASS' if a == b else 'FAIL'))
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i7b_class4.json', 'w'), indent=1, default=str)
    print('[%.0fs] saved i7b_class4.json' % (time.time() - t0))
