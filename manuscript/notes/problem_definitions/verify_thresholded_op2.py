"""Stress-test the thresholded inexact OP2 construction on small graphs.

The script injects random errors at the full energy tolerance allowed by
Theorem 10.  It checks support safety and the requested final objective gap.
The theorem remains analytic; this file is only a regression test for signs,
scales, and constants in the implementation wrapper.
"""

from __future__ import annotations

import math
import random

import numpy as np

from search_exact_batch_counterexample import exact_batch_history, pagerank_matrix
from verify_exact_batch_cholesky import random_weighted_graph


def inexact_solve(
    matrix: np.ndarray,
    linear: np.ndarray,
    indices: np.ndarray,
    tolerance: float,
    rng: random.Random,
) -> tuple[np.ndarray, np.ndarray]:
    exact = np.zeros(len(matrix))
    exact[indices] = np.linalg.solve(
        matrix[np.ix_(indices, indices)], linear[indices]
    )
    direction = np.array([rng.gauss(0.0, 1.0) for _ in indices])
    local_matrix = matrix[np.ix_(indices, indices)]
    energy = float(direction @ local_matrix @ direction)
    if energy > 0.0:
        direction *= tolerance / math.sqrt(energy)
    approximate = exact.copy()
    approximate[indices] += direction
    return exact, approximate


def check_instance(
    adjacency: np.ndarray,
    alpha: float,
    rho: float,
    eps: float,
    seed: int,
    rng: random.Random,
) -> None:
    result = exact_batch_history(adjacency, alpha, rho, seed)
    matrix, degrees = pagerank_matrix(adjacency, alpha)
    weights = np.sqrt(degrees)
    source = np.zeros(len(adjacency))
    source[seed] = 1.0
    linear = alpha * source / weights - rho * alpha * weights
    if result is None:
        if np.any(linear > 0.0):
            raise AssertionError("empty optimum with positive initial source")
        return
    _, exact_history = result
    optimum = exact_history[-1]
    optimum_support = set(np.flatnonzero(optimum > 1.0e-9))

    constant = 1.0 / 128.0
    threshold = constant * alpha * math.sqrt(rho * eps)
    enclosure = threshold / 4.0
    phases = math.ceil((math.sqrt(2.0 / alpha) + 2.0) * math.log2(32.0 / eps))
    support = set(np.flatnonzero(linear > 0.0))
    if not support:
        return

    approximate = np.zeros(len(adjacency))
    exact = np.zeros(len(adjacency))
    for phase in range(phases + 1):
        indices = np.array(sorted(support), dtype=int)
        exact, approximate = inexact_solve(
            matrix,
            linear,
            indices,
            enclosure * math.sqrt(alpha),
            rng,
        )
        if phase == phases:
            break
        estimated = linear - matrix @ approximate
        new = {
            int(vertex)
            for vertex in np.flatnonzero(estimated > 2.0 * threshold * weights)
            if int(vertex) not in support
        }
        if not new:
            break
        if not new.issubset(optimum_support):
            raise AssertionError("thresholded solve added false support")
        support.update(new)

    output = np.zeros(len(adjacency))
    indices = np.array(sorted(support), dtype=int)
    output[indices] = np.maximum(
        approximate[indices] - enclosure * weights[indices], 0.0
    )
    error = output - optimum
    gap = 0.5 * float(error @ matrix @ error)
    if gap > eps * (1.0 + 2.0e-6) + 2.0e-10:
        raise AssertionError(("objective gap", gap, eps, alpha, rho))
    if np.any(output - exact > 2.0e-8):
        raise AssertionError("output is not a certified lower vector")


def main() -> None:
    rng = random.Random(8675309)
    checked = 0
    for _ in range(750):
        vertices = rng.randrange(5, 30)
        adjacency = random_weighted_graph(vertices, rng)
        adjacency /= adjacency.sum(axis=1).min()
        alpha = 10.0 ** rng.uniform(-2.5, -0.05)
        seed = rng.randrange(vertices)
        rho = (0.9 / adjacency[seed].sum()) * 10.0 ** rng.uniform(-4.0, -0.1)
        eps = min(alpha / 4.0, 10.0 ** rng.uniform(-8.0, -2.0))
        check_instance(adjacency, alpha, rho, eps, seed, rng)
        checked += 1
    print(f"verified {checked} thresholded inexact instances")


if __name__ == "__main__":
    main()
