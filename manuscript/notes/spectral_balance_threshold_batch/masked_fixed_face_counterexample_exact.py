#!/usr/bin/env python3
"""Exact point-source fixed-face stop for history-free lead induction.

The enhanced masked and unpushed omniscient recurrences start from the same
zero state on the same supplied full face, with one point-source residual.  The
first-to-second-product lead holds, as predicted by the phase-base identity,
but the third-product one-step lead reverses before the quarter-residual stop.
Hence a proof for the canonical one-source run must use its *locally grown*
face history; even a point source on a supplied fixed face is insufficient.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


ROOT = F(1, 250)
ALPHA = ROOT * ROOT / (2 - ROOT * ROOT)  # 1/124999
DIAGONAL = (1 + 3 * ALPHA) / 2
COUPLING = (1 - ALPHA) / 2
LIPSCHITZ = 1 + ALPHA
MOMENTUM = (1 - ROOT) / (1 + ROOT)
AUXILIARY_SCALE = (1 - ROOT) / ROOT

EDGES = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 7),
    (0, 9),
    (0, 10),
    (0, 11),
    (1, 2),
    (1, 5),
    (1, 9),
    (2, 3),
    (2, 7),
    (2, 10),
    (3, 4),
    (3, 6),
    (4, 7),
    (4, 8),
    (5, 6),
    (6, 8),
    (9, 11),
    (10, 11),
)
INITIAL_RESIDUAL = (F(1),) + (F(0),) * 11


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def add(left: list[F], right: list[F]) -> list[F]:
    return [a + b for a, b in zip(left, right)]


def subtract(left: list[F], right: list[F]) -> list[F]:
    return [a - b for a, b in zip(left, right)]


def scale(value: F, vector: list[F]) -> list[F]:
    return [value * item for item in vector]


def main() -> None:
    size = 12
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
    direction = matvec(matrix, [F(1) for _ in range(size)])
    assert all(value == 2 * ALPHA for value in direction)

    load = list(INITIAL_RESIDUAL)
    lower = [F(0) for _ in range(size)]
    current = lower[:]
    previous = lower[:]
    omniscient_lower = lower[:]
    omniscient_current = lower[:]
    omniscient_previous = lower[:]
    leads: list[tuple[int, int, F]] = []
    post_push_residual_maxima: list[F] = []
    masked_raw_residual_minima: list[tuple[int, int, F]] = []
    omniscient_lower_history: list[list[F]] = []

    def retract(
        state: list[F], prior: list[F], envelope: list[F]
    ) -> tuple[list[F], list[F], list[F], list[F]]:
        residual = subtract(load, matvec(matrix, state))
        shift = max([F(0)] + [-residual[i] / direction[i] for i in range(size)])
        envelope = [
            max(envelope[i], state[i] - shift, F(0)) for i in range(size)
        ]
        auxiliary = add(
            state, scale(AUXILIARY_SCALE, subtract(state, prior))
        )
        state = [max(state[i], envelope[i]) for i in range(size)]
        auxiliary = [max(auxiliary[i], envelope[i]) for i in range(size)]
        prior = subtract(
            state, scale(F(1, 1) / AUXILIARY_SCALE, subtract(auxiliary, state))
        )
        return state, prior, envelope, auxiliary

    for product in range(1, 4):
        starting_lower = lower[:]

        extrapolate = add(
            current, scale(MOMENTUM, subtract(current, previous))
        )
        following = add(
            extrapolate,
            scale(
                F(1, 1) / LIPSCHITZ,
                subtract(load, matvec(matrix, extrapolate)),
            ),
        )
        previous, current = current, following
        raw_residual = subtract(load, matvec(matrix, current))
        raw_vertex = min(range(size), key=raw_residual.__getitem__)
        masked_raw_residual_minima.append(
            (product, raw_vertex, raw_residual[raw_vertex])
        )
        current, previous, lower, auxiliary = retract(
            current, previous, lower
        )
        residual = subtract(load, matvec(matrix, lower))
        increment = [max(value, F(0)) / DIAGONAL for value in residual]
        lower = add(lower, increment)
        post_push_residual = subtract(load, matvec(matrix, lower))
        post_push_residual_maxima.append(
            max([F(0)] + post_push_residual)
        )
        current = [max(current[i], lower[i]) for i in range(size)]
        auxiliary = [max(auxiliary[i], lower[i]) for i in range(size)]
        previous = subtract(
            current,
            scale(F(1, 1) / AUXILIARY_SCALE, subtract(auxiliary, current)),
        )

        omniscient_extrapolate = add(
            omniscient_current,
            scale(
                MOMENTUM,
                subtract(omniscient_current, omniscient_previous),
            ),
        )
        omniscient_following = add(
            omniscient_extrapolate,
            scale(
                F(1, 1) / LIPSCHITZ,
                subtract(load, matvec(matrix, omniscient_extrapolate)),
            ),
        )
        omniscient_previous, omniscient_current = (
            omniscient_current,
            omniscient_following,
        )
        (
            omniscient_current,
            omniscient_previous,
            omniscient_lower,
            _,
        ) = retract(
            omniscient_current, omniscient_previous, omniscient_lower
        )
        omniscient_lower_history.append(omniscient_lower[:])

        if product > 1:
            gaps = [
                starting_lower[i] - omniscient_lower[i] for i in range(size)
            ]
            vertex = min(range(size), key=gaps.__getitem__)
            leads.append((product, vertex, gaps[vertex]))

    second = next(item for item in leads if item[0] == 2)
    first_negative = next(item for item in leads if item[2] < 0)
    minimum_masked_raw_residual = min(
        masked_raw_residual_minima, key=lambda item: item[2]
    )
    worst = min(leads, key=lambda item: item[2])
    assert second[2] >= 0
    assert first_negative[0] == 3
    assert minimum_masked_raw_residual[2] >= 0
    # With old_width=1/(2*alpha), the phase stop threshold in residual
    # coordinates is exactly 1/4.  The violating third product is executed
    # and is the first product that meets that stopping threshold.
    assert post_push_residual_maxima[0] > F(1, 4)
    assert post_push_residual_maxima[1] > F(1, 4)
    assert post_push_residual_maxima[2] <= F(1, 4)

    # Repeat only the masked side with the canonical minimal initial face
    # {source} and exact-positive append closure.  The omniscient comparator
    # is unchanged.  The first closure reaches the whole connected graph, but
    # the positive values deposited along that causal cascade preserve the
    # third-product lead that the gratuitously supplied zero rows destroy.
    local_face = {0}
    local_lower = [F(0) for _ in range(size)]
    local_current = local_lower[:]
    local_previous = local_lower[:]
    local_leads: list[F] = []
    local_face_sizes: list[int] = []
    for product in range(1, 4):
        starting_local_lower = local_lower[:]
        extrapolate = [F(0) for _ in range(size)]
        following = [F(0) for _ in range(size)]
        for vertex in local_face:
            extrapolate[vertex] = local_current[vertex] + MOMENTUM * (
                local_current[vertex] - local_previous[vertex]
            )
        for vertex in local_face:
            following[vertex] = extrapolate[vertex] + (
                load[vertex] - matvec(matrix, extrapolate)[vertex]
            ) / LIPSCHITZ
        local_previous, local_current = local_current, following
        active_residual = subtract(load, matvec(matrix, local_current))
        active_direction = [
            sum(matrix[i][j] for j in local_face) for i in range(size)
        ]
        shift = max(
            [F(0)]
            + [
                -active_residual[i] / active_direction[i]
                for i in local_face
            ]
        )
        for vertex in local_face:
            local_lower[vertex] = max(
                local_lower[vertex], local_current[vertex] - shift, F(0)
            )
        local_auxiliary = add(
            local_current,
            scale(
                AUXILIARY_SCALE,
                subtract(local_current, local_previous),
            ),
        )
        for vertex in local_face:
            local_current[vertex] = max(
                local_current[vertex], local_lower[vertex]
            )
            local_auxiliary[vertex] = max(
                local_auxiliary[vertex], local_lower[vertex]
            )
            local_previous[vertex] = local_current[vertex] - (
                local_auxiliary[vertex] - local_current[vertex]
            ) / AUXILIARY_SCALE

        local_residual = subtract(load, matvec(matrix, local_lower))
        active_increment = [F(0) for _ in range(size)]
        for vertex in local_face:
            active_increment[vertex] = max(local_residual[vertex], F(0)) / DIAGONAL
        local_lower = add(local_lower, active_increment)
        local_residual = subtract(load, matvec(matrix, local_lower))
        for vertex in local_face:
            local_current[vertex] = max(
                local_current[vertex], local_lower[vertex]
            )
            local_auxiliary[vertex] = max(
                local_auxiliary[vertex], local_lower[vertex]
            )
            local_previous[vertex] = local_current[vertex] - (
                local_auxiliary[vertex] - local_current[vertex]
            ) / AUXILIARY_SCALE

        while True:
            batch = {
                vertex
                for vertex in range(size)
                if vertex not in local_face and local_residual[vertex] > 0
            }
            if not batch:
                break
            batch_increment = [F(0) for _ in range(size)]
            for vertex in batch:
                batch_increment[vertex] = local_residual[vertex] / DIAGONAL
            local_lower = add(local_lower, batch_increment)
            local_residual = subtract(load, matvec(matrix, local_lower))
            for vertex in batch:
                local_current[vertex] = local_lower[vertex]
                local_auxiliary[vertex] = local_lower[vertex]
                local_previous[vertex] = local_lower[vertex]
            local_face.update(batch)
        local_face_sizes.append(len(local_face))
        if product > 1:
            local_leads.append(
                min(
                    starting_local_lower[i]
                    - omniscient_lower_history[product - 1][i]
                    for i in range(size)
                )
            )
    assert local_face_sizes[0] == size
    assert min(local_leads) >= 0

    two_push_lower = [F(0) for _ in range(size)]
    two_push_current = two_push_lower[:]
    two_push_previous = two_push_lower[:]
    two_push_leads: list[F] = []
    for product in range(1, 4):
        starting_two_push_lower = two_push_lower[:]
        extrapolate = add(
            two_push_current,
            scale(
                MOMENTUM,
                subtract(two_push_current, two_push_previous),
            ),
        )
        following = add(
            extrapolate,
            scale(
                F(1, 1) / LIPSCHITZ,
                subtract(load, matvec(matrix, extrapolate)),
            ),
        )
        two_push_previous, two_push_current = two_push_current, following
        (
            two_push_current,
            two_push_previous,
            two_push_lower,
            two_push_auxiliary,
        ) = retract(two_push_current, two_push_previous, two_push_lower)
        for _ in range(2):
            two_push_residual = subtract(
                load, matvec(matrix, two_push_lower)
            )
            two_push_increment = [
                max(value, F(0)) / DIAGONAL for value in two_push_residual
            ]
            two_push_lower = add(two_push_lower, two_push_increment)
            two_push_current = [
                max(two_push_current[i], two_push_lower[i])
                for i in range(size)
            ]
            two_push_auxiliary = [
                max(two_push_auxiliary[i], two_push_lower[i])
                for i in range(size)
            ]
            two_push_previous = subtract(
                two_push_current,
                scale(
                    F(1, 1) / AUXILIARY_SCALE,
                    subtract(two_push_auxiliary, two_push_current),
                ),
            )
        if product > 1:
            two_push_leads.append(
                min(
                    starting_two_push_lower[i]
                    - omniscient_lower_history[product - 1][i]
                    for i in range(size)
                )
            )
    assert min(two_push_leads) > 0
    assert worst == first_negative and worst[2] < 0
    value = worst[2]
    print(
        json.dumps(
            {
                "warning": "exact point-source supplied-full-face stop, not a canonical locally-grown-face counterexample",
                "root": str(ROOT),
                "alpha": str(ALPHA),
                "vertices": size,
                "edges": EDGES,
                "initial_residual": [str(value) for value in INITIAL_RESIDUAL],
                "second_product_minimum_lead": float(second[2]),
                "first_negative_product": first_negative[0],
                "first_negative_vertex": first_negative[1],
                "first_negative_lead_decimal": float(first_negative[2]),
                "minimum_masked_raw_residual_product": minimum_masked_raw_residual[0],
                "minimum_masked_raw_residual_vertex": minimum_masked_raw_residual[1],
                "minimum_masked_raw_residual_decimal": float(
                    minimum_masked_raw_residual[2]
                ),
                "first_three_post_push_residual_maxima": [
                    float(value) for value in post_push_residual_maxima[:3]
                ],
                "synthetic_phase_residual_stop_threshold": 0.25,
                "minimal_face_sizes": local_face_sizes,
                "minimal_face_minimum_one_step_lead": float(min(local_leads)),
                "supplied_face_two_push_minimum_one_step_lead": float(
                    min(two_push_leads)
                ),
                "worst_product": worst[0],
                "worst_vertex": worst[1],
                "worst_lead_sign": -1,
                "worst_lead_decimal": float(value),
                "worst_numerator_digits": len(str(abs(value.numerator))),
                "worst_denominator_digits": len(str(value.denominator)),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
