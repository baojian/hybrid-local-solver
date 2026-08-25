"""Phase 1: truncation-injection amplification A(alpha, m) across the zoo.
Injection e_i at step k0=K-m; measure ||u_K||_2 (A2), semantic gain (Asem),
running peak, vs envelope (t_k0/t_K)(m+1) and A_bar(alpha)."""
import sys
import math
import json
import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w5_cheb")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from cheb import measure_amp, A_bar, consts, bfs_dist  # noqa
from model import Model  # noqa
import zoo  # noqa

GRAPHS = {
    "path": zoo.path(500),
    "spider": zoo.spider(8, 80),
    "star": zoo.star(300),
    "caterpillar": zoo.caterpillar(150, 1),
    "btree": zoo.binary_tree(10),
    "decoy_hub": zoo.decoy_hub(120, 300),
    "grid": zoo.grid(50, 50),
}
ALPHAS = [2 ** -4, 2 ** -6, 2 ** -8, 2 ** -10]

results = []
for gname, (adj, seed) in GRAPHS.items():
    dist = bfs_dist(adj, seed)
    dmax = max(dist)
    degs = [len(adj[u]) for u in range(len(adj))]
    hub = int(np.argmax(degs))
    for alpha in ALPHAS:
        mod = Model(adj, alpha, seed)
        K = int(math.ceil(2.5 / math.sqrt(alpha))) + 10
        # m values: log spaced up to K-1
        ms = sorted(set([1, 2, 4, 8, 16, 32, 64, 128, 256,
                         max(1, int(round(0.5 / math.sqrt(alpha)))),
                         max(1, int(round(1.0 / math.sqrt(alpha)))),
                         K - 1]))
        ms = [m for m in ms if 1 <= m <= K - 1]
        # sites: seed, hub, a mid-distance vertex on the reachable frontier
        mid_d = min(max(1, int(round(1.0 / math.sqrt(alpha)))), dmax)
        mid = next(u for u in range(len(adj)) if dist[u] == mid_d)
        sites = sorted(set([seed, hub, mid]))
        rows = measure_amp(mod, K, ms, sites)
        for r in rows:
            r.update(graph=gname, alpha=alpha, K=K,
                     dist_site=dist[r["site"]])
        results.extend(rows)
        Amax = max(r["A2"] for r in rows)
        Apeak = max(r["A2peak"] for r in rows)
        best = max(rows, key=lambda r: r["A2"])
        print(f"{gname:12s} a=2^{int(math.log2(alpha)):3d} K={K:3d} "
              f"A2max={Amax:8.3f} (m={best['m']}, site d={best['d_site']},"
              f" dist={best['dist_site']}) peak={Apeak:8.3f} "
              f"A_bar={A_bar(alpha):7.3f}")

with open("/home/claude/work/overnight/w5_cheb/out/amp.json", "w") as f:
    json.dump(results, f)

# fit A2max ~ alpha^{-r} per graph
print("\nfit A2max ~ C * alpha^{-r}:")
for gname in GRAPHS:
    xs, ys = [], []
    for alpha in ALPHAS:
        rows = [r for r in results if r["graph"] == gname
                and r["alpha"] == alpha]
        xs.append(math.log(1 / alpha))
        ys.append(math.log(max(r["A2"] for r in rows)))
    A = np.vstack([np.ones(len(xs)), xs]).T
    c, r_ = np.linalg.lstsq(A, np.array(ys), rcond=None)[0:2][0], None
    # envelope fit too
    ex, ey = [], []
    for alpha in ALPHAS:
        ex.append(math.log(1 / alpha))
        ey.append(math.log(A_bar(alpha)))
    ce = np.linalg.lstsq(np.vstack([np.ones(4), ex]).T, np.array(ey),
                         rcond=None)[0]
    print(f"  {gname:12s} r={c[1]:.3f} C={math.exp(c[0]):.3f}   "
          f"(A_bar fit r={ce[1]:.3f} C={math.exp(ce[0]):.3f})")
