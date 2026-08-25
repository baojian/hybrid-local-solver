"""Isolate the V-cycle rate from region growth: fixed graph, fixed region
(= the whole graph), Dirichlet-free, sweep alpha down to 2^-20.
Answers (a): is the SA V-cycle rate alpha-uniform off-lattice?"""
import sys
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
import zoo
from amglib import GModel, VecMeter, build_hierarchy, v_cycle
from run_zoo import fast_grid, rand_recursive_tree

GRAPHS = {
    "grid(101,101)": lambda: fast_grid(101, 101),
    "rand_reg(4000,3)": lambda: zoo.random_regular(4000, 3),
    "rand_reg(4000,4)": lambda: zoo.random_regular(4000, 4),
    "double_cycle(500)": lambda: zoo.double_cycle(500),
    "binary_tree(11)": lambda: zoo.binary_tree(11),
    "caterpillar(2000)": lambda: zoo.caterpillar(2000, arm=1),
    "spider(6,500)": lambda: zoo.spider(6, 500),
    "rrt(4000)": lambda: rand_recursive_tree(4000),
    "star(4000)": lambda: zoo.star(4000),
}
ALPHAS = [2. ** -2, 2. ** -4, 2. ** -6, 2. ** -8, 2. ** -10, 2. ** -12,
          2. ** -16, 2. ** -20]

print(f"{'graph':20s} " + " ".join(f"{'2^-'+str(int(round(-np.log2(a)))):>7s}"
                                   for a in ALPHAS) + "   nlev  opcx")
for name, gen in GRAPHS.items():
    adj, seed = gen()
    row = []
    nlev = opcx = 0
    for a in ALPHAS:
        m = GModel(adj, a, seed)
        mt = VecMeter(m.d)
        lv, info = build_hierarchy(m.Q.tocsr(), m.sqd.copy(), mt,
                                   lambda k: None, rho0=2.0 / (1.0 + a),
                                   vol0=float(m.d.sum()))
        nlev = len(lv)
        opcx = sum(l["nnz"] for l in lv) / lv[0]["nnz"]
        x = np.zeros(m.n)
        rs = []
        prev = None
        for i in range(14):
            v_cycle(lv, 0, x, m.b, mt, lambda k: None, 2, 2)
            r = float(np.max(np.abs(m.b - m.Q @ x) / m.sqd))
            if prev is not None and prev > 1e-13:
                rs.append(r / prev)
            prev = r
        row.append(np.median(rs[2:]) if len(rs) > 3 else np.median(rs))
    print(f"{name:20s} " + " ".join(f"{v:>7.3f}" for v in row)
          + f"   {nlev:>4d}  {opcx:>4.2f}")
