"""I4-B sweep: the composed solver vs every single-mechanism baseline."""
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/i4b_composed")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/lib")

import zoo
import run_zoo
from amglib import (GModel, VecMeter, support_stats, push_c, amg_local,
                    direct_local)
from ledger import Ledger, from_vecmeter, KEYS
from composed import composed_solve, wy_active

OUT = "/home/claude/work/overnight/i4b_composed/out"

FAM = dict(run_zoo.FAMILIES)


def _path(alpha, eps):
    a, s = zoo.path(200000)
    return a, s, "path(200000) endpoint-seeded"


def _theta(alpha, eps):
    a, s = zoo.theta_graph(20000, 26000, 33000)
    return a, s, "theta(20000,26000,33000)"


FAM["path"] = _path
FAM["theta"] = _theta

ORDER = ["star", "path", "caterpillar", "comb", "spider", "theta",
         "decoy_hub", "double_cycle", "binary_tree", "rrt", "grid2d",
         "rand_reg3", "rand_reg4", "grid3d"]

EXTRA_BASE = {"path", "theta"}       # not in the I3-A json; run amg/direct


def lv(led):
    return led.vector()


_GCACHE = {}


def get_graph(famname, alpha, eps):
    key = (famname, alpha, eps) if famname == "grid2d" else famname
    if key not in _GCACHE:
        _GCACHE.clear()
        _GCACHE[key] = FAM[famname](alpha, eps)
    return _GCACHE[key]


def one(famname, alpha, eps, caps):
    adj, seed, desc = get_graph(famname, alpha, eps)
    m = GModel(adj, alpha, seed)
    t0 = time.perf_counter()
    x0 = m.solve_exact()
    st = support_stats(m, eps)
    res = dict(fam=famname, desc=desc, n=m.n, alpha=alpha, eps=eps,
               volG=float(m.d.sum()), volS=st["volS"], nS_eps=st["nS"],
               Rsem=st["R"], t_exact=time.perf_counter() - t0)
    if st["nS"] == 0:
        res["degenerate"] = True
        return res

    def run(tag, fn, cap):
        led = Ledger(m.d)
        tt = time.perf_counter()
        try:
            r = fn(led, cap)
        except Exception as e:
            res[tag] = dict(status="err", msg=str(e)[:160])
            return
        err = float(np.max(np.abs(r["x"] - x0) / m.sqd))
        cert = float(np.max(np.abs(m.Q @ r["x"] - m.b) / m.sqd))
        v = lv(led)
        v.update(status=r["status"], err=err, err_eps=err / eps,
                 certres=cert, cert_ok=bool(cert < alpha * eps),
                 wall=time.perf_counter() - tt,
                 rounds=r.get("rounds"), flips=r.get("flips"),
                 nS=r.get("nS"), volReg=r.get("volS"),
                 routes="".join("E" if q == "elim" else "A"
                                for q in r.get("routes", [])),
                 sweeps=r.get("sweeps"))
        res[tag] = v

    run("comp", lambda L, c: composed_solve(m, eps, L, wall_cap=c),
        caps["comp"])
    if eps == 1e-6:
        run("comp_pull", lambda L, c: composed_solve(m, eps, L, gate="pull",
                                                     wall_cap=c), caps["pull"])
    run("comp_E", lambda L, c: composed_solve(m, eps, L, force="elim",
                                              wall_cap=c), caps["forced"])
    run("comp_A", lambda L, c: composed_solve(m, eps, L, force="amg",
                                              wall_cap=c), caps["forced"])
    if alpha == 2 ** -8 and eps == 1e-6:
        run("comp_nb", lambda L, c: composed_solve(m, eps, L, batch=False,
                                                   wall_cap=c), caps["forced"])
    if eps == 1e-6:
        run("wy", lambda L, c: wy_active(m, eps, L, wall_cap=c), caps["wy"])
    # ---- push (C kernel, 2 counters)
    if 1.0 / (alpha * eps) <= 4e9:
        tt = time.perf_counter()
        p = push_c(m, eps)
        errp = float(np.max(np.abs(p["x"] - x0) / m.sqd))
        vv = {k: 0.0 for k in KEYS}
        vv["C_adj"] = p["C_adj"]; vv["R_adj"] = p["R_adj"]
        vv["C_emit"] = float(np.count_nonzero(p["x"]))
        vv["W"] = p["W"] + vv["C_emit"]
        vv.update(status="cert", err=errp, err_eps=errp / eps,
                  wall=time.perf_counter() - tt, approx_map=True)
        res["push"] = vv
    # ---- I3-A baselines only for families absent from the I3-A json
    if famname in EXTRA_BASE:
        for tag, fn, cap in (("amg", amg_local, caps["forced"]),
                             ("direct", direct_local, caps["forced"])):
            mt = VecMeter(m.d)
            tt = time.perf_counter()
            try:
                r = fn(m, eps, mt, wall_cap=cap)
                err = float(np.max(np.abs(r["x"] - x0) / m.sqd))
                vv = from_vecmeter(mt.vector())
                vv.update(status=r["status"], err=err, err_eps=err / eps,
                          wall=time.perf_counter() - tt, approx_map=True)
                res[tag] = vv
            except Exception as e:
                res[tag] = dict(status="err", msg=str(e)[:160])
    return res


def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 1100.0
    fams = sys.argv[2].split(",") if len(sys.argv) > 2 else ORDER
    tag = sys.argv[3] if len(sys.argv) > 3 else "main"
    caps = dict(comp=22.0, pull=10.0, forced=12.0, wy=6.0)
    alphas = [2 ** -4, 2 ** -8, 2 ** -12]
    epss = [1e-6, 1e-8]
    out = []
    path = os.path.join(OUT, f"i4b_{tag}.json")
    t00 = time.perf_counter()
    for f in fams:
        for a in alphas:
            for e in epss:
                if time.perf_counter() - t00 > budget:
                    print("BUDGET EXHAUSTED", flush=True)
                    with open(path, "w") as fh:
                        json.dump(out, fh)
                    return
                t0 = time.perf_counter()
                try:
                    r = one(f, a, e, caps)
                except Exception as exc:
                    r = dict(fam=f, alpha=a, eps=e, error=str(exc)[:200])
                out.append(r)
                with open(path, "w") as fh:
                    json.dump(out, fh)
                vs = max(r.get("volS", 1) or 1, 1)
                C = r.get("comp", {})
                def wv(k):
                    d = r.get(k, {})
                    w = d.get("W")
                    return (w / vs) if w else float("nan")
                print(f"{f:12s} a=2^{int(round(math.log2(a))):<4d} e={e:g} "
                      f"volS={vs:>8.0f} | comp {C.get('status','-'):4s} "
                      f"rd={C.get('rounds',0):>3} fl={C.get('flips',0)} "
                      f"{C.get('routes','')[:14]:14s} "
                      f"W/v={wv('comp'):>9.1f} pull={wv('comp_pull'):>9.1f} "
                      f"E={wv('comp_E'):>9.1f} A={wv('comp_A'):>9.1f} "
                      f"nb={wv('comp_nb'):>9.1f} "
                      f"wy={wv('wy'):>10.1f} push={wv('push'):>10.1f} "
                      f"e/eps={C.get('err_eps',float('nan')):.3f} "
                      f"[{time.perf_counter()-t0:.0f}s]", flush=True)
    print("wrote", path, f"{time.perf_counter()-t00:.0f}s")


if __name__ == "__main__":
    main()
