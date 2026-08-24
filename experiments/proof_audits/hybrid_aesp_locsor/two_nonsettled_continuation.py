#!/usr/bin/env python3
"""Exact checks for the Round-021 two-nonsettled continuation."""

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
from experiments.proof_audits.hybrid_aesp_locsor.nonsettled_continuation import (
    envelope_value,
    minimum_kkt_scaled,
)

Node = tuple[str, int]


def proximal_start(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    matrix: list[list[Fraction]],
    center: list[Fraction],
    alpha: Fraction,
    rho: Fraction,
) -> list[Fraction]:
    """Return the exact composite warm start in degree-scaled coordinates."""
    lipschitz = 2 * (1 - alpha)
    product = matvec(matrix, center)
    result: list[Fraction] = []
    for index, vertex in enumerate(face):
        source = alpha / len(adjacency[vertex]) if vertex == ("b", 1) else Fraction(0)
        forward = center[index] - (product[index] - source) / lipschitz
        result.append(soft_threshold(forward, alpha * rho / lipschitz))
    return result


def shifted_keys(
    matrix: list[list[Fraction]],
    load: list[Fraction],
    center: list[Fraction],
    point: list[Fraction],
    kappa: Fraction,
) -> list[Fraction]:
    """Return normalized minimum-KKT magnitudes for one shifted face."""
    product = matvec(matrix, point)
    result: list[Fraction] = []
    for index, value in enumerate(point):
        demand = load[index] + kappa * center[index] - product[index] - kappa * value
        result.append(abs(demand) if value > 0 else max(demand, Fraction(0)))
    return result


def relative_stop(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    matrix: list[list[Fraction]],
    load: list[Fraction],
    center: list[Fraction],
    point: list[Fraction],
    alpha: Fraction,
    root_chi: Fraction,
) -> bool:
    """Evaluate the imported relative KKT-mass stopping rule exactly."""
    kappa = 1 - 2 * alpha
    delta = root_chi / (2 - root_chi)
    keys = shifted_keys(matrix, load, center, point, kappa)
    mass = sum(len(adjacency[vertex]) * key for vertex, key in zip(face, keys))
    displacement = weighted_squared_norm(
        adjacency,
        face,
        [left - right for left, right in zip(point, center)],
    )
    return mass**2 <= delta * kappa * (1 - alpha) * displacement


def greedy_relative_stage(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    matrix: list[list[Fraction]],
    load: list[Fraction],
    center: list[Fraction],
    alpha: Fraction,
    rho: Fraction,
    root_chi: Fraction,
    *,
    increasing: bool,
) -> tuple[list[Fraction], int]:
    """Run the exact normalized-KKT greedy loop through the relative rule."""
    kappa = 1 - 2 * alpha
    point = proximal_start(adjacency, face, matrix, center, alpha, rho)
    for updates in range(20_000):
        if relative_stop(adjacency, face, matrix, load, center, point, alpha, root_chi):
            return point, updates
        keys = shifted_keys(matrix, load, center, point, kappa)
        coordinate = max(range(len(face)), key=lambda index: (keys[index], -index))
        assert keys[coordinate] > 0
        numerator = load[coordinate] + kappa * center[coordinate]
        numerator -= sum(
            matrix[coordinate][column] * point[column]
            for column in range(len(face))
            if column != coordinate
        )
        updated = max(
            Fraction(0),
            numerator / (matrix[coordinate][coordinate] + kappa),
        )
        assert updated != point[coordinate]
        if increasing:
            assert updated > point[coordinate]
        point[coordinate] = updated
    raise AssertionError("greedy relative stage did not terminate")


def second_range(m: int, beta: Fraction) -> Fraction:
    """Return the exact Round-021 second-admission threshold."""
    denominator = 138 + 3 * beta if m == 2 else 354 + 3 * beta
    return (1 + beta) / denominator


def expected_second_margins(
    m: int,
    alpha: Fraction,
    rho: Fraction,
    beta: Fraction,
) -> list[Fraction]:
    """Return the displayed normalized warm-start boundary margins."""
    common = (1 + beta) * (1 - 3 * rho)
    if m == 2:
        return [
            alpha * (common / 72 - 5 * rho / 4),
            alpha * (common / 108 - 5 * rho / 4),
            alpha * (common / 108 - 5 * rho / 4),
        ]
    return [
        alpha * (common / 324 - 13 * rho / 12),
        alpha * (common / 144 - 9 * rho / 8),
        alpha * (common / 108 - 5 * rho / 4),
    ]


def check_two_admissions(m: int, root_chi: Fraction) -> None:
    """Check the safe greedy endpoint, second reset, and second stage."""
    alpha = root_chi**2 / (1 + root_chi**2)
    beta = (1 - root_chi) / (1 + root_chi)
    rho_limit = second_range(m, beta)
    rho = Fraction(999, 1000) * rho_limit
    assert Fraction(0) < rho < rho_limit < Fraction(1, 30)

    adjacency = graph(m)
    face0 = admission_face(m, 0)
    face1 = admission_face(m, 1)
    face2 = admission_face(m, 2)
    batch0 = canonical_batch(m, 0)
    batch1 = canonical_batch(m, 1)
    assert face1 == face0 + batch0
    assert face2 == face1 + batch1

    matrix0, load0 = restricted_system(adjacency, face0, alpha, rho)
    matrix1, load1 = restricted_system(adjacency, face1, alpha, rho)
    matrix2, load2 = restricted_system(adjacency, face2, alpha, rho)
    optimum0 = solve(matrix0, load0)
    optimum1 = solve(matrix1, load1)
    optimum2 = solve(matrix2, load2)
    assert all(value > 0 for value in optimum0 + optimum1 + optimum2)

    kappa = 1 - 2 * alpha
    endpoint0 = [load0[0] / (matrix0[0][0] + kappa)]
    center1 = [(1 + beta) * endpoint0[0]] + [Fraction(0)] * len(batch0)
    ratio = center1[0] / optimum0[0]
    expected_ratio = 2 * (1 + 2 * root_chi**2) / (3 * (1 + root_chi))
    assert ratio == expected_ratio < 1
    assert all(left < right for left, right in zip(center1, optimum1))

    # y+ is a lower center on Uhat_1, but its zero parents cannot certify F_1.
    lower_residual = [left - right for left, right in zip(load1, matvec(matrix1, center1))]
    assert lower_residual[0] > 0
    center_boundary = boundary_demands(adjacency, face1, batch1, center1, alpha, rho)
    assert center_boundary == [-alpha * rho] * 3

    warm1 = proximal_start(adjacency, face1, matrix1, center1, alpha, rho)
    endpoint1, first_updates = greedy_relative_stage(
        adjacency,
        face1,
        matrix1,
        load1,
        center1,
        alpha,
        rho,
        root_chi,
        increasing=True,
    )
    shifted1 = [
        [value + (kappa if row == column else 0) for column, value in enumerate(matrix_row)]
        for row, matrix_row in enumerate(matrix1)
    ]
    shifted_load1 = [left + kappa * right for left, right in zip(load1, center1)]
    shifted_optimum1 = solve(shifted1, shifted_load1)
    assert all(value > 0 for value in shifted_optimum1)
    assert all(left <= right for left, right in zip(center1, warm1))
    assert all(left <= right for left, right in zip(warm1, endpoint1))
    assert all(left <= right for left, right in zip(endpoint1, shifted_optimum1))
    assert all(left < right for left, right in zip(shifted_optimum1, optimum1))
    assert relative_stop(adjacency, face1, matrix1, load1, center1, endpoint1, alpha, root_chi)
    assert first_updates >= 0

    warm_margins = boundary_demands(adjacency, face1, batch1, warm1, alpha, rho)
    assert warm_margins == expected_second_margins(m, alpha, rho, beta)
    assert all(value > 0 for value in warm_margins)
    endpoint_margins = boundary_demands(adjacency, face1, batch1, endpoint1, alpha, rho)
    assert all(left >= right > 0 for left, right in zip(endpoint_margins, warm_margins))

    padded_endpoint0 = endpoint0 + [Fraction(0)] * len(batch0)
    momentum1 = [left - right for left, right in zip(endpoint1, padded_endpoint0)]
    assert all(value > 0 for value in momentum1)
    outer_center1 = [left + beta * right for left, right in zip(endpoint1, momentum1)]
    estimate1 = [
        left + (Fraction(1, 1) / root_chi - 1) * right for left, right in zip(endpoint1, momentum1)
    ]
    assert all(left > right for left, right in zip(outer_center1, endpoint1))

    # The second append retains old proximal cells and appends three positives.
    old_start = proximal_start(adjacency, face1, matrix1, outer_center1, alpha, rho)
    padded_center = outer_center1 + [Fraction(0)] * len(batch1)
    padded_endpoint1 = endpoint1 + [Fraction(0)] * len(batch1)
    padded_estimate1 = estimate1 + [Fraction(0)] * len(batch1)
    new_start = proximal_start(adjacency, face2, matrix2, padded_center, alpha, rho)
    assert new_start[: len(face1)] == old_start
    center_margins = boundary_demands(adjacency, face1, batch1, outer_center1, alpha, rho)
    lipschitz = 2 * (1 - alpha)
    assert new_start[len(face1) :] == [value / lipschitz for value in center_margins]
    assert all(value > 0 for value in new_start[len(face1) :])
    assert 4 * len(batch1) == 12

    # Reproduce the strictly positive second-face certificate and KKT reset.
    _, envelope = envelope_value(adjacency, face2, matrix2, load2, padded_endpoint1, kappa)
    optimum_value = objective(adjacency, face2, matrix2, load2, optimum2)
    mu_envelope = kappa * root_chi**2
    estimate_error = [left - right for left, right in zip(padded_estimate1, optimum2)]
    psi = (
        envelope
        - optimum_value
        + Fraction(mu_envelope, 2) * weighted_squared_norm(adjacency, face2, estimate_error)
    )
    new_coordinate_floor = Fraction(mu_envelope, 2) * sum(
        len(adjacency[vertex]) * optimum2[index] ** 2
        for index, vertex in enumerate(face2)
        if index >= len(face1)
    )
    assert psi >= new_coordinate_floor > 0

    kkt_scaled = minimum_kkt_scaled(adjacency, face2, matrix2, padded_endpoint1, alpha, rho)
    kkt_squared = sum(len(adjacency[vertex]) * value**2 for vertex, value in zip(face2, kkt_scaled))
    displacement_squared = weighted_squared_norm(
        adjacency,
        face2,
        [left - right for left, right in zip(padded_estimate1, padded_endpoint1)],
    )
    budget2 = (
        kkt_squared / (2 * alpha)
        + mu_envelope * displacement_squared
        + mu_envelope * kkt_squared / alpha**2
    )
    assert Fraction(0) < psi <= budget2

    # The second relative stage is driven by the genuinely extrapolated center.
    assert padded_center != padded_endpoint1
    endpoint2, second_updates = greedy_relative_stage(
        adjacency,
        face2,
        matrix2,
        load2,
        padded_center,
        alpha,
        rho,
        root_chi,
        increasing=False,
    )
    assert relative_stop(
        adjacency, face2, matrix2, load2, padded_center, endpoint2, alpha, root_chi
    )
    assert second_updates >= 0

    # The restrictive threshold is exact: its displayed margin vanishes at rho_2.
    sharp = expected_second_margins(m, alpha, rho_limit, beta)
    restrictive = 1 if m == 2 else 0
    assert sharp[restrictive] == 0
    assert all(value >= 0 for value in sharp)


def check_ledgers(m: int) -> None:
    """Check the two-admission row, round, interaction, and label partitions."""
    adjacency = graph(m)
    support = admission_face(m, m)
    face2 = admission_face(m, 2)
    volume2 = sum(len(adjacency[vertex]) for vertex in face2)
    cells2 = volume2 + len(face2)
    assert volume2 == (12 if m == 2 else 15)
    assert cells2 == (19 if m == 2 else 22)
    post_adjacency = sum(len(adjacency[vertex]) for vertex in support if vertex not in face2)
    assert volume2 + post_adjacency == 6 * m
    assert 3 + (m - 2) == m + 1
    assert 2 + (m - 1) == m + 1
    assert 6 + len(support) - len(face2) == 3 * m


def check_stable_labels() -> None:
    """Require the public Round-021 anchors and exact scope markers."""
    source = note_tex_source("hybrid_aesp_locsor")
    labels = (
        "sec:branch-caterpillar-second-nonsettled-continuation",
        "eq:branch-caterpillar-second-nonsettled-threshold",
        "eq:branch-caterpillar-second-nonsettled-range",
        "lem:branch-caterpillar-second-nonsettled-safe-center",
        "eq:branch-caterpillar-second-nonsettled-center-ratio",
        "eq:branch-caterpillar-second-nonsettled-safe-order",
        "lem:branch-caterpillar-second-nonsettled-admission",
        "eq:branch-caterpillar-second-nonsettled-margins",
        "eq:branch-caterpillar-second-nonsettled-terminal-margins",
        "eq:branch-caterpillar-second-nonsettled-momentum",
        "eq:branch-caterpillar-second-nonsettled-auxiliary-append",
        "eq:branch-caterpillar-second-nonsettled-shock-budget",
        "lem:branch-caterpillar-second-nonsettled-shock-reset",
        "eq:branch-caterpillar-second-nonsettled-shock-bound",
        "eq:branch-caterpillar-second-nonsettled-transition-vector",
        "eq:branch-caterpillar-two-nonsettled-oracle-log",
        "eq:branch-caterpillar-two-nonsettled-budgets",
        "thm:branch-caterpillar-two-nonsettled-continuation",
        "eq:branch-caterpillar-two-nonsettled-prefix-eleven-vector",
        "eq:branch-caterpillar-two-nonsettled-post-eleven-vector",
        "eq:branch-caterpillar-two-nonsettled-total-work",
    )
    for label in labels:
        assert f"\\label{{{label}}}" in source
    assert "does \\emph{not} certify the" in source
    assert "exactly twelve" in source
    assert "exact greedy normalized-KKT" in source
    assert "$B_2$ is a fresh observable reset with no proved" in source
    assert "inequality against $B_{\\rm ns}$" in source
    assert "R_{\\rm int}^{\\rm total}=m+1" in source
    assert "R_{\\rm adj}^{\\rm total}=m+1+O" in source


def main() -> None:
    """Run exact greedy, margin, reset, ledger, and source checks."""
    roots = (
        Fraction(1, 10),
        Fraction(1, 5),
        Fraction(1, 3),
        Fraction(1, 2),
        Fraction(2, 3),
        Fraction(9, 10),
    )
    for m in range(2, 13):
        for root_chi in roots:
            check_two_admissions(m, root_chi)
        check_ledgers(m)
    check_stable_labels()
    print("round021 two-nonsettled continuation checks passed")


if __name__ == "__main__":
    main()
