#!/usr/bin/env python3
"""Fast heuristic search for beta-stopped masked-input-residual failures.

This is an unregistered floating-point falsification aid, not a proof.  It
implements only the canonical point-source retained-prox chronology needed by
the beta-stop question: input-residual frontier admission, one simultaneous
active diagonal push, maximal exterior append-and-push closure, and stopping
when the shifted residual width is at most ``beta * old_width``.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np


N20_EDGES = (
    (0, 1),
    (0, 11),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (7, 8),
    (7, 15),
    (8, 9),
    (9, 10),
    (10, 11),
    (10, 14),
    (11, 12),
    (11, 19),
    (12, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (15, 17),
    (15, 18),
    (16, 17),
    (17, 18),
    (18, 19),
)


def adjacency_from_edges(vertices: int, edges: list[tuple[int, int]]) -> np.ndarray:
    """Build a simple symmetric zero-diagonal adjacency matrix."""
    adjacency = np.zeros((vertices, vertices), dtype=float)
    for left, right in edges:
        adjacency[left, right] = 1.0
        adjacency[right, left] = 1.0
    return adjacency


def connected(adjacency: np.ndarray) -> bool:
    """Return whether every vertex is reachable from vertex zero."""
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in np.flatnonzero(adjacency[vertex]):
            neighbor = int(neighbor)
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(adjacency)


def edge_list(adjacency: np.ndarray) -> list[list[int]]:
    """Serialize the upper-triangular edge set."""
    return [
        [left, right]
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left, right]
    ]


def mutate(
    rng: np.random.Generator,
    adjacency: np.ndarray,
    flips: int,
) -> np.ndarray:
    """Flip edges while retaining a connected simple graph."""
    candidate = adjacency.copy()
    vertices = len(candidate)
    for _ in range(flips):
        left = int(rng.integers(vertices))
        right = int(rng.integers(vertices - 1))
        if right >= left:
            right += 1
        if left > right:
            left, right = right, left
        candidate[left, right] = candidate[right, left] = 1.0 - candidate[left, right]
    if np.min(candidate.sum(axis=1)) == 0 or not connected(candidate):
        return adjacency.copy()
    return candidate


def trace(
    adjacency: np.ndarray,
    alpha: float,
    rho_scale: float,
    beta: float,
    *,
    relative_width: float = 1.0e-3,
    maximum_products: int = 4000,
    maximum_phases: int = 1000,
    sign_floor: float = 1.0e-14,
) -> dict[str, object]:
    """Run the minimal beta-stopped chronology and return its first failure."""
    vertices = len(adjacency)
    degrees = adjacency.sum(axis=1)
    if np.min(degrees) <= 0 or not connected(adjacency):
        raise ValueError("the graph must be connected and nontrivial")
    if not 0.0 < beta < 0.5:
        raise ValueError("beta must lie in (0,1/2)")

    sqrt_degrees = np.sqrt(degrees)
    normalized_adjacency = adjacency / np.outer(sqrt_degrees, sqrt_degrees)
    original_diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    original_matrix = original_diagonal * np.eye(vertices) - coupling * normalized_adjacency
    shifted_matrix = original_matrix + alpha * np.eye(vertices)
    shifted_diagonal = np.diag(shifted_matrix)
    lipschitz = 1.0 + alpha
    shifted_gap = 2.0 * alpha
    root = math.sqrt(shifted_gap / lipschitz)
    momentum = (1.0 - root) / (1.0 + root)
    auxiliary_scale = (1.0 - root) / root
    rho = rho_scale / degrees[0]
    load = -alpha * rho * sqrt_degrees
    load[0] += alpha / sqrt_degrees[0]

    lower = np.zeros(vertices)
    certified = {0}
    width = 1.0 / degrees[0] - rho
    initial_width = width
    total_products = 0
    minimum_ratio = math.inf
    minimum_witness: dict[str, object] = {}
    chronology_beta_lower = 0.0
    chronology_beta_upper = 0.5
    phase = 0

    while width > relative_width * initial_width:
        if phase >= maximum_phases:
            return {
                "status": "phase_limit",
                "minimum_normalized_input_residual_over_old_width": minimum_ratio,
                "minimum_witness": minimum_witness,
                "phases": phase,
                "products": total_products,
            }
        old_lower = lower.copy()
        old_width = width
        shifted_load = load + alpha * old_lower
        current = old_lower.copy()
        previous = old_lower.copy()
        preceding_width = math.inf

        for product in range(1, maximum_products + 1):
            extrapolate = np.zeros(vertices)
            face = np.array(sorted(certified), dtype=int)
            extrapolate[face] = current[face] + momentum * (current[face] - previous[face])
            input_residual = shifted_load - shifted_matrix @ extrapolate
            outside = np.array(sorted(set(range(vertices)) - certified), dtype=int)
            if len(outside):
                scale = max(1.0, shifted_gap * old_width)
                batch = outside[input_residual[outside] > sign_floor * scale]
                certified.update(map(int, batch))
            face = np.array(sorted(certified), dtype=int)

            local = input_residual[face]
            local_vertex = int(np.argmin(local))
            value = float(local[local_vertex])
            vertex = int(face[local_vertex])
            ratio = value / (shifted_gap * sqrt_degrees[vertex] * old_width)
            # Phase-start momentum is reset, so product one is automatically
            # safe and often has a tiny tautological row.  Excluding it gives
            # the evolutionary objective a meaningful distance to the first
            # possible failure without changing any execution branch.
            if product > 1 and ratio < minimum_ratio:
                minimum_ratio = ratio
                minimum_witness = {
                    "phase_zero_based": phase,
                    "product_one_based": product,
                    "vertex": vertex,
                    "normalized_input_residual_over_old_width": ratio,
                    "preceding_inner_width_over_old_width": preceding_width / old_width,
                    "face_size": len(face),
                }
            if value < -sign_floor * max(1.0, shifted_gap * old_width):
                return {
                    "status": "counterexample",
                    "failure": minimum_witness,
                    "minimum_normalized_input_residual_over_old_width": minimum_ratio,
                    "same_chronology_stop_beta_interval": [
                        chronology_beta_lower,
                        chronology_beta_upper,
                    ],
                    "phases_before_failure": phase,
                    "products_before_failure": total_products,
                }

            following = np.zeros(vertices)
            following[face] = extrapolate[face] + input_residual[face] / lipschitz
            previous, current = current, following

            # The input cone makes the uniform lowerization shave exactly zero.
            lower[face] = np.maximum(lower[face], current[face])
            auxiliary = current + auxiliary_scale * (current - previous)
            current[face] = np.maximum(current[face], lower[face])
            auxiliary[face] = np.maximum(auxiliary[face], lower[face])
            previous[face] = current[face] - (auxiliary[face] - current[face]) / auxiliary_scale

            residual = shifted_load - shifted_matrix @ lower
            active = face[residual[face] > sign_floor * max(1.0, shifted_gap * old_width)]
            lower[active] += residual[active] / shifted_diagonal[active]
            residual = shifted_load - shifted_matrix @ lower
            current[face] = np.maximum(current[face], lower[face])
            auxiliary[face] = np.maximum(auxiliary[face], lower[face])
            previous[face] = current[face] - (auxiliary[face] - current[face]) / auxiliary_scale

            while True:
                outside = np.array(sorted(set(range(vertices)) - certified), dtype=int)
                if not len(outside):
                    break
                batch = outside[residual[outside] > sign_floor * max(1.0, shifted_gap * old_width)]
                if not len(batch):
                    break
                lower[batch] += residual[batch] / shifted_diagonal[batch]
                current[batch] = lower[batch]
                previous[batch] = lower[batch]
                auxiliary[batch] = lower[batch]
                certified.update(map(int, batch))
                residual = shifted_load - shifted_matrix @ lower

            total_products += 1
            inner_width = float(np.max(np.maximum(residual, 0.0) / (shifted_gap * sqrt_degrees)))
            if inner_width <= beta * old_width:
                chronology_beta_lower = max(
                    chronology_beta_lower,
                    inner_width / old_width,
                )
                width = old_width / 2.0 + inner_width
                break
            chronology_beta_upper = min(
                chronology_beta_upper,
                inner_width / old_width,
            )
            preceding_width = inner_width
        else:
            return {
                "status": "product_limit",
                "minimum_normalized_input_residual_over_old_width": minimum_ratio,
                "minimum_witness": minimum_witness,
            }
        phase += 1

    return {
        "status": "pass",
        "minimum_normalized_input_residual_over_old_width": minimum_ratio,
        "minimum_witness": minimum_witness,
        "phases": phase,
        "products": total_products,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=20)
    parser.add_argument("--alpha", type=float, default=1.0e-5)
    parser.add_argument("--rho-scale", type=float, default=923.0 / 20_000.0)
    parser.add_argument("--beta", type=float, default=1.0 / 3.0)
    parser.add_argument("--population", type=int, default=20)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260904)
    args = parser.parse_args()

    if args.vertices < 20:
        parser.error("the n20 seed requires at least 20 vertices")
    rng = np.random.default_rng(args.seed)
    seed_edges = list(N20_EDGES)
    for vertex in range(20, args.vertices):
        seed_edges.append((vertex - 1, vertex))
    seed_graph = adjacency_from_edges(args.vertices, seed_edges)
    population = [(seed_graph, args.rho_scale)]
    for _ in range(args.population - 1):
        population.append(
            (
                mutate(rng, seed_graph, int(rng.integers(1, max(2, args.vertices // 4)))),
                float(np.clip(args.rho_scale * 10 ** rng.normal(0.0, 0.4), 1.0e-9, 0.9)),
            )
        )

    best: tuple[tuple[float, float], np.ndarray, float, dict[str, object]] | None = None
    for generation in range(args.generations):
        ranked = []
        for adjacency, rho_scale in population:
            result = trace(adjacency, args.alpha, rho_scale, args.beta)
            failure = result.get("failure", {})
            predecessor = float(failure.get("preceding_inner_width_over_old_width", -math.inf))
            minimum = float(result["minimum_normalized_input_residual_over_old_width"])
            score = (predecessor, -minimum) if failure else (-math.inf, -minimum)
            ranked.append((score, adjacency, rho_scale, result))
            if best is None or score > best[0]:
                best = (score, adjacency.copy(), rho_scale, result)
        ranked.sort(key=lambda item: item[0], reverse=True)
        elites = ranked[: max(2, args.population // 4)]
        population = [(item[1].copy(), item[2]) for item in elites]
        while len(population) < args.population:
            parent = elites[int(rng.integers(len(elites)))]
            population.append(
                (
                    mutate(rng, parent[1], int(rng.integers(1, max(2, args.vertices // 5)))),
                    float(np.clip(parent[2] * 10 ** rng.normal(0.0, 0.25), 1.0e-9, 0.9)),
                )
            )
        if generation % 10 == 0 or generation + 1 == args.generations:
            assert best is not None
            print(
                json.dumps(
                    {
                        "generation": generation,
                        "score": best[0],
                        "rho_scale": best[2],
                        "result": best[3],
                        "edge_count": int(best[1].sum() // 2),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    assert best is not None
    print(
        json.dumps(
            {
                "warning": "floating-point adversary search, not a proof",
                "vertices": args.vertices,
                "alpha": args.alpha,
                "beta": args.beta,
                "rho_scale": best[2],
                "score": best[0],
                "result": best[3],
                "edges": edge_list(best[1]),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
