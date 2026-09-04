#!/usr/bin/env python3
"""Exact two-vertex zero-start audit for repeated-Peeling ABoxStop.

The instance is the canonical unit edge with ``alpha=s**2``, point source
zero, and ``rho=1/2-s``.  After the second SafeBoxLC outer update both
coordinates are positive.  From that point the state has the exact form

    c-Qx = R (1,1),       z-x = (V,W).

This verifier evolves only ``(R,V,W)``.  Every peeling event time, ABoxStop
decision, and outer transition uses ``fractions.Fraction``.  The decimal
fields in the final JSON are display-only.  It is an exact finite-instance
check accompanying the asymptotic proof in the companion note; it is not by
itself the proof of the asymptotic lower bound.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F


Vector = tuple[F, F]


def add(left: Vector, right: Vector) -> Vector:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Vector, right: Vector) -> Vector:
    return left[0] - right[0], left[1] - right[1]


def scale(factor: F, vector: Vector) -> Vector:
    return factor * vector[0], factor * vector[1]


def apply_q(s: F, vector: Vector) -> Vector:
    a = (1 + s * s) / 2
    b = (1 - s * s) / 2
    return a * vector[0] - b * vector[1], -b * vector[0] + a * vector[1]


def q_norm_squared(s: F, vector: Vector) -> F:
    image = apply_q(s, vector)
    return vector[0] * image[0] + vector[1] * image[1]


def norm_squared(vector: Vector) -> F:
    return vector[0] * vector[0] + vector[1] * vector[1]


def peeling_pass(s: F, slack: Vector, direction: Vector) -> tuple[Vector, Vector]:
    """Run one literal two-coordinate event pass exactly."""
    elapsed = F(0)
    increment = (F(0), F(0))
    moving = [direction[0] > 0, direction[1] > 0]
    current_slack = slack

    while any(moving) and elapsed < 1:
        rate = (
            direction[0] if moving[0] else F(0),
            direction[1] if moving[1] else F(0),
        )
        pressure = apply_q(s, rate)
        candidates = [
            (current_slack[index] / pressure[index], index)
            for index in range(2)
            if moving[index] and pressure[index] > 0
        ]
        remaining_time = 1 - elapsed
        if not candidates:
            step = remaining_time
            hits: list[int] = []
        else:
            first_time = min(time for time, _ in candidates)
            if first_time >= remaining_time:
                step = remaining_time
                hits = []
            else:
                step = first_time
                hits = [index for time, index in candidates if time == first_time]

        increment = add(increment, scale(step, rate))
        current_slack = subtract(current_slack, scale(step, pressure))
        elapsed += step
        if elapsed == 1:
            break
        for index in hits:
            assert current_slack[index] == 0
            moving[index] = False

    assert 0 <= elapsed <= 1
    assert min(current_slack) >= 0
    assert min(increment) >= 0
    assert min(subtract(direction, increment)) >= 0
    return increment, current_slack


def initial_full_state(s: F) -> tuple[F, F, F]:
    """Return the exact state immediately after the second outer update."""
    # These expressions follow by doing the singleton first update and the
    # first frontier admission symbolically for rho=1/2-s.
    residual = s**3 * (1 - s) * (2 + s - 2 * s * s) / 2
    first = s * (1 - s) ** 2 * (1 + 2 * s) / 2
    second = s * s * (1 - s) * (3 - 2 * s) / 2
    assert residual > 0 and first > second > 0
    return residual, first, second


def outer_round(s: F, residual: F, first: F, second: F) -> tuple[F, F, F, int, bool, F]:
    """Run repeated peeling to the first exact ABoxStop success."""
    q = s / (1 + s)
    trial_increment = q * first, q * second
    remaining = trial_increment
    slack = residual, residual
    accepted = F(0), F(0)
    passes = 0

    while True:
        movement, slack = peeling_pass(s, slack, remaining)
        accepted = add(accepted, movement)
        remaining = subtract(remaining, movement)
        passes += 1

        zeta = remaining[0] * slack[0] + remaining[1] * slack[1]
        estimate_gap = first - accepted[0], second - accepted[1]
        credit = q_norm_squared(s, accepted) / 2
        credit += s**3 * norm_squared(estimate_gap) / 2
        if (1 + s) * zeta <= credit:
            break
        if passes > 10_000:
            raise RuntimeError("exact repeated peeling exceeded the safety cap")

    b = (1 - s * s) / 2
    a = (1 + s * s) / 2
    exact_continuation = trial_increment[1] + (residual - s * s * trial_increment[1]) / a
    shortfall = exact_continuation - accepted[0]
    assert accepted[1] == trial_increment[1]
    assert shortfall >= 0
    assert slack == (a * shortfall, (residual - s * s * trial_increment[1]) / a - b * shortfall)
    gamma = shortfall / (s * s * first)
    next_residual = b * (slack[0] + slack[1])
    next_first = (1 - s) * (first - accepted[0] + slack[0] / s)
    next_second = (1 - s) * (second - accepted[1] + slack[1] / s)
    assert next_residual > 0 and next_first > 0 and next_second >= 0

    # Positive homogeneity permits exact normalization by next_first.  This
    # keeps the rational state smaller without changing later event times or
    # stopping decisions.
    return (
        next_residual / next_first,
        F(1),
        next_second / next_first,
        passes,
        shortfall == 0,
        gamma,
    )


def serialize(value: object) -> object:
    if isinstance(value, F):
        return str(value)
    if isinstance(value, tuple | list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=128)
    parser.add_argument("--outer-rounds", type=int)
    args = parser.parse_args()
    if args.m < 20:
        raise ValueError("m must be at least 20")

    s = F(1, args.m)
    alpha = s * s
    residual, first, second = initial_full_state(s)
    # Normalize the exact full-support state.
    residual, second, first = residual / first, second / first, F(1)
    outer_rounds = args.outer_rounds or max(1, args.m // 10)
    total_passes = 2  # the two zero-start prefix rounds each use one pass
    pass_counts: list[int] = []
    nonexact_acceptances = 0
    snapshots: list[dict[str, object]] = []

    for index in range(3, outer_rounds + 1):
        residual, first, second, passes, exact_acceptance, gamma = outer_round(
            s, residual, first, second
        )
        pass_counts.append(passes)
        total_passes += passes
        nonexact_acceptances += int(not exact_acceptance)
        if index in {3, max(3, outer_rounds // 2), outer_rounds}:
            snapshots.append(
                {
                    "outer_round": index,
                    "passes": passes,
                    "exact_acceptance": exact_acceptance,
                    "gamma_decimal": float(gamma),
                    "kappa_decimal": float(residual / (s * s * first)),
                    "ratio_decimal": float(second / first),
                }
            )

    result = {
        "warning": "exact finite audit; the companion note proves the asymptotic statement",
        "m": args.m,
        "s": s,
        "alpha": alpha,
        "rho": F(1, 2) - s,
        "outer_rounds": outer_rounds,
        "total_passes": total_passes,
        "alpha_times_total_passes": alpha * total_passes,
        "minimum_passes": min(pass_counts, default=1),
        "maximum_passes": max(pass_counts, default=1),
        "nonexact_acceptances": nonexact_acceptances,
        "snapshots": snapshots,
    }
    print(json.dumps(serialize(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
