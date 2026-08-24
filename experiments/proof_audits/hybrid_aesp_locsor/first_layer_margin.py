#!/usr/bin/env python3
"""Exact-structure checks for the Round-014 first-layer margin formulas."""

from __future__ import annotations

import math


def solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Small pivoted Gaussian solve used only by this independent checker."""
    aug = [row[:] + [value] for row, value in zip(matrix, rhs)]
    n = len(rhs)
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        assert abs(scale) > 1.0e-14
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [value - factor * base for value, base in zip(aug[row], aug[col])]
    return [aug[row][-1] for row in range(n)]


def check_instance(alpha: float, rho: float, terminal: bool) -> None:
    a0 = (1.0 + alpha) / 2.0
    h0 = (1.0 - alpha) / 2.0
    degrees = [3.0, 3.0, 2.0, 1.0]  # b1, b2, a1, r1
    q = [[0.0] * 4 for _ in range(4)]
    for index in range(4):
        q[index][index] = a0
    for child in range(1, 4):
        coupling = -h0 / math.sqrt(degrees[0] * degrees[child])
        q[0][child] = coupling
        q[child][0] = coupling
    ell = [
        alpha * (1.0 - 3.0 * rho) / math.sqrt(3.0),
        -alpha * rho * math.sqrt(3.0),
        -alpha * rho * math.sqrt(2.0),
        -alpha * rho,
    ]
    direct = solve(q, ell)

    xi1 = a0 * a0 - 11.0 * h0 * h0 / 18.0
    xb1 = alpha * (a0 - 3.0 * rho) / (math.sqrt(3.0) * xi1)
    formula = [
        xb1,
        (h0 * xb1 / 3.0 - alpha * rho * math.sqrt(3.0)) / a0,
        (h0 * xb1 / math.sqrt(6.0) - alpha * rho * math.sqrt(2.0)) / a0,
        (h0 * xb1 / math.sqrt(3.0) - alpha * rho) / a0,
    ]
    for got, expected in zip(formula, direct):
        assert math.isclose(got, expected, rel_tol=2.0e-12, abs_tol=2.0e-12)

    if terminal:
        boundary = [(1, 3.0, 1.0), (2, 2.0, 1.0), (1, 3.0, 1.0)]
        displayed = min(
            formula[1] - alpha * rho * math.sqrt(3.0) / h0,
            formula[2] - alpha * rho * math.sqrt(2.0) / h0,
        )
    else:
        boundary = [(1, 3.0, 3.0), (2, 2.0, 2.0), (1, 3.0, 1.0)]
        displayed = min(
            formula[1] - 3.0 * alpha * rho * math.sqrt(3.0) / h0,
            formula[2] - 2.0 * alpha * rho * math.sqrt(2.0) / h0,
        )

    ratios = []
    for parent, parent_degree, child_degree in boundary:
        beta = h0 / math.sqrt(parent_degree * child_degree)
        demand = -alpha * rho * math.sqrt(child_degree) + beta * formula[parent]
        ratios.append(demand / beta)
    mu1 = min(ratios)
    assert mu1 > 0.0
    assert math.isclose(displayed, mu1, rel_tol=2.0e-12, abs_tol=2.0e-12)

    zero_gap = 0.5 * sum(
        formula[row] * q[row][col] * formula[col] for row in range(4) for col in range(4)
    )
    assert zero_gap > 0.0
    optimum = 0.5 * sum(
        formula[row] * q[row][col] * formula[col] for row in range(4) for col in range(4)
    ) - sum(ell[index] * formula[index] for index in range(4))
    assert math.isclose(zero_gap, -optimum, rel_tol=2.0e-12, abs_tol=2.0e-12)

    chi = alpha / (1.0 - alpha)
    for gap in (zero_gap, alpha * mu1 * mu1 / 8.0, 10.0 * zero_gap):
        logarithm = max(0.0, math.log(4.0 * gap / (alpha * mu1 * mu1)))
        stage_cap = 1 + math.floor(2.0 * logarithm / math.sqrt(chi))
        upper = 2.0 * math.exp(-stage_cap * math.sqrt(chi) / 2.0) * gap
        assert upper < alpha * mu1 * mu1 / 2.0


def main() -> None:
    for alpha in (0.05, 0.2, 0.49):
        for terminal in (False, True):
            check_instance(alpha, rho=1.0e-5, terminal=terminal)
    print("round014 first-layer margin checks passed")


if __name__ == "__main__":
    main()
