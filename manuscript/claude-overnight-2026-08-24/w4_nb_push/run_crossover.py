"""Absolute crossover: EES-G vs FIFO-SOR on spider at very small alpha."""
import sys, math, json
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w4_nb_push")
import numpy as np
from model import Model
from meter import Meter
import zoo
from ees import ees, fifo_sor

eps = 2.0 ** -7
k = 32
rows = []
for aexp in (12, 14, 16, 18):
    alpha = 2.0 ** (-aexp)
    L = int(round(2 / math.sqrt(alpha)))
    adj, seed = zoo.spider(k, L)
    n = len(adj)
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    me = Meter(adj)
    res = ees(adj, alpha, seed, eps, meter=me, gate_trust=True)
    z = np.array(res["z"]) / mod.sqd
    ok_e = mod.cert_resid(z) < alpha * eps and mod.semantic_err(z, x0) <= eps
    ms = Meter(adj)
    rs = fifo_sor(adj, alpha, seed, eps, meter=ms, cap=10 ** 8)
    zs = np.array(rs["z"]) / mod.sqd
    ok_s = mod.cert_resid(zs) < alpha * eps and mod.semantic_err(zs, x0) <= eps
    rows.append(dict(aexp=aexp, L=L, n=n, ees=me.total(), sor=ms.total(),
                     S=len(res["S"]), ok_e=ok_e, ok_s=ok_s))
    print(f"a=2^-{aexp} L={L:5d} n={n:6d} | EES-G={me.total():>9d} (|S|={len(res['S'])}, ok={ok_e}) "
          f"| SOR={ms.total():>10d} (ok={ok_s}) | SOR/EES-G={ms.total()/me.total():5.2f}",
          flush=True)
json.dump(rows, open("/home/claude/work/overnight/w4_nb_push/crossover_results.json", "w"),
          default=float, indent=1)
