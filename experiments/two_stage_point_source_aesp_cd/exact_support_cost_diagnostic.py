#!/usr/bin/env python3
"""Compare literal exact-RPPR support discovery with semantic PPR lanes."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from green_ball_high_accuracy_benchmark import run_case as run_green_case
from mass_capture_diagnostic import distances
from portfolio_benchmark import (
    binary_tree,
    cycle_graph,
    grid_graph,
    monotone_obstacle,
    path_graph,
    star_graph,
)


@dataclass(frozen=True)
class ExactSupportRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    rho: float
    support_nodes: int
    support_volume: int
    support_radius: int
    rppr_discovery_work: int
    green_radius: int
    green_volume: int
    green_work: int
    direct_ppr_work: int
    rppr_to_green: float
    rppr_to_direct: float


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
) -> ExactSupportRow:
    rho = epsilon / 2.0
    obstacle = monotone_obstacle(adjacency, alpha, rho, 0)
    support = obstacle.vector > 1e-12
    degree = np.asarray([len(row) for row in adjacency], dtype=int)
    distance = distances(adjacency, 0)
    support_radius = int(np.max(distance[support])) if np.any(support) else 0
    green = run_green_case(family, adjacency, alpha, epsilon)
    return ExactSupportRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        rho,
        int(support.sum()),
        int(degree[support].sum()),
        support_radius,
        obstacle.work,
        green.radius,
        green.envelope_volume,
        green.lane_work,
        green.direct_work,
        obstacle.work / green.lane_work,
        obstacle.work / green.direct_work,
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
        ("grid-32x32", grid_graph(32, 32)),
    ]
    rows = [
        run_case(family, graph, alpha, 0.0001) for family, graph in graphs for alpha in (0.01, 0.04)
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=asdict(rows[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    print(
        f"rows={len(rows)} median-rppr/green="
        f"{np.median([row.rppr_to_green for row in rows]):.3f} "
        f"median-rppr/direct={np.median([row.rppr_to_direct for row in rows]):.3f}"
    )
    for row in rows:
        print(
            row.family,
            row.alpha,
            f"S=({row.support_nodes},{row.support_volume},R{row.support_radius})",
            f"W-rppr={row.rppr_discovery_work}",
            f"W-green={row.green_work}",
            f"W-direct={row.direct_ppr_work}",
        )


if __name__ == "__main__":
    main()
