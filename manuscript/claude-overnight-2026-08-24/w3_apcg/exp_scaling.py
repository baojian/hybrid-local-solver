"""Fixed-support scaling experiment: W(alpha) for APCG vs baselines on
star / path / spider / caterpillar, S = supp(x*(rho)) computed offline."""
import json
import math
import random
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import (Model, Meter, Restricted, apcg_run, cd_run, ista_run,
                     exact_support_solver, fit_exponent)
import zoo

ALPHAS = [2.0 ** -4, 2.0 ** -6, 2.0 ** -8, 2.0 ** -10, 2.0 ** -12]

INSTANCES = {
    "star": dict(make=lambda: zoo.star(250), rho=1.0 / 2000),      # m=1/(8rho)
    "path": dict(make=lambda: zoo.path(1200), rho=1.0 / 4000),
    "spider": dict(make=lambda: zoo.spider(6, 150), rho=1.0 / 4000),
    "caterpillar": dict(make=lambda: zoo.caterpillar(500, 1), rho=1.0 / 4000),
}

N_SEEDS_APCG = 5


def n_seeds_cd(alpha):
    if alpha >= 2.0 ** -8:
        return 5
    if alpha >= 2.0 ** -10:
        return 3
    return 2


def med(v):
    return float(np.median(v)) if v else None


def main():
    t00 = time.time()
    results = {}
    traj_store = {}
    for gname, spec in INSTANCES.items():
        adj, seed = spec["make"]()
        rho = spec["rho"]
        results[gname] = dict(rho=rho, n_graph=len(adj), cells=[])
        for alpha in ALPHAS:
            t0 = time.time()
            mdl = Model(adj, alpha, seed)
            xstar, S = exact_support_solver(mdl, rho)
            Fstar = mdl.F_rho(xstar, rho)
            R = Restricted(mdl, rho, S, xstar=xstar[S], Fstar=Fstar)
            cell = dict(alpha=alpha, nS=R.n, volS=R.vol,
                        h0=R.h0, arho=R.arho)
            # --- APCG ---
            Wl, il, Wsl, errl, stat = [], [], [], [], []
            for s in range(N_SEEDS_APCG):
                m = Meter(mdl.adj)
                res = apcg_run(R, m, random.Random(1000 + s))
                stat.append(res["status"])
                if res["it_h"] is not None:
                    Wl.append(res["W_h"]); il.append(res["it_h"])
                if res["W_sym"] is not None:
                    Wsl.append(res["W_sym"])
                errl.append(R.err_vs_star(res["x"]))
                if s == 0 and alpha in (2.0 ** -6, 2.0 ** -12):
                    traj_store[f"{gname}_a{alpha:.6g}_apcg"] = res["traj"][:400]
            cell["apcg"] = dict(W=med(Wl), iters=med(il), W_sym=med(Wsl),
                                err=max(errl), status=stat,
                                W_all=[float(w) for w in Wl])
            # --- CD uniform ---
            Wl, il, Wsl, errl, stat = [], [], [], [], []
            for s in range(n_seeds_cd(alpha)):
                m = Meter(mdl.adj)
                res = cd_run(R, m, rng=random.Random(2000 + s),
                             rule="uniform")
                stat.append(res["status"])
                if res["it_h"] is not None:
                    Wl.append(res["W_h"]); il.append(res["it_h"])
                if res["W_sym"] is not None:
                    Wsl.append(res["W_sym"])
                errl.append(R.err_vs_star(res["x"]))
            cell["cd_uniform"] = dict(W=med(Wl), iters=med(il), W_sym=med(Wsl),
                                      err=max(errl), status=stat,
                                      W_all=[float(w) for w in Wl])
            # --- CD GS ---
            m = Meter(mdl.adj)
            res = cd_run(R, m, rule="gs")
            cell["cd_gs"] = dict(W=res["W_h"], iters=res["it_h"],
                                 W_sym=res["W_sym"],
                                 err=R.err_vs_star(res["x"]),
                                 status=[res["status"]])
            if alpha in (2.0 ** -6, 2.0 ** -12):
                traj_store[f"{gname}_a{alpha:.6g}_gs"] = res["traj"][:400]
            # --- ISTA ---
            m = Meter(mdl.adj)
            res = ista_run(R, m)
            cell["ista"] = dict(W=res["W_h"], iters=res["it_h"],
                                W_sym=res["W_sym"],
                                err=R.err_vs_star(res["x"]),
                                status=[res["status"]])
            cell["wall_s"] = time.time() - t0
            results[gname]["cells"].append(cell)
            print(f"[{time.time() - t00:7.1f}s] {gname} a=2^{math.log2(alpha):.0f} "
                  f"|S|={R.n} vol={R.vol} "
                  f"W_apcg={cell['apcg']['W']:.3g} "
                  f"W_unif={cell['cd_uniform']['W']:.3g} "
                  f"W_gs={cell['cd_gs']['W']:.3g} "
                  f"W_ista={cell['ista']['W']:.3g} "
                  f"({cell['wall_s']:.1f}s)", flush=True)
        # --- fits per graph ---
        cells = results[gname]["cells"]
        al = [c["alpha"] for c in cells]
        vols = np.array([c["volS"] for c in cells], float)
        fits = {}
        for meth in ("apcg", "cd_uniform", "cd_gs", "ista"):
            Ws = [c[meth]["W"] for c in cells]
            if all(w is not None for w in Ws):
                p_raw, dev = fit_exponent(al, Ws)
                p_norm, devn = fit_exponent(al, np.array(Ws) / vols)
                fits[meth] = dict(p_raw=p_raw, dev_raw=dev,
                                  p_norm=p_norm, dev_norm=devn)
        results[gname]["fits"] = fits
        print(f"  fits {gname}: " + "  ".join(
            f"{mth}: p_raw={f['p_raw']:.3f} p_norm={f['p_norm']:.3f}"
            for mth, f in fits.items()), flush=True)

    with open("/home/claude/work/overnight/w3_apcg/results_scaling.json",
              "w") as f:
        json.dump(results, f, indent=1)
    with open("/home/claude/work/overnight/w3_apcg/results_traj.json",
              "w") as f:
        json.dump(traj_store, f)
    print(f"TOTAL {time.time() - t00:.1f}s")


if __name__ == "__main__":
    main()
