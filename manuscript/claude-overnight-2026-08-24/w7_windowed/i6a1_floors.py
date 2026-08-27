"""I6-A1 second pass: floors on the trigger ladder, exact.

zeta_t := ct - Qt a_t on S_t  (trigger vector; NF <=> zeta_t >= 0 on S_t).
Same-face identity (proved): zeta_{t+1}|_S = kap D tau_{t+1},
tau obeys tau_{t+1} = M[(1+b)tau_t - b tau_{t-1}].
Induction closes at level k if the k-th floor holds:
  ZFh : zeta_{t+1} >= [b/(1+b)] zeta_t   (needed: gives tau_{t+2} >= 0)
  ZFb : zeta_{t+1} >= b zeta_t           (ladder-strong version)
  Cpos: c_t = d_{t+1} - b d_t >= 0
  CFb : c_{t+1} >= b c_t                 (r2 >= 0)
  CFh : c_{t+1} >= [b/(1+b)] c_t
All tested on same-face consecutive pairs (zeta compared on S_t), exact Fr.
"""
import sys, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst
from i5c_core import run_i5c
from i6a1_checks import CELLS


def run(name, Tov=None):
    adj, seed, q, rho, T = CELLS[name]
    if Tov:
        T = Tov
    I = Inst(adj, seed, q, rho)
    n = I.n
    recs = run_i5c(I, T, variant='fm')
    Qt, ct = I.Qt, I.ct
    C = {k: [0, 0] for k in ('ZFh', 'ZFb', 'Cpos', 'CFb', 'CFh', 'Zpos')}
    worst = {k: None for k in ('ZFh', 'ZFb', 'CFb', 'CFh')}
    fails = []

    def upd(k, v):
        worst[k] = v if worst[k] is None else min(worst[k], v)

    zeta_prev = None
    Sprev = None
    beprev = None
    for t, r in enumerate(recs):
        S, be = r['S'], r['beta']
        ah = r['ah']
        zeta = {i: ct[i] - sum(Qt[i][j] * ah[j] for j in S) for i in S}
        C['Zpos'][1] += 1
        C['Zpos'][0] += all(v >= 0 for v in zeta.values())
        if zeta_prev is not None and S == Sprev and S:
            C['ZFh'][1] += 1
            ok = all(zeta[i] >= be / (1 + be) * zeta_prev[i] for i in S)
            C['ZFh'][0] += ok
            if not ok:
                fails.append(('ZFh', t))
            C['ZFb'][1] += 1
            okb = all(zeta[i] >= be * zeta_prev[i] for i in S)
            C['ZFb'][0] += okb
            for i in S:
                if zeta_prev[i] > 0:
                    rt = zeta[i] / zeta_prev[i]
                    upd('ZFh', float(rt / (be / (1 + be))))
                    upd('ZFb', float(rt / be))
        zeta_prev, Sprev, beprev = zeta, S, be
    # c-ladder
    for t in range(len(recs) - 2):
        r, rn = recs[t], recs[t + 1]
        if r['S'] != rn['S'] or not r['S']:
            continue
        be = rn['beta']
        x, xn, xnn = r['x'], r['xn'], rn['xn']
        d1 = [xn[i] - x[i] for i in range(n)]
        d2 = [xnn[i] - xn[i] for i in range(n)]
        c = [d2[i] - be * d1[i] for i in range(n)]
        C['Cpos'][1] += 1
        C['Cpos'][0] += all(v >= 0 for v in c)
        if t + 2 < len(recs) and recs[t + 2]['S'] == r['S']:
            be2 = recs[t + 2]['beta']
            xnnn = recs[t + 2]['xn']
            d3 = [xnnn[i] - xnn[i] for i in range(n)]
            c2 = [d3[i] - be2 * d2[i] for i in range(n)]
            C['CFb'][1] += 1
            okb = all(c2[i] >= be2 * c[i] for i in range(n))
            C['CFb'][0] += okb
            C['CFh'][1] += 1
            okh = all(c2[i] >= be2 / (1 + be2) * c[i] for i in range(n))
            C['CFh'][0] += okh
            for i in r['S']:
                if c[i] > 0:
                    rt = c2[i] / c[i]
                    upd('CFb', float(rt / be2))
                    upd('CFh', float(rt / (be2 / (1 + be2))))
    return dict(cell=name, T=len(recs), checks={k: tuple(v) for k, v in C.items()},
                worst=worst, fails=fails[:25])


if __name__ == '__main__':
    name = sys.argv[1]
    Tov = int(sys.argv[2]) if len(sys.argv) > 2 else None
    print(json.dumps(run(name, Tov), default=str))
