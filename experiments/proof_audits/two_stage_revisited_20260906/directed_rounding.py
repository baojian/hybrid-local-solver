"""Exact audit of bounded-state rounding, the reporter, and fixed pruning.

This implements the rounded recurrence using rational arithmetic to make every
rounding direction and tie exact. The stored state is dyadic and is rebased;
it does not follow an ever-growing exact rational trajectory. Python label
dictionaries are audit conveniences, not a deterministic map complexity claim.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import heapq
import json
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .orthant_continuation import ExactObstacle, dot, mv, solve, sub
from .sparse_state import GraphOracle, ImplicitStar, SparseCooling


def floor_grid(value, grid):
    return (value // grid) * grid


def ceil_grid(value, grid):
    return -((-value) // grid) * grid


class RoundedCooling(SparseCooling):
    def __init__(self, oracle, seed, alpha, epsilon, *, prune=False, grid=None):
        self.prune = prune
        self.neighbor_low = {}
        super().__init__(oracle, seed, alpha, epsilon)
        self.tau = alpha * epsilon**2 / 32
        grid_bound = min(F(1, 16), self.theta, self.theta * alpha**2 * self.rho / 256)
        grid_bound = min(grid_bound, self.theta * self.tau / 512)
        self.h = F(1)
        while self.h > grid_bound:
            self.h /= 2
        if grid is not None:
            self.h = grid
        self.gamma = 256 * self.h / self.theta
        self.cooling_grid = self.theta * self.rho / 8

    def allowed(self, label):
        return not self.prune or self.degree(label) * self.rho <= 1

    def refresh(self, label):
        if not self.allowed(label):
            return
        self.response[label] = (self.diagonal - self.mu) * self.x_normalized.get(label, F(0))
        self.response[label] -= (
            self.offdiagonal * self.neighbor_low.get(label, F(0)) / self.degree(label)
        )
        super().refresh(label)

    def step(self):
        theta, h = self.theta, self.h
        lam = self.alpha * self.r
        threshold = (lam + h) / (theta * self.sigma)
        next_kinetic = {}
        while self.heap:
            negative_key, label, version = self.heap[0]
            self.counts["heap_top_reads"] += 1
            if self.versions[label] != version:
                heapq.heappop(self.heap)
                self.counts["stale_heap_pops"] += 1
                continue
            if -negative_key < threshold:
                break
            heapq.heappop(self.heap)
            self.counts["positive_heap_pops"] += 1
            raw = self.sigma * (-negative_key) - lam / theta
            value = floor_grid(raw, h / theta)
            assert value > 0
            next_kinetic[label] = value

        scale = floor_grid(self.chi * self.sigma, h)
        assert scale > 0
        touched = set(self.kinetic) | set(self.kinetic_response) | {self.seed}
        rebase = scale < F(1, 2)
        if rebase:
            for label, value in self.x_normalized.items():
                self.x_normalized[label] = floor_grid(scale * value, h)
                self.counts["rebase_primal_cells"] += 1
            for label, value in self.neighbor_low.items():
                self.neighbor_low[label] = max(
                    F(0), floor_grid(scale * value, h) - self.degree(label) * h
                )
                self.counts["rebase_neighbor_cells"] += 1
            scale = F(1)
            self.counts["rebases"] += 1
        next_response = {}

        def scatter_response(label, amount):
            next_response[label] = next_response.get(label, F(0)) + amount
            touched.add(label)
            self.counts["response_cell_updates"] += 1

        for label, value in next_kinetic.items():
            delta = floor_grid(theta * value / scale, h)
            assert scale * delta >= theta * value / 2
            self.x_normalized[label] = self.x_normalized.get(label, F(0)) + delta
            self.counts["primal_cell_updates"] += 1
            scatter_response(label, (self.diagonal - self.mu) * value)
            for neighbor in self.scan(label):
                if self.allowed(neighbor):
                    self.neighbor_low[neighbor] = self.neighbor_low.get(neighbor, F(0)) + delta
                    self.counts["neighbor_cell_updates"] += 1
                    scatter_response(neighbor, -self.offdiagonal * value / self.degree(neighbor))
        self.sigma = scale
        self.kinetic = next_kinetic
        self.kinetic_response = next_response
        if rebase:
            self.heap.clear()
            self.keys.clear()
            self.versions.clear()
            touched = set(self.degrees)
        for label in touched:
            self.refresh(label)
        self.inverse_r_sum += 1 / self.r
        self.steps += 1
        self.counts["max_heap_records"] = max(self.counts["max_heap_records"], len(self.heap))
        assert self.counts["all_adjacency_incidences"] <= 60 * self.inverse_r_sum

    def run(self, callback=None):
        if self.rho >= self.r or self.alpha == 1:
            return super().run(callback)
        while self.r > self.rho:
            old_r = self.r
            self.step()
            self.r = max(self.rho, ceil_grid(self.eta * self.r, self.cooling_grid))
            assert self.eta * old_r <= self.r < old_r
            if callback:
                callback(self, old_r)
        self.counts["cooling_steps"] = self.steps
        doubling = 1
        blocks = 0
        while doubling * self.epsilon < 416:
            doubling *= 2
            blocks += 1
        for _ in range(blocks * int(1 / self.theta)):
            self.step()
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


def check_case(graph, seed, alpha, epsilon, *, prune=False):
    labels = [i for i in graph if not prune or graph.degree(i) * epsilon / 2 <= 1]
    if seed not in labels:
        labels = [seed]  # Constant zero branch; no recurrence uses this matrix.
    degrees = [graph.degree(i) for i in labels]
    n = len(labels)
    matrix = [
        [
            (1 + alpha) / 2
            if i == j
            else -(1 - alpha) / (2 * graph.degree(i))
            if graph.has_edge(i, j)
            else F(0)
            for j in labels
        ]
        for i in labels
    ]
    source = [alpha / graph.degree(i) if i == seed else F(0) for i in labels]
    state = RoundedCooling(GraphOracle(graph), seed, alpha, epsilon, prune=prune)
    previous_x = [F(0)] * n
    previous_z = previous_x.copy()
    previous_low = previous_x.copy()
    previous_sigma = F(1)
    reference = ExactObstacle(matrix, source)
    t = solve(matrix, source)
    ones = [F(1)] * n
    max_deficit = F(0)
    max_primal_mass = F(0)
    maximum_bits = 0
    lost_ideal_positives = 0
    selected_slack = F(0)
    selected_force = F(0)
    previous_excess = F(0)

    def objective(x, lam):
        return dot(degrees, x, mv(matrix, x)) / 2 - dot(degrees, sub(source, [lam] * n), x)

    def bank(x, z, lam):
        residual = sub(mv(matrix, x), source)
        dz = sub(z, t)
        return (
            dot(degrees, residual, residual) / 2
            + lam * dot(degrees, mv(matrix, x), ones)
            - alpha * lam
            + state.mu * dot(degrees, dz, mv(matrix, dz)) / 2
        )

    def callback(actual, old_r):
        nonlocal previous_x, previous_z, previous_low, previous_sigma
        nonlocal max_deficit, max_primal_mass, maximum_bits, lost_ideal_positives
        nonlocal selected_slack, selected_force, previous_excess
        theta, mu, chi, h = actual.theta, actual.mu, actual.chi, actual.h
        lam = alpha * old_r
        next_lam = alpha * actual.r
        current = actual.materialize()
        x = [current.get(i, F(0)) for i in labels]
        z = [actual.kinetic.get(i, F(0)) for i in labels]
        y = [(xi + theta * zi) / (1 + theta) for xi, zi in zip(previous_x, previous_z)]
        gradient = [v - b + lam for v, b in zip(mv(matrix, y), source)]
        raw = [chi * zi + theta * yi - gi / theta for zi, yi, gi in zip(previous_z, y, gradient)]
        represented_raw = []
        for j, label in enumerate(labels):
            actual_neighbor_sum = sum(
                previous_x[k] / previous_sigma
                for k, neighbor in enumerate(labels)
                if graph.has_edge(label, neighbor)
            )
            deficit = actual_neighbor_sum - previous_low[j]
            error = (
                -previous_sigma * actual.offdiagonal * deficit / (theta * (1 + theta) * degrees[j])
            )
            assert -2 * h / theta <= error <= 0
            represented_raw.append(raw[j] + error)
        p0 = [max(F(0), value) for value in represented_raw]
        assert z == [floor_grid(value, h / theta) for value in p0]
        for xi, old_xi, zi in zip(x, previous_x, z):
            assert -8 * h <= xi - chi * old_xi - theta * zi <= 0
            assert xi >= theta * zi / 2
        lost_ideal_positives += sum(a > 0 and b == 0 for a, b in zip(p0, z))
        mass = dot(degrees, x, ones)
        max_primal_mass = max(max_primal_mass, mass)
        assert 0 <= mass <= 3
        assert dot(degrees, z, ones) <= 6 / theta
        opt, _ = reference.at(lam)
        next_opt, _ = reference.at(next_lam)
        old_e = objective(previous_x, lam) - objective(opt, lam)
        old_e += mu * dot(degrees, sub(previous_z, opt), sub(previous_z, opt)) / 2
        new_e = objective(x, lam) - objective(opt, lam)
        new_e += mu * dot(degrees, sub(z, opt), sub(z, opt)) / 2
        assert 0 <= new_e <= chi * old_e + 256 * h
        old_b = bank(previous_x, previous_z, lam)
        fixed_b = bank(x, z, lam)
        assert fixed_b <= chi * old_b + 256 * h
        current_b = bank(x, z, next_lam)
        assert current_b <= chi * old_b + 256 * h + alpha * (lam - next_lam)
        assert current_b <= alpha * next_lam + actual.gamma
        response = sub(mv(matrix, x), source)
        assert dot(degrees, response, response) <= 6 * alpha * next_lam
        force_base = sub(previous_x, opt)
        force_density = [
            -(v - mu * e) / (1 + theta) for v, e in zip(mv(matrix, force_base), force_base)
        ]
        slack_density = [v - b + lam for v, b in zip(mv(matrix, opt), source)]
        selected = [j for j in range(n) if z[j] > next_opt[j]]
        excess = theta * sum(degrees[j] * max(F(0), z[j] - next_opt[j]) for j in range(n))
        slack = sum(degrees[j] * slack_density[j] for j in selected)
        force = sum(degrees[j] * force_density[j] for j in selected)
        beta0 = (1 - alpha) / (1 + theta)
        assert excess + slack <= beta0 * previous_excess + force
        selected_slack += slack / lam
        selected_force += force / lam
        assert selected_slack <= selected_force
        previous_excess = excess
        normalized = [actual.x_normalized.get(i, F(0)) for i in labels]
        low = [actual.neighbor_low.get(i, F(0)) for i in labels]
        for j, label in enumerate(labels):
            neighbor_sum = sum(
                normalized[k]
                for k, neighbor in enumerate(labels)
                if graph.has_edge(label, neighbor)
            )
            deficit = (neighbor_sum - low[j]) / degrees[j]
            assert 0 <= deficit <= 4 * h
            max_deficit = max(max_deficit, deficit / h)
            if label in actual.keys:
                q_response = (actual.diagonal - mu) * normalized[j] - actual.offdiagonal * low[
                    j
                ] / degrees[j]
                kinetic_response = mv(matrix, z)[j] - mu * z[j]
                key = -q_response / (theta * (1 + theta))
                key += (
                    chi * z[j] - kinetic_response / (1 + theta) + source[j] / theta
                ) / actual.sigma
                assert key == actual.keys[label]
        assert F(1, 2) <= actual.sigma <= 1
        for value in normalized + low + z + [actual.sigma]:
            assert (value / h).denominator == 1
            maximum_bits = max(
                maximum_bits, value.numerator.bit_length(), value.denominator.bit_length()
            )
        previous_x, previous_z = x, z
        previous_low, previous_sigma = low, actual.sigma

    answer = state.run(callback)
    full_labels = list(graph)
    full_matrix = [
        [
            (1 + alpha) / 2
            if i == j
            else -(1 - alpha) / (2 * graph.degree(i))
            if graph.has_edge(i, j)
            else F(0)
            for j in full_labels
        ]
        for i in full_labels
    ]
    full_source = [alpha / graph.degree(i) if i == seed else F(0) for i in full_labels]
    full_ppr = solve(full_matrix, full_source)
    full_opt, _ = ExactObstacle(full_matrix, full_source).at(alpha * epsilon / 2)
    result = [answer.get(i, F(0)) for i in full_labels]
    assert all(0 <= a <= b <= c for a, b, c in zip(result, full_opt, full_ppr))
    semantic_error = max(abs(a - b) for a, b in zip(result, full_ppr))
    assert semantic_error <= epsilon
    if state.steps:
        x = [state.materialize().get(i, F(0)) for i in labels]
        opt, _ = reference.at(alpha * state.rho)
        assert objective(x, alpha * state.rho) - objective(opt, alpha * state.rho) <= state.tau
    if prune:
        assert all(graph.degree(i) * state.rho <= 1 for i in state.rows)
    return {
        "n": len(graph),
        "seed": seed,
        "alpha": str(alpha),
        "eps_ppr": str(epsilon),
        "fixed_pruning": prune,
        "grid": str(state.h),
        "steps": state.steps,
        "max_neighbor_deficit_over_grid": float(max_deficit),
        "max_primal_mass": float(max_primal_mass),
        "max_stored_fraction_bits": maximum_bits,
        "rounded_away_ideal_positives": lost_ideal_positives,
        "semantic_error": float(semantic_error),
        "counts": dict(state.counts),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--alphas", default="1/4,1/16")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    source_record = provenance({"max_n": args.max_n, "alphas": args.alphas}, args.output)
    rows = []
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in map(F, args.alphas.split(",")):
                for prune in (False, True):
                    row = check_case(graph, seed, alpha, F(1, 8), prune=prune)
                    row["atlas_id"] = atlas_id
                    rows.append(row)
    for graph, seed in ((nx.path_graph(6), 0), (nx.star_graph(20), 1), (nx.star_graph(20), 0)):
        for alpha in (F(1), F(3, 4), F(1, 256)):
            for prune in (False, True):
                rows.append(check_case(graph, seed, alpha, F(1, 4), prune=prune))
    stars = []
    for leaves in (10**6, 10**12):
        for prune in (False, True):
            run = RoundedCooling(ImplicitStar(leaves), 1, F(1, 256), F(1, 4), prune=prune)
            output = run.run()
            assert 0 not in run.rows and set(output) <= {1}
            assert len(run.degrees) == 2
            stars.append({"leaves": leaves, "fixed_pruning": prune, "counts": dict(run.counts)})
    record = {
        "provenance": source_record,
        "status": "passed",
        "arithmetic": "exact dyadic rounding via rationals",
        "case_count": len(rows),
        "huge_star_cases": len(stars),
        "elapsed_seconds": time.monotonic() - started,
        "cases": rows,
        "stars": stars,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k not in ("cases", "stars")}), flush=True)


if __name__ == "__main__":
    main()
