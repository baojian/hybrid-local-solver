"""Cyclic families: EES (doubling) vs FIFO-SOR. Records explored-region Betti
number, junction-core size, and charged work; fits work vs Betti."""
import sys, math, json
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w4_nb_push")
import numpy as np
from model import Model
from meter import Meter
import zoo
from ees import ees, fifo_sor, region_stats

rows = []

def run(name, adj, seed, alpha, eps, dense_limit=2600):
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    me = Meter(adj)
    try:
        res = ees(adj, alpha, seed, eps, meter=me, dense_limit=dense_limit)
        z = np.array(res["z"]) / mod.sqd
        ok_e = mod.cert_resid(z) < alpha * eps and mod.semantic_err(z, x0) <= eps
        vol, E, comps, betti = region_stats(adj, res["S"])
        core = max((h["core"] for h in res["hist"]), default=0)
        e_tot = me.total(); Ssz = len(res["S"]); rounds = res["rounds"]
    except RuntimeError as err:
        ok_e, vol, betti, core, e_tot, Ssz, rounds = False, -1, -1, -1, -1, -1, -1
        print(f"  EES ABORT: {err}")
    ms = Meter(adj)
    rs = fifo_sor(adj, alpha, seed, eps, meter=ms, cap=3 * 10 ** 7)
    zs = np.array(rs["z"]) / mod.sqd
    ok_s = (not rs["capped"]) and mod.cert_resid(zs) < alpha * eps \
        and mod.semantic_err(zs, x0) <= eps
    row = dict(name=name, n=len(adj), alpha=alpha, eps=eps, ees_total=e_tot,
               ees_vec=(me.vector() if e_tot >= 0 else None), S=Ssz,
               rounds=rounds, vol=vol, betti=betti, core=core, ok_e=ok_e,
               sor_total=ms.total(), sor_pushes=rs["pushes"],
               capped=rs["capped"], ok_s=ok_s)
    rows.append(row)
    rat = e_tot / max(ms.total(), 1) if e_tot >= 0 else float("nan")
    print(f"{name:24s} n={len(adj):6d} a=2^{int(round(math.log2(alpha))):3d} eps={eps:g} | "
          f"EES tot={e_tot:>12d} |S|={Ssz:>6d} betti={betti:>5d} core={core:>5d} ok={ok_e} | "
          f"SOR tot={ms.total():>10d}{'(CAP)' if rs['capped'] else ''} ok={ok_s} | E/S ratio={rat:9.2f}",
          flush=True)
    return row

eps = 1e-3
print("== alpha sweeps, fixed families ==")
for aexp in (4, 6, 8, 10, 12):
    alpha = 2.0 ** (-aexp)
    isa = 1 / math.sqrt(alpha)
    l = max(2, int(round(1.5 * isa)))
    run(f"theta({l},{l+1},{l+2})", *zoo.theta_graph(l, l + 1, l + 2), alpha, eps)
for aexp in (4, 6, 8, 10, 12):
    alpha = 2.0 ** (-aexp)
    n = max(6, int(round(3 / math.sqrt(alpha))))
    run(f"cycle({n})", *zoo.cycle(n), alpha, eps)
for aexp in (4, 6, 8, 10, 12):
    alpha = 2.0 ** (-aexp)
    t = max(4, int(round(1.5 / math.sqrt(alpha))) + 2)
    run(f"double_cycle({t})", *zoo.double_cycle(t), alpha, eps)
for aexp in (4, 6, 8, 10, 12):
    alpha = 2.0 ** (-aexp)
    run("grid(16,16)", *zoo.grid(16, 16), alpha, eps)

print("\n== Betti scaling at fixed alpha=2^-8, eps=1e-3 ==")
for t in (6, 10, 16, 26, 40, 64):
    run(f"double_cycle({t})", *zoo.double_cycle(t), 2.0 ** -8, eps)
for w in (6, 8, 12, 16, 24, 32):
    run(f"grid({w},{w})", *zoo.grid(w, w), 2.0 ** -8, eps, dense_limit=2600)

json.dump(rows, open("/home/claude/work/overnight/w4_nb_push/cycles_results.json", "w"),
          default=float, indent=1)

print("\n== fit: EES total vs betti (core-dominated families, fixed alpha) ==")
for fam in ("double_cycle", "grid"):
    sub = [r for r in rows if r["name"].startswith(fam) and r["alpha"] == 2.0 ** -8
           and r["betti"] > 2 and r["ees_total"] > 0]
    if len(sub) >= 3:
        xs = np.log2([r["betti"] for r in sub])
        ys = np.log2([r["ees_total"] for r in sub])
        s, b = np.polyfit(xs, ys, 1)
        yc = np.log2([max(r["core"], 1) for r in sub])
        sc, _ = np.polyfit(xs, yc, 1)
        print(f"  {fam}: log2(EES work) ~ {s:.2f} * log2(betti) ; core ~ betti^{sc:.2f}")
        for r in sub:
            print(f"    {r['name']:20s} betti={r['betti']:>5d} core={r['core']:>5d} "
                  f"EES={r['ees_total']:>12d} SOR={r['sor_total']:>10d} "
                  f"core^3/EES={(r['core']**3)/max(r['ees_total'],1):5.2f}")
