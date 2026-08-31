#!/usr/bin/env python3
"""Exact arithmetic checks for the terminal early--late regime reduction."""

import math
from fractions import Fraction

from verify import _fraction_optimum, _fraction_residual, _fraction_step


def exact_full_entry_replay_checks() -> None:
    """Check the N=m+1 old-row identity and actual endpoint in exact arithmetic."""
    for edge_count in (8, 12):
        q = Fraction(1, 16 * edge_count)
        delta = 1 - q
        eta = (1 - q * q) / 2
        degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]
        p = [Fraction(0)]
        velocity = [Fraction(0)]
        last_entry_residual: list[Fraction] | None = None
        last_optimum: list[Fraction] | None = None
        last_sigma: Fraction | None = None

        for length in range(1, edge_count + 1):
            optimum = _fraction_optimum(length, degrees, q)
            if length == edge_count:
                last_entry_residual = _fraction_residual(p, degrees[:length], q)
                last_optimum = optimum
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

        assert last_entry_residual is not None
        assert last_optimum is not None
        assert last_sigma is not None
        entry_residual = _fraction_residual(p, degrees, q)
        average = [
            (position + q * center) / (1 + q) for position, center in zip(p, velocity, strict=True)
        ]
        average_residual = _fraction_residual(average, degrees, q)
        assert all(value < 0 for value in average_residual)
        assert [(1 + q) * average_residual[index] for index in range(edge_count)] == [
            2 * entry_residual[index] - delta * last_entry_residual[index]
            for index in range(edge_count)
        ]
        endpoint_formula = -2 * eta * last_sigma + eta * q * last_optimum[-1] + q**3 / 5
        assert (1 + q) * average_residual[-1] == endpoint_formula

        ideal_last = [
            q**2 * delta ** (edge_count - 1) * Fraction(2, 2**edge_count)
            if index == 0
            else q**2
            * delta ** (edge_count - 1)
            * Fraction(math.comb(edge_count - 1, index), 2**edge_count)
            for index in range(edge_count)
        ]
        ideal_extended = [
            q**2 * delta**edge_count * Fraction(2, 2 ** (edge_count + 1))
            if index == 0
            else q**2
            * delta**edge_count
            * Fraction(math.comb(edge_count, index), 2 ** (edge_count + 1))
            for index in range(edge_count)
        ]
        correction_last = [
            -last_entry_residual[index] - ideal_last[index] for index in range(edge_count)
        ]
        correction_extended = [
            -entry_residual[index] - ideal_extended[index] for index in range(edge_count)
        ]
        hypothetical_difference = [
            correction_extended[index] - delta * correction_last[index] / 2
            for index in range(edge_count)
        ]
        assert all(value > 0 for value in hypothetical_difference)

    print("exact_full_entry_replay=m=8,12 old_rows=pass endpoint=pass K_tilde_positive=pass")


def main() -> None:
    q_max = Fraction(1, 1024)
    x_zero = Fraction(1, 8) + Fraction(1, 4194304)

    # The uniform upper bound on x=2m*atanh(q), q=1/(16m).
    assert Fraction(1, 8) / (1 - q_max**2) <= x_zero < Fraction(1, 7)

    # Full-optimum extrema: coth(x)-1/5<157/20 and csch(x)-1/5>1243/160.
    tanh_lower = Fraction(1, 8) - Fraction(1, 8) ** 3 / 3
    assert tanh_lower - Fraction(20, 161) == Fraction(31, 247296)
    assert Fraction(161, 20) - Fraction(1, 5) == Fraction(157, 20)
    sinh_upper = x_zero + x_zero**3 / 5
    sinh_slack = Fraction(32, 255) - sinh_upper
    assert sinh_slack == Fraction(
        1868969381144821709,
        18815678955183742648320,
    )
    assert sinh_slack > 0
    assert Fraction(255, 32) - Fraction(1, 5) == Fraction(1243, 160)

    # The proper-prefix seed optimum is below q/8.
    exponential_lower = (
        1 - x_zero + x_zero**2 / 2 - x_zero**3 / 6 + x_zero**4 / 24 - x_zero**5 / 120
    )
    t_lower = Fraction(2711, 3072)
    assert exponential_lower > t_lower
    proper_seed_ratio = 2 * (2 + t_lower - 3 * t_lower**2) / (5 * (1 + t_lower**2))
    proper_seed_slack = Fraction(1, 8) - proper_seed_ratio
    assert proper_seed_slack == Fraction(1469573, 671468200)
    assert proper_seed_slack > 0
    assert 1 - 10 * Fraction(7, 8) - Fraction(7, 8) ** 2 < 0

    # One-step extension of the finite correction ledger and the actual
    # degree-one endpoint sign for the first full-face average residual.
    extended_correction_margin = Fraction(179, 14400) - Fraction(1, 600 * 64)
    assert extended_correction_margin == Fraction(1429, 115200)
    raw_frontier_lower = Fraction(596861, 326570)
    endpoint_residual_upper = Fraction(255, 512) * (
        -2 * raw_frontier_lower + Fraction(33, 16)
    ) + Fraction(1, 5)
    assert endpoint_residual_upper == -Fraction(46683733, 78684160)
    assert endpoint_residual_upper < 0

    # Late position minus safe-envelope comparison at s=3/50.
    time = Fraction(3, 50)
    position_constant = Fraction(649, 80)
    position_slope = Fraction(89, 40)
    assert position_slope < position_constant
    exponential_upper = 1 - time + time**2 / 2
    late_slack = Fraction(1243, 160) - exponential_upper * (
        position_constant + position_slope * time
    )
    assert late_slack == Fraction(1667, 625000)
    assert late_slack > 0

    exact_full_entry_replay_checks()

    print(
        "terminal_regime_reduction=PASS arithmetic=Fraction "
        f"sinh_slack={sinh_slack} "
        f"proper_seed_slack={proper_seed_slack} "
        f"extended_margin={extended_correction_margin} "
        f"endpoint_upper={endpoint_residual_upper} "
        f"late_slack={late_slack}"
    )
    print(
        "scope=proved_entry_bounds_and_late_stitch "
        "early_signed_half_retention=PROVED_BY_FINITE_STOPPED_LEDGER"
    )


if __name__ == "__main__":
    main()
