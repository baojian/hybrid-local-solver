#!/usr/bin/env python3
"""Exact Round-027 audits for the weighted-reserve proof boundary.

All trajectory, reserve, and stress-family arithmetic uses ``Fraction``.
The checker verifies the lagged energy indexing that pays the actual stage
defect, the reachable pre-gate K2 trajectory, the two-family stagewise STOP,
and the surviving K8 high-band payment.  It does not claim the open windowed
spectral transfer, the finite net exponent, or an unconditional solver vector.
"""

from __future__ import annotations

from fractions import Fraction as F
from experiments.proof_audits import note_directory, note_tex_source


Vector = list[F]
A_STAR = F(6_929_307, 98_509_850)


def dot(left: Vector, right: Vector) -> F:
    """Return an exact Euclidean inner product."""
    return sum((a * b for a, b in zip(left, right)), F(0))


def check_q_weighted_euclidean_reserve() -> None:
    """Check the exact reserve identity, defect payment, and q^2 drift."""
    for q in (F(1, 100), F(1, 20), F(1, 10)):
        a_q = (1 - q) / q
        mu = F(7, 13)
        current_error = [F(2, 5), F(1, 3), F(1, 7)]
        displacement = [F(1, 100), F(1, 80), F(1, 120)]
        previous_error = [error + step for error, step in zip(current_error, displacement)]
        correction = [
            a_q * displacement[0] / 4,
            a_q * displacement[1] / 3,
            a_q * displacement[2] / 2,
        ]
        assert all(0 <= value <= a_q * step for value, step in zip(correction, displacement))

        momentum_error = [error - a_q * step for error, step in zip(current_error, displacement)]
        corrected_error = [value + extra for value, extra in zip(momentum_error, correction)]
        defect = dot(corrected_error, corrected_error) - dot(momentum_error, momentum_error)
        error_drop = dot(previous_error, previous_error) - dot(current_error, current_error)
        assert defect <= a_q * error_drop

        finite_momentum = [-value for value in momentum_error]
        identity_rhs = [
            (error + q * momentum) / (1 - q)
            for error, momentum in zip(current_error, finite_momentum)
        ]
        assert identity_rhs == previous_error

        omega = (1 - q) ** 2 * mu / (2 * q)
        assert omega == (1 - q) * mu * a_q / 2
        phi_lower = (
            mu * (dot(current_error, current_error) + dot(finite_momentum, finite_momentum)) / 2
        )
        reserve = omega * dot(previous_error, previous_error)
        assert reserve <= (1 + q * q) * phi_lower / q

        comparison = (1 + q + q * q) / q
        drift = q / comparison
        assert drift == q * q / (1 + q + q * q)


def k2_quantities(q: F, stage: int) -> tuple[F, F, F]:
    """Return normalized K2 error amplitude, Phi/S, and Q-energy/S."""
    alpha = q * q / (1 + q * q)
    kappa = (1 - q * q) / (1 + q * q)
    mu = kappa * q * q
    decay = (1 + stage * q) * (1 - q) ** stage
    momentum_decay = (1 - q) ** stage
    phi_over_s = mu * (decay * decay + momentum_decay * momentum_decay) / 2
    energy_over_s = alpha * decay * decay
    return decay, phi_over_s, energy_over_s


def check_k2_reachable_pre_gate() -> None:
    """Check the exact recurrence and the gate at the trial center ell_t."""
    rho = tau = F(1, 16)
    optimum = F(1, 2) - rho
    assert optimum == F(7, 16)

    for n in (100, 101, 200, 1000):
        q = F(1, n)
        alpha = q * q / (1 + q * q)
        kappa = (1 - q * q) / (1 + q * q)
        beta = (1 - q) / (1 + q)
        mapping = kappa / (kappa + alpha)
        assert mapping == 1 - q * q

        previous_error = optimum
        current_error = optimum
        for stage in range(n + 1):
            expected = optimum * (1 + stage * q) * (1 - q) ** stage
            assert current_error == expected
            if stage >= 1:
                assert optimum - current_error > 0

            trial_error = (1 + beta) * current_error - beta * previous_error
            displayed_trial = optimum * (1 + (stage + 1) * q) * (1 - q) ** stage / (1 + q)
            assert trial_error == displayed_trial > optimum / 4 > tau
            assert alpha * trial_error > alpha * tau
            if stage == n:
                break

            next_error = mapping * trial_error
            previous_error, current_error = current_error, next_error

        assert (1 - q) ** n >= F(1, 4)


def lagged_psi(q: F, coefficient: F, stage: int) -> F:
    """Return Psi_t/S=Phi_t/S+(A/q)E_(t-1)/S for t>=1."""
    assert stage >= 1
    _, phi, _ = k2_quantities(q, stage)
    _, _, previous_energy = k2_quantities(q, stage - 1)
    return phi + coefficient * previous_energy / q


def check_unsplit_floor_and_lagged_stop() -> None:
    """Audit the K8 coefficient floor and the lagged K2 O(q^2) loss."""
    q_max = F(1, 100)
    kappa_min = (1 - q_max * q_max) / (1 + q_max * q_max)
    assert 14 * (1 - q_max) * kappa_min / 197 == A_STAR

    for n in (100, 101, 200, 1000, 10_000):
        q = F(1, n)
        b_q = (1 - q * q) / 2
        for coefficient in (A_STAR, F(1), F(10)):
            ratio = lagged_psi(q, coefficient, 3) / lagged_psi(q, coefficient, 2)
            displayed = (
                (1 - q) ** 2
                * (b_q * (1 - q) ** 2 * ((1 + 3 * q) ** 2 + 1) + coefficient * (1 + 2 * q) ** 2 / q)
            ) / (b_q * (1 - q) ** 2 * ((1 + 2 * q) ** 2 + 1) + coefficient * (1 + q) ** 2 / q)
            assert ratio == displayed

            _, phi_2, energy_2 = k2_quantities(q, 2)
            _, phi_3, _ = k2_quantities(q, 3)
            _, _, energy_1 = k2_quantities(q, 1)
            phi_weight = phi_2 / (phi_2 + coefficient * energy_1 / q)
            assert 0 <= 1 - phi_3 / phi_2 <= 2 * q
            assert 0 <= 1 - energy_2 / energy_1 <= 4 * q * q
            assert phi_weight <= q / coefficient
            assert 0 <= 1 - ratio <= (4 + 2 / A_STAR) * q * q


def check_k2_global_non_obstruction() -> None:
    """Check the rational part of the lagged all-time normalization bound."""
    # For u>=0, calculus gives exp(-u)(1+u)^2<=4/e.  The checks
    # below verify the exact rational precursor for both bank components.
    for n in (100, 101, 200):
        q = F(1, n)
        _, phi_0, energy_0 = k2_quantities(q, 0)
        for stage in (1, 2, n // 2, n, 2 * n, 10 * n):
            _, phi_t, _ = k2_quantities(q, stage)
            _, phi_1, _ = k2_quantities(q, 1)
            _, _, energy_previous = k2_quantities(q, stage - 1)
            u = (stage - 1) * q
            rational_envelope = (1 - q) ** (2 * (stage - 1)) * (1 + u) ** 2
            assert phi_t / phi_1 <= rational_envelope
            assert energy_previous / energy_0 == rational_envelope

        for coefficient in (A_STAR, F(1), F(10)):
            psi_one = lagged_psi(q, coefficient, 1)
            assert psi_one / phi_0 <= 1 + coefficient / (q * (1 - q * q))
            for stage in (1, 2, n // 2, n, 2 * n, 10 * n):
                u = (stage - 1) * q
                rational_envelope = (1 - q) ** (2 * (stage - 1)) * (1 + u) ** 2
                assert lagged_psi(q, coefficient, stage) / psi_one <= rational_envelope


def high_band_data(q: F) -> tuple[F, F, F]:
    """Return scaled K8 defect, high-band drop, and payment ratio."""
    alpha = q * q / (1 + q * q)
    kappa = (1 - q * q) / (1 + q * q)
    lambda_h = (4 + 3 * alpha) / 7
    m_h = 7 * (1 - q * q) / 11
    s_h = (1 - q) * (3 + 14 * q) / (11 * (1 + q))
    assert m_h == kappa / (kappa + lambda_h)

    high_error_2 = 12 * q * q * m_h * s_h
    high_shift = 12 * q * (1 - q) * m_h * (1 - s_h)
    defect = 32 * q * (1 - q) ** 4 * (1 + q)
    defect += F(8, 7) * (2 * high_error_2 * high_shift - high_shift * high_shift)
    high_drop = F(8, 7) * lambda_h * (12 * q * q * m_h) ** 2 * (1 - s_h * s_h)
    ratio = (1 - q) * kappa * q**3 * defect / (2 * high_drop)
    return defect, high_drop, ratio


def check_k8_high_band_limit() -> None:
    """Audit the exact high-band compatibility constants and samples."""
    high_drop_limit = F(8, 7) * F(4, 7) * 144 * F(7, 11) ** 2 * (1 - F(3, 11) ** 2)
    assert high_drop_limit == F(516_096, 14_641)
    payment_limit = 16 / high_drop_limit
    assert payment_limit == F(14_641, 32_256)

    expected = {
        100: F(7_404_350_273_085_253_653, 17_098_214_209_400_000_000),
        101: F(5_444_820_503_251_812_500_000, 12_567_354_408_526_150_519_831),
        200: F(10_250_734_027_824_595_021_623_943, 23_119_273_363_671_862_400_000_000),
        1000: F(
            76_152_202_964_659_466_767_563_293_853,
            168_559_399_873_706_294_000_000_000_000,
        ),
    }
    previous = F(0)
    for n, wanted in expected.items():
        defect, high_drop, ratio = high_band_data(F(1, n))
        assert defect > 0 and high_drop > 0
        assert ratio == wanted
        assert previous < ratio < payment_limit
        previous = ratio


def check_source_scope() -> None:
    """Guard stable labels, lagged indexing, gate scope, and non-overclaims."""
    base = note_directory("aesp_cd_l1_rppr")
    main = note_tex_source("aesp_cd_l1_rppr")
    readme = (base / "README.md").read_text()
    status = (base / "STATUS.md").read_text()
    assert "lem:aesp-cd-q-weighted-euclidean-reserve" in main
    assert "prop:aesp-cd-unsplit-q-energy-stagewise-stop" in main
    assert r"\mathfrak E_{t-1}^Q" in main
    assert r"\Psi_3^A" in main
    assert r"x^\star-\ell_t" in main
    assert "does not provide the windowed" in main
    assert "weighted_reserve_boundary" in readme
    assert "windowed spectral, nonlinear" in status
    assert "No graph-uniform exact accelerated solver" in readme


def main() -> None:
    check_q_weighted_euclidean_reserve()
    check_k2_reachable_pre_gate()
    check_unsplit_floor_and_lagged_stop()
    check_k2_global_non_obstruction()
    check_k8_high_band_limit()
    check_source_scope()
    print("Round-027 exact weighted-reserve audit passed")
    print("  Euclidean reserve: exact monotonicity with only q^2 drift")
    print("  lagged unsplit bank: K8 payment and K2 one-step STOP")
    print("  scope: no net/additive-B obstruction; spectral windows remain open")


if __name__ == "__main__":
    main()
