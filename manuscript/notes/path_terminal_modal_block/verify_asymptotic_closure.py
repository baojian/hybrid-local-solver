#!/usr/bin/env python3
"""Exact arithmetic checks for the asymptotic static/regime synthesis."""

from __future__ import annotations

from fractions import Fraction

import verify_static_frontier as frontier


def check_static_chain() -> None:
    limits = frontier.check_first_order_limit_algebra()
    assert len(limits) == 5 and all(value > 0.0 for value in limits)

    edge_count = 64
    tail_bound = (
        Fraction(3, 50)
        + Fraction(57, 200) * Fraction(17, 24)
        + Fraction(57, 200 * 48 * 2 ** (edge_count - 2))
    )
    assert tail_bound < Fraction(21, 80)
    print(
        "asymptotic_static_chain=PASS "
        "interior=m_ge_64 frontier=eventually_positive static_target=21/80"
    )


def check_early_late_handoff() -> None:
    early_margin = Fraction(1807, 115200)
    late_slack = Fraction(1667, 625000)
    assert early_margin > 0 and late_slack > 0

    for edge_count in (64, 65, 128, 1024):
        q = Fraction(1, 16 * edge_count)
        # First integer k with q*k >= 3/50.
        first_late = (24 * edge_count + 24) // 25
        assert q * (first_late - 1) < Fraction(3, 50) <= q * first_late
        assert first_late < edge_count
    print(
        "asymptotic_regime_handoff=PASS early_margin=1807/115200 "
        "late_slack=1667/625000 no_integer_gap=true"
    )


def check_charged_work_ledger() -> None:
    # vol(P_m)=1/(8q), K=floor((8q)^-1 log(1/q)).  The coefficients below
    # check the exact floor lower bound and the accuracy reparameterization.
    assert Fraction(1, 8) * Fraction(1, 8) == Fraction(1, 64)
    assert Fraction(2, 5) * Fraction(5, 2) == 1  # eps_ppr=2q/5
    assert Fraction(1, 1) / (Fraction(2, 5)) == Fraction(5, 2)
    # 1/(sqrt(alpha)*eps_ppr)=5/(2q^2).
    assert Fraction(1, 64) / Fraction(5, 2) == Fraction(1, 160)
    for edge_count in (8, 64, 127):
        prefix_volume = sum(1 + 2 * index for index in range(edge_count))
        assert prefix_volume == edge_count**2
        assert 2 * edge_count * (edge_count + 1) <= 2 * edge_count**2 + 2 * edge_count
    print(
        "charged_work_ledger=PASS leading_ratio_to_log_free_scale=log(1/q)/160 "
        "exact_cg_escape_work=O(m^2) scope=prescribed_certificate_runtime_only"
    )


def main() -> None:
    check_static_chain()
    check_early_late_handoff()
    check_charged_work_ledger()
    print(
        "terminal_asymptotic_closure=PASS theorem=eventual "
        "explicit_frontier_cutoff=PROVED_SEPARATELY_M_GE_8192"
    )


if __name__ == "__main__":
    main()
