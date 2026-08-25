"""W8 regime map sweep: push vs WY-style active set vs target oracle
over alpha in 2^{-2..-14} (step 4... actually step 2: 7 values),
eps in 2^{-3..-13} (6 values), on 5 sized families.
Every feasible cell verified against the exact solve (all n <= 131k here).
Output: map.csv (one row per graph x cell)."""
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

ALPHAS = [2.0 ** -k for k in range(2, 15)]      # 2^-2 .. 2^-14, step 1
EPSS = [2.0 ** -k for k in range(3, 14)]        # 2^-3 .. 2^-13, step 1
FAMILIES = ["star", "spider", "spider2", "caterpillar", "btree", "grid"]
EDGE_CAP = 200_000
BUDGET_S = 25 * 60

LOG = open(os.path.join(HERE, "..", "logs", "w8_map.log"), "w")


def log(msg):
    print(msg)
    LOG.write(msg + "\n")
    LOG.flush()


def main():
    t_start = time.time()
    cells = []
    for name in FAMILIES:
        for alpha in ALPHAS:
            for eps in EPSS:
                (kind, args), n_est, m_edges = C.family_params(name, alpha, eps)
                cost_key = 1.0 / (alpha * eps) + 50.0 * n_est
                cells.append((cost_key, name, alpha, eps, kind, args, n_est,
                              m_edges))
    cells.sort()
    log(f"{len(cells)} cells")

    graph_cache = {}
    model_cache = {}
    rows = []
    n_fail = 0
    for i, (ck, name, alpha, eps, kind, args, n_est, m_edges) in \
            enumerate(cells):
        la, le = round(math.log2(alpha)), round(math.log2(eps))
        base = dict(graph=name, alpha_log2=la, eps_log2=le, alpha=alpha,
                    eps=eps, n=n_est, edges=m_edges)
        if m_edges > EDGE_CAP:
            rows.append({**base, "status": "skip-size"})
            log(f"[{i}] {name} a=2^{la} e=2^{le}: skip-size ({m_edges} edges)")
            continue
        if time.time() - t_start > BUDGET_S:
            rows.append({**base, "status": "skip-time"})
            log(f"[{i}] {name} a=2^{la} e=2^{le}: skip-time")
            continue
        gk = (kind, args)
        if gk not in graph_cache:
            if len(graph_cache) > 4:
                graph_cache.pop(next(iter(graph_cache)))
            graph_cache[gk] = C.build_graph(kind, args)
        adj, seed = graph_cache[gk]
        mk = (kind, args, alpha)
        if mk not in model_cache:
            model_cache.clear()
            model_cache[mk] = Model(adj, alpha, seed)
        model = model_cache[mk]
        n = model.n
        x0 = model.solve_exact()
        pi0 = model.sqd * x0
        lvl0 = float(np.max(pi0 / model.d))       # err of x=0
        triv = int(lvl0 <= eps)

        pr = C.push_c(model, eps, seed)
        err_push = float(np.max(np.abs(pr["p"] - pi0) / model.d))
        onesided = float(np.min(pi0 - pr["p"]))
        assert err_push <= eps * (1 + 1e-9), (name, la, le, err_push / eps)
        assert onesided >= -1e-10 * max(1.0, pi0.max())

        wy = C.wy_active_set(model, eps, seed, x0=x0, time_guard=150.0)
        err_wy = float(model.semantic_err(wy["x"], x0))
        ok_wy = wy["status"] == "ok"
        if ok_wy:
            assert err_wy <= eps * (1 + 1e-9), (name, la, le, err_wy / eps)
        else:
            n_fail += 1

        W_t = C.target_oracle(alpha, eps)
        W_p, W_w = pr["W"], wy["W"]
        winner = "push" if W_p <= W_w else "WY"
        ratio = min(W_p, W_w) / W_t
        rows.append({**base, "status": "ok" if ok_wy else wy["status"],
                     "triv": triv, "lvl0_over_eps": lvl0 / eps,
                     "W_push": W_p, "W_WY": W_w, "W_target": W_t,
                     "E_expansions": wy["rounds"],
                     "tightenings": wy["tightenings"],
                     "winner": winner, "ratio_to_target": ratio,
                     "err_push_over_eps": err_push / eps,
                     "err_wy_over_eps": err_wy / eps,
                     "push_maxrd_over_eps": pr["max_rd"] / eps,
                     "const_push": W_p * alpha * eps,
                     "const_wy": W_w * eps * eps,
                     "wy_S": wy["S_size"], "wy_volS": wy["vol_S"],
                     "wy_nnzlu": wy["nnz_lu"],
                     "wy_C_adj": wy["C_adj"], "wy_R_adj": wy["R_adj"],
                     "wy_C_rec": wy["C_rec"], "wy_C_resp": wy["C_resp"],
                     "push_C_adj": pr["C_adj"], "push_R_adj": pr["R_adj"],
                     "n_push": pr["n_push"],
                     "wall_push": round(pr["wall"], 3),
                     "wall_wy": round(wy["wall"], 3)})
        log(f"[{i}] {name} a=2^{la} e=2^{le} n={n}: W_p={W_p:.3g} "
            f"W_wy={W_w:.3g} W_t={W_t:.3g} win={winner} r2t={ratio:.2f} "
            f"E={wy['rounds']} tight={wy['tightenings']} triv={triv} "
            f"errP={err_push/eps:.2f} errW={err_wy/eps:.2f} "
            f"[{pr['wall']:.2f}s/{wy['wall']:.2f}s] {wy['status']}")

    cols = ["graph", "alpha_log2", "eps_log2", "alpha", "eps", "n", "edges",
            "status", "triv", "lvl0_over_eps", "W_push", "W_WY", "W_target",
            "E_expansions", "tightenings", "winner", "ratio_to_target",
            "err_push_over_eps", "err_wy_over_eps", "push_maxrd_over_eps",
            "const_push", "const_wy", "wy_S", "wy_volS", "wy_nnzlu",
            "wy_C_adj", "wy_R_adj", "wy_C_rec", "wy_C_resp",
            "push_C_adj", "push_R_adj", "n_push", "wall_push", "wall_wy"]
    with open(os.path.join(HERE, "map.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["graph"], -r["alpha_log2"],
                                             -r["eps_log2"])):
            w.writerow(r)
    log(f"done in {time.time()-t_start:.0f}s; {len(rows)} rows, "
        f"{n_fail} non-ok WY cells -> map.csv")


if __name__ == "__main__":
    main()
