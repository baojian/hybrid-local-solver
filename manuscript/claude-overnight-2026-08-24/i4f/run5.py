"""Stage 5: push (fixed accumulator) -- amplification + certificate tax."""
import json, math, sys, time
import numpy as np
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
ALPHAS = [2.0**-4, 2.0**-6, 2.0**-8, 2.0**-10]
rows = []
for name, mk in FAMS:
    adj, seed = mk()
    for a in ALPHAS:
        m = GModel(adj, a, seed); c, ga = consts(a)
        x0, pi = exact(m); u = pi / m.d
        Se = np.flatnonzero(u > EPS)
        if Se.size == 0 or Se.size >= m.n: continue
        pc, rc, Wc = push_run(m, ga * EPS)
        st = stats(m, pc, pi)
        best = (1.0, Wc, st["err"])
        if st["err"] <= EPS:
            for mult in [1.5, 2, 3, 5, 8, 12, 20, 32, 50, 80, 128, 200, 320]:
                p2, _, W2 = push_run(m, ga * EPS * mult)
                e2 = float(np.max(np.abs(p2 - pi) / m.d))
                if e2 <= EPS: best = (mult, W2, e2)
                else: break
        rows.append(dict(fam=name, alpha=a, volSe=float(m.d[Se].sum()),
                         A_real=st["A"], err_cert=st["err"], theta=st["theta"],
                         volT=st["volT"], nT=st["nT"], sign=st["signT"],
                         W_cert=Wc, W_oracle=best[1], mult_oracle=best[0],
                         tax=Wc / max(best[1], 1e-12)))
        print("%-11s a=2^%-4.0f push A_real=%.4g err/eps=%.3g sign=%s W %.4g -> %.4g  tax x%.2f (mult %.0f)"
              % (name, math.log2(a), st["A"], st["err"]/EPS, st["signT"], Wc, best[1],
                 Wc/max(best[1],1e-12), best[0]), flush=True)
    del adj
json.dump(rows, open(f"{OUT}/push5.json", "w"))
print("done", len(rows))
