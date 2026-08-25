"""Refined adversarial sweep: S(q) = max slope over path families, per q."""
import sys, math, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
import numpy as np
from fengine import FInst, window_table, tail_slope
from engine import path_graph

def slope_of(adj, seed, q, rho, T):
    try:
        F = FInst(adj, seed, q=q, rho=rho)
        if F.xstar.max() <= 0:
            return None
        res = F.run(T)
        sl, B = tail_slope(res, q)
        rows = window_table(res, q)
        wm = max((r['ratio'] for r in rows[1:]), default=0.0)
        gam = np.array(res['gamma'])
        ev = np.where(gam > 1)[0]
        last = int(ev[-1]) if len(ev) else -1
        sus = last > T - int(3 / q) - 2
        return dict(q=q, rho=rho, n=len(adj), slope=sl, maxwin=wm,
                    J=res['J'][-1], nev=int(len(ev)), last=last,
                    sustained=bool(sus), maxgam=float(gam.max()),
                    nSstar=int(len(F.Sstar)))
    except Exception:
        return None

t0 = time.time()
best = {}
allr = []
qs = [1/8, 1/12, 1/16, 1/24]
ns = [4, 5, 6, 8, 12, 16]
for q in qs:
    T = int(150 / q)
    for n in ns:
        adj = path_graph(n)
        seed = [1.0] + [0.0] * (n - 1)
        # coarse rho scan: find support breakpoints, then probe near them
        rhos = np.geomspace(0.002, 0.45, 26)
        sizes = {}
        for rho in rhos:
            F = FInst(adj, seed, q=q, rho=rho)
            k = len(F.Sstar)
            sizes.setdefault(k, []).append(rho)
        cand = set()
        for k, lst in sizes.items():
            lst = sorted(lst)
            cand.add(lst[0]); cand.add(lst[-1])
            cand.add(lst[len(lst) // 2])
        # refine near breakpoints: pairs of adjacent rhos w/ different size
        srt = sorted(rhos)
        for a, b in zip(srt, srt[1:]):
            Fa = FInst(adj, seed, q=q, rho=a)
            Fb = FInst(adj, seed, q=q, rho=b)
            if len(Fa.Sstar) != len(Fb.Sstar):
                for frac in (0.35, 0.7, 0.9, 0.97):
                    cand.add(a + frac * (b - a))
        for rho in sorted(cand):
            r = slope_of(adj, seed, q, rho, T)
            if r is None:
                continue
            allr.append(r)
            key = q
            if key not in best or r['slope'] > best[key]['slope']:
                best[key] = r
    print("q=1/%d done (%.0fs): best slope=%.5f at n=%d rho=%.5f maxwin=%.4f %s"
          % (round(1/q), time.time() - t0, best[q]['slope'], best[q]['n'],
             best[q]['rho'], best[q]['maxwin'],
             'SUST' if best[q]['sustained'] else 'trans'), flush=True)

print("\nS(q) trend:")
for q in qs:
    b = best[q]
    print("  q=1/%-3d  S(q)=%.5f  (n=%d rho=%.5f maxwin=%.4f nev=%d last=%d "
          "maxgam=%.4f |S*|=%d %s)" %
          (round(1/q), b['slope'], b['n'], b['rho'], b['maxwin'], b['nev'],
           b['last'], b['maxgam'], b['nSstar'],
           'SUST' if b['sustained'] else 'trans'))
# top-10 overall
srt = sorted(allr, key=lambda r: -r['slope'])[:10]
print("\nTOP-10 overall:")
for r in srt:
    print("  q=1/%-3d n=%2d rho=%.5f slope=%.5f maxwin=%.4f J=%.3f nev=%d %s"
          % (round(1/r['q']), r['n'], r['rho'], r['slope'], r['maxwin'],
             r['J'], r['nev'], 'SUST' if r['sustained'] else 'trans'))
json.dump(allr, open('/home/claude/work/overnight/w7_windowed/search2_results.json', 'w'), indent=1)
print("elapsed %.0fs" % (time.time() - t0))
