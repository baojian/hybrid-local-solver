"""Sweep the SOR relaxation parameter omega at loose eps.

Hypothesis (author): the "optimal" omega = 2(1+a)/(1+sqrt(a))^2 is derived from
the GLOBAL graph's spectral radius.  At loose eps the push only touches a small
LOCAL subgraph, whose conditioning is better, so the locally-optimal omega
should be SMALLER (nearer 1) than the global one -- and opt-sor's fixed 1.40
over-relaxes.

For each eps this runs sdd_local_sor at a grid of omega in [1, 2) over several
seeded sources and reports the median operations, marking the theoretical
optimum and the empirical best.  omega >= 2 diverges, so the grid stops below
that; any run whose l1 error blows up is flagged UNSTABLE and excluded.

    uv run python -m experiments.run_omega_sweep \
        --dataset com-dblp --alpha 0.05
"""

import argparse

import numpy as np

from src.baselines.sdd_solver import sdd_get_opt, sdd_local_sor
from src.graphs import load_graph


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="com-dblp")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--num-sources", type=int, default=10)
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--min-deg", type=int, default=1)
    ap.add_argument("--mults", default="10,1", help="eps = mult / n")
    ap.add_argument("--omega-lo", type=float, default=1.0)
    ap.add_argument("--omega-hi", type=float, default=1.95)
    ap.add_argument("--omega-step", type=float, default=0.05)
    a = ap.parse_args()

    graph = load_graph(a.dataset)
    n = graph.n
    indptr, indices, degree = graph.indptr, graph.indices, graph.degree
    sq = np.sqrt(degree)
    opt_omega = 2.0 * (1.0 + a.alpha) / (1.0 + np.sqrt(a.alpha)) ** 2.0

    sources = graph.sample_sources(
        count=a.num_sources,
        seed=a.seed,
        min_degree=a.min_deg,
    )
    k = len(sources)

    omegas = list(np.round(np.arange(a.omega_lo, a.omega_hi + 1e-9, a.omega_step), 4))
    # insert the exact theoretical opt only if no grid point is already within
    # half a step of it (otherwise it duplicates a row that rounds the same)
    if not any(abs(w - opt_omega) < a.omega_step / 2.0 for w in omegas):
        omegas.append(round(opt_omega, 4))
        omegas.sort()
    # the grid point nearest the theoretical opt, for the "<- theoretical" mark
    near_opt = min(omegas, key=lambda w: abs(w - opt_omega))
    mults = [float(x) for x in a.mults.split(",")]

    print(f"\n{a.dataset}: n={n:,} alpha={a.alpha}  theoretical opt-omega = {opt_omega:.4f}")
    print(f"{k} sources (seed={a.seed}): {sources}")

    # precompute ground truth + rhs per source (also warms up numba)
    src_b, src_opt = {}, {}
    for src in sources:
        b = np.zeros(n, dtype=np.float64)
        b[src] = 2.0 * a.alpha / ((1.0 + a.alpha) * sq[src])
        src_b[src] = b
        src_opt[src] = sdd_get_opt(n, indptr, indices, degree, src, a.alpha, 1e-10)

    for mult in mults:
        eps = mult / n
        lab = "1/n" if mult == 1 else f"{mult:g}/n"
        print(f"\n===== eps = {lab}  ({eps:.3e}) =====")
        print(f"{'omega':>7} {'median_opers':>14} {'median_l1':>12}  note")
        rows = []
        for w in omegas:
            ops, l1s, unstable = [], [], False
            for src in sources:
                r = sdd_local_sor(
                    n, indptr, indices, degree, src_b[src], a.alpha, eps, w, src_opt[src]
                )
                ops.append(float(np.sum(r[3])))
                le = float(r[2][-1]) if len(r[2]) else float("nan")
                l1s.append(le)
                if not np.isfinite(le) or le > 10.0:
                    unstable = True
            mo = float(np.median(ops))
            ml = float(np.median(l1s))
            rows.append((w, mo, ml, unstable))

        stable = [r for r in rows if not r[3]]
        best_w = min(stable, key=lambda r: r[1])[0] if stable else None
        for w, mo, ml, unstable in rows:
            note = ""
            if w == near_opt:
                note = f"<- theoretical opt ({opt_omega:.4f})"
            if w == best_w:
                note = ("best empirical  " + note).strip()
            if unstable:
                note = "UNSTABLE (l1 blew up)"
            star = "*" if w == best_w else " "
            print(f"{star}{w:>6.2f} {mo:>14,.0f} {ml:>12.3e}  {note}")

        if best_w is not None:
            bo = min(stable, key=lambda r: r[1])[1]
            to = next((r[1] for r in rows if r[0] == near_opt), None)
            msg = f"  -> best omega={best_w:.2f} ({bo:,.0f} median opers)"
            if to:
                msg += f"  vs theoretical {opt_omega:.2f} ({to:,.0f}) = {to / bo:.2f}x"
            print(msg)


if __name__ == "__main__":
    main()
