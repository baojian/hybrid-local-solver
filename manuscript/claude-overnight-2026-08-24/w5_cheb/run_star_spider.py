"""Phase 3: the star test and spider L-scaling (task 4)."""
import sys
import math
import json
import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w5_cheb")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from cheb import (cheb_sweep, cheb_restarted, push_solve, VecMeter,
                  consts, bfs_dist)  # noqa
from model import Model  # noqa
import zoo  # noqa

out_all = {}

# ---------- STAR, center seed, k = 1/(4 eps) ----------
print("=== star center-seeded, k=1/(4eps): W vs prediction K*2k ===")
star_rows = []
for eps in (1e-2, 1e-3):
    k_leaves = int(round(1 / (4 * eps)))
    adj, seed = zoo.star(k_leaves)
    for alpha in (2 ** -6, 2 ** -8, 2 ** -10, 2 ** -12):
        mod = Model(adj, alpha, seed)
        x0 = mod.solve_exact()
        m = VecMeter(mod)
        out = cheb_restarted(mod, eps, m, record=True)
        err = mod.semantic_err(out["x"], x0)
        vols = out["vol_hist"]
        volbar = float(np.mean(vols)) if vols else 0.0
        # prediction: iters * 2k
        pred = out["iters"] * 2 * k_leaves
        mp = VecMeter(mod)
        po = push_solve(mod, eps, mp)
        perr = mod.semantic_err(po["x"], x0)
        row = dict(eps=eps, alpha=alpha, k=k_leaves, iters=out["iters"],
                   W=m.scan_work(), pred_K2k=pred, volbar=volbar,
                   err=err, W_push=mp.scan_work(), push_err=perr,
                   inv_sqae=1 / (math.sqrt(alpha) * eps),
                   inv_ae=1 / (alpha * eps))
        star_rows.append(row)
        print(f" eps={eps:g} k={k_leaves:4d} a=2^{int(math.log2(alpha)):3d}"
              f" iters={out['iters']:4d} W={m.scan_work():9.0f}"
              f" K*2k={pred:9.0f} volbar/2k={volbar/(2*k_leaves):5.2f}"
              f" W/(1/(sqrt(a)eps))={m.scan_work()*math.sqrt(alpha)*eps:6.2f}"
              f" W_push={mp.scan_work():9.0f}"
              f" W_push*(a*eps)={mp.scan_work()*alpha*eps:6.2f}")
out_all["star_center"] = star_rows

# ---------- STAR, leaf seed, k=10^4 (wrong side) ----------
print("\n=== star leaf-seeded, k=10000: repeat-scan of the center ===")
leaf_rows = []
adj, seed = zoo.star(10000, center_seed=False)
for alpha in (2 ** -6, 2 ** -10):
    eps = 1e-2
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    res = {}
    for name, fn in (
        ("none", lambda: (lambda m: (m, cheb_sweep(mod, eps, mode="none",
            stop="cert_oracle", meter=m)))(VecMeter(mod))),
        ("restart", lambda: (lambda m: (m, cheb_restarted(mod, eps, m)))(
            VecMeter(mod))),
        ("push", lambda: (lambda m: (m, push_solve(mod, eps, m)))(
            VecMeter(mod))),
    ):
        m, out = fn()
        err = mod.semantic_err(out["x"], x0)
        it = out.get("k", out.get("iters", out.get("sweeps")))
        res[name] = dict(W=m.scan_work(), C_adj=m.C_adj, R_adj=m.R_adj,
                         iters=it, err=err)
        print(f" a=2^{int(math.log2(alpha)):3d} {name:8s} W={m.scan_work():10.0f}"
              f" (first={m.C_adj:.0f} repeat={m.R_adj:.0f}) iters={it}"
              f" err/eps={err/eps:.3f}")
    leaf_rows.append(dict(alpha=alpha, eps=eps, res=res))
out_all["star_leaf"] = leaf_rows

# ---------- SPIDER: W(L) at fixed alpha, eps ----------
print("\n=== spider k=16 arms, L sweep: kL vs kL^2 ===")
sp_rows = []
alpha, eps = 2 ** -8, 1e-3
for L in (25, 50, 100, 200, 400):
    adj, seed = zoo.spider(16, L)
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    dist = bfs_dist(adj, seed)
    m = VecMeter(mod)
    out = cheb_restarted(mod, eps, m, record=True)
    err = mod.semantic_err(out["x"], x0)
    reach = max((dist[u] for u in np.flatnonzero(out["x"])), default=0)
    vols = out["vol_hist"]
    row = dict(L=L, iters=out["iters"], W=m.scan_work(), err=err,
               reach=int(reach), volmax=float(np.max(vols)),
               volbar=float(np.mean(vols)),
               kL=16 * L, kL2=16 * L * L)
    # push comparison
    mp = VecMeter(mod)
    po = push_solve(mod, eps, mp)
    row["W_push"] = mp.scan_work()
    sp_rows.append(row)
    print(f" L={L:4d} iters={row['iters']:4d} reach={reach:4d} "
          f"volmax={row['volmax']:7.0f} W={row['W']:10.0f} "
          f"W/kL={row['W']/(16*L):8.1f} W/kL^2={row['W']/(16*L*L):6.3f} "
          f"W_push={row['W_push']:9.0f}")
# local slopes
for i in range(1, len(sp_rows)):
    a, b = sp_rows[i - 1], sp_rows[i]
    sl = math.log(b["W"] / a["W"]) / math.log(b["L"] / a["L"])
    print(f"   local d logW/d logL between L={a['L']},{b['L']}: {sl:.2f}")
out_all["spider"] = sp_rows

# ---------- SPIDER: alpha sweep at fixed L to see saturation ----------
print("\n=== spider k=16, L=100, alpha sweep (radius vs alpha) ===")
sp2 = []
for alpha in (2 ** -4, 2 ** -6, 2 ** -8, 2 ** -10, 2 ** -12):
    eps = 1e-3
    adj, seed = zoo.spider(16, 100)
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    dist = bfs_dist(adj, seed)
    m = VecMeter(mod)
    out = cheb_restarted(mod, eps, m, record=True)
    err = mod.semantic_err(out["x"], x0)
    reach = max((dist[u] for u in np.flatnonzero(out["x"])), default=0)
    sp2.append(dict(alpha=alpha, W=m.scan_work(), iters=out["iters"],
                    reach=int(reach), err=err))
    print(f" a=2^{int(math.log2(alpha)):3d} iters={out['iters']:4d} "
          f"reach={reach:4d} W={m.scan_work():10.0f} "
          f"W*alpha={m.scan_work()*alpha:8.1f} "
          f"W*sqrt(a)={m.scan_work()*math.sqrt(alpha):9.1f}")
out_all["spider_alpha"] = sp2

# ---------- DECOY: truncation payoff ----------
print("\n=== decoy_hub(60, 20000): untruncated vs truncated ===")
dc = []
for alpha in (2 ** -6, 2 ** -10):
    eps = 1e-2
    adj, seed = zoo.decoy_hub(60, 20000)
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    m1 = VecMeter(mod)
    o1 = cheb_sweep(mod, eps, mode="none", stop="cert_oracle", meter=m1)
    m2 = VecMeter(mod)
    o2 = cheb_restarted(mod, eps, m2)
    e2 = mod.semantic_err(o2["x"], x0)
    m3 = VecMeter(mod)
    o3 = push_solve(mod, eps, m3)
    e3 = mod.semantic_err(o3["x"], x0)
    dc.append(dict(alpha=alpha, W_none=m1.scan_work(), W_tr=m2.scan_work(),
                   W_push=m3.scan_work()))
    print(f" a=2^{int(math.log2(alpha)):3d} W_untrunc={m1.scan_work():10.0f} "
          f"W_certtrunc={m2.scan_work():10.0f} "
          f"(ratio {m1.scan_work()/max(1,m2.scan_work()):6.1f}x) "
          f"W_push={m3.scan_work():9.0f} errs ok={e2<=eps and e3<=eps}")
out_all["decoy"] = dc

with open("/home/claude/work/overnight/w5_cheb/out/star_spider.json", "w") as f:
    json.dump(out_all, f)
print("\nsaved star_spider.json")
