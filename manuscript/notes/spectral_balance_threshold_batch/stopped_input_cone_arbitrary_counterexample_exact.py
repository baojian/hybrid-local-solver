#!/usr/bin/env python3
"""Fraction-exact stopped-input-cone counterexample for arbitrary phase data.

The four-vertex matrix is the normalized shifted RPPR Hessian at retained
root 3/10.  A nonnegative initial residual passes the quarter-width
continuation test after product one, but product two would start with a
strictly negative active input residual.  The residual is embedded exactly
as a phase centered at a positive lower subsolution of a canonical
point-source RPPR instance.  That center is not asserted reachable from the
zero-start outer chronology, so reachability remains the essential premise.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


EDGES = ((0, 1), (0, 2), (0, 3), (1, 2))
NEIGHBORS = ({1, 2, 3}, {0, 2}, {0, 1}, {0})
DEGREES = tuple(map(len, NEIGHBORS))


def apply(vector: list[F]) -> list[F]:
    diagonal = F(109, 200)
    coupling = F(91, 200)
    return [
        diagonal * vector[vertex]
        - coupling
        * sum((vector[neighbor] for neighbor in NEIGHBORS[vertex]), F(0))
        / DEGREES[vertex]
        for vertex in range(len(vector))
    ]


def subtract(left: list[F], right: list[F]) -> list[F]:
    return [left[index] - right[index] for index in range(len(left))]


def solve(matrix: list[list[F]], load: list[F]) -> list[F]:
    augmented = [row[:] + [load[index]] for index, row in enumerate(matrix)]
    size = len(load)
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][entry] - factor * augmented[column][entry]
                for entry in range(size + 1)
            ]
    return [augmented[row][-1] for row in range(size)]


def main() -> None:
    root = F(3, 10)
    strong = root * root
    diagonal = F(109, 200)
    initial_residual = [F(4), F(1), F(128), F(32)]

    # Canonical point-source embedding.  The original RPPR alpha is chosen so
    # that 2*alpha/(1+alpha)=root^2.  In degree coordinates the original and
    # normalized shifted matrices are rational.
    alpha = F(9, 191)
    smooth = 1 + alpha
    rho = F(1, 1000)
    original = [[F(0) for _ in range(4)] for _ in range(4)]
    for vertex in range(4):
        original[vertex][vertex] = F(100, 191)
        for neighbor in NEIGHBORS[vertex]:
            original[vertex][neighbor] = -F(91, 191) / DEGREES[vertex]
    original_load = [-alpha * rho for _ in range(4)]
    original_load[0] += alpha / DEGREES[0]
    optimum = solve(original, original_load)
    embedding_scale = F(1, 10**6)
    response = solve(original, [smooth * embedding_scale * value for value in initial_residual])
    phase_center = [optimum[index] - response[index] for index in range(4)]
    assert min(phase_center) > 0
    assert all(phase_center[index] < optimum[index] for index in range(4))
    original_center_residual = subtract(
        original_load,
        [
            sum(
                (original[row][column] * phase_center[column] for column in range(4)),
                F(0),
            )
            for row in range(4)
        ],
    )
    assert original_center_residual == [
        smooth * embedding_scale * value for value in initial_residual
    ]
    shifted_load = [
        original_load[index] + alpha * phase_center[index] for index in range(4)
    ]
    shifted_center_image = [
        sum(
            (original[row][column] * phase_center[column] for column in range(4)),
            F(0),
        )
        + alpha * phase_center[row]
        for row in range(4)
    ]
    assert subtract(shifted_load, shifted_center_image) == original_center_residual

    # The phase starts from zero, so the initial residual is also its load.
    raw_current = initial_residual[:]
    raw_residual = subtract(initial_residual, apply(raw_current))
    pushed_lower = [
        raw_current[index] + raw_residual[index] / diagonal for index in range(4)
    ]
    raw_auxiliary = [value / root for value in raw_current]
    auxiliary = [
        max(raw_auxiliary[index], pushed_lower[index]) for index in range(4)
    ]
    next_input = [
        (pushed_lower[index] + root * auxiliary[index]) / (1 + root)
        for index in range(4)
    ]
    next_input_residual = subtract(initial_residual, apply(next_input))

    assert raw_residual == [
        F(15743, 600),
        F(6097, 200),
        F(23751, 400),
        F(819, 50),
    ]
    assert pushed_lower == [
        F(17051, 327),
        F(6206, 109),
        F(51655, 218),
        F(6764, 109),
    ]
    assert auxiliary == [F(17051, 327), F(6206, 109), F(1280, 3), F(320, 3)]
    assert next_input == [
        F(17051, 327),
        F(6206, 109),
        F(397795, 1417),
        F(102520, 1417),
    ]
    assert next_input_residual == [
        F(308749, 8175),
        F(1494353, 32700),
        -F(310303, 1700400),
        F(13853693, 850200),
    ]

    initial_width = max(initial_residual) / strong
    next_width = max(max(value, F(0)) for value in next_input_residual) / strong
    continuation_ratio = next_width / initial_width
    assert continuation_ratio == F(1494353, 4185600)
    assert continuation_ratio > F(1, 4)
    assert min(next_input_residual) < 0

    def serialize(value: object) -> object:
        if isinstance(value, F):
            return str(value)
        if isinstance(value, tuple):
            return [serialize(item) for item in value]
        if isinstance(value, list):
            return [serialize(item) for item in value]
        if isinstance(value, dict):
            return {key: serialize(item) for key, item in value.items()}
        return value

    print(
        json.dumps(
            serialize(
                {
                    "warning": "exact canonical-phase-center counterexample; zero-start reachability is not claimed",
                    "edges": EDGES,
                    "degrees": DEGREES,
                    "rppr_alpha": alpha,
                    "rho": rho,
                    "retained_root": root,
                    "normalized_strong_convexity": strong,
                    "embedding_scale": embedding_scale,
                    "phase_center": phase_center,
                    "initial_residual": initial_residual,
                    "next_input": next_input,
                    "next_input_residual": next_input_residual,
                    "continuation_ratio": continuation_ratio,
                    "quarter_threshold": F(1, 4),
                    "negative_margin": min(next_input_residual),
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
