"""Numerical witnesses for the spectral-balance research note.

The script is diagnostic only.  It uses dense linear algebra on small graphs
to test exact formulas before they are promoted to proofs.
"""

from __future__ import annotations

import argparse
import json

import numpy as np


def pagerank_matrix(adjacency: np.ndarray, alpha: float) -> tuple[np.ndarray, np.ndarray]:
    degree = adjacency.sum(axis=1)
    inv_sqrt = np.diag(1.0 / np.sqrt(degree))
    normalized_adjacency = inv_sqrt @ adjacency @ inv_sqrt
    q = ((1.0 + alpha) / 2.0) * np.eye(len(degree))
    q -= ((1.0 - alpha) / 2.0) * normalized_adjacency
    return q, degree


def clique_with_seed_leaf(size: int) -> np.ndarray:
    """K_size on [0,size), plus a leaf opposite the seed.

    The seed is vertex 0 and the leaf is adjacent to vertex ``size-1``.  Thus
    a batch may expose the clique before the leaf becomes a live boundary
    violation; the small Dirichlet mode is not an artifact of putting the
    omitted vertex directly beside the source.
    """
    adjacency = np.zeros((size + 1, size + 1))
    adjacency[:size, :size] = 1.0
    np.fill_diagonal(adjacency, 0.0)
    adjacency[size - 1, size] = 1.0
    adjacency[size, size - 1] = 1.0
    return adjacency


def clique_with_tail(size: int, tail_length: int) -> np.ndarray:
    """K_size with a path of ``tail_length`` vertices at the opposite side."""
    n = size + tail_length
    adjacency = np.zeros((n, n))
    adjacency[:size, :size] = 1.0
    np.fill_diagonal(adjacency[:size, :size], 0.0)
    previous = size - 1
    for vertex in range(size, n):
        adjacency[previous, vertex] = 1.0
        adjacency[vertex, previous] = 1.0
        previous = vertex
    return adjacency


def clique_leaf_witness(size: int, alpha: float) -> dict[str, float | int]:
    adjacency = clique_with_seed_leaf(size)
    q, degree = pagerank_matrix(adjacency, alpha)
    face = np.arange(size)
    quu = q[np.ix_(face, face)]

    seed_load = np.zeros(size)
    seed_load[0] = alpha / np.sqrt(degree[0])
    degree_root = np.sqrt(degree[face])
    x_zero_penalty = np.linalg.solve(quu, seed_load)
    penalty_response = np.linalg.solve(quu, alpha * degree_root)

    attachment = size - 1
    coupling = -q[size, attachment]
    rho_cross = coupling * x_zero_penalty[attachment]
    rho_cross /= alpha + coupling * penalty_response[attachment]
    rho = rho_cross / 2.0

    c_u = seed_load - alpha * rho * degree_root
    x_u = np.linalg.solve(quu, c_u)
    leaf_residual = -alpha * rho - q[size, attachment] * x_u[attachment]

    seed_face_value = c_u[0] / quu[0, 0]
    seed_face_residual = c_u - quu[:, 0] * seed_face_value
    first_batch_min_residual = seed_face_residual[1:].min()

    lnorm_uu = (quu - alpha * np.eye(size)) * (2.0 / (1.0 - alpha))
    delta_u = np.linalg.eigvalsh(lnorm_uu)[0]
    mu_u = np.linalg.eigvalsh(quu)[0]
    positive_margin = float(x_u.min())

    return {
        "size": size,
        "alpha": alpha,
        "rho": float(rho),
        "rho_cross": float(rho_cross),
        "delta_u": float(delta_u),
        "mu_u": float(mu_u),
        "leaf_residual": float(leaf_residual),
        "leaf_residual_over_alpha_rho": float(leaf_residual / (alpha * rho)),
        "first_batch_min_clique_residual": float(first_batch_min_residual),
        "min_face_coordinate": positive_margin,
        "face_volume": int(degree[face].sum()),
    }


def weak_clique_chain(cluster_size: int, clusters: int, alpha: float) -> dict[str, object]:
    """Chain of cliques, used to count an arbitrarily large low spectrum."""
    n = cluster_size * clusters
    adjacency = np.zeros((n, n))
    for block in range(clusters):
        start = block * cluster_size
        stop = start + cluster_size
        adjacency[start:stop, start:stop] = 1.0
        np.fill_diagonal(adjacency[start:stop, start:stop], 0.0)
        if block:
            adjacency[start - 1, start] = 1.0
            adjacency[start, start - 1] = 1.0
    q, _ = pagerank_matrix(adjacency, alpha)
    eigenvalues = np.linalg.eigvalsh(q)
    cutoffs = [2.0 * alpha, 4.0 * alpha, np.sqrt(alpha)]
    return {
        "cluster_size": cluster_size,
        "clusters": clusters,
        "vertices": n,
        "alpha": alpha,
        "smallest_eigenvalues": eigenvalues[: min(2 * clusters, n)].tolist(),
        "counts": {
            f"below_{cutoff:.8g}": int(np.count_nonzero(eigenvalues <= cutoff))
            for cutoff in cutoffs
        },
    }


def clique_tail_witness(size: int, tail_length: int, alpha: float) -> dict[str, object]:
    adjacency = clique_with_tail(size, tail_length)
    q, degree = pagerank_matrix(adjacency, alpha)
    n = len(degree)
    seed_load = np.zeros(n)
    seed_load[0] = alpha / np.sqrt(degree[0])
    ppr = np.linalg.solve(q, seed_load)
    normalized_ppr = ppr / np.sqrt(degree)
    rho = 0.5 * normalized_ppr.min()

    c = seed_load - alpha * rho * np.sqrt(degree)
    full_solution = np.linalg.solve(q, c)
    degree_solution = full_solution / np.sqrt(degree)
    degree_scaling = np.diag(np.sqrt(degree))
    h_matrix = degree_scaling @ q @ degree_scaling
    floor_response = alpha * rho * np.linalg.solve(h_matrix, degree)
    source_profile = normalized_ppr
    green_decomposition_error = float(
        np.max(np.abs(degree_solution - (source_profile - floor_response)))
    )
    a = (1.0 + alpha) / 2.0
    face = np.arange(size)
    quu = q[np.ix_(face, face)]
    face_solution = np.linalg.solve(quu, c[face])
    first_tail_residual = c[size] - q[size, size - 1] * face_solution[-1]
    lnorm_uu = (quu - alpha * np.eye(size)) * (2.0 / (1.0 - alpha))

    return {
        "size": size,
        "tail_length": tail_length,
        "alpha": alpha,
        "rho": float(rho),
        "mu_u": float(np.linalg.eigvalsh(quu)[0]),
        "delta_u": float(np.linalg.eigvalsh(lnorm_uu)[0]),
        "first_tail_residual": float(first_tail_residual),
        "min_face_coordinate": float(face_solution.min()),
        "min_full_coordinate": float(full_solution.min()),
        "minimum_degree_solution": float(degree_solution.min()),
        "minimum_source_green_profile": float(source_profile.min()),
        "maximum_source_green_profile": float(source_profile.max()),
        "canonical_green_lower_bound": float(alpha * rho / a),
        "minimum_floor_response": float(floor_response.min()),
        "green_decomposition_error": green_decomposition_error,
        "full_support": int(np.count_nonzero(full_solution > 0.0)),
        "vertices": n,
        "face_volume": int(degree[face].sum()),
        "tail_volume": int(degree[size:].sum()),
    }


def regular_tree_chebyshev_l1(degree: int, max_order: int) -> dict[str, object]:
    """Radial ``||T_k(P)e_root||_1`` on an infinite regular tree.

    Only levels through ``max_order`` can be reached, so the calculation is
    exact without materializing the exponentially large tree.  It stress
    tests the graph-uniform stability assumption used by subset-Chebyshev
    localization.  The outermost level alone has l1 mass
    ``(2*(degree-1)/degree)**(k-1)`` for order ``k>=1``.
    """
    if degree < 3:
        raise ValueError("degree must be at least three")
    levels = max_order + 2
    counts = np.ones(levels)
    counts[1:] = degree * np.power(float(degree - 1), np.arange(levels - 1, dtype=float))

    def transition(radial_values: np.ndarray) -> np.ndarray:
        result = np.zeros_like(radial_values)
        result[0] = radial_values[1]
        result[1:-1] = (radial_values[:-2] + (degree - 1) * radial_values[2:]) / degree
        result[-1] = radial_values[-2] / degree
        return result

    previous = np.zeros(levels)
    previous[0] = 1.0
    current = transition(previous)
    norms = [float(np.sum(counts * np.abs(previous)))]
    norms.append(float(np.sum(counts * np.abs(current))))
    for _ in range(1, max_order):
        following = 2.0 * transition(current) - previous
        previous, current = current, following
        norms.append(float(np.sum(counts * np.abs(current))))

    outer_level_lower_bounds = [1.0]
    outer_level_lower_bounds.extend(
        (2.0 * (degree - 1) / degree) ** (order - 1) for order in range(1, max_order + 1)
    )
    return {
        "degree": degree,
        "max_order": max_order,
        "l1_norms": norms,
        "outer_level_lower_bounds": outer_level_lower_bounds,
    }


def shifted_two_vertex_stop(alpha: float) -> dict[str, float]:
    """Minimal stop for obtaining a low-tail discount from a scalar shift.

    This is the normalized SDDM block on one edge, with eigenvalues
    ``alpha`` and one.  A newly admitted frontier coordinate supplies the
    load ``e_2``.  The identity

        Q^-1 = (Q+sigma I)^-1
               + sigma Q^-1 (Q+sigma I)^-1

    accelerates the first term only by leaving a constant fraction of the
    slow-mode response in the second term once ``sigma >= alpha``.
    """
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    q = np.array([[diagonal, -coupling], [-coupling, diagonal]], dtype=float)
    source = np.array([0.0, 1.0])
    sigma = alpha
    exact = np.linalg.solve(q, source)
    rented = np.linalg.solve(q + sigma * np.eye(2), source)
    bought = exact - rented
    slow = np.array([1.0, 1.0]) / np.sqrt(2.0)
    exact_slow = float(slow @ exact)
    bought_slow = float(slow @ bought)
    contraction_per_pair = (coupling / diagonal) ** 2
    pairs_for_half_reduction = np.ceil(np.log(0.5) / np.log(contraction_per_pair))
    return {
        "alpha": alpha,
        "sigma": sigma,
        "minimum_eigenvalue": float(np.linalg.eigvalsh(q)[0]),
        "shifted_condition_number": float((1.0 + sigma) / (alpha + sigma)),
        "slow_tail_fraction": bought_slow / exact_slow,
        "predicted_slow_tail_fraction": sigma / (alpha + sigma),
        "shift_identity_error": float(np.linalg.norm(exact - rented - bought)),
        "row_settlement_contraction_per_pair": contraction_per_pair,
        "row_settlement_pairs_for_half_reduction": float(pairs_for_half_reduction),
        "alpha_times_pairs": float(alpha * pairs_for_half_reduction),
    }


def cut_commutator_witness(alpha: float) -> dict[str, float | int]:
    """Check the rank-two proper-face floor conjugacy numerically."""
    rng = np.random.default_rng(20260831)
    vertices = 24
    adjacency = np.zeros((vertices, vertices))
    for vertex in range(vertices - 1):
        adjacency[vertex, vertex + 1] = 1.0
        adjacency[vertex + 1, vertex] = 1.0
    for _ in range(48):
        left, right = sorted(rng.choice(vertices, 2, replace=False))
        adjacency[left, right] = 1.0
        adjacency[right, left] = 1.0
    q, degree = pagerank_matrix(adjacency, alpha)
    face = np.arange(15)
    quu = q[np.ix_(face, face)]
    s = np.sqrt(degree[face])
    b = (1.0 - alpha) / 2.0
    outside = np.arange(15, vertices)
    d_out = adjacency[np.ix_(face, outside)].sum(axis=1)
    ell = b * d_out / s
    h = quu @ s
    capital_h = float(s @ h)
    projector = np.outer(h, s) / capital_h
    propagation = np.eye(len(face)) - quu
    xi = np.sqrt(alpha)
    change = np.eye(len(face)) + xi * projector
    inverse_change = np.linalg.inv(change)
    commutator = projector @ propagation - propagation @ projector
    explicit_commutator = (np.outer(quu @ ell, s) - np.outer(h, ell)) / capital_h
    conjugated = change @ propagation @ inverse_change
    predicted = propagation + xi * commutator @ inverse_change
    singular_values = np.linalg.svd(commutator, compute_uv=False)
    cut = float(d_out.sum())
    commutator_bound = 0.5 * np.sqrt(b / alpha) + np.sqrt(b)
    return {
        "alpha": alpha,
        "face_vertices": len(face),
        "cut": cut,
        "h_identity_error": float(np.linalg.norm(h - alpha * s - ell)),
        "commutator_formula_error": float(np.linalg.norm(commutator - explicit_commutator)),
        "conjugacy_error": float(np.linalg.norm(conjugated - predicted)),
        "numerical_commutator_rank": int(np.count_nonzero(singular_values > 1.0e-11)),
        "ell_norm_squared": float(ell @ ell),
        "ell_cut_bound": float(b * b * cut),
        "commutator_norm": float(singular_values[0]),
        "commutator_norm_bound": float(commutator_bound),
        "scaled_full_perturbation_norm": float(
            xi * np.linalg.norm(commutator, 2) * np.linalg.norm(inverse_change, 2)
        ),
    }


def deterministic_frontier_probe(alpha: float) -> dict[str, object]:
    """Check the one-positive-probe leverage domination identity.

    The graph and partition are fixed rather than sampled at run time, so the
    output is a reproducible numerical regression.  The theorem tested here
    is algebraic; dense eigendecompositions are used only for diagnostics.
    """
    rng = np.random.default_rng(20260831)
    vertices = 24
    adjacency = np.zeros((vertices, vertices))
    for vertex in range(vertices - 1):
        adjacency[vertex, vertex + 1] = 1.0
        adjacency[vertex + 1, vertex] = 1.0
    for left in range(vertices):
        for right in range(left + 2, vertices):
            if rng.random() < 0.16:
                weight = float(rng.choice([0.5, 1.0, 1.5]))
                adjacency[left, right] = weight
                adjacency[right, left] = weight

    q, degree = pagerank_matrix(adjacency, alpha)
    anchor = np.arange(8)
    frontier = np.arange(8, 14)
    exterior = np.arange(14, vertices)
    t = np.concatenate((anchor, frontier))

    q_aa = q[np.ix_(anchor, anchor)]
    q_af = q[np.ix_(anchor, frontier)]
    lift = np.vstack((-np.linalg.solve(q_aa, q_af), np.eye(len(frontier))))
    q_tt = q[np.ix_(t, t)]
    k = lift.T @ q_tt @ lift
    eigenvalues, eigenvectors = np.linalg.eigh(k)
    k_inverse_half = (eigenvectors * np.power(eigenvalues, -0.5)) @ eigenvectors.T

    q_wt = q[np.ix_(exterior, t)]
    d_w_inverse_half = np.diag(1.0 / np.sqrt(degree[exterior]))
    response = -d_w_inverse_half @ q_wt @ lift @ k_inverse_half
    ones_f = np.ones(len(frontier))
    u = np.linalg.solve(q_tt, np.concatenate((np.zeros(len(anchor)), ones_f)))
    probe = -d_w_inverse_half @ q_wt @ u
    row_norms = np.linalg.norm(response, axis=1)
    whitened_probe = response @ ones_f

    weighted_mass = float(degree[exterior] @ probe)
    whitened_l1_mass = float(degree[exterior] @ whitened_probe)
    whitened_l2_mass = float(degree[exterior] @ np.square(whitened_probe))
    frontier_volume = float(degree[frontier].sum())
    return {
        "alpha": alpha,
        "vertices": vertices,
        "anchor_size": len(anchor),
        "frontier_size": len(frontier),
        "min_schur_eigenvalue": float(eigenvalues[0]),
        "min_inverse_half_entry": float(k_inverse_half.min()),
        "min_response_entry": float(response.min()),
        "min_probe_minus_row_norm": float(np.min(probe - row_norms)),
        "weighted_probe_mass": weighted_mass,
        "weighted_whitened_l1_mass": whitened_l1_mass,
        "weighted_whitened_l2_mass": whitened_l2_mass,
        "frontier_rank": len(frontier),
        "frontier_volume": frontier_volume,
        "mass_slack": frontier_volume - weighted_mass,
    }


def evolving_heavy_ball_path(
    alpha: float,
    vertices: int = 128,
    rho: float = 1.0e-5,
    max_iterations: int = 20000,
) -> dict[str, object]:
    """Stress test a no-restart accelerated recurrence on a growing path.

    This is deliberately an experiment, not a correctness theorem.  A signed
    heavy-ball state is padded by zero when the certified face grows.  At
    every step a Stieltjes common retraction is joined with the historical
    lower subsolution, and only that lower envelope controls admission.
    """
    adjacency = np.zeros((vertices, vertices))
    path_index = np.arange(vertices - 1)
    adjacency[path_index, path_index + 1] = 1.0
    adjacency[path_index + 1, path_index] = 1.0
    q, degree = pagerank_matrix(adjacency, alpha)

    load = -alpha * rho * np.sqrt(degree)
    load[0] += alpha / np.sqrt(degree[0])
    threshold = alpha * rho / 8.0
    step = 4.0 / (1.0 + np.sqrt(alpha)) ** 2
    momentum = ((1.0 - np.sqrt(alpha)) / (1.0 + np.sqrt(alpha))) ** 2

    active = np.zeros(vertices, dtype=bool)
    active[0] = True
    iterate = np.zeros(vertices)
    previous = np.zeros(vertices)
    lower = np.zeros(vertices)
    volume_work = 0.0
    expansion_iterations: list[int] = []
    expansion_sizes: list[int] = []

    for iteration in range(1, max_iterations + 1):
        face = np.flatnonzero(active)
        quu = q[np.ix_(face, face)]
        residual = load[face] - quu @ iterate[face]
        following = iterate[face] + step * residual
        following += momentum * (iterate[face] - previous[face])
        previous[face] = iterate[face]
        iterate[face] = following

        signed_residual = load[face] - quu @ iterate[face]
        super_solution = quu @ np.sqrt(degree[face])
        retraction = float(max(0.0, np.max(-signed_residual / super_solution)))
        candidate = iterate[face] - retraction * np.sqrt(degree[face])
        lower[face] = np.maximum(lower[face], candidate)

        outside = np.flatnonzero(~active)
        boundary_residual = load[outside] - q[np.ix_(outside, face)] @ lower[face]
        admitted = outside[boundary_residual > threshold / 2.0]
        if len(admitted):
            active[admitted] = True
            expansion_iterations.append(iteration)
            expansion_sizes.append(len(admitted))

        volume_work += float(degree[face].sum())
        if np.all(active):
            break

    face = np.flatnonzero(active)
    subsolution_violation = float(np.max(q[np.ix_(face, face)] @ lower[face] - load[face]))
    gaps = np.diff([0, *expansion_iterations]).tolist()
    return {
        "alpha": alpha,
        "vertices": vertices,
        "rho": rho,
        "threshold": threshold,
        "iterations": iteration,
        "active_vertices": int(active.sum()),
        "expansion_events": len(expansion_iterations),
        "max_batch_size": max(expansion_sizes, default=0),
        "max_iterations_between_expansions": max(gaps, default=0),
        "mean_iterations_between_expansions": float(np.mean(gaps)) if gaps else 0.0,
        "volume_work": volume_work,
        "subsolution_violation": subsolution_violation,
    }


def fresh_krylov_path_locality(alpha: float) -> dict[str, object]:
    """Check the endpoint-path fresh-Krylov locality lower bound.

    Each proper prefix has a transformed right-hand side at its two
    endpoints.  A zero-start polynomial of degree below half the prefix
    length therefore vanishes in the middle, while the exact transformed
    solution is bounded below by ``rho``.
    """
    vertices = max(8, int(round(1.0 / np.sqrt(alpha))))
    adjacency = np.zeros((vertices, vertices))
    path_index = np.arange(vertices - 1)
    adjacency[path_index, path_index + 1] = 1.0
    adjacency[path_index + 1, path_index] = 1.0
    degree = adjacency.sum(axis=1)
    a = (1.0 + alpha) / 2.0
    b = (1.0 - alpha) / 2.0
    h = a * np.diag(degree) - b * adjacency
    seed_load = np.zeros(vertices)
    seed_load[0] = alpha
    unregularized = np.linalg.solve(h, seed_load)
    rho = 0.5 * float(unregularized.min())
    regularized_load = seed_load - alpha * rho * degree

    minimum_boundary_excess = np.inf
    minimum_z_over_rho = np.inf
    maximum_transform_error = 0.0
    locality_work_lower_bound = 0.0
    long_faces = 0
    for size in range(1, vertices):
        face = np.arange(size)
        huu = h[np.ix_(face, face)]
        y = np.linalg.solve(huu, regularized_load[face])
        z = y + rho
        minimum_z_over_rho = min(
            minimum_z_over_rho,
            float(z.min() / rho),
        )

        transformed_load = np.zeros(size)
        transformed_load[0] = alpha
        transformed_load[-1] += rho * b
        maximum_transform_error = max(
            maximum_transform_error,
            float(np.max(np.abs(huu @ z - transformed_load))),
        )

        next_vertex = size
        boundary_excess = b * y[-1] - alpha * rho * degree[next_vertex]
        minimum_boundary_excess = min(
            minimum_boundary_excess,
            float(boundary_excess),
        )
        if size >= vertices // 2:
            long_faces += 1
            required_degree = max(0, (size - 2) // 2)
            locality_work_lower_bound += degree[face].sum() * required_degree

    final_regularized = np.linalg.solve(h, regularized_load)
    final_z = final_regularized + rho
    final_volume = float(degree.sum())
    return {
        "alpha": alpha,
        "vertices": vertices,
        "rho": rho,
        "rho_over_sqrt_alpha": rho / np.sqrt(alpha),
        "minimum_unregularized_over_sqrt_alpha": (float(unregularized.min()) / np.sqrt(alpha)),
        "minimum_boundary_excess": minimum_boundary_excess,
        "minimum_prefix_z_over_rho": minimum_z_over_rho,
        "maximum_cut_transform_error": maximum_transform_error,
        "final_z_equals_unregularized_error": float(np.max(np.abs(final_z - unregularized))),
        "long_faces": long_faces,
        "fresh_krylov_volume_work_lower_bound": locality_work_lower_bound,
        "target_M_over_sqrt_alpha": final_volume / np.sqrt(alpha),
        "fresh_M_over_alpha_scale": final_volume / alpha,
        "lower_bound_over_M_over_alpha": (locality_work_lower_bound * alpha / final_volume),
    }


def ballasted_broom_witness(alpha: float) -> dict[str, object]:
    """Evaluate the analytic reduced systems of the ballasted broom.

    The ``N`` leaves are eliminated symbolically, so even ``N=Theta(1/alpha)``
    uses only an ``O(1/sqrt(alpha))`` dense tridiagonal diagnostic.
    """
    a = (1.0 + alpha) / 2.0
    b = (1.0 - alpha) / 2.0
    leaves = int(np.ceil(10.0 / alpha))
    root_degree = leaves + 1
    rho = 1.0 / (4.0 * root_degree)
    depth = int(np.floor(1.0 / (8.0 * np.sqrt(alpha))))

    seed_value = 3.0 * alpha / (4.0 * a * root_degree)
    first_leaf_residual = -alpha * rho + b * seed_value
    first_path_residual = -2.0 * alpha * rho + b * seed_value

    root_diagonal = (root_degree * alpha + b * b) / a
    root_rhs = alpha * (3.0 - (leaves / root_degree) * (b / a)) / 4.0
    endpoint_residuals: list[float] = []
    gap_upper_bounds: list[float] = []
    volumes: list[float] = []
    spectral_ledger_lower_bound = 0.0
    for path_vertices in range(1, depth + 1):
        reduced = np.zeros((path_vertices + 1, path_vertices + 1))
        rhs = np.full(path_vertices + 1, -2.0 * alpha * rho)
        reduced[0, 0] = root_diagonal
        rhs[0] = root_rhs
        for index in range(1, path_vertices + 1):
            reduced[index, index] = 2.0 * a
            reduced[index - 1, index] = -b
            reduced[index, index - 1] = -b
        solution = np.linalg.solve(reduced, rhs)
        endpoint_residuals.append(float(b * solution[-1] - 2.0 * alpha * rho))
        volume = float(2 * leaves + 1 + 2 * path_vertices)
        gap_upper = alpha + b / volume
        volumes.append(volume)
        gap_upper_bounds.append(gap_upper)
        spectral_ledger_lower_bound += volume / np.sqrt(gap_upper)

    # Symmetry reduction of the normalized face matrix: root, the normalized
    # aggregate of all ballast leaves, then the path coordinates.  This checks
    # whether the nonnegative ``z=y+rho*1`` cut-supported right-hand side can
    # ignore the low spectral band.  It cannot on this family: the seed has
    # constant overlap with the Perron mode.
    alignment_depth = max(1, depth)
    reduced_q = np.eye(alignment_depth + 2) * a
    reduced_q[0, 1] = reduced_q[1, 0] = -b * np.sqrt(leaves / root_degree)
    reduced_q[0, 2] = reduced_q[2, 0] = -b / np.sqrt(2.0 * root_degree)
    for index in range(2, alignment_depth + 1):
        reduced_q[index, index + 1] = -b / 2.0
        reduced_q[index + 1, index] = -b / 2.0
    reduced_eigenvalues, reduced_eigenvectors = np.linalg.eigh(reduced_q)
    cut_source = np.zeros(alignment_depth + 2)
    cut_source[0] = alpha / np.sqrt(root_degree)
    cut_source[-1] = rho * b / np.sqrt(2.0)
    low_cutoff = min(20.0 * alpha, 1.0)
    low_columns = reduced_eigenvectors[:, reduced_eigenvalues <= low_cutoff]
    low_cut_source_mass = float(np.linalg.norm(low_columns.T @ cut_source))
    unit_accuracy_residual_scale = alpha * np.sqrt(rho) / 32.0

    # More generally z_gamma=y+gamma*rho*1 has normalized load
    #   alpha e_o/sqrt(d_o)+rho(gamma Q-alpha I)sqrt(d_U).
    # The minimax scalar for the whole interval [alpha,beta] is
    # gamma=2alpha/(alpha+beta).  We also record the least-squares scalar for
    # the *actual* low eigenspace of this broom.  The latter is an oracle
    # diagnostic, not an implementable cutoff rule: constructing the
    # projector is exactly the spectral work at issue.
    sqrt_degree = np.full(alignment_depth + 2, np.sqrt(2.0))
    sqrt_degree[0] = np.sqrt(root_degree)
    sqrt_degree[1] = np.sqrt(leaves)
    seed_source = np.zeros(alignment_depth + 2)
    seed_source[0] = alpha / np.sqrt(root_degree)
    gamma_minimax = 2.0 * alpha / (alpha + low_cutoff)
    gamma_load = seed_source + rho * (gamma_minimax * reduced_q @ sqrt_degree - alpha * sqrt_degree)
    gamma_low_mass = float(np.linalg.norm(low_columns.T @ gamma_load))

    projected_intercept = low_columns.T @ (seed_source - rho * alpha * sqrt_degree)
    projected_slope = low_columns.T @ (rho * reduced_q @ sqrt_degree)
    slope_norm_squared = float(projected_slope @ projected_slope)
    if slope_norm_squared > 0.0:
        gamma_oracle = max(
            0.0,
            -float(projected_intercept @ projected_slope) / slope_norm_squared,
        )
    else:
        gamma_oracle = 0.0
    oracle_low_mass = float(np.linalg.norm(projected_intercept + gamma_oracle * projected_slope))

    path_orders = np.arange(1, alignment_depth + 1, dtype=float)
    path_eigenvalues = a - b * np.cos(path_orders * np.pi / (alignment_depth + 1.0))
    constant_deflation_cutoff = 0.1

    return {
        "alpha": alpha,
        "leaves": leaves,
        "rho": rho,
        "singleton_depth": depth,
        "first_leaf_residual": first_leaf_residual,
        "first_path_residual": first_path_residual,
        "minimum_later_path_residual": min(endpoint_residuals, default=0.0),
        "minimum_face_volume": min(volumes, default=0.0),
        "maximum_gap_upper_over_alpha": (max(gap_upper_bounds, default=alpha) / alpha),
        "fresh_face_spectral_ledger_lower_bound": spectral_ledger_lower_bound,
        "target_1_over_rho_sqrt_alpha": 1.0 / (rho * np.sqrt(alpha)),
        "ledger_to_target_ratio": (spectral_ledger_lower_bound * rho * np.sqrt(alpha)),
        "cut_source_low_cutoff_over_alpha": low_cutoff / alpha,
        "reduced_face_minimum_eigenvalue_over_alpha": (float(reduced_eigenvalues[0]) / alpha),
        "reduced_face_maximum_eigenvalue": float(reduced_eigenvalues[-1]),
        "reduced_face_condition_number": float(reduced_eigenvalues[-1] / reduced_eigenvalues[0]),
        "cut_source_low_band_dimension": int(np.count_nonzero(reduced_eigenvalues <= low_cutoff)),
        "cut_source_low_mass_over_unit_accuracy_tolerance": (
            low_cut_source_mass / unit_accuracy_residual_scale
        ),
        "balanced_shift_gamma": gamma_minimax,
        "balanced_shift_low_mass_over_unit_accuracy_tolerance": (
            gamma_low_mass / unit_accuracy_residual_scale
        ),
        "oracle_low_band_gamma": gamma_oracle,
        "oracle_shift_low_mass_over_unit_accuracy_tolerance": (
            oracle_low_mass / unit_accuracy_residual_scale
        ),
        "perron_root_coordinate": float(abs(reduced_eigenvectors[0, 0])),
        "constant_deflation_cutoff": constant_deflation_cutoff,
        "path_modes_below_constant_cutoff": int(
            np.count_nonzero(path_eigenvalues <= constant_deflation_cutoff)
        ),
        "path_mode_count": alignment_depth,
    }


def canonical_l1_ledger(alpha: float) -> dict[str, object]:
    """Check the exact face and batch ``L1`` conservation identities."""
    rng = np.random.default_rng(20260831)
    vertices = 31
    adjacency = np.zeros((vertices, vertices))
    for vertex in range(vertices - 1):
        adjacency[vertex, vertex + 1] = 1.0
        adjacency[vertex + 1, vertex] = 1.0
    for left in range(vertices):
        for right in range(left + 2, vertices):
            if rng.random() < 0.09:
                weight = float(rng.choice([0.5, 1.0, 2.0]))
                adjacency[left, right] = weight
                adjacency[right, left] = weight

    degree = adjacency.sum(axis=1)
    a = (1.0 + alpha) / 2.0
    b = (1.0 - alpha) / 2.0
    h = a * np.diag(degree) - b * adjacency
    inverse_sqrt_degree = np.diag(1.0 / np.sqrt(degree))
    q = inverse_sqrt_degree @ h @ inverse_sqrt_degree
    seed = 0
    unregularized_load = np.zeros(vertices)
    unregularized_load[seed] = alpha
    unregularized_solution = np.linalg.solve(h, unregularized_load)
    rho = 0.25 * float(unregularized_solution.min())
    load = unregularized_load - alpha * rho * degree

    # Independently solve a decreasing sequence of regularization parameters
    # by exact safe pivots.  This checks the global fixed-obstacle KKT system
    # for z=y+rho*1 and the nesting of the Stieltjes homotopy support.
    homotopy_rhos = np.geomspace(
        0.99 / degree[seed],
        rho,
        num=12,
    )
    homotopy_supports: list[set[int]] = []
    obstacle_kkt_errors: list[float] = []
    obstacle_objective_errors: list[float] = []
    for homotopy_rho in homotopy_rhos:
        homotopy_load = unregularized_load - alpha * homotopy_rho * degree
        homotopy_active = np.zeros(vertices, dtype=bool)
        if homotopy_load[seed] > 0.0:
            homotopy_active[seed] = True
        homotopy_y = np.zeros(vertices)
        while np.any(homotopy_active):
            homotopy_face = np.flatnonzero(homotopy_active)
            homotopy_y[homotopy_face] = np.linalg.solve(
                h[np.ix_(homotopy_face, homotopy_face)],
                homotopy_load[homotopy_face],
            )
            homotopy_slack = h @ homotopy_y - homotopy_load
            admitted = (~homotopy_active) & (homotopy_slack < -1.0e-13)
            if not np.any(admitted):
                break
            homotopy_active[admitted] = True

        homotopy_z = homotopy_y + homotopy_rho
        obstacle_slack = h @ homotopy_z - unregularized_load
        obstacle_kkt_errors.append(
            max(
                float(np.max(homotopy_rho - homotopy_z)),
                float(np.max(-obstacle_slack)),
                float(np.max(np.abs((homotopy_z - homotopy_rho) * obstacle_slack))),
            )
        )
        original_objective = (
            0.5 * homotopy_y @ h @ homotopy_y
            - unregularized_load @ homotopy_y
            + alpha * homotopy_rho * degree @ homotopy_y
        )
        obstacle_objective = 0.5 * homotopy_z @ h @ homotopy_z - unregularized_load @ homotopy_z
        objective_constant = alpha * homotopy_rho - 0.5 * alpha * homotopy_rho**2 * degree.sum()
        obstacle_objective_errors.append(
            abs(original_objective - obstacle_objective - objective_constant)
        )
        homotopy_supports.append(set(np.flatnonzero(homotopy_active)))

    homotopy_is_nested = all(
        earlier.issubset(later)
        for earlier, later in zip(
            homotopy_supports,
            homotopy_supports[1:],
        )
    )

    active = np.zeros(vertices, dtype=bool)
    active[seed] = True
    face_errors: list[float] = []
    batch_errors: list[float] = []
    monotonicity_slacks: list[float] = []
    batch_excesses: list[float] = []
    padding_cancellation_errors: list[float] = []
    defect_energies: list[float] = []
    frontier_source_norm_squares: list[float] = []
    previous_cut_vector = np.zeros(vertices)
    total_cut_variation = 0.0

    while not np.all(active):
        face = np.flatnonzero(active)
        outside = np.flatnonzero(~active)
        y_u = np.linalg.solve(h[np.ix_(face, face)], load[face])
        cut_vector = np.zeros(vertices)
        cut_vector[face] = np.sum(adjacency[np.ix_(face, outside)], axis=1)
        total_cut_variation += float(np.linalg.norm(cut_vector - previous_cut_vector, ord=1))
        previous_cut_vector = cut_vector
        outside_signal = b * adjacency[np.ix_(outside, face)] @ y_u / degree[outside]
        total_signal_u = float(degree[outside] @ outside_signal)
        active_mass_u = float(degree[face] @ y_u)
        cut_u = float(np.sum(y_u * np.sum(adjacency[np.ix_(face, outside)], axis=1)))
        face_errors.append(
            abs(rho * degree[face].sum() + active_mass_u + (b / alpha) * cut_u - 1.0)
        )
        face_errors.append(
            abs(total_signal_u - alpha * (1.0 - rho * degree[face].sum() - active_mass_u))
        )

        excess = outside_signal - alpha * rho
        batch = outside[excess > 1.0e-13]
        if not len(batch):
            break
        persistent = outside[excess <= 1.0e-13]
        next_active = active.copy()
        next_active[batch] = True
        next_face = np.flatnonzero(next_active)
        y_t = np.linalg.solve(h[np.ix_(next_face, next_face)], load[next_face])

        next_index = {vertex: index for index, vertex in enumerate(next_face)}
        old_in_next = np.array([next_index[vertex] for vertex in face])
        batch_in_next = np.array([next_index[vertex] for vertex in batch])
        monotonicity_slacks.append(float(np.min(y_t[old_in_next] - y_u)))

        # For z=y+rho*1, padding the newly admitted block by rho cancels the
        # signed change of the cut-supported right-hand side on all old rows.
        zbar = np.full(len(next_face), rho)
        zbar[old_in_next] = y_u + rho
        next_outside = np.flatnonzero(~next_active)
        next_d_out = np.sum(adjacency[np.ix_(next_face, next_outside)], axis=1)
        transformed_load = rho * b * next_d_out
        transformed_load[next_index[seed]] += alpha
        padding_residual = transformed_load - h[np.ix_(next_face, next_face)] @ zbar
        expected_padding_residual = np.zeros(len(next_face))
        batch_positions = np.searchsorted(outside, batch)
        expected_padding_residual[batch_in_next] = degree[batch] * excess[batch_positions]
        padding_cancellation_errors.append(
            float(np.max(np.abs(padding_residual - expected_padding_residual)))
        )

        normalized_frontier_load = np.sqrt(degree[batch]) * excess[batch_positions]
        q_ub = q[np.ix_(face, batch)]
        repair = np.linalg.solve(
            q[np.ix_(face, face)],
            q_ub @ normalized_frontier_load,
        )
        defect_energies.append(float(repair @ q[np.ix_(face, face)] @ repair))
        frontier_source_norm_squares.append(
            float(normalized_frontier_load @ normalized_frontier_load)
        )

        if len(persistent):
            signal_t = b * adjacency[np.ix_(persistent, next_face)] @ y_t / degree[persistent]
            old_signal_persistent = (
                b * adjacency[np.ix_(persistent, face)] @ y_u / degree[persistent]
            )
            persistent_increase = float(degree[persistent] @ (signal_t - old_signal_persistent))
        else:
            persistent_increase = 0.0

        active_mass_t = float(degree[next_face] @ y_t)
        batch_excess = float(degree[batch] @ excess[batch_positions])
        batch_excesses.append(batch_excess)
        batch_errors.append(
            abs(persistent_increase + alpha * (active_mass_t - active_mass_u) - batch_excess)
        )
        active = next_active

    return {
        "alpha": alpha,
        "rho": rho,
        "vertices": vertices,
        "batches": len(batch_excesses),
        "active_vertices": int(active.sum()),
        "max_face_identity_error": max(face_errors, default=0.0),
        "max_batch_identity_error": max(batch_errors, default=0.0),
        "minimum_old_coordinate_increase": min(monotonicity_slacks, default=0.0),
        "total_batch_excess": float(sum(batch_excesses)),
        "per_phase_alpha_bound": alpha * len(batch_excesses),
        "total_cut_l1_variation": total_cut_variation,
        "final_face_volume": float(degree[np.flatnonzero(active)].sum()),
        "cut_variation_slack": float(degree[np.flatnonzero(active)].sum() - total_cut_variation),
        "max_padding_cancellation_error": max(padding_cancellation_errors, default=0.0),
        "total_recycling_defect_energy": float(sum(defect_energies)),
        "total_frontier_source_norm_squared": float(sum(frontier_source_norm_squares)),
        "minimum_defect_energy_slack": min(
            (
                source_norm_squared - defect_energy
                for source_norm_squared, defect_energy in zip(
                    frontier_source_norm_squares, defect_energies
                )
            ),
            default=0.0,
        ),
        "alpha_to_three_halves_scale": alpha**1.5,
        "homotopy_samples": len(homotopy_rhos),
        "homotopy_support_sizes": [len(support) for support in homotopy_supports],
        "homotopy_is_nested": homotopy_is_nested,
        "max_obstacle_kkt_error": max(obstacle_kkt_errors, default=0.0),
        "max_obstacle_objective_error": max(
            obstacle_objective_errors,
            default=0.0,
        ),
    }


def monotone_obstacle_closure(
    matrix: np.ndarray,
    rhs: np.ndarray,
    initial_support: np.ndarray | None = None,
    tolerance: float = 1.0e-12,
) -> tuple[np.ndarray, int]:
    """Solve a Stieltjes obstacle system by exact positive face closures.

    The routine is only a dense diagnostic.  Starting from a support-safe
    face, it admits every positive exterior residual and resolves the new
    principal system.  Inverse positivity makes the face solutions monotone.
    """
    vertices = len(rhs)
    if initial_support is None:
        active = rhs > tolerance
    else:
        active = np.asarray(initial_support, dtype=bool).copy()
        if not np.any(active):
            active |= rhs > tolerance

    batches = 0
    while True:
        solution = np.zeros(vertices)
        face = np.flatnonzero(active)
        if len(face):
            solution[face] = np.linalg.solve(matrix[np.ix_(face, face)], rhs[face])
        residual = rhs - matrix @ solution
        outside = np.flatnonzero(~active)
        batch = outside[residual[outside] > tolerance]
        if not len(batch):
            return solution, batches
        active[batch] = True
        batches += 1


def shifted_obstacle_prox_path(
    alpha: float,
    vertices: int = 48,
    tolerance: float = 1.0e-9,
) -> dict[str, object]:
    """Check global shifted-prox contraction and positive closure on a path.

    This is the constructive distinction between a one-shot shifted inverse
    split and repeated obstacle resolvents.  The shift is ``sigma=alpha``, so
    the theorem predicts a Euclidean contraction factor of exactly one half.
    """
    adjacency = np.zeros((vertices, vertices))
    path_index = np.arange(vertices - 1)
    adjacency[path_index, path_index + 1] = 1.0
    adjacency[path_index + 1, path_index] = 1.0
    q, degree = pagerank_matrix(adjacency, alpha)

    seed_load = np.zeros(vertices)
    seed_load[0] = alpha / np.sqrt(degree[0])
    unregularized = np.linalg.solve(q, seed_load)
    rho = 0.5 * float(np.min(unregularized / np.sqrt(degree)))
    load = seed_load - alpha * rho * np.sqrt(degree)
    optimum, optimum_batches = monotone_obstacle_closure(q, load)

    sigma = alpha
    shifted = q + sigma * np.eye(vertices)
    iterate = np.zeros(vertices)
    contraction_ratios: list[float] = []
    inner_batches: list[int] = []
    monotonicity_slacks: list[float] = []
    upper_slacks: list[float] = []
    kkt_errors: list[float] = []
    support_sizes: list[int] = []

    initial_error = float(np.linalg.norm(optimum))
    for _ in range(256):
        old_error = float(np.linalg.norm(iterate - optimum))
        residual = load - q @ iterate
        support = iterate > 1.0e-13
        correction, batches = monotone_obstacle_closure(
            shifted,
            residual,
            initial_support=support,
        )
        following = iterate + correction
        new_error = float(np.linalg.norm(following - optimum))
        if old_error:
            contraction_ratios.append(new_error / old_error)
        inner_batches.append(batches)
        monotonicity_slacks.append(float(np.min(following - iterate)))
        upper_slacks.append(float(np.min(optimum - following)))

        prox_residual = q @ following - load + sigma * (following - iterate)
        positive = following > 1.0e-12
        complementarity_error = 0.0
        if np.any(positive):
            complementarity_error = float(np.max(np.abs(prox_residual[positive])))
        if np.any(~positive):
            complementarity_error = max(
                complementarity_error,
                float(np.max(np.maximum(-prox_residual[~positive], 0.0))),
            )
        kkt_errors.append(complementarity_error)
        support_sizes.append(int(np.count_nonzero(positive)))
        iterate = following
        if new_error <= tolerance * max(1.0, initial_error):
            break

    predicted_factor = sigma / (alpha + sigma)
    return {
        "alpha": alpha,
        "vertices": vertices,
        "rho": rho,
        "sigma": sigma,
        "predicted_contraction_factor": predicted_factor,
        "outer_prox_calls": len(contraction_ratios),
        "maximum_observed_contraction_factor": max(contraction_ratios, default=0.0),
        "minimum_monotonicity_slack": min(monotonicity_slacks, default=0.0),
        "minimum_upper_slack": min(upper_slacks, default=0.0),
        "maximum_prox_kkt_error": max(kkt_errors, default=0.0),
        "optimum_discovery_batches": optimum_batches,
        "total_inner_expansion_batches": int(sum(inner_batches)),
        "maximum_inner_expansion_batches": max(inner_batches, default=0),
        "support_sizes": support_sizes,
        "final_relative_error": float(
            np.linalg.norm(iterate - optimum) / max(initial_error, 1.0e-300)
        ),
    }


def projective_tree_segment_witness() -> dict[str, float]:
    """Verify lazy Möbius tags for tree-response derivative segments."""
    slopes = np.array([0.05, 0.12, 0.21, 0.36, 0.49])
    lengths = np.array([0.7, 0.2, 1.1, 0.4, 0.9])

    a_1, w_1 = 1.35, 0.43
    matrix_1 = np.array([[0.0, w_1**2], [-1.0, a_1]])
    kappa_1 = 1.0 / w_1
    slopes_1 = w_1**2 / (a_1 - slopes)
    lengths_1 = (a_1 - slopes) * lengths / w_1

    a_2, w_2 = 1.17, 0.37
    matrix_2 = np.array([[0.0, w_2**2], [-1.0, a_2]])
    kappa_2 = 1.0 / w_2
    slopes_2 = w_2**2 / (a_2 - slopes_1)
    lengths_2 = (a_2 - slopes_1) * lengths_1 / w_2

    combined = matrix_2 @ matrix_1
    kappa = kappa_2 * kappa_1
    denominator = combined[1, 0] * slopes + combined[1, 1]
    slopes_combined = (combined[0, 0] * slopes + combined[0, 1]) / denominator
    lengths_combined = kappa * denominator * lengths

    moments = np.array([float(slopes @ lengths), float(np.sum(lengths))])
    transformed_moments = kappa * combined @ moments
    explicit_moments = np.array([float(slopes_2 @ lengths_2), float(np.sum(lengths_2))])

    delta = 0.19
    suffix = slice(2, None)
    shifted_slopes = slopes.copy()
    shifted_slopes[suffix] += delta
    suffix_moments = np.array(
        [
            float(slopes[suffix] @ lengths[suffix]),
            float(np.sum(lengths[suffix])),
        ]
    )
    shift_matrix = np.array([[1.0, delta], [0.0, 1.0]])
    shifted_suffix_moments = shift_matrix @ suffix_moments
    explicit_shifted_suffix = np.array(
        [
            float(shifted_slopes[suffix] @ lengths[suffix]),
            float(np.sum(lengths[suffix])),
        ]
    )
    return {
        "maximum_composed_slope_error": float(np.max(np.abs(slopes_2 - slopes_combined))),
        "maximum_composed_length_error": float(np.max(np.abs(lengths_2 - lengths_combined))),
        "maximum_moment_error": float(np.max(np.abs(transformed_moments - explicit_moments))),
        "maximum_suffix_shift_moment_error": float(
            np.max(np.abs(shifted_suffix_moments - explicit_shifted_suffix))
        ),
        "minimum_first_schur_denominator": float(np.min(a_1 - slopes)),
        "minimum_second_schur_denominator": float(np.min(a_2 - slopes_1)),
    }


def arbitrary_source_depth_witness(
    alpha: float,
    vertices: int = 72,
) -> dict[str, object]:
    """Stress the generalized block-depth bound with a many-row source.

    A positive target vector is chosen first and ``rhs=A@target``.  The
    target is therefore the full-support obstacle optimum even though the
    right-hand side has both signs.  Exact all-positive face pivots then test
    the arbitrary-initial-block argument rather than the canonical
    point-source specialization.
    """
    rng = np.random.default_rng(20260831)
    adjacency = np.zeros((vertices, vertices))
    for vertex in range(1, vertices):
        parent = int(rng.integers(0, vertex))
        weight = float(rng.uniform(0.4, 1.0))
        adjacency[vertex, parent] = weight
        adjacency[parent, vertex] = weight
    q, _ = pagerank_matrix(adjacency, alpha)
    sigma = max(alpha, np.sqrt(alpha) / 3.0)
    matrix = q + sigma * np.eye(vertices)
    target = np.exp(rng.normal(0.0, 1.15, size=vertices))
    target /= np.linalg.norm(target)
    rhs = matrix @ target

    active = rhs > 1.0e-13
    if not np.any(active):
        active[int(np.argmax(rhs))] = True
    eigenvalues = np.linalg.eigvalsh(matrix)
    mu = float(eigenvalues[0])
    upper = float(eigenvalues[-1])
    decay = (np.sqrt(2.0 * upper / mu) - 1.0) / (np.sqrt(2.0 * upper / mu) + 1.0)
    target_energy = float(target @ matrix @ target)
    ratios: list[float] = []
    bounds: list[float] = []
    batch_sizes: list[int] = []
    minimum_monotonicity = float("inf")
    previous = np.zeros(vertices)

    for batch_index in range(vertices + 1):
        face = np.flatnonzero(active)
        solution = np.zeros(vertices)
        solution[face] = np.linalg.solve(matrix[np.ix_(face, face)], rhs[face])
        error = target - solution
        ratio = np.sqrt(float(error @ matrix @ error) / target_energy)
        bound = (4.0 * upper / mu) * decay**batch_index
        ratios.append(float(ratio))
        bounds.append(float(bound))
        minimum_monotonicity = min(
            minimum_monotonicity,
            float(np.min(solution - previous)),
        )
        residual = rhs - matrix @ solution
        outside = np.flatnonzero(~active)
        batch = outside[residual[outside] > 1.0e-12]
        if not len(batch):
            break
        batch_sizes.append(int(len(batch)))
        active[batch] = True
        previous = solution

    return {
        "alpha": alpha,
        "sigma": sigma,
        "vertices": vertices,
        "initial_positive_rows": int(np.count_nonzero(rhs > 1.0e-13)),
        "batches": len(batch_sizes),
        "batch_sizes": batch_sizes,
        "minimum_eigenvalue": mu,
        "maximum_eigenvalue": upper,
        "decay": float(decay),
        "maximum_bound_violation": float(
            max((ratio - bound for ratio, bound in zip(ratios, bounds)), default=0.0)
        ),
        "minimum_monotonicity_slack": minimum_monotonicity,
        "final_relative_energy_error": ratios[-1],
    }


def affine_tree_transfer_witness(
    alpha: float,
    vertices: int = 31,
) -> dict[str, float | int]:
    """Verify the homogeneous 3x3 Schur transfer for arbitrary tree loads."""
    adjacency = np.zeros((vertices, vertices))
    edge = np.arange(vertices - 1)
    adjacency[edge, edge + 1] = 1.0
    adjacency[edge + 1, edge] = 1.0
    q, _ = pagerank_matrix(adjacency, alpha)
    matrix = q + max(alpha, 0.03) * np.eye(vertices)
    rng = np.random.default_rng(314159)
    load = rng.normal(size=vertices)
    diagonal = np.diag(matrix)
    weights = -np.diag(matrix, k=1)

    delta = np.empty(vertices)
    eta = np.empty(vertices)
    delta[-1] = diagonal[-1]
    eta[-1] = load[-1]
    for index in range(vertices - 2, -1, -1):
        weight = weights[index]
        delta[index] = diagonal[index] - weight**2 / delta[index + 1]
        eta[index] = load[index] + weight * eta[index + 1] / delta[index + 1]

    product = np.eye(3)
    for index in range(vertices):
        weight = weights[index] if index + 1 < vertices else 0.0
        transfer = np.array(
            [
                [diagonal[index], 0.0, -(weight**2)],
                [load[index], weight, 0.0],
                [1.0, 0.0, 0.0],
            ]
        )
        product = product @ transfer
    homogeneous = product @ np.array([1.0, 0.0, 0.0])
    delta_product = homogeneous[0] / homogeneous[2]
    eta_product = homogeneous[1] / homogeneous[2]
    direct = np.linalg.solve(matrix, load)

    return {
        "alpha": alpha,
        "vertices": vertices,
        "delta_transfer_error": float(abs(delta_product - delta[0])),
        "eta_transfer_error": float(abs(eta_product - eta[0])),
        "root_solution_error": float(abs(eta_product / delta_product - direct[0])),
        "minimum_schur_pivot": float(np.min(delta)),
    }


def pinning_leverage_witness(alpha: float) -> dict[str, object]:
    """Check why principal activation is high-leverage unpinning."""
    adjacency = np.zeros((9, 9))
    edge = np.arange(8)
    adjacency[edge, edge + 1] = 1.0
    adjacency[edge + 1, edge] = 1.0
    q, _ = pagerank_matrix(adjacency, alpha)
    vertex = 4
    inverse_diagonal = float(np.linalg.inv(q)[vertex, vertex])
    rows = []
    for pin in [1.0, 10.0, 1.0e2, 1.0e4, 1.0e8]:
        pinned = q.copy()
        pinned[vertex, vertex] += pin
        measured = pin * float(np.linalg.inv(pinned)[vertex, vertex])
        predicted = pin * inverse_diagonal / (1.0 + pin * inverse_diagonal)
        rows.append(
            {
                "pin": pin,
                "leverage": measured,
                "formula_error": abs(measured - predicted),
            }
        )
    return {
        "alpha": alpha,
        "inverse_diagonal": inverse_diagonal,
        "rows": rows,
        "largest_pin_gap_to_one": 1.0 - rows[-1]["leverage"],
    }


def green_logdet_separation_witness(alpha: float) -> dict[str, float]:
    """Two-vertex separation between Green amplification and log-det loss."""
    a = (1.0 + alpha) / 2.0
    b = (1.0 - alpha) / 2.0
    coupling = b / a
    schur_fraction = 1.0 - coupling**2
    logdet_loss = -np.log(schur_fraction)
    lift_to_schur = coupling**2 / schur_fraction
    return {
        "alpha": alpha,
        "normalized_coupling": coupling,
        "schur_fraction": schur_fraction,
        "schur_fraction_formula_error": abs(schur_fraction - alpha / a**2),
        "extension_condition": (1.0 + coupling) / (1.0 - coupling),
        "extension_condition_times_alpha": alpha * (1.0 + coupling) / (1.0 - coupling),
        "logdet_loss": float(logdet_loss),
        "lift_to_schur_energy_ratio": lift_to_schur,
        "ratio_over_logdet": float(lift_to_schur / logdet_loss),
    }


def light_rank_logdet_witness(tau: float) -> dict[str, float | int]:
    """Constant log-det loss can hide 1/tau^2 independent response columns."""
    tau = min(max(tau, 1.0e-4), 0.5)
    batches = int(np.ceil(1.0 / tau**2))
    response = tau * np.eye(batches)
    total_logdet = batches * (-np.log1p(-(tau**2)))
    return {
        "tau": tau,
        "batches": batches,
        "response_rank": int(np.linalg.matrix_rank(response)),
        "total_logdet_loss": float(total_logdet),
        "total_response_frobenius_squared": float(np.linalg.norm(response, ord="fro") ** 2),
        "final_pair_condition": (1.0 + tau) / (1.0 - tau),
    }


def chronological_block_cholesky_witness(
    alpha: float,
    vertices: int = 24,
) -> dict[str, float | int]:
    """Verify that admission-order block Cholesky retains the old factor."""
    rng = np.random.default_rng(20260831)
    adjacency = np.zeros((vertices, vertices))
    edge = np.arange(vertices - 1)
    adjacency[edge, edge + 1] = 1.0
    adjacency[edge + 1, edge] = 1.0
    for left in range(vertices):
        for right in range(left + 2, vertices):
            if rng.random() < 0.12:
                weight = float(rng.uniform(0.1, 1.0))
                adjacency[left, right] = weight
                adjacency[right, left] = weight
    q, _ = pagerank_matrix(adjacency, alpha)
    matrix = q + max(alpha, 0.02) * np.eye(vertices)

    factor = np.linalg.cholesky(matrix[:1, :1])
    maximum_reconstruction_error = 0.0
    maximum_old_factor_change = 0.0
    for stop in range(2, vertices + 1):
        coupling = matrix[: stop - 1, stop - 1 : stop]
        raw = matrix[stop - 1 : stop, stop - 1 : stop]
        response = np.linalg.solve(factor, coupling)
        schur = raw - response.T @ response
        enlarged = np.zeros((stop, stop))
        enlarged[:-1, :-1] = factor
        enlarged[-1:, :-1] = response.T
        enlarged[-1, -1] = np.sqrt(schur[0, 0])
        direct = np.linalg.cholesky(matrix[:stop, :stop])
        maximum_old_factor_change = max(
            maximum_old_factor_change,
            float(np.max(np.abs(direct[:-1, :-1] - factor))),
        )
        factor = enlarged
        maximum_reconstruction_error = max(
            maximum_reconstruction_error,
            float(np.linalg.norm(factor @ factor.T - matrix[:stop, :stop], ord=np.inf)),
        )

    return {
        "alpha": alpha,
        "vertices": vertices,
        "factor_nonzeros": int(np.count_nonzero(np.abs(factor) > 1.0e-13)),
        "maximum_old_factor_change": maximum_old_factor_change,
        "maximum_reconstruction_error": maximum_reconstruction_error,
    }


def formed_face_prox_contraction_witness(
    alpha: float,
    ambient_vertices: int = 40,
    face_vertices: int = 12,
) -> dict[str, float | int]:
    """Saturate the prox contraction on the final-face lowest eigenvector."""
    adjacency = np.zeros((ambient_vertices, ambient_vertices))
    edge = np.arange(ambient_vertices - 1)
    adjacency[edge, edge + 1] = 1.0
    adjacency[edge + 1, edge] = 1.0
    q, _ = pagerank_matrix(adjacency, alpha)
    face = q[:face_vertices, :face_vertices]
    eigenvalues, eigenvectors = np.linalg.eigh(face)
    mu_star = float(eigenvalues[0])
    optimum = eigenvectors[:, 0]
    if optimum.sum() < 0.0:
        optimum = -optimum
    load = face @ optimum
    sigma = mu_star
    prox = np.linalg.solve(face + sigma * np.eye(face_vertices), load)
    measured = float(np.linalg.norm(prox - optimum) / np.linalg.norm(optimum))
    predicted = sigma / (mu_star + sigma)
    return {
        "alpha": alpha,
        "ambient_vertices": ambient_vertices,
        "face_vertices": face_vertices,
        "mu_star": mu_star,
        "mu_star_over_alpha": mu_star / alpha,
        "minimum_load": float(np.min(load)),
        "measured_contraction": measured,
        "predicted_contraction": predicted,
        "formula_error": abs(measured - predicted),
    }


def floor_aware_boundary_coupling_witness(alpha: float) -> dict[str, float | int]:
    """Check the floor-aware boundary-coupling inequality.

    If the full PageRank operator has spectrum in ``[alpha,1]``, then for a
    principal block ``A`` and exterior coupling ``C=-Q_WU`` one has

        C.T C <= (A-alpha I)(I-A).

    The endpoint path supplies eigenvalues close enough to the floor to also
    exercise the low window ``[alpha,alpha+tau^2]`` at ``tau=sqrt(alpha)``.
    """
    face_vertices = max(16, min(512, int(np.ceil(np.pi / np.sqrt(alpha)))))
    vertices = face_vertices + 1
    adjacency = np.zeros((vertices, vertices))
    edge = np.arange(vertices - 1)
    adjacency[edge, edge + 1] = 1.0
    adjacency[edge + 1, edge] = 1.0
    q, _ = pagerank_matrix(adjacency, alpha)
    a = q[:face_vertices, :face_vertices]
    c = -q[face_vertices:, :face_vertices]
    identity = np.eye(face_vertices)
    old_slack = a - a @ a - c.T @ c
    floor_slack = (a - alpha * identity) @ (identity - a) - c.T @ c

    eigenvalues, eigenvectors = np.linalg.eigh(a)
    tau = np.sqrt(alpha)
    low = eigenvalues <= alpha + tau**2 + 1.0e-14
    p_low = eigenvectors[:, low] @ eigenvectors[:, low].T
    p_high = identity - p_low
    low_coupling = float(np.linalg.norm(c @ p_low, ord=2))
    high_slack = p_high @ a @ a @ p_high - tau**2 * p_high @ c.T @ c @ p_high
    rng = np.random.default_rng(20260831)
    low_error = p_low @ rng.normal(size=face_vertices)
    positive_error = np.maximum(low_error, 0.0)
    laplacian = a - alpha * identity
    s_u = np.sqrt(adjacency.sum(axis=1)[:face_vertices])
    s_w = np.sqrt(adjacency.sum(axis=1)[face_vertices:])
    positive_output = np.maximum(c @ low_error, 0.0)
    weighted_positive_output = float(s_w @ positive_output)
    markov_energy = float(positive_error @ laplacian @ positive_error)
    original_energy = float(low_error @ laplacian @ low_error)
    stationary_cut_energy = float(s_u @ laplacian @ s_u)
    one_sided_bound = tau * np.sqrt(stationary_cut_energy) * np.linalg.norm(low_error)
    return {
        "alpha": alpha,
        "tau": tau,
        "face_vertices": face_vertices,
        "minimum_face_eigenvalue": float(eigenvalues[0]),
        "low_window_dimension": int(np.count_nonzero(low)),
        "minimum_old_slack_eigenvalue": float(np.linalg.eigvalsh(old_slack)[0]),
        "minimum_floor_slack_eigenvalue": float(np.linalg.eigvalsh(floor_slack)[0]),
        "low_coupling_norm": low_coupling,
        "low_coupling_over_tau": low_coupling / tau,
        "minimum_high_split_slack_eigenvalue": float(np.linalg.eigvalsh(high_slack)[0]),
        "stationary_identity_error": float(np.linalg.norm(laplacian @ s_u - c.T @ s_w)),
        "positive_truncation_energy_slack": original_energy - markov_energy,
        "weighted_positive_low_output": weighted_positive_output,
        "one_sided_low_output_bound": float(one_sided_bound),
        "one_sided_bound_slack": float(one_sided_bound - weighted_positive_output),
    }


def damped_nag_spectral_balance_witness(alpha: float) -> dict[str, float | int]:
    """Check the tunable underdamped/overdamped NAG root split."""
    tau = max(np.sqrt(alpha), alpha**0.25)
    damping = np.sqrt(alpha + tau**2)
    beta = (1.0 - damping) / (1.0 + damping)
    eigenvalues = np.geomspace(alpha, 1.0, 2000)
    high_modulus_violation = 0.0
    low_rate_violation = 0.0
    low_count = 0
    high_count = 0
    largest_floor_root = 0.0
    for eigenvalue in eigenvalues:
        coefficient = (1.0 + beta) * (1.0 - eigenvalue)
        discriminant = coefficient**2 - 4.0 * beta * (1.0 - eigenvalue)
        roots = np.roots([1.0, -coefficient, beta * (1.0 - eigenvalue)])
        modulus = float(np.max(np.abs(roots)))
        if eigenvalue >= damping**2 * (1.0 - 1.0e-12):
            high_count += 1
            high_modulus_violation = max(
                high_modulus_violation,
                modulus - np.sqrt(beta),
            )
        else:
            low_count += 1
            largest_root = float(np.max(np.real(roots)))
            low_rate_violation = max(
                low_rate_violation,
                largest_root - (1.0 - eigenvalue / (4.0 * damping)),
            )
            if eigenvalue <= alpha * (1.0 + 1.0e-12):
                largest_floor_root = largest_root
        if eigenvalue < damping**2 and discriminant < -1.0e-10:
            low_rate_violation = max(low_rate_violation, -discriminant)

    return {
        "alpha": alpha,
        "tau": tau,
        "damping": damping,
        "beta": beta,
        "breakpoint": damping**2,
        "low_grid_points": low_count,
        "high_grid_points": high_count,
        "maximum_high_modulus_violation": high_modulus_violation,
        "maximum_low_rate_violation": low_rate_violation,
        "floor_largest_root": largest_floor_root,
        "floor_decay_lower_bound": alpha / (4.0 * damping),
        "fast_time_scale": 1.0 / damping,
        "slow_time_scale": damping / alpha,
    }


def narrow_band_asynchronous_crossing_witness(
    alpha: float,
) -> dict[str, object]:
    """Show that one identical floor eigenvalue permits arbitrary crossings.

    This is an operator-level obstruction only.  It checks that spectral
    width, quadratic energy, and absolute output mass cannot by themselves
    imply a projective first-crossing count.
    """
    tau = np.sqrt(alpha)
    damping = np.sqrt(alpha + tau**2)
    beta = (1.0 - damping) / (1.0 + damping)
    eigenvalue = alpha
    coefficient = (1.0 + beta) * (1.0 - eigenvalue)
    roots = np.sort(np.roots([1.0, -coefficient, beta * (1.0 - eigenvalue)]).real)
    r_minus = float(roots[0])
    r_plus = float(roots[1])
    ratio = r_plus / r_minus
    crossing_times = [1, 2, 4, 8, 16, 32]
    zero_errors: list[float] = []
    negative_before: list[bool] = []
    positive_after: list[bool] = []
    initial_energy = 0.0
    total_sampled_flux = 0.0
    scale = 1.0e-8
    scaled_zero_errors: list[float] = []

    for index, crossing_time in enumerate(crossing_times, start=1):
        epsilon = 2.0 ** (-index) * ratio ** (-crossing_time)

        def value(time: int, multiplier: float = 1.0) -> float:
            return multiplier * epsilon * (r_plus**time - ratio**crossing_time * r_minus**time)

        zero_errors.append(abs(value(crossing_time)))
        negative_before.append(value(crossing_time - 1) < 0.0)
        positive_after.append(value(crossing_time + 1) > 0.0)
        initial_energy += value(0) ** 2 + value(1) ** 2
        total_sampled_flux += sum(abs(value(time)) for time in range(crossing_time + 2))
        scaled_zero_errors.append(abs(value(crossing_time, scale)))

    return {
        "alpha": alpha,
        "tau": tau,
        "shared_eigenvalue": eigenvalue,
        "spectral_window_upper_endpoint": alpha + tau**2,
        "r_minus": r_minus,
        "r_plus": r_plus,
        "prescribed_crossing_times": crossing_times,
        "maximum_zero_error": max(zero_errors),
        "all_negative_before": all(negative_before),
        "all_positive_after": all(positive_after),
        "summable_initial_state_energy": initial_energy,
        "sampled_absolute_flux": total_sampled_flux,
        "common_rescaling": scale,
        "rescaled_sampled_absolute_flux": scale * total_sampled_flux,
        "maximum_rescaled_zero_error": max(scaled_zero_errors),
    }


def canonical_initial_asynchronous_batch_witness(
    alpha: float,
) -> dict[str, object]:
    """Check many distinct first-step crossings from canonical zero state."""
    neighbor_count = max(4, int(np.ceil(alpha ** (-0.25))))
    b = (1.0 - alpha) / 2.0
    rho = b / (4.0 * neighbor_count**2)
    seed_step = alpha * (1.0 - rho * neighbor_count) / np.sqrt(neighbor_count)
    degrees = np.arange(1, neighbor_count + 1, dtype=float)
    endpoint_residuals = -alpha * rho * np.sqrt(degrees) + b * seed_step / np.sqrt(
        neighbor_count * degrees
    )
    crossing_times = (
        alpha * rho * np.sqrt(degrees) / (b * seed_step / np.sqrt(neighbor_count * degrees))
    )
    formula_times = degrees / (4.0 * neighbor_count * (1.0 - b / (4.0 * neighbor_count)))
    normalized_endpoint_residuals = np.sqrt(degrees) * endpoint_residuals
    vertex_count = 1 + neighbor_count + neighbor_count * (neighbor_count - 1) // 2
    adjacency = np.zeros((vertex_count, vertex_count), dtype=float)
    next_leaf = 1 + neighbor_count
    for degree in range(1, neighbor_count + 1):
        neighbor = degree
        adjacency[0, neighbor] = 1.0
        adjacency[neighbor, 0] = 1.0
        for _ in range(degree - 1):
            adjacency[neighbor, next_leaf] = 1.0
            adjacency[next_leaf, neighbor] = 1.0
            next_leaf += 1
    graph_degrees = adjacency.sum(axis=1)
    inv_sqrt_degree = np.diag(1.0 / np.sqrt(graph_degrees))
    q_matrix = ((1.0 + alpha) / 2.0) * np.eye(
        vertex_count
    ) - b * inv_sqrt_degree @ adjacency @ inv_sqrt_degree
    load = -alpha * rho * np.sqrt(graph_degrees)
    load[0] += alpha / np.sqrt(graph_degrees[0])
    first_iterate = np.zeros(vertex_count)
    first_iterate[0] = load[0]
    direct_residual = load - q_matrix @ first_iterate
    direct_neighbor_residuals = direct_residual[1 : 1 + neighbor_count]
    direct_crossing_times = -load[1 : 1 + neighbor_count] / (
        direct_neighbor_residuals - load[1 : 1 + neighbor_count]
    )

    return {
        "alpha": alpha,
        "neighbor_count": neighbor_count,
        "vertex_count": vertex_count,
        "rho": rho,
        "seed_first_step": seed_step,
        "minimum_crossing_time": float(np.min(crossing_times)),
        "maximum_crossing_time": float(np.max(crossing_times)),
        "minimum_crossing_separation": float(np.min(np.diff(crossing_times))),
        "maximum_formula_error": float(np.max(np.abs(crossing_times - formula_times))),
        "maximum_direct_matrix_time_error": float(
            np.max(np.abs(direct_crossing_times - crossing_times))
        ),
        "maximum_direct_matrix_residual_error": float(
            np.max(np.abs(direct_neighbor_residuals - endpoint_residuals))
        ),
        "minimum_full_matrix_eigenvalue": float(np.linalg.eigvalsh(q_matrix)[0]),
        "maximum_full_matrix_eigenvalue": float(np.linalg.eigvalsh(q_matrix)[-1]),
        "all_cross_in_first_step": bool(
            np.all(crossing_times > 0.0) and np.all(crossing_times < 1.0)
        ),
        "all_endpoint_residuals_positive": bool(np.all(endpoint_residuals > 0.0)),
        "minimum_normalized_endpoint_residual": float(np.min(normalized_endpoint_residuals)),
    }


def abstract_fresh_load_root_wait_witness(alpha: float) -> dict[str, object]:
    """Check the root-time-per-stage obstruction without one-source signs."""
    if 2.5 * alpha >= 1.0:
        raise ValueError("witness requires alpha < 0.4")
    theta = alpha
    eigenvalue = 2.0 * alpha
    coupling = alpha / 2.0
    exact_center = 4.0 * theta / alpha
    beta = (1.0 - np.sqrt(alpha)) / (1.0 + np.sqrt(alpha))
    h = -exact_center
    velocity = 0.0
    products = 0
    pending_residual = theta + coupling * h
    while pending_residual < 0.0 and products < 10_000_000:
        next_h = (1.0 - eigenvalue) * (h + beta * velocity)
        next_velocity = next_h - h
        h = next_h
        velocity = next_velocity
        pending_residual = theta + coupling * h
        products += 1

    stage_count = max(1, int(np.floor(1.0 / np.sqrt(alpha))))
    return {
        "alpha": alpha,
        "block_eigenvalues": [1.5 * alpha, 2.5 * alpha],
        "exact_old_face_gate": theta,
        "initial_pending_residual": -theta,
        "products_to_first_crossing": products,
        "products_times_sqrt_alpha": products * np.sqrt(alpha),
        "root_scale_stage_count": stage_count,
        "serial_fresh_load_products": stage_count * products,
        "serial_products_times_alpha": stage_count * products * alpha,
        "final_pending_residual": pending_residual,
    }


def scratch_dominance_projection_stop() -> dict[str, object]:
    """Show that joining scratch with a subsolution can raise NAG energy."""
    alpha = 1.6402418651905565e-5
    adjacency = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
    degrees = adjacency.sum(axis=1)
    q_matrix = ((1.0 + alpha) / 2.0) * np.eye(3) - ((1.0 - alpha) / 2.0) * adjacency / np.outer(
        np.sqrt(degrees), np.sqrt(degrees)
    )
    exact = np.array([0.57714942, 0.71292356, 0.59825843])
    lower = np.array([0.09098101, 0.02539009, 0.11210235])
    scratch = np.array([0.04021504, 0.12062264, 0.62105751])
    projected = np.maximum(scratch, lower)
    error = scratch - exact
    projected_error = projected - exact

    def zero_velocity_energy(vector: np.ndarray) -> float:
        return float(
            0.5 * np.linalg.norm(q_matrix @ vector) ** 2 + 0.5 * alpha * vector @ q_matrix @ vector
        )

    old_energy = zero_velocity_energy(error)
    projected_energy = zero_velocity_energy(projected_error)
    old_q_energy = float(error @ q_matrix @ error)
    projected_q_energy = float(projected_error @ q_matrix @ projected_error)
    return {
        "alpha": alpha,
        "minimum_subsolution_slack": float(np.min(q_matrix @ (exact - lower))),
        "old_accelerated_energy": old_energy,
        "projected_accelerated_energy": projected_energy,
        "accelerated_energy_ratio": projected_energy / old_energy,
        "old_q_energy": old_q_energy,
        "projected_q_energy": projected_q_energy,
        "ordinary_q_energy_decreased": projected_q_energy < old_q_energy,
        "accelerated_energy_increased": projected_energy > old_energy,
    }


def perron_survival_and_overlap_witness(alpha: float) -> dict[str, object]:
    """Check chamber attenuation, leakage, and sliding-interval overlap."""
    chamber_length = max(4, int(np.ceil(2.0 / np.sqrt(alpha))))
    angle = np.pi / (chamber_length + 1)
    perron_root = float(np.cos(angle))
    coordinates = np.arange(1, chamber_length + 1, dtype=float)
    perron = np.sin(angle * coordinates)
    perron /= np.max(perron)
    a = (1.0 + alpha) / 2.0
    b = (1.0 - alpha) / 2.0
    theta = b / a
    chamber_eigenvalue = a - b * perron_root
    attenuation_generating_bound = theta * (1.0 - perron_root) / (1.0 - theta * perron_root)
    attenuation_spectral_ratio = (chamber_eigenvalue - alpha) / chamber_eigenvalue
    cut_leakage = float(perron[0] + perron[-1])
    degree_mass = float(2.0 * np.sum(perron))
    leakage_identity_right = (1.0 - perron_root) * degree_mass
    chamber_volume = 2 * chamber_length
    leakage_volume_lower_bound = cut_leakage / (1.0 - perron_root)
    sliding_intervals = chamber_length + 1
    counted_sliding_volume = sliding_intervals * chamber_volume
    ambient_path_volume = 4 * chamber_length
    tau = np.sqrt(alpha)
    sigma = tau**2
    shifted_attenuation = (chamber_eigenvalue - alpha) / (chamber_eigenvalue + sigma)
    target_shifted_bound = tau**2 / (alpha + tau**2)

    return {
        "alpha": alpha,
        "chamber_length": chamber_length,
        "perron_root": perron_root,
        "chamber_eigenvalue": chamber_eigenvalue,
        "gap_over_alpha": (chamber_eigenvalue - alpha) / alpha,
        "survival_generating_bound": attenuation_generating_bound,
        "spectral_attenuation_ratio": attenuation_spectral_ratio,
        "survival_identity_error": abs(attenuation_generating_bound - attenuation_spectral_ratio),
        "cut_leakage": cut_leakage,
        "leakage_identity_right": leakage_identity_right,
        "leakage_identity_error": abs(cut_leakage - leakage_identity_right),
        "chamber_volume": chamber_volume,
        "leakage_volume_lower_bound": leakage_volume_lower_bound,
        "shifted_attenuation": shifted_attenuation,
        "target_shifted_bound": target_shifted_bound,
        "shifted_bound_slack": target_shifted_bound - shifted_attenuation,
        "sliding_intervals": sliding_intervals,
        "counted_sliding_volume": counted_sliding_volume,
        "ambient_path_volume": ambient_path_volume,
        "overlap_blowup": counted_sliding_volume / ambient_path_volume,
    }


def positive_fractional_polynomial_barrier(
    alpha: float,
    relative_error: float = 1.0 / 25.0,
) -> dict[str, float | int]:
    """Scalar degree bound for a universally positive walk polynomial."""
    if not 0.0 < alpha <= 0.5:
        raise ValueError("the displayed constant bound assumes alpha<=1/2")
    b = (1.0 - alpha) / 2.0
    exact_ratio = 1.0 / np.sqrt(1.0 + b)
    allowed_ratio = (1.0 + relative_error) / (1.0 - relative_error) * exact_ratio
    if allowed_ratio >= 1.0:
        raise ValueError("relative error is too large for this two-point bound")
    degree_lower_bound = int(np.ceil(np.log(allowed_ratio) / np.log(1.0 - alpha)))
    return {
        "alpha": alpha,
        "relative_error": relative_error,
        "exact_two_point_ratio": float(exact_ratio),
        "allowed_approximation_ratio": float(allowed_ratio),
        "degree_lower_bound": degree_lower_bound,
        "scaled_degree_lower_bound": float(alpha * degree_lower_bound),
    }


def positive_fractional_flow_witness(alpha: float) -> dict[str, float]:
    """Check positivity and principal-domain order for the ideal flow."""
    adjacency = np.zeros((7, 7))
    for vertex in range(6):
        adjacency[vertex, vertex + 1] = 1.0
        adjacency[vertex + 1, vertex] = 1.0
    q_matrix, _ = pagerank_matrix(adjacency, alpha)
    old = np.arange(4)
    enlarged = np.arange(7)
    packet_old = np.zeros(len(old))
    packet_old[0] = 1.0
    packet_enlarged = np.zeros(len(enlarged))
    packet_enlarged[0] = 1.0

    def matrix_function(matrix: np.ndarray, function) -> np.ndarray:
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        return (eigenvectors * function(eigenvalues)) @ eigenvectors.T

    old_block = q_matrix[np.ix_(old, old)]
    enlarged_block = q_matrix[np.ix_(enlarged, enlarged)]
    old_inverse_sqrt = matrix_function(old_block, lambda value: value**-0.5)
    enlarged_inverse_sqrt = matrix_function(enlarged_block, lambda value: value**-0.5)
    old_velocity = old_inverse_sqrt @ packet_old
    enlarged_velocity = enlarged_inverse_sqrt @ packet_enlarged

    time = 2.0 / np.sqrt(alpha)
    enlarged_inverse = np.linalg.inv(enlarged_block)
    semigroup = matrix_function(
        enlarged_block,
        lambda value: np.exp(-time * np.sqrt(value)),
    )
    state = enlarged_inverse @ (np.eye(len(enlarged)) - semigroup) @ packet_enlarged
    residual = packet_enlarged - enlarged_block @ state
    velocity = enlarged_inverse_sqrt @ residual
    error = enlarged_inverse @ packet_enlarged - state
    initial_energy = float(packet_enlarged @ enlarged_inverse @ packet_enlarged)
    error_energy = float(error @ enlarged_block @ error)

    return {
        "alpha": alpha,
        "minimum_old_velocity": float(np.min(old_velocity)),
        "minimum_enlarged_velocity": float(np.min(enlarged_velocity)),
        "minimum_domain_order_slack": float(np.min(enlarged_velocity[: len(old)] - old_velocity)),
        "minimum_flow_state": float(np.min(state)),
        "minimum_flow_residual": float(np.min(residual)),
        "minimum_flow_velocity": float(np.min(velocity)),
        "observed_energy_error_ratio": error_energy / initial_energy,
        "root_exponential_upper_bound": float(np.exp(-2.0 * time * np.sqrt(alpha))),
    }


def canonical_relative_drift_witness(alpha: float) -> dict[str, float | bool]:
    """Two-vertex stop for an unweighted relative-reservoir inequality."""
    a = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    rho = coupling / 2.0
    q_matrix = np.array([[a, -coupling], [-coupling, a]])
    load = np.array([alpha * (1.0 - rho), -alpha * rho])
    lower = alpha / 2.0
    face_center = load[0] / a
    face_error = face_center - lower
    unopened_residual = load[1] + coupling * lower
    schur = a - coupling**2 / a
    full_solution = np.linalg.solve(q_matrix, load)
    future_energy = 0.5 * schur * full_solution[1] ** 2
    active_energy = a * face_error**2
    exact_gate = load[1] + coupling * face_center

    return {
        "alpha": alpha,
        "rho": rho,
        "lower": lower,
        "face_center": face_center,
        "face_error": face_error,
        "unopened_residual": unopened_residual,
        "schur_complement": schur,
        "future_coordinate": full_solution[1],
        "exact_gate": exact_gate,
        "future_energy": future_energy,
        "active_error_energy": active_energy,
        "energy_amplification": future_energy / active_energy,
        "predicted_amplification": coupling**2 / (2.0 * alpha),
        "lower_is_face_subsolution": bool(a * lower <= load[0]),
        "first_step_affine_parameter": lower / load[0],
        "full_support_is_positive": bool(np.min(full_solution) > 0.0),
        "current_face_gap": a,
    }


def local_landscape_witness(alpha: float) -> dict[str, float | int | bool]:
    """Audit the stationary-vector ground-state identity on a path face."""
    face_size = 64
    adjacency = np.zeros((face_size + 2, face_size + 2))
    for vertex in range(face_size + 1):
        adjacency[vertex, vertex + 1] = 1.0
        adjacency[vertex + 1, vertex] = 1.0
    q_matrix, degrees = pagerank_matrix(adjacency, alpha)
    face = np.arange(1, face_size + 1)
    block = q_matrix[np.ix_(face, face)]
    square_degrees = np.sqrt(degrees[face])
    potential = (block @ square_degrees) / square_degrees

    rng = np.random.default_rng(20260831)
    trial = rng.normal(size=face_size)
    left = float(trial @ block @ trial)
    right = float(potential @ (trial**2))
    coupling = (1.0 - alpha) / 2.0
    for vertex in range(face_size - 1):
        difference = (
            trial[vertex] / square_degrees[vertex] - trial[vertex + 1] / square_degrees[vertex + 1]
        )
        right += coupling * difference**2

    eigenvalues, eigenvectors = np.linalg.eigh(block)
    low_rank = 4
    cutoff = float(eigenvalues[low_rank - 1])
    factor = 2.0
    well = potential <= factor * cutoff
    low_basis = eigenvectors[:, :low_rank]
    outside_mass = np.sum(low_basis[~well, :] ** 2, axis=0)
    well_bessel_mass = float(np.sum(low_basis[well, :] ** 2))

    expected_potential = np.full(face_size, alpha)
    expected_potential[[0, -1]] += coupling / 2.0
    return {
        "alpha": alpha,
        "face_size": face_size,
        "identity_error": abs(left - right),
        "potential_formula_error": float(np.max(np.abs(potential - expected_potential))),
        "cutoff": cutoff,
        "well_size": int(np.count_nonzero(well)),
        "low_rank": low_rank,
        "maximum_outside_mass": float(np.max(outside_mass)),
        "outside_mass_upper_bound": 1.0 / factor,
        "well_bessel_mass": well_bessel_mass,
        "well_bessel_lower_bound": (1.0 - 1.0 / factor) * low_rank,
        "rank_purchase_holds": bool(low_rank <= np.count_nonzero(well)),
    }


def connected_well_low_rank_witness(
    alpha: float,
    clusters: int = 8,
    cluster_size: int = 24,
) -> dict[str, float | int | bool]:
    """One landscape component can contain arbitrarily many low modes.

    Disjoint cliques are joined to one hub by one edge per clique.  On the
    full face the local landscape is identically ``alpha``, hence there is
    only one well component.  Vectors which are degree-constant on each
    clique and zero at the hub give an ``r``-dimensional trial space with
    Rayleigh quotient at most ``alpha+c/vol(clique)``.
    """
    if clusters < 2 or cluster_size < 2:
        raise ValueError("need at least two clusters of size at least two")
    vertices = clusters * cluster_size + 1
    hub = vertices - 1
    adjacency = np.zeros((vertices, vertices))
    for cluster in range(clusters):
        start = cluster * cluster_size
        stop = start + cluster_size
        adjacency[start:stop, start:stop] = 1.0
        np.fill_diagonal(adjacency[start:stop, start:stop], 0.0)
        port = start
        adjacency[port, hub] = 1.0
        adjacency[hub, port] = 1.0

    q_matrix, degrees = pagerank_matrix(adjacency, alpha)
    square_degrees = np.sqrt(degrees)
    landscape = (q_matrix @ square_degrees) / square_degrees
    eigenvalues = np.linalg.eigvalsh(q_matrix)
    coupling = (1.0 - alpha) / 2.0
    clique_volume = cluster_size * (cluster_size - 1) + 1
    trial_cutoff = alpha + coupling / clique_volume
    low_count = int(np.count_nonzero(eigenvalues <= trial_cutoff + 1.0e-12))

    return {
        "alpha": alpha,
        "clusters": clusters,
        "cluster_size": cluster_size,
        "vertices": vertices,
        "clique_volume": clique_volume,
        "maximum_landscape_error": float(np.max(np.abs(landscape - alpha))),
        "well_components": 1,
        "trial_cutoff": trial_cutoff,
        "eigenvalues_below_trial_cutoff": low_count,
        "minmax_rank_lower_bound": clusters,
        "minmax_bound_holds": bool(low_count >= clusters),
        "smallest_eigenvalues": eigenvalues[: clusters + 2].tolist(),
    }


def singleton_path_merge_response(
    alpha: float,
    old_vertices: int = 64,
) -> dict[str, float | int | bool]:
    """A singleton path merge requires a dense old-face lift.

    The Toeplitz block is the normalized PageRank matrix of degree-two path
    vertices.  Adding one endpoint couples through the final coordinate, so
    block inversion needs ``A^-1 e_n``.  Every entry is strictly positive;
    the explicit hyperbolic-sine formula also checks the critical
    ``Theta(1/sqrt(alpha))`` propagation length.  Paths can store this vector
    implicitly by a recurrence, so this is an interface witness rather than
    an algorithmic lower bound.
    """
    if old_vertices < 2:
        raise ValueError("old_vertices must be at least two")
    diagonal = (1.0 + alpha) / 2.0
    edge_coupling = (1.0 - alpha) / 4.0
    old_block = np.eye(old_vertices) * diagonal
    positions = np.arange(old_vertices - 1)
    old_block[positions, positions + 1] = -edge_coupling
    old_block[positions + 1, positions] = -edge_coupling
    endpoint = np.zeros(old_vertices)
    endpoint[-1] = edge_coupling
    response = np.linalg.solve(old_block, endpoint)

    kappa = np.arccosh(diagonal / (2.0 * edge_coupling))
    indices = np.arange(1, old_vertices + 1, dtype=float)
    explicit = np.sinh(indices * kappa) / np.sinh((old_vertices + 1) * kappa)
    significant = int(np.count_nonzero(response >= response[-1] / np.e))
    return {
        "alpha": alpha,
        "old_vertices": old_vertices,
        "kappa": float(kappa),
        "kappa_over_sqrt_alpha": float(kappa / np.sqrt(alpha)),
        "minimum_response_entry": float(response.min()),
        "maximum_response_entry": float(response.max()),
        "all_old_coordinates_change": bool(np.all(response > 0.0)),
        "hyperbolic_formula_error": float(np.max(np.abs(response - explicit))),
        "coordinates_within_e_of_endpoint": significant,
        "critical_length": float(1.0 / np.sqrt(alpha)),
    }


def moving_face_variation_witness(alpha: float) -> dict[str, float | bool]:
    """Unit ``P3`` stop for local stitching of the variation Gramian."""
    square_root = np.sqrt(alpha)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    q_matrix = np.array(
        [
            [diagonal, -coupling / np.sqrt(2.0), 0.0],
            [-coupling / np.sqrt(2.0), diagonal, -coupling / np.sqrt(2.0)],
            [0.0, -coupling / np.sqrt(2.0), diagonal],
        ]
    )
    old = q_matrix[:2, :2]
    cut = -q_matrix[2:3, :2]
    h = np.array([1.0, 0.0])
    w = np.zeros(2)
    q_state = (h + w) / (1.0 + square_root)

    def hard_response(matrix: np.ndarray) -> np.ndarray:
        return np.linalg.inv(2.0 * square_root * np.eye(len(matrix)) + (1.0 - square_root) * matrix)

    old_response = hard_response(old)
    grown_response = hard_response(q_matrix)[:2, :2]
    hard_jump = float(h @ (grown_response - old_response) @ h)

    def variation_hh(matrix: np.ndarray) -> np.ndarray:
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        s = square_root
        lam = eigenvalues
        a_den = 4.0 - (3.0 - s) * lam
        b_den = 2.0 * s + (1.0 - s) * lam
        numerator = (
            lam**2 * s**2
            - 4.0 * lam**2 * s
            + 3.0 * lam**2
            + 2.0 * lam * s**3
            - 8.0 * lam * s**2
            + 8.0 * lam * s
            + 2.0 * lam
            + 2.0 * s**4
            - 4.0 * s**3
            + 2.0 * s**2
        )
        values = lam * numerator / ((1.0 + s) ** 2 * a_den * b_den)
        return (eigenvectors * values) @ eigenvectors.T

    old_variation = variation_hh(old)
    grown_variation = variation_hh(q_matrix)[:2, :2]
    variation_jump = float(h @ (grown_variation - old_variation) @ h)
    return {
        "alpha": alpha,
        "cut_h": float(np.linalg.norm(cut @ h)),
        "cut_w": float(np.linalg.norm(cut @ w)),
        "cut_q": float(np.linalg.norm(cut @ q_state)),
        "hard_resolvent_jump": hard_jump,
        "remaining_variation_jump": variation_jump,
        "strict_hidden_jump": bool(hard_jump > 0.0 and variation_jump > 0.0),
        "quarter_scale_radius": float(alpha ** (-0.25)),
    }


def unsafe_offsupport_radius_witness(
    alpha: float, number_of_leaves: int = 256
) -> dict[str, float | int | bool]:
    """A radius-two traversal can cost far more than the final support.

    The seed ``o`` has one neighbor ``h`` and ``h`` has ``number_of_leaves``
    private leaves.  At the chosen canonical threshold the exact obstacle
    solution is supported only on ``o``.  Inspecting the ordinary radius-two
    ball nevertheless exposes every private leaf.
    """
    assert number_of_leaves >= 2
    number_of_vertices = number_of_leaves + 2
    adjacency = np.zeros((number_of_vertices, number_of_vertices))
    adjacency[0, 1] = adjacency[1, 0] = 1.0
    adjacency[1, 2:] = 1.0
    adjacency[2:, 1] = 1.0
    degree = adjacency.sum(axis=1)
    square_root_degree = np.sqrt(degree)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    q_matrix = diagonal * np.eye(number_of_vertices) - coupling * adjacency / np.outer(
        square_root_degree, square_root_degree
    )

    rho = 2.0 / (number_of_leaves + 1.0)
    load = -alpha * rho * square_root_degree
    load[0] += alpha / square_root_degree[0]
    solution = np.zeros(number_of_vertices)
    solution[0] = load[0] / diagonal
    residual = load - q_matrix @ solution
    complementarity_ok = bool(
        solution[0] > 0.0 and abs(residual[0]) <= 1.0e-13 and np.max(residual[1:]) < 0.0
    )
    return {
        "alpha": alpha,
        "number_of_leaves": number_of_leaves,
        "rho": rho,
        "hub_residual": float(residual[1]),
        "largest_exterior_residual": float(np.max(residual[1:])),
        "exact_support_size": 1,
        "exact_support_volume": int(degree[0]),
        "radius_two_vertices": number_of_vertices,
        "radius_two_edge_touches": number_of_leaves + 1,
        "radius_to_support_volume_ratio": float(number_of_leaves + 1),
        "canonical_complementarity_verified": complementarity_ok,
    }


def tunable_f0_substitution_stop(alpha: float) -> dict[str, float | bool]:
    """Show that the critical F0 LMI cannot be naively retuned."""
    tau = alpha**0.25
    tuned_root = np.sqrt(alpha + tau**2)
    coupling = (1.0 - alpha) / 2.0
    f_zero_at_floor = alpha * coupling
    position_update = (1.0 - alpha) / (1.0 + tuned_root)
    companion_update = tau**2 / (1.0 + tuned_root)
    initial_energy = alpha
    next_energy = alpha * position_update**2 + (1.0 + f_zero_at_floor) * companion_update**2
    return {
        "alpha": alpha,
        "tau": tau,
        "tuned_root": tuned_root,
        "floor_mode_energy_ratio": next_energy / initial_energy,
        "naive_f0_energy_increases": bool(next_energy > initial_energy),
        "small_alpha_limit": 2.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=1.0e-4)
    parser.add_argument("--max-clique", type=int, default=128)
    parser.add_argument("--clusters", type=int, default=12)
    parser.add_argument("--cluster-size", type=int, default=32)
    parser.add_argument("--tree-degree", type=int, default=4)
    parser.add_argument("--tree-order", type=int, default=16)
    args = parser.parse_args()

    clique_rows = [
        clique_leaf_witness(size, args.alpha) for size in [4, 8, 16, 32, 64, args.max_clique]
    ]
    chain = weak_clique_chain(args.cluster_size, args.clusters, args.alpha)
    tail = clique_tail_witness(
        args.cluster_size,
        max(4, int(round(1.0 / np.sqrt(args.alpha)))),
        args.alpha,
    )
    tree = regular_tree_chebyshev_l1(args.tree_degree, args.tree_order)
    shifted_stop = shifted_two_vertex_stop(args.alpha)
    cut_commutator = cut_commutator_witness(args.alpha)
    probe = deterministic_frontier_probe(args.alpha)
    evolving_path = evolving_heavy_ball_path(max(args.alpha, 1.0e-3))
    krylov_path = fresh_krylov_path_locality(args.alpha)
    broom = ballasted_broom_witness(args.alpha)
    l1_ledger = canonical_l1_ledger(args.alpha)
    shifted_prox = shifted_obstacle_prox_path(args.alpha)
    projective_segments = projective_tree_segment_witness()
    arbitrary_depth = arbitrary_source_depth_witness(args.alpha)
    affine_transfer = affine_tree_transfer_witness(args.alpha)
    pinning_leverage = pinning_leverage_witness(args.alpha)
    green_logdet = green_logdet_separation_witness(args.alpha)
    light_rank_logdet = light_rank_logdet_witness(np.sqrt(args.alpha))
    block_cholesky = chronological_block_cholesky_witness(args.alpha)
    formed_face_prox = formed_face_prox_contraction_witness(args.alpha)
    floor_aware_coupling = floor_aware_boundary_coupling_witness(args.alpha)
    damped_nag_balance = damped_nag_spectral_balance_witness(args.alpha)
    asynchronous_crossing = narrow_band_asynchronous_crossing_witness(args.alpha)
    canonical_async_batch = canonical_initial_asynchronous_batch_witness(args.alpha)
    abstract_root_wait = abstract_fresh_load_root_wait_witness(args.alpha)
    dominance_projection_stop = scratch_dominance_projection_stop()
    perron_chamber = perron_survival_and_overlap_witness(args.alpha)
    fractional_barrier = positive_fractional_polynomial_barrier(args.alpha)
    fractional_flow = positive_fractional_flow_witness(args.alpha)
    relative_drift = canonical_relative_drift_witness(args.alpha)
    local_landscape = local_landscape_witness(args.alpha)
    connected_well_rank = connected_well_low_rank_witness(args.alpha)
    path_merge_response = singleton_path_merge_response(args.alpha)
    moving_variation = moving_face_variation_witness(args.alpha)
    unsafe_radius = unsafe_offsupport_radius_witness(args.alpha)
    tunable_f0_stop = tunable_f0_substitution_stop(args.alpha)
    print(
        json.dumps(
            {
                "clique_leaf": clique_rows,
                "clique_tail": tail,
                "clique_chain": chain,
                "regular_tree_chebyshev": tree,
                "shifted_two_vertex_stop": shifted_stop,
                "cut_commutator_witness": cut_commutator,
                "deterministic_frontier_probe": probe,
                "evolving_heavy_ball_path": evolving_path,
                "fresh_krylov_path_locality": krylov_path,
                "ballasted_broom": broom,
                "canonical_l1_ledger": l1_ledger,
                "shifted_obstacle_prox_path": shifted_prox,
                "projective_tree_segment_witness": projective_segments,
                "arbitrary_source_depth_witness": arbitrary_depth,
                "affine_tree_transfer_witness": affine_transfer,
                "pinning_leverage_witness": pinning_leverage,
                "green_logdet_separation_witness": green_logdet,
                "light_rank_logdet_witness": light_rank_logdet,
                "chronological_block_cholesky_witness": block_cholesky,
                "formed_face_prox_contraction_witness": formed_face_prox,
                "floor_aware_boundary_coupling_witness": floor_aware_coupling,
                "damped_nag_spectral_balance_witness": damped_nag_balance,
                "narrow_band_asynchronous_crossing_witness": (asynchronous_crossing),
                "canonical_initial_asynchronous_batch_witness": (canonical_async_batch),
                "abstract_fresh_load_root_wait_witness": abstract_root_wait,
                "scratch_dominance_projection_stop": (dominance_projection_stop),
                "perron_survival_and_overlap_witness": perron_chamber,
                "positive_fractional_polynomial_barrier": (fractional_barrier),
                "positive_fractional_flow_witness": fractional_flow,
                "canonical_relative_drift_witness": relative_drift,
                "local_landscape_witness": local_landscape,
                "connected_well_low_rank_witness": connected_well_rank,
                "singleton_path_merge_response": path_merge_response,
                "moving_face_variation_witness": moving_variation,
                "unsafe_offsupport_radius_witness": unsafe_radius,
                "tunable_f0_substitution_stop": tunable_f0_stop,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
