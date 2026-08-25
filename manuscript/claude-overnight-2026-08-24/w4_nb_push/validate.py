"""Correctness validation of EES and FIFO-SOR vs Model.solve_exact on small
graphs. Checks: Model.cert_resid(x_hat) < alpha*eps AND semantic_err <= eps.
Also: tree one-round exactness (machine precision) via solve_region on S=V."""
import sys, math
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w4_nb_push")
import numpy as np
from model import Model, push_params
from meter import Meter
import zoo
from ees import ees, fifo_sor, solve_region, region_stats

def check(name, adj, seed, alpha, eps):
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    out = {}
    for algname, fn in (("EES", lambda m: ees(adj, alpha, seed, eps, meter=m)),
                        ("SOR", lambda m: fifo_sor(adj, alpha, seed, eps, meter=m, cap=5*10**6))):
        m = Meter(adj)
        res = fn(m)
        z = np.array(res["z"])
        x_hat = z / mod.sqd
        cert = mod.cert_resid(x_hat)
        err = mod.semantic_err(x_hat, x0)
        ok = (cert < alpha * eps * 1.0000001) and (err <= eps)
        out[algname] = (ok, cert, err, m.total())
        extra = ""
        if algname == "EES":
            vol, E, comps, betti = region_stats(adj, res["S"])
            extra = f" rounds={res['rounds']} |S|={len(res['S'])} betti={betti}"
        print(f"  {name:22s} a={alpha:<8g} eps={eps:<8g} {algname}: "
              f"ok={ok} cert={cert:.3e} (lim {alpha*eps:.1e}) err={err:.3e} "
              f"work={m.total()}{extra}")
        if not ok:
            print("  *** FAIL ***")
    return out

def tree_exactness():
    print("== tree one-round exactness (S = V, single elimination sweep) ==")
    cases = [("path(30)", *zoo.path(30)), ("spider(4,6)", *zoo.spider(4, 6)),
             ("binary_tree(4)", *zoo.binary_tree(4)),
             ("caterpillar(6,2)", *zoo.caterpillar(6, 2)),
             ("star(7)", *zoo.star(7))]
    for name, adj, seed in cases:
        for alpha in (0.25, 2**-8):
            mod = Model(adj, alpha, seed)
            x0 = mod.solve_exact()
            n = len(adj)
            d = [len(adj[u]) for u in range(n)]
            c, gamma = push_params(alpha)
            z = [0.0] * n
            r = {seed: gamma}
            S = set(range(n))
            m, ne, fl = solve_region(adj, d, c, S, r, z, meter=None)
            err = mod.semantic_err(np.array(z) / mod.sqd, x0)
            print(f"  {name:18s} a={alpha:<8g} core={m} err={err:.3e} "
                  f"{'OK' if err < 1e-12 else '*** FAIL ***'}")

if __name__ == "__main__":
    tree_exactness()
    print("== EES / SOR vs exact on the zoo ==")
    cases = [
        ("path(40)", *zoo.path(40)),
        ("path(40,mid)", *zoo.path(40, seed_end=False)),
        ("star(12)", *zoo.star(12)),
        ("star(12,leaf)", *zoo.star(12, center_seed=False)),
        ("spider(5,8)", *zoo.spider(5, 8)),
        ("binary_tree(5)", *zoo.binary_tree(5)),
        ("caterpillar(8,3)", *zoo.caterpillar(8, 3)),
        ("theta(3,4,5)", *zoo.theta_graph(3, 4, 5)),
        ("cycle(17)", *zoo.cycle(17)),
        ("double_cycle(5)", *zoo.double_cycle(5)),
        ("grid(6,5)", *zoo.grid(6, 5)),
        ("decoy_hub(11,8)", *zoo.decoy_hub(11, 8)),
        ("complete(9)", *zoo.complete(9)),
        ("rand_reg(24,3)", *zoo.random_regular(24, 3)),
    ]
    nfail = 0
    for name, adj, seed in cases:
        for alpha in (0.2, 2**-6):
            for eps in (1e-3, 1e-6):
                out = check(name, adj, seed, alpha, eps)
                for k, (ok, *_1) in out.items():
                    if not ok:
                        nfail += 1
    print(f"FAILURES: {nfail}")
