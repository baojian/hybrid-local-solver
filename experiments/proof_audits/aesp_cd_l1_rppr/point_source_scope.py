#!/usr/bin/env python3
"""Exact audit of point-source linear reduction and RPPR nonlinearity."""

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


def obstacle_solution(hessian: list[list[F]], load: list[F]) -> list[F]:
    size = len(load)
    for support_size in range(size + 1):
        for support in combinations(range(size), support_size):
            point = [F(0)] * size
            if support:
                values = solve(
                    [[hessian[i][j] for j in support] for i in support],
                    [load[i] for i in support],
                )
                if any(value <= 0 for value in values):
                    continue
                for index, value in zip(support, values, strict=True):
                    point[index] = value
            residual = [
                sum(hessian[i][j] * point[j] for j in range(size)) - load[i] for i in range(size)
            ]
            if all(residual[i] == 0 for i in support) and all(
                residual[i] >= 0 for i in range(size) if i not in support
            ):
                return point
    raise AssertionError("obstacle support not found")


def path_hessian(alpha: F, size: int) -> tuple[list[list[F]], list[int]]:
    degree = [1, *([2] * (size - 2)), 1]
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    hessian = [
        [
            diagonal * degree[i] if i == j else (-coupling if abs(i - j) == 1 else F(0))
            for j in range(size)
        ]
        for i in range(size)
    ]
    return hessian, degree


def check_linear_superposition() -> None:
    alpha = F(1, 5)
    hessian, degree = path_hessian(alpha, 4)
    weights = [F(1, 2), F(1, 3), F(0), F(1, 6)]
    point_solutions = [
        solve(hessian, [alpha * F(i == source) for i in range(4)]) for source in range(4)
    ]
    combined = solve(hessian, [alpha * value for value in weights])
    superposed = [sum(weights[v] * point_solutions[v][i] for v in range(4)) for i in range(4)]
    assert combined == superposed
    # pi=D*y in the rational degree-unscaled congruence, so equality persists.
    assert [degree[i] * combined[i] for i in range(4)] == [
        degree[i] * superposed[i] for i in range(4)
    ]


def check_rppr_nonlinearity() -> None:
    alpha, rho = F(1, 3), F(1, 8)
    hessian, degree = path_hessian(alpha, 3)

    def rppr(seed: list[F]) -> list[F]:
        load = [alpha * seed[i] - alpha * rho * degree[i] for i in range(3)]
        return obstacle_solution(hessian, load)

    left = rppr([F(1), F(0), F(0)])
    right = rppr([F(0), F(0), F(1)])
    joint = rppr([F(1, 2), F(0), F(1, 2)])
    superposed = [(left[i] + right[i]) / 2 for i in range(3)]
    assert left == [F(13, 28), F(3, 56), F(0)]
    assert right == [F(0), F(3, 56), F(13, 28)]
    assert joint == [F(5, 24), F(1, 24), F(5, 24)]
    assert superposed == [F(13, 56), F(3, 56), F(13, 56)]
    assert joint != superposed


def check_superlevel_stop() -> None:
    alpha, rho = F(1, 5), F(5, 21)
    hessian, degree = path_hessian(alpha, 3)
    load = [alpha * (F(i == 0) - rho * degree[i]) for i in range(3)]
    unconstrained = solve(hessian, load)
    obstacle = obstacle_solution(hessian, load)
    assert load == [F(16, 105), F(-2, 21), F(-1, 21)]
    assert unconstrained == [F(8, 35), F(-4, 105), F(-11, 105)]
    assert obstacle == [F(38, 147), F(1, 147), F(0)]
    assert {i for i, value in enumerate(unconstrained) if value > 0} == {0}
    assert {i for i, value in enumerate(obstacle) if value > 0} == {0, 1}
    root = load[0] / hessian[0][0]
    assert load[1] - hessian[1][0] * root == F(2, 315) > 0
    assert hessian[2][1] * obstacle[1] - load[2] == F(11, 245) > 0


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-point-source-linear-reduction}" in source
    assert r"\label{lem:aesp-cd-point-source-subsolution-connected}" in source
    assert r"\label{prop:aesp-cd-point-source-superlevel-stop}" in source
    check_linear_superposition()
    check_rppr_nonlinearity()
    check_superlevel_stop()
    print("PASS point-source scope audit")
    print("  linear PPR: exact weighted point-source superposition")
    print("  RPPR P3: joint obstacle solution differs from weighted point solves")
    print("  RPPR P3: obstacle support strictly exceeds shifted-PPR positive support")
    print("  scope: point-source theorem target, general-seed linear corollary only")


if __name__ == "__main__":
    main()
