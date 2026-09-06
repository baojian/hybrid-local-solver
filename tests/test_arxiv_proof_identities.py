"""Finite falsification checks for the arXiv proof, not proof certificates.

Tiny obstacle optima are found by exhaustive KKT basis enumeration, independently
of the local algorithms. Fraction arithmetic checks the two-metric projection,
perturbed energies, signed-flow identity, and safe repair exactly. A separate
floating-point check exercises Cholesky batching with a nonsingleton seed block.
No timing or experimental performance claim is derived from these tests.
"""

from __future__ import annotations

import itertools
import random
from fractions import Fraction as F

import numpy as np
import pytest


GRAPHS = (
    ((0, 1),),
    ((0, 1), (1, 2)),
    ((0, 1), (0, 2), (0, 3)),
    ((0, 1), (1, 2), (2, 3), (3, 0)),
    ((0, 1), (1, 2), (2, 3), (3, 4), (1, 4)),
)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y, strict=True)), F(0))


def add(x, y, scale=F(1)):
    return [a + scale * b for a, b in zip(x, y, strict=True)]


def matvec(matrix, x):
    return [dot(row, x) for row in matrix]


def solve(matrix, rhs):
    """Small exact Gaussian elimination; no active-set continuation is used."""
    size = len(rhs)
    augmented = [list(row) + [value] for row, value in zip(matrix, rhs, strict=True)]
    for col in range(size):
        pivot = next(row for row in range(col, size) if augmented[row][col])
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        augmented[col] = [entry / divisor for entry in augmented[col]]
        for row in range(size):
            if row != col:
                factor = augmented[row][col]
                augmented[row] = add(augmented[row], augmented[col], -factor)
    return [row[-1] for row in augmented]


def instance(edges, alpha, mixture):
    size = 1 + max(itertools.chain.from_iterable(edges))
    adjacency = [[F(0) for _ in range(size)] for _ in range(size)]
    for left, right in edges:
        adjacency[left][right] = adjacency[right][left] = F(1)
    degrees = [sum(row) for row in adjacency]
    source = [F(0) for _ in range(size)]
    source[0] = F(2, 3) if mixture else F(1)
    if mixture:
        source[-1] = F(1, 3)
    hessian = [
        [
            (1 + alpha) * degrees[i] / 2 if i == j else -(1 - alpha) * adjacency[i][j] / 2
            for j in range(size)
        ]
        for i in range(size)
    ]
    operator = [[entry / degrees[i] for entry in row] for i, row in enumerate(hessian)]
    return adjacency, degrees, source, hessian, operator


def optimum(hessian, degrees, source, alpha, regularizer):
    """Enumerate all faces and accept the unique full KKT point."""
    size = len(degrees)
    load = [alpha * (s - regularizer * d) for s, d in zip(source, degrees, strict=True)]
    for mask in range(1 << size):
        support = [i for i in range(size) if mask & (1 << i)]
        point = [F(0) for _ in range(size)]
        if support:
            restricted = [[hessian[i][j] for j in support] for i in support]
            values = solve(restricted, [load[i] for i in support])
            for i, value in zip(support, values, strict=True):
                point[i] = value
        slack = add(matvec(hessian, point), load, F(-1))
        if all(x >= 0 and g >= 0 and x * g == 0 for x, g in zip(point, slack, strict=True)):
            return point
    raise AssertionError("No exact KKT basis was found")


def projection(raw, degrees, upper, mass):
    """Exhaustive breakpoint sweep, independent of the ordered-tree reporter."""

    def at(multiplier):
        return [min(upper, max(F(0), value - multiplier)) for value in raw]

    if dot(degrees, at(F(0))) <= mass:
        return at(F(0))
    points = sorted({F(0), *(max(F(0), x) for x in raw), *(max(F(0), x - upper) for x in raw)})
    for lo, hi in zip(points[:-1], points[1:], strict=True):
        mass_lo, mass_hi = dot(degrees, at(lo)), dot(degrees, at(hi))
        if mass_lo == mass:
            return at(lo)
        if mass_hi <= mass < mass_lo:
            multiplier = lo + (mass_lo - mass) * (hi - lo) / (mass_lo - mass_hi)
            return at(multiplier)
    raise AssertionError("Projection breakpoint sweep failed")


def feasible(rng, degrees, upper, mass):
    point = [upper * F(rng.randrange(9), 8) for _ in degrees]
    current = dot(degrees, point)
    if current > mass:
        point = [x * mass / current for x in point]
    return point


@pytest.mark.parametrize("edges", GRAPHS)
@pytest.mark.parametrize("mixture", (False, True))
def test_exact_two_metric_comparison_and_perturbations(edges, mixture):
    alpha, theta = F(1, 8), F(1, 4)
    curvature, contraction = theta**2, 1 - theta
    adjacency, degrees, seed, hessian, operator = instance(edges, alpha, mixture)
    regularizer = max(s / d for s, d in zip(seed, degrees, strict=True)) / 8
    load_scale = alpha * regularizer
    baseline = optimum(hessian, degrees, seed, alpha, 2 * regularizer)
    target = optimum(hessian, degrees, seed, alpha, regularizer)
    correction = add(target, baseline, F(-1))
    source = add(
        [alpha * s / d for s, d in zip(seed, degrees, strict=True)],
        matvec(operator, baseline),
        F(-1),
    )
    assert all(0 <= x <= 4 * load_scale for x in source)
    mass = dot(degrees, source) / alpha
    comparator = solve(hessian, [d * s for d, s in zip(degrees, source, strict=True)])
    upper = 4 * regularizer

    def objective(x):
        return dot(x, matvec(hessian, x)) / 2 - dot(
            [d * (s - load_scale) for d, s in zip(degrees, source, strict=True)], x
        )

    def auxiliary(x):
        response = add(matvec(operator, x), source, F(-1))
        return dot(degrees, [q * q for q in response]) / 2 + alpha * load_scale * dot(degrees, x)

    def energies(x, z):
        mirror = add(z, correction, F(-1))
        second_mirror = add(z, comparator, F(-1))
        return (
            objective(x)
            - objective(correction)
            + curvature * dot(degrees, [a * a for a in mirror]) / 2,
            auxiliary(x)
            - auxiliary(comparator)
            + curvature * dot(second_mirror, matvec(hessian, second_mirror)) / 2,
        )

    rng = random.Random(20260906 + len(degrees) + int(mixture))
    for attempt in range(12):
        x = correction if attempt == 0 else feasible(rng, degrees, upper, mass)
        z = comparator if attempt == 0 else feasible(rng, degrees, upper, mass)
        y = [(a + theta * b) / (1 + theta) for a, b in zip(x, z, strict=True)]
        gradient = add(matvec(operator, y), [load_scale - a for a in source])
        raw = [
            contraction * a + theta * b - g / theta for a, b, g in zip(z, y, gradient, strict=True)
        ]
        exact_projected = projection(raw, degrees, upper, mass)
        normal = add(raw, exact_projected, F(-1))
        assert (
            dot(
                add(exact_projected, correction, F(-1)),
                [d * a for d, a in zip(degrees, normal, strict=True)],
            )
            >= 0
        )
        assert dot(add(exact_projected, comparator, F(-1)), matvec(hessian, normal)) >= 0

        # Exact raw-flow identity in mass coordinates, including the optimum slack.
        slack = add(matvec(operator, correction), [load_scale - a for a in source])
        velocity_error = [
            theta * d * (a - b) for d, a, b in zip(degrees, z, correction, strict=True)
        ]
        walk = [
            (
                velocity_error[i]
                + sum(adjacency[i][j] * velocity_error[j] / degrees[j] for j in range(len(degrees)))
            )
            / 2
            for i in range(len(degrees))
        ]
        difference = add(x, correction, F(-1))
        response = add(matvec(operator, difference), difference, -curvature)
        forcing = [-d * q / (1 + theta) for d, q in zip(degrees, response, strict=True)]
        flow = [
            (1 - alpha) * w / (1 + theta) + h - d * ell
            for w, h, d, ell in zip(walk, forcing, degrees, slack, strict=True)
        ]
        assert flow == [
            theta * d * (q - u) for d, q, u in zip(degrees, raw, correction, strict=True)
        ]

        raw_error, projection_error, primal_error = F(1, 4096), F(1, 16384), F(1, 8192)
        perturbed = [q + raw_error * F(rng.randrange(-4, 5), 4) for q in raw]
        ideal = projection(perturbed, degrees, upper, mass)
        projected = [max(F(0), p - projection_error * F(rng.randrange(5), 4)) for p in ideal]
        next_x = [
            max(F(0), contraction * a + theta * p - primal_error * F(rng.randrange(5), 4))
            for a, p in zip(x, projected, strict=True)
        ]
        old_e, old_b = energies(x, z)
        next_e, next_b = energies(next_x, projected)
        error_budget = (
            2 * curvature * raw_error
            + F(5, 2) * primal_error
            + F(5, 2) * (theta + curvature) * projection_error
        )
        assert next_e <= contraction * old_e + error_budget
        assert next_b <= contraction * old_b + error_budget


@pytest.mark.parametrize("edges", GRAPHS)
@pytest.mark.parametrize("mixture", (False, True))
def test_exact_projected_gradient_repair_and_acl_residual(edges, mixture):
    alpha = F(1, 8)
    _, degrees, source, hessian, operator = instance(edges, alpha, mixture)
    rho = max(s / d for s, d in zip(source, degrees, strict=True)) / 8
    target = optimum(hessian, degrees, source, alpha, rho)
    delta = alpha * rho / 2
    tolerance = alpha * delta**2 / 8
    # A nonnegative candidate with a certified gap, found independently of any solver.
    for sign in (F(-1), F(1)):
        step = delta / (8 * sum(degrees))
        while True:
            candidate = [max(F(0), x + sign * step) for x in target]
            error = add(candidate, target, F(-1))
            target_slack = add(
                matvec(hessian, target),
                [alpha * (rho * d - s) for d, s in zip(degrees, source, strict=True)],
            )
            gap = dot(error, matvec(hessian, error)) / 2 + dot(target_slack, error)
            if gap <= tolerance:
                break
            step /= 2
        gradient = add(
            matvec(operator, candidate),
            [alpha * (rho - s / d) for s, d in zip(source, degrees, strict=True)],
        )
        pg = [max(F(0), x - g) for x, g in zip(candidate, gradient, strict=True)]
        grid = F(1, 2)
        while grid > min(delta / 2, alpha * rho / 8):
            grid /= 2
        repaired = [grid * (max(F(0), p - delta) // grid) for p in pg]
        residual = add(
            [alpha * s / d for s, d in zip(source, degrees, strict=True)],
            matvec(operator, repaired),
            F(-1),
        )
        assert all(0 <= x <= optimum_x for x, optimum_x in zip(repaired, target, strict=True))
        assert all(0 <= value <= 2 * alpha * rho for value in residual)
        repaired_error = add(repaired, target, F(-1))
        assert dot(repaired_error, matvec(hessian, repaired_error)) / 2 <= 2 * delta**2 / rho


def test_multisource_cholesky_depth_and_delayed_thresholds():
    rng = random.Random(20260906)
    tested = nonsingleton = 0
    for size in (5, 8, 13, 21):
        adjacency = np.zeros((size, size))
        for i in range(1, size):
            j = rng.randrange(i)
            adjacency[i, j] = adjacency[j, i] = 1
        degrees = adjacency.sum(axis=1)
        for alpha in (0.015625, 0.125, 0.75):
            for support_size in (2, min(4, size), size):
                source = np.zeros(size)
                labels = rng.sample(range(size), support_size)
                weights = np.array([rng.randrange(1, 20) for _ in labels], dtype=float)
                source[labels] = weights / weights.sum()
                for rho_fraction in (0.02, 0.3, 0.8):
                    rho = rho_fraction * np.max(source / degrees)
                    matrix = (1 + alpha) / 2 * np.eye(size) - (1 - alpha) / 2 * adjacency / np.sqrt(
                        degrees[:, None] * degrees[None, :]
                    )
                    load = alpha * (source / np.sqrt(degrees) - rho * np.sqrt(degrees))
                    for threshold in (0.0, 0.002 * alpha):
                        active = list(np.flatnonzero(load > 0))
                        blocks = [active.copy()]
                        faces = []
                        switched = False
                        while True:
                            point = np.zeros(size)
                            point[active] = np.linalg.solve(
                                matrix[np.ix_(active, active)], load[active]
                            )
                            faces.append(point)
                            residual = load - matrix @ point
                            new = [
                                i
                                for i in range(size)
                                if i not in active
                                and residual[i] > (1e-12 if switched else max(1e-12, threshold))
                            ]
                            if not new and not switched:
                                switched = True
                                new = [
                                    i
                                    for i in range(size)
                                    if i not in active and residual[i] > 1e-12
                                ]
                            if not new:
                                break
                            blocks.append(new)
                            active.extend(new)
                        assert np.min(point) >= -1e-10
                        assert np.min(matrix @ point - load) >= -1e-10
                        principal = matrix[np.ix_(active, active)]
                        chol = np.linalg.cholesky(principal)
                        chain = np.zeros_like(chol)
                        endpoints = np.cumsum([0] + [len(block) for block in blocks])
                        slices = [
                            slice(a, b) for a, b in zip(endpoints[:-1], endpoints[1:], strict=True)
                        ]
                        for j, current in enumerate(slices):
                            chain[current, current] = chol[current, current]
                            if j:
                                chain[current, slices[j - 1]] = chol[current, slices[j - 1]]
                        transformed = np.linalg.solve(chol, load[active])
                        forcing = chain @ transformed
                        assert np.max(forcing[endpoints[1] :], initial=0) <= threshold + 1e-10
                        assert np.linalg.norm(chain, 2) <= np.sqrt(2) + 1e-10
                        assert np.linalg.svd(chain, compute_uv=False)[-1] >= np.sqrt(alpha) - 1e-10
                        assert np.max(np.linalg.inv(chain) - np.linalg.inv(chol)) <= 1e-9
                        decay = (np.sqrt(2 / alpha) - 1) / (np.sqrt(2 / alpha) + 1)
                        for j, face in enumerate(faces):
                            error = point - face
                            gap = 0.5 * error @ matrix @ error
                            tail = 0.5 * np.sum(transformed[endpoints[j + 1] :] ** 2)
                            assert abs(gap - tail) < 1e-9
                            assert gap <= 8 * decay ** (2 * j) + threshold**2 / (alpha * rho) + 1e-9
                        tested += 1
                        nonsingleton += len(blocks[0]) > 1
    assert tested == 216
    assert nonsingleton > 100
