#!/usr/bin/env python3
"""Numerical regression for the scalar shifted-debt and source-bank lemmas.

Run with NumPy available, for example

    uv run --with numpy python shifted_debt_envelope_verify.py

This is a normalization/identity audit.  The proofs in README.md are the
authority for the stated inequalities.
"""

import random

import numpy as np


def random_connected_graph(rng, n):
    edges = {(i, i + 1) for i in range(n - 1)}
    for i in range(n):
        for j in range(i + 2, n):
            if rng.random() < 0.24:
                edges.add((i, j))
    adjacency = np.zeros((n, n))
    for i, j in edges:
        adjacency[i, j] = adjacency[j, i] = 1
    return adjacency


def normalized_matrix(adjacency, alpha):
    degree = adjacency.sum(axis=1)
    invsqrt = 1 / np.sqrt(degree)
    normalized_adjacency = invsqrt[:, None] * adjacency * invsqrt[None, :]
    a = (1 + alpha) / 2
    c = (1 - alpha) / 2
    return a * np.eye(len(adjacency)) - c * normalized_adjacency, degree


def audit_scalar_envelope(rng, qmat, alpha, sigma):
    n = len(qmat)
    face_size = rng.randrange(1, n)
    face = sorted(rng.sample(range(n), face_size))
    exterior = [i for i in range(n) if i not in face]
    amat = qmat[np.ix_(face, face)] + sigma * np.eye(face_size)
    debt = np.array([10 ** rng.uniform(-8, 0) for _ in face])
    correction = np.linalg.solve(amat, debt)
    factor = np.sqrt(((1 + alpha) / 2 + sigma) / (alpha + sigma))

    assert np.min(correction) >= -2e-12
    for vertex in exterior:
        crow = -qmat[vertex, face]
        response = crow @ correction
        schur_leverage = crow @ np.linalg.solve(amat, crow)
        assert np.min(crow) >= 0
        assert schur_leverage < (1 + alpha) / 2 + sigma + 2e-12
        assert response >= -2e-12
        assert response <= factor * np.linalg.norm(debt) + 2e-11


def audit_zero_append(rng, qmat, sigma):
    n = len(qmat)
    split = rng.randrange(1, n)
    permutation = rng.sample(range(n), n)
    face = permutation[:split]
    batch = permutation[split:]
    old = np.array([rng.random() for _ in face])
    old_debt = np.array([rng.random() for _ in face])
    amat = qmat + sigma * np.eye(n)
    rhs = np.zeros(n)
    rhs[face] = amat[np.ix_(face, face)] @ old + old_debt
    visible = np.array([rng.random() for _ in batch])
    rhs[batch] = amat[np.ix_(batch, face)] @ old + visible
    padded = np.zeros(n)
    padded[face] = old
    expanded_debt = rhs - amat @ padded

    assert np.max(np.abs(expanded_debt[face] - old_debt)) < 2e-12
    assert np.max(np.abs(expanded_debt[batch] - visible)) < 2e-12
    expected = np.linalg.norm(old_debt) ** 2 + np.linalg.norm(visible) ** 2
    assert abs(np.linalg.norm(expanded_debt) ** 2 - expected) < 2e-11


def exact_obstacle_solution(amat, rhs):
    face = [i for i, value in enumerate(rhs) if value > 0]
    solution = np.zeros(len(rhs))
    while face:
        solution[:] = 0
        solution[face] = np.linalg.solve(amat[np.ix_(face, face)], rhs[face])
        assert np.min(solution[face]) > -2e-11
        exterior = [i for i in range(len(rhs)) if i not in face]
        scores = rhs[exterior] - amat[np.ix_(exterior, face)] @ solution[face]
        new_batch = [vertex for vertex, score in zip(exterior, scores) if score > 1e-12]
        if not new_batch:
            break
        face.extend(new_batch)
    return solution


def audit_global_subgradient_stop(rng, qmat, alpha, sigma):
    n = len(qmat)
    face = sorted(rng.sample(range(n), rng.randrange(1, n)))
    exterior = [i for i in range(n) if i not in face]
    amat = qmat + sigma * np.eye(n)
    active_matrix = amat[np.ix_(face, face)]
    base_load = np.array([0.2 + rng.random() for _ in face])
    current = np.zeros(n)
    current[face] = np.linalg.solve(active_matrix, base_load)
    debt = np.array([10 ** rng.uniform(-7, -1) for _ in face])
    negative_margin = np.array([10 ** rng.uniform(-7, -1) for _ in exterior])
    rhs = amat @ current
    rhs[face] += debt
    rhs[exterior] -= negative_margin

    assert np.min(current) >= -2e-12
    assert np.max(rhs[exterior] - amat[np.ix_(exterior, face)] @ current[face]) < 0
    optimum = exact_obstacle_solution(amat, rhs)

    def objective(vector):
        return 0.5 * vector @ amat @ vector - rhs @ vector

    gap = objective(current) - objective(optimum)
    gap_bound = np.linalg.norm(debt) ** 2 / (2 * (alpha + sigma))
    distance_bound = np.linalg.norm(debt) / (alpha + sigma)
    assert gap >= -2e-10
    assert gap <= gap_bound + 3e-10
    assert np.linalg.norm(current - optimum) <= distance_bound + 3e-10


def audit_exact_packet_bank(qmat, degree, alpha, sigma, source):
    n = len(qmat)
    rho = 0.02 / degree.sum()
    rhs = -alpha * rho * np.sqrt(degree)
    rhs[source] += alpha / np.sqrt(degree[source])
    amat = qmat + sigma * np.eye(n)
    face = [source]
    packets = []
    sources = []
    previous = np.zeros(n)

    while True:
        solution = np.zeros(n)
        solution[face] = np.linalg.solve(amat[np.ix_(face, face)], rhs[face])
        packet = solution - previous
        packets.append(packet)

        exterior = [i for i in range(n) if i not in face]
        scores = rhs[exterior] - qmat[np.ix_(exterior, face)] @ solution[face]
        new_batch = [vertex for vertex, score in zip(exterior, scores) if score > 1e-12]
        if not new_batch:
            break
        sources.append(np.array([score for score in scores if score > 1e-12]))
        previous = solution
        face.extend(new_batch)
        assert len(packets) <= n

    for i, left in enumerate(packets):
        assert left @ amat @ left >= -2e-12
        for right in packets[i + 1 :]:
            assert abs(left @ amat @ right) < 3e-10

    packet_energy = sum(packet @ amat @ packet for packet in packets[1:])
    source_square = sum(source_vector @ source_vector for source_vector in sources)
    final_energy = solution @ amat @ solution
    assert source_square <= (1 + sigma) * packet_energy + 3e-10
    assert packet_energy <= final_energy + 3e-10
    assert final_energy <= alpha + 3e-10


def main():
    rng = random.Random(20260831)
    for n in range(3, 18):
        for _ in range(80):
            adjacency = random_connected_graph(rng, n)
            alpha = 10 ** rng.uniform(-4, -0.3)
            sigma = 10 ** rng.uniform(np.log10(alpha), 0)
            qmat, degree = normalized_matrix(adjacency, alpha)
            assert np.linalg.eigvalsh(qmat)[0] >= alpha - 2e-12
            assert np.linalg.eigvalsh(qmat)[-1] <= 1 + 2e-12
            audit_scalar_envelope(rng, qmat, alpha, sigma)
            audit_zero_append(rng, qmat, sigma)
            audit_global_subgradient_stop(rng, qmat, alpha, sigma)
            audit_exact_packet_bank(qmat, degree, alpha, sigma, rng.randrange(n))

    print("shifted-debt envelope, global cap, zero append, and packet bank verified")


if __name__ == "__main__":
    main()
