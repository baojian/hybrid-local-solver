#!/usr/bin/env python3
"""Diagnose whether a small halo can make the two-stage leakage gate useful."""

from __future__ import annotations

import argparse
import csv
import heapq
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from leakage_screen_benchmark import direct_priority_ppr
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
class HaloDiagnosticRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    succeeded: bool
    checkpoint: int
    halo_depth: int
    support_volume: int
    envelope_volume: int
    prefix_work: int
    exposure_work: int
    scan_work: int
    cg_iterations: int
    cg_work: int
    total_work: int
    direct_work: int
    ratio: float
    semantic_error: float


def priority_checkpoints(
    adjacency: list[list[int]], alpha: float, epsilon: float, seed: int
) -> list[tuple[np.ndarray, np.ndarray, int]]:
    """Return every newly enlarged support along the priority APPR trace."""
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    vector = np.zeros(len(adjacency))
    residual = source.copy()
    versions = np.zeros(len(adjacency), dtype=np.int64)
    heap: list[tuple[float, int, int]] = [(-residual[seed] / root_degree[seed], seed, 0)]
    support = np.zeros(len(adjacency), dtype=bool)
    checkpoints: list[tuple[np.ndarray, np.ndarray, int]] = []
    work = 0
    while heap:
        _key, vertex, version = heapq.heappop(heap)
        if version != versions[vertex] or residual[vertex] <= 0.0:
            continue
        if residual[vertex] / root_degree[vertex] <= alpha * epsilon:
            break
        value = residual[vertex]
        step = value / diagonal
        vector[vertex] += step
        residual[vertex] = 0.0
        versions[vertex] += 1
        work += int(degree[vertex])
        enlarged = not support[vertex]
        support[vertex] = True
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
        if enlarged:
            checkpoints.append((vector.copy(), support.copy(), work))
    return checkpoints


def halo(
    adjacency: list[list[int]], support: np.ndarray, depth: int, cap: int
) -> tuple[np.ndarray, bool]:
    """Return the depth-neighborhood, refusing before its volume exceeds cap."""
    degree = np.asarray([len(row) for row in adjacency], dtype=int)
    envelope = support.copy()
    volume = int(degree[envelope].sum())
    queue = deque((int(vertex), 0) for vertex in np.flatnonzero(support))
    while queue:
        vertex, distance = queue.popleft()
        if distance >= depth:
            continue
        for neighbor in adjacency[vertex]:
            if envelope[neighbor]:
                continue
            if volume + int(degree[neighbor]) > cap:
                return envelope, False
            envelope[neighbor] = True
            volume += int(degree[neighbor])
            queue.append((neighbor, distance + 1))
    return envelope, True


def warm_cg_gate(
    adjacency: list[list[int]],
    degree: np.ndarray,
    matrix,
    source: np.ndarray,
    envelope: np.ndarray,
    initial: np.ndarray,
    alpha: float,
    leakage_budget: float,
    terminal_budget: float,
) -> tuple[np.ndarray | None, int]:
    """Warm-started principal CG with the direct boundary-leakage gate."""
    indices = np.flatnonzero(envelope)
    position = {int(vertex): offset for offset, vertex in enumerate(indices)}
    principal = matrix[indices][:, indices]
    restricted_source = source[indices]
    root_degree = np.sqrt(degree)
    coupling = (1.0 - alpha) / 2.0
    boundary = sorted(
        {
            neighbor
            for vertex in indices
            for neighbor in adjacency[int(vertex)]
            if not envelope[neighbor]
        }
    )
    vector = initial[indices].copy()
    residual = np.asarray(restricted_source - principal @ vector)
    direction = residual.copy()
    residual_squared = float(residual @ residual)
    for iteration in range(2 * len(indices) + 2):
        error_bar = np.sqrt(max(0.0, residual_squared)) / alpha
        maximum_upper = 0.0
        for vertex in boundary:
            estimate = (
                coupling
                * sum(
                    vector[position[neighbor]] / root_degree[neighbor]
                    for neighbor in adjacency[vertex]
                    if envelope[neighbor]
                )
                / degree[vertex]
            )
            internal_degree = sum(envelope[neighbor] for neighbor in adjacency[vertex])
            maximum_upper = max(
                maximum_upper,
                estimate + coupling * internal_degree * error_bar / degree[vertex],
            )
        if maximum_upper <= alpha * leakage_budget * (
            1 + 1e-10
        ) and error_bar <= terminal_budget * (1 + 1e-10):
            output = np.zeros(len(adjacency))
            output[indices] = np.maximum(vector, 0.0)
            return output, iteration
        if residual_squared <= 1e-30:
            break
        image = np.asarray(principal @ direction)
        denominator = float(direction @ image)
        if denominator <= 0.0:
            raise AssertionError("principal matrix must be positive definite")
        step = residual_squared / denominator
        vector += step * direction
        following = residual - step * image
        following_squared = float(following @ following)
        if following_squared <= 1e-30:
            residual = following
            residual_squared = following_squared
            continue
        direction = following + following_squared / residual_squared * direction
        residual = following
        residual_squared = following_squared
    return None, 2 * len(indices) + 1


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> HaloDiagnosticRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    full_solution = np.asarray(spsolve(matrix, source))
    _fifo, _support, fifo_work, _pushes = appr_envelope(adjacency, alpha, epsilon, seed)
    _priority, priority_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    direct_work = min(fifo_work, priority_work)
    cap = max(1, int(np.floor(2.0 / epsilon)))
    best: HaloDiagnosticRow | None = None
    checkpoints = priority_checkpoints(adjacency, alpha, epsilon, seed)
    for checkpoint, (initial, support, prefix_work) in enumerate(checkpoints, 1):
        support_volume = int(degree[support].sum())
        for depth in (0, 1, 2, 4, 8, 16, 32, 64):
            envelope, retained = halo(adjacency, support, depth, cap)
            if not retained:
                continue
            envelope_volume = int(degree[envelope].sum())
            output, iterations = warm_cg_gate(
                adjacency,
                degree,
                matrix,
                source,
                envelope,
                initial,
                alpha,
                epsilon / 2.0,
                epsilon / 2.0,
            )
            if output is None:
                continue
            error = float(np.max(np.abs((output - full_solution) / root_degree)))
            if error > epsilon * (1 + 1e-7):
                raise AssertionError("certified halo output missed semantic target")
            exposure_work = envelope_volume - support_volume
            scan_work = envelope_volume
            cg_work = iterations * envelope_volume
            total = prefix_work + exposure_work + scan_work + cg_work
            row = HaloDiagnosticRow(
                family,
                len(adjacency),
                alpha,
                epsilon,
                True,
                checkpoint,
                depth,
                support_volume,
                envelope_volume,
                prefix_work,
                exposure_work,
                scan_work,
                iterations,
                cg_work,
                total,
                direct_work,
                total / direct_work,
                error,
            )
            if best is None or row.total_work < best.total_work:
                best = row
    if best is not None:
        return best
    return HaloDiagnosticRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        False,
        0,
        0,
        0,
        0,
        priority_work,
        0,
        0,
        0,
        0,
        direct_work,
        direct_work,
        1.0,
        float(np.max(np.abs((_priority - full_solution) / root_degree))),
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
        for epsilon in (0.005, 0.01, 0.02)
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=asdict(rows[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    successes = [row for row in rows if row.succeeded]
    wins = [row for row in successes if row.ratio < 1.0]
    print(
        f"rows={len(rows)} successes={len(successes)} wins={len(wins)} "
        f"best={min(row.ratio for row in rows):.6f} "
        f"median={np.median([row.ratio for row in rows]):.6f}"
    )
    for row in sorted(wins, key=lambda item: item.ratio):
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"ratio={row.ratio:.6f}",
            f"checkpoint={row.checkpoint}",
            f"halo={row.halo_depth}",
            f"volume={row.envelope_volume}",
            f"cg={row.cg_iterations}",
        )


if __name__ == "__main__":
    main()
