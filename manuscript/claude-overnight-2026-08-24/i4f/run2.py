"""Stage 2: candidate replacement certificates -- soundness, tightness, charged cost.

All amplification numbers are NORMALISED:  a bound Ahat is valid iff
   err <= Ahat * theta/(1-c),   i.e. the repo rule is Ahat = 1.
Smaller Ahat = tighter = fewer wasted work units.  A_real = (1-c) err/theta.
"""
import json, math, sys, time
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla
sys.path.insert(0, "/home/claude/work/overnight/i4f")
from core import *
from core import neumann_curve_correct, escape_curve

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
  ("star",       lambda: zoo.star(15000)),
  ("decoy_hub",  lambda: zoo.decoy_hub(3000, 3000)),
]
ALPHAS = [2.0**-2, 2.0**-4, 2.0**-6, 2.0**-8, 2.0**-10, 2.0**-12]


rows = []
for name, mk in FAMS:
    adj, seed = mk()
    for a in ALPHAS:
        t0 = time.time()
        m = GModel(adj, a, seed)
        c, ga = consts(a)
        x0, pi = exact(m); u = pi / m.d
        Se = np.flatnonzero(u > EPS)
        if Se.size == 0 or Se.size >= m.n:
            continue
        # region method: exact restricted solve on S_eps -> residual on the ring T
        pih = xh_restricted(m, Se)
        st = stats(m, pih, pi)
        r = resid_push(m, pih)
        T = np.flatnonzero(np.abs(r) > 1e-13 * st["theta"] * m.d)
        if T.size == 0 or T.size > 0.9 * m.n:
            continue
        Ash, G = Ahat_sharp(m, T)
        # (d) max-principle bound: tau = max_{v in T} |N(v) cap Omega| / d_v
        inS = np.zeros(m.n, bool); inS[Se] = True
        tau = 0.0
        for v in T:
            nb = m.indices[m.indptr[v]:m.indptr[v+1]]
            tau = max(tau, float(inS[nb].sum()) / m.d[v])
        Amp = 1.0 / (1.0 + c * tau)
        # (b) one-sided l1 variant
        Al1 = min(1.0, float(np.abs(r).sum()) / (st["theta"] * m.d.min()) * (1 - c) / (1 - c))
        Al1 = min(1.0, float(np.abs(r).sum()) / (st["theta"] * m.d.min()))
        Ks = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        Ks = [k for k in Ks if k <= 512]
        neu = neumann_curve_correct(m, T, set(Ks))
        esc = escape_curve(m, T, set([1, 2, 4, 8, 16, 32, 64]))
        rows.append(dict(fam=name, alpha=a, nT=int(T.size), volT=float(m.d[T].sum()),
                         volSe=float(m.d[Se].sum()), A_real=st["A"], A_sharp=Ash,
                         A_mp=Amp, tau=tau, A_l1=Al1, sign=st["signT"],
                         neumann={str(k): neu[k] for k in neu},
                         escape={str(k): esc[k] for k in esc},
                         maxdegT=float(m.d[T].max()), sqrt_a=math.sqrt(a)))
        print("%-12s a=2^%-4.0f nT=%-5d A_real=%.4g A_sharp=%.4g A_mp=%.3f  %.1fs"
              % (name, math.log2(a), T.size, st["A"], Ash, Amp, time.time()-t0), flush=True)
    del adj
json.dump(rows, open(f"{OUT}/cert2.json", "w"))
print("done", len(rows))
