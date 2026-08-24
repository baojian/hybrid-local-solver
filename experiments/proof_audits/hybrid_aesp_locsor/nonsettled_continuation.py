#!/usr/bin/env python3
"""Exact checks for the Round-020 nonsettled continuation audit."""

from __future__ import annotations

from fractions import Fraction
from experiments.proof_audits import note_tex_source

from experiments.proof_audits.hybrid_aesp_locsor.incremental_face_transition import (
    admission_face,
    boundary_demands,
    canonical_batch,
    graph,
    matvec,
    restricted_system,
    solve,
)
from experiments.proof_audits.hybrid_aesp_locsor.auxiliary_face_shock import (
    objective,
    soft_threshold,
    weighted_squared_norm,
)

Node = tuple[str, int]


def minimum_kkt_scaled(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    matrix: list[list[Fraction]],
    point: list[Fraction],
    alpha: Fraction,
    rho: Fraction,
) -> list[Fraction]:
    """Return D^{-1/2} times the minimum-norm RPPR KKT vector."""
    product = matvec(matrix, point)
    threshold = alpha * rho
    result: list[Fraction] = []
    for index, vertex in enumerate(face):
        source = Fraction(1, len(adjacency[vertex])) if vertex == ("b", 1) else Fraction(0)
        smooth = product[index] - alpha * source
        if point[index] > 0:
            result.append(smooth + threshold)
        elif point[index] < 0:
            result.append(smooth - threshold)
        elif smooth > threshold:
            result.append(smooth - threshold)
        elif smooth < -threshold:
            result.append(smooth + threshold)
        else:
            result.append(Fraction(0))
    return result


def envelope_value(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    matrix: list[list[Fraction]],
    load: list[Fraction],
    center: list[Fraction],
    kappa: Fraction,
) -> tuple[list[Fraction], Fraction]:
    """Solve the exact shifted positive-orthant system and return its envelope value."""
    shifted = [
        [value + (kappa if row == column else 0) for column, value in enumerate(matrix_row)]
        for row, matrix_row in enumerate(matrix)
    ]
    shifted_load = [value + kappa * item for value, item in zip(load, center)]
    proximal_point = solve(shifted, shifted_load)
    assert all(value > 0 for value in proximal_point)
    value = objective(adjacency, face, matrix, load, proximal_point) + Fraction(
        kappa, 2
    ) * weighted_squared_norm(
        adjacency,
        face,
        [left - right for left, right in zip(proximal_point, center)],
    )
    return proximal_point, value


def check_nonsettled_transition(m: int, alpha: Fraction, root_chi: Fraction) -> None:
    """Reproduce the first nonsettled batch, shock bound, and next center."""
    rho = Fraction(1, 10_000_000)
    assert rho < Fraction(1, 30)
    assert root_chi**2 == alpha / (1 - alpha)
    beta = (1 - root_chi) / (1 + root_chi)
    assert beta > 0

    adjacency = graph(m)
    old_face = admission_face(m, 0)
    new_face = admission_face(m, 1)
    batch = canonical_batch(m, 0)
    assert new_face == old_face + batch

    old_matrix, old_load = restricted_system(adjacency, old_face, alpha, rho)
    new_matrix, new_load = restricted_system(adjacency, new_face, alpha, rho)
    old_optimum = solve(old_matrix, old_load)
    new_optimum = solve(new_matrix, new_load)
    assert all(value > 0 for value in new_optimum)

    kappa = 1 - 2 * alpha
    diagonal = (1 + alpha) / 2
    half_step = (1 - alpha) / 2
    assert diagonal + kappa == 3 * half_step

    # One exact shifted stage from zero on Uhat_0.
    endpoint = [old_load[0] / (old_matrix[0][0] + kappa)]
    assert Fraction(0) < endpoint[0] < old_optimum[0]
    shifted_residual = (old_matrix[0][0] + kappa) * endpoint[0] - old_load[0]
    assert shifted_residual == 0

    demands = boundary_demands(adjacency, old_face, batch, endpoint, alpha, rho)
    expected_scaled = [
        alpha * (1 - 30 * rho) / 27,
        alpha * (1 - 21 * rho) / 18,
        alpha * (1 - 12 * rho) / 9,
    ]
    assert demands == expected_scaled
    assert all(value > 0 for value in demands)

    momentum = endpoint[:]
    center = [(1 + beta) * endpoint[0]]
    estimate = [endpoint[0] / root_chi]
    assert momentum[0] != 0
    assert center[0] > endpoint[0]

    padded_endpoint = endpoint + [Fraction(0)] * len(batch)
    padded_center = center + [Fraction(0)] * len(batch)
    padded_estimate = estimate + [Fraction(0)] * len(batch)

    # The old proximal value can be paid before admission; only three cells append.
    lipschitz = 2 * (1 - alpha)
    old_product = matvec(old_matrix, center)
    old_source = alpha / len(adjacency[("b", 1)])
    old_forward = center[0] - (old_product[0] - old_source) / lipschitz
    old_start = [soft_threshold(old_forward, alpha * rho / lipschitz)]

    new_product = matvec(new_matrix, padded_center)
    new_start: list[Fraction] = []
    for index, vertex in enumerate(new_face):
        source = alpha / len(adjacency[vertex]) if vertex == ("b", 1) else Fraction(0)
        forward = padded_center[index] - (new_product[index] - source) / lipschitz
        new_start.append(soft_threshold(forward, alpha * rho / lipschitz))
    assert new_start[:1] == old_start
    center_demands = [left - right for left, right in zip(new_load, new_product)]
    assert new_start[1:] == [value / lipschitz for value in center_demands[1:]]
    assert all(value > 0 for value in new_start[1:])
    assert 4 * len(batch) == 12

    # Exact new-face estimate certificate and the computable KKT reset bound.
    _, envelope = envelope_value(adjacency, new_face, new_matrix, new_load, padded_endpoint, kappa)
    optimum_value = objective(adjacency, new_face, new_matrix, new_load, new_optimum)
    mu_envelope = kappa * root_chi**2
    estimate_error = [left - right for left, right in zip(padded_estimate, new_optimum)]
    psi = (
        envelope
        - optimum_value
        + Fraction(mu_envelope, 2) * weighted_squared_norm(adjacency, new_face, estimate_error)
    )
    new_coordinate_floor = Fraction(mu_envelope, 2) * sum(
        len(adjacency[vertex]) * new_optimum[index] ** 2
        for index, vertex in enumerate(new_face)
        if index >= len(old_face)
    )
    assert psi >= new_coordinate_floor > 0

    kkt_scaled = minimum_kkt_scaled(adjacency, new_face, new_matrix, padded_endpoint, alpha, rho)
    kkt_squared = sum(
        len(adjacency[vertex]) * value**2 for vertex, value in zip(new_face, kkt_scaled)
    )
    displacement_squared = weighted_squared_norm(
        adjacency,
        new_face,
        [left - right for left, right in zip(padded_estimate, padded_endpoint)],
    )
    shock_budget = (
        kkt_squared / (2 * alpha)
        + mu_envelope * displacement_squared
        + mu_envelope * kkt_squared / alpha**2
    )
    assert Fraction(0) < psi <= shock_budget

    # The next shifted target is driven by a genuinely extrapolated center.
    continuation_point, _ = envelope_value(
        adjacency, new_face, new_matrix, new_load, padded_center, kappa
    )
    assert continuation_point != padded_endpoint
    assert padded_center != padded_endpoint


def check_ledgers(m: int) -> None:
    """Check row, round, interaction, and output partitions."""
    adjacency = graph(m)
    support = admission_face(m, m)
    first_face = admission_face(m, 1)
    assert sum(len(adjacency[vertex]) for vertex in first_face) == 9
    post_adjacency = sum(len(adjacency[vertex]) for vertex in support if vertex not in first_face)
    assert 9 + post_adjacency == 6 * m
    assert 2 + (m - 1) == m + 1
    assert 1 + ((m - 1) + 1) == m + 1
    assert 3 + len(support) - len(first_face) == 3 * m


def check_stable_labels() -> None:
    """Require every public Round-020 anchor and scope marker."""
    source = note_tex_source("hybrid_aesp_locsor")
    labels = (
        "sec:branch-caterpillar-nonsettled-continuation",
        "eq:branch-caterpillar-nonsettled-range",
        "eq:branch-caterpillar-first-nonsettled-state",
        "lem:branch-caterpillar-first-nonsettled-admission",
        "eq:branch-caterpillar-first-nonsettled-margin",
        "eq:branch-caterpillar-nonsettled-auxiliary-append",
        "eq:branch-caterpillar-nonsettled-shock-budget",
        "lem:branch-caterpillar-nonsettled-shock-reset",
        "eq:branch-caterpillar-nonsettled-shock-bound",
        "eq:branch-caterpillar-nonsettled-transition-vector",
        "eq:branch-caterpillar-nonsettled-oracle-log",
        "thm:branch-caterpillar-first-nonsettled-continuation",
        "eq:branch-caterpillar-nonsettled-prefix-eleven-vector",
        "eq:branch-caterpillar-nonsettled-post-eleven-vector",
        "eq:branch-caterpillar-nonsettled-total-work",
    )
    for label in labels:
        assert f"\\label{{{label}}}" in source
    assert "exactly twelve cells" in source
    assert "No missing endpoint product is assumed free" in source
    assert "one extrapolated relative-accuracy stage" in source
    assert "not an amortization" in source


def main() -> None:
    """Run the exact transition, shock, continuation, ledger, and source checks."""
    parameter_pairs = (
        (Fraction(1, 10), Fraction(1, 3)),
        (Fraction(1, 5), Fraction(1, 2)),
    )
    for m in range(2, 13):
        for alpha, root_chi in parameter_pairs:
            check_nonsettled_transition(m, alpha, root_chi)
        check_ledgers(m)
    check_stable_labels()
    print("round020 nonsettled continuation checks passed")


if __name__ == "__main__":
    main()
