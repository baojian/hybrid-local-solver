"""E1/E2: the DECISIVE measurement -- W*eps vs M on the two families that
break ball-based region growth."""
import json, sys
sys.path.insert(0, "/home/claude/work/overnight/i4e")
from common import cell, fam

out = []
MECH = ("push", "composed", "directDQ", "amgDQ", "vgf", "vgfO")
print("=== E1  BALL TRAP  ball_trap(400, M, at=60), alpha=7.4e-6, eps=1e-3 ===")
print("    (correct output S_eps is EMPTY: ideal work is O(1))")
for M in (50, 100, 200, 400, 800, 1600):
    adj, s = fam.ball_trap(400, M, at=60)
    out.append(cell(adj, s, 7.4e-6, 1e-3, "ball_trap M=%d" % M, MECH))
print()
print("=== E1b BALL TRAP at a NON-degenerate cell  alpha=2^-10, eps=1e-4 ===")
for M in (50, 100, 200, 400, 800):
    adj, s = fam.ball_trap(400, M, at=60)
    out.append(cell(adj, s, 2.0 ** -10, 1e-4, "ball_trap2 M=%d" % M, MECH))
print()
print("=== E2  HIDDEN HUB  hidden_hub(6, M), alpha=2^-6, eps=1e-3 ===")
for M in (1000, 10000, 100000):
    adj, s = fam.hidden_hub(6, M)
    out.append(cell(adj, s, 2.0 ** -6, 1e-3, "hidden_hub M=%d" % M, MECH))
with open("/home/claude/work/overnight/i4e/out/trap.json", "w") as fh:
    json.dump(out, fh, default=str)
print("done")
