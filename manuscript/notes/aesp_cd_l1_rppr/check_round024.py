#!/usr/bin/env python3
"""Exact Round-024 audits for retraction stability and fixed-face structure.

All branch decisions and matrix identities below use ``Fraction``.  The
checker certifies the P2 discontinuity/amplification examples, one exact
full-correction separation instance, its finite residual bound, and the
high-Dirichlet scalar contraction.  It does not claim the open low-Dirichlet
net exponent.
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path


Vector = list[F]
Matrix = list[list[F]]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    """Return an exact matrix-vector product."""
    return [sum((a * b for a, b in zip(row, vector)), F(0)) for row in matrix]


def add(left: Vector, right: Vector) -> Vector:
    """Return the sum of two vectors."""
    return [a + b for a, b in zip(left, right)]


def scale(factor: F, vector: Vector) -> Vector:
    """Return a scaled vector."""
    return [factor * value for value in vector]


def inverse_two(matrix: Matrix) -> Matrix:
    """Invert a nonsingular symmetric two-by-two matrix exactly."""
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    assert determinant
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def multiply(left: Matrix, right: Matrix) -> Matrix:
    """Return an exact matrix product."""
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    """Return an exact matrix sum."""
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def matrix_scale(factor: F, matrix: Matrix) -> Matrix:
    """Return an exact scaled matrix."""
    return [[factor * value for value in row] for row in matrix]


def identity(size: int) -> Matrix:
    """Return an exact identity matrix."""
    return [[F(i == j) for j in range(size)] for i in range(size)]


def p2_data(alpha: F) -> tuple[F, F, F, Matrix, Vector]:
    """Return the P2 coefficients used by the retraction proposition."""
    lam = (1 + alpha) / 2
    nu = (1 - alpha) / 2
    rho = nu / 4
    matrix = [[lam, -nu], [-nu, lam]]
    load = [alpha * (1 - rho), -alpha * rho]
    return lam, nu, rho, matrix, load


def retract(alpha: F, matrix: Matrix, load: Vector, point: Vector) -> tuple[Vector, F, int | None]:
    """Apply the support-indexed P2 lower retraction exactly."""
    residual = [a - b for a, b in zip(load, matvec(matrix, point))]
    support = [index for index, value in enumerate(point) if value]
    row_values = {index: -residual[index] / alpha for index in support}
    delta = max([F(0), *row_values.values()])
    controllers = [index for index, value in row_values.items() if value == delta and delta > 0]
    controller = controllers[0] if len(controllers) == 1 else None
    return [max(F(0), value - delta) for value in point], delta, controller


def check_retraction_stop() -> None:
    """Verify discontinuity and sharp fixed-support amplification."""
    for alpha in (F(1, 5), F(1, 10), F(1, 100)):
        lam, nu, rho, matrix, load = p2_data(alpha)

        point = [alpha / 8, F(0)]
        eta = alpha * nu / 100
        entered = [alpha / 8, eta]
        lower, delta, controller = retract(alpha, matrix, load, point)
        entered_lower, entered_delta, entered_controller = retract(alpha, matrix, load, entered)
        assert lower == point
        assert delta == 0 and controller is None
        assert entered_delta == nu / 8 + lam * eta / alpha
        assert entered_controller == 1
        assert entered_lower == [F(0), F(0)]

        base = [lam / 2, nu / 2]
        epsilon = alpha * nu / 8
        perturbed = [base[0] + epsilon, base[1] - epsilon]
        base_lower, base_delta, base_controller = retract(alpha, matrix, load, base)
        perturbed_lower, perturbed_delta, perturbed_controller = retract(
            alpha, matrix, load, perturbed
        )
        assert rho == nu / 4
        assert base_delta == rho and base_controller == 1
        assert perturbed_delta == rho - epsilon / alpha
        assert perturbed_controller == 1
        assert all(value > 0 for value in base_lower + perturbed_lower)
        difference = [b - a for a, b in zip(base_lower, perturbed_lower)]
        assert max(abs(value) for value in difference) == (1 + 1 / alpha) * epsilon


def check_full_correction_separation() -> None:
    """Verify the exact fixed-face map and finite adjacent bound on P2."""
    q = F(1, 5)
    alpha = q * q / (1 + q * q)
    kappa = (1 - q * q) / (1 + q * q)
    beta = (1 - q) / (1 + q)
    lam = (1 + alpha) / 2
    nu = (1 - alpha) / 2
    matrix = [[lam, -nu], [-nu, lam]]
    shifted = matrix_add(matrix, matrix_scale(kappa, identity(2)))
    shifted_inverse = inverse_two(shifted)
    mapping = matrix_scale(kappa, shifted_inverse)
    separation = matrix_add(matrix_scale(1 + beta, mapping), matrix_scale(-beta, identity(2)))

    # Entrywise positivity, commutation, and the exact spectral lower bound.
    assert all(value >= 0 for row in separation for value in row)
    shifted_separation = matrix_add(separation, matrix_scale(-q * beta, identity(2)))
    assert shifted_separation[0][0] >= 0
    assert (
        shifted_separation[0][0] * shifted_separation[1][1]
        - shifted_separation[0][1] * shifted_separation[1][0]
        >= 0
    )
    assert multiply(separation, matrix) == multiply(matrix, separation)

    error = [F(1), F(1)]
    assert all(value >= 0 for value in matvec(matrix, error))
    next_trial_error = matvec(separation, error)
    assert all(value >= 0 for value in matvec(matrix, next_trial_error))

    # A finite end residual can create only the bounded adjacent correction.
    end_residual = [F(0), F(1, 100)]
    finite_error = add(
        next_trial_error,
        scale(1 + beta, matvec(shifted_inverse, end_residual)),
    )
    trial_residual = matvec(matrix, finite_error)
    delta = max(F(0), *(-value / alpha for value in trial_residual))
    bound = 2 * (1 - q) * max(end_residual) / alpha
    assert delta <= bound


def check_high_dirichlet_branch() -> None:
    """Verify the scalar direct-contraction and finite-error recursion."""
    q = F(1, 8)
    alpha = q * q / (1 + q * q)
    kappa = (1 - q * q) / (1 + q * q)
    face_eigenvalue = (1 + alpha) / 2
    theta = face_eigenvalue / (kappa + face_eigenvalue)
    exact_factor = kappa / (kappa + face_eigenvalue)
    assert exact_factor == 1 - theta
    center_error = F(3, 4)
    current_error = F(4, 5)
    finite_error = F(1, 1000)
    next_error = exact_factor * center_error + finite_error
    assert center_error <= current_error
    assert next_error <= (1 - theta) * current_error + finite_error
    assert theta > q


def check_source_guardrails() -> None:
    """Keep the new theorems attached to their deliberately narrow scopes."""
    directory = Path(__file__).resolve().parent
    main_text = (directory / "main.tex").read_text(encoding="utf-8")
    readme_text = (directory / "README.md").read_text(encoding="utf-8")
    status_text = (directory / "STATUS.md").read_text(encoding="utf-8")
    for anchor in (
        "prop:aesp-cd-retraction-shadowing-stop",
        "lem:aesp-cd-full-correction-separation",
        "thm:aesp-cd-high-dirichlet-branch",
        "eq:aesp-cd-high-dirichlet-vector",
    ):
        assert anchor in main_text
    combined = " ".join((main_text + " " + readme_text + " " + status_text).split())
    assert "black-box shadowing" in combined
    assert "not a graph-uniform solver theorem" in combined
    assert "low-Dirichlet" in combined
    assert "not a counterexample to direct finite-sequence packing" in combined


def main() -> None:
    check_retraction_stop()
    check_full_correction_separation()
    check_high_dirichlet_branch()
    check_source_guardrails()
    print("Round-024 exact structural audit passed")
    print("  P2 retraction: support-entry discontinuity; sharp fixed-support factor 1+1/alpha")
    print(
        "  settled face: exact full corrections are separated; adjacent finite correction is residual-only"
    )
    print("  high-Dirichlet branch: direct finite error contraction and accelerated cached vector")
    print("  scope: low-Dirichlet actual-finite net exponent remains open")


if __name__ == "__main__":
    main()
