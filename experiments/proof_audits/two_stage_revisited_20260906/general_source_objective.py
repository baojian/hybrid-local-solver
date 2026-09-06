"""Exact audit of the source-envelope / original-objective two-stage theorem.

Stage I uses the metered sparse reporter. Stage II is a dense arithmetic
reference; its ledger records the original-incidence charge of implementing
that recurrence by fixed-face row scans. Dense reference arithmetic and exact
obstacle solves are not claimed to have the theorem's local running time.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .directed_rounding import ceil_grid, floor_grid
from .orthant_continuation import ExactObstacle, dot, mv, sub
from .sparse_sources import MultiSourceExact, MultiSourceRounded
from .sparse_state import GraphOracle


def first_stage(graph, hot, alpha, rho, delta, rounded):
    implementation = MultiSourceRounded if rounded else MultiSourceExact
    state = implementation(GraphOracle(graph), hot, alpha, F(1, 2))
    state.rho = rho
    tau = alpha * delta**2 / 2
    if rounded:
        bound = min(F(1, 16), state.theta, state.theta * alpha**2 * rho / 256)
        bound = min(bound, state.theta * tau / 512)
        state.h = F(1)
        while state.h > bound:
            state.h /= 2
        state.gamma = 256 * state.h / state.theta
        state.cooling_grid = state.theta * rho / 8
    while state.r > rho:
        state.step()
        state.r = max(
            rho,
            ceil_grid(state.eta * state.r, state.cooling_grid) if rounded else state.eta * state.r,
        )
    bound = (13 if rounded else 9) * alpha * rho
    if rounded:
        power, blocks = 1, 0
        while power * tau < 2 * bound:
            power *= 2
            blocks += 1
        for _ in range(blocks * int(1 / state.theta)):
            state.step()
    else:
        while bound > tau:
            state.step()
            bound *= state.chi
    values = state.materialize()
    state.counts["terminal_materialized_cells"] += len(values)
    answer = {i: value - delta for i, value in values.items() if value > delta}
    return state, answer


def dense_step(matrix, source, lam, theta, x, z, grid=None):
    chi = 1 - theta
    y = [(a + theta * b) / (1 + theta) for a, b in zip(x, z)]
    gradient = [a - b + lam for a, b in zip(mv(matrix, y), source)]
    raw = [chi * b + theta * c - g / theta for b, c, g in zip(z, y, gradient)]
    p = [max(F(0), value) for value in raw]
    if grid is not None:
        p = [floor_grid(value, grid) for value in p]
    result = [chi * a + theta * b for a, b in zip(x, p)]
    if grid is not None:
        result = [floor_grid(value, grid) for value in result]
    return result, p


def check_case(graph, weights, alpha, rho, epsilon, rounded):
    n = len(graph)
    degree = [graph.degree(i) for i in range(n)]
    matrix = [
        [
            (1 + alpha) / 2
            if i == j
            else -(1 - alpha) / (2 * degree[i])
            if graph.has_edge(i, j)
            else F(0)
            for j in range(n)
        ]
        for i in range(n)
    ]
    source = [alpha * weights.get(i, F(0)) / degree[i] for i in range(n)]
    optimum, _ = ExactObstacle(matrix, source).at(alpha * rho)

    def objective(x):
        return dot(degree, x, mv(matrix, x)) / 2 - dot(degree, sub(source, [alpha * rho] * n), x)

    delta = F(1, 2)
    while delta**2 > epsilon * rho / 4:
        delta /= 2
    hot = {i: value for i, value in weights.items() if value / degree[i] > rho / 2}
    assert sum(degree[i] for i in hot) < 2 / rho
    hot_source = [alpha * hot.get(i, F(0)) / degree[i] for i in range(n)]
    hot_opt, _ = ExactObstacle(matrix, hot_source).at(alpha * rho / 2)
    assert all(u <= h for u, h in zip(optimum, hot_opt))
    state = None
    stage_two_steps = 0
    grid = None
    face = []
    stage_one_gap = None
    envelope_gap = F(0)
    missed = 0
    if rho >= max(value / degree[i] for i, value in weights.items()):
        output = [F(0)] * n
    elif alpha == 1:
        output = [max(F(0), weights.get(i, F(0)) / degree[i] - rho) for i in range(n)]
    else:
        state, first = first_stage(graph, hot, alpha, rho / 2, delta, rounded)
        first_dense = [first.get(i, F(0)) for i in range(n)]
        assert all(0 <= p <= h and h - p <= 2 * delta for p, h in zip(first_dense, hot_opt))
        stage_one_gap = objective(first_dense) - objective(optimum)
        face = sorted(first)
        volume = sum(degree[i] for i in face)
        assert volume <= 2 / rho
        missed = sum(optimum[i] > 0 for i in range(n) if i not in first)
        assert all(optimum[i] <= 2 * delta for i in range(n) if i not in first)
        principal = [[matrix[i][j] for j in face] for i in face]
        restricted_source = [source[i] for i in face]
        restricted_degrees = [degree[i] for i in face]
        restricted, _ = ExactObstacle(principal, restricted_source).at(alpha * rho)
        extended = [F(0)] * n
        for i, value in zip(face, restricted):
            extended[i] = value
        assert all(u <= v for u, v in zip(extended, optimum))
        assert all(v - u <= 2 * delta for u, v in zip(extended, optimum))
        envelope_gap = objective(extended) - objective(optimum)
        assert 0 <= envelope_gap <= 2 * delta**2 / rho
        x = [F(0)] * len(face)
        z = x.copy()
        exact_x, exact_z = x.copy(), z.copy()
        if face:
            theta = state.theta
            grid_bound = delta * theta**2 / (16 * max(1, volume))
            if rounded:
                grid = F(1)
                while grid > grid_bound:
                    grid /= 2
            power, blocks = 1, 0
            while power * alpha * delta**2 < 8:
                power *= 2
                blocks += 1
            stage_two_steps = blocks * int(1 / theta)
            for _ in range(stage_two_steps):
                x, z = dense_step(principal, restricted_source, alpha * rho, theta, x, z, grid)
                if rounded:
                    exact_x, exact_z = dense_step(
                        principal, restricted_source, alpha * rho, theta, exact_x, exact_z
                    )
                    dx, dz = sub(x, exact_x), sub(z, exact_z)
                    distance_squared = dot(restricted_degrees, dx, mv(principal, dx)) / 2
                    distance_squared += theta**2 * dot(restricted_degrees, dz, dz) / 2
                    assert distance_squared <= 16 * grid**2 * volume / theta**2
                    assert all(value.denominator <= grid.denominator for value in x + z)
            error = sub(x, restricted)
            assert dot(restricted_degrees, error, error) <= delta**2
        output = [F(0)] * n
        for i, value in zip(face, x):
            output[i] = max(F(0), value - delta)
        final_face_gap = objective(output) - objective(extended)
        assert 0 <= final_face_gap <= 2 * delta**2 / rho
    assert all(0 <= x <= u for x, u in zip(output, optimum))
    assert all(u - x <= 4 * delta for x, u in zip(output, optimum))
    residual = sub(source, mv(matrix, output))
    kkt = max(
        abs(alpha * rho - value) if x > 0 else max(F(0), value - alpha * rho)
        for x, value in zip(output, residual)
    )
    assert kkt <= 4 * delta
    acl_certified = delta <= alpha * rho / 4
    if acl_certified:
        assert all(0 <= value <= 2 * alpha * rho for value in residual)
    gap = objective(output) - objective(optimum)
    assert 0 <= gap <= epsilon
    output_volume = sum(degree[i] for i, value in enumerate(output) if value > 0)
    assert output_volume <= 1 / rho
    face_volume = sum(degree[i] for i in face)
    return {
        "n": n,
        "source": {str(i): str(value) for i, value in weights.items()},
        "alpha": str(alpha),
        "rho": str(rho),
        "eps_obj": str(epsilon),
        "rounded": rounded,
        "delta": str(delta),
        "input_source_reads": 2 * len(weights),
        "input_degree_queries": len(weights),
        "retained_source_count": len(hot),
        "cold_source_entries_restored": sum(i not in hot and i in face for i in weights),
        "missed_optimal_coordinates": missed,
        "stage_one_original_objective_gap": float(stage_one_gap)
        if stage_one_gap is not None
        else None,
        "stage_one_alone_exceeds_budget": stage_one_gap is not None and stage_one_gap > epsilon,
        "envelope_gap": float(envelope_gap),
        "objective_gap": float(gap),
        "normalized_kkt_density": float(kkt),
        "positive_residual_certified": acl_certified,
        "stage_one_counts": dict(state.counts) if state else {},
        "stage_two_steps": stage_two_steps,
        "stage_two_grid": str(grid) if grid is not None else None,
        "face_volume": face_volume,
        "stage_two_incidences": stage_two_steps * face_volume,
        "principal_build_incidences": face_volume,
        "output_volume": output_volume,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    source_record = provenance({"max_n": args.max_n}, args.output)
    cases = []
    last_progress = started

    def save(status):
        record = {
            "provenance": source_record,
            "status": status,
            "arithmetic": "exact rational and specified dyadic rounding",
            "case_count": len(cases),
            "elapsed_seconds": time.monotonic() - started,
            "cases": cases,
        }
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(record, indent=2) + "\n")
        return record

    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        n = len(graph)
        sources = [
            {i: F(1, n) for i in graph},
            {0: F(1, 3), n - 1: F(2, 3)},
            {0: F(999, 1000)} | {i: F(1, 1000 * (n - 1)) for i in range(1, n)},
        ]
        for weights in sources:
            for alpha in (F(1), F(1, 4), F(1, 64)):
                for factor in (2, 8):
                    rho = max(value / graph.degree(i) for i, value in weights.items()) / factor
                    for epsilon in (F(1, 100), F(1, 10**6)):
                        for rounded in (False, True):
                            row = check_case(graph, weights, alpha, rho, epsilon, rounded)
                            row["atlas_id"] = atlas_id
                            cases.append(row)
                            if time.monotonic() - last_progress >= 30:
                                print(
                                    json.dumps({"passed": len(cases), "last_atlas_id": atlas_id}),
                                    flush=True,
                                )
                                save("running")
                                last_progress = time.monotonic()
    for alpha in (F(1), F(3, 4)):
        for rounded in (False, True):
            cases.append(check_case(nx.path_graph(4), {0: F(1)}, alpha, F(2), F(1, 100), rounded))
    record = save("passed")
    print(json.dumps({key: value for key, value in record.items() if key != "cases"}), flush=True)


if __name__ == "__main__":
    main()
