"""E5 (DECISIVE): follow each family's OUTPUT-SATURATING RIDGE  (the (alpha,eps)
curve on which vol(S_eps)*eps is maximal, i.e. where the output is Theta(1/eps))
and ask whether the BEST mechanism's total charged work W satisfies W = O~(1/eps).
If W*eps is flat in eps -> O(1/eps).  If it grows polylog -> O~(1/eps).
If it grows like a power of 1/eps -> the target is refuted."""
import json, math, sys, time
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4d")
import fam
from fam import GModel
from amglib import VecMeter, amg_local, push_c, cheb_local, direct_local


class DQMeter(VecMeter):
    """boundary ring is DEGREE-QUERIED only (I4-D Lemma C)."""
    def ring_scan(self, idx):
        k = len(idx)
        if k:
            self.C_resp += float(k); self.solve += float(k)


OUT = "/home/claude/work/overnight/i4d/out"
WALL = 25.0


def one(adj, seed, alpha, eps, tag, mechs):
    m = GModel(adj, alpha, seed)
    x0 = m.solve_exact()
    u = x0 * m.sqd / m.d
    volS = float(m.d[u > eps].sum())
    res = []
    for w in mechs:
        t0 = time.time()
        try:
            if w == "push":
                if 1.0 / (alpha * eps) > 3e8:
                    res.append(dict(mech=w, W=float("nan"), status="skip")); continue
                r = push_c(m, eps); W, x, st = r["W"], r["x"], "cert"
            elif w == "cheb":
                mt = VecMeter(m.d); r = cheb_local(m, eps, mt, max_wall=WALL)
                W, x, st = mt.total(), r["x"], r["status"]
            elif w == "direct":
                mt = DQMeter(m.d); r = direct_local(m, eps, mt, wall_cap=WALL)
                W, x, st = mt.total(), r["x"], r["status"]
            elif w == "amg":
                mt = DQMeter(m.d); r = amg_local(m, eps, mt, wall_cap=WALL)
                W, x, st = mt.total(), r["x"], r["status"]
            elif w == "amgO":
                mt = DQMeter(m.d)
                r = amg_local(m, eps, mt, wall_cap=WALL, x_exact=x0, oracle=True)
                W, x, st = mt.total(), r["x"], r["status"] + "-oracle"
            err = float(np.max(np.abs(x - x0) / m.sqd))
            res.append(dict(mech=w, W=float(W), status=st, err=err,
                            ok=bool(err <= eps * 1.0000001), wall=time.time()-t0))
        except Exception as e:
            res.append(dict(mech=w, W=float("nan"), status="EXC:%s" % e,
                            err=float("nan"), ok=False))
    best = min([r for r in res if np.isfinite(r["W"]) and r.get("ok")],
               key=lambda r: r["W"], default=None)
    row = dict(tag=tag, alpha=alpha, eps=eps, n=m.n, volS=volS,
               volS_eps=volS*eps, runs=res,
               bestW=(best["W"] if best else float("nan")),
               bestmech=(best["mech"] if best else None))
    print("  %-10s eps=%-8.1e a=%-9.3g vol*eps=%-6.3f | " % (tag, eps, alpha,
          volS*eps) + "  ".join("%s:%.3g" % (r["mech"], r["W"]*eps)
          for r in res) + " | best W*eps=%.4g (%s)"
          % (row["bestW"]*eps, row["bestmech"]), flush=True)
    return row


def main():
    rows = []
    print("== PATH ridge  alpha = 7.4 eps^2 ==", flush=True)
    for eps in (3e-3, 1e-3, 3e-4, 1e-4, 3e-5):
        adj, seed = fam.zoo.path(int(min(60000, 4.0/eps)), seed_end=True)
        rows.append(one(adj, seed, 7.4*eps*eps, eps, "path_ridge",
                        ("direct", "amg", "amgO"))); del adj
    print("== STAR ridge  m = 0.9/(2 eps),  alpha = 2^-10 ==", flush=True)
    for eps in (1e-3, 1e-4, 1e-5, 3e-6):
        a = 2.0**-10; mst = int(0.9*(1-a)/(2*eps))
        adj, seed = fam.zoo.star(mst)
        rows.append(one(adj, seed, a, eps, "star_ridge",
                        ("push", "direct", "amg"))); del adj
    print("== GRID2D ridge  alpha = 15.3 eps ==", flush=True)
    for eps in (1e-4, 3e-5, 1e-5, 3e-6, 1e-6):
        a = 15.3*eps
        w = int(min(501, max(41, 2.4*2.0/math.sqrt(2*a))))
        w += (w % 2 == 0)
        adj, seed = fam.fast_grid(w, w)
        rows.append(one(adj, seed, a, eps, "grid2d_ridge",
                        ("amg", "amgO", "direct"))); del adj
    print("== EXPANDER ridge  n = 0.85/(3 eps) ==", flush=True)
    for eps in (1e-3, 3e-4, 1e-4, 3e-5):
        for a in (2.0**-4, 2.0**-12):
            nn = int(0.85/(3*eps))
            adj, seed = fam.zoo.random_regular(nn, 3)
            rows.append(one(adj, seed, a, eps, "exp_ridge_a%g" % a,
                            ("amg", "amgO", "cheb", "push"))); del adj
    json.dump(rows, open(f"{OUT}/ridge.json", "w"))
    print("\n== SLOPES of log(W*eps) vs log(1/eps) (0 = exactly O(1/eps)) ==")
    for tag in sorted(set(r["tag"] for r in rows)):
        rs = [r for r in rows if r["tag"] == tag and np.isfinite(r["bestW"])]
        if len(rs) < 3: continue
        x = np.log([1/r["eps"] for r in rs]); y = np.log([r["bestW"]*r["eps"] for r in rs])
        sl = np.polyfit(x, y, 1)[0]
        vv = np.log([max(r["volS_eps"],1e-12) for r in rs])
        slv = np.polyfit(x, vv, 1)[0]
        print("%-16s slope(W*eps) = %+.3f    slope(vol*eps) = %+.3f   "
              "W*eps range [%.3g, %.3g]   mechs %s"
              % (tag, sl, slv, min(r["bestW"]*r["eps"] for r in rs),
                 max(r["bestW"]*r["eps"] for r in rs),
                 sorted(set(r["bestmech"] for r in rs))))


main()
