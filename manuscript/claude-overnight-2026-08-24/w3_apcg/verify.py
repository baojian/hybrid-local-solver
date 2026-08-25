"""Verification of the APCG implementation on tiny problems.

1. exact_support_solver vs Model.rppr_exact (ISTA to 1e-14).
2. lazy APCG vs full-vector reference APCG with the UNSIMPLIFIED paper
   step 4, same rng: iterates must match to roundoff.
3. Expected objective decrease: mean gap over many seeds decays at least at
   the theoretical rate (1 - sqrt(sigma)/n) per iteration.
4. Baselines converge to xstar.
5. Long-run lazy-representation stability at small alpha.
"""
import math
import random
import sys

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import (Model, Meter, Restricted, apcg_run, apcg_reference,
                     cd_run, ista_run, exact_support_solver)
import zoo

ok = True


def report(name, cond, detail=""):
    global ok
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond:
        ok = False


# ---- 1. ground truth solver ------------------------------------------------
adj, seed = zoo.path(12)
mdl = Model(adj, 0.3, seed)
rho = 0.05
xs, S = exact_support_solver(mdl, rho)
xs2 = mdl.rppr_exact(rho, tol=1e-15)
report("exact-vs-ISTA path12", np.max(np.abs(xs - xs2)) < 1e-11,
       f"maxdiff={np.max(np.abs(xs - xs2)):.2e} |S|={len(S)}")

adj, seed = zoo.star(20)
mdl_s = Model(adj, 2.0 ** -6, seed)
rho_s = 1.0 / 160
xs_s, S_s = exact_support_solver(mdl_s, rho_s)
xs2_s = mdl_s.rppr_exact(rho_s, tol=1e-15)
report("exact-vs-ISTA star20", np.max(np.abs(xs_s - xs2_s)) < 1e-11,
       f"maxdiff={np.max(np.abs(xs_s - xs2_s)):.2e} |S|={len(S_s)}")

# ---- 2. lazy vs reference (unsimplified step 4) ----------------------------
R = Restricted(mdl, rho, S, xstar=xs[S], Fstar=mdl.F_rho(xs, rho))
for trial, iters in [(0, 300), (1, 997)]:
    rng1 = random.Random(42 + trial)
    rng2 = random.Random(42 + trial)
    res = apcg_run(R, Meter(mdl.adj), rng1, delta=-1.0, max_iter=iters,
                   check_every=10 ** 9, want_sym=False)
    xref = apcg_reference(R, rng2, iters)
    scale = max(1.0, np.max(np.abs(xref)))
    d = np.max(np.abs(res["x"] - xref)) / scale
    report(f"lazy==reference iters={iters}", d < 1e-10, f"reldiff={d:.2e}")

# ---- 3. expected rate ------------------------------------------------------
adj, seed = zoo.path(30)
mdl3 = Model(adj, 2.0 ** -6, seed)
rho3 = 1.0 / 200
xs3, S3 = exact_support_solver(mdl3, rho3)
F3 = mdl3.F_rho(xs3, rho3)
R3 = Restricted(mdl3, rho3, S3, xstar=xs3[S3], Fstar=F3)
n3 = R3.n
a3 = math.sqrt(R3.sigma) / n3
K = int(12 / a3)
nseeds = 60
step = max(n3, K // 40)
gapmat = []
for s in range(nseeds):
    rng = random.Random(s)
    res = apcg_run(R3, Meter(mdl3.adj), rng, delta=-1.0, max_iter=K,
                   check_every=step, want_sym=False)
    gapmat.append([t[4] for t in res["traj"]])
L = min(len(r) for r in gapmat)
gapmat = np.array([r[:L] for r in gapmat])
mean_gap = gapmat.mean(axis=0)
its = np.arange(1, L + 1) * step
# fit exponential slope on the tail (skip first quarter)
q0 = L // 4
sl = np.polyfit(its[q0:], np.log(np.maximum(mean_gap[q0:], 1e-300)), 1)[0]
theory = math.log(1 - a3)
report("E[gap] decays >= theory rate", sl <= 0.8 * theory,
       f"measured slope/iter={sl:.3e}, theory (1-a): {theory:.3e}, "
       f"n={n3} a={a3:.3e}")
report("E[gap] monotone-ish",
       bool(np.all(np.diff(np.log(np.maximum(mean_gap, 1e-300))) < 0.5)),
       f"final mean gap={mean_gap[-1]:.2e} initial={mean_gap[0]:.2e}")

# ---- 4. all solvers converge to xstar --------------------------------------
for name, runner in [
        ("apcg", lambda: apcg_run(R3, Meter(mdl3.adj), random.Random(7))),
        ("cd-uniform", lambda: cd_run(R3, Meter(mdl3.adj),
                                      rng=random.Random(7), rule="uniform")),
        ("cd-gs", lambda: cd_run(R3, Meter(mdl3.adj), rule="gs")),
        ("ista", lambda: ista_run(R3, Meter(mdl3.adj)))]:
    res = runner()
    err = R3.err_vs_star(res["x"])
    report(f"{name} converges (h-stop, then sym)", res["status"] == "ok"
           and err < 0.2 * R3.rho, f"err={err:.2e} it_h={res['it_h']} "
           f"it_sym={res['it_sym']} W_h={res['W_h']}")

# ---- 5. long-run stability at small alpha ----------------------------------
adj, seed = zoo.path(40)
mdl5 = Model(adj, 2.0 ** -10, seed)
rho5 = 1.0 / 300
xs5, S5 = exact_support_solver(mdl5, rho5)
R5 = Restricted(mdl5, rho5, S5, xstar=xs5[S5], Fstar=mdl5.F_rho(xs5, rho5))
iters5 = 20000
rng1 = random.Random(3)
rng2 = random.Random(3)
res5 = apcg_run(R5, Meter(mdl5.adj), rng1, delta=-1.0, max_iter=iters5,
                check_every=10 ** 9, want_sym=False)
xref5 = apcg_reference(R5, rng2, iters5)
scale5 = max(np.max(np.abs(xref5)), 1e-30)
d5 = np.max(np.abs(res5["x"] - xref5)) / scale5
report("lazy stable 20k iters alpha=2^-10", d5 < 1e-8,
       f"reldiff={d5:.2e} n={R5.n}")

# and APCG at small alpha still reaches xstar
res5b = apcg_run(R5, Meter(mdl5.adj), random.Random(11))
err5 = R5.err_vs_star(res5b["x"])
report("apcg alpha=2^-10 reaches xstar", res5b["status"] == "ok"
       and err5 < 0.2 * R5.rho,
       f"err={err5:.2e} it_h={res5b['it_h']} status={res5b['status']}")

print("ALL PASS" if ok else "SOME FAILURES")
sys.exit(0 if ok else 1)
