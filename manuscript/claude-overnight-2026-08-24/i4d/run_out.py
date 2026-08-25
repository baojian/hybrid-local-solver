"""E1: exact OUTPUT-MEASURE sweep.  For every family and (alpha,eps) cell we
compute S_eps={v: pi_v/d_v > eps}, its cardinality, its DEGREE VOLUME, and the
volume of its outer boundary ring, and we test the identity vol(S_eps) < 1/eps."""
import json, math, sys, time
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4d")
import fam
from fam import GModel

OUT = "/home/claude/work/overnight/i4d/out"
EPS = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
ALPHAS = [2.0**-2, 2.0**-4, 2.0**-6, 2.0**-8, 2.0**-10, 2.0**-12,
          2.0**-14, 2.0**-16, 2.0**-20]


def builders():
    B = {}
    B["path"]        = lambda: fam.zoo.path(40000, seed_end=True)
    B["star"]        = lambda: fam.zoo.star(60000)
    B["spider"]      = lambda: fam.zoo.spider(64, 900)
    B["caterpillar"] = lambda: fam.zoo.caterpillar(30000, arm=1)
    B["comb"]        = lambda: fam.comb(400, 60)
    B["btree"]       = lambda: fam.zoo.binary_tree(16)
    B["rrt"]         = lambda: fam.rrt(60000)
    B["pa_tree"]     = lambda: fam.powerlaw_tree(60000)
    B["grid2d"]      = lambda: fam.fast_grid(401, 401)
    B["grid3d"]      = lambda: fam.fast_grid3(61)
    B["exp3reg"]     = lambda: fam.zoo.random_regular(40000, 3)
    B["complete"]    = lambda: fam.zoo.complete(400)
    B["cycle"]       = lambda: fam.zoo.cycle(40000)
    B["decoy_hub"]   = lambda: fam.zoo.decoy_hub(2000, 20000)
    return B


def main():
    rows = []
    B = builders()
    for name, mk in B.items():
        t0 = time.time()
        adj, seed = mk()
        n = len(adj)
        for a in ALPHAS:
            m = GModel(adj, a, seed)
            how = "cg" if name in ("exp3reg", "grid3d", "complete") else "lu"
            try:
                _, u = fam.exact_u(m, how=how)
            except Exception as e:
                print(name, a, "SOLVEFAIL", e, flush=True); continue
            for eps in EPS:
                st = fam.out_stats(m, eps, u=u)
                st.update(family=name, n=n, alpha=a, eps=eps,
                          clipped=(st["nB"] == 0 and st["nS"] > 0),
                          Winf=1.0 / eps, target_fy=1.0 / (math.sqrt(a) * eps))
                rows.append(st)
            del m
        print(f"{name}: n={n} done in {time.time()-t0:.1f}s", flush=True)
    with open(f"{OUT}/out_measure.json", "w") as f:
        json.dump(rows, f)
    # ---- summary ----
    print("\n%-12s %8s | %-38s | %-24s" % ("family", "n",
          "max vol(S_eps)*eps  (unclipped)", "max volB/volS"))
    for name in B:
        rs = [r for r in rows if r["family"] == name and not r["clipped"]
              and r["nS"] > 0]
        if not rs:
            print("%-12s  (all cells clipped or empty)" % name); continue
        best = max(rs, key=lambda r: r["volS_eps"])
        rb = max(rs, key=lambda r: (r["volB"] / max(r["volS"], 1.0)))
        viol = [r for r in rs if r["volS_eps"] >= 1.0]
        print("%-12s %8d | %.4f  @ a=2^%-5.1f eps=%.0e nS=%-7d | %.2f @ a=2^%-5.1f eps=%.0e  %s"
              % (name, best["n"], best["volS_eps"], math.log2(best["alpha"]),
                 best["eps"], best["nS"],
                 rb["volB"] / max(rb["volS"], 1.0), math.log2(rb["alpha"]),
                 rb["eps"], ("VIOLATION" if viol else "")))


main()
