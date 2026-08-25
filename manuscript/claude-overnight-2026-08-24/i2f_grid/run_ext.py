"""I2-F extensions:
 (1) deep-alpha 2D cell (alpha = 2^-12, eps = 1e-6, w = 773) to extend the
     alpha-exponent lever arm for MG vs Chebyshev;
 (2) 3D sanity (dimension dependence of the parameter map and of MG).
"""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/i2f_grid")
from gridlib import (LatticeModel, VecMeter, support_stats, push_c,
                     cheb_local, mg_local, nd_ees)

OUT = "/home/claude/work/overnight/i2f_grid/out"
res = {"2d_deep": [], "3d": []}


def kappa(alpha, dim):
    return math.sqrt(4.0 * dim * alpha / (1.0 - alpha))


# ---------------------------------------------------------------- 2D deep --
for (a, eps, w) in [(2.0 ** -12, 1e-6, 773)]:
    t0 = time.time()
    M = LatticeModel(w, a, 2)
    x0 = M.solve_exact()
    ss = support_stats(M, eps)
    r = dict(alpha=a, eps=eps, w=w, n=M.n, **ss,
             target_classic=1 / (math.sqrt(a) * eps))
    mm = VecMeter(M.d)
    o = mg_local(M, eps, mm, x_exact=x0)
    e = M.semantic_err(o["x"])
    r.update(W_mg=mm.total(), m_mg=o["m"], cyc_mg=o["cycles"],
             err_mg=e, mg_status=o["status"], volOmega_mg=o["volOmega"])
    assert e <= eps * (1 + 1e-9)
    mm = VecMeter(M.d)
    o = cheb_local(M, eps, mm, max_wall=400.0)
    e = M.semantic_err(o["x"])
    r.update(W_cheb=mm.total(), it_cheb=o["iters"], err_cheb=e,
             cheb_status=o["status"])
    if o["status"] == "cert":
        assert e <= eps * (1 + 1e-9)
    r["wall"] = time.time() - t0
    res["2d_deep"].append(r)
    print(f"2D deep a=2^-12 eps=1e-6 w={w} volS={ss['volS']:.0f} "
          f"R={ss['R']} | mg={r['W_mg']:.3g} (m={r['m_mg']} "
          f"cyc={r['cyc_mg']}) W/vol={r['W_mg']/ss['volS']:.1f} | "
          f"cheb={r['W_cheb']:.3g} W/vol={r['W_cheb']/ss['volS']:.1f} "
          f"[{r['wall']:.0f}s]", flush=True)
    with open(f"{OUT}/ext.json", "w") as f:
        json.dump(res, f, default=str)

# -------------------------------------------------------------------- 3D --
for a in (2.0 ** -4, 2.0 ** -6, 2.0 ** -8):
    for eps in (1e-4, 1e-5, 1e-6, 1e-7):
        R = math.log(max(2.0, a / (6 * eps))) / kappa(a, 3) if eps < a else 1
        w = int(2 * math.ceil(max(3.0, 1.35 * R)) + 7) | 1
        if w > 73:
            print(f"  3D skip a=2^{round(math.log2(a))} eps={eps:g} (w={w})",
                  flush=True)
            continue
        t0 = time.time()
        M = LatticeModel(w, a, 3)
        x0 = M.solve_exact()
        ss = support_stats(M, eps)
        if ss["nS"] == 0:
            print(f"  3D trivial a=2^{round(math.log2(a))} eps={eps:g}",
                  flush=True)
            res["3d"].append(dict(alpha=a, eps=eps, w=w, trivial=True, **ss))
            continue
        r = dict(alpha=a, eps=eps, w=w, n=M.n, trivial=False, **ss,
                 target_classic=1 / (math.sqrt(a) * eps),
                 target_push=1 / (a * eps))
        mm = VecMeter(M.d)
        o = mg_local(M, eps, mm, x_exact=x0)
        e = M.semantic_err(o["x"])
        r.update(W_mg=mm.total(), m_mg=o["m"], cyc_mg=o["cycles"], err_mg=e,
                 mg_status=o["status"], volOmega_mg=o["volOmega"])
        if o["status"] == "cert":
            assert e <= eps * (1 + 1e-9), ("mg3d", e, eps)
        mm = VecMeter(M.d)
        o = cheb_local(M, eps, mm, max_wall=120.0)
        e = M.semantic_err(o["x"])
        r.update(W_cheb=mm.total(), it_cheb=o["iters"], err_cheb=e,
                 cheb_status=o["status"])
        if 0.3 / (a * eps) < 5e8:
            p = push_c(M, eps)
            e = M.semantic_err(p["x"])
            assert e <= eps * (1 + 1e-9), ("push3d", e, eps)
            r.update(W_push=p["W"], err_push=e)
        else:
            r.update(W_push=float("nan"))
        mm = VecMeter(M.d)
        o = nd_ees(M, eps, mm, x_exact=x0)
        r.update(W_nd=mm.total(), m_nd=o["m"], nd_status=o["status"])
        if o["status"] == "cert":
            assert M.semantic_err(o["x"]) <= eps * (1 + 1e-9)
        r["wall"] = time.time() - t0
        res["3d"].append(r)
        vs = ss["volS"]
        print(f"3D a=2^{round(math.log2(a)):>3d} eps={eps:g} w={w} "
              f"nS={ss['nS']} volS={vs:.0f} R={ss['R']} "
              f"Tclassic/volS={r['target_classic']/vs:.2f} | "
              f"mg={r['W_mg']:.3g}({r['W_mg']/vs:.0f}x) "
              f"cheb={r['W_cheb']:.3g}({r['W_cheb']/vs:.0f}x) "
              f"push={r['W_push']:.3g} nd={r['W_nd']:.3g}"
              f"({r['W_nd']/vs:.0f}x) [{r['wall']:.0f}s]", flush=True)
        with open(f"{OUT}/ext.json", "w") as f:
            json.dump(res, f, default=str)

with open(f"{OUT}/ext.json", "w") as f:
    json.dump(res, f, default=str)
print("done")
