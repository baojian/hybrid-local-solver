"""I2-C task 4: pin the tuned-rho path stress family (P_24, q=1/32) to an
EXACT rational rho so it can drop into the project's exact-checker battery.

Family: endpoint-seeded path, rho tuned just below the support breakpoint at
which the far endpoint leaves S*.  Iteration-1 float optimum: n=24, q=1/32,
rho ~= 0.016026, |S*| = 23, windowed slope 0.1445, 109 inflation events in
T=4800, max per-event gamma 1.4453.
"""
import sys, math, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
import numpy as np
from fengine import FInst, window_table, tail_slope
from engine import Inst, path_graph

n, q = 24, 1 / 32
adj = path_graph(n)
seed = [1.0] + [0.0] * (n - 1)

# --- 1. locate the support breakpoint exactly (bisection on |S*|) ----------
def nS(rho):
    return len(FInst(adj, seed, q=q, rho=float(rho)).Sstar)

lo, hi = Fr(1, 100), Fr(2, 100)          # nS(lo)=24 ... nS(hi)=23 expected
print("nS(0.01)=%d  nS(0.02)=%d" % (nS(lo), nS(hi)))
for _ in range(40):
    mid = (lo + hi) / 2
    if nS(mid) == nS(lo):
        lo = mid
    else:
        hi = mid
print("breakpoint rho* in [%.10f, %.10f]  (|S*| %d -> %d)"
      % (float(lo), float(hi), nS(lo), nS(hi)))

# --- 2. exact rational candidates just above the breakpoint ---------------
T = 4800
cands = [Fr(1, 62), Fr(2, 125), Fr(101, 6300), Fr(641, 40000), Fr(1, 64),
         Fr(17, 1000), Fr(33, 2000), Fr(65, 4096)]
rows = []
for rho in cands:
    F = FInst(adj, seed, q=q, rho=float(rho))
    if F.xstar.max() <= 0:
        continue
    res = F.run(T)
    sl, B = tail_slope(res, q)
    g = np.array(res['gamma'])
    ev = np.where(g > 1)[0]
    wm = max((r['ratio'] for r in window_table(res, q)[1:]), default=0.0)
    rows.append(dict(rho=str(rho), fl=float(rho), nS=int(len(F.Sstar)),
                     slope=float(sl), B=float(B), J=float(res['J'][-1]),
                     nev=int(len(ev)), last=int(ev[-1]) if len(ev) else -1,
                     maxgam=float(g.max()), maxwin=float(wm)))
    print("  rho=%-12s (%.6f) |S*|=%2d slope=%.5f J=%7.3f nev=%3d last=%4d "
          "maxgam=%.4f maxwin=%.4f" %
          (rho, float(rho), rows[-1]['nS'], sl, res['J'][-1], len(ev),
           rows[-1]['last'], g.max(), wm))

best = max(rows, key=lambda r: r['slope'])
print("\nSELECTED rho = %s  (slope %.5f, %d events, sustained to t=%d)"
      % (best['rho'], best['slope'], best['nev'], best['last']))

# --- 3. exact Fraction cross-check of the selected cell -------------------
rho = Fr(best['rho'])
Tx = 26
I = Inst(adj, [Fr(1)] + [Fr(0)] * (n - 1), Fr(1, 32), rho)
recs = I.run(Tx)
Fl = FInst(adj, seed, q=q, rho=float(rho)).run(Tx)
wex = ''.join(r['cls'] for r in recs)
print("exact word   [0:%d] = %s" % (Tx, wex))
print("float word   [0:%d] = %s" % (Tx, Fl['cls']))
print("words agree:", wex == Fl['cls'])
dev = max(abs(float(r['gamma']) - g) for r, g in zip(recs, Fl['gamma']))
print("max |gamma_exact - gamma_float| over %d stages: %.3e" % (Tx, dev))
print("|S*| exact =", len(I.Sstar), " x*_last =", float(I.xstar[-1]))
print("first exact gammas > 1:",
      [(r['t'], str(r['gamma'])[:34]) for r in recs if r['gamma'] > 1][:4])
json.dump(dict(rows=rows, selected=best['rho'], word=wex),
          open('/home/claude/work/overnight/w7_windowed/p24_audit.json', 'w'),
          indent=1)
