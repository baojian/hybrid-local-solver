"""Self-certified WY bracket: same active-set growth, termination on the
DETERMINISTIC certificate max_v cert_v < alpha*eps, which proves
err <= cert_max/alpha <= eps with no oracle (M^{-1} >= 0, M^{-1}d = d/alpha).
Run on the coarse specified grid; verified against exact anyway.
Output: cert.csv."""
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

ALPHAS = [2.0 ** -k for k in range(2, 15, 2)]
EPSS = [2.0 ** -k for k in range(3, 14, 2)]
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
                rows.append({**base, "status_cert": "skip-size"})
                continue
            gk = (kind, args)
            if gk not in graph_cache:
                if len(graph_cache) > 3:
                    graph_cache.pop(next(iter(graph_cache)))
                graph_cache[gk] = C.build_graph(kind, args)
            adj, seed = graph_cache[gk]
            model = Model(adj, alpha, seed)
            x0 = model.solve_exact()
            wy = C.wy_active_set(model, eps, seed, x0=None, tau_factor=alpha,
                                 time_guard=150.0)
            err = float(model.semantic_err(wy["x"], x0))
            ok = wy["status"] == "ok"
            if ok:
                assert err <= eps * (1 + 1e-9), (name, la, le, err / eps)
            rows.append({**base, "status_cert": wy["status"],
                         "W_WYcert": wy["W"], "E_cert": wy["rounds"],
                         "S_cert": wy["S_size"],
                         "err_cert_over_eps": err / eps,
                         "wall_cert": round(wy["wall"], 2)})
            print(f"{name} a=2^{la} e=2^{le} n={model.n}: Wc={wy['W']:.3g} "
                  f"E={wy['rounds']} S={wy['S_size']} err={err/eps:.3f} "
                  f"[{wy['wall']:.1f}s] {wy['status']}", flush=True)

cols = ["graph", "alpha_log2", "eps_log2", "status_cert", "W_WYcert",
        "E_cert", "S_cert", "err_cert_over_eps", "wall_cert"]
with open(os.path.join(HERE, "cert.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
print(f"done in {time.time()-t0:.0f}s; {len(rows)} rows -> cert.csv")
