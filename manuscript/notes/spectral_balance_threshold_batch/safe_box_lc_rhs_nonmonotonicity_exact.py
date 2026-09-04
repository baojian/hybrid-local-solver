#!/usr/bin/env python3
"""Exact SafeBoxLC RHS/active-set nonmonotonicity on the unit triangle.

All state and LCP computations use fractions.  The audit verifies a genuine
fixed-support SafeBoxLC trajectory, rather than a sequence of unrelated LCPs.
"""

from __future__ import annotations

from fractions import Fraction


F = Fraction


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    n = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        value = aug[col][col]
        aug[col] = [entry / value for entry in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            value = aug[row][col]
            aug[row] = [
                aug[row][j] - value * aug[col][j]
                for j in range(n + 1)
            ]
    return [aug[i][-1] for i in range(n)]


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum((a * b for a, b in zip(row, vector)), F(0)) for row in matrix]


def lcp(matrix: list[list[F]], trial: list[F]) -> tuple[list[F], list[F], tuple[int, ...]]:
    """Enumerate the eight complementary bases of the three-coordinate LCP."""
    n = len(trial)
    for mask in range(1 << n):
        active = tuple(i for i in range(n) if mask & (1 << i))
        correction = [F(0)] * n
        if active:
            principal = [[matrix[i][j] for j in active] for i in active]
            values = solve(principal, [-trial[i] for i in active])
            for i, value in zip(active, values):
                correction[i] = value
        residual = [
            trial[i] + value
            for i, value in enumerate(matvec(matrix, correction))
        ]
        if (
            all(value >= 0 for value in correction)
            and all(value >= 0 for value in residual)
            and all(correction[i] * residual[i] == 0 for i in range(n))
        ):
            return correction, residual, active
    raise AssertionError("the SPD Stieltjes LCP must have a solution")


def quadratic(matrix: list[list[F]], vector: list[F]) -> F:
    product = matvec(matrix, vector)
    return sum((a * b for a, b in zip(vector, product)), F(0))


def audit() -> None:
    alpha = F(1, 9)
    s = F(1, 3)
    q = s / (1 + s)
    hessian = [
        [F(5, 9) if i == j else F(-2, 9) for j in range(3)]
        for i in range(3)
    ]
    response = [
        [F(i == j) - hessian[i][j] for j in range(3)]
        for i in range(3)
    ]

    slack = [F(0), F(0), F(1, 4)]
    displacement = [F(7, 4), F(3, 2), F(1)]

    # Explicit canonical realization in the common rescaling x_tilde=sqrt(2)x.
    # For source 0 and rho=1/14, c_tilde=alpha e_0-2 alpha rho 1.
    rho = F(1, 14)
    scale = F(1, 100)
    canonical_linear_term = [
        alpha - 2 * alpha * rho,
        -2 * alpha * rho,
        -2 * alpha * rho,
    ]
    optimum = solve(hessian, canonical_linear_term)
    assert optimum == [F(2, 7), F(1, 7), F(1, 7)]
    initial_slack_response = solve(hessian, [scale * value for value in slack])
    current = [optimum[i] - initial_slack_response[i] for i in range(3)]
    estimate = [current[i] + scale * displacement[i] for i in range(3)]
    assert all(value > 0 for value in current)
    assert all(value > 0 for value in estimate)
    assert [
        canonical_linear_term[i] - value
        for i, value in enumerate(matvec(hessian, current))
    ] == [scale * value for value in slack]

    expected_active = ((0, 1), (0,), (), (2,), (0, 1, 2))
    corrections: list[list[F]] = []
    trials: list[list[F]] = []

    for expected in expected_active:
        qv = matvec(hessian, displacement)
        trial = [slack[i] - q * qv[i] for i in range(3)]
        correction, safe_residual, active = lcp(hessian, trial)
        assert active == expected
        assert all(value >= 0 for value in slack)
        assert all(value >= 0 for value in displacement)
        trials.append(trial)
        corrections.append(correction)

        slack = matvec(response, safe_residual)
        displacement = [
            (1 - s)
            * (
                displacement[i] / (1 + s)
                + correction[i]
                + safe_residual[i] / s
            )
            for i in range(3)
        ]

    assert trials == [
        [F(-5, 48), F(-1, 18), F(7, 24)],
        [F(-5, 648), F(2, 81), F(5, 72)],
        [F(7, 1944), F(35, 1944), F(1, 81)],
        [F(2, 729), F(5, 972), F(-5, 2916)],
        [F(-5, 5832), F(-29, 17496), F(-1, 243)],
    ]

    old_correction = corrections[0]
    next_old_residual = [
        trials[1][i] + value
        for i, value in enumerate(matvec(hessian, old_correction))
    ]
    assert next_old_residual == [F(125, 1296), F(13, 162), F(-1, 27)]
    assert min(next_old_residual) < 0

    next_exact = corrections[1]
    positive_drop = [
        max(F(0), old_correction[i] - next_exact[i])
        for i in range(3)
    ]
    monotone_gap_floor = alpha * sum(value * value for value in positive_drop) / 2
    assert positive_drop == [F(37, 144), F(5, 24), F(0)]
    assert monotone_gap_floor == F(2269, 373248)

    print("active correction sets:", expected_active)
    print("old correction is infeasible for next RHS:", next_old_residual)
    print("monotone-correction primal-dual gap floor:", monotone_gap_floor)
    print("all exact SafeBoxLC nonmonotonicity assertions passed")


if __name__ == "__main__":
    audit()
