#!/usr/bin/env python3
"""Focused checks for the Round-015 lower-point gate certificate."""

from __future__ import annotations

import math
from pathlib import Path


def solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Solve one small dense system with pivoted elimination."""
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    dimension = len(rhs)
    for column in range(dimension):
        pivot = max(range(column, dimension), key=lambda row: abs(augmented[row][column]))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        assert abs(scale) > 1.0e-14
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(dimension):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * base for value, base in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(dimension)]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """Multiply a small dense matrix by a vector."""
    return [sum(value * item for value, item in zip(row, vector)) for row in matrix]


def lower_map(
    alpha: float,
    matrix: list[list[float]],
    load: list[float],
    degrees: list[float],
    trial: list[float],
) -> list[float]:
    """Evaluate the displayed principal-face lower retraction."""
    residual = [left - right for left, right in zip(load, matvec(matrix, trial))]
    delta = (
        max(max(-value, 0.0) / math.sqrt(degree) for value, degree in zip(residual, degrees))
        / alpha
    )
    return [max(value - delta * math.sqrt(degree), 0.0) for value, degree in zip(trial, degrees)]


def first_layer(alpha: float, rho: float) -> tuple[list[list[float]], list[float]]:
    """Return the four-row first-layer system and shifted load."""
    a0 = (1.0 + alpha) / 2.0
    h0 = (1.0 - alpha) / 2.0
    degrees = [3.0, 3.0, 2.0, 1.0]
    matrix = [[0.0] * 4 for _ in range(4)]
    for index in range(4):
        matrix[index][index] = a0
    for child in range(1, 4):
        coupling = -h0 / math.sqrt(degrees[0] * degrees[child])
        matrix[0][child] = coupling
        matrix[child][0] = coupling
    load = [
        alpha * (1.0 - 3.0 * rho) / math.sqrt(3.0),
        -alpha * rho * math.sqrt(3.0),
        -alpha * rho * math.sqrt(2.0),
        -alpha * rho,
    ]
    return matrix, load


def check_lower_certificate(alpha: float, rho: float, terminal: bool) -> None:
    """Check lower order and all three one-sided boundary inequalities."""
    degrees = [3.0, 3.0, 2.0, 1.0]
    matrix, load = first_layer(alpha, rho)
    optimum = solve(matrix, load)
    assert min(optimum) > 0.0

    trials = [
        [0.0, 0.0, 0.0, 0.0],
        [1.2 * optimum[0], -0.1, 0.7 * optimum[2], 0.02],
        [0.99 * value for value in optimum],
        optimum,
    ]
    if terminal:
        boundary = [(1, 3.0, 1.0), (2, 2.0, 1.0), (1, 3.0, 1.0)]
    else:
        boundary = [(1, 3.0, 3.0), (2, 2.0, 2.0), (1, 3.0, 1.0)]

    h0 = (1.0 - alpha) / 2.0
    for trial in trials:
        lower = lower_map(alpha, matrix, load, degrees, trial)
        for value, exact in zip(lower, optimum):
            assert value >= 0.0
            assert value <= exact + 2.0e-12
        for parent, parent_degree, child_degree in boundary:
            beta = h0 / math.sqrt(parent_degree * child_degree)
            exact_demand = -alpha * rho * math.sqrt(child_degree) + beta * optimum[parent]
            lower_demand = -alpha * rho * math.sqrt(child_degree) + beta * lower[parent]
            assert exact_demand > 0.0
            assert lower_demand <= exact_demand + 2.0e-12
        if trial == optimum:
            assert all(
                math.isclose(value, exact, rel_tol=2.0e-12, abs_tol=2.0e-12)
                for value, exact in zip(lower, optimum)
            )


def check_stage_bound(alpha: float, gap: float, margin: float) -> None:
    """Check the strict analysis-side integer cap."""
    chi = alpha / (1.0 - alpha)
    factor = 4.0 * (alpha + math.sqrt(3.0)) ** 2 * gap / (alpha**3 * margin**2)
    logarithm = max(0.0, math.log(factor))
    stages = 1 + math.floor(2.0 * logarithm / math.sqrt(chi))
    contracted_gap = 2.0 * math.exp(-stages * math.sqrt(chi) / 2.0) * gap
    threshold = alpha**3 * margin**2 / (2.0 * (alpha + math.sqrt(3.0)) ** 2)
    assert contracted_gap < threshold


def check_stable_labels() -> None:
    """Require every Round-015 public anchor in the note source."""
    source = Path(__file__).with_name("main.tex").read_text(encoding="utf-8")
    labels = (
        "lem:branch-caterpillar-local-lower-gate-certificate",
        "eq:branch-caterpillar-local-lower-certificate-vector",
        "prop:branch-caterpillar-first-layer-row-preexposure-obstruction",
        "thm:branch-caterpillar-two-face-lower-handoff",
        "eq:branch-caterpillar-two-face-lower-prefix-eleven-vector",
        "eq:branch-caterpillar-two-face-lower-post-eleven-vector",
    )
    for label in labels:
        assert f"\\label{{{label}}}" in source


def main() -> None:
    for alpha in (0.05, 0.2, 0.49):
        for terminal in (False, True):
            check_lower_certificate(alpha, rho=1.0e-5, terminal=terminal)
        for gap in (1.0e-9, 1.0e-3, 1.0):
            check_stage_bound(alpha, gap=gap, margin=1.0e-4)
    assert 3 + 3 + 2 + 1 == 9
    assert 3 + 2 + 1 == 6
    check_stable_labels()
    print("round015 lower-point gate checks passed")


if __name__ == "__main__":
    main()
