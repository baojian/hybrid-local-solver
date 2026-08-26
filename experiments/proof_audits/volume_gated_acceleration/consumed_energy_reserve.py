#!/usr/bin/env python3
"""Audit the consumed-energy reserve, quartic certificates, and small-q STOP.

The fast path checks the committed six-vertex witness, exact rational
specializations of the leaf-seeded ``K_{1,4}`` formulas, and the reachable
quartic ``K_{2,r}``-plus-leaf family.  ``--enumerate`` also checks every seed
of every connected NetworkX graph-atlas representative on two through seven
vertices at ``q=1/5``.  The atlas is finite evidence, not an asymptotic or
graph-uniform theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import comb

import networkx as nx

from experiments.proof_audits.volume_gated_acceleration.nonpath_causal_stop import (
    ZERO,
    apply_h,
    boundary,
    degrees_from_edges,
    neighbors_from_edges,
    objective,
    one_step,
    residual,
    restricted_optimum,
    solve_fraction,
)


THREE_ADMISSION_EDGES = (
    (0, 2),
    (0, 5),
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 4),
    (4, 5),
)
STAR_FOUR_EDGES = ((0, 1), (1, 2), (1, 3), (1, 4))
STAR_FIVE_EDGES = ((0, 5), (1, 5), (2, 5), (3, 5), (4, 5))
QUARTIC_EDGES = (
    (0, 2),
    (1, 2),
    (1, 4),
    (2, 3),
    (2, 5),
    (3, 4),
    (4, 5),
)

WITNESS_MINIMUM = Fraction(
    1772625800261634289972166085525,
    136208548497122966464402947962896,
)
ATLAS_MAXIMUM = Fraction(2786829024075210327, 1036704485947225385)

BERNSTEIN_DETERMINANT = (
    (
        0,
        0,
        0,
        0,
        Fraction(1, 70),
        Fraction(5, 63),
        Fraction(9, 35),
        Fraction(13, 20),
        Fraction(13, 9),
        Fraction(14, 5),
        4,
    ),
    (
        0,
        0,
        Fraction(4, 225),
        Fraction(3, 50),
        Fraction(149, 1050),
        Fraction(187, 630),
        Fraction(613, 1050),
        Fraction(163, 150),
        Fraction(17, 9),
        Fraction(74, 25),
        4,
    ),
    (
        0,
        Fraction(1, 50),
        Fraction(11, 150),
        Fraction(7, 40),
        Fraction(29, 84),
        Fraction(257, 420),
        Fraction(353, 350),
        Fraction(469, 300),
        Fraction(57, 25),
        Fraction(78, 25),
        4,
    ),
    (
        0,
        Fraction(2, 25),
        Fraction(16, 75),
        Fraction(31, 75),
        Fraction(29, 42),
        Fraction(331, 315),
        Fraction(157, 105),
        Fraction(101, 50),
        Fraction(589, 225),
        Fraction(82, 25),
        4,
    ),
    (
        Fraction(1, 5),
        Fraction(9, 25),
        Fraction(128, 225),
        Fraction(83, 100),
        Fraction(601, 525),
        Fraction(953, 630),
        Fraction(338, 175),
        Fraction(719, 300),
        Fraction(653, 225),
        Fraction(86, 25),
        4,
    ),
    (
        0,
        Fraction(1, 5),
        Fraction(7, 15),
        Fraction(4, 5),
        Fraction(251, 210),
        Fraction(23, 14),
        Fraction(149, 70),
        Fraction(79, 30),
        Fraction(47, 15),
        Fraction(18, 5),
        4,
    ),
)


def transported_energy(
    iterate,
    center,
    active,
    optimum,
    seed,
    neighbors,
    degrees,
    alpha,
    rho,
):
    """Evaluate the exact normalized transported-center energy."""
    primal_gap = objective(
        iterate,
        active,
        seed,
        neighbors,
        degrees,
        alpha,
        rho,
    ) - objective(
        optimum,
        active,
        seed,
        neighbors,
        degrees,
        alpha,
        rho,
    )
    center_gap = alpha * sum(
        (
            Fraction(degrees[vertex], 2) * (value - optimum_value) ** 2
            for vertex, value, optimum_value in zip(active, center, optimum)
        ),
        ZERO,
    )
    return primal_gap + center_gap


def replay_with_reserve(order, edges, seed, q=Fraction(1, 5), max_stages=500):
    """Replay the exact recurrence and retain every reserve checkpoint."""
    alpha = q * q
    rho = tau = q / 5
    degrees = degrees_from_edges(order, edges)
    neighbors = neighbors_from_edges(order, edges)
    active = [seed]
    iterate = [ZERO]
    center = [ZERO]
    optimum = restricted_optimum(active, seed, neighbors, degrees, alpha, rho)
    initial_energy = transported_energy(
        iterate,
        center,
        active,
        optimum,
        seed,
        neighbors,
        degrees,
        alpha,
        rho,
    )
    credit = ZERO
    last_energy = initial_energy
    last_reserve = ZERO
    checkpoints = []
    snapshots = {}
    admissions = []

    for stage in range(1, max_stages + 1):
        active_before = active[:]
        optimum_before = optimum[:]
        stepped = one_step(
            iterate,
            center,
            active,
            seed,
            neighbors,
            degrees,
            q,
            rho,
        )
        if stepped is None:
            return None
        candidate, center_next = stepped
        active_residual = residual(
            candidate,
            active,
            seed,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        delta = max(ZERO, max(active_residual) / alpha)
        score = delta * delta
        energy_before_admission = transported_energy(
            candidate,
            center_next,
            active,
            optimum,
            seed,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        reserve_before_admission = initial_energy + credit - energy_before_admission
        assert energy_before_admission <= (1 - q) * last_energy
        assert reserve_before_admission - last_reserve == last_energy - energy_before_admission
        assert reserve_before_admission >= last_reserve >= 0
        checkpoints.append(
            (
                f"{stage}-",
                score,
                credit - score,
                energy_before_admission,
                credit,
                reserve_before_admission,
            )
        )

        envelope = [max(ZERO, value - delta) for value in candidate]
        envelope_residual = residual(
            envelope,
            active,
            seed,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        position = {vertex: index for index, vertex in enumerate(active)}
        outside_residual = {}
        for vertex in boundary(active, neighbors):
            incoming = sum(
                (envelope[position[other]] for other in neighbors[vertex] if other in position),
                ZERO,
            )
            outside_residual[vertex] = -(1 - alpha) * incoming / (2 * degrees[vertex]) + alpha * rho
        admitted = sorted(
            vertex for vertex, value in outside_residual.items() if value < -alpha * tau
        )
        drop = ZERO
        post_delta = delta
        energy_after_admission = energy_before_admission
        if admitted:
            action = "admit"
            admissions.append((stage, tuple(admitted)))
            active = active + admitted
            new_optimum = restricted_optimum(
                active,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            )
            old_optimum = dict(zip(active_before, optimum_before))
            old_candidate = dict(zip(active_before, candidate))
            old_center = dict(zip(active_before, center_next))
            padded_optimum = [old_optimum.get(vertex, ZERO) for vertex in active]
            iterate = [old_candidate.get(vertex, ZERO) for vertex in active]
            padded_center = [old_center.get(vertex, ZERO) for vertex in active]
            displacement = [
                new_value - old_value for new_value, old_value in zip(new_optimum, padded_optimum)
            ]
            center = [value + shift for value, shift in zip(padded_center, displacement)]
            optimum = new_optimum
            drop = objective(
                padded_optimum,
                active,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            ) - objective(
                new_optimum,
                active,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            )
            credit += drop
            post_residual = residual(
                iterate,
                active,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            )
            post_delta = max(ZERO, max(post_residual) / alpha)
            post_score = post_delta * post_delta
            energy_after_admission = transported_energy(
                iterate,
                center,
                active,
                optimum,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            )
            reserve_after_admission = initial_energy + credit - energy_after_admission
            assert energy_after_admission == energy_before_admission + drop
            assert reserve_after_admission == reserve_before_admission
            assert post_score == score
            checkpoints.append(
                (
                    f"{stage}+",
                    post_score,
                    credit - post_score,
                    energy_after_admission,
                    credit,
                    reserve_after_admission,
                )
            )
            last_energy = energy_after_admission
            last_reserve = reserve_after_admission
        elif min(envelope_residual) >= -alpha * tau:
            action = "certify"
            iterate, center = candidate, center_next
            last_energy = energy_before_admission
            last_reserve = reserve_before_admission
        else:
            action = "hold"
            iterate, center = candidate, center_next
            last_energy = energy_before_admission
            last_reserve = reserve_before_admission

        snapshots[stage] = {
            "action": action,
            "active": tuple(active_before),
            "admitted": tuple(admitted),
            "candidate": tuple(candidate),
            "delta": delta,
            "post_delta": post_delta,
            "drop": drop,
            "energy_before_admission": energy_before_admission,
            "energy_after_admission": energy_after_admission,
        }
        if action == "certify" or stage == max_stages:
            return {
                "checkpoints": checkpoints,
                "snapshots": snapshots,
                "admissions": admissions,
                "initial_energy": initial_energy,
                "credit": credit,
                "terminal_stage": stage if action == "certify" else None,
            }
    raise AssertionError("unreachable")


def required_coefficient(run):
    """Return the exact finite-trace minimum coefficient and checkpoint."""
    requirements = []
    for label, _score, balance, _energy, _credit, reserve in run["checkpoints"]:
        if balance < 0:
            assert reserve > 0
            requirements.append((-balance / reserve, label, -balance, reserve))
    return max(requirements, default=(ZERO, None, ZERO, ZERO))


def polynomial_value(coefficients, q):
    """Evaluate low-to-high exact polynomial coefficients by Horner's rule."""
    value = ZERO
    for coefficient in reversed(coefficients):
        value = value * q + coefficient
    return value


def series_multiply(left, right, order):
    """Multiply truncated exact power series."""
    result = [ZERO] * order
    for left_index, left_value in enumerate(left[:order]):
        for right_index, right_value in enumerate(right[: order - left_index]):
            result[left_index + right_index] += left_value * right_value
    return result


def series_inverse(series, order):
    """Invert a truncated exact power series with nonzero constant term."""
    assert series[0]
    result = [ZERO] * order
    result[0] = Fraction(1, 1) / series[0]
    for index in range(1, order):
        result[index] = (
            -sum(
                (
                    series[offset] * result[index - offset]
                    for offset in range(1, min(index + 1, len(series)))
                ),
                ZERO,
            )
            / series[0]
        )
    return result


def series_divide(numerator, denominator, order):
    """Return the exact truncated series of one polynomial quotient."""
    return series_multiply(numerator, series_inverse(denominator, order), order)


def series_add_values(left, right, order):
    """Add two exact truncated power series."""
    return [
        (left[index] if index < len(left) else ZERO)
        + (right[index] if index < len(right) else ZERO)
        for index in range(order)
    ]


def series_subtract(left, right, order):
    """Subtract two exact truncated power series."""
    return [
        (left[index] if index < len(left) else ZERO)
        - (right[index] if index < len(right) else ZERO)
        for index in range(order)
    ]


def series_scale(series, scalar, order):
    """Scale an exact truncated power series."""
    return [scalar * (series[index] if index < len(series) else ZERO) for index in range(order)]


def series_shift(series, order):
    """Multiply an exact truncated power series by its variable."""
    return [ZERO, *series[: order - 1]]


def series_matrix_solve(matrix, right_hand_side, order):
    """Solve a square system over exact truncated power series."""
    size = len(right_hand_side)
    augmented = [
        [[*entry[:order], *([ZERO] * (order - len(entry)))] for entry in row]
        + [[*value[:order], *([ZERO] * (order - len(value)))]]
        for row, value in zip(matrix, right_hand_side)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column][0])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse = series_inverse(augmented[column][column], order)
        augmented[column] = [series_multiply(entry, inverse, order) for entry in augmented[column]]
        for row in range(size):
            if row == column or not any(augmented[row][column]):
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                series_subtract(
                    entry,
                    series_multiply(multiplier, pivot_entry, order),
                    order,
                )
                for entry, pivot_entry in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(size)]


P = (-5, 23, -56, 72, -59, 9)
P_DEBT = (
    25,
    -330,
    1759,
    -7852,
    27077,
    -63382,
    110787,
    -156264,
    165371,
    -136886,
    83213,
    -35308,
    9511,
    -1386,
    81,
)
A_RESERVE = (
    1800,
    8415,
    17298,
    47652,
    156238,
    11221,
    834896,
    -1158068,
    3155456,
    -5015994,
    7379436,
    -8729164,
    8711380,
    -7264518,
    5080528,
    -2980028,
    1452888,
    -575637,
    180450,
    -41832,
    5886,
    -351,
)


def star_formula_values(q):
    """Evaluate the proposition's exact rational star formulas."""
    p_value = polynomial_value(P, q)
    debt_polynomial = polynomial_value(P_DEBT, q)
    reserve_polynomial = polynomial_value(A_RESERVE, q)
    score = (1 - q) ** 4 * p_value**2 / (6400 * (1 + q * q) ** 2)
    credit = q**2 * (73 * q**4 + 80 * q**3 + 14 * q**2 - 80 * q + 25) / (400 * (1 + q * q))
    initial_energy = q**4 * (q - 5) ** 2 * (3 * q**2 + 1) / (25 * (1 + q * q) ** 2)
    reserve = (
        q**3
        * reserve_polynomial
        / (1600 * (1 + q * q) ** 2 * (q * q + 3) ** 2 * (3 * q * q + 1) ** 2)
    )
    debt = debt_polynomial / (6400 * (1 + q * q) ** 2)
    coefficient = (
        (q * q + 3) ** 2 * (3 * q * q + 1) ** 2 * debt_polynomial / (4 * q**3 * reserve_polynomial)
    )
    return score, credit, initial_energy, reserve, debt, coefficient


def polynomial_add(*polynomials):
    """Add sparse exact bivariate polynomials keyed by ``(q,t)`` degree."""
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, ZERO) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def polynomial_scale(polynomial, scalar):
    """Scale a sparse exact bivariate polynomial."""
    return {monomial: scalar * coefficient for monomial, coefficient in polynomial.items()}


def polynomial_multiply(left, right):
    """Multiply sparse exact bivariate polynomials."""
    result = {}
    for (left_q, left_t), left_value in left.items():
        for (right_q, right_t), right_value in right.items():
            monomial = (left_q + right_q, left_t + right_t)
            result[monomial] = result.get(monomial, ZERO) + left_value * right_value
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def polynomial_power(polynomial, exponent):
    """Raise a sparse exact bivariate polynomial to a nonnegative power."""
    result = {(0, 0): Fraction(1)}
    for _ in range(exponent):
        result = polynomial_multiply(result, polynomial)
    return result


def bernstein_decrement_check():
    """Verify the exact Bernstein certificate for the inactive q^-4 lemma."""
    q_polynomial = {(1, 0): Fraction(1)}
    t_polynomial = {(0, 1): Fraction(1)}
    one = {(0, 0): Fraction(1)}
    q_squared = polynomial_power(q_polynomial, 2)
    eigenvalue = polynomial_add(
        q_squared,
        polynomial_multiply(
            polynomial_add(one, polynomial_scale(q_squared, -1)),
            t_polynomial,
        ),
    )

    def term(coefficient, eigenvalue_power, q_power):
        return polynomial_scale(
            polynomial_multiply(
                polynomial_power(eigenvalue, eigenvalue_power),
                polynomial_power(q_polynomial, q_power),
            ),
            coefficient,
        )

    determinant = polynomial_add(
        term(-1, 5, 0),
        term(1, 4, 2),
        term(-2, 4, 1),
        term(1, 4, 0),
        term(-1, 3, 2),
        term(2, 3, 1),
        term(-1, 2, 2),
        term(2, 2, 1),
        term(4, 1, 2),
        term(-1, 0, 4),
    )
    quadratic_a = polynomial_add(eigenvalue, polynomial_scale(q_squared, -1), term(2, 0, 1))
    quadratic_b = polynomial_add(
        polynomial_multiply(eigenvalue, q_polynomial),
        polynomial_scale(eigenvalue, -1),
        term(-2, 0, 1),
    )
    quadratic_c = polynomial_add(
        polynomial_scale(polynomial_power(eigenvalue, 4), -1),
        polynomial_power(eigenvalue, 3),
        eigenvalue,
        q_squared,
        term(2, 0, 1),
    )
    assert (
        polynomial_add(
            polynomial_multiply(quadratic_a, quadratic_c),
            polynomial_scale(polynomial_power(quadratic_b, 2), -1),
            polynomial_scale(determinant, -1),
        )
        == {}
    )
    assert max(q_degree for q_degree, _ in determinant) <= 10
    assert max(t_degree for _, t_degree in determinant) <= 5

    converted = []
    for t_index in range(6):
        row = []
        for q_index in range(11):
            coefficient = sum(
                (
                    value
                    * Fraction(comb(q_index, q_degree), comb(10, q_degree))
                    * Fraction(comb(t_index, t_degree), comb(5, t_degree))
                    for (q_degree, t_degree), value in determinant.items()
                    if q_degree <= q_index and t_degree <= t_index
                ),
                ZERO,
            )
            row.append(coefficient)
        converted.append(tuple(row))
    assert tuple(converted) == BERNSTEIN_DETERMINANT
    assert all(coefficient >= 0 for row in converted for coefficient in row)


def projection_active_stop_check():
    """Verify the original-score projected q^-4 STOP and support repair."""
    q = Fraction(1, 100)
    alpha = q * q
    active = [0, 1, 2]
    edges = ((0, 1), (0, 2))
    neighbors = neighbors_from_edges(3, edges)
    degrees = degrees_from_edges(3, edges)
    rho = Fraction(269947, 1080080)
    seed_distribution = (
        Fraction(1, 27002),
        Fraction(1010067, 1080080),
        Fraction(69973, 1080080),
    )
    assert sum(seed_distribution, ZERO) == 1
    normalized_load = [
        alpha * (mass / degree - rho) for mass, degree in zip(seed_distribution, degrees)
    ]
    optimum = [Fraction(1, 23480), Fraction(97, 540040), Fraction(3, 540040)]
    assert apply_h(optimum, active, neighbors, degrees, alpha) == normalized_load

    iterate = [Fraction(1, 270020), Fraction(29, 270020), ZERO]
    center = [
        Fraction(31, 54004),
        Fraction(737, 540040),
        Fraction(8, 67505),
    ]
    interpolation = [
        (value + q * center_value) / (1 + q) for value, center_value in zip(iterate, center)
    ]
    assert interpolation == [
        Fraction(51, 5454404),
        Fraction(6537, 54544040),
        Fraction(8, 6818005),
    ]
    interpolation_residual = [
        image - load_value
        for image, load_value in zip(
            apply_h(interpolation, active, neighbors, degrees, alpha),
            normalized_load,
        )
    ]
    raw_candidate = [
        value - derivative for value, derivative in zip(interpolation, interpolation_residual)
    ]
    assert raw_candidate == [
        Fraction(1717, 172812800),
        Fraction(1437773, 10800800000),
        -Fraction(35787, 2700200000),
    ]
    candidate = [max(ZERO, value) for value in raw_candidate]
    assert candidate[-1] == 0 and all(value > 0 for value in candidate[:-1])
    center_next = [new + (1 - q) * (new - old) / q for new, old in zip(candidate, iterate)]
    post_residual = [
        image - load_value
        for image, load_value in zip(
            apply_h(candidate, active, neighbors, degrees, alpha),
            normalized_load,
        )
    ]
    assert post_residual == [
        -Fraction(31146687, 9392000000000),
        -Fraction(2992499829, 432032000000000),
        Fraction(46823397, 3456256000000),
    ]

    def error_energy(point, point_center):
        error = [value - optimum_value for value, optimum_value in zip(point, optimum)]
        center_error = [
            value - optimum_value for value, optimum_value in zip(point_center, optimum)
        ]
        image = apply_h(error, active, neighbors, degrees, alpha)
        return sum(
            (
                Fraction(degree, 2) * left * right + Fraction(alpha * degree, 2) * center_value**2
                for degree, left, right, center_value in zip(
                    degrees,
                    error,
                    image,
                    center_error,
                )
            ),
            ZERO,
        )

    energy = error_energy(iterate, center)
    energy_next = error_energy(candidate, center_next)
    assert energy == Fraction(3820147, 5832864032000000)
    assert energy_next == Fraction(
        5396449315539933,
        9332582451200000000000000,
    )
    original_score_numerator = max(ZERO, max(post_residual)) ** 2
    twice_drop = 2 * (energy - energy_next)
    assert original_score_numerator == Fraction(
        2192430506619609,
        11945705537536000000000000,
    )
    assert twice_drop == Fraction(
        715785884460067,
        4666291225600000000000000,
    )
    assert (
        original_score_numerator - twice_drop
        == Fraction(
            9000466060045937,
            298642638438400000000000000,
        )
        > 0
    )
    assert (
        (1 - q) * energy - energy_next
        == Fraction(
            654663532460067,
            9332582451200000000000000,
        )
        > 0
    )

    supported_residuals = [
        derivative for value, derivative in zip(candidate, post_residual) if value > 0
    ]
    assert max(ZERO, max(supported_residuals)) == 0
    assert all(value <= optimum_value for value, optimum_value in zip(candidate, optimum))


def witness_check():
    """Reproduce the exact reserve and minimum on the committed witness."""
    run = replay_with_reserve(6, THREE_ADMISSION_EDGES, 0)
    assert run is not None
    assert run["initial_energy"] == Fraction(3703, 5281250)
    assert run["credit"] == Fraction(1305901, 5362906250)
    requirement = required_coefficient(run)
    assert requirement[:2] == (WITNESS_MINIMUM, "7-")
    assert requirement[2] == Fraction(
        22103647843883061483647,
        1825088026185798645019531250,
    )
    assert requirement[3] == Fraction(
        5238790326812421787092421075496,
        5629419085753779695034027099609375,
    )
    assert WITNESS_MINIMUM < 1


def star_check():
    """Check the actual chronology, formulas, and q^-3 leading constant."""
    for q in (Fraction(1, 100), Fraction(1, 80), Fraction(1, 50)):
        run = replay_with_reserve(5, STAR_FOUR_EDGES, 0, q=q, max_stages=3)
        assert run is not None
        snapshots = run["snapshots"]
        assert snapshots[1]["action"] == "admit"
        assert snapshots[1]["admitted"] == (1,)
        assert snapshots[2]["action"] == "admit"
        assert snapshots[2]["admitted"] == (2, 3, 4)
        assert snapshots[3]["action"] == "hold"
        assert snapshots[3]["active"] == (0, 1, 2, 3, 4)
        assert all(min(snapshots[stage]["candidate"]) > 0 for stage in (1, 2, 3))
        delta = snapshots[3]["delta"]
        assert all(max(ZERO, value - delta) == 0 for value in snapshots[3]["candidate"])

        stage_three = next(row for row in run["checkpoints"] if row[0] == "3-")
        score, credit, initial_energy, reserve, debt, coefficient = star_formula_values(q)
        assert stage_three[1] == score
        assert stage_three[4] == credit
        assert run["initial_energy"] == initial_energy
        assert stage_three[5] == reserve
        assert -stage_three[2] == debt == score - credit
        assert coefficient == debt / reserve

    # Exact Taylor coefficients from the displayed rational functions.
    one_plus_q_squared = [1, 0, 1]
    score_numerator = series_multiply(
        series_multiply([1, -4, 6, -4, 1], list(P), 8),
        list(P),
        8,
    )
    score_denominator = [
        6400 * value
        for value in series_multiply(
            one_plus_q_squared,
            one_plus_q_squared,
            8,
        )
    ]
    assert series_divide(score_numerator, score_denominator, 4) == [
        Fraction(1, 256),
        -Fraction(33, 640),
        Fraction(2109, 6400),
        -Fraction(1059, 800),
    ]

    credit_numerator = [0, 0, 25, -80, 14, 80, 73]
    credit_denominator = [400, 0, 400]
    assert series_divide(credit_numerator, credit_denominator, 5)[2:] == [
        Fraction(1, 16),
        -Fraction(1, 5),
        -Fraction(11, 400),
    ]

    reserve_denominator = [1600]
    for factor in ([1, 0, 1], [1, 0, 1], [3, 0, 1], [3, 0, 1], [1, 0, 3], [1, 0, 3]):
        reserve_denominator = series_multiply(reserve_denominator, factor, 6)
    reserve_series = series_divide([ZERO, ZERO, ZERO, *A_RESERVE], reserve_denominator, 6)
    assert reserve_series[3:] == [
        Fraction(1, 8),
        Fraction(187, 320),
        Fraction(283, 2400),
    ]

    debt_denominator = [
        6400 * value
        for value in series_multiply(
            one_plus_q_squared,
            one_plus_q_squared,
            4,
        )
    ]
    assert series_divide(list(P_DEBT), debt_denominator, 4) == [
        Fraction(1, 256),
        -Fraction(33, 640),
        Fraction(1709, 6400),
        -Fraction(899, 800),
    ]

    numerator = [1]
    for factor in ([3, 0, 1], [3, 0, 1], [1, 0, 3], [1, 0, 3], P_DEBT):
        numerator = series_multiply(numerator, list(factor), 4)
    denominator = [4 * value for value in A_RESERVE]
    assert series_divide(numerator, denominator, 4) == [
        Fraction(1, 32),
        -Fraction(143, 256),
        Fraction(144943, 30720),
        -Fraction(2464299, 81920),
    ]


def quartic_lower_check():
    """Verify the reachable q^-4 lower family and its exact leading series."""
    order = 2
    graph_order = 6
    degrees = degrees_from_edges(graph_order, QUARTIC_EDGES)
    neighbors = neighbors_from_edges(graph_order, QUARTIC_EDGES)
    assert degrees == [1, 2, 4, 2, 3, 2]
    faces = ([0], [0, 2], [0, 2, 1, 3, 5])

    def formal_matrix(active):
        position = {vertex: index for index, vertex in enumerate(active)}
        matrix = [[[ZERO] * order for _ in active] for _ in active]
        for row, vertex in enumerate(active):
            matrix[row][row] = [Fraction(1, 2), ZERO]
            for other in neighbors[vertex]:
                if other in position:
                    matrix[row][position[other]] = [
                        -Fraction(1, 2 * degrees[vertex]),
                        ZERO,
                    ]
        return matrix

    def formal_load(active):
        return [[Fraction(1) if vertex == 0 else ZERO, -Fraction(1, 5)] for vertex in active]

    def formal_apply(matrix, vector):
        result = []
        for row in matrix:
            value = [ZERO] * order
            for entry, coordinate in zip(row, vector):
                value = series_add_values(
                    value,
                    series_multiply(entry, coordinate, order),
                    order,
                )
            result.append(value)
        return result

    def formal_optimum(active):
        return series_matrix_solve(formal_matrix(active), formal_load(active), order)

    def formal_pad(vector, old, new):
        values = dict(zip(old, vector))
        return [values.get(vertex, [ZERO] * order) for vertex in new]

    def formal_step(active, iterate, center):
        interpolation = [
            series_divide(
                series_add_values(value, center_value, order),
                [Fraction(1), Fraction(1)],
                order,
            )
            for value, center_value in zip(iterate, center)
        ]
        gradient = [
            series_subtract(image, load_value, order)
            for image, load_value in zip(
                formal_apply(formal_matrix(active), interpolation),
                formal_load(active),
            )
        ]
        candidate = [
            series_subtract(value, derivative, order)
            for value, derivative in zip(interpolation, gradient)
        ]
        center_next = [
            series_add_values(
                series_shift(new, order),
                series_multiply(
                    [Fraction(1), -Fraction(1)],
                    series_subtract(new, old, order),
                    order,
                ),
                order,
            )
            for new, old in zip(candidate, iterate)
        ]
        return candidate, center_next

    def formal_transport(iterate, center, old, new):
        old_optimum = formal_optimum(old)
        new_optimum = formal_optimum(new)
        padded_optimum = formal_pad(old_optimum, old, new)
        displacement = [
            series_subtract(new_value, old_value, order)
            for new_value, old_value in zip(new_optimum, padded_optimum)
        ]
        return (
            formal_pad(iterate, old, new),
            [
                series_add_values(value, series_shift(shift, order), order)
                for value, shift in zip(formal_pad(center, old, new), displacement)
            ],
        )

    def formal_objective(active, point):
        image = formal_apply(formal_matrix(active), point)
        value = [ZERO] * order
        for vertex, coordinate, applied, load_value in zip(
            active,
            point,
            image,
            formal_load(active),
        ):
            quadratic = series_scale(
                series_multiply(coordinate, applied, order),
                Fraction(degrees[vertex], 2),
                order,
            )
            linear = series_scale(
                series_multiply(load_value, coordinate, order),
                degrees[vertex],
                order,
            )
            value = series_add_values(value, series_subtract(quadratic, linear, order), order)
        return value

    def formal_energy(active, iterate, center):
        optimum = formal_optimum(active)
        error = [
            series_subtract(value, optimum_value, order)
            for value, optimum_value in zip(iterate, optimum)
        ]
        image = formal_apply(formal_matrix(active), error)
        value = [ZERO] * order
        for vertex, coordinate, applied, center_value, optimum_value in zip(
            active,
            error,
            image,
            center,
            optimum,
        ):
            primal = series_scale(
                series_multiply(coordinate, applied, order),
                Fraction(degrees[vertex], 2),
                order,
            )
            center_error = series_subtract(
                center_value,
                series_shift(optimum_value, order),
                order,
            )
            center_term = series_scale(
                series_multiply(center_error, center_error, order),
                Fraction(degrees[vertex], 2),
                order,
            )
            value = series_add_values(value, series_add_values(primal, center_term, order), order)
        return value

    iterate = [[ZERO] * order]
    center = [[ZERO] * order]
    initial_energy = formal_energy(faces[0], iterate, center)
    formal_states = []
    iterate, center = formal_step(faces[0], iterate, center)
    formal_states.append((faces[0], iterate, center))
    iterate, center = formal_transport(iterate, center, faces[0], faces[1])
    iterate, center = formal_step(faces[1], iterate, center)
    formal_states.append((faces[1], iterate, center))
    iterate, center = formal_transport(iterate, center, faces[1], faces[2])
    iterate, center = formal_step(faces[2], iterate, center)
    formal_states.append((faces[2], iterate, center))
    iterate, center = formal_step(faces[2], iterate, center)
    formal_states.append((faces[2], iterate, center))

    expected_candidates = (
        ((1, -Fraction(1, 5)),),
        ((2, -Fraction(11, 15)), (Fraction(1, 4), -Fraction(1, 12))),
        (
            (Fraction(11, 4), -Fraction(3, 2)),
            (Fraction(5, 8), -Fraction(11, 40)),
            (Fraction(1, 8), Fraction(2, 15)),
            (Fraction(1, 8), Fraction(2, 15)),
            (Fraction(1, 8), Fraction(2, 15)),
        ),
        (
            (Fraction(13, 4), -Fraction(323, 120)),
            (Fraction(33, 32), -Fraction(611, 480)),
            (Fraction(3, 8), -Fraction(119, 240)),
            (Fraction(3, 8), -Fraction(119, 240)),
            (Fraction(3, 8), -Fraction(119, 240)),
        ),
    )
    expected_residuals = (
        ((-Fraction(1, 2), Fraction(1, 10)),),
        (
            (-Fraction(1, 8), -Fraction(1, 8)),
            (-Fraction(1, 8), Fraction(1, 4)),
        ),
        (
            (Fraction(1, 16), -Fraction(33, 80)),
            (-Fraction(5, 64), Fraction(1, 5)),
            (-Fraction(3, 32), Fraction(161, 480)),
            (-Fraction(3, 32), Fraction(161, 480)),
            (-Fraction(3, 32), Fraction(161, 480)),
        ),
        (
            (Fraction(7, 64), -Fraction(163, 320)),
            (-Fraction(1, 32), Fraction(11, 128)),
            (-Fraction(9, 128), Fraction(173, 640)),
            (-Fraction(9, 128), Fraction(173, 640)),
            (-Fraction(9, 128), Fraction(173, 640)),
        ),
    )
    for (active, candidate, _), expected_candidate, expected_residual in zip(
        formal_states,
        expected_candidates,
        expected_residuals,
    ):
        post_residual = [
            series_subtract(image, load_value, order)
            for image, load_value in zip(
                formal_apply(formal_matrix(active), candidate),
                formal_load(active),
            )
        ]
        assert tuple(map(tuple, candidate)) == expected_candidate
        assert tuple(map(tuple, post_residual)) == expected_residual

    stage_four_seed_residual = list(expected_residuals[3][0])
    stage_four_score = series_multiply(stage_four_seed_residual, stage_four_seed_residual, order)
    assert stage_four_score == [Fraction(49, 4096), -Fraction(1141, 10240)]
    credit = series_subtract(
        formal_objective(faces[0], formal_optimum(faces[0])),
        formal_objective(faces[2], formal_optimum(faces[2])),
        order,
    )
    assert credit == [Fraction(2, 3), -Fraction(32, 15)]
    energy_four = formal_energy(faces[2], formal_states[3][1], formal_states[3][2])
    assert initial_energy == [Fraction(1), -Fraction(2, 5)]
    assert energy_four == [Fraction(2207, 3072), -Fraction(18281, 3072)]
    reserve = series_subtract(series_add_values(initial_energy, credit, order), energy_four, order)
    assert reserve == [Fraction(971, 1024), Fraction(52493, 15360)]
    limiting_constant = stage_four_score[0] / reserve[0]
    assert limiting_constant == Fraction(49, 3884)

    previous_scaled_requirement = ZERO
    for denominator in (20, 40, 80, 160, 320, 640):
        q = Fraction(1, denominator)
        run = replay_with_reserve(graph_order, QUARTIC_EDGES, 0, q=q, max_stages=16)
        assert run is not None
        assert run["admissions"] == [(1, (2,)), (2, (1, 3, 5)), (15, (4,))]
        assert [run["snapshots"][stage]["action"] for stage in range(1, 5)] == [
            "admit",
            "admit",
            "hold",
            "hold",
        ]
        assert all(min(run["snapshots"][stage]["candidate"]) > 0 for stage in range(1, 5))
        requirement = required_coefficient(run)
        assert requirement[1] == "4-"
        scaled_requirement = q**4 * requirement[0]
        assert previous_scaled_requirement < scaled_requirement < limiting_constant
        previous_scaled_requirement = scaled_requirement

        snapshot = run["snapshots"][4]
        active = list(snapshot["active"])
        post_residual = residual(
            snapshot["candidate"],
            active,
            0,
            neighbors,
            degrees,
            q * q,
            q / 5,
        )
        support_delta = max(
            ZERO,
            max(
                value
                for coordinate, value in zip(snapshot["candidate"], post_residual)
                if coordinate > 0
            )
            / (q * q),
        )
        assert support_delta == snapshot["delta"]


def bipartite_family_leading_check():
    """Check the exact q=0 scaled algebra for several K_{2,r}-plus-leaf graphs."""
    for middle_count in (3, 4, 5, 7, 10, 30):
        middle = list(range(3, 3 + middle_count))
        graph_order = 3 + middle_count
        edges = (
            ((0, 1),)
            + tuple((1, vertex) for vertex in middle)
            + tuple((2, vertex) for vertex in middle)
        )
        degrees = degrees_from_edges(graph_order, edges)
        neighbors = neighbors_from_edges(graph_order, edges)
        faces = ([0], [0, 1], [0, 1, *middle])

        def leading_apply(active, vector):
            position = {vertex: index for index, vertex in enumerate(active)}
            return [
                Fraction(value, 2)
                - sum(
                    (vector[position[other]] for other in neighbors[vertex] if other in position),
                    ZERO,
                )
                / (2 * degrees[vertex])
                for vertex, value in zip(active, vector)
            ]

        def leading_optimum(active):
            columns = []
            for column in range(len(active)):
                basis = [ZERO] * len(active)
                basis[column] = Fraction(1)
                columns.append(leading_apply(active, basis))
            matrix = [list(row) for row in zip(*columns)]
            right_hand_side = [Fraction(1) if vertex == 0 else ZERO for vertex in active]
            return solve_fraction(matrix, right_hand_side)

        def leading_objective(active, vector):
            image = leading_apply(active, vector)
            return sum(
                (
                    degrees[vertex]
                    * (Fraction(value * applied, 2) - (value if vertex == 0 else ZERO))
                    for vertex, value, applied in zip(active, vector, image)
                ),
                ZERO,
            )

        def leading_energy(active, iterate, center):
            optimum = leading_optimum(active)
            error = [value - optimum_value for value, optimum_value in zip(iterate, optimum)]
            image = leading_apply(active, error)
            return sum(
                (
                    Fraction(degrees[vertex], 2) * (coordinate * applied + center_value**2)
                    for vertex, coordinate, applied, center_value in zip(
                        active,
                        error,
                        image,
                        center,
                    )
                ),
                ZERO,
            )

        def leading_step(active, iterate, center):
            interpolation = [left + right for left, right in zip(iterate, center)]
            gradient = [
                image - (Fraction(1) if vertex == 0 else ZERO)
                for vertex, image in zip(active, leading_apply(active, interpolation))
            ]
            candidate = [value - derivative for value, derivative in zip(interpolation, gradient)]
            center_next = [new - old for new, old in zip(candidate, iterate)]
            return candidate, center_next

        initial_energy = leading_energy(faces[0], [ZERO], [ZERO])
        stage_one, center_one = leading_step(faces[0], [ZERO], [ZERO])
        stage_two, center_two = leading_step(faces[1], [stage_one[0], ZERO], [center_one[0], ZERO])
        padded_two = [stage_two[0], stage_two[1], *([ZERO] * middle_count)]
        padded_center = [center_two[0], center_two[1], *([ZERO] * middle_count)]
        stage_three, center_three = leading_step(faces[2], padded_two, padded_center)
        stage_four, center_four = leading_step(faces[2], stage_three, center_three)
        stage_four_residual = leading_apply(faces[2], stage_four)
        stage_four_residual[0] -= 1

        size_parameter = middle_count + 1
        assert stage_two == [Fraction(2), Fraction(1, size_parameter)]
        assert stage_three == [
            Fraction(5, 2) + Fraction(1, size_parameter),
            Fraction(5, 2 * size_parameter),
            *([Fraction(1, 2 * size_parameter)] * middle_count),
        ]
        assert stage_four == [
            Fraction(5, 2) + Fraction(3, size_parameter),
            Fraction(4, size_parameter) + Fraction(1, 2 * size_parameter**2),
            *([Fraction(3, 2 * size_parameter)] * middle_count),
        ]
        assert stage_four_residual == [
            Fraction(size_parameter**2 - 2 * size_parameter - 1, 4 * size_parameter**2),
            -Fraction(1, 2 * size_parameter**2),
            *([-Fraction(2 * size_parameter + 1, 8 * size_parameter**2)] * middle_count),
        ]

        credit = leading_objective(faces[0], leading_optimum(faces[0])) - leading_objective(
            faces[2],
            leading_optimum(faces[2]),
        )
        reserve = initial_energy + credit - leading_energy(faces[2], stage_four, center_four)
        reserve_formula = Fraction(
            15 * size_parameter**4
            - 15 * size_parameter**3
            + 2 * size_parameter**2
            + size_parameter
            - 3,
            16 * size_parameter**3 * (size_parameter - 1),
        )
        constant_formula = Fraction(
            (size_parameter - 1) * (size_parameter**2 - 2 * size_parameter - 1) ** 2,
            size_parameter
            * (
                15 * size_parameter**4
                - 15 * size_parameter**3
                + 2 * size_parameter**2
                + size_parameter
                - 3
            ),
        )
        assert credit == Fraction(2, size_parameter - 1)
        assert reserve == reserve_formula
        assert stage_four_residual[0] ** 2 / reserve == constant_formula


def atlas_check():
    """Enumerate every rooted connected graph-atlas representative through n=7."""
    rooted_counts = {}
    insolvencies = 0
    maximum = ZERO
    for graph in nx.graph_atlas_g():
        order = graph.number_of_nodes()
        if order < 2 or order > 7 or not nx.is_connected(graph):
            continue
        relabeled = nx.convert_node_labels_to_integers(graph, ordering="sorted")
        edges = tuple(
            sorted((min(left, right), max(left, right)) for left, right in relabeled.edges())
        )
        for seed in range(order):
            run = replay_with_reserve(order, edges, seed)
            assert run is not None and run["terminal_stage"] is not None
            rooted_counts[order] = rooted_counts.get(order, 0) + 1
            requirement = required_coefficient(run)[0]
            if requirement:
                insolvencies += 1
            maximum = max(maximum, requirement)

    assert rooted_counts == {2: 2, 3: 6, 4: 24, 5: 105, 6: 672, 7: 5971}
    assert sum(rooted_counts.values()) == 6780
    assert insolvencies == 2847
    assert maximum == ATLAS_MAXIMUM
    assert 3 - maximum == Fraction(323284433766465828, 1036704485947225385)

    named_star = replay_with_reserve(6, STAR_FIVE_EDGES, 0)
    assert named_star is not None
    assert required_coefficient(named_star)[:2] == (ATLAS_MAXIMUM, "4-")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--enumerate",
        action="store_true",
        help="also exhaust the connected rooted graph atlas through order seven",
    )
    arguments = parser.parse_args()

    witness_check()
    star_check()
    quartic_lower_check()
    bipartite_family_leading_check()
    bernstein_decrement_check()
    projection_active_stop_check()
    if arguments.enumerate:
        atlas_check()
    suffix = "; atlas n<=7 verified" if arguments.enumerate else ""
    print(
        "consumed-energy reserve verified: exact witness lambda*=0.013..., "
        "leaf-seeded K1,4 needs lambda(q)=Omega(q^-3) with limit 1/32; "
        "reachable K2,3-plus-leaf needs lambda(q)=Omega(q^-4) with limit 49/3884; "
        "K2,r-plus-leaf leading constants tend to 1/15; "
        "q^-4 Bernstein GO and original-score projected STOP verified"
        f"{suffix}"
    )


if __name__ == "__main__":
    main()
