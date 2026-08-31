#!/usr/bin/env python3
"""Oracle diagnostic for one BFS ball, one CG solve, and one leakage scan."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from leakage_screen_benchmark import (
    boundary_rows,
    direct_priority_ppr,
    fixed_cg_to_error,
)
from mass_capture_diagnostic import distances
from portfolio_benchmark import (
    appr_envelope,
    binary_tree,
    broom_graph,
    cycle_graph,
    grid_graph,
    normalized_matrix,
    path_graph,
    star_graph,
)


@dataclass(frozen=True)
class SingleBallRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    succeeded: bool
    radius: int
    envelope_volume: int
    exposure_work: int
    cg_iterations: int
    cg_work: int
    boundary_work: int
    total_work: int
    direct_work: int
    ratio: float
    semantic_error: float
    maximum_leakage_upper: float


def leakage_upper(
    adjacency: list[list[int]],
    degree: np.ndarray,
    envelope: np.ndarray,
    candidate: np.ndarray,
    error_bar: float,
    alpha: float,
) -> tuple[float, int]:
    indices = np.flatnonzero(envelope)
    position = {int(vertex): offset for offset, vertex in enumerate(indices)}
    root_degree = np.sqrt(degree)
    coupling = (1.0 - alpha) / 2.0
    boundary, internal_counts = boundary_rows(adjacency, envelope)
    maximum = 0.0
    work = 0
    for offset, vertex in enumerate(boundary):
        internal_neighbors = [neighbor for neighbor in adjacency[int(vertex)] if envelope[neighbor]]
        work += len(internal_neighbors)
        estimate = (
            coupling
            * sum(
                candidate[position[neighbor]] / root_degree[neighbor]
                for neighbor in internal_neighbors
            )
            / degree[int(vertex)]
        )
        maximum = max(
            maximum,
            estimate + coupling * internal_counts[offset] * error_bar / degree[int(vertex)],
        )
    return maximum, work


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> SingleBallRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    reference = np.asarray(spsolve(matrix, source))
    _fifo, _support, fifo_work, _pushes = appr_envelope(adjacency, alpha, epsilon, seed)
    _priority, priority_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    direct_work = min(fifo_work, priority_work)
    cap = max(1, int(np.floor(2.0 / epsilon)))
    distance = distances(adjacency, seed)
    best: SingleBallRow | None = None
    for radius in range(int(np.max(distance)) + 1):
        envelope = distance <= radius
        volume = int(degree[envelope].sum())
        if volume > cap:
            break
        indices = np.flatnonzero(envelope)
        principal = matrix[indices][:, indices]
        restricted_source = source[indices]
        candidate, iterations, error_bar = fixed_cg_to_error(
            principal,
            restricted_source,
            alpha,
            epsilon / 2.0,
            np.zeros(len(indices)),
        )
        maximum, boundary_work = leakage_upper(
            adjacency,
            degree,
            envelope,
            candidate,
            error_bar,
            alpha,
        )
        if maximum > alpha * epsilon / 2.0 * (1 + 1e-10):
            continue
        output = np.zeros(len(adjacency))
        output[indices] = candidate
        error = float(np.max(np.abs((output - reference) / root_degree)))
        if error > epsilon * (1 + 1e-7):
            raise AssertionError("single-ball leakage certificate failed")
        cg_work = iterations * volume
        total = volume + cg_work + boundary_work
        row = SingleBallRow(
            family,
            len(adjacency),
            alpha,
            epsilon,
            True,
            radius,
            volume,
            volume,
            iterations,
            cg_work,
            boundary_work,
            total,
            direct_work,
            total / direct_work,
            error,
            maximum,
        )
        if best is None or row.total_work < best.total_work:
            best = row
    if best is not None:
        return best
    return SingleBallRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        False,
        -1,
        0,
        0,
        0,
        0,
        0,
        direct_work,
        direct_work,
        1.0,
        float("nan"),
        float("nan"),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    graphs = [
        ("path-96", path_graph(96)),
        ("cycle-96", cycle_graph(96)),
        ("star-96", star_graph(95)),
        ("binary-depth-7", binary_tree(7)),
        ("broom-48-47", broom_graph(48, 47)),
        ("grid-12x12", grid_graph(12, 12)),
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
    print(
        f"rows={len(rows)} successes={len(successes)} wins={len(wins)} "
        f"median={np.median([row.ratio for row in successes]):.6f}"
    )
    for row in sorted(wins, key=lambda item: item.ratio):
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"ratio={row.ratio:.6f}",
            f"radius={row.radius}",
            f"volume={row.envelope_volume}",
            f"cg={row.cg_iterations}",
        )


if __name__ == "__main__":
    main()
