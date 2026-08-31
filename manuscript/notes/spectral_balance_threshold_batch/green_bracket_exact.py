#!/usr/bin/env python3
"""Exact finite-tree counterexample to a raw critical-NAG Green bracket.

The exact radial check needs only the Python standard library.  ``--sparse``
also materializes the 20,478-vertex simple unit tree and needs NumPy/SciPy.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F


ALPHA = F(1, 16384)
SROOT = F(1, 128)
QPAR = 1 - SROOT
TARGET_EXACT = F(
    -8553933855081135756983326558552827234956991324361526382607697112612692951,
    2091325902307205928829760216702303879947764171471658161874093352239862120448,
)


def radial_normalized_adjacency(values, degree=3):
    """Apply normalized adjacency on the infinite regular tree, radially."""
    output = [F(0) for _ in values]
    output[0] = values[1]
    for radius in range(1, len(values) - 1):
        output[radius] = (values[radius - 1] + (degree - 1) * values[radius + 1]) / degree
    return output


def exact_unprojected(iterations=29, radius=40):
    """Use x_{-1}=x_0=0 and return the indicated raw NAG iterate."""
    previous = [F(0) for _ in range(radius)]
    current = [F(0) for _ in range(radius)]
    for _ in range(iterations):
        s_current = radial_normalized_adjacency(current)
        s_previous = radial_normalized_adjacency(previous)
        following = [
            QPAR * (current[r] + s_current[r]) - QPAR * QPAR / 2 * (previous[r] + s_previous[r])
            for r in range(radius)
        ]
        following[0] += 1
        previous, current = current, following
    return current


def build_finite_tree(path_length=7, off_depth=11):
    """Materialize the finite tree whose radius-29 computation is exact."""
    edges = []
    path = list(range(path_length + 1))
    next_vertex = len(path)
    for i in range(path_length):
        edges.append((path[i], path[i + 1]))

    branch_counts = [2] + [1] * (path_length - 1) + [2]
    for path_vertex, count in zip(path, branch_counts):
        for _ in range(count):
            level = [next_vertex]
            next_vertex += 1
            edges.append((path_vertex, level[0]))
            for _ in range(1, off_depth):
                new_level = []
                for parent in level:
                    for _ in range(2):
                        child = next_vertex
                        next_vertex += 1
                        edges.append((parent, child))
                        new_level.append(child)
                level = new_level
    return next_vertex, edges, path[0], path[-1]


def sparse_check():
    import numpy as np
    from scipy.sparse import coo_matrix, eye

    n, edges, source, target = build_finite_tree()
    rows, columns = [], []
    for u, v in edges:
        rows.extend((u, v))
        columns.extend((v, u))
    adjacency = coo_matrix((np.ones(len(rows)), (rows, columns)), shape=(n, n)).tocsr()
    degree = np.asarray(adjacency.sum(axis=1)).ravel()
    inv_sqrt_degree = 1.0 / np.sqrt(degree)
    normalized = (
        adjacency.multiply(inv_sqrt_degree[:, None]).multiply(inv_sqrt_degree[None, :]).tocsr()
    )

    alpha = float(ALPHA)
    qmat = (1 + alpha) / 2 * eye(n, format="csr")
    qmat -= (1 - alpha) / 2 * normalized
    richardson = eye(n, format="csr") - qmat
    beta = 127 / 129
    forcing = np.zeros(n)
    forcing[source] = 1
    previous = np.zeros(n)
    current = np.zeros(n)
    for _ in range(29):
        following = richardson @ ((1 + beta) * current - beta * previous)
        following += forcing
        previous, current = current, following
    assert abs(current[target] - float(TARGET_EXACT)) < 2e-15
    print(f"explicit vertices={n}, x_29[target]={current[target]:.17g}")


def canonical_threshold_check(green_lower):
    """Check that the witness is not hidden below the RPPR threshold."""
    rho = F(1, 10**30)
    epsilon_objective = rho
    theta = SROOT * rho / 8
    volume = 40954

    # The source and target both have degree three.  Multiplication by
    # sqrt(3) turns both comparisons into exact rational square tests.
    scaled_true_numerator = ALPHA * green_lower - 3 * rho
    assert scaled_true_numerator > 0
    assert scaled_true_numerator**2 > 3 * theta**2

    # The floor component of the raw iterate is nonpositive, so this is a
    # lower bound on the magnitude of the already-negative coordinate.
    floor_error_factor = (1 - SROOT) ** 29 * (1 + 29 * SROOT)
    assert 0 <= floor_error_factor <= 1
    scaled_bad_numerator = ALPHA * (-TARGET_EXACT)
    assert scaled_bad_numerator**2 > 3 * theta**2

    # Every vertex is within distance 18; this proves the unconstrained
    # global PPR vector stays above rho*sqrt(d), hence S*=V.
    uniform_scaled_lower = ALPHA / 6**18 - 3 * rho
    assert uniform_scaled_lower > 0
    assert rho * volume <= 1
    assert epsilon_objective < ALPHA / 2

    print("publication theta =", float(theta))
    print(
        "certified true-coordinate/theta >",
        float(scaled_true_numerator / theta) / 3**0.5,
    )
    print(
        "certified bad-iterate/theta >",
        float(scaled_bad_numerator / theta) / 3**0.5,
    )
    print("rho*vol(S*) =", float(rho * volume))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sparse", action="store_true")
    args = parser.parse_args()

    assert ALPHA == SROOT * SROOT
    assert F(127, 129) == (1 - SROOT) / (1 + SROOT)
    iterate = exact_unprojected()
    assert iterate[7] == TARGET_EXACT
    assert iterate[7] < 0

    a = (1 + ALPHA) / 2
    c = (1 - ALPHA) / 2
    green_lower = (1 / a) * (c / a) ** 7 / 3**7
    assert green_lower > 14 * ALPHA
    assert -iterate[7] > 67 * ALPHA
    n, edges, _, _ = build_finite_tree()
    assert n == 20478 and len(edges) == n - 1

    print("exact x_29(distance 7) =", iterate[7])
    print("decimal =", float(iterate[7]))
    print("Green lower bound / alpha =", float(green_lower / ALPHA))
    canonical_threshold_check(green_lower)
    if args.sparse:
        sparse_check()


if __name__ == "__main__":
    main()
