#!/usr/bin/env python3
"""Exact Round-028 audits for the cross-normalized window bank.

The checker verifies the modal PSD remainder, the full-reset constant, the
critical K2 trajectory, and the source claim boundary using exact rational
arithmetic.  It does not claim payment of mixed correction forcing, a moving-
face theorem, or an unconditional accelerated solver.
"""

from __future__ import annotations

from fractions import Fraction as F

from experiments.proof_audits import note_directory, note_tex_source


def modal_data(q: F, s: F) -> tuple[F, F, F, F]:
    """Return the direct PSD remainder entries and determinant."""
    assert 0 < q < 1 and 0 <= s <= 1
    theta = 1 - q
    alpha = q * q / (1 + q * q)
    kappa = (1 - q * q) / (1 + q * q)
    c = kappa + alpha
    lam = (q * q + s) / (1 + q * q)
    m = kappa / (kappa + lam)
    a = m / (1 + q)
    weight = c / lam
    r11 = theta - a * a - weight * (a - theta) ** 2
    r12 = -(a * a + weight * a * (a - theta))
    r22 = theta * weight - a * a - weight * a * a
    determinant = r11 * r22 - r12 * r12
    return r11, r12, r22, determinant


def check_modal_psd_remainder() -> None:
    """Match the displayed rational formulas and verify exact PSD signs."""
    for q in (F(1, 100), F(1, 20), F(1, 5), F(1, 2), F(4, 5)):
        for s in (F(0), F(1, 13), F(1, 2), F(1)):
            r11, r12, r22, determinant = modal_data(q, s)
            denominator = (q * q + s) * (1 + s) ** 2
            wanted_11 = (1 - q) * (
                q**3 + q * q * s * s + 2 * q * q * s + q * s * s
                + q * s + s**3 + s * s
            ) / denominator
            wanted_12 = -(q * q * (1 - q) ** 2) / denominator
            wanted_22 = (1 - q) * (
                q**3 - q * q + q * s + q + s * s + s
            ) / denominator
            wanted_det = (1 - q) ** 2 * (
                q**5 + 2 * q**3 * s + q * q * s * s + q * q * s
                + 2 * q * s * s + s**3
            ) / ((q * q + s) ** 2 * (1 + s) ** 2)
            assert (r11, r12, r22, determinant) == (
                wanted_11,
                wanted_12,
                wanted_22,
                wanted_det,
            )
            assert r11 >= 0 and r22 >= 0 and determinant >= 0


def check_full_reset_constant() -> None:
    """Verify the exact modal full-reset coefficient and its endpoint max."""
    for q in (F(1, 100), F(1, 20), F(1, 5), F(1, 2)):
        theta = 1 - q
        alpha = q * q / (1 + q * q)
        kappa = (1 - q * q) / (1 + q * q)
        c = kappa + alpha
        bound = theta * theta * (q * q + 2 * q + 2)
        endpoint = None
        for s in (F(0), F(1, 100), F(1, 13), F(1, 2), F(1)):
            lam = (q * q + s) / (1 + q * q)
            m = kappa / (kappa + lam)
            coefficient = m * m + c * (m - theta) ** 2 / lam
            assert coefficient <= bound < 2
            if s == 0:
                endpoint = coefficient
        assert endpoint == bound


def check_k2_critical_mode() -> None:
    """Check that the K2 critical mode contracts at the accelerated scale."""
    amplitude = F(7, 16)
    for q in (F(1, 100), F(1, 20), F(1, 5)):
        theta = 1 - q
        previous_bank = None
        for stage in range(1, 30):
            error = amplitude * (1 + stage * q) * theta**stage
            velocity = amplitude * q * theta**stage
            bank = error * error + velocity * velocity / (q * q)
            displayed = amplitude * amplitude * theta ** (2 * stage) * (
                (1 + stage * q) ** 2 + 1
            )
            assert bank == displayed
            if previous_bank is not None:
                assert bank <= theta * previous_bank
            previous_bank = bank


def check_forced_state_identity() -> None:
    """Verify that one correction adds the same Mr to e and u."""
    q = F(1, 7)
    theta = 1 - q
    m = F(5, 9)
    error = F(3, 5)
    velocity = F(2, 11)
    correction = F(1, 13)
    homogeneous_error = m * (error + velocity) / (1 + q)
    next_error = homogeneous_error + m * correction
    homogeneous_velocity = homogeneous_error - theta * error
    next_velocity = next_error - theta * error
    assert next_velocity == homogeneous_velocity + m * correction


def check_source_scope() -> None:
    """Guard theorem labels and the explicit non-overclaim boundary."""
    base = note_directory("aesp_cd_l1_rppr")
    main = note_tex_source("aesp_cd_l1_rppr")
    readme = (base / "README.md").read_text()
    status = (base / "STATUS.md").read_text()
    assert "prop:aesp-cd-cross-normalized-bank" in main
    assert "eq:aesp-cd-cross-normalized-forcing" in main
    assert "nonoptimal proper face" in main
    assert "mixed coordinate clipping" in main
    assert "cross-normalized" in readme
    assert "Q_A^-1" in status
    assert "No graph-uniform exact accelerated solver" in readme


def main() -> None:
    check_modal_psd_remainder()
    check_full_reset_constant()
    check_k2_critical_mode()
    check_forced_state_identity()
    check_source_scope()
    print("Round-028 exact cross-normalized window audit passed")
    print("  modal bank: one-step (1-q) contraction")
    print("  full reset: exact C0(q)<2 and Theta(1/q) window")
    print("  scope: mixed correction transfer remains open")


if __name__ == "__main__":
    main()
