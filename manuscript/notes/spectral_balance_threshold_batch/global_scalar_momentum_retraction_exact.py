#!/usr/bin/env python3
"""Exact obstruction to a one-step scalar-retraction NAG proof.

The matrix is the normalized retained shifted RPPR matrix on one unit edge at
root 1/20.  A full-face current has nonnegative residual.  The maximal common
scalar applied to its momentum makes the input residual nonnegative exactly,
but the usual strongly-convex NAG potential increases even after the existing
active diagonal push and auxiliary clamp.  The state is embedded in a
canonical point-source shifted load, but is not asserted reachable from the
zero-start chronology.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


VERTICES = 2
ROOT = F(1, 20)
MOMENTUM = (1 - ROOT) / (1 + ROOT)
AUXILIARY_SCALE = (1 - ROOT) / ROOT
VELOCITY_PUSH_SCALE = ROOT / (1 - ROOT)
DIAGONAL = (1 + ROOT * ROOT) / 2
DELTA = (1 - ROOT * ROOT) / 2
OFF_DIAGONAL_COUPLING = DELTA / (VERTICES - 1)


def matvec(vector: list[F]) -> list[F]:
    return [
        DIAGONAL * vector[row]
        - OFF_DIAGONAL_COUPLING
        * sum((vector[column] for column in range(VERTICES) if column != row), F(0))
        for row in range(VERTICES)
    ]


def residual_map(vector: list[F]) -> list[F]:
    image = matvec(vector)
    return [vector[index] - image[index] for index in range(VERTICES)]


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    augmented = [row[:] + [rhs[index]] for index, row in enumerate(matrix)]
    for column in range(len(rhs)):
        pivot = next(row for row in range(column, len(rhs)) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(len(rhs)):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                left - factor * right for left, right in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(len(rhs))]


def matrix() -> list[list[F]]:
    return [
        [DIAGONAL if row == column else -OFF_DIAGONAL_COUPLING for column in range(VERTICES)]
        for row in range(VERTICES)
    ]


def dot(left: list[F], right: list[F]) -> F:
    return sum((left[index] * right[index] for index in range(len(left))), F(0))


def subtract(left: list[F], right: list[F]) -> list[F]:
    return [left[index] - right[index] for index in range(len(left))]


def add(left: list[F], right: list[F]) -> list[F]:
    return [left[index] + right[index] for index in range(len(left))]


def scale(coefficient: F, vector: list[F]) -> list[F]:
    return [coefficient * value for value in vector]


def energy(error: list[F], velocity: list[F]) -> F:
    estimate_error = subtract(error, scale(AUXILIARY_SCALE, velocity))
    return dot(error, matvec(error)) / 2 + ROOT * ROOT * dot(estimate_error, estimate_error) / 2


def serialize(value: object) -> object:
    if isinstance(value, F):
        return str(value)
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def main() -> None:
    current_residual = [F(0), F(1)]
    velocity = [F(5), F(0)]
    optimum_error = solve(matrix(), current_residual)
    velocity_image = matvec(velocity)
    raw_input_residual = subtract(
        current_residual,
        scale(MOMENTUM, velocity_image),
    )
    assert raw_input_residual[0] < 0
    admissible_ratios = [
        current_residual[index] / (MOMENTUM * velocity_image[index])
        for index in range(VERTICES)
        if velocity_image[index] > 0
    ]
    gamma = min([F(1), *admissible_ratios])
    assert gamma == 0

    input_residual = subtract(
        current_residual,
        scale(gamma * MOMENTUM, velocity_image),
    )
    assert min(input_residual) == 0
    assert input_residual[0] == 0

    active_push = scale(1 / DIAGONAL, residual_map(input_residual))
    gradient_displacement = add(
        scale(gamma * MOMENTUM, velocity),
        input_residual,
    )
    next_error = subtract(
        optimum_error,
        add(gradient_displacement, active_push),
    )
    next_velocity = [
        max(
            gradient_displacement[index] - VELOCITY_PUSH_SCALE * active_push[index],
            F(0),
        )
        for index in range(VERTICES)
    ]

    initial_energy = energy(optimum_error, velocity)
    next_energy = energy(next_error, next_velocity)
    ratio = next_energy / initial_energy
    assert ratio > 1
    assert ratio > 1 - ROOT

    # Embed the scaled state at a strictly positive center of a canonical edge
    # point-source phase.  This validates the load namespace, not chronology.
    alpha = ROOT * ROOT / (2 - ROOT * ROOT)
    smooth = 1 + alpha
    original_matrix = [
        [
            smooth / 2 if row == column else -smooth * OFF_DIAGONAL_COUPLING
            for column in range(VERTICES)
        ]
        for row in range(VERTICES)
    ]
    rho = F(1, 100000)
    original_load = [-alpha * rho for _ in range(VERTICES)]
    original_load[0] += alpha / (VERTICES - 1)
    original_optimum = solve(original_matrix, original_load)
    embedding_scale = F(1, 10**8)
    center_response = solve(
        original_matrix,
        scale(smooth * embedding_scale, current_residual),
    )
    phase_center = subtract(original_optimum, center_response)
    previous = subtract(phase_center, scale(embedding_scale, velocity))
    phase_optimum = add(phase_center, scale(embedding_scale, optimum_error))
    assert min(original_optimum) > 0
    assert min(phase_center) > 0
    assert min(previous) > 0
    assert all(
        phase_center[index] < phase_optimum[index] <= original_optimum[index]
        for index in range(VERTICES)
    )
    assert min(next_error) > 0
    assert subtract(
        original_load,
        [
            sum(
                (original_matrix[row][column] * phase_center[column] for column in range(VERTICES)),
                F(0),
            )
            for row in range(VERTICES)
        ],
    ) == scale(smooth * embedding_scale, current_residual)

    print(
        json.dumps(
            serialize(
                {
                    "warning": (
                        "exact canonical-load proof-interface obstruction; "
                        "zero-start reachability is not claimed"
                    ),
                    "graph": "one unit edge",
                    "root": ROOT,
                    "alpha": alpha,
                    "normalized_diagonal": DIAGONAL,
                    "normalized_edge_coupling": OFF_DIAGONAL_COUPLING,
                    "current_residual": current_residual,
                    "velocity": velocity,
                    "raw_input_residual": raw_input_residual,
                    "maximal_gamma": gamma,
                    "safe_input_residual": input_residual,
                    "active_push": active_push,
                    "initial_energy": initial_energy,
                    "next_energy": next_energy,
                    "energy_ratio": ratio,
                    "claimed_accelerated_factor": 1 - ROOT,
                    "embedding_scale": embedding_scale,
                    "canonical_rho": rho,
                    "canonical_phase_center": phase_center,
                    "canonical_previous_state": previous,
                    "canonical_phase_optimum": phase_optimum,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
