"""Spider sweep: EES vs FIFO-SOR (omega* tail). k = 1/(4 eps) arms, L = 2/sqrt(alpha).
Predicts: SOR total ~ 1/(alpha*eps) (triangular re-traversal), EES ~ 1/(sqrt(alpha)*eps).
Charged work via Meter; certificate + semantic error verified vs Model.solve_exact."""
import sys, math, json, time
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w4_nb_push")
import numpy as np
from model import Model
from meter import Meter
import zoo
from ees import ees, fifo_sor, region_stats

rows = []
for eps_exp in (5, 7):
    eps = 2.0 ** (-eps_exp)
    k = int(round(1 / (4 * eps)))
    for aexp in range(4, 13):
        alpha = 2.0 ** (-aexp)
        L = int(round(2 / math.sqrt(alpha)))
        adj, seed = zoo.spider(k, L)
        n = len(adj)
        mod = Model(adj, alpha, seed)
        x0 = mod.solve_exact()

        me = Meter(adj)
        t0 = time.time()
        res_e = ees(adj, alpha, seed, eps, meter=me)
        te = time.time() - t0
        ze = np.array(res_e["z"]) / mod.sqd
        cert_e = mod.cert_resid(ze); err_e = mod.semantic_err(ze, x0)
        vol, E, comps, betti = region_stats(adj, res_e["S"])

        ms = Meter(adj)
        t0 = time.time()
        res_s = fifo_sor(adj, alpha, seed, eps, meter=ms, cap=3 * 10 ** 7)
        ts = time.time() - t0
        zs = np.array(res_s["z"]) / mod.sqd
        cert_s = mod.cert_resid(zs); err_s = mod.semantic_err(zs, x0)

        row = dict(eps=eps, k=k, alpha=alpha, aexp=aexp, L=L, n=n,
                   ees_total=me.total(), ees_vec=me.vector(),
                   ees_rounds=res_e["rounds"], ees_S=len(res_e["S"]),
                   ees_cert=cert_e, ees_err=err_e, betti=betti,
                   sor_total=ms.total(), sor_pushes=res_s["pushes"],
                   sor_capped=res_s.get("capped", False),
                   sor_cert=cert_s, sor_err=err_s,
                   kL=k * L, inv_ae=1 / (alpha * eps),
                   t_ees=te, t_sor=ts)
        rows.append(row)
        ok_e = cert_e < alpha * eps and err_e <= eps
        ok_s = cert_s < alpha * eps and err_s <= eps
        print(f"eps=2^-{eps_exp} k={k:3d} a=2^-{aexp:2d} L={L:4d} n={n:6d} | "
              f"EES tot={me.total():>10d} rounds={res_e['rounds']} |S|={len(res_e['S']):>6d} "
              f"ok={ok_e} | SOR tot={ms.total():>11d} pushes={res_s['pushes']:>9d} ok={ok_s} "
              f"| kL={k*L:>6d} 1/(ae)={int(1/(alpha*eps)):>8d} ratio={ms.total()/max(me.total(),1):6.1f}",
              flush=True)

json.dump(rows, open("/home/claude/work/overnight/w4_nb_push/spider_results.json", "w"),
          default=float, indent=1)

# ---- fits: log2(work) vs aexp = log2(1/alpha), fixed eps ----
print("\n== fitted exponents: work ~ (1/alpha)^s at fixed eps ==")
for eps_exp in (5, 7):
    sub = [r for r in rows if abs(r["eps"] - 2.0 ** (-eps_exp)) < 1e-12]
    xs = np.array([r["aexp"] for r in sub], float)
    for lab, key in (("EES", "ees_total"), ("SOR", "sor_total")):
        ys = np.log2(np.array([r[key] for r in sub], float))
        s, b = np.polyfit(xs, ys, 1)
        # also tail fit (last 5 points, asymptotic)
        s2, _ = np.polyfit(xs[-5:], ys[-5:], 1)
        print(f"  eps=2^-{eps_exp} {lab}: slope(all)={s:.3f} slope(tail5)={s2:.3f}")
    # normalized: work / (k*L) for EES ; work/(1/(alpha eps)) for SOR
    print("   EES total/(k*L):     ",
          [f"{r['ees_total']/r['kL']:.2f}" for r in sub])
    print("   SOR total*alpha*eps: ",
          [f"{r['sor_total']*r['alpha']*r['eps']:.2f}" for r in sub])
