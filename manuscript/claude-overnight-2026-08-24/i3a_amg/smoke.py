import sys, time
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
import zoo
from amglib import (GModel, VecMeter, amg_local, support_stats, push_c,
                    direct_local)

def run(name, adj, seed, alpha, eps, **kw):
    m = GModel(adj, alpha, seed)
    st = support_stats(m, eps)
    x0 = m.solve_exact()
    mt = VecMeter(m.d)
    t0 = time.perf_counter()
    r = amg_local(m, eps, mt, x_exact=x0, verbose=True, **kw)
    dt = time.perf_counter() - t0
    err = m.semantic_err(r["x"])
    v = mt.vector()
    print(f"{name} a={alpha:.5g} eps={eps:g} n={m.n} volS={st['volS']:.0f} "
          f"Rsem={st['R']} | {r['status']} R={r['R']} cyc={r['cycles']} "
          f"rate={r['rate']} nlev={r['nlev']} W={v['total']:.3g} "
          f"W/vol={v['total']/max(st['volS'],1):.1f} "
          f"setup%={100*v['setup']/v['total']:.0f} err/eps={err/eps:.3f} "
          f"wall={dt:.1f}s")
    if r.get("levels"):
        print("   levels:", [(l.get('n'), l.get('nnz'), l.get('nagg')) for l in r["levels"]])
    return r

if __name__ == "__main__":
    w = 129
    adj, _ = zoo.grid(w, w)
    seed = (w // 2) * w + w // 2
    for alpha in (2**-4, 2**-8):
        run("grid129", adj, seed, alpha, 1e-6)
    adj, s = zoo.double_cycle(400)
    run("dcycle", adj, s, 2**-8, 1e-6)
    adj, s = zoo.binary_tree(14)
    run("btree14", adj, s, 2**-8, 1e-6)
    adj, s = zoo.random_regular(5000, 3)
    run("rr3", adj, s, 2**-8, 1e-6)
    adj, s = zoo.star(20000)
    run("star", adj, s, 2**-8, 1e-6)
