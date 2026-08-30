#!/usr/bin/env python3
"""Couple Green-ball exposure with a charged APPR warm start for fixed CG."""

from __future__ import annotations

import argparse
import csv
import heapq
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from green_ball_high_accuracy_benchmark import green_radius
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
class WarmHybridRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    succeeded: bool
    radius: int
    envelope_volume: int
    exposure_work: int
    appr_prefix_work: int
    appr_prefix_pushes: int
    zero_cg_iterations: int
    warm_cg_iterations: int
    warm_cg_work: int
    hybrid_work: int
    direct_work: int
    ratio: float
    semantic_error: float


def priority_prefix(
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int,
    work_budget: int,
) -> tuple[np.ndarray, int, int]:
    """Run a resumable priority-PPR prefix for at most the charged budget."""
    degree, _matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    vector = np.zeros(len(adjacency))
    residual = source.copy()
    versions = np.zeros(len(adjacency), dtype=np.int64)
    heap: list[tuple[float, int, int]] = [(-residual[seed] / root_degree[seed], seed, 0)]
    work = pushes = 0
    while heap:
        _key, vertex, version = heapq.heappop(heap)
        if version != versions[vertex] or residual[vertex] <= 0.0:
            continue
        if residual[vertex] / root_degree[vertex] <= alpha * epsilon:
            break
        if work + int(degree[vertex]) > work_budget:
            break
        value = residual[vertex]
        step = value / diagonal
        vector[vertex] += step
        residual[vertex] = 0.0
        versions[vertex] += 1
        work += int(degree[vertex])
        pushes += 1
        for neighbor in adjacency[vertex]:
            residual[neighbor] += coupling * step / (root_degree[vertex] * root_degree[neighbor])
            versions[neighbor] += 1
            if residual[neighbor] > 0.0:
                heapq.heappush(
                    heap,
                    (
                        -residual[neighbor] / root_degree[neighbor],
                        neighbor,
                        int(versions[neighbor]),
                    ),
                )
    return vector, work, pushes


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> WarmHybridRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    reference = np.asarray(spsolve(matrix, source))
    _fifo, _support, fifo_work, _pushes = appr_envelope(adjacency, alpha, epsilon, seed)
    _priority, priority_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    direct_work = min(fifo_work, priority_work)
    radius = green_radius(alpha, epsilon / 2.0)
    cap = max(1, int(np.floor(2.0 / epsilon)))
    envelope, exposure_work, retained = radius_screen(adjacency, radius, cap, seed)
    if not retained:
        return WarmHybridRow(
            family,
            len(adjacency),
            alpha,
            epsilon,
            False,
            radius,
            int(degree[envelope].sum()),
            exposure_work,
            0,
            0,
            0,
            0,
            0,
            exposure_work + direct_work,
            direct_work,
            (exposure_work + direct_work) / direct_work,
            float("nan"),
        )
    prefix, prefix_work, prefix_pushes = priority_prefix(
        adjacency, alpha, epsilon, seed, exposure_work
    )
    indices = np.flatnonzero(envelope)
    principal = matrix[indices][:, indices]
    restricted_source = source[indices]
    _zero, zero_iterations, _bar = fixed_cg_to_error(
        principal,
        restricted_source,
        alpha,
        epsilon / 2.0,
        np.zeros(len(indices)),
    )
    candidate, warm_iterations, _bar = fixed_cg_to_error(
        principal,
        restricted_source,
        alpha,
        epsilon / 2.0,
        prefix[indices],
    )
    output = np.zeros(len(adjacency))
    output[indices] = candidate
    error = float(np.max(np.abs((output - reference) / root_degree)))
    if error > epsilon * (1 + 1e-7):
        raise AssertionError("warm Green--APPR hybrid missed semantic target")
    volume = int(degree[envelope].sum())
    cg_work = warm_iterations * volume
    hybrid_work = exposure_work + prefix_work + cg_work
    return WarmHybridRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        True,
        radius,
        volume,
        exposure_work,
        prefix_work,
        prefix_pushes,
        zero_iterations,
        warm_iterations,
        cg_work,
        hybrid_work,
        direct_work,
        hybrid_work / direct_work,
        error,
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
    reductions = [row.zero_cg_iterations - row.warm_cg_iterations for row in successes]
    print(
        f"rows={len(rows)} successes={len(successes)} wins={len(wins)} "
        f"median={np.median([row.ratio for row in successes]):.6f} "
        f"median-cg-reduction={np.median(reductions):.1f}"
    )
    for row in sorted(wins, key=lambda item: item.ratio):
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"ratio={row.ratio:.6f}",
            f"cg={row.zero_cg_iterations}->{row.warm_cg_iterations}",
        )


if __name__ == "__main__":
    main()
