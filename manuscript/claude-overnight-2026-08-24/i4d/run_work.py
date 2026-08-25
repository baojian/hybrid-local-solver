"""E2+E3: TOTAL charged work at output-saturating cells, and on adversaries.

Reference curves per cell:  1/eps ,  1/(sqrt(alpha)*eps) [classic FY22] ,
vol(S_eps) [the true output measure].  Every run is verified: semantic error
max_i |pi_hat_i - pi_i|/d_i <= eps.
"""
import json, math, os, sys, time
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4d")
import fam
from fam import GModel
from amglib import VecMeter, amg_local, push_c, cheb_local, direct_local

OUT = "/home/claude/work/overnight/i4d/out"
WALL = 30.0


class DQMeter(VecMeter):
    """Same ledger, except the outer boundary RING is only DEGREE-QUERIED.
    Justification (I4-D Lemma C): the residual row at a ring vertex h is
    r_h/sqrt(d_h) = -((1-a)/2) * sum_{w in S, w~h} u_w / d_h ; the edges S->h
    and the values u_w are already known from having scanned S, so d_h is the
    ONLY new datum, i.e. one O(1) degree query.  A ring vertex that is later
    admitted to the region is charged its full degree at that point."""
    def ring_scan(self, idx):
        k = len(idx)
        if k:
            self.C_resp += float(k)
            self.solve += float(k)
        self.ring_dq = getattr(self, "ring_dq", 0.0) + float(k)


def run_cell(adj, seed, alpha, eps, tag, which=("push", "cheb", "direct",
                                                "amg", "directDQ", "amgDQ"),
             volS=None, nS=None, note=""):
    m = GModel(adj, alpha, seed)
    x0 = m.solve_exact()
    u = x0 * m.sqd / m.d
    S = np.flatnonzero(u > eps)
    if volS is None:
        volS = float(m.d[S].sum()); nS = int(S.size)
    rows = []
    base = dict(tag=tag, n=m.n, alpha=alpha, eps=eps, volS=volS, nS=nS,
                inv_eps=1.0 / eps, fy22=1.0 / (math.sqrt(alpha) * eps),
                note=note)
    for w in which:
        t0 = time.time()
        try:
            if w == "push":
                if 1.0 / (alpha * eps) > 3e8:
                    rows.append(dict(base, mech=w, W=float("nan"),
                                     status="skip-too-slow", err=float("nan")))
                    continue
                r = push_c(m, eps)
                W, x, status = r["W"], r["x"], "cert"
            elif w == "cheb":
                mt = VecMeter(m.d)
                r = cheb_local(m, eps, mt, max_wall=WALL)
                W, x, status = mt.total(), r["x"], r["status"]
            elif w in ("direct", "directDQ"):
                mt = (DQMeter if w.endswith("DQ") else VecMeter)(m.d)
                r = direct_local(m, eps, mt, wall_cap=WALL)
                W, x, status = mt.total(), r["x"], r["status"]
            else:
                mt = (DQMeter if w.endswith("DQ") else VecMeter)(m.d)
                r = amg_local(m, eps, mt, wall_cap=WALL)
                W, x, status = mt.total(), r["x"], r["status"]
            err = float(np.max(np.abs(x - x0) / m.sqd))
            rows.append(dict(base, mech=w, W=float(W), status=status,
                             err=err, ok=bool(err <= eps * 1.0000001),
                             wall=time.time() - t0))
        except Exception as e:
            rows.append(dict(base, mech=w, W=float("nan"), status="EXC:%s" % e,
                             err=float("nan"), ok=False))
        print("  %-9s W=%-12.4g W*eps=%-9.3g W/vol=%-8.3g err/eps=%-8.3g %s"
              % (w, rows[-1]["W"], rows[-1]["W"] * eps,
                 rows[-1]["W"] / max(volS, 1.0), rows[-1]["err"] / eps,
                 rows[-1]["status"]), flush=True)
    return rows


def main():
    allrows = []
    E1 = json.load(open(f"{OUT}/out_measure.json"))
    B = {"path": lambda: fam.zoo.path(40000, seed_end=True),
         "star": lambda: fam.zoo.star(60000),
         "spider": lambda: fam.zoo.spider(64, 900),
         "caterpillar": lambda: fam.zoo.caterpillar(30000, arm=1),
         "comb": lambda: fam.comb(400, 60),
         "btree": lambda: fam.zoo.binary_tree(16),
         "rrt": lambda: fam.rrt(60000),
         "pa_tree": lambda: fam.powerlaw_tree(60000),
         "grid2d": lambda: fam.fast_grid(401, 401),
         "grid3d": lambda: fam.fast_grid3(61),
         "exp3reg": lambda: fam.zoo.random_regular(40000, 3),
         "cycle": lambda: fam.zoo.cycle(40000)}
    # --- E2: the output-saturating cell of every family (bounded size) ---
    cells = []
    for name in B:
        cand = [r for r in E1 if r["family"] == name and not r["clipped"]
                and 1500 <= r["volS"] <= 90000]
        if not cand:
            continue
        best = max(cand, key=lambda r: r["volS_eps"])
        cells.append((name, best["alpha"], best["eps"], best["volS"],
                      best["nS"], "saturating"))
    for name, a, eps, volS, nS, note in cells:
        print(f"\n[E2 {name}] a=2^{math.log2(a):.1f} eps={eps:g} "
              f"vol(S_eps)={volS:.0f} vol*eps={volS*eps:.3f}", flush=True)
        adj, seed = B[name]()
        allrows += run_cell(adj, seed, a, eps, name, volS=volS, nS=nS,
                            note=note)
        del adj

    # --- E3a: STAR at the critical width (output ratio -> 1) ---
    for eps in (1e-4, 1e-5):
        a = 2.0 ** -10
        mstar = int(0.9 * (1 - a) / (2 * eps))
        print(f"\n[E3 star-critical] m={mstar} eps={eps:g}", flush=True)
        adj, seed = fam.zoo.star(mstar)
        allrows += run_cell(adj, seed, a, eps, "star_crit", note="critical")
        del adj
    # --- E3b: EXPANDER at the critical size n = 1/(3 eps) ---
    for eps in (1e-4, 3e-5):
        for a in (2.0 ** -4, 2.0 ** -12):
            nexp = int(0.85 / (3 * eps))
            print(f"\n[E3 exp-critical] n={nexp} a=2^{math.log2(a):.0f} "
                  f"eps={eps:g}", flush=True)
            adj, seed = fam.zoo.random_regular(nexp, 3)
            allrows += run_cell(adj, seed, a, eps, "exp_crit",
                                note="critical")
            del adj
    # --- E3c: DEEP PATH at the saturating alpha = 7.4 eps^2 ---
    for eps in (1e-3, 1e-4):
        a = 7.4 * eps * eps
        print(f"\n[E3 path-saturating] a={a:.3g} eps={eps:g}", flush=True)
        adj, seed = fam.zoo.path(30000, seed_end=True)
        allrows += run_cell(adj, seed, a, eps, "path_sat", note="alpha~eps^2")
        del adj
    # --- E3d: HIDDEN HUB (boundary of unbounded degree) ---
    for M in (1000, 10000, 100000):
        a, eps = 2.0 ** -6, 1e-3
        print(f"\n[E3 hidden-hub] M={M}", flush=True)
        adj, seed = fam.hidden_hub(6, M)
        allrows += run_cell(adj, seed, a, eps, "hidden_hub_M%d" % M,
                            which=("push", "direct", "directDQ", "amg",
                                   "amgDQ"), note="hub deg %d" % M)
        del adj
    # --- E3e: BALL TRAP (clique off the middle of the support path) ---
    for M in (100, 300, 600):
        eps = 1e-3
        a = 7.4 * eps * eps
        L = 400
        print(f"\n[E3 ball-trap] M={M} clique-vol={M*(M-1)}", flush=True)
        adj, seed = fam.ball_trap(L, M, at=60)
        allrows += run_cell(adj, seed, a, eps, "ball_trap_M%d" % M,
                            which=("push", "direct", "directDQ", "amg",
                                   "amgDQ"), note="clique %d at depth 60" % M)
        del adj
    with open(f"{OUT}/work.json", "w") as f:
        json.dump(allrows, f)
    bad = [r for r in allrows if r.get("ok") is False
           and not str(r["status"]).startswith("skip")]
    print("\nFAILED/UNCERTIFIED runs:", len(bad))
    for r in bad[:20]:
        print("   ", r["tag"], r["mech"], r["status"], r["err"], r["eps"])


main()
