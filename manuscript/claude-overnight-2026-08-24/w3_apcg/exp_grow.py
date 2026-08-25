"""Growing-support APCG with the safe expansion gate.

Start S_0 = violating seeds; every |S| iterations evaluate the boundary:
admit j when grad_j f(x) < -alpha*rho*sqrt(d_j) (safe gate; exact certificate
only when 0 <= x <= x*, which momentum can violate -> track spurious
admissions, i.e. admitted nodes not in supp(x*)).

Variants: restart (z <- x, fresh momentum each admission) and carry
(keep the two-accumulator state, append zeros for new coordinates).
Compare total charged work vs the fixed-support APCG run.
"""
import json
import math
import random
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import (Model, Meter, Restricted, apcg_run,
                     exact_support_solver)
import zoo

ALPHAS = [2.0 ** -6, 2.0 ** -10, 2.0 ** -12]
INSTANCES = {
    "star": dict(make=lambda: zoo.star(250), rho=1.0 / 2000),
    "path": dict(make=lambda: zoo.path(1200), rho=1.0 / 4000),
    "spider": dict(make=lambda: zoo.spider(6, 150), rho=1.0 / 4000),
    "caterpillar": dict(make=lambda: zoo.caterpillar(500, 1), rho=1.0 / 4000),
}
MAX_TOTAL_IT = 40_000_000


def apcg_grow(mdl, rho, rng, Strue, variant="restart", delta=0.1):
    lam = mdl.alpha * rho * mdl.sqd
    S = sorted(int(i) for i in np.nonzero(mdl.s)[0]
               if mdl.b[i] > lam[i])
    meter = Meter(mdl.adj)
    for g in S:
        meter.rec(int(mdl.d[g]))          # incremental structure exposure
    xmap = {}
    smap = {}                             # carry: node -> (p, Mh)
    phi_carry = 1.0
    n_admit_events = 0
    n_admitted = 0
    spurious = []
    tot_iters = 0
    Strueset = set(Strue)
    while True:
        R = Restricted(mdl, rho, S, boundary=True)
        if variant == "carry":
            p0 = [smap.get(g, (0.0, 0.0))[0] for g in R.S]
            M0 = [smap.get(g, (0.0, 0.0))[1] for g in R.S]
            res = apcg_run(R, meter, rng, delta=delta, boundary=True,
                           want_sym=False, state=(p0, M0, phi_carry),
                           max_iter=MAX_TOTAL_IT - tot_iters)
        else:
            x0 = [xmap.get(g, 0.0) for g in R.S]
            res = apcg_run(R, meter, rng, delta=delta, boundary=True,
                           want_sym=False, x0=x0,
                           max_iter=MAX_TOTAL_IT - tot_iters)
        tot_iters += res["iters"]
        if res["status"] == "admit":
            n_admit_events += 1
            adm = res["admit"]
            n_admitted += len(adm)
            spurious += [j for j in adm if j not in Strueset]
            if variant == "carry":
                p, Mh, phi_carry = res["state"]
                smap = {g: (p[k], Mh[k]) for k, g in enumerate(R.S)}
            else:
                xmap = {g: float(v) for g, v in zip(R.S, res["x"])}
            for j in adm:
                meter.rec(int(mdl.d[j]))
            S = sorted(set(S) | set(adm))
            continue
        return dict(status=res["status"], W=meter.total(),
                    iters=tot_iters, nS=len(S), volS=R.vol,
                    admit_events=n_admit_events, admitted=n_admitted,
                    spurious=len(spurious), spurious_nodes=spurious[:20],
                    x=res["x"], S=S,
                    missed=len(set(Strue) - set(S)))


def main():
    t0 = time.time()
    out = {}
    for gname, spec in INSTANCES.items():
        adj, seed = spec["make"]()
        rho = spec["rho"]
        out[gname] = []
        for alpha in ALPHAS:
            mdl = Model(adj, alpha, seed)
            xstar, Strue = exact_support_solver(mdl, rho)
            Fstar = mdl.F_rho(xstar, rho)
            Rfix = Restricted(mdl, rho, Strue, xstar=xstar[Strue],
                              Fstar=Fstar)
            cell = dict(alpha=alpha, nS=Rfix.n, volS=Rfix.vol)
            # fixed-support reference (same rngs)
            Wf = []
            for s in range(3):
                res = apcg_run(Rfix, Meter(mdl.adj), random.Random(700 + s),
                               want_sym=False)
                Wf.append(res["W_h"])
            cell["W_fixed"] = float(np.median(Wf))
            for variant in ("restart", "carry"):
                Wg, evs, spur, errs, miss = [], [], [], [], []
                for s in range(3):
                    res = apcg_grow(mdl, rho, random.Random(700 + s),
                                    Strue, variant=variant)
                    if res["status"] != "ok":
                        print("  CAP/FAIL", gname, alpha, variant, s,
                              res["status"], flush=True)
                    Wg.append(res["W"])
                    evs.append(res["admit_events"])
                    spur.append(res["spurious"])
                    miss.append(res["missed"])
                    xf = np.zeros(mdl.n)
                    for g_, v in zip(res["S"], res["x"]):
                        xf[g_] = v
                    errs.append(float(np.max(
                        np.abs(xf - xstar) / mdl.sqd)))
                cell[variant] = dict(
                    W=float(np.median(Wg)),
                    ratio=float(np.median(Wg)) / cell["W_fixed"],
                    admit_events=evs, spurious=spur, missed=miss,
                    err=max(errs))
                print(f"[{time.time()-t0:6.1f}s] {gname} "
                      f"a=2^{round(math.log2(alpha))} {variant}: "
                      f"W={cell[variant]['W']:.3g} "
                      f"(x{cell[variant]['ratio']:.2f} vs fixed "
                      f"{cell['W_fixed']:.3g}) "
                      f"events={evs} spurious={spur} missed={miss} "
                      f"err={cell[variant]['err']:.1e}", flush=True)
            out[gname].append(cell)
    with open("/home/claude/work/overnight/w3_apcg/results_grow.json",
              "w") as f:
        json.dump({g: [{k: v for k, v in c.items()} for c in cs]
                   for g, cs in out.items()}, f, indent=1, default=str)
    print(f"TOTAL {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
