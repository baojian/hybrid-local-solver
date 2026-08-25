"""I2-A driver: try to BREAK carry-mode growing-support APCG.

Families (a) marginal-hub ring (symmetric, tuned to the activation
breakpoint), (b) staircase path, (c) lollipop two-scale, (d) K8 pulse head
with a growing path tail.  Reports vol-normalized alpha-exponents, spurious
volume ratio, missed nodes, final semantic error.
"""
import json
import math
import random
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import (Model, Restricted, apcg_run, exact_support_solver,   # noqa
                     fit_exponent)
from meter import Meter                                                    # noqa
from grow2 import apcg_grow2                                               # noqa
import fam_attack as FA                                                    # noqa
import zoo                                                                 # noqa

ALPHAS = [2.0 ** -6, 2.0 ** -8, 2.0 ** -10, 2.0 ** -12]
NSEED = 5
NSEED_R = 3


def build_families():
    fams = {}
    adj, sd, meta = FA.ring_star(m=60, hub_deg=48)
    fams["ring"] = dict(adj=adj, seed=sd, meta=meta, tune=0.985)
    adj2, sd2, meta2 = FA.ring_star(m=60, hub_deg=48)
    fams["ring_edge"] = dict(adj=adj2, seed=sd2, meta=meta2, tune=0.9995)
    a, s = zoo.path(3000)
    fams["staircase"] = dict(adj=a, seed=s, rho=1.0 / 12000)
    a, s = FA.lollipop(16, 360)
    fams["lollipop"] = dict(adj=a, seed=s, rho=1.0 / 4000)
    a, s = FA.k8_embedded(260)
    fams["k8emb"] = dict(adj=a, seed=s, rho=1.0 / 2000)
    return fams


def run_cell(spec, alpha, t0, name, variants=("carry", "restart"),
             gate_mult=1.0, batch_iters=0, nseed=NSEED):
    adj, sd = spec["adj"], spec["seed"]
    if "tune" in spec:
        rho, rel = FA.tune_rho_breakpoint(adj, sd, alpha, spec["meta"]["hubs"],
                                          target_rel=spec["tune"])
    else:
        rho, rel = spec["rho"], None
    mdl = Model(adj, alpha, sd)
    xstar, Strue = exact_support_solver(mdl, rho)
    Fstar = mdl.F_rho(xstar, rho)
    Rfix = Restricted(mdl, rho, Strue, xstar=xstar[Strue], Fstar=Fstar)
    cell = dict(alpha=alpha, rho=rho, hub_rel=rel, nS=Rfix.n, volS=Rfix.vol)
    Wf = []
    for s in range(nseed):
        r = apcg_run(Rfix, Meter(mdl.adj), random.Random(900 + s),
                     want_sym=False)
        assert r["status"] == "ok", r["status"]
        Wf.append(r["W_h"])
    cell["W_fixed"] = float(np.median(Wf))
    for variant in variants:
        ns = nseed if variant == "carry" else NSEED_R
        Wg, evs, spurv, spurn, errs, miss, sts = [], [], [], [], [], [], []
        for s in range(ns):
            res = apcg_grow2(mdl, rho, random.Random(900 + s), Strue,
                             variant=variant, gate_mult=gate_mult,
                             batch_iters=batch_iters)
            Wg.append(res["W"])
            evs.append(res["admit_events"])
            spurv.append(res["spur_vol"])
            spurn.append(res["spurious"])
            miss.append(res["missed"])
            sts.append(res["status"])
            xf = np.zeros(mdl.n)
            for g_, v in zip(res["S"], res["x"]):
                xf[g_] = v
            errs.append(float(np.max(np.abs(xf - xstar) / mdl.sqd)))
        cell[variant] = dict(
            W=float(np.median(Wg)), Wmax=float(max(Wg)),
            ratio=float(np.median(Wg)) / cell["W_fixed"],
            events=int(np.median(evs)), spur_nodes=int(max(spurn)),
            spur_vol=int(max(spurv)),
            spur_ratio=float(max(spurv)) / Rfix.vol,
            missed=int(max(miss)), err=float(max(errs)),
            err_ok=bool(max(errs) <= 0.1 * rho),
            status=sorted(set(sts)))
        c = cell[variant]
        print(f"[{time.time()-t0:6.1f}s] {name} a=2^{round(math.log2(alpha))} "
              f"{variant} gm={gate_mult} bt={batch_iters}: W={c['W']:.4g} "
              f"({c['ratio']:.2f}x fix {cell['W_fixed']:.4g}) vol={Rfix.vol} "
              f"ev={c['events']} spur={c['spur_nodes']}/{c['spur_vol']} "
              f"(={c['spur_ratio']:.2f}xvol) miss={c['missed']} "
              f"err={c['err']:.1e}{'' if c['err_ok'] else ' !!'} "
              f"{c['status']}", flush=True)
    return cell


def fit_cells(cells, key):
    al = [c["alpha"] for c in cells]
    W = [c[key]["W"] if isinstance(c[key], dict) else c[key] for c in cells]
    Wn = [w / c["volS"] for w, c in zip(W, cells)]
    p_raw, r1 = fit_exponent(al, W)
    p_vol, r2 = fit_exponent(al, Wn)
    return dict(p_raw=p_raw, dev_raw=r1, p_vol=p_vol, dev_vol=r2)


def main():
    t0 = time.time()
    fams = build_families()
    which = sys.argv[1:] or list(fams)
    out = {}
    for name in which:
        spec = fams[name]
        cells = []
        for alpha in ALPHAS:
            cells.append(run_cell(spec, alpha, t0, name))
        fits = dict(fixed=fit_cells(cells, "W_fixed"),
                    carry=fit_cells(cells, "carry"),
                    restart=fit_cells(cells, "restart"))
        out[name] = dict(cells=cells, fits=fits)
        print(f"  == {name} exponents: fixed {fits['fixed']['p_vol']:.3f} | "
              f"carry {fits['carry']['p_vol']:.3f} "
              f"(raw {fits['carry']['p_raw']:.3f}, dev "
              f"{fits['carry']['dev_vol']:.2f}) | "
              f"restart {fits['restart']['p_vol']:.3f}", flush=True)
        with open("/home/claude/work/overnight/w3_apcg/results_attack.json",
                  "w") as f:
            json.dump(out, f, indent=1, default=str)
    print(f"TOTAL {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
