#!/usr/bin/env python3
"""JIT local search above the exact edge-retimed beta cell.

This is an unregistered floating-point falsification aid, not a certificate.
It preserves the two source edges of the exact n=27 near-half witness and
mutates only nonsource edges and the source-scaled threshold.  Any reported
candidate must be replayed by the Fraction-exact tracer.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np
from numba import njit

from beta_stopped_input_cone_search import connected, edge_list
from stopped_masked_input_residual_high_beta_counterexample_exact import (
    NEAR_HALF_EDGES,
    NEAR_HALF_RHO_SCALE,
    STRUCTURED_VERTICES,
)


@njit(cache=True)
def evaluate(
    adjacency: np.ndarray,
    alpha: float,
    rho_scale: float,
    beta: float,
    maximum_phases: int,
    maximum_products: int,
) -> tuple[int, float, int, int, int, float, int, int, float]:
    """Return a compact chronology score; status 1 denotes a strict failure.

    The final entry is the smallest residual-width ratio at a product which
    continued.  For a failing trace this is the open upper endpoint of its
    same-chronology beta cell.  Keeping it in the fast trace lets the search
    optimize the actual certified cell endpoint rather than only the product
    immediately preceding the failure.
    """
    vertices = adjacency.shape[0]
    degrees = np.empty(vertices)
    for vertex in range(vertices):
        degrees[vertex] = np.sum(adjacency[vertex])
        if degrees[vertex] <= 0.0:
            return -1, math.inf, -1, -1, -1, -math.inf, 0, 0, 0.5

    sqrt_degrees = np.sqrt(degrees)
    diagonal = (1.0 + 3.0 * alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    lipschitz = 1.0 + alpha
    gap = 2.0 * alpha
    root = math.sqrt(gap / lipschitz)
    momentum = (1.0 - root) / (1.0 + root)
    auxiliary_scale = (1.0 - root) / root

    matrix = np.zeros((vertices, vertices))
    for left in range(vertices):
        matrix[left, left] = diagonal
        for right in range(vertices):
            if adjacency[left, right] != 0.0:
                matrix[left, right] = -coupling / math.sqrt(
                    degrees[left] * degrees[right]
                )

    rho = rho_scale / degrees[0]
    load = -alpha * rho * sqrt_degrees
    load[0] += alpha / sqrt_degrees[0]
    lower = np.zeros(vertices)
    certified = np.zeros(vertices, dtype=np.bool_)
    certified[0] = True
    width = 1.0 / degrees[0] - rho
    initial_width = width
    minimum_ratio = math.inf
    minimum_phase = -1
    minimum_product = -1
    minimum_vertex = -1
    total_products = 0
    chronology_upper = 0.5

    for phase in range(1, maximum_phases + 1):
        if width <= 1.0e-3 * initial_width:
            return (
                0,
                minimum_ratio,
                minimum_phase,
                minimum_product,
                minimum_vertex,
                -math.inf,
                total_products,
                phase - 1,
                chronology_upper,
            )
        old_width = width
        shifted_load = load + alpha * lower
        current = lower.copy()
        previous = lower.copy()
        preceding_ratio = math.inf

        for product in range(1, maximum_products + 1):
            extrapolate = np.zeros(vertices)
            for vertex in range(vertices):
                if certified[vertex]:
                    extrapolate[vertex] = current[vertex] + momentum * (
                        current[vertex] - previous[vertex]
                    )
            input_residual = shifted_load - matrix @ extrapolate
            for vertex in range(vertices):
                if not certified[vertex] and input_residual[vertex] > 1.0e-14:
                    certified[vertex] = True

            input_vertex = -1
            input_value = math.inf
            for vertex in range(vertices):
                if certified[vertex] and input_residual[vertex] < input_value:
                    input_vertex = vertex
                    input_value = input_residual[vertex]
            ratio = input_value / (gap * sqrt_degrees[input_vertex] * old_width)
            if product > 1 and ratio < minimum_ratio:
                minimum_ratio = ratio
                minimum_phase = phase
                minimum_product = product
                minimum_vertex = input_vertex
            if input_value < -1.0e-13:
                return (
                    1,
                    ratio,
                    phase,
                    product,
                    input_vertex,
                    preceding_ratio,
                    total_products,
                    phase - 1,
                    chronology_upper,
                )

            following = np.zeros(vertices)
            for vertex in range(vertices):
                if certified[vertex]:
                    following[vertex] = extrapolate[vertex] + input_residual[vertex] / lipschitz
            previous = current
            current = following
            for vertex in range(vertices):
                if certified[vertex]:
                    if current[vertex] > lower[vertex]:
                        lower[vertex] = current[vertex]
                    if lower[vertex] < 0.0:
                        lower[vertex] = 0.0

            auxiliary = np.zeros(vertices)
            for vertex in range(vertices):
                if certified[vertex]:
                    auxiliary[vertex] = current[vertex] + auxiliary_scale * (
                        current[vertex] - previous[vertex]
                    )
                    if current[vertex] < lower[vertex]:
                        current[vertex] = lower[vertex]
                    if auxiliary[vertex] < lower[vertex]:
                        auxiliary[vertex] = lower[vertex]
                    previous[vertex] = current[vertex] - (
                        auxiliary[vertex] - current[vertex]
                    ) / auxiliary_scale

            residual = shifted_load - matrix @ lower
            for vertex in range(vertices):
                if certified[vertex] and residual[vertex] > 1.0e-14:
                    increment = residual[vertex] / diagonal
                    lower[vertex] += increment
            residual = shifted_load - matrix @ lower
            for vertex in range(vertices):
                if certified[vertex]:
                    if current[vertex] < lower[vertex]:
                        current[vertex] = lower[vertex]
                    if auxiliary[vertex] < lower[vertex]:
                        auxiliary[vertex] = lower[vertex]
                    previous[vertex] = current[vertex] - (
                        auxiliary[vertex] - current[vertex]
                    ) / auxiliary_scale

            while True:
                additions = np.zeros(vertices)
                admitted = False
                for vertex in range(vertices):
                    if not certified[vertex] and residual[vertex] > 1.0e-14:
                        additions[vertex] = residual[vertex] / diagonal
                        admitted = True
                if not admitted:
                    break
                for vertex in range(vertices):
                    if additions[vertex] > 0.0:
                        lower[vertex] += additions[vertex]
                        current[vertex] = lower[vertex]
                        previous[vertex] = lower[vertex]
                        auxiliary[vertex] = lower[vertex]
                        certified[vertex] = True
                residual = shifted_load - matrix @ lower

            maximum = 0.0
            for vertex in range(vertices):
                scaled = residual[vertex] / (gap * sqrt_degrees[vertex])
                if scaled > maximum:
                    maximum = scaled
            inner_ratio = maximum / old_width
            total_products += 1
            if inner_ratio <= beta:
                width = old_width / 2.0 + maximum
                break
            chronology_upper = min(chronology_upper, inner_ratio)
            preceding_ratio = inner_ratio
        else:
            return (
                -2,
                minimum_ratio,
                minimum_phase,
                minimum_product,
                minimum_vertex,
                preceding_ratio,
                total_products,
                phase,
                chronology_upper,
            )

    return (
        -3,
        minimum_ratio,
        minimum_phase,
        minimum_product,
        minimum_vertex,
        -math.inf,
        total_products,
        maximum_phases,
        chronology_upper,
    )


def adjacency_from_seed() -> np.ndarray:
    adjacency = np.zeros((STRUCTURED_VERTICES, STRUCTURED_VERTICES), dtype=np.float64)
    for left, right in NEAR_HALF_EDGES:
        adjacency[left, right] = 1.0
        adjacency[right, left] = 1.0
    return adjacency


def mutate_local(
    rng: np.random.Generator,
    adjacency: np.ndarray,
    flips: int,
) -> np.ndarray:
    """Mutate nonsource edges while retaining a simple connected graph."""
    candidate = adjacency.copy()
    vertices = len(candidate)
    for _ in range(flips):
        left = int(rng.integers(1, vertices))
        right = int(rng.integers(1, vertices - 1))
        if right >= left:
            right += 1
        if left > right:
            left, right = right, left
        candidate[left, right] = 1.0 - candidate[left, right]
        candidate[right, left] = candidate[left, right]
    if np.min(candidate.sum(axis=1)) == 0.0 or not connected(candidate):
        return adjacency.copy()
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--beta", type=float, default=0.475)
    parser.add_argument("--population", type=int, default=256)
    parser.add_argument("--generations", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=2026090401)
    parser.add_argument("--report-every", type=int, default=50)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    seed_adjacency = adjacency_from_seed()
    seed_rho = float(NEAR_HALF_RHO_SCALE)
    population = [(seed_adjacency, seed_rho)]
    for _ in range(args.population - 1):
        population.append(
            (
                mutate_local(rng, seed_adjacency, int(rng.integers(1, 4))),
                float(np.clip(seed_rho * math.exp(rng.normal(0.0, 0.08)), 1.0e-5, 0.2)),
            )
        )

    alpha = 1.0 / 100351.0
    # Compile before timing/reporting the population loop.
    evaluate(seed_adjacency, alpha, seed_rho, args.beta, 70, 100)
    best: tuple[tuple[float, float], np.ndarray, float, tuple[object, ...]] | None = None
    for generation in range(args.generations):
        ranked = []
        for adjacency, rho_scale in population:
            result = evaluate(adjacency, alpha, rho_scale, args.beta, 70, 100)
            status, minimum = int(result[0]), float(result[1])
            score = (1.0, -minimum) if status == 1 else (0.0, -minimum)
            record = (score, adjacency, rho_scale, result)
            ranked.append(record)
            if best is None or score > best[0]:
                best = (score, adjacency.copy(), rho_scale, result)
                print(
                    json.dumps(
                        {
                            "generation": generation,
                            "score": score,
                            "rho_scale": rho_scale,
                            "result": result,
                            "edge_count": int(adjacency.sum() // 2),
                        }
                    ),
                    flush=True,
                )
                if status == 1:
                    print(
                        json.dumps(
                            {
                                "warning": "floating-point candidate; exact replay required",
                                "vertices": len(adjacency),
                                "alpha": alpha,
                                "beta": args.beta,
                                "rho_scale": rho_scale,
                                "result": result,
                                "edges": edge_list(adjacency),
                            },
                            indent=2,
                        ),
                        flush=True,
                    )
                    return
        ranked.sort(key=lambda item: item[0], reverse=True)
        elites = ranked[: max(4, args.population // 8)]
        population = [(item[1].copy(), item[2]) for item in elites]
        while len(population) < args.population:
            parent = elites[int(rng.integers(len(elites)))]
            flips = 1 if rng.random() < 0.65 else int(rng.integers(2, 5))
            population.append(
                (
                    mutate_local(rng, parent[1], flips),
                    float(
                        np.clip(
                            parent[2] * math.exp(rng.normal(0.0, 0.035)),
                            1.0e-5,
                            0.2,
                        )
                    ),
                )
            )
        if generation % args.report_every == 0:
            assert best is not None
            print(
                json.dumps(
                    {
                        "generation": generation,
                        "best_score": best[0],
                        "rho_scale": best[2],
                        "result": best[3],
                        "edge_count": int(best[1].sum() // 2),
                    }
                ),
                flush=True,
            )

    assert best is not None
    print(
        json.dumps(
            {
                "warning": "floating-point search only; no failure found",
                "vertices": len(best[1]),
                "alpha": alpha,
                "beta": args.beta,
                "rho_scale": best[2],
                "score": best[0],
                "result": best[3],
                "edges": edge_list(best[1]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
