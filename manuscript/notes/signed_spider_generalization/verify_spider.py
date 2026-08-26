"""Deterministic numerical audit for the signed spider generalization note."""

from __future__ import annotations

from itertools import combinations
from math import cos, pi, sqrt

import numpy as np
from numpy.typing import NDArray


Array = NDArray[np.float64]


def mode_matrix(alpha: float, sigma: float, omega: float) -> Array:
    """Return one red--black SOR singular-mode matrix."""
    c_alpha = (1.0 - alpha) / (1.0 + alpha)
    coupling = c_alpha * sigma
    return np.array(
        [
            [1.0 - omega, omega * coupling],
            [omega * coupling * (1.0 - omega), 1.0 - omega + omega**2 * coupling**2],
        ]
    )


def check_sor_modes() -> int:
    """Check the optimal radius and finite power estimate mode by mode."""
    cells = 0
    for alpha in (1e-4, 0.01, 0.1, 0.49, 0.9):
        c_alpha = (1.0 - alpha) / (1.0 + alpha)
        for sigma_max in (0.1, 0.5, 0.9, 1.0):
            rho = c_alpha * sigma_max
            t_value = sqrt(1.0 - rho**2)
            omega = 2.0 / (1.0 + t_value)
            zeta = omega - 1.0
            for fraction in (0.0, 0.2, 0.7, 1.0):
                matrix = mode_matrix(alpha, fraction * sigma_max, omega)
                radius = max(abs(np.linalg.eigvals(matrix)))
                # The extremal block has a repeated eigenvalue, for which
                # generic floating eigensolvers lose a few square-root-epsilon digits.
                assert radius <= zeta + 5e-8
                if fraction == 1.0:
                    assert abs(radius - zeta) <= 5e-8
                for power in range(1, 13):
                    lhs = np.linalg.norm(np.linalg.matrix_power(matrix, power), 2)
                    rhs = 6.0 * power * zeta ** (power - 1)
                    assert lhs <= rhs + 2e-11
                cells += 1
    return cells


def spider_normalized_adjacency(arms: int, depth: int) -> Array:
    """Build the ambient-degree normalized adjacency of a truncated spider."""
    size = 1 + arms * depth
    matrix = np.zeros((size, size))
    degrees = np.array([float(arms), *([2.0] * (arms * depth))])
    for arm in range(arms):
        previous = 0
        for level in range(depth):
            vertex = 1 + arm * depth + level
            weight = 1.0 / sqrt(degrees[previous] * degrees[vertex])
            matrix[previous, vertex] = weight
            matrix[vertex, previous] = weight
            previous = vertex
    return matrix


def check_spider_spectrum() -> int:
    """Check the exact Perron value and the alpha-plus-depth scale."""
    cells = 0
    for arms in (1, 2, 5, 11):
        for depth in range(1, 10):
            matrix = spider_normalized_adjacency(arms, depth)
            observed = max(np.linalg.eigvalsh(matrix))
            expected = cos(pi / (2.0 * (depth + 1)))
            assert abs(observed - expected) <= 3e-12
            for alpha in (1e-4, 0.01, 0.2, 0.8):
                c_alpha = (1.0 - alpha) / (1.0 + alpha)
                t_squared = 1.0 - (c_alpha * observed) ** 2
                scale = alpha + depth**-2
                assert 0.05 * scale <= t_squared <= 5.0 * scale
                cells += 1
    return cells


def radial_profile(alpha: float, arms: int, depth: int) -> Array:
    """Return the exact hub-seeded semantic PPR profile by depth."""
    root_alpha = sqrt(alpha)
    lambda_alpha = (1.0 - root_alpha) / (1.0 + root_alpha)
    reflected = lambda_alpha ** (2 * depth)
    center = root_alpha / arms * (1.0 + reflected) / (1.0 - reflected)
    levels = np.arange(depth + 1)
    return (
        center * (lambda_alpha**levels + lambda_alpha ** (2 * depth - levels)) / (1.0 + reflected)
    )


def path_neighbor_average(values: Array) -> Array:
    """Return the reflecting nearest-neighbor average on a finite arm."""
    depth = len(values) - 1
    average = np.empty_like(values)
    average[0] = values[1]
    average[depth] = values[depth - 1]
    if depth > 1:
        average[1:depth] = 0.5 * (values[: depth - 1] + values[2:])
    return average


def semantic_sor_sweep(values: Array, alpha: float) -> Array:
    """Apply one even-then-odd optimal SOR sweep in semantic coordinates."""
    root_alpha = sqrt(alpha)
    lambda_alpha = (1.0 - root_alpha) / (1.0 + root_alpha)
    zeta = lambda_alpha**2
    c_alpha = (1.0 - alpha) / (1.0 + alpha)
    omega = 1.0 + zeta
    updated = values.copy()
    for parity in (0, 1):
        average = path_neighbor_average(updated)
        updated[parity::2] = -zeta * updated[parity::2] + omega * c_alpha * average[parity::2]
    return updated


def reflected_colors(values: Array) -> tuple[Array, Array]:
    """Split the even reflection of a depth profile into two cyclic colors."""
    reflected_cycle = np.concatenate((values, values[-2:0:-1]))
    return reflected_cycle[0::2], reflected_cycle[1::2]


def cyclic_two_step_average(values: Array) -> Array:
    """Apply M=(L+L^-1)/2 on one color cycle."""
    return 0.5 * (np.roll(values, 1) + np.roll(values, -1))


def check_radial_semantic_damping() -> int:
    """Check the Chebyshev recurrence, mismatches, and log-free envelope."""
    cells = 0
    for alpha in (1e-4, 1e-3, 0.01, 0.1, 0.4, 0.8):
        root_alpha = sqrt(alpha)
        lambda_alpha = (1.0 - root_alpha) / (1.0 + root_alpha)
        zeta = lambda_alpha**2
        c_alpha = (1.0 - alpha) / (1.0 + alpha)
        gamma_alpha = 1.0 - c_alpha
        max_sweeps = min(500, max(12, round(4.0 / root_alpha)))
        for arms in (1, 3, 17):
            for depth in (1, 2, 3, 4, 7, 12, 25, 50):
                profile = radial_profile(alpha, arms, depth)
                center = profile[0]
                residual = profile - c_alpha * path_neighbor_average(profile)
                expected = np.zeros_like(profile)
                expected[0] = gamma_alpha / arms
                assert np.max(np.abs(residual - expected)) <= 3e-12
                assert np.max(profile) == center

                previous_even, previous_odd = reflected_colors(profile)
                iterate = profile.copy()
                first = semantic_sor_sweep(iterate, alpha)
                first_even, first_odd = reflected_colors(first)
                for initial, after_one in (
                    (previous_even, first_even),
                    (previous_odd, first_odd),
                ):
                    mismatch = after_one / zeta - cyclic_two_step_average(initial)
                    assert np.max(np.abs(mismatch)) <= (2.0 * (1.0 - zeta) * center + 3e-12)

                penultimate_even: Array | None = None
                penultimate_odd: Array | None = None
                last_even: Array | None = None
                last_odd: Array | None = None
                for sweep in range(max_sweeps + 1):
                    even, odd = reflected_colors(iterate)
                    if (
                        penultimate_even is not None
                        and penultimate_odd is not None
                        and last_even is not None
                        and last_odd is not None
                    ):
                        predicted_even = (
                            2.0 * zeta * cyclic_two_step_average(last_even)
                            - zeta**2 * penultimate_even
                        )
                        predicted_odd = (
                            2.0 * zeta * cyclic_two_step_average(last_odd)
                            - zeta**2 * penultimate_odd
                        )
                        assert np.max(np.abs(even - predicted_even)) <= 4e-12
                        assert np.max(np.abs(odd - predicted_odd)) <= 4e-12

                    observed = np.max(np.abs(iterate))
                    bound = zeta**sweep * (1.0 + 2.0 * sweep * (1.0 - zeta)) * center
                    assert observed <= bound * (1.0 + 3e-10) + 3e-12
                    cells += 1
                    penultimate_even, last_even = last_even, even
                    penultimate_odd, last_odd = last_odd, odd
                    iterate = semantic_sor_sweep(iterate, alpha)
    return cells


def check_sweep_order_witness() -> int:
    """Check the exact P2 witness for relaxing the nonsource color first."""
    alpha = 1.0 / 9.0
    error = np.array([4.0 / 9.0, 5.0 / 9.0])
    after_one = semantic_sor_sweep(error, alpha)
    observed_ratio = np.max(np.abs(after_one)) / np.max(error)
    zeta = 0.25
    sharp_factor = zeta * (1.0 + 2.0 * (1.0 - zeta))
    assert np.max(np.abs(after_one - np.array([4.0 / 9.0, 11.0 / 36.0]))) <= 2e-15
    assert abs(observed_ratio - 4.0 / 5.0) <= 2e-15
    assert abs(sharp_factor - 5.0 / 8.0) <= 2e-15
    assert observed_ratio > sharp_factor
    return 1


def pagerank_matrix(adjacency: Array, alpha: float) -> tuple[Array, Array]:
    """Return Q and the degree vector for one graph."""
    degrees = adjacency.sum(axis=1)
    inv_sqrt = np.diag(1.0 / np.sqrt(degrees))
    normalized = inv_sqrt @ adjacency @ inv_sqrt
    matrix = 0.5 * ((1.0 + alpha) * np.eye(len(degrees)) - (1.0 - alpha) * normalized)
    return matrix, degrees


def exact_rppr_by_support(
    matrix: Array, degrees: Array, seed: int, alpha: float, rho: float
) -> Array:
    """Enumerate the positive face of a small RPPR instance."""
    size = len(degrees)
    load = np.zeros(size)
    load[seed] = alpha / sqrt(degrees[seed])
    threshold = alpha * rho * np.sqrt(degrees)
    for support_size in range(1, size + 1):
        for support_tuple in combinations(range(size), support_size):
            support = np.array(support_tuple, dtype=int)
            candidate = np.zeros(size)
            candidate[support] = np.linalg.solve(
                matrix[np.ix_(support, support)],
                load[support] - threshold[support],
            )
            if np.min(candidate[support]) <= 1e-12:
                continue
            residual = load - matrix @ candidate
            if np.max(np.abs(residual[support] - threshold[support])) > 2e-10:
                continue
            inactive = np.setdiff1d(np.arange(size), support)
            if inactive.size and (
                np.min(residual[inactive]) < -2e-10
                or np.max(residual[inactive] - threshold[inactive]) > 2e-10
            ):
                continue
            return candidate
    raise AssertionError("support enumeration did not find the RPPR minimizer")


def graph_suite() -> list[Array]:
    """Return paths, cycles, and stars with no isolated vertices."""
    graphs: list[Array] = []
    for size in range(2, 7):
        path = np.zeros((size, size))
        for vertex in range(size - 1):
            path[vertex, vertex + 1] = path[vertex + 1, vertex] = 1.0
        graphs.append(path)
        star = np.zeros((size, size))
        star[0, 1:] = 1.0
        star[1:, 0] = 1.0
        graphs.append(star)
        if size >= 3:
            cycle = path.copy()
            cycle[0, -1] = cycle[-1, 0] = 1.0
            graphs.append(cycle)
    return graphs


def check_bias_bridge() -> int:
    """Check the componentwise residual and semantic bias boxes."""
    cells = 0
    for adjacency in graph_suite():
        for alpha in (0.01, 0.1, 0.5):
            matrix, degrees = pagerank_matrix(adjacency, alpha)
            for seed in range(len(degrees)):
                load = np.zeros(len(degrees))
                load[seed] = alpha / sqrt(degrees[seed])
                ppr = np.linalg.solve(matrix, load)
                for rho in (1e-4, 0.01, 0.05):
                    rppr = exact_rppr_by_support(matrix, degrees, seed, alpha, rho)
                    residual = load - matrix @ rppr
                    threshold = alpha * rho * np.sqrt(degrees)
                    assert np.min(residual) >= -3e-10
                    assert np.max(residual - threshold) <= 3e-10
                    bias = ppr - rppr
                    assert np.min(bias) >= -3e-10
                    assert np.max(bias - rho * np.sqrt(degrees)) <= 3e-10
                    assert np.max(np.abs(bias) / np.sqrt(degrees)) <= rho + 3e-10
                    cells += 1
    return cells


def check_face_shock_pythagoras() -> int:
    """Check exact optimum-shift orthogonality at nonsettled old iterates."""
    cells = 0
    for adjacency in graph_suite():
        size = len(adjacency)
        for alpha in (0.01, 0.1, 0.5):
            matrix, degrees = pagerank_matrix(adjacency, alpha)
            load = np.zeros(size)
            load[0] = alpha / sqrt(degrees[0])
            for old_size in range(1, size):
                old = np.arange(old_size)
                enlarged = np.arange(old_size + 1)
                old_matrix = matrix[np.ix_(old, old)]
                enlarged_matrix = matrix[np.ix_(enlarged, enlarged)]
                old_solution = np.linalg.solve(old_matrix, load[old])
                enlarged_solution = np.linalg.solve(enlarged_matrix, load[enlarged])
                padded_old = np.zeros(old_size + 1)
                padded_old[:old_size] = old_solution
                shift = enlarged_solution - padded_old

                phase = np.arange(1, old_size + 1, dtype=float)
                current = 0.4 * old_solution + 0.01 * np.sin(phase)
                padded_current = np.zeros(old_size + 1)
                padded_current[:old_size] = current
                old_error = old_solution - current
                enlarged_error = enlarged_solution - padded_current

                left = enlarged_error @ enlarged_matrix @ enlarged_error
                old_energy = old_error @ old_matrix @ old_error
                shock_energy = shift @ enlarged_matrix @ shift
                assert abs(left - old_energy - shock_energy) <= 2e-11

                new_vertex = old_size
                demand = load[new_vertex] - matrix[new_vertex, old] @ old_solution
                assert abs(shock_energy - demand * enlarged_solution[new_vertex]) <= 2e-11
                cells += 1
    return cells


def main() -> None:
    """Run every deterministic audit family."""
    mode_cells = check_sor_modes()
    spider_cells = check_spider_spectrum()
    radial_cells = check_radial_semantic_damping()
    order_cells = check_sweep_order_witness()
    bias_cells = check_bias_bridge()
    shock_cells = check_face_shock_pythagoras()
    print(
        "signed-spider checks passed: "
        f"{mode_cells} SOR modes, {spider_cells} spider cells, "
        f"{radial_cells} radial semantic cells, "
        f"{order_cells} sweep-order witness, "
        f"{bias_cells} RPPR bias cells, {shock_cells} face-shock cells"
    )


if __name__ == "__main__":
    main()
