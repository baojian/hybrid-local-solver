#!/usr/bin/env python3
"""Deterministic floating screen for the short-path terminal candidate.

The script writes no artifacts. It reconstructs the actual transported-center
admission chronology and uses the literal global residual range on the full
face. Its output is measured float64 evidence, not an exact proof.
"""

from __future__ import annotations

import argparse
import math
from fractions import Fraction
from functools import lru_cache

import numpy as np


def _fraction_h_apply(
    z: list[Fraction],
    degrees: list[Fraction],
    q: Fraction,
) -> list[Fraction]:
    """Apply the normalized path operator in exact rational arithmetic."""
    a = (1 + q * q) / 2
    eta = (1 - q * q) / 2
    out = [a * value for value in z]
    for index in range(1, len(z)):
        out[index] -= eta * z[index - 1] / degrees[index]
    for index in range(len(z) - 1):
        out[index] -= eta * z[index + 1] / degrees[index]
    return out


def _fraction_load(length: int, q: Fraction) -> list[Fraction]:
    out = [-(q**3) / 5 for _ in range(length)]
    out[0] += q * q
    return out


def _fraction_residual(
    z: list[Fraction],
    degrees: list[Fraction],
    q: Fraction,
) -> list[Fraction]:
    return [
        left - right
        for left, right in zip(
            _fraction_h_apply(z, degrees, q),
            _fraction_load(len(z), q),
            strict=True,
        )
    ]


def _fraction_optimum(
    length: int,
    degrees: list[Fraction],
    q: Fraction,
) -> list[Fraction]:
    """Exact Thomas solve for a restricted optimum."""
    a = (1 + q * q) / 2
    eta = (1 - q * q) / 2
    right = _fraction_load(length, q)
    diagonal = [a for _ in range(length)]
    upper = [-eta / degrees[index] for index in range(length - 1)]
    lower = [-eta / degrees[index] for index in range(1, length)]
    for index in range(1, length):
        multiplier = lower[index - 1] / diagonal[index - 1]
        diagonal[index] -= multiplier * upper[index - 1]
        right[index] -= multiplier * right[index - 1]
    answer = [Fraction(0) for _ in range(length)]
    answer[-1] = right[-1] / diagonal[-1]
    for index in range(length - 2, -1, -1):
        answer[index] = (right[index] - upper[index] * answer[index + 1]) / diagonal[index]
    return answer


def _fraction_step(
    p: list[Fraction],
    v: list[Fraction],
    degrees: list[Fraction],
    q: Fraction,
) -> tuple[list[Fraction], list[Fraction]]:
    y = [(left + q * right) / (1 + q) for left, right in zip(p, v, strict=True)]
    residual_y = _fraction_residual(y, degrees, q)
    raw = [left - right for left, right in zip(y, residual_y, strict=True)]
    assert min(raw) >= 0
    v_next = [
        current + (1 - q) * (current - previous) / q
        for current, previous in zip(raw, p, strict=True)
    ]
    return raw, v_next


def _fraction_stencil(
    values: list[Fraction],
    length: int,
    coefficient: Fraction,
) -> list[Fraction]:
    padded = values + [Fraction(0) for _ in range(length - len(values))]
    return [
        coefficient
        * (
            2 * padded[index]
            + (padded[index - 1] if index else 0)
            + (padded[index + 1] if index + 1 < length else 0)
        )
        for index in range(length)
    ]


def _polynomial_add(
    left: dict[int, Fraction],
    right: dict[int, Fraction],
    right_scale: Fraction = Fraction(1),
) -> dict[int, Fraction]:
    out = dict(left)
    for exponent, coefficient in right.items():
        out[exponent] = out.get(exponent, Fraction(0)) + right_scale * coefficient
        if out[exponent] == 0:
            del out[exponent]
    return out


def _polynomial_product(
    left: dict[int, Fraction],
    right: dict[int, Fraction],
) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            out[exponent] = out.get(exponent, Fraction(0)) + left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in out.items() if coefficient}


def _polynomial_power(
    polynomial: dict[int, Fraction],
    exponent: int,
) -> dict[int, Fraction]:
    out = {0: Fraction(1)}
    for _ in range(exponent):
        out = _polynomial_product(out, polynomial)
    return out


def _even_polynomial(values: list[Fraction]) -> dict[int, Fraction]:
    out = {0: values[0]}
    for index, value in enumerate(values[1:], start=1):
        if value:
            out[index] = value
            out[-index] = value
    return {exponent: coefficient for exponent, coefficient in out.items() if coefficient}


def exact_chronology_reduction_checks() -> None:
    """Check the proved reduction identities and finite shared-sign evidence."""
    p_lower = Fraction(3488, 1921)
    p_upper = Fraction(33, 16)
    eta_lower = Fraction(255, 512)
    raw_lower = Fraction(1215, 1088) * p_lower - Fraction(1, 5)
    gate_upper = Fraction(2048, 1275)
    frontier_residual_upper = eta_lower * (-raw_lower + p_upper / 2) + Fraction(1, 5)
    assert raw_lower == Fraction(596861, 326570)
    assert raw_lower - gate_upper == Fraction(1084499, 4898550)
    assert frontier_residual_upper == -Fraction(30946901, 157368320)

    for edge_count in (8, 12):
        q = Fraction(1, 16 * edge_count)
        eta = (1 - q * q) / 2
        chi = (1 - q) / (1 + q)
        degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]
        p = [Fraction(0)]
        v = [Fraction(0)]
        previous_x: list[Fraction] | None = None
        previous_optimum: list[Fraction] | None = None
        previous_frontier_raw: Fraction | None = None

        for length in range(1, edge_count + 1):
            optimum = _fraction_optimum(length, degrees, q)
            p_frontier = optimum[-1]
            t = chi**length
            formula_frontier = (
                Fraction(2, 1)
                / (1 + q)
                * (t * (1 + t / 5) / chi + t - Fraction(1, 5))
                / (1 + t * t)
                * q**2
            )
            assert p_frontier == formula_frontier
            assert p_lower * q**2 <= p_frontier <= p_upper * q**2

            y = [(left + q * right) / (1 + q) for left, right in zip(p, v, strict=True)]
            average_residual = _fraction_residual(y, degrees[:length], q)
            entry_residual = _fraction_residual(p, degrees[:length], q)
            x_value = [-value for value in entry_residual]

            if length > 1:
                assert previous_x is not None
                assert previous_optimum is not None
                assert previous_frontier_raw is not None
                shared_sign = [
                    x_value[index] - (1 - q) * previous_x[index] / 2 for index in range(length - 1)
                ]
                assert min(shared_sign) > 0
                assert all(
                    average_residual[index] == -2 * shared_sign[index] / (1 + q)
                    for index in range(length - 1)
                )
                frontier_identity = (
                    -eta * previous_frontier_raw + q * eta * previous_optimum[-1] / 2 + q**3 / 5
                ) / (1 + q)
                assert average_residual[-1] == frontier_identity
                assert average_residual[-1] < 0
                frontier_ratio = y[-2] / y[-1]
                assert frontier_ratio >= (3 - q) / (1 + q)

            raw = [left - right for left, right in zip(y, average_residual, strict=True)]
            assert min(raw) > 0
            assert raw[-1] > raw_lower * q**3
            post_residual = _fraction_residual(raw, degrees[:length], q)
            b_average_residual = [
                left - right
                for left, right in zip(
                    average_residual,
                    _fraction_h_apply(average_residual, degrees[:length], q),
                    strict=True,
                )
            ]
            assert post_residual == b_average_residual
            assert max(post_residual) < 0

            outside_residual = q**3 / 5 - eta * raw[-1] / degrees[length]
            assert outside_residual < -(q**3) / 5

            v_out = [
                current + (1 - q) * (current - previous) / q
                for current, previous in zip(raw, p, strict=True)
            ]
            new_optimum = _fraction_optimum(length + 1, degrees, q)
            p = raw + [Fraction(0)]
            v = [
                value + new_value - old_value
                for value, new_value, old_value in zip(
                    v_out + [Fraction(0)],
                    new_optimum,
                    optimum + [Fraction(0)],
                    strict=True,
                )
            ]
            previous_x = x_value
            previous_optimum = optimum
            previous_frontier_raw = raw[-1]

    print(
        "exact_chronology_reduction_checks=m=8,12 constants=pass "
        "identities=pass finite_shared_sign=pass analytic_followup=m>=64"
    )


def _fraction_ideal_prefix_packet(
    length: int,
    q: Fraction,
) -> list[Fraction]:
    """Return the reflected ideal prefix packet used in the correction split."""
    scale = q * q * (1 - q) ** (length - 1) / (2**length)
    return [scale * (2 if index == 0 else math.comb(length - 1, index)) for index in range(length)]


def exact_chronology_correction_checks() -> None:
    """Check the exact correction recurrence and positive Green reduction."""
    edge_count = 12
    q = Fraction(1, 16 * edge_count)
    eta = (1 - q * q) / 2
    c1 = (1 - q) / 2
    degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]
    entries: dict[int, list[Fraction]] = {}
    corrections: dict[int, list[Fraction]] = {}
    optima: dict[int, list[Fraction]] = {}
    p = [Fraction(0)]
    v = [Fraction(0)]
    for length in range(1, edge_count + 1):
        optimum = _fraction_optimum(length, degrees, q)
        entry_x = [-value for value in _fraction_residual(p, degrees[:length], q)]
        ideal = _fraction_ideal_prefix_packet(length, q)
        entries[length] = entry_x
        corrections[length] = [left - right for left, right in zip(entry_x, ideal, strict=True)]
        optima[length] = optimum
        p_next, v_next = _fraction_step(p, v, degrees[:length], q)
        new_optimum = _fraction_optimum(length + 1, degrees, q)
        p = p_next + [Fraction(0)]
        v = [
            value + new_value - old_value
            for value, new_value, old_value in zip(
                v_next + [Fraction(0)],
                new_optimum,
                optimum + [Fraction(0)],
                strict=True,
            )
        ]

    r_plus = {0: c1, 1: c1}
    r_minus = {0: c1, -1: c1}
    first_operator = _polynomial_add(r_plus, r_minus)
    second_operator = _polynomial_product(r_plus, r_minus)
    for length in range(2, edge_count):
        correction = corrections[length]
        previous = corrections[length - 1]
        frontier_z = (2 * correction[-1] + q**3 / 5 - q * eta * optima[length - 1][-1] / 2) / (
            1 + q
        )
        correction_z = [
            (2 * correction[index] - (1 - q) * previous[index]) / (1 + q)
            for index in range(length - 1)
        ] + [frontier_z]
        b_correction_z = [
            left - right
            for left, right in zip(
                correction_z,
                _fraction_h_apply(correction_z, degrees[:length], q),
                strict=True,
            )
        ]
        assert corrections[length + 1][:-1] == b_correction_z
        new_row = eta * (frontier_z + q * optima[length][-1] / (1 + q)) / 2 - q**3 / 5
        assert corrections[length + 1][-1] == new_row

        ideal = _fraction_ideal_prefix_packet(length, q)
        previous_ideal = _fraction_ideal_prefix_packet(length - 1, q)
        for index in range(length - 1):
            ideal_sign = ideal[index] - c1 * previous_ideal[index]
            if index == 0:
                assert ideal_sign == 0
            else:
                assert ideal_sign == (
                    c1 * previous_ideal[index] * Fraction(index, length - 1 - index)
                )
            full_sign = entries[length][index] - c1 * entries[length - 1][index]
            correction_sign = correction[index] - c1 * previous[index]
            assert full_sign == ideal_sign + correction_sign

    for length in range(4, edge_count):
        current = _even_polynomial(corrections[length])
        previous = _even_polynomial(corrections[length - 1])
        following = _even_polynomial(corrections[length + 1])
        source = _polynomial_add(
            following,
            _polynomial_product(first_operator, current),
            Fraction(-1),
        )
        source = _polynomial_add(
            source,
            _polynomial_product(second_operator, previous),
        )
        source_error = q**3 / 5 - q * eta * optima[length - 1][-1] / 2
        source_u = (1 - q) * source_error / 4
        source_w = source_u + (1 - q) * q * optima[length][-1] / 4 - q**3 / 5
        expected: dict[int, Fraction] = {}
        for position, value in (
            (length - 2, source_u),
            (length - 1, 2 * source_u),
            (length, source_w),
        ):
            expected[position] = value
            expected[-position] = value
        assert source == expected
        assert source_error < 0

    green_previous: dict[int, Fraction] = {}
    green = {0: Fraction(1)}
    for step in range(1, 13):
        explicit: dict[int, Fraction] = {}
        for exponent in range(step):
            term = _polynomial_product(
                _polynomial_power(r_plus, exponent),
                _polynomial_power(r_minus, step - 1 - exponent),
            )
            explicit = _polynomial_add(explicit, term)
        assert green == explicit
        difference = _polynomial_add(green, green_previous, -c1)
        positive_form = _polynomial_add(
            _polynomial_power(r_plus, step - 1),
            _polynomial_product({-1: c1}, green_previous),
        )
        assert difference == positive_form
        assert min(difference.values()) >= 0
        assert sum(difference.values()) == Fraction(step + 1, 2) * (1 - q) ** (step - 1)
        green_previous, green = (
            green,
            _polynomial_add(
                _polynomial_product(first_operator, green),
                _polynomial_product(second_operator, green_previous),
                Fraction(-1),
            ),
        )
    positive_series = [
        Fraction(1, 3) + Fraction(2, 3) * Fraction(-1, 2) ** exponent for exponent in range(13)
    ]
    assert positive_series[0] == 1
    assert positive_series[1] == 0
    assert min(positive_series[2:]) > 0

    leading_previous = [Fraction(-1, 5)]
    leading = [Fraction(2, 5), Fraction(0)]
    leading_minimum: tuple[Fraction, int, int] | None = None
    for length in range(2, 257):
        differences = [leading[index] - leading_previous[index] / 2 for index in range(length - 1)]
        if length == 2:
            assert differences[0] == Fraction(1, 2)
        elif length % 2 == 0:
            half_length = length // 2
            assert differences[0] == (
                Fraction(1, 10) - Fraction(1, 10) * Fraction(1, 4) ** (half_length - 1)
            )
            if length >= 4:
                assert differences[1] == Fraction(1, 10) + Fraction(1, 4) ** half_length
        else:
            half_length = (length - 1) // 2
            assert differences[0] == (
                Fraction(1, 10) + Fraction(1, 20) * Fraction(1, 4) ** (half_length - 1)
            )
            if length >= 3:
                assert differences[1] == Fraction(1, 10)
        for index, value in enumerate(differences):
            candidate = (value, length, index)
            if leading_minimum is None or candidate < leading_minimum:
                leading_minimum = candidate
        if length == 256:
            break
        leading_z = [
            2 * leading[index] - leading_previous[index] for index in range(length - 1)
        ] + [2 * leading[-1] - Fraction(3, 10)]
        next_leading = [
            (leading_z[0] + leading_z[1]) / 2,
            *[
                (
                    leading_z[index]
                    + leading_z[index - 1] / 2
                    + (leading_z[index + 1] / 2 if index + 1 < length else 0)
                )
                / 2
                for index in range(1, length)
            ],
            leading_z[-1] / 4 + Fraction(3, 10),
        ]
        leading_previous, leading = leading, next_leading
    assert leading_minimum == (Fraction(1, 80), 4, 2)

    pascal_q = Fraction(1, 80)
    # This is the positive-only upper bound used in the written certificate:
    # discard every negative nonconstant monomial, then put q=1/80 in each
    # remaining positive monomial.
    pascal_positive_upper_bound = (
        -27
        + 226 * pascal_q**3
        + 602 * pascal_q**5
        + 7392 * pascal_q**6
        + 18855 * pascal_q**8
        + 5844 * pascal_q**10
        + 547 * pascal_q**12
        + 16 * pascal_q**14
    )
    assert pascal_positive_upper_bound < Fraction(-26999, 1000)
    print(
        "exact_chronology_correction_checks=m=12 recurrence=pass source=pass "
        "positive_green=k<=12 leading_formula_audit=n<=256:min=1/80@(4,2) "
        "finite_q_followup=separate"
    )


def exact_finite_q_correction_checks() -> None:
    """Audit the exact constants in the finite-q correction theorem."""

    @lru_cache(maxsize=None)
    def ell(step: int, offset: int) -> Fraction:
        if step == 1:
            return Fraction(int(offset == 0))
        lower = max(abs(offset) - 1, 0)
        if lower > step - 2:
            return Fraction(0)
        return Fraction(
            sum(math.comb(step - 2, index) for index in range(lower, step - 1)),
            2 ** (step - 1),
        )

    @lru_cache(maxsize=None)
    def derivative_weight(step: int, distance: int) -> Fraction:
        return (
            ell(step, step - distance)
            + 2 * ell(step, step - distance - 1)
            - 3 * ell(step, step - distance - 2)
        )

    for distance in range(129):
        positive_lobe = sum(derivative_weight(step, distance) for step in range(1, distance + 2))
        assert positive_lobe == Fraction(4, 3) + Fraction(2, 3) * Fraction(-1, 2) ** distance
        assert 0 <= positive_lobe <= 2
        for step in range(max(distance + 2, 2), distance + 66):
            trials = step - 2
            expected = -Fraction(1, 2) * (
                Fraction(math.comb(trials, distance), 2**trials)
                + 3
                * (
                    Fraction(math.comb(trials, distance + 1), 2**trials)
                    if distance + 1 <= trials
                    else 0
                )
            )
            assert derivative_weight(step, distance) == expected <= 0
    assert -Fraction(1, 2) * (2 + 3 * 2) == -4

    for final_length in range(6, 129):
        for coordinate in range(final_length - 1):
            distance = final_length - 2 - coordinate
            reflected_distance = final_length - 2 + coordinate
            running = Fraction(0)
            for source_time in range(2, final_length):
                step = final_length - source_time
                running += derivative_weight(step, distance)
                running += derivative_weight(step, reflected_distance)
                assert -4 <= running <= 4
                folded_mass = ell(step, coordinate - source_time) + ell(
                    step, coordinate + source_time
                )
                assert 0 <= folded_mass <= 1

    assert Fraction(19, 320) - Fraction(43, 1200) - Fraction(1, 90) == Fraction(179, 14400)
    for final_length in range(6, 129):
        assert (Fraction(3, 5) + Fraction(43 * (final_length - 2), 75)) / (
            16 * final_length
        ) < Fraction(43, 1200)
    assert Fraction(1, 375) + Fraction(16, 15 * 1024 * 10) == Fraction(133, 48000)
    assert Fraction(133, 48000) < Fraction(1, 360)
    assert Fraction(9707, 18080) < Fraction(43, 80)
    q_max = Fraction(1, 1024)
    epsilon_2 = q_max * (1 + 10 * q_max - q_max**2) / (10 * (1 + q_max**2))
    assert 0 < epsilon_2 < q_max / 8
    low_derivative_loss = q_max / 8 + 2 * Fraction(4, 15) * q_max
    assert low_derivative_loss == Fraction(79, 120) * q_max
    low_total_loss = (Fraction(3, 5) + Fraction(43, 25) + Fraction(79, 120)) * q_max
    assert low_total_loss == Fraction(1787, 600) * q_max
    assert low_total_loss < 3 * q_max < Fraction(1, 80)

    delta = 1 - q_max
    eta = (1 - q_max**2) / 2
    chi = delta / (1 + q_max)

    def scaled_frontier(index: int) -> Fraction:
        t_value = chi**index
        return (
            Fraction(2, 1)
            / (1 + q_max)
            * (t_value * (1 + t_value / 5) / chi + t_value - Fraction(1, 5))
            / (1 + t_value**2)
        )

    for source_time in (2, 3):
        p_previous = scaled_frontier(source_time - 1)
        p_current = scaled_frontier(source_time)
        source_e = Fraction(1, 5) - eta * p_previous / 2
        source_E = delta ** (-(source_time - 2)) * source_e
        source_F = delta ** (-(source_time - 2)) * (source_e + p_current) / 4 - Fraction(
            1, 5
        ) * delta ** (-(source_time - 1))
        source_mu = source_F + 3 * source_E / 4
        s_value = (chi ** (source_time - 1) + chi ** (-(source_time - 1))) / (
            chi**source_time + chi ** (-source_time)
        )
        normalized_mass = delta * p_previous * (2 * eta - s_value) / (4 * q_max) + (
            delta * s_value + 2 * eta
        ) / (10 * eta)
        assert source_mu == -(delta ** (-(source_time - 1))) * q_max * normalized_mass
        assert -Fraction(43, 75) * q_max < source_mu < 0

    print(
        "exact_finite_q_correction_checks=low_n_perturbation:pass "
        "stopped_derivative_prefix=[-4,4]:pass ledger=179/14400:pass "
        "analytic_theorem=m>=64"
    )


def exact_boundary_source_checks() -> None:
    """Check the sparse source and its formal transform over the rationals."""
    edge_count = 8
    q = Fraction(1, 16 * edge_count)
    rho = q / 5
    eta = (1 - q * q) / 2
    a = (1 + q * q) / 2
    chi = (1 - q) / (1 + q)
    degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]

    def f(index: int) -> Fraction:
        return chi**index + chi ** (-index)

    def b(index: int) -> Fraction:
        if index == 0:
            return (rho - q) / 2
        return (rho - q * chi**index) / (chi**index + chi ** (-index))

    entries: dict[int, list[Fraction]] = {}
    optima: dict[int, list[Fraction]] = {}
    residuals: dict[int, list[Fraction]] = {}
    p = [Fraction(0)]
    v = [Fraction(0)]
    for length in range(1, edge_count + 1):
        optimum = _fraction_optimum(length, degrees, q)
        entries[length] = p
        optima[length] = optimum
        residuals[length] = _fraction_residual(p, degrees[:length], q)
        p_next, v_next = _fraction_step(p, v, degrees[:length], q)
        new_optimum = _fraction_optimum(length + 1, degrees, q)
        p = p_next + [Fraction(0)]
        v = v_next + [Fraction(0)]
        v = [
            value + new_value - old_value
            for value, new_value, old_value in zip(
                v,
                new_optimum,
                optimum + [Fraction(0)],
                strict=True,
            )
        ]
    entries[edge_count + 1] = p
    optima[edge_count + 1] = _fraction_optimum(edge_count + 1, degrees, q)
    residuals[edge_count + 1] = _fraction_residual(p, degrees, q)

    c1 = (1 - q) / 2
    c2 = (1 - q) ** 2 / 4
    r_plus = {0: c1, 1: c1}
    r_minus = {0: c1, -1: c1}
    first_operator = _polynomial_add(r_plus, r_minus)
    second_operator = _polynomial_product(r_plus, r_minus)

    for prefix in (4, 6, 7, edge_count):
        length = prefix + 1
        first = _fraction_stencil(residuals[prefix], length, c1)
        second = _fraction_stencil(residuals[prefix - 1], length, c2)
        defect = [
            residuals[length][index] - first[index] + second[index] for index in range(length)
        ]
        delta = b(prefix) - b(prefix - 1)
        p_frontier = optima[prefix][-1]
        previous_frontier = optima[prefix - 1][-1]
        u_value = q * eta**2 / (4 * (1 + q)) * (previous_frontier - 2 * q * rho / eta)
        assert 0 < u_value <= Fraction(3, 40) * q**3
        expected: dict[int, Fraction] = {
            0: c1 * residuals[prefix][1] - c2 * residuals[prefix - 1][1],
            prefix - 2: u_value,
            prefix - 1: 2 * u_value,
        }
        if prefix < edge_count:
            next_delta = b(prefix + 1) - b(prefix)
            w_value = (
                u_value
                + c1 * p_frontier
                - a * delta * f(prefix) / (1 + q)
                + eta / 2 * (delta / (1 + q) - next_delta) * f(prefix + 1)
            )
            s_value = f(prefix - 1) / f(prefix)
            d_value = 2 * q * q * rho / eta
            mass = w_value + 3 * u_value
            exact_mass = (
                q * (1 - q) / 4 * (2 * eta - s_value) * previous_frontier
                + q / 4 * ((1 - q) * s_value + 2 * eta) * d_value
            )
            assert mass == exact_mass
            assert abs(mass) <= Fraction(3, 2) * q**4
        else:
            w_value = (
                c1 * residuals[prefix][-1]
                + (1 - q) ** 2 / 2 * p_frontier
                - eta * (1 - q) ** 2 / 4 * previous_frontier
                - delta * eta**2 / (1 + q) * (f(prefix - 1) + f(prefix - 2) / 2)
                + q**3 / 5
            )
            simplified_endpoint = (
                c1 * residuals[prefix][-1]
                - q * (1 - q) * p_frontier / 2
                + q * eta * (1 - q) * previous_frontier / 4
                + q**3 * (1 + q) / 10
            )
            assert w_value == simplified_endpoint
        expected[prefix] = w_value
        assert all(value == expected.get(index, Fraction(0)) for index, value in enumerate(defect))

        formal_defect = _even_polynomial(residuals[length])
        formal_defect = _polynomial_add(
            formal_defect,
            _polynomial_product(first_operator, _even_polynomial(residuals[prefix])),
            Fraction(-1),
        )
        formal_defect = _polynomial_add(
            formal_defect,
            _polynomial_product(
                second_operator,
                _even_polynomial(residuals[prefix - 1]),
            ),
        )
        expected_even: dict[int, Fraction] = {}
        for index in (prefix - 2, prefix - 1, prefix):
            expected_even[index] = expected[index]
            expected_even[-index] = expected[index]
        assert formal_defect == expected_even

        if prefix < edge_count:
            factored_positive = {
                prefix - 2: u_value,
                prefix - 1: 2 * u_value,
                prefix: mass - 3 * u_value,
            }
            assert factored_positive[prefix] == w_value

    print(
        "exact_boundary_source_checks=m=8 n=4,6,7,8 "
        "support=pass entries=pass formal_transform=pass arithmetic=Fraction"
    )


def exact_directional_packet_checks() -> None:
    """Audit the directed packet, entry sign, and folded J-kernel bound."""

    def shift(values: list[Fraction], amount: int) -> list[Fraction]:
        size = len(values)
        return [values[(index - amount) % size] for index in range(size)]

    def average_shift(values: list[Fraction], amount: int) -> list[Fraction]:
        shifted = shift(values, amount)
        return [(left + right) / 2 for left, right in zip(values, shifted, strict=True)]

    def cycle_l(values: list[Fraction]) -> list[Fraction]:
        plus = average_shift(values, 1)
        minus = average_shift(values, -1)
        return [(left + right) / 2 for left, right in zip(plus, minus, strict=True)]

    for edge_count in (5, 8):
        size = 2 * edge_count
        packet = [
            Fraction(math.comb(edge_count, index), 2**edge_count) for index in range(edge_count + 1)
        ]
        plus_packet = [Fraction(0) for _ in range(size)]
        plus_packet[: edge_count + 1] = packet
        plus_packet[0] /= 2
        plus_packet[edge_count] /= 2
        minus_packet = [plus_packet[-index % size] for index in range(size)]
        even_packet = [
            packet[index] if index <= edge_count else packet[size - index] for index in range(size)
        ]
        assert [
            left + right for left, right in zip(plus_packet, minus_packet, strict=True)
        ] == even_packet

        directed_velocity = [
            plus - middle + minus - middle_other
            for plus, middle, minus, middle_other in zip(
                average_shift(plus_packet, 1),
                cycle_l(plus_packet),
                average_shift(minus_packet, -1),
                cycle_l(minus_packet),
                strict=True,
            )
        ]
        lower_plus = [Fraction(0) for _ in range(size)]
        lower_plus[1:edge_count] = [
            Fraction(math.comb(edge_count - 2, index - 1), 2 ** (edge_count - 2))
            for index in range(1, edge_count)
        ]
        lower_minus = [lower_plus[-index % size] for index in range(size)]
        cycle_d = [
            (plus_forward - plus_backward - minus_forward + minus_backward) / 4
            for plus_forward, plus_backward, minus_forward, minus_backward in zip(
                shift(lower_plus, 1),
                shift(lower_plus, -1),
                shift(lower_minus, 1),
                shift(lower_minus, -1),
                strict=True,
            )
        ]
        assert cycle_l(cycle_d) == directed_velocity
        assert cycle_d[0] == -lower_plus[1] / 2
        assert cycle_d[edge_count] == lower_plus[edge_count - 1] / 2
        trajectory_previous = even_packet
        trajectory = [
            left + right
            for left, right in zip(
                cycle_l(even_packet),
                directed_velocity,
                strict=True,
            )
        ]
        directed_plus = average_shift(plus_packet, 1)
        directed_minus = average_shift(minus_packet, -1)
        assert trajectory == [
            left + right for left, right in zip(directed_plus, directed_minus, strict=True)
        ]
        for _step in range(1, 4 * edge_count):
            directed_plus = average_shift(directed_plus, 1)
            directed_minus = average_shift(directed_minus, -1)
            expected = [
                left + right for left, right in zip(directed_plus, directed_minus, strict=True)
            ]
            following = [
                2 * middle - previous
                for middle, previous in zip(
                    cycle_l(trajectory),
                    cycle_l(trajectory_previous),
                    strict=True,
                )
            ]
            assert following == expected
            trajectory_previous, trajectory = trajectory, following

    for edge_count in (3, 4, 5):
        period = 2 * edge_count
        for step in range(1, 8 * edge_count + 1):
            tail = {
                offset: sum(
                    Fraction(math.comb(step - 1, count), 2 ** (step - 1))
                    for count in range(abs(offset), step)
                )
                for offset in range(-(step - 1), step)
            }
            assert max(tail.values()) <= 1
            aliases = [
                sum(value for offset, value in tail.items() if offset % period == residue)
                for residue in range(period)
            ]
            assert max(aliases) <= 1 + Fraction(step - 1, 2 * edge_count)
            for offset in range(-step, step + 1):
                jl_direct = (
                    tail.get(offset - 1, Fraction(0))
                    + 2 * tail.get(offset, Fraction(0))
                    + tail.get(offset + 1, Fraction(0))
                ) / 4
                jl_window = sum(
                    Fraction(math.comb(step + 1, step + offset - count), 2 ** (step + 1))
                    for count in range(step)
                    if 0 <= step + offset - count <= step + 1
                )
                assert jl_direct == jl_window

    for edge_count in (8, 12):
        q = Fraction(1, 16 * edge_count)
        degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]
        p = [Fraction(0)]
        v = [Fraction(0)]
        proper_residual = None
        proper_average_residual = None
        proper_post_residual = None
        proper_sigma = None
        proper_frontier = None
        for length in range(1, edge_count + 1):
            optimum = _fraction_optimum(length, degrees, q)
            if length == edge_count:
                proper_residual = _fraction_residual(p, degrees[:length], q)
                average = [(left + q * right) / (1 + q) for left, right in zip(p, v, strict=True)]
                proper_average_residual = _fraction_residual(average, degrees[:length], q)
            p_next, v_next = _fraction_step(p, v, degrees[:length], q)
            if length == edge_count:
                proper_post_residual = _fraction_residual(p_next, degrees[:length], q)
                proper_sigma = p_next[-1]
                proper_frontier = optimum[-1]
            new_optimum = _fraction_optimum(length + 1, degrees, q)
            p = p_next + [Fraction(0)]
            v = [
                value + new_value - old_value
                for value, new_value, old_value in zip(
                    v_next + [Fraction(0)],
                    new_optimum,
                    optimum + [Fraction(0)],
                    strict=True,
                )
            ]
        entry_residual = _fraction_residual(p, degrees, q)
        ideal = [
            -(q * q)
            * (1 - q) ** edge_count
            * Fraction(math.comb(edge_count, index), 2 ** (edge_count + 1))
            for index in range(edge_count + 1)
        ]
        assert all(left <= right for left, right in zip(entry_residual, ideal, strict=True))

        assert proper_residual is not None
        assert proper_average_residual is not None
        assert proper_post_residual is not None
        assert proper_sigma is not None
        assert proper_frontier is not None
        velocity_residual = _fraction_residual(v, degrees, q)
        entry_b = [q * value for value in velocity_residual]
        delta = 1 - q
        assert entry_b[:-1] == [
            post - delta * old
            for post, old in zip(
                proper_post_residual,
                proper_residual,
                strict=True,
            )
        ]
        eta = (1 - q * q) / 2
        assert entry_b[-1] == eta * (q * proper_frontier - proper_sigma)

        gamma = [Fraction(0) for _ in range(edge_count + 1)]
        gamma[1:edge_count] = [
            -(q * q)
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
        path_l_static = [
            (static_data[0] + static_data[1]) / 2,
            *[
                (static_data[index - 1] + 2 * static_data[index] + static_data[index + 1]) / 4
                for index in range(1, edge_count)
            ],
            (static_data[-2] + static_data[-1]) / 2,
        ]

        signed_ideal = ideal
        plus_ideal = [Fraction(0) for _ in range(2 * edge_count)]
        plus_ideal[: edge_count + 1] = signed_ideal
        plus_ideal[0] /= 2
        plus_ideal[edge_count] /= 2
        minus_ideal = [plus_ideal[-index % (2 * edge_count)] for index in range(2 * edge_count)]
        directed_signed = [
            plus - middle + minus - middle_other
            for plus, middle, minus, middle_other in zip(
                average_shift(plus_ideal, 1),
                cycle_l(plus_ideal),
                average_shift(minus_ideal, -1),
                cycle_l(minus_ideal),
                strict=True,
            )
        ][: edge_count + 1]
        path_l_b = [
            (entry_b[0] + entry_b[1]) / 2,
            *[
                (entry_b[index - 1] + 2 * entry_b[index] + entry_b[index + 1]) / 4
                for index in range(1, edge_count)
            ],
            (entry_b[-2] + entry_b[-1]) / 2,
        ]
        assert path_l_static == [
            left - right for left, right in zip(path_l_b, directed_signed, strict=True)
        ]

    print(
        "exact_directional_packet_checks=cycle_split:pass directed_sign:pass "
        "J_alias:pass JL_kernel:pass exact_entry_c_sign=m=8,12 "
        "static_u=Ld:pass"
    )
def position_profile_asymptotic_checks() -> None:
    """Audit exact constants and the finite constant-U Chebyshev formula."""
    t_lower = Fraction(2711, 3072)
    p_lower = 2 * (2 * t_lower + t_lower * t_lower / 5 - Fraction(1, 5)) / (1 + t_lower * t_lower)
    variation_numerator = 2 - p_lower
    assert variation_numerator == Fraction(5478536, 83933525)
    assert variation_numerator < Fraction(1, 15)

    rational_ledger = Fraction(1, 2160) + Fraction(1, 1080) + Fraction(43, 30720)
    assert rational_ledger == Fraction(257, 92160)
    assert Fraction(1, 256) - rational_ledger == Fraction(103, 92160)

    for edge_count in (64, 128, 256):
        q = 1.0 / (16.0 * edge_count)
        constant_u = 3.0 * q**3 / 40.0
        for mode_index in (1, 2, 3):
            phi = mode_index * math.pi / edge_count
            z = complex(math.cos(2.0 * phi), math.sin(2.0 * phi))
            cosine = math.cos(phi)
            radius = (1.0 - q) * cosine
            first = 2.0 * radius * cosine
            second = radius * radius

            values = [0.0] * (edge_count + 2)
            for prefix in range(2, edge_count + 1):
                source = 0.0
                if 4 <= prefix < edge_count:
                    source = (
                        2.0
                        * constant_u
                        * (
                            math.cos((prefix - 2) * 2.0 * phi)
                            + 2.0 * math.cos((prefix - 1) * 2.0 * phi)
                            - 3.0 * math.cos(prefix * 2.0 * phi)
                        )
                    )
                values[prefix + 1] = first * values[prefix] - second * values[prefix - 1] + source

            cutoff = edge_count - 4
            chebyshev_previous = 1.0
            chebyshev_current = 2.0 * cosine
            direct_sum = chebyshev_current * (radius / z)
            for index in range(2, cutoff + 1):
                chebyshev_next = 2.0 * cosine * chebyshev_current - chebyshev_previous
                direct_sum += chebyshev_next * (radius / z) ** index
                chebyshev_previous = chebyshev_current
                chebyshev_current = chebyshev_next
            closed_response = (
                2.0 * constant_u * (z**-2 * (1.0 - z) * (1.0 + 3.0 * z) * direct_sum).real
            )
            assert math.isclose(
                values[edge_count + 1],
                closed_response,
                rel_tol=2.0e-10,
                abs_tol=2.0e-18,
            )

    print("position_profile_asymptotic_checks=rational_constants=pass constant_U_Chebyshev=pass")


def h_apply(z: np.ndarray, degrees: np.ndarray, q: float) -> np.ndarray:
    """Apply D^(-1/2) Q D^(1/2) in normalized path coordinates."""
    a = (1.0 + q * q) / 2.0
    eta = (1.0 - q * q) / 2.0
    out = a * z.copy()
    out[1:] -= eta * z[:-1] / degrees[1:]
    out[:-1] -= eta * z[1:] / degrees[:-1]
    return out


def normalized_load(length: int, q: float) -> np.ndarray:
    """Return the affine RPPR load with rho=q/5 and endpoint seed zero."""
    out = np.full(length, -(q**3) / 5.0)
    out[0] += q * q
    return out


def residual(z: np.ndarray, degrees: np.ndarray, q: float) -> np.ndarray:
    return h_apply(z, degrees, q) - normalized_load(len(z), q)


def restricted_optimum(length: int, degrees: np.ndarray, q: float) -> np.ndarray:
    """Thomas solve for one normalized restricted optimum."""
    a = (1.0 + q * q) / 2.0
    eta = (1.0 - q * q) / 2.0
    right = normalized_load(length, q)
    diagonal = np.full(length, a)
    upper = -eta / degrees[: length - 1]
    lower = -eta / degrees[1:length]
    for index in range(1, length):
        multiplier = lower[index - 1] / diagonal[index - 1]
        diagonal[index] -= multiplier * upper[index - 1]
        right[index] -= multiplier * right[index - 1]
    answer = np.empty(length)
    answer[-1] = right[-1] / diagonal[-1]
    for index in range(length - 2, -1, -1):
        answer[index] = (right[index] - upper[index] * answer[index + 1]) / diagonal[index]
    return answer


def one_step(
    p: np.ndarray,
    v: np.ndarray,
    degrees: np.ndarray,
    q: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    y = (p + q * v) / (1.0 + q)
    raw = y - residual(y, degrees, q)
    p_next = np.maximum(raw, 0.0)
    v_next = p_next + (1.0 - q) * (p_next - p) / q
    return p_next, v_next, raw


def full_face_entry(
    edge_count: int,
) -> tuple[
    float,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    list[np.ndarray],
    float,
    float,
]:
    """Replay one fixed-face step and one transported singleton per prefix."""
    q = 1.0 / (16.0 * edge_count)
    degrees = np.r_[1.0, np.full(edge_count - 1, 2.0), 1.0]
    p = np.zeros(1)
    v = np.zeros(1)
    prefix_residuals = []
    last_proper_error = None
    last_proper_frontier = None
    for length in range(1, edge_count + 1):
        prefix_residuals.append(residual(p, degrees[:length], q))
        p_next, v_next, raw = one_step(p, v, degrees[:length], q)
        assert raw.min() >= -1.0e-14, f"projection active during admission {length}"
        r_next = residual(p_next, degrees[:length], q)
        delta = max(0.0, r_next.max() / (q * q))
        assert delta <= 1.0e-12, f"nonzero admission correction at prefix {length}"
        outside = -(1.0 - q * q) * p_next[-1] / (2.0 * degrees[length]) + q**3 / 5.0
        assert outside < -(q**3) / 5.0, f"next vertex not strongly admitted at prefix {length}"
        old_optimum = restricted_optimum(length, degrees, q)
        new_optimum = restricted_optimum(length + 1, degrees, q)
        if length == edge_count:
            last_proper_error = float(p[-1] - old_optimum[-1])
            last_proper_frontier = float(old_optimum[-1])
        p = np.r_[p_next, 0.0]
        v = np.r_[v_next, 0.0] + new_optimum - np.r_[old_optimum, 0.0]
    prefix_residuals.append(residual(p, degrees, q))
    assert last_proper_error is not None
    assert last_proper_frontier is not None
    return (
        q,
        degrees,
        p,
        v,
        prefix_residuals,
        last_proper_error,
        last_proper_frontier,
    )


def cosine_coefficients(r: np.ndarray, degrees: np.ndarray) -> np.ndarray:
    """Return coefficients in the degree-weighted path cosine basis."""
    edge_count = len(r) - 1
    vertices = np.arange(edge_count + 1)
    coefficients = np.empty(edge_count + 1)
    for mode in range(edge_count + 1):
        norm = 2.0 * edge_count if mode in (0, edge_count) else edge_count
        cosine = np.cos(math.pi * mode * vertices / edge_count)
        coefficients[mode] = np.dot(degrees * r, cosine) / norm
    return coefficients


def binomial_probabilities(edge_count: int) -> np.ndarray:
    """Compute a stable Binomial(edge_count, 1/2) probability vector."""
    return np.array(
        [
            math.exp(
                math.lgamma(edge_count + 1)
                - math.lgamma(index + 1)
                - math.lgamma(edge_count - index + 1)
                - edge_count * math.log(2.0)
            )
            for index in range(edge_count + 1)
        ]
    )


def five_piece_decomposition(
    prefix_residuals: list[np.ndarray],
    proper_error_last: float,
    proper_frontier: float,
    q: float,
) -> tuple[dict[str, float], dict[str, float]]:
    """Measure the exact linear five-piece split at the first even mode."""
    edge_count = len(prefix_residuals) - 1
    theta = 2.0 * math.pi / edge_count
    phi = theta / 2.0
    first_coefficient = 2.0 * (1.0 - q) * math.cos(phi) ** 2
    second_coefficient = (1.0 - q) ** 2 * math.cos(phi) ** 2
    transforms: list[float | None] = [None]
    for values in prefix_residuals:
        transforms.append(
            float(values[0])
            + 2.0
            * sum(float(values[index]) * math.cos(theta * index) for index in range(1, len(values)))
        )

    names = ("base", "constant_u", "delta_u", "mass", "endpoint")
    components = {name: [0.0, 0.0, 0.0] for name in names}
    components["base"][1] = float(transforms[1])
    components["base"][2] = float(transforms[2])
    constant_u = 3.0 * q**3 / 40.0

    def stencil(values: np.ndarray, length: int, coefficient: float) -> np.ndarray:
        padded = np.zeros(length)
        padded[: len(values)] = values
        return coefficient * (2.0 * padded + np.r_[0.0, padded[:-1]] + np.r_[padded[1:], 0.0])

    for prefix in range(2, edge_count + 1):
        source = {
            "base": 0.0,
            "constant_u": 0.0,
            "delta_u": 0.0,
            "mass": 0.0,
            "endpoint": 0.0,
        }
        full_source = (
            float(transforms[prefix + 1])
            - first_coefficient * float(transforms[prefix])
            + second_coefficient * float(transforms[prefix - 1])
        )
        if prefix <= 3:
            source["base"] = full_source
        elif prefix < edge_count:
            defect = (
                prefix_residuals[prefix]
                - stencil(
                    prefix_residuals[prefix - 1],
                    prefix + 1,
                    (1.0 - q) / 2.0,
                )
                + stencil(
                    prefix_residuals[prefix - 2],
                    prefix + 1,
                    (1.0 - q) ** 2 / 4.0,
                )
            )
            u_value = float(defect[prefix - 2])
            mass = float(defect[prefix] + 3.0 * u_value)

            def u_transform(value: float) -> float:
                return (
                    2.0
                    * value
                    * (
                        math.cos((prefix - 2) * theta)
                        + 2.0 * math.cos((prefix - 1) * theta)
                        - 3.0 * math.cos(prefix * theta)
                    )
                )

            source["constant_u"] = u_transform(constant_u)
            source["delta_u"] = u_transform(u_value - constant_u)
            source["mass"] = 2.0 * mass * math.cos(prefix * theta)
            assert abs(full_source - sum(source.values())) <= 1.0e-12
        else:
            source["endpoint"] = full_source

        for name in names:
            components[name].append(
                first_coefficient * components[name][prefix]
                - second_coefficient * components[name][prefix - 1]
                + source[name]
            )

    ideal = (
        -(q * q)
        * (1.0 - q) ** edge_count
        * (-(math.cos(phi) ** edge_count) - math.ldexp(1.0, -edge_count))
    )
    final_endpoint = float(prefix_residuals[-1][-1])
    position = {name: components[name][edge_count + 1] / q**2 for name in names}
    position["base"] -= ideal / q**2
    position["endpoint"] -= final_endpoint / q**2

    velocity = {
        name: (components[name][edge_count + 1] - (1.0 - q) * components[name][edge_count]) / q**3
        for name in names
    }
    velocity["base"] += ideal / (5.0 * q**2)
    eta = (1.0 - q * q) / 2.0
    kappa = eta * proper_frontier - q**3 / 5.0
    velocity["endpoint"] += (-final_endpoint + kappa + (1.0 - q) * eta * proper_error_last) / q**3
    return position, velocity


def screen(edge_count: int, max_qk: float) -> None:
    (
        q,
        degrees,
        p,
        v,
        prefix_residuals,
        proper_error_last,
        proper_frontier,
    ) = full_face_entry(edge_count)
    r_zero = residual(p, degrees, q)
    r_velocity_zero = residual(v, degrees, q)
    packet = -(q * q / 2.0) * (1.0 - q) ** edge_count * binomial_probabilities(edge_count)
    packet_error = r_zero - packet

    p_one, _, raw_one = one_step(p, v, degrees, q)
    assert raw_one.min() > 0.0
    r_one = residual(p_one, degrees, q)
    coefficient_zero = cosine_coefficients(r_zero, degrees)
    coefficient_velocity = cosine_coefficients(r_velocity_zero, degrees)
    coefficient_one = cosine_coefficients(r_one, degrees)
    band = min(
        (edge_count - 1) // 2,
        max(1, int(math.sqrt(edge_count / max(1.0, math.log(edge_count))))),
    )
    lemma_band = int(math.sqrt(edge_count / (64.0 * math.log(16.0 * edge_count))))
    relative_defects = []
    position_profiles = []
    velocity_correction_profiles = []
    combined_lemma_defects = []
    lemma_position_profiles = []
    lemma_velocity_correction_profiles = []
    quadrature_consistency = []
    first_position_signed = None
    first_velocity_correction_signed = None
    first_quadrature_relative = None
    for index in range(1, band + 1):
        mode = 2 * index
        phi = mode * math.pi / (2.0 * edge_count)
        radius = (1.0 - q) * math.cos(phi)
        quadrature_from_first_step = (
            coefficient_one[mode] / radius - coefficient_zero[mode] * math.cos(phi)
        ) / math.sin(phi)
        quadrature = q * coefficient_velocity[mode] / math.tan(phi)
        endpoint_mass = math.ldexp(1.0, -edge_count)
        signed_ideal = (
            -(q * q / edge_count)
            * (1.0 - q) ** edge_count
            * ((-1.0) ** index * math.cos(phi) ** edge_count - endpoint_mass)
        )
        ideal_amplitude = abs(signed_ideal)
        position_profile = edge_count * abs(coefficient_zero[mode] - signed_ideal) / q**2
        velocity_correction_profile = (
            edge_count * abs(coefficient_velocity[mode] + signed_ideal / 5.0) / q**2
        )
        position_profiles.append(position_profile)
        velocity_correction_profiles.append(velocity_correction_profile)
        quadrature_consistency.append(
            abs(quadrature - quadrature_from_first_step) / ideal_amplitude
        )
        if index == 1:
            first_position_signed = edge_count * (coefficient_zero[mode] - signed_ideal) / q**2
            first_velocity_correction_signed = (
                edge_count * (coefficient_velocity[mode] + signed_ideal / 5.0) / q**2
            )
            first_quadrature_relative = quadrature / signed_ideal
        relative_defects.append(
            max(
                abs(coefficient_zero[mode] - signed_ideal),
                abs(quadrature),
            )
            / ideal_amplitude
        )
        if index <= lemma_band:
            lemma_position_profiles.append(position_profile)
            lemma_velocity_correction_profiles.append(velocity_correction_profile)
            combined_lemma_defects.append(
                (abs(coefficient_zero[mode] - signed_ideal) + abs(quadrature)) / ideal_amplitude
            )

    if combined_lemma_defects:
        maximum_combined_lemma_defect = max(combined_lemma_defects)
        assert maximum_combined_lemma_defect <= 1.0 / 64.0
        lemma_check = f"{maximum_combined_lemma_defect:.6g}<=1/64"
        maximum_lemma_position_profile = max(lemma_position_profiles)
        maximum_lemma_velocity_profile = max(lemma_velocity_correction_profiles)
        assert maximum_lemma_position_profile <= 1.0 / 256.0
        assert maximum_lemma_velocity_profile <= 1.0 / 4.0
        profile_check = (
            f"C={maximum_lemma_position_profile:.6g}<=1/256 "
            f"V={maximum_lemma_velocity_profile:.6g}<=1/4"
        )
    else:
        lemma_check = "vacuous(H_m=0)"
        profile_check = "vacuous(H_m=0)"

    maximum_quadrature_consistency = max(quadrature_consistency)
    assert maximum_quadrature_consistency <= 1.0e-6

    first_range_crossing = None
    first_certificate = None
    min_raw_margin = math.inf
    min_envelope_margin = math.inf
    maximum_steps = math.ceil(max_qk / q)
    for step in range(1, maximum_steps + 1):
        p_next, v_next, raw = one_step(p, v, degrees, q)
        r_next = residual(p_next, degrees, q)
        delta = max(0.0, r_next.max() / (q * q))
        min_raw_margin = min(min_raw_margin, float(raw.min()))
        min_envelope_margin = min(
            min_envelope_margin,
            float((p_next - delta).min()),
        )
        assert raw.min() > 0.0, f"projection activated at terminal step {step}"
        assert (p_next - delta).min() > 0.0, f"safe subtraction clipped at terminal step {step}"
        if first_range_crossing is None and np.ptp(r_next) <= q**3 / 5.0:
            first_range_crossing = step
        corrected_minimum = float(r_next.min()) - max(0.0, float(r_next.max()))
        if corrected_minimum >= -(q**3) / 5.0:
            first_certificate = step
            break
        p, v = p_next, v_next
    assert first_certificate is not None, (
        "no literal safe-envelope certificate in requested horizon"
    )
    assert first_range_crossing is not None

    weighted_l1 = float(np.dot(degrees, np.abs(r_zero)))
    weighted_packet_error = float(np.dot(degrees, np.abs(packet_error)))
    l_r_zero = (r_zero - h_apply(r_zero, degrees, q)) / (1.0 - q * q)
    velocity_source = r_one / (1.0 - q) - l_r_zero
    cycle_size = 2 * edge_count
    directed_plus = np.zeros(cycle_size)
    directed_plus[: edge_count + 1] = packet
    directed_plus[0] /= 2.0
    directed_plus[edge_count] /= 2.0
    directed_minus = np.array([directed_plus[-index % cycle_size] for index in range(cycle_size)])

    def average_cycle_shift(values: np.ndarray, amount: int) -> np.ndarray:
        return (values + np.roll(values, amount)) / 2.0

    directed_l_plus = (
        average_cycle_shift(directed_plus, 1) + average_cycle_shift(directed_plus, -1)
    ) / 2.0
    directed_l_minus = (
        average_cycle_shift(directed_minus, 1) + average_cycle_shift(directed_minus, -1)
    ) / 2.0
    directed_velocity = (
        average_cycle_shift(directed_plus, 1)
        - directed_l_plus
        + average_cycle_shift(directed_minus, -1)
        - directed_l_minus
    )[: edge_count + 1]
    directed_remainder = velocity_source - directed_velocity
    directed_positive_mass = float(np.dot(degrees, np.maximum(directed_remainder, 0.0)))
    lower_packet = np.zeros(edge_count + 1)
    lower_packet[1:edge_count] = (
        -0.5 * q**2 * (1.0 - q) ** edge_count * binomial_probabilities(edge_count - 2)
    )
    deconvolution = np.zeros(edge_count + 1)
    deconvolution[0] = -lower_packet[1] / 2.0
    deconvolution[-1] = lower_packet[-2] / 2.0
    deconvolution[1:-1] = (lower_packet[:-2] - lower_packet[2:]) / 4.0
    static_data = q * r_velocity_zero - deconvolution
    static_remainder = (static_data - h_apply(static_data, degrees, q)) / (1.0 - q * q)
    assert np.max(np.abs(static_remainder - directed_remainder)) <= 1.0e-7 * q**3
    static_positive_mass = float(np.dot(degrees, np.maximum(static_data, 0.0)))
    print(
        f"m={edge_count:5d} q={q:.9g} alpha={q * q:.9g} "
        f"rho=tau={q / 5.0:.9g} graph=P_m seed=v0 "
        "stop=min(r)-max(0,max(r))>=-q^3/5 arithmetic=float64"
    )
    print(
        f"  entry_L1D/q2={weighted_l1 / q**2:.9f} "
        f"entry_range/q^(5/2)={np.ptp(r_zero) / q**2.5:.9f} "
        f"packet_error_L1D/q2={weighted_packet_error / q**2:.9f}"
    )
    print(
        f"  modal_band={band} "
        f"max_even_modal_defect={max(relative_defects):.6g} "
        f"lemma_band={lemma_band} combined_lemma_check={lemma_check} "
        f"first_range_k={first_range_crossing} "
        f"qk_range={q * first_range_crossing:.9f} "
        f"first_certificate_k={first_certificate} "
        f"qk_certificate={q * first_certificate:.9f} "
        f"raw_margin/q2={min_raw_margin / q**2:.6g} "
        f"envelope_margin/q2={min_envelope_margin / q**2:.6g}"
    )
    print(
        f"  wider_profile_C={max(position_profiles):.6g} "
        f"wider_profile_VplusG5={max(velocity_correction_profiles):.6g} "
        f"profile_lemma_check={profile_check} "
        f"first_signed_C={first_position_signed:.6g} "
        f"first_signed_VplusG5={first_velocity_correction_signed:.6g} "
        f"first_D_over_G={first_quadrature_relative:.6g} "
        f"velocity_identity_relerr={maximum_quadrature_consistency:.3g}"
    )
    print(
        f"  measured_c_over_q3=[{packet_error.min() / q**3:.6g},"
        f"{packet_error.max() / q**3:.6g}] "
        f"measured_w_over_q3=[{velocity_source.min() / q**3:.6g},"
        f"{velocity_source.max() / q**3:.6g}] "
        f"weighted_mean_w_over_q3={np.dot(degrees, velocity_source) / q**3:.6g} "
        f"directed_uplus_L1D/q3={directed_positive_mass / q**3:.6g} "
        f"static_dplus_L1D/q3={static_positive_mass / q**3:.6g} "
        f"entry_c_max/q3={packet_error.max() / q**3:.6g}"
    )
    position_pieces, velocity_pieces = five_piece_decomposition(
        prefix_residuals,
        proper_error_last,
        proper_frontier,
        q,
    )
    piece_names = ("base", "constant_u", "delta_u", "mass", "endpoint")
    position_text = ",".join(f"{name}:{position_pieces[name]:.6g}" for name in piece_names)
    velocity_text = ",".join(f"{name}:{velocity_pieces[name]:.6g}" for name in piece_names)
    print(
        f"  measured_five_piece_C=[{position_text}] "
        f"sum={sum(position_pieces.values()):.6g} "
        f"measured_five_piece_V=[{velocity_text}] "
        f"sum={sum(velocity_pieces.values()):.6g}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "m",
        nargs="*",
        type=int,
        default=[128, 256, 512, 1024],
        help="path edge counts",
    )
    parser.add_argument(
        "--max-qk",
        type=float,
        default=8.0,
        help="maximum normalized terminal horizon",
    )
    arguments = parser.parse_args()
    exact_chronology_reduction_checks()
    exact_chronology_correction_checks()
    exact_finite_q_correction_checks()
    exact_boundary_source_checks()
    exact_directional_packet_checks()
    position_profile_asymptotic_checks()
    for edge_count in arguments.m:
        if edge_count < 3:
            raise ValueError("every screened path needs at least three edges")
        screen(edge_count, arguments.max_qk)


if __name__ == "__main__":
    main()
