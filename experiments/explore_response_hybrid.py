"""Compare exact-response, mixed, and iterative-frontier reference backends."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from experiments.explore_evolving_cg import synthetic_cases
from experiments.result_schema import make_result_bundle, write_result_bundle
from src.hybrid_solver_codex.evolving_cg import pagerank_matrix, pagerank_rhs
from src.hybrid_solver_codex.response_hybrid import dense_response_frontier_hybrid

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "raw" / "response-hybrid-synthetic.json"
STOPPING_RULE = (
    "terminate only after dense reference verification of r = b - Qx and "
    "max_i |r[i]| / sqrt(d[i]) <= alpha * eps_ppr"
)
WORK_UNIT = (
    "degree-weighted adjacency entries in verifier Q products; dense response arithmetic, "
    "global boundary reads, and materialization writes are separate metrics"
)


def run_exploration(
    *,
    alpha: float,
    eps_ppr: float,
    random_seed: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the three inverse-realization endpoints on deterministic graphs."""
    variants = (
        ("dense_response_every_batch", 1.0, 1.0, False),
        ("dense_response_frontier_hybrid", 2.0, 2.0, True),
        ("dense_anchor_iterative_frontier", "never", np.inf, False),
    )
    cases = synthetic_cases(random_seed)
    records: list[dict[str, object]] = []

    for graph, source, graph_kind in cases:
        matrix = pagerank_matrix(graph, alpha)
        right_hand_side = pagerank_rhs(graph, alpha, source)
        direct_solution = spsolve(matrix, right_hand_side)
        for solver_name, recorded_factor, numerical_factor, probe_first in variants:
            result = dense_response_frontier_hybrid(
                graph,
                alpha=alpha,
                source=source,
                eps_ppr=eps_ppr,
                rebuild_volume_factor=numerical_factor,
                probe_frontier_before_rebuild=probe_first,
            )
            scaled_residual = float(np.max(np.abs(result.residual) / np.sqrt(graph.degree)))
            scaled_error = float(
                np.max(np.abs(result.solution - direct_solution) / np.sqrt(graph.degree))
            )
            records.append(
                {
                    "graph": graph.name,
                    "alpha": alpha,
                    "epsilon": eps_ppr,
                    "epsilon_name": "eps_ppr_note_scoped",
                    "random_seed": random_seed,
                    "stopping_rule": STOPPING_RULE,
                    "solver": solver_name,
                    "solver_parameters": {
                        "rebuild_volume_factor": recorded_factor,
                        "probe_frontier_before_rebuild": probe_first,
                        "inner_tolerance_fraction": 0.25,
                        "response_representation": "exact dense principal inverse",
                        "boundary_reporter": "global dense reference scan",
                    },
                    "source": source,
                    "status": (
                        "completed" if result.certified else "completed_without_target_certificate"
                    ),
                    "work": {
                        "outer_acceleration_iterations": result.outer_restarts,
                        "local_inner_iterations": result.local_inner_iterations,
                        "edge_operations": result.edge_operations,
                        "unit": WORK_UNIT,
                    },
                    "metrics": {
                        "graph_kind": graph_kind,
                        "nodes": graph.n,
                        "edges": graph.m,
                        "degree_volume": float(np.sum(graph.degree)),
                        "certified": result.certified,
                        "termination_reason": result.termination_reason,
                        "terminal_scaled_residual": scaled_residual,
                        "direct_scaled_error": scaled_error,
                        "explored_vertices": int(result.explored_vertices.size),
                        "explored_volume": float(np.sum(graph.degree[result.explored_vertices])),
                        "support_epochs": len(result.trace.anchor_size),
                        "response_updates": result.work.response_updates,
                        "boundary_coordinate_reads": result.work.boundary_coordinate_reads,
                        "response_update_dense_flops": (result.work.response_update_dense_flops),
                        "schur_build_dense_flops": result.work.schur_build_dense_flops,
                        "frontier_iteration_dense_flops": (
                            result.work.frontier_iteration_dense_flops
                        ),
                        "active_materialization_writes": (
                            result.work.active_materialization_writes
                        ),
                        "final_output_writes": result.work.final_output_writes,
                        "peak_anchor_volume": max(result.trace.anchor_volume),
                        "peak_frontier_volume": max(result.trace.frontier_volume),
                        "anchor_volume_trajectory": list(result.trace.anchor_volume),
                        "frontier_volume_trajectory": list(result.trace.frontier_volume),
                        "frontier_iteration_trajectory": list(result.trace.frontier_iterations),
                        "response_rebuild_trajectory": list(result.trace.response_rebuilt),
                        "warm_start_trajectory": list(result.trace.frontier_warm_started),
                    },
                }
            )

    config: dict[str, object] = {
        "alpha": alpha,
        "epsilon": eps_ppr,
        "epsilon_name": "eps_ppr_note_scoped",
        "random_seed": random_seed,
        "stopping_rule": STOPPING_RULE,
        "work_unit": WORK_UNIT,
        "graphs": [graph.name for graph, _, _ in cases],
        "reference_solver": "scipy.sparse.linalg.spsolve",
        "scope_warning": (
            "the backend materializes Q, reads every boundary coordinate, and stores dense "
            "inverses; results validate identities and switching but not locality"
        ),
    }
    return config, records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--eps-ppr", type=float, default=1.0e-7)
    parser.add_argument("--random-seed", type=int, default=7)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    config, records = run_exploration(
        alpha=args.alpha,
        eps_ppr=args.eps_ppr,
        random_seed=args.random_seed,
    )
    payload = make_result_bundle(
        experiment="dense response--iterative hybrid reference comparison",
        config=config,
        records=records,
    )
    write_result_bundle(args.output, payload)

    print(f"wrote {len(records)} records to {args.output}")
    for record in records:
        work = record["work"]
        metrics = record["metrics"]
        print(
            f"{record['graph']:>20} {record['solver']:>32}: "
            f"Q-work={work['edge_operations']:>9.0f}, "
            f"frontier-CG={work['local_inner_iterations']:>4}, "
            f"response-updates={metrics['response_updates']:>3}, "
            f"response-flops={metrics['response_update_dense_flops']:>12.0f}"
        )


if __name__ == "__main__":
    main()
