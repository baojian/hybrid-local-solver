#!/usr/bin/env python3
"""Priority-APPR exposure with geometric fixed-envelope mass tests."""

from __future__ import annotations

import argparse
import csv
import heapq
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from mass_screen_benchmark import fixed_envelope_scratch, priority_cleanup
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
class AdaptiveRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    cap: int
    succeeded: bool
    checkpoint_count: int
    envelope_volume: int
    priority_work: int
    priority_pushes: int
    scratch_iterations: int
    scratch_work: int
    cleanup_work: int
    total_work: int
    direct_appr_work: int
    direct_priority_work: int
    ratio_to_best_direct: float
    semantic_error: float
    published_mass_deficit: float


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> AdaptiveRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    full_solution = np.asarray(spsolve(matrix, source))
    _fifo_vector, _fifo_support, fifo_work, _fifo_pushes = appr_envelope(
        adjacency, alpha, epsilon, seed
    )

    cap = max(1, int(np.floor(2.0 / epsilon)))
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    vector = np.zeros(len(adjacency))
    residual = source.copy()
    versions = np.zeros(len(adjacency), dtype=np.int64)
    heap: list[tuple[float, int, int]] = [(-residual[seed] / root_degree[seed], seed, 0)]
    support = np.zeros(len(adjacency), dtype=bool)
    support_volume = 0
    next_checkpoint_volume = int(degree[seed])
    checkpoint_count = 0
    scratch_iterations = scratch_work = 0
    priority_work = priority_pushes = 0
    publication = None
    current_mass = 0.0
    local_residual_mass = 0.0
    internal_degree = np.zeros(len(adjacency), dtype=np.int64)
    q_versions = np.zeros(len(adjacency), dtype=np.int64)
    q_heap: list[tuple[float, int, int]] = []

    while heap:
        _negative_key, vertex, version = heapq.heappop(heap)
        if version != versions[vertex] or residual[vertex] <= 0.0:
            continue
        if residual[vertex] / root_degree[vertex] <= alpha * epsilon:
            break
        value = residual[vertex]
        step = value / diagonal
        vector[vertex] += step
        current_mass += root_degree[vertex] * step
        was_supported = bool(support[vertex])
        if was_supported:
            local_residual_mass -= root_degree[vertex] * value
        residual[vertex] = 0.0
        versions[vertex] += 1
        priority_work += int(degree[vertex])
        priority_pushes += 1
        if not support[vertex]:
            support[vertex] = True
            support_volume += int(degree[vertex])
            for neighbor in adjacency[vertex]:
                if not support[neighbor]:
                    continue
                internal_degree[vertex] += 1
                internal_degree[neighbor] += 1
                q_versions[neighbor] += 1
                neighbor_ratio = diagonal - coupling * (
                    internal_degree[neighbor] / degree[neighbor]
                )
                heapq.heappush(
                    q_heap,
                    (
                        -neighbor_ratio,
                        neighbor,
                        int(q_versions[neighbor]),
                    ),
                )
            vertex_ratio = diagonal - coupling * (internal_degree[vertex] / degree[vertex])
            heapq.heappush(
                q_heap,
                (-vertex_ratio, vertex, int(q_versions[vertex])),
            )
        for neighbor in adjacency[vertex]:
            increment = coupling * step / (root_degree[vertex] * root_degree[neighbor])
            residual[neighbor] += increment
            if support[neighbor]:
                local_residual_mass += root_degree[neighbor] * increment
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

        if support_volume > cap or support_volume < next_checkpoint_volume:
            continue
        checkpoint_count += 1
        next_checkpoint_volume = max(
            support_volume + 1,
            2 * support_volume,
        )
        while q_heap:
            negative_ratio, q_vertex, q_version = q_heap[0]
            if q_version == q_versions[q_vertex] and support[q_vertex]:
                break
            heapq.heappop(q_heap)
        if not q_heap:
            raise AssertionError("nonempty support lost its row-ratio heap")
        q_maximum = -negative_ratio
        lower_mass = current_mass + local_residual_mass / q_maximum
        upper_mass = current_mass + local_residual_mass / alpha
        if upper_mass < 1.0 - np.sqrt(alpha):
            continue
        # A strict lower endpoint above the actual cleanup threshold proves
        # that the principal solve has positive trigger margin.  The scratch
        # is refined until the observable publication itself passes.
        if lower_mass <= 1.0 - np.sqrt(alpha) + 1e-12:
            continue
        indices = np.flatnonzero(support)
        principal = matrix[indices][:, indices]
        restricted_source = source[indices]
        candidate, iterations = fixed_envelope_scratch(
            principal,
            restricted_source,
            root_degree[indices],
            alpha,
            vector[indices],
            require_trigger=True,
        )
        scratch_iterations += iterations
        scratch_work += iterations * support_volume
        if candidate is None:
            continue
        publication = np.zeros(len(adjacency))
        publication[indices] = candidate
        break

    cleanup_work = 0
    if publication is not None:
        output, cleanup_work = priority_cleanup(adjacency, alpha, epsilon, seed, publication)
        published_deficit = max(0.0, 1.0 - float(root_degree @ publication))
    else:
        output = vector
        published_deficit = float("nan")
    semantic_error = float(np.max(np.abs((output - full_solution) / root_degree)))
    if semantic_error > epsilon * (1.0 + 1e-7):
        raise AssertionError("adaptive mass-screen lane missed semantic target")

    # The same priority trajectory without mass tests is the direct-priority
    # baseline.  Continue a fresh copy only to make its charged comparison
    # explicit and independent.
    baseline_vector = np.zeros(len(adjacency))
    baseline_residual = source.copy()
    baseline_versions = np.zeros(len(adjacency), dtype=np.int64)
    baseline_heap: list[tuple[float, int, int]] = [
        (-baseline_residual[seed] / root_degree[seed], seed, 0)
    ]
    direct_priority_work = 0
    while baseline_heap:
        _key, vertex, version = heapq.heappop(baseline_heap)
        if version != baseline_versions[vertex] or baseline_residual[vertex] <= 0.0:
            continue
        if baseline_residual[vertex] / root_degree[vertex] <= alpha * epsilon:
            break
        value = baseline_residual[vertex]
        step = value / diagonal
        baseline_vector[vertex] += step
        baseline_residual[vertex] = 0.0
        baseline_versions[vertex] += 1
        direct_priority_work += int(degree[vertex])
        for neighbor in adjacency[vertex]:
            baseline_residual[neighbor] += (
                coupling * step / (root_degree[vertex] * root_degree[neighbor])
            )
            baseline_versions[neighbor] += 1
            if baseline_residual[neighbor] > 0.0:
                heapq.heappush(
                    baseline_heap,
                    (
                        -baseline_residual[neighbor] / root_degree[neighbor],
                        neighbor,
                        int(baseline_versions[neighbor]),
                    ),
                )
    baseline_error = float(np.max(np.abs((baseline_vector - full_solution) / root_degree)))
    if baseline_error > epsilon * (1.0 + 1e-7):
        raise AssertionError("direct-priority baseline missed semantic target")

    total_work = priority_work + scratch_work + cleanup_work
    best_direct = min(fifo_work, direct_priority_work)
    ratio = total_work / best_direct if best_direct else (0.0 if total_work == 0 else np.inf)
    return AdaptiveRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        cap,
        publication is not None,
        checkpoint_count,
        support_volume if publication is not None else 0,
        priority_work,
        priority_pushes,
        scratch_iterations,
        scratch_work,
        cleanup_work,
        total_work,
        fifo_work,
        direct_priority_work,
        ratio,
        semantic_error,
        published_deficit,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--alphas", nargs="+", type=float)
    parser.add_argument("--epsilons", nargs="+", type=float)
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
        tuple(args.alphas)
        if args.alphas is not None
        else ((0.04, 0.16) if args.quick else (0.01, 0.04, 0.16))
    )
    epsilons = (
        tuple(args.epsilons)
        if args.epsilons is not None
        else ((0.1,) if args.quick else (0.05, 0.1))
    )
    rows = [
        run_case(family, adjacency, alpha, epsilon)
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
