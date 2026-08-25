import sys
sys.path.insert(0, "/home/claude/work/overnight/i4e")
from common import cell, fam, zoo

M = ("push", "vgf", "v3", "v3E", "v3O")
for tag, gen, a, eps in [
    ("path4k", lambda: zoo.path(4000), 2.0 ** -8, 1e-5),
    ("path4k-12", lambda: zoo.path(4000), 2.0 ** -12, 1e-5),
    ("grid60", lambda: fam.fast_grid(60, 60), 2.0 ** -8, 1e-5),
    ("star", lambda: zoo.star(3000), 2.0 ** -8, 1e-5),
    ("btree", lambda: zoo.binary_tree(11), 2.0 ** -8, 1e-5),
    ("exp3", lambda: zoo.random_regular(3000, 3), 2.0 ** -6, 1e-5),
]:
    adj, s = gen()
    row = cell(adj, s, a, eps, tag, M, wall=25.0)
    print("   v3: R=%s ns=%s bv=%.4g vol=%s | v3E sb=%s ew=%.4g" % (
        row.get("v3_R"), row.get("v3_ns"), row.get("v3_bv") or 0,
        row.get("v3_vol"), row.get("v3E_sb"), row.get("v3E_ew") or 0))
