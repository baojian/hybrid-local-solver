#!/usr/bin/env python3
"""Exact audit of an Omega(alpha^-1/2) repeated-peeling ABoxStop delay.

The instance is the canonical point-source RPPR objective on one unit edge.
All arithmetic and all event-time comparisons use ``fractions.Fraction``.
The dense two-coordinate operations are proof checks, not a local solver.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


Q = Fraction
Vector = tuple[Q, Q]
Matrix = tuple[tuple[Q, Q], tuple[Q, Q]]


def add(left: Vector, right: Vector) -> Vector:
    return (left[0] + right[0], left[1] + right[1])


def subtract(left: Vector, right: Vector) -> Vector:
    return (left[0] - right[0], left[1] - right[1])


def scale(value: Q, vector: Vector) -> Vector:
    return (value * vector[0], value * vector[1])


def dot(left: Vector, right: Vector) -> Q:
    return left[0] * right[0] + left[1] * right[1]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def solve_edge(matrix: Matrix, right: Vector) -> Vector:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2
    return (
        (matrix[1][1] * right[0] - matrix[0][1] * right[1]) / determinant,
        (-matrix[1][0] * right[0] + matrix[0][0] * right[1]) / determinant,
    )


def peeling_pass(
    matrix: Matrix,
    load: Vector,
    current: Vector,
    trial: Vector,
) -> tuple[Vector, Vector, tuple[Q, ...]]:
    """Run the literal event-driven peeling pass exactly."""
    direction = subtract(trial, current)
    increment: Vector = (Q(0), Q(0))
    moving = {0, 1}
    elapsed = Q(0)
    event_times: list[Q] = []

    while moving and elapsed < 1:
        moving_direction: Vector = (
            direction[0] if 0 in moving else Q(0),
            direction[1] if 1 in moving else Q(0),
        )
        pressure = matvec(matrix, moving_direction)
        point = add(current, increment)
        residual = subtract(load, matvec(matrix, point))
        candidates = [
            (elapsed + residual[index] / pressure[index], index)
            for index in moving
            if pressure[index] > 0
        ]
        if not candidates:
            increment = add(increment, scale(1 - elapsed, moving_direction))
            elapsed = Q(1)
            break
        hit_time = min(time for time, _ in candidates)
        if hit_time >= 1:
            increment = add(increment, scale(1 - elapsed, moving_direction))
            elapsed = Q(1)
            break
        increment = add(increment, scale(hit_time - elapsed, moving_direction))
        elapsed = hit_time
        event_times.append(hit_time)
        for time, index in candidates:
            if time == hit_time:
                moving.remove(index)

    safe = add(current, increment)
    residual = subtract(load, matvec(matrix, safe))
    assert min(residual) >= 0
    assert min(subtract(safe, current)) >= 0
    assert min(subtract(trial, safe)) >= 0
    return safe, residual, tuple(event_times)


def audit(m: int) -> dict[str, object]:
    if m < 256 or m % 32:
        raise ValueError("m must be a multiple of 32 and at least 256")

    s = Q(1, m)
    alpha = s**2
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    matrix: Matrix = (
        (diagonal, -coupling),
        (-coupling, diagonal),
    )

    # Canonical unit-edge, source-zero, rho=1/4 RPPR data.
    rho = Q(1, 4)
    load: Vector = (alpha * (1 - rho), -alpha * rho)
    optimum = solve_edge(matrix, load)
    assert optimum == (Q(1, 4) + alpha / 2, Q(1, 4) - alpha / 2)

    eta = s**3
    initial_residual: Vector = (4 * eta, Q(0))
    current = subtract(optimum, solve_edge(matrix, initial_residual))
    correction: Vector = (4 * eta / s, 2 * eta / s)
    trial = add(current, correction)
    estimate = add(current, scale((1 + s) / s, correction))
    assert min(current) > 0
    assert subtract(load, matvec(matrix, current)) == initial_residual
    assert trial == scale(Q(1, 1 + s), add(current, scale(s, estimate)))

    safe = current
    scaled_e_1 = Q(4)
    scaled_e_2 = Q(2)
    scaled_r = Q(4)
    passes = m // 32
    first_ratio: Q | None = None
    last_ratio: Q | None = None
    maximum_events = 0
    movement_squared_sum = Q(0)
    movement_l1_sum = Q(0)

    for pass_index in range(1, passes + 1):
        difference = scaled_e_1 - scaled_e_2
        positive_pressure = diagonal * difference + alpha * scaled_e_2
        negative_pressure = coupling * difference - alpha * scaled_e_2
        theta = s * scaled_r / positive_pressure
        next_e_1 = scaled_e_1 * (1 - theta)
        next_e_2 = scaled_e_2 - theta * (coupling / diagonal) * scaled_e_1
        next_r = scaled_r * (coupling / diagonal) * negative_pressure / positive_pressure

        previous_safe = safe
        safe, residual, event_times = peeling_pass(matrix, load, safe, trial)
        maximum_events = max(maximum_events, len(event_times))
        assert len(event_times) == 2
        assert event_times[0] == theta
        assert event_times[1] == theta * coupling * scaled_e_1 / (diagonal * scaled_e_2)

        scaled_e_1, scaled_e_2, scaled_r = next_e_1, next_e_2, next_r
        actual_e = subtract(trial, safe)
        assert actual_e == (
            eta * scaled_e_1 / s,
            eta * scaled_e_2 / s,
        )
        assert residual == (eta * scaled_r, Q(0))
        assert min(actual_e) > 0
        assert actual_e[0] <= correction[0]
        assert actual_e[1] <= correction[1]

        accepted = subtract(safe, current)
        movement = subtract(safe, previous_safe)
        zeta = dot(actual_e, residual)
        credit = dot(accepted, matvec(matrix, accepted)) / 2
        estimate_gap = subtract(estimate, safe)
        credit += s * alpha * dot(estimate_gap, estimate_gap) / 2
        ratio = (1 + s) * zeta / credit
        assert ratio > 1
        off_diagonal_response = (coupling * movement[1], coupling * movement[0])
        assert residual[0] <= off_diagonal_response[0]
        assert residual[1] <= off_diagonal_response[1]
        assert dot(movement, movement) > ((s / (1 + s)) ** 2 * dot(correction, correction))
        movement_squared_sum += dot(movement, movement)
        movement_l1_sum += movement[0] + movement[1]
        if first_ratio is None:
            first_ratio = ratio
        last_ratio = ratio

        # The inequalities used by the uniform proof in the companion note.
        assert scaled_e_1 >= Q(10, 3)
        assert scaled_e_2 >= Q(4, 3)
        assert scaled_e_1 - scaled_e_2 >= 2 - 4 * alpha / 3
        assert scaled_r >= Q(15, 4)

    assert first_ratio is not None
    assert last_ratio is not None
    cumulative_movement = subtract(safe, current)
    assert movement_l1_sum == cumulative_movement[0] + cumulative_movement[1]
    assert movement_squared_sum <= dot(correction, correction)
    return {
        "arithmetic": "Fraction-exact",
        "graph": "one unit edge",
        "source": 0,
        "rho": str(rho),
        "m": m,
        "alpha": str(alpha),
        "certified_failed_passes": passes,
        "failed_passes_times_sqrt_alpha": float(passes * s),
        "first_stop_ratio": float(first_ratio),
        "last_stop_ratio": float(last_ratio),
        "events_per_pass": maximum_events,
        "minimum_current_coordinate": float(min(current)),
        "final_scaled_correction": [float(scaled_e_1), float(scaled_e_2)],
        "final_scaled_residual": float(scaled_r),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=4096)
    args = parser.parse_args()
    print(json.dumps(audit(args.m), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
