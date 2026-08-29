#!/usr/bin/env python3
"""Compare APPR and gap-threshold two-stage point-source lanes."""

from __future__ import annotations

import argparse
import csv
import heapq
import math
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def add_edge(adjacency: list[list[int]], left: int, right: int) -> None:
    adjacency[left].append(right)
    adjacency[right].append(left)


def path_graph(size: int) -> list[list[int]]:
    adjacency = [[] for _ in range(size)]
    for vertex in range(size - 1):
        add_edge(adjacency, vertex, vertex + 1)
    return adjacency


def cycle_graph(size: int) -> list[list[int]]:
    adjacency = path_graph(size)
    add_edge(adjacency, 0, size - 1)
    return adjacency


def star_graph(leaves: int) -> list[list[int]]:
    adjacency = [[] for _ in range(leaves + 1)]
    for leaf in range(1, leaves + 1):
        add_edge(adjacency, 0, leaf)
    return adjacency


def binary_tree(depth: int) -> list[list[int]]:
    size = 2 ** (depth + 1) - 1
    adjacency = [[] for _ in range(size)]
    for vertex in range((size - 1) // 2):
        add_edge(adjacency, vertex, 2 * vertex + 1)
        add_edge(adjacency, vertex, 2 * vertex + 2)
    return adjacency


def broom_graph(handle: int, leaves: int) -> list[list[int]]:
    adjacency = path_graph(handle + 1)
    for _ in range(leaves):
        adjacency.append([])
        add_edge(adjacency, handle, len(adjacency) - 1)
    return adjacency


def grid_graph(rows: int, columns: int) -> list[list[int]]:
    adjacency = [[] for _ in range(rows * columns)]
    for row in range(rows):
        for column in range(columns):
            vertex = row * columns + column
            if row + 1 < rows:
                add_edge(adjacency, vertex, vertex + columns)
            if column + 1 < columns:
                add_edge(adjacency, vertex, vertex + 1)
    return adjacency


def normalized_matrix(adjacency: list[list[int]], alpha: float):
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    rows = list(range(len(adjacency)))
    columns = list(range(len(adjacency)))
    values = [diagonal for _ in adjacency]
    for vertex, neighbors in enumerate(adjacency):
        for neighbor in neighbors:
            rows.append(vertex)
            columns.append(neighbor)
            values.append(-coupling / np.sqrt(degree[vertex] * degree[neighbor]))
    matrix = coo_matrix((values, (rows, columns)), shape=(len(adjacency),) * 2).tocsr()
    return degree, matrix


def obstacle_objective(
    adjacency: list[list[int]],
    alpha: float,
    rho: float,
    vector: np.ndarray,
    seed: int,
) -> float:
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    energy = diagonal * np.dot(degree * vector, vector)
    for vertex, neighbors in enumerate(adjacency):
        energy -= coupling * vector[vertex] * sum(vector[neighbor] for neighbor in neighbors)
    load = -alpha * rho * degree
    load[seed] += alpha
    return 0.5 * energy - np.dot(load, vector)


@dataclass(frozen=True)
class CoordinateResult:
    vector: np.ndarray
    work: int
    objective: float
    pushes: int


def monotone_obstacle(
    adjacency: list[list[int]],
    alpha: float,
    rho: float,
    seed: int,
    *,
    residual_tolerance: float = 1e-14,
    target_gap: float | None = None,
    optimum_value: float | None = None,
    target_mapping: float | None = None,
) -> CoordinateResult:
    """Monotone exact-coordinate obstacle relaxations in degree-unscaled y."""
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    diagonal = (1.0 + alpha) * degree / 2.0
    coupling = (1.0 - alpha) / 2.0
    load = -alpha * rho * degree
    load[seed] += alpha
    residual = load.copy()
    vector = np.zeros(len(adjacency))
    queue = deque(int(i) for i in np.flatnonzero(residual > residual_tolerance))
    queued = np.zeros(len(adjacency), dtype=bool)
    queued[list(queue)] = True
    objective = 0.0
    work = 0
    pushes = 0
    if target_mapping is not None:
        mapping_norm = np.sqrt(np.sum(np.maximum(residual, 0.0) ** 2 / degree))
        if mapping_norm <= target_mapping:
            return CoordinateResult(vector, work, objective, pushes)
    while queue:
        vertex = queue.popleft()
        queued[vertex] = False
        value = residual[vertex]
        if value <= residual_tolerance:
            continue
        step = value / diagonal[vertex]
        vector[vertex] += step
        residual[vertex] = 0.0
        objective -= value * value / (2.0 * diagonal[vertex])
        work += int(degree[vertex])
        pushes += 1
        for neighbor in adjacency[vertex]:
            residual[neighbor] += coupling * step
            if residual[neighbor] > residual_tolerance and not queued[neighbor]:
                queue.append(neighbor)
                queued[neighbor] = True
        if target_gap is not None and objective - float(optimum_value) <= target_gap:
            break
        if target_mapping is not None:
            mapping_norm = np.sqrt(np.sum(np.maximum(residual, 0.0) ** 2 / degree))
            if mapping_norm <= target_mapping:
                break
    return CoordinateResult(vector, work, objective, pushes)


def priority_obstacle(
    adjacency: list[list[int]],
    alpha: float,
    rho: float,
    seed: int,
    *,
    target_density: float,
) -> CoordinateResult:
    """Positive-residual priority GS with a lazy normalized-key heap."""
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    diagonal = (1.0 + alpha) * degree / 2.0
    coupling = (1.0 - alpha) / 2.0
    load = -alpha * rho * degree
    load[seed] += alpha
    residual = load.copy()
    vector = np.zeros(len(adjacency))
    versions = np.zeros(len(adjacency), dtype=np.int64)
    heap: list[tuple[float, int, int]] = []
    for vertex in np.flatnonzero(residual > 0.0):
        heapq.heappush(
            heap,
            (-residual[vertex] / degree[vertex], int(vertex), 0),
        )
    objective = 0.0
    work = 0
    pushes = 0
    while True:
        while heap:
            _key, vertex, version = heapq.heappop(heap)
            if version == versions[vertex] and residual[vertex] > 0.0:
                break
        else:
            break
        if residual[vertex] / degree[vertex] <= target_density:
            break
        value = residual[vertex]
        step = value / diagonal[vertex]
        vector[vertex] += step
        residual[vertex] = 0.0
        versions[vertex] += 1
        objective -= value * value / (2.0 * diagonal[vertex])
        work += int(degree[vertex])
        pushes += 1
        for neighbor in adjacency[vertex]:
            residual[neighbor] += coupling * step
            versions[neighbor] += 1
            if residual[neighbor] > 0.0:
                heapq.heappush(
                    heap,
                    (
                        -residual[neighbor] / degree[neighbor],
                        neighbor,
                        int(versions[neighbor]),
                    ),
                )
    return CoordinateResult(vector, work, objective, pushes)


def appr_envelope(
    adjacency: list[list[int]], alpha: float, rho: float, seed: int
) -> tuple[np.ndarray, np.ndarray, int, int]:
    """Classical residual-coordinate APPR at normalized threshold alpha*rho."""
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    diagonal = (1.0 + alpha) * degree / 2.0
    coupling = (1.0 - alpha) / 2.0
    residual = np.zeros(len(adjacency))
    residual[seed] = alpha
    vector = np.zeros(len(adjacency))
    threshold = alpha * rho * degree
    queue = deque(int(i) for i in np.flatnonzero(residual >= threshold))
    queued = np.zeros(len(adjacency), dtype=bool)
    queued[list(queue)] = True
    work = 0
    pushes = 0
    while queue:
        vertex = queue.popleft()
        queued[vertex] = False
        value = residual[vertex]
        if value < threshold[vertex]:
            continue
        step = value / diagonal[vertex]
        vector[vertex] += step
        residual[vertex] = 0.0
        work += int(degree[vertex])
        pushes += 1
        for neighbor in adjacency[vertex]:
            residual[neighbor] += coupling * step
            if residual[neighbor] >= threshold[neighbor] and not queued[neighbor]:
                queue.append(neighbor)
                queued[neighbor] = True
    return vector, vector > 0.0, work, pushes


def radius_screen(
    adjacency: list[list[int]],
    radius: int,
    cap: float,
    seed: int,
) -> tuple[np.ndarray, int, bool]:
    """Try the certified point-source support ball under a hard volume cap."""
    degree = np.asarray([len(row) for row in adjacency], dtype=int)
    retained = np.zeros(len(adjacency), dtype=bool)
    retained[seed] = True
    volume = int(degree[seed])
    if volume > cap:
        return retained, 0, False
    queue = deque([(seed, 0)])
    while queue:
        vertex, distance = queue.popleft()
        if distance >= radius:
            continue
        for neighbor in adjacency[vertex]:
            if retained[neighbor]:
                continue
            candidate_volume = volume + int(degree[neighbor])
            if candidate_volume > cap:
                return retained, volume, False
            retained[neighbor] = True
            volume = candidate_volume
            queue.append((neighbor, distance + 1))
    # Charge one complete materialization of the successful set; it also
    # prepares the principal rows for the optional tail.
    return retained, volume, True


def handoff_semantic_error(
    vector: np.ndarray,
    envelope: np.ndarray,
    degree: np.ndarray,
    full_solution: np.ndarray,
) -> float:
    """Semantic error of the positive, envelope-truncated unscaled vector."""
    output = np.where(envelope, np.maximum(vector, 0.0), 0.0)
    return float(np.max(np.abs(output - full_solution / np.sqrt(degree))))


def accelerated_linear_tail(
    matrix,
    degree: np.ndarray,
    seed: int,
    envelope: np.ndarray,
    alpha: float,
    tolerance: float,
    full_solution: np.ndarray,
) -> tuple[int, int, float]:
    indices = np.flatnonzero(envelope)
    if len(indices) == 0:
        error = float(np.max(np.abs(full_solution / np.sqrt(degree))))
        return 0, 0, error
    principal = matrix[indices][:, indices]
    source = np.zeros(len(indices))
    positions = {int(vertex): position for position, vertex in enumerate(indices)}
    if seed in positions:
        source[positions[seed]] = alpha / np.sqrt(degree[seed])
    target = np.asarray(spsolve(principal, source))
    previous = np.zeros(len(indices))
    current = np.zeros(len(indices))
    beta = (1.0 - np.sqrt(alpha)) / (1.0 + np.sqrt(alpha))
    iteration = 0
    while True:
        error = np.max(np.abs((current - target) / np.sqrt(degree[indices])))
        if error <= tolerance:
            break
        momentum = current + beta * (current - previous)
        following = momentum - (principal @ momentum - source)
        previous, current = current, np.asarray(following)
        iteration += 1
        if iteration > 100_000:
            raise RuntimeError("accelerated tail did not converge")
    output = np.zeros(len(degree))
    output[indices] = np.maximum(current, 0.0)
    semantic_error = float(np.max(np.abs((output - full_solution) / np.sqrt(degree))))
    volume = int(np.sum(degree[indices]))
    return iteration, iteration * volume, semantic_error


@dataclass(frozen=True)
class Row:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    engine: str
    stage1_work: int
    stage1_pushes: int
    envelope_volume: int
    reference_support_volume: int
    handoff_semantic_error: float
    tail_iterations: int
    stage2_work: int
    total_work: int
    semantic_error: float
    screen_succeeded: bool | None = None


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> list[Row]:
    degree, matrix = normalized_matrix(adjacency, alpha)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / np.sqrt(degree[seed])
    full_solution = np.asarray(spsolve(matrix, source))
    rows = []

    # Fair direct-return baselines.  Both stop from an observable residual
    # certificate and therefore need no restricted linear tail.
    direct_appr_vector, direct_appr_support, direct_appr_work, direct_appr_pushes = appr_envelope(
        adjacency, alpha, epsilon, seed
    )
    direct_appr_error = handoff_semantic_error(
        direct_appr_vector, direct_appr_support, degree, full_solution
    )
    if direct_appr_error > epsilon * (1.0 + 1e-8):
        raise AssertionError("direct APPR missed semantic target")
    direct_reference = monotone_obstacle(adjacency, alpha, epsilon, seed)
    rows.append(
        Row(
            family,
            len(adjacency),
            alpha,
            epsilon,
            "appr-direct-ppr",
            direct_appr_work,
            direct_appr_pushes,
            int(np.sum(degree[direct_appr_support])),
            int(np.sum(degree[direct_reference.vector > 1e-11])),
            direct_appr_error,
            0,
            0,
            direct_appr_work,
            direct_appr_error,
        )
    )

    # A genuinely set-only lane: point-source Green decay certifies that the
    # PPR amplitude outside this ball is at most eps/2.  Abort before the ball
    # exceeds 2/eps degree volume; failure falls back to direct APPR.
    delta = epsilon / 2.0
    if alpha >= 1.0:
        green_radius = 0
    else:
        denominator = math.log((1.0 + math.sqrt(alpha)) / (1.0 - math.sqrt(alpha)))
        green_radius = max(0, math.ceil(math.log(2.0 / delta) / denominator) - 1)
    radius_envelope, radius_work, radius_success = radius_screen(
        adjacency,
        green_radius,
        2.0 / epsilon,
        seed,
    )
    if radius_success:
        outside = np.logical_not(radius_envelope)
        if np.any(full_solution[outside] / np.sqrt(degree[outside]) > delta * (1.0 + 1e-8)):
            raise AssertionError("certified Green ball missed exterior amplitude bound")
        radius_iterations, radius_tail_work, radius_error = accelerated_linear_tail(
            matrix,
            degree,
            seed,
            radius_envelope,
            alpha,
            epsilon / 2.0,
            full_solution,
        )
        if radius_error > epsilon * (1.0 + 1e-8):
            raise AssertionError("radius-screen lane missed semantic target")
        rows.append(
            Row(
                family,
                len(adjacency),
                alpha,
                epsilon,
                "green-ball-screen-or-appr",
                radius_work,
                0,
                int(np.sum(degree[radius_envelope])),
                int(np.sum(degree)),
                float("nan"),
                radius_iterations,
                radius_tail_work,
                radius_work + radius_tail_work,
                radius_error,
                True,
            )
        )
    else:
        rows.append(
            Row(
                family,
                len(adjacency),
                alpha,
                epsilon,
                "green-ball-screen-or-appr",
                radius_work + direct_appr_work,
                direct_appr_pushes,
                int(np.sum(degree[direct_appr_support])),
                int(np.sum(degree[direct_reference.vector > 1e-11])),
                direct_appr_error,
                0,
                0,
                radius_work + direct_appr_work,
                direct_appr_error,
                False,
            )
        )

    direct_priority = priority_obstacle(
        adjacency,
        alpha,
        0.0,
        seed,
        target_density=alpha * epsilon,
    )
    direct_priority_support = direct_priority.vector > 0.0
    direct_priority_error = handoff_semantic_error(
        direct_priority.vector, direct_priority_support, degree, full_solution
    )
    if direct_priority_error > epsilon * (1.0 + 1e-8):
        raise AssertionError("direct priority SOR missed semantic target")
    rows.append(
        Row(
            family,
            len(adjacency),
            alpha,
            epsilon,
            "priority-gs-direct-ppr",
            direct_priority.work,
            direct_priority.pushes,
            int(np.sum(degree[direct_priority_support])),
            int(np.sum(degree)),
            direct_priority_error,
            0,
            0,
            direct_priority.work,
            direct_priority_error,
        )
    )

    rho = epsilon / 2.0
    reference = monotone_obstacle(adjacency, alpha, rho, seed)
    support = reference.vector > 1e-11
    appr_vector, envelope, discovery_work, pushes = appr_envelope(adjacency, alpha, rho, seed)
    if not np.all(envelope[support]):
        raise AssertionError("APPR envelope missed reference RPPR support")
    direct_error = handoff_semantic_error(appr_vector, envelope, degree, full_solution)
    if direct_error > epsilon * (1.0 + 1e-8):
        raise AssertionError("APPR handoff vector missed semantic target")
    tail_iterations, tail_work, error = accelerated_linear_tail(
        matrix, degree, seed, envelope, alpha, epsilon / 2.0, full_solution
    )
    if error > epsilon * (1.0 + 1e-8):
        raise AssertionError("APPR two-stage lane missed semantic target")
    rows.append(
        Row(
            family,
            len(adjacency),
            alpha,
            epsilon,
            "appr-envelope",
            discovery_work,
            pushes,
            int(np.sum(degree[envelope])),
            int(np.sum(degree[support])),
            direct_error,
            tail_iterations,
            tail_work,
            discovery_work + tail_work,
            error,
        )
    )

    rho = delta = tolerance = epsilon / 3.0
    reference = monotone_obstacle(adjacency, alpha, rho, seed)
    optimum_value = obstacle_objective(adjacency, alpha, rho, reference.vector, seed)
    target_gap = alpha * delta * delta / 8.0
    checkpoint = monotone_obstacle(
        adjacency,
        alpha,
        rho,
        seed,
        target_gap=target_gap,
        optimum_value=optimum_value,
    )
    envelope = checkpoint.vector > delta / 2.0
    outside = np.logical_not(envelope)
    if np.any(reference.vector[outside] > delta * (1.0 + 1e-8)):
        raise AssertionError("gap-threshold lane failed approximate-envelope certificate")
    if np.sum(degree[envelope]) >= 2.0 / delta + 1e-8:
        raise AssertionError("gap-threshold envelope exceeded its mass bound")
    direct_error = handoff_semantic_error(checkpoint.vector, envelope, degree, full_solution)
    if direct_error > epsilon * (1.0 + 1e-8):
        raise AssertionError("gap-threshold handoff vector missed semantic target")
    tail_iterations, tail_work, error = accelerated_linear_tail(
        matrix, degree, seed, envelope, alpha, tolerance, full_solution
    )
    if error > epsilon * (1.0 + 1e-8):
        raise AssertionError("gap-threshold two-stage lane missed semantic target")
    support = reference.vector > 1e-11
    rows.append(
        Row(
            family,
            len(adjacency),
            alpha,
            epsilon,
            "gs-gap-envelope-oracle-stop",
            checkpoint.work,
            checkpoint.pushes,
            int(np.sum(degree[envelope])),
            int(np.sum(degree[support])),
            direct_error,
            tail_iterations,
            tail_work,
            checkpoint.work + tail_work,
            error,
        )
    )

    mapping_checkpoint = priority_obstacle(
        adjacency,
        alpha,
        rho,
        seed,
        target_density=alpha * delta / 2.0,
    )
    envelope = mapping_checkpoint.vector > delta / 2.0
    outside = np.logical_not(envelope)
    if np.any(reference.vector[outside] > delta * (1.0 + 1e-8)):
        raise AssertionError("residual-threshold lane failed approximate envelope")
    direct_error = handoff_semantic_error(
        mapping_checkpoint.vector, envelope, degree, full_solution
    )
    if direct_error > epsilon * (1.0 + 1e-8):
        raise AssertionError("positive-key handoff vector missed semantic target")
    tail_iterations, tail_work, error = accelerated_linear_tail(
        matrix, degree, seed, envelope, alpha, tolerance, full_solution
    )
    if error > epsilon * (1.0 + 1e-8):
        raise AssertionError("residual-threshold two-stage lane missed semantic target")
    rows.append(
        Row(
            family,
            len(adjacency),
            alpha,
            epsilon,
            "priority-gs-positive-key-envelope",
            mapping_checkpoint.work,
            mapping_checkpoint.pushes,
            int(np.sum(degree[envelope])),
            int(np.sum(degree[support])),
            direct_error,
            tail_iterations,
            tail_work,
            mapping_checkpoint.work + tail_work,
            error,
        )
    )

    # The leading proxy W_disc + W_tail is minimized at rho/delta=alpha^{-1/4}.
    # Keep a fixed quarter of the semantic budget for the terminal solve and
    # tune the remaining two budgets accordingly.
    tolerance = epsilon / 4.0
    remaining = epsilon - tolerance
    alpha_quarter = alpha**0.25
    rho = remaining / (1.0 + alpha_quarter)
    delta = remaining * alpha_quarter / (1.0 + alpha_quarter)
    reference = monotone_obstacle(adjacency, alpha, rho, seed)
    mapping_checkpoint = priority_obstacle(
        adjacency,
        alpha,
        rho,
        seed,
        target_density=alpha * delta / 2.0,
    )
    envelope = mapping_checkpoint.vector > delta / 2.0
    outside = np.logical_not(envelope)
    if np.any(reference.vector[outside] > delta * (1.0 + 1e-8)):
        raise AssertionError("tuned residual lane failed approximate envelope")
    direct_error = handoff_semantic_error(
        mapping_checkpoint.vector, envelope, degree, full_solution
    )
    if direct_error > epsilon * (1.0 + 1e-8):
        raise AssertionError("tuned positive-key handoff vector missed semantic target")
    tail_iterations, tail_work, error = accelerated_linear_tail(
        matrix, degree, seed, envelope, alpha, tolerance, full_solution
    )
    if error > epsilon * (1.0 + 1e-8):
        raise AssertionError("tuned residual two-stage lane missed semantic target")
    support = reference.vector > 1e-11
    rows.append(
        Row(
            family,
            len(adjacency),
            alpha,
            epsilon,
            "priority-gs-positive-key-envelope-tuned",
            mapping_checkpoint.work,
            mapping_checkpoint.pushes,
            int(np.sum(degree[envelope])),
            int(np.sum(degree[support])),
            direct_error,
            tail_iterations,
            tail_work,
            mapping_checkpoint.work + tail_work,
            error,
        )
    )
    return rows


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
    alphas = [0.01, 0.04] if args.quick else [0.01, 0.04, 0.16]
    epsilons = [0.1] if args.quick else [0.05, 0.1]
    rows = [
        row
        for family, adjacency in graphs
        for alpha in alphas
        for epsilon in epsilons
        for row in run_case(family, adjacency, alpha, epsilon)
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
            row.engine,
            f"W=({row.stage1_work}+{row.stage2_work})",
            f"V={row.envelope_volume}",
            f"err={row.semantic_error:.3e}",
        )


if __name__ == "__main__":
    main()
