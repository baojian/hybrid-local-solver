#!/usr/bin/env python3
"""Exact scalar audit for the projected quartic and terminal-horizon theorems.

The proofs are symbolic.  This audit checks the quartic rational identities,
the first-admission energy minimization, the clipped-row reserve comparison,
and the terminal cap/threshold identities on a deterministic grid.  It is a
regression check, not the source of either graph-uniform theorem.
"""

from __future__ import annotations

from fractions import Fraction
from math import ceil, log


def constants(q: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    """Return ``a_q``, ``eta_q``, and the admission slope ``K_q``."""
    a_q = (1 + q * q) / 2
    eta_q = (1 - q * q) / 2
    k_q = 2 * a_q / (5 * eta_q)
    return a_q, eta_q, k_q


def audit_q(q: Fraction) -> int:
    """Check all exact inequalities at one rational parameter."""
    assert 0 < q < 1
    _, _, k_q = constants(q)
    c0 = k_q * k_q / ((1 + q * q) * (Fraction(1, 5) + k_q))
    closed_c0 = 4 * (1 + q * q) / (5 * (1 - q * q) * (3 + q * q))
    assert c0 == closed_c0
    assert c0 * (1 - q * q) > Fraction(1, 25)

    checked = 0
    for boundary_degree in range(1, 17):
        threshold = q * (Fraction(1, 5) + k_q * boundary_degree)
        # The proof minimizes over real x=1/d_s above this threshold.  Scan
        # every integer seed degree that satisfies the necessary admission
        # inequality and compare its actual singleton objective gap.
        for seed_degree in range(1, 257):
            x = Fraction(1, seed_degree)
            if x <= threshold:
                continue
            h_seed = q * q * (x - q / 5)
            objective_gap = seed_degree * h_seed * h_seed / (1 + q * q)
            assert objective_gap > c0 * q**5

            threshold_gap = (threshold - q / 5) ** 2 / threshold
            actual_gap = (x - q / 5) ** 2 / x
            factorized_difference = (x - threshold) * (1 - q * q / (25 * x * threshold))
            assert actual_gap - threshold_gap == factorized_difference > 0
            checked += 1

    # The first triggering step has R > c0 q^6.  The support-aware
    # coefficient then dominates the largest possible clipped-zero score.
    reserve_floor = c0 * q**6
    clipped_score_ceiling = q * q / 25
    coefficient = (1 - q * q) / q**4
    assert coefficient * reserve_floor > clipped_score_ceiling
    return checked


def audit_terminal_horizon(q: Fraction) -> int:
    """Check the exact scalar identities behind the complete-gate horizon."""
    assert 0 < q < 1
    q2 = q * q
    a_q = (1 + q2) / 2
    eta_q = (1 - q2) / 2
    assert a_q + eta_q == 1

    # The full-obstacle objective and singleton-center contributions are each
    # at most q^2/2.  The exact slack factorization is positive for q<1.
    energy_cap = q2 / 2 + 2 * q**6 / (1 + q2) ** 2
    scaled_slack = 2 * (1 + q2) ** 2 * (q2 - energy_cap) / q2
    assert scaled_slack == (1 - q2) * (1 + 3 * q2) > 0
    assert energy_cap < q2

    # At this energy threshold the envelope error is exactly at most
    # q^2 tau=q^3/5.
    gate_energy = q**12 / (50 * (1 + q2) ** 2)
    coordinate_error_squared = 2 * gate_energy / q2
    envelope_error_squared = (1 + 1 / q2) ** 2 * coordinate_error_squared
    assert envelope_error_squared == q**6 / 25

    ratio = float(q2 / gate_energy)
    hold_bound = ceil(log(ratio) / -log(float(1 - q)))
    assert float((1 - q) ** hold_bound * q2) <= float(gate_energy) * (1 + 1e-14)
    if hold_bound:
        assert float((1 - q) ** (hold_bound - 1) * q2) > float(gate_energy) * (1 - 1e-14)
    return 1


def main() -> None:
    q_values = (
        Fraction(1, 2),
        Fraction(1, 3),
        Fraction(1, 5),
        Fraction(1, 8),
        Fraction(1, 16),
        Fraction(12, 625),
        Fraction(1, 100),
        Fraction(1, 1000),
    )
    cells = sum(audit_q(q) for q in q_values)
    horizon_cells = sum(audit_terminal_horizon(q) for q in q_values)
    print(
        "original-score quartic and terminal-horizon scalar audit: "
        f"PASS ({cells} degree cells, {horizon_cells} horizon cells)"
    )


if __name__ == "__main__":
    main()
