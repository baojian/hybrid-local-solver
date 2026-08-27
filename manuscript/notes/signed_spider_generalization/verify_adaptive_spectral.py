"""Exact audits for certified spectral tuning and finite propagation."""

from __future__ import annotations

from fractions import Fraction

RationalMatrix = list[list[Fraction]]


def matvec(matrix: RationalMatrix, vector: list[Fraction]) -> list[Fraction]:
    """Multiply an exact rational matrix and vector."""
    return [
        sum((entry * vector[column] for column, entry in enumerate(row)), Fraction())
        for row in matrix
    ]


def funnel_blocks(depth: int) -> tuple[RationalMatrix, RationalMatrix, RationalMatrix]:
    """Return the semantic A, C, and K=AC blocks of the layered funnel."""
    weights = [3 ** (depth - 1 - layer) for layer in range(depth)]
    red_degrees = [weights[0]]
    red_degrees.extend(weights[layer - 1] + weights[layer] for layer in range(1, depth))
    red_degrees.append(weights[-1])

    red_from_blue = [[Fraction() for _ in range(depth)] for _ in range(depth + 1)]
    blue_from_red = [[Fraction() for _ in range(depth + 1)] for _ in range(depth)]
    for layer, weight in enumerate(weights):
        red_from_blue[layer][layer] = Fraction(weight, red_degrees[layer])
        red_from_blue[layer + 1][layer] = Fraction(weight, red_degrees[layer + 1])
        blue_from_red[layer][layer] = Fraction(1, 2)
        blue_from_red[layer][layer + 1] = Fraction(1, 2)

    two_step = [
        [
            sum(
                (
                    red_from_blue[row][layer] * blue_from_red[layer][column]
                    for layer in range(depth)
                ),
                Fraction(),
            )
            for column in range(depth + 1)
        ]
        for row in range(depth + 1)
    ]
    return red_from_blue, blue_from_red, two_step


def check_certified_upper_tuning() -> int:
    """Check safe upper spectral advice and the required squared-gap accuracy."""
    cells = 0
    # Rational points on rho^2+t^2=1 keep every trace calculation exact.
    for u, v in ((2, 1), (3, 1), (4, 1), (3, 2), (5, 2), (5, 3)):
        denominator = u * u + v * v
        rho = Fraction(2 * u * v, denominator)
        true_t = Fraction(u * u - v * v, denominator)
        assert rho * rho + true_t * true_t == 1
        for gamma in (Fraction(1, 3), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
            advised_t = gamma * true_t
            advised_rho_sq = 1 - advised_t * advised_t
            assert rho * rho <= advised_rho_sq < 1
            assert advised_rho_sq - rho * rho == (1 - gamma * gamma) * true_t * true_t
            omega = 2 / (1 + advised_t)
            zeta = omega - 1
            assert omega * omega * advised_rho_sq == 4 * zeta
            for fraction in (
                Fraction(0),
                Fraction(1, 4),
                Fraction(1, 2),
                Fraction(3, 4),
                Fraction(1),
            ):
                coupling_sq = rho * rho * fraction * fraction
                trace = 2 * (1 - omega) + omega * omega * coupling_sq
                determinant = (1 - omega) ** 2
                assert determinant == zeta * zeta
                assert -2 * zeta <= trace <= 2 * zeta
                cells += 1

        # A Rayleigh/power estimate from below is unsafe if treated as an upper bound.
        underestimated_t = (1 + true_t) / 2
        underestimated_rho_sq = 1 - underestimated_t * underestimated_t
        assert rho * rho > underestimated_rho_sq
        unsafe_omega = 2 / (1 + underestimated_t)
        unsafe_zeta = unsafe_omega - 1
        true_top_trace = 2 * (1 - unsafe_omega) + unsafe_omega**2 * rho**2
        assert unsafe_omega**2 * underestimated_rho_sq == 4 * unsafe_zeta
        assert true_top_trace > 2 * unsafe_zeta
    return cells


def collatz_component_bounds(
    cross: RationalMatrix,
    initial: list[Fraction],
    steps: int,
) -> list[tuple[Fraction, Fraction]]:
    """Return exact Collatz bounds for M=(I+J)/2 on one component."""
    red_size = len(cross)
    blue_size = len(cross[0])
    size = red_size + blue_size
    matrix = [[Fraction(row == column, 2) for column in range(size)] for row in range(size)]
    for red in range(red_size):
        for blue in range(blue_size):
            value = cross[red][blue] / 2
            matrix[red][red_size + blue] = value
            matrix[red_size + blue][red] = value

    current = initial
    bounds: list[tuple[Fraction, Fraction]] = []
    for _ in range(steps):
        following = matvec(matrix, current)
        ratios = [next_value / value for next_value, value in zip(following, current, strict=True)]
        bounds.append((min(ratios), max(ratios)))
        current = following
    return bounds


def check_collatz_face_certificate() -> int:
    """Audit component bounds, aggregation, certification, and full-face scope."""
    pythagorean_red = (Fraction(3, 5), Fraction(4, 5))
    pythagorean_blue = (Fraction(5, 13), Fraction(12, 13))

    def rank_one_cross(singular: Fraction) -> RationalMatrix:
        return [[singular * red * blue for blue in pythagorean_blue] for red in pythagorean_red]

    components = (
        ([[Fraction(3, 5)]], [Fraction(1), Fraction(3)], Fraction(3, 5)),
        (
            rank_one_cross(Fraction(4, 5)),
            [Fraction(1), Fraction(2), Fraction(3), Fraction(5)],
            Fraction(4, 5),
        ),
    )
    component_bounds: list[list[tuple[Fraction, Fraction]]] = []
    cells = 0
    for cross, initial, singular in components:
        bounds = collatz_component_bounds(cross, initial, 48)
        perron = (1 + singular) / 2
        for index, (lower, upper) in enumerate(bounds):
            assert lower <= perron <= upper
            if index:
                assert bounds[index - 1][0] <= lower
                assert upper <= bounds[index - 1][1]
            sigma_lower = max(Fraction(), 2 * lower - 1)
            sigma_upper = min(Fraction(1), 2 * upper - 1)
            assert sigma_lower <= singular <= sigma_upper
            cells += 1
        component_bounds.append(bounds)

    coupling = Fraction(9, 10)
    true_sigma = Fraction(4, 5)
    true_radius = coupling * true_sigma
    gamma = Fraction(1, 2)
    certified_step = None
    for step in range(48):
        sigma_lower = max(max(Fraction(), 2 * bounds[step][0] - 1) for bounds in component_bounds)
        sigma_upper = max(min(Fraction(1), 2 * bounds[step][1] - 1) for bounds in component_bounds)
        assert sigma_lower <= true_sigma <= sigma_upper
        radius_lower = coupling * sigma_lower
        radius_upper = coupling * sigma_upper
        if 1 - radius_upper**2 >= gamma**2 * (1 - radius_lower**2):
            assert 1 - radius_upper**2 >= gamma**2 * (1 - true_radius**2)
            certified_step = step + 1
            break
    assert certified_step is not None

    # On a complete connected face sigma=1.  Clipping every valid Collatz
    # upper bound gives exactly the graph-global scaled radius.
    full_bounds = collatz_component_bounds(
        rank_one_cross(Fraction(1)),
        [Fraction(1), Fraction(2), Fraction(3), Fraction(5)],
        48,
    )
    full_certified = None
    for step, (lower, upper) in enumerate(full_bounds, start=1):
        sigma_lower = max(Fraction(), 2 * lower - 1)
        sigma_upper = min(Fraction(1), 2 * upper - 1)
        assert sigma_upper == 1
        radius_lower = coupling * sigma_lower
        radius_upper = coupling * sigma_upper
        assert radius_upper == coupling
        if 1 - radius_upper**2 >= gamma**2 * (1 - radius_lower**2):
            full_certified = step
            break
    assert full_certified is not None

    print(
        "collatz_face_certificate=component_monotonicity:pass aggregation:pass "
        f"certified_step={certified_step} full_face_step={full_certified} "
        "full_face_advice=global"
    )
    return cells + 2


def relaxation(sweep: int, coordinate: int, color: int) -> Fraction:
    """One deterministic nonconstant relaxation schedule in (0,2)."""
    return Fraction(2 + ((3 * sweep + coordinate + color) % 4), 3)


def check_scalar_adaptive_sor_support() -> int:
    """Check that arbitrary scalar relaxations do not outrun the light cone."""
    cells = 0
    for depth in range(2, 13):
        red_from_blue, blue_from_red, _ = funnel_blocks(depth)
        alpha = Fraction(1, (depth + 1) ** 2)
        coupling = (1 - alpha) / (1 + alpha)
        red = [Fraction() for _ in range(depth + 1)]
        blue = [Fraction() for _ in range(depth)]
        for sweep in range(1, depth + 1):
            red_average = matvec(red_from_blue, blue)
            red = [
                (1 - relaxation(sweep, vertex, 0)) * value
                + relaxation(sweep, vertex, 0)
                * (coupling * red_average[vertex] + Fraction(vertex == 0))
                for vertex, value in enumerate(red)
            ]
            blue_average = matvec(blue_from_red, red)
            blue = [
                (1 - relaxation(sweep, vertex, 1)) * value
                + relaxation(sweep, vertex, 1) * coupling * blue_average[vertex]
                for vertex, value in enumerate(blue)
            ]
            assert red[sweep:] == [Fraction()] * (depth + 1 - sweep)
            assert blue[sweep:] == [Fraction()] * (depth - sweep)
            assert red[-1] == 0

        # The block order is essential.  A single interleaved Gauss--Seidel
        # permutation r0,B0,r1,B1,...,rn carries a nonzero value to rn.
        red = [Fraction() for _ in range(depth + 1)]
        blue = [Fraction() for _ in range(depth)]
        red[0] = 1
        for layer in range(depth):
            blue[layer] = coupling * sum(
                (blue_from_red[layer][vertex] * red[vertex] for vertex in range(depth + 1)),
                Fraction(),
            )
            red[layer + 1] = coupling * sum(
                (red_from_blue[layer + 1][channel] * blue[channel] for channel in range(depth)),
                Fraction(),
            )
        assert red[-1] > 0
        cells += 1
    return cells


def check_source_krylov_support() -> int:
    """Check polynomial and three-term source-Krylov finite propagation."""
    cells = 0
    for depth in range(2, 17):
        red_from_blue, blue_from_red, two_step = funnel_blocks(depth)
        source = [Fraction(1)] + [Fraction()] * depth
        powers = [source]
        for degree in range(1, depth + 1):
            powers.append(matvec(two_step, powers[-1]))
            if degree < depth:
                assert powers[-1][-1] == 0
        assert powers[depth][-1] > 0

        # Adaptive scalar coefficients can use all earlier scalar history but
        # cannot move a source-Krylov vector outside the same polynomial span.
        for dimension in range(1, depth + 1):
            iterate = [
                sum(
                    (
                        Fraction((basis + 1) * (dimension + 2), dimension + basis + 3)
                        * powers[basis][coordinate]
                        for basis in range(dimension)
                    ),
                    Fraction(),
                )
                for coordinate in range(depth + 1)
            ]
            assert iterate[-1] == 0

        # A literal variable-coefficient three-term recurrence remains in
        # span{e0,K e0,...}; after k states its degree is at most k-1.
        previous = [Fraction() for _ in range(depth + 1)]
        current = source.copy()
        assert current[-1] == 0
        for step in range(1, depth):
            product = matvec(two_step, current)
            following = [
                Fraction(step + 1, step + 2) * product[index]
                - Fraction(step, 2 * step + 1) * current[index]
                + Fraction(1, step + 3) * previous[index]
                + Fraction(1, (step + 2) ** 2) * source[index]
                for index in range(depth + 1)
            ]
            assert following[-1] == 0
            previous, current = current, following

        # This semantic PageRank operator is diagonally similar to the
        # symmetric normalized Q and has the same one-hop sparsity.  Hence a
        # degree-d polynomial cannot reach graph distance 2*depth before that
        # degree, irrespective of its scalar coefficients.
        alpha = Fraction(1, (depth + 1) ** 2)
        coupling = (1 - alpha) / (1 + alpha)
        size = 2 * depth + 1
        full_q = [[Fraction(row == column) for column in range(size)] for row in range(size)]
        for red_vertex in range(depth + 1):
            for blue_vertex in range(depth):
                full_q[red_vertex][depth + 1 + blue_vertex] -= (
                    coupling * red_from_blue[red_vertex][blue_vertex]
                )
        for blue_vertex in range(depth):
            for red_vertex in range(depth + 1):
                full_q[depth + 1 + blue_vertex][red_vertex] -= (
                    coupling * blue_from_red[blue_vertex][red_vertex]
                )
        full_source = [Fraction(1)] + [Fraction()] * (size - 1)
        full_power = full_source
        for degree in range(1, 2 * depth + 1):
            full_power = matvec(full_q, full_power)
            if degree < 2 * depth:
                assert full_power[depth] == 0
        assert full_power[depth] != 0
        cells += 1
    return cells


def main() -> None:
    tuning = check_certified_upper_tuning()
    collatz = check_collatz_face_certificate()
    adaptive = check_scalar_adaptive_sor_support()
    krylov = check_source_krylov_support()
    print(
        "adaptive spectral checks passed: "
        f"{tuning + collatz + adaptive + krylov} cells "
        f"({tuning} certified-tuning, {collatz} Collatz, "
        f"{adaptive} scalar-SOR, {krylov} Krylov)"
    )


if __name__ == "__main__":
    main()
