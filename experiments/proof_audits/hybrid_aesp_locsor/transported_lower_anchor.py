#!/usr/bin/env python3
"""Exact focused checks for the Round-016 transported lower anchor."""

from __future__ import annotations

import math
from fractions import Fraction
from experiments.proof_audits import note_tex_source

Node = tuple[str, int]


def graph(m: int) -> dict[Node, set[Node]]:
    """Construct the fixed branch caterpillar."""
    vertices = (
        [("b", index) for index in range(1, m + 1)]
        + [("a", index) for index in range(1, m + 1)]
        + [("r", index) for index in range(1, m + 2)]
    )
    adjacency = {vertex: set() for vertex in vertices}

    def add(left: Node, right: Node) -> None:
        adjacency[left].add(right)
        adjacency[right].add(left)

    for index in range(1, m):
        add(("b", index), ("b", index + 1))
        add(("a", index), ("a", index + 1))
    add(("b", 1), ("a", 1))
    for index in range(1, m + 1):
        add(("b", index), ("r", index))
    add(("b", m), ("r", m + 1))
    return adjacency


def canonical_face(m: int, k: int) -> list[Node]:
    """Return Uhat_k in a stable order."""
    if k == m:
        return (
            [("b", index) for index in range(1, m + 1)]
            + [("a", index) for index in range(1, m + 1)]
            + [("r", index) for index in range(1, m + 2)]
        )
    return (
        [("b", index) for index in range(1, k + 2)]
        + [("a", index) for index in range(1, k + 1)]
        + [("r", index) for index in range(1, k + 1)]
    )


def canonical_batch(m: int, k: int) -> list[Node]:
    """Return the exact canonical boundary F_k."""
    if k < m - 1:
        return [("b", k + 2), ("a", k + 1), ("r", k + 1)]
    return [("a", m), ("r", m), ("r", m + 1)]


def solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Solve a rational system by pivoted elimination."""
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    dimension = len(rhs)
    for column in range(dimension):
        pivot = next(row for row in range(column, dimension) if augmented[row][column] != 0)
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(dimension):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            augmented[row] = [
                value - factor * base for value, base in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(dimension)]


def restricted_system(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    alpha: Fraction,
    rho: Fraction,
) -> tuple[list[list[Fraction]], list[Fraction]]:
    """Build the rational degree-scaled restricted system."""
    index = {vertex: position for position, vertex in enumerate(face)}
    a0 = (1 + alpha) / 2
    h0 = (1 - alpha) / 2
    matrix = [[Fraction(0) for _ in face] for _ in face]
    load: list[Fraction] = []
    for row, vertex in enumerate(face):
        degree = len(adjacency[vertex])
        matrix[row][row] = a0
        for neighbor in adjacency[vertex]:
            if neighbor in index:
                matrix[row][index[neighbor]] = -h0 / degree
        if vertex == ("b", 1):
            load.append(alpha * (Fraction(1, degree) - rho))
        else:
            load.append(-alpha * rho)
    return matrix, load


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    """Multiply one rational matrix and vector."""
    return [sum((value * item for value, item in zip(row, vector)), Fraction(0)) for row in matrix]


def lower_map(
    matrix: list[list[Fraction]],
    load: list[Fraction],
    trial: list[Fraction],
    alpha: Fraction,
) -> list[Fraction]:
    """Evaluate the displayed lower retraction in degree-scaled coordinates."""
    residual = [left - right for left, right in zip(load, matvec(matrix, trial))]
    delta = max([Fraction(0), *(-value for value in residual)]) / alpha
    return [max(value - delta, Fraction(0)) for value in trial]


def boundary_demands(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    batch: list[Node],
    point: list[Fraction],
    alpha: Fraction,
    rho: Fraction,
) -> list[Fraction]:
    """Compute scaled tree-boundary demands from a point on the current face."""
    index = {vertex: position for position, vertex in enumerate(face)}
    h0 = (1 - alpha) / 2
    demands = []
    for vertex in batch:
        parent = next(neighbor for neighbor in adjacency[vertex] if neighbor in index)
        degree = len(adjacency[vertex])
        demands.append(-alpha * rho + h0 * point[index[parent]] / degree)
    return demands


def check_transport(m: int, alpha: Fraction, rho: Fraction) -> None:
    """Check every canonical face, anchored retraction, and zero padding exactly."""
    adjacency = graph(m)
    anchor = [Fraction(0)]
    previous_exact: tuple[list[Node], list[Fraction]] | None = None

    for k in range(m):
        face = canonical_face(m, k)
        batch = canonical_batch(m, k)
        matrix, load = restricted_system(adjacency, face, alpha, rho)
        exact = solve(matrix, load)
        assert all(value > 0 for value in exact)
        assert len(anchor) == len(face)
        assert all(0 <= value <= optimum for value, optimum in zip(anchor, exact))
        if k > 0:
            assert any(value > 0 for value in anchor)

        if previous_exact is not None:
            old_face, old_exact = previous_exact
            exact_by_node = dict(zip(face, exact))
            assert all(exact_by_node[vertex] >= value for vertex, value in zip(old_face, old_exact))

        signed_trial = [
            -value / 7 if position % 3 == 0 else 6 * value / 5
            for position, value in enumerate(exact)
        ]
        raw_signed = lower_map(matrix, load, signed_trial, alpha)
        assert all(0 <= value <= optimum for value, optimum in zip(raw_signed, exact))

        near_trial = [Fraction(999_999, 1_000_000) * value for value in exact]
        raw = lower_map(matrix, load, near_trial, alpha)
        anchored = [max(base, value) for base, value in zip(anchor, raw)]
        assert all(base <= value for base, value in zip(anchor, anchored))
        assert all(0 <= value <= optimum for value, optimum in zip(anchored, exact))

        exact_demands = boundary_demands(adjacency, face, batch, exact, alpha, rho)
        lower_demands = boundary_demands(adjacency, face, batch, anchored, alpha, rho)
        assert all(value > 0 for value in exact_demands)
        assert all(lower <= exact_value for lower, exact_value in zip(lower_demands, exact_demands))
        assert all(value > 0 for value in lower_demands)

        next_face = canonical_face(m, k + 1)
        next_matrix, next_load = restricted_system(adjacency, next_face, alpha, rho)
        next_exact = solve(next_matrix, next_load)
        anchored_by_node = dict(zip(face, anchored))
        anchor = [anchored_by_node.get(vertex, Fraction(0)) for vertex in next_face]
        assert any(value > 0 for value in anchor)
        assert all(value <= optimum for value, optimum in zip(anchor, next_exact))
        assert all(
            anchor[next_face.index(vertex)] == value for vertex, value in zip(face, anchored)
        )
        previous_exact = (face, exact)

    assert sum(len(neighbors) for neighbors in adjacency.values()) == 6 * m
    assert len(canonical_face(m, m)) == 3 * m + 1
    for k in range(m):
        expected_volume = 6 if k < m - 1 else 3
        assert sum(len(adjacency[vertex]) for vertex in canonical_batch(m, k)) == (expected_volume)


def check_stage_cap(alpha: float, gap: float, margin: float) -> None:
    """Check the strict integer cap used for every transported face."""
    chi = alpha / (1.0 - alpha)
    factor = 4.0 * (alpha + math.sqrt(3.0)) ** 2 * gap / (alpha**3 * margin**2)
    stages = 1 + math.floor(2.0 * max(0.0, math.log(factor)) / math.sqrt(chi))
    contracted = 2.0 * math.exp(-stages * math.sqrt(chi) / 2.0) * gap
    threshold = alpha**3 * margin**2 / (2.0 * (alpha + math.sqrt(3.0)) ** 2)
    assert contracted < threshold


def check_ledger(m: int, q: int) -> None:
    """Check the exact row, round, interaction, and label partition."""
    adjacency = graph(m)
    support = canonical_face(m, m)
    prefix_rows = canonical_face(m, q)
    prefix_before_handoff = canonical_face(m, q - 1)
    prefix_volume = sum(len(adjacency[vertex]) for vertex in prefix_rows)
    post_volume = sum(len(adjacency[vertex]) for vertex in support if vertex not in prefix_rows)
    assert prefix_volume + post_volume == 6 * m
    assert (q + 1) + (m - q) == m + 1
    assert (q - 1) + (m - q + 2) == m + 1
    prefix_labels = 3 * (q - 1)
    post_labels = len(support) - len(prefix_before_handoff)
    assert prefix_labels + post_labels == 3 * m


def check_stable_labels() -> None:
    """Require every public Round-016 anchor in the note source."""
    source = note_tex_source("hybrid_aesp_locsor")
    labels = (
        "lem:branch-caterpillar-anchored-lower-transport",
        "eq:branch-caterpillar-padded-lower-transport",
        "eq:branch-caterpillar-anchored-lower-invariant",
        "def:branch-caterpillar-transported-lower-policy",
        "eq:branch-caterpillar-transported-lower-stage-bound",
        "thm:branch-caterpillar-transported-lower-handoff",
        "eq:branch-caterpillar-transported-lower-prefix-eleven-vector",
        "eq:branch-caterpillar-transported-lower-post-eleven-vector",
    )
    for label in labels:
        assert f"\\label{{{label}}}" in source


def main() -> None:
    rho = Fraction(1, 10_000_000)
    for m in range(2, 8):
        for alpha in (Fraction(1, 20), Fraction(1, 5), Fraction(49, 100)):
            check_transport(m, alpha, rho)
        for q in range(2, m + 1):
            check_ledger(m, q)
    for alpha in (0.05, 0.2, 0.49):
        for gap in (1.0e-9, 1.0e-3, 1.0):
            check_stage_cap(alpha, gap, margin=1.0e-4)
    check_stable_labels()
    print("round016 transported lower-anchor checks passed")


if __name__ == "__main__":
    main()
