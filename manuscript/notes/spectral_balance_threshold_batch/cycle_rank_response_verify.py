#!/usr/bin/env python3
"""Numerical audit of the tree-plus-cycle-rank Woodbury decomposition.

Run with NumPy available, for example

    uv run --with numpy python cycle_rank_response_verify.py
"""

from collections import deque
import random

import numpy as np


def spanning_tree(n, edges):
    adjacency = [[] for _ in range(n)]
    for index, (i, j) in enumerate(edges):
        adjacency[i].append((j, index))
        adjacency[j].append((i, index))
    seen = {0}
    queue = deque([0])
    tree_indices = set()
    while queue:
        i = queue.popleft()
        for j, index in adjacency[i]:
            if j not in seen:
                seen.add(j)
                queue.append(j)
                tree_indices.add(index)
    assert len(seen) == n
    return tree_indices


def cavity_messages(matrix, tree_edges):
    """Return exact-formula cavity pivots for every directed tree edge."""
    adjacency = [[] for _ in range(len(matrix))]
    for i, j in tree_edges:
        adjacency[i].append(j)
        adjacency[j].append(i)
    memo = {}

    def message(vertex, excluded):
        key = (vertex, excluded)
        if key not in memo:
            pivot = matrix[vertex, vertex]
            for neighbor in adjacency[vertex]:
                if neighbor != excluded:
                    pivot -= matrix[vertex, neighbor] ** 2 / message(neighbor, vertex)
            memo[key] = pivot
        return memo[key]

    for i, j in tree_edges:
        message(i, j)
        message(j, i)
    full_pivot = np.array(
        [
            matrix[i, i] - sum(matrix[i, j] ** 2 / message(j, i) for j in adjacency[i])
            for i in range(len(matrix))
        ]
    )
    return adjacency, memo, full_pivot


def tree_green_query(matrix, adjacency, messages, full_pivot, source, target):
    """Evaluate one inverse entry by the directed path-product formula."""
    if source == target:
        return 1 / full_pivot[source]
    parent = {source: None}
    queue = deque([source])
    while queue and target not in parent:
        i = queue.popleft()
        for j in adjacency[i]:
            if j not in parent:
                parent[j] = i
                queue.append(j)
    path = []
    vertex = target
    while parent[vertex] is not None:
        path.append((parent[vertex], vertex))
        vertex = parent[vertex]
    value = 1 / full_pivot[source]
    for old, new in reversed(path):
        value *= -matrix[new, old] / messages[(new, old)]
    return value


def main():
    random.seed(23)
    for n in range(2, 13):
        for _ in range(100):
            edges = {(i, i + 1) for i in range(n - 1)}
            for i in range(n):
                for j in range(i + 2, n):
                    if random.random() < 0.18:
                        edges.add((i, j))
            edges = sorted(edges)
            tree_indices = spanning_tree(n, edges)
            feedback = [edge for index, edge in enumerate(edges) if index not in tree_indices]

            internal_degree = np.zeros(n)
            for i, j in edges:
                internal_degree[i] += 1
                internal_degree[j] += 1
            degree_out = np.array([random.randrange(0, 4) for _ in range(n)], dtype=float)
            full_degree = internal_degree + degree_out
            assert np.all(full_degree > 0)

            alpha = 0.031
            c = (1 - alpha) / 2
            invsqrt = 1 / np.sqrt(full_degree)
            adjacency = np.zeros((n, n))
            tree_laplacian = np.zeros((n, n))
            for index, (i, j) in enumerate(edges):
                adjacency[i, j] = adjacency[j, i] = 1
                if index in tree_indices:
                    tree_laplacian[i, i] += 1
                    tree_laplacian[j, j] += 1
                    tree_laplacian[i, j] -= 1
                    tree_laplacian[j, i] -= 1

            grounded = np.diag(full_degree) - adjacency
            qmat = alpha * np.eye(n) + c * (invsqrt[:, None] * grounded * invsqrt[None, :])
            tree_base = alpha * np.eye(n) + c * (
                invsqrt[:, None] * (tree_laplacian + np.diag(degree_out)) * invsqrt[None, :]
            )
            incidence = np.zeros((n, len(feedback)))
            for column, (i, j) in enumerate(feedback):
                incidence[i, column] = invsqrt[i]
                incidence[j, column] = -invsqrt[j]

            assert np.linalg.eigvalsh(tree_base)[0] >= alpha - 1e-11
            reconstructed = tree_base + c * incidence @ incidence.T
            assert np.max(np.abs(qmat - reconstructed)) < 1e-11

            tree_edges = [edge for index, edge in enumerate(edges) if index in tree_indices]
            tree_adjacency, messages, full_pivot = cavity_messages(tree_base, tree_edges)
            inverse_tree_base = np.linalg.inv(tree_base)
            for source in range(n):
                for target in range(n):
                    queried = tree_green_query(
                        tree_base,
                        tree_adjacency,
                        messages,
                        full_pivot,
                        source,
                        target,
                    )
                    assert abs(queried - inverse_tree_base[target, source]) < 2e-10

            rhs = np.array([random.uniform(-1, 1) for _ in range(n)])
            base_solution = np.linalg.solve(tree_base, rhs)
            if len(feedback):
                core = np.eye(len(feedback)) / c
                core += incidence.T @ np.linalg.solve(tree_base, incidence)
                coefficients = np.linalg.solve(core, incidence.T @ base_solution)
                answer = np.linalg.solve(tree_base, rhs - incidence @ coefficients)
                assert np.linalg.eigvalsh(core)[0] > 0
            else:
                answer = base_solution
            truth = np.linalg.solve(qmat, rhs)
            assert np.max(np.abs(answer - truth)) < 2e-10

    print("random tree-plus-cycle-rank Woodbury solves verified")


if __name__ == "__main__":
    main()
