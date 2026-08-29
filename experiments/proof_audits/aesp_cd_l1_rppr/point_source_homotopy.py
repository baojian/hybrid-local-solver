#!/usr/bin/env python3
"""Exact audit of point-source homotopy mixing and breakpoint reordering."""

from __future__ import annotations

from fractions import Fraction as F

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


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-point-source-homotopy-reorder}" in source
    assert r"\label{eq:aesp-cd-point-source-homotopy-mix}" in source

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

    print("PASS point-source homotopy breakpoint audit")
    print("  first tied batch: {1,4} at 5/96; next winner: 3 at 185/4231")
    print("  exact nonnegative rank-one mixing for surviving rows {2,5}")
    print("  strict priority reversal: 5>2 before, 2>5 after")


if __name__ == "__main__":
    main()
