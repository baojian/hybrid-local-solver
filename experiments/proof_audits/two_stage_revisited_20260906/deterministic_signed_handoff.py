"""Exact audit of a coarse orthant prefix and signed reserved GS delivery.

The actual sparse prefix is reused, with a distinct coarse stopping target.
Reference obstacle solves and dense residuals only check invariants offline.
The optional early gate is tested at geometric regularizer checkpoints.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction as F
import json
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .directed_rounding import RoundedCooling, ceil_grid, floor_grid
from .orthant_continuation import ExactObstacle, dot, mv, solve, sub
from .sparse_state import GraphOracle, SparseCooling


def check_case(
    graph, seed, alpha, epsilon, rounded, early, *, external_signed=False, external_composite=False
):
    implementation = RoundedCooling if rounded else SparseCooling
    state = implementation(GraphOracle(graph), seed, alpha, F(1, 2))
    sigma, reserve, final_r = epsilon / 3, epsilon / 6, epsilon / 12
    state.rho = final_r
    budget = alpha**2 * state.theta * reserve
    if rounded:
        bound = min(F(1, 16), state.theta, state.theta * alpha**2 * final_r / 256)
        bound = min(bound, state.theta * budget / 512)
        state.h = F(1)
        while state.h > bound:
            state.h /= 2
        state.gamma = 256 * state.h / state.theta
        state.cooling_grid = state.theta * final_r / 8
    n = len(graph)
    degree = [graph.degree(i) for i in graph]
    q0, c = (1 + alpha) / 2, (1 - alpha) / 2
    matrix = [
        [q0 if i == j else -c / degree[i] if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    source = [alpha / degree[i] if i == seed else F(0) for i in graph]
    optimum, _ = ExactObstacle(matrix, source).at(alpha * final_r)
    ppr = solve(matrix, source)
    counts = Counter()

    def objective(x):
        return dot(degree, x, mv(matrix, x)) / 2 - dot(
            degree, sub(source, [alpha * final_r] * n), x
        )

    def get_residual():
        represented = state.materialize()
        x = [represented.get(i, F(0)) for i in graph]
        counts["checkpoint_incidences"] += sum(degree[i] for i in graph if x[i])
        counts["checkpoints"] += 1
        residual = sub(source, mv(matrix, x))
        return x, residual

    def excess(residual):
        return sum(
            d * max(F(0), abs(value) - alpha * reserve) for d, value in zip(degree, residual)
        )

    next_checkpoint = state.r / 2
    reason, frozen_steps = "coarse_objective", 0
    while state.r > final_r:
        state.step()
        state.r = max(
            final_r,
            ceil_grid(state.eta * state.r, state.cooling_grid) if rounded else state.eta * state.r,
        )
        if early and state.r <= next_checkpoint:
            x, residual = get_residual()
            if excess(residual) <= alpha * state.theta:
                reason = "early_residual_excess"
                break
            next_checkpoint /= 2
    if reason == "coarse_objective":
        bound = (13 if rounded else 9) * alpha * final_r
        if rounded:
            power, blocks = 1, 0
            while power * budget < 2 * bound:
                power *= 2
                blocks += 1
            frozen_steps = blocks * int(1 / state.theta)
            for _ in range(frozen_steps):
                state.step()
        else:
            while bound > budget:
                state.step()
                bound *= state.chi
                frozen_steps += 1
        x, residual = get_residual()
        gap = objective(x) - objective(optimum)
        assert 0 <= gap <= budget
        response_error = mv(matrix, sub(x, optimum))
        assert dot(degree, response_error, response_error) <= 2 * gap
        assert excess(residual) <= gap / (2 * alpha * (reserve - final_r))
    if external_signed:
        # A separate tail-only witness. It is explicitly NOT an output of
        # the accelerated prefix. Its purpose is to exercise negative rows.
        x = ppr.copy()
        perturbation = alpha * state.theta / (8 * degree[seed])
        if rounded:
            x = [floor_grid(value, state.h**2) for value in x]
            perturbation = floor_grid(perturbation, state.h**2)
        x[seed] += perturbation
        residual = sub(source, mv(matrix, x))
        assert x[seed] > ppr[seed] and residual[seed] < -alpha * sigma
    signed_composite_gap = None
    if external_composite:
        # A separate signed composite-gap interface, not an AESP trajectory.
        x = optimum.copy()
        vertex = next(i for i in reversed(list(graph)) if x[i] == 0)
        magnitude = F(1)
        while True:
            x[vertex] = -magnitude
            signed_composite_gap = (
                objective(x) + 2 * alpha * final_r * degree[vertex] * magnitude - objective(optimum)
            )
            if signed_composite_gap <= budget:
                break
            magnitude /= 2
        if rounded:
            # Round the entire supplied interface state toward zero on the
            # same fixed grid, and verify its actual composite gap again.
            x = [
                floor_grid(value, state.h**2) if value >= 0 else -floor_grid(-value, state.h**2)
                for value in x
            ]
            signed_composite_gap = (
                objective(x)
                - objective(optimum)
                + sum(2 * alpha * final_r * d * max(F(0), -value) for d, value in zip(degree, x))
            )
        residual = sub(source, mv(matrix, x))
        assert min(x) < 0 and 0 <= signed_composite_gap <= budget
        assert max(map(abs, residual)) > alpha * sigma
        assert (
            dot(degree, mv(matrix, sub(x, optimum)), mv(matrix, sub(x, optimum)))
            <= 2 * signed_composite_gap
        )
        assert excess(residual) <= signed_composite_gap / (2 * alpha * (reserve - final_r))
    initial_excess = excess(residual)
    assert initial_excess <= alpha * state.theta
    initial_max_residual = max(map(abs, residual))
    initial_signed = min(residual) < 0
    initial_above_ppr = any(value > u for value, u in zip(x, ppr))
    initial_nonnegative = min(x) >= 0
    tail_grid = state.h**2 if rounded else None
    if rounded:
        while tail_grid > alpha * (sigma - reserve) / (2 * q0):
            tail_grid /= 2
        assert all(value % tail_grid == 0 for value in x)
    queue = deque(i for i in graph if abs(residual[i]) > alpha * sigma)
    queued = set(queue)
    while queue:
        i = queue.popleft()
        queued.remove(i)
        if abs(residual[i]) <= alpha * sigma:
            continue
        previous_excess = excess(residual)
        sign = 1 if residual[i] > 0 else -1
        ideal = (abs(residual[i]) - alpha * reserve) / q0
        magnitude = floor_grid(ideal, tail_grid) if rounded else ideal
        assert magnitude >= ideal / 2
        increment = sign * magnitude
        x[i] += increment
        residual[i] -= q0 * increment
        if initial_nonnegative:
            assert x[i] >= 0
        assert abs(residual[i]) < alpha * sigma
        counts["tail_updates"] += 1
        counts["negative_tail_updates"] += sign < 0
        for neighbor in graph.neighbors(i):
            residual[neighbor] += c * increment / degree[neighbor]
            counts["tail_incidences"] += 1
            if abs(residual[neighbor]) > alpha * sigma and neighbor not in queued:
                queued.add(neighbor)
                queue.append(neighbor)
        assert excess(residual) <= previous_excess - alpha * degree[i] * magnitude
        factor = 2 if rounded else 1
        assert counts["tail_incidences"] <= factor * q0 * initial_excess / (
            alpha**2 * (sigma - reserve)
        )
    assert residual == sub(source, mv(matrix, x))
    assert max(map(abs, residual)) <= alpha * sigma
    assert max(abs(value - u) for value, u in zip(x, ppr)) <= sigma
    answer = [max(F(0), value - 2 * sigma) for value in x]
    delivered_optimum, _ = ExactObstacle(matrix, source).at(alpha * sigma)
    clipped_residual = sub(source, mv(matrix, answer))
    assert all(0 <= value <= u for value, u in zip(answer, delivered_optimum))
    assert min(clipped_residual) >= 0
    assert all(r >= alpha * sigma for value, r in zip(answer, clipped_residual) if value > 0)
    assert all(0 <= value <= u for value, u in zip(answer, ppr))
    assert max(u - value for value, u in zip(answer, ppr)) <= epsilon
    assert sum(d for d, value in zip(degree, answer) if value) <= 3 / epsilon
    if external_signed:
        assert counts["negative_tail_updates"] > 0
    if external_composite:
        assert counts["tail_updates"] > 0
    scope = "actual two-stage run"
    if external_signed:
        scope = "external signed tail-only witness"
    if external_composite:
        scope = "external signed composite-gap tail-only witness"
    return {
        "n": n,
        "seed": seed,
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "rounded": rounded,
        "early_enabled": early,
        "scope": scope,
        "supplied_signed_composite_gap": str(signed_composite_gap),
        "initial_nonnegative": initial_nonnegative,
        "prefix_stop_reason": reason,
        "prefix_regularizer_at_stop": float(state.r),
        "prefix_steps": state.steps,
        "frozen_steps": frozen_steps,
        "initial_excess_mass": float(initial_excess),
        "initial_max_residual_density": float(initial_max_residual),
        "initial_signed_residual": initial_signed,
        "initial_above_ppr": initial_above_ppr,
        "prefix_counts": None if external_signed or external_composite else dict(state.counts),
        "delivery_counts": dict(counts),
    }


def check_endpoint(graph, seed, alpha, epsilon):
    """Exercise the constant-work branches; dense references are offline."""
    sigma = epsilon / 3
    degree = [graph.degree(i) for i in graph]
    assert sigma * degree[seed] >= 1 or alpha == 1
    answer = [F(0)] * len(graph)
    if sigma * degree[seed] < 1:
        answer[seed] = F(1, degree[seed]) - sigma
    q0, c = (1 + alpha) / 2, (1 - alpha) / 2
    matrix = [
        [q0 if i == j else -c / degree[i] if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    source = [alpha / degree[i] if i == seed else F(0) for i in graph]
    optimum, _ = ExactObstacle(matrix, source).at(alpha * sigma)
    ppr = solve(matrix, source)
    residual = sub(source, mv(matrix, answer))
    assert all(0 <= value <= u for value, u in zip(answer, optimum))
    assert min(residual) >= 0
    assert all(r >= alpha * sigma for value, r in zip(answer, residual) if value > 0)
    assert max(u - value for value, u in zip(answer, ppr)) <= epsilon
    assert sum(d for d, value in zip(degree, answer) if value) <= 3 / epsilon
    return {
        "n": len(graph),
        "seed": seed,
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "scope": "constant-work endpoint branch",
        "degree_replies": 1,
        "adjacency_incidences": 0,
        "output_records": sum(value > 0 for value in answer),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=3)
    parser.add_argument("--alphas", default="1/4,1/64")
    parser.add_argument("--early", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    alpha_values = tuple(map(F, args.alphas.split(",")))
    if not alpha_values or any(not 0 < value < 1 for value in alpha_values):
        parser.error(
            "--alphas must contain values strictly between zero and one; endpoints are separate"
        )
    source_record = provenance(vars(args) | {"output": str(args.output)}, args.output)
    started = time.monotonic()
    rows = []
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in alpha_values:
                for epsilon in (F(1, 32), F(1, 65536)):
                    for rounded in (False, True):
                        row = check_case(graph, seed, alpha, epsilon, rounded, args.early)
                        row["atlas_id"] = atlas_id
                        rows.append(row)
    signed_witnesses = [
        check_case(graph, 0, alpha, F(1, 65536), rounded, False, external_signed=True)
        for graph in (nx.path_graph(4), nx.cycle_graph(4), nx.star_graph(7))
        for alpha in (F(1, 4), F(1, 64))
        for rounded in (False, True)
    ]
    endpoints = [
        check_endpoint(graph, seed, alpha, F(1, 2))
        for graph in (nx.path_graph(4), nx.star_graph(8))
        for seed in graph
        for alpha in (F(1), F(1, 64))
        if graph.degree(seed) >= 6 or alpha == 1
    ]
    signed_composite_witnesses = [
        check_case(
            nx.path_graph(16), seed, F(1, 4), F(1, 65536), rounded, False, external_composite=True
        )
        for seed in (0, 15)
        for rounded in (False, True)
    ]
    record = {
        "provenance": source_record,
        "status": "passed",
        "arithmetic": "exact sparse rational prefix and separately rounded prefix/tail",
        "case_count": len(rows),
        "nonempty_tail_cases": sum(
            row["delivery_counts"].get("tail_updates", 0) > 0 for row in rows
        ),
        "early_handoff_cases": sum(
            row["prefix_stop_reason"] == "early_residual_excess" for row in rows
        ),
        "signed_handoff_cases": sum(row["initial_signed_residual"] for row in rows),
        "external_signed_tail_cases": len(signed_witnesses),
        "endpoint_cases": len(endpoints),
        "external_signed_composite_cases": len(signed_composite_witnesses),
        "elapsed_seconds": time.monotonic() - started,
        "cases": rows,
        "external_signed_tail_witnesses": signed_witnesses,
        "endpoint_witnesses": endpoints,
        "external_signed_composite_witnesses": signed_composite_witnesses,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(
        json.dumps(
            {
                k: v
                for k, v in record.items()
                if k
                not in (
                    "cases",
                    "external_signed_tail_witnesses",
                    "endpoint_witnesses",
                    "external_signed_composite_witnesses",
                )
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
