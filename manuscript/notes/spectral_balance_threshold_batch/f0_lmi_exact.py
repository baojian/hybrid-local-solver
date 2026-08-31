#!/usr/bin/env python3
"""Exact Bernstein audit for the projection-compatible F0 held-step LMI.

Run, for example, with::

    uv run --with sympy python f0_lmi_exact.py

Nonnegative tensor-product Bernstein coefficients certify each polynomial
minor on ``(sqrt(alpha), y) in [0,1]^2``.
"""

from math import comb

import sympy as sp


s, y = sp.symbols("s y", nonnegative=True, real=True)
alpha = s**2
eigenvalue = alpha + (1 - alpha) * y
a = (1 + alpha) / 2
coupling = (1 - alpha) / 2

update = sp.Matrix(
    [
        [1 - eigenvalue, 1 - eigenvalue],
        [alpha - eigenvalue, 1 - eigenvalue],
    ]
) / (1 + s)
f_zero = sp.factor(a * coupling - (a - eigenvalue) ** 2)
metric = sp.diag(eigenvalue, 1 + f_zero)
slack = sp.simplify((1 - s) * metric - update.T * metric * update)


def bernstein_coefficients(
    polynomial: sp.Expr,
    first: sp.Symbol,
    second: sp.Symbol,
) -> tuple[int, int, list[list[sp.Expr]]]:
    """Convert a bivariate power polynomial to the Bernstein basis."""
    expanded = sp.Poly(sp.expand(polynomial), first, second)
    first_degree = expanded.degree(first)
    second_degree = expanded.degree(second)
    monomial = {
        (i, j): expanded.coeff_monomial(first**i * second**j)
        for i in range(first_degree + 1)
        for j in range(second_degree + 1)
    }
    coefficients: list[list[sp.Expr]] = []
    for k in range(first_degree + 1):
        row: list[sp.Expr] = []
        for ell in range(second_degree + 1):
            value = sum(
                monomial[i, j]
                * sp.Rational(comb(k, i), comb(first_degree, i))
                * sp.Rational(comb(ell, j), comb(second_degree, j))
                for i in range(k + 1)
                for j in range(ell + 1)
            )
            row.append(sp.factor(value))
        coefficients.append(row)
    return first_degree, second_degree, coefficients


def main() -> None:
    for name, expression in (
        ("K11", slack[0, 0]),
        ("K22", slack[1, 1]),
        ("detK", slack.det()),
    ):
        numerator, denominator = sp.fraction(sp.factor(sp.cancel(expression)))
        degree_s, degree_y, coefficient_rows = bernstein_coefficients(numerator, s, y)
        flat = [value for row in coefficient_rows for value in row]
        assert all(value >= 0 for value in flat), (name, coefficient_rows)
        positive = [value for value in flat if value > 0]
        print(
            name,
            "degrees=",
            (degree_s, degree_y),
            "denominator=",
            sp.factor(denominator),
            "zeros=",
            sum(value == 0 for value in flat),
            "min_positive=",
            min(positive),
        )
    print("F0(lambda)=", f_zero)
    print("Exact Bernstein/Sylvester audit passed.")


if __name__ == "__main__":
    main()
