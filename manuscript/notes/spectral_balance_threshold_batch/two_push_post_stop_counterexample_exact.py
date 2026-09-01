#!/usr/bin/env python3
"""Exact two-push lead reversal that occurs only after the phase must stop.

This fixed-face history has an arbitrary nonnegative initial residual, not a
canonical point-source/minimal-admission start.  It proves that two diagonal
pushes do not give an unconditional all-time temporal lead.  The predecessor
residual is already strictly below one quarter, however, so the reversing
product is unreachable under the intended stopped phase.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


ROOT = F(430, 51139)
ALPHA = ROOT * ROOT / (2 - ROOT * ROOT)
DIAGONAL = (1 + 3 * ALPHA) / 2
COUPLING = (1 - ALPHA) / 2
LIPSCHITZ = 1 + ALPHA
MOMENTUM = (1 - ROOT) / (1 + ROOT)
AUXILIARY_SCALE = (1 - ROOT) / ROOT

EDGES = (
    (0, 1),
    (0, 10),
    (1, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 8),
    (2, 9),
    (2, 11),
    (3, 4),
    (3, 10),
    (4, 5),
    (4, 7),
    (4, 10),
    (5, 6),
    (5, 7),
    (5, 8),
    (5, 9),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (10, 11),
)

# Exact decimal rationalization of the deterministic search witness.
INITIAL_RESIDUAL = tuple(
    F(value)
    for value in (
        "1.4371673058882067e-09",
        "1",
        "0.01538633195850794",
        "0.0004725821010569229",
        "2.6617764246431307e-09",
        "2.5087487947834067e-05",
        "2.3336170964280316e-07",
        "2.7542598242021725e-05",
        "4.880044265839293e-06",
        "2.1682153002127403e-05",
        "4.026572639252166e-09",
        "0.018651667286389315",
    )
)


def main() -> None:
    size = len(INITIAL_RESIDUAL)
    neighbors = [set() for _ in range(size)]
    for left, right in EDGES:
        neighbors[left].add(right)
        neighbors[right].add(left)
    degrees = [len(row) for row in neighbors]
    matrix = [[F(0) for _ in range(size)] for _ in range(size)]
    for vertex in range(size):
        matrix[vertex][vertex] = DIAGONAL
        for neighbor in neighbors[vertex]:
            matrix[vertex][neighbor] = -COUPLING / degrees[vertex]

    def matvec(vector: list[F]) -> list[F]:
        return [sum(matrix[i][j] * vector[j] for j in range(size)) for i in range(size)]

    def residual(vector: list[F]) -> list[F]:
        product = matvec(vector)
        return [INITIAL_RESIDUAL[i] - product[i] for i in range(size)]

    direction = matvec([F(1) for _ in range(size)])
    assert all(value == 2 * ALPHA for value in direction)

    def advance(
        current: list[F],
        previous: list[F],
        lower: list[F],
    ) -> tuple[list[F], list[F], list[F], list[F]]:
        extrapolate = [current[i] + MOMENTUM * (current[i] - previous[i]) for i in range(size)]
        input_residual = residual(extrapolate)
        following = [extrapolate[i] + input_residual[i] / LIPSCHITZ for i in range(size)]
        old_current = current
        current = following
        raw_residual = residual(current)
        shift = max([F(0)] + [-raw_residual[i] / direction[i] for i in range(size)])
        lower = [max(lower[i], current[i] - shift, F(0)) for i in range(size)]
        auxiliary = [
            current[i] + AUXILIARY_SCALE * (current[i] - old_current[i]) for i in range(size)
        ]
        current = [max(current[i], lower[i]) for i in range(size)]
        auxiliary = [max(auxiliary[i], lower[i]) for i in range(size)]
        previous = [current[i] - (auxiliary[i] - current[i]) / AUXILIARY_SCALE for i in range(size)]
        return current, previous, lower, auxiliary

    zero = [F(0) for _ in range(size)]
    lower = zero[:]
    current = zero[:]
    previous = zero[:]
    omniscient_lower = zero[:]
    omniscient_current = zero[:]
    omniscient_previous = zero[:]
    leads: list[tuple[int, int, F]] = []
    post_residual_maxima: list[F] = []

    for product in range(1, 4):
        starting_lower = lower[:]
        current, previous, lower, auxiliary = advance(current, previous, lower)
        (
            omniscient_current,
            omniscient_previous,
            omniscient_lower,
            _,
        ) = advance(
            omniscient_current,
            omniscient_previous,
            omniscient_lower,
        )
        if product > 1:
            gaps = [starting_lower[i] - omniscient_lower[i] for i in range(size)]
            vertex = min(range(size), key=gaps.__getitem__)
            leads.append((product, vertex, gaps[vertex]))

        for _ in range(2):
            lower_residual = residual(lower)
            increment = [max(lower_residual[i], F(0)) / DIAGONAL for i in range(size)]
            lower = [lower[i] + increment[i] for i in range(size)]
            current = [max(current[i], lower[i]) for i in range(size)]
            auxiliary = [max(auxiliary[i], lower[i]) for i in range(size)]
            previous = [
                current[i] - (auxiliary[i] - current[i]) / AUXILIARY_SCALE for i in range(size)
            ]
        post_residual_maxima.append(max([F(0)] + residual(lower)))

    assert leads[0][2] >= 0
    assert leads[1][2] < 0
    assert post_residual_maxima[0] < F(1, 4)
    print(
        json.dumps(
            {
                "warning": "exact arbitrary-residual fixed-face stop, not a canonical source-history counterexample",
                "root": str(ROOT),
                "alpha": str(ALPHA),
                "edges": EDGES,
                "first_three_post_push_residual_maxima": [
                    float(value) for value in post_residual_maxima
                ],
                "first_stopping_product": 1,
                "first_negative_lead_product": leads[1][0],
                "first_negative_lead_vertex": leads[1][1],
                "first_negative_lead_decimal": float(leads[1][2]),
                "first_negative_lead_numerator": str(leads[1][2].numerator),
                "first_negative_lead_denominator": str(leads[1][2].denominator),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
