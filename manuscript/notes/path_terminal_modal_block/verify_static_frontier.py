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

    # Exact finite first-order remainder interface from the note.
    coefficients = [Fraction(0)] + [
        -Fraction(4, 3) + Fraction((-1) ** distance, 3 * 2**distance) for distance in range(1, 8)
    ]
    source_e_next = delta ** (-(edge_count - 1)) * (Fraction(1, 5) - eta * p_value / 2)
    source_slope = (source_e_next - source_e) / q
    local_ell = [Fraction(0) for _ in range(6)]
    for distance in range(1, 6):
        current_y = (x(distance) - coefficients[distance] * source_e) / q
        next_x = x(distance) - d_formula[distance]
        next_y = (next_x - coefficients[distance + 1] * source_e_next) / q
        local_ell[distance] = current_y - next_y - coefficients[distance + 1] * source_slope
        assert d_formula[distance] == (
            (coefficients[distance] - coefficients[distance + 1]) * source_e
            + q * local_ell[distance]
        )
    endpoint_remainder = (beta - delta ** (edge_count - 1) * source_e) / q
    interface_margins = [
        delta ** (edge_count - 1) * local_ell[1] + endpoint_remainder / 4,
        delta ** (edge_count - 1) * local_ell[2] - endpoint_remainder / 8,
        *[
            delta ** (edge_count - 1) * (local_ell[distance] - local_ell[distance - 2] / 4)
            for distance in range(3, 6)
        ],
    ]
    assert [margin / q**4 for margin in exact_margins] == interface_margins
    return q, static_data, exact_margins


def check_first_order_limit_algebra() -> list[float]:
    """Check the triangular limit tables and positivity certificates exactly."""

    coefficients = [Fraction(0)] + [
        -Fraction(4, 3) + Fraction((-1) ** distance, 3 * 2**distance) for distance in range(1, 8)
    ]
    assert coefficients == [
        Fraction(0),
        -Fraction(3, 2),
        -Fraction(5, 4),
        -Fraction(11, 8),
        -Fraction(21, 16),
        -Fraction(43, 32),
        -Fraction(85, 64),
        -Fraction(171, 128),
    ]

    # A pair stores the coefficients of (nu, a) in the stationary y limit.
    def add(*values: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return tuple(sum(value[index] for value in values) for index in range(2))  # type: ignore[return-value]

    def scale(scalar: Fraction, value: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return scalar * value[0], scalar * value[1]

    nu_pair = (Fraction(1), Fraction(0))
    a_pair = (Fraction(0), Fraction(1))
    stationary: list[tuple[Fraction, Fraction]] = [(Fraction(0), Fraction(0))] * 8
    stationary[1] = add(scale(-2, nu_pair), scale(-2 * coefficients[1], a_pair))
    stationary[2] = add(
        scale(Fraction(3, 2), stationary[1]),
        scale(coefficients[1] / 2 - 2 * coefficients[2], a_pair),
    )
    for distance in range(3, 8):
        forcing = (
            coefficients[distance - 1]
            + 2 * coefficients[distance - 2]
            + coefficients[distance - 3]
            - 4 * coefficients[distance]
        ) / 2
        stationary[distance] = add(
            scale(Fraction(3, 2), stationary[distance - 1]),
            scale(-Fraction(1, 2), stationary[distance - 3]),
            scale(forcing, a_pair),
        )
    assert stationary[1:] == [
        (Fraction(-2), Fraction(3)),
        (Fraction(-3), Fraction(25, 4)),
        (Fraction(-9, 2), Fraction(10)),
        (Fraction(-23, 4), Fraction(215, 16)),
        (Fraction(-57, 8), Fraction(273, 16)),
        (Fraction(-135, 16), Fraction(1317, 64)),
        (Fraction(-313, 32), Fraction(773, 32)),
    ]
    local_limits = [
        add(
            stationary[distance],
            scale(-1, stationary[distance + 1]),
            scale(-coefficients[distance + 1], a_pair),
        )
        for distance in range(1, 6)
    ]
    assert local_limits == [
        (Fraction(1), Fraction(-2)),
        (Fraction(3, 2), Fraction(-19, 8)),
        (Fraction(5, 4), Fraction(-17, 8)),
        (Fraction(11, 8), Fraction(-73, 32)),
        (Fraction(21, 16), Fraction(-35, 16)),
    ]

    f_poly = [3, 10, 12, -30, 1]
    g_poly = [1, 10, 6, -10, 1]
    cases = [
        (8, 7, [228817, 127116, 19830, 1068, 1], 160),
        (16, 13, [463475, 236196, 35682, 1924, 3], 320),
        (32, 27, [921109, 490428, 75342, 4060, 5], 640),
        (64, 53, [1848059, 962820, 146706, 7908, 11], 1280),
    ]

    def substitute_on_window(polynomial: list[int]) -> list[Fraction]:
        result = [Fraction(0) for _ in range(5)]
        for power, value in enumerate(polynomial):
            for y_power in range(power + 1):
                result[y_power] += (
                    value
                    * math.comb(power, y_power)
                    * Fraction(7, 8) ** (power - y_power)
                    * Fraction(1, 8) ** y_power
                )
        return result

    for g_factor, f_factor, expected, denominator_upper in cases:
        polynomial = [
            g_factor * g_value - f_factor * f_value
            for g_value, f_value in zip(g_poly, f_poly, strict=True)
        ]
        transformed = substitute_on_window(polynomial)
        assert [int(value * 4096) for value in transformed] == expected
        assert all(value > 0 for value in transformed)
        assert 3 * expected[0] > 4096 * denominator_upper

    terminal_t = math.exp(-1.0 / 8.0)
    denominator = (1.0 + terminal_t**2) ** 2
    f_value = (terminal_t**4 - 30 * terminal_t**3 + 12 * terminal_t**2 + 10 * terminal_t + 3) / (
        10 * denominator
    )
    g_value = (terminal_t**4 - 10 * terminal_t**3 + 6 * terminal_t**2 + 10 * terminal_t + 1) / (
        5 * denominator
    )
    limits = [
        2 * (g_value - 13 * f_value / 8),
        g_value - 7 * f_value / 4,
        g_value - 13 * f_value / 8,
        g_value - 27 * f_value / 16,
        g_value - 53 * f_value / 32,
    ]
    assert limits[0] > 2 / 3 and min(limits[1:]) > 1 / 3
    return limits


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
    limits = check_first_order_limit_algebra()
    print(
        "static_frontier_first_order=pass limits="
        + ",".join(f"{value:.12g}" for value in limits)
        + " lower_bounds=2/3,1/3,1/3,1/3,1/3 scope=PROVED"
    )
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
            f"margins/q3={','.join(f'{value:.9g}' for value in margins)} "
            f"margins/q4={','.join(f'{value * 16 * edge_count:.9g}' for value in margins)} "
            "scope=MEASURED"
        )
    print(
        "terminal_static_frontier_reduction=PASS joint_first_order=PROVED uniform_m_ge_64_sign=OPEN"
    )


if __name__ == "__main__":
    main()
