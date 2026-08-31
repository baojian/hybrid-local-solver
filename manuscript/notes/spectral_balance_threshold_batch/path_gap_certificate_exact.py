#!/usr/bin/env python3
"""Checks for the Collatz--Wielandt and path-Poincare gap certificates.

Run with NumPy and SymPy available, for example

    uv run --with numpy --with sympy python path_gap_certificate_exact.py
"""

from collections import deque
import random

import numpy as np
import sympy as sp


def certificate(n, edges, face, alpha):
    """Return the exact gap and two certified lower bounds for one face."""
    face = set(face)
    adjacency = [[] for _ in range(n)]
    for i, j in edges:
        adjacency[i].append(j)
        adjacency[j].append(i)
    degrees = np.array([len(adjacency[i]) for i in range(n)], dtype=float)

    order = sorted(face)
    position = {vertex: index for index, vertex in enumerate(order)}
    normalized = np.zeros((len(order), len(order)))
    for i, j in edges:
        if i in face and j in face:
            weight = 1 / np.sqrt(degrees[i] * degrees[j])
            normalized[position[i], position[j]] = weight
            normalized[position[j], position[i]] = weight
    a = (1 + alpha) / 2
    c = (1 - alpha) / 2
    qmat = a * np.eye(len(order)) - c * normalized

    # Multi-source BFS from the internal boundary.  Each root also selects
    # one final edge leading to the exterior zero.
    roots = [i for i in face if any(j not in face for j in adjacency[i])]
    parent = {root: None for root in roots}
    root_edge = {root: (root, next(j for j in adjacency[root] if j not in face)) for root in roots}
    distance = {root: 0 for root in roots}
    root_of = {root: root for root in roots}
    queue = deque(roots)
    while queue:
        i = queue.popleft()
        for j in adjacency[i]:
            if j in face and j not in parent:
                parent[j] = i
                root_of[j] = root_of[i]
                distance[j] = distance[i] + 1
                queue.append(j)
    assert len(parent) == len(face)

    edge_load = {}
    for i in face:
        path_length = distance[i] + 1
        load = degrees[i] * path_length
        j = i
        while parent[j] is not None:
            edge = tuple(sorted((j, parent[j])))
            edge_load[edge] = edge_load.get(edge, 0.0) + load
            j = parent[j]
        edge = root_edge[root_of[i]]
        edge_load[edge] = edge_load.get(edge, 0.0) + load
    gamma = max(edge_load.values())
    mu_path = alpha + c / gamma

    positive_test = 0.2 + np.arange(1, len(order) + 1, dtype=float)
    row_ratio = np.max((normalized @ positive_test) / positive_test)
    mu_collatz = a - c * min(1.0, row_ratio)
    return np.linalg.eigvalsh(qmat)[0], mu_path, mu_collatz


def main():
    random.seed(17)
    for n in range(3, 10):
        for _ in range(100):
            edges = {(i, i + 1) for i in range(n - 1)}
            for i in range(n):
                for j in range(i + 2, n):
                    if random.random() < 0.25:
                        edges.add((i, j))
            face = {i for i in range(n) if random.random() < 0.7}
            if not face or len(face) == n:
                face = set(range(n - 1))
            exact, path, collatz = certificate(n, sorted(edges), face, alpha=0.037)
            assert path <= exact + 1e-11, (exact, path)
            assert collatz <= exact + 1e-11, (exact, collatz)

    # Exact congestion on the canonical ballasted broom.
    leaves, depth = sp.symbols("N j", integer=True, positive=True)
    gamma = (leaves + 1) * (depth + 1) + leaves * (depth + 2) + depth * (depth + 1)
    claimed = depth**2 + (2 * leaves + 2) * depth + 3 * leaves + 1
    assert sp.expand(gamma - claimed) == 0

    print("random Collatz/path certificates verified")
    print("exact broom congestion identity verified")


if __name__ == "__main__":
    main()
