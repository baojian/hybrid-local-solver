"""I4-B addendum: the one place the KINETIC GATE is supposed to matter --
a boundary whose VOLUME is much larger than its SIZE.  hubpath(L,D): a path
b_0..b_{L-1} seeded at b_0, every b_i carrying a pendant hub of degree D whose
D-1 further leaves are dead ends.  The active set is a prefix of the path, so
|dS| ~ |S| but vol(dS) ~ D|S|: pulling the boundary costs Theta(D) per check,
pushing costs O(1).  Same trajectory for both -- an exact A/B."""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/i4b_composed")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from amglib import GModel, support_stats, push_c
from ledger import Ledger
from composed import composed_solve, wy_active


def hubpath(L, D):
    adj = {i: [] for i in range(L)}
    nid = L
    for i in range(L - 1):
        adj[i].append(i + 1); adj[i + 1].append(i)
    for i in range(L):
        h = nid; nid += 1
        adj[h] = [i]; adj[i].append(h)
        for _ in range(D - 1):
            adj[nid] = [h]; adj[h].append(nid); nid += 1
    return {u: sorted(v) for u, v in adj.items()}, 0


out = []
for D in (4, 32, 256, 1024):
    for alpha in (2 ** -4, 2 ** -8):
        eps = 1e-6
        adj, seed = hubpath(400, D)
        m = GModel(adj, alpha, seed)
        st = support_stats(m, eps)
        row = dict(D=D, alpha=alpha, eps=eps, n=m.n, volS=st["volS"],
                   nS=st["nS"])
        for tag, kw in (("push_gate", dict(gate="push")),
                        ("pull_gate", dict(gate="pull"))):
            led = Ledger(m.d)
            t0 = time.perf_counter()
            r = composed_solve(m, eps, led, wall_cap=25.0, **kw)
            err = float(np.max(np.abs(r["x"] - m.solve_exact()) / m.sqd))
            v = led.vector()
            v.update(status=r["status"], err_eps=err / eps,
                     rounds=r["rounds"], volReg=r["volS"],
                     wall=time.perf_counter() - t0)
            row[tag] = v
        led = Ledger(m.d)
        r = wy_active(m, eps, led, wall_cap=10.0)
        row["wy"] = dict(W=led.W(), status=r["status"])
        if 1.0 / (alpha * eps) <= 4e9:
            p = push_c(m, eps)
            row["push"] = dict(W=p["W"])
        out.append(row)
        P, U = row["push_gate"], row["pull_gate"]
        vs = max(st["volS"], 1)
        print(f"D={D:5d} a=2^{int(round(math.log2(alpha))):<4d} "
              f"volS={vs:8.0f} volB~{D*row['nS']:9d} | "
              f"push W={P['W']:11.4g} ({P['W']/vs:8.1f}/vol) "
              f"pull W={U['W']:11.4g} ({U['W']/vs:9.1f}/vol) "
              f"pull/push={U['W']/P['W']:7.2f} "
              f"gate%={100*P['ctl_gate']/P['W']:4.1f} "
              f"R_adj_pull={U['R_adj']:.3g} e/eps={P['err_eps']:.3f}",
              flush=True)
with open("/home/claude/work/overnight/i4b_composed/out/hub.json", "w") as fh:
    json.dump(out, fh)
print("done")
