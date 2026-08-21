"""Measure the high-degree decoy obstruction to geometric-envelope CG."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from experiments.result_schema import make_result_bundle, write_result_bundle
from src.hybrid_solver_codex.evolving_cg import (
    geometric_envelope_cg,
    restarted_evolving_set_cg,
)
from src.synthetic_graphs import decoy_hub_graph

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "raw" / "geometric-envelope-obstruction.json"
DEFAULT_HUB_DEGREES = (16, 64, 256, 1024, 4096)
STOPPING_RULE = (
    "terminate only after recomputing r = b - Qx and verifying "
    "max_i |r[i]| / sqrt(d[i]) <= alpha * eps_ppr"
)
WORK_UNIT = (
    "degree-weighted adjacency-list entries scanned by local Q products or envelope discovery"
)


def threshold_ratios(alpha: float, hub_degree: int) -> tuple[float, float, float, float]:
    """Return the exact residual-to-alpha ratios used in the proof."""
    first_branch = (1.0 - alpha) / (3.0 * (1.0 + alpha))
    true_leaf = (1.0 - alpha) ** 2 / (3.0 * (1.0 + alpha) ** 2 - (1.0 - alpha) ** 2)
    decoy_hub = true_leaf / hub_degree
    terminal_hub = (1.0 - alpha) ** 2 / (
        hub_degree * (3.0 * (1.0 + alpha) ** 2 - 2.0 * (1.0 - alpha) ** 2)
    )
    return first_branch, true_leaf, decoy_hub, terminal_hub


def run_exploration(
    *,
    alpha: float,
    eps_ppr: float,
    hub_degrees: tuple[int, ...],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Return schema-ready literal and geometric records for the obstruction."""
    records: list[dict[str, object]] = []
    for hub_degree in hub_degrees:
        graph = decoy_hub_graph(hub_degree)
        first_ratio, leaf_ratio, hub_ratio, terminal_hub_ratio = threshold_ratios(alpha, hub_degree)
        if not max(hub_ratio, terminal_hub_ratio) <= eps_ppr < min(first_ratio, leaf_ratio):
            raise ValueError(
                "parameters must make the branch and leaf violate while the hub does not"
            )

        for solver_name, solver, policy in (
            (
                "restarted_evolving_set_cg",
                restarted_evolving_set_cg,
                "admit boundary violations only",
            ),
            (
                "geometric_envelope_cg",
                geometric_envelope_cg,
                "admit violations then double degree volume by BFS halo",
            ),
        ):
            result = solver(
                graph,
                alpha=alpha,
                source=0,
                eps_ppr=eps_ppr,
            )
            records.append(
                {
                    "graph": graph.name,
                    "alpha": alpha,
                    "epsilon": eps_ppr,
                    "epsilon_name": "eps_ppr_note_scoped",
                    "random_seed": 0,
                    "stopping_rule": STOPPING_RULE,
                    "solver": solver_name,
                    "solver_parameters": {
                        "support_change_policy": policy,
                        "volume_growth_factor": 2.0
                        if solver_name == "geometric_envelope_cg"
                        else None,
                    },
                    "source": 0,
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
                        "hub_degree": hub_degree,
                        "nodes": graph.n,
                        "edges": graph.m,
                        "certified": result.certified,
                        "terminal_scaled_residual": float(
                            np.max(np.abs(result.residual) / np.sqrt(graph.degree))
                        ),
                        "explored_vertices": int(result.explored_vertices.size),
                        "explored_volume": float(np.sum(graph.degree[result.explored_vertices])),
                        "first_branch_residual_over_alpha": first_ratio,
                        "true_leaf_residual_over_alpha": leaf_ratio,
                        "decoy_hub_residual_over_alpha": hub_ratio,
                        "terminal_hub_residual_over_alpha": terminal_hub_ratio,
                    },
                }
            )

    config: dict[str, object] = {
        "alpha": alpha,
        "epsilon": eps_ppr,
        "epsilon_name": "eps_ppr_note_scoped",
        "hub_degrees": list(hub_degrees),
        "random_seed": 0,
        "stopping_rule": STOPPING_RULE,
        "work_unit": WORK_UNIT,
    }
    return config, records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--eps-ppr", type=float, default=0.25)
    parser.add_argument(
        "--hub-degrees",
        type=int,
        nargs="+",
        default=list(DEFAULT_HUB_DEGREES),
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    config, records = run_exploration(
        alpha=args.alpha,
        eps_ppr=args.eps_ppr,
        hub_degrees=tuple(args.hub_degrees),
    )
    payload = make_result_bundle(
        experiment="high-degree decoy obstruction to geometric-envelope CG",
        config=config,
        records=records,
    )
    write_result_bundle(args.output, payload)

    print(f"wrote {len(records)} records to {args.output}")
    for record in records:
        print(
            f"hub_degree={record['metrics']['hub_degree']:>5} "
            f"{record['solver']:>28}: "
            f"work={record['work']['edge_operations']:>7.0f}, "
            f"explored_volume={record['metrics']['explored_volume']:>7.0f}"
        )


if __name__ == "__main__":
    main()
