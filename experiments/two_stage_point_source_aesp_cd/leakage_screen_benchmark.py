#!/usr/bin/env python3
"""Hard-capped direct-PPR boundary-leakage screen followed by fixed CG."""

from __future__ import annotations

import argparse
import csv
import heapq
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from mass_screen_benchmark import geometric_radii
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
class LeakageRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    cap: int
    succeeded: bool
    trigger_radius: int
    envelope_volume: int
    exposure_work: int
    attempt_count: int
    scratch_iterations: int
    scratch_work: int
    fallback_work: int
    total_work: int
    direct_appr_work: int
    direct_priority_work: int
    ratio_to_best_direct: float
    semantic_error: float
    leakage_budget: float
    terminal_error_bar: float


def direct_priority_ppr(
    adjacency: list[list[int]], alpha: float, epsilon: float, seed: int
) -> tuple[np.ndarray, int]:
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
    return vector, work


def boundary_rows(
    adjacency: list[list[int]], envelope: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    inside = set(int(vertex) for vertex in np.flatnonzero(envelope))
    outside = sorted(
        {neighbor for vertex in inside for neighbor in adjacency[vertex] if neighbor not in inside}
    )
    internal_counts = np.asarray(
        [sum(neighbor in inside for neighbor in adjacency[vertex]) for vertex in outside],
        dtype=float,
    )
    return np.asarray(outside, dtype=int), internal_counts


def fixed_cg_with_leakage_gate(
    adjacency: list[list[int]],
    degree: np.ndarray,
    matrix,
    source: np.ndarray,
    envelope: np.ndarray,
    alpha: float,
    leakage_budget: float,
    terminal_budget: float,
) -> tuple[np.ndarray | None, int, float]:
    """Run exact-face CG until both boundary and terminal certificates pass."""
    indices = np.flatnonzero(envelope)
    position = {int(vertex): offset for offset, vertex in enumerate(indices)}
    principal = matrix[indices][:, indices]
    restricted_source = source[indices]
    root_degree = np.sqrt(degree)
    boundary, internal_counts = boundary_rows(adjacency, envelope)
    coupling = (1.0 - alpha) / 2.0

    vector = np.zeros(len(indices))
    residual = restricted_source.copy()
    direction = residual.copy()
    residual_squared = float(residual @ residual)
    iterations = 0
    terminal_error = np.sqrt(residual_squared) / alpha

    for _ in range(max(1, 2 * len(indices) + 1)):
        terminal_error = np.sqrt(max(0.0, residual_squared)) / alpha
        leakage_passes = True
        if len(boundary):
            maximum_upper = -np.inf
            for offset, vertex in enumerate(boundary):
                # This directly mirrors
                # -Q_{vE} u / sqrt(d_v) = c/d_v sum u_i/sqrt(d_i).
                estimate = (
                    coupling
                    * sum(
                        vector[position[neighbor]] / root_degree[neighbor]
                        for neighbor in adjacency[int(vertex)]
                        if neighbor in position
                    )
                    / degree[int(vertex)]
                )
                upper = estimate + (
                    coupling * internal_counts[offset] / degree[int(vertex)] * terminal_error
                )
                maximum_upper = max(maximum_upper, upper)
            leakage_passes = maximum_upper <= alpha * leakage_budget * (1 + 1e-10)
        if leakage_passes and terminal_error <= terminal_budget * (1 + 1e-10):
            output = np.zeros(len(adjacency))
            output[indices] = np.maximum(vector, 0.0)
            return output, iterations, terminal_error
        if residual_squared <= 1e-30:
            break
        image = np.asarray(principal @ direction)
        denominator = float(direction @ image)
        if denominator <= 0.0:
            raise AssertionError("principal PPR matrix is not positive definite")
        step = residual_squared / denominator
        vector = vector + step * direction
        following = residual - step * image
        following_squared = float(following @ following)
        iterations += 1
        if following_squared <= 1e-30:
            residual = following
            residual_squared = following_squared
            continue
        direction = following + (following_squared / residual_squared) * direction
        residual = following
        residual_squared = following_squared
    return None, iterations, terminal_error


def fixed_cg_to_error(
    matrix,
    source: np.ndarray,
    alpha: float,
    terminal_budget: float,
    initial: np.ndarray,
) -> tuple[np.ndarray, int, float]:
    """CG from a certified warm start until the strong-convexity error bar."""
    vector = initial.copy()
    residual = np.asarray(source - matrix @ vector)
    direction = residual.copy()
    residual_squared = float(residual @ residual)
    iterations = 0
    for _ in range(max(1, 2 * len(source) + 1)):
        error_bar = np.sqrt(max(0.0, residual_squared)) / alpha
        if error_bar <= terminal_budget * (1 + 1e-10):
            return np.maximum(vector, 0.0), iterations, error_bar
        image = np.asarray(matrix @ direction)
        denominator = float(direction @ image)
        if denominator <= 0.0:
            raise AssertionError("principal PPR matrix is not positive definite")
        step = residual_squared / denominator
        vector = vector + step * direction
        following = residual - step * image
        following_squared = float(following @ following)
        iterations += 1
        if following_squared <= 1e-30:
            residual = following
            residual_squared = following_squared
            continue
        direction = following + (following_squared / residual_squared) * direction
        residual = following
        residual_squared = following_squared
    raise RuntimeError("fixed CG failed to reach its residual certificate")


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> LeakageRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    full_solution = np.asarray(spsolve(matrix, source))
    _fifo, _support, fifo_work, _pushes = appr_envelope(adjacency, alpha, epsilon, seed)
    priority_output, priority_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    priority_error = float(np.max(np.abs((priority_output - full_solution) / root_degree)))
    if priority_error > epsilon * (1 + 1e-7):
        raise AssertionError("priority baseline missed the target")

    cap = max(1, int(np.floor(2.0 / epsilon)))
    leakage_budget = epsilon / 2.0
    terminal_budget = epsilon / 2.0
    if priority_work == 0:
        semantic_error = float(np.max(np.abs((priority_output - full_solution) / root_degree)))
        return LeakageRow(
            family,
            len(adjacency),
            alpha,
            epsilon,
            cap,
            False,
            -1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            fifo_work,
            priority_work,
            0.0,
            semantic_error,
            leakage_budget,
            float("nan"),
        )
    attempts = geometric_radii(adjacency, seed, cap)
    output = None
    total_iterations = scratch_work = 0
    attempt_count = 0
    trigger_radius = -1
    trigger_volume = 0
    terminal_error = float("nan")
    for radius, envelope, volume in attempts:
        attempt_count += 1
        candidate, iterations, error_bar = fixed_cg_with_leakage_gate(
            adjacency,
            degree,
            matrix,
            source,
            envelope,
            alpha,
            leakage_budget,
            terminal_budget,
        )
        total_iterations += iterations
        scratch_work += iterations * volume
        if candidate is None:
            continue
        output = candidate
        trigger_radius = radius
        trigger_volume = volume
        terminal_error = error_bar
        break

    exposure_work = attempts[-1][2] if attempts else 0
    fallback_work = 0
    if output is None:
        output = priority_output
        fallback_work = priority_work
    semantic_error = float(np.max(np.abs((output - full_solution) / root_degree)))
    if semantic_error > epsilon * (1 + 1e-7):
        raise AssertionError("leakage-screen lane missed the semantic target")
    total_work = exposure_work + scratch_work + fallback_work
    best_direct = min(fifo_work, priority_work)
    ratio = total_work / best_direct if best_direct else (0.0 if total_work == 0 else np.inf)
    return LeakageRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        cap,
        trigger_radius >= 0,
        trigger_radius,
        trigger_volume,
        exposure_work,
        attempt_count,
        total_iterations,
        scratch_work,
        fallback_work,
        total_work,
        fifo_work,
        priority_work,
        ratio,
        semantic_error,
        leakage_budget,
        terminal_error,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--alphas", nargs="+", type=float)
    parser.add_argument("--epsilons", nargs="+", type=float)
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
            "success" if row.succeeded else "fallback",
            f"R={row.trigger_radius}",
            f"V={row.envelope_volume}",
            f"K={row.scratch_iterations}",
            f"W={row.total_work}",
            f"ratio={row.ratio_to_best_direct:.2f}",
            f"err={row.semantic_error:.2e}",
        )


if __name__ == "__main__":
    main()
