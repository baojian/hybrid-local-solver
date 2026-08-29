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
    assert r"\label{lem:aesp-cd-point-source-frontier-universe}" in source
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
    for size in range(3, 8):
        for _ in range(40):
            adjacency, degree = connected_graph(size, rng)
            alpha = rng.choice((F(1, 5), F(2, 7), F(1, 3), F(3, 7)))
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
            rho = rng.choice((F(1, 20), F(1, 12), F(1, 8), F(1, 6)))
            load = [alpha * (F(i == 0) - rho * degree[i]) for i in range(size)]
            expected = obstacle_support(hessian, load)
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
    print(f"  persistent original-frontier records audited={frontier_record_count}")
    print(f"  dissipative legal topplings audited={toppling_count}; least action exact")
    print("  finite KKT slope band: exact P3 calibration")
    print("  certified pair intervals: worst-centered exact width bound")
    print("  spectral-only STOP: positive ratio 1/3 is approximated by zero")


if __name__ == "__main__":
    main()
