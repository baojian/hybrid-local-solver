"""Exact Gramian/Bernstein checks for the fixed-face square functions.

Run with a Python environment containing SymPy, for example

    uv run --with sympy python moving_face_smoothing_exact.py
"""

import sympy as sp


s, lam, y = sp.symbols("s lam y", nonnegative=True)
delta = lam - s**2
r = 1 - lam
a_den = 4 - (3 - s) * lam
b_den = 2 * s + (1 - s) * lam

companion = sp.Matrix([[r, r], [-delta, r]]) / (1 + s)
output = sp.Matrix([[1, 1]]) / (1 + s)


def check_zero_matrix(matrix: sp.Matrix, label: str) -> None:
    for entry in matrix:
        assert sp.factor(entry) == 0, (label, sp.factor(entry))


def bernstein_coefficients(poly: sp.Expr) -> tuple[int, int, list[sp.Expr]]:
    """Return tensor Bernstein coefficients on ``[0,1]^2`` in ``(s,y)``."""
    expanded = sp.Poly(sp.expand(poly), s, y)
    degree_s, degree_y = expanded.degree(s), expanded.degree(y)
    coefficients: list[sp.Expr] = []
    for row in range(degree_s + 1):
        for column in range(degree_y + 1):
            value = 0
            for i in range(row + 1):
                for j in range(column + 1):
                    value += (
                        expanded.coeff_monomial(s**i * y**j)
                        * sp.binomial(row, i)
                        / sp.binomial(degree_s, i)
                        * sp.binomial(column, j)
                        / sp.binomial(degree_y, j)
                    )
            coefficients.append(sp.factor(value))
    return degree_s, degree_y, coefficients


def certify(poly: sp.Expr, label: str) -> None:
    degree_s, degree_y, coefficients = bernstein_coefficients(poly)
    assert all(value >= 0 for value in coefficients), (
        label,
        [value for value in coefficients if value < 0],
    )
    positive = [value for value in coefficients if value > 0]
    print(
        label,
        "degrees=",
        (degree_s, degree_y),
        "zeros=",
        sum(value == 0 for value in coefficients),
        "min_positive=",
        min(positive) if positive else None,
    )


def certify_univariate(poly: sp.Expr, variable: sp.Symbol, label: str) -> None:
    """Certify nonnegativity on ``[0,1]`` by Bernstein coefficients."""
    expanded = sp.Poly(sp.expand(poly), variable)
    degree = expanded.degree()
    coefficients = []
    for row in range(degree + 1):
        value = sum(
            expanded.coeff_monomial(variable**i) * sp.binomial(row, i) / sp.binomial(degree, i)
            for i in range(row + 1)
        )
        coefficients.append(sp.factor(value))
    assert all(value >= 0 for value in coefficients), (label, coefficients)
    print(label, "degree=", degree, "Bernstein=", coefficients)


# Cut-output observability Gramian.
n_cut = lam * s**3 - 3 * lam * s**2 + 2 * lam + 2 * s**2
c_cut = 2 - (1 - s) * lam
w_cut = sp.Matrix(
    [
        [
            delta * r * n_cut / (lam * (1 + s) * a_den * b_den),
            delta * r / (lam * (1 + s) * a_den),
        ],
        [
            delta * r / (lam * (1 + s) * a_den),
            delta * r * c_cut / (lam * (1 + s) * a_den * b_den),
        ],
    ]
)
cut_source = delta * r * (output.T * output)
check_zero_matrix(
    w_cut - companion.T * w_cut * companion - cut_source,
    "cut Lyapunov",
)

a = (1 + s**2) / 2
c = (1 - s**2) / 2
f_zero = a * c - (a - lam) ** 2
p_metric = sp.diag(lam, 1 + f_zero)
common_cut = lam * (1 + s) * a_den * b_den
sub_lam = s**2 + (1 - s**2) * y

cut_u_cert = sp.cancel((lam / (4 * s) - w_cut[0, 0]) * 4 * s * common_cut)
cut_w_cert = sp.cancel(((1 + f_zero) / (4 * s) - w_cut[1, 1]) * 4 * s * common_cut)
for label, expression in (("cut u", cut_u_cert), ("cut w", cut_w_cert)):
    numerator, denominator = sp.fraction(sp.factor(expression.subs(lam, sub_lam)))
    assert denominator > 0
    certify(numerator, label)


# Q-variation observability Gramian.
variation_output = output * (companion - sp.eye(2))
n_u = (
    lam**2 * s**2
    - 4 * lam**2 * s
    + 3 * lam**2
    + 2 * lam * s**3
    - 8 * lam * s**2
    + 8 * lam * s
    + 2 * lam
    + 2 * s**4
    - 4 * s**3
    + 2 * s**2
)
n_w = (
    lam**2 * s**2
    - 4 * lam**2 * s
    + 3 * lam**2
    - 2 * lam * s**2
    + 10 * lam * s
    - 4 * lam
    + 2 * s**2
    - 4 * s
    + 2
)
w_variation = sp.Matrix(
    [
        [
            lam * n_u / ((1 + s) ** 2 * a_den * b_den),
            lam * ((3 - s) * lam - (1 - s) ** 2) / ((1 + s) ** 2 * a_den),
        ],
        [
            lam * ((3 - s) * lam - (1 - s) ** 2) / ((1 + s) ** 2 * a_den),
            lam * n_w / ((1 + s) ** 2 * a_den * b_den),
        ],
    ]
)
variation_source = lam * (variation_output.T * variation_output)
check_zero_matrix(
    w_variation - companion.T * w_variation * companion - variation_source,
    "variation Lyapunov",
)

common_variation = (1 + s) ** 2 * a_den * b_den
variation_u_cert = sp.cancel((5 * lam - w_variation[0, 0]) * common_variation / lam)
variation_w_cert = sp.cancel(((1 + f_zero) - w_variation[1, 1]) * common_variation)
for label, expression in (
    ("variation u", variation_u_cert),
    ("variation w", variation_w_cert),
):
    numerator, denominator = sp.fraction(sp.factor(expression.subs(lam, sub_lam)))
    assert denominator > 0
    certify(numerator, label)


# Sharp ``1/s`` asymptotic at ``lam=k*s^2``.
k = sp.symbols("k", positive=True)
w_k = w_cut.subs(lam, k * s**2)
p_k = p_metric.subs(lam, k * s**2)
generalized_limit = sp.Matrix(
    [
        [
            sp.limit(s * w_k[0, 0] / p_k[0, 0], s, 0, dir="+"),
            sp.limit(
                s * w_k[0, 1] / sp.sqrt(p_k[0, 0] * p_k[1, 1]),
                s,
                0,
                dir="+",
            ),
        ],
        [
            sp.limit(
                s * w_k[1, 0] / sp.sqrt(p_k[0, 0] * p_k[1, 1]),
                s,
                0,
                dir="+",
            ),
            sp.limit(s * w_k[1, 1] / p_k[1, 1], s, 0, dir="+"),
        ],
    ]
)
expected = (k - 1) / (4 * k) * sp.Matrix([[(k + 1) / k, 1 / sp.sqrt(k)], [1 / sp.sqrt(k), 1]])
check_zero_matrix(generalized_limit - expected, "sharp asymptotic")
at_six = expected.subs(k, 6)
assert sp.factor(at_six.det() - sp.Rational(5, 16) * at_six.trace() + sp.Rational(5, 16) ** 2) == 0
print("all exact checks passed; at k=6 the top asymptotic eigenvalue is 5/16")


# Exact unit-P3 moving-face witness.  Each pencil has diagonal ``p`` and
# adjacent off-diagonal ``sign*r``.  Direct inversion shows that adding the
# third vertex raises the old ``(1,1)`` inverse entry by the displayed
# positive rational function, independently of the off-diagonal sign.
pencils = (
    (
        "hard P3 pencil",
        2 * s + (1 - s) * a,
        (1 - s) * c / sp.sqrt(2),
        -1,
    ),
    (
        "uniform P3 pencil",
        4 - (3 - s) * a,
        (3 - s) * c / sp.sqrt(2),
        1,
    ),
)
p3_jumps = []
for label, p_value, r_value, sign in pencils:
    old_pencil = sp.Matrix([[p_value, sign * r_value], [sign * r_value, p_value]])
    grown_pencil = sp.Matrix(
        [
            [p_value, sign * r_value, 0],
            [sign * r_value, p_value, sign * r_value],
            [0, sign * r_value, p_value],
        ]
    )
    direct_jump = sp.factor(grown_pencil.inv()[0, 0] - old_pencil.inv()[0, 0])
    formula_jump = sp.factor(
        r_value**4 / (p_value * (p_value**2 - r_value**2) * (p_value**2 - 2 * r_value**2))
    )
    assert sp.factor(direct_jump - formula_jump) == 0, label
    certify_univariate(p_value, s, label + " p")
    certify_univariate(p_value**2 - r_value**2, s, label + " p2-r2")
    certify_univariate(p_value**2 - 2 * r_value**2, s, label + " p2-2r2")
    p3_jumps.append(formula_jump)

# For every ``0<s<1`` both denominators above are positive and both
# numerators are nonzero.  These positive inverse lifts enter the h-h
# variation Gramian with positive coefficients; affine terms have no jump.
variation_p3_jump = sp.factor(
    2 * s**2 / (1 + s) * p3_jumps[0] + 4 * (2 - s) / (1 + s) * p3_jumps[1]
)
assert variation_p3_jump != 0
print("exact P3 hard and remaining-variation jumps are strictly positive")


# The hard pencil on an interior degree-two path has diagonal ``path_p`` and
# off-diagonal magnitude ``path_r``.  Its Green transfer exponent satisfies
# ``cosh(gamma)=path_p/(2*path_r)``.  The exact limits certify
# ``gamma~sqrt(8s)``, hence correlation length ``Theta(s^-1/2)``.
path_p = 2 * s + (1 - s) * a
path_r = (1 - s) * c / 2
path_cosh = sp.factor(path_p / (2 * path_r))
assert sp.limit((path_cosh - 1) / s, s, 0, dir="+") == 4
assert sp.limit(sp.acosh(path_cosh) / sp.sqrt(s), s, 0, dir="+") == (2 * sp.sqrt(2))
print("exact path Green exponent is sqrt(8s)+o(sqrt(s))")


# Canonical masked-Duhamel checks.  On P2 a published exterior residual can
# be exactly zero although the inactive fixed-final forcing stays constant.
alpha_symbol = sp.symbols("alpha_symbol", positive=True)
a_alpha = (1 + alpha_symbol) / 2
c_alpha = (1 - alpha_symbol) / 2
rho_p2 = c_alpha / 2
q_p2 = sp.Matrix([[a_alpha, -c_alpha], [-c_alpha, a_alpha]])
rhs_p2 = alpha_symbol * sp.Matrix([1 - rho_p2, -rho_p2])
face_center_p2 = sp.factor(rhs_p2[0] / a_alpha)
lower_p2 = alpha_symbol / 2
exterior_residual_p2 = sp.factor(rhs_p2[1] + c_alpha * lower_p2)
full_center_p2 = sp.simplify(q_p2.inv() * rhs_p2)
inactive_forcing_p2 = sp.factor(c_alpha * full_center_p2[1])
assert exterior_residual_p2 == 0
assert sp.factor(face_center_p2 - alpha_symbol * (1 + a_alpha) / (2 * a_alpha)) == 0
assert sp.factor(full_center_p2[1] - c_alpha / 2) == 0
assert sp.limit(inactive_forcing_p2, alpha_symbol, 0, dir="+") == sp.Rational(1, 8)
print("canonical P2 has zero published gate and inactive forcing -> 1/8")


# On canonical P3 the exact safe-event center charge can vanish while an old
# packet's future shifted-resolvent lift stays positive.  The reachability of
# that packet from zero at this event is intentionally not asserted.
epsilon = sp.symbols("epsilon", positive=True)
q_p3 = sp.Matrix(
    [
        [a_alpha, -c_alpha / sp.sqrt(2), 0],
        [-c_alpha / sp.sqrt(2), a_alpha, -c_alpha / sp.sqrt(2)],
        [0, -c_alpha / sp.sqrt(2), a_alpha],
    ]
)
rho_zero = (1 - alpha_symbol) ** 2 / (4 * (1 + alpha_symbol))
rho_p3 = rho_zero - epsilon
rhs_p3 = alpha_symbol * sp.Matrix([1 - rho_p3, -sp.sqrt(2) * rho_p3, -rho_p3])
old_center_p3 = sp.simplify(q_p3[:2, :2].inv() * rhs_p3[:2, :])
gate_p3 = sp.factor(rhs_p3[2] + c_alpha / sp.sqrt(2) * old_center_p3[1])
claimed_gate_p3 = (
    4 * alpha_symbol * (1 + alpha_symbol) / (alpha_symbol**2 + 6 * alpha_symbol + 1) * epsilon
)
assert sp.factor(gate_p3 - claimed_gate_p3) == 0
center_charge_p3 = sp.factor(gate_p3**2 * q_p3.inv()[2, 2])
claimed_charge_p3 = (
    4 * alpha_symbol * (1 + alpha_symbol) / (alpha_symbol**2 + 6 * alpha_symbol + 1) * epsilon**2
)
assert sp.factor(center_charge_p3 - claimed_charge_p3) == 0
assert sp.limit(center_charge_p3, epsilon, 0, dir="+") == 0
print("canonical P3 safe-event center charge is exact O(epsilon^2)")
