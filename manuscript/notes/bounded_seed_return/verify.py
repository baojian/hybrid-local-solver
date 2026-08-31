#!/usr/bin/env python3
"""Deterministic checks for the bounded-seed-return note.

The script uses only NumPy.  It verifies the local spectral-measure and
resolvent bounds on a deterministic random-graph battery, checks the exact
closed forms against long finite truncations, and prints the semantic-support
screen reported in the note.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Graph:
    n: int
    src: np.ndarray
    dst: np.ndarray
    degree: np.ndarray


def graph_from_edges(n: int, edges: list[tuple[int, int]]) -> Graph:
    simple = sorted({(min(u, w), max(u, w)) for u, w in edges if u != w})
    edge_array = np.asarray(simple, dtype=np.int64)
    src = np.concatenate((edge_array[:, 0], edge_array[:, 1]))
    dst = np.concatenate((edge_array[:, 1], edge_array[:, 0]))
    degree = np.bincount(src, minlength=n).astype(float)
    assert np.all(degree >= 1)
    return Graph(n, src, dst, degree)


def path(n: int) -> Graph:
    return graph_from_edges(n, [(j, j + 1) for j in range(n - 1)])


def caterpillar(backbone: int) -> Graph:
    edges = [(j, j + 1) for j in range(backbone - 1)]
    edges.extend((j, backbone + j) for j in range(backbone))
    return graph_from_edges(2 * backbone, edges)


def hub_ladder(backbone: int, hub_degree: int) -> Graph:
    edges = [(j, j + 1) for j in range(backbone - 1)]
    next_vertex = backbone
    for j in range(backbone):
        hub = next_vertex
        next_vertex += 1
        edges.append((j, hub))
        for _ in range(hub_degree - 1):
            edges.append((hub, next_vertex))
            next_vertex += 1
    return graph_from_edges(next_vertex, edges)


def binary_tree(depth: int) -> Graph:
    n = 2 ** (depth + 1) - 1
    edges = []
    for parent in range(n):
        for child in (2 * parent + 1, 2 * parent + 2):
            if child < n:
                edges.append((parent, child))
    return graph_from_edges(n, edges)


def cycle_antipode(n: int) -> Graph:
    assert n % 2 == 0
    edges = [(j, (j + 1) % n) for j in range(n)]
    edges.extend((j, j + n // 2) for j in range(n // 2))
    return graph_from_edges(n, edges)


def matvec(graph: Graph, c: float, vector: np.ndarray) -> np.ndarray:
    adjacent_sum = np.bincount(graph.src, weights=vector[graph.dst], minlength=graph.n)
    return graph.degree * vector - c * adjacent_sum


def solve_q(
    graph: Graph, alpha: float, seed: int = 0, tolerance: float = 1.0e-12
) -> tuple[np.ndarray, float]:
    c = (1.0 - alpha) / (1.0 + alpha)
    gamma = 2.0 * alpha / (1.0 + alpha)
    right = np.zeros(graph.n)
    right[seed] = gamma
    solution = np.zeros(graph.n)
    residual = right.copy()
    preconditioned = residual / graph.degree
    direction = preconditioned.copy()
    residual_dot = float(residual @ preconditioned)
    initial_norm = float(np.linalg.norm(right))
    for _ in range(20_000):
        image = matvec(graph, c, direction)
        step = residual_dot / float(direction @ image)
        solution += step * direction
        residual -= step * image
        relative = float(np.linalg.norm(residual) / initial_norm)
        if relative <= tolerance:
            return solution, relative
        preconditioned = residual / graph.degree
        next_dot = float(residual @ preconditioned)
        direction = preconditioned + (next_dot / residual_dot) * direction
        residual_dot = next_dot
    raise AssertionError("preconditioned conjugate gradient did not converge")


def statistics(graph: Graph, alpha: float) -> tuple[float, float, float, float]:
    q, relative = solve_q(graph, alpha)
    gamma = 2.0 * alpha / (1.0 + alpha)
    pi = graph.degree * q
    amplification = float(pi[0] / gamma)
    order = np.argsort(-q)
    cumulative_volume = np.cumsum(graph.degree[order])
    saturation_left_limits = q[order] * cumulative_volume
    support_supremum = float(np.max(saturation_left_limits))
    return amplification, support_supremum, relative, float(pi.sum())


def path_formula(alpha: float) -> float:
    return (1.0 + alpha) / (2.0 * math.sqrt(alpha))


def caterpillar_formula(alpha: float) -> float:
    c = (1.0 - alpha) / (1.0 + alpha)
    middle = 3.0 - c * c
    r = (middle - math.sqrt(middle * middle - 4.0 * c * c)) / (2.0 * c)
    return 2.0 / (2.0 - c * c - c * r)


def hub_ladder_formula(alpha: float, hub_degree: int) -> float:
    c = (1.0 - alpha) / (1.0 + alpha)
    transfer = c / (hub_degree - (hub_degree - 1) * c * c)
    middle = (3.0 - c * transfer) / c
    r = (middle - math.sqrt(middle * middle - 4.0)) / 2.0
    return 2.0 / (2.0 - c * (transfer + r))


def dense_adjacency(graph: Graph) -> np.ndarray:
    adjacency = np.zeros((graph.n, graph.n))
    adjacency[graph.src, graph.dst] = 1.0
    return adjacency


def random_connected_graph(n: int, generator: np.random.Generator) -> Graph:
    edges = [(j, int(generator.integers(0, j))) for j in range(1, n)]
    probability = min(0.18, 3.0 / n)
    existing = {(min(u, w), max(u, w)) for u, w in edges}
    for u in range(n):
        for w in range(u + 1, n):
            if (u, w) not in existing and generator.random() < probability:
                edges.append((u, w))
    return graph_from_edges(n, edges)


def check_spectral_theorem() -> None:
    generator = np.random.default_rng(19)
    cells = 0
    worst_measure_ratio = 0.0
    worst_resolvent_ratio = 0.0
    for n in range(2, 31):
        for _ in range(3):
            graph = random_connected_graph(n, generator)
            adjacency = dense_adjacency(graph)
            inverse_sqrt = 1.0 / np.sqrt(graph.degree)
            normalized = adjacency * inverse_sqrt[:, None] * inverse_sqrt[None, :]
            eigenvalues, eigenvectors = np.linalg.eigh(np.eye(n) - normalized)
            volume = float(graph.degree.sum())
            for seed in range(n):
                cumulative = 0.0
                for k in range(1, n):
                    cumulative += float(eigenvectors[seed, k] ** 2)
                    bound = 4.0 * graph.degree[seed] * math.sqrt(eigenvalues[k])
                    assert cumulative <= bound + 2.0e-12
                    worst_measure_ratio = max(worst_measure_ratio, cumulative / bound)
                for alpha in (2.0**-3, 2.0**-6, 2.0**-10):
                    c = (1.0 - alpha) / (1.0 + alpha)
                    gamma = 2.0 * alpha / (1.0 + alpha)
                    amplification = float(
                        np.sum(eigenvectors[seed, :] ** 2 / (gamma + c * eigenvalues))
                    )
                    bound = (
                        graph.degree[seed] / (volume * gamma)
                        + 1.0 / (1.0 + c)
                        + 2.0 * math.pi * graph.degree[seed] / math.sqrt(c * gamma)
                    )
                    assert amplification <= bound + 2.0e-10
                    worst_resolvent_ratio = max(worst_resolvent_ratio, amplification / bound)
                    cells += 1
    print(
        f"spectral battery: {cells} rooted parameter cells; "
        f"max measure/bound={worst_measure_ratio:.6f}; "
        f"max resolvent/bound={worst_resolvent_ratio:.6f}"
    )


def check_alpha_one_endpoint() -> None:
    graph = cycle_antipode(32)
    q, relative = solve_q(graph, 1.0)
    pi = graph.degree * q
    expected = np.zeros(graph.n)
    expected[0] = 1.0
    assert relative <= 1.0e-12
    assert np.array_equal(pi, expected)
    assert pi[0] == 1.0
    print("alpha=1 endpoint: H=I, gamma=1, pi=e_v, A=1 passed")


def check_closed_forms() -> None:
    cases = (
        ("path", path(4_000), path_formula),
        ("caterpillar", caterpillar(2_000), caterpillar_formula),
        (
            "hub-ladder",
            hub_ladder(120, 32),
            lambda alpha: hub_ladder_formula(alpha, 32),
        ),
    )
    for name, graph, formula in cases:
        for alpha in (2.0**-6, 2.0**-9, 2.0**-12):
            measured, _, relative, mass = statistics(graph, alpha)
            exact = formula(alpha)
            assert abs(measured / exact - 1.0) <= 2.0e-9
            assert relative <= 1.0e-11
            assert abs(mass - 1.0) <= 2.0e-10
        print(f"closed form: {name} passed")


def print_screen() -> None:
    families = (
        ("path", path(4_000)),
        ("caterpillar", caterpillar(2_000)),
        ("hub-ladder-D32", hub_ladder(120, 32)),
        ("binary-tree", binary_tree(11)),
        ("cycle-antipode", cycle_antipode(4_000)),
    )
    print("family             alpha   dv   alpha*A   sqrt(alpha)*A   sup eps*vol(S)")
    for name, graph in families:
        for exponent in (6, 9, 12):
            alpha = 2.0 ** (-exponent)
            amplification, support_score, relative, mass = statistics(graph, alpha)
            assert relative <= 1.0e-11
            assert abs(mass - 1.0) <= 2.0e-10
            print(
                f"{name:18s} 2^-{exponent:<2d}  {graph.degree[0]:.0f}  "
                f"{alpha * amplification:9.5f}  "
                f"{math.sqrt(alpha) * amplification:13.5f}  "
                f"{support_score:14.5f}"
            )


def main() -> None:
    check_spectral_theorem()
    check_alpha_one_endpoint()
    check_closed_forms()
    print_screen()
    print("all bounded-seed-return checks passed")


if __name__ == "__main__":
    main()
