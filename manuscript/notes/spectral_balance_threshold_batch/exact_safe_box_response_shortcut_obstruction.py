#!/usr/bin/env python3
"""Exact-arithmetic audit for the safe-box Schur-pivot obstruction.

The degree-coordinate matrix of the canonical unit path is

    K = D^(1/2) Q D^(1/2) = a D - beta A.

For the correction LCP with trial residual -r e_0, the monotone
principal-pivot path adds the path vertices in order.  Every insertion
strictly changes every previously materialized response coordinate.

This script uses rational arithmetic throughout.  It is a companion audit,
not a solver implementation or a claimed lower bound for all algorithms.
"""

from __future__ import annotations

from fractions import Fraction


def solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Solve a nonsingular rational system by Gauss-Jordan elimination."""
    n = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            scale = aug[row][col]
            if scale != 0:
                aug[row] = [
                    aug[row][j] - scale * aug[col][j]
                    for j in range(n + 1)
                ]
    return [aug[i][-1] for i in range(n)]


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((a * b for a, b in zip(row, vector)), Fraction(0)) for row in matrix]


def add(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return [a + b for a, b in zip(left, right)]


def subtract(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return [a - b for a, b in zip(left, right)]


def scale(value: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [value * entry for entry in vector]


def path_matrix(n: int, alpha: Fraction) -> list[list[Fraction]]:
    if n < 2:
        raise ValueError("the canonical graph is nontrivial")
    a = (1 + alpha) / 2
    beta = (1 - alpha) / 2
    degrees = [1] + [2] * (n - 2) + [1]
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i, degree in enumerate(degrees):
        matrix[i][i] = a * degree
    for i in range(n - 1):
        matrix[i][i + 1] = -beta
        matrix[i + 1][i] = -beta
    return matrix


def audit_safe_lc_state(n: int, alpha: Fraction, s: Fraction) -> None:
    """Check a full-support canonical RPPR state giving trial residual -r e_0."""
    matrix = path_matrix(n, alpha)
    degrees = [1] + [2] * (n - 2) + [1]
    source = [Fraction(alpha)] + [Fraction(0)] * (n - 1)
    unregularized = solve(matrix, source)
    rho = min(unregularized) / 2
    linear_term = [
        source[i] - alpha * rho * degrees[i]
        for i in range(n)
    ]
    optimum = solve(matrix, linear_term)
    assert optimum == [value - rho for value in unregularized]
    assert all(value > 0 for value in optimum)

    first = solve(matrix, [Fraction(1)] + [Fraction(0)] * (n - 1))
    last = solve(matrix, [Fraction(0)] * (n - 1) + [Fraction(1)])
    r = min(optimum) / (4 * max(first))
    delta = min(optimum) / (4 * max(last))

    sigma = [Fraction(0)] * (n - 1) + [delta]
    current = subtract(optimum, scale(delta, last))
    trial = add(optimum, scale(r, first))
    estimate = add(current, scale((1 + s) / s, subtract(trial, current)))
    reconstructed_trial = scale(1 / (1 + s), add(current, scale(s, estimate)))
    correction = scale(r, first)
    safe_box = subtract(trial, correction)

    assert all(value > 0 for value in current)
    assert all(estimate[i] >= current[i] for i in range(n))
    assert reconstructed_trial == trial
    assert subtract(linear_term, matvec(matrix, current)) == sigma
    assert subtract(linear_term, matvec(matrix, trial)) == [
        -r
    ] + [Fraction(0)] * (n - 1)
    assert safe_box == optimum


def audit(n: int = 9, alpha: Fraction = Fraction(1, 16)) -> None:
    matrix = path_matrix(n, alpha)
    previous: list[Fraction] = []
    materialized_changes = 0

    for k in range(1, n + 1):
        principal = [row[:k] for row in matrix[:k]]
        rhs = [Fraction(1)] + [Fraction(0)] * (k - 1)
        response = solve(principal, rhs)
        padded = response + [Fraction(0)] * (n - k)
        residual = matvec(matrix, padded)
        residual[0] -= 1

        assert all(value > 0 for value in response)
        assert all(residual[i] == 0 for i in range(k))
        if k < n:
            assert residual[k] < 0
            assert all(residual[i] == 0 for i in range(k + 1, n))
        else:
            assert all(value == 0 for value in residual)

        if previous:
            assert all(response[i] > previous[i] for i in range(k - 1))
            materialized_changes += k - 1
        previous = response

    expected = n * (n - 1) // 2
    assert materialized_changes == expected
    if alpha == Fraction(1, 16):
        audit_safe_lc_state(n, alpha, Fraction(1, 4))
    print(f"n={n}, alpha={alpha}")
    print(f"strict old-coordinate changes={materialized_changes} (= n(n-1)/2)")
    print("all exact safe-state, prefix-pivot, and unique-frontier assertions passed")


if __name__ == "__main__":
    audit()
