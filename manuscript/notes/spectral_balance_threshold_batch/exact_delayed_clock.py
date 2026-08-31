#!/usr/bin/env python3
"""Exact Q(sqrt(10)) certificate for the 34-vertex delayed NAG event trace.

Conjugating the normalized recurrence by x=D^(1/2)y makes every coefficient
rational except sqrt(alpha)=sqrt(10)/100.  The quadratic-field class below
therefore certifies every branch of the moving-face recurrence exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F


EDGES = [
    (0, 1),
    (1, 2),
    (2, 3),
    (2, 20),
    (3, 4),
    (3, 9),
    (3, 18),
    (4, 5),
    (4, 11),
    (4, 13),
    (4, 17),
    (5, 6),
    (5, 11),
    (5, 19),
    (6, 7),
    (6, 22),
    (7, 8),
    (8, 9),
    (8, 33),
    (9, 10),
    (9, 12),
    (9, 24),
    (9, 33),
    (10, 11),
    (10, 15),
    (10, 25),
    (11, 12),
    (11, 19),
    (11, 20),
    (12, 13),
    (12, 16),
    (12, 17),
    (13, 14),
    (13, 19),
    (13, 24),
    (14, 15),
    (14, 16),
    (14, 18),
    (14, 26),
    (15, 26),
    (15, 30),
    (16, 17),
    (16, 28),
    (17, 20),
    (18, 19),
    (18, 25),
    (19, 20),
    (19, 32),
    (20, 21),
    (20, 28),
    (21, 22),
    (21, 30),
    (22, 23),
    (22, 29),
    (23, 25),
    (23, 30),
    (24, 25),
    (24, 32),
    (25, 26),
    (25, 27),
    (26, 27),
    (27, 28),
    (27, 29),
    (27, 32),
    (28, 29),
    (29, 30),
    (30, 31),
    (31, 32),
    (32, 33),
]


@dataclass(frozen=True)
class K:
    """An exact element a+b*sqrt(10)."""

    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def lift(value: object) -> "K":
        return value if isinstance(value, K) else K(F(value), F(0))

    def __add__(self, other: object) -> "K":
        value = K.lift(other)
        return K(self.a + value.a, self.b + value.b)

    __radd__ = __add__

    def __neg__(self) -> "K":
        return K(-self.a, -self.b)

    def __sub__(self, other: object) -> "K":
        return self + (-K.lift(other))

    def __rsub__(self, other: object) -> "K":
        return K.lift(other) - self

    def __mul__(self, other: object) -> "K":
        value = K.lift(other)
        return K(
            self.a * value.a + 10 * self.b * value.b,
            self.a * value.b + self.b * value.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> "K":
        value = K.lift(other)
        denominator = value.a * value.a - 10 * value.b * value.b
        assert denominator != 0
        return K(
            (self.a * value.a - 10 * self.b * value.b) / denominator,
            (self.b * value.a - self.a * value.b) / denominator,
        )

    def sign(self) -> int:
        """Return the exact sign using only rational comparisons."""
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        rational_square = self.a * self.a
        radical_square = 10 * self.b * self.b
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
        return (
            Decimal(self.a.numerator) / Decimal(self.a.denominator)
            + (Decimal(self.b.numerator) / Decimal(self.b.denominator)) * Decimal(10).sqrt()
        )


def maximum(values: list[K]) -> K:
    answer = values[0]
    for value in values[1:]:
        if value > answer:
            answer = value
    return answer


def minimum(values: list[K]) -> K:
    answer = values[0]
    for value in values[1:]:
        if value < answer:
            answer = value
    return answer


def solve_fraction(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve a rational system exactly by Gaussian elimination."""
    dimension = len(rhs)
    augmented = [matrix[row][:] + [rhs[row]] for row in range(dimension)]
    for column in range(dimension):
        pivot = next(row for row in range(column, dimension) if augmented[row][column] != 0)
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        pivot_value = augmented[column][column]
        for row in range(column + 1, dimension):
            if augmented[row][column] == 0:
                continue
            factor = augmented[row][column] / pivot_value
            for entry in range(column, dimension + 1):
                augmented[row][entry] -= factor * augmented[column][entry]
    answer = [F(0) for _ in range(dimension)]
    for row in range(dimension - 1, -1, -1):
        tail = sum(
            (augmented[row][column] * answer[column] for column in range(row + 1, dimension)),
            F(0),
        )
        answer[row] = (augmented[row][dimension] - tail) / augmented[row][row]
    return answer


def main() -> None:
    getcontext().prec = 60
    vertex_count = 34
    neighbors = [set() for _ in range(vertex_count)]
    assert len(EDGES) == len(set(EDGES)) == 69
    for left, right in EDGES:
        assert 0 <= left < right < vertex_count
        neighbors[left].add(right)
        neighbors[right].add(left)
    degrees = [len(row) for row in neighbors]
    assert min(degrees) > 0 and degrees[0] == 1
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in neighbors[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    assert len(seen) == vertex_count and sum(degrees) == 138

    alpha = F(1, 1000)
    rho = F(1, 100000)
    objective_tolerance = F(1, 10**20)
    publication_threshold_squared = alpha * rho * objective_tolerance / 256
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    beta = K(F(1001, 999), F(-20, 999))
    auxiliary_scale = K(F(-1), F(10))
    assert beta == (K(1) - K(F(0), F(1, 100))) / (K(1) + K(F(0), F(1, 100)))

    # D^(-1/2) times the canonical normalized point-source load.
    conjugated_load = [F(-alpha * rho) for _ in range(vertex_count)]
    conjugated_load[0] += alpha / degrees[0]
    assert rho * sum(degrees) == F(69, 50000)

    # The unrestricted rational center is strictly positive.  Since H is
    # Stieltjes positive definite, the obstacle solution is this center and
    # the exact canonical support S* is all 34 vertices.
    full_matrix = [[F(0) for _ in range(vertex_count)] for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        full_matrix[vertex][vertex] = diagonal * degrees[vertex]
    for left, right in EDGES:
        full_matrix[left][right] = -coupling
        full_matrix[right][left] = -coupling
    full_center = solve_fraction(
        full_matrix,
        [degrees[vertex] * conjugated_load[vertex] for vertex in range(vertex_count)],
    )
    assert all(coordinate > 0 for coordinate in full_center)

    scratch = {0}
    certified = {0}
    current = [K() for _ in range(vertex_count)]
    previous = [K() for _ in range(vertex_count)]
    lower = [K() for _ in range(vertex_count)]
    events: list[tuple[int, tuple[int, ...]]] = []
    event_minima: list[K] = []
    quiet_maxima: list[K] = []
    quiet_early_stop_ratios: list[K] = []

    def h_apply(state: list[K], vertex: int) -> K:
        return diagonal * degrees[vertex] * state[vertex] - coupling * sum(
            (state[neighbor] for neighbor in neighbors[vertex]), K()
        )

    for iteration in range(39):
        extrapolated = [K() for _ in range(vertex_count)]
        next_iterate = [K() for _ in range(vertex_count)]
        for vertex in scratch:
            extrapolated[vertex] = current[vertex] + beta * (current[vertex] - previous[vertex])
        for vertex in scratch:
            neighbor_sum = sum(
                (extrapolated[neighbor] for neighbor in neighbors[vertex] if neighbor in scratch),
                K(),
            )
            next_iterate[vertex] = (
                coupling * (extrapolated[vertex] + neighbor_sum / degrees[vertex])
                + conjugated_load[vertex]
            )
        previous, current = current, next_iterate

        # Common retraction along 1 in degree coordinates.
        ratios: list[K] = []
        for vertex in scratch:
            active_residual = degrees[vertex] * conjugated_load[vertex] - h_apply(current, vertex)
            stationary = diagonal * degrees[vertex] - coupling * len(neighbors[vertex] & scratch)
            assert stationary > 0
            ratios.append((-active_residual) / stationary)
        shift = maximum([K()] + ratios)
        for vertex in scratch:
            candidate = current[vertex] - shift
            if candidate > lower[vertex]:
                lower[vertex] = candidate

        active_lower_residuals = {
            vertex: degrees[vertex] * conjugated_load[vertex] - h_apply(lower, vertex)
            for vertex in scratch
        }
        assert all(lower[vertex] >= 0 for vertex in scratch)
        assert all(residual.sign() >= 0 for residual in active_lower_residuals.values())

        # Project both physical states above the historical lower envelope.
        auxiliary = [K() for _ in range(vertex_count)]
        for vertex in scratch:
            auxiliary[vertex] = current[vertex] + auxiliary_scale * (
                current[vertex] - previous[vertex]
            )
            if current[vertex] < lower[vertex]:
                current[vertex] = lower[vertex]
            if auxiliary[vertex] < lower[vertex]:
                auxiliary[vertex] = lower[vertex]
            velocity = (auxiliary[vertex] - current[vertex]) / auxiliary_scale
            previous[vertex] = current[vertex] - velocity

        outside = sorted(set(range(vertex_count)) - certified)
        residuals = {
            vertex: degrees[vertex] * conjugated_load[vertex] - h_apply(lower, vertex)
            for vertex in outside
        }
        batch = tuple(vertex for vertex in outside if residuals[vertex] > 0)
        if batch:
            # For epsilon_obj=1e-20, the exact-positive and manuscript
            # threshold publication batches coincide.
            assert all(
                residuals[vertex] * residuals[vertex]
                > degrees[vertex] * publication_threshold_squared
                for vertex in batch
            )
            events.append((iteration, batch))
            event_minima.append(minimum([residuals[vertex] for vertex in batch]))
            scratch.update(batch)
            certified.update(batch)
        elif outside:
            largest = maximum(list(residuals.values()))
            assert largest <= 0
            assert largest == K(F(-1, 50_000_000))
            # This is exactly the implementation's active early-stop norm:
            # normalized-coordinate residual divided once more by sqrt(d).
            scaled_active = [active_lower_residuals[vertex] / degrees[vertex] for vertex in scratch]
            norm_squared = sum(
                (coordinate * coordinate for coordinate in scaled_active),
                K(),
            )
            assert norm_squared > F(1, 10**20)
            quiet_early_stop_ratios.append(norm_squared / F(1, 10**20))
            quiet_maxima.append(largest)

    expected = [
        (0, (1,)),
        (1, (2,)),
        (2, (3, 20)),
        (3, (4, 9, 11, 17, 18, 19, 21, 28)),
        (4, (5, 8, 10, 12, 13, 14, 16, 22, 24, 25, 27, 29, 30, 32, 33)),
        (38, (6, 7, 15, 23, 26, 31)),
    ]
    assert events == expected
    assert len(certified) == vertex_count
    assert len(quiet_maxima) == 33

    worst_quiet = maximum(quiet_maxima)
    print("exact_field=Q(sqrt(10)) comparisons=pass")
    print("events=", events)
    print("event_min_residuals=", [value.decimal() for value in event_minima])
    print("eps_obj=1e-20 thresholded_batches=same")
    print("quiet_iterations=5..37 count=", len(quiet_maxima))
    print("largest_quiet_residual_decimal=", worst_quiet.decimal())
    print("iteration37_largest_residual_decimal=", quiet_maxima[-1].decimal())
    print(
        "minimum_early_stop_squared_ratio=",
        minimum(quiet_early_stop_ratios).decimal(),
    )


if __name__ == "__main__":
    main()
