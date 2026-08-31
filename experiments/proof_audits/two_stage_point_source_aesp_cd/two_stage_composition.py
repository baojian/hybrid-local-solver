#!/usr/bin/env python3
"""Exact audit of the point-source two-stage composition interfaces."""

from fractions import Fraction as F
from itertools import combinations
from math import ceil, log
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "manuscript/notes/two_stage_point_source_aesp_cd"


def solve(matrix, rhs):
    """Exact dense Gaussian elimination."""
    n = len(rhs)
    augmented = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for column in range(n):
        pivot_row = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[column],
        )
        pivot = augmented[column][column]
        augmented[column] = [value / pivot for value in augmented[column]]
        for row in range(n):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                value - scale * base for value, base in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def edge(adjacency, left, right):
    adjacency[left].append(right)
    adjacency[right].append(left)


def path_graph(size):
    adjacency = [[] for _ in range(size)]
    for vertex in range(size - 1):
        edge(adjacency, vertex, vertex + 1)
    return adjacency


def cycle_graph(size):
    adjacency = path_graph(size)
    edge(adjacency, 0, size - 1)
    return adjacency


def star_graph(leaves):
    adjacency = [[] for _ in range(leaves + 1)]
    for leaf in range(1, leaves + 1):
        edge(adjacency, 0, leaf)
    return adjacency


def complete_bipartite(left_size, right_size):
    adjacency = [[] for _ in range(left_size + right_size)]
    for left in range(left_size):
        for right in range(left_size, left_size + right_size):
            edge(adjacency, left, right)
    return adjacency


def broom_graph(handle, leaves):
    adjacency = path_graph(handle + 1)
    for _ in range(leaves):
        adjacency.append([])
        edge(adjacency, handle, len(adjacency) - 1)
    return adjacency


def degree_unscaled_system(adjacency, alpha, rho, seed):
    """Return H=aD-bA and the point-source RPPR load."""
    size = len(adjacency)
    degree = [len(row) for row in adjacency]
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    hessian = [[F(0) for _ in range(size)] for _ in range(size)]
    for vertex in range(size):
        hessian[vertex][vertex] = diagonal * degree[vertex]
        for neighbor in adjacency[vertex]:
            hessian[vertex][neighbor] = -coupling
    load = [alpha * ((1 if vertex == seed else 0) - rho * degree[vertex]) for vertex in range(size)]
    return degree, hessian, load


def restricted_solution(hessian, load, active):
    indices = sorted(active)
    values = solve(
        [[hessian[i][j] for j in indices] for i in indices],
        [load[i] for i in indices],
    )
    return dict(zip(indices, values))


def obstacle_solution(hessian, load, allowed=None):
    """Enumerate active sets; small exact reference independent of an iteration."""
    size = len(load)
    allowed = tuple(range(size)) if allowed is None else tuple(sorted(allowed))
    candidates = []
    for count in range(len(allowed) + 1):
        for active_tuple in combinations(allowed, count):
            active = set(active_tuple)
            values = restricted_solution(hessian, load, active) if active else {}
            if any(value <= 0 for value in values.values()):
                continue
            vector = [values.get(vertex, F(0)) for vertex in range(size)]
            keys = [
                load[i] - sum(hessian[i][j] * vector[j] for j in range(size)) for i in range(size)
            ]
            if any(keys[i] > 0 for i in allowed if i not in active):
                continue
            candidates.append((vector, active, keys))
    assert len(candidates) == 1
    return candidates[0]


def quadratic_value(hessian, load, vector):
    energy = sum(
        vector[i] * hessian[i][j] * vector[j]
        for i in range(len(vector))
        for j in range(len(vector))
    )
    return energy / 2 - sum(a * b for a, b in zip(load, vector))


def boundary(adjacency, active):
    return {
        neighbor for vertex in active for neighbor in adjacency[vertex] if neighbor not in active
    }


def audit_obstacle_interfaces():
    cases = [
        ("path", path_graph(7), 0, F(1, 4), F(1, 8)),
        ("cycle", cycle_graph(6), 0, F(1, 3), F(1, 7)),
        ("star", star_graph(5), 0, F(1, 4), F(1, 10)),
        ("broom", broom_graph(4, 3), 0, F(1, 5), F(1, 9)),
    ]
    summaries = []
    for name, adjacency, seed, alpha, rho in cases:
        degree, hessian, load = degree_unscaled_system(adjacency, alpha, rho, seed)
        ppr_load = [alpha if vertex == seed else F(0) for vertex in range(len(load))]
        ppr = solve(hessian, ppr_load)
        rppr, support, keys = obstacle_solution(hessian, load)

        assert all(F(0) <= ppr[i] - rppr[i] <= rho for i in range(len(load)))
        assert sum(degree[i] for i in support) <= 1 / rho
        assert all(keys[i] == 0 for i in support)
        frontier = boundary(adjacency, support)
        assert all(keys[i] <= 0 for i in frontier)
        assert seed in support

        envelope = support | frontier
        envelope_solution, envelope_support, _ = obstacle_solution(hessian, load, envelope)
        assert envelope_solution == rppr
        assert envelope_support == support

        linear_values = restricted_solution(hessian, ppr_load, envelope)
        restricted_ppr = [linear_values.get(vertex, F(0)) for vertex in range(len(load))]
        assert all(rppr[i] <= restricted_ppr[i] <= ppr[i] for i in envelope)
        assert all(ppr[i] - restricted_ppr[i] <= rho for i in range(len(load)))

        initial_gap = -quadratic_value(hessian, load, rppr)
        assert initial_gap <= alpha / (2 * degree[seed])
        summaries.append((name, len(support), sum(degree[i] for i in envelope)))
    return summaries


def audit_exact_positive_boundary_batches():
    """Exact active-set refits admit only true support and end at global KKT."""
    cases = [
        ("path", path_graph(8), F(1, 4), F(1, 10)),
        ("cycle", cycle_graph(7), F(1, 3), F(1, 12)),
        ("star", star_graph(6), F(1, 4), F(1, 12)),
        ("broom", broom_graph(4, 4), F(1, 5), F(1, 10)),
    ]
    summaries = []
    for name, adjacency, alpha, rho in cases:
        _degree, hessian, load = degree_unscaled_system(adjacency, alpha, rho, 0)
        optimum, support, _ = obstacle_solution(hessian, load)
        assert load[0] > 0
        active = {0}
        previous = [F(0) for _ in adjacency]
        batches = []
        while True:
            values = restricted_solution(hessian, load, active)
            current = [values.get(vertex, F(0)) for vertex in range(len(load))]
            assert all(current[vertex] > 0 for vertex in active)
            assert all(current[vertex] >= previous[vertex] for vertex in range(len(load)))
            keys = [
                load[i] - sum(hessian[i][j] * current[j] for j in range(len(load)))
                for i in range(len(load))
            ]
            positive = {i for i in boundary(adjacency, active) if keys[i] > 0}
            assert positive <= support
            if not positive:
                assert active == support
                assert current == optimum
                assert all(keys[i] <= 0 for i in range(len(load)) if i not in active)
                break
            batches.append(len(positive))
            previous = current
            active |= positive
        summaries.append((name, tuple(batches), len(active)))
    return summaries


def audit_linear_sparse_source_superposition():
    """Ordinary PPR superposes exactly before the RPPR obstruction below."""
    hessian = [
        [F(2, 3), -F(1, 3), F(0)],
        [-F(1, 3), F(4, 3), -F(1, 3)],
        [F(0), -F(1, 3), F(2, 3)],
    ]
    alpha = F(1, 3)
    left = solve(hessian, [alpha, F(0), F(0)])
    right = solve(hessian, [F(0), F(0), alpha])
    weights = (F(1, 5), F(4, 5))
    combined = [weights[0] * left[i] + weights[1] * right[i] for i in range(3)]
    joint = solve(
        hessian,
        [weights[0] * alpha, F(0), weights[1] * alpha],
    )
    assert combined == joint
    return weights, joint


def audit_multisource_obstruction():
    # Degree-unscaled P3 data from the scope remark.
    hessian = [
        [F(2, 3), -F(1, 3), F(0)],
        [-F(1, 3), F(4, 3), -F(1, 3)],
        [F(0), -F(1, 3), F(2, 3)],
    ]
    load = [F(1, 8), -F(1, 12), F(1, 8)]
    endpoint = load[0] / hessian[0][0]
    assert endpoint == F(3, 16)
    separate_key = load[1] - hessian[1][0] * endpoint
    joint_key = load[1] - hessian[1][0] * endpoint - hessian[1][2] * endpoint
    assert separate_key == -F(1, 48) < 0
    assert joint_key == F(1, 24) > 0
    optimum, support, _keys = obstacle_solution(hessian, load)
    assert support == {0, 1, 2}
    assert all(value > 0 for value in optimum)
    return separate_key, joint_key


def audit_every_approximate_envelope():
    """Stress the linearization on all subsets, including multiple sources."""
    cases = [
        (path_graph(6), F(1, 4), F(1, 9), [F(1, 2), 0, 0, 0, 0, F(1, 2)]),
        (star_graph(5), F(1, 3), F(1, 8), [0, F(2, 3), F(1, 3), 0, 0, 0]),
        (star_graph(5), F(1, 4), F(1, 2), [F(1), 0, 0, 0, 0, 0]),
    ]
    checked = 0
    for adjacency, alpha, rho, source_mass in cases:
        degree, hessian, _ = degree_unscaled_system(adjacency, alpha, rho, 0)
        ppr_load = [alpha * mass for mass in source_mass]
        rppr_load = [ppr_load[i] - alpha * rho * degree[i] for i in range(len(degree))]
        ppr = solve(hessian, ppr_load)
        rppr, support, _ = obstacle_solution(hessian, rppr_load)
        vertices = tuple(range(len(degree)))
        for count in range(len(vertices) + 1):
            for envelope_tuple in combinations(vertices, count):
                envelope = set(envelope_tuple)
                values = restricted_solution(hessian, ppr_load, envelope)
                restricted_ppr = [values.get(vertex, F(0)) for vertex in range(len(degree))]
                delta = max(
                    (rppr[i] for i in vertices if i not in envelope),
                    default=F(0),
                )
                assert all(restricted_ppr[i] <= ppr[i] for i in envelope)
                assert all(
                    F(0) <= ppr[i] - restricted_ppr[i] <= rho + delta for i in range(len(degree))
                )
                if support <= envelope:
                    assert all(rppr[i] <= restricted_ppr[i] for i in envelope)
                checked += 1
    return checked


def normalized_bipartite_system(alpha, rho):
    """Rational Q and loads for a seed in K_4,4 (all square degrees)."""
    adjacency = complete_bipartite(4, 4)
    degree = [4 for _ in adjacency]
    root_degree = [F(2) for _ in adjacency]
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    size = len(adjacency)
    q_matrix = [[F(0) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        q_matrix[i][i] = diagonal
        for j in adjacency[i]:
            q_matrix[i][j] = -coupling / (root_degree[i] * root_degree[j])
    source = [alpha / root_degree[0], *[F(0) for _ in range(size - 1)]]
    load = [source[i] - alpha * rho * root_degree[i] for i in range(size)]
    return degree, root_degree, q_matrix, source, load


def linear_acceleration(q_matrix, load, beta, iterations):
    """Unit-step strongly-convex accelerated-gradient linear scratch."""
    previous = [F(0) for _ in load]
    current = [F(0) for _ in load]
    trace = [current]
    for _ in range(iterations):
        momentum = [current[i] + beta * (current[i] - previous[i]) for i in range(len(load))]
        gradient = [
            sum(q_matrix[i][j] * momentum[j] for j in range(len(load))) - load[i]
            for i in range(len(load))
        ]
        following = [momentum[i] - gradient[i] for i in range(len(load))]
        previous, current = current, following
        trace.append(current)
    return trace


def audit_fixed_envelope_tail():
    alpha, rho, tolerance = F(1, 4), F(1, 16), F(1, 16)
    degree, root_degree, q_matrix, source, load = normalized_bipartite_system(alpha, rho)
    _rppr, support, _ = obstacle_solution(q_matrix, load)
    ppr = solve(q_matrix, source)
    adjacency = complete_bipartite(4, 4)
    assert support == {0}
    envelope = support | boundary(adjacency, support)
    assert len(envelope) == 5 < len(adjacency)
    linear_values = restricted_solution(q_matrix, source, envelope)
    target = [linear_values.get(vertex, F(0)) for vertex in range(len(source))]
    regularization_error = max(abs(target[i] - ppr[i]) / root_degree[i] for i in range(len(target)))
    assert regularization_error <= rho

    sqrt_alpha = F(1, 2)
    beta = (1 - sqrt_alpha) / (1 + sqrt_alpha)
    ids = sorted(envelope)
    restricted_q = [[q_matrix[i][j] for j in ids] for i in ids]
    restricted_source = [source[i] for i in ids]
    restricted_target = [target[i] for i in ids]
    trace = linear_acceleration(restricted_q, restricted_source, beta, 80)
    first_certified = None
    for iteration, vector in enumerate(trace):
        error = max(
            abs(vector[position] - restricted_target[position]) / root_degree[vertex]
            for position, vertex in enumerate(ids)
        )
        if error <= tolerance:
            first_certified = iteration
            break
    assert first_certified is not None
    final = [F(0) for _ in source]
    for position, vertex in enumerate(ids):
        final[vertex] = max(F(0), trace[first_certified][position])
    semantic_error = max(abs(final[i] - ppr[i]) / root_degree[i] for i in range(len(final)))
    assert semantic_error <= rho + tolerance

    gap = quadratic_value(restricted_q, restricted_source, trace[0]) - quadratic_value(
        restricted_q, restricted_source, restricted_target
    )
    assert gap <= alpha / (2 * degree[0])
    return first_certified, regularization_error, semantic_error


def audit_direct_boundary_leakage_certificate():
    """Audit the direct PPR envelope gate without an RPPR support."""
    alpha = F(1, 4)
    degree, root_degree, q_matrix, source, _load = normalized_bipartite_system(alpha, F(0))
    adjacency = complete_bipartite(4, 4)
    ids = [0, 4]
    exact_restricted = solve(
        [[q_matrix[i][j] for j in ids] for i in ids],
        [source[i] for i in ids],
    )
    approximate = [F(3, 4) * value for value in exact_restricted]
    eta = max(
        abs(exact_restricted[position] - approximate[position]) / root_degree[vertex]
        for position, vertex in enumerate(ids)
    )
    coupling = (1 - alpha) / 2
    envelope = set(ids)
    leakage_uppers = []
    for vertex in sorted(boundary(adjacency, envelope)):
        estimate = (
            -sum(
                q_matrix[vertex][inside] * approximate[position]
                for position, inside in enumerate(ids)
            )
            / root_degree[vertex]
        )
        internal_neighbors = len(envelope.intersection(adjacency[vertex]))
        upper = estimate + coupling * F(internal_neighbors, degree[vertex]) * eta
        exact_leakage = (
            -sum(
                q_matrix[vertex][inside] * exact_restricted[position]
                for position, inside in enumerate(ids)
            )
            / root_degree[vertex]
        )
        assert exact_leakage <= upper
        leakage_uppers.append(upper)
    delta = max(leakage_uppers) / alpha

    full = solve(q_matrix, source)
    restricted_padding = [F(0) for _ in full]
    for position, vertex in enumerate(ids):
        restricted_padding[vertex] = exact_restricted[position]
    semantic_error = max(
        (full[i] - restricted_padding[i]) / root_degree[i] for i in range(len(full))
    )
    assert all(F(0) <= restricted_padding[i] <= full[i] for i in range(len(full)))
    assert semantic_error <= delta

    residual = [
        source[position]
        - sum(q_matrix[ids[position]][inside] * approximate[j] for j, inside in enumerate(ids))
        for position in range(len(ids))
    ]
    maximum_semantic_error = max(
        abs(exact_restricted[position] - approximate[position]) / root_degree[vertex]
        for position, vertex in enumerate(ids)
    )
    assert (alpha * maximum_semantic_error) ** 2 <= sum(value**2 for value in residual)

    lower_checkpoint = [F(1, 3) * value for value in exact_restricted]
    checkpoint_residual = [
        source[inside]
        - sum(q_matrix[inside][other] * lower_checkpoint[j] for j, other in enumerate(ids))
        for inside in ids
    ]
    internal_density = max(
        checkpoint_residual[position] / root_degree[vertex] for position, vertex in enumerate(ids)
    )
    principal_error = [
        exact_restricted[position] - lower_checkpoint[position] for position in range(len(ids))
    ]
    assert all(
        F(0) <= principal_error[position] <= internal_density * root_degree[vertex] / alpha
        for position, vertex in enumerate(ids)
    )
    monotone_uppers = []
    for vertex in sorted(boundary(adjacency, envelope)):
        current_density = (
            -sum(
                q_matrix[vertex][inside] * lower_checkpoint[position]
                for position, inside in enumerate(ids)
            )
            / root_degree[vertex]
        )
        internal_neighbors = len(envelope.intersection(adjacency[vertex]))
        monotone_uppers.append(
            current_density
            + coupling * F(internal_neighbors, degree[vertex]) * internal_density / alpha
        )
    assert max(monotone_uppers) / alpha >= semantic_error
    return eta, delta, semantic_error, max(monotone_uppers) / alpha


def audit_gap_to_envelope():
    alpha, rho, delta = F(1, 4), F(1, 16), F(1, 16)
    degree, root_degree, q_matrix, source, load = normalized_bipartite_system(alpha, rho)
    ppr = solve(q_matrix, source)
    optimum, _support, _ = obstacle_solution(q_matrix, load)
    checkpoint = [F(15, 16) * value for value in optimum]
    gap = quadratic_value(q_matrix, load, checkpoint) - quadratic_value(q_matrix, load, optimum)
    assert gap <= alpha * delta * delta / 8
    projected = [
        max(
            F(0),
            checkpoint[i] + load[i] - sum(q_matrix[i][j] * checkpoint[j] for j in range(len(load))),
        )
        for i in range(len(load))
    ]
    mapping_norm_squared = sum((checkpoint[i] - projected[i]) ** 2 for i in range(len(load)))
    assert gap <= mapping_norm_squared / (2 * alpha)
    assert mapping_norm_squared <= (alpha * delta / 2) ** 2
    envelope = {
        i for i in range(len(checkpoint)) if abs(checkpoint[i]) / root_degree[i] > delta / 2
    }
    assert all(
        optimum[i] / root_degree[i] <= delta for i in range(len(optimum)) if i not in envelope
    )
    mass = sum(root_degree[i] * abs(checkpoint[i]) for i in range(len(checkpoint)))
    assert mass <= 1
    assert sum(degree[i] for i in envelope) < 2 / delta
    early_output = [max(F(0), checkpoint[i]) if i in envelope else F(0) for i in range(len(load))]
    early_error = max(abs(early_output[i] - ppr[i]) / root_degree[i] for i in range(len(load)))
    assert early_error <= rho + delta
    return gap, len(envelope), early_error


def audit_interval_face_verifier():
    alpha, rho = F(1, 4), F(1, 16)
    degree, root_degree, q_matrix, _source, load = normalized_bipartite_system(alpha, rho)
    adjacency = complete_bipartite(4, 4)
    active = {0}
    exact = restricted_solution(q_matrix, load, active)[0]
    approximate = F(999, 1000) * exact
    eta = (exact - approximate) / root_degree[0]
    assert approximate - eta * root_degree[0] > 0
    coupling = (1 - alpha) / 2
    for vertex in boundary(adjacency, active):
        approximate_key = load[vertex] - q_matrix[vertex][0] * approximate
        upper = (
            approximate_key
            + coupling
            * F(len(active.intersection(adjacency[vertex])), 1)
            / root_degree[vertex]
            * eta
        )
        exact_key = load[vertex] - q_matrix[vertex][0] * exact
        assert exact_key <= upper <= 0
    optimum, support, _keys = obstacle_solution(q_matrix, load)
    assert support == active
    assert optimum[0] == exact
    return exact, eta


def audit_mass_capped_positive_exposure():
    cases = [
        ("path", path_graph(7), F(1, 4), F(1, 8)),
        ("cycle", cycle_graph(6), F(1, 3), F(1, 9)),
        ("star", star_graph(5), F(1, 4), F(1, 10)),
        ("broom", broom_graph(4, 3), F(1, 5), F(1, 9)),
    ]
    summaries = []
    for name, adjacency, alpha, rho in cases:
        degree, hessian, load = degree_unscaled_system(adjacency, alpha, rho, 0)
        denominator = 2 * sum(range(1, len(degree) + 1))
        mass_weights = [F(i + 1, denominator) for i in range(len(degree))]
        point = [mass_weights[i] / degree[i] for i in range(len(degree))]
        mass = sum(degree[i] * point[i] for i in range(len(degree)))
        assert mass == F(1, 2)
        residual = [
            load[i] - sum(hessian[i][j] * point[j] for j in range(len(degree)))
            for i in range(len(degree))
        ]
        positive_mass = sum(max(F(0), value) for value in residual)
        coupling = (1 - alpha) / 2
        assert positive_mass <= alpha + coupling * mass
        eta = F(1, 50)
        active = {i for i in range(len(degree)) if max(F(0), residual[i]) / degree[i] >= eta}
        assert sum(degree[i] for i in active) <= positive_mass / eta
        for vertex, value in enumerate(residual):
            if value <= 0:
                continue
            bound = (alpha + coupling) / (alpha * rho) if vertex == 0 else coupling / (alpha * rho)
            assert degree[vertex] < bound

        center = [F(1, 3) * value for value in point]
        kappa = F(1, 3)
        shifted = [
            load[i]
            + kappa * degree[i] * center[i]
            - sum(
                (hessian[i][j] + (kappa * degree[i] if i == j else 0)) * point[j]
                for j in range(len(degree))
            )
            for i in range(len(degree))
        ]
        shifted_positive_mass = sum(max(F(0), value) for value in shifted)
        center_mass = sum(degree[i] * center[i] for i in range(len(degree)))
        assert shifted_positive_mass <= alpha + coupling * mass + kappa * center_mass
        summaries.append((name, positive_mass, len(active)))
    return summaries


def audit_priority_sor():
    cases = [
        ("path", path_graph(7), F(1, 4), F(1, 8), F(1, 8)),
        ("cycle", cycle_graph(6), F(1, 3), F(1, 9), F(1, 10)),
        ("star", star_graph(5), F(1, 4), F(1, 10), F(1, 12)),
        ("broom", broom_graph(4, 3), F(1, 5), F(1, 9), F(1, 10)),
    ]
    summaries = []
    for name, adjacency, alpha, rho, delta in cases:
        degree, hessian, load = degree_unscaled_system(adjacency, alpha, rho, 0)
        optimum, support, _ = obstacle_solution(hessian, load)
        diagonal_factor = (1 + alpha) / 2
        vector = [F(0) for _ in load]
        residual = list(load)
        work = 0
        updates = 0
        density_threshold = alpha * delta / 2
        while True:
            maximum_density = max(
                (residual[i] / degree[i] for i in range(len(load)) if residual[i] > 0),
                default=F(0),
            )
            if maximum_density <= density_threshold:
                break
            positive = [i for i in range(len(load)) if residual[i] > 0]
            vertex = max(positive, key=lambda i: residual[i] ** 2 / degree[i] ** 2)
            positive_mass_before = sum(residual[i] for i in positive)
            step = residual[vertex] / (diagonal_factor * degree[vertex])
            vector[vertex] += step
            residual[vertex] = F(0)
            coupling = (1 - alpha) / 2
            for neighbor in adjacency[vertex]:
                residual[neighbor] += coupling * step
            positive_mass_after = sum(max(F(0), value) for value in residual)
            assert positive_mass_after <= positive_mass_before * (
                1 - alpha * rho * degree[vertex] / diagonal_factor
            )
            assert all(F(0) <= vector[i] <= optimum[i] for i in range(len(load)))
            work += degree[vertex]
            updates += 1
        envelope = {i for i in range(len(load)) if vector[i] > delta / 2}
        assert all(optimum[i] - vector[i] <= delta / 2 for i in range(len(load)))
        assert all(optimum[i] <= delta for i in range(len(load)) if i not in envelope)
        assert sum(degree[i] for i in envelope) < 2 / delta
        ppr_load = [alpha if i == 0 else F(0) for i in range(len(load))]
        ppr = solve(hessian, ppr_load)
        early_output = [vector[i] if i in envelope else F(0) for i in range(len(load))]
        assert max(abs(early_output[i] - ppr[i]) for i in range(len(load))) <= rho + delta
        scale = float((1 + alpha) / (2 * alpha * rho))
        logarithm = 1 + log(max(1.0, float(2 / delta)))
        exponential_bound = scale * logarithm
        additive_bound = float((1 + alpha) / (alpha * delta))
        assert work <= ceil(min(exponential_bound, additive_bound))
        assert {i for i, value in enumerate(residual) if value > 0} <= support
        summaries.append((name, updates, work, len(envelope)))
    return summaries


def audit_direct_ppr_priority():
    cases = [
        ("path", path_graph(7), F(1, 4), F(1, 8)),
        ("cycle", cycle_graph(6), F(1, 3), F(1, 10)),
        ("star", star_graph(5), F(1, 4), F(1, 12)),
        ("broom", broom_graph(4, 3), F(1, 5), F(1, 10)),
    ]
    summaries = []
    for name, adjacency, alpha, epsilon in cases:
        degree, hessian, load = degree_unscaled_system(adjacency, alpha, F(0), 0)
        optimum = solve(hessian, load)
        diagonal_factor = (1 + alpha) / 2
        coupling = (1 - alpha) / 2
        vector = [F(0) for _ in load]
        residual = list(load)
        work = updates = 0
        while (
            max(
                (residual[i] / degree[i] for i in range(len(load)) if residual[i] > 0),
                default=F(0),
            )
            > alpha * epsilon
        ):
            vertex = max(
                (i for i in range(len(load)) if residual[i] > 0),
                key=lambda i: residual[i] / degree[i],
            )
            step = residual[vertex] / (diagonal_factor * degree[vertex])
            vector[vertex] += step
            residual[vertex] = F(0)
            for neighbor in adjacency[vertex]:
                residual[neighbor] += coupling * step
            work += degree[vertex]
            updates += 1
        assert all(F(0) <= optimum[i] - vector[i] <= epsilon for i in range(len(load)))
        assert work < diagonal_factor / (alpha * epsilon)
        summaries.append((name, updates, work))
    return summaries


def audit_green_ball_screen():
    alpha = F(1, 4)
    delta = F(1, 16)
    contraction = F(1, 3)
    radius = 0
    while 2 * contraction**radius > delta:
        radius += 1
    assert radius == 4
    summaries = []
    for name, adjacency in (("path", path_graph(12)), ("cycle", cycle_graph(14))):
        degree, hessian, load = degree_unscaled_system(adjacency, alpha, F(0), 0)
        ppr = solve(hessian, load)
        distance = [None for _ in adjacency]
        distance[0] = 0
        queue = [0]
        for vertex in queue:
            for neighbor in adjacency[vertex]:
                if distance[neighbor] is None:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        envelope = {i for i, value in enumerate(distance) if value < radius}
        assert all(ppr[i] <= delta for i in range(len(ppr)) if i not in envelope)
        values = restricted_solution(hessian, load, envelope)
        output = [values.get(i, F(0)) for i in range(len(load))]
        assert all(F(0) <= ppr[i] - output[i] <= delta for i in range(len(load)))
        summaries.append((name, len(envelope), sum(degree[i] for i in envelope)))
    return summaries


def tree_leaf_solve(adjacency, matrix, rhs, root=0):
    """Exact no-fill leaf elimination and back substitution on a tree."""
    parent = [-1 for _ in adjacency]
    order = [root]
    for vertex in order:
        for neighbor in adjacency[vertex]:
            if neighbor == parent[vertex]:
                continue
            assert parent[neighbor] == -1
            parent[neighbor] = vertex
            order.append(neighbor)
    assert len(order) == len(adjacency)
    diagonal = [matrix[i][i] for i in range(len(adjacency))]
    reduced_rhs = list(rhs)
    for vertex in reversed(order[1:]):
        ancestor = parent[vertex]
        coupling = matrix[ancestor][vertex]
        reduced_rhs[ancestor] -= coupling * reduced_rhs[vertex] / diagonal[vertex]
        diagonal[ancestor] -= coupling * coupling / diagonal[vertex]
        assert diagonal[ancestor] > 0
    solution = [F(0) for _ in adjacency]
    solution[root] = reduced_rhs[root] / diagonal[root]
    for vertex in order[1:]:
        ancestor = parent[vertex]
        solution[vertex] = (
            reduced_rhs[vertex] - matrix[vertex][ancestor] * solution[ancestor]
        ) / diagonal[vertex]
    return solution


def tridiagonal_solve(lower, diagonal, upper, rhs):
    reduced_diagonal = list(diagonal)
    reduced_rhs = list(rhs)
    for index in range(1, len(diagonal)):
        multiplier = lower[index - 1] / reduced_diagonal[index - 1]
        reduced_diagonal[index] -= multiplier * upper[index - 1]
        reduced_rhs[index] -= multiplier * reduced_rhs[index - 1]
        assert reduced_diagonal[index] > 0
    output = [F(0) for _ in diagonal]
    output[-1] = reduced_rhs[-1] / reduced_diagonal[-1]
    for index in range(len(diagonal) - 2, -1, -1):
        output[index] = (reduced_rhs[index] - upper[index] * output[index + 1]) / reduced_diagonal[
            index
        ]
    return output


def cyclic_tridiagonal_solve(matrix, rhs):
    size = len(matrix)
    diagonal = [matrix[i][i] for i in range(size)]
    lower = [matrix[i + 1][i] for i in range(size - 1)]
    upper = [matrix[i][i + 1] for i in range(size - 1)]
    alpha_corner = matrix[0][-1]
    beta_corner = matrix[-1][0]
    gamma = -diagonal[0]
    modified = list(diagonal)
    modified[0] -= gamma
    modified[-1] -= alpha_corner * beta_corner / gamma
    first = tridiagonal_solve(lower, modified, upper, rhs)
    correction_rhs = [F(0) for _ in rhs]
    correction_rhs[0] = gamma
    correction_rhs[-1] = alpha_corner
    correction = tridiagonal_solve(lower, modified, upper, correction_rhs)
    factor = (first[0] + beta_corner * first[-1] / gamma) / (
        1 + correction[0] + beta_corner * correction[-1] / gamma
    )
    return [first[i] - factor * correction[i] for i in range(size)]


def audit_tree_structural_tail():
    summaries = []
    for name, adjacency in (
        ("path", path_graph(9)),
        ("star", star_graph(8)),
        ("broom", broom_graph(5, 4)),
    ):
        _degree, hessian, load = degree_unscaled_system(adjacency, F(1, 7), F(0), 0)
        reference = solve(hessian, load)
        leaf_solution = tree_leaf_solve(adjacency, hessian, load)
        assert leaf_solution == reference
        assert all(value > 0 for value in leaf_solution)
        summaries.append((name, len(adjacency), sum(len(row) for row in adjacency)))
    adjacency = cycle_graph(9)
    _degree, hessian, load = degree_unscaled_system(adjacency, F(1, 7), F(0), 0)
    cycle_solution = cyclic_tridiagonal_solve(hessian, load)
    assert cycle_solution == solve(hessian, load)
    assert all(value > 0 for value in cycle_solution)
    summaries.append(("cycle", len(adjacency), sum(len(row) for row in adjacency)))
    return summaries


def audit_mass_completion_handoff():
    alpha, epsilon = F(1, 4), F(1, 128)
    degree, root_degree, q_matrix, source, _load = normalized_bipartite_system(alpha, F(0))
    optimum = solve(q_matrix, source)
    diagonal = (1 + alpha) / 2
    vector = [F(0) for _ in source]
    residual = list(source)

    # One safe prefix update provides a nontrivial handoff checkpoint.
    step = residual[0] / diagonal
    vector[0] += step
    residual = [residual[i] - q_matrix[i][0] * step for i in range(len(residual))]
    assert all(value >= 0 for value in residual)
    mass_deficit = 1 - sum(root_degree[i] * vector[i] for i in range(len(vector)))
    weighted_residual_mass = sum(root_degree[i] * residual[i] for i in range(len(residual)))
    assert weighted_residual_mass == alpha * mass_deficit

    cleanup_work = 0
    while (
        max(
            (residual[i] / root_degree[i] for i in range(len(residual))),
            default=F(0),
        )
        > alpha * epsilon
    ):
        vertex = max(range(len(residual)), key=lambda i: residual[i] / root_degree[i])
        step = residual[vertex] / diagonal
        vector[vertex] += step
        residual = [residual[i] - q_matrix[i][vertex] * step for i in range(len(residual))]
        assert all(value >= 0 for value in residual)
        cleanup_work += degree[vertex]
    assert cleanup_work < diagonal * mass_deficit / (alpha * epsilon)
    assert max((optimum[i] - vector[i]) / root_degree[i] for i in range(len(vector))) <= epsilon
    return mass_deficit, cleanup_work


def audit_mass_capturing_retraction():
    """Audit the signed-scratch lower retraction used by the AESP--APPR lane."""
    alpha = F(1, 4)
    degree, root_degree, q_matrix, source, _load = normalized_bipartite_system(alpha, F(0))
    envelope = {0, 1, 4, 5}
    ids = sorted(envelope)
    restricted_q = [[q_matrix[i][j] for j in ids] for i in ids]
    restricted_source = [source[i] for i in ids]
    restricted_solution_vector = solve(restricted_q, restricted_source)
    volume = sum(degree[i] for i in ids)
    assert volume == 16
    assert all(value > 0 for value in restricted_solution_vector)

    # A deliberately signed raw approximation exercises both the shift and
    # positive-part publication, rather than merely auditing the exact solve.
    perturbation = [F(1, 400), -F(1, 500), F(1, 600), -F(1, 700)]
    raw = [restricted_solution_vector[i] + perturbation[i] for i in range(len(ids))]
    residual = [
        restricted_source[i] - sum(restricted_q[i][j] * raw[j] for j in range(len(ids)))
        for i in range(len(ids))
    ]
    restricted_v = [root_degree[i] for i in ids]
    assert all(
        sum(restricted_q[i][j] * restricted_v[j] for j in range(len(ids)))
        >= alpha * restricted_v[i]
        for i in range(len(ids))
    )
    shift = max([F(0)] + [-residual[i] / (alpha * restricted_v[i]) for i in range(len(ids))])
    published_restricted = [max(F(0), raw[i] - shift * restricted_v[i]) for i in range(len(ids))]
    published = [F(0) for _ in source]
    for position, vertex in enumerate(ids):
        published[vertex] = published_restricted[position]

    global_residual = [
        source[i] - sum(q_matrix[i][j] * published[j] for j in range(len(source)))
        for i in range(len(source))
    ]
    assert all(value >= 0 for value in global_residual)
    assert all(
        F(0) <= published_restricted[i] <= restricted_solution_vector[i] for i in range(len(ids))
    )

    residual_norm_squared = sum(value * value for value in residual)
    error_norm_squared = sum(
        (restricted_solution_vector[i] - published_restricted[i]) ** 2 for i in range(len(ids))
    )
    # Here sqrt(vol(E))=4, so the theorem's Euclidean error bar is rational.
    error_factor = F(1 + 4, 1) / alpha
    assert error_norm_squared <= error_factor**2 * residual_norm_squared

    restricted_mass = sum(restricted_v[i] * restricted_solution_vector[i] for i in range(len(ids)))
    published_mass = sum(root_degree[i] * published[i] for i in range(len(published)))
    assert F(0) <= published_mass <= restricted_mass <= 1
    return shift, restricted_mass, published_mass


def audit_rooted_ball_mass():
    alpha = F(1, 4)
    _degree, root_degree, q_matrix, source, _load = normalized_bipartite_system(alpha, F(0))
    contraction = (1 - alpha) / (1 + alpha)
    assert contraction == F(3, 5)
    summaries = []
    for radius, envelope in ((0, {0}), (1, set(range(8)))):
        ids = sorted(envelope)
        values = solve(
            [[q_matrix[i][j] for j in ids] for i in ids],
            [source[i] for i in ids],
        )
        mass = sum(root_degree[vertex] * values[position] for position, vertex in enumerate(ids))
        deficit = 1 - mass
        assert F(0) <= deficit <= contraction ** (radius + 1)
        summaries.append((radius, deficit, contraction ** (radius + 1)))
    assert summaries[0][1] == summaries[0][2]
    return summaries


def audit_mass_attempt_interval():
    alpha = F(1, 4)
    _degree, root_degree, q_matrix, source, _load = normalized_bipartite_system(alpha, F(0))
    ids = [0, 1, 4, 5]
    restricted_q = [[q_matrix[i][j] for j in ids] for i in ids]
    restricted_source = [source[i] for i in ids]
    exact = solve(restricted_q, restricted_source)
    checkpoint = [F(1, 3) * value for value in exact]
    residual = [
        restricted_source[i] - sum(restricted_q[i][j] * checkpoint[j] for j in range(len(ids)))
        for i in range(len(ids))
    ]
    mass = sum(root_degree[ids[i]] * checkpoint[i] for i in range(len(ids)))
    residual_mass = sum(root_degree[ids[i]] * residual[i] for i in range(len(ids)))
    exact_mass = sum(root_degree[ids[i]] * exact[i] for i in range(len(ids)))
    q_values = [
        sum(restricted_q[i][j] * root_degree[ids[j]] for j in range(len(ids))) / root_degree[ids[i]]
        for i in range(len(ids))
    ]
    lower = mass + residual_mass / max(q_values)
    upper = mass + residual_mass / min(q_values)
    assert lower <= exact_mass <= upper
    return lower, exact_mass, upper


def audit_star_mass_barrier():
    alpha = F(1, 16)
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    leaves = 128
    target_deficit = F(1, 8)

    def deficit(retained_leaves):
        return (
            diagonal
            * coupling
            * (leaves - retained_leaves)
            / (diagonal**2 * leaves - coupling**2 * retained_leaves)
        )

    minimum = next(
        retained for retained in range(leaves + 1) if deficit(retained) <= target_deficit
    )
    assert minimum == 124
    assert deficit(minimum) == F(255, 2273)
    assert deficit(minimum - 1) == F(1275, 9317) > target_deficit
    epsilon = F(1, 64)
    assert max(diagonal / leaves, coupling / leaves) <= epsilon
    assert leaves + minimum > 2 / epsilon
    return minimum, deficit(minimum), diagonal / leaves


def audit_star_two_krylov_iterations():
    """The source-centered full-star solve has Krylov dimension two."""
    alpha = F(1, 16)
    leaves = 7
    adjacency = star_graph(leaves)
    _degree, hessian, load = degree_unscaled_system(adjacency, alpha, F(0), 0)
    exact = solve(hessian, load)
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    assert exact[0] == diagonal / leaves
    assert all(value == coupling / leaves for value in exact[1:])

    first = list(load)
    second = [sum(hessian[i][j] * first[j] for j in range(len(first))) for i in range(len(first))]
    coefficient_first = diagonal * (1 + F(1, leaves)) / alpha
    coefficient_second = -F(1, alpha * leaves)
    reconstructed = [
        coefficient_first * first[i] + coefficient_second * second[i] for i in range(len(first))
    ]
    assert reconstructed == exact

    third = [sum(hessian[i][j] * second[j] for j in range(len(first))) for i in range(len(first))]
    # The third Krylov vector is already in span{b,Hb}; equivalently the
    # source-visible minimal polynomial has degree at most two.
    coefficients = solve(
        [[first[0], second[0]], [first[1], second[1]]],
        [third[0], third[1]],
    )
    assert all(
        third[i] == coefficients[0] * first[i] + coefficients[1] * second[i]
        for i in range(len(first))
    )
    return leaves, coefficients


def audit_fair_scheduler():
    required = [17, 29, 5]
    consumed = [0, 0, 0]
    total = 0
    winner = None
    while winner is None:
        for engine in range(len(required)):
            consumed[engine] += 1
            total += 1
            if consumed[engine] == required[engine]:
                winner = engine
                break
    assert winner == 2
    assert total <= len(required) * min(required)
    return total


def audit_two_lane_screen_race():
    """A failed screen and a successful screen both obey the factor-two race."""
    summaries = []
    for direct_work, screen_work, screen_succeeds in (
        (17, 5, True),
        (17, 7, False),
        (3, 7, False),
    ):
        direct = screen = total = 0
        screen_live = True
        winner = None
        while winner is None:
            direct += 1
            total += 1
            if direct == direct_work:
                winner = "direct"
                break
            if screen_live:
                screen += 1
                total += 1
                if screen == screen_work:
                    if screen_succeeds:
                        winner = "screen"
                        break
                    screen_live = False
        if screen_succeeds:
            assert total <= 2 * min(direct_work, screen_work)
        else:
            assert winner == "direct"
            assert total <= 2 * direct_work
        summaries.append((direct_work, screen_work, screen_succeeds, total))
    return summaries


def audit_exact_rppr_warm_start():
    """Check the structured residual and energy bound for the second RHS."""
    alpha, rho = F(1, 2), F(1, 8)
    q_matrix = [[F(3, 4), -F(1, 4)], [-F(1, 4), F(3, 4)]]
    ppr_source = [alpha, F(0)]
    rppr_source = [value - alpha * rho for value in ppr_source]
    rppr = solve(q_matrix, rppr_source)
    ppr = solve(q_matrix, ppr_source)
    assert rppr == [F(5, 8), F(1, 8)]
    residual = [ppr_source[i] - sum(q_matrix[i][j] * rppr[j] for j in range(2)) for i in range(2)]
    assert residual == [alpha * rho, alpha * rho]
    correction = [ppr[i] - rppr[i] for i in range(2)]
    assert correction == solve(q_matrix, residual)
    assert all(value >= 0 for value in correction)
    energy_gap = sum(residual[i] * correction[i] for i in range(2)) / 2
    volume = F(2)
    assert energy_gap <= alpha * rho * rho * volume / 2
    assert energy_gap <= alpha * rho / 2
    return residual, correction, energy_gap


def audit_source_guards():
    text = "\n".join(path.read_text() for path in SOURCE.rglob("*.tex"))
    for label in (
        "prop:two-stage-sparse-source-superposition",
        "lem:two-stage-point-source-connected",
        "prop:two-stage-envelope-linearization",
        "def:two-stage-leakage-certificate",
        "prop:two-stage-leakage-certificate",
        "cor:two-stage-monotone-leakage-screen",
        "cor:two-stage-leakage-composition",
        "prop:two-stage-gap-to-envelope",
        "prop:two-stage-interval-face-verifier",
        "thm:two-stage-appr-face-race",
        "cor:two-stage-sor-support-then-solve",
        "prop:two-stage-exact-batch-refit",
        "prop:two-stage-mass-cap-positive-exposure",
        "cor:two-stage-numerical-handoff-returns",
        "cor:two-stage-direct-priority-ppr",
        "thm:two-stage-screen-or-solve",
        "cor:two-stage-exact-tail-full-budget",
        "cor:two-stage-factor-reuse",
        "cor:two-stage-rppr-warm-start",
        "thm:two-stage-green-ball-screen",
        "cor:two-stage-green-structural-tail",
        "thm:short-green-cg",
        "cor:short-green-structural",
        "thm:short-appr-face-race",
        "thm:short-tree-exact-support",
        "lem:strict-linearization",
        "thm:strict-composition",
        "prop:two-stage-aesp-appr-mass-handoff",
        "thm:two-stage-mass-capturing-envelope",
        "prop:two-stage-mass-attempt-screen",
        "thm:two-stage-rooted-ball-mass",
        "thm:two-stage-hard-capped-mass-screen",
        "prop:two-stage-star-two-krylov",
        "prop:two-stage-star-mass-barrier",
        "thm:two-stage-priority-sor-discovery",
        "thm:two-stage-composition",
        "thm:two-stage-certificate-race",
        "prob:two-stage-general-discovery",
    ):
        assert f"\\label{{{label}}}" in text


def main():
    summaries = audit_obstacle_interfaces()
    batch_refit_summaries = audit_exact_positive_boundary_batches()
    superposition_summary = audit_linear_sparse_source_superposition()
    multisource_summary = audit_multisource_obstruction()
    approximate_envelopes = audit_every_approximate_envelope()
    tail_iteration, regularization_error, semantic_error = audit_fixed_envelope_tail()
    leakage_summary = audit_direct_boundary_leakage_certificate()
    certified_gap, threshold_envelope_size, gap_early_error = audit_gap_to_envelope()
    face_verifier_summary = audit_interval_face_verifier()
    mass_cap_summaries = audit_mass_capped_positive_exposure()
    priority_summaries = audit_priority_sor()
    direct_priority_summaries = audit_direct_ppr_priority()
    green_ball_summaries = audit_green_ball_screen()
    structural_tail_summaries = audit_tree_structural_tail()
    mass_handoff_summary = audit_mass_completion_handoff()
    mass_retraction_summary = audit_mass_capturing_retraction()
    mass_interval_summary = audit_mass_attempt_interval()
    rooted_ball_summary = audit_rooted_ball_mass()
    star_krylov_summary = audit_star_two_krylov_iterations()
    star_mass_barrier_summary = audit_star_mass_barrier()
    scheduler_work = audit_fair_scheduler()
    two_lane_race = audit_two_lane_screen_race()
    warm_start_summary = audit_exact_rppr_warm_start()
    audit_source_guards()
    print("two-stage point-source composition audit: PASS")
    print("  obstacle cases:", summaries)
    print("  exact positive-boundary batches:", batch_refit_summaries)
    print("  linear sparse-source superposition:", superposition_summary)
    print("  multisource separate/joint middle keys:", multisource_summary)
    print("  approximate envelopes checked:", approximate_envelopes)
    print("  fixed-envelope certified iteration:", tail_iteration)
    print("  exact envelope-linearization error:", regularization_error)
    print("  exact semantic error:", semantic_error)
    print("  direct leakage gate (error bar, budget, true error):", leakage_summary)
    print(
        "  certified gap / threshold-envelope size / early error:",
        certified_gap,
        threshold_envelope_size,
        gap_early_error,
    )
    print("  interval exact-face verifier (value, error bar):", face_verifier_summary)
    print("  mass-cap positive exposure cases:", mass_cap_summaries)
    print("  priority-SOR cases (name, updates, work, envelope size):", priority_summaries)
    print("  direct priority-PPR cases (name, updates, work):", direct_priority_summaries)
    print("  hard-capped Green-ball cases (name, size, volume):", green_ball_summaries)
    print("  exact tree leaf-elimination tails:", structural_tail_summaries)
    print("  AESP-to-APPR mass handoff (deficit, cleanup work):", mass_handoff_summary)
    print(
        "  mass-capturing retraction (shift, restricted mass, published mass):",
        mass_retraction_summary,
    )
    print("  mass-attempt interval (lower, exact, upper):", mass_interval_summary)
    print("  rooted-ball mass bounds (radius, deficit, bound):", rooted_ball_summary)
    print("  star source-visible Krylov dimension audit:", star_krylov_summary)
    print(
        "  star mass barrier (minimum leaves, deficit, zero-output error):",
        star_mass_barrier_summary,
    )
    print("  fair-race work:", scheduler_work)
    print("  Green/APPR two-lane race:", two_lane_race)
    print("  exact RPPR warm residual/correction/gap:", warm_start_summary)


if __name__ == "__main__":
    main()
