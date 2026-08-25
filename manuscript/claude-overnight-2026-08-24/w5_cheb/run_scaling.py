"""Phase 2: end-to-end degree-charged work scaling W(alpha, eps) per graph,
variants vs push and untruncated Chebyshev.  Fits W ~ alpha^-p eps^-q."""
import sys
import math
import json
import time
import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w5_cheb")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from cheb import (cheb_sweep, cheb_restarted, cheb_meas, push_solve,
                  VecMeter, consts, K_cert, fit_pq)  # noqa
from model import Model  # noqa
import zoo  # noqa

BUILDERS = {
    "path_end": lambda eps: zoo.path(1500),
    "spider": lambda eps: zoo.spider(16, 100),
    "star_center": lambda eps: zoo.star(max(8, int(round(1 / (4 * eps))))),
    "star_leaf": lambda eps: zoo.star(10000, center_seed=False),
    "caterpillar": lambda eps: zoo.caterpillar(400, 1),
    "btree": lambda eps: zoo.binary_tree(12),
    "decoy_hub": lambda eps: zoo.decoy_hub(60, 20000),
    "grid": lambda eps: zoo.grid(100, 100),
}
ALPHAS = [2 ** -4, 2 ** -6, 2 ** -8, 2 ** -10, 2 ** -12]
EPSS = [1e-2, 1e-3]

rows = []
t_start = time.time()
for gname, build in BUILDERS.items():
    for eps in EPSS:
        adj, seed = build(eps)
        for alpha in ALPHAS:
            mod = Model(adj, alpha, seed)
            x0 = mod.solve_exact()

            def rec(algo, m, out, err, cert, extra=None):
                # target: certificate cert_resid <= alpha*eps (=> err <= eps)
                d = dict(graph=gname, alpha=alpha, eps=eps, algo=algo,
                         n=mod.n, W_scan=m.scan_work(), W_total=m.total(),
                         err=err, cert=cert,
                         ok=bool(cert <= alpha * eps * 1.001),
                         status=out.get("status"), iters=out.get("k",
                         out.get("iters", out.get("sweeps"))))
                if extra:
                    d.update(extra)
                rows.append(d)
                return d

            # untruncated Chebyshev, stop at true certificate (oracle eval)
            m = VecMeter(mod)
            out = cheb_sweep(mod, eps, mode="none", stop="cert_oracle",
                             meter=m, hard_factor=4)
            rec("cheb_none", m, out, mod.semantic_err(out["x"], x0),
                mod.cert_resid(out["x"]))

            # fixed-tau grid, cert_oracle stop; cheapest passing
            best = None
            for lab, tau0 in (("t_eps", 0.25 * eps),
                              ("t_sqa", 0.25 * eps * math.sqrt(alpha)),
                              ("t_a", 0.25 * eps * alpha)):
                m = VecMeter(mod)
                out = cheb_sweep(mod, eps, mode="fixed", tau0=tau0,
                                 stop="cert_oracle", meter=m, hard_factor=4)
                cert = mod.cert_resid(out["x"])
                if cert <= alpha * eps * 1.001 and (
                        best is None or m.scan_work() < best[0].scan_work()):
                    best = (m, out, cert, lab)
            if best:
                rec("cheb_fixed", best[0], best[1],
                    mod.semantic_err(best[1]["x"], x0), best[2],
                    dict(tau=best[3]))
            # ledger-certified single sweep
            m = VecMeter(mod)
            out = cheb_sweep(mod, eps, mode="cert", stop="ledger", meter=m)
            rec("cheb_cert", m, out, mod.semantic_err(out["x"], x0),
                mod.cert_resid(out["x"]))

            # restarted, measured-certificate
            m = VecMeter(mod)
            out = cheb_restarted(mod, eps, m)
            rec("cheb_restart", m, out, mod.semantic_err(out["x"], x0),
                mod.cert_resid(out["x"]), dict(cycles=out["cycles"]))

            # per-iteration measured certificate + adaptive semantic tau
            m = VecMeter(mod)
            out = cheb_meas(mod, eps, m)
            rec("cheb_meas", m, out, mod.semantic_err(out["x"], x0),
                mod.cert_resid(out["x"]), dict(tau_final=out["tau_final"]))

            # push baseline: eps_appr = eps gives cert = alpha*max r/d
            m = VecMeter(mod)
            out = push_solve(mod, eps, m, max_sweeps=250_000)
            rec("push", m, out, mod.semantic_err(out["x"], x0),
                mod.cert_resid(out["x"]))
            print(f"{gname:12s} a=2^{int(math.log2(alpha)):3d} eps={eps:g} "
                  f"done  [{time.time()-t_start:6.1f}s]", flush=True)

with open("/home/claude/work/overnight/w5_cheb/out/scaling.json", "w") as f:
    json.dump(rows, f)

# ---- fits ----
print("\n=== fits: W_scan ~ alpha^-p eps^-q (ok runs only) ===")
fits = {}
for gname in BUILDERS:
    for algo in ("cheb_none", "cheb_fixed", "cheb_cert", "cheb_restart",
                 "cheb_meas", "push"):
        sub = [r for r in rows if r["graph"] == gname and r["algo"] == algo
               and r["ok"]]
        if len(sub) >= 6:
            ft = fit_pq(sub)
            fits[f"{gname}/{algo}"] = ft
            print(f"{gname:12s} {algo:12s} p={ft['p']:5.2f} q={ft['q']:5.2f} "
                  f"rms={ft['rms']:.2f} (n={len(sub)})")
        else:
            print(f"{gname:12s} {algo:12s} -- only {len(sub)} ok runs")
with open("/home/claude/work/overnight/w5_cheb/out/fits.json", "w") as f:
    json.dump(fits, f)
