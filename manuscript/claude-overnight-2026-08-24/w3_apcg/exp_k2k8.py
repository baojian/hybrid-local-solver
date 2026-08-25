"""Adversarial families K_2 and K_8: iteration-count scaling in q, where
alpha = q^2/(1+q^2).  Deterministic safeguarded accelerated-CD is blocked
per-trajectory on these (persistent low mode / pulse); question: does the
RANDOMIZED method's expected iteration count scale like 1/q (accelerated)
or 1/q^2 (blocked)?  n is constant, so work == iteration count."""
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

QS = [1.0 / 30, 1.0 / 100, 1.0 / 300, 1.0 / 1000]

FAMS = {
    "K2": dict(make=lambda: zoo.complete(2), rho=1.0 / 16,
               seed=lambda n: {i: 1.0 / n for i in range(n)}),
    "K8": dict(make=lambda: zoo.complete(8), rho=1.0 / 112,
               seed=lambda n: {i: 1.0 / n for i in range(n)}),
}


def main():
    t0 = time.time()
    out = {}
    for fam, spec in FAMS.items():
        adj, _ = spec["make"]()
        n = len(adj)
        rho = spec["rho"]
        rows = []
        for q in QS:
            alpha = q * q / (1.0 + q * q)
            mdl = Model(adj, alpha, spec["seed"](n))
            xstar, S = exact_support_solver(mdl, rho)
            assert len(S) == n, (fam, q, len(S))
            R = Restricted(mdl, rho, S, xstar=xstar[S],
                           Fstar=mdl.F_rho(xstar, rho))
            # APCG: 25 seeds
            its_a = []
            for s in range(25):
                res = apcg_run(R, Meter(mdl.adj), random.Random(50 + s),
                               want_sym=False, check_every=n)
                assert res["status"] == "ok", (fam, q, s, res["status"])
                its_a.append(res["it_h"])
            # uniform CD: fewer seeds at extreme q (1/q^2 cost)
            nseeds_cd = 15 if q >= 1.0 / 300 else 4
            its_c = []
            for s in range(nseeds_cd):
                res = cd_run(R, Meter(mdl.adj), rng=random.Random(90 + s),
                             rule="uniform", want_sym=False, check_every=n)
                assert res["status"] == "ok", (fam, q, s, res["status"])
                its_c.append(res["it_h"])
            row = dict(q=q, alpha=alpha,
                       apcg_med=float(np.median(its_a)),
                       apcg_iqr=[float(np.percentile(its_a, 25)),
                                 float(np.percentile(its_a, 75))],
                       cd_med=float(np.median(its_c)),
                       cd_iqr=[float(np.percentile(its_c, 25)),
                               float(np.percentile(its_c, 75))],
                       err_a=None)
            rows.append(row)
            print(f"[{time.time()-t0:6.1f}s] {fam} q=1/{round(1/q)} "
                  f"apcg_med={row['apcg_med']:.0f} "
                  f"iqr={row['apcg_iqr']}  cd_med={row['cd_med']:.0f}",
                  flush=True)
        lq = [r["q"] for r in rows]
        s_a, dev_a = fit_exponent(lq, [r["apcg_med"] for r in rows])
        s_c, dev_c = fit_exponent(lq, [r["cd_med"] for r in rows])
        # fit_exponent fits W ~ q^{-p} when passed q as "alpha"
        out[fam] = dict(rows=rows, slope_apcg=s_a, dev_apcg=dev_a,
                        slope_cd=s_c, dev_cd=dev_c)
        print(f"  {fam}: iter ~ q^-p  p_apcg={s_a:.3f} (dev {dev_a:.2f})  "
              f"p_cd={s_c:.3f} (dev {dev_c:.2f})", flush=True)
    with open("/home/claude/work/overnight/w3_apcg/results_k2k8.json",
              "w") as f:
        json.dump(out, f, indent=1)
    print(f"TOTAL {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
