#!/usr/bin/env python3
"""Exact Round-025 audits for boundary shielding and post-full filtering.

All identities and inequalities use ``Fraction``.  The checker verifies the
finite support-entry bound, the one-sided same-state correction comparison,
the exact ``4 delta q`` pre-gate constant, the post-full scalar filter, and
the mixed-mode K8 stress test.  It does not claim the open persistent-row net
packing theorem.
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path


Vector = list[F]
Matrix = list[list[F]]


def positive(value: F) -> F:
    """Return the positive part of an exact scalar."""
    return max(F(0), value)


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    """Return an exact matrix-vector product."""
    return [sum((entry * value for entry, value in zip(row, vector)), F(0)) for row in matrix]


def check_support_entry_shield() -> None:
    """Verify the universal new-row collapse inequality on exact samples."""
    kappa = F(7, 8)
    beta = F(3, 4)
    samples = (
        (F(1, 9), F(0), F(0), F(0)),
        (F(1, 9), F(1, 50), F(1, 60), F(1, 70)),
        (F(1, 100), F(1, 20), F(0), F(1, 30)),
    )
    entry_values: Vector = []
    previous_values: Vector = []
    for current_step, previous_residual, current_residual, previous_multiplier in samples:
        collapse = positive(
            -(1 + beta) * kappa * current_step
            + beta * previous_residual
            - (1 + beta) * current_residual
            - beta * previous_multiplier
        )
        assert collapse <= beta * previous_residual
        entry_values.append(collapse)
        previous_values.append(previous_residual)

    entry_maximum = max(entry_values)
    persistent_maximum = F(1, 1000)
    end_mass = sum(previous_values, F(0))
    assert entry_maximum <= beta * max(previous_values)
    assert entry_maximum <= beta * end_mass
    assert max(entry_maximum, persistent_maximum) >= entry_maximum

    # Exact solves have no positive end residual on the preceding stage.
    exact_entry = positive(-(1 + beta) * kappa * F(1, 9))
    assert exact_entry == 0


def check_one_sided_correction_excess() -> None:
    """Verify finite residuals can only add the stated one-sided excess."""
    alpha = F(1, 26)
    kappa = F(12, 13)
    beta = F(2, 3)
    driver = [F(1, 30), F(-1, 40), F(1, 50), F(-1, 60)]
    previous_residual = [F(1, 400), F(1, 500), F(1, 600), F(1, 700)]
    current_residual = [F(0), F(1, 1000), F(0), F(1, 1100)]
    previous_multiplier = [F(1, 800), F(0), F(1, 900), F(0)]
    caps = [F(1, 4), F(1, 5), F(1, 6), F(1, 7)]

    finite_collapse = [
        positive(
            kappa * value + beta * old_residual - (1 + beta) * new_residual - beta * multiplier
        )
        for value, old_residual, new_residual, multiplier in zip(
            driver,
            previous_residual,
            current_residual,
            previous_multiplier,
        )
    ]
    delta = max(finite_collapse) / alpha
    bar_delta = kappa * max(positive(value) for value in driver) / alpha
    residual_delta = beta * max(previous_residual) / alpha
    assert delta <= bar_delta + residual_delta

    correction = [min(cap, delta) for cap in caps]
    bar_correction = [min(cap, bar_delta) for cap in caps]
    for actual, residual_free in zip(correction, bar_correction):
        assert positive(actual - residual_free) <= residual_delta

    # A perfect-square volume keeps the exact l2 bound rational.
    volume = F(4)
    sqrt_volume = F(2)
    mu = alpha + kappa
    xi = F(1, 100)
    end_mass_target = mu * xi / sqrt_volume
    residual_delta_from_stop = beta * end_mass_target / alpha
    l2_positive_excess = residual_delta_from_stop * sqrt_volume
    assert l2_positive_excess == beta * mu * xi / alpha

    q = F(1, 5)
    momentum_excess = (1 + q) * l2_positive_excess / q
    assert momentum_excess == (1 - q) * mu * xi / (q * alpha)
    assert volume == sqrt_volume * sqrt_volume


def check_entry_inflation_constant() -> None:
    """Audit the exact algebra behind the 4 delta q pre-gate charge."""
    q = F(1, 10)
    alpha = q * q / (1 + q * q)
    beta = (1 - q) / (1 + q)
    c_q = (1 + q) / q
    tolerance = F(1, 2)
    eta_gate = 2 * alpha * tolerance / (1 + alpha)
    ledger_delta = F(1, 100)
    end_mass = ledger_delta * alpha * eta_gate * eta_gate * q * q

    retraction = beta * end_mass / alpha
    momentum_correction = c_q * retraction
    error_mass = F(1)
    defect_upper = 2 * error_mass * momentum_correction
    normalized_inflation_upper = defect_upper / (eta_gate * eta_gate)
    assert normalized_inflation_upper == 2 * c_q * beta * ledger_delta * q * q
    assert normalized_inflation_upper <= 4 * ledger_delta * q

    # The exact defect is smaller because 0 <= h <= a_q d.
    a_q = (1 - q) / q
    displacement = momentum_correction / a_q
    exact_defect = (
        momentum_correction * momentum_correction
        + 2 * error_mass * momentum_correction
        - 2 * a_q * displacement * momentum_correction
    )
    assert exact_defect <= defect_upper


def filter_coefficient(lam: F, kappa: F, sigma: F) -> F:
    """Return the exact two-stage post-full scalar filter coefficient."""
    return lam * (sigma * lam - kappa) / (kappa + lam) ** 2


def check_post_full_filter() -> None:
    """Verify the modal formula, threshold, and mixed K8 stress test."""
    for q, lam in ((F(1, 10), F(1, 101)), (F(1, 10), F(407, 707)), (F(1, 5), F(3, 5))):
        alpha = q * q / (1 + q * q)
        kappa = 1 - 2 * alpha
        beta = (1 - q) / (1 + q)
        sigma = beta * (2 + beta)
        mapping = kappa / (kappa + lam)
        separation = (1 + beta) * mapping - beta
        first_step = 1 - mapping
        second_step = (1 - mapping) * separation
        collapse = beta * first_step - (1 + beta) * second_step
        assert collapse == filter_coefficient(lam, kappa, sigma)
        assert (collapse > 0) == (lam / kappa > 1 / sigma)
        assert 1 / sigma == (1 + q) ** 2 / ((1 - q) * (3 + q))

    # Exact K8 mixed-mode witness from the note.
    q = F(1, 10)
    alpha = F(1, 101)
    kappa = F(99, 101)
    beta = F(9, 11)
    sigma = F(279, 121)
    size = 8
    high_eigenvalue = F(407, 707)
    diagonal = (1 + alpha) / 2
    off_diagonal = -(1 - alpha) / (2 * (size - 1))
    matrix = [[diagonal if i == j else off_diagonal for j in range(size)] for i in range(size)]
    error = [F(5693, 5000), *([F(1)] * (size - 1))]
    qe = matvec(matrix, error)
    assert qe[0] == F(40343, 505000)
    assert qe[1:] == [F(1, 10100)] * (size - 1)
    assert all(value > 0 for value in qe)

    mean = sum(error, F(0)) / size
    constant_coefficient = filter_coefficient(alpha, kappa, sigma)
    high_coefficient = filter_coefficient(high_eigenvalue, kappa, sigma)
    filtered = [constant_coefficient * mean + high_coefficient * (value - mean) for value in error]
    assert constant_coefficient == F(-117, 12100)
    assert high_coefficient == F(999, 12100)
    assert filtered[0] == F(21267, 121000000) > 0
    assert filtered[1:] == [F(-1363347, 121000000)] * (size - 1)


def check_source_guardrails() -> None:
    """Keep the package attached to its deliberately incomplete scope."""
    directory = Path(__file__).resolve().parent
    main_text = (directory / "main.tex").read_text(encoding="utf-8")
    readme_text = (directory / "README.md").read_text(encoding="utf-8")
    status_text = (directory / "STATUS.md").read_text(encoding="utf-8")
    for anchor in (
        "lem:aesp-cd-support-entry-shield",
        "lem:aesp-cd-one-sided-correction-excess",
        "cor:aesp-cd-entry-inflation-ledger",
        "prop:aesp-cd-post-full-high-pass",
        "eq:aesp-cd-post-full-k8-mixing",
    ):
        assert anchor in main_text
    combined = " ".join((main_text + " " + readme_text + " " + status_text).split())
    for required_scope in (
        "entry-dominated",
        "persistent-row",
        "one-sided",
        "not a graph-uniform two-step separation",
        "does not prove finite net packing",
    ):
        assert required_scope in combined
    assert "graph-uniform net exponent" in combined
    assert "not a claimed reachable outer state" in combined


def main() -> None:
    check_support_entry_shield()
    check_one_sided_correction_excess()
    check_entry_inflation_constant()
    check_post_full_filter()
    check_source_guardrails()
    print("Round-025 exact boundary/filter audit passed")
    print("  support entries: exact zero; finite contribution is previous-residual-only")
    print("  finite correction: same-state excess is one-sided and polynomial")
    print("  pre-gate entry ledger: at most 4 delta q per entry-dominated stage")
    print("  post-full window: exact high-pass filter; K8 mixed-mode caveat retained")
    print("  scope: persistent-row low-Dirichlet net exponent remains open")


if __name__ == "__main__":
    main()
