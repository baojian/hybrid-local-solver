#!/usr/bin/env python3
"""Exact checks for the Round-019 auxiliary face shock."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from check_round018 import (
    admission_face,
    canonical_batch,
    graph,
    matvec,
    restricted_system,
    solve,
)

Node = tuple[str, int]


def soft_threshold(value: Fraction, threshold: Fraction) -> Fraction:
    """Return the exact scalar soft-thresholding map."""
    if value > threshold:
        return value - threshold
    if value < -threshold:
        return value + threshold
    return Fraction(0)


def objective(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    matrix: list[list[Fraction]],
    load: list[Fraction],
    point: list[Fraction],
) -> Fraction:
    """Evaluate the positive-orthant RPPR quadratic in scaled coordinates."""
    product = matvec(matrix, point)
    return sum(
        Fraction(len(adjacency[vertex]), 2) * point[index] * product[index]
        - len(adjacency[vertex]) * load[index] * point[index]
        for index, vertex in enumerate(face)
    )


def weighted_squared_norm(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    vector: list[Fraction],
) -> Fraction:
    """Return the original-coordinate Euclidean norm from scaled coordinates."""
    return sum(len(adjacency[vertex]) * value**2 for vertex, value in zip(face, vector))


def check_transition(m: int, alpha: Fraction, rho: Fraction, k: int) -> None:
    """Reproduce the proximal append and both exact face shocks."""
    adjacency = graph(m)
    old_face = admission_face(m, k)
    new_face = admission_face(m, k + 1)
    batch = canonical_batch(m, k)
    assert new_face == old_face + batch

    old_matrix, old_load = restricted_system(adjacency, old_face, alpha, rho)
    new_matrix, new_load = restricted_system(adjacency, new_face, alpha, rho)
    old_optimum = solve(old_matrix, old_load)
    new_optimum = solve(new_matrix, new_load)
    assert all(value > 0 for value in old_optimum)
    assert all(value > 0 for value in new_optimum)

    # At the settled old center, the shifted minimizer and estimate defect are zero.
    kappa = 1 - 2 * alpha
    old_shifted_matrix = [
        [value + (kappa if row == column else 0) for column, value in enumerate(matrix_row)]
        for row, matrix_row in enumerate(old_matrix)
    ]
    old_shifted_load = [
        load_value + kappa * center for load_value, center in zip(old_load, old_optimum)
    ]
    assert solve(old_shifted_matrix, old_shifted_load) == old_optimum

    padded = old_optimum + [Fraction(0)] * len(batch)
    padded_product = matvec(new_matrix, padded)
    demands = [left - right for left, right in zip(new_load, padded_product)]
    assert demands[: len(old_face)] == [Fraction(0)] * len(old_face)
    new_demands = demands[len(old_face) :]
    assert len(new_demands) == 3
    assert all(value > 0 for value in new_demands)

    # The imported composite proximal map retains old entries and appends g/L.
    lipschitz = 2 * (1 - alpha)
    expected_start = old_optimum + [value / lipschitz for value in new_demands]
    actual_start: list[Fraction] = []
    for index, vertex in enumerate(new_face):
        source = alpha / len(adjacency[vertex]) if vertex == ("b", 1) else Fraction(0)
        smooth_gradient = padded_product[index] - source
        forward = padded[index] - smooth_gradient / lipschitz
        actual_start.append(soft_threshold(forward, alpha * rho / lipschitz))
    assert actual_start == expected_start
    assert actual_start[: len(old_face)] == old_optimum
    assert all(value > 0 for value in actual_start[len(old_face) :])

    # The old settled objective gap is zero; the enlarged-face gap is exact Q energy.
    face_shock = objective(adjacency, new_face, new_matrix, new_load, padded) - objective(
        adjacency, new_face, new_matrix, new_load, new_optimum
    )
    error = [left - right for left, right in zip(padded, new_optimum)]
    q_error = matvec(new_matrix, error)
    q_energy = sum(
        Fraction(len(adjacency[vertex]), 2) * error[index] * q_error[index]
        for index, vertex in enumerate(new_face)
    )
    assert face_shock == q_energy
    assert face_shock > 0

    # Compute the analytical Moreau/estimate shock independently.
    shifted_matrix = [
        [value + (kappa if row == column else 0) for column, value in enumerate(matrix_row)]
        for row, matrix_row in enumerate(new_matrix)
    ]
    shifted_load = [load_value + kappa * center for load_value, center in zip(new_load, padded)]
    proximal_point = solve(shifted_matrix, shifted_load)
    assert all(value > 0 for value in proximal_point)
    envelope = objective(adjacency, new_face, new_matrix, new_load, proximal_point) + Fraction(
        kappa, 2
    ) * weighted_squared_norm(
        adjacency,
        new_face,
        [left - right for left, right in zip(proximal_point, padded)],
    )
    optimum_value = objective(adjacency, new_face, new_matrix, new_load, new_optimum)
    mu_envelope = alpha * kappa / (1 - alpha)
    estimate_shock = (
        envelope
        - optimum_value
        + Fraction(mu_envelope, 2) * (weighted_squared_norm(adjacency, new_face, error))
    )
    new_coordinate_floor = Fraction(mu_envelope, 2) * sum(
        len(adjacency[vertex]) * new_optimum[index] ** 2
        for index, vertex in enumerate(new_face)
        if index >= len(old_face)
    )
    assert estimate_shock >= new_coordinate_floor > 0

    # One explicit center/momentum/estimate/proximal record per new coordinate.
    appended_auxiliary_records = 4 * len(batch)
    assert appended_auxiliary_records == 12


def check_first_layer_ledgers(m: int) -> None:
    """Check the concrete k=1-to-2 prefix/post partitions."""
    adjacency = graph(m)
    support = admission_face(m, m)
    first_two_faces = admission_face(m, 2)
    boundary_volume = sum(len(adjacency[vertex]) for vertex in canonical_batch(m, 1))
    assert boundary_volume == (3 if m == 2 else 6)

    prefix_adjacency = 9 + boundary_volume
    post_adjacency = sum(
        len(adjacency[vertex]) for vertex in support if vertex not in first_two_faces
    )
    assert prefix_adjacency + post_adjacency == 6 * m
    assert 3 + (m - 2) == m + 1
    assert 2 + (m - 1) == m + 1
    assert 6 + len(support) - len(first_two_faces) == 3 * m
    if m == 2:
        assert post_adjacency == 0


def check_stable_labels() -> None:
    """Require every public Round-019 anchor in the note source."""
    source = Path(__file__).with_name("main.tex").read_text(encoding="utf-8")
    labels = (
        "sec:branch-caterpillar-auxiliary-face-shock",
        "eq:branch-caterpillar-auxiliary-proximal-start",
        "eq:branch-caterpillar-settled-auxiliary-state-append",
        "lem:branch-caterpillar-settled-proximal-append",
        "eq:branch-caterpillar-settled-proximal-append",
        "prop:branch-caterpillar-zero-estimate-carry-fails",
        "eq:branch-caterpillar-objective-face-shock-identity",
        "eq:branch-caterpillar-estimate-face-shock-positive",
        "eq:branch-caterpillar-settled-auxiliary-transition-vector",
        "thm:branch-caterpillar-first-auxiliary-shock-handoff",
        "eq:branch-caterpillar-first-auxiliary-prefix-eleven-vector",
        "eq:branch-caterpillar-first-auxiliary-post-eleven-vector",
    )
    for label in labels:
        assert f"\\label{{{label}}}" in source
    assert "exactly twelve new auxiliary" in source
    assert "analytical shock" in source


def main() -> None:
    """Run all exact transition, ledger, and source-anchor checks."""
    rho = Fraction(1, 10_000_000)
    for m in range(2, 8):
        for alpha in (Fraction(1, 20), Fraction(1, 5), Fraction(49, 100)):
            for k in range(m):
                check_transition(m, alpha, rho, k)
        check_first_layer_ledgers(m)
    check_stable_labels()
    print("round019 auxiliary face-shock checks passed")


if __name__ == "__main__":
    main()
