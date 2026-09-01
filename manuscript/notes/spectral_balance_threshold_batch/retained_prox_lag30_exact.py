#!/usr/bin/env python3
"""Exact Q(sqrt(20002)) canonical counterexample to one-step dominance."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F


RADICAND = 20_002
EDGES = (
    (0, 1),
    (0, 2),
    (0, 7),
    (0, 22),
    (0, 29),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 14),
    (2, 19),
    (2, 22),
    (3, 9),
    (3, 16),
    (3, 23),
    (3, 28),
    (4, 10),
    (4, 17),
    (5, 6),
    (7, 8),
    (7, 9),
    (7, 10),
    (7, 21),
    (7, 25),
    (7, 29),
    (8, 11),
    (8, 12),
    (8, 15),
    (9, 10),
    (9, 16),
    (10, 18),
    (10, 28),
    (11, 12),
    (11, 13),
    (11, 15),
    (13, 18),
    (13, 20),
    (13, 24),
    (13, 29),
    (14, 22),
    (17, 28),
    (18, 27),
    (19, 26),
    (20, 22),
    (22, 25),
    (22, 26),
    (23, 24),
    (23, 25),
    (24, 25),
    (25, 28),
)


@dataclass(frozen=True)
class K:
    """An exact element a+b*sqrt(20002)."""

    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def lift(value: object) -> K:
        return value if isinstance(value, K) else K(F(value))

    def __add__(self, other: object) -> K:
        value = K.lift(other)
        return K(self.a + value.a, self.b + value.b)

    __radd__ = __add__

    def __neg__(self) -> K:
        return K(-self.a, -self.b)

    def __sub__(self, other: object) -> K:
        return self + (-K.lift(other))

    def __rsub__(self, other: object) -> K:
        return K.lift(other) - self

    def __mul__(self, other: object) -> K:
        value = K.lift(other)
        return K(
            self.a * value.a + RADICAND * self.b * value.b,
            self.a * value.b + self.b * value.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> K:
        value = K.lift(other)
        denominator = value.a * value.a - RADICAND * value.b * value.b
        assert denominator
        return K(
            (self.a * value.a - RADICAND * self.b * value.b) / denominator,
            (self.b * value.a - self.a * value.b) / denominator,
        )

    def sign(self) -> int:
        if not self.b:
            return (self.a > 0) - (self.a < 0)
        if not self.a:
            return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        rational_square = self.a * self.a
        radical_square = RADICAND * self.b * self.b
        assert rational_square != radical_square
        if self.a > 0:
            return 1 if rational_square > radical_square else -1
        return 1 if radical_square > rational_square else -1

    def __lt__(self, other: object) -> bool:
        return (self - other).sign() < 0

    def __le__(self, other: object) -> bool:
        return (self - other).sign() <= 0

    def __gt__(self, other: object) -> bool:
        return (self - other).sign() > 0

    def __ge__(self, other: object) -> bool:
        return (self - other).sign() >= 0

    def decimal(self) -> Decimal:
        return Decimal(self.a.numerator) / Decimal(self.a.denominator) + (
            Decimal(self.b.numerator)
            / Decimal(self.b.denominator)
            * Decimal(RADICAND).sqrt()
        )


def maximum(values: list[K]) -> K:
    answer = values[0]
    for value in values[1:]:
        if value > answer:
            answer = value
    return answer


def solve_fraction(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    size = len(rhs)
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    left - factor * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(size)]


def main() -> None:
    getcontext().prec = 90
    vertex_count = 30
    neighbors = [set() for _ in range(vertex_count)]
    for left, right in EDGES:
        neighbors[left].add(right)
        neighbors[right].add(left)
    degrees = [len(row) for row in neighbors]
    assert min(degrees) > 0 and degrees[0] == 5 and len(EDGES) == 49

    alpha = F(1, 10_000)
    rho = F(17, 2_000)
    sigma = alpha
    diagonal = (1 + alpha) / 2 + sigma
    coupling = (1 - alpha) / 2
    lipschitz = 1 + sigma
    shifted_gap = alpha + sigma
    root = K(F(0), F(1, 10_001))
    momentum = (1 - root) / (1 + root)
    auxiliary_scale = (1 - root) / root
    assert root * root == K(F(2, 10_001))

    operator = [[F(0) for _ in range(vertex_count)] for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        operator[vertex][vertex] = diagonal
        for neighbor in neighbors[vertex]:
            operator[vertex][neighbor] = -coupling / degrees[vertex]
    original_load = [F(-alpha * rho) for _ in range(vertex_count)]
    original_load[0] += alpha / degrees[0]

    # The phase-zero unconstrained shifted solution is strictly positive.
    # Every later shifted RHS adds alpha*lower>=0, so inverse positivity keeps
    # every later omniscient proximal support equal to the full graph.
    phase_zero_solution = solve_fraction(operator, original_load)
    assert min(phase_zero_solution) > 0
    omniscient_face = set(range(vertex_count))

    def apply(state: list[K], vertex: int, face: set[int] | None = None) -> K:
        active = range(vertex_count) if face is None else face
        return sum((operator[vertex][other] * state[other] for other in active), K())

    def advance(
        face: set[int],
        shifted_load: list[K],
        state: list[K],
        prior: list[K],
        envelope: list[K],
    ) -> tuple[list[K], list[K], list[K]]:
        extrapolated = [K() for _ in range(vertex_count)]
        following = [K() for _ in range(vertex_count)]
        for vertex in face:
            extrapolated[vertex] = state[vertex] + momentum * (
                state[vertex] - prior[vertex]
            )
        for vertex in face:
            residual = shifted_load[vertex] - apply(extrapolated, vertex, face)
            following[vertex] = extrapolated[vertex] + residual / lipschitz
        prior, state = state, following

        shifts = [K()]
        ones = [K(1) for _ in range(vertex_count)]
        for vertex in face:
            residual = shifted_load[vertex] - apply(state, vertex, face)
            stationary = apply(ones, vertex, face)
            shifts.append((-residual) / stationary)
        shift = maximum(shifts)
        for vertex in face:
            candidate = state[vertex] - shift
            if candidate > envelope[vertex] and candidate > 0:
                envelope[vertex] = candidate

        auxiliary = [K() for _ in range(vertex_count)]
        for vertex in face:
            auxiliary[vertex] = state[vertex] + auxiliary_scale * (
                state[vertex] - prior[vertex]
            )
            if state[vertex] < envelope[vertex]:
                state[vertex] = envelope[vertex]
            if auxiliary[vertex] < envelope[vertex]:
                auxiliary[vertex] = envelope[vertex]
            velocity = (auxiliary[vertex] - state[vertex]) / auxiliary_scale
            prior[vertex] = state[vertex] - velocity
        return state, prior, envelope

    lower = [K() for _ in range(vertex_count)]
    certified = {0}
    width = K(F(1, degrees[0]) - rho)
    maximum_deficit = K()
    witness = (-1, -1, -1)
    events: list[tuple[int, int]] = []

    for phase in range(9):
        old_lower = lower[:]
        shifted_load = [
            K(original_load[vertex]) + sigma * old_lower[vertex]
            for vertex in range(vertex_count)
        ]
        requested = width / 4
        current = old_lower[:]
        previous = old_lower[:]
        omniscient_current = old_lower[:]
        omniscient_previous = old_lower[:]
        omniscient_lower = old_lower[:]
        lagged_omniscient_lower = old_lower[:]

        for iteration in range(500):
            current, previous, lower = advance(
                set(certified), shifted_load, current, previous, lower
            )
            omniscient_current, omniscient_previous, omniscient_lower = advance(
                omniscient_face,
                shifted_load,
                omniscient_current,
                omniscient_previous,
                omniscient_lower,
            )

            batch = {
                vertex
                for vertex in range(vertex_count)
                if vertex not in certified
                and shifted_load[vertex] - apply(lower, vertex) > 0
            }
            if batch:
                certified.update(batch)
                events.append((phase, iteration + 1))

            deficits = [
                lagged_omniscient_lower[vertex] - lower[vertex]
                for vertex in range(vertex_count)
            ]
            deficit = maximum(deficits)
            if deficit > maximum_deficit:
                maximum_deficit = deficit
                witness = (phase, iteration + 1, deficits.index(deficit))
            lagged_omniscient_lower = omniscient_lower[:]

            residual_width = maximum(
                [K()]
                + [
                    (shifted_load[vertex] - apply(lower, vertex)) / shifted_gap
                    for vertex in range(vertex_count)
                ]
            )
            if residual_width <= requested:
                width = width / 2 + residual_width
                break
        else:
            raise AssertionError("phase did not reach its exact quarter bracket")

    expected_events = [
        (0, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (6, 2),
        (7, 1),
        (8, 3),
        (8, 4),
        (8, 5),
        (8, 6),
        (8, 69),
        (8, 70),
    ]
    assert events == expected_events
    assert witness == (8, 86, 12)
    assert maximum_deficit > F(28, 100_000)
    print("exact canonical one-step lag counterexample verified")
    print("phase / iteration / vertex =", witness)
    print("deficit =", maximum_deficit.decimal())
    print("events =", events)


if __name__ == "__main__":
    main()
