"""Compare finite-propagation CG with restarted evolving-set CG offline."""

from __future__ import annotations

import argparse
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.sparse.linalg import spsolve

from experiments.result_schema import make_result_bundle, write_result_bundle
from src.graphs import GraphData
from src.hybrid_solver_codex.evolving_cg import (
    CGTrace,
    EvolvingCGTrace,
    frontier_sparse_cg,
    pagerank_matrix,
    pagerank_rhs,
    restarted_evolving_set_cg,
)
from src.synthetic_graphs import graph_from_edges, path_graph, spider_graph, star_graph

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "raw" / "evolving-cg-synthetic.json"
STOPPING_RULE = (
    "terminate only after recomputing r = b - Qx and verifying "
    "max_i |r[i]| / sqrt(d[i]) <= alpha * eps_ppr"
)
WORK_UNIT = "degree-weighted adjacency-list entries scanned by local Q products"


def _binary_tree(node_count: int) -> GraphData:
    edges = [((node - 1) // 2, node) for node in range(1, node_count)]
    return graph_from_edges(f"binary-tree-{node_count}", node_count, edges)


def _random_regular(node_count: int, degree: int, random_seed: int) -> GraphData:
    graph = nx.random_regular_graph(degree, node_count, seed=random_seed)
    edges = [(int(first), int(second)) for first, second in graph.edges()]
    return graph_from_edges(f"regular-{degree}-{node_count}", node_count, edges)


def synthetic_cases(random_seed: int) -> list[tuple[GraphData, int, str]]:
    """Return deterministic slow-growth, branching, and fast-growth cases."""
    return [
        (path_graph(511), 255, "center-seeded path"),
        (star_graph(510), 0, "center-seeded star"),
        (_binary_tree(511), 0, "root-seeded binary tree"),
        (spider_graph(8, 64), 0, "center-seeded long spider"),
        (_random_regular(512, 4, random_seed), 0, "seeded random 4-regular graph"),
    ]


def run_exploration(
    *,
    alpha: float,
    eps_ppr: float,
    random_seed: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run all synthetic cases and return schema-ready records."""
    records: list[dict[str, object]] = []
    cases = synthetic_cases(random_seed)
    for graph, source, graph_kind in cases:
        matrix = pagerank_matrix(graph, alpha)
        right_hand_side = pagerank_rhs(graph, alpha, source)
        direct_solution = spsolve(matrix, right_hand_side)
        for solver_name, solver, parameters in (
            (
                "frontier_sparse_cg",
                frontier_sparse_cg,
                {"direction_thresholding": False, "support_change_policy": "exact CG"},
            ),
            (
                "restarted_evolving_set_cg",
                restarted_evolving_set_cg,
                {
                    "inner_tolerance_fraction": 0.25,
                    "support_change_policy": "batch boundary violations then restart",
                },
            ),
        ):
            result = solver(
                graph,
                alpha=alpha,
                source=source,
                eps_ppr=eps_ppr,
            )
            scaled_residual = float(np.max(np.abs(result.residual) / np.sqrt(graph.degree)))
            scaled_error = float(
                np.max(np.abs(result.solution - direct_solution) / np.sqrt(graph.degree))
            )
            trace_metrics: dict[str, object]
            if isinstance(result.trace, CGTrace):
                trace_metrics = {
                    "max_direction_support": max(result.trace.direction_support_size),
                    "max_direction_volume": max(result.trace.direction_volume),
                    "support_trajectory": list(result.trace.direction_support_size),
                }
            elif isinstance(result.trace, EvolvingCGTrace):
                trace_metrics = {
                    "max_active_size": max(result.trace.active_size),
                    "max_active_volume": max(result.trace.active_volume),
                    "active_size_trajectory": list(result.trace.active_size),
                    "added_size_trajectory": list(result.trace.added_size),
                }
            else:  # pragma: no cover - exhaustiveness guard for future trace types
                raise TypeError(f"unknown trace type {type(result.trace)!r}")

            records.append(
                {
                    "graph": graph.name,
                    "alpha": alpha,
                    "epsilon": eps_ppr,
                    "epsilon_name": "eps_ppr_note_scoped",
                    "random_seed": random_seed,
                    "stopping_rule": STOPPING_RULE,
                    "solver": solver_name,
                    "solver_parameters": parameters,
                    "source": source,
                    "status": "completed"
                    if result.certified
                    else "completed_without_target_certificate",
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
                        "outer_restarts": result.outer_restarts,
                        **trace_metrics,
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
        experiment="synthetic evolving-support conjugate-gradient exploration",
        config=config,
        records=records,
    )
    write_result_bundle(args.output, payload)

    print(f"wrote {len(records)} records to {args.output}")
    for record in records:
        work = record["work"]
        metrics = record["metrics"]
        print(
            f"{record['graph']:>20} {record['solver']:>28}: "
            f"work={work['edge_operations']:>9.0f}, "
            f"inner={work['local_inner_iterations']:>4}, "
            f"restarts={metrics['outer_restarts']:>3}, "
            f"explored={metrics['explored_vertices']:>4}"
        )


if __name__ == "__main__":
    main()
