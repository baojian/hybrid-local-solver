#!/usr/bin/env python3
"""Falsification audit for the threshold-batch Cholesky depth theorem.

This script is not a proof.  It checks the block-factor identities, inverse
ordering, causal forcing, and final energy bound on paths, stars, random
trees, and sparse random connected graphs.  All theorem claims are proved in
``main.tex``; floating point is used here only to catch algebra/index errors.
"""

from __future__ import annotations

import math
import random

import numpy as np


def path_graph(vertices: int) -> np.ndarray:
    adjacency = np.zeros((vertices, vertices))
    for vertex in range(vertices - 1):
        adjacency[vertex, vertex + 1] = 1.0
        adjacency[vertex + 1, vertex] = 1.0
    return adjacency


def star_graph(vertices: int) -> np.ndarray:
    adjacency = np.zeros((vertices, vertices))
    for vertex in range(1, vertices):
        adjacency[0, vertex] = 1.0
        adjacency[vertex, 0] = 1.0
    return adjacency


def random_graph(vertices: int, rng: random.Random, extra_probability: float) -> np.ndarray:
    adjacency = np.zeros((vertices, vertices))
    for vertex in range(1, vertices):
        parent = rng.randrange(vertex)
        adjacency[vertex, parent] = 1.0
        adjacency[parent, vertex] = 1.0
    for left in range(vertices):
        for right in range(left + 1, vertices):
            if adjacency[left, right] == 0.0 and rng.random() < extra_probability:
                adjacency[left, right] = 1.0
                adjacency[right, left] = 1.0
    return adjacency


def pagerank_lcp(
    adjacency: np.ndarray, alpha: float, rho: float, seed: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    degrees = adjacency.sum(axis=1)
    inverse_sqrt = 1.0 / np.sqrt(degrees)
    normalized = inverse_sqrt[:, None] * adjacency * inverse_sqrt[None, :]
    matrix = ((1.0 + alpha) / 2.0) * np.eye(len(adjacency))
    matrix -= ((1.0 - alpha) / 2.0) * normalized
    linear = -alpha * rho * np.sqrt(degrees)
    linear[seed] += alpha / math.sqrt(degrees[seed])
    return matrix, linear, degrees


def face_solution(matrix: np.ndarray, linear: np.ndarray, active: list[int]) -> np.ndarray:
    point = np.zeros(len(linear))
    indices = np.array(active, dtype=int)
    point[indices] = np.linalg.solve(matrix[np.ix_(indices, indices)], linear[indices])
    return point


def threshold_partition(
    matrix: np.ndarray,
    linear: np.ndarray,
    seed: int,
    threshold: float,
) -> tuple[list[list[int]], list[np.ndarray], int]:
    blocks = [[seed]]
    active = [seed]
    faces = [face_solution(matrix, linear, active)]
    threshold_blocks = 1

    while True:
        residual = linear - matrix @ faces[-1]
        new = [
            index
            for index in range(len(linear))
            if index not in active and residual[index] > threshold
        ]
        if not new:
            break
        blocks.append(new)
        active.extend(new)
        faces.append(face_solution(matrix, linear, active))
        threshold_blocks += 1

    while True:
        residual = linear - matrix @ faces[-1]
        new = [
            index
            for index in range(len(linear))
            if index not in active and residual[index] > 2.0e-11
        ]
        if not new:
            break
        blocks.append(new)
        active.extend(new)
        faces.append(face_solution(matrix, linear, active))

    return blocks, faces, threshold_blocks


def block_ranges(blocks: list[list[int]]) -> list[slice]:
    ranges = []
    start = 0
    for block in blocks:
        ranges.append(slice(start, start + len(block)))
        start += len(block)
    return ranges


def audit_instance(
    adjacency: np.ndarray,
    alpha: float,
    rho: float,
    seed: int,
    threshold: float,
) -> tuple[float, int]:
    matrix, linear, _ = pagerank_lcp(adjacency, alpha, rho, seed)
    blocks, faces, threshold_blocks = threshold_partition(matrix, linear, seed, threshold)
    support = [index for block in blocks for index in block]
    permutation = np.array(support, dtype=int)
    principal = matrix[np.ix_(permutation, permutation)]
    rhs = linear[permutation]
    cholesky = np.linalg.cholesky(principal)
    assert cholesky[np.triu_indices(len(cholesky), 1)].max(initial=0.0) <= 1.0e-12
    off_diagonal = cholesky.copy()
    np.fill_diagonal(off_diagonal, 0.0)
    assert off_diagonal.max(initial=0.0) <= 1.0e-10

    ranges = block_ranges(blocks)
    bidiagonal = np.zeros_like(cholesky)
    for block, current in enumerate(ranges):
        bidiagonal[current, current] = cholesky[current, current]
        if block:
            previous = ranges[block - 1]
            bidiagonal[current, previous] = cholesky[current, previous]

    inverse_full = np.linalg.inv(cholesky)
    inverse_bidiagonal = np.linalg.inv(bidiagonal)
    assert inverse_bidiagonal.min() >= -2.0e-9
    assert (inverse_bidiagonal - inverse_full).max() <= 2.0e-8
    assert np.linalg.svd(bidiagonal, compute_uv=False)[-1] >= math.sqrt(alpha) - 2.0e-8
    assert np.linalg.norm(bidiagonal, 2) <= math.sqrt(2.0) + 2.0e-8

    transformed = np.linalg.solve(cholesky, rhs)
    assert transformed.min() >= -2.0e-8
    forcing = bidiagonal @ transformed
    assert np.max(forcing[ranges[0]] - rhs[ranges[0]]) <= 2.0e-8
    for current in ranges[1:]:
        assert forcing[current].max(initial=-math.inf) <= threshold + 2.0e-8

    q_alpha = (math.sqrt(2.0 / alpha) - 1.0) / (math.sqrt(2.0 / alpha) + 1.0)
    optimum = faces[-1]
    maximum_ratio = 0.0
    for block_index, face in enumerate(faces[:threshold_blocks]):
        error = optimum - face
        gap = 0.5 * float(error @ matrix @ error)
        tail = 0.5 * sum(
            float(transformed[current] @ transformed[current])
            for current in ranges[block_index + 1 :]
        )
        assert abs(gap - tail) <= 2.0e-7 * max(1.0, gap, tail)
        bound = 8.0 * q_alpha ** (2 * block_index) + threshold**2 / (alpha * rho)
        assert gap <= bound + 2.0e-8
        maximum_ratio = max(maximum_ratio, gap / bound if bound else 0.0)

    seed_source = np.zeros(len(support))
    seed_source[ranges[0]] = rhs[ranges[0]]
    seed_response = inverse_bidiagonal @ seed_source
    for block_index in range(len(blocks)):
        tail_norm = np.linalg.norm(seed_response[ranges[block_index].stop :])
        decay_bound = 2.0 * math.sqrt(2.0) * q_alpha**block_index
        assert tail_norm <= decay_bound + 2.0e-8

    return maximum_ratio, len(blocks)


def main() -> None:
    rng = random.Random(20260830)
    cases = 0
    largest_ratio = 0.0
    largest_blocks = 0

    for vertices in (4, 6, 9, 13, 18, 24):
        graphs = [
            path_graph(vertices),
            star_graph(vertices),
            random_graph(vertices, rng, 0.0),
            random_graph(vertices, rng, min(0.25, 3.0 / vertices)),
        ]
        for adjacency in graphs:
            for alpha in (0.02, 0.08, 0.25, 0.6):
                seed = rng.randrange(vertices)
                maximum_rho = 1.0 / adjacency[seed].sum()
                for rho_fraction in (0.01, 0.08, 0.3, 0.7):
                    rho = rho_fraction * maximum_rho
                    for threshold_fraction in (0.0, 1.0e-4, 2.0e-3):
                        threshold = threshold_fraction * alpha
                        ratio, blocks = audit_instance(adjacency, alpha, rho, seed, threshold)
                        largest_ratio = max(largest_ratio, ratio)
                        largest_blocks = max(largest_blocks, blocks)
                        cases += 1

    print(f"structured/random cases checked: {cases}")
    print(f"largest admission-block count: {largest_blocks}")
    print(f"largest observed exact-gap/theorem-bound ratio: {largest_ratio:.12g}")
    print("verdict: all block-factor, forcing, decay, and energy checks passed")


if __name__ == "__main__":
    main()
