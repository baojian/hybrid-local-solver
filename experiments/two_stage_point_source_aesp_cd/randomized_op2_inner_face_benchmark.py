#!/usr/bin/env python3
"""Algebraic prototype of the randomized-OP2 two-stage transfer.

This is not an implementation of the Koutis--Miller--Peng solver.  Each face
is solved directly, then perturbed in a random direction whose active residual
passes exactly the deterministic certificate required by the OP2 wrapper.
The experiment therefore stresses every post-solver decision against an
adversarially shaped accepted error while keeping the source black box honest.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

try:
    from .portfolio_benchmark import (
        binary_tree,
        broom_graph,
        cycle_graph,
        grid_graph,
        normalized_matrix,
        path_graph,
        star_graph,
    )
except ImportError:  # pragma: no cover - direct script execution
    from portfolio_benchmark import (
        binary_tree,
        broom_graph,
        cycle_graph,
        grid_graph,
        normalized_matrix,
        path_graph,
        star_graph,
    )


@dataclass(frozen=True)
class TransferRow:
    graph: str
    budget: str
    vertices: int
    alpha: float
    epsilon: float
    rho: float
    eta: float
    tau: float
    phases: int
    stop: str
    active_vertices: int
    support_vertices: int
    omitted_support_vertices: int
    active_volume: int
    support_volume: int
    cumulative_face_volume: int
    maximum_certified_residual_ratio: float
    face_gap_ratio: float
    theorem_gap_ratio: float
    direct_semantic_ratio: float
    stage2_certified_residual_ratio: float
    stage2_semantic_ratio: float


def face_solve(matrix, load: np.ndarray, active: set[int]) -> np.ndarray:
    indices = np.asarray(sorted(active), dtype=int)
    point = np.zeros(len(load))
    point[indices] = spsolve(matrix[indices][:, indices], load[indices])
    return point


def graph_boundary(adjacency: list[list[int]], active: set[int]) -> set[int]:
    return {
        neighbor for vertex in active for neighbor in adjacency[vertex] if neighbor not in active
    }


def obstacle_optimum(matrix, load: np.ndarray, seed: int) -> tuple[np.ndarray, set[int]]:
    active = {seed}
    for _ in range(len(load)):
        point = face_solve(matrix, load, active)
        residual = load - matrix @ point
        batch = {
            vertex
            for vertex in graph_boundary_from_matrix(matrix, active)
            if residual[vertex] > 5.0e-12
        }
        if not batch:
            return point, active
        active |= batch
    raise AssertionError("exact positive-batch reference did not terminate")


def graph_boundary_from_matrix(matrix, active: set[int]) -> set[int]:
    boundary: set[int] = set()
    for vertex in active:
        start, stop = matrix.indptr[vertex], matrix.indptr[vertex + 1]
        for neighbor in matrix.indices[start:stop]:
            neighbor = int(neighbor)
            if neighbor != vertex and neighbor not in active:
                boundary.add(neighbor)
    return boundary


def objective(matrix, load: np.ndarray, point: np.ndarray) -> float:
    return 0.5 * float(point @ (matrix @ point)) - float(load @ point)


def accepted_random_face_point(
    matrix,
    load: np.ndarray,
    active: set[int],
    exact: np.ndarray,
    residual_target: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, float]:
    indices = np.asarray(sorted(active), dtype=int)
    direction = rng.normal(size=len(indices))
    image = matrix[indices][:, indices] @ direction
    image_norm = float(np.linalg.norm(image))
    if image_norm == 0.0:
        return exact.copy(), 0.0
    requested = residual_target * (0.55 + 0.35 * float(rng.random()))
    point = exact.copy()
    point[indices] += requested * direction / image_norm
    residual = matrix[indices][:, indices] @ point[indices] - load[indices]
    ratio = float(np.linalg.norm(residual)) / residual_target
    assert ratio <= 1.0 + 2.0e-10
    return point, ratio


def run_case(
    name: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    rho: float,
    seed: int,
    random_seed: int,
    budget: str = "balanced",
) -> TransferRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    ppr_load = np.zeros(len(adjacency))
    ppr_load[seed] = alpha / root_degree[seed]
    eta = (epsilon - rho) / 2.0
    tau = epsilon - rho - eta
    assert rho > 0.0 and eta > 0.0 and tau > 0.0
    rppr_load = ppr_load - alpha * rho * root_degree
    full_ppr = spsolve(matrix, ppr_load)
    optimum, support = obstacle_optimum(matrix, rppr_load, seed)
    optimum_value = objective(matrix, rppr_load, optimum)

    eps_obj = alpha * eta * eta / 2.0
    threshold = math.sqrt(alpha * rho * eps_obj) / 8.0
    numerical_target = threshold / 4.0
    q_alpha = (math.sqrt(2.0 / alpha) - 1.0) / (math.sqrt(2.0 / alpha) + 1.0)
    phase_cap = math.ceil(math.log(64.0 / eps_obj) / (2.0 * math.log(1.0 / q_alpha)))
    rng = np.random.default_rng(random_seed)

    active = {seed}
    cumulative_volume = 0
    maximum_residual_ratio = 0.0
    stop = "cap"
    accepted = None
    exact_face = None
    phase = 0
    for phase in range(phase_cap + 1):
        exact_face = face_solve(matrix, rppr_load, active)
        cumulative_volume += int(degree[list(active)].sum())
        accepted, residual_ratio = accepted_random_face_point(
            matrix,
            rppr_load,
            active,
            exact_face,
            numerical_target * math.sqrt(alpha),
            rng,
        )
        maximum_residual_ratio = max(maximum_residual_ratio, residual_ratio)
        if phase == phase_cap:
            break
        approximate_residual = rppr_load - matrix @ accepted
        batch = {
            vertex
            for vertex in graph_boundary(adjacency, active)
            if approximate_residual[vertex] > threshold / 2.0
        }
        exact_residual = rppr_load - matrix @ exact_face
        assert all(exact_residual[vertex] > threshold / 4.0 for vertex in batch)
        assert batch <= support
        if not batch:
            stop = "empty"
            break
        active |= batch

    assert accepted is not None and exact_face is not None
    face_gap = objective(matrix, rppr_load, exact_face) - optimum_value
    theorem_gap = 8.0 * q_alpha ** (2 * phase) + threshold**2 / (alpha * rho)
    assert face_gap <= theorem_gap + 2.0e-9
    assert face_gap <= eps_obj * (1.0 + 2.0e-6)

    exact_stage2 = face_solve(matrix, ppr_load, active)
    approximate_stage2, stage2_residual_ratio = accepted_random_face_point(
        matrix,
        ppr_load,
        active,
        exact_stage2,
        alpha * tau,
        rng,
    )
    direct = np.maximum(accepted, 0.0)
    stage2 = np.maximum(approximate_stage2, 0.0)
    direct_error = float(np.max(np.abs(direct - full_ppr) / root_degree))
    stage2_error = float(np.max(np.abs(stage2 - full_ppr) / root_degree))
    assert direct_error <= epsilon * (1.0 + 5.0e-6)
    assert stage2_error <= epsilon * (1.0 + 5.0e-6)

    active_volume = int(degree[list(active)].sum())
    support_volume = int(degree[list(support)].sum())
    assert active_volume <= support_volume <= 1.0 / rho + 1.0e-8
    return TransferRow(
        graph=name,
        budget=budget,
        vertices=len(adjacency),
        alpha=alpha,
        epsilon=epsilon,
        rho=rho,
        eta=eta,
        tau=tau,
        phases=phase + 1,
        stop=stop,
        active_vertices=len(active),
        support_vertices=len(support),
        omitted_support_vertices=len(support - active),
        active_volume=active_volume,
        support_volume=support_volume,
        cumulative_face_volume=cumulative_volume,
        maximum_certified_residual_ratio=maximum_residual_ratio,
        face_gap_ratio=face_gap / eps_obj,
        theorem_gap_ratio=face_gap / theorem_gap,
        direct_semantic_ratio=direct_error / epsilon,
        stage2_certified_residual_ratio=stage2_residual_ratio,
        stage2_semantic_ratio=stage2_error / epsilon,
    )


def random_tree(size: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    adjacency = [[] for _ in range(size)]
    for vertex in range(1, size):
        parent = rng.randrange(vertex)
        adjacency[vertex].append(parent)
        adjacency[parent].append(vertex)
    return adjacency


def graph_suite() -> list[tuple[str, list[list[int]], int]]:
    return [
        ("path", path_graph(96), 0),
        ("cycle", cycle_graph(96), 0),
        ("star", star_graph(95), 0),
        ("binary", binary_tree(6), 0),
        ("broom", broom_graph(64, 31), 0),
        ("grid", grid_graph(10, 10), 0),
        ("random_tree", random_tree(100, 17), 0),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("randomized_op2_inner_face_results.csv"),
    )
    args = parser.parse_args()

    rows = []
    for graph_index, (name, adjacency, seed) in enumerate(graph_suite()):
        for alpha in (0.01, 0.04, 0.16):
            for epsilon in (0.005, 0.01, 0.02):
                rows.append(
                    run_case(
                        name,
                        adjacency,
                        alpha,
                        epsilon,
                        epsilon / 2.0,
                        seed,
                        20260830 + 100 * graph_index + len(rows),
                    )
                )

    stress_graphs = [
        ("path_inner_face", path_graph(96)),
        ("cycle_inner_face", cycle_graph(96)),
        ("broom_inner_face", broom_graph(64, 31)),
        ("random_tree_inner_face", random_tree(100, 29)),
    ]
    for graph_index, (name, adjacency) in enumerate(stress_graphs):
        rows.append(
            run_case(
                name,
                adjacency,
                alpha=0.5,
                epsilon=0.1,
                rho=1.0e-12,
                seed=0,
                random_seed=20269900 + graph_index,
                budget="tiny-rho stress",
            )
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=TransferRow.__dataclass_fields__,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)

    incomplete = sum(row.omitted_support_vertices > 0 for row in rows)
    caps = sum(row.stop == "cap" for row in rows)
    print(f"cases: {len(rows)}")
    print(f"incomplete inner faces: {incomplete}")
    print(f"cap exits: {caps}")
    print(f"largest face-gap ratio: {max(row.face_gap_ratio for row in rows):.12g}")
    print(
        "largest direct/stage2 semantic ratios: "
        f"{max(row.direct_semantic_ratio for row in rows):.12g} / "
        f"{max(row.stage2_semantic_ratio for row in rows):.12g}"
    )


if __name__ == "__main__":
    main()
