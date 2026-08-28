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
            wanted_11 = (
                (1 - q)
                * (q**3 + q * q * s * s + 2 * q * q * s + q * s * s + q * s + s**3 + s * s)
                / denominator
            )
            wanted_12 = -(q * q * (1 - q) ** 2) / denominator
            wanted_22 = (1 - q) * (q**3 - q * q + q * s + q + s * s + s) / denominator
            wanted_det = (
                (1 - q) ** 2
                * (q**5 + 2 * q**3 * s + q * q * s * s + q * q * s + 2 * q * s * s + s**3)
                / ((q * q + s) ** 2 * (1 + s) ** 2)
            )
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
            displayed = amplitude * amplitude * theta ** (2 * stage) * ((1 + stage * q) ** 2 + 1)
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


def check_contract_or_spend_endpoint() -> None:
    """Verify the exact low-endpoint normalizer in the spend corollary."""
    for q in (F(1, 100), F(1, 20), F(1, 5), F(1, 2)):
        alpha = q * q / (1 + q * q)
        kappa = (1 - q * q) / (1 + q * q)
        mu = kappa * q * q
        c = kappa + alpha
        m0 = 1 - q * q
        previous = None
        for s in (F(0), F(1, 100), F(1, 13), F(1, 2), F(1)):
            lam = (q * q + s) / (1 + q * q)
            mode = kappa / (kappa + lam)
            kernel = mode * mode * (1 + c / lam)
            assert mu * kernel <= m0**3
            if previous is not None:
                assert kernel < previous
            previous = kernel
            if s == 0:
                assert mu * kernel == m0**3


def check_moreau_event_kernel() -> None:
    """Verify the bounded Moreau forcing metric and the raw face shock."""
    for q in (F(1, 100), F(1, 20), F(1, 5), F(1, 2)):
        alpha = q * q / (1 + q * q)
        kappa = (1 - q * q) / (1 + q * q)
        m0 = 1 - q * q
        previous = None
        endpoint = None
        for s in (F(0), F(1, 100), F(1, 13), F(1, 2), F(1)):
            lam = (q * q + s) / (1 + q * q)
            mode = kappa / (kappa + lam)
            kernel = kappa * mode * mode + alpha * mode**3
            assert kernel <= m0**3
            if previous is not None:
                assert kernel < previous
            previous = kernel
            if s == 1:
                endpoint = kernel
        assert endpoint == m0**3 * (2 + q * q) / (8 * (1 + q * q))

    q = F(1, 100)
    m0 = 1 - q * q
    singleton_diagonal = F(2, 3) * m0
    full_diagonal = F(3, 4) * m0
    assert singleton_diagonal == F(3333, 5000)
    assert full_diagonal == F(29997, 40000)
    assert full_diagonal / singleton_diagonal == F(9, 8)


def kn_cross_data(n: int) -> tuple[F, F, F]:
    """Return the exact K_N full/preceding and low/initial-high ratios."""
    q = F(1, 100)
    alpha = q * q / (1 + q * q)
    kappa = (1 - q * q) / (1 + q * q)
    mu = kappa * q * q
    beta = (1 - q) / (1 + q)
    c = kappa + alpha
    m0 = 1 - q * q
    amplitude = F(12)
    k = n - 1
    a0 = F(1, 2 * n * k)
    lam = F(n + (n - 2) * alpha, 2 * k)
    mh = kappa / (kappa + lam)
    s0 = (1 - q) * (1 + 2 * q) / (1 + q)
    sh = (1 + beta) * mh - beta

    # Exact positivity and chronology inequalities used in the proof.
    assert amplitude * lam * (1 + q * q) < k
    assert amplitude * lam / (kappa * k) < 1
    assert 3 - 2 * q > amplitude / k
    assert s0 / (1 + q * q) - amplitude * lam * sh / k > 0
    t0 = (1 + beta) * s0 - beta
    th = (1 + beta) * sh - beta
    fh = -lam * mh * th
    l0 = m0 * t0 / (1 + q * q)
    assert th < 0 and fh > F(9, 100)
    assert amplitude * fh - l0 > F(2, 25)
    cap = a0 * m0 * (amplitude * fh - l0)
    assert cap > F(79, 1000) * a0

    e1_low = a0 * m0
    e2_low = e1_low * s0
    u2_low = e2_low - (1 - q) * e1_low
    e1_high = a0 * amplitude * q * q * mh
    e2_high = e1_high * sh
    u2_high = e2_high - (1 - q) * e1_high
    moreau_bank_2 = n * (alpha * m0 * e2_low * e2_low + c * m0 * u2_low * u2_low)
    moreau_bank_2 += F(n, k) * (lam * mh * e2_high * e2_high + c * mh * u2_high * u2_high)

    r_low = beta * m0 * (1 - s0) * a0
    r_high = beta * amplitude * q * q * mh * (1 - sh) * a0
    assert r_low + r_high < a0 * q * q * (2 + amplitude)
    correction_norm = n * r_low * r_low + F(n, k) * r_high * r_high
    assert m0**3 * correction_norm / (q * moreau_bank_2) < F(1, 16)
    forcing = n * m0 * m0 * (1 + c / alpha) * r_low * r_low
    forcing += F(n, k) * mh * mh * (1 + c / lam) * r_high * r_high
    preceding_high_drop = F(n, k) * lam * (amplitude * q * q * mh * a0) ** 2 * (1 - sh * sh)
    full_ratio = mu * forcing / preceding_high_drop

    low_forcing = 4 * n * a0 * a0 * q**4 * m0 * (1 - q) ** 6
    initial_high = F(n, k) * lam * amplitude * amplitude * q**4 * a0 * a0
    global_ratio = low_forcing / initial_high
    displayed = 4 * k * m0 * (1 - q) ** 6 / (lam * amplitude * amplitude)
    assert global_ratio == displayed > F(k, 23)
    return full_ratio, global_ratio, cap


def check_kn_high_drop_stop() -> None:
    """Check the reachable complete-graph high-drop-only obstruction."""
    expected = {
        8: F(73_387_864_081_058_649_690_843, 85_491_071_047_000_000_000_000),
        12: F(
            161_030_072_622_852_958_763_160_029_349,
            116_243_846_625_372_641_000_000_000_000,
        ),
        20: F(
            3_968_141_818_754_077_651_395_627_573_501,
            1_622_745_677_658_664_481_000_000_000_000,
        ),
    }
    for n in [*range(8, 301), 1000]:
        full_ratio, global_ratio, cap = kn_cross_data(n)
        assert full_ratio > 0 and global_ratio > 0 and cap > 0
        if n in expected:
            assert full_ratio == expected[n]
    assert expected[8] < 1 < expected[12]


def check_source_scope() -> None:
    """Guard theorem labels and the explicit non-overclaim boundary."""
    base = note_directory("aesp_cd_l1_rppr")
    main = note_tex_source("aesp_cd_l1_rppr")
    readme = (base / "README.md").read_text()
    status = (base / "STATUS.md").read_text()
    assert "prop:aesp-cd-cross-normalized-bank" in main
    assert "eq:aesp-cd-cross-normalized-forcing" in main
    assert "prop:aesp-cd-kn-cross-bank-stop" in main
    assert "prop:aesp-cd-cross-normalized-contract-spend" in main
    assert "eq:aesp-cd-cross-normalized-low-spend" in main
    assert "prop:aesp-cd-moreau-epoch-restart" in main
    assert "eq:aesp-cd-moreau-epoch-net" in main
    assert "nonoptimal proper face" in main
    assert "high-drop-only payment" in main
    assert "cross-normalized" in readme
    assert "Q_A^-1" in status
    assert "No graph-uniform exact accelerated solver" in readme


def main() -> None:
    check_modal_psd_remainder()
    check_full_reset_constant()
    check_k2_critical_mode()
    check_forced_state_identity()
    check_contract_or_spend_endpoint()
    check_moreau_event_kernel()
    check_kn_high_drop_stop()
    check_source_scope()
    print("Round-028 exact cross-normalized window audit passed")
    print("  modal bank: one-step (1-q) contraction")
    print("  full reset: exact C0(q)<2 and Theta(1/q) window")
    print("  K_N: high-drop-only correction payment has Omega(N) loss")
    print("  contract-or-spend: exact low Euclidean endpoint normalizer")
    print("  Moreau epoch bank: bounded forcing metric and exact K2 face shock")
    print("  scope: changing-face finite-inner restart transfer remains open")


if __name__ == "__main__":
    main()
