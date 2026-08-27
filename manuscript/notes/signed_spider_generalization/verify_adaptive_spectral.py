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
    adaptive = check_scalar_adaptive_sor_support()
    krylov = check_source_krylov_support()
    print(
        "adaptive spectral checks passed: "
        f"{tuning + adaptive + krylov} cells "
        f"({tuning} certified-tuning, {adaptive} scalar-SOR, {krylov} Krylov)"
    )


if __name__ == "__main__":
    main()
