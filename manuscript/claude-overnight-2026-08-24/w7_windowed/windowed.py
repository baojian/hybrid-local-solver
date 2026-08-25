"""Task 2: windowed exponent test on K_2, K_8-q, P_4 families."""
import sys, math, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
import numpy as np
from fengine import FInst, window_table, tail_slope
from engine import complete_graph, path_graph
from fractions import Fraction as Fr

ASTAR = 6929307 / 98509850
out = {}

def report(name, F, res, q, w=None, maxrows=14):
    rows = window_table(res, q, w)
    T = len(res['J'])
    sl, B = tail_slope(res, q)
    ncorr = sum(1 for c in res['cls'] if c != 'N')
    print("--- %s (q=%.5g, T=%d, w=%d) ---" % (name, q, T,
          w or math.ceil(1 / q)))
    print("  corrections: %d  (word head: %s)" % (ncorr, res['cls'][:40]))
    print("  J_T = %.6f   qT = %.3f   J_T/(qT) = %.6f" %
          (res['J'][-1], q * T, res['J'][-1] / (q * T)))
    print("  tail LS: slope=%.6f  intercept(B)=%.4f" % (sl, B))
    print("  window: j  t0  inflation  infl/(qw)  dlogPhi  dloge2  ncorr")
    step = max(1, len(rows) // maxrows)
    for r in rows[::step]:
        print("   %4d %5d  %9.6f  %9.6f  %8.4f  %8.4f  %4d" %
              (r['j'], r['t0'], r['infl'], r['ratio'], r['dlogPhi'],
               r['dloge2'], r['ncorr']))
    wm = max(r['ratio'] for r in rows[1:]) if len(rows) > 1 else 0.0
    print("  MAX per-window infl/(qw) over windows j>=1: %.6f" % wm)
    out[name] = dict(q=q, T=T, J=res['J'][-1], slope=sl, B=B,
                     max_window_ratio=wm, ncorr=ncorr,
                     rows=[{k: (None if isinstance(v, float) and
                                math.isnan(v) else v)
                            for k, v in r.items()} for r in rows])
    return rows

print("========== K_2 family (uniform seed, rho=1/16) ==========")
for n in (100, 200, 400, 800):
    q = 1 / n
    F = FInst([[1], [0]], [0.5, 0.5], q=q, rho=1 / 16)
    T = int(20 / q)
    res = F.run(T)
    report("K2 n=%d" % n, F, res, q, maxrows=8)

print("========== K_8 small-q family (rho=1/112) ==========")
for nn in (100, 200, 400):
    q = 1 / nn
    al = q * q / (1 + q * q)
    lam_h = (4 + 3 * al) / 7
    v = np.array([1.0] + [-1 / 7] * 7)
    Qe0 = al + 12 * q * q * lam_h * v
    s = (1 + Qe0 / al) / 16
    F = FInst(complete_graph(8), s.tolist(), q=q, rho=1 / 112)
    T = int(20 / q)
    res = F.run(T)
    report("K8 q=1/%d" % nn, F, res, q, maxrows=8)

print("========== P_4 neutral (endpoint seed, q=1/8, rho=7/40) ==========")
F = FInst(path_graph(4), [1, 0, 0, 0], q=1 / 8, rho=7 / 40)
res = F.run(2000)   # 250/q — long horizon to nail the linear rate
report("P4", F, res, 1 / 8, maxrows=12)
# per-cycle inflation events
gam = np.array(res['gamma'])
ev = np.where(gam > 1)[0]
print("  inflation events: %d; last at t=%d; per-event gamma tail: %s" %
      (len(ev), ev[-1], ["%.6f" % gam[t] for t in ev[-4:]]))
print("  asymptotic rate: J gain per 11-stage cycle = %.6f -> slope vs qT = %.6f"
      % (res['J'][-1] - res['J'][-1 - 11 * 20],
         (res['J'][-1] - res['J'][-1 - 11 * 20]) / (1 / 8 * 11 * 20)))

json.dump(out, open('/home/claude/work/overnight/w7_windowed/windowed_results.json', 'w'), indent=1)
print("saved windowed_results.json")
