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
    hessian: list[list[F]], load: list[F], alpha: F
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
        remaining = [v for v in exterior if v != winner]
        for vertex in remaining:
            gamma = -schur[vertex, winner] / pivot
            assert gamma >= 0
            residual[vertex] += gamma * residual[winner]
        next_positive_mass = sum(
            (max(residual[vertex], F(0)) for vertex in remaining), F(0)
        )
        assert next_positive_mass <= positive_mass
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

    rng = Random(20260829)
    checked = 0
    event_count = 0
    residual_event_count = 0
    order_difference_count = 0
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
            rho = rng.choice((F(1, 20), F(1, 12), F(1, 8), F(1, 6)))
            load = [alpha * (F(i == 0) - rho * degree[i]) for i in range(size)]
            expected = obstacle_support(hessian, load)
            actual, events = pivot_support(hessian, degree, alpha, rho)
            residual_actual, residual_events = residual_pivot_support(
                hessian, load, alpha
            )
            assert actual == expected
            assert residual_actual == expected
            assert all(events[index][1] >= events[index + 1][1] for index in range(len(events) - 1))
            event_count += len(events)
            residual_event_count += len(residual_events)
            if [vertex for vertex, _ in events] != [
                vertex for vertex, _ in residual_events
            ]:
                order_difference_count += 1
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
    print("  finite KKT slope band: exact P3 calibration")
    print("  certified pair intervals: worst-centered exact width bound")
    print("  spectral-only STOP: positive ratio 1/3 is approximated by zero")


if __name__ == "__main__":
    main()
