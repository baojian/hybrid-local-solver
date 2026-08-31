"""Proof-audit checks for the fixed-face SOR and spider formulas."""

from __future__ import annotations

import cmath
import math
from fractions import Fraction

Matrix2 = tuple[tuple[float, float], tuple[float, float]]


def exact_modal_matrix(
    omega: Fraction, coupling: Fraction
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    """Return the exact two-coordinate red--black SOR error block."""
    one_minus = 1 - omega
    return (
        (one_minus, omega * coupling),
        (
            omega * coupling * one_minus,
            one_minus + omega * omega * coupling * coupling,
        ),
    )


def exact_trace(matrix: tuple[tuple[Fraction, Fraction], ...]) -> Fraction:
    return matrix[0][0] + matrix[1][1]


def exact_det(matrix: tuple[tuple[Fraction, Fraction], ...]) -> Fraction:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def float_modal_matrix(omega: float, coupling: float) -> Matrix2:
    one_minus = 1.0 - omega
    return (
        (one_minus, omega * coupling),
        (
            omega * coupling * one_minus,
            one_minus + omega * omega * coupling * coupling,
        ),
    )


def multiply(left: Matrix2, right: Matrix2) -> Matrix2:
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def power(matrix: Matrix2, exponent: int) -> Matrix2:
    result: Matrix2 = ((1.0, 0.0), (0.0, 1.0))
    base = matrix
    value = exponent
    while value:
        if value & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        value //= 2
    return result


def spectral_norm(matrix: Matrix2) -> float:
    frobenius_sq = sum(value * value for row in matrix for value in row)
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    discriminant = max(0.0, frobenius_sq * frobenius_sq - 4.0 * determinant**2)
    return math.sqrt((frobenius_sq + math.sqrt(discriminant)) / 2.0)


def root_moduli(trace: float, determinant: float) -> tuple[float, float]:
    discriminant_value = trace * trace - 4.0 * determinant
    scale = max(1.0, abs(trace * trace), abs(4.0 * determinant))
    if abs(discriminant_value) <= 1e-12 * scale:
        discriminant_value = 0.0
    discriminant = complex(discriminant_value)
    root = cmath.sqrt(discriminant)
    return (abs((trace + root) / 2.0), abs((trace - root) / 2.0))


def check_exact_global_parameter() -> int:
    cells = 0
    square_roots = [
        Fraction(1, 100),
        Fraction(1, 20),
        Fraction(1, 10),
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(3, 4),
    ]
    sigmas = [
        Fraction(0),
        Fraction(1, 5),
        Fraction(1, 2),
        Fraction(4, 5),
        Fraction(1),
    ]
    for root_alpha in square_roots:
        alpha = root_alpha * root_alpha
        coupling_max = (1 - alpha) / (1 + alpha)
        t_alpha = 2 * root_alpha / (1 + alpha)
        zeta = ((1 - root_alpha) / (1 + root_alpha)) ** 2
        omega = 1 + zeta
        assert omega == 2 / (1 + t_alpha)
        assert 1 - coupling_max * coupling_max == t_alpha * t_alpha
        assert omega * omega * coupling_max * coupling_max == 4 * zeta

        for sigma in sigmas:
            coupling = coupling_max * sigma
            matrix = exact_modal_matrix(omega, coupling)
            trace = exact_trace(matrix)
            determinant = exact_det(matrix)
            assert determinant == zeta * zeta
            assert -2 * zeta <= trace <= 2 * zeta
            cells += 1
    return cells


def check_exact_face_parameter() -> int:
    cells = 0
    # Pythagorean parameterizations make rho and sqrt(1-rho^2) rational.
    pairs = [(2, 1), (3, 1), (4, 1), (3, 2), (5, 2), (5, 3)]
    fractions = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)]
    for u, v in pairs:
        denominator = u * u + v * v
        rho = Fraction(2 * u * v, denominator)
        t_face = Fraction(u * u - v * v, denominator)
        zeta = (1 - t_face) / (1 + t_face)
        omega = 1 + zeta
        assert rho * rho + t_face * t_face == 1
        assert omega == 2 / (1 + t_face)
        assert omega * omega * rho * rho == 4 * zeta

        for fraction in fractions:
            coupling = rho * fraction
            matrix = exact_modal_matrix(omega, coupling)
            trace = exact_trace(matrix)
            determinant = exact_det(matrix)
            assert determinant == zeta * zeta
            assert -2 * zeta <= trace <= 2 * zeta
            if fraction == 1:
                assert trace == 2 * zeta
            cells += 1
    return cells


def check_finite_power_bound() -> int:
    cells = 0
    for alpha in (1e-4, 1e-3, 1e-2, 0.1, 0.4):
        c_alpha = (1.0 - alpha) / (1.0 + alpha)
        for sigma_max in (0.2, 0.6, 0.9, 1.0):
            rho = c_alpha * sigma_max
            t_face = math.sqrt(1.0 - rho * rho)
            omega = 2.0 / (1.0 + t_face)
            zeta = omega - 1.0
            for fraction in (0.0, 0.25, 0.75, 1.0):
                matrix = float_modal_matrix(omega, rho * fraction)
                trace = matrix[0][0] + matrix[1][1]
                determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
                moduli = root_moduli(trace, determinant)
                assert max(moduli) <= zeta + 2e-12
                for exponent in (1, 2, 3, 5, 8, 13):
                    lhs = spectral_norm(power(matrix, exponent))
                    rhs = 6.0 * exponent * zeta ** (exponent - 1)
                    assert lhs <= rhs + 2e-11
                    cells += 1
    return cells


def check_spider_prefix() -> int:
    cells = 0
    for alpha in (1e-4, 1e-3, 1e-2, 0.1, 0.5):
        c_alpha = (1.0 - alpha) / (1.0 + alpha)
        for depth in (1, 2, 4, 8, 16, 32):
            theta = math.pi / (2.0 * (depth + 1))
            sigma = math.cos(theta)
            t_face = math.sqrt(1.0 - c_alpha * c_alpha * sigma * sigma)
            decomposed = math.sqrt(
                (1.0 - c_alpha * c_alpha) + c_alpha * c_alpha * math.sin(theta) ** 2
            )
            assert math.isclose(t_face, decomposed, rel_tol=2e-14, abs_tol=2e-14)
            omega = 2.0 / (1.0 + t_face)
            zeta = omega - 1.0
            matrix = float_modal_matrix(omega, c_alpha * sigma)
            trace = matrix[0][0] + matrix[1][1]
            determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            moduli = root_moduli(trace, determinant)
            assert all(math.isclose(value, zeta, rel_tol=2e-10, abs_tol=2e-12) for value in moduli)
            cells += 1
    return cells


def main() -> None:
    exact_global = check_exact_global_parameter()
    exact_face = check_exact_face_parameter()
    finite_power = check_finite_power_bound()
    spider = check_spider_prefix()
    total = exact_global + exact_face + finite_power + spider
    print(
        "fixed-face SOR checks passed: "
        f"{total} cells "
        f"({exact_global} exact-global, {exact_face} exact-face, "
        f"{finite_power} powers, {spider} spiders)"
    )


if __name__ == "__main__":
    main()
