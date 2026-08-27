#!/usr/bin/env python3
"""Exact reduction and finite evidence for the five static frontier rows."""

from __future__ import annotations

from fractions import Fraction
import math

import numpy as np

import verify as base


def exact_frontier_data(edge_count: int) -> tuple[Fraction, list[Fraction], list[Fraction]]:
    q = Fraction(1, 16 * edge_count)
    delta = 1 - q
    eta = (1 - q * q) / 2
    degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]
    position = [Fraction(0)]
    velocity = [Fraction(0)]
    entry_residuals: list[list[Fraction]] = []
    frontier_optima: list[Fraction] = []
    final_raw_frontier = Fraction(0)

    for length in range(1, edge_count + 1):
        entry_residuals.append(base._fraction_residual(position, degrees[:length], q))
        optimum = base._fraction_optimum(length, degrees, q)
        frontier_optima.append(optimum[-1])
        position_next, velocity_next = base._fraction_step(position, velocity, degrees[:length], q)
        if length == edge_count:
            final_raw_frontier = position_next[-1]
        new_optimum = base._fraction_optimum(length + 1, degrees, q)
        position = position_next + [Fraction(0)]
        velocity = [
            value + new_value - old_value
            for value, new_value, old_value in zip(
                velocity_next + [Fraction(0)],
                new_optimum,
                optimum + [Fraction(0)],
                strict=True,
            )
        ]
    entry_residuals.append(base._fraction_residual(position, degrees, q))

    corrections: dict[int, list[Fraction]] = {}
    for length in (edge_count - 1, edge_count):
        ideal = base._fraction_ideal_prefix_packet(length, q)
        corrections[length] = [
            -actual - ideal_value
            for actual, ideal_value in zip(entry_residuals[length - 1], ideal, strict=True)
        ]

    rescaled_current = [
        value / (q**3 * delta ** (edge_count - 2)) for value in corrections[edge_count]
    ]
    rescaled_previous = [
        value / (q**3 * delta ** (edge_count - 3)) for value in corrections[edge_count - 1]
    ]

    def x(distance: int) -> Fraction:
        return rescaled_current[edge_count - distance]

    def previous_x(distance: int) -> Fraction:
        return rescaled_previous[edge_count - 1 - distance]

    def correction_k(distance: int) -> Fraction:
        return x(distance) - previous_x(distance - 1) / 2

    p_previous = frontier_optima[edge_count - 2] / q**2
    source_e = delta ** (-(edge_count - 2)) * (Fraction(1, 5) - eta * p_previous / 2)

    d_formula = [Fraction(0) for _ in range(6)]
    d_formula[1] = -(correction_k(2) + source_e) / 2
    d_formula[2] = x(2) - correction_k(3) / 2 - correction_k(2) - x(1) / 2 - source_e / 4
    for distance in range(3, 6):
        d_formula[distance] = (
            previous_x(distance - 1) - correction_k(distance + 1) - correction_k(distance - 1)
        ) / 2

    entry_b = [q * value for value in base._fraction_residual(velocity, degrees, q)]
    gamma = [Fraction(0) for _ in range(edge_count + 1)]
    gamma[1:edge_count] = [
        -(q**2)
        * delta**edge_count
        * Fraction(math.comb(edge_count - 2, index - 1), 2 ** (edge_count - 1))
        for index in range(1, edge_count)
    ]
    deconvolution = [Fraction(0) for _ in range(edge_count + 1)]
    deconvolution[0] = -gamma[1] / 2
    deconvolution[-1] = gamma[-2] / 2
    deconvolution[1:-1] = [
        (gamma[index - 1] - gamma[index + 1]) / 4 for index in range(1, edge_count)
    ]
    static_data = [left - right for left, right in zip(entry_b, deconvolution, strict=True)]

    for distance in range(1, 6):
        assert static_data[edge_count - distance] == (
            q**3 * delta ** (edge_count - 1) * d_formula[distance]
        )

    p_value = frontier_optima[-1] / q**2
    scaled_sigma = final_raw_frontier / q**3
    beta = eta * (p_value - scaled_sigma) + delta**edge_count / (q * 2**edge_count)
    assert static_data[-1] / q**3 == beta

    exact_margins = [
        static_data[-2] + static_data[-1] / 4,
        static_data[-3] - static_data[-1] / 8,
        static_data[-4] - static_data[-2] / 4,
        static_data[-5] - static_data[-3] / 4,
        static_data[-6] - static_data[-4] / 4,
    ]
    formula_margins = [
        q**3 * (delta ** (edge_count - 1) * d_formula[1] + beta / 4),
        q**3 * (delta ** (edge_count - 1) * d_formula[2] - beta / 8),
        *[
            q**3 * delta ** (edge_count - 1) * (d_formula[distance] - d_formula[distance - 2] / 4)
            for distance in range(3, 6)
        ],
    ]
    assert exact_margins == formula_margins
    return q, static_data, exact_margins


def float_frontier_margins(edge_count: int) -> list[float]:
    q, degrees, _, velocity, _, _, _ = base.full_face_entry(edge_count)
    delta = 1.0 - q
    entry_b = q * base.residual(velocity, degrees, q)
    gamma = np.zeros(edge_count + 1)
    gamma[1:edge_count] = (
        -0.5 * q**2 * delta**edge_count * base.binomial_probabilities(edge_count - 2)
    )
    deconvolution = np.zeros(edge_count + 1)
    deconvolution[0] = -gamma[1] / 2.0
    deconvolution[-1] = gamma[-2] / 2.0
    deconvolution[1:-1] = (gamma[:-2] - gamma[2:]) / 4.0
    static_data = entry_b - deconvolution
    return [
        float((static_data[-2] + static_data[-1] / 4.0) / q**3),
        float((static_data[-3] - static_data[-1] / 8.0) / q**3),
        float((static_data[-4] - static_data[-2] / 4.0) / q**3),
        float((static_data[-5] - static_data[-3] / 4.0) / q**3),
        float((static_data[-6] - static_data[-4] / 4.0) / q**3),
    ]


def main() -> None:
    for edge_count in (8, 12, 16):
        q, _, margins = exact_frontier_data(edge_count)
        print(
            f"static_frontier_exact=m={edge_count} identities=pass "
            f"min_margin/q3={float(min(margins) / q**3):.9g} scope=FINITE"
        )

    q, _, margins = exact_frontier_data(64)
    assert all(margin > 0 for margin in margins)
    print(
        "static_frontier_exact=m=64 identities=pass signs=pass "
        f"min_margin/q3={float(min(margins) / q**3):.9g} scope=FINITE"
    )

    for edge_count in (64, 128, 256, 512, 1024):
        margins = float_frontier_margins(edge_count)
        assert min(margins) > 0.0
        print(
            f"static_frontier_screen=m={edge_count} "
            f"margins/q3={','.join(f'{value:.9g}' for value in margins)} scope=MEASURED"
        )
    print("terminal_static_frontier_reduction=PASS uniform_sign=OPEN")


if __name__ == "__main__":
    main()
