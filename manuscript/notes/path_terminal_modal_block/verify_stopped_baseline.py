#!/usr/bin/env python3
"""Exact preflight for the stopped leading combined baseline."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import math


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


def derivative_weight(step: int, distance: int) -> Fraction:
    return (
        ell(step, step - distance)
        + 2 * ell(step, step - distance - 1)
        - 3 * ell(step, step - distance - 2)
    )


def tail(step: int, distance: int) -> Fraction:
    if distance > step:
        return Fraction(0)
    return Fraction(
        sum(math.comb(step, index) for index in range(distance, step + 1)),
        2 ** (step + 1),
    )


def stopped_sum(step: int, distance: int) -> Fraction:
    return sum(
        (derivative_weight(source_lag, step - 1 + distance) for source_lag in range(1, step + 1)),
        Fraction(0),
    )


def fixed_p(index: int) -> Fraction:
    if index == 0:
        return Fraction(18)
    if index == 1:
        return Fraction(6)
    return Fraction(8) + 4 * Fraction(-1, 2) ** index


def a_coefficient(row: int, index: int) -> Fraction:
    if index < 0:
        return Fraction(0)
    return Fraction(math.comb(row + index - 1, index), 2 ** (row + index))


def alternating_r(row: int, index: int) -> Fraction:
    return sum(
        (Fraction(-1, 2) ** (index - part) * a_coefficient(row, part) for part in range(index + 1)),
        Fraction(0),
    )


def geometric_factor(index: int) -> Fraction:
    """Coefficient of 1 / ((1-t)(1+t/2))."""
    if index < 0:
        return Fraction(0)
    return sum((Fraction(-1, 2) ** part for part in range(index + 1)), Fraction(0))


def h_coefficient(row: int, index: int) -> Fraction:
    """Coefficient h_{row,index} from the fixed-row generating function."""
    factor = [
        18 * geometric_factor(power)
        - 16 * geometric_factor(power - 1)
        - 4 * geometric_factor(power - 2)
        + 5 * geometric_factor(power - 3)
        for power in range(index + 1)
    ]
    return sum(
        (a_coefficient(row, part) * factor[index - part] for part in range(index + 1)),
        Fraction(0),
    )


def check_tail_domination() -> None:
    differences: dict[tuple[int, int], Fraction] = {}
    for step in range(1, 129):
        for distance in range(step + 2):
            value = stopped_sum(step, distance) - 2 * tail(step, distance)
            differences[step, distance] = value
            assert value >= 0

        if step == 1:
            assert differences[1, 0] == 1
            assert differences[1, 1] == Fraction(1, 2)
        else:
            assert differences[step, 0] == Fraction(1, 3) * (1 - Fraction(-1, 2) ** (step - 2))
        if step >= 2:
            for distance in range(1, step + 1):
                assert (
                    differences[step, distance]
                    == (
                        differences[step - 1, distance - 1]
                        + differences.get((step - 1, distance), Fraction(0))
                    )
                    / 2
                )
    print("stopped_tail_domination=PASS k<=128 exact_pascal=pass S>=2t=pass")


def check_h_axis_certificate() -> None:
    central_slack = 2**127 - 28 * math.comb(126, 63)
    assert central_slack == 1163019259149843951707093891970921728 > 0

    for edge_count in (64, 65, 96, 128):
        coefficients = [a_coefficient(edge_count, index) for index in range(edge_count)]
        assert sum(coefficients, Fraction(0)) == Fraction(1, 2)
        assert coefficients[-2] == coefficients[-1]
        central = coefficients[-1]
        reverse_sum = alternating_r(edge_count, edge_count - 1)
        assert reverse_sum >= central / 2

        endpoint_h = h_coefficient(edge_count, edge_count - 1)
        partial_fraction_value = (
            18 * coefficients[-1]
            - 10 * coefficients[-2]
            + 2 * sum(coefficients, Fraction(0))
            - 2 * reverse_sum
        )
        assert endpoint_h == partial_fraction_value <= 1 + 7 * central < Fraction(5, 4)

        previous = h_coefficient(edge_count, 1)
        for index in range(1, edge_count - 1):
            n_value = index + 1
            current = h_coefficient(edge_count, index + 1)
            r_value = alternating_r(edge_count, n_value)
            exact_difference = (
                10 * a_coefficient(edge_count, n_value - 2)
                - 28 * a_coefficient(edge_count, n_value - 1)
                + 24 * a_coefficient(edge_count, n_value)
                - 6 * r_value
            )
            assert current - previous == exact_difference
            assert r_value <= (
                a_coefficient(edge_count, n_value)
                - a_coefficient(edge_count, n_value - 1) / 2
                + a_coefficient(edge_count, n_value - 2) / 4
            )
            lower = (
                18 * a_coefficient(edge_count, n_value)
                - 25 * a_coefficient(edge_count, n_value - 1)
                + Fraction(17, 2) * a_coefficient(edge_count, n_value - 2)
            )
            d_value = edge_count - n_value - 1
            denominator = (edge_count + n_value - 1) * (edge_count + n_value - 2)
            polynomial = 2 * (
                3 * n_value**2
                + 11 * n_value * d_value
                + 9 * d_value**2
                - 10 * n_value
                - 9 * d_value
            )
            assert lower * denominator / a_coefficient(edge_count, n_value) == polynomial > 0
            assert current > previous
            previous = current
        assert previous == endpoint_h < Fraction(5, 4)

    assert a_coefficient(65, 64) / a_coefficient(64, 63) == Fraction(127, 128)
    print(
        "stopped_h_axis_certificate=PASS m=64,65,96,128 "
        "delta_h=positive central_binomial=pass h<5/4"
    )


def leading_corrections(maximum: int) -> dict[int, list[Fraction]]:
    corrections: dict[int, list[Fraction]] = {
        1: [Fraction(-1, 5)],
        2: [Fraction(2, 5), Fraction(0)],
    }
    for length in range(2, maximum):
        previous = corrections[length - 1]
        current = corrections[length]
        z_value = [2 * current[index] - previous[index] for index in range(length - 1)] + [
            2 * current[-1] - Fraction(3, 10)
        ]
        corrections[length + 1] = [
            (z_value[0] + z_value[1]) / 2,
            *[
                (
                    z_value[index]
                    + z_value[index - 1] / 2
                    + (z_value[index + 1] / 2 if index + 1 < length else 0)
                )
                / 2
                for index in range(1, length)
            ],
            z_value[-1] / 4 + Fraction(3, 10),
        ]
    return corrections


def even_extension(values: list[Fraction]) -> list[Fraction]:
    return values + values[-2:0:-1]


def lazy(values: list[Fraction]) -> list[Fraction]:
    size = len(values)
    return [
        (values[(index - 1) % size] + 2 * values[index] + values[(index + 1) % size]) / 4
        for index in range(size)
    ]


def check_stopped_comparison() -> None:
    for edge_count in (8, 12, 16, 64):
        corrections = leading_corrections(2 * edge_count + 1)
        older = even_extension(corrections[edge_count] + [Fraction(0)])
        current = even_extension(corrections[edge_count + 1])
        folded_differences: dict[tuple[int, int], Fraction] = {}

        for step in range(1, edge_count):
            following = [
                2 * left - right for left, right in zip(lazy(current), lazy(older), strict=True)
            ]
            proper_half_difference = [
                left - right / 2 for left, right in zip(following, current, strict=True)
            ]
            older, current = current, following

            endpoint_tail = [tail(step, abs(index - edge_count)) for index in range(2 * edge_count)]

            continued_time = edge_count + step + 1
            continued = [
                corrections[continued_time][index] - corrections[continued_time - 1][index] / 2
                for index in range(continued_time - 1)
            ]

            for distance in range(edge_count + 1):
                path_index = edge_count - distance
                folded_sum = (
                    proper_half_difference[path_index] - continued[path_index]
                ) / Fraction(3, 40)
                folded_difference = folded_sum - 2 * tail(step, distance)
                folded_differences[step, distance] = folded_difference
                assert folded_difference >= 0

            axis_formula = (
                4
                - (fixed_p(step) + 2 * h_coefficient(edge_count, step)) / 3
                + Fraction(6, 2**edge_count)
            )
            assert folded_differences[step, 0] == axis_formula

            # Match the proof's monotone lower bound: discard A H >= 0 and
            # replace B by its uniform upper bound 3/20.
            combined = [
                value - Fraction(3, 20) * t_value
                for value, t_value in zip(proper_half_difference, endpoint_tail, strict=True)
            ]
            assert all(combined[index] >= continued[index] for index in range(edge_count + 1))

        assert folded_differences[1, 1] == Fraction(1, 2)
        assert all(folded_differences[1, distance] == 0 for distance in range(2, edge_count + 1))
        for step in range(1, edge_count - 1):
            for distance in range(1, edge_count + 1):
                assert (
                    folded_differences[step + 1, distance]
                    == (folded_differences[step, distance - 1] + folded_differences[step, distance])
                    / 2
                )
    print(
        "stopped_leading_comparison=PASS m=8,12,16,64 all_k<m "
        "folded_axis=exact folded_pascal=exact A_discarded B=3/20"
    )


def check_frontier_bound() -> None:
    q = Fraction(1, 1024)
    t = Fraction(113, 128)
    cleared_gap = 6 - q - 5 * q**2 - 10 * t + t**2 * (4 - q - 5 * q**2)
    assert cleared_gap == Fraction(4940251803, 17179869184) > 0
    lower = Fraction(3488, 1921)
    assert 3 * lower / 8 - Fraction(1, 10) > 0
    assert Fraction(2, 8) - Fraction(1, 10) == Fraction(3, 20)
    print(f"stopped_frontier_bound=PASS cleared_gap={cleared_gap} wp_interval=[{lower},2]")


def main() -> None:
    check_tail_domination()
    check_h_axis_certificate()
    check_stopped_comparison()
    check_frontier_bound()
    print("terminal_stopped_baseline=PASS leading_margin=31/320 finite_q_ledger=OPEN")


if __name__ == "__main__":
    main()
