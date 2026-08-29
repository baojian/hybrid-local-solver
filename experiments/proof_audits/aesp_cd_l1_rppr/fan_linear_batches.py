#!/usr/bin/env python3
"""Exact audit for the point-source fan family with linearly many batches."""

from __future__ import annotations

from fractions import Fraction as F

from experiments.proof_audits import note_tex_source


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve a rational system by Gauss--Jordan elimination."""
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


def fibonacci(index: int) -> int:
    left, right = 0, 1
    for _ in range(index):
        left, right = right, left + right
    return left


def arm_matrix(length: int) -> list[list[F]]:
    matrix = [[F(0)] * length for _ in range(length)]
    for index in range(length):
        matrix[index][index] = F(2 if index == 0 else 3)
        if index:
            matrix[index][index - 1] = matrix[index - 1][index] = F(-1)
    return matrix


def check_continuant_identities() -> None:
    """Derive every coefficient from the matrix, not from the claimed formulas."""
    for length in range(1, 21):
        matrix = arm_matrix(length)
        inverse_one = solve(matrix, [F(1)] * length)
        inverse_degree = solve(matrix, [F(2), *([F(3)] * (length - 1))])
        determinant = fibonacci(2 * length + 1)
        tail_one = inverse_one[-1]
        tail_degree = inverse_degree[-1]
        sum_one = sum(inverse_one, F(0))
        sum_degree = sum(inverse_degree, F(0))
        assert tail_one == F(fibonacci(2 * length), determinant)
        assert tail_degree == F(3 * fibonacci(2 * length) - 1, determinant)
        assert sum_one == length - tail_one
        assert sum_degree == 3 * length - 1 - tail_degree

        # Check the two exterior-key identities at the smallest m with a
        # strict next batch, using independently solved arm coordinates.
        size = 2 * length + 4
        rho = F(1, 4 * size - 2)
        root = 2 * (1 - rho * (size + 2 * sum_degree)) / (size - 2 * sum_one)
        arm = solve(
            matrix,
            [root - 4 * rho, *([root - 6 * rho] * (length - 1))],
        )
        delta = (4 * size - 2) * (size - 2 * sum_one)
        assert root - 6 * rho == F(-4, determinant) / delta
        assert root + arm[-1] - 6 * rho == F(2 * (size - 2 * length - 2), determinant) / delta
        assert all(value > 0 for value in arm)


def fan_trace(size: int, alpha: F) -> tuple[list[tuple[int, ...]], set[int], F]:
    """Replay the finite-alpha all-positive batch rule exactly."""
    order = size + 1
    edges = [(0, vertex) for vertex in range(1, order)]
    edges += [(vertex, vertex + 1) for vertex in range(1, size)]
    adjacency = [[F(0)] * order for _ in range(order)]
    degree = [0] * order
    for left, right in edges:
        adjacency[left][right] = adjacency[right][left] = 1
        degree[left] += 1
        degree[right] += 1
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    hessian = [
        [
            diagonal * degree[i] if i == j else -coupling * adjacency[i][j]
            for j in range(order)
        ]
        for i in range(order)
    ]
    rho = F(1, 4 * size - 2)
    load = [alpha * (F(i == 0) - rho * degree[i]) for i in range(order)]
    face = {0}
    batches: list[tuple[int, ...]] = []
    final_max_key = F(0)
    while True:
        indices = sorted(face)
        values = solve(
            [[hessian[i][j] for j in indices] for i in indices],
            [load[i] for i in indices],
        )
        assert all(value > 0 for value in values)
        point = [F(0)] * order
        for index, value in zip(indices, values, strict=True):
            point[index] = value
        keys = [
            load[i] - sum(hessian[i][j] * point[j] for j in range(order))
            for i in range(order)
        ]
        positive = tuple(i for i in range(order) if i not in face and keys[i] > 0)
        if not positive:
            final_max_key = max((keys[i] for i in range(order) if i not in face), default=F(0))
            break
        batches.append(positive)
        face.update(positive)
    return batches, face, final_max_key


def check_finite_instances() -> None:
    # A single explicit rational alpha works for these deterministic witnesses;
    # the theorem itself only needs the finite-family continuity argument.
    for size in range(4, 16, 2):
        batches, face, final_max_key = fan_trace(size, F(1, 10_000))
        expected = [(layer, size - layer + 1) for layer in range(1, size // 2)]
        assert batches == expected
        assert face == {0, *range(1, size // 2), *range(size // 2 + 2, size + 1)}
        assert final_max_key < 0
        assert all(vertex == 0 or 1 <= vertex <= size for vertex in face)


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-fan-linear-batches}" in source
    assert r"\label{eq:aesp-cd-fan-linear-batch-keys}" in source
    check_continuant_identities()
    check_finite_instances()
    print("PASS point-source fan linear-batch family")
    print("  continuant identities: exact for arm lengths 1..20")
    print("  finite alpha=1/10000 traces: m=4,6,...,14")
    print("  batch count=m/2-1 while every graph vertex has source radius one")


if __name__ == "__main__":
    main()
