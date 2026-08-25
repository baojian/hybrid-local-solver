"""I5-B E1: round-count / exponent decomposition on the worst families."""
import json, math, sys
sys.path.insert(0, "/home/claude/work/overnight/i4e")
from common import cell, fam, zoo

EPS = 1e-5
FAMS = [
    ("path",     lambda: zoo.path(20000)),
    ("caterpil", lambda: zoo.caterpillar(8000, 1)),
    ("spider",   lambda: zoo.spider(6, 2500)),
    ("grid2d",   lambda: fam.fast_grid(110, 110)),
]
MECH = ("vgf", "v3", "v3E", "v3O")
out = []
for name, gen in FAMS:
    adj, s = gen()
    for k in (4, 6, 8, 10, 12, 14):
        a = 2.0 ** -k
        row = cell(adj, s, a, EPS, "%s a=2^-%d" % (name, k), MECH, wall=25.0)
        print("     vgf R=%s | v3 R=%s ns=%s bv=%.3g vol=%s | v3E R=%s sb=%s"
              % (row.get("vgf_R"), row.get("v3_R"), row.get("v3_ns"),
                 row.get("v3_bv") or 0, row.get("v3_vol"),
                 row.get("v3E_R"), row.get("v3E_sb")), flush=True)
        out.append(row)
        with open("/home/claude/work/overnight/i4e/out/sp3.json", "w") as fh:
            json.dump(out, fh, default=str)
print("done")
