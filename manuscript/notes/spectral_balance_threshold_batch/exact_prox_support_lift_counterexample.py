#!/usr/bin/env python3
"""Exact support-entry obstruction for fixed-face and fixed-full APG recurrences.

The canonical point-source unit edge uses a rational accelerated-prox root.
Its first exact proximal point has singleton support and its second has full
support.  The script verifies the obstacle-multiplier terms absent from both a
zero-appended fixed-face recurrence and the natural fixed-full-dimensional APG
recurrence, as well as the strict Schur increase of the old ``Q^{-1}`` metric.
All decisions use Fraction.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import combinations


Vector = list[F]
Matrix = list[list[F]]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum((matrix[row][column] * vector[column] for column in range(2)), F(0)) for row in range(2)
    ]


def add(left: Vector, right: Vector) -> Vector:
    return [left[index] + right[index] for index in range(2)]


def subtract(left: Vector, right: Vector) -> Vector:
    return [left[index] - right[index] for index in range(2)]


def scale(factor: F, vector: Vector) -> Vector:
    return [factor * value for value in vector]


def solve_on_face(matrix: Matrix, load: Vector, face: tuple[int, ...]) -> Vector:
    result = [F(0), F(0)]
    if not face:
        return result
    if len(face) == 1:
        index = face[0]
        result[index] = load[index] / matrix[index][index]
        return result
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    result[0] = (matrix[1][1] * load[0] - matrix[0][1] * load[1]) / determinant
    result[1] = (matrix[0][0] * load[1] - matrix[1][0] * load[0]) / determinant
    return result


def obstacle_solution(matrix: Matrix, load: Vector) -> Vector:
    for size in range(3):
        for face in combinations(range(2), size):
            state = solve_on_face(matrix, load, face)
            residual = subtract(matvec(matrix, state), load)
            if all(state[index] > 0 for index in face) and all(
                residual[index] >= 0 for index in range(2) if index not in face
            ):
                return state
    raise AssertionError("the two-dimensional LCP has no enumerated solution")


def safe_box(matrix: Matrix, load: Vector, previous: Vector, current: Vector, theta: F) -> Vector:
    trial = add(current, scale(theta, subtract(current, previous)))
    support = tuple(index for index in range(2) if current[index] > 0)
    if support == (0,):
        raw = load[0] - matvec(matrix, trial)[0]
        correction = max(F(0), -raw / matrix[0][0])
        return [trial[0] - correction, F(0)]
    raw = subtract(load, matvec(matrix, trial))
    correction = obstacle_solution(matrix, scale(F(-1), raw))
    return subtract(trial, correction)


def projected_slack(matrix: Matrix, raw: Vector) -> Vector:
    correction = obstacle_solution(matrix, scale(F(-1), raw))
    slack = add(raw, matvec(matrix, correction))
    assert min(slack) >= 0
    assert all(correction[index] * slack[index] == 0 for index in range(2))
    return slack


def serialize(value: object) -> object:
    if isinstance(value, F):
        return str(value)
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def main() -> None:
    root = F(1, 10)
    alpha = root * root / (1 - root * root)
    theta = (1 - root) / (1 + root)
    rho = F(1, 3)
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    matrix = [[diagonal, -coupling], [-coupling, diagonal]]
    proximal = [[1 + diagonal, -coupling], [-coupling, 1 + diagonal]]
    load = [alpha * (1 - rho), -alpha * rho]

    zero = [F(0), F(0)]
    first = obstacle_solution(proximal, load)
    first_center = safe_box(matrix, load, zero, first, theta)
    second = obstacle_solution(proximal, add(load, first_center))
    second_center = safe_box(matrix, load, first, second, theta)
    second_trial = add(second, scale(theta, subtract(second, first)))
    assert first[0] > 0 and first[1] == 0
    assert min(second) > 0
    assert first_center == [F(40, 4917), F(0)]
    assert second_center == second_trial

    first_residual = subtract(load, matvec(matrix, first))
    first_positive_part = [first_residual[0], F(0)]
    released_multiplier = [F(0), -first_residual[1]]
    assert released_multiplier[1] > 0
    assert first_residual == subtract(first_positive_part, released_multiplier)

    second_residual = subtract(load, matvec(matrix, second))
    assert min(second_residual) > 0
    actual_raw = subtract(scale(1 + theta, second_residual), scale(theta, first_residual))
    zero_append_raw = subtract(scale(1 + theta, second_residual), scale(theta, first_positive_part))
    assert actual_raw == add(zero_append_raw, scale(theta, released_multiplier))

    actual_slack = projected_slack(matrix, actual_raw)
    zero_append_slack = projected_slack(matrix, zero_append_raw)
    center_slack = subtract(load, matvec(matrix, second_center))
    assert actual_slack == center_slack
    assert actual_slack != zero_append_slack

    # A fixed-full-dimensional version would retain the global center
    # residuals t^0=c-Qw^0 and t^1=c-Qw^1, use B=(I+Q)^{-1}, and predict
    # Proj_+^{Q^{-1}} B((1+theta)t^1-theta*t^0).  Proximal KKT gives instead
    # the extra term theta(I-B)lambda^1 here because lambda^2=0.
    initial_center_residual = load
    first_center_residual = subtract(load, matvec(matrix, first_center))
    accelerated_center_argument = subtract(
        scale(1 + theta, first_center_residual),
        scale(theta, initial_center_residual),
    )
    fixed_full_raw = solve_on_face(proximal, accelerated_center_argument, (0, 1))
    kernel_multiplier_injection = scale(
        theta,
        subtract(released_multiplier, solve_on_face(proximal, released_multiplier, (0, 1))),
    )
    assert kernel_multiplier_injection == [F(-833, 3605800), F(867, 3605800)]
    assert actual_raw == add(fixed_full_raw, kernel_multiplier_injection)
    assert min(fixed_full_raw) > 0
    fixed_full_slack = projected_slack(matrix, fixed_full_raw)
    assert fixed_full_slack == fixed_full_raw
    assert actual_slack == actual_raw
    assert actual_slack != fixed_full_slack

    # If one instead insists that every old-face APG state be made feasible
    # in the full orthant by zero extension, the discrepancy is larger: the
    # fixed-full APG step projects to zero while the real center is positive.
    zero_extended_initial = [initial_center_residual[0], F(0)]
    zero_extended_first = [first_center_residual[0], F(0)]
    zero_extended_argument = subtract(
        scale(1 + theta, zero_extended_first),
        scale(theta, zero_extended_initial),
    )
    zero_extended_full_raw = solve_on_face(proximal, zero_extended_argument, (0, 1))
    assert zero_extended_full_raw == [F(-73, 133100), F(-3577, 19831900)]
    zero_extended_full_slack = projected_slack(matrix, zero_extended_full_raw)
    assert zero_extended_full_slack == zero
    assert actual_slack != zero_extended_full_slack

    old_inverse_metric = 1 / diagonal
    lifted_inverse_metric = diagonal / alpha
    schur_jump_ratio = lifted_inverse_metric / old_inverse_metric
    assert schur_jump_ratio == diagonal * diagonal / alpha
    assert schur_jump_ratio > 1

    print(
        json.dumps(
            serialize(
                {
                    "warning": "proof-interface obstruction, not a rate counterexample",
                    "alpha": alpha,
                    "proximal_root": root,
                    "theta": theta,
                    "rho": rho,
                    "first_prox": first,
                    "first_center": first_center,
                    "first_residual": first_residual,
                    "released_multiplier": released_multiplier,
                    "second_prox": second,
                    "second_clipping_correction": subtract(second_trial, second_center),
                    "actual_trial_slack": actual_raw,
                    "zero_append_trial_slack": zero_append_raw,
                    "actual_projected_slack": actual_slack,
                    "zero_append_projected_slack": zero_append_slack,
                    "fixed_full_apg_raw_prediction": fixed_full_raw,
                    "fixed_full_apg_projected_prediction": fixed_full_slack,
                    "fixed_full_kernel_multiplier_injection": kernel_multiplier_injection,
                    "zero_extended_full_apg_raw_prediction": zero_extended_full_raw,
                    "zero_extended_full_apg_projected_prediction": (
                        zero_extended_full_slack
                    ),
                    "old_inverse_metric": old_inverse_metric,
                    "lifted_inverse_metric": lifted_inverse_metric,
                    "schur_jump_ratio": schur_jump_ratio,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
