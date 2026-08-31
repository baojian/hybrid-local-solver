"""Exact-arithmetic check for Section 6 of open_conjectures_proof_attempt.md."""

from fractions import Fraction as F


def solve_two_by_two(a, b, c, d, e, f):
    determinant = a * d - b * c
    return (e * d - b * f) / determinant, (a * f - c * e) / determinant


beta = F(1, 20)
lambda_value = F(3, 40)
kappa = F(3, 40)

# Phase 0, S={0}.  Vertex 0 has degree 3.
y0_initial = beta * (1 - 3 * lambda_value) / 3
r_boundary_initial = (1 - beta) * y0_initial / beta

assert y0_initial == F(31, 2400)
assert r_boundary_initial == F(589, 2400)
assert r_boundary_initial > (lambda_value + kappa) * 1
assert r_boundary_initial < (lambda_value + kappa) * 2

# Phase 1, S={0,1}.  The principal matrix is
# [[3, -(1-beta)], [-(1-beta), 1]].
y0_updated, y1_updated = solve_two_by_two(
    F(3),
    -(1 - beta),
    -(1 - beta),
    F(1),
    beta * (1 - 3 * lambda_value),
    -beta * lambda_value,
)
r_boundary_updated = (1 - beta) * y0_updated / beta

assert y0_updated == F(563, 33560)
assert y1_updated == F(409, 33560)
assert r_boundary_updated == F(10697, 33560)
assert r_boundary_updated > (lambda_value + kappa) * 2

print("exact boundary counterexample verified")

