"""Exact audit of the independent RPPR objective stopping and clipping rule."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .directed_rounding import RoundedCooling, ceil_grid
from .orthant_continuation import ExactObstacle, dot, mv, sub
from .sparse_state import GraphOracle, SparseCooling


def check_case(graph, seed, alpha, rho, objective_epsilon, rounded):
    # The common step routines are driven with this independent rho and delta.
    # Their semantic-PPR run() methods are deliberately not used here.
    implementation = RoundedCooling if rounded else SparseCooling
    state = implementation(GraphOracle(graph), seed, alpha, F(1, 2))
    state.rho = rho
    delta = F(1, 2)
    while delta**2 > objective_epsilon * rho / 2:
        delta /= 2
    tau = alpha * delta**2 / 2
    if rounded:
        bound = min(F(1, 16), state.theta, state.theta * alpha**2 * rho / 256)
        bound = min(bound, state.theta * tau / 512)
        state.h = F(1)
        while state.h > bound:
            state.h /= 2
        state.gamma = 256 * state.h / state.theta
        state.cooling_grid = state.theta * rho / 8
    n = len(graph)
    degrees = [graph.degree(i) for i in range(n)]
    matrix = [
        [
            (1 + alpha) / 2
            if i == j
            else -(1 - alpha) / (2 * degrees[i])
            if graph.has_edge(i, j)
            else F(0)
            for j in range(n)
        ]
        for i in range(n)
    ]
    source = [alpha / degrees[i] if i == seed else F(0) for i in range(n)]
    optimum, _ = ExactObstacle(matrix, source).at(alpha * rho)

    def objective(x):
        return dot(degrees, x, mv(matrix, x)) / 2 - dot(degrees, sub(source, [alpha * rho] * n), x)

    frozen_steps = 0
    if rho * degrees[seed] >= 1:
        answer = {}
    elif alpha == 1:
        answer = {seed: F(1, degrees[seed]) - rho}
    else:
        while state.r > rho:
            state.step()
            state.r = max(
                rho,
                ceil_grid(state.eta * state.r, state.cooling_grid)
                if rounded
                else state.eta * state.r,
            )
        bound = (13 if rounded else 9) * alpha * rho
        primal = [state.materialize().get(i, F(0)) for i in range(n)]
        kinetic = [state.kinetic.get(i, F(0)) for i in range(n)]
        energy = objective(primal) - objective(optimum)
        energy += state.mu * dot(degrees, sub(kinetic, optimum), sub(kinetic, optimum)) / 2
        assert energy <= bound
        if rounded:
            doubling, blocks = 1, 0
            while doubling * tau < 2 * bound:
                doubling *= 2
                blocks += 1
            frozen_steps = blocks * int(1 / state.theta)
            for _ in range(frozen_steps):
                state.step()
        else:
            while bound > tau:
                state.step()
                bound *= state.chi
                frozen_steps += 1
        primal = [state.materialize().get(i, F(0)) for i in range(n)]
        assert objective(primal) - objective(optimum) <= tau
        assert dot(degrees, sub(primal, optimum), sub(primal, optimum)) <= delta**2
        answer = {}
        for label, value in state.materialize().items():
            state.counts["terminal_materialized_cells"] += 1
            if value > delta:
                answer[label] = value - delta
    output = [answer.get(i, F(0)) for i in range(n)]
    assert all(0 <= x <= u for x, u in zip(output, optimum))
    gap = objective(output) - objective(optimum)
    difference = sub(output, optimum)
    assert gap == dot(degrees, difference, mv(matrix, difference)) / 2
    assert 0 <= gap <= objective_epsilon
    volume = sum(degrees[i] for i in answer)
    assert volume <= 1 / rho
    residual = sub(source, mv(matrix, output))
    kkt_density = max(
        abs(alpha * rho - value) if coordinate > 0 else max(F(0), value - alpha * rho)
        for coordinate, value in zip(output, residual)
    )
    assert kkt_density <= 2 * delta
    positive_residual_certified = delta <= alpha * rho / 2
    if positive_residual_certified:
        assert all(0 <= value <= 2 * alpha * rho for value in residual)
    values = (
        list(state.x_normalized.values()) + list(state.kinetic.values()) + [state.sigma, state.r]
    )
    max_bits = max(
        max(value.numerator.bit_length(), value.denominator.bit_length()) for value in values
    )
    return {
        "n": n,
        "seed": seed,
        "alpha": str(alpha),
        "rho": str(rho),
        "objective_epsilon": str(objective_epsilon),
        "rounded": rounded,
        "delta": str(delta),
        "steps": state.steps,
        "frozen_steps": frozen_steps,
        "objective_gap": float(gap),
        "output_volume": volume,
        "positive_residual_certified": positive_residual_certified,
        "normalized_kkt_over_alpha": float(kkt_density / alpha),
        "max_final_state_fraction_bits": max_bits,
        "counts": dict(state.counts),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    source_record = provenance({"max_n": args.max_n}, args.output)
    cases = []
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in (F(1, 4), F(1, 64)):
                for rho_factor in (4, 32):
                    rho = F(1, rho_factor * graph.degree(seed))
                    for epsilon in (F(1, 100), F(1, 10**6), alpha**2 * rho / 2):
                        for rounded in (False, True):
                            row = check_case(graph, seed, alpha, rho, epsilon, rounded)
                            row["atlas_id"] = atlas_id
                            cases.append(row)
    for alpha in (F(1), F(3, 4)):
        for rho in (F(1, 8), F(1), F(2)):
            for rounded in (False, True):
                cases.append(check_case(nx.path_graph(4), 0, alpha, rho, F(1, 100), rounded))
    record = {
        "provenance": source_record,
        "status": "passed",
        "arithmetic": "exact rational and specified dyadic rounding",
        "case_count": len(cases),
        "elapsed_seconds": time.monotonic() - started,
        "cases": cases,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
