"""Run the deterministic, offline APPR reproduction smoke experiment."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

from experiments.result_schema import make_result_bundle, write_result_bundle
from src.baselines.appr import approximate_pagerank
from src.synthetic_graphs import star_graph

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "raw" / "reproduction_smoke.json"

ALPHA = 1.0 / 4.0
EPS_APPR = 1.0 / 32.0
RANDOM_SEED = 17
SOURCE = 0
ORDERING = "fifo"
STOPPING_RULE = (
    "a vertex u is active while r[u] >= eps_appr * d[u]; terminate when "
    "r[u] < eps_appr * d[u] for every vertex u, evaluated after every push"
)
WORK_UNIT = "degree-weighted adjacency-list work W = sum_t d[u_t]"


def run_smoke() -> tuple[dict[str, object], dict[str, object]]:
    """Run one center-seeded hard-star case and return config plus result record."""
    leaf_count = math.floor(1.0 / (8.0 * EPS_APPR))
    graph = star_graph(leaf_count)
    result = approximate_pagerank(
        graph,
        SOURCE,
        alpha=ALPHA,
        eps_appr=EPS_APPR,
        ordering=ORDERING,
        random_seed=RANDOM_SEED,
    )

    lower_bound = 3.0 / (128.0 * ALPHA * EPS_APPR)
    upper_bound = 1.0 / (ALPHA * EPS_APPR)
    lower_bound_verified = bool(result.work > lower_bound)
    upper_bound_verified = bool(result.work <= upper_bound)
    terminal_residual_verified = bool(np.all(result.residual < EPS_APPR * graph.degree))
    terminal_mass = float(result.estimate.sum() + result.residual.sum())
    mass_conservation_verified = math.isclose(
        terminal_mass,
        result.initial_mass,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )

    failed_checks = [
        name
        for name, passed in (
            ("strict star lower bound", lower_bound_verified),
            ("APPR upper bound", upper_bound_verified),
            ("terminal residual condition", terminal_residual_verified),
            ("mass conservation", mass_conservation_verified),
        )
        if not passed
    ]
    if failed_checks:
        raise AssertionError(f"APPR reproduction smoke failed: {', '.join(failed_checks)}")

    graph_metadata = {
        "name": graph.name,
        "kind": "center-seeded star",
        "nodes": graph.n,
        "edges": graph.m,
        "leaf_count": leaf_count,
    }
    solver_parameters = {
        "ordering": ORDERING,
        "max_pushes": None,
    }
    config = {
        "graph": graph_metadata,
        "alpha": ALPHA,
        "epsilon": EPS_APPR,
        "epsilon_name": "eps_appr",
        "random_seed": RANDOM_SEED,
        "source": SOURCE,
        "solver": "src.baselines.appr.approximate_pagerank",
        "solver_parameters": solver_parameters,
        "stopping_rule": STOPPING_RULE,
        "theorem_regime": "0 < eps_appr <= 1/16",
    }
    record = {
        "graph": graph.name,
        "alpha": ALPHA,
        "epsilon": EPS_APPR,
        "epsilon_name": "eps_appr",
        "random_seed": RANDOM_SEED,
        "stopping_rule": STOPPING_RULE,
        "solver": "src.baselines.appr.approximate_pagerank",
        "solver_parameters": solver_parameters,
        "source": SOURCE,
        "status": "passed",
        "work": {
            "outer_acceleration_iterations": 0,
            "local_inner_iterations": int(result.pushes),
            "edge_operations": float(result.work),
            "unit": WORK_UNIT,
        },
        "metrics": {
            "graph_kind": graph_metadata["kind"],
            "nodes": graph.n,
            "edges": graph.m,
            "leaf_count": leaf_count,
            "pushes": int(result.pushes),
            "terminal_mass": terminal_mass,
            "terminal_max_residual_ratio": float(np.max(result.residual / graph.degree)),
            "terminal_residual_verified": terminal_residual_verified,
            "mass_conservation_verified": mass_conservation_verified,
            "star_lower_bound": lower_bound,
            "star_lower_bound_verified": lower_bound_verified,
            "appr_upper_bound": upper_bound,
            "appr_upper_bound_verified": upper_bound_verified,
            "scaled_work": float(ALPHA * EPS_APPR * result.work),
        },
    }
    return config, record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    config, record = run_smoke()
    payload = make_result_bundle(
        experiment="deterministic offline APPR hard-star reproduction smoke",
        config=config,
        records=[record],
    )
    write_result_bundle(args.output, payload)

    metrics = record["metrics"]
    work = record["work"]
    print(
        f"APPR smoke passed on {record['graph']}: "
        f"{work['edge_operations']:.0f} edge operations, "
        f"{metrics['pushes']} pushes; wrote {args.output}"
    )


if __name__ == "__main__":
    main()
