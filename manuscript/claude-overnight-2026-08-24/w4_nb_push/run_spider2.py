"""Spider sweep for EES-G (gate-trusting, one-shot lam-gated expansion) plus
over-exploration audit on branching graphs (binary tree, random regular)."""
import sys, math, json
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w4_nb_push")
import numpy as np
from model import Model
from meter import Meter
import zoo
from ees import ees, region_stats

rows = []
for eps_exp in (5, 7):
    eps = 2.0 ** (-eps_exp)
    k = int(round(1 / (4 * eps)))
    for aexp in range(4, 13):
        alpha = 2.0 ** (-aexp)
        L = int(round(2 / math.sqrt(alpha)))
        adj, seed = zoo.spider(k, L)
        mod = Model(adj, alpha, seed)
        x0 = mod.solve_exact()
        me = Meter(adj)
        res = ees(adj, alpha, seed, eps, meter=me, gate_trust=True)
        z = np.array(res["z"]) / mod.sqd
        cert = mod.cert_resid(z); err = mod.semantic_err(z, x0)
        ok = cert < alpha * eps and err <= eps
        rows.append(dict(eps=eps, k=k, alpha=alpha, aexp=aexp, L=L,
                         total=me.total(), vec=me.vector(),
                         rounds=res["rounds"], S=len(res["S"]),
                         cert=cert, err=err, kL=k * L))
        print(f"eps=2^-{eps_exp} k={k:3d} a=2^-{aexp:2d} L={L:4d} | EES-G "
              f"tot={me.total():>9d} rounds={res['rounds']} |S|={len(res['S']):>6d} "
              f"ok={ok} tot/(kL)={me.total()/(k*L):5.2f} tot/(2|S|)={me.total()/(2*len(res['S'])):5.2f}",
              flush=True)

json.dump(rows, open("/home/claude/work/overnight/w4_nb_push/spider_g_results.json", "w"),
          default=float, indent=1)

print("\n== fitted exponents EES-G: work ~ (1/alpha)^s ==")
for eps_exp in (5, 7):
    sub = [r for r in rows if abs(r["eps"] - 2.0 ** (-eps_exp)) < 1e-12]
    xs = np.array([r["aexp"] for r in sub], float)
    ys = np.log2(np.array([r["total"] for r in sub], float))
    s, b = np.polyfit(xs, ys, 1)
    s2, _ = np.polyfit(xs[-5:], ys[-5:], 1)
    print(f"  eps=2^-{eps_exp} EES-G: slope(all)={s:.3f} slope(tail5)={s2:.3f}")

print("\n== over-exploration audit on branching graphs (EES-G vs EES) ==")
for name, (adj, seed) in [("binary_tree(12)", zoo.binary_tree(12)),
                          ("rand_reg(2000,3)", zoo.random_regular(2000, 3))]:
    for alpha in (2.0 ** -6, 2.0 ** -10):
        for eps in (1e-4,):
            mod = Model(adj, alpha, seed)
            x0 = mod.solve_exact()
            out = {}
            for lab, gt in (("EES", False), ("EES-G", True)):
                m = Meter(adj)
                try:
                    res = ees(adj, alpha, seed, eps, meter=m, gate_trust=gt)
                    z = np.array(res["z"]) / mod.sqd
                    ok = mod.cert_resid(z) < alpha * eps and mod.semantic_err(z, x0) <= eps
                    # true support needed: vertices with |pi|/d >= gamma-ish scale eps
                    print(f"  {name:18s} a=2^{int(np.log2(alpha))} eps={eps} {lab:6s}: "
                          f"tot={m.total():>9d} |S|={len(res['S']):>6d} rounds={res['rounds']} ok={ok}", flush=True)
                except RuntimeError as e:
                    print(f"  {name:18s} a=2^{int(np.log2(alpha))} eps={eps} {lab:6s}: ABORT {e}")
