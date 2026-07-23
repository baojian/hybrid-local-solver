"""Sweep eps over several random sources and report which local solver is
cheapest at each accuracy level.

    uv run python -m experiments.run_eps_sweep \
        --dataset com-dblp --alpha 0.05 --num-sources 10

For eps in {1/n, 0.1/n, 0.01/n, 0.001/n, 0.0001/n}, across `--num-sources`
seeded-random source nodes, it reports per (eps, solver):
  opers    total nodes accessed with multiplicity (sum of `opers`), MEDIAN
           over the sources; the row-minimum is marked with a leading '*'
  l1-err   the solver's OWN `errs[-1]` = ||xt/sqrt(d) - opt_x||_1, MEDIAN
  wins     how many sources that solver had the FEWEST opers on, at that eps

l1-err note: all six solvers here scale to x-coordinates before comparing, so
their `errs` are mutually consistent.

Comparability of `opers` across solvers.  The stop threshold `eps_vec` is
  appr          eps * d          (indicator residual; Lemma 2.1)
  gd sor hb cheby  eps * alpha * d  (gradient residual;  Lemma 2.2)
so the five GRADIENT solvers stop at the SAME certificate and their opers ARE
comparable at equal nominal eps (they land at the same achieved accuracy -- see
the near-equal `gate` column).  Only `appr` uses a looser threshold, so it does
slightly less work for slightly less accuracy; keep that in mind when it wins.
Strictly equal-achieved-accuracy comparisons require a separate calibration
workflow.

Cost warning: APPR is O(1/(alpha*eps)), so tightening eps by 10x costs it ~10x
more work, while the accelerated methods grow far more slowly.  At 1e-4/n APPR
needs ~1e11 operations.  --max-ops skips a solver at all tighter eps once it
exceeds the budget (its cost is monotone in 1/eps, so this never skips a run
that would have been cheap).
"""

import argparse
import time

import numpy as np

from src.baselines.sdd_solver import (
    sdd_get_opt,
    sdd_local_gd,
    sdd_local_appr,
    sdd_local_sor,
    sdd_local_heavy_ball,
    sdd_local_cheby,
    opt_omega,
    adaptive_omega,
)
from src.graphs import load_graph

ALGOS = ("gd", "appr", "sor", "opt-sor", "adp-sor", "hb", "cheby")


def run_one(algo, n, indptr, indices, degree, b, s, alpha, eps, opt_x):
    """Returns (ret, x_hat) with x_hat always in x-coordinates."""
    if algo == "gd":
        ret = sdd_local_gd(n, indptr, indices, degree, b, alpha, eps, opt_x)
    elif algo == "appr":
        ret = sdd_local_appr(n, indptr, indices, degree, s, alpha, eps, opt_x)
    elif algo == "sor":
        ret = sdd_local_sor(n, indptr, indices, degree, b, alpha, eps, 1.0, opt_x)
    elif algo == "opt-sor":
        ret = sdd_local_sor(n, indptr, indices, degree, b, alpha, eps, opt_omega(alpha), opt_x)
    elif algo == "adp-sor":
        ret = sdd_local_sor(
            n, indptr, indices, degree, b, alpha, eps, adaptive_omega(alpha, eps, n), opt_x
        )
    elif algo == "hb":
        ret = sdd_local_heavy_ball(n, indptr, indices, degree, b, alpha, eps, opt_x)
    elif algo == "cheby":
        ret = sdd_local_cheby(n, indptr, indices, degree, b, alpha, eps, opt_x)
    else:
        raise ValueError(f"unknown algorithm: {algo!r}")
    # sdd_local_appr returns pi; every other solver returns x = D^-1/2 pi
    x_hat = ret[0] / np.sqrt(degree) if algo == "appr" else ret[0]
    return ret, x_hat


def main():
    ap = argparse.ArgumentParser(description="eps sweep, l1 error + operations")
    ap.add_argument("--dataset", default="com-dblp")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--num-sources", type=int, default=10)
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument(
        "--min-deg", type=int, default=1, help="only sample sources with degree >= this"
    )
    ap.add_argument("--algos", default=",".join(ALGOS))
    ap.add_argument("--mults", default="10,1,0.1,0.01,0.001,0.0001", help="eps = mult / n")
    ap.add_argument(
        "--max-ops",
        type=float,
        default=2e9,
        help="skip a solver at tighter eps once it exceeds this",
    )
    a = ap.parse_args()

    graph = load_graph(a.dataset)
    n, m = graph.n, graph.m
    indptr, indices, degree = graph.indptr, graph.indices, graph.degree
    sq = np.sqrt(degree)
    algos = [x for x in a.algos.split(",") if x]
    mults = [float(x) for x in a.mults.split(",")]

    sources = graph.sample_sources(
        count=a.num_sources,
        seed=a.seed,
        min_degree=a.min_deg,
    )
    k = len(sources)

    print(
        f"\n{a.dataset}: n={n:,} m={m:,} alpha={a.alpha}  "
        f"{k} sources (seed={a.seed}, min-deg={a.min_deg})"
    )
    print(f"sources: {sources}\n")
    # warm-up so numba JIT is not billed to the first timed run
    b0 = np.zeros(n, dtype=np.float64)
    b0[sources[0]] = 2.0 * a.alpha / ((1.0 + a.alpha) * sq[sources[0]])
    s0 = np.zeros(n, dtype=np.float64)
    s0[sources[0]] = 1.0
    opt0 = sdd_get_opt(n, indptr, indices, degree, sources[0], a.alpha, 1e-10)
    for algo in algos:
        run_one(algo, n, indptr, indices, degree, b0, s0, a.alpha, 1.0, opt0)

    # collect per (mult, algo): list of opers / l1 over sources, and win count
    ops_all = {(mu, al): [] for mu in mults for al in algos}
    l1_all = {(mu, al): [] for mu in mults for al in algos}
    wins = {(mu, al): 0 for mu in mults for al in algos}

    for src in sources:
        b = np.zeros(n, dtype=np.float64)
        b[src] = 2.0 * a.alpha / ((1.0 + a.alpha) * sq[src])
        s = np.zeros(n, dtype=np.float64)
        s[src] = 1.0
        opt_x = sdd_get_opt(n, indptr, indices, degree, src, a.alpha, 1e-10)
        t0 = time.time()
        over = set()
        for mu in mults:
            eps = mu / n
            row = {}
            for algo in algos:
                if algo in over:
                    continue
                ret, _ = run_one(algo, n, indptr, indices, degree, b, s, a.alpha, eps, opt_x)
                opers = float(np.sum(ret[3]))
                errs = ret[2]
                l1 = float(errs[-1]) if len(errs) else float("nan")
                ops_all[(mu, algo)].append(opers)
                l1_all[(mu, algo)].append(l1)
                row[algo] = opers
                if opers > a.max_ops:
                    over.add(algo)
            if row:
                wins[(mu, min(row, key=row.get))] += 1
        print(
            f"  source {src:>8} (deg {int(degree[src]):>4})  done in {time.time() - t0:5.1f}s",
            flush=True,
        )

    med_ops = {k2: (float(np.median(v)) if v else None) for k2, v in ops_all.items()}
    med_l1 = {k2: (float(np.median(v)) if v else None) for k2, v in l1_all.items()}
    best = {
        mu: min(
            (al for al in algos if med_ops[(mu, al)] is not None), key=lambda al: med_ops[(mu, al)]
        )
        for mu in mults
    }
    best_keys = {(mu, best[mu]) for mu in mults}

    _pivot(
        f"median operations over {k} sources  ('*' = fewest at that eps)",
        med_ops,
        mults,
        algos,
        lambda v: f"{v:,.0f}",
        best=best_keys,
    )
    _pivot(f"median l1 error over {k} sources", med_l1, mults, algos, lambda v: f"{v:.3e}")
    _pivot(
        f"wins  (# of {k} sources with the fewest opers)",
        wins,
        mults,
        algos,
        lambda v: f"{v:d}",
        best=best_keys,
    )

    print(f"\nlowest median opers per eps (alpha={a.alpha}):")
    for mu in mults:
        lab = "1/n" if mu == 1 else f"{mu:g}/n"
        print(
            f"  eps={lab:>8}  ->  {best[mu]:>8}  "
            f"({med_ops[(mu, best[mu])]:,.0f} median opers, "
            f"{wins[(mu, best[mu])]}/{k} sources)"
        )
    from collections import Counter

    tally = Counter(best.values())
    top, cnt = tally.most_common(1)[0]
    print(
        f"\noverall: {top} is cheapest at {cnt}/{len(mults)} eps levels "
        f"on {a.dataset} at alpha={a.alpha}."
    )


def _pivot(title, table, mults, algos, fmt, best=None):
    """Box-drawn eps x algo matrix; keys in `best` are prefixed with '*'."""
    best = best or set()

    def label(mult):
        return "1/n" if mult == 1 else f"{mult:g}/n"

    def cell(m, al):
        v = table.get((m, al))
        if v is None:
            return "--"
        return ("*" if (m, al) in best else "") + fmt(v)

    cells = [[cell(m, al) for al in algos] for m in mults]
    w0 = max([len("eps")] + [len(label(m)) for m in mults]) + 2
    ws = [max([len(al)] + [len(r[j]) for r in cells]) + 2 for j, al in enumerate(algos)]

    def rule(left, middle, right):
        return left + "─" * w0 + "".join(middle + "─" * w for w in ws) + right

    print(f"\n{title}")
    print(rule("┌", "┬", "┐"))
    print("│" + "eps".center(w0) + "".join("│" + al.center(w) for al, w in zip(algos, ws)) + "│")
    for i, m in enumerate(mults):
        print(rule("├", "┼", "┤"))
        print(
            "│"
            + label(m).ljust(w0 - 1).rjust(w0)
            + "".join("│" + c.rjust(w - 1).ljust(w) for c, w in zip(cells[i], ws))
            + "│"
        )
    print(rule("└", "┴", "┘"))


if __name__ == "__main__":
    main()
