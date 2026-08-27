"""I6-A1: never-triggering lemma -- induction/comparison route, exact checks.

Trigger predicate (verbatim from engine.py:149-159 / i5c_core.py:136-171):
    dh = x_t - x_{t-1};  ah = x_t + beta_t*dh;  S = supp(ah)
    for i in S:  zt_i = ct_i - (Qt ah)_i        (lower residual)
    Delta_t = max(0, max_{i in S, zt<0} -zt_i/dv_i),  dv_i > 0
  => Delta_t = 0  <=>  zeta(a_t)_i >= 0 for all i in supp(a_t)
     (subsolution-on-support; denominator-free).

Reduction (exact, any faces, exact solves): on supp(x_{t+1}),
    ct_i - (Qt x_{t+1})_i = kap d_i (x_{t+1} - ell_t)_i        [KKT]
so if stage t never fired (ell_t = a_t) and supp(a_{t+1}) = supp(x_{t+1}):
    zeta(a_{t+1})_i = kap d_i (d_{t+1} - beta_t d_t)_i - beta_{t+1}(Qt d_{t+1})_i
and never-fire at t+1  <=>  this is >= 0 on S_{t+1}.        (T-gen')

Same face S, two consecutive interior solves, constant beta:
    d_{t+1} = M_S[(1+b)d_t - b d_{t-1}],  M_S = (Qt_S+kapD_S)^{-1} kapD_S >= 0
    (T-gen') <=> (1+b)d_{t+1} - b(2+b)d_t + b^2 d_{t-1} >= 0        (T)
and [d_t <= d_{t-1}] + [d_{t+1} >= (1-qr)d_t]  ==>  (T)   exactly, since
    b(2+b)-b^2 = 2b and 2b/(1+b) = 1-qr.

This script verifies, per stage, in exact Fractions:
  NF     Delta == 0
  KKT    the KKT identity above on supp(x_{t+1})
  TRIGID the (T-gen') formula reproduces zeta(a_{t+1}) exactly
  SWU    d_{t+1} <= d_t componentwise   [same-face pair / change pair old/new]
  SWL    d_{t+1} >= (1-qr_{t+1}) d_t    [same split]
  TT     (T) three-term inequality with the stage's betas (same-face triples)
  MC     M_S d_t >= (1-qr^2) d_t on S_t     (alignment cone)
  MCU    M_S u_t >= (1-qr^2) u_t (same-face; u_t = (1+b)d_t - b_prev d_{t-1})
  DF     delta-floor: delta_{t+1} >= ((1-qr)/2) delta_t, delta = d_{t-1}-d_t
  NEWNEG at face-change stages, (Qt d_{t+1})_i <= 0 on entering coords
Margins are tracked as rationals (reported as floats).
"""
import sys, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, star_graph, complete_graph, _gauss
from i5c_core import run_i5c


def caterpillar(m, k):
    n = m + m * k
    adj = [[] for _ in range(n)]

    def ae(a, b):
        adj[a].append(b); adj[b].append(a)
    for i in range(m - 1):
        ae(i, i + 1)
    for i in range(m):
        for j in range(k):
            ae(i, m + i * k + j)
    return [sorted(a) for a in adj]


def btree(depth):
    n = 2 ** (depth + 1) - 1
    adj = [[] for _ in range(n)]
    for i in range(n):
        for c in (2 * i + 1, 2 * i + 2):
            if c < n:
                adj[i].append(c); adj[c].append(i)
    return [sorted(a) for a in adj]


def random_tree(n, seed):
    import random
    rnd = random.Random(seed)
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        u = rnd.randrange(v)
        adj[u].append(v); adj[v].append(u)
    return [sorted(a) for a in adj]


CELLS = {
    'P24': (path_graph(24), [Fr(1)] + [Fr(0)] * 23, Fr(1, 32), Fr(65, 4096), 400),
    'P16': (path_graph(16), [Fr(1)] + [Fr(0)] * 15, Fr(1, 24), Fr(1, 32), 250),
    'P20': (path_graph(20), [Fr(1)] + [Fr(0)] * 19, Fr(1, 32), Fr(7, 256), 250),
    'P12': (path_graph(12), [Fr(1)] + [Fr(0)] * 11, Fr(1, 20), Fr(5, 128), 200),
    'cat5_2': (caterpillar(5, 2), [Fr(1)] + [Fr(0)] * 14, Fr(1, 20), Fr(5, 128), 200),
    'S16': (star_graph(16), [Fr(0), Fr(1)] + [Fr(0)] * 14, Fr(1, 20), Fr(5, 128), 150),
    'P18': (path_graph(18), [Fr(1)] + [Fr(0)] * 17, Fr(1, 24), Fr(11, 512), 200),
    'cat4_3': (caterpillar(4, 3), [Fr(1)] + [Fr(0)] * 15, Fr(1, 24), Fr(9, 256), 200),
    'bt15': (btree(3), [Fr(1)] + [Fr(0)] * 14, Fr(1, 20), Fr(3, 64), 200),
    # negative control (interior face; corrections known to fire)
    'K8ctl': (complete_graph(8), [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7,
              Fr(1, 10), Fr(1, 112), 16),
    # fresh instances (screened by driver): filled in below
    'P24rho2': (path_graph(24), [Fr(1)] + [Fr(0)] * 23, Fr(1, 32), Fr(15, 1024), 250),
    'P24rho3': (path_graph(24), [Fr(1)] + [Fr(0)] * 23, Fr(1, 32), Fr(17, 1024), 250),
    'rt18': (random_tree(18, 5), [Fr(1)] + [Fr(0)] * 17, Fr(1, 20), Fr(5, 128), 200),
    'rt16b': (random_tree(16, 11), [Fr(0)] * 3 + [Fr(1)] + [Fr(0)] * 12, Fr(1, 24),
              Fr(3, 128), 200),
}


def msolve(Qt, dvec, kap, S, rhs_vec):
    """Solve (Qt_S + kap D_S) y = kap D_S rhs  on face S; return dict i->y_i."""
    idx = list(S)
    A = [[Qt[i][j] + (kap * dvec[i] if i == j else 0) for j in idx] for i in idx]
    b = [kap * dvec[i] * rhs_vec[i] for i in idx]
    y = _gauss(A, b)
    return {i: v for i, v in zip(idx, y)}


def check_cell(name, T_override=None):
    adj, seed, q, rho, T = CELLS[name]
    if T_override:
        T = T_override
    I = Inst(adj, seed, q, rho)
    n = I.n
    proper = 0 < len(I.Sstar) < n
    t0 = time.time()
    recs = run_i5c(I, T, variant='fm')
    kap, d, Qt, ct = I.kappa, I.d, I.Qt, I.ct

    def QtV(v):
        return [sum(Qt[i][j] * v[j] for j in range(n) if v[j] != 0)
                for i in range(n)]

    C = {k: [0, 0] for k in
         ('NF', 'KKT', 'TRIGID', 'SWU_same', 'SWL_same', 'SWU_chg_old',
          'SWL_chg_old', 'SWU_chg_new', 'TT_same', 'MC', 'MCU', 'DF_same',
          'NEWNEG', 'SUPPA')}
    worst = dict(SWL_same=None, SWU_same=None, MC=None, MCU=None, DF=None,
                 TT=None, TGEN=None)
    fails = []

    def upd(key, val):
        worst[key] = val if worst[key] is None else min(worst[key], val)

    for t in range(len(recs)):
        r = recs[t]
        S, x, xn, dh, ell, be, qr = (r['S'], r['x'], r['xn'], r['dh'],
                                     r['ell'], r['beta'], r['qr'])
        C['NF'][1] += 1
        C['NF'][0] += (r['Delta'] == 0)
        if r['Delta'] != 0:
            fails.append(('NF', t))
        dnext = [xn[i] - x[i] for i in range(n)]
        # KKT on supp(xn)
        Qxn = QtV(xn)
        ok = all(ct[i] - Qxn[i] == kap * d[i] * (xn[i] - ell[i])
                 for i in range(n) if xn[i] > 0)
        C['KKT'][1] += 1
        C['KKT'][0] += ok
        if not ok:
            fails.append(('KKT', t))
        if t + 1 < len(recs):
            rn = recs[t + 1]
            Sn, ben = rn['S'], rn['beta']
            qrn = rn['qr']
            # supp(a_{t+1}) subset supp(x_{t+1})?
            ok = all(xn[i] > 0 for i in Sn)
            C['SUPPA'][1] += 1
            C['SUPPA'][0] += ok
            # TRIGID: zeta(a_{t+1}) == kapD(xn-ell) - ben*Qt dnext on Sn
            Qdn = QtV(dnext)
            an = rn['ah']
            Qan = QtV(an)
            ok = all(ct[i] - Qan[i] ==
                     kap * d[i] * (xn[i] - ell[i]) - ben * Qdn[i] for i in Sn)
            C['TRIGID'][1] += 1
            C['TRIGID'][0] += ok
            if not ok:
                fails.append(('TRIGID', t + 1))
            tg = min((kap * d[i] * (xn[i] - ell[i]) - ben * Qdn[i]
                      for i in Sn), default=Fr(0))
            upd('TGEN', float(tg))
            samef = (Sn == S)
            newc = [i for i in Sn if i not in S]
            oldc = [i for i in Sn if i in S]
            # sandwich on the pair (d_t=dh, d_{t+1}=dnext)
            if any(v != 0 for v in dh) or any(v != 0 for v in dnext):
                if samef:
                    okU = all(dnext[i] <= dh[i] for i in range(n))
                    okL = all(dnext[i] >= (1 - qrn) * dh[i] for i in range(n))
                    C['SWU_same'][1] += 1; C['SWU_same'][0] += okU
                    C['SWL_same'][1] += 1; C['SWL_same'][0] += okL
                    if not okU:
                        fails.append(('SWU_same', t + 1))
                    if not okL:
                        fails.append(('SWL_same', t + 1))
                    for i in range(n):
                        if dh[i] > 0:
                            upd('SWU_same', float(dnext[i] / dh[i]))
                            upd('SWL_same', float(dnext[i] / dh[i]))
                else:
                    okU = all(dnext[i] <= dh[i] for i in oldc)
                    okL = all(dnext[i] >= (1 - qrn) * dh[i] for i in oldc)
                    C['SWU_chg_old'][1] += 1; C['SWU_chg_old'][0] += okU
                    C['SWL_chg_old'][1] += 1; C['SWL_chg_old'][0] += okL
                    okUn = all(dnext[i] <= dh[i] for i in newc)
                    C['SWU_chg_new'][1] += 1; C['SWU_chg_new'][0] += okUn
                    if newc:
                        C['NEWNEG'][1] += 1
                        C['NEWNEG'][0] += all(Qdn[i] <= 0 for i in newc)
            # MC alignment at stage t (face S, d_t = dh) -- needs supp(dh)<=S
            if S and any(dh[i] != 0 for i in S) and \
                    all(dh[i] == 0 for i in range(n) if i not in S):
                y = msolve(Qt, d, kap, S, dh)
                thr = 1 - qr * qr
                ok = all(y[i] >= thr * dh[i] for i in S)
                C['MC'][1] += 1
                C['MC'][0] += ok
                if not ok:
                    fails.append(('MC', t))
                for i in S:
                    if dh[i] > 0:
                        upd('MC', float(y[i] / dh[i] / thr))
        # same-face triple checks need t-1
        if t >= 1 and t + 1 < len(recs):
            rp = recs[t - 1]
            if rp['S'] == S == recs[t + 1]['S'] and S:
                bep = rp['beta']
                dprev = rp['dh']
                ben = recs[t + 1]['beta']
                # (T) with per-stage betas:
                # (1+ben)d_{t+1} - [be + ben(1+be)]d_t + ben*bep*d_{t-1} >= 0
                lhs = [(1 + ben) * dnext[i] - (be + ben * (1 + be)) * dh[i]
                       + ben * bep * dprev[i] for i in range(n)]
                ok = all(v >= 0 for v in lhs)
                C['TT_same'][1] += 1
                C['TT_same'][0] += ok
                if not ok:
                    fails.append(('TT_same', t + 1))
                nz = [lhs[i] for i in S
                      if dprev[i] != 0 or dh[i] != 0 or dnext[i] != 0]
                if nz:
                    upd('TT', float(min(nz)))
                # u_t and MCU
                u = [(1 + be) * dh[i] - bep * dprev[i] for i in range(n)]
                if any(u[i] != 0 for i in S) and \
                        all(u[i] == 0 for i in range(n) if i not in S):
                    y = msolve(Qt, d, kap, S, u)
                    thr = 1 - qr * qr
                    ok = all(y[i] >= thr * u[i] for i in S)
                    C['MCU'][1] += 1
                    C['MCU'][0] += ok
                    for i in S:
                        if u[i] > 0:
                            upd('MCU', float(y[i] / u[i] / thr))
                # delta floor
                delta_t = [dprev[i] - dh[i] for i in range(n)]
                delta_n = [dh[i] - dnext[i] for i in range(n)]
                if all(v >= 0 for v in delta_t) and all(v >= 0 for v in delta_n):
                    ok = all(delta_n[i] >= (1 - qr) / 2 * delta_t[i]
                             for i in range(n))
                    C['DF_same'][1] += 1
                    C['DF_same'][0] += ok
                    for i in range(n):
                        if delta_t[i] > 0:
                            upd('DF', float(delta_n[i] / delta_t[i]
                                            / ((1 - qr) / 2)))
    out = dict(cell=name, n=n, nS=len(I.Sstar), proper=proper, T=len(recs),
               checks={k: tuple(v) for k, v in C.items()},
               worst={k: v for k, v in worst.items()},
               fails=fails[:60], nfails=len(fails),
               secs=round(time.time() - t0, 1))
    return out


if __name__ == '__main__':
    name = sys.argv[1]
    Tov = int(sys.argv[2]) if len(sys.argv) > 2 else None
    o = check_cell(name, Tov)
    print(json.dumps(o, default=str))
