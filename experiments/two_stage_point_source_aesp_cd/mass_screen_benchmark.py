#!/usr/bin/env python3
"""Executable hard-capped fixed-envelope AESP/CG to APPR mass handoff."""

from __future__ import annotations

import argparse
import csv
import heapq
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

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
class ScreenRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    cap: int
    succeeded: bool
    trigger_radius: int
    envelope_volume: int
    exposure_work: int
    scratch_iterations: int
    scratch_work: int
    cleanup_work: int
    fallback_work: int
    total_work: int
    direct_appr_work: int
    work_ratio: float
    semantic_error: float
    published_mass_deficit: float


def safe_publication(
    matrix,
    source: np.ndarray,
    root_degree: np.ndarray,
    raw: np.ndarray,
    alpha: float,
) -> tuple[np.ndarray, np.ndarray, float]:
    residual = np.asarray(source - matrix @ raw)
    shift = max(0.0, float(np.max(-residual / (alpha * root_degree))))
    published = np.maximum(raw - shift * root_degree, 0.0)
    published_residual = np.asarray(source - matrix @ published)
    if np.min(published_residual) < -1e-9:
        raise AssertionError("safe publication lost the subsolution residual")
    return published, published_residual, max(0.0, 1.0 - float(root_degree @ published))


def fixed_envelope_scratch(
    matrix,
    source: np.ndarray,
    root_degree: np.ndarray,
    alpha: float,
    initial: np.ndarray | None = None,
    *,
    require_trigger: bool = False,
) -> tuple[np.ndarray | None, int]:
    """CG signed scratch, tested only through the safe publication interface."""
    size = len(source)
    volume = int(round(float(root_degree @ root_degree)))
    target_residual = alpha**1.5 / (2.0 * np.sqrt(volume) * (1.0 + np.sqrt(volume)))
    raw = np.zeros(size) if initial is None else initial.copy()
    published, _published_residual, deficit = safe_publication(
        matrix, source, root_degree, raw, alpha
    )
    if deficit <= np.sqrt(alpha) * (1.0 + 1e-10):
        return published, 0
    residual = np.asarray(source - matrix @ raw)
    direction = residual.copy()
    residual_squared = float(residual @ residual)
    iterations = 0
    if residual_squared == 0.0:
        published, _r, deficit = safe_publication(matrix, source, root_degree, raw, alpha)
        return (published if deficit <= np.sqrt(alpha) else None), iterations
    # In exact arithmetic CG terminates in at most |E| steps.  The extra
    # numerical guard permits a few cleanup steps near repeated eigenvalues.
    for _ in range(max(1, 2 * size)):
        image = np.asarray(matrix @ direction)
        denominator = float(direction @ image)
        if denominator <= 0.0:
            raise AssertionError("principal PPR matrix is not positive definite")
        step = residual_squared / denominator
        raw = raw + step * direction
        following_residual = residual - step * image
        iterations += 1
        published, _published_residual, deficit = safe_publication(
            matrix, source, root_degree, raw, alpha
        )
        if deficit <= np.sqrt(alpha) * (1.0 + 1e-10):
            return published, iterations
        following_squared = float(following_residual @ following_residual)
        if not require_trigger and np.sqrt(following_squared) <= target_residual:
            return None, iterations
        if following_squared <= 1e-30:
            return None, iterations
        direction = following_residual + (following_squared / residual_squared) * direction
        residual = following_residual
        residual_squared = following_squared
    raise RuntimeError("CG scratch exceeded its numerical guard")


def priority_cleanup(
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int,
    checkpoint: np.ndarray,
) -> tuple[np.ndarray, int]:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    residual = np.asarray(source - matrix @ checkpoint)
    if np.min(residual) < -1e-8:
        raise AssertionError("cleanup checkpoint is not a global subsolution")
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    versions = np.zeros(len(adjacency), dtype=np.int64)
    heap: list[tuple[float, int, int]] = []
    for vertex in np.flatnonzero(residual > 0.0):
        heapq.heappush(
            heap,
            (-residual[vertex] / root_degree[vertex], int(vertex), 0),
        )
    output = checkpoint.copy()
    work = 0
    while heap:
        _negative_key, vertex, version = heapq.heappop(heap)
        if version != versions[vertex] or residual[vertex] <= 0.0:
            continue
        if residual[vertex] / root_degree[vertex] <= alpha * epsilon:
            break
        value = residual[vertex]
        step = value / diagonal
        output[vertex] += step
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
    return output, work


def geometric_radii(
    adjacency: list[list[int]], seed: int, cap: int
) -> list[tuple[int, np.ndarray, int]]:
    degree = np.asarray([len(row) for row in adjacency], dtype=int)
    distance = distances(adjacency, seed)
    radii = []
    last_volume = 0
    maximum_radius = int(np.max(distance))
    for radius in range(maximum_radius + 1):
        envelope = distance <= radius
        volume = int(np.sum(degree[envelope]))
        if volume > cap:
            break
        if not radii or volume >= 2 * last_volume or radius == maximum_radius:
            radii.append((radius, envelope, volume))
            last_volume = volume
    return radii


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> ScreenRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    full_solution = np.asarray(spsolve(matrix, source))
    _direct_vector, _direct_support, direct_work, _direct_pushes = appr_envelope(
        adjacency, alpha, epsilon, seed
    )

    cap = max(1, int(np.floor(2.0 / epsilon)))
    attempts = geometric_radii(adjacency, seed, cap)
    scratch_iterations = scratch_work = 0
    triggered = None
    trigger_radius = -1
    trigger_volume = 0
    for radius, envelope, volume in attempts:
        indices = np.flatnonzero(envelope)
        principal = matrix[indices][:, indices]
        restricted_source = source[indices]
        restricted_degree = root_degree[indices]
        publication, iterations = fixed_envelope_scratch(
            principal,
            restricted_source,
            restricted_degree,
            alpha,
        )
        scratch_iterations += iterations
        scratch_work += iterations * volume
        if publication is None:
            continue
        triggered = np.zeros(len(adjacency))
        triggered[indices] = publication
        trigger_radius = radius
        trigger_volume = volume
        break

    exposure_work = attempts[-1][2] if attempts else 0
    cleanup_work = fallback_work = 0
    if triggered is not None:
        output, cleanup_work = priority_cleanup(adjacency, alpha, epsilon, seed, triggered)
        published_deficit = max(0.0, 1.0 - float(root_degree @ triggered))
    else:
        fallback_vector, fallback_support, fallback_work, _pushes = appr_envelope(
            adjacency, alpha, epsilon, seed
        )
        output = np.sqrt(degree) * np.where(fallback_support, fallback_vector, 0.0)
        published_deficit = float("nan")
    semantic_error = float(np.max(np.abs((output - full_solution) / root_degree)))
    if semantic_error > epsilon * (1.0 + 1e-7):
        raise AssertionError("hard-capped mass-screen lane missed semantic target")
    total_work = exposure_work + scratch_work + cleanup_work + fallback_work
    ratio = total_work / direct_work if direct_work else (0.0 if total_work == 0 else np.inf)
    return ScreenRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        cap,
        triggered is not None,
        trigger_radius,
        trigger_volume,
        exposure_work,
        scratch_iterations,
        scratch_work,
        cleanup_work,
        fallback_work,
        total_work,
        direct_work,
        ratio,
        semantic_error,
        published_deficit,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
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
    alphas = (0.04, 0.16) if args.quick else (0.01, 0.04, 0.16)
    epsilons = (0.1,) if args.quick else (0.05, 0.1)
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
            f"W={row.total_work}",
            f"ratio={row.work_ratio:.2f}",
            f"err={row.semantic_error:.2e}",
        )


if __name__ == "__main__":
    main()
