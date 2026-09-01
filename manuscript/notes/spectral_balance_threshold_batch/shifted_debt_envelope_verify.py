#!/usr/bin/env python3
"""Numerical regression for the scalar shifted-debt and source-bank lemmas.

Run with NumPy available, for example

    uv run --with numpy python shifted_debt_envelope_verify.py

This is a normalization/identity audit.  The proofs in README.md are the
authority for the stated inequalities.
"""

import random
from fractions import Fraction

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


def audit_global_positive_boundary_subgradient(rng, qmat, alpha, sigma):
    """Check the minimal exterior subgradient without assuming a quiet scan."""
    n = len(qmat)
    face = sorted(rng.sample(range(n), rng.randrange(1, n)))
    exterior = [i for i in range(n) if i not in face]
    amat = qmat + sigma * np.eye(n)
    active_matrix = amat[np.ix_(face, face)]
    base_load = np.array([0.2 + rng.random() for _ in face])
    current = np.zeros(n)
    current[face] = np.linalg.solve(active_matrix, base_load)
    debt = np.array([10 ** rng.uniform(-7, -1) for _ in face])
    exterior_scores = np.array(
        [rng.choice((-1.0, 1.0)) * 10 ** rng.uniform(-7, -1) for _ in exterior]
    )
    rhs = amat @ current
    rhs[face] += debt
    rhs[exterior] += exterior_scores
    optimum = exact_obstacle_solution(amat, rhs)

    def objective(vector):
        return 0.5 * vector @ amat @ vector - rhs @ vector

    positive_scores = np.maximum(exterior_scores, 0)
    subgradient_norm = np.sqrt(np.linalg.norm(debt) ** 2 + np.linalg.norm(positive_scores) ** 2)
    gap = objective(current) - objective(optimum)
    gap_bound = subgradient_norm**2 / (2 * (alpha + sigma))
    distance_bound = subgradient_norm / (alpha + sigma)
    assert gap >= -2e-10
    assert gap <= gap_bound + 3e-10
    assert np.linalg.norm(current - optimum) <= distance_bound + 3e-10


def audit_arbitrary_feasible_minimum_subgradient(rng, qmat, alpha, sigma):
    """Check the minimum orthant subgradient for a non-lower feasible point."""
    n = len(qmat)
    amat = qmat + sigma * np.eye(n)
    positive = sorted(rng.sample(range(n), rng.randrange(1, n)))
    current = np.zeros(n)
    current[positive] = np.array([10 ** rng.uniform(-4, 0) for _ in positive])
    smooth_gradient = np.array(
        [rng.choice((-1.0, 1.0)) * 10 ** rng.uniform(-6, -0.2) for _ in range(n)]
    )
    rhs = amat @ current - smooth_gradient
    optimum = exact_obstacle_solution(amat, rhs)

    minimum_subgradient = smooth_gradient.copy()
    zero = current == 0
    minimum_subgradient[zero] = np.minimum(smooth_gradient[zero], 0)

    def objective(vector):
        return 0.5 * vector @ amat @ vector - rhs @ vector

    gap = objective(current) - objective(optimum)
    norm = np.linalg.norm(minimum_subgradient)
    assert gap >= -2e-10
    assert gap <= norm**2 / (2 * (alpha + sigma)) + 5e-9
    assert np.linalg.norm(current - optimum) <= norm / (alpha + sigma) + 5e-9


def audit_proximal_gradient_mapping_cap(rng, qmat, alpha, sigma):
    """Check the final-only cap obtained from one projected-gradient map."""
    n = len(qmat)
    amat = qmat + sigma * np.eye(n)
    lipschitz = float(np.linalg.eigvalsh(amat)[-1])
    current = np.array([rng.choice((0.0, 10 ** rng.uniform(-5, 0))) for _ in range(n)])
    rhs = np.array([rng.choice((-1.0, 1.0)) * 10 ** rng.uniform(-6, -0.2) for _ in range(n)])
    gradient = amat @ current - rhs
    next_point = np.maximum(current - gradient / lipschitz, 0.0)
    mapping = lipschitz * (current - next_point)
    optimum = exact_obstacle_solution(amat, rhs)

    # Projection optimality supplies this particular subgradient at next_point.
    next_subgradient = mapping + amat @ (next_point - current)

    def objective(vector):
        return 0.5 * vector @ amat @ vector - rhs @ vector

    gap = objective(next_point) - objective(optimum)
    mapping_norm = np.linalg.norm(mapping)
    assert gap >= -2e-10
    assert np.linalg.norm(next_subgradient) <= 2 * mapping_norm + 2e-10
    assert gap <= 2 * mapping_norm**2 / (alpha + sigma) + 5e-9
    assert np.linalg.norm(next_point - optimum) <= (2 * mapping_norm / (alpha + sigma) + 5e-9)


def audit_constant_bracket_nonmonotonicity():
    """Give an exact two-vertex counterexample to monotonicity of c(ell)."""
    alpha = Fraction(1, 4)
    rho = Fraction(1, 20)
    a = Fraction(5, 8)
    b = Fraction(3, 8)
    hmat = ((a, -b), (-b, a))
    load = (alpha * (1 - rho), -alpha * rho)
    optimum = (a - rho, b - rho)
    lower_zero = (Fraction(3, 8), Fraction(1, 8))
    lower_one = (Fraction(17, 40), Fraction(47, 200))

    def multiply(matrix, vector):
        return tuple(sum(row[j] * vector[j] for j in range(2)) for row in matrix)

    def residual(lower):
        product = multiply(hmat, lower)
        return tuple(load[i] - product[i] for i in range(2))

    residual_zero = residual(lower_zero)
    residual_one = residual(lower_one)
    width_zero = max(value / alpha for value in residual_zero)
    width_one = max(value / alpha for value in residual_one)

    assert multiply(hmat, optimum) == load
    assert all(Fraction(0) < lower_zero[i] <= lower_one[i] <= optimum[i] for i in range(2))
    assert residual_zero == (Fraction(1, 20), Fraction(1, 20))
    assert residual_one == (Fraction(3, 50), Fraction(0))
    assert width_zero == Fraction(1, 5)
    assert width_one == Fraction(6, 25) > width_zero


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

    lipschitz = float(np.linalg.eigvalsh(amat)[-1])
    for packet, source_vector in zip(packets[1:], sources):
        energy = packet @ amat @ packet
        source_square = source_vector @ source_vector
        assert energy >= source_square / lipschitz - 3e-10
        assert energy <= source_square / (alpha + sigma) + 3e-10

    packet_energy = sum(packet @ amat @ packet for packet in packets[1:])
    source_square = sum(source_vector @ source_vector for source_vector in sources)
    final_energy = solution @ amat @ solution
    assert source_square <= (1 + sigma) * packet_energy + 3e-10
    assert packet_energy <= final_energy + 3e-10
    assert final_energy <= alpha + 3e-10


def audit_green_amplitude_spine(adjacency, qmat, degree, alpha, source):
    """Check the point-source Green ascent, mass, and amplitude range."""
    n = len(qmat)
    rho = 0.01 / degree.sum()
    rhs = -alpha * rho * np.sqrt(degree)
    rhs[source] += alpha / np.sqrt(degree[source])
    optimum = exact_obstacle_solution(qmat, rhs)
    support = np.flatnonzero(optimum > 1e-10)
    assert source in support

    support_set = set(map(int, support))
    seen = {int(source)}
    stack = [int(source)]
    while stack:
        vertex = stack.pop()
        for neighbor in np.flatnonzero(adjacency[vertex]):
            neighbor = int(neighbor)
            if neighbor in support_set and neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    assert seen == support_set

    hmat = np.diag(np.sqrt(degree)) @ qmat @ np.diag(np.sqrt(degree))
    p = np.linalg.solve(
        hmat[np.ix_(support, support)],
        alpha * (support == source).astype(float),
    )
    position = {int(vertex): index for index, vertex in enumerate(support)}
    for vertex in support:
        vertex = int(vertex)
        if vertex == source:
            continue
        value = p[position[vertex]]
        assert any(
            int(neighbor) in support_set and p[position[int(neighbor)]] > value + 1e-12
            for neighbor in np.flatnonzero(adjacency[vertex])
        )

    internal_degree = adjacency[np.ix_(support, support)].sum(axis=1)
    exterior_degree = degree[support] - internal_degree
    mass_identity = alpha * (degree[support] @ p) + ((1 - alpha) / 2) * (exterior_degree @ p)
    assert abs(mass_identity - alpha) < 2e-9
    assert degree[support] @ p <= 1 + 2e-9
    assert np.min(p) > alpha * rho / ((1 + alpha) / 2) - 2e-10
    assert np.max(p) <= 1 + 2e-10

    # The RPPR solution itself has strict ascent, connected positive
    # superlevels, and a constant-shave lower path for the rho homotopy.
    degree_solution = optimum / np.sqrt(degree)
    for vertex in support:
        vertex = int(vertex)
        if vertex == source:
            continue
        assert any(
            degree_solution[int(neighbor)] > degree_solution[vertex] + 1e-11
            for neighbor in np.flatnonzero(adjacency[vertex])
        )
    assert degree_solution[source] >= np.max(degree_solution) - 2e-9
    assert degree @ degree_solution <= 1 + 2e-9
    final_degree_load = -alpha * rho * degree
    final_degree_load[source] += alpha

    def degree_objective(vector, load=final_degree_load):
        return 0.5 * vector @ hmat @ vector - load @ vector

    # Retained two-sided constant bracket under an exact or certified-lower
    # shifted obstacle prox.  This quantity contracts even though recomputing
    # c(ell) after an arbitrary monotone lower update need not be monotone.
    for eta_fraction in (0.15, 0.35, 0.7):
        bracket_width = eta_fraction * degree_solution[source]
        lower = np.maximum(degree_solution - bracket_width, 0.0)
        assert np.min(degree_solution - lower) >= -2e-9
        assert np.max(degree_solution - lower) <= bracket_width + 2e-9
        for tau_square in (alpha, np.sqrt(alpha), 0.4):
            shifted_matrix = hmat + tau_square * np.diag(degree)
            shifted_load = final_degree_load + tau_square * degree * lower
            prox = exact_obstacle_solution(shifted_matrix, shifted_load)
            contraction = tau_square / (alpha + tau_square)
            assert np.min(prox - lower) >= -3e-8
            assert np.min(degree_solution - prox) >= -3e-8
            assert np.max(degree_solution - prox) <= contraction * bracket_width + 3e-8

            inner_error = 0.3 * contraction * bracket_width
            approximate = np.maximum(prox - inner_error, 0.0)
            shifted_residual = shifted_load - shifted_matrix @ approximate
            inner_width = np.max(
                np.maximum(shifted_residual, 0.0) / ((alpha + tau_square) * degree)
            )
            assert np.min(prox - approximate) >= -3e-8
            assert np.max(prox - approximate) <= inner_width + 3e-8
            assert np.min(degree_solution - approximate) >= -3e-8
            assert np.max(degree_solution - approximate) <= (
                contraction * bracket_width + inner_width + 3e-8
            )

    for eta_fraction in (0.2, 0.5, 0.8):
        eta = eta_fraction * degree_solution[source]
        shaved = np.maximum(degree_solution - eta, 0.0)
        shaved_support = np.flatnonzero(shaved > 1e-10)
        if len(shaved_support):
            shaved_set = set(map(int, shaved_support))
            seen = {int(source)}
            stack = [int(source)]
            while stack:
                vertex = stack.pop()
                for neighbor in np.flatnonzero(adjacency[vertex]):
                    neighbor = int(neighbor)
                    if neighbor in shaved_set and neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            assert seen == shaved_set

            shifted_load = -alpha * (rho + eta) * degree
            shifted_load[source] += alpha
            shifted_residual = shifted_load - hmat @ shaved
            assert np.min(shifted_residual[shaved_support]) >= -3e-8
        else:
            shifted_load = -alpha * (rho + eta) * degree
            shifted_load[source] += alpha

        shaved_gap = degree_objective(shaved) - degree_objective(degree_solution)
        assert shaved_gap >= -3e-9
        assert shaved_gap <= 0.5 * alpha * eta + 3e-8

        shifted_solution = exact_obstacle_solution(hmat, shifted_load)
        assert np.min(shifted_solution - shaved) >= -3e-8
        assert np.max(shifted_solution - degree_solution) <= 3e-8
        assert np.max(degree_solution - shifted_solution) <= eta + 3e-8
        shifted_gap = degree_objective(shifted_solution) - degree_objective(degree_solution)
        assert shifted_gap >= -3e-9
        assert shifted_gap <= 0.5 * alpha * eta + 3e-8

    # On the final support, the Green ground-state Schur row sums form an
    # exact decreasing capacity ledger.  The largest remaining relative
    # slack has a gate at least slack times its current harmonic row sum.
    support_solution = optimum[support] / np.sqrt(degree[support])
    support_slack = support_solution / p
    support_k = np.diag(p) @ hmat[np.ix_(support, support)] @ np.diag(p)
    source_position = position[int(source)]
    source_capacity = alpha * p[source_position]
    source_basis = np.zeros(len(support))
    source_basis[source_position] = 1.0
    assert np.max(np.abs(support_k @ np.ones(len(support)) - source_capacity * source_basis)) < 3e-9
    support_mass = degree[support] * p
    support_load = source_capacity * source_basis - alpha * rho * support_mass
    order = [source_position] + sorted(
        (index for index in range(len(support)) if index != source_position),
        key=lambda index: support_slack[index],
        reverse=True,
    )
    previous_capacity = source_capacity + 1.0e-9
    for split in range(1, len(order)):
        active = order[:split]
        remaining = order[split:]
        active_matrix = support_k[np.ix_(active, active)]
        cross = support_k[np.ix_(remaining, active)]
        schur = support_k[np.ix_(remaining, remaining)] - cross @ np.linalg.solve(
            active_matrix,
            cross.T,
        )
        harmonic_rows = schur @ np.ones(len(remaining))
        capacity = float(harmonic_rows.sum())
        assert np.min(harmonic_rows) >= -3e-9
        assert capacity <= previous_capacity + 3e-9
        assert capacity <= source_capacity + 3e-9

        active_center = np.linalg.solve(active_matrix, support_load[active])
        gate = support_load[remaining] - cross @ active_center
        assert np.max(np.abs(gate - schur @ support_slack[remaining])) < 3e-8
        largest_position = int(np.argmax(support_slack[remaining]))
        largest_slack = support_slack[remaining[largest_position]]
        assert gate[largest_position] >= largest_slack * harmonic_rows[largest_position] - 3e-8

        # Eliminate the next singleton and audit the exact capacity drop.
        rest = list(range(1, len(remaining)))
        if rest:
            next_schur = (
                schur[np.ix_(rest, rest)]
                - np.outer(
                    schur[rest, 0],
                    schur[0, rest],
                )
                / schur[0, 0]
            )
            next_capacity = float(np.ones(len(rest)) @ next_schur @ np.ones(len(rest)))
        else:
            next_capacity = 0.0
        predicted_drop = harmonic_rows[0] ** 2 / schur[0, 0]
        assert abs(capacity - next_capacity - predicted_drop) < 3e-8
        previous_capacity = capacity

    # Source-amplitude homotopy: nested support, Green-direction speed,
    # relative-slack sandwich, and the final-objective cap.
    final_degree_solution = optimum / np.sqrt(degree)
    final_degree_load = -alpha * rho * degree
    final_degree_load[source] += alpha
    full_support_p = np.zeros(n)
    full_support_p[support] = p
    full_support_slack = np.zeros(n)
    full_support_slack[support] = support_slack
    previous_homotopy = np.zeros(n)

    def final_objective(vector):
        return 0.5 * vector @ hmat @ vector - final_degree_load @ vector

    for source_scale in (0.25, 0.5, 0.75, 1.0):
        degree_load = -alpha * rho * degree
        degree_load[source] += source_scale * alpha
        homotopy = exact_obstacle_solution(hmat, degree_load)
        assert np.min(homotopy - previous_homotopy) >= -3e-8
        assert np.max(homotopy - final_degree_solution) <= 3e-8
        barrier = full_support_p * np.maximum(
            full_support_slack - (1.0 - source_scale),
            0.0,
        )
        assert np.min(homotopy - barrier) >= -3e-8

        gap = final_objective(homotopy) - final_objective(final_degree_solution)
        assert gap >= -3e-9
        assert gap <= 0.5 * alpha * p[source_position] * (1.0 - source_scale) + 3e-8

        homotopy_support = np.flatnonzero(homotopy > 1e-10)
        if len(homotopy_support):
            assert source in homotopy_support
            path_green = np.linalg.solve(
                hmat[np.ix_(homotopy_support, homotopy_support)],
                alpha * (homotopy_support == source).astype(float),
            )
            speed_square = (
                path_green @ hmat[np.ix_(homotopy_support, homotopy_support)] @ path_green
            )
            source_homotopy_position = list(map(int, homotopy_support)).index(int(source))
            assert abs(speed_square - alpha * path_green[source_homotopy_position]) < 3e-9
            assert speed_square <= alpha / degree[source] + 3e-9

        if source_scale < 1.0:
            rescaled_load = -alpha * (rho / source_scale) * degree
            rescaled_load[source] += alpha
            rescaled_solution = exact_obstacle_solution(hmat, rescaled_load)
            assert np.max(np.abs(homotopy - source_scale * rescaled_solution)) < 3e-8
        previous_homotopy = homotopy

    # Global point-source Green transform: RPPR is an upper-box obstacle in
    # the relative Green coordinate.
    source_vector = np.zeros(n)
    source_vector[source] = alpha
    global_p = np.linalg.solve(hmat, source_vector)
    assert abs(degree @ global_p - 1.0) < 2e-9
    degree_solution = optimum / np.sqrt(degree)
    global_q = global_p - degree_solution
    assert np.min(global_q) >= -2e-9
    assert np.max(global_q - global_p) <= 2e-9
    upper_gradient = hmat @ global_q - alpha * rho * degree
    free = degree_solution > 1e-9
    contact = ~free
    assert np.max(np.abs(upper_gradient[free])) < 2e-8
    assert np.max(upper_gradient[contact], initial=-np.inf) <= 2e-8

    # The relative solution slack s=y*/p has strict ascent to the source.
    # Its positive superlevels are connected, and uniformly shaving s gives
    # a connected-support lower subsolution with a linear objective cap.
    solution_slack = degree_solution / global_p
    assert np.min(solution_slack) >= -2e-8
    assert np.max(solution_slack) <= 1 + 2e-8
    for vertex in np.flatnonzero(free):
        vertex = int(vertex)
        if vertex == source:
            continue
        assert any(
            solution_slack[int(neighbor)] > solution_slack[vertex] + 1e-10
            for neighbor in np.flatnonzero(adjacency[vertex])
        )
    assert solution_slack[source] >= np.max(solution_slack) - 2e-8
    for eta in (0.2, 0.5, 0.8):
        eta *= solution_slack[source]
        truncated_slack = np.maximum(solution_slack - eta, 0.0)
        truncated_solution = global_p * truncated_slack
        truncated_support = np.flatnonzero(truncated_solution > 1e-10)
        if len(truncated_support):
            truncated_set = set(map(int, truncated_support))
            seen = {int(source)}
            stack = [int(source)]
            while stack:
                vertex = stack.pop()
                for neighbor in np.flatnonzero(adjacency[vertex]):
                    neighbor = int(neighbor)
                    if neighbor in truncated_set and neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            assert seen == truncated_set

            degree_load = -alpha * rho * degree
            degree_load[source] += alpha
            residual = degree_load - hmat @ truncated_solution
            assert np.min(residual[truncated_support]) >= -3e-8

        degree_load = -alpha * rho * degree
        degree_load[source] += alpha

        def objective(vector):
            return 0.5 * vector @ hmat @ vector - degree_load @ vector

        gap = objective(truncated_solution) - objective(degree_solution)
        assert gap >= -3e-9
        assert gap <= 0.5 * alpha * global_p[source] * eta + 3e-8

    relative = np.linspace(0.1, 0.9, n)
    transformed = global_p * relative
    left = transformed @ hmat @ transformed
    edge_energy = 0.0
    coupling = (1 - alpha) / 2
    for left_vertex in range(n):
        for right_vertex in range(left_vertex + 1, n):
            if adjacency[left_vertex, right_vertex]:
                edge_energy += (
                    coupling
                    * global_p[left_vertex]
                    * global_p[right_vertex]
                    * (relative[left_vertex] - relative[right_vertex]) ** 2
                )
    right = alpha * global_p[source] * relative[source] ** 2 + edge_energy
    assert abs(left - right) < 3e-9


def main():
    rng = random.Random(20260831)
    audit_constant_bracket_nonmonotonicity()
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
            audit_global_positive_boundary_subgradient(rng, qmat, alpha, sigma)
            audit_arbitrary_feasible_minimum_subgradient(rng, qmat, alpha, sigma)
            audit_proximal_gradient_mapping_cap(rng, qmat, alpha, sigma)
            audit_exact_packet_bank(qmat, degree, alpha, sigma, rng.randrange(n))
            shifted = qmat + alpha * np.eye(n)
            lipschitz = 1.0 + alpha
            root = np.sqrt(2.0 * alpha / lipschitz)
            transition = np.eye(n) - shifted / lipschitz
            diagonal = (1.0 - root * root) / 2.0
            assert np.max(np.abs(np.diag(transition) - diagonal)) < 3e-12
            off_diagonal_transition = transition - diagonal * np.eye(n)
            assert np.min(off_diagonal_transition) >= -3e-12
            current_gap = np.array([rng.uniform(-1.0, 1.0) for _ in range(n)])
            auxiliary_gap = np.array([rng.uniform(-1.0, 1.0) for _ in range(n)])
            extrapolate_gap = (
                current_gap + root * auxiliary_gap
            ) / (1.0 + root)
            next_current_gap = transition @ extrapolate_gap
            direct_next_extrapolate_gap = (
                2.0 * next_current_gap
                - (1.0 - root) * current_gap
            ) / (1.0 + root)
            flux_next_extrapolate_gap = (
                root * (1.0 - root) * auxiliary_gap
                + 2.0 * off_diagonal_transition @ extrapolate_gap
            ) / (1.0 + root)
            assert np.max(
                np.abs(
                    direct_next_extrapolate_gap
                    - flux_next_extrapolate_gap
                )
            ) < 3e-12
            audit_green_amplitude_spine(
                adjacency,
                qmat,
                degree,
                alpha,
                rng.randrange(n),
            )

    print(
        "shifted-debt envelope, arbitrary feasible minimum-subgradient and "
        "proximal-gradient caps, solution-shave/Green/relative-slack/capacity/"
        "source-ramp, retained-prox-bracket, and momentum-flux identities, "
        "exact constant-"
        "bracket nonmonotonicity, zero append, and packet bank verified"
    )


if __name__ == "__main__":
    main()
