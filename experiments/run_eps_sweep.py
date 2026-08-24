"""Sweep eps over several random sources and report which local solver is
cheapest at each accuracy level.

    uv run python -m experiments.run_eps_sweep \
        --data-dir /path/to/graphs \
        --dataset com-dblp --alpha 0.05 --num-sources 10

For eps in {1/n, 0.1/n, 0.01/n, 0.001/n, 0.0001/n}, across `--num-sources`
seeded-random source nodes, it reports per (eps, solver):
  opers    total nodes accessed with multiplicity (sum of `opers`), MEDIAN
           over the sources; the row-minimum is marked with a leading '*'
  l1-err   the solver's OWN `errs[-1]` = ||xt/sqrt(d) - opt_x||_1, MEDIAN
  wins     how many sources that solver had the FEWEST opers on, at that eps

l1-err note: all seven solver configurations here scale to x-coordinates before comparing, so
their `errs` are mutually consistent.

Comparability of `opers` across solvers.  The active-vertex threshold `eps_vec` is
  appr          eps * d          (indicator residual; Lemma 2.1)
  gd sor hb cheby  eps * alpha * d  (implemented gradient-residual threshold)
The six non-APPR solver configurations therefore share one intended threshold inside this
script, but an empty active frontier is not automatically a residual certificate
for every legacy accelerated implementation.  Each run checks the returned
residual, and rankings require every sampled source to pass.  This is still not
a project-wide accuracy convention: the canonical residual decision remains
open, and no conversion to APPR's looser certificate has been adopted.  All
cross-method rankings printed here are exploratory.  A definitive equal-accuracy
comparison requires a separate, documented calibration workflow.

Cost warning: APPR is O(1/(alpha*eps)), so tightening eps by 10x costs it ~10x
more work, while the accelerated methods grow far more slowly.  At 1e-4/n APPR
needs ~1e11 operations.  --max-ops skips a solver at all tighter eps once it
exceeds the budget (its cost is monotone in 1/eps, so this never skips a run
that would have been cheap).
"""

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from experiments.result_schema import make_result_bundle, write_result_bundle
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
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results" / "raw"
APPR_STOPPING_RULE = (
    "terminate when the FIFO active queue is empty; a vertex u is (re)enqueued whenever "
    "r[u] >= eps * d[u]"
)
GD_STOPPING_RULE = (
    "terminate when the next active frontier is empty; after processing u, a neighboring "
    "vertex v is activated whenever r[v] >= eps * alpha * d[v]"
)
SIGNED_STOPPING_RULE = (
    "terminate when the next active queue/frontier is empty; after processing u, only "
    "neighboring vertices v with abs(r[v]) >= eps * alpha * d[v] are activated, and u is "
    "not retested solely because its own residual changed"
)
WORK_UNIT = "degree-weighted adjacency-list entries scanned"


def _stopping_rule(algo: str) -> str:
    if algo == "appr":
        return APPR_STOPPING_RULE
    if algo == "gd":
        return GD_STOPPING_RULE
    return SIGNED_STOPPING_RULE


def _solver_parameters(algo: str, *, alpha: float, eps: float, n: int) -> dict:
    if algo == "appr":
        return {"ordering": "fifo"}
    if algo == "sor":
        return {"omega": 1.0}
    if algo == "opt-sor":
        return {"omega": float(opt_omega(alpha)), "omega_rule": "global spectral optimum"}
    if algo == "adp-sor":
        return {
            "omega": float(adaptive_omega(alpha, eps, n)),
            "omega_rule": "legacy adaptive heuristic",
        }
    return {}


def _certificate_metrics(
    algo: str,
    residual: np.ndarray,
    degree: np.ndarray,
    *,
    alpha: float,
    eps: float,
) -> tuple[bool, float]:
    """Evaluate the intended coordinate residual certificate after termination."""
    threshold = eps * degree if algo == "appr" else eps * alpha * degree
    magnitude = residual if algo == "gd" or algo == "appr" else np.abs(residual)
    normalized = np.divide(
        magnitude,
        threshold,
        out=np.where(magnitude == 0.0, 0.0, np.inf),
        where=threshold > 0.0,
    )
    return bool(np.all(magnitude < threshold)), float(np.max(normalized))


def _result_record(
    *,
    dataset: str,
    source: int,
    alpha: float,
    eps: float,
    random_seed: int,
    algo: str,
    n: int,
    status: str,
    edge_operations: float | None,
    local_iterations: int | None,
    runtime_seconds: float | None,
    l1_error: float | None,
    target_certificate_achieved: bool | None,
    terminal_max_normalized_residual: float | None,
) -> dict:
    return {
        "graph": dataset,
        "alpha": alpha,
        "epsilon": eps,
        "epsilon_name": "eps_appr" if algo == "appr" else "eps_gradient_residual",
        "random_seed": random_seed,
        "stopping_rule": _stopping_rule(algo),
        "solver": algo,
        "solver_parameters": _solver_parameters(algo, alpha=alpha, eps=eps, n=n),
        "source": source,
        "status": status,
        "work": {
            "edge_operations": edge_operations,
            "local_inner_iterations": local_iterations,
            "outer_acceleration_iterations": 0,
            "runtime_seconds": runtime_seconds,
            "unit": WORK_UNIT,
        },
        "metrics": {
            "l1_error": l1_error,
            "target_certificate": (
                "r[u] < eps * d[u] for every vertex u"
                if algo == "appr"
                else "r[u] < eps * alpha * d[u] for every vertex u"
                if algo == "gd"
                else "abs(r[u]) < eps * alpha * d[u] for every vertex u"
            ),
            "target_certificate_achieved": target_certificate_achieved,
            "terminal_max_normalized_residual": terminal_max_normalized_residual,
            "comparison_status": "exploratory; project-wide residual conversion unresolved",
        },
    }


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
    ap.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="local graph root created by the explicit data-acquisition command",
    )
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
    ap.add_argument(
        "--output",
        type=Path,
        help="structured JSON output (default: results/raw/eps-sweep-<dataset>.json)",
    )
    a = ap.parse_args()

    graph = load_graph(a.dataset, data_dir=a.data_dir)
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
    records = []

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
                    records.append(
                        _result_record(
                            dataset=a.dataset,
                            source=int(src),
                            alpha=a.alpha,
                            eps=eps,
                            random_seed=a.seed,
                            algo=algo,
                            n=n,
                            status="skipped_after_operation_budget",
                            edge_operations=None,
                            local_iterations=None,
                            runtime_seconds=None,
                            l1_error=None,
                            target_certificate_achieved=None,
                            terminal_max_normalized_residual=None,
                        )
                    )
                    continue
                ret, _ = run_one(algo, n, indptr, indices, degree, b, s, a.alpha, eps, opt_x)
                opers = float(np.sum(ret[3]))
                errs = ret[2]
                l1 = float(errs[-1]) if len(errs) else float("nan")
                certificate_achieved, max_normalized_residual = _certificate_metrics(
                    algo,
                    np.asarray(ret[1]),
                    degree,
                    alpha=a.alpha,
                    eps=eps,
                )
                finite_run = bool(
                    np.isfinite(opers) and np.isfinite(l1) and np.isfinite(float(ret[4]))
                )
                if not finite_run:
                    status = "unstable"
                elif certificate_achieved:
                    status = "completed"
                else:
                    status = "completed_without_target_certificate"
                if status == "completed":
                    ops_all[(mu, algo)].append(opers)
                    l1_all[(mu, algo)].append(l1)
                    row[algo] = opers
                records.append(
                    _result_record(
                        dataset=a.dataset,
                        source=int(src),
                        alpha=a.alpha,
                        eps=eps,
                        random_seed=a.seed,
                        algo=algo,
                        n=n,
                        status=status,
                        edge_operations=opers if np.isfinite(opers) else None,
                        local_iterations=len(ret[3]),
                        runtime_seconds=float(ret[4]) if np.isfinite(float(ret[4])) else None,
                        l1_error=l1 if np.isfinite(l1) else None,
                        target_certificate_achieved=certificate_achieved,
                        terminal_max_normalized_residual=(
                            max_normalized_residual
                            if np.isfinite(max_normalized_residual)
                            else None
                        ),
                    )
                )
                if np.isfinite(opers) and opers > a.max_ops:
                    over.add(algo)
            if row:
                wins[(mu, min(row, key=row.get))] += 1
        print(
            f"  source {src:>8} (deg {int(degree[src]):>4})  done in {time.time() - t0:5.1f}s",
            flush=True,
        )

    med_ops = {k2: (float(np.median(v)) if v else None) for k2, v in ops_all.items()}
    med_l1 = {k2: (float(np.median(v)) if v else None) for k2, v in l1_all.items()}
    best = {}
    for mu in mults:
        eligible = [al for al in algos if len(ops_all[(mu, al)]) == k]
        if eligible:
            best[mu] = min(eligible, key=lambda al: med_ops[(mu, al)])
    best_keys = set(best.items())

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
        if mu in best:
            print(
                f"  eps={lab:>8}  ->  {best[mu]:>8}  "
                f"({med_ops[(mu, best[mu])]:,.0f} median opers, "
                f"{wins[(mu, best[mu])]}/{k} sources)"
            )
        else:
            print(f"  eps={lab:>8}  ->  no solver certified on all {k} sources")
    from collections import Counter

    tally = Counter(best.values())
    if tally:
        top, cnt = tally.most_common(1)[0]
        print(
            f"\nexploratory ranking among certified runs: {top} is cheapest at "
            f"{cnt}/{len(best)} rankable eps levels on {a.dataset} at alpha={a.alpha}."
        )
    else:
        print("\nno eps level had a solver certified on every sampled source")

    output_path = a.output or RESULTS_DIR / f"eps-sweep-{a.dataset}.json"
    bundle = make_result_bundle(
        experiment="local-solver-epsilon-sweep",
        config={
            "dataset": a.dataset,
            "nodes": n,
            "edges": m,
            "alpha": a.alpha,
            "num_sources": a.num_sources,
            "random_seed": a.seed,
            "minimum_source_degree": a.min_deg,
            "solvers": algos,
            "epsilon_multipliers_over_n": mults,
            "max_operations_budget": a.max_ops,
            "comparison_status": "exploratory; canonical residual conversion unresolved",
            "reference_solution": {
                "solver": "src.baselines.sdd_solver.sdd_get_opt",
                "solver_epsilon": 1.0e-10,
                "reported_error_norm": "l1",
                "reported_error_coordinates": "x = D^(-1/2) pi",
                "appr_output_conversion": "pi / sqrt(degree)",
            },
        },
        records=records,
        argv=sys.argv,
    )
    write_result_bundle(output_path, bundle)
    print(f"structured results: {output_path}")


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
