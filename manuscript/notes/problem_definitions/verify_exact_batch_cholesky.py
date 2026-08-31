"""Numerically check the block-Cholesky identities in Theorem 9.

This is a regression check for the proof, not evidence replacing it.  It
generates small weighted RPPR instances, orders the exact active support by
release batch, and verifies the first-crossing and weighted-tail inequalities.
"""

from __future__ import annotations

import random

import numpy as np

from search_exact_batch_counterexample import exact_batch_history, pagerank_matrix


def random_weighted_graph(vertices: int, rng: random.Random) -> np.ndarray:
    adjacency = np.zeros((vertices, vertices), dtype=float)
    for vertex in range(1, vertices):
        neighbor = rng.randrange(vertex)
        weight = np.exp(rng.uniform(-2.0, 2.0))
        adjacency[vertex, neighbor] = adjacency[neighbor, vertex] = weight
    for left in range(vertices):
        for right in range(left + 1, vertices):
            if adjacency[left, right] == 0.0 and rng.random() < 1.5 / vertices:
                weight = np.exp(rng.uniform(-2.0, 2.0))
                adjacency[left, right] = adjacency[right, left] = weight
    return adjacency


def check_instance(
    adjacency: np.ndarray, alpha: float, rho: float, seed: int
) -> None:
    result = exact_batch_history(adjacency, alpha, rho, seed)
    if result is None:
        return
    matrix, history = result
    degrees = adjacency.sum(axis=1)
    source = np.zeros(len(adjacency))
    source[seed] = 1.0
    linear = alpha * source / np.sqrt(degrees) - rho * alpha * np.sqrt(degrees)

    supports = [set(np.flatnonzero(point > 1.0e-9)) for point in history]
    batches: list[list[int]] = []
    previous: set[int] = set()
    for support in supports:
        batch = sorted(support - previous)
        if not batch:
            raise AssertionError("empty exact release batch")
        batches.append(batch)
        previous = support

    order = [vertex for batch in batches for vertex in batch]
    principal = matrix[np.ix_(order, order)]
    cholesky = np.linalg.cholesky(principal)
    transformed = np.linalg.solve(cholesky, linear[order])

    offsets = np.cumsum([0] + [len(batch) for batch in batches])
    z_blocks = [
        transformed[offsets[index] : offsets[index + 1]]
        for index in range(len(batches))
    ]
    if min(float(block.min()) for block in z_blocks) < -2.0e-7:
        raise AssertionError("a forward-solve block is negative")

    reordered_history = [point[order] for point in history]
    previous_point = np.zeros(len(order))
    for index, point in enumerate(reordered_history):
        increment = point - previous_point
        energy = float(increment @ principal @ increment)
        expected = float(z_blocks[index] @ z_blocks[index])
        if not np.isclose(energy, expected, rtol=2.0e-6, atol=2.0e-8):
            raise AssertionError(("increment energy", energy, expected))
        previous_point = point

    for index in range(1, len(batches)):
        row = slice(offsets[index], offsets[index + 1])
        previous_column = slice(offsets[index - 1], offsets[index])
        diagonal = cholesky[row, row]
        adjacent = cholesky[row, previous_column]
        current_rhs = diagonal @ z_blocks[index]
        old_rhs = adjacent @ z_blocks[index - 1] + current_rhs
        if current_rhs.min(initial=0.0) < -2.0e-7:
            raise AssertionError("current Schur residual is negative")
        if old_rhs.max(initial=0.0) > 2.0e-7:
            raise AssertionError("first-crossing inequality failed")

    for tail in range(len(batches)):
        weighted = sum(
            (index - tail + 1) ** 2 * float(z_blocks[index] @ z_blocks[index])
            for index in range(tail, len(batches))
        )
        total = sum(
            float(z_blocks[index] @ z_blocks[index])
            for index in range(tail, len(batches))
        )
        if weighted > total / alpha * (1.0 + 2.0e-6) + 2.0e-8:
            raise AssertionError(("weighted tail", weighted, total / alpha))


def main() -> None:
    rng = random.Random(20260830)
    checked = 0
    for _ in range(500):
        vertices = rng.randrange(5, 24)
        adjacency = random_weighted_graph(vertices, rng)
        alpha = 10.0 ** rng.uniform(-2.5, -0.05)
        seed = rng.randrange(vertices)
        rho = (0.95 / adjacency[seed].sum()) * 10.0 ** rng.uniform(-5.0, -0.05)
        check_instance(adjacency, alpha, rho, seed)
        checked += 1
    print(f"verified {checked} weighted instances")


if __name__ == "__main__":
    main()
