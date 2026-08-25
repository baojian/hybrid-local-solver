"""Stage 3: how much measured work is CERTIFICATE TAX?
For each mechanism: work at the CERTIFIED stop (repo rule) vs work at the
ORACLE stop (exact semantic error <= eps) vs work at the SHARP/ESCAPE stop.
"""
import json, math, sys, time
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla
sys.path.insert(0, "/home/claude/work/overnight/i4f")
from core import *
from core import escape_curve

OUT = "/home/claude/work/overnight/i4f/out"
EPS = 1e-5
FAMS = [
  ("path",       lambda: zoo.path(6000, seed_end=True)),
  ("grid2d",     lambda: fam.fast_grid(121, 121)),
  ("spider",     lambda: zoo.spider(16, 400)),
  ("exp3reg",    lambda: zoo.random_regular(6000, 3)),
  ("rrt",        lambda: fam.rrt(15000)),
  ("hidden_hub", lambda: fam.hidden_hub(6, 15000)),
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
        volSe = float(m.d[Se].sum())
        rec = dict(fam=name, alpha=a, volSe=volSe, nSe=int(Se.size))
        # ---- MECHANISM 1: lazy push (r>=0). work = pushed degree volume.
        # certified stop: eps_appr = ga*eps.  oracle: largest eps_appr with err<=eps.
        pc, rc, Wc = push_run(m, ga * EPS)
        errc = float(np.max(np.abs(pc - pi) / m.d))
        lo, hi = ga * EPS, ga * EPS
        best = (ga * EPS, Wc, errc)
        for mult in [1.5, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200, 400, 800]:
            p2, _, W2 = push_run(m, ga * EPS * mult)
            e2 = float(np.max(np.abs(p2 - pi) / m.d))
            if e2 <= EPS: best = (ga * EPS * mult, W2, e2)
            else: break
        rec["push_W_cert"] = Wc; rec["push_err_cert"] = errc
        rec["push_W_oracle"] = best[1]; rec["push_mult_oracle"] = best[0] / (ga * EPS)
        rec["push_tax"] = Wc / max(best[1], 1e-12)
        # ---- MECHANISM 2: ball-restricted exact solve (elimination/region line)
        sh, dist = bfs_shells(m)
        Rc = Ro = Re = None; volc = volo = vole = None
        prev = None
        for R in range(1, len(sh) - 1):
            S = np.concatenate(sh[:R + 1])
            if S.size >= m.n: break
            pih = xh_restricted(m, S)
            st = stats(m, pih, pi)
            volB = float(m.d[S].sum())
            if Ro is None and st["err"] <= EPS: Ro, volo = R, volB
            if Rc is None and st["thetaQ"] < a * EPS: Rc, volc = R, volB
            if Re is None:
                r = resid_push(m, pih)
                T = np.flatnonzero(np.abs(r) > 1e-13 * st["theta"] * m.d)
                if T.size and T.size < 0.9 * m.n:
                    Ash, _ = Ahat_sharp(m, T)
                    if st["theta"] * Ash / (1 - c) <= EPS: Re, vole = R, volB
            if Rc is not None and Ro is not None and Re is not None: break
        rec.update(ball_R_cert=Rc, ball_R_oracle=Ro, ball_R_sharp=Re,
                   ball_vol_cert=volc, ball_vol_oracle=volo, ball_vol_sharp=vole)
        if volc and volo: rec["ball_tax_vol"] = volc / volo
        if volc and vole: rec["ball_tax_removed"] = volc / vole
        rows.append(rec)
        print("%-11s a=2^%-4.0f push tax x%.2f (W %.3g->%.3g)  ball R %s/%s/%s vol tax x%s"
              % (name, math.log2(a), rec["push_tax"], Wc, best[1], Rc, Re, Ro,
                 ("%.2f" % rec["ball_tax_vol"]) if rec.get("ball_tax_vol") else "-"), flush=True)
    del adj
json.dump(rows, open(f"{OUT}/tax3.json", "w"))
print("done", len(rows))
