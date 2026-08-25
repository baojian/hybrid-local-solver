"""I3-A zoo sweep: local AMG vs push / Chebyshev / local direct elimination."""
import json
import math
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
import zoo
from amglib import (GModel, VecMeter, amg_local, support_stats, push_c,
                    cheb_local, direct_local)

OUT = "/home/claude/work/overnight/i3a_amg/out"


# ------------------------------------------------------------ generators ---

def fast_grid(w, h):
    adj = {}
    for y in range(h):
        for x in range(w):
            u = y * w + x
            nb = []
            if x: nb.append(u - 1)
            if x + 1 < w: nb.append(u + 1)
            if y: nb.append(u - w)
            if y + 1 < h: nb.append(u + w)
            adj[u] = sorted(nb)
    return adj, (h // 2) * w + w // 2


def fast_grid3(w):
    adj = {}
    for z in range(w):
        for y in range(w):
            for x in range(w):
                u = (z * w + y) * w + x
                nb = []
                if x: nb.append(u - 1)
                if x + 1 < w: nb.append(u + 1)
                if y: nb.append(u - w)
                if y + 1 < w: nb.append(u + w)
                if z: nb.append(u - w * w)
                if z + 1 < w: nb.append(u + w * w)
                adj[u] = sorted(nb)
    c = w // 2
    return adj, (c * w + c) * w + c


def rand_recursive_tree(n, sd=7):
    rng = random.Random(sd)
    adj = {i: [] for i in range(n)}
    for i in range(1, n):
        p = rng.randrange(i)
        adj[i].append(p); adj[p].append(i)
    return {u: sorted(v) for u, v in adj.items()}, 0


def grid_w(alpha, eps, cap=451):
    """Host grid side wide enough that the certified region fits inside."""
    kap = 2.0 * math.sqrt(2.0 * alpha)
    z = max(1.0, math.log(max(alpha / (math.pi * eps), 1.1)))
    R = z / kap
    return int(min(cap, 2 * int(math.ceil(2.6 * R)) + 7)) | 1


FAMILIES = {}


def fam(name, cap_n=None):
    def deco(f):
        FAMILIES[name] = f
        return f
    return deco


@fam("grid2d")
def _g(alpha, eps):
    w = grid_w(alpha, eps)
    a, s = fast_grid(w, w)
    return a, s, f"grid({w},{w})"


@fam("grid3d")
def _g3(alpha, eps):
    w = 41
    a, s = fast_grid3(w)
    return a, s, f"grid3({w}^3)"


@fam("double_cycle")
def _dc(alpha, eps):
    a, s = zoo.double_cycle(1500)
    return a, s, "double_cycle(1500) n=6000 3-reg closed prism"


@fam("binary_tree")
def _bt(alpha, eps):
    a, s = zoo.binary_tree(15)
    return a, s, "binary_tree(15) n=65535"


@fam("caterpillar")
def _cp(alpha, eps):
    a, s = zoo.caterpillar(15000, arm=1)
    return a, s, "caterpillar(15000,1) n=30000"


@fam("comb")
def _cb(alpha, eps):
    a, s = zoo.caterpillar(3000, arm=12)
    return a, s, "comb: caterpillar(3000,arm=12) n=39000"


@fam("spider")
def _sp(alpha, eps):
    a, s = zoo.spider(6, 6000)
    return a, s, "spider(6,6000) n=36001"


@fam("star")
def _st(alpha, eps):
    a, s = zoo.star(100000)
    return a, s, "star(100000)"


@fam("decoy_hub")
def _dh(alpha, eps):
    a, s = zoo.decoy_hub(20000, 4000)
    return a, s, "decoy_hub(20000,4000) n=24000"


@fam("rand_reg3")
def _r3(alpha, eps):
    a, s = zoo.random_regular(20000, 3)
    return a, s, "random_regular(20000,3)"


@fam("rand_reg4")
def _r4(alpha, eps):
    a, s = zoo.random_regular(20000, 4)
    return a, s, "random_regular(20000,4)"


@fam("rrt")
def _rt(alpha, eps):
    a, s = rand_recursive_tree(40000)
    return a, s, "random recursive tree n=40000"


# ---------------------------------------------------------------- driver ---

def _f(x):
    return float('nan') if x is None else float(x)


def opcomplexity(levels):
    if not levels:
        return None
    n0 = float(levels[0]["nnz"])
    return float(sum(l["nnz"] for l in levels)) / max(n0, 1.0)


def one(famname, alpha, eps, do_push=True, do_cheb=True, do_direct=True,
        verbose=False):
    if famname in ("rand_reg3", "rand_reg4", "rrt"):
        do_direct = False        # measured separately: fill is catastrophic
    adj, seed, desc = FAMILIES[famname](alpha, eps)
    m = GModel(adj, alpha, seed)
    t0 = time.perf_counter()
    x0 = m.solve_exact()
    st = support_stats(m, eps)
    res = dict(fam=famname, desc=desc, n=m.n, alpha=alpha, eps=eps,
               volG=float(m.d.sum()), volS=st["volS"], nS=st["nS"],
               Rsem=st["R"], t_exact=time.perf_counter() - t0)
    if st["nS"] == 0:
        res["degenerate"] = True
        return res
    # ---------------- AMG certified
    mt = VecMeter(m.d)
    t0 = time.perf_counter()
    r = amg_local(m, eps, mt, x_exact=x0, verbose=verbose)
    v = mt.vector()
    err = m.semantic_err(r["x"])
    res["amg"] = dict(status=r["status"], R=r["R"], cycles=r["cycles"],
                      tot_cycles=r.get("tot_cycles"),
                      attempts=r.get("attempts"), allrate=r.get("allrate"),
                      rmax_rate=r.get("rmax_rate"),
                      W_seq=v["total_seq"], agg=v["agg"],
                      rate=r["rate"], nlev=r.get("nlev"),
                      volOmega=r["volOmega"], nOmega=r.get("nOmega"),
                      opcx=opcomplexity(r.get("levels")),
                      W=v["total"], setup=v["setup"], solve=v["solve"],
                      C_adj=v["C_adj"], R_adj=v["R_adj"], C_rec=v["C_rec"],
                      C_resp=v["C_resp"], C_mat=v["C_mat"],
                      err=err, err_eps=err / eps, cert=r["cert"],
                      wall=time.perf_counter() - t0,
                      levels=r.get("levels"))
    # ---------------- AMG oracle-stopped
    mt2 = VecMeter(m.d)
    t0 = time.perf_counter()
    r2 = amg_local(m, eps, mt2, x_exact=x0, oracle=True)
    v2 = mt2.vector()
    err2 = m.semantic_err(r2["x"])
    res["amg_oracle"] = dict(status=r2["status"], R=r2["R"],
                             cycles=r2["cycles"], rate=r2["rate"],
                             volOmega=r2["volOmega"], W=v2["total"],
                             setup=v2["setup"], solve=v2["solve"],
                             err_eps=err2 / eps,
                             wall=time.perf_counter() - t0)
    # ---------------- push
    if do_push and 1.0 / (alpha * eps) <= 2e10:
        t0 = time.perf_counter()
        p = push_c(m, eps)
        errp = m.semantic_err(p["x"])
        res["push"] = dict(W=p["W"], err_eps=errp / eps,
                           wall=time.perf_counter() - t0)
    # ---------------- Chebyshev
    if do_cheb:
        mt3 = VecMeter(m.d)
        t0 = time.perf_counter()
        c = cheb_local(m, eps, mt3)
        v3 = mt3.vector()
        errc = m.semantic_err(c["x"])
        res["cheb"] = dict(W=v3["total"], iters=c["iters"],
                           status=c["status"], err_eps=errc / eps,
                           wall=time.perf_counter() - t0)
    # ---------------- local direct elimination (generalized ND-EES)
    if do_direct:
        mt4 = VecMeter(m.d)
        t0 = time.perf_counter()
        try:
            d = direct_local(m, eps, mt4, wall_cap=12.0)
            v4 = mt4.vector()
            errd = m.semantic_err(d["x"])
            res["direct"] = dict(W=v4["total"], status=d["status"],
                                 R=d["R"], err_eps=errd / eps,
                                 wall=time.perf_counter() - t0)
        except Exception as e:
            res["direct"] = dict(status="err", msg=str(e)[:120])
    return res


def main():
    fams = sys.argv[1].split(",") if len(sys.argv) > 1 else list(FAMILIES)
    alphas = [2 ** -4, 2 ** -8, 2 ** -12]
    epss = [1e-6, 1e-8]
    if len(sys.argv) > 2:
        epss = [float(x) for x in sys.argv[2].split(",")]
    tag = sys.argv[3] if len(sys.argv) > 3 else "main"
    out = []
    path = os.path.join(OUT, f"zoo_{tag}.json")
    for f in fams:
        for a in alphas:
            for e in epss:
                t0 = time.perf_counter()
                try:
                    r = one(f, a, e)
                except Exception as exc:
                    r = dict(fam=f, alpha=a, eps=e, error=str(exc)[:200])
                out.append(r)
                with open(path, "w") as fh:
                    json.dump(out, fh)
                A = r.get("amg", {})
                vs = max(r.get("volS", 1) or 1, 1)
                print(f"{f:14s} a=2^{int(round(math.log2(a))):<4d} e={e:g} "
                      f"n={r.get('n','-'):>7} volS={r.get('volS',0):>9.0f} "
                      f"Rs={r.get('Rsem','-'):>3} | AMG {A.get('status','-'):5s} "
                      f"R={A.get('R','-'):>4} cyc={A.get('cycles','-'):>3} "
                      f"rate={_f(A.get('allrate')):.3f} cy={A.get('tot_cycles') or 0:>3} "
                      f"opcx={_f(A.get('opcx')):.2f} "
                      f"W/vol={A.get('W',0)/vs:>9.1f} "
                      f"set%={100*A.get('setup',0)/max(A.get('W',1),1):>4.0f} "
                      f"e/eps={A.get('err_eps',float('nan')):.3f} "
                      f"| push {r.get('push',{}).get('W',float('nan'))/vs:>10.1f} "
                      f"cheb {r.get('cheb',{}).get('W',float('nan'))/vs:>9.1f} "
                      f"dir {r.get('direct',{}).get('W',float('nan'))/vs:>10.1f} "
                      f"[{time.perf_counter()-t0:.0f}s]", flush=True)
    print("wrote", path)


if __name__ == "__main__":
    main()
