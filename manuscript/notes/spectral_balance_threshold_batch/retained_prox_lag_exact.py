#!/usr/bin/env python3
"""Exact Q(sqrt(202)) audit of same-time versus lag-one domain dominance.

The four-vertex canonical instance is a strict counterexample to same-time
lower-envelope dominance over an omniscient final-prox-support run.  The
weaker one-step-lag lower, primal, and next-extrapolate inequalities hold
through the witness phase.  The latter checks are evidence for a conjecture,
not a proof for all graphs.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F


RADICAND = 202
EDGES = ((0, 1), (0, 2), (1, 2), (1, 3))


@dataclass(frozen=True)
class K:
    """An exact element a+b*sqrt(202)."""

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
            Decimal(self.b.numerator) / Decimal(self.b.denominator) * Decimal(RADICAND).sqrt()
        )


def maximum(values: list[K]) -> K:
    answer = values[0]
    for value in values[1:]:
        if value > answer:
            answer = value
    return answer


def solve(matrix: list[list[K]], rhs: list[K]) -> list[K]:
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    size = len(rhs)
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column].sign())
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor.sign():
                augmented[row] = [
                    left - factor * right for left, right in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(size)]


def main() -> None:
    getcontext().prec = 60
    vertex_count = 4
    neighbors = [set() for _ in range(vertex_count)]
    for left, right in EDGES:
        neighbors[left].add(right)
        neighbors[right].add(left)
    degrees = [len(row) for row in neighbors]
    assert degrees == [2, 3, 2, 1]

    alpha = F(1, 100)
    rho = F(1, 10)
    sigma = alpha
    diagonal = F(101, 200)
    coupling = F(99, 200)
    lipschitz = F(101, 100)
    shifted_gap = F(1, 50)
    root = K(F(0), F(1, 101))
    momentum = K(F(10403, 9999), F(-202, 9999))
    auxiliary_scale = K(F(-1), F(1, 2))
    assert root * root == K(F(2, 101))
    assert momentum == (1 - root) / (1 + root)

    operator = [[K() for _ in range(vertex_count)] for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        operator[vertex][vertex] = K(diagonal + sigma)
        for neighbor in neighbors[vertex]:
            operator[vertex][neighbor] = K(-coupling / degrees[vertex])

    original_load = [K(-alpha * rho) for _ in range(vertex_count)]
    original_load[0] += alpha / degrees[0]

    def apply(state: list[K], vertex: int, face: set[int] | None = None) -> K:
        active = range(vertex_count) if face is None else face
        return sum((operator[vertex][other] * state[other] for other in active), K())

    def exact_support(load: list[K]) -> set[int]:
        face = {vertex for vertex, value in enumerate(load) if value > 0}
        while face:
            ordered = sorted(face)
            block = [[operator[left][right] for right in ordered] for left in ordered]
            solution = solve(block, [load[vertex] for vertex in ordered])
            assert all(value > 0 for value in solution)
            full = [K() for _ in range(vertex_count)]
            for vertex, value in zip(ordered, solution):
                full[vertex] = value
            batch = {
                vertex
                for vertex in range(vertex_count)
                if vertex not in face and load[vertex] - apply(full, vertex) > 0
            }
            if not batch:
                return face
            face.update(batch)
        return set()

    lower = [K() for _ in range(vertex_count)]
    certified = {0}
    width = K(F(2, 5))
    strict_witness: tuple[int, int, K] | None = None

    for phase in range(8):
        old_lower = lower[:]
        shifted_load = [original_load[i] + sigma * old_lower[i] for i in range(vertex_count)]
        omniscient_face = exact_support(shifted_load)
        requested = width / 4

        current = old_lower[:]
        previous = old_lower[:]
        omniscient_current = old_lower[:]
        omniscient_previous = old_lower[:]
        omniscient_lower = old_lower[:]
        lag_lower = old_lower[:]
        lag_current = old_lower[:]
        lag_extrapolate = old_lower[:]

        for iteration in range(30):
            scratch = set(certified)

            def advance(
                face: set[int],
                state: list[K],
                prior: list[K],
                envelope: list[K],
            ) -> tuple[list[K], list[K], list[K], list[K]]:
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
                for vertex in face:
                    residual = shifted_load[vertex] - apply(state, vertex, face)
                    stationary = apply([K(1) for _ in range(vertex_count)], vertex, face)
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
                next_extrapolate = [
                    (state[vertex] + root * auxiliary[vertex]) / (1 + root)
                    for vertex in range(vertex_count)
                ]
                return state, prior, envelope, next_extrapolate

            current, previous, lower, masked_extrapolate = advance(
                scratch,
                current,
                previous,
                lower,
            )
            (
                omniscient_current,
                omniscient_previous,
                omniscient_lower,
                omniscient_extrapolate,
            ) = advance(
                omniscient_face,
                omniscient_current,
                omniscient_previous,
                omniscient_lower,
            )

            batch = {
                vertex
                for vertex in range(vertex_count)
                if vertex not in certified and shifted_load[vertex] - apply(lower, vertex) > 0
            }
            certified.update(batch)

            assert all(lower[i] >= lag_lower[i] for i in range(vertex_count))
            assert all(current[i] >= lag_current[i] for i in range(vertex_count))
            assert all(masked_extrapolate[i] >= lag_extrapolate[i] for i in range(vertex_count))
            assert all(lower[i] >= lag_current[i] for i in range(vertex_count))
            assert all(lower[i] >= lag_extrapolate[i] for i in range(vertex_count))

            deficits = [omniscient_lower[i] - lower[i] for i in range(vertex_count)]
            deficit = maximum(deficits)
            if deficit > 0 and (strict_witness is None or deficit > strict_witness[2]):
                strict_witness = (phase, iteration + 1, deficit)

            lag_lower = omniscient_lower[:]
            lag_current = omniscient_current[:]
            lag_extrapolate = omniscient_extrapolate[:]

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

    assert strict_witness is not None
    phase, iteration, deficit = strict_witness
    print("same-time dominance fails exactly at phase/iteration =", phase, iteration)
    print("strict lower deficit =", deficit.decimal())
    print(
        "lag-one lower dominance over the omniscient lower/primal/extrapolate "
        "states verified through phase 7"
    )


if __name__ == "__main__":
    main()
