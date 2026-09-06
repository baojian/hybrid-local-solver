"""Exact audit of source-density truncation and joint sparse-source acceleration."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .directed_rounding import RoundedCooling, ceil_grid, floor_grid
from .orthant_continuation import ExactObstacle, dot, mv, solve, sub
from .sparse_state import GraphOracle, ImplicitStar, SparseCooling


class MultiSourceMixin:
    def __init__(self, oracle, weights, alpha, retained_epsilon, **kwargs):
        assert weights and all(weight > 0 for weight in weights.values())
        self.source_weights = dict(weights)
        super().__init__(oracle, next(iter(weights)), alpha, retained_epsilon, **kwargs)
        self.r = max(weight / self.degree(label) for label, weight in weights.items())
        for label in weights:
            self.refresh(label)

    def source_density(self, label):
        return self.alpha * self.source_weights.get(label, F(0)) / self.degree(label)

    def step(self):
        super().step()
        for label in self.source_weights:
            self.refresh(label)
            self.counts["retained_source_refreshes"] += 1

    def run(self, callback=None):
        if self.rho >= self.r:
            return {}
        if self.alpha == 1:
            output = {
                label: weight / self.degree(label) - self.rho
                for label, weight in self.source_weights.items()
                if weight / self.degree(label) > self.rho
            }
            self.counts["output_cells"] = len(output)
            self.counts["output_volume"] = sum(self.degree(i) for i in output)
            return output
        return super().run(callback)


class MultiSourceExact(MultiSourceMixin, SparseCooling):
    pass


class MultiSourceRounded(MultiSourceMixin, RoundedCooling):
    pass


def prepare_source(oracle, weights, epsilon):
    retained = {}
    for label, weight in weights.items():
        degree = oracle.degree(label)
        if weight / degree > epsilon / 2:
            retained[label] = weight
    return retained


def run_acl(state, callback=None):
    if state.alpha == 1 or state.rho >= state.r:
        return state.run(callback)
    rounded = isinstance(state, RoundedCooling)
    delta = state.alpha * state.epsilon / 4
    tau = state.alpha * delta**2 / 2
    if rounded:
        bound = min(F(1, 16), state.theta, state.theta * state.alpha**2 * state.rho / 256)
        bound = min(bound, state.theta * tau / 512)
        state.h = F(1)
        while state.h > bound:
            state.h /= 2
        state.gamma = 256 * state.h / state.theta
    while state.r > state.rho:
        old_r = state.r
        state.step()
        state.r = max(
            state.rho,
            ceil_grid(state.eta * state.r, state.cooling_grid) if rounded else state.eta * state.r,
        )
        if callback:
            callback(state, old_r)
    bound = (13 if rounded else 9) * state.alpha * state.rho
    if rounded:
        doubling, blocks = 1, 0
        while doubling * tau < 2 * bound:
            doubling *= 2
            blocks += 1
        for _ in range(blocks * int(1 / state.theta)):
            state.step()
            if callback:
                callback(state, state.r)
    else:
        while bound > tau:
            state.step()
            bound *= state.chi
            if callback:
                callback(state, state.r)
    output = {}
    for label, value in state.materialize().items():
        state.counts["terminal_materialized_cells"] += 1
        if value > delta:
            output[label] = value - delta
    state.counts["output_cells"] = len(output)
    state.counts["output_volume"] = sum(state.degree(i) for i in output)
    return output


def check_case(graph, weights, alpha, epsilon, *, rounded, acl):
    assert sum(weights.values()) == 1
    n = len(graph)
    degree = [graph.degree(i) for i in range(n)]
    oracle = GraphOracle(graph)
    hot = prepare_source(oracle, weights, epsilon)
    assert sum(degree[i] for i in hot) < 2 / epsilon
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
    source = [alpha * hot.get(i, F(0)) / degree[i] for i in range(n)]
    full_source = [alpha * weights.get(i, F(0)) / degree[i] for i in range(n)]
    full_ppr = solve(matrix, full_source)
    retained_ppr = solve(matrix, source)
    assert all(0 <= a - b <= epsilon / 2 for a, b in zip(full_ppr, retained_ppr))
    previous_x = [F(0)] * n
    previous_z = previous_x.copy()
    previous_low = previous_x.copy()
    previous_sigma = F(1)
    mass = sum(hot.values())
    ones = [F(1)] * n
    state = None

    def bank(x, z, lam):
        residual = sub(mv(matrix, x), source)
        dz = sub(z, retained_ppr)
        return (
            dot(degree, residual, residual) / 2
            + alpha * lam * (dot(degree, x, ones) - mass)
            + state.mu * dot(degree, dz, mv(matrix, dz)) / 2
        )

    def callback(actual, old_r):
        nonlocal previous_x, previous_z, previous_low, previous_sigma
        theta, chi = actual.theta, actual.chi
        lam = alpha * old_r
        y = [(x + theta * z) / (1 + theta) for x, z in zip(previous_x, previous_z)]
        gradient = [a - b + lam for a, b in zip(mv(matrix, y), source)]
        raw = [chi * z + theta * yi - g / theta for z, yi, g in zip(previous_z, y, gradient)]
        if rounded:
            for i in range(n):
                neighbor_sum = sum(previous_x[j] / previous_sigma for j in graph.neighbors(i))
                deficit = neighbor_sum - previous_low[i]
                raw[i] -= (
                    previous_sigma
                    * actual.offdiagonal
                    * deficit
                    / (theta * (1 + theta) * degree[i])
                )
            expected_z = [floor_grid(max(F(0), q), actual.h / theta) for q in raw]
        else:
            expected_z = [max(F(0), q) for q in raw]
        z = [actual.kinetic.get(i, F(0)) for i in range(n)]
        assert z == expected_z
        x = [actual.materialize().get(i, F(0)) for i in range(n)]
        for value, old, kinetic in zip(x, previous_x, z):
            error = value - chi * old - theta * kinetic
            assert (-8 * actual.h <= error <= 0) if rounded else error == 0
        error_budget = 256 * actual.h if rounded else F(0)
        assert bank(x, z, lam) <= chi * bank(previous_x, previous_z, lam) + error_budget
        next_lam = alpha * actual.r
        gamma = actual.gamma if rounded else F(0)
        assert bank(x, z, next_lam) <= alpha * next_lam + gamma
        assert dot(degree, x, ones) <= (3 if rounded else 2)
        if rounded:
            normalized = [actual.x_normalized.get(i, F(0)) for i in range(n)]
            low = [actual.neighbor_low.get(i, F(0)) for i in range(n)]
            for i in range(n):
                deficit = sum(normalized[j] for j in graph.neighbors(i)) - low[i]
                assert 0 <= deficit <= 4 * degree[i] * actual.h
            previous_low = low
        previous_x, previous_z, previous_sigma = x, z, actual.sigma
        assert actual.counts["retained_source_refreshes"] == actual.steps * len(hot)

    if hot:
        implementation = MultiSourceRounded if rounded else MultiSourceExact
        state = implementation(oracle, hot, alpha, epsilon / 2)
        answer = run_acl(state, callback) if acl else state.run(callback)
    else:
        answer = {}
    output = [answer.get(i, F(0)) for i in range(n)]
    optimum, _ = ExactObstacle(matrix, source).at(alpha * epsilon / 4)
    assert all(0 <= a <= b <= c for a, b, c in zip(output, optimum, full_ppr))
    error = max(abs(a - b) for a, b in zip(output, full_ppr))
    assert error <= epsilon
    if acl:
        residual = sub(full_source, mv(matrix, output))
        assert all(0 <= value <= alpha * epsilon for value in residual)
    return {
        "n": n,
        "source": {str(i): str(weight) for i, weight in weights.items()},
        "alpha": str(alpha),
        "eps_ppr": str(epsilon),
        "rounded": rounded,
        "acl": acl,
        "input_source_count": len(weights),
        "input_degree_queries": len(weights),
        "retained_source_count": len(hot),
        "retained_source_mass": str(mass),
        "semantic_error": float(error),
        "counts": dict(state.counts) if state else {},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    source_record = provenance({"max_n": args.max_n}, args.output)
    cases = []
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        n = len(graph)
        sources = [
            {i: F(1, n) for i in graph},
            {0: F(1, 3), n - 1: F(2, 3)},
            {i: F(2 * (i + 1), n * (n + 1)) for i in graph},
        ]
        for weights in sources:
            for alpha in (F(1), F(1, 4), F(1, 64)):
                for rounded in (False, True):
                    for acl in (False, True):
                        row = check_case(graph, weights, alpha, F(1, 4), rounded=rounded, acl=acl)
                        row["atlas_id"] = atlas_id
                        cases.append(row)
    huge = []
    weights = {1: F(1, 2)} | {i: F(1, 1998) for i in range(2, 1001)}
    for rounded in (False, True):
        for acl in (False, True):
            oracle = ImplicitStar(10**12)
            hot = prepare_source(oracle, weights, F(1, 32))
            assert hot == {1: F(1, 2)}
            implementation = MultiSourceRounded if rounded else MultiSourceExact
            state = implementation(oracle, hot, F(1, 4), F(1, 64))
            answer = run_acl(state) if acl else state.run()
            assert set(answer) <= {1} and 0 not in state.rows
            huge.append(
                {
                    "rounded": rounded,
                    "acl": acl,
                    "source_input_count": len(weights),
                    "counts": dict(state.counts),
                }
            )
    record = {
        "provenance": source_record,
        "status": "passed",
        "arithmetic": "exact rational and specified dyadic rounding",
        "case_count": len(cases),
        "implicit_star_cases": len(huge),
        "elapsed_seconds": time.monotonic() - start,
        "cases": cases,
        "huge": huge,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k not in ("cases", "huge")}), flush=True)


if __name__ == "__main__":
    main()
