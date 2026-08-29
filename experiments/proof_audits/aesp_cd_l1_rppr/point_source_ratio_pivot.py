#!/usr/bin/env python3
"""Exact point-source ratio-pivot homotopy versus exhaustive obstacle KKT."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from random import Random

from experiments.proof_audits import note_tex_source


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    size = len(rhs)
    work = [row[:] + [value] for row, value in zip(matrix, rhs, strict=True)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        diagonal = work[column][column]
        work[column] = [entry / diagonal for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column], strict=True)
            ]
    return [row[-1] for row in work]


def obstacle_support(hessian: list[list[F]], load: list[F]) -> set[int]:
    size = len(load)
    for support_size in range(size + 1):
        for support_tuple in combinations(range(size), support_size):
            support = set(support_tuple)
            point = [F(0)] * size
            if support:
                indices = sorted(support)
                values = solve(
                    [[hessian[i][j] for j in indices] for i in indices],
                    [load[i] for i in indices],
                )
                if any(value <= 0 for value in values):
                    continue
                for index, value in zip(indices, values, strict=True):
                    point[index] = value
            key = [
                load[i] - sum(hessian[i][j] * point[j] for j in range(size))
                for i in range(size)
            ]
            if all(key[i] == 0 for i in support) and all(
                key[i] <= 0 for i in range(size) if i not in support
            ):
                return support
    raise AssertionError("obstacle support not found")


def obstacle_point(
    hessian: list[list[F]], load: list[F], support: set[int]
) -> list[F]:
    point = [F(0)] * len(load)
    if support:
        indices = sorted(support)
        values = solve(
            [[hessian[i][j] for j in indices] for i in indices],
            [load[i] for i in indices],
        )
        for index, value in zip(indices, values, strict=True):
            point[index] = value
    return point


def appr_support(
    adjacency: list[list[F]],
    degree: list[int],
    alpha: F,
    rho: F,
    source: list[F] | None = None,
) -> tuple[set[int], int]:
    """Run exact lazy APPR with the smallest active label."""
    size = len(degree)
    coupling = (1 - alpha) / 2
    settled = [F(0)] * size
    residual = source[:] if source is not None else [F(i == 0) for i in range(size)]
    assert len(residual) == size and all(value >= 0 for value in residual)
    assert sum(residual, F(0)) == 1
    pushes = 0
    while True:
        active = [i for i in range(size) if residual[i] >= rho * degree[i]]
        if not active:
            return {i for i, value in enumerate(settled) if value > 0}, pushes
        vertex = min(active)
        mass = residual[vertex]
        settled[vertex] += alpha * mass
        residual[vertex] = coupling * mass
        for neighbor in range(size):
            if adjacency[vertex][neighbor]:
                residual[neighbor] += coupling * mass / degree[vertex]
        pushes += 1
        assert sum(settled, F(0)) + sum(residual, F(0)) == 1
        assert pushes < 100_000


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    size = len(matrix)
    columns = [
        solve(matrix, [F(i == column) for i in range(size)])
        for column in range(size)
    ]
    return [[columns[column][row] for column in range(size)] for row in range(size)]


def audit_harmonic_exit(
    hessian: list[list[F]],
    adjacency: list[list[F]],
    degree: list[int],
    alpha: F,
    eliminated: list[int],
) -> None:
    size = len(degree)
    exterior = [vertex for vertex in range(size) if vertex not in eliminated]
    if not eliminated or not exterior:
        return
    p, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    transition = [
        [
            coupling * adjacency[i][j] / (p * degree[i])
            for j in range(size)
        ]
        for i in range(size)
    ]
    interior_kernel = [
        [F(i == j) - transition[i][j] for j in eliminated]
        for i in eliminated
    ]
    green = inverse(interior_kernel)
    trace = [[transition[u][v] for v in exterior] for u in exterior]
    for iu, u in enumerate(exterior):
        for iv, v in enumerate(exterior):
            trace[iu][iv] += sum(
                transition[u][a]
                * green[ia][ib]
                * transition[b][v]
                for ia, a in enumerate(eliminated)
                for ib, b in enumerate(eliminated)
            )

    h_ss = [[hessian[i][j] for j in eliminated] for i in eliminated]
    h_ss_inv = inverse(h_ss)
    schur = [[hessian[u][v] for v in exterior] for u in exterior]
    for iu, u in enumerate(exterior):
        for iv, v in enumerate(exterior):
            schur[iu][iv] -= sum(
                hessian[u][a]
                * h_ss_inv[ia][ib]
                * hessian[b][v]
                for ia, a in enumerate(eliminated)
                for ib, b in enumerate(eliminated)
            )
            expected = p * degree[u] * (F(iu == iv) - trace[iu][iv])
            assert schur[iu][iv] == expected

    for iw in range(len(exterior)):
        denominator = 1 - trace[iw][iw]
        gamma = [
            -schur[iv][iw] / schur[iw][iw]
            for iv in range(len(exterior))
            if iv != iw
        ]
        trace_exit = [
            trace[iw][iv] / denominator
            for iv in range(len(exterior))
            if iv != iw
        ]
        assert gamma == trace_exit
        assert sum(gamma, F(0)) <= coupling / p


def audit_hitting_column(
    hessian: list[list[F]],
    adjacency: list[list[F]],
    degree: list[int],
    alpha: F,
    active: list[int],
    rng: Random,
) -> int:
    """Audit the exact block response and its killed-hitting equations."""
    size = len(degree)
    exterior = [vertex for vertex in range(size) if vertex not in active]
    if not active or not exterior:
        return 0
    p, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    transition = [
        [
            coupling * adjacency[i][j] / (p * degree[i])
            for j in range(size)
        ]
        for i in range(size)
    ]
    h_ss = [[hessian[i][j] for j in active] for i in active]
    killed_green = inverse(
        [
            [F(i == j) - transition[i][j] for j in active]
            for i in active
        ]
    )
    audited = 0
    for w in exterior:
        rhs = [-hessian[i][w] for i in active]
        hitting = solve(h_ss, rhs)
        assert all(0 <= value <= 1 for value in hitting)
        for row, i in enumerate(active):
            expected = transition[i][w] + sum(
                transition[i][j] * hitting[column]
                for column, j in enumerate(active)
            )
            assert hitting[row] == expected

        occupation = [
            sum(
                transition[w][j] * killed_green[column][row]
                for column, j in enumerate(active)
            )
            for row, i in enumerate(active)
        ]
        assert all(
            occupation[row] == F(degree[i], degree[w]) * hitting[row]
            for row, i in enumerate(active)
        )
        assert sum(occupation, F(0)) <= coupling / alpha

        cut_flux = sum(
            hitting[row]
            for row, i in enumerate(active)
            for v in exterior
            if adjacency[i][v]
        )
        edge_count = sum(adjacency[i][w] for i in active)
        assert (
            alpha
            * sum(
                degree[i] * hitting[row] for row, i in enumerate(active)
            )
            + coupling * cut_flux
            == coupling * edge_count
        )

        # Force a positive synthetic pivot residual and compare the enlarged
        # restricted solve against y'=(y+h*Delta, Delta).
        old_load = [F(rng.randrange(-3, 6), 11) for _ in active]
        old_point = solve(h_ss, old_load)
        delta = F(1 + rng.randrange(5), 13)
        enlarged = active + [w]
        target = [
            old_point[row] + hitting[row] * delta
            for row in range(len(active))
        ] + [delta]
        enlarged_load = [
            sum(hessian[i][j] * target[column] for column, j in enumerate(enlarged))
            for i in enlarged
        ]
        direct = solve(
            [[hessian[i][j] for j in enlarged] for i in enlarged],
            enlarged_load,
        )
        assert direct == target
        old_extended_load = old_load + [enlarged_load[-1]]
        residual = old_extended_load[-1] - sum(
            hessian[w][j] * old_point[column]
            for column, j in enumerate(active)
        )
        schur_pivot = hessian[w][w] - sum(
            hessian[w][i]
            * solve(h_ss, [hessian[j][w] for j in active])[row]
            for row, i in enumerate(active)
        )
        assert residual == schur_pivot * delta > 0
        audited += 1
    return audited


def graph_distances(
    adjacency: list[list[F]], allowed: set[int], source: int
) -> dict[int, int]:
    distance = {source: 0}
    frontier = [source]
    while frontier:
        vertex = frontier.pop(0)
        for neighbor in allowed:
            if adjacency[vertex][neighbor] and neighbor not in distance:
                distance[neighbor] = distance[vertex] + 1
                frontier.append(neighbor)
    return distance


def source_distances(
    adjacency: list[list[F]], sources: set[int]
) -> dict[int, int]:
    distance = {source: 0 for source in sources}
    frontier = sorted(sources)
    while frontier:
        vertex = frontier.pop(0)
        for neighbor, edge in enumerate(adjacency[vertex]):
            if edge and neighbor not in distance:
                distance[neighbor] = distance[vertex] + 1
                frontier.append(neighbor)
    return distance


def support_components(
    adjacency: list[list[F]], support: set[int]
) -> list[set[int]]:
    unseen = set(support)
    components: list[set[int]] = []
    while unseen:
        seed = min(unseen)
        component = {seed}
        frontier = [seed]
        unseen.remove(seed)
        while frontier:
            vertex = frontier.pop()
            for neighbor in tuple(unseen):
                if adjacency[vertex][neighbor]:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    frontier.append(neighbor)
        components.append(component)
    return components


def audit_separated_source_decomposition() -> None:
    """Exact P5 witness for the scaled point-source RPPR decomposition."""
    size = 5
    adjacency = [
        [F(abs(i - j) == 1) for j in range(size)] for i in range(size)
    ]
    degree = [1, 2, 2, 2, 1]
    alpha, rho = F(1, 5), F(3, 20)
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    hessian = [
        [
            diagonal * degree[i]
            if i == j
            else -coupling * adjacency[i][j]
            for j in range(size)
        ]
        for i in range(size)
    ]
    weight = F(1, 2)
    point_threshold = rho / weight
    point_candidates: list[list[F]] = []
    point_supports: list[set[int]] = []
    for source in (0, 4):
        load = [
            alpha * (F(i == source) - point_threshold * degree[i])
            for i in range(size)
        ]
        support = obstacle_support(hessian, load)
        assert support == {source}
        point_supports.append(support)
        point_candidates.append(obstacle_point(hessian, load, support))
    assert {0, 1}.isdisjoint({3, 4})

    combined = [
        weight * (point_candidates[0][i] + point_candidates[1][i])
        for i in range(size)
    ]
    sparse_source = [weight, F(0), F(0), F(0), weight]
    general_load = [
        alpha * (sparse_source[i] - rho * degree[i]) for i in range(size)
    ]
    general_support = obstacle_support(hessian, general_load)
    general_point = obstacle_point(hessian, general_load, general_support)
    assert general_support == point_supports[0] | point_supports[1] == {0, 4}
    assert combined == general_point
    assert sum(degree[i] for i in general_support) <= 1 / rho


def audit_response_residual_certificate(
    hessian: list[list[F]],
    degree: list[int],
    alpha: F,
    active: list[int],
    rng: Random,
) -> int:
    """Audit alpha^2 d_i e_i^2 <= ||D^-1/2 H e||_2^2 exactly."""
    if not active:
        return 0
    error = [F(rng.randrange(-5, 6), 17) for _ in active]
    residual = [
        sum(
            hessian[i][j] * error[column]
            for column, j in enumerate(active)
        )
        for i in active
    ]
    dual_norm_squared = sum(
        residual[row] ** 2 / degree[i]
        for row, i in enumerate(active)
    )
    for row, i in enumerate(active):
        assert alpha**2 * degree[i] * error[row] ** 2 <= dual_norm_squared
    return len(active)


def audit_hitting_radius(
    hessian: list[list[F]],
    adjacency: list[list[F]],
    degree: list[int],
    alpha: F,
    active: list[int],
) -> int:
    """Audit the rational Chebyshev tail when sqrt(alpha)=1/3."""
    if alpha != F(1, 9):
        return 0
    lam = F(1, 2)
    exterior = [vertex for vertex in range(len(degree)) if vertex not in active]
    if not active or not exterior:
        return 0
    h_ss = [[hessian[i][j] for j in active] for i in active]
    checked = 0
    for w in exterior:
        hitting = solve(h_ss, [-hessian[i][w] for i in active])
        distance = graph_distances(adjacency, set(active) | {w}, w)
        delta = F(1, 2 * degree[w])
        for row, i in enumerate(active):
            radius = distance.get(i)
            if radius is None or radius < 2:
                continue
            normalized_square = hitting[row] ** 2 * F(degree[i], degree[w])
            chebyshev_square = F(4, alpha**2) * lam ** (2 * (radius - 1))
            assert normalized_square <= chebyshev_square
            event_square = (delta * hitting[row]) ** 2
            event_bound_square = (
                F(4, alpha**2 * degree[i] * degree[w])
                * lam ** (2 * (radius - 1))
            )
            assert event_square <= event_bound_square
            checked += 1
    return checked


def audit_frontier_universe(
    adjacency: list[list[F]], degree: list[int], support: set[int], order: list[int]
) -> int:
    if not support:
        return 0
    active = {0}
    seen_frontier: set[int] = set()
    for vertex in [*order, -1]:
        seen_frontier.update(
            v
            for v in range(len(degree))
            if v not in active and any(adjacency[v][u] for u in active)
        )
        if vertex >= 0:
            assert vertex in support
            active.add(vertex)
    final_boundary = {
        v
        for v in range(len(degree))
        if v not in support and any(adjacency[v][u] for u in support)
    }
    assert seen_frontier <= support | final_boundary
    cut_edges = sum(
        adjacency[u][v] for u in support for v in range(len(degree)) if v not in support
    )
    assert len(final_boundary) <= cut_edges
    assert len(support | final_boundary) <= 2 * sum(degree[u] for u in support)
    return len(seen_frontier)


def audit_orthogonal_pivots(
    hessian: list[list[F]],
    load: list[F],
    degree: list[int],
    alpha: F,
    support: set[int],
    events: list[tuple[int, F]],
) -> int:
    size = len(load)
    active: set[int] = set()
    old_point = [F(0)] * size
    increments: list[list[F]] = []
    energies: list[F] = []
    for winner, residual in [(0, load[0]), *events] if support else []:
        active.add(winner)
        new_point = obstacle_point(hessian, load, active)
        increment = [new_point[i] - old_point[i] for i in range(size)]
        energy = sum(
            increment[i] * hessian[i][j] * increment[j]
            for i in range(size)
            for j in range(size)
        )
        assert energy == residual * increment[winner] > 0
        for prior in increments:
            assert (
                sum(
                    prior[i] * hessian[i][j] * increment[j]
                    for i in range(size)
                    for j in range(size)
                )
                == 0
            )
        increments.append(increment)
        energies.append(energy)
        old_point = new_point

    assert active == support
    objective = (
        sum(
            old_point[i] * hessian[i][j] * old_point[j]
            for i in range(size)
            for j in range(size)
        )
        / 2
        - sum(load[i] * old_point[i] for i in range(size))
    )
    assert sum(energies, F(0)) / 2 == -objective
    assert sum(load[i] * old_point[i] for i in range(size)) <= F(alpha, degree[0])
    assert sum(
        degree[i] * increment[i]
        for increment in increments
        for i in range(size)
    ) == sum(degree[i] * old_point[i] for i in range(size)) <= 1

    hessian_inverse = inverse(hessian)
    for i in range(size):
        leverage = sum(
            increment[i] * increment[i] / energy
            for increment, energy in zip(increments, energies, strict=True)
        )
        assert leverage <= hessian_inverse[i][i]
        assert hessian_inverse[i][i] <= F(1, alpha * degree[i])
    return len(increments)


def audit_ppr_screening(
    hessian: list[list[F]],
    degree: list[int],
    alpha: F,
    rho: F,
    support: set[int],
) -> int:
    size = len(degree)
    ordinary_load = [alpha * F(i == 0) for i in range(size)]
    ordinary = solve(hessian, ordinary_load)
    p = (1 + alpha) / 2
    threshold = alpha * rho / p
    assert all(ordinary[i] > threshold for i in support)
    superlevel = [i for i in range(size) if ordinary[i] > threshold]
    assert sum(degree[i] for i in superlevel) < p / (alpha * rho)
    return len(support)


def audit_ppr_screening_sharpness() -> F:
    """Exact equitable solve for the root--candidate--clique family."""
    alpha = F(1, 100)
    p, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    candidate_ratio = F(0)
    for m, clique_size in ((10, 10_000), (25, 25_000), (50, 50_000)):
        equitable = [
            [p, -coupling, F(0), F(0)],
            [-coupling, p * (m + 1), -coupling * m, F(0)],
            [
                F(0),
                -coupling,
                p * clique_size - coupling * (m - 1),
                -coupling * (clique_size - m),
            ],
            [
                F(0),
                F(0),
                -coupling * m,
                p * (clique_size - 1)
                - coupling * (clique_size - m - 1),
            ],
        ]
        ordinary = solve(equitable, [alpha, F(0), F(0), F(0)])
        threshold = coupling / (p * (m + 1) + coupling)
        ratio = ordinary[1] / threshold
        assert ratio > alpha / p
        candidate_ratio = ratio

        rho = threshold * (1 - F(1, 10**8))
        restricted = solve(
            [[p, -coupling], [-coupling, p * (m + 1)]],
            [alpha * (1 - rho), -alpha * rho * (m + 1)],
        )
        assert restricted[0] > 0 and restricted[1] > 0
        selected_clique_key = -alpha * rho * clique_size + coupling * restricted[1]
        unselected_clique_key = -alpha * rho * (clique_size - 1)
        assert selected_clique_key < 0 and unselected_clique_key < 0
    assert candidate_ratio < 3 * alpha
    return candidate_ratio


def audit_legal_topplings(
    hessian: list[list[F]],
    load: list[F],
    degree: list[int],
    alpha: F,
    support: set[int],
    rng: Random,
) -> int:
    optimum = obstacle_point(hessian, load, support)
    size = len(load)

    # Least action: adding H^{-1}u for u>=0 produces exact stabilizers above
    # the obstacle point.
    extra_load = [F(rng.randrange(4), 17) for _ in range(size)]
    extra = solve(hessian, extra_load)
    stabilizer = [optimum[i] + extra[i] for i in range(size)]
    assert all(stabilizer[i] >= optimum[i] for i in range(size))
    assert all(
        sum(hessian[i][j] * stabilizer[j] for j in range(size)) >= load[i]
        for i in range(size)
    )

    state = [F(0)] * size
    topplings = 0
    diagonal = (1 + alpha) / 2
    for _ in range(30):
        residual = [
            load[i] - sum(hessian[i][j] * state[j] for j in range(size))
            for i in range(size)
        ]
        positive = [i for i in range(size) if residual[i] > 0]
        if not positive:
            break
        row = max(positive, key=lambda i: (residual[i] / degree[i], -i))
        assert row in support
        old_mass = sum((max(value, F(0)) for value in residual), F(0))
        amount = residual[row] / hessian[row][row]
        assert hessian[row][row] == diagonal * degree[row]
        state[row] += amount
        assert all(state[i] <= optimum[i] for i in range(size))
        next_residual = [
            load[i] - sum(hessian[i][j] * state[j] for j in range(size))
            for i in range(size)
        ]
        assert next_residual[row] == 0
        next_mass = sum((max(value, F(0)) for value in next_residual), F(0))
        assert next_mass - old_mass <= -(alpha / diagonal) * residual[row]
        topplings += 1
    return topplings


def pivot_support(
    hessian: list[list[F]], degree: list[int], alpha: F, rho: F
) -> tuple[set[int], list[tuple[int, F]]]:
    size = len(degree)
    if rho >= F(1, degree[0]):
        return set(), []

    support = {0}
    exterior = list(range(1, size))
    root_pivot = hessian[0][0]
    source_root = alpha / root_pivot
    degree_root = alpha * degree[0] / root_pivot
    intercept = {v: -hessian[v][0] * source_root for v in exterior}
    slope = {
        v: alpha * degree[v] - hessian[v][0] * degree_root for v in exterior
    }
    schur = {
        (u, v): hessian[u][v] - hessian[u][0] * hessian[0][v] / root_pivot
        for u in exterior
        for v in exterior
    }
    events: list[tuple[int, F]] = []
    while exterior:
        threshold = {v: intercept[v] / slope[v] for v in exterior if intercept[v] > 0}
        if not threshold:
            break
        winner = max(threshold, key=lambda v: (threshold[v], -v))
        event = threshold[winner]
        if event <= rho:
            break
        events.append((winner, event))
        pivot = schur[winner, winner]
        remaining = [v for v in exterior if v != winner]
        for vertex in remaining:
            gamma = -schur[vertex, winner] / pivot
            assert gamma >= 0
            intercept[vertex] += gamma * intercept[winner]
            slope[vertex] += gamma * slope[winner]
        schur = {
            (u, v): schur[u, v] - schur[u, winner] * schur[winner, v] / pivot
            for u in remaining
            for v in remaining
        }
        support.add(winner)
        exterior = remaining
    return support, events


def residual_pivot_support(
    hessian: list[list[F]], load: list[F], degree: list[int], alpha: F
) -> tuple[set[int], list[tuple[int, F]]]:
    """Fixed-target principal pivots, deliberately not in ratio order."""
    size = len(load)
    if load[0] <= 0:
        return set(), []

    support = {0}
    exterior = list(range(1, size))
    root_pivot = hessian[0][0]
    root_value = load[0] / root_pivot
    residual = {v: load[v] - hessian[v][0] * root_value for v in exterior}
    positive_mass = sum((max(value, F(0)) for value in residual.values()), F(0))
    assert positive_mass <= alpha
    schur = {
        (u, v): hessian[u][v] - hessian[u][0] * hessian[0][v] / root_pivot
        for u in exterior
        for v in exterior
    }
    events: list[tuple[int, F]] = []
    while True:
        positive = [v for v in exterior if residual[v] > 0]
        if not positive:
            break
        # Largest label is intentionally unrelated to ratio/event order.
        winner = max(positive)
        events.append((winner, residual[winner]))
        pivot = schur[winner, winner]
        row_sum = sum((schur[vertex, winner] for vertex in exterior), F(0))
        diagonal = (1 + alpha) / 2
        assert row_sum >= alpha * degree[winner]
        assert pivot <= diagonal * degree[winner]
        remaining = [v for v in exterior if v != winner]
        for vertex in remaining:
            gamma = -schur[vertex, winner] / pivot
            assert gamma >= 0
            residual[vertex] += gamma * residual[winner]
        next_positive_mass = sum(
            (max(residual[vertex], F(0)) for vertex in remaining), F(0)
        )
        assert (
            next_positive_mass
            <= positive_mass - (alpha / diagonal) * residual[winner]
        )
        positive_mass = next_positive_mass
        schur = {
            (u, v): schur[u, v] - schur[u, winner] * schur[winner, v] / pivot
            for u in remaining
            for v in remaining
        }
        support.add(winner)
        exterior = remaining
    return support, events


def connected_graph(size: int, rng: Random) -> tuple[list[list[F]], list[int]]:
    adjacency = [[F(0)] * size for _ in range(size)]
    degree = [0] * size
    edges = {(vertex, vertex + 1) for vertex in range(size - 1)}
    edges.update(
        (left, right)
        for left in range(size)
        for right in range(left + 2, size)
        if rng.randrange(4) == 0
    )
    for left, right in edges:
        adjacency[left][right] = adjacency[right][left] = 1
        degree[left] += 1
        degree[right] += 1
    return adjacency, degree


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-point-source-appr-envelope}" in source
    assert r"\label{eq:aesp-cd-point-source-appr-envelope}" in source
    assert r"\label{eq:aesp-cd-point-source-appr-envelope-volume}" in source
    assert r"\label{eq:aesp-cd-point-source-appr-envelope-radius}" in source
    assert r"\label{eq:aesp-cd-point-source-appr-envelope-reuse-gap}" in source
    assert r"\label{prop:aesp-cd-sparse-source-radius}" in source
    assert r"\label{eq:aesp-cd-sparse-source-radius}" in source
    assert r"\label{prop:aesp-cd-separated-source-decomposition}" in source
    assert r"\label{eq:aesp-cd-separated-source-decomposition}" in source
    assert r"\label{eq:aesp-cd-separated-source-volume}" in source
    assert r"\label{cor:aesp-cd-point-source-appr-envelope-oracle}" in source
    assert r"\label{cor:aesp-cd-appr-envelope-oracle}" in source
    assert r"\label{eq:aesp-cd-point-source-appr-envelope-oracle-error}" in source
    assert r"\label{eq:aesp-cd-point-source-appr-envelope-oracle-work}" in source
    assert r"\label{thm:aesp-cd-point-source-ratio-pivot}" in source
    assert r"\label{eq:aesp-cd-ratio-pivot-pair}" in source
    assert r"\label{eq:aesp-cd-ratio-pivot-schur}" in source
    assert r"\label{cor:aesp-cd-ratio-pivot-finite-stop}" in source
    assert r"\label{eq:aesp-cd-ratio-pivot-slope-band}" in source
    assert r"\label{cor:aesp-cd-ratio-pivot-interval-interface}" in source
    assert r"\label{eq:aesp-cd-ratio-pivot-interval-width}" in source
    assert r"\label{prop:aesp-cd-spectral-schur-ratio-stop}" in source
    assert r"\label{cor:aesp-cd-point-source-fixed-target-pivot}" in source
    assert r"\label{eq:aesp-cd-fixed-target-residual-stop}" in source
    assert r"\label{lem:aesp-cd-point-source-residual-mass}" in source
    assert r"\label{eq:aesp-cd-point-source-residual-mass}" in source
    assert r"\label{eq:aesp-cd-point-source-pivot-injection}" in source
    assert r"\label{prop:aesp-cd-point-source-harmonic-exit}" in source
    assert r"\label{prop:aesp-cd-point-source-hitting-column}" in source
    assert r"\label{eq:aesp-cd-point-source-hitting-flux}" in source
    assert r"\label{eq:aesp-cd-point-source-hitting-occupation}" in source
    assert (
        r"\label{lem:aesp-cd-point-source-response-residual-certificate}"
        in source
    )
    assert (
        r"\label{eq:aesp-cd-point-source-response-residual-certificate}"
        in source
    )
    assert r"\label{eq:aesp-cd-point-source-response-residual-target}" in source
    assert r"\label{lem:aesp-cd-point-source-hitting-radius}" in source
    assert r"\label{eq:aesp-cd-point-source-hitting-event-locality}" in source
    assert r"\label{cor:aesp-cd-point-source-route-output-interface}" in source
    assert r"\label{eq:aesp-cd-point-source-route-output-interface}" in source
    assert r"\label{lem:aesp-cd-point-source-frontier-universe}" in source
    assert r"\label{prop:aesp-cd-point-source-orthogonal-pivots}" in source
    assert r"\label{eq:aesp-cd-point-source-pivot-bessel}" in source
    assert r"\label{eq:aesp-cd-point-source-pivot-variation}" in source
    assert r"\label{prop:aesp-cd-point-source-ppr-screening}" in source
    assert r"\label{eq:aesp-cd-point-source-ppr-screening-sharp}" in source
    assert r"\label{prop:aesp-cd-point-source-dissipative-sandpile}" in source
    assert r"\label{eq:aesp-cd-point-source-least-action}" in source

    rng = Random(20260829)
    checked = 0
    event_count = 0
    residual_event_count = 0
    order_difference_count = 0
    toppling_count = 0
    hitting_column_count = 0
    frontier_record_count = 0
    orthogonal_direction_count = 0
    hitting_radius_count = 0
    residual_certificate_count = 0
    screened_support_count = 0
    appr_envelope_count = 0
    appr_push_count = 0
    sparse_radius_coordinates = 0
    sparse_appr_coordinates = 0
    for size in range(3, 8):
        for _ in range(40):
            adjacency, degree = connected_graph(size, rng)
            alpha = rng.choice((F(1, 9), F(1, 5), F(2, 7), F(1, 3), F(3, 7)))
            diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
            hessian = [
                [
                    diagonal * degree[i] if i == j else -coupling * adjacency[i][j]
                    for j in range(size)
                ]
                for i in range(size)
            ]
            audit_harmonic_exit(
                hessian,
                adjacency,
                degree,
                alpha,
                list(range(1 + rng.randrange(size - 1))),
            )
            hitting_column_count += audit_hitting_column(
                hessian,
                adjacency,
                degree,
                alpha,
                list(range(1 + rng.randrange(size - 1))),
                rng,
            )
            hitting_radius_count += audit_hitting_radius(
                hessian,
                adjacency,
                degree,
                alpha,
                list(range(1 + rng.randrange(size - 1))),
            )
            residual_certificate_count += audit_response_residual_certificate(
                hessian,
                degree,
                alpha,
                list(range(1 + rng.randrange(size - 1))),
                rng,
            )
            rho = rng.choice((F(1, 20), F(1, 12), F(1, 8), F(1, 6)))
            load = [alpha * (F(i == 0) - rho * degree[i]) for i in range(size)]
            expected = obstacle_support(hessian, load)
            appr_envelope, pushes = appr_support(
                adjacency, degree, alpha, rho
            )
            enlarged_load = [
                alpha
                * (F(i == 0) - coupling * rho * degree[i])
                for i in range(size)
            ]
            enlarged_support = obstacle_support(hessian, enlarged_load)
            assert expected <= appr_envelope <= enlarged_support
            assert sum(degree[i] for i in appr_envelope) <= 1 / (
                coupling * rho
            )
            assert set(graph_distances(adjacency, appr_envelope, 0)) == (
                appr_envelope
            )
            appr_envelope_count += len(appr_envelope)
            appr_push_count += pushes

            # General sparse sources retain the same exact source-set radius.
            sparse_alpha = F(1, 9)
            sparse_coupling = (1 - sparse_alpha) / 2
            sparse_diagonal = (1 + sparse_alpha) / 2
            sparse_hessian = [
                [
                    sparse_diagonal * degree[i]
                    if i == j
                    else -sparse_coupling * adjacency[i][j]
                    for j in range(size)
                ]
                for i in range(size)
            ]
            source_count = min(size, 2 + rng.randrange(2))
            source_indices = set(rng.sample(range(size), source_count))
            raw_weights = {i: 1 + rng.randrange(5) for i in source_indices}
            total_weight = sum(raw_weights.values())
            sparse_source = [
                F(raw_weights.get(i, 0), total_weight) for i in range(size)
            ]
            sparse_load = [
                sparse_alpha * (sparse_source[i] - rho * degree[i])
                for i in range(size)
            ]
            sparse_support = obstacle_support(sparse_hessian, sparse_load)
            for component in support_components(adjacency, sparse_support):
                assert component & source_indices
            distance = source_distances(adjacency, source_indices)
            if sparse_support:
                radius = max(distance[i] for i in sparse_support)
                if radius:
                    assert F(1, 2) ** (radius - 1) > (
                        sparse_alpha * rho / (1 - sparse_alpha)
                    )
            sparse_radius_coordinates += len(sparse_support)

            sparse_envelope, _ = appr_support(
                adjacency,
                degree,
                sparse_alpha,
                rho,
                sparse_source,
            )
            sparse_eta = sparse_coupling * rho
            sparse_enlarged_load = [
                sparse_alpha * (sparse_source[i] - sparse_eta * degree[i])
                for i in range(size)
            ]
            sparse_enlarged_support = obstacle_support(
                sparse_hessian, sparse_enlarged_load
            )
            assert sparse_support <= sparse_envelope <= sparse_enlarged_support
            for component in support_components(adjacency, sparse_envelope):
                assert component & source_indices
            if sparse_envelope:
                envelope_radius = max(distance[i] for i in sparse_envelope)
                if envelope_radius:
                    assert F(1, 2) ** (envelope_radius - 1) > (
                        sparse_alpha * rho / 2
                    )
            sparse_appr_coordinates += len(sparse_envelope)
            toppling_count += audit_legal_topplings(
                hessian, load, degree, alpha, expected, rng
            )
            actual, events = pivot_support(hessian, degree, alpha, rho)
            residual_actual, residual_events = residual_pivot_support(
                hessian, load, degree, alpha
            )
            assert actual == expected
            assert residual_actual == expected
            assert all(events[index][1] >= events[index + 1][1] for index in range(len(events) - 1))
            event_count += len(events)
            residual_event_count += len(residual_events)
            assert sum((value for _, value in residual_events), F(0)) <= coupling
            if [vertex for vertex, _ in events] != [
                vertex for vertex, _ in residual_events
            ]:
                order_difference_count += 1
            frontier_record_count += audit_frontier_universe(
                adjacency,
                degree,
                expected,
                [vertex for vertex, _ in residual_events],
            )
            orthogonal_direction_count += audit_orthogonal_pivots(
                hessian,
                load,
                degree,
                alpha,
                expected,
                residual_events,
            )
            screened_support_count += audit_ppr_screening(
                hessian, degree, alpha, rho, expected
            )
            checked += 1

    # Exact finite stopping-band calibration on P3, face {0}.
    alpha = F(1, 5)
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    degree = [1, 2, 1]
    hessian = [
        [
            diagonal * degree[i]
            if i == j
            else (-coupling if abs(i - j) == 1 else F(0))
            for j in range(3)
        ]
        for i in range(3)
    ]
    root_source = alpha / hessian[0][0]
    root_degree = alpha * degree[0] / hessian[0][0]
    intercept = -hessian[1][0] * root_source
    slope = alpha * degree[1] - hessian[1][0] * root_degree
    assert slope == F(8, 15)
    assert alpha * degree[1] <= slope <= diagonal * degree[1]
    threshold = intercept / slope
    rho = F(1, 5)
    eta = threshold - rho
    key = intercept - rho * slope
    assert threshold == F(1, 4) and eta == F(1, 20)
    assert key / degree[1] <= diagonal * eta

    # Worst-centered pair intervals still obey the certified ratio-width bound.
    epsilon_a, epsilon_b = F(1, 300), F(1, 100)
    row_degree = degree[1]
    estimate_a = intercept + epsilon_a * row_degree
    estimate_b = slope - epsilon_b * row_degree
    upper_a = estimate_a + epsilon_a * row_degree
    lower_b = max(alpha * row_degree, estimate_b - epsilon_b * row_degree)
    upper_threshold = upper_a / lower_b
    assert epsilon_b <= alpha / 4
    assert 0 <= upper_threshold - threshold
    assert upper_threshold - threshold <= 4 * (epsilon_a + epsilon_b) / alpha
    assert upper_threshold == F(11, 37)

    # A two-sided spectral approximation can erase a positive updated ratio.
    spectral_error, base_slope = F(1, 10), F(1, 5)
    exact_schur = [[F(1), -spectral_error], [-spectral_error, F(1)]]
    approximate_schur = [[F(1), F(0)], [F(0), F(1)]]
    lower_difference = [
        [
            exact_schur[i][j]
            - (1 - spectral_error) * approximate_schur[i][j]
            for j in range(2)
        ]
        for i in range(2)
    ]
    upper_difference = [
        [
            (1 + spectral_error) * approximate_schur[i][j]
            - exact_schur[i][j]
            for j in range(2)
        ]
        for i in range(2)
    ]
    for difference in (lower_difference, upper_difference):
        assert difference[0][0] >= 0
        assert difference[1][1] >= 0
        assert (
            difference[0][0] * difference[1][1]
            - difference[0][1] * difference[1][0]
            >= 0
        )
    exact_multiplier = -exact_schur[1][0] / exact_schur[0][0]
    approximate_multiplier = -approximate_schur[1][0] / approximate_schur[0][0]
    exact_updated_ratio = exact_multiplier / (base_slope + exact_multiplier)
    approximate_updated_ratio = approximate_multiplier / (
        base_slope + approximate_multiplier
    )
    assert exact_updated_ratio == F(1, 3)
    assert approximate_updated_ratio == 0
    sharp_screening_ratio = audit_ppr_screening_sharpness()
    audit_separated_source_decomposition()

    print("PASS point-source ratio-pivot homotopy")
    print(f"  exact random connected instances={checked}, admitted events={event_count}")
    print("  pivot support equals exhaustive obstacle KKT support in every case")
    print("  event thresholds are nonincreasing; every coordinate enters once")
    print(f"  arbitrary-order fixed-target residual events={residual_event_count}")
    print(f"  traces using a different legal pivot order={order_difference_count}")
    assert order_difference_count > 0
    print("  positive exterior residual mass is nonincreasing and at most alpha")
    print("  total exact block-pivot residual injection is at most (1-alpha)/2")
    print(f"  killed hitting-response columns audited={hitting_column_count}")
    print(f"  square-root response-radius coordinates audited={hitting_radius_count}")
    print(
        "  residual-certified response coordinates audited="
        f"{residual_certificate_count}"
    )
    print(f"  persistent original-frontier records audited={frontier_record_count}")
    print(f"  energy-orthogonal pivot directions audited={orthogonal_direction_count}")
    print(f"  ordinary-PPR screened support coordinates audited={screened_support_count}")
    print(
        "  APPR sandwich coordinates/pushes audited="
        f"{appr_envelope_count}/{appr_push_count}"
    )
    print(
        "  sparse-source RPPR/APPR radius coordinates audited="
        f"{sparse_radius_coordinates}/{sparse_appr_coordinates}"
    )
    print("  separated sparse-source RPPR decomposition: exact P5 witness")
    print(
        "  alpha-rho screening sharpness ratio="
        f"{float(sharp_screening_ratio):.12f}"
    )
    print(f"  dissipative legal topplings audited={toppling_count}; least action exact")
    print("  finite KKT slope band: exact P3 calibration")
    print("  certified pair intervals: worst-centered exact width bound")
    print("  spectral-only STOP: positive ratio 1/3 is approximated by zero")


if __name__ == "__main__":
    main()
