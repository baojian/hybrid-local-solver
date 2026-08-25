"""Stage 4: the practical certificate (e') -- profile localized supersolution.
Tradeoff curve Ahat_e(K) vs charged cost, on the residual an algorithm ACTUALLY
leaves (region-restricted solve => ring residual; push => nonneg dense residual).
Plus adversarial soundness tests for every candidate."""
import json, math, sys, time
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla
sys.path.insert(0, "/home/claude/work/overnight/i4f")
from core import *

OUT = "/home/claude/work/overnight/i4f/out"
EPS = 1e-5
FAMS = [
  ("path",       lambda: zoo.path(6000, seed_end=True)),
  ("caterpillar",lambda: zoo.caterpillar(3000, arm=1)),
  ("spider",     lambda: zoo.spider(16, 400)),
  ("grid2d",     lambda: fam.fast_grid(121, 121)),
  ("grid3d",     lambda: fam.fast_grid3(21)),
  ("btree",      lambda: zoo.binary_tree(13)),
  ("exp3reg",    lambda: zoo.random_regular(6000, 3)),
  ("rrt",        lambda: fam.rrt(15000)),
  ("hidden_hub", lambda: fam.hidden_hub(6, 15000)),
  ("decoy_hub",  lambda: zoo.decoy_hub(3000, 3000)),
  ("star",       lambda: zoo.star(15000)),
]
ALPHAS = [2.0**-4, 2.0**-6, 2.0**-8, 2.0**-10, 2.0**-12]
KS = [0, 1, 2, 4, 8, 16, 32, 64, 128]

rows = []
for name, mk in FAMS:
    adj, seed = mk()
    for a in ALPHAS:
        m = GModel(adj, a, seed); c, ga = consts(a)
        x0, pi = exact(m); u = pi / m.d
        Se = np.flatnonzero(u > EPS)
        if Se.size == 0 or Se.size >= m.n: continue
        volSe = float(m.d[Se].sum())
        for kind in ("opt", "push"):
            if kind == "opt":
                pih = xh_restricted(m, Se)
            else:
                pih, _, _ = push_run(m, ga * EPS)
            st = stats(m, pih, pi)
            r = resid_push(m, pih)
            if st["theta"] <= 0: continue
            t0 = time.time()
            try:
                curve = escape_profile(m, r, set(KS))
            except Exception as e:
                print("EXC", name, a, kind, e, flush=True); continue
            # soundness: Ahat_e(K) must be >= A_real for every K
            snd = all(v[0] >= st["A"] - 1e-9 for v in curve.values())
            rows.append(dict(fam=name, alpha=a, kind=kind, A_real=st["A"],
                             volSe=volSe, volT=st["volT"], nT=st["nT"],
                             sign=st["signT"], sound=bool(snd),
                             curve={str(k): curve[k] for k in curve},
                             sqrt_a=math.sqrt(a), wall=time.time()-t0))
            ks = sorted(curve)
            print("%-11s a=2^%-4.0f %-5s A_real=%.4g  Ahat_e: %s"
                  % (name, math.log2(a), kind, st["A"],
                     " ".join("K%d=%.3g" % (k, curve[k][0]) for k in ks[:6])), flush=True)
    del adj
json.dump(rows, open(f"{OUT}/esc4.json", "w"))
print("done", len(rows))
