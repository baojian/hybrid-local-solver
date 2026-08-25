"""I5-B E2: fan trap with (e')-gated stopping; ball trap; hidden hub."""
import json, sys
sys.path.insert(0, "/home/claude/work/overnight/i4e")
from common import cell, fam, zoo
from run_fail import fan_trap

out = []
MECH = ("push", "composed", "vgf", "v3", "v3E", "v3O")
print("=== FAN TRAP fan_trap(400,K,D=200,at=20)  a=2^-10 eps=1e-4 ===")
for K in (10, 50, 200, 800):
    adj, s = fan_trap(400, K, 200, at=20)
    row = cell(adj, s, 2.0 ** -10, 1e-4, "fan_trap K=%d" % K, MECH)
    print("     v3 vol=%s | v3E vol=%s sb=%s ew=%.3g | v3O vol=%s"
          % (row.get("v3_vol"), row.get("v3E_vol"), row.get("v3E_sb"),
             row.get("v3E_ew") or 0, row.get("v3O_vol")), flush=True)
    out.append(row)
print("=== BALL TRAP ball_trap(400,M,at=60)  a=7.4e-6 eps=1e-3 (S_eps empty) ===")
for M in (100, 400, 1600):
    adj, s = fam.ball_trap(400, M, at=60)
    row = cell(adj, s, 7.4e-6, 1e-3, "ball_trap M=%d" % M, MECH)
    print("     v3 vol=%s | v3E vol=%s sb=%s" % (
        row.get("v3_vol"), row.get("v3E_vol"), row.get("v3E_sb")), flush=True)
    out.append(row)
print("=== HIDDEN HUB hidden_hub(6,M)  a=2^-6 eps=1e-3 ===")
for M in (1000, 10000, 100000):
    adj, s = fam.hidden_hub(6, M)
    out.append(cell(adj, s, 2.0 ** -6, 1e-3, "hidden_hub M=%d" % M, MECH))
print("=== SHALLOW SUPPORT path(40000) eps=0.5*umax ===")
from common import GModel
import numpy as np
for k in (4, 8, 12):
    a = 2.0 ** -k
    adj, s = zoo.path(40000)
    m = GModel(adj, a, s)
    x0 = m.solve_exact()
    umax = float((x0 * m.sqd / m.d).max())
    out.append(cell(adj, s, a, 0.5 * umax, "shallow a=2^-%d" % k, MECH))
with open("/home/claude/work/overnight/i4e/out/fan3.json", "w") as fh:
    json.dump(out, fh, default=str)
print("done")
