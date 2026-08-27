#!/usr/bin/env python3
"""Exact preflights and finite screens for the terminal early kernel."""

from __future__ import annotations

import math
import sys
from fractions import Fraction

import numpy as np

from verify import (
    _fraction_optimum,
    _fraction_residual,
    _fraction_step,
    binomial_probabilities,
    full_face_entry,
    residual,
)

Polynomial = dict[int, Fraction]


def add(left: Polynomial, right: Polynomial, scale: Fraction = Fraction(1)) -> Polynomial:
    answer = dict(left)
    for exponent, value in right.items():
        answer[exponent] = answer.get(exponent, Fraction(0)) + scale * value
        if answer[exponent] == 0:
            del answer[exponent]
    return answer


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for left_exponent, left_value in left.items():
        for right_exponent, right_value in right.items():
            exponent = left_exponent + right_exponent
            answer[exponent] = answer.get(exponent, Fraction(0)) + left_value * right_value
    return {exponent: value for exponent, value in answer.items() if value}


def scale(values: Polynomial, factor: Fraction) -> Polynomial:
    return {exponent: factor * value for exponent, value in values.items() if factor * value}


def power(values: Polynomial, exponent: int) -> Polynomial:
    answer: Polynomial = {0: Fraction(1)}
    for _ in range(exponent):
        answer = multiply(answer, values)
    return answer


def monomial(exponent: int, coefficient: Fraction = Fraction(1)) -> Polynomial:
    return {exponent: coefficient}


B_POLY = {0: Fraction(1, 2), -1: Fraction(1, 2)}
L_POLY = {-1: Fraction(1, 4), 0: Fraction(1, 2), 1: Fraction(1, 4)}


def j_polynomials(maximum: int) -> list[Polynomial]:
    kernels: list[Polynomial] = [{}, {0: Fraction(1)}]
    for _ in range(1, maximum):
        kernels.append(
            add(
                scale(multiply(L_POLY, kernels[-1]), Fraction(2)),
                multiply(L_POLY, kernels[-2]),
                Fraction(-1),
            )
        )
    return kernels[: maximum + 1]


def tail_coefficient(step: int, displacement: int) -> Fraction:
    distance = abs(displacement)
    if distance > step:
        return Fraction(0)
    return Fraction(
        sum(math.comb(step, index) for index in range(distance, step + 1)), 2 ** (step + 1)
    )


def exact_laurent_checks() -> None:
    kernels = j_polynomials(16)
    for step in range(1, 16):
        direct = multiply(
            add(kernels[step], kernels[step - 1], Fraction(-1, 2)),
            L_POLY,
        )
        closed = scale(
            multiply(power(B_POLY, step), {index: Fraction(1) for index in range(step + 1)}),
            Fraction(1, 2),
        )
        assert direct == closed
        for displacement in range(-step - 2, step + 3):
            assert direct.get(displacement, Fraction(0)) == tail_coefficient(step, displacement)

    assert tail_coefficient(2, 0) == Fraction(1, 2)
    assert tail_coefficient(2, 1) == Fraction(3, 8)
    assert tail_coefficient(2, 2) == Fraction(1, 8)
    assert 2 * tail_coefficient(2, 1) == Fraction(3, 4)
    assert tail_coefficient(2, 1) > Fraction(1, 4)

    # Check both exact moving-source formulas against direct multiplication.
    delta = Fraction(7, 8)
    derivative_strength = Fraction(5, 17)
    mass_strength = Fraction(3, 19)
    for step, source_time, lag in ((1, 4, 3), (3, 5, 4), (7, 6, 2)):
        source_derivative = scale(
            multiply(
                monomial(source_time - 2),
                multiply({0: Fraction(1), 1: Fraction(-1)}, {0: Fraction(1), 1: Fraction(3)}),
            ),
            derivative_strength,
        )
        source_mass = monomial(source_time, mass_strength)
        entry_difference = scale(
            add(kernels[lag + 1], kernels[lag], Fraction(-1)),
            delta**lag,
        )
        direct_derivative = multiply(
            multiply(
                add(kernels[step], kernels[step - 1], Fraction(-1, 2)),
                L_POLY,
            ),
            multiply(entry_difference, source_derivative),
        )
        direct_mass = multiply(
            multiply(
                add(kernels[step], kernels[step - 1], Fraction(-1, 2)),
                L_POLY,
            ),
            multiply(entry_difference, source_mass),
        )

        common = multiply(
            power(B_POLY, step + lag - 1),
            multiply(
                add({0: Fraction(1)}, monomial(step + 1), Fraction(-1)),
                add(monomial(-1), monomial(lag)),
            ),
        )
        closed_derivative = scale(
            multiply(
                common,
                multiply(monomial(source_time - 2), {0: Fraction(1), 1: Fraction(3)}),
            ),
            delta**lag * derivative_strength / 4,
        )
        # common already contains 1-z^(k+1); the mass formula needs division
        # by 1-z, so replace that factor by the geometric sum once.
        common_without_difference = multiply(
            power(B_POLY, step + lag - 1),
            add(monomial(-1), monomial(lag)),
        )
        closed_mass = scale(
            multiply(
                common_without_difference,
                multiply(
                    {index: Fraction(1) for index in range(step + 1)},
                    monomial(source_time),
                ),
            ),
            delta**lag * mass_strength / 4,
        )
        assert direct_derivative == closed_derivative
        assert direct_mass == closed_mass

    print("exact_early_laurent=tail_kernel:pass moving_sources:pass reflection_3/8:pass")


def even_extension(values: list[Fraction]) -> list[Fraction]:
    return values + values[-2:0:-1]


def cycle_l(values: list[Fraction]) -> list[Fraction]:
    size = len(values)
    return [
        (values[(index - 1) % size] + 2 * values[index] + values[(index + 1) % size]) / 4
        for index in range(size)
    ]


def apply_folded_tail(values: list[Fraction], step: int) -> list[Fraction]:
    size = len(values)
    return [
        sum(
            tail_coefficient(step, (target - source + size // 2) % size - size // 2) * value
            for source, value in enumerate(values)
        )
        for target in range(size)
    ]


def exact_replay_checks() -> None:
    for edge_count in (8, 12):
        q = Fraction(1, 16 * edge_count)
        delta = 1 - q
        degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]
        position = [Fraction(0)]
        velocity = [Fraction(0)]
        for length in range(1, edge_count + 1):
            optimum = _fraction_optimum(length, degrees, q)
            next_position, next_velocity = _fraction_step(position, velocity, degrees[:length], q)
            next_optimum = _fraction_optimum(length + 1, degrees, q)
            position = next_position + [Fraction(0)]
            velocity = [
                value + new_value - old_value
                for value, new_value, old_value in zip(
                    next_velocity + [Fraction(0)],
                    next_optimum,
                    optimum + [Fraction(0)],
                    strict=True,
                )
            ]

        entry_b = [q * value for value in _fraction_residual(velocity, degrees, q)]
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
        cycle_data = even_extension(static_data)
        source = cycle_l(cycle_data)
        previous = [Fraction(0) for _ in source]
        current = source
        for step in range(1, min(6, edge_count)):
            half_velocity = [
                value - old_value / 2 for value, old_value in zip(current, previous, strict=True)
            ]
            assert half_velocity == apply_folded_tail(cycle_data, step)
            following = [
                2 * value - old_value
                for value, old_value in zip(cycle_l(current), cycle_l(previous), strict=True)
            ]
            previous, current = current, following

    print("exact_early_replay=m=8,12 u=Ld:pass folded_T_recurrence:pass")


def finite_screen(edge_count: int) -> float:
    q, degrees, position, velocity, *_ = full_face_entry(edge_count)
    delta = 1.0 - q
    entry_b = q * residual(velocity, degrees, q)
    gamma = np.zeros(edge_count + 1)
    gamma[1:edge_count] = -0.5 * q**2 * delta**edge_count * binomial_probabilities(edge_count - 2)
    deconvolution = np.zeros(edge_count + 1)
    deconvolution[0] = -gamma[1] / 2.0
    deconvolution[-1] = gamma[-2] / 2.0
    deconvolution[1:-1] = (gamma[:-2] - gamma[2:]) / 4.0
    path_data = entry_b - deconvolution
    cycle_data = np.r_[path_data, path_data[-2:0:-1]]

    def lazy(values: np.ndarray) -> np.ndarray:
        return (np.roll(values, 1) + 2.0 * values + np.roll(values, -1)) / 4.0

    source = lazy(cycle_data)
    previous = np.zeros_like(source)
    current = source.copy()
    maximum = -math.inf
    maximum_step = 0
    maximum_row = 0
    final_step = math.ceil((3.0 / 50.0) / q) - 1
    for step in range(1, final_step + 1):
        half_velocity = current - previous / 2.0
        row = int(np.argmax(half_velocity[: edge_count + 1]))
        value = float(half_velocity[row] / q**3)
        if value > maximum:
            maximum = value
            maximum_step = step
            maximum_row = row
        following = 2.0 * lazy(current) - lazy(previous)
        previous, current = current, following
    assert maximum < 1.0 / 16.0
    print(
        f"finite_early_screen=m={edge_count} max/q3={maximum:.9f} "
        f"k={maximum_step} row={maximum_row} qk={q * maximum_step:.9f} "
        "scope=MEASURED"
    )
    return maximum


def main() -> None:
    exact_laurent_checks()
    exact_replay_checks()
    sizes = [int(value) for value in sys.argv[1:]] or [64, 128]
    for edge_count in sizes:
        assert edge_count >= 8
        finite_screen(edge_count)
    print("terminal_early_kernel=PASS theorem=exact_reduction short_window_1/16=OPEN")


if __name__ == "__main__":
    main()
