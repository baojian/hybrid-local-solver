#!/usr/bin/env python3
"""Exact preflight for the finite-q stopped correlated ledger."""

from __future__ import annotations

from collections import defaultdict
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


@lru_cache(maxsize=None)
def folded_ell(step: int, offset: int, edge_count: int) -> Fraction:
    period = 2 * edge_count
    support = step - 1
    return sum(
        (
            ell(step, offset + period * alias)
            for alias in range(-2, 3)
            if abs(offset + period * alias) <= support
        ),
        Fraction(0),
    )


@lru_cache(maxsize=None)
def endpoint_tail(step: int, distance: int) -> Fraction:
    if distance > step:
        return Fraction(0)
    return Fraction(
        sum(math.comb(step, index) for index in range(distance, step + 1)),
        2 ** (step + 1),
    )


def literal_derivative_atoms(edge_count: int, source: int) -> dict[int, int]:
    atoms: defaultdict[int, int] = defaultdict(int)
    period = 2 * edge_count
    for orientation in (1, -1):
        for position, weight in ((source - 2, 1), (source - 1, 2), (source, -3)):
            # The antipode is one cycle coordinate, not two reflected copies.
            if position == edge_count and orientation == -1:
                continue
            atoms[(orientation * position) % period] += weight
    return dict(atoms)


def derivative_response(edge_count: int, final_time: int, source: int, target: int) -> Fraction:
    step = final_time - source
    return sum(
        (
            weight * folded_ell(step, target - position, edge_count)
            for position, weight in literal_derivative_atoms(edge_count, source).items()
        ),
        Fraction(0),
    )


def mass_response(edge_count: int, final_time: int, source: int, target: int) -> Fraction:
    step = final_time - source
    result = folded_ell(step, target - source, edge_count)
    if source < edge_count:
        result += folded_ell(step, target + source, edge_count)
    return result


def check_folded_source_kernels() -> None:
    positive_alias = ell(14, 14 - 26) + 2 * ell(14, 14 - 26 - 1) - 3 * ell(14, 14 - 26 - 2)
    assert positive_alias == Fraction(15, 8192) > 0
    global_low = Fraction(0)
    global_high = Fraction(0)
    for edge_count in (8, 12, 16, 32, 64):
        for full_step in range(1, edge_count):
            final_time = edge_count + full_step + 1
            for source in range(2, edge_count + 1):
                step = final_time - source
                assert all(
                    folded_ell(step, offset, edge_count) <= Fraction(1, 2)
                    for offset in range(2 * edge_count)
                )
            for target in range(edge_count + 1):
                partial = Fraction(0)
                for source in range(2, edge_count + 1):
                    partial += derivative_response(edge_count, final_time, source, target)
                    global_low = min(global_low, partial)
                    global_high = max(global_high, partial)
                    assert Fraction(-10) <= partial <= Fraction(10)

                    mass = mass_response(edge_count, final_time, source, target)
                    assert 0 <= mass <= 1
    print(
        "finite_stopped_folded_kernels=PASS "
        f"m=8,12,16,32,64 derivative_prefix=[{float(global_low):.9f},{float(global_high):.9f}] "
        f"positive_alias={positive_alias} abel_gain=10 mass_gain=1 atom_gain=1/2"
    )


def lazy_folded_ell(step: int, offset: int, edge_count: int) -> Fraction:
    return (
        folded_ell(step, offset - 1, edge_count)
        + 2 * folded_ell(step, offset, edge_count)
        + folded_ell(step, offset + 1, edge_count)
    ) / 4


def check_base_response() -> None:
    for edge_count in (64, 96):
        q = Fraction(1, 16 * edge_count)
        base_one = {0: q / 5}
        neighbor = -q / 4 + q**2 / 20
        base_two = {0: -q / 2 + q**2 / 10, 1: neighbor, 2 * edge_count - 1: neighbor}
        for full_step in range(1, edge_count):
            final_time = edge_count + full_step + 1
            for target in range(edge_count + 1):
                response_two = sum(
                    (
                        value * folded_ell(final_time - 1, target - source, edge_count)
                        for source, value in base_two.items()
                    ),
                    Fraction(0),
                )
                response_one = sum(
                    (
                        value * lazy_folded_ell(final_time - 2, target - source, edge_count)
                        for source, value in base_one.items()
                    ),
                    Fraction(0),
                )
                assert abs(response_two - response_one) <= 3 * q / 5
    print("finite_stopped_base=PASS m=64,96 exact_cycle_replay loss<=3q/5<=3/5120")


def frontier_value(q: Fraction, index: int) -> Fraction:
    chi = (1 - q) / (1 + q)
    t_value = chi**index
    return (
        Fraction(2, 1 + q)
        * (t_value * (1 + t_value / 5) / chi + t_value - Fraction(1, 5))
        / (1 + t_value**2)
    )


@lru_cache(maxsize=None)
def directed_h_coefficient(edge_count: int, step: int, target: int) -> Fraction:
    period = 2 * edge_count
    plus_moves = (target - edge_count) % period
    minus_moves = (edge_count - target) % period

    def one_way(moves: int) -> Fraction:
        if not 1 <= moves <= step:
            return Fraction(0)
        return Fraction(math.comb(step - 1, moves - 1), 2 ** (step - 1))

    return (one_way(plus_moves) + one_way(minus_moves)) / 4


def check_endpoint_ledger() -> None:
    for edge_count in (64, 96, 128):
        q = Fraction(1, 16 * edge_count)
        delta = 1 - q
        eta = (1 - q**2) / 2
        p_values = {index: frontier_value(q, index) for index in range(1, edge_count + 1)}
        scaled_sigma = Fraction(1, q) - Fraction(1, 5)
        zeta = scaled_sigma - (3 * p_values[1] / 2 - Fraction(2, 5))
        assert 0 < zeta < 1 / q

        for index in range(2, edge_count):
            previous_p = p_values[index - 1]
            current_p = p_values[index]
            assert 0 < previous_p - current_p < 4 * q
            q_value = (
                eta * (previous_p - current_p)
                - q * (Fraction(3, 2) + q / 2) * current_p
                + 2 * q / 5
                + q**2 / 5
            )
            scaled_sigma = (
                current_p + eta * scaled_sigma - eta * previous_p / 2 - Fraction(1, 5)
            ) / (1 + q)
            new_zeta = scaled_sigma - (3 * current_p / 2 - Fraction(2, 5))
            assert new_zeta == (eta * zeta + q_value) / (1 + q)
            assert abs(q_value) < 11 * q / 2
            zeta = new_zeta
        assert abs(zeta) < Fraction(3, 256)

        p_value = p_values[edge_count]
        previous_p = p_values[edge_count - 1]
        p_dimensional = q**2 * p_value
        previous_dimensional = q**2 * previous_p
        sigma_dimensional = q**3 * scaled_sigma
        standard = (
            q * eta**2 * previous_dimensional / (4 * (1 + q))
            - delta * q * p_dimensional / 4
            + (3 + q) * q**3 / 20
        )
        endpoint = (
            -delta * eta * sigma_dimensional / 4
            - q * delta * p_dimensional / 2
            + q * eta * delta * previous_dimensional / 4
            + q**3 / 5
        )
        c_endpoint = endpoint - standard
        assert c_endpoint == delta * (
            -eta * sigma_dimensional / 4
            - q * p_dimensional / 4
            + q * eta * previous_dimensional / 8
            + q**3 / 20
        )
        d_endpoint = c_endpoint + q * eta * p_dimensional - q**3 / 5

        scale = delta ** (edge_count - 1)
        c_zero = Fraction(1, 10) - 3 * p_value / 8
        d_zero = p_value / 8 - Fraction(1, 10)
        e_value = (
            (p_value - previous_p) / 8 + q**2 * (previous_p / 8 - Fraction(1, 20)) - eta * zeta / 4
        )
        assert abs(e_value) < Fraction(1, 500)
        r_c = c_endpoint / q**3 - scale * c_zero
        r_d = d_endpoint / q**3 - scale * d_zero
        assert r_c == delta * e_value + (delta - scale) * c_zero
        assert r_d == (
            delta * e_value + p_value * (delta * (1 + 4 * q) - scale) / 8 - (q + 1 - scale) / 10
        )
        assert abs(r_c) < Fraction(7, 160)
        assert abs(r_d) < Fraction(1, 40)

        for step in range(1, edge_count):
            for target in range(edge_count + 1):
                h_value = directed_h_coefficient(edge_count, step, target)
                t_value = endpoint_tail(step, abs(target - edge_count))
                assert 0 <= h_value <= Fraction(1, 4)
                assert 0 <= t_value <= Fraction(1, 2)
                assert h_value * Fraction(7, 160) + t_value * Fraction(1, 40) <= Fraction(3, 128)
    print(
        "finite_stopped_endpoint=PASS m=64,96,128 "
        "frontier_recurrence=exact Rc<7/160 Rd<1/40 kernel_loss<3/128"
    )


def check_rational_ledger() -> None:
    q_max = Fraction(1, 1024)
    assert (
        2 + (Fraction(3, 2) + q_max / 2) * Fraction(33, 16) + Fraction(2, 5) + q_max / 5
        == Fraction(900293, 163840)
        < Fraction(11, 2)
    )
    assert Fraction(16 * 64, 2**62) < Fraction(1, 1024)
    assert (
        Fraction(1, 2048) + Fraction(1, 4194304) + Fraction(3, 2048)
        == Fraction(8193, 4194304)
        < Fraction(1, 500)
    )
    assert Fraction(1, 500) + Fraction(13, 320) == Fraction(341, 8000) < Fraction(7, 160)
    assert Fraction(3, 320) + Fraction(13, 20480) == Fraction(41, 4096)
    assert Fraction(1, 500) + Fraction(41, 4096) == Fraction(6149, 512000) < Fraction(1, 40)
    assert Fraction(7, 160) / 4 + Fraction(1, 40) / 2 == Fraction(3, 128)

    loss = Fraction(11, 720) + Fraction(3, 5120) + Fraction(43, 1200) + Fraction(3, 128)
    assert loss == Fraction(17311, 230400)
    assert Fraction(31, 320) - loss == Fraction(5009, 230400)
    final_margin = Fraction(15, 16) * Fraction(31, 320) - loss
    assert final_margin == Fraction(1807, 115200) > 0
    print(f"finite_stopped_rational_ledger=PASS loss={loss} margin={final_margin}")


def main() -> None:
    check_folded_source_kernels()
    check_base_response()
    check_endpoint_ledger()
    check_rational_ledger()
    print("terminal_finite_stopped_ledger=PASS static_late_target=OPEN")


if __name__ == "__main__":
    main()
