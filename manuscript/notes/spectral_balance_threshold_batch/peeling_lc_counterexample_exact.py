#!/usr/bin/env python3
"""Exact canonical counterexample to per-step contraction for LC peeling.

The persistent-estimate exact safe box contracts the accelerated potential.
Replacing it by one peeling pass satisfies the certified additive inequality,
but need not even make the potential monotone on an arbitrary safe state.
The state below belongs to a canonical single-source unit-edge RPPR objective;
reachability from its zero start is not claimed.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


def main() -> None:
    root = F(1, 30)
    alpha = root * root
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    rho = F(1, 100)
    scale = F(1, 10**6)
    matrix = [[diagonal, -coupling], [-coupling, diagonal]]
    load = [alpha * (1 - rho), -alpha * rho]

    def apply(vector: list[F]) -> list[F]:
        return [
            matrix[row][0] * vector[0] + matrix[row][1] * vector[1]
            for row in range(2)
        ]

    def solve(rhs: list[F]) -> list[F]:
        determinant = diagonal * diagonal - coupling * coupling
        return [
            (diagonal * rhs[0] + coupling * rhs[1]) / determinant,
            (coupling * rhs[0] + diagonal * rhs[1]) / determinant,
        ]

    def subtract(left: list[F], right: list[F]) -> list[F]:
        return [left[index] - right[index] for index in range(2)]

    def b_norm_squared(vector: list[F]) -> F:
        image = apply(vector)
        return sum((vector[index] * image[index] for index in range(2)), F(0))

    def norm_squared(vector: list[F]) -> F:
        return sum((value * value for value in vector), F(0))

    optimum = solve(load)
    starting_slack = [F(0), diagonal * scale]
    current = subtract(optimum, solve(starting_slack))
    direction = [11 * scale, scale]
    estimate = [
        current[index] + (1 + root) * direction[index] / root
        for index in range(2)
    ]
    trial = [current[index] + direction[index] for index in range(2)]
    assert trial == [
        (current[index] + root * estimate[index]) / (1 + root)
        for index in range(2)
    ]
    assert min(current) > 0
    assert subtract(load, apply(current)) == starting_slack

    # Row zero freezes at time zero; row one moves for the whole pass.
    pressure = apply(direction)
    assert pressure[0] > 0 and pressure[1] < 0
    peeled = [current[0], current[1] + scale]
    correction = subtract(trial, peeled)
    peeled_slack = subtract(load, apply(peeled))
    assert peeled_slack == [coupling * scale, F(0)]
    zeta = sum(
        (correction[index] * peeled_slack[index] for index in range(2)), F(0)
    )
    assert zeta == 11 * coupling * scale * scale

    gradient = [-value for value in peeled_slack]
    next_current = subtract(peeled, gradient)
    next_estimate = [
        (1 - root) * estimate[index]
        + root * peeled[index]
        - gradient[index] / root
        for index in range(2)
    ]
    assert min(subtract(load, apply(next_current))) >= 0
    assert min(subtract(next_estimate, next_current)) >= 0

    def energy(primal: list[F], auxiliary: list[F]) -> F:
        primal_error = subtract(primal, optimum)
        auxiliary_error = subtract(auxiliary, optimum)
        return (
            b_norm_squared(primal_error) / 2
            + alpha * norm_squared(auxiliary_error) / 2
        )

    old_energy = energy(current, estimate)
    new_energy = energy(next_current, next_estimate)
    assert new_energy > old_energy
    assert new_energy > (1 - root) * old_energy

    movement = subtract(peeled, current)
    estimate_gap = subtract(estimate, peeled)
    negative_credit = (
        b_norm_squared(movement) / 2
        + root * alpha * norm_squared(estimate_gap) / 2
    )
    certified_upper_bound = (
        (1 - root) * old_energy
        + (1 - root * root) * zeta
        - (1 - root) * negative_credit
    )
    assert new_energy <= certified_upper_bound

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
                    "warning": "exact canonical objective; zero-start reachability of the state is not claimed",
                    "alpha": alpha,
                    "rho": rho,
                    "root": root,
                    "optimum": optimum,
                    "current": current,
                    "estimate": estimate,
                    "trial": trial,
                    "peeled": peeled,
                    "peeled_slack": peeled_slack,
                    "zeta": zeta,
                    "old_energy": old_energy,
                    "new_energy": new_energy,
                    "energy_growth": new_energy / old_energy,
                    "target_normalized_ratio": new_energy / ((1 - root) * old_energy),
                    "certified_upper_bound": certified_upper_bound,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
