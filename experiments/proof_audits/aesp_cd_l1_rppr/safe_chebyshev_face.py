#!/usr/bin/env python3
"""Exact audit of the fixed-face safe-Chebyshev interface.

The checker separates two facts which must not be conflated:

* a literal Chebyshev semi-iterate can have a negative coordinate residual
  and overshoot the exact Stieltjes solution already at degree two;
* the displayed a-posteriori common retraction restores the obstacle
  subsolution order, and its strict same-face guard is nonvacuous.

It also checks the elementary positive-coefficient polynomial obstruction:
cone-preserving residual polynomials require linear-in-condition-number
degree for constant contraction, even when composed through restarts.
"""

from __future__ import annotations

from fractions import Fraction as F

from experiments.proof_audits import note_tex_source


Matrix = list[list[F]]
Vector = list[F]


def solve(matrix: Matrix, rhs: Vector) -> Vector:
    """Solve one small rational system by exact Gauss-Jordan elimination."""
    size = len(rhs)
    work = [row[:] for row in matrix]
    value = rhs[:]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        value[column], value[pivot] = value[pivot], value[column]
        diagonal = work[column][column]
        work[column] = [entry / diagonal for entry in work[column]]
        value[column] /= diagonal
        for row in range(size):
            if row == column:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    work[row][index] - multiplier * work[column][index]
                    for index in range(size)
                ]
                value[row] -= multiplier * value[column]
    return value


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [sum(entry * value for entry, value in zip(row, vector, strict=True)) for row in matrix]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    size = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(size)) for j in range(size)]
        for i in range(size)
    ]


def cube_star_face() -> tuple[F, Matrix, Matrix, F]:
    """Return alpha, H, W, and the Chebyshev denominator for the witness.

    In the three-regular cube, one vertex together with its three neighbors
    induces a proper S4 face.  Hence its normalized adjacency is A_S4/3 and
    is rational in the symmetric coordinates used by the theorem.
    """
    alpha = F(1, 17)
    center = (1 + alpha) / 2
    radius = (1 - alpha) / 2
    walk = [[F(0)] * 4 for _ in range(4)]
    for leaf in range(1, 4):
        walk[0][leaf] = walk[leaf][0] = F(1, 3)
    hessian = [
        [center * F(i == j) - radius * walk[i][j] for j in range(4)]
        for i in range(4)
    ]
    sigma = center / radius
    denominator = 2 * sigma * sigma - 1
    assert sigma > 1 and denominator > 0
    return alpha, hessian, walk, denominator


def degree_two_residual(walk: Matrix, denominator: F, rhs: Vector) -> Vector:
    """Apply T_2(W)/T_2((1+alpha)/(1-alpha)) exactly."""
    square = matmul(walk, walk)
    chebyshev = [
        [2 * square[i][j] - F(i == j) for j in range(4)]
        for i in range(4)
    ]
    return [entry / denominator for entry in matvec(chebyshev, rhs)]


def retract(
    alpha: F,
    hessian: Matrix,
    exact: Vector,
    residual: Vector,
) -> tuple[Vector, Vector, F, Vector]:
    """Apply the theorem with upsilon=one and mu_upsilon=alpha."""
    error = solve(hessian, residual)
    semi_iterate = [exact[i] - error[i] for i in range(4)]
    delta = max(max(-entry, F(0)) / alpha for entry in residual)
    lower = [max(semi_iterate[i] - delta, F(0)) for i in range(4)]
    return lower, semi_iterate, delta, error


def check_literal_chebyshev_stop_and_safe_retraction() -> None:
    """Certify the negative wave, overshoot, and safe published checkpoint."""
    alpha, hessian, walk, denominator = cube_star_face()
    one = [F(1)] * 4
    assert all(entry >= alpha for entry in matvec(hessian, one))

    rhs = [F(0), F(1), F(0), F(0)]
    exact = solve(hessian, rhs)
    assert all(entry > 0 for entry in exact)
    residual = degree_two_residual(walk, denominator, rhs)
    assert residual[1] == F(-32, 63) < 0

    lower, semi_iterate, delta, _ = retract(alpha, hessian, exact, residual)
    assert [semi_iterate[i] > exact[i] for i in range(4)] == [True, True, False, False]
    assert delta == F(544, 63)
    assert all(F(0) <= lower[i] <= exact[i] for i in range(4))
    lower_residual = [rhs[i] - matvec(hessian, lower)[i] for i in range(4)]
    assert all(lower_residual[i] >= 0 for i in range(4) if lower[i] > 0)

    # The strict relative-interior guard is nonvacuous.  A large positive
    # baseline preserves the same signed Chebyshev wave while leaving enough
    # room for the published max-retraction checkpoint to stay on all rows.
    guarded_rhs = [F(100), F(101), F(100), F(100)]
    guarded_exact = solve(hessian, guarded_rhs)
    guarded_residual = degree_two_residual(walk, denominator, guarded_rhs)
    guarded_lower, guarded_semi_iterate, guarded_delta, _ = retract(
        alpha,
        hessian,
        guarded_exact,
        guarded_residual,
    )
    checkpoint = max(max(-entry, F(0)) / alpha for entry in guarded_residual)
    assert guarded_delta == checkpoint == F(167008, 441)
    assert min(guarded_semi_iterate) > guarded_delta
    assert all(F(0) < guarded_lower[i] <= guarded_exact[i] for i in range(4))
    guarded_lower_residual = [
        guarded_rhs[i] - matvec(hessian, guarded_lower)[i]
        for i in range(4)
    ]
    assert all(entry >= 0 for entry in guarded_lower_residual)


def convolve(left: list[F], right: list[F]) -> list[F]:
    """Multiply two restart polynomials in coefficient form."""
    product = [F(0)] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            product[i + j] += first * second
    return product


def check_positive_polynomial_obstruction() -> None:
    """Check the exact cone-preserving Omega(K) degree lower bound.

    For B=I-H/L >= 0, write the residual polynomial as
    P(B)=sum_j a_j B^j with a_j>=0 and P(1)=sum_j a_j=1.  On the slow
    eigenvalue b=1-1/K, every degree-k such polynomial satisfies
    P(b)>=b^k>=1-k/K.  Thus no degree at most K/2 can halve that mode.
    """
    coefficient_families = (
        [F(1, 3), F(1, 6), F(1, 2)],
        [F(1, 5), F(0), F(1, 5), F(3, 5)],
        convolve([F(1, 3), F(2, 3)], [F(1, 4), F(0), F(3, 4)]),
    )
    for coefficients in coefficient_families:
        assert all(entry >= 0 for entry in coefficients)
        assert sum(coefficients) == 1
        degree = len(coefficients) - 1
        for condition in (4, 8, 16, 32, 64):
            slow = F(condition - 1, condition)
            value = sum(entry * slow**power for power, entry in enumerate(coefficients))
            assert value >= slow**degree >= 1 - F(degree, condition)

    # A family whose degree grows with K makes the linear obstruction
    # explicit: even the extremal all-mass-at-highest-degree polynomial has
    # not halved the slow mode by floor(K/2).
    for condition in (4, 8, 16, 32, 64, 128):
        degree = condition // 2
        slow = F(condition - 1, condition)
        extremal = slow**degree
        assert extremal >= 1 - F(degree, condition) == F(1, 2)


def check_source_scope() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert "thm:aesp-cd-safe-chebyshev-face" in source
    assert "eq:aesp-cd-safe-chebyshev-retraction" in source
    assert "cor:aesp-cd-collatz-small-shift" in source
    assert "prop:aesp-cd-positive-polynomial-stop" in source
    assert "signed intermediate residuals" in source


def main() -> None:
    check_literal_chebyshev_stop_and_safe_retraction()
    check_positive_polynomial_obstruction()
    check_source_scope()
    print("Safe fixed-face Chebyshev audit passed")
    print("  cube proper S4: literal degree-two residual is negative and overshoots")
    print("  max Stieltjes checkpoint: order-safe, with a strict full-face witness")
    print("  positive coefficients/restarts: exact Omega(condition number) STOP")


if __name__ == "__main__":
    main()
