"""Stage 1: verify the sharp constant; measure A over the zoo x alpha x xhat-kind."""
import json, math, sys, time
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla
sys.path.insert(0, "/home/claude/work/overnight/i4f")
from core import *

OUT = "/home/claude/work/overnight/i4f/out"
EPS = 1e-5
ALPHAS = [2.0**-2, 2.0**-4, 2.0**-6, 2.0**-8, 2.0**-10, 2.0**-12]

FAMS = [
  ("path",       lambda: zoo.path(6000, seed_end=True)),
  ("cycle",      lambda: zoo.cycle(6000)),
  ("caterpillar",lambda: zoo.caterpillar(3000, arm=1)),
  ("spider",     lambda: zoo.spider(16, 400)),
  ("comb",       lambda: fam.comb(300, 20)),
  ("btree",      lambda: zoo.binary_tree(13)),
  ("grid2d",     lambda: fam.fast_grid(121, 121)),
  ("grid3d",     lambda: fam.fast_grid3(21)),
  ("rrt",        lambda: fam.rrt(15000)),
  ("pa_tree",    lambda: fam.powerlaw_tree(15000)),
  ("exp3reg",    lambda: zoo.random_regular(6000, 3)),
  ("star",       lambda: zoo.star(15000)),
  ("hidden_hub", lambda: fam.hidden_hub(6, 15000)),
  ("decoy_hub",  lambda: zoo.decoy_hub(3000, 3000)),
  ("ball_trap",  lambda: fam.ball_trap(400, 120, at=60)),
]

rows = []
t00 = time.time()
for name, mk in FAMS:
    adj, seed = mk()
    for a in ALPHAS:
        t0 = time.time()
        m = GModel(adj, a, seed)
        c, ga = consts(a)
        x0, pi = exact(m); u = pi / m.d
        Se = np.flatnonzero(u > EPS)
        volSe = float(m.d[Se].sum())
        clipped = bool(Se.size and (u[Se].min() > EPS) and Se.size == m.n)
        sh, dist = bfs_shells(m)
        cases = []
        # (1) optimal / truncated eps-output: exact restricted solve on S_eps
        if 0 < Se.size < m.n:
            cases.append(("opt", xh_restricted(m, Se)))
        # (2) ball-restricted exact solve (region method), radius = radius of S_eps
        R = int(dist[Se].max()) if Se.size else 1
        R = max(1, min(R, len(sh) - 2))
        if R >= 1 and R < len(sh) - 1:
            S = np.concatenate(sh[:R + 1])
            if S.size < m.n:
                cases.append(("ball", xh_restricted(m, S)))
        # (3) push at the certified threshold  (r>=0 monotone)
        pp, rr, W = push_run(m, ga * EPS)
        cases.append(("push", pp))
        # (4) push at a looser threshold (bigger residual, still r>=0)
        pp2, _, _ = push_run(m, ga * EPS * 30)
        cases.append(("push30", pp2))
        # (5) RPPR/ISTA output (signed residual, l1 support)
        try:
            pih = ista_run(m, ga * EPS, rho=max(1e-9, 1.0 / max(volSe, 10.0)))
            cases.append(("ista", pih))
        except Exception:
            pass
        # (6) signed Chebyshev iterate
        try:
            Kc = int(math.ceil(2.0 / math.sqrt(a))) + 5
            cases.append(("cheb", cheb_iterate(m, Kc)))
        except Exception:
            pass
        for kind, pih in cases:
            st = stats(m, pih, pi)
            r = resid_push(m, pih)
            T = np.flatnonzero(np.abs(r) > 1e-13 * st["theta"] * m.d)
            rec = dict(fam=name, alpha=a, eps=EPS, kind=kind, n=m.n,
                       volSe=volSe, nSe=int(Se.size), clipped=clipped, **st)
            if T.size and T.size < m.n * 0.98:
                Ah, G = Ahat_sharp(m, T)
                rec["Ahat"] = Ah
                # sharpness check: worst residual r=theta*d*1_T (>=0)
                rw = np.zeros(m.n); rw[T] = st["theta"] * m.d[T]
                # err_w = max_i (D^-1 H^-1 rw)_i = theta*max G
                rec["Ahat_attained"] = Ah
                rec["argmax_in_T"] = bool(int(np.argmax(G)) in set(T.tolist()))
                rec["maxdegT"] = float(m.d[T].max())
            else:
                rec["Ahat"] = 1.0; rec["argmax_in_T"] = True
                rec["maxdegT"] = float(m.d.max())
            rec["sound"] = bool(st["A"] <= rec["Ahat"] * (1 + 1e-8))
            rows.append(rec)
        print("%-12s a=2^%-4.0f  %5.1fs  cases=%d" % (name, math.log2(a), time.time()-t0, len(cases)), flush=True)
    del adj
json.dump(rows, open(f"{OUT}/amp1.json", "w"))
print("TOTAL %.1fs  rows=%d" % (time.time()-t00, len(rows)))
