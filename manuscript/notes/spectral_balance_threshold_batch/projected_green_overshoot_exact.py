#!/usr/bin/env python3
"""Exact projected-NAG overshoot on a finite simple unit tree.

The default audit uses exact fractions.  ``--sparse`` additionally needs
NumPy/SciPy and materializes the 6,142-coordinate principal face.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F


ALPHA = F(1, 10**6)
QPAR = F(999, 1000)
BETA = F(999, 1001)
RHO = F(1, 10**30)
THETA = F(1, 8 * 1000 * 10**30)
TARGET_SOURCE = F(
    6540133644733406413842599552575751344874676117372379874525139330415433020976577583960981125351077647367331526131657,
    131072000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
)


def radial_normalized_adjacency(values, degree=3):
    output = [F(0) for _ in values]
    output[0] = values[1]
    for radius in range(1, len(values) - 1):
        output[radius] = (values[radius - 1] + (degree - 1) * values[radius + 1]) / degree
    return output


def projected_radial(floor=F(0), iterations=39, size=64):
    """Run the clipped radial recurrence with load e_root-floor*one."""
    previous = [F(0) for _ in range(size)]
    current = [F(0) for _ in range(size)]
    for _ in range(iterations):
        s_current = radial_normalized_adjacency(current)
        s_previous = radial_normalized_adjacency(previous)
        raw = [
            QPAR * (current[i] + s_current[i])
            - QPAR * QPAR / 2 * (previous[i] + s_previous[i])
            - floor
            for i in range(size)
        ]
        raw[0] += 1
        following = [max(F(0), value) for value in raw]
        previous, current = current, following
    return current


def exact_face_green():
    """Endpoint Green entry after eliminating the depth-eight side trees."""
    a = (1 + ALPHA) / 2
    c = (1 - ALPHA) / 2
    edge = c / 3
    branch_pivot = a
    for _ in range(7):
        branch_pivot = a - 2 * edge * edge / branch_pivot
    self_energy = edge * edge / branch_pivot

    diagonal = [a - 2 * self_energy] + [a - self_energy] * 20 + [a - 2 * self_energy]
    determinant_previous = F(1)
    determinant = diagonal[0]
    for i in range(1, 22):
        determinant_previous, determinant = (
            determinant,
            diagonal[i] * determinant - edge * edge * determinant_previous,
        )
    return edge**21 / determinant


def build_graph(path_length=21, shell_depth=9):
    path = list(range(path_length + 1))
    next_vertex = len(path)
    edges = []
    core = set(path)
    for i in range(path_length):
        edges.append((path[i], path[i + 1]))
    branch_counts = [2] + [1] * (path_length - 1) + [2]
    for path_vertex, count in zip(path, branch_counts):
        for _ in range(count):
            level = [next_vertex]
            next_vertex += 1
            edges.append((path_vertex, level[0]))
            core.add(level[0])
            for depth in range(1, shell_depth):
                new_level = []
                for parent in level:
                    for _ in range(2):
                        child = next_vertex
                        next_vertex += 1
                        edges.append((parent, child))
                        new_level.append(child)
                        if depth + 1 < shell_depth:
                            core.add(child)
                level = new_level
    return next_vertex, edges, sorted(core), path[0], path[-1]


def sparse_check():
    import numpy as np
    from scipy.sparse import coo_matrix, eye

    n, edges, core, source, target = build_graph()
    rows, columns = [], []
    for u, v in edges:
        rows.extend((u, v))
        columns.extend((v, u))
    adjacency = coo_matrix((np.ones(len(rows)), (rows, columns)), shape=(n, n)).tocsr()
    degree = np.asarray(adjacency.sum(axis=1)).ravel()
    index = {vertex: i for i, vertex in enumerate(core)}
    principal = adjacency[core, :][:, core]
    inv_sqrt = 1 / np.sqrt(degree[core])
    normalized = principal.multiply(inv_sqrt[:, None]).multiply(inv_sqrt[None, :]).tocsr()
    qmat = float((1 + ALPHA) / 2) * eye(len(core), format="csr")
    qmat -= float((1 - ALPHA) / 2) * normalized
    richardson = eye(len(core), format="csr") - qmat
    forcing = np.zeros(len(core))
    forcing[index[source]] = 1
    previous = np.zeros(len(core))
    current = np.zeros(len(core))
    for _ in range(39):
        following = richardson @ ((1 + float(BETA)) * current - float(BETA) * previous)
        following += forcing
        following = np.maximum(following, 0)
        previous, current = current, following
    assert abs(current[index[target]] - float(TARGET_SOURCE)) < 2e-15
    print(f"ambient vertices={n}, face vertices={len(core)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sparse", action="store_true")
    args = parser.parse_args()

    source_iterate = projected_radial()[21]
    assert source_iterate == TARGET_SOURCE
    assert source_iterate > F(49, 10**6)
    face_green = exact_face_green()
    infinite_green_upper = F(1, 524288)
    assert ALPHA < face_green < infinite_green_upper
    assert source_iterate > 20 * face_green

    # Multiplying the canonical face RHS by sqrt(3)/alpha gives
    # e_source-3*rho*one.  Projection is positively homogeneous.
    canonical_iterate = projected_radial(floor=3 * RHO)[21]
    assert canonical_iterate > F(49, 10**6)
    canonical_solution_lower = face_green - 3 * RHO / ALPHA
    assert canonical_solution_lower > ALPHA - 3 * RHO / ALPHA > 0
    assert canonical_iterate > 20 * face_green
    assert (ALPHA * canonical_iterate) ** 2 > 3 * THETA**2
    assert (ALPHA * canonical_solution_lower) ** 2 > 3 * THETA**2

    n, edges, core, _, _ = build_graph()
    assert n == 12286 and len(core) == 6142 and len(edges) == n - 1
    volume = 2 * len(edges)
    assert RHO * volume < 1
    assert ALPHA / (2 * 6**30) > 2 * RHO

    print("projected x_39(radius 21) =", float(source_iterate))
    print("principal-face Green =", float(face_green))
    print("iterate / Green =", float(source_iterate / face_green))
    print("publication theta =", float(THETA))
    print("rho*vol(S*) =", float(RHO * volume))
    if args.sparse:
        sparse_check()


if __name__ == "__main__":
    main()
