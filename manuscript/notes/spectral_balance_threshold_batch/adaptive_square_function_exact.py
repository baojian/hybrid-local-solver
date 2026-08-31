"""Exact audit for the certified-gap adaptive fixed-cut square function.

Run with a Python environment containing SymPy, for example

    uv run --with sympy python adaptive_square_function_exact.py

The script proves, in exact arithmetic, the scalar observability Gramian
formula and the sharp uniform operator bound

    W_{alpha,mu}(lambda)
        <= ((3 + sqrt(5)) / (8 sqrt(mu))) P_{mu}(lambda).

It also checks the four-vertex path witness showing that this exact
remaining-output Gramian cannot be stitched locally through a face growth.
"""

from __future__ import annotations

import itertools

import sympy as sp


s, lam, alpha, y, z = sp.symbols("s lam alpha y z", nonnegative=True)
mu = s**2
r = 1 - lam
delta = lam - mu

companion = sp.Matrix([[r, r], [-delta, r]]) / (1 + s)
output = sp.Matrix([[1, 1]]) / (1 + s)

a_den = 4 - (3 - s) * lam
b_den = 2 * s + (1 - s) * lam
n_cut = lam * (s**3 - 3 * s**2 + 2) + 2 * s**2
h_cut = 2 - (1 - s) * lam
cut_factor = (lam - alpha) * (1 - lam) / (lam * (1 + s) * a_den)

gramian = sp.Matrix(
    [
        [cut_factor * n_cut / b_den, cut_factor],
        [cut_factor, cut_factor * h_cut / b_den],
    ]
)

f_mu = (1 + mu) * lam - lam**2 - mu * (1 + alpha) / 2
metric = sp.diag(lam, 1 + f_mu)


def check_zero_matrix(matrix: sp.Matrix, label: str) -> None:
    """Assert that every entry of ``matrix`` is the zero rational function."""
    for entry in matrix:
        assert sp.factor(entry) == 0, (label, sp.factor(entry))


check_zero_matrix(
    gramian - companion.T * gramian * companion - (lam - alpha) * (1 - lam) * output.T * output,
    "adaptive cut Lyapunov equation",
)


def tensor_bernstein_coefficients(
    expression: sp.Expr,
) -> tuple[tuple[int, int, int], list[sp.Expr]]:
    """Return exact tensor-Bernstein coefficients on ``[0,1]^3``."""
    polynomial = sp.Poly(sp.expand(expression), s, y, z, extension=sp.sqrt(5))
    variables = (s, y, z)
    degrees = tuple(polynomial.degree(variable) for variable in variables)
    coefficients: list[sp.Expr] = []

    for rows in itertools.product(*(range(degree + 1) for degree in degrees)):
        value = 0
        for exponents in itertools.product(*(range(row + 1) for row in rows)):
            monomial = sp.prod(
                variable**exponent for variable, exponent in zip(variables, exponents)
            )
            term = polynomial.coeff_monomial(monomial)
            for row, exponent, degree in zip(rows, exponents, degrees):
                term *= sp.binomial(row, exponent) / sp.binomial(degree, exponent)
            value += term
        coefficients.append(sp.simplify(value))

    return degrees, coefficients


def certify(expression: sp.Expr, label: str) -> None:
    """Certify nonnegativity by exact tensor-Bernstein coefficients."""
    degrees, coefficients = tensor_bernstein_coefficients(expression)
    assert all(value.is_nonnegative is True for value in coefficients), (
        label,
        [value for value in coefficients if value.is_nonnegative is not True],
    )
    positive = [value for value in coefficients if value != 0]
    minimum = min(positive, key=lambda value: float(sp.N(value, 30)))
    print(
        label,
        "degrees=",
        degrees,
        "zeros=",
        sum(value == 0 for value in coefficients),
        "min_positive=",
        minimum,
    )


# Clear the common positive denominator in
#
#   ((3 + sqrt(5)) / (8 s)) metric - gramian.
#
# Its two diagonal entries and determinant are then the three polynomials
# below.  The substitution parameterizes exactly
# alpha <= mu <= lambda <= 1.
kappa = (3 + sp.sqrt(5)) / 8
common_denominator = lam * (1 + s) * a_den * b_den

h_11 = kappa * common_denominator * lam - s * (lam - alpha) * r * n_cut
h_22 = kappa * common_denominator * (1 + f_mu) - s * (lam - alpha) * r * h_cut
h_12_magnitude = s * (lam - alpha) * r * b_den
determinant = sp.expand(h_11 * h_22 - h_12_magnitude**2)

cube_substitution = {
    alpha: z * s**2,
    lam: s**2 + (1 - s**2) * y,
}

certify(h_11.subs(cube_substitution), "adaptive cut H11")
certify(h_22.subs(cube_substitution), "adaptive cut H22")
certify(determinant.subs(cube_substitution), "adaptive cut determinant")


# The uniform constant is sharp for the scalar relaxation.  Along
# alpha / mu -> 0 and lambda = mu -> 0, the normalized Gramian converges
# to this matrix, whose top eigenvalue is kappa.
sharp_limit = sp.Matrix(
    [[sp.Rational(1, 2), sp.Rational(1, 4)], [sp.Rational(1, 4), sp.Rational(1, 4)]]
)
sharp_eigenvalues = sorted(sharp_limit.eigenvals(), key=lambda value: float(sp.N(value)))
assert sharp_eigenvalues[-1] == kappa
print("sharp scalar limit eigenvalues=", sharp_eigenvalues)


# Moving-face tail-jump witness.  In the normalized unit path P4, take
# U={1,2}, add B={3}, and keep W={4} exterior.  The old W-to-U cut is zero.
# After the growth, the W-to-(U union B) cut is supported at coordinate 3.
# Starting from h=e_1,w=0, q_0 and q_1 vanish there, but q_2 does not.
path_alpha = sp.symbols("path_alpha", nonnegative=True)
path_a = (1 + path_alpha) / 2
path_c = (1 - path_alpha) / 2
root = sp.symbols("root", positive=True)

path_face = sp.Matrix(
    [
        [path_a, -path_c / sp.sqrt(2), 0],
        [-path_c / sp.sqrt(2), path_a, -path_c / 2],
        [0, -path_c / 2, path_a],
    ]
)
identity = sp.eye(3)
seed = sp.Matrix([1, 0, 0])

q_0 = seed / (1 + root)
q_1 = ((1 + root**2) * identity - 2 * path_face) * seed / (1 + root) ** 2
q_2 = (
    -(path_face - identity)
    * (-4 * path_face + (3 * root**2 + 1) * identity)
    * seed
    / (1 + root) ** 3
)

new_exterior_cut = sp.Matrix([[0, 0, path_c / sp.sqrt(2)]])
assert q_0[2] == 0
assert q_1[2] == 0
assert sp.factor(q_2[2] - sp.sqrt(2) * path_c**2 / (1 + root) ** 3) == 0
assert sp.factor((new_exterior_cut * q_2)[0] - path_c**3 / (1 + root) ** 3) == 0

print(
    "P4 new exterior output at time 2=",
    sp.factor((new_exterior_cut * q_2)[0]),
)
print("all exact adaptive square-function checks passed")
