"""Oracle-stopped push bracket (symmetric to oracle-WY): the cheapest push
run whose TRUE semantic error is <= eps, found by bisection over the
activation threshold t >= eps (err(t) checked against the exact solution).
This is the generous LO incumbent for push; the certified variant is push
at t = eps (which self-certifies via the alpha*eps residual certificate).
Coarse grid. Output: push_oracle.csv."""
import csv
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
from model import Model  # noqa: E402
import contenders as C   # noqa: E402

ALPHAS = [2.0 ** -k for k in range(2, 15)]
EPSS = [2.0 ** -k for k in range(3, 14)]
FAMILIES = ["star", "spider", "spider2", "caterpillar", "btree", "grid"]
EDGE_CAP = 200_000

rows = []
t0 = time.time()
graph_cache = {}
for name in FAMILIES:
    for alpha in ALPHAS:
        for eps in EPSS:
            la, le = round(math.log2(alpha)), round(math.log2(eps))
            (kind, args), n_est, m_edges = C.family_params(name, alpha, eps)
            base = dict(graph=name, alpha_log2=la, eps_log2=le)
            if m_edges > EDGE_CAP:
                rows.append({**base, "status_po": "skip-size"})
                continue
            gk = (kind, args)
            if gk not in graph_cache:
                if len(graph_cache) > 3:
                    graph_cache.pop(next(iter(graph_cache)))
                graph_cache[gk] = C.build_graph(kind, args)
            adj, seed = graph_cache[gk]
            model = Model(adj, alpha, seed)
            x0 = model.solve_exact()
            pi0 = model.sqd * x0

            def err_at(t):
                res = C.push_c(model, t, seed)
                e = float(np.max(np.abs(res["p"] - pi0) / model.d))
                return e, res["W"]

            # exponential bracket then bisection on log t
            lo_t = eps            # err(eps) <= eps guaranteed
            e_lo, W_lo = err_at(lo_t)
            hi_t = eps
            for _ in range(8):
                hi_t *= 2.0
                e_hi, W_hi = err_at(hi_t)
                if e_hi > eps:
                    break
                lo_t, W_lo = hi_t, W_hi
            else:
                e_hi = None
            if e_hi is not None and e_hi > eps:
                for _ in range(6):
                    mid = math.sqrt(lo_t * hi_t)
                    e_m, W_m = err_at(mid)
                    if e_m <= eps:
                        lo_t, W_lo = mid, W_m
                    else:
                        hi_t = mid
            rows.append({**base, "status_po": "ok", "W_push_oracle": W_lo,
                         "thr_ratio": lo_t / eps})
            print(f"{name} a=2^{la} e=2^{le}: W_po={W_lo:.4g} "
                  f"thr={lo_t/eps:.2f}x", flush=True)

cols = ["graph", "alpha_log2", "eps_log2", "status_po", "W_push_oracle",
        "thr_ratio"]
with open(os.path.join(HERE, "push_oracle.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
print(f"done in {time.time()-t0:.0f}s; {len(rows)} rows -> push_oracle.csv")
