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


def main() -> None:
    """Run every deterministic audit family."""
    mode_cells = check_sor_modes()
    spider_cells = check_spider_spectrum()
    bias_cells = check_bias_bridge()
    print(
        "signed-spider checks passed: "
        f"{mode_cells} SOR modes, {spider_cells} spider cells, "
        f"{bias_cells} RPPR bias cells"
    )


if __name__ == "__main__":
    main()
