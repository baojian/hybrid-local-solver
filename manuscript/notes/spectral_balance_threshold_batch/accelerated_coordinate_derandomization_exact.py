#!/usr/bin/env python3
"""Exact canonical stop for max-residual accelerated-coordinate derandomization.

Run with ``uv run --with sympy python accelerated_coordinate_derandomization_exact.py``.
The script checks the exact NU-ACDM branch-score identity and the point-source
RPPR three-vertex witness from ACCELERATED_COORDINATE_DERANDOMIZATION_STOP.md.
"""

from __future__ import annotations

import json

import sympy as sp


def quadratic_value(
    point: sp.Matrix,
    matrix: sp.Matrix,
    load: sp.Matrix,
) -> sp.Expr:
    return sp.expand((point.T * matrix * point)[0] / 2 - (load.T * point)[0])


def squared_norm(vector: sp.Matrix) -> sp.Expr:
    return sp.expand((vector.T * vector)[0])


def zero_start_supplied_face_trace() -> dict[str, object]:
    """Verify the zero-start Gauss--Southwell strengthening exactly."""
    alpha = sp.Rational(1, 10)
    rho = sp.Rational(1, 1000)
    size = 3
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    root_two = sp.sqrt(2)
    matrix = sp.Matrix(
        [
            [diagonal, -coupling / root_two, -coupling / root_two],
            [-coupling / root_two, diagonal, 0],
            [-coupling / root_two, 0, diagonal],
        ]
    )
    stationary = sp.Matrix([root_two, 1, 1])
    load = alpha * sp.Matrix([1, 0, 0]) / root_two - alpha * rho * stationary
    optimum = sp.simplify(matrix.inv() * load)
    tau = sp.Rational(2) / (1 + sp.sqrt(199))
    eta = sp.simplify(1 / (tau * size**2 * diagonal))
    choices = [0, 1, 2, 0, 1, 2, 0, 1]
    primal = sp.zeros(size, 1)
    auxiliary = sp.zeros(size, 1)
    final_score_gap = sp.Integer(0)
    final_gradient: list[sp.Expr] = []

    for iteration, chosen in enumerate(choices):
        current = sp.Matrix(sp.simplify(tau * auxiliary + (1 - tau) * primal))
        gradient = sp.Matrix(sp.simplify(matrix * current - load))
        auxiliary_center = sp.Matrix(
            sp.simplify((auxiliary + eta * alpha * current) / (1 + eta * alpha))
        )
        scores = [
            sp.simplify(
                gradient[index] ** 2 / (2 * diagonal)
                + size * gradient[index] * (auxiliary_center[index] - optimum[index])
            )
            for index in range(size)
        ]
        for index in range(size):
            dominance = sp.simplify(gradient[chosen] ** 2 - gradient[index] ** 2)
            assert dominance >= 0
            if index < chosen:
                assert dominance > 0

        next_primal = sp.Matrix(current)
        next_primal[chosen] = sp.simplify(next_primal[chosen] - gradient[chosen] / diagonal)
        next_auxiliary = sp.Matrix(auxiliary_center)
        next_auxiliary[chosen] = sp.simplify(
            next_auxiliary[chosen] - eta * size * gradient[chosen] / (1 + eta * alpha)
        )
        assert all(value >= 0 for value in next_primal)
        assert all(value >= 0 for value in next_auxiliary)

        if iteration == len(choices) - 1:
            final_score_gap = sp.factor(scores[chosen] - sum(scores, sp.Integer(0)) / size)
            final_gradient = list(gradient)
        primal = next_primal
        auxiliary = next_auxiliary

    numerator_a = sp.Integer(5206883677438968880700576045466387285942759064488726267403483901)
    numerator_b = sp.Integer(184502567533428390482163481628210822751800043275281785240489199)
    denominator = sp.Integer(66415297273919678808531096953240398855459148134920443936880000000)
    asserted_gap = (-numerator_a + 2 * numerator_b * sp.sqrt(199)) / denominator
    assert sp.simplify(final_score_gap - asserted_gap) == 0
    assert final_score_gap < 0
    rational_upper_numerator = sp.simplify(-numerator_a + 2 * numerator_b * sp.Rational(1411, 100))
    assert rational_upper_numerator < 0

    return {
        "alpha": str(alpha),
        "rho": str(rho),
        "choices": choices,
        "iteration_seven_gradient": [str(value) for value in final_gradient],
        "iteration_seven_gradient_decimal": [str(sp.N(value, 18)) for value in final_gradient],
        "chosen_score_minus_conditional_mean": str(final_score_gap),
        "chosen_score_minus_conditional_mean_decimal": str(sp.N(final_score_gap, 18)),
        "verified": (
            "zero-start max-gradient branch has potential strictly above "
            "the uniform conditional mean at iteration seven"
        ),
    }


def main() -> None:
    alpha = sp.Rational(1, 1000)
    rho = sp.Rational(1, 10000)
    scale = sp.Rational(1, 10**6)
    size = 3
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    root_two = sp.sqrt(2)

    matrix = sp.Matrix(
        [
            [diagonal, -coupling / root_two, -coupling / root_two],
            [-coupling / root_two, diagonal, 0],
            [-coupling / root_two, 0, diagonal],
        ]
    )
    stationary = sp.Matrix([root_two, 1, 1])
    source = sp.Matrix([1, 0, 0])
    load = alpha * source / root_two - alpha * rho * stationary
    optimum = sp.simplify(matrix.inv() * load)
    asserted_optimum = sp.Matrix(
        [sp.Rational(5003, 20000) * root_two, sp.Rational(4993, 20000), sp.Rational(4993, 20000)]
    )
    assert optimum == asserted_optimum
    assert sp.simplify(matrix * optimum - load) == sp.zeros(size, 1)
    assert all(value > 0 for value in optimum)

    residual_profile = sp.Matrix([9, 10, 11])
    inverse_response = sp.simplify(matrix.inv() * residual_profile)
    lower = sp.simplify(optimum - scale * inverse_response)
    residual = sp.simplify(load - matrix * lower)
    assert residual == scale * residual_profile
    assert all(value > 0 for value in lower)
    assert all(value > 0 for value in inverse_response)

    tau = sp.simplify(2 / (1 + sp.sqrt(1 + 4 * size**2 * diagonal / alpha)))
    eta = sp.simplify(1 / (tau * size**2 * diagonal))
    potential_weight = sp.simplify(tau / (2 * eta * (1 - tau)))
    coordinate_scale = sp.simplify(eta * size / (1 + eta * alpha))
    assert sp.simplify(alpha * (1 - tau) - tau**2 * size**2 * diagonal) == 0
    assert sp.simplify(1 + eta * alpha - 1 / (1 - tau)) == 0
    assert sp.simplify(potential_weight * coordinate_scale**2 - (1 - tau) / (2 * diagonal)) == 0
    assert sp.simplify(2 * potential_weight * coordinate_scale - tau * size) == 0

    current = lower
    auxiliary_center = lower
    gradient = sp.simplify(matrix * current - load)
    optimum_value = quadratic_value(optimum, matrix, load)
    common = sp.simplify(
        quadratic_value(current, matrix, load)
        - optimum_value
        + potential_weight * squared_norm(auxiliary_center - optimum)
    )
    current_potential = common

    branch_scores: list[sp.Expr] = []
    branch_potentials: list[sp.Expr] = []
    for index in range(size):
        basis = sp.eye(size).col(index)
        next_primal = sp.simplify(current - gradient[index] * basis / diagonal)
        next_auxiliary = sp.simplify(auxiliary_center - coordinate_scale * gradient[index] * basis)
        assert all(value > 0 for value in next_primal)
        assert all(value > 0 for value in next_auxiliary)
        score = sp.simplify(
            gradient[index] ** 2 / (2 * diagonal)
            + size * gradient[index] * (auxiliary_center[index] - optimum[index])
        )
        potential = sp.simplify(
            quadratic_value(next_primal, matrix, load)
            - optimum_value
            + potential_weight * squared_norm(next_auxiliary - optimum)
        )
        assert sp.simplify(potential - (common - tau * score)) == 0
        branch_scores.append(score)
        branch_potentials.append(potential)

    reduced_scores = [sp.simplify(value / scale**2) for value in branch_scores]
    conditional_gap = sp.factor(reduced_scores[0] + reduced_scores[1] - 2 * reduced_scores[2])
    asserted_gap = -sp.Rational(135584135, 2002) + sp.Rational(242757, 4) * root_two
    assert sp.simplify(conditional_gap - asserted_gap) == 0
    assert conditional_gap > 0
    assert reduced_scores[2] < sum(reduced_scores, sp.Integer(0)) / size
    assert branch_potentials[2] > sum(branch_potentials, sp.Integer(0)) / size
    contraction_gap = sp.factor(branch_potentials[2] - (1 - tau) * current_potential)
    asserted_contraction_gap = (
        3
        * (sp.sqrt(18019) - 1)
        * (-sp.Integer(6754568984311) + sp.Integer(6020007979986) * root_two)
        / sp.Integer(8024024008000000000000000)
    )
    assert sp.simplify(contraction_gap - asserted_contraction_gap) == 0
    assert contraction_gap > 0
    assert max(range(size), key=lambda index: residual[index]) == 2
    degree_normalized = [residual[0] / root_two, residual[1], residual[2]]
    assert max(range(size), key=lambda index: degree_normalized[index]) == 2

    print(
        json.dumps(
            {
                "graph": "three-vertex unit path with center source",
                "alpha": str(alpha),
                "rho": str(rho),
                "diagonal": str(diagonal),
                "optimum": [str(value) for value in optimum],
                "lower_state": [str(value) for value in lower],
                "residual": [str(value) for value in residual],
                "reduced_branch_scores": [str(value) for value in reduced_scores],
                "reduced_branch_scores_decimal": [str(sp.N(value, 18)) for value in reduced_scores],
                "max_residual_coordinate": 2,
                "conditional_mean_gap_R0_plus_R1_minus_2R2": str(conditional_gap),
                "conditional_mean_gap_decimal": str(sp.N(conditional_gap, 18)),
                "chosen_branch_contraction_gap": str(contraction_gap),
                "chosen_branch_contraction_gap_decimal": str(sp.N(contraction_gap, 18)),
                "verified": (
                    "max-residual branch is above the conditional mean and "
                    "violates the one-step accelerated contraction"
                ),
                "zero_start_supplied_face_trace": zero_start_supplied_face_trace(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
