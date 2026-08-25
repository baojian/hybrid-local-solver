"""Stage 6: the payoff.  Certified stopping radius of a region method under
(a) the repo rule vs (e') profile localized supersolution at K=ceil(4/sqrt(a))
vs the ORACLE (exact semantic error)."""
import json, math, sys, time
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4f")
from core import *
EPS = 1e-5
OUT = "/home/claude/work/overnight/i4f/out"
FAMS = [("path", lambda: zoo.path(6000, seed_end=True)),
        ("spider", lambda: zoo.spider(16, 400)),
        ("grid2d", lambda: fam.fast_grid(101, 101)),
        ("hidden_hub", lambda: fam.hidden_hub(6, 15000))]
rows = []
for name, mk in FAMS:
    adj, seed = mk()
    for a in [2.0 ** -4, 2.0 ** -6, 2.0 ** -8]:
        m = GModel(adj, a, seed)
        c, ga = consts(a)
        x0, pi = exact(m)
        u = pi / m.d
        Se = np.flatnonzero(u > EPS)
        if Se.size == 0 or Se.size >= m.n:
            continue
        sh, dist = bfs_shells(m)
        K = int(math.ceil(4.0 / math.sqrt(a)))
        Rc = Ro = Re = None
        vc = vo = ve = ce = None
        for R in range(1, len(sh) - 1):
            S = np.concatenate(sh[:R + 1])
            if S.size >= m.n:
                break
            pih = xh_restricted(m, S)
            st = stats(m, pih, pi)
            volB = float(m.d[S].sum())
            if Ro is None and st["err"] <= EPS:
                Ro, vo = R, volB
            if Rc is None and st["thetaQ"] < a * EPS:
                Rc, vc = R, volB
            if Re is None and st["theta"] > 0 and st["theta"] / (1 - c) <= 50 * EPS:
                try:
                    cv = escape_profile(m, resid_push(m, pih), {K}, cap=60000)
                    Ah, volO, nnzO = cv[K]
                    if st["theta"] * Ah / (1 - c) <= EPS:
                        Re, ve, ce = R, volB, volO
                except Exception as e:
                    pass
            if Rc and Ro and Re:
                break
        volSe = float(m.d[Se].sum())
        rows.append(dict(fam=name, alpha=a, K=K, R_cert=Rc, R_esc=Re, R_oracle=Ro,
                         vol_cert=vc, vol_esc=ve, vol_oracle=vo, cert_read=ce,
                         volSe=volSe))
        print("%-11s a=2^%-4.0f K=%-4d R %s/%s/%s vol %s/%s/%s tax_repo=%s tax_esc=%s certread/volSe=%s"
              % (name, math.log2(a), K, Rc, Re, Ro, vc, ve, vo,
                 ("%.2f" % (vc / vo)) if vc and vo else "-",
                 ("%.2f" % (ve / vo)) if ve and vo else "-",
                 ("%.2f" % (ce / max(volSe, 1))) if ce else "-"), flush=True)
    del adj
json.dump(rows, open(f"{OUT}/pay6.json", "w"))
print("done")
