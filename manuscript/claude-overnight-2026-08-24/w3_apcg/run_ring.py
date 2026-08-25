"""I2-A ring probes: (1) hub-degree scaling of the spurious volume ratio,
(2) graded ring -> the momentum overshoot threshold tau(alpha),
(3) mitigations (gate hysteresis, deferred-confirmation batching)."""
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

ALPHAS = [2.0 ** -6, 2.0 ** -8, 2.0 ** -10, 2.0 ** -12]


def ring_graded(m=40, dmin=8, dmax=512):
    """Star core, hub k has degree geometrically spaced in [dmin, dmax];
    since rel_j = |grad_j|/lam_j is exactly proportional to 1/d_j, this
    grades the KKT slack over a dmax/dmin range in one graph."""
    degs = [int(round(dmin * (dmax / dmin) ** (k / (m - 1))))
            for k in range(m)]
    edges = [(0, k + 1) for k in range(m)]
    nid = m + 1
    hubs = []
    for k in range(m):
        hub = nid
        nid += 1
        edges.append((k + 1, hub))
        for _ in range(degs[k] - 1):
            edges.append((hub, nid))
            nid += 1
        hubs.append(hub)
    return FA._sym(edges, nid), 0, dict(hubs=hubs, m=m, degs=degs, n=nid)


def cell(adj, sd, hubs, alpha, tune, nseed=5, tag="", **kw):
    rho, rel = FA.tune_rho_breakpoint(adj, sd, alpha, hubs, target_rel=tune)
    mdl = Model(adj, alpha, sd)
    xstar, Strue = exact_support_solver(mdl, rho)
    Rfix = Restricted(mdl, rho, Strue, xstar=xstar[Strue])
    Wf = [apcg_run(Rfix, Meter(mdl.adj), random.Random(900 + s),
                   want_sym=False)["W_h"] for s in range(nseed)]
    grad = mdl.Q @ xstar - mdl.b
    lam = mdl.alpha * rho * mdl.sqd
    rels = {h: float(-grad[h] / lam[h]) for h in hubs}
    W, sv, sn, ms, er, adm_rel = [], [], [], [], [], []
    for s in range(nseed):
        r = apcg_grow2(mdl, rho, random.Random(900 + s), Strue,
                       variant="carry", **kw)
        W.append(r["W"]); sv.append(r["spur_vol"]); sn.append(r["spurious"])
        ms.append(r["missed"])
        xf = np.zeros(mdl.n)
        for g_, v in zip(r["S"], r["x"]):
            xf[g_] = v
        er.append(float(np.max(np.abs(xf - xstar) / mdl.sqd)))
        got = [rels[h] for h in hubs if h in set(r["S"]) and h not in
               set(Strue)]
        adm_rel.append(min(got) if got else None)
    tau = [t for t in adm_rel if t is not None]
    out = dict(alpha=alpha, rho=rho, hub_rel_max=rel, volS=Rfix.vol,
               nS=Rfix.n, W_fixed=float(np.median(Wf)),
               W=float(np.median(W)), ratio=float(np.median(W) / np.median(Wf)),
               spur_vol=int(max(sv)), spur_nodes=int(max(sn)),
               spur_ratio=float(max(sv)) / Rfix.vol, missed=int(max(ms)),
               err=float(max(er)), err_ok=bool(max(er) <= 0.1 * rho),
               tau=float(min(tau)) if tau else None,
               n_hubs_admitted=int(max(
                   sum(1 for h in hubs if rels[h] >= (min(tau) if tau else 9))
                   for _ in [0])) if tau else 0)
    print(f"  {tag} a=2^{round(math.log2(alpha))} vol={Rfix.vol} "
          f"W={out['W']:.4g} ({out['ratio']:.2f}x) spur={out['spur_nodes']}"
          f"/{out['spur_vol']} ({out['spur_ratio']:.2f}xvol) "
          f"miss={out['missed']} tau={out['tau']} err_ok={out['err_ok']}",
          flush=True)
    return out


def main():
    t0 = time.time()
    res = {}
    what = sys.argv[1:] or ["degscale", "graded", "mitig"]

    if "degscale" in what:
        print("== hub-degree scaling (alpha=2^-10, m=60) ==", flush=True)
        res["degscale"] = []
        for hd in [12, 24, 48, 96, 192]:
            adj, sd, meta = FA.ring_star(m=60, hub_deg=hd)
            c = cell(adj, sd, meta["hubs"], 2.0 ** -10, 0.985, nseed=3,
                     tag=f"hub_deg={hd}")
            c["hub_deg"] = hd
            res["degscale"].append(c)
        print(f"  [{time.time()-t0:.1f}s]", flush=True)

    if "graded" in what:
        print("== graded ring: overshoot threshold tau(alpha) ==", flush=True)
        adj, sd, meta = ring_graded(m=40, dmin=8, dmax=512)
        res["graded"] = []
        for alpha in ALPHAS:
            c = cell(adj, sd, meta["hubs"], alpha, 0.99, nseed=5,
                     tag="graded")
            res["graded"].append(c)
        f = fit_exponent([c["alpha"] for c in res["graded"]],
                         [c["W"] / c["volS"] for c in res["graded"]])
        res["graded_fit"] = dict(p_vol=f[0], dev=f[1])
        print(f"  graded p_vol={f[0]:.3f} dev={f[1]:.2f} "
              f"[{time.time()-t0:.1f}s]", flush=True)

    if "mitig" in what:
        adj, sd, meta = FA.ring_star(m=60, hub_deg=48)
        hubs = meta["hubs"]
        cfgs = {
            "base": {},
            "hyst2": dict(gate_mult=2.0),
            "hyst4": dict(gate_mult=4.0),
            "batch": dict(recheck=True, batch_iters=0),
            "hyst2_batch": dict(gate_mult=2.0, recheck=True, batch_iters=0),
        }
        for cn, kw in cfgs.items():
            print(f"== mitigation {cn} {kw} ==", flush=True)
            cells = []
            for alpha in ALPHAS:
                kw2 = dict(kw)
                if kw2.get("batch_iters", None) == 0 and "recheck" in kw2:
                    kw2["batch_iters"] = max(1, int(1.0 / math.sqrt(alpha)))
                cells.append(cell(adj, sd, hubs, alpha, 0.985, nseed=5,
                                  tag=cn, **kw2))
            f = fit_exponent([c["alpha"] for c in cells],
                             [c["W"] / c["volS"] for c in cells])
            res[f"mitig_{cn}"] = dict(cells=cells, p_vol=f[0], dev=f[1])
            print(f"  {cn}: p_vol={f[0]:.3f} maxspur="
                  f"{max(c['spur_ratio'] for c in cells):.2f}xvol "
                  f"maxmiss={max(c['missed'] for c in cells)} "
                  f"[{time.time()-t0:.1f}s]", flush=True)

    fn = "/home/claude/work/overnight/w3_apcg/results_ring.json"
    try:
        prev = json.load(open(fn))
    except Exception:
        prev = {}
    prev.update(res)
    with open(fn, "w") as fh:
        json.dump(prev, fh, indent=1, default=str)
    print(f"TOTAL {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
