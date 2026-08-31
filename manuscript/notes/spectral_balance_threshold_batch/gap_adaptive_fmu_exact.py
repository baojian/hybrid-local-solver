"""Exact certificates for the certified-gap adaptive companion metric.

Run with a Python environment containing SymPy, for example

    uv run --with sympy python gap_adaptive_fmu_exact.py
"""

import itertools

import sympy as sp


t, y, z = sp.symbols("t y z", nonnegative=True)
variables = (t, y, z)
mu = t**2
alpha = z * t**2
a = (1 + alpha) / 2
lam = mu + (1 - mu) * y

f_mu = (1 + mu) * lam - lam**2 - mu * a
companion = sp.Matrix([[1 - lam, 1 - lam], [mu - lam, 1 - lam]]) / (1 + t)
metric = sp.diag(lam, 1 + f_mu)
held_slack = sp.simplify((1 + t) ** 2 * ((1 - t) * metric - companion.T * metric * companion))


def tensor_bernstein(poly: sp.Expr) -> tuple[tuple[int, ...], list[sp.Expr]]:
    expanded = sp.Poly(sp.expand(poly), *variables)
    degrees = tuple(expanded.degree(variable) for variable in variables)
    coefficients = []
    for outer in itertools.product(*(range(degree + 1) for degree in degrees)):
        value = 0
        for inner in itertools.product(*(range(index + 1) for index in outer)):
            monomial = sp.prod(variable**power for variable, power in zip(variables, inner))
            factor = sp.prod(
                sp.binomial(index, power) / sp.binomial(degree, power)
                for index, power, degree in zip(outer, inner, degrees)
            )
            value += expanded.coeff_monomial(monomial) * factor
        coefficients.append(sp.factor(value))
    return degrees, coefficients


for label, polynomial in (
    ("H11", held_slack[0, 0]),
    ("H22", held_slack[1, 1]),
    ("det(H)", sp.det(held_slack)),
):
    degrees, coefficients = tensor_bernstein(polynomial)
    assert all(coefficient >= 0 for coefficient in coefficients)
    positive = [coefficient for coefficient in coefficients if coefficient > 0]
    print(
        label,
        "degrees=",
        degrees,
        "zeros=",
        sum(coefficient == 0 for coefficient in coefficients),
        "min_positive=",
        min(positive),
    )


# Exact metric-change identity.  If ``alpha <= nu <= mu`` and the physical
# auxiliary error is kept fixed, its scaled companion coordinate changes by
# ``sqrt(nu/mu)``.  The new auxiliary metric never exceeds the old one.
old_mu, new_mu, eigenvalue, diagonal = sp.symbols(
    "old_mu new_mu eigenvalue diagonal", positive=True
)


def f(parameter: sp.Expr) -> sp.Expr:
    return (1 + parameter) * eigenvalue - eigenvalue**2 - parameter * diagonal


switch_slack = sp.factor(1 + f(old_mu) - new_mu / old_mu * (1 + f(new_mu)))
switch_bracket = sp.factor(
    1 + eigenvalue - eigenvalue**2 + (old_mu + new_mu) * (eigenvalue - diagonal)
)
assert sp.factor(switch_slack - (old_mu - new_mu) / old_mu * switch_bracket) == 0

# With ``diagonal=(1+alpha)/2``, the bracket is positive.  For eigenvalue
# above the diagonal this is immediate.  Below it, ``old_mu+new_mu<=2``
# gives the lower bound ``3*eigenvalue-eigenvalue**2-alpha``, whose minimum
# on ``[alpha,diagonal]`` is ``2*alpha-alpha**2>0``.
alpha_symbol = sp.symbols("alpha_symbol", positive=True)
lower_bound = 3 * eigenvalue - eigenvalue**2 - alpha_symbol
assert (
    sp.factor(lower_bound.subs(eigenvalue, alpha_symbol) - (2 * alpha_symbol - alpha_symbol**2))
    == 0
)

print("all exact gap-adaptive F_mu and decreasing-gap switch checks passed")


# Stale-root principal growth is genuinely unsafe.  On the unit triangle,
# retain the exact old two-vertex gap while adding the third vertex, whose
# full-face gap is alpha.  The resulting companion recenter jump is
# Theta(1/alpha) relative to source energy, with exact coefficient 7/32.
triangle_alpha = sp.symbols("triangle_alpha", positive=True)
triangle_a = (1 + triangle_alpha) / 2
triangle_c = (1 - triangle_alpha) / 2
triangle_s = sp.Matrix(
    [
        [0, sp.Rational(1, 2), sp.Rational(1, 2)],
        [sp.Rational(1, 2), 0, sp.Rational(1, 2)],
        [sp.Rational(1, 2), sp.Rational(1, 2), 0],
    ]
)
triangle_q = triangle_a * sp.eye(3) - triangle_c * triangle_s
triangle_rhs = triangle_alpha / sp.sqrt(2) * sp.Matrix([1, 0, 0])
old_q = triangle_q[:2, :2]
old_center = old_q.inv() * triangle_rhs[:2, :]
new_center = triangle_q.inv() * triangle_rhs
center_increment = sp.simplify(new_center - sp.Matrix([old_center[0], old_center[1], 0]))
old_gap = sp.factor(triangle_a - triangle_c / 2)
stale_f = (1 + old_gap) * triangle_q - triangle_q**2 - old_gap * triangle_a * sp.eye(3)
source_energy = sp.factor((new_center.T * triangle_q * new_center)[0])
stale_jump = sp.factor(
    (center_increment.T * triangle_q * center_increment)[0]
    + old_gap * (center_increment.T * (sp.eye(3) + stale_f) * center_increment)[0]
)
assert sp.limit(
    triangle_alpha * stale_jump / source_energy,
    triangle_alpha,
    0,
    dir="+",
) == sp.Rational(7, 32)
print("stale-mu triangle expansion has exact asymptotic coefficient 7/32")
