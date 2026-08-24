#!/usr/bin/env python3
"""Exact checks for the Round-022 reset-budget obstruction and telescope."""

from __future__ import annotations

from fractions import Fraction
from experiments.proof_audits import note_directory, note_tex_source

from experiments.proof_audits.hybrid_aesp_locsor.incremental_face_transition import (
    admission_face,
    graph,
)


def quadratic_value(
    matrix: list[list[Fraction]],
    load: list[Fraction],
    point: list[Fraction],
) -> Fraction:
    """Evaluate one rational quadratic exactly."""
    product = [sum(entry * value for entry, value in zip(row, point)) for row in matrix]
    return sum(left * right for left, right in zip(point, product)) / 2 - sum(
        left * right for left, right in zip(load, point)
    )


def solve_two(matrix: list[list[Fraction]], load: list[Fraction]) -> list[Fraction]:
    """Solve a two-by-two rational system."""
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    assert determinant > 0
    return [
        (load[0] * matrix[1][1] - matrix[0][1] * load[1]) / determinant,
        (matrix[0][0] * load[1] - load[0] * matrix[1][0]) / determinant,
    ]


def check_path_three(sample_s: Fraction) -> None:
    """Reproduce the complete settled P3 trace and reset/drop identities."""
    assert Fraction(0) < sample_s < Fraction(1, 12)
    rho = Fraction(3, 10)
    alpha = sample_s / (1 + sample_s)
    poly_a = 1 + 2 * sample_s
    poly_e = 1 + 8 * sample_s + 8 * sample_s**2

    # Degree-scaled Hessian H=D^(1/2)QD^(1/2) on the path of degrees 1,2,1.
    denominator = 1 + sample_s
    matrix = [
        [
            poly_a / (2 * denominator),
            -Fraction(1, 2) / denominator,
            Fraction(0),
        ],
        [
            -Fraction(1, 2) / denominator,
            poly_a / denominator,
            -Fraction(1, 2) / denominator,
        ],
        [
            Fraction(0),
            -Fraction(1, 2) / denominator,
            poly_a / (2 * denominator),
        ],
    ]
    load = [alpha * (1 - rho), -2 * alpha * rho, -alpha * rho]

    point0 = [load[0] / matrix[0][0]]
    expected_point0 = 2 * sample_s * (1 - rho) / poly_a
    assert point0 == [expected_point0]

    demand1_scaled = load[1] - matrix[1][0] * point0[0]
    gate0 = sample_s * (1 - 12 * sample_s) / (20 * (1 + sample_s) * poly_a)
    assert demand1_scaled == 2 * gate0
    assert gate0 > 0

    matrix1 = [row[:2] for row in matrix[:2]]
    point1 = solve_two(matrix1, load[:2])
    expected_point1 = [
        4 * sample_s * (poly_a * (1 - rho) - rho) / poly_e,
        2 * sample_s * (1 - rho * (3 + 4 * sample_s)) / poly_e,
    ]
    assert point1 == expected_point1
    assert all(value > 0 for value in point1)

    gate1 = load[2] - matrix[2][1] * point1[1]
    expected_gate1 = sample_s * (1 - 4 * rho * (1 + sample_s) * poly_a) / ((1 + sample_s) * poly_e)
    assert gate1 == expected_gate1 < 0

    schur = matrix[1][1] - matrix[1][0] * matrix[0][1] / matrix[0][0]
    expected_schur = poly_e / (2 * (1 + sample_s) * poly_a)
    assert schur == expected_schur

    old_value = quadratic_value([[matrix[0][0]]], [load[0]], point0)
    new_value = quadratic_value(matrix1, load[:2], point1)
    drop = old_value - new_value
    expected_drop = 4 * (1 + sample_s) * poly_a * gate0**2 / poly_e
    assert drop == (2 * gate0) ** 2 / (2 * schur) == expected_drop > 0

    kkt_squared = 2 * gate0**2
    mu_envelope = alpha * (1 - 2 * alpha) / (1 - alpha)
    budget = kkt_squared / (2 * alpha) + mu_envelope * kkt_squared / alpha**2
    expected_budget = (3 - 2 * sample_s) * gate0**2 / alpha
    assert budget == expected_budget

    ratio = budget / drop
    expected_ratio = poly_e * (3 - 2 * sample_s) / (4 * poly_a * sample_s)
    exact_expansion = Fraction(3, 4) / sample_s + 2 * (2 + sample_s - 2 * sample_s**2) / poly_a
    assert ratio == expected_ratio == exact_expansion

    settled_coefficient = (3 - 5 * alpha) / (alpha * (1 - alpha))
    reset_prefactor = Fraction(1, 2) / alpha + mu_envelope / alpha**2
    assert 2 * reset_prefactor == settled_coefficient
    assert drop >= kkt_squared / 2
    assert budget <= settled_coefficient * drop


def check_conditional_scaling(root_ratio: Fraction) -> None:
    """Check the rational dominant term in the conditional telescope."""
    assert Fraction(0) < root_ratio < 1
    alpha = root_ratio**2 / (1 + root_ratio**2)
    mu_envelope = alpha * (1 - 2 * alpha) / (1 - alpha)
    prefactor = Fraction(1, 2) / alpha + mu_envelope / alpha**2
    beta = (1 - root_ratio) / (1 + root_ratio)
    expected_prefactor = (3 + root_ratio**2 - 2 * root_ratio**4) / (2 * root_ratio**2)
    assert prefactor == expected_prefactor

    dominant = 2 * prefactor * beta**2 / alpha
    scaled_dominant = root_ratio**4 * dominant
    expected_scaled = (
        (3 + root_ratio**2 - 2 * root_ratio**4)
        * (1 - root_ratio) ** 2
        * (1 + root_ratio**2)
        / (1 + root_ratio) ** 2
    )
    assert scaled_dominant == expected_scaled > 0


def check_literal_product_count(m: int) -> None:
    """Check the declared no-sharing two-product caterpillar row count."""
    adjacency = graph(m)
    volumes = []
    for face_index in range(1, m + 1):
        face = admission_face(m, face_index)
        volume = sum(len(adjacency[vertex]) for vertex in face)
        expected = 6 * face_index + 3 if face_index < m else 6 * m
        assert volume == expected
        volumes.append(volume)
    assert 2 * sum(volumes) == 6 * m**2 + 12 * m - 6


def check_stable_labels() -> None:
    """Require the public Round-022 anchors and scope guardrails."""
    directory = note_directory("hybrid_aesp_locsor")
    source = note_tex_source("hybrid_aesp_locsor")
    readme = (directory / "README.md").read_text(encoding="utf-8")
    labels = (
        "sec:settled-reset-budget-amortization",
        "eq:path-three-reset-parameters",
        "eq:path-three-first-settlement-demand",
        "eq:path-three-second-settlement",
        "eq:path-three-terminal-demand",
        "eq:path-three-reset-budget",
        "eq:path-three-schur-drop",
        "eq:path-three-reset-drop-ratio",
        "eq:settled-actual-shock-drop-bound",
        "prop:path-three-settled-reset-drop-obstruction",
        "lem:settled-reset-optimum-drop-bound",
        "eq:settled-reset-optimum-drop-bound",
        "prop:conditional-nested-reset-budget-telescope",
        "eq:conditional-reset-local-bound",
        "eq:conditional-reset-global-telescope",
        "eq:branch-caterpillar-literal-reset-product-count",
    )
    for label in labels:
        assert f"\\label{{{label}}}" in source
    assert "not a work\nlower bound" in source
    assert "inside a logarithm" in source
    assert "not\n$\\Theta(q_{\\rm r}^{-3})$" in source
    assert "literal} no-sharing" in source
    assert "not a necessary\ncost" in source
    assert "reset_budget_obstruction" in readme


def main() -> None:
    """Run exact path, telescope-scaling, ledger, and source checks."""
    for sample_s in (
        Fraction(1, 10_000),
        Fraction(1, 400),
        Fraction(1, 100),
        Fraction(1, 25),
        Fraction(1, 13),
    ):
        check_path_three(sample_s)
    for root_ratio in (
        Fraction(1, 100),
        Fraction(1, 20),
        Fraction(1, 10),
        Fraction(1, 4),
        Fraction(1, 2),
    ):
        check_conditional_scaling(root_ratio)
    for m in range(2, 25):
        check_literal_product_count(m)
    check_stable_labels()
    print("round022 reset-budget obstruction and telescope checks passed")


if __name__ == "__main__":
    main()
