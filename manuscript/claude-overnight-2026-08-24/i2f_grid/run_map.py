"""I2-F main sweep on grid(w,w), CENTER seed.

For each (alpha, eps): size w so that the eps-support (and, where feasible,
the certified region) sit strictly inside the grid; then run

  PUSH            lazy ACL push at threshold eps (C kernel)      [one-hop]
  CHEB            truncated Chebyshev, measured certificate      [polynomial]
  PUSHCHEB        push to a warm tolerance, then Chebyshev       [hybrid]
  ND-EES          explore + nested-dissection direct solve       [elimination]
  MG              local geometric multigrid V-cycles             [multilevel]

all charged with the same Meter, all verified against the exact sparse solve.
MG and ND are additionally run in an ORACLE bracket (stop at semantic error
<= eps rather than at the certificate) to separate mechanism cost from the
cost of self-certification.
"""
import csv
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/i2f_grid")
from gridlib import (LatticeModel, VecMeter, support_stats, push_c,
                     cheb_local, mg_local, nd_ees, ladder)

WMAX = 517
PUSH_CAP = 1.5e9          # skip push above this predicted charge
OUT = "/home/claude/work/overnight/i2f_grid/out"


def size_w(alpha, eps):
    """Grid side: 2*R_cert + margin, R_cert from the certified-boundary
    estimate  (alpha/2) e^{-2 sqrt(a) r} = 8 alpha eps  =>  r =
    ln(1/(16 eps))/(2 sqrt(alpha)), floored by the diffusive scale 1/sqrt(a)."""
    ra = math.sqrt(alpha)
    R = max(1.0 / ra, math.log(1.0 / (16 * eps)) / (2 * ra))
    m_need = 2 * int(math.ceil(R)) + 1
    lad = [m for m in ladder(4 * WMAX, 2) if m >= m_need]
    m = lad[0] if lad else m_need
    w = min(WMAX, m + 5)
    return int(w) | 1, int(m)


def run_cell(alpha, eps, verbose=True):
    t0 = time.time()
    w, m_pred = size_w(alpha, eps)
    M = LatticeModel(w, alpha, 2)
    x0 = M.solve_exact()
    ss = support_stats(M, eps)
    row = dict(alpha=alpha, eps=eps, w=w, n=M.n, m_pred=m_pred,
               nS=ss["nS"], volS=ss["volS"], R_sem=ss["R"],
               supp_bd=ss["touches_bd"],
               target_classic=1.0 / (math.sqrt(alpha) * eps),
               target_push=1.0 / (alpha * eps))
    if ss["nS"] == 0:
        row["trivial"] = True
        return row
    row["trivial"] = False

    # ---------------- push ----------------
    if 0.3 / (alpha * eps) < PUSH_CAP:
        p = push_c(M, eps)
        e = M.semantic_err(p["x"])
        assert e <= eps * (1 + 1e-9), ("push", e, eps)
        row.update(W_push=p["W"], err_push=e, push_status="ok")
    else:
        row.update(W_push=float("nan"), err_push=float("nan"),
                   push_status="skipped")

    # ---------------- Chebyshev ----------------
    mm = VecMeter(M.d)
    o = cheb_local(M, eps, mm, max_wall=200.0)
    e = M.semantic_err(o["x"])
    row.update(W_cheb=mm.total(), it_cheb=o["iters"], err_cheb=e,
               cheb_status=o["status"], cheb_vec=mm.vector())
    if o["status"] == "cert":
        assert e <= eps * (1 + 1e-9), ("cheb", e, eps)

    # ---------------- push -> Chebyshev hybrid ----------------
    best = None
    for ew in (1e-2, 1e-3, 1e-4, 1e-5):
        if ew <= 10 * eps or 0.3 / (alpha * ew) > 3e8:
            continue
        pw = push_c(M, ew)
        mmh = VecMeter(M.d)
        mmh.C_adj = pw["C_adj"]; mmh.R_adj = pw["R_adj"]
        mmh.seen = (pw["x"] != 0.0)
        oh = cheb_local(M, eps, mmh, x_init=pw["x"], max_wall=200.0)
        eh = M.semantic_err(oh["x"])
        tot = mmh.total()
        if oh["status"] == "cert" and (best is None or tot < best[0]):
            best = (tot, ew, oh["iters"], eh, pw["W"])
    if best:
        row.update(W_hyb=best[0], eps_warm=best[1], it_hyb=best[2],
                   err_hyb=best[3], W_hyb_push=best[4], hyb_status="cert")
        assert best[3] <= eps * (1 + 1e-9), ("hyb", best[3], eps)
    else:
        row.update(W_hyb=float("nan"), hyb_status="none")

    # ---------------- ND-EES ----------------
    mm = VecMeter(M.d)
    o = nd_ees(M, eps, mm, x_exact=x0)
    e = M.semantic_err(o["x"])
    row.update(W_nd=mm.total(), m_nd=o["m"], err_nd=e, nd_status=o["status"],
               volOmega_nd=o["volOmega"], nd_vec=mm.vector())
    if o["status"] == "cert":
        assert e <= eps * (1 + 1e-9), ("nd", e, eps)
    mm = VecMeter(M.d)
    o = nd_ees(M, eps, mm, x_exact=x0, oracle=True)
    row.update(W_nd_or=mm.total(), m_nd_or=o["m"], nd_or_status=o["status"])

    # ---------------- local multigrid ----------------
    mm = VecMeter(M.d)
    o = mg_local(M, eps, mm, x_exact=x0)
    e = M.semantic_err(o["x"])
    row.update(W_mg=mm.total(), m_mg=o["m"], cyc_mg=o["cycles"], err_mg=e,
               mg_status=o["status"], volOmega_mg=o["volOmega"],
               mg_vec=mm.vector(), mg_hist=o["hist"])
    if o["status"] == "cert":
        assert e <= eps * (1 + 1e-9), ("mg", e, eps)
    mm = VecMeter(M.d)
    o = mg_local(M, eps, mm, x_exact=x0, oracle=True)
    row.update(W_mg_or=mm.total(), m_mg_or=o["m"], cyc_mg_or=o["cycles"],
               mg_or_status=o["status"])

    row["wall"] = time.time() - t0
    if verbose:
        print(f"  a=2^{int(round(math.log2(alpha))):>3d} eps={eps:g} w={w} "
              f"nS={row['nS']} volS={row['volS']:.0f} Rsem={row['R_sem']} | "
              f"push={row['W_push']:.3g} cheb={row['W_cheb']:.3g} "
              f"hyb={row.get('W_hyb', float('nan')):.3g} "
              f"nd={row['W_nd']:.3g} mg={row['W_mg']:.3g} "
              f"(mg m={row['m_mg']} cyc={row['cyc_mg']} {row['mg_status']}) "
              f"[{row['wall']:.1f}s]", flush=True)
    return row


def main():
    alphas = [2.0 ** -k for k in (4, 6, 8, 10, 12)]
    epss = [1e-3, 1e-4, 1e-6, 1e-8]
    rows = []
    for eps in epss:
        for a in alphas:
            w, mneed = size_w(a, eps)
            if mneed + 5 > WMAX:
                print(f"  skip a=2^{int(round(math.log2(a)))} eps={eps:g}: "
                      f"needs w>={mneed+5} > WMAX", flush=True)
                continue
            try:
                rows.append(run_cell(a, eps))
            except Exception as ex:
                print(f"  FAILED a={a} eps={eps}: {type(ex).__name__}: {ex}",
                      flush=True)
                rows.append(dict(alpha=a, eps=eps, error=str(ex)))
            with open(f"{OUT}/map.json", "w") as f:
                json.dump(rows, f, default=str)
    # flat CSV
    keys = ["alpha", "eps", "w", "n", "trivial", "nS", "volS", "R_sem",
            "supp_bd", "target_classic", "target_push", "W_push", "W_cheb",
            "it_cheb", "W_hyb", "eps_warm", "W_nd", "m_nd", "W_nd_or",
            "W_mg", "m_mg", "cyc_mg", "W_mg_or", "m_mg_or", "cyc_mg_or",
            "volOmega_mg", "volOmega_nd", "mg_status", "nd_status",
            "cheb_status", "push_status", "err_mg", "err_nd", "err_cheb",
            "err_push", "wall"]
    with open(f"{OUT}/map.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        wtr.writeheader()
        for r in rows:
            wtr.writerow(r)
    print("wrote", f"{OUT}/map.csv")


if __name__ == "__main__":
    main()
