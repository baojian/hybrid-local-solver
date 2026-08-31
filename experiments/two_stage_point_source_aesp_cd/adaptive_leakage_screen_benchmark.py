#!/usr/bin/env python3
"""Priority APPR discovery followed by one fixed solve after a leakage gate."""

from __future__ import annotations

import argparse
import csv
import heapq
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
    star_graph,
)


@dataclass(frozen=True)
class AdaptiveLeakageRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    leakage_fraction: float
    cap: int
    succeeded: bool
    checkpoint_count: int
    envelope_volume: int
    priority_work: int
    priority_pushes: int
    gate_work: int
    scratch_iterations: int
    scratch_work: int
    total_work: int
    direct_appr_work: int
    direct_priority_work: int
    ratio_to_best_direct: float
    semantic_error: float


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
    leakage_fraction: float = 0.5,
) -> AdaptiveLeakageRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    full_solution = np.asarray(spsolve(matrix, source))
    _fifo, _support, fifo_work, _pushes = appr_envelope(adjacency, alpha, epsilon, seed)
    _priority_output, direct_priority_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)

    cap = max(1, int(np.floor(2.0 / epsilon)))
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    if not 0.0 < leakage_fraction < 1.0:
        raise ValueError("leakage_fraction must lie strictly between zero and one")
    leakage_budget = leakage_fraction * epsilon
    terminal_budget = (1.0 - leakage_fraction) * epsilon
    vector = np.zeros(len(adjacency))
    residual = source.copy()
    versions = np.zeros(len(adjacency), dtype=np.int64)
    heap: list[tuple[float, int, int]] = [(-residual[seed] / root_degree[seed], seed, 0)]
    support = np.zeros(len(adjacency), dtype=bool)
    support_volume = 0
    boundary: set[int] = set()
    internal_versions = np.zeros(len(adjacency), dtype=np.int64)
    internal_heap: list[tuple[float, int, int]] = []
    boundary_heap: list[tuple[float, int, int]] = []
    next_checkpoint_volume = int(degree[seed])
    checkpoints_enabled = True
    checkpoint_count = 0
    priority_work = priority_pushes = gate_work = 0
    scratch_iterations = scratch_work = 0
    publication = None
    trigger_volume = 0

    while heap:
        _negative_key, vertex, version = heapq.heappop(heap)
        if version != versions[vertex] or residual[vertex] <= 0.0:
            continue
        if residual[vertex] / root_degree[vertex] <= alpha * epsilon:
            break
        value = residual[vertex]
        step = value / diagonal
        vector[vertex] += step
        residual[vertex] = 0.0
        versions[vertex] += 1
        internal_versions[vertex] += 1
        priority_work += int(degree[vertex])
        priority_pushes += 1
        if not support[vertex]:
            support[vertex] = True
            support_volume += int(degree[vertex])
            boundary.discard(vertex)
            for neighbor in adjacency[vertex]:
                if not support[neighbor]:
                    boundary.add(neighbor)
                    heapq.heappush(
                        boundary_heap,
                        (
                            -residual[neighbor] / root_degree[neighbor],
                            neighbor,
                            int(versions[neighbor]),
                        ),
                    )
        for neighbor in adjacency[vertex]:
            residual[neighbor] += coupling * step / (root_degree[vertex] * root_degree[neighbor])
            versions[neighbor] += 1
            if support[neighbor]:
                internal_versions[neighbor] += 1
                heapq.heappush(
                    internal_heap,
                    (
                        -residual[neighbor] / root_degree[neighbor],
                        neighbor,
                        int(internal_versions[neighbor]),
                    ),
                )
            if residual[neighbor] > 0.0:
                heapq.heappush(
                    heap,
                    (
                        -residual[neighbor] / root_degree[neighbor],
                        neighbor,
                        int(versions[neighbor]),
                    ),
                )
            if neighbor in boundary and not support[neighbor]:
                heapq.heappush(
                    boundary_heap,
                    (
                        -residual[neighbor] / root_degree[neighbor],
                        neighbor,
                        int(versions[neighbor]),
                    ),
                )
        heapq.heappush(
            internal_heap,
            (
                -residual[vertex] / root_degree[vertex],
                vertex,
                int(internal_versions[vertex]),
            ),
        )

        if support_volume > cap:
            checkpoints_enabled = False
        if not checkpoints_enabled or support_volume < next_checkpoint_volume:
            continue
        checkpoint_count += 1
        next_checkpoint_volume = max(support_volume + 1, 2 * support_volume)
        while internal_heap:
            _key, inside, inside_version = internal_heap[0]
            if inside_version == internal_versions[inside] and support[inside]:
                break
            heapq.heappop(internal_heap)
        internal_density = max(0.0, -internal_heap[0][0]) if internal_heap else 0.0
        while boundary_heap:
            _key, outside, outside_version = boundary_heap[0]
            if (
                outside_version == versions[outside]
                and outside in boundary
                and not support[outside]
            ):
                break
            heapq.heappop(boundary_heap)
        boundary_density = max(0.0, -boundary_heap[0][0]) if boundary_heap else 0.0
        gate_work += 1
        leakage_passes = not boundary or (
            boundary_density + coupling * internal_density / alpha
            <= alpha * leakage_budget * (1 + 1e-10)
        )
        if not leakage_passes:
            continue

        indices = np.flatnonzero(support)
        principal = matrix[indices][:, indices]
        restricted_source = source[indices]
        candidate, iterations, _error_bar = fixed_cg_to_error(
            principal,
            restricted_source,
            alpha,
            terminal_budget,
            vector[indices],
        )
        scratch_iterations += iterations
        scratch_work += iterations * support_volume
        publication = np.zeros(len(adjacency))
        publication[indices] = candidate
        trigger_volume = support_volume
        break

    output = vector if publication is None else publication
    semantic_error = float(np.max(np.abs((output - full_solution) / root_degree)))
    if semantic_error > epsilon * (1 + 1e-7):
        raise AssertionError("adaptive leakage lane missed the target")
    total_work = priority_work + gate_work + scratch_work
    best_direct = min(fifo_work, direct_priority_work)
    ratio = total_work / best_direct if best_direct else (0.0 if total_work == 0 else np.inf)
    return AdaptiveLeakageRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        leakage_fraction,
        cap,
        publication is not None,
        checkpoint_count,
        trigger_volume,
        priority_work,
        priority_pushes,
        gate_work,
        scratch_iterations,
        scratch_work,
        total_work,
        fifo_work,
        direct_priority_work,
        ratio,
        semantic_error,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--alphas", nargs="+", type=float)
    parser.add_argument("--epsilons", nargs="+", type=float)
    parser.add_argument("--leakage-fraction", type=float, default=0.5)
    parser.add_argument("--quick", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    graphs = [
        ("path-96", path_graph(96)),
        ("cycle-96", cycle_graph(96)),
        ("star-96", star_graph(95)),
        ("binary-depth-7", binary_tree(7)),
        ("broom-48-47", broom_graph(48, 47)),
        ("grid-12x12", grid_graph(12, 12)),
    ]
    alphas = (
        tuple(args.alphas) if args.alphas else ((0.04, 0.16) if args.quick else (0.01, 0.04, 0.16))
    )
    epsilons = tuple(args.epsilons) if args.epsilons else ((0.1,) if args.quick else (0.05, 0.1))
    rows = [
        run_case(
            family,
            adjacency,
            alpha,
            epsilon,
            leakage_fraction=args.leakage_fraction,
        )
        for family, adjacency in graphs
        for alpha in alphas
        for epsilon in epsilons
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(asdict(rows[0])))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    print(f"wrote {len(rows)} rows to {args.output}")
    for row in rows:
        print(
            row.family,
            f"a={row.alpha:g}",
            f"eps={row.epsilon:g}",
            "success" if row.succeeded else "direct",
            f"K={row.checkpoint_count}",
            f"V={row.envelope_volume}",
            f"W={row.total_work}",
            f"ratio={row.ratio_to_best_direct:.2f}",
            f"err={row.semantic_error:.2e}",
        )


if __name__ == "__main__":
    main()
