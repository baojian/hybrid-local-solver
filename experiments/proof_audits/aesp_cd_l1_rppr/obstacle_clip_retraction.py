#!/usr/bin/env python3
"""Exact audit of the margin-free obstacle clip-or-pay retraction."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from random import Random

from experiments.proof_audits import note_tex_source


Matrix = list[list[F]]
Vector = list[F]


def solve(matrix: Matrix, rhs: Vector) -> Vector:
    """Solve a small rational system by exact Gauss-Jordan elimination."""
    size = len(rhs)
    work = [row[:] + [value] for row, value in zip(matrix, rhs, strict=True)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        diagonal = work[column][column]
        work[column] = [entry / diagonal for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column], strict=True)
            ]
    return [row[-1] for row in work]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [sum(entry * value for entry, value in zip(row, vector, strict=True)) for row in matrix]


def obstacle_solution(hessian: Matrix, rhs: Vector) -> Vector:
    """Enumerate supports and return the exact obstacle minimizer."""
    size = len(rhs)
    for support_size in range(size + 1):
        for support_tuple in combinations(range(size), support_size):
            support = set(support_tuple)
            candidate = [F(0)] * size
            if support:
                active = solve(
                    [[hessian[i][j] for j in support_tuple] for i in support_tuple],
                    [rhs[i] for i in support_tuple],
                )
                if any(value <= 0 for value in active):
                    continue
                for index, value in zip(support_tuple, active, strict=True):
                    candidate[index] = value
            residual = [matvec(hessian, candidate)[i] - rhs[i] for i in range(size)]
            if all(residual[i] == 0 for i in support) and all(
                residual[i] >= 0 for i in range(size) if i not in support
            ):
                return candidate
    raise AssertionError("no obstacle KKT support found")


def retract(
    hessian: Matrix,
    rhs: Vector,
    approximate: Vector,
    supersolution: Vector,
) -> tuple[Vector, F]:
    """Apply the theorem's coordinatewise clip-or-pay shift."""
    hv = matvec(hessian, supersolution)
    assert all(value > 0 for value in hv)
    residual = [
        value - target for value, target in zip(matvec(hessian, approximate), rhs, strict=True)
    ]
    delta = max(
        max(min(approximate[i] / supersolution[i], residual[i] / hv[i]), F(0))
        for i in range(len(rhs))
    )
    published = [max(approximate[i] - delta * supersolution[i], F(0)) for i in range(len(rhs))]
    return published, delta


def assert_certificate(
    hessian: Matrix,
    rhs: Vector,
    exact: Vector,
    approximate: Vector,
    supersolution: Vector,
) -> Vector:
    """Check subsolution order and the exact a-posteriori error bound."""
    published, delta = retract(hessian, rhs, approximate, supersolution)
    image = matvec(hessian, published)
    assert all(rhs[i] - image[i] >= 0 for i, value in enumerate(published) if value > 0)
    assert all(F(0) <= published[i] <= exact[i] for i in range(len(rhs)))

    epsilon = max(abs(approximate[i] - exact[i]) for i in range(len(rhs)))
    hv = matvec(hessian, supersolution)
    mu_v = min(hv[i] / supersolution[i] for i in range(len(rhs)))
    row_norm = max(sum(abs(entry) for entry in row) for row in hessian)
    v_min, v_max = min(supersolution), max(supersolution)
    delta_bound = epsilon / v_min * max(F(1), row_norm / mu_v)
    error_bound = epsilon + v_max * delta_bound
    assert delta <= delta_bound
    assert max(exact[i] - published[i] for i in range(len(rhs))) <= error_bound
    return published


def random_strict_stieltjes(rng: Random, size: int) -> Matrix:
    """Construct an exact strictly diagonally dominant Stieltjes matrix."""
    matrix = [[F(0)] * size for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            if rng.randrange(3):
                weight = F(rng.randrange(1, 5), rng.randrange(5, 11))
                matrix[i][j] = matrix[j][i] = -weight
    for i in range(size):
        matrix[i][i] = sum(abs(value) for value in matrix[i]) + F(rng.randrange(1, 5), 3)
    return matrix


def check_random_exact_instances() -> tuple[int, int]:
    """Audit mixed active/inactive supports and max-closure exactly."""
    rng = Random(20260829)
    cases = 0
    mixed = 0
    for size in range(2, 7):
        for _ in range(45):
            hessian = random_strict_stieltjes(rng, size)
            rhs = [F(rng.randrange(-8, 9), 5) for _ in range(size)]
            exact = obstacle_solution(hessian, rhs)
            if any(value == 0 for value in exact) and any(value > 0 for value in exact):
                mixed += 1
            supersolution = [F(1)] * size
            publications: list[Vector] = []
            for trial in range(2):
                approximate = []
                for value in exact:
                    perturbation = F(rng.randrange(-4, 5), 100 + 17 * trial)
                    approximate.append(max(value + perturbation, F(0)))
                publications.append(
                    assert_certificate(hessian, rhs, exact, approximate, supersolution)
                )
            joined = [max(left, right) for left, right in zip(*publications, strict=True)]
            joined_image = matvec(hessian, joined)
            assert all(rhs[i] - joined_image[i] >= 0 for i, value in enumerate(joined) if value > 0)
            assert all(joined[i] <= exact[i] for i in range(size))
            cases += 1
    assert mixed > 100
    return cases, mixed


def check_clip_or_pay_witness() -> None:
    """Show why paying a huge inactive dual residual is unnecessary."""
    hessian = [[F(1), F(0)], [F(0), F(1)]]
    rhs = [F(-100), F(1)]
    exact = [F(0), F(1)]
    approximate = [F(1, 100), F(1)]
    published, delta = retract(hessian, rhs, approximate, [F(1), F(1)])
    assert delta == F(1, 100)
    assert published == [F(0), F(99, 100)]
    ordinary_all_row_shift = max(
        value - target for value, target in zip(matvec(hessian, approximate), rhs, strict=True)
    )
    assert ordinary_all_row_shift == F(10001, 100)
    assert ordinary_all_row_shift / delta == 10001
    assert_certificate(hessian, rhs, exact, approximate, [F(1), F(1)])


def check_point_source_connected() -> int:
    """Check rooted connected support for exact and published subsolutions."""
    rng = Random(1701)
    cases = 0
    for size in range(2, 10):
        for _ in range(20):
            hessian = [[F(0)] * size for _ in range(size)]
            for i in range(size - 1):
                weight = F(rng.randrange(1, 7), 10)
                hessian[i][i + 1] = hessian[i + 1][i] = -weight
            for i in range(size):
                hessian[i][i] = sum(abs(value) for value in hessian[i]) + F(1, 2)
            rhs = [F(rng.randrange(1, 8), 3)] + [
                -F(rng.randrange(0, 6), 7) for _ in range(size - 1)
            ]
            exact = obstacle_solution(hessian, rhs)
            approximate = [max(value + F(rng.randrange(-3, 4), 100), F(0)) for value in exact]
            published = assert_certificate(hessian, rhs, exact, approximate, [F(1)] * size)
            for vector in (exact, published):
                support = [i for i, value in enumerate(vector) if value > 0]
                if support:
                    assert support[0] == 0
                    assert support == list(range(support[-1] + 1))
            cases += 1
    return cases


def check_source_scope() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{thm:aesp-cd-obstacle-clip-retraction}" in source
    assert r"\label{cor:aesp-cd-margin-free-obstacle-primitive}" in source
    assert r"\label{lem:aesp-cd-point-source-subsolution-connected}" in source
    assert "clip-or-pay" in source


def main() -> None:
    cases, mixed = check_random_exact_instances()
    check_clip_or_pay_witness()
    rooted = check_point_source_connected()
    check_source_scope()
    print("PASS margin-free obstacle clip-or-pay retraction")
    print(f"  exact rational Stieltjes cases={cases}, mixed supports={mixed}")
    print(f"  rooted point-source connected cases={rooted}")
    print("  inactive dual-residual overcharge ratio=10001")


if __name__ == "__main__":
    main()
