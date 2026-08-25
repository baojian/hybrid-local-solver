import sys, time, math
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4e")
sys.path.insert(0, "/home/claude/work/overnight/i4d")
sys.path.insert(0, "/home/claude/work/overnight/i4b_composed")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
import fam, zoo                                     # noqa
from amglib import GModel, push_c, direct_local, amg_local   # noqa
from ledger import Ledger                            # noqa
from composed import composed_solve                  # noqa
from vgf import vgf_local, DQMeter, out_measure      # noqa


def cell(adj, seed, a, eps, tag, mechs, wall=25.0, verbose=True):
    m = GModel(adj, a, seed)
    x0 = m.solve_exact()
    om = out_measure(m, eps, x0)
    volS = om["volS"]
    row = dict(tag=tag, alpha=a, eps=eps, n=m.n, volS=volS, nS=om["nS"],
               volB=om["volB"])
    for w in mechs:
        t = time.perf_counter()
        try:
            if w == "push":
                r = push_c(m, eps)
                W, x, st = r["W"], r["x"], "cert"
            elif w == "composed":
                led = Ledger(m.d)
                r = composed_solve(m, eps, led, wall_cap=wall)
                W, x, st = led.W(), r["x"], r["status"]
            elif w in ("direct", "directDQ"):
                mt = DQMeter(m.d) if w.endswith("DQ") else None
                from amglib import VecMeter
                mt = mt or VecMeter(m.d)
                r = direct_local(m, eps, mt, wall_cap=wall)
                W, x, st = mt.total(), r["x"], r["status"]
            elif w in ("amg", "amgDQ"):
                from amglib import VecMeter
                mt = DQMeter(m.d) if w.endswith("DQ") else VecMeter(m.d)
                r = amg_local(m, eps, mt, wall_cap=wall)
                W, x, st = mt.total(), r["x"], r["status"]
            elif w.startswith("vgf"):
                kw = dict(wall_cap=wall)
                if w == "vgfO":
                    kw.update(oracle=True)
                if w == "vgfS":
                    kw.update(spec=False)
                mt = DQMeter(m.d)
                r = vgf_local(m, eps, mt, x_exact=x0, **kw)
                W, x, st = mt.total(), r["x"], r["status"]
                row[w + "_vol"] = r.get("volS")
                row[w + "_cvol"] = r.get("cert_vol")
                row[w + "_R"] = r.get("rounds")
            else:
                raise ValueError(w)
            e = float(np.max(np.abs(x - x0) / m.sqd))
            miss = int(np.setdiff1d(om["Sset"],
                                    np.flatnonzero(x != 0)).size)
            ok = (e <= eps) and st in ("cert",) and miss == 0
            row[w] = dict(W=float(W), We=float(W) * eps, err_eps=e / eps,
                          status=st, miss=miss, ok=bool(ok),
                          wall=time.perf_counter() - t)
        except Exception as ex:
            row[w] = dict(W=float("nan"), We=float("nan"), status="EXC:%s" % ex)
    if verbose:
        s = "%-26s n=%-8d volS=%-8.0f vSe=%-6.3f |" % (tag, m.n, volS,
                                                       volS * eps)
        for w in mechs:
            v = row[w]
            flag = "" if v.get("ok") else ("!" if v.get("miss") else "?")
            s += " %s=%.4g%s" % (w, v["We"], flag)
        print(s, flush=True)
    return row
