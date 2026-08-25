"""Robustness extras: (a) delta=0.01 exponent check on star+path;
(b) K2 mean/max iteration scaling (expectation, not just median);
(c) objective-gap decay rate vs theory from stored trajectories."""
import json
import math
import random
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import (Model, Meter, Restricted, apcg_run, cd_run,
                     exact_support_solver, fit_exponent)
import zoo

t0 = time.time()
out = {}

# ---- (a) delta = 0.01 ------------------------------------------------------
ALPHAS = [2.0 ** -4, 2.0 ** -6, 2.0 ** -8, 2.0 ** -10, 2.0 ** -12]
for gname, make, rho in [("star", lambda: zoo.star(250), 1 / 2000.),
                         ("path", lambda: zoo.path(1200), 1 / 4000.)]:
    adj, seed = make()
    rows = []
    for alpha in ALPHAS:
        mdl = Model(adj, alpha, seed)
        xstar, S = exact_support_solver(mdl, rho)
        R = Restricted(mdl, rho, S, xstar=xstar[S],
                       Fstar=mdl.F_rho(xstar, rho))
        Wl = []
        for s in range(5):
            res = apcg_run(R, Meter(mdl.adj), random.Random(3000 + s),
                           delta=0.01, want_sym=False)
            assert res["status"] == "ok"
            Wl.append(res["W_h"])
        res_gs = cd_run(R, Meter(mdl.adj), rule="gs", delta=0.01,
                        want_sym=False)
        rows.append(dict(alpha=alpha, volS=R.vol,
                         W_apcg=float(np.median(Wl)),
                         W_gs=res_gs["W_h"]))
        print(f"[{time.time()-t0:5.1f}s] d=0.01 {gname} "
              f"a=2^{round(math.log2(alpha))} vol={R.vol} "
              f"W_apcg={rows[-1]['W_apcg']:.3g} W_gs={rows[-1]['W_gs']:.3g}",
              flush=True)
    al = [r["alpha"] for r in rows]
    vols = np.array([r["volS"] for r in rows], float)
    pa, _ = fit_exponent(al, np.array([r["W_apcg"] for r in rows]) / vols)
    pg, _ = fit_exponent(al, np.array([r["W_gs"] for r in rows]) / vols)
    out[f"delta001_{gname}"] = dict(rows=rows, p_norm_apcg=pa, p_norm_gs=pg)
    print(f"  delta=0.01 {gname}: p_norm apcg={pa:.3f} gs={pg:.3f}",
          flush=True)

# ---- (b) K2 mean/max -------------------------------------------------------
adj, _ = zoo.complete(2)
k2rows = []
for q in (1 / 100., 1 / 300., 1 / 1000.):
    alpha = q * q / (1 + q * q)
    mdl = Model(adj, alpha, {0: .5, 1: .5})
    xstar, S = exact_support_solver(mdl, 1 / 16.)
    R = Restricted(mdl, 1 / 16., S, xstar=xstar[S],
                   Fstar=mdl.F_rho(xstar, 1 / 16.))
    its = []
    for s in range(40):
        res = apcg_run(R, Meter(mdl.adj), random.Random(5000 + s),
                       want_sym=False, check_every=2)
        its.append(res["it_h"])
    k2rows.append(dict(q=q, mean=float(np.mean(its)),
                       median=float(np.median(its)),
                       mx=int(np.max(its)), mn=int(np.min(its))))
    print(f"[{time.time()-t0:5.1f}s] K2 q=1/{round(1/q)} mean={k2rows[-1]['mean']:.0f} "
          f"median={k2rows[-1]['median']:.0f} max={k2rows[-1]['mx']}",
          flush=True)
pm, _ = fit_exponent([r["q"] for r in k2rows], [r["mean"] for r in k2rows])
px, _ = fit_exponent([r["q"] for r in k2rows], [r["mx"] for r in k2rows])
out["k2_meanmax"] = dict(rows=k2rows, p_mean=pm, p_max=px)
print(f"  K2 40 seeds: mean-iter ~ q^-{pm:.3f}, max-iter ~ q^-{px:.3f}",
      flush=True)

# ---- (c) gap-rate from stored trajectories ---------------------------------
traj = json.load(open("/home/claude/work/overnight/w3_apcg/results_traj.json"))
rates = {}
for key in ("star_a0.000244141_apcg", "path_a0.000244141_apcg",
            "star_a0.015625_apcg"):
    if key not in traj:
        continue
    T = [t for t in traj[key] if t[4] is not None and t[4] > 0]
    its = np.array([t[0] for t in T], float)
    gap = np.array([t[4] for t in T], float)
    q1 = len(T) // 5
    sl = np.polyfit(its[q1:], np.log(gap[q1:]), 1)[0]
    # theory: per-iteration factor (1 - a), a = sqrt(sigma)/n
    gname = key.split("_")[0]
    alpha = float(key.split("_a")[1].split("_")[0])
    rates[key] = dict(slope=float(sl))
    print(f"  gap-rate {key}: fitted slope/iter={sl:.3e}", flush=True)
out["gap_rates"] = rates

with open("/home/claude/work/overnight/w3_apcg/results_extra.json", "w") as f:
    json.dump(out, f, indent=1)
print(f"TOTAL {time.time()-t0:.1f}s")
