"""I6-B step 2: genuinely-partial stages on GENERAL in-class graphs, with the
general clip identity and the two candidate C9' certificates.

General clip identity (D-inner products, P = D-orth projection off 1):
  ell_t = x_t + phi,  phi_i = (be*d_i - Delta)_+   [hat coords]
  h_{t+1} = Mm (h_t - phih)
  V_{t+1} = VF + |Mm phih|^2 - (1-be) <Mm h, Mm phih>,  VF = be<h, Mm(I-Mm)h>
  (1-q)^2 V_t - VF = be^2 m0 <co,Mm co> + be*Gslack,
      co = hm - ((1+be)/(2be)) h,   Gslack = m0|h|^2 - 2<h,Mm h> + |Mm h|^2

Route A (comonotone-kernel):  TK := <Mm phih, Mm(vh-phih)>_D >= 0  implies
  E_gen <= -|Mm phih|^2 + 2be<Mm phih, Mm co>  <= be^2 |Mm co|^2
  and be^2|Mm co|^2 <= be^2 m2 <co,Mm co> <= be^2 m0 <co,Mm co>  (margin m2/m0).
  TK >= 0 is PROVED under (H-K): (Mm^2)_ij <= m0^2 d_j / vol  for all i != j.
Route B (unconditional):
  E_gen <= m2^2(-m^2 + 2*be*X*m) + (1-be)*sqrt(spread_h * spread_phi),
      m = |phih|, X = |co|, spread_h = m2^2|h|^2 - |Mm h|^2,
      spread_phi = m2^2 m^2 - |Mm phih|^2.
"""
import sys, math, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i4a_half2 import (GenInst, complete_bipartite, hypercube, petersen, rook,
                       cocktail, cycle, circulant, sqrt_ub, spectral_bracket,
                       connected)
from engine import complete_graph, path_graph

def analyze_cell(name, adj, seed, q, rho, T, m2ex=None, brk=None, hk=None,
                 full_id_check=False):
    n = len(adj)
    I = GenInst(adj, seed, q, rho)
    if not (I.H0 and I.interior):
        return None, []
    al, be, kap, m0, d = I.alpha, I.beta, I.kappa, I.m0, I.d
    qq = Fr(q)
    nu = qq / (1 + qq)
    # certified m2 bracket
    if m2ex is not None:
        lam2 = al + (1 - al) * m2ex / 2
        m2lb = m2ub = kap / (kap + lam2)
    else:
        mu2lo, mu2hi = brk[0], brk[1]
        m2ub = kap / (kap + al + (1 - al) * mu2lo / 2)
        m2lb = kap / (kap + al + (1 - al) * mu2hi / 2)
    try:
        recs, xs = I.run(T, diag=False)
    except AssertionError:
        return None, []
    word = ''.join(r['cls'] for r in recs)
    E_ = [[I.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    vol = I.vol
    def split(u):
        L = sum(d[i] * u[i] for i in range(n)) / vol
        return L, [u[i] - L for i in range(n)]
    def Vform(u, v):
        Mv = I.Mmv(v)
        return I.dotD(u, u) - (1 + be) * I.dotD(u, Mv) + be * I.dotD(v, Mv)
    prec = []
    idfail = 0
    ts = range(1, T - 1) if full_id_check else \
        [t for t in range(1, T - 1) if recs[t]['cls'] == 'P']
    for t in ts:
        rec = recs[t]
        Delta, dt = rec['Delta'], rec['dt']
        Lm, hm = split(E_[t]); L, h = split(E_[t + 1]); Ln, hn = split(E_[t + 2])
        V, Vn = Vform(h, hm), Vform(hn, h)
        phi = [max(be * dt[i] - Delta, Fr(0)) for i in range(n)]
        _, phih = split(phi)
        co = [hm[i] - (1 + be) / (2 * be) * h[i] for i in range(n)]
        Mh, Mphi, Mco = I.Mmv(h), I.Mmv(phih), I.Mmv(co)
        H2, m2v, X2 = I.dotD(h, h), I.dotD(phih, phih), I.dotD(co, co)
        MH2, Mm2v, MX2 = I.dotD(Mh, Mh), I.dotD(Mphi, Mphi), I.dotD(Mco, Mco)
        VF = be * (I.dotD(h, Mh) - MH2)
        Egen = Mm2v - (1 - be) * I.dotD(Mh, Mphi)
        Y2 = I.dotD(co, Mco)
        Gslack = m0 * H2 - 2 * I.dotD(h, Mh) + MH2
        # identities
        okI3 = (Vn == VF + Egen)
        okI4 = ((1 - qq) ** 2 * V - VF == be * be * m0 * Y2 + be * Gslack)
        if not (okI3 and okI4):
            idfail += 1
        if rec['cls'] != 'P':
            continue
        vh = [be * co[i] + nu * h[i] for i in range(n)]
        Mvh = I.Mmv(vh)
        TK = I.dotD(Mphi, Mvh) - Mm2v      # <Mm phih, Mm(vh - phih)>_D
        tgt = (1 - qq) ** 2 * V
        # Route A certificates (valid if TK >= 0)
        UAex = VF - Mm2v + 2 * be * I.dotD(Mphi, Mco)
        UApr = VF + be * be * MX2
        # Route B (unconditional certified)
        sph = m2ub * m2ub * H2 - MH2       # spread_h  (>=0 by m2ub >= m2)
        spp = m2ub * m2ub * m2v - Mm2v     # spread_phi
        UB = VF + m2lb * m2lb * (-m2v) + \
            2 * be * m2ub * m2ub * sqrt_ub(X2 * m2v) + \
            (1 - be) * sqrt_ub(max(sph, Fr(0)) * max(spp, Fr(0)))
        # plain-metric truncation check (unconditional lemma)
        Tpl = I.dotD(phih, vh) - m2v
        nclip = sum(1 for i in range(n) if be * dt[i] > Delta)
        prec.append(dict(
            cell=name, n=n, q=str(qq), t=t, word=word[:t + 2],
            nclip=nclip, fclip=nclip / n,
            ratio=float(Vn / V) if V > 0 else None,
            rr_true=float(Vn / tgt) if V > 0 else None,
            TK_pos=bool(TK >= 0), TK=float(TK),
            Tplain_ok=bool(Tpl >= 0),
            m_Aex=float(UAex / tgt) if V > 0 else None,
            m_Apr=float(UApr / tgt) if V > 0 else None,
            m_B=float(UB / tgt) if V > 0 else None,
            ok_Aex=bool(UAex <= tgt), ok_Apr=bool(UApr <= tgt),
            ok_B=bool(UB <= tgt),
            m2_over_m0=float(m2ub / m0),
            Y2_vs_m2X2=float(m0 * Y2 / (m2ub * m2ub * X2)) if X2 > 0 else None,
            idok=bool(okI3 and okI4)))
    summ = dict(cell=name, n=n, q=str(qq), word=word, nP=word.count('P'),
                nF=word.count('F'), nC=word.count('C'), idfail=idfail)
    return summ, prec

def hk_check(I):
    """(H-K): (Mm^2)_ij <= m0^2 d_j / vol for all i != j. Exact."""
    n, m0, vol, d = I.n, I.m0, I.vol, I.d
    # Mm2 = Mm * Mm  exact
    worst = None
    ok = True
    for i in range(n):
        row = [sum(I.Mm[i][k] * I.Mm[k][j] for k in range(n)) for j in range(n)]
        for j in range(n):
            if i == j:
                continue
            lhs, rhs = row[j], m0 * m0 * d[j] / vol
            rat = lhs / rhs
            if worst is None or rat > worst:
                worst = rat
            if lhs > rhs:
                ok = False
    return ok, float(worst)

GRAPHS = {
    'K33': (complete_bipartite(3, 3), Fr(1)),
    'K24': (complete_bipartite(2, 4), Fr(1)),
    'Q3': (hypercube(3), Fr(2, 3)),
    'Q4': (hypercube(4), Fr(1, 2)),
    'Pet': (petersen(), Fr(2, 3)),
    'Rook3': (rook(3), Fr(3, 4)),
    'Cock3': (cocktail(3), Fr(1)),
    'Cock4': (cocktail(4), Fr(1)),
    'C6': (cycle(6), Fr(1, 2)),
    'Circ12': (circulant(12, (1, 2, 3)), None),
    'K8': (complete_graph(8), Fr(8, 7)),
}

def pulse_seed(n, w):
    w = Fr(w)
    return [w] + [(1 - w) / (n - 1)] * (n - 1)

if __name__ == '__main__':
    t0 = time.time()
    brkc, hkc = {}, {}
    allP, sums = [], []
    cells = []
    for gname, (adj, mu2) in GRAPHS.items():
        n = len(adj)
        if mu2 is not None:
            qs = [mu2 / 2, Fr(9, 10) * mu2 / 2, Fr(1, 2) * mu2 / 2,
                  Fr(51, 50) * mu2 / 2]          # eq, in, in, just-out
        else:
            qs = [Fr(1, 10), Fr(1, 20)]
        for q in qs:
            if q >= Fr(1, 2):
                q = Fr(93, 200)                  # keep alpha < 1/2 regime sane
            for w in ('0.6', '0.8'):
                sd = pulse_seed(n, Fr(w))
                mn = min(sd[i] / Fr(len(adj[i])) for i in range(n))
                for fr in (Fr(9, 10), Fr(99, 100)):
                    cells.append((gname, adj, mu2, sd, q, fr * mn, 20,
                                  '%s q=%s w=%s f=%s' % (gname, q, w, fr)))
    print('cells: %d' % len(cells))
    done = 0
    for (gname, adj, mu2, sd, q, rho, T, nm) in cells:
        if mu2 is None and gname not in brkc:
            brkc[gname] = spectral_bracket(adj)
        summ, prec = analyze_cell(nm, adj, sd, q, rho, T, m2ex=mu2,
                                  brk=brkc.get(gname),
                                  full_id_check=(done < 4))
        done += 1
        if summ:
            sums.append(summ)
            allP.extend(prec)
        if done % 30 == 0:
            print('  ... %d cells, %d P stages [%.0fs]' %
                  (done, len(allP), time.time() - t0))
    # (H-K) per (graph, q) for graphs that produced P stages + all graphs at
    # one representative q
    hk_results = {}
    for gname, (adj, mu2) in GRAPHS.items():
        q = (mu2 / 2 if mu2 is not None else Fr(1, 10))
        if q >= Fr(1, 2):
            q = Fr(93, 200)
        sd = pulse_seed(len(adj), Fr('0.6'))
        mn = min(sd[i] / Fr(len(adj[i])) for i in range(len(adj)))
        I = GenInst(adj, sd, q, Fr(9, 10) * mn)
        ok, worst = hk_check(I)
        # (H-band): m2^2 <= m0*m_min, certified via bracket
        if gname not in brkc:
            brkc[gname] = spectral_bracket(adj)
        mu2lo, mu2hi, _, muMhi = brkc[gname]
        if mu2 is not None:
            mu2lo = mu2hi = mu2
        al, kap, m0 = I.alpha, I.kappa, I.m0
        m2ub = kap / (kap + al + (1 - al) * mu2lo / 2)
        mminlb = kap / (kap + al + (1 - al) * muMhi / 2)
        hb = bool(m2ub * m2ub <= m0 * mminlb)
        hk_results[gname] = dict(q=str(q), HK=ok, HK_worst=worst, HB=hb,
                                 m2ub=float(m2ub), mminlb=float(mminlb))
        print('%-8s (H-K): %-5s worst=%.4f   (H-band): %s' %
              (gname, ok, worst, hb))
    print('\ncells run: %d; P stages: %d; identity failures: %d' %
          (len(sums), len(allP), sum(s['idfail'] for s in sums)))
    if allP:
        import statistics as st
        rt = [r['rr_true'] for r in allP]
        mB = [r['m_B'] for r in allP]
        mAp = [r['m_Apr'] for r in allP]
        tkpos = sum(1 for r in allP if r['TK_pos'])
        print('true ratio/(1-q)^2 : max %.4f mean %.4f  (#>1: %d)' %
              (max(rt), st.mean(rt), sum(1 for x in rt if x > 1)))
        print('TK >= 0 (route A valid): %d/%d' % (tkpos, len(allP)))
        print('Tplain >= 0 (lemma)    : %d/%d' %
              (sum(1 for r in allP if r['Tplain_ok']), len(allP)))
        print('route A proof bound    : max %.4f  #>1: %d' %
              (max(mAp), sum(1 for x in mAp if x > 1)))
        print('route A exact bound ok : %d/%d' %
              (sum(1 for r in allP if r['ok_Aex']), len(allP)))
        print('route B (uncond) bound : max %.4f  #>1: %d' %
              (max(mB), sum(1 for x in mB if x > 1)))
        okAll = sum(1 for r in allP if (r['TK_pos'] and r['ok_Aex']) or r['ok_B'])
        print('C17-prime (A|B disjunction) passes: %d/%d' % (okAll, len(allP)))
        for r in sorted(allP, key=lambda r: -(r['m_B'] or 0))[:8]:
            print('   %-28s t=%-2d rr=%.3f A:%s%.3f B:%.3f TK%s' %
                  (r['cell'], r['t'], r['rr_true'],
                   '+' if r['TK_pos'] else '-', r['m_Apr'], r['m_B'],
                   '+' if r['TK_pos'] else '-'))
    json.dump(dict(summaries=sums, pstages=allP, hk=hk_results),
              open('/home/claude/work/overnight/w7_windowed/i6b_cbattery.json',
                   'w'), indent=1, default=str)
    print('[%.1fs] saved i6b_cbattery.json' % (time.time() - t0))
