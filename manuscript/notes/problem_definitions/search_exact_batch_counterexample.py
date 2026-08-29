"""Heuristic search for slow exact-batch RPPR active-set instances.

This is a falsification tool, not evidence for a theorem.  It searches simple
connected unweighted graphs and one-sparse seeds.  The score is the fraction
of the initial Q-energy gap remaining after ceil(1/sqrt(alpha)) exact batch
expansions.  A large score would challenge the depth lemma in
op2_support_safe_acceleration.md.
"""

from __future__ import annotations

import argparse
import math
import random

import numpy as np


def connected(adjacency: np.ndarray) -> bool:
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


def pagerank_matrix(adjacency: np.ndarray, alpha: float) -> tuple[np.ndarray, np.ndarray]:
    degrees = adjacency.sum(axis=1).astype(float)
    inverse_sqrt = 1.0 / np.sqrt(degrees)
    normalized = inverse_sqrt[:, None] * adjacency * inverse_sqrt[None, :]
    matrix = ((1.0 + alpha) / 2.0) * np.eye(len(adjacency))
    matrix -= ((1.0 - alpha) / 2.0) * normalized
    return matrix, degrees


def exact_batch_history(
    adjacency: np.ndarray, alpha: float, rho: float, seed: int
) -> tuple[np.ndarray, list[np.ndarray]] | None:
    matrix, degrees = pagerank_matrix(adjacency, alpha)
    source = np.zeros(len(adjacency))
    source[seed] = 1.0
    linear = alpha * source / np.sqrt(degrees) - rho * alpha * np.sqrt(degrees)
    support = set(int(index) for index in np.flatnonzero(linear > 0.0))
    if not support:
        return None

    history: list[np.ndarray] = []
    for _ in range(len(adjacency) + 1):
        indices = np.array(sorted(support), dtype=int)
        point = np.zeros(len(adjacency))
        point[indices] = np.linalg.solve(
            matrix[np.ix_(indices, indices)], linear[indices]
        )
        if point[indices].min(initial=0.0) < -1.0e-10:
            return None
        history.append(point)
        violation = linear - matrix @ point
        new = {
            int(index)
            for index in np.flatnonzero(violation > 2.0e-11)
            if int(index) not in support
        }
        if not new:
            return matrix, history
        support.update(new)
    raise AssertionError("monotone support did not terminate")


def score_instance(
    adjacency: np.ndarray, alpha: float, rho: float, seed: int
) -> tuple[float, list[np.ndarray]]:
    result = exact_batch_history(adjacency, alpha, rho, seed)
    if result is None:
        return 0.0, []
    matrix, history = result
    block = math.ceil(1.0 / math.sqrt(alpha))
    if len(history) <= block:
        return 0.0, history
    optimum = history[-1]

    def energy(point: np.ndarray) -> float:
        error = optimum - point
        return float(error @ matrix @ error)

    initial = energy(history[0])
    if initial <= 1.0e-24:
        return 0.0, history
    return energy(history[block]) / initial, history


def initial_graph(vertices: int, rng: random.Random) -> np.ndarray:
    adjacency = np.zeros((vertices, vertices), dtype=float)
    for vertex in range(1, vertices):
        neighbor = rng.randrange(vertex)
        adjacency[vertex, neighbor] = adjacency[neighbor, vertex] = 1.0
    for left in range(vertices):
        for right in range(left + 1, vertices):
            if adjacency[left, right] == 0.0 and rng.random() < 2.0 / vertices:
                adjacency[left, right] = adjacency[right, left] = 1.0
    return adjacency


def path_graph(vertices: int) -> np.ndarray:
    adjacency = np.zeros((vertices, vertices), dtype=float)
    for vertex in range(vertices - 1):
        adjacency[vertex, vertex + 1] = adjacency[vertex + 1, vertex] = 1.0
    return adjacency


def mutate(adjacency: np.ndarray, rng: random.Random) -> np.ndarray:
    candidate = adjacency.copy()
    vertices = len(candidate)
    for _ in range(20):
        left, right = rng.sample(range(vertices), 2)
        if left > right:
            left, right = right, left
        candidate[left, right] = candidate[right, left] = 1.0 - candidate[left, right]
        if candidate.sum(axis=1).min() > 0 and connected(candidate):
            return candidate
        candidate[left, right] = candidate[right, left] = 1.0 - candidate[left, right]
    return adjacency.copy()


def describe(adjacency: np.ndarray, rho: float, seed: int, history: list[np.ndarray]) -> None:
    edges = [
        (left, right)
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left, right]
    ]
    batches = []
    previous: set[int] = set()
    for point in history:
        support = set(int(index) for index in np.flatnonzero(point > 1.0e-10))
        batches.append(sorted(support - previous))
        previous = support
    print("rho:", format(rho, ".17g"))
    print("seed:", seed)
    print("edges:", edges)
    print("batches:", batches)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--vertices", type=int, default=32)
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--steps", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=1729)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    best = (0.0, None, None, None, None)

    path = path_graph(args.vertices)
    path_rho = 1.0e-8
    path_value, path_history = score_instance(path, args.alpha, path_rho, 0)
    best = (path_value, path.copy(), path_rho, 0, path_history)
    print(f"path baseline: {path_value:.9f}")

    for restart in range(args.restarts):
        if restart == 0:
            adjacency = path.copy()
            seed = 0
        else:
            adjacency = initial_graph(args.vertices, rng)
            seed = rng.randrange(args.vertices)
        degree = adjacency[seed].sum()
        rho = 1.0e-8 if restart == 0 else (0.98 / degree) * 10.0 ** (-5.0 * rng.random())
        value, history = score_instance(adjacency, args.alpha, rho, seed)
        temperature = 0.003

        for _ in range(args.steps):
            proposal = mutate(adjacency, rng)
            proposal_seed = seed if rng.random() > 0.03 else rng.randrange(args.vertices)
            maximum_rho = 0.98 / proposal[proposal_seed].sum()
            proposal_rho = min(maximum_rho, rho * math.exp(rng.gauss(0.0, 0.35)))
            proposal_rho = max(proposal_rho, maximum_rho * 1.0e-8)
            proposal_value, proposal_history = score_instance(
                proposal, args.alpha, proposal_rho, proposal_seed
            )
            if proposal_value >= value or rng.random() < math.exp(
                (proposal_value - value) / max(temperature, 1.0e-9)
            ):
                adjacency, seed, rho = proposal, proposal_seed, proposal_rho
                value, history = proposal_value, proposal_history
            temperature *= 0.999
            if value > best[0]:
                best = (value, adjacency.copy(), rho, seed, history)
        print(f"restart {restart + 1}: best score {best[0]:.9f}")

    value, adjacency, rho, seed, history = best
    print("best score:", value)
    if adjacency is not None and rho is not None and seed is not None and history is not None:
        describe(adjacency, rho, seed, history)


if __name__ == "__main__":
    main()
