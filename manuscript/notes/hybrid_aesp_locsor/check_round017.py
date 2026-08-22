#!/usr/bin/env python3
"""Exact focused checks for the Round-017 implicit lower heap."""

from __future__ import annotations

import heapq
from fractions import Fraction
from pathlib import Path

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
    """Return Uhat_k in stable order."""
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
        pivot = next(row for row in range(column, dimension) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(dimension):
            if row == column:
                continue
            factor = augmented[row][column]
            if not factor:
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
    """Build the exact degree-scaled restricted system."""
    index = {vertex: position for position, vertex in enumerate(face)}
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    matrix = [[Fraction(0) for _ in face] for _ in face]
    load: list[Fraction] = []
    for row, vertex in enumerate(face):
        degree = len(adjacency[vertex])
        matrix[row][row] = diagonal
        for neighbor in adjacency[vertex]:
            if neighbor in index:
                matrix[row][index[neighbor]] = -coupling / degree
        source = Fraction(1, degree) if vertex == ("b", 1) else Fraction(0)
        load.append(alpha * (source - rho))
    return matrix, load


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    """Multiply a rational matrix and vector."""
    return [sum((value * item for value, item in zip(row, vector)), Fraction(0)) for row in matrix]


def dense_anchored_lower(
    matrix: list[list[Fraction]],
    load: list[Fraction],
    trial: list[Fraction],
    anchor: list[Fraction],
    alpha: Fraction,
) -> tuple[Fraction, list[Fraction]]:
    """Evaluate the literal dense anchored lower map in scaled coordinates."""
    residual = [left - right for left, right in zip(load, matvec(matrix, trial))]
    delta = max([Fraction(0), *(-value for value in residual)]) / alpha
    point = [max(base, value - delta, Fraction(0)) for base, value in zip(anchor, trial)]
    return delta, point


class ExactImplicitLowerHeap:
    """Maintain the displayed lower state with exact lazy heap rekeys."""

    def __init__(
        self,
        matrix: list[list[Fraction]],
        load: list[Fraction],
        trial: list[Fraction],
        anchor: list[Fraction],
        alpha: Fraction,
    ) -> None:
        self.matrix = matrix
        self.load = load
        self.trial = trial[:]
        self.anchor = anchor[:]
        self.alpha = alpha
        self.residual = [left - right for left, right in zip(load, matvec(matrix, self.trial))]
        self.version = [0 for _ in trial]
        self.heap: list[tuple[Fraction, int, int]] = []
        for index in range(len(trial)):
            self._push(index)

    def _key(self, index: int) -> Fraction:
        return max(-self.residual[index], Fraction(0)) / self.alpha

    def _push(self, index: int) -> None:
        heapq.heappush(self.heap, (-self._key(index), self.version[index], index))

    def delta(self) -> Fraction:
        while True:
            negative, version, index = self.heap[0]
            if version == self.version[index] and -negative == self._key(index):
                return -negative
            heapq.heappop(self.heap)

    def point_at(self, index: int) -> Fraction:
        return max(self.anchor[index], self.trial[index] - self.delta(), Fraction(0))

    def update(self, column: int, change: Fraction) -> list[int]:
        """Apply one coordinate write and return precisely the changed rows."""
        self.trial[column] += change
        affected = [row for row in range(len(self.trial)) if self.matrix[row][column]]
        for row in affected:
            self.residual[row] -= self.matrix[row][column] * change
            self.version[row] += 1
            self._push(row)
        return affected


def boundary_demands(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    batch: list[Node],
    point: list[Fraction],
    alpha: Fraction,
    rho: Fraction,
) -> list[Fraction]:
    """Compute exact degree-scaled tree-boundary demands."""
    index = {vertex: position for position, vertex in enumerate(face)}
    coupling = (1 - alpha) / 2
    demands: list[Fraction] = []
    for vertex in batch:
        parent = next(neighbor for neighbor in adjacency[vertex] if neighbor in index)
        demands.append(-alpha * rho + coupling * point[index[parent]] / len(adjacency[vertex]))
    return demands


def check_heap(m: int, k: int, alpha: Fraction, rho: Fraction) -> None:
    """Compare every lazy update/query with the literal dense map exactly."""
    adjacency = graph(m)
    face = canonical_face(m, k)
    batch = canonical_batch(m, k)
    matrix, load = restricted_system(adjacency, face, alpha, rho)
    exact = solve(matrix, load)
    assert all(value > 0 for value in exact)
    anchor = [value / 7 for value in exact]
    trial = [
        -value / 5 if position % 3 == 0 else 6 * value / 5 for position, value in enumerate(exact)
    ]
    state = ExactImplicitLowerHeap(matrix, load, trial, anchor, alpha)

    for step in range(3 * len(face) + 7):
        dense_delta, dense_point = dense_anchored_lower(matrix, load, state.trial, anchor, alpha)
        assert state.delta() == dense_delta
        implicit_point = [state.point_at(index) for index in range(len(face))]
        assert implicit_point == dense_point
        assert all(
            base <= value <= optimum for base, value, optimum in zip(anchor, dense_point, exact)
        )

        dense_demands = boundary_demands(adjacency, face, batch, dense_point, alpha, rho)
        implicit_demands = boundary_demands(adjacency, face, batch, implicit_point, alpha, rho)
        exact_demands = boundary_demands(adjacency, face, batch, exact, alpha, rho)
        assert implicit_demands == dense_demands
        assert all(value <= optimum for value, optimum in zip(implicit_demands, exact_demands))

        column = (5 * step + 1) % len(face)
        change = Fraction((step % 7) - 3, 29 + step) * exact[column]
        affected = state.update(column, change)
        expected = [row for row in range(len(face)) if matrix[row][column]]
        assert affected == expected
        assert len(affected) <= len(adjacency[face[column]]) + 1


def check_shock_and_ledger(m: int, q: int) -> None:
    """Check exact restart shock and prefix/post partitions."""
    adjacency = graph(m)
    row_shock = sum(
        sum(len(adjacency[vertex]) for vertex in canonical_face(m, k)) for k in range(q)
    )
    admission_shock = sum(len(canonical_face(m, k)) for k in range(1, q))
    assert row_shock == 3 * q * q
    assert admission_shock == (q - 1) * (3 * q + 2) // 2

    support = canonical_face(m, m)
    exposed = canonical_face(m, q)
    prehandoff = canonical_face(m, q - 1)
    prefix_volume = sum(len(adjacency[vertex]) for vertex in exposed)
    post_volume = sum(len(adjacency[vertex]) for vertex in support if vertex not in exposed)
    assert prefix_volume + post_volume == 6 * m
    assert (q - 1) + (m - q + 2) == m + 1
    assert 3 * (q - 1) + len(support) - len(prehandoff) == 3 * m


def check_stable_labels() -> None:
    """Require every public Round-017 anchor in the note source."""
    source = Path(__file__).with_name("main.tex").read_text(encoding="utf-8")
    labels = (
        "sec:branch-caterpillar-implicit-lower-heap",
        "lem:branch-caterpillar-implicit-lower-heap",
        "eq:branch-caterpillar-implicit-lower-update",
        "eq:branch-caterpillar-implicit-lower-init-vector",
        "prop:branch-caterpillar-literal-dense-lower-sweep-cost",
        "def:branch-caterpillar-implicit-lower-policy",
        "eq:branch-caterpillar-implicit-lower-stopping-time",
        "eq:branch-caterpillar-implicit-lower-shock",
        "thm:branch-caterpillar-implicit-lower-handoff",
        "eq:branch-caterpillar-implicit-lower-prefix-eleven-vector",
        "eq:branch-caterpillar-implicit-lower-post-eleven-vector",
    )
    for label in labels:
        assert f"\\label{{{label}}}" in source


def main() -> None:
    rho = Fraction(1, 10_000_000)
    for m in range(2, 8):
        for alpha in (Fraction(1, 20), Fraction(1, 5), Fraction(49, 100)):
            for k in range(m):
                check_heap(m, k, alpha, rho)
        for q in range(2, m + 1):
            check_shock_and_ledger(m, q)
    check_stable_labels()
    print("round017 implicit lower-heap checks passed")


if __name__ == "__main__":
    main()
