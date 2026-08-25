"""Stage 7 (quick): A_real for residual-SPREADING methods (ISTA/RPPR, Chebyshev)."""
import math, sys, json
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4f")
from core import *
EPS = 1e-5
FAMS = [("path", lambda: zoo.path(4000, seed_end=True)),
        ("grid2d", lambda: fam.fast_grid(81, 81)),
        ("rrt", lambda: fam.rrt(8000)),
        ("exp3reg", lambda: zoo.random_regular(4000, 3))]
rows = []
for name, mk in FAMS:
    adj, seed = mk()
    for a in [2.0 ** -4, 2.0 ** -6, 2.0 ** -8]:
        m = GModel(adj, a, seed); c, ga = consts(a)
        x0, pi = exact(m); u = pi / m.d
        Se = np.flatnonzero(u > EPS)
        if Se.size == 0 or Se.size >= m.n: continue
        out = {}
        try:
            pih = ista_run(m, ga * EPS, rho=max(1e-9, 1.0 / max(float(m.d[Se].sum()), 10.0)), iters=3000)
            out["ista"] = stats(m, pih, pi)
        except Exception as e:
            out["ista"] = None
        try:
            out["cheb"] = stats(m, cheb_iterate(m, int(math.ceil(2.0 / math.sqrt(a))) + 5), pi)
        except Exception:
            out["cheb"] = None
        rows.append(dict(fam=name, alpha=a,
                         A_ista=out["ista"]["A"] if out["ista"] else None,
                         A_cheb=out["cheb"]["A"] if out["cheb"] else None,
                         nT_ista=out["ista"]["nT"] if out["ista"] else None,
                         nT_cheb=out["cheb"]["nT"] if out["cheb"] else None, n=m.n))
        print("%-8s a=2^%-4.0f  A_ista=%s (nT=%s)  A_cheb=%s (nT=%s)  n=%d"
              % (name, math.log2(a),
                 ("%.4g" % rows[-1]["A_ista"]) if rows[-1]["A_ista"] else "-", rows[-1]["nT_ista"],
                 ("%.4g" % rows[-1]["A_cheb"]) if rows[-1]["A_cheb"] else "-", rows[-1]["nT_cheb"], m.n), flush=True)
    del adj
json.dump(rows, open("/home/claude/work/overnight/i4f/out/spread7.json", "w"))
print("done")
