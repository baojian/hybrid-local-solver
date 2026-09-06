"""Exact lazy-state and terminal-output audit for gradual orthant acceleration.

The heap is an actual output-sensitive reporter. Python dictionaries stand in
for the label maps that the theorem implements with deterministic balanced
trees. Counts distinguish row/edge work from heap and scalar-state events;
Python timing is not claimed to establish a worst-case word-work theorem.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import heapq
import json
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .orthant_continuation import ExactObstacle, dot, mv, solve


class GraphOracle:
    def __init__(self, graph):
        self.graph = graph

    def degree(self, label):
        return self.graph.degree(label)

    def neighbors(self, label):
        return iter(self.graph.neighbors(label))


class ImplicitStar:
    """A unit-weight star with arbitrarily many leaves, without building it."""

    def __init__(self, leaves):
        self.leaves = leaves

    def degree(self, label):
        assert 0 <= label <= self.leaves
        return self.leaves if label == 0 else 1

    def neighbors(self, label):
        if label == 0:
            return iter(range(1, self.leaves + 1))
        return iter((0,))


class SparseCooling:
    """Audit implementation: exact degree densities and explicitly metered rows."""

    def __init__(self, oracle, seed, alpha, epsilon, *, max_row=1_000_000):
        assert 0 < alpha <= 1 and 0 < epsilon < 1
        self.oracle = oracle
        self.seed = seed
        self.alpha = alpha
        self.epsilon = epsilon
        self.rho = epsilon / 2
        self.max_row = max_row
        self.counts = Counter()
        self.degrees = {}
        self.rows = {}
        seed_degree = self.degree(seed)
        self.r = F(1, seed_degree)
        self.theta = F(1, 2)
        while self.theta**2 > alpha:
            self.theta /= 2
        self.mu = self.theta**2
        self.chi = 1 - self.theta
        self.eta = 1 - self.theta / 2
        self.diagonal = (1 + alpha) / 2
        self.offdiagonal = (1 - alpha) / 2
        self.sigma = F(1)
        self.x_normalized = {}
        self.response = {}
        self.kinetic = {}
        self.kinetic_response = {}
        self.versions = {}
        self.keys = {}
        self.heap = []
        self.inverse_r_sum = F(0)
        self.steps = 0
        self.refresh(seed)

    def degree(self, label):
        if label not in self.degrees:
            self.degrees[label] = self.oracle.degree(label)
            self.counts["degree_queries"] += 1
        return self.degrees[label]

    def scan(self, label):
        degree = self.degree(label)
        if degree > self.max_row:
            raise AssertionError(f"Unexpected high-degree row activation: {label}, degree={degree}")
        if label not in self.rows:
            self.rows[label] = tuple(self.oracle.neighbors(label))
            assert len(self.rows[label]) == degree
            self.counts["first_adjacency_incidences"] += degree
        self.counts["all_adjacency_incidences"] += degree
        self.counts["row_operations"] += 1
        for neighbor in self.rows[label]:
            self.degree(neighbor)
            yield neighbor

    def source_density(self, label):
        return self.alpha / self.degree(label) if label == self.seed else F(0)

    def refresh(self, label):
        theta = self.theta
        key = -self.response.get(label, F(0)) / (theta * (1 + theta))
        key += (
            self.chi * self.kinetic.get(label, F(0))
            - self.kinetic_response.get(label, F(0)) / (1 + theta)
            + self.source_density(label) / theta
        ) / self.sigma
        version = self.versions.get(label, 0) + 1
        self.versions[label] = version
        self.keys[label] = key
        heapq.heappush(self.heap, (-key, label, version))
        self.counts["key_refreshes"] += 1

    def step(self):
        theta = self.theta
        lam = self.alpha * self.r
        threshold = lam / (theta * self.sigma)
        next_kinetic = {}
        while self.heap:
            negative_key, label, version = self.heap[0]
            self.counts["heap_top_reads"] += 1
            if self.versions[label] != version:
                heapq.heappop(self.heap)
                self.counts["stale_heap_pops"] += 1
                continue
            if -negative_key <= threshold:
                break
            heapq.heappop(self.heap)
            self.counts["positive_heap_pops"] += 1
            next_kinetic[label] = self.sigma * (-negative_key) - lam / theta
            assert next_kinetic[label] > 0
        next_sigma = self.sigma * self.chi
        touched = set(self.kinetic) | set(self.kinetic_response) | {self.seed}
        next_response = {}

        def scatter(label, kinetic_delta, primal_delta):
            next_response[label] = next_response.get(label, F(0)) + kinetic_delta
            self.response[label] = self.response.get(label, F(0)) + primal_delta
            touched.add(label)
            self.counts["response_cell_updates"] += 1

        for label, value in next_kinetic.items():
            delta = theta * value / next_sigma
            self.x_normalized[label] = self.x_normalized.get(label, F(0)) + delta
            self.counts["primal_cell_updates"] += 1
            scatter(label, (self.diagonal - self.mu) * value, (self.diagonal - self.mu) * delta)
            for neighbor in self.scan(label):
                coefficient = -self.offdiagonal / self.degree(neighbor)
                scatter(neighbor, coefficient * value, coefficient * delta)
        self.sigma = next_sigma
        self.kinetic = next_kinetic
        self.kinetic_response = next_response
        for label in touched:
            self.refresh(label)
        self.inverse_r_sum += 1 / self.r
        self.steps += 1
        self.counts["max_heap_records"] = max(self.counts["max_heap_records"], len(self.heap))
        assert self.counts["all_adjacency_incidences"] <= 44 * self.inverse_r_sum

    def materialize(self):
        return {i: self.sigma * value for i, value in self.x_normalized.items()}

    def run(self, callback=None):
        if self.rho >= self.r:
            self.counts["output_cells"] = 0
            self.counts["output_volume"] = 0
            return {}
        if self.alpha == 1:
            self.counts["output_cells"] = 1
            self.counts["output_volume"] = self.degree(self.seed)
            return {self.seed: F(1, self.degree(self.seed)) - self.rho}
        while self.r > self.rho:
            old_r = self.r
            self.step()
            self.r = max(self.rho, self.eta * self.r)
            if callback:
                callback(self, old_r)
        self.counts["cooling_steps"] = self.steps
        bound = 9 * self.alpha * self.rho
        tau = self.alpha * self.epsilon**2 / 32
        while bound > tau:
            self.step()
            bound *= self.chi
            if callback:
                callback(self, self.r)
        answer = {}
        for label, value in self.x_normalized.items():
            clipped = self.sigma * value - self.epsilon / 4
            self.counts["terminal_materialized_cells"] += 1
            if clipped > 0:
                answer[label] = clipped
        self.counts["output_cells"] = len(answer)
        self.counts["output_volume"] = sum(self.degree(i) for i in answer)
        assert self.counts["output_volume"] <= 2 / self.epsilon
        return answer


def compare_dense(graph, seed, alpha, epsilon):
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
    sparse = SparseCooling(GraphOracle(graph), seed, alpha, epsilon)
    dense_x = [F(0)] * n
    dense_z = dense_x.copy()
    older_x = dense_x.copy()

    def callback(state, r):
        nonlocal dense_x, dense_z, older_x
        theta = state.theta
        y = [(a + theta * b) / (1 + theta) for a, b in zip(dense_x, dense_z)]
        m_y = mv(matrix, y)
        raw = [
            state.chi * z + theta * yi - (qi - hi + alpha * r) / theta
            for z, yi, qi, hi in zip(dense_z, y, m_y, source)
        ]
        dense_z = [max(F(0), q) for q in raw]
        next_x = [state.chi * x + theta * z for x, z in zip(dense_x, dense_z)]
        beta = state.chi / (1 + theta)
        extrapolated = [x + beta * (x - old) for x, old in zip(dense_x, older_x)]
        assert y == extrapolated
        floor_step = [
            max(state.chi * x, yi - qi + hi - alpha * r)
            for x, yi, qi, hi in zip(dense_x, y, m_y, source)
        ]
        assert next_x == floor_step
        older_x, dense_x = dense_x, next_x
        actual = state.materialize()
        assert dense_x == [actual.get(i, F(0)) for i in range(n)]
        assert dense_z == [state.kinetic.get(i, F(0)) for i in range(n)]
        assert dot(degrees, dense_x, [F(1)] * n) <= 2
        for i in state.keys:
            density = state.sigma * state.keys[i] - alpha * state.r / theta
            x_y = [(a + theta * b) / (1 + theta) for a, b in zip(dense_x, dense_z)]
            gradient = mv(matrix, x_y)
            direct = state.chi * dense_z[i] + theta * x_y[i]
            direct -= (gradient[i] - source[i] + alpha * state.r) / theta
            assert direct == density

    answer = sparse.run(callback)
    ppr = solve(matrix, source)
    optimum, _ = ExactObstacle(matrix, source).at(alpha * epsilon / 2)
    output = [answer.get(i, F(0)) for i in range(n)]
    assert all(0 <= a <= b <= c for a, b, c in zip(output, optimum, ppr))
    error = max(abs(a - b) for a, b in zip(output, ppr))
    assert error <= epsilon
    return {
        "n": n,
        "seed": seed,
        "alpha": str(alpha),
        "eps_ppr": str(epsilon),
        "steps": sparse.steps,
        "semantic_error": float(error),
        "counts": dict(sparse.counts),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    source_record = provenance({"max_n": args.max_n}, args.output)
    results = []
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in (F(1, 4), F(1, 16)):
                row = compare_dense(graph, seed, alpha, F(1, 8))
                row["atlas_id"] = atlas_id
                results.append(row)
    endpoints = []
    for graph, seed in ((nx.path_graph(4), 0), (nx.star_graph(20), 0)):
        for alpha in (F(1), F(3, 4), F(1, 256)):
            for epsilon in (F(1, 4), F(3, 4)):
                endpoints.append(compare_dense(graph, seed, alpha, epsilon))
    stars = []
    for leaves in (100, 10**6, 10**12):
        for alpha in (F(1, 4), F(1, 16), F(1, 64), F(1, 256)):
            run = SparseCooling(ImplicitStar(leaves), 1, alpha, F(1, 4))
            answer = run.run()
            assert 0 not in run.rows
            assert set(answer) <= {1}
            assert len(run.degrees) == 2
            c = (1 + alpha) / 2
            a = (1 - alpha) / 2
            quotient = [
                [c, -a, F(0)],
                [-a / leaves, c, -a * (leaves - 1) / leaves],
                [F(0), -a, c],
            ]
            true_density = solve(quotient, [alpha, F(0), F(0)])
            output_density = [answer.get(1, F(0)), F(0), F(0)]
            error = max(abs(x - y) for x, y in zip(true_density, output_density))
            assert error <= F(1, 4)
            stars.append(
                {
                    "leaves": leaves,
                    "alpha": str(alpha),
                    "eps_ppr": "1/4",
                    "semantic_error": float(error),
                    "counts": dict(run.counts),
                }
            )
    record = {
        "provenance": source_record,
        "status": "passed",
        "arithmetic": "exact rational",
        "random_seed": None,
        "case_count": len(results),
        "endpoint_cases": len(endpoints),
        "huge_inactive_star_cases": len(stars),
        "elapsed_seconds": time.monotonic() - start,
        "cases": results,
        "endpoints": endpoints,
        "stars": stars,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(
        json.dumps({k: v for k, v in record.items() if k not in ("cases", "stars", "endpoints")}),
        flush=True,
    )


if __name__ == "__main__":
    main()
