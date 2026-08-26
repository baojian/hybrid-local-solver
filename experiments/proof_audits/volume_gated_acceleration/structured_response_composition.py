#!/usr/bin/env python3
"""Exact scalar audit for the structured-response composition.

The path and structured-graph algorithms are proved in the manuscripts.  This
script checks the exact shared/source variable map, strict gate equivalence,
and the face/volume constants used when composing those results.  It is a
regression check, not a construction of an arbitrary-graph response backend.
"""

from __future__ import annotations

from fractions import Fraction


def dense_solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Solve one rational system by dense elimination."""
    n = len(rhs)
    aug = [row.copy() + [value] for row, value in zip(matrix, rhs, strict=True)]
    for pivot in range(n):
        assert aug[pivot][pivot] != 0
        scale = aug[pivot][pivot]
        aug[pivot] = [value / scale for value in aug[pivot]]
        for row in range(n):
            if row == pivot:
                continue
            multiplier = aug[row][pivot]
            aug[row] = [
                left - multiplier * right for left, right in zip(aug[row], aug[pivot], strict=True)
            ]
    return [aug[index][-1] for index in range(n)]


def audit_tree_leaf_solve(parents: tuple[int, ...]) -> int:
    """Check exact leaf elimination with a distributed signed right-hand side."""
    n = len(parents) + 1
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for vertex, parent in enumerate(parents, start=1):
        assert 0 <= parent < vertex
        adjacency[vertex].append(parent)
        adjacency[parent].append(vertex)

    diagonal = [Fraction(5 + len(neighbors)) for neighbors in adjacency]
    rhs = [Fraction(3)] + [Fraction(-vertex, vertex + 3) for vertex in range(1, n)]
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for vertex in range(n):
        matrix[vertex][vertex] = diagonal[vertex]
        for neighbor in adjacency[vertex]:
            matrix[vertex][neighbor] = -1

    effective_diagonal = diagonal.copy()
    effective_rhs = rhs.copy()
    for vertex in range(n - 1, 0, -1):
        parent = parents[vertex - 1]
        effective_diagonal[parent] -= 1 / effective_diagonal[vertex]
        effective_rhs[parent] += effective_rhs[vertex] / effective_diagonal[vertex]

    solution = [Fraction(0) for _ in range(n)]
    solution[0] = effective_rhs[0] / effective_diagonal[0]
    for vertex in range(1, n):
        parent = parents[vertex - 1]
        solution[vertex] = (effective_rhs[vertex] + solution[parent]) / effective_diagonal[vertex]
    assert solution == dense_solve(matrix, rhs)
    return n


def audit_parameter_map(q: Fraction, degree: int) -> int:
    """Check one exact gate-map and work-ledger specialization."""
    assert 0 < q < 1
    assert degree >= 1
    alpha = q * q
    rho = tau = q / 5
    a = (1 + alpha) / 2
    edge_coefficient = (1 - alpha) / 2
    bar_alpha = alpha / a

    assert bar_alpha == 2 * alpha / (1 + alpha)
    assert a * bar_alpha == alpha
    assert a * (1 - bar_alpha) == edge_coefficient

    threshold = (rho + tau) * degree
    offsets = (-q * degree / 7, Fraction(0), q * degree / 7)
    for offset in offsets:
        source_residue = threshold + offset
        scaled_shared_kkt = alpha * (rho * degree - source_residue)
        shared_violates = scaled_shared_kkt < -alpha * tau * degree
        source_violates = source_residue > threshold
        assert shared_violates == source_violates

    max_faces = 5 / q + 1
    max_volume = 5 / q
    repeated_face_charge = max_faces * max_volume
    product_scale = 1 / (rho * q)
    assert product_scale == 5 / (q * q)
    assert repeated_face_charge / product_scale == 5 + q <= 6

    charged_path_volume = 2 * max_volume
    assert charged_path_volume == 10 / q
    assert charged_path_volume <= product_scale
    return len(offsets)


def main() -> None:
    q_values = (
        Fraction(1, 2),
        Fraction(1, 3),
        Fraction(1, 5),
        Fraction(1, 8),
        Fraction(1, 16),
        Fraction(12, 625),
        Fraction(1, 100),
        Fraction(1, 1000),
    )
    cells = sum(audit_parameter_map(q, degree) for q in q_values for degree in range(1, 18))
    tree_cells = sum(
        audit_tree_leaf_solve(parents)
        for parents in (
            tuple(range(8)),
            (0,) * 8,
            (0, 0, 1, 1, 2, 2, 3, 3),
            (0, 1, 1, 3, 2, 5, 5, 4),
        )
    )
    print(
        "structured-response composition scalar audit: "
        f"PASS ({cells} gate cells, {tree_cells} tree-solve cells)"
    )


if __name__ == "__main__":
    main()
