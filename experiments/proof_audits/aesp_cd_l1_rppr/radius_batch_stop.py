#!/usr/bin/env python3
"""Exact radius-one STOP for all-positive restricted-solve batches."""

from __future__ import annotations

from fractions import Fraction as F

from experiments.proof_audits import note_tex_source


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve a small rational system by Gauss-Jordan elimination."""
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


def exact_trace() -> tuple[list[tuple[int, ...]], list[F]]:
    """Replay the canonical all-positive batch trace in exact arithmetic."""
    size = 8
    edges = (
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        (1, 2), (1, 3), (1, 7), (2, 4), (2, 6), (3, 4),
        (4, 5), (4, 7), (5, 6), (5, 7), (6, 7),
    )
    adjacency = [[F(0)] * size for _ in range(size)]
    for left, right in edges:
        adjacency[left][right] = adjacency[right][left] = 1
    degree = [sum(row) for row in adjacency]
    alpha, rho = F(1, 200), F(23, 800)
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    hessian = [
        [
            diagonal * degree[i] if i == j else -coupling * adjacency[i][j]
            for j in range(size)
        ]
        for i in range(size)
    ]
    rhs = [alpha * ((1 if i == 0 else 0) - rho * degree[i]) for i in range(size)]

    face = {0}
    batches: list[tuple[int, ...]] = []
    positive_margins: list[F] = []
    while True:
        indices = sorted(face)
        solution = solve(
            [[hessian[i][j] for j in indices] for i in indices],
            [rhs[i] for i in indices],
        )
        assert all(value > 0 for value in solution)
        padded = [F(0)] * size
        for index, value in zip(indices, solution, strict=True):
            padded[index] = value
        keys = [
            rhs[i] - sum(hessian[i][j] * padded[j] for j in range(size))
            for i in range(size)
        ]
        positive = tuple(i for i in range(size) if i not in face and keys[i] > 0)
        if not positive:
            assert keys[4] < 0 and keys[7] < 0
            break
        batches.append(positive)
        positive_margins.append(min(keys[i] for i in positive))
        face.update(positive)

    assert batches == [(3,), (1,), (2,), (6,), (5,)]
    assert face == {0, 1, 2, 3, 5, 6}
    assert all((0, vertex) in edges for vertex in face - {0})
    assert positive_margins == [
        F(5013, 37520000),
        F(344981, 8088200000),
        F(49777913, 4439456576000),
        F(169932330613, 61418243753760000),
        F(44816054369, 84444409556591680),
    ]
    return batches, positive_margins


def sharp_killing_contraction() -> None:
    """Check the exact path multiplier and its first-order alpha gap."""
    for denominator in (8, 16, 32, 64, 128, 256):
        alpha = F(1, denominator)
        p = (1 + alpha) / 2
        coupling = (1 - alpha) / 2
        schur_diagonal = 2 * p - coupling * coupling / p
        multiplier = coupling / schur_diagonal
        closed_form = (1 - alpha * alpha) / (
            1 + 6 * alpha + alpha * alpha
        )
        assert multiplier == closed_form
        assert 0 < multiplier < 1
        # The normalized gap tends to six, so it is Theta(alpha), not
        # Theta(sqrt(alpha)).  These rational bounds hold on the audited grid.
        normalized_gap = (1 - multiplier) / alpha
        assert F(3) < normalized_gap < F(6)

        # Use a positive rational rho small enough that the root-only path
        # face has W={1} and row 2 becomes positive after that batch.
        rho = alpha**3
        y_root = alpha * (1 - rho) / p
        key_one = -2 * alpha * rho + coupling * y_root
        key_two = -alpha * rho
        assert key_one > 0 > key_two
        new_key_two = key_two + multiplier * key_one
        assert new_key_two > 0
        assert new_key_two / key_one < multiplier


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-all-positive-radius-stop}" in source
    assert (
        r"\label{prop:aesp-cd-point-source-parallel-batch-contraction}"
        in source
    )
    batches, margins = exact_trace()
    sharp_killing_contraction()
    print("PASS radius-one all-positive batch STOP")
    print("  exact batches", batches)
    print("  positive margins", margins)
    print("  final support radius=1, nonempty batches=5")
    print("  path batch contraction gap is Theta(alpha)")


if __name__ == "__main__":
    main()
