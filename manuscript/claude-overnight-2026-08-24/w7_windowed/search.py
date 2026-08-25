"""Task 3: search for a worse family — sustained corrections with slope >= 1?"""
import sys, math, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
import numpy as np
from fengine import FInst, window_table, tail_slope
from engine import complete_graph, path_graph, star_graph, disjoint_union, add_edge

results = []

def probe(name, adj, seed, q, rho, T=None, alpha=None, quiet=False):
    try:
        F = FInst(adj, seed, q=q, rho=rho, alpha=alpha)
        if F.xstar.max() <= 0:
            print("  %s: x*=0, skip" % name); return None
        T = T or int(30 / q)
        res = F.run(T)
        sl, B = tail_slope(res, q)
        rows = window_table(res, q)
        wm = max((r['ratio'] for r in rows[1:]), default=0.0)
        ncorr = sum(1 for c in res['cls'] if c != 'N')
        gam = np.array(res['gamma'])
        ev = np.where(gam > 1)[0]
        last = ev[-1] if len(ev) else -1
        maxg = gam.max()
        rec = dict(name=name, q=q, rho=rho, n=len(adj), T=T,
                   J=res['J'][-1], slope=sl, B=B, maxwin=wm, ncorr=ncorr,
                   nevents=int(len(ev)), last_event=int(last),
                   maxgamma=float(maxg),
                   sustained=bool(last > T - int(3 / q) - 2))
        results.append(rec)
        if not quiet:
            print("  %-34s n=%3d q=%.4g J=%.4f slope=%.5f maxwin=%.5f "
                  "nev=%d last=%d maxgam=%.4f %s" %
                  (name, len(adj), q, res['J'][-1], sl, wm, len(ev), last,
                   maxg, "SUSTAINED" if rec['sustained'] else "transient"))
        return rec
    except Exception as ex:
        print("  %s: ERROR %s" % (name, ex))
        return None

t0 = time.time()
print("== S1: P_4 mechanism vs q (fixed graph/seed/rho) ==")
for q in (1/8, 1/12, 1/16, 1/24, 1/32, 1/48, 1/64):
    probe("P4 q=1/%d" % round(1/q), path_graph(4), [1,0,0,0], q, 7/40)

print("== S2: P_4 rho sweep toward support breakpoint ==")
for rho in (0.10, 0.13, 0.15, 0.165, 0.175, 0.180, 0.184, 0.1875, 0.19, 0.20, 0.22):
    F = FInst(path_graph(4), [1,0,0,0], q=1/8, rho=rho)
    mn = F.xstar[F.xstar > 0].min() / F.xstar.max()
    r = probe("P4 rho=%.4f" % rho, path_graph(4), [1,0,0,0], 1/8, rho, quiet=True)
    if r: print("  rho=%.4f |S*|=%d minx*/maxx*=%.2e slope=%.5f maxwin=%.5f nev=%d %s"
                % (rho, len(F.Sstar), mn, r['slope'], r['maxwin'], r['nevents'],
                   "SUST" if r['sustained'] else "trans"))

print("== S3: longer paths, endpoint seed (rho scaled to keep partial support) ==")
for m, rho in ((4,7/40),(6,0.10),(6,0.05),(8,0.06),(8,0.03),(12,0.02),
               (16,0.012),(24,0.006),(32,0.004)):
    probe("P%d rho=%.3g" % (m, rho), path_graph(m), [1]+[0]*(m-1), 1/8, rho)
for m, rho in ((8,0.03),(16,0.012)):
    for q in (1/16, 1/32):
        probe("P%d rho=%.3g q=1/%d" % (m, rho, round(1/q)),
              path_graph(m), [1]+[0]*(m-1), q, rho)

print("== S4: K_m analogues of the v-pulse (m=16,32) ==")
for m in (16, 32):
    for q in (1/50, 1/100):
        al = q*q/(1+q*q)
        lam_h = al + (1-al)/2 * m/(m-1)
        v = np.array([1.0] + [-1/(m-1)]*(m-1))
        for cv in (12, 40, 100):
            e0 = 1 + cv*q*q*v
            Qe0 = al + cv*q*q*lam_h*v
            s = (1 + Qe0/al)/(2*m)
            if s.min() <= 0: continue
            probe("K%d cv=%d q=1/%d" % (m, cv, round(1/q)),
                  complete_graph(m), s.tolist(), q, 1/(2*m*(m-1)), T=int(20/q))

print("== S5: repeated pulses — two/three K_8 clusters coupled ==")
q = 1/50
al = q*q/(1+q*q)
# path of K_8s: clusters joined 7-8, 15-16 by single edges; seed in cluster 0
for k in (2, 3, 4):
    adj = disjoint_union([complete_graph(8) for _ in range(k)])
    for c in range(k-1):
        adj = add_edge(adj, 8*c+7, 8*(c+1))
    n = len(adj)
    s = [1/8]*8 + [0]*(n-8)          # all seed in cluster 0
    probe("chainK8 x%d q=1/50" % k, adj, s, q, 1/(4*8*7*k), T=int(25/q))
    s2 = [0.9/8]*8 + [0.1/(n-8)]*(n-8)  # shared seed mass
    probe("chainK8 x%d shared seed" % k, adj, s2, q, 1/(4*8*7*k), T=int(25/q))

print("== S6: barbell K8-path-K8; star; dense-seed path ==")
adjb = disjoint_union([complete_graph(8), path_graph(4), complete_graph(8)])
adjb = add_edge(adjb, 7, 8); adjb = add_edge(adjb, 11, 12)
probe("barbell K8-P4-K8", adjb, [1/8]*8+[0]*12, 1/50, 1/600, T=1500)
probe("star16", star_graph(16), [1]+[0]*15, 1/16, 1/40)
probe("star16 leafseed", star_graph(16), [0,1]+[0]*14, 1/16, 1/60)
m = 12
probe("P12 dense seed", path_graph(m), [1/m]*m, 1/16, 0.02)
probe("P12 two-end seed", path_graph(m), [0.5]+[0]*(m-2)+[0.5], 1/16, 0.02)

print("elapsed %.1fs" % (time.time() - t0))
json.dump(results, open('/home/claude/work/overnight/w7_windowed/search_results.json','w'), indent=1)
worst = sorted([r for r in results], key=lambda r: -r['slope'])[:8]
print("\nWORST BY SLOPE:")
for r in worst:
    print("  %-34s slope=%.5f maxwin=%.5f J=%.4f %s" %
          (r['name'], r['slope'], r['maxwin'], r['J'],
           "SUSTAINED" if r['sustained'] else "transient"))
