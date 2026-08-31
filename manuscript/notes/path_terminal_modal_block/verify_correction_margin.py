#!/usr/bin/env python3
"""Exact preflight for the sharpened full-entry correction margin.

This verifier checks the rational constants, every edge case in the sharpened
q=0 coefficient argument, the final-time folded source-support count, and the
correct two-row frontier-defect identity on exact representative replays.
"""

from fractions import Fraction
from functools import lru_cache
import math

from verify import (
    _fraction_ideal_prefix_packet,
    _fraction_optimum,
    _fraction_residual,
    _fraction_step,
)


def check_leading_coefficient_ledger() -> None:
    """Check the h edge cases, double induction, and final diagonal."""

    cutoff = 260
    h: dict[int, list[Fraction]] = {2: []}
    for step in range(cutoff + 1):
        h[2].append(
            2
            - Fraction(1, 8) * Fraction((-1) ** step, 2**step)
            + Fraction(21 - 10 * step, 8 * 2**step)
        )
    for row in range(3, cutoff + 1):
        h[row] = []
        for step in range(cutoff + 1):
            previous_step = h[row][step - 1] if step else Fraction(0)
            h[row].append((h[row - 1][step] + previous_step) / 2)

    assert h[3][0:2] == [Fraction(9, 4), Fraction(5, 2)]
    assert all(h[3][step] <= 2 + Fraction(1, 2**step) for step in range(2, cutoff + 1))
    assert h[4][0:4] == [
        Fraction(9, 8),
        Fraction(29, 16),
        Fraction(65, 32),
        Fraction(131, 64),
    ]
    for step in range(cutoff + 1):
        numerator = (
            -((-1) ** step)
            - 129
            - 66 * (step + 1)
            + 124 * math.comb(step + 2, 2)
            - 40 * math.comb(step + 3, 3)
        )
        assert h[4][step] - 2 == Fraction(numerator, 2 ** (step + 7))
    assert all(h[4][step] <= 2 for step in range(4, cutoff + 1))
    assert h[5][0:4] == [
        Fraction(9, 16),
        Fraction(19, 16),
        Fraction(103, 64),
        Fraction(117, 64),
    ]
    assert all(h[row][step] <= 2 for row in range(5, cutoff + 1) for step in range(cutoff + 1))

    # Reconstruct the q=0 correction recurrence itself and check the sharpened
    # final diagonal, including the separately treated seed and neighbor.
    previous = [Fraction(-1, 5)]
    current = [Fraction(2, 5), Fraction(0)]
    final_minima: dict[int, Fraction] = {}
    for length in range(2, 257):
        differences = [current[index] - previous[index] / 2 for index in range(length - 1)]
        if length >= 64:
            final_minima[length] = min(differences)
            assert final_minima[length] >= Fraction(31, 320)
        if length == 256:
            break
        z_value = [2 * current[index] - previous[index] for index in range(length - 1)] + [
            2 * current[-1] - Fraction(3, 10)
        ]
        following = [
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
        previous, current = current, following

    print(
        f"leading_coefficient_ledger=PASS min_m64={final_minima[64]} min_m256={final_minima[256]}"
    )


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


def check_folded_mass_support() -> None:
    """Check the exact final-time support count, including k=1/reflection."""
    for edge_count in range(64, 130):
        for coordinate in range(edge_count - 1):
            coefficient_sum = Fraction(0)
            support_count = 0
            for source_time in range(2, edge_count):
                step = edge_count - source_time
                positive = ell(step, coordinate - source_time)
                reflected = ell(step, coordinate + source_time)
                if step == 1:
                    assert positive == reflected == 0
                else:
                    assert positive <= Fraction(1, 2)
                    assert reflected <= Fraction(1, 2)
                    if positive:
                        assert 2 * source_time <= edge_count + coordinate - 1
                        support_count += 1
                    if reflected:
                        assert 2 * source_time <= edge_count - coordinate - 1
                        support_count += 1
                coefficient_sum += positive + reflected
            assert support_count <= edge_count - 1
            assert coefficient_sum <= Fraction(edge_count - 1, 2)
    print("folded_mass_support=PASS m=64..129 k1=zero reflection=counted")


def lazy_prefix(values: list[Fraction], degrees: list[Fraction]) -> list[Fraction]:
    out: list[Fraction] = []
    for index, value in enumerate(values):
        neighbors = Fraction(0)
        if index:
            neighbors += values[index - 1] / degrees[index]
        if index + 1 < len(values):
            neighbors += values[index + 1] / degrees[index]
        out.append((value + neighbors) / 2)
    return out


def check_two_row_defect_identity() -> None:
    """Replay exact prefixes and check the old-row and endpoint identities."""
    for edge_count in (8, 12):
        q = Fraction(1, 16 * edge_count)
        delta = 1 - q
        eta = (1 - q * q) / 2
        degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]
        p = [Fraction(0)]
        velocity = [Fraction(0)]
        corrections: dict[int, list[Fraction]] = {}
        optima: dict[int, list[Fraction]] = {}
        last_sigma: Fraction | None = None

        for length in range(1, edge_count + 1):
            optimum = _fraction_optimum(length, degrees, q)
            optima[length] = optimum
            negative_residual = [-value for value in _fraction_residual(p, degrees[:length], q)]
            ideal = _fraction_ideal_prefix_packet(length, q)
            corrections[length] = [
                left - right for left, right in zip(negative_residual, ideal, strict=True)
            ]
            p_next, velocity_next = _fraction_step(p, velocity, degrees[:length], q)
            if length == edge_count:
                last_sigma = p_next[-1]
            new_optimum = _fraction_optimum(length + 1, degrees, q)
            p = p_next + [Fraction(0)]
            velocity = [
                value + new_value - old_value
                for value, new_value, old_value in zip(
                    velocity_next + [Fraction(0)],
                    new_optimum,
                    optimum + [Fraction(0)],
                    strict=True,
                )
            ]

        assert last_sigma is not None
        full_residual = _fraction_residual(p, degrees, q)
        g = [
            -(q**2)
            * delta**edge_count
            * Fraction(math.comb(edge_count, index), 2 ** (edge_count + 1))
            for index in range(edge_count + 1)
        ]
        entry_correction = [left - right for left, right in zip(full_residual, g, strict=True)]

        current = corrections[edge_count]
        previous = corrections[edge_count - 1]
        correction_difference = [
            current[index] - delta * previous[index] / 2 for index in range(edge_count - 1)
        ] + [current[-1]]
        lazy_k = lazy_prefix(correction_difference, degrees[:edge_count])
        endpoint_basis = [Fraction(0)] * (edge_count - 1) + [Fraction(1)]
        lazy_endpoint = lazy_prefix(endpoint_basis, degrees[:edge_count])
        assert lazy_endpoint[-2:] == [Fraction(1, 4), Fraction(1, 2)]
        assert all(value == 0 for value in lazy_endpoint[:-2])
        frontier_defect = q * eta * optima[edge_count - 1][-1] / 2 - q**3 / 5
        expected_old = [
            -2 * delta * lazy_k[index]
            + delta * frontier_defect * lazy_endpoint[index]
            + (g[-1] if index == 0 else 0)
            for index in range(edge_count)
        ]
        assert entry_correction[:-1] == expected_old
        assert entry_correction[-1] == q**3 / 5 - eta * last_sigma - g[-1]

    print("two_row_defect_identity=PASS m=8,12 old_rows=exact endpoint=exact")


def check_sharpened_variation() -> None:
    """Check the sixteen-cell TV certificate and its parameter remainder."""

    def variation_function(value: Fraction) -> Fraction:
        return (value**4 - 30 * value**3 + 12 * value**2 + 10 * value + 3) / (
            10 * (1 + value**2) ** 2
        )

    left_endpoint = Fraction(7, 8)
    cell_width = Fraction(1, 128)
    cell_sum = Fraction(0)
    for index in range(16):
        left = left_endpoint + index * cell_width
        right = left + cell_width
        cell_sum += (
            cell_width / left * max(abs(variation_function(left)), abs(variation_function(right)))
        )
    assert cell_sum < Fraction(77, 12500)

    q_max = Fraction(1, 1024)
    parameter_error = 2 * q_max / (5 * (1 - q_max)) + 2 * q_max**2 / (5 * (1 - q_max**2))
    assert parameter_error == Fraction(684, 1747625) < Fraction(1, 2500)
    variation_bound = Fraction(8, 15) * (Fraction(77, 12500) + Fraction(1, 17500))
    assert variation_bound == Fraction(1088, 328125) < Fraction(1, 300)
    derivative_loss = Fraction(1, 360) + Fraction(1, 300)
    assert derivative_loss == Fraction(11, 1800)
    print(
        "sharpened_final_variation=PASS "
        f"cell_sum={cell_sum} variation_bound={variation_bound} "
        f"derivative_loss={derivative_loss}"
    )


def check_rational_constants() -> None:
    shared = Fraction(31, 320) - Fraction(11, 1800) - Fraction(3, 5120) - Fraction(43, 2400)
    assert shared == Fraction(16649, 230400) > Fraction(7, 100)
    frontier_source_slack = Fraction(9, 40) - Fraction(479, 600 * 1024) - Fraction(7, 32)
    assert frontier_source_slack == Fraction(3361, 614400) > 0
    frontier_recurrence_slack = Fraction(105, 256) - Fraction(1, 65536) - Fraction(2, 5)
    assert frontier_recurrence_slack == Fraction(3323, 327680) > 0

    interior = 2 * Fraction(15, 16) * shared
    penultimate = 2 * Fraction(15, 16) * (Fraction(3, 4) * shared + Fraction(1, 10)) - Fraction(
        101, 1280
    )
    frontier = 2 * Fraction(15, 16) * (Fraction(1, 5) + Fraction(1, 4) * shared) - Fraction(
        101, 640
    )
    endpoint = Fraction(6985811, 9835520) - Fraction(1, 8)
    assert interior == Fraction(16649, 122880) > Fraction(13, 100)
    assert penultimate == Fraction(34441, 163840) > Fraction(13, 100)
    assert frontier == Fraction(123401, 491520) > Fraction(13, 100)
    assert endpoint == Fraction(5756371, 9835520) > Fraction(13, 100)
    print(
        "rational_constants=PASS "
        f"shared={shared} interior={interior} penultimate={penultimate} "
        f"frontier={frontier} endpoint={endpoint}"
    )


def main() -> None:
    check_leading_coefficient_ledger()
    check_folded_mass_support()
    check_two_row_defect_identity()
    check_sharpened_variation()
    check_rational_constants()
    print(
        "scope=c_entry_margin_only "
        "combined_early_half_retention=PROVED_BY_FINITE_STOPPED_LEDGER "
        "T_d_bound_13/200=OPEN_UNNEEDED"
    )


if __name__ == "__main__":
    main()
