#!/usr/bin/env python3
"""Exact two-vertex stop for a naive input-safeguarded NAG proof.

The greatest safe point in the current momentum box does make the NAG input
a lower subsolution.  It does not, for an arbitrary safe physical state,
preserve the usual one-step ``1 - sqrt(alpha)`` estimate-potential bound.
All arithmetic below uses ``Fraction``.  The state is not asserted reachable
from the canonical zero-start chronology, so this is a proof-interface
counterexample rather than a counterexample to that algorithm.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [
        sum((matrix[row][column] * vector[column] for column in range(len(vector))), F(0))
        for row in range(len(matrix))
    ]


def subtract(left: list[F], right: list[F]) -> list[F]:
    return [left[index] - right[index] for index in range(len(left))]


def squared_norm(vector: list[F]) -> F:
    return sum((value * value for value in vector), F(0))


def objective(matrix: list[list[F]], load: list[F], vector: list[F]) -> F:
    image = matvec(matrix, vector)
    return sum((vector[index] * image[index] for index in range(len(vector))), F(0)) / 2 - sum(
        (load[index] * vector[index] for index in range(len(vector))), F(0)
    )


def main() -> None:
    # The endpoint-seeded unit edge with alpha = (3/10)^2.  Its eigenvalues
    # are alpha and one, so the retained NAG root is exactly 3/10.
    root = F(3, 10)
    alpha = root * root
    rho = F(1, 100)
    matrix = [[F(109, 200), -F(91, 200)], [-F(91, 200), F(109, 200)]]
    load = [alpha * (1 - rho), -alpha * rho]
    optimum = [F(107, 200), F(89, 200)]

    current = [F(19, 50), F(13, 50)]
    estimate = [F(29, 50), F(27, 100)]
    current_residual = subtract(load, matvec(matrix, current))
    assert current_residual == [F(3, 10000), F(303, 10000)]
    assert all(value >= 0 for value in current_residual)
    assert all(current[index] <= estimate[index] for index in range(2))
    assert matvec(matrix, optimum) == load

    input_point = [
        (current[index] + root * estimate[index]) / (1 + root) for index in range(2)
    ]
    input_residual = subtract(load, matvec(matrix, input_point))
    assert input_point == [F(277, 650), F(341, 1300)]
    assert input_residual == [-F(6189, 260000), F(13011, 260000)]

    # The correction is the exact Q^{-1}-metric projection/LCP correction.
    correction = [F(6189, 141700), F(0)]
    safe_input = subtract(input_point, correction)
    safe_residual = subtract(load, matvec(matrix, safe_input))
    assert safe_input == [F(4169, 10900), F(341, 1300)]
    assert safe_residual == [F(0), F(171, 5668)]
    assert all(current[index] <= safe_input[index] <= input_point[index] for index in range(2))
    assert all(value >= 0 for value in safe_residual)
    projected_slack = [
        input_residual[index] + matvec(matrix, correction)[index] for index in range(2)
    ]
    assert projected_slack == safe_residual
    assert all(correction[index] * projected_slack[index] == 0 for index in range(2))

    # Reset the estimate so that the safeguarded input remains the physical
    # NAG convex combination, and take the ordinary unit-smooth NAG step.
    safe_estimate = [
        current[index] + (1 + root) * (safe_input[index] - current[index]) / root
        for index in range(2)
    ]
    next_current = [safe_input[index] + safe_residual[index] for index in range(2)]
    next_estimate = [
        next_current[index]
        + (1 - root) * (next_current[index] - current[index]) / root
        for index in range(2)
    ]

    optimum_value = objective(matrix, load, optimum)

    def potential(primal: list[F], auxiliary: list[F]) -> F:
        return (
            objective(matrix, load, primal)
            - optimum_value
            + alpha * squared_norm(subtract(auxiliary, optimum)) / 2
        )

    initial_potential = potential(current, estimate)
    safeguarded_initial_potential = potential(current, safe_estimate)
    next_potential = potential(next_current, next_estimate)
    contraction_ratio = next_potential / initial_potential
    assert initial_potential == F(17181, 4000000)
    assert next_potential == F(145089, 43600000)
    assert contraction_ratio == F(161210, 208081)
    assert contraction_ratio > 1 - root
    assert safeguarded_initial_potential > initial_potential

    def serialize(value: object) -> object:
        if isinstance(value, F):
            return str(value)
        if isinstance(value, list):
            return [serialize(item) for item in value]
        if isinstance(value, dict):
            return {key: serialize(item) for key, item in value.items()}
        return value

    print(
        json.dumps(
            serialize(
                {
                    "warning": "exact proof-interface counterexample; reachability is not claimed",
                    "alpha": alpha,
                    "rho": rho,
                    "root": root,
                    "current": current,
                    "estimate": estimate,
                    "unsafe_input_residual": input_residual,
                    "safe_input": safe_input,
                    "safe_input_residual": safe_residual,
                    "initial_potential": initial_potential,
                    "safeguarded_initial_potential": safeguarded_initial_potential,
                    "next_potential": next_potential,
                    "observed_ratio": contraction_ratio,
                    "claimed_one_step_factor": 1 - root,
                    "strict_excess": contraction_ratio - (1 - root),
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
