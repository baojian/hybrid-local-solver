"""I5-B E3: full zoo, VGF-SP3 vs VGF vs push vs composed."""
import json, math, sys
sys.path.insert(0, "/home/claude/work/overnight/i4e")
from common import cell, fam, zoo

EPS = 1e-5
FAMS = [
    ("path",      lambda: zoo.path(20000)),
    ("caterpil",  lambda: zoo.caterpillar(8000, 1)),
    ("comb",      lambda: fam.comb(1500, 6)),
    ("spider",    lambda: zoo.spider(6, 2500)),
    ("star",      lambda: zoo.star(6000)),
    ("btree",     lambda: zoo.binary_tree(13)),
    ("rrt",       lambda: fam.rrt(8000)),
    ("pa_tree",   lambda: fam.powerlaw_tree(8000)),
    ("theta",     lambda: zoo.theta_graph(3000, 3000, 3000)),
    ("prism",     lambda: zoo.double_cycle(2000)),
    ("grid2d",    lambda: fam.fast_grid(130, 130)),
    ("grid3d",    lambda: fam.fast_grid3(26)),
    ("decoy_hub", lambda: zoo.decoy_hub(6000, 500)),
    ("exp3reg",   lambda: zoo.random_regular(9000, 3)),
    ("exp5reg",   lambda: zoo.random_regular(9000, 5)),
]
MECH = ("push", "composed", "vgf", "v3", "v3E", "v3O")
out = []
for name, gen in FAMS:
    adj, s = gen()
    for a in (2.0 ** -4, 2.0 ** -8, 2.0 ** -12):
        out.append(cell(adj, s, a, EPS,
                        "%s a=2^-%d" % (name, int(round(-math.log2(a)))),
                        MECH, wall=15.0))
        with open("/home/claude/work/overnight/i4e/out/zoo3.json", "w") as fh:
            json.dump(out, fh, default=str)
print("done")
