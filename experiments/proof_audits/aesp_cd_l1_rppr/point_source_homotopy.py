#!/usr/bin/env python3
"""Exact audit of point-source homotopy mixing and breakpoint reordering."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations

from experiments.proof_audits import note_tex_source


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    size = len(rhs)
    work = [row[:] + [value] for row, value in zip(matrix, rhs, strict=True)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        diagonal = work[column][column]
        work[column] = [entry / diagonal for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column], strict=True)
            ]
    return [row[-1] for row in work]


def breakpoint_data(
    hessian: list[list[F]], degree: list[int], face: set[int], alpha: F
) -> tuple[dict[int, tuple[F, F]], dict[int, F]]:
    indices = sorted(face)
    principal = [[hessian[i][j] for j in indices] for i in indices]
    source_response = solve(principal, [alpha * F(i == 0) for i in indices])
    degree_response = solve(principal, [alpha * degree[i] for i in indices])
    pairs: dict[int, tuple[F, F]] = {}
    thresholds: dict[int, F] = {}
    for vertex in range(len(degree)):
        if vertex in face:
            continue
        intercept = -sum(
            hessian[vertex][i] * source_response[position]
            for position, i in enumerate(indices)
        )
        slope = alpha * degree[vertex] - sum(
            hessian[vertex][i] * degree_response[position]
            for position, i in enumerate(indices)
        )
        assert slope > 0
        if intercept > 0:
            pairs[vertex] = (intercept, slope)
            thresholds[vertex] = intercept / slope
    return pairs, thresholds


def determinant(matrix: list[list[F]]) -> F:
    """Exact determinant with row pivoting."""
    size = len(matrix)
    if size == 0:
        return F(1)
    work = [row[:] for row in matrix]
    value = F(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        diagonal = work[column][column]
        value *= diagonal
        for row in range(column + 1, size):
            multiplier = work[row][column] / diagonal
            for index in range(column + 1, size):
                work[row][index] -= multiplier * work[column][index]
    return value


def assert_psd(matrix: list[list[F]]) -> None:
    """Use the all-principal-minors characterization of symmetric PSD."""
    size = len(matrix)
    assert all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(size))
    for order in range(1, size + 1):
        for indices in combinations(range(size), order):
            principal = [[matrix[i][j] for j in indices] for i in indices]
            assert determinant(principal) >= 0


def check_ground_state_normalization(
    hessian: list[list[F]],
    degree: list[int],
    adjacency: list[list[F]],
    alpha: F,
) -> int:
    """Audit every connected root-containing principal face exactly."""
    size = len(degree)
    checked = 0
    for mask in range(1, 1 << size):
        if not mask & 1:
            continue
        face = [vertex for vertex in range(size) if mask & (1 << vertex)]
        reached = {face[0]}
        queue = [face[0]]
        for vertex in queue:
            for neighbor in face:
                if adjacency[vertex][neighbor] and neighbor not in reached:
                    reached.add(neighbor)
                    queue.append(neighbor)
        if len(reached) != len(face):
            continue

        principal = [[hessian[i][j] for j in face] for i in face]
        response = solve(principal, [alpha * degree[i] for i in face])
        assert all(F(0) < value <= 1 for value in response)
        mass = [F(degree[i], 1) / response[position] for position, i in enumerate(face)]
        assert all(
            sum(principal[row][column] * response[column] for column in range(len(face)))
            == alpha * mass[row] * response[row]
            for row in range(len(face))
        )

        lower = [
            [
                principal[i][j] - alpha * mass[i] * F(i == j)
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        upper = [
            [
                mass[i] * F(i == j) - principal[i][j]
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        assert_psd(lower)
        assert_psd(upper)

        shift = F(3, 5)
        shifted = [
            [
                principal[i][j] + shift * mass[i] * F(i == j)
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        resolvent = solve(shifted, [shift * mass[i] * response[i] for i in range(len(face))])
        expected_factor = shift / (shift + alpha)
        assert resolvent == [expected_factor * value for value in response]
        checked += 1
    return checked


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-point-source-homotopy-reorder}" in source
    assert r"\label{eq:aesp-cd-point-source-homotopy-mix}" in source
    assert r"\label{lem:aesp-cd-point-source-ground-state-normalization}" in source

    size, alpha = 6, F(2, 7)
    edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 3), (2, 3), (2, 5), (3, 4), (4, 5))
    adjacency = [[F(0)] * size for _ in range(size)]
    degree = [0] * size
    for left, right in edges:
        adjacency[left][right] = adjacency[right][left] = 1
        degree[left] += 1
        degree[right] += 1
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    hessian = [
        [
            diagonal * degree[i] if i == j else -coupling * adjacency[i][j]
            for j in range(size)
        ]
        for i in range(size)
    ]

    _, first = breakpoint_data(hessian, degree, {0}, alpha)
    assert first == {1: F(5, 96), 3: F(5, 123), 4: F(5, 96)}
    assert {vertex for vertex, value in first.items() if value == max(first.values())} == {1, 4}

    face = {0, 1, 4}
    old_pairs, old = breakpoint_data(hessian, degree, face, alpha)
    assert old == {2: F(25, 2517), 3: F(185, 4231), 5: F(25, 1838)}
    assert max(old, key=old.get) == 3
    winner = 3
    new_pairs, new = breakpoint_data(hessian, degree, face | {winner}, alpha)
    assert new == {2: F(975, 53696), 5: F(1025, 64318)}
    assert old[5] > old[2] and new[2] > new[5]

    # Independently recover each nonnegative mixture coefficient from A and
    # verify that the same value updates B.
    winner_intercept, winner_slope = old_pairs[winner]
    for vertex in (2, 5):
        old_intercept, old_slope = old_pairs[vertex]
        new_intercept, new_slope = new_pairs[vertex]
        gamma = (new_intercept - old_intercept) / winner_intercept
        assert gamma >= 0
        assert new_slope == old_slope + gamma * winner_slope
        assert old[vertex] <= new[vertex] <= old[winner]

    ground_faces = check_ground_state_normalization(
        hessian,
        degree,
        adjacency,
        alpha,
    )
    assert ground_faces == 25

    print("PASS point-source homotopy breakpoint audit")
    print("  first tied batch: {1,4} at 5/96; next winner: 3 at 185/4231")
    print("  exact nonnegative rank-one mixing for surviving rows {2,5}")
    print("  strict priority reversal: 5>2 before, 2>5 after")
    print(f"  canonical proper-face ground normalization: {ground_faces} connected faces")


if __name__ == "__main__":
    main()
