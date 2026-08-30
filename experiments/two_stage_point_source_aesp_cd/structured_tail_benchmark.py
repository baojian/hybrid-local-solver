#!/usr/bin/env python3
"""Green set-only discovery followed by a linear-work structural solve."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from green_ball_high_accuracy_benchmark import green_radius
from leakage_screen_benchmark import direct_priority_ppr
from mass_capture_diagnostic import distances
from portfolio_benchmark import (
    appr_envelope,
    binary_tree,
    broom_graph,
    cycle_graph,
    normalized_matrix,
    path_graph,
    star_graph,
)
from structural_solvers import (
    principal_residual,
    tree_or_unicyclic_principal_solve,
)


@dataclass(frozen=True)
class StructuredTailRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    radius: int
    cap: int
    succeeded: bool
    solver_kind: str
    envelope_volume: int
    exposure_work: int
    factor_solve_work: int
    arithmetic_updates: int
    total_work: int
    direct_work: int
    ratio: float
    semantic_error: float


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> StructuredTailRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    reference = np.asarray(spsolve(matrix, source))
    _fifo, _support, fifo_work, _pushes = appr_envelope(adjacency, alpha, epsilon, seed)
    _priority, priority_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    direct_work = min(fifo_work, priority_work)
    # Exact structural elimination needs no terminal-error allocation, so the
    # whole semantic budget can be spent on the Green truncation.
    radius = green_radius(alpha, epsilon)
    cap = max(1, int(np.floor(2.0 / epsilon)))
    distance = distances(adjacency, seed)
    envelope = distance <= min(radius, int(np.max(distance)))
    volume = int(degree[envelope].sum())
    if volume > cap:
        return StructuredTailRow(
            family,
            len(adjacency),
            alpha,
            epsilon,
            radius,
            cap,
            False,
            "cap-abort",
            0,
            cap,
            0,
            0,
            cap + direct_work,
            direct_work,
            (cap + direct_work) / direct_work if direct_work else 0.0,
            float("nan"),
        )
    output, arithmetic_updates, solver_kind = tree_or_unicyclic_principal_solve(
        adjacency, envelope, degree, alpha, source, seed
    )
    retained_residual = principal_residual(adjacency, envelope, degree, alpha, source, output)
    residual_norm = float(np.max(np.abs(retained_residual[envelope])))
    if residual_norm > 2e-10:
        raise AssertionError(f"structural solver retained residual {residual_norm:.3e}")
    output = np.maximum(output, 0.0)
    error = float(np.max(np.abs((output - reference) / root_degree)))
    if error > epsilon * (1 + 1e-7):
        raise AssertionError("certified structural envelope exceeded Green budget")
    # Charge the actual scalar elimination/back-substitution updates plus one
    # retained-volume residual/materialization scan.
    factor_work = arithmetic_updates + volume
    total = volume + factor_work
    return StructuredTailRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        radius,
        cap,
        True,
        solver_kind,
        volume,
        volume,
        factor_work,
        arithmetic_updates,
        total,
        direct_work,
        total / direct_work if direct_work else 0.0,
        error,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    graphs = [
        ("path-1024", path_graph(1024)),
        ("cycle-1024", cycle_graph(1024)),
        ("star-1024", star_graph(1023)),
        ("binary-depth-10", binary_tree(10)),
        ("broom-512-511", broom_graph(512, 511)),
    ]
    rows = [
        run_case(family, graph, alpha, epsilon)
        for family, graph in graphs
        for alpha in (0.01, 0.04, 0.16)
        for epsilon in (0.0001, 0.0005, 0.001, 0.002, 0.005)
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=asdict(rows[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    successes = [row for row in rows if row.succeeded]
    wins = [row for row in successes if row.ratio < 1]
    fair_wins = [row for row in successes if 2 * row.ratio < 1]
    print(
        f"rows={len(rows)} successes={len(successes)} "
        f"standalone-wins={len(wins)} fair-wins={len(fair_wins)} "
        f"median={np.median([row.ratio for row in successes]):.6f}"
    )
    for row in sorted(wins, key=lambda item: item.ratio)[:20]:
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"ratio={row.ratio:.6f}",
            f"volume={row.envelope_volume}",
        )


if __name__ == "__main__":
    main()
