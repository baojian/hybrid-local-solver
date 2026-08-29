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

    rng = Random(20260829)
    checked = 0
    event_count = 0
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
            assert actual == expected
            assert all(events[index][1] >= events[index + 1][1] for index in range(len(events) - 1))
            event_count += len(events)
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

    print("PASS point-source ratio-pivot homotopy")
    print(f"  exact random connected instances={checked}, admitted events={event_count}")
    print("  pivot support equals exhaustive obstacle KKT support in every case")
    print("  event thresholds are nonincreasing; every coordinate enters once")
    print("  finite KKT slope band: exact P3 calibration")


if __name__ == "__main__":
    main()
