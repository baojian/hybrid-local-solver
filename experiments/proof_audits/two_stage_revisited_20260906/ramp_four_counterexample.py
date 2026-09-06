"""Rigorous interval certificate refuting a universal 4r ramp tracking bound.

The graph is the ordinary unit-weight lollipop K_128 with a 384-vertex tail,
seeded at a non-connector clique vertex. Equitable classes compress only
this offline verification; the proposed local algorithm uses no quotient
oracle. The trajectory certificate uses integer dyadic floors plus a proved
pairwise contraction bound. The PPR reference is certified by an exact
residual bound, regardless of the floating-point solve used to propose it.
"""

from __future__ import annotations

from fractions import Fraction as F
import json
from math import isqrt

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def quotient(clique=128, tail=384):
    # Classes: seed, other ordinary clique vertices, connector, tail chain.
    size = tail + 3
    degree = [clique - 1, clique - 1, clique] + [2] * (tail - 1) + [1]
    cardinality = [1, clique - 2, 1] + [1] * tail
    neighbors = [
        [(1, clique - 2), (2, 1)],
        [(0, 1), (1, clique - 3), (2, 1)],
        [(0, 1), (1, clique - 2), (3, 1)],
    ]
    neighbors += [[(i - 1, 1), (i + 1, 1)] for i in range(3, size - 1)]
    neighbors += [[(size - 2, 1)]]
    assert all(sum(count for _, count in row) == d for row, d in zip(neighbors, degree))
    for i, row in enumerate(neighbors):
        for j, count in row:
            reverse = next((n for k, n in neighbors[j] if k == i), 0)
            assert cardinality[i] * count == cardinality[j] * reverse
    return degree, cardinality, neighbors


def main():
    degree, cardinality, neighbors = quotient()
    n = len(degree)
    t_parameter = 256
    alpha = F(1, t_parameter**2)
    horizon = 5468
    grid_denominator = 2**80
    x, z = [0] * n, [0] * n
    r = grid_denominator // degree[0]
    for _ in range(horizon):
        next_z = []
        for i, (d, row) in enumerate(zip(degree, neighbors)):
            neighbor_x = sum(count * x[j] for j, count in row)
            neighbor_z = sum(count * z[j] for j, count in row)
            numerator = (t_parameter - 1) * (d * z[i] + neighbor_z)
            numerator -= t_parameter * (t_parameter - 1) * (d * x[i] - neighbor_x)
            numerator += 2 * grid_denominator * (i == 0) - 2 * d * r
            next_z.append(max(0, numerator // (2 * t_parameter * d)))
        x = [((t_parameter - 1) * a + b) // t_parameter for a, b in zip(x, next_z)]
        z = next_z
        r = ((2 * t_parameter - 1) * r) // (2 * t_parameter)

    matrix = sparse.lil_matrix((n, n))
    for i, (d, row) in enumerate(zip(degree, neighbors)):
        matrix[i, i] = float((1 + alpha) / 2)
        for j, count in row:
            matrix[i, j] -= float((1 - alpha) * count / (2 * d))
    source = np.zeros(n)
    source[0] = float(alpha / degree[0])
    approximate_ppr = spsolve(matrix.tocsr(), source)
    proposed_ppr = [int(F(float(value)) * grid_denominator) for value in approximate_ppr]
    # M-matrix maximum principle: ||t-u||_infty <= ||M u-b||_infty/alpha
    # in degree densities. Every quantity below is exact rational arithmetic.
    reference_error = F(0)
    for i, (d, row) in enumerate(zip(degree, neighbors)):
        neighbor_u = sum(count * proposed_ppr[j] for j, count in row)
        numerator = (t_parameter**2 + 1) * d * proposed_ppr[i]
        numerator -= (t_parameter**2 - 1) * neighbor_u
        numerator -= 2 * grid_denominator * (i == 0)
        reference_error = max(reference_error, F(abs(numerator), 2 * d * grid_denominator))

    volume = sum(d * count for d, count in zip(degree, cardinality))
    square_root_upper = isqrt(volume) + 1
    trajectory_error = F(24 * square_root_upper * t_parameter**2, grid_denominator)
    exact_r = F(1, degree[0]) * F(2 * t_parameter - 1, 2 * t_parameter) ** horizon
    assert exact_r > F(1, 1024 * volume)
    witness = max(range(n), key=lambda i: proposed_ppr[i] - x[i])
    proposed_error = F(proposed_ppr[witness] - x[witness], grid_denominator)
    assert all(F(abs(a - b), grid_denominator) <= proposed_error for a, b in zip(proposed_ppr, x))
    lower = (proposed_error - reference_error - trajectory_error) / exact_r
    upper = (proposed_error + reference_error + trajectory_error) / exact_r
    assert F(401807, 100000) < lower < upper < F(401809, 100000)
    assert lower > 4
    print(
        json.dumps(
            {
                "status": "passed",
                "arithmetic": "integer dyadic trajectory with exact rational error certificates",
                "graph": "unit-weight lollipop: K_128 and 384 tail vertices; non-connector clique seed",
                "full_vertex_count": 512,
                "quotient_class_count": n,
                "original_volume": volume,
                "alpha": str(alpha),
                "theta": "1/256",
                "eta": "511/512",
                "step": horizon,
                "r": "(1/127)*(511/512)^5468",
                "witness_quotient_class": witness,
                "certified_semantic_error_over_r_interval": ["4.01807", "4.01809"],
                "reference_density_error_bound": float(reference_error),
                "trajectory_density_error_bound": float(trajectory_error),
                "scope": "Refutes a universal constant-four ramp-only bound; does not refute larger constants or the two-phase theorem",
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
