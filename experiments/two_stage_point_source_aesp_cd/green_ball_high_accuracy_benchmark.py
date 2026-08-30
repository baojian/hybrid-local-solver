#!/usr/bin/env python3
"""One-shot point-source Green ball followed by one fixed principal CG solve."""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from leakage_screen_benchmark import direct_priority_ppr, fixed_cg_to_error
from portfolio_benchmark import (
    appr_envelope,
    binary_tree,
    broom_graph,
    cycle_graph,
    grid_graph,
    normalized_matrix,
    path_graph,
    radius_screen,
    star_graph,
)


@dataclass(frozen=True)
class GreenBallRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    radius: int
    cap: int
    succeeded: bool
    envelope_volume: int
    exposure_work: int
    cg_iterations: int
    cg_work: int
    lane_work: int
    fallback_work: int
    total_sequential_work: int
    direct_work: int
    lane_ratio: float
    sequential_ratio: float
    semantic_error: float


def green_radius(alpha: float, delta: float) -> int:
    """Certified radius for point-source PPR exterior amplitude delta."""
    if alpha >= 1.0:
        return 0
    denominator = math.log((1.0 + math.sqrt(alpha)) / (1.0 - math.sqrt(alpha)))
    return max(0, math.ceil(math.log(2.0 / delta) / denominator) - 1)


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> GreenBallRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    reference = np.asarray(spsolve(matrix, source))
    direct_vector, direct_support, fifo_work, _pushes = appr_envelope(
        adjacency, alpha, epsilon, seed
    )
    priority_vector, priority_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    direct_work = min(fifo_work, priority_work)

    radius = green_radius(alpha, epsilon / 2.0)
    cap = max(1, int(np.floor(2.0 / epsilon)))
    envelope, exposure_work, retained = radius_screen(adjacency, radius, cap, seed)
    cg_iterations = cg_work = 0
    lane_work = exposure_work
    fallback_work = 0
    if retained:
        indices = np.flatnonzero(envelope)
        principal = matrix[indices][:, indices]
        restricted_source = source[indices]
        candidate, cg_iterations, _bar = fixed_cg_to_error(
            principal,
            restricted_source,
            alpha,
            epsilon / 2.0,
            np.zeros(len(indices)),
        )
        output = np.zeros(len(adjacency))
        output[indices] = candidate
        volume = int(degree[envelope].sum())
        cg_work = cg_iterations * volume
        lane_work += cg_work
    else:
        volume = int(degree[envelope].sum())
        fallback_work = direct_work
        if fifo_work <= priority_work:
            output = np.sqrt(degree) * np.where(direct_support, direct_vector, 0.0)
        else:
            output = priority_vector
    error = float(np.max(np.abs((output - reference) / root_degree)))
    if error > epsilon * (1 + 1e-7):
        raise AssertionError("Green-ball lane missed its semantic target")
    sequential = lane_work + fallback_work
    return GreenBallRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        radius,
        cap,
        retained,
        volume,
        exposure_work,
        cg_iterations,
        cg_work,
        lane_work,
        fallback_work,
        sequential,
        direct_work,
        lane_work / direct_work if direct_work else 0.0,
        sequential / direct_work if direct_work else 0.0,
        error,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--alphas", nargs="+", type=float)
    parser.add_argument("--epsilons", nargs="+", type=float)
    args = parser.parse_args()
    graphs = [
        ("path-96", path_graph(96)),
        ("cycle-96", cycle_graph(96)),
        ("star-96", star_graph(95)),
        ("binary-depth-7", binary_tree(7)),
        ("broom-48-47", broom_graph(48, 47)),
        ("grid-12x12", grid_graph(12, 12)),
    ]
    alphas = tuple(args.alphas) if args.alphas else (0.01, 0.04, 0.16)
    epsilons = tuple(args.epsilons) if args.epsilons else (0.0001, 0.0005, 0.001, 0.002, 0.005)
    rows = [
        run_case(family, graph, alpha, epsilon)
        for family, graph in graphs
        for alpha in alphas
        for epsilon in epsilons
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=asdict(rows[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    nontrivial = [row for row in rows if row.direct_work]
    successful = [row for row in nontrivial if row.succeeded]
    wins = [row for row in successful if row.lane_ratio < 1.0]
    fair_wins = [row for row in successful if 2 * row.lane_ratio < 1.0]
    print(
        f"rows={len(rows)} successful={len(successful)} "
        f"standalone-wins={len(wins)} fair-wins={len(fair_wins)} "
        f"median-lane={np.median([row.lane_ratio for row in successful]):.6f}"
    )
    for row in sorted(wins, key=lambda item: item.lane_ratio):
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"ratio={row.lane_ratio:.6f}",
            f"R={row.radius}",
            f"V={row.envelope_volume}",
            f"cg={row.cg_iterations}",
        )


if __name__ == "__main__":
    main()
