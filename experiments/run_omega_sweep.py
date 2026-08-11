"""Sweep the SOR relaxation parameter omega at loose eps.

Hypothesis (author): the "optimal" omega = 2(1+a)/(1+sqrt(a))^2 is derived from
the GLOBAL graph's spectral radius.  At loose eps the push only touches a small
LOCAL subgraph, whose conditioning is better, so the locally-optimal omega
should be SMALLER (nearer 1) than the global one -- and opt-sor's fixed 1.40
over-relaxes.

For each eps this runs sdd_local_sor at a grid of omega in [1, 2) over several
seeded sources and reports the median operations, marking the theoretical
optimum and the empirical best.  omega >= 2 diverges, so the grid stops below
that; any run whose l1 error blows up is flagged UNSTABLE. An omega is excluded
from the empirical-best comparison if any source is unstable or fails the
intended signed residual certificate after the active queue empties.

    uv run python -m experiments.run_omega_sweep \
        --dataset com-dblp --alpha 0.05
"""

import argparse
import sys
from pathlib import Path

import numpy as np

from experiments.result_schema import make_result_bundle, write_result_bundle
from src.baselines.sdd_solver import sdd_get_opt, sdd_local_sor
from src.graphs import load_graph

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results" / "raw"
STOPPING_RULE = (
    "terminate when the active queue contains only the local-round marker after at least one "
    "recorded round; after processing u, only neighboring vertices v with abs(r[v]) >= "
    "eps * alpha * d[v] are enqueued, and u is not retested solely because its own residual "
    "changed"
)
WORK_UNIT = "degree-weighted adjacency-list entries scanned"


def _certificate_metrics(
    residual: np.ndarray,
    degree: np.ndarray,
    *,
    alpha: float,
    eps: float,
) -> tuple[bool, float]:
    """Evaluate the intended signed coordinate residual certificate."""
    threshold = eps * alpha * degree
    magnitude = np.abs(residual)
    normalized = np.divide(
        magnitude,
        threshold,
        out=np.where(magnitude == 0.0, 0.0, np.inf),
        where=threshold > 0.0,
    )
    return bool(np.all(magnitude < threshold)), float(np.max(normalized))


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
    ap.add_argument(
        "--output",
        type=Path,
        help="structured JSON output (default: results/raw/omega-sweep-<dataset>.json)",
    )
    a = ap.parse_args()

    graph = load_graph(a.dataset)
    n, m = graph.n, graph.m
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

    records = []
    for mult in mults:
        eps = mult / n
        lab = "1/n" if mult == 1 else f"{mult:g}/n"
        print(f"\n===== eps = {lab}  ({eps:.3e}) =====")
        print(f"{'omega':>7} {'median_opers':>14} {'median_l1':>12}  note")
        rows = []
        for w in omegas:
            ops, l1s, unstable, certified = [], [], False, True
            for src in sources:
                r = sdd_local_sor(
                    n, indptr, indices, degree, src_b[src], a.alpha, eps, w, src_opt[src]
                )
                edge_operations = float(np.sum(r[3]))
                runtime_seconds = float(r[4])
                ops.append(edge_operations)
                le = float(r[2][-1]) if len(r[2]) else float("nan")
                l1s.append(le)
                certificate_achieved, max_normalized_residual = _certificate_metrics(
                    np.asarray(r[1]),
                    degree,
                    alpha=a.alpha,
                    eps=eps,
                )
                run_unstable = bool(
                    not np.isfinite(le)
                    or le > 10.0
                    or not np.isfinite(edge_operations)
                    or not np.isfinite(runtime_seconds)
                )
                if run_unstable:
                    status = "unstable"
                elif certificate_achieved:
                    status = "completed"
                else:
                    status = "completed_without_target_certificate"
                records.append(
                    {
                        "graph": a.dataset,
                        "alpha": a.alpha,
                        "epsilon": eps,
                        "epsilon_name": "eps_gradient_residual",
                        "random_seed": a.seed,
                        "stopping_rule": STOPPING_RULE,
                        "solver": "sor",
                        "solver_parameters": {
                            "omega": float(w),
                            "theoretical_global_omega": float(opt_omega),
                        },
                        "source": int(src),
                        "status": status,
                        "work": {
                            "edge_operations": (
                                edge_operations if np.isfinite(edge_operations) else None
                            ),
                            "local_inner_iterations": len(r[3]),
                            "outer_acceleration_iterations": 0,
                            "runtime_seconds": (
                                runtime_seconds if np.isfinite(runtime_seconds) else None
                            ),
                            "unit": WORK_UNIT,
                        },
                        "metrics": {
                            "l1_error": le if np.isfinite(le) else None,
                            "target_certificate": (
                                "abs(r[u]) < eps * alpha * d[u] for every vertex u"
                            ),
                            "target_certificate_achieved": certificate_achieved,
                            "terminal_max_normalized_residual": (
                                max_normalized_residual
                                if np.isfinite(max_normalized_residual)
                                else None
                            ),
                            "comparison_status": (
                                "exploratory; canonical residual convention unresolved"
                            ),
                        },
                    }
                )
                if run_unstable:
                    unstable = True
                if not certificate_achieved:
                    certified = False
            mo = float(np.median(ops))
            ml = float(np.median(l1s))
            rows.append((w, mo, ml, unstable, certified))

        stable = [r for r in rows if not r[3] and r[4]]
        best_w = min(stable, key=lambda r: r[1])[0] if stable else None
        for w, mo, ml, unstable, certified in rows:
            note = ""
            if w == near_opt:
                note = f"<- theoretical opt ({opt_omega:.4f})"
            if w == best_w:
                note = ("best empirical  " + note).strip()
            if unstable:
                note = "UNSTABLE (l1 blew up)"
            elif not certified:
                note = "UNCERTIFIED (target residual threshold not achieved)"
            star = "*" if w == best_w else " "
            print(f"{star}{w:>6.2f} {mo:>14,.0f} {ml:>12.3e}  {note}")

        if best_w is not None:
            bo = min(stable, key=lambda r: r[1])[1]
            msg = f"  -> best omega={best_w:.2f} ({bo:,.0f} median opers)"
            theoretical_row = next((r for r in stable if r[0] == near_opt), None)
            if theoretical_row is not None:
                to = theoretical_row[1]
                msg += f"  vs theoretical {opt_omega:.2f} ({to:,.0f}) = {to / bo:.2f}x"
            else:
                msg += f"  vs theoretical {opt_omega:.2f} = N/A (uncertified or unstable)"
            print(msg)

    output_path = a.output or RESULTS_DIR / f"omega-sweep-{a.dataset}.json"
    bundle = make_result_bundle(
        experiment="local-sor-omega-sweep",
        config={
            "dataset": a.dataset,
            "nodes": n,
            "edges": m,
            "alpha": a.alpha,
            "num_sources": a.num_sources,
            "random_seed": a.seed,
            "minimum_source_degree": a.min_deg,
            "epsilon_multipliers_over_n": mults,
            "omega_range": {
                "low": a.omega_lo,
                "high": a.omega_hi,
                "step": a.omega_step,
            },
            "evaluated_omegas": [float(omega) for omega in omegas],
            "theoretical_global_omega": float(opt_omega),
            "comparison_status": "exploratory; canonical residual convention unresolved",
            "reference_solution": {
                "solver": "src.baselines.sdd_solver.sdd_get_opt",
                "solver_epsilon": 1.0e-10,
                "reported_error_norm": "l1",
                "reported_error_coordinates": "x = D^(-1/2) pi",
            },
        },
        records=records,
        argv=sys.argv,
    )
    write_result_bundle(output_path, bundle)
    print(f"structured results: {output_path}")


if __name__ == "__main__":
    main()
