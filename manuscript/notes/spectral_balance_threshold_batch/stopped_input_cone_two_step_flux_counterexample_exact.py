#!/usr/bin/env python3
"""Exact stopped two-step flux obstruction for masked input residuals.

The witness obeys the reduced one-push recurrence on a connected simple unit
graph.  Its first next-input residual is nonnegative, both of the first two
products pass the literal quarter-width continuation test, and the input to
product three is negative.  The initial full-face residual is not asserted
reachable from the canonical zero-start point-source chronology, so this is a
proof-interface obstruction rather than a counterexample to
``StoppedMaskedInputResidual``.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


NEIGHBORS = ({2, 3, 4}, {3}, {0, 3, 4}, {0, 1, 2, 4}, {0, 2, 3})
EDGES = tuple(
    (left, right) for left in range(len(NEIGHBORS)) for right in NEIGHBORS[left] if left < right
)
DEGREES = tuple(map(len, NEIGHBORS))

ROOT = F(1, 20)
NORMALIZED_DIAGONAL = (1 + ROOT * ROOT) / 2
NORMALIZED_COUPLING = (1 - ROOT * ROOT) / 2
MOMENTUM = (1 - ROOT) / (1 + ROOT)
VELOCITY_PUSH_SCALE = ROOT / (1 - ROOT)


def random_walk(vector: list[F]) -> list[F]:
    return [
        sum((vector[neighbor] for neighbor in NEIGHBORS[vertex]), F(0)) / DEGREES[vertex]
        for vertex in range(len(vector))
    ]


def step(input_residual: list[F], velocity: list[F]) -> dict[str, list[F]]:
    neighbor_input = random_walk(input_residual)
    push = [
        NORMALIZED_COUPLING / NORMALIZED_DIAGONAL * (input_residual[index] + neighbor_input[index])
        for index in range(len(input_residual))
    ]
    next_velocity = [
        max(
            MOMENTUM * velocity[index] + input_residual[index] - VELOCITY_PUSH_SCALE * push[index],
            F(0),
        )
        for index in range(len(input_residual))
    ]

    # With one full-face active diagonal-push batch, the certified residual is
    # exactly the neighbor flux K p, K=((1-s^2)/2)P.
    certified_residual = [NORMALIZED_COUPLING * value for value in random_walk(push)]
    neighbor_velocity = random_walk(next_velocity)
    next_input = [
        certified_residual[index]
        - MOMENTUM
        * (
            NORMALIZED_DIAGONAL * next_velocity[index]
            - NORMALIZED_COUPLING * neighbor_velocity[index]
        )
        for index in range(len(input_residual))
    ]
    return {
        "push": push,
        "velocity": next_velocity,
        "certified_residual": certified_residual,
        "input_residual": next_input,
    }


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


def main() -> None:
    initial_input = [F(0), F(800), F(0), F(500), F(0)]
    initial_velocity = [F(0) for _ in initial_input]
    phase_width = max(initial_input) / (ROOT * ROOT)

    first = step(initial_input, initial_velocity)
    second = step(first["input_residual"], first["velocity"])
    first_ratio = max(first["certified_residual"]) / (ROOT * ROOT * phase_width)
    second_ratio = max(second["certified_residual"]) / (ROOT * ROOT * phase_width)

    assert min(initial_input) >= 0
    assert min(first["input_residual"]) > 0
    assert first_ratio == F(1114407, 2566400) > F(1, 4)
    assert second_ratio == F(330779369823, 1317281792000) > F(1, 4)
    assert second["input_residual"][1] == -F(4389594301, 864466176) < 0

    print(
        json.dumps(
            serialize(
                {
                    "warning": (
                        "exact stopped full-face obstruction; canonical point-source "
                        "zero-start reachability is not claimed"
                    ),
                    "edges": EDGES,
                    "degrees": DEGREES,
                    "root": ROOT,
                    "normalized_diagonal": NORMALIZED_DIAGONAL,
                    "normalized_coupling": NORMALIZED_COUPLING,
                    "momentum": MOMENTUM,
                    "phase_width": phase_width,
                    "initial_input_residual": initial_input,
                    "product_1": first,
                    "product_1_continuation_ratio": first_ratio,
                    "product_2": second,
                    "product_2_continuation_ratio": second_ratio,
                    "product_3_negative_input_row": 1,
                    "product_3_negative_input_margin": second["input_residual"][1],
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
