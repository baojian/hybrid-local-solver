#!/usr/bin/env python3
"""Exact checks for the Round-018 incremental face transition."""

from __future__ import annotations

import heapq
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


def canonical_batch(m: int, k: int) -> list[Node]:
    """Return the exact canonical boundary in admission order."""
    if k < m - 1:
        return [("b", k + 2), ("a", k + 1), ("r", k + 1)]
    return [("a", m), ("r", m), ("r", m + 1)]


def admission_face(m: int, k: int) -> list[Node]:
    """Return Uhat_k in a physically nested, append-only order."""
    face = [("b", 1)]
    for layer in range(k):
        face.extend(canonical_batch(m, layer))
    return face


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
    """Build the exact restricted system in rational degree-scaled coordinates."""
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


def dense_lower(
    matrix: list[list[Fraction]],
    load: list[Fraction],
    trial: list[Fraction],
    anchor: list[Fraction],
    alpha: Fraction,
) -> tuple[Fraction, list[Fraction]]:
    """Evaluate the literal anchored lower map in scaled coordinates."""
    residual = [left - right for left, right in zip(load, matvec(matrix, trial))]
    delta = max([Fraction(0), *(-value for value in residual)]) / alpha
    point = [max(base, value - delta, Fraction(0)) for base, value in zip(anchor, trial)]
    return delta, point


def boundary_demands(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    batch: list[Node],
    point: list[Fraction],
    alpha: Fraction,
    rho: Fraction,
) -> list[Fraction]:
    """Compute exact tree-boundary demands in scaled coordinates."""
    index = {vertex: position for position, vertex in enumerate(face)}
    coupling = (1 - alpha) / 2
    demands: list[Fraction] = []
    for vertex in batch:
        old_neighbors = [neighbor for neighbor in adjacency[vertex] if neighbor in index]
        assert len(old_neighbors) == 1
        parent = old_neighbors[0]
        demands.append(-alpha * rho + coupling * point[index[parent]] / len(adjacency[vertex]))
    return demands


class ExactFaceCarry:
    """Maintain the lazy anchor, raw residual, and exact lazy heap."""

    def __init__(
        self,
        matrix: list[list[Fraction]],
        load: list[Fraction],
        trial: list[Fraction],
        alpha: Fraction,
    ) -> None:
        self.matrix = matrix
        self.load = load
        self.trial = trial[:]
        self.alpha = alpha
        self.base = [Fraction(0) for _ in trial]
        self.marker = [-1 for _ in trial]
        self.tags: list[Fraction] = []
        self.explicit_anchor = [Fraction(0) for _ in trial]
        self.residual = [left - right for left, right in zip(load, matvec(matrix, trial))]
        self.version = [0 for _ in trial]
        self.heap: list[tuple[Fraction, int, int]] = []
        for index in range(len(trial)):
            self._push(index)

    def _key(self, index: int) -> Fraction:
        return max(-self.residual[index], Fraction(0)) / self.alpha

    def _push(self, index: int) -> None:
        heapq.heappush(self.heap, (-self._key(index), self.version[index], index))

    def delta(self) -> Fraction:
        """Return the exact heap maximum."""
        while True:
            negative, version, index = self.heap[0]
            if version == self.version[index] and -negative == self._key(index):
                return -negative
            heapq.heappop(self.heap)

    def anchor_at(self, index: int) -> Fraction:
        """Evaluate one exact lazy-anchor coordinate."""
        pending = self.tags[self.marker[index] + 1 :]
        candidate = Fraction(0)
        if pending:
            candidate = max(self.trial[index] - min(pending), Fraction(0))
        return max(self.base[index], candidate)

    def flush(self, index: int) -> None:
        """Resolve all pending successful tags before a numerical write."""
        self.base[index] = self.anchor_at(index)
        self.marker[index] = len(self.tags) - 1

    def check_exact(self) -> None:
        """Compare every maintained quantity with a dense rebuild."""
        direct = [left - right for left, right in zip(self.load, matvec(self.matrix, self.trial))]
        assert self.residual == direct
        assert self.delta() == max([Fraction(0), *(-value for value in direct)]) / self.alpha
        assert [self.anchor_at(index) for index in range(len(self.trial))] == self.explicit_anchor

    def write(self, column: int, change: Fraction) -> list[int]:
        """Flush, write one numerical coordinate, and locally update the raw state."""
        self.flush(column)
        self.trial[column] += change
        affected = [row for row in range(len(self.trial)) if self.matrix[row][column]]
        for row in affected:
            self.residual[row] -= self.matrix[row][column] * change
            self.version[row] += 1
            self._push(row)
        return affected

    def bulk_replace(self, trial: list[Fraction]) -> None:
        """Charge the semantic flushes and replace a bulk endpoint exactly."""
        assert len(trial) == len(self.trial)
        for index in range(len(self.trial)):
            self.flush(index)
        self.trial = trial[:]
        self.residual = [
            left - right for left, right in zip(self.load, matvec(self.matrix, self.trial))
        ]
        for index in range(len(self.trial)):
            self.version[index] += 1
            self._push(index)

    def transition(
        self,
        new_matrix: list[list[Fraction]],
        new_load: list[Fraction],
    ) -> None:
        """Append one successful scalar tag and exactly three new face records."""
        old_dimension = len(self.trial)
        assert len(new_load) == old_dimension + 3
        delta = self.delta()
        dense_delta, point = dense_lower(
            self.matrix, self.load, self.trial, self.explicit_anchor, self.alpha
        )
        assert delta == dense_delta

        old_residual = self.residual[:]
        old_keys = [self._key(index) for index in range(old_dimension)]
        self.tags.append(delta)
        for _ in range(3):
            self.trial.append(Fraction(0))
            self.base.append(Fraction(0))
            self.marker.append(len(self.tags) - 1)
            self.explicit_anchor.append(Fraction(0))
            self.residual.append(Fraction(0))
            self.version.append(0)
        self.explicit_anchor[:old_dimension] = point
        self.matrix = new_matrix
        self.load = new_load

        direct = [left - right for left, right in zip(new_load, matvec(new_matrix, self.trial))]
        assert direct[:old_dimension] == old_residual
        self.residual = old_residual + direct[old_dimension:]
        for index in range(old_dimension, old_dimension + 3):
            self._push(index)
        assert [self._key(index) for index in range(old_dimension)] == old_keys
        self.check_exact()


def near_exact_success(
    adjacency: dict[Node, set[Node]],
    face: list[Node],
    batch: list[Node],
    matrix: list[list[Fraction]],
    load: list[Fraction],
    exact: list[Fraction],
    anchor: list[Fraction],
    alpha: Fraction,
    rho: Fraction,
) -> list[Fraction]:
    """Find a nonzero-delta rational endpoint whose lower gate is strict."""
    for exponent in range(6, 90, 6):
        trial = exact[:]
        trial[-1] += Fraction(1, 10**exponent)
        delta, point = dense_lower(matrix, load, trial, anchor, alpha)
        demands = boundary_demands(adjacency, face, batch, point, alpha, rho)
        if delta > 0 and all(value > 0 for value in demands):
            return trial
    raise AssertionError("failed to find a strict nonzero-delta endpoint")


def check_chain(m: int, alpha: Fraction, rho: Fraction) -> None:
    """Check every expansion, including the full-support terminal expansion."""
    adjacency = graph(m)
    face = admission_face(m, 0)
    matrix, load = restricted_system(adjacency, face, alpha, rho)
    state = ExactFaceCarry(matrix, load, [Fraction(0)], alpha)

    for k in range(m):
        face = admission_face(m, k)
        batch = canonical_batch(m, k)
        assert len(state.trial) == 3 * k + 1
        exact = solve(state.matrix, state.load)
        assert all(value > 0 for value in exact)
        assert all(base <= value for base, value in zip(state.explicit_anchor, exact))

        # Exercise exact flush-before-write and closed-neighborhood residual updates.
        for step in range(k + 2):
            column = (2 * step + k) % len(face)
            change = Fraction((step % 5) - 2, 101 + 7 * step) * exact[column]
            affected = state.write(column, change)
            expected = [row for row in range(len(face)) if state.matrix[row][column]]
            assert affected == expected
            assert len(affected) <= len(adjacency[face[column]]) + 1
            state.check_exact()

        trial = near_exact_success(
            adjacency,
            face,
            batch,
            state.matrix,
            state.load,
            exact,
            state.explicit_anchor,
            alpha,
            rho,
        )
        state.bulk_replace(trial)
        state.check_exact()
        delta, lower = dense_lower(
            state.matrix, state.load, state.trial, state.explicit_anchor, alpha
        )
        assert delta > 0
        exact_demands = boundary_demands(adjacency, face, batch, exact, alpha, rho)
        lower_demands = boundary_demands(adjacency, face, batch, lower, alpha, rho)
        assert all(value > 0 for value in lower_demands)
        assert all(left <= right for left, right in zip(lower_demands, exact_demands))

        next_face = admission_face(m, k + 1)
        assert next_face == face + batch
        next_matrix, next_load = restricted_system(adjacency, next_face, alpha, rho)
        state.transition(next_matrix, next_load)
        next_exact = solve(next_matrix, next_load)
        assert all(base <= value for base, value in zip(state.explicit_anchor, next_exact))
        assert len(state.tags) == k + 1
        assert state.marker[-3:] == [k, k, k]
        assert state.explicit_anchor[-3:] == [Fraction(0)] * 3

    assert len(state.trial) == 3 * m + 1
    assert state.check_exact() is None


def check_lazy_range_min() -> None:
    """Exercise several unflushed tags on a coordinate with constant numerical value."""
    alpha = Fraction(1, 5)
    matrix = [[Fraction(3, 5)]]
    load = [Fraction(0)]
    state = ExactFaceCarry(matrix, load, [Fraction(7, 5)], alpha)
    state.explicit_anchor = [Fraction(0)]
    state.tags = [Fraction(3, 10), Fraction(1, 4), Fraction(2, 5)]
    state.explicit_anchor[0] = Fraction(23, 20)
    assert state.anchor_at(0) == Fraction(23, 20)
    state.flush(0)
    assert state.base[0] == Fraction(23, 20)
    assert state.marker[0] == 2


def check_ledgers(m: int, q: int) -> None:
    """Check the exact auxiliary shock and every prefix/post partition."""
    adjacency = graph(m)
    support = admission_face(m, m)
    exposed = admission_face(m, q)
    auxiliary_cells = sum(len(admission_face(m, k)) for k in range(q))
    assert auxiliary_cells == q * (3 * q - 1) // 2
    assert sum(len(canonical_batch(m, k)) for k in range(q)) == 3 * q
    assert len(exposed) == 3 * q + 1

    prefix_volume = sum(len(adjacency[vertex]) for vertex in exposed)
    post_volume = sum(len(adjacency[vertex]) for vertex in support if vertex not in exposed)
    assert prefix_volume + post_volume == 6 * m
    prefix_first_exposure_rounds = q + 1
    post_first_exposure_rounds = m - q
    assert prefix_first_exposure_rounds + post_first_exposure_rounds == m + 1
    prefix_interactions = q
    post_interactions = m - q + 1
    assert prefix_interactions + post_interactions == m + 1
    assert 3 * q + len(support) - len(exposed) == 3 * m

    transition_new_keys = sum(len(canonical_batch(m, k)) for k in range(q))
    assert transition_new_keys == 3 * q
    if q == m:
        assert post_volume == 0
        assert len(support) - len(exposed) == 0


def check_stable_labels() -> None:
    """Require every public Round-018 anchor in the note source."""
    source = note_tex_source("hybrid_aesp_locsor")
    labels = (
        "sec:branch-caterpillar-incremental-face-transition",
        "eq:branch-caterpillar-lazy-anchor-state",
        "lem:branch-caterpillar-lazy-anchor",
        "lem:branch-caterpillar-incremental-face-transition",
        "eq:branch-caterpillar-incremental-face-residual",
        "eq:branch-caterpillar-incremental-face-transition-vector",
        "prop:branch-caterpillar-fresh-auxiliary-shock",
        "eq:branch-caterpillar-fresh-auxiliary-shock",
        "def:branch-caterpillar-incremental-face-policy",
        "eq:branch-caterpillar-incremental-face-stage-bound",
        "thm:branch-caterpillar-incremental-face-handoff",
        "eq:branch-caterpillar-incremental-face-prefix-eleven-vector",
        "eq:branch-caterpillar-incremental-face-post-eleven-vector",
        "eq:branch-caterpillar-incremental-face-total-rounds",
    )
    for label in labels:
        assert f"\\label{{{label}}}" in source
    assert "R_{\\rm int}^{\\rm total}=m+1" in source
    assert "R_{\\rm adj}^{\\rm total}" in source
    assert "=m+1+O(\\mathfrak A_{<q}^{\\rm fc})" in source


def main() -> None:
    rho = Fraction(1, 10_000_000)
    for m in range(2, 8):
        for alpha in (Fraction(1, 20), Fraction(1, 5), Fraction(49, 100)):
            check_chain(m, alpha, rho)
        for q in range(2, m + 1):
            check_ledgers(m, q)
    check_lazy_range_min()
    check_stable_labels()
    print("round018 incremental face-transition checks passed")


if __name__ == "__main__":
    main()
