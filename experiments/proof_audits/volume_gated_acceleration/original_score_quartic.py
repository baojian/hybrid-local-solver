#!/usr/bin/env python3
"""Exact scalar audit for the projected original-score quartic theorem.

The proof is symbolic.  This audit checks its rational identities, the
first-admission energy minimization, and the clipped-row reserve comparison on
a deterministic grid.  It is a regression check, not the source of the
graph-uniform theorem.
"""

from __future__ import annotations

from fractions import Fraction


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
    print(f"original-score quartic scalar audit: PASS ({cells} degree cells)")


if __name__ == "__main__":
    main()
