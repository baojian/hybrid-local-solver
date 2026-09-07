"""Exact local obstacle solver for a clique with unequal private pendants.

The graph is promised to consist of a clique of at least three core vertices
and private degree-one leaves; the physical seed is in the clique. Core
membership and all core degrees are discovered from the single seed row.
A scalar piecewise-affine fixed-point sweep then determines the entire core
response before any other row is scanned. Only positive rows are scanned.
This is a structural theorem, not an arbitrary-graph solver or bit-cost claim.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from geometric_value_events import obstacle
from local_sun_solver import Oracle
import networkx as nx


class CliquePendantSolver:
    def __init__(self, oracle, seed, alpha, lam):
        assert 0 < alpha < 1 and lam > 0
        self.oracle, self.seed, self.alpha, self.lam = oracle, seed, alpha, lam
        self.gamma, self.bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        self.counts = Counter()
        self.core = []
        self.core_values = {}
        self.pendants = {}
        self.root = F(0)

    def run(self):
        degree = self.oracle.degree(self.seed)
        if self.lam * degree >= 1:
            self.counts["trivial_obstacle_zero_stops"] += 1
            return {}
        seed_row = self.oracle.row(self.seed)
        self.core = [self.seed]
        for neighbor in seed_row:
            if self.oracle.degree(neighbor) > 1:
                self.core.append(neighbor)
            self.counts["seed_neighbor_classifications"] += 1
        k = len(self.core)
        assert k >= 3
        core_set = set(self.core)
        self.counts["core_identifier_words"] += 2 * k
        self.pendants = {i: self.oracle.degree(i) - (k - 1) for i in self.core}
        assert all(t >= 0 for t in self.pendants.values())
        coefficients = {}
        events = []
        slope = F(0)
        offset = F(0)
        for index, i in enumerate(self.core):
            d = self.oracle.degree(i)
            t = self.pendants[i]
            b = F(i == self.seed) - self.lam * d
            a = d + self.gamma
            c = a - self.gamma * self.gamma * t
            assert c >= k - 1 + self.gamma > 0
            pieces = [
                (F(0), F(0)),
                (self.gamma / a, b / a),
                (self.gamma / c, (b - self.gamma * self.lam * t) / c),
            ]
            phase = 0 if b <= 0 else 2 if t and self.gamma * b > self.lam * a else 1
            coefficients[i] = pieces[phase]
            slope += pieces[phase][0]
            offset += pieces[phase][1]
            if phase == 0:
                events.append((-b / self.gamma, index, i, pieces[1]))
            if t and phase < 2:
                events.append(((self.lam * a / self.gamma - b) / self.gamma, index, i, pieces[2]))
            self.counts["core_response_pieces"] += 3
            self.counts["initial_response_words"] += 8
        events.sort(key=lambda item: (item[0], item[1]))
        self.counts["sorted_event_records"] += len(events)
        self.counts["sorting_comparison_budget"] += len(events) * max(1, len(events).bit_length())
        self.counts["event_storage_words"] += 5 * len(events)
        cursor = 0
        while True:
            assert 0 <= slope < 1 and offset > 0
            root = offset / (1 - slope)
            self.counts["scalar_root_candidates"] += 1
            if cursor == len(events) or root <= events[cursor][0]:
                break
            event, _, i, updated = events[cursor]
            cursor += 1
            old = coefficients[i]
            assert old[0] * event + old[1] == updated[0] * event + updated[1]
            slope += updated[0] - old[0]
            offset += updated[1] - old[1]
            coefficients[i] = updated
            self.counts["crossed_response_breakpoints"] += 1
            self.counts["aggregate_coefficient_update_words"] += 8
        self.root = root
        for i in self.core:
            d = self.oracle.degree(i)
            t = self.pendants[i]
            z = F(i == self.seed) - self.lam * d + self.gamma * root
            a = d + self.gamma
            c = a - self.gamma * self.gamma * t
            self.core_values[i] = (
                F(0)
                if z <= 0
                else z / a
                if self.gamma * z <= self.lam * a
                else (z - self.gamma * self.lam * t) / c
            )
            self.counts["final_core_value_words"] += 1
        assert sum(self.core_values.values()) == root
        out = {i: u for i, u in self.core_values.items() if u > 0}
        for i in self.core:
            if self.core_values[i] <= 0:
                continue
            row = seed_row if i == self.seed else self.oracle.row(i)
            leaf_value = max(F(0), self.gamma * self.core_values[i] - self.lam)
            seen_core = 0
            seen_leaf = 0
            for j in row:
                self.counts["active_core_incidence_reads"] += 1
                if j in core_set:
                    seen_core += 1
                    continue
                seen_leaf += 1
                assert self.oracle.degree(j) == 1
                if leaf_value > 0:
                    assert self.oracle.row(j) == [i]
                    out[j] = leaf_value
                    self.counts["positive_pendant_output_words"] += 1
            assert seen_core == k - 1 and seen_leaf == self.pendants[i]
        self.counts["final_output_words"] += len(out)
        return out


def explicit_graph(pendants):
    k = len(pendants)
    graph = nx.complete_graph(k)
    next_vertex = k
    for i, t in enumerate(pendants):
        for _ in range(t):
            graph.add_edge(i, next_vertex)
            next_vertex += 1
    return graph


def check_case(pendants, seed, alpha, lam, counts):
    graph = explicit_graph(pendants)
    state = CliquePendantSolver(Oracle(graph), seed, alpha, lam)
    out = state.run()
    matrix = [
        [F(graph.degree(i)) if i == j else -state.gamma if j in graph[i] else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in graph]
    expected = obstacle(matrix, load)
    vector = [out.get(i, F(0)) for i in graph]
    assert vector == expected
    assert state.oracle.rows == set(out)
    volume = sum(graph.degree(i) for i in out)
    assert lam * volume < 1
    assert state.oracle.counts["adjacency_entries_inspected"] == volume
    for i in graph:
        residual = F(i == seed) - sum(matrix[i][j] * vector[j] for j in graph)
        assert residual >= 0
        assert (
            residual == lam * graph.degree(i)
            if vector[i] > 0
            else residual <= lam * graph.degree(i)
        )
    counts["exact_original_obstacle_comparisons"] += 1
    counts["inactive_core_with_unread_rows"] += sum(i not in out for i in range(len(pendants)))
    counts["nonzero_partial_core_cases"] += bool(out) and any(
        i not in out for i in range(len(pendants))
    )
    counts["zero_seed_gate_cases"] += lam * graph.degree(seed) == 1
    return state


class ImplicitCliquePendants:
    def __init__(self, pendants):
        self.pendants = pendants
        self.k = len(pendants)

    def degree(self, i):
        return 1 if isinstance(i, tuple) else self.k - 1 + self.pendants[i]

    def __getitem__(self, i):
        if isinstance(i, tuple):
            return [i[0]]
        assert self.pendants[i] < 1000, "An inactive enormous pendant row must not be scanned"
        return [j for j in range(self.k) if j != i] + [(i, j) for j in range(self.pendants[i])]


def implicit_cases(counts):
    results = []
    for pendants in [[0, 1, 10**6], [2, 0, 3, 10**12], [0, 2, 0, 4, 10**18]]:
        graph = ImplicitCliquePendants(pendants)
        for alpha in [F(1, 3), F(1, 1009)]:
            lam = F(1, 40)
            state = CliquePendantSolver(Oracle(graph), 0, alpha, lam)
            out = state.run()
            u = {i: out.get(i, F(0)) for i in range(graph.k)}
            total = sum(u.values())
            for i, t in enumerate(pendants):
                leaf = max(F(0), state.gamma * u[i] - lam)
                residual = (
                    F(i == 0) - graph.degree(i) * u[i] + state.gamma * (total - u[i] + t * leaf)
                )
                assert residual >= 0
                assert (
                    residual == lam * graph.degree(i)
                    if u[i] > 0
                    else residual <= lam * graph.degree(i)
                )
                if leaf > 0:
                    assert u[i] > 0 and all(out[(i, j)] == leaf for j in range(t))
                else:
                    assert state.gamma * u[i] <= lam
            assert state.oracle.rows == set(out)
            assert all(not isinstance(i, int) or pendants[i] < 1000 for i in state.oracle.rows)
            assert lam * sum(graph.degree(i) for i in out) < 1
            counts["implicit_original_kkt_certificates"] += 1
            results.append(
                {
                    "pendant_counts": pendants,
                    "ambient_vertices": graph.k + sum(pendants),
                    "seed": 0,
                    "alpha_lazy": str(alpha),
                    "lambda": str(lam),
                    "core_values": {str(i): str(x) for i, x in u.items()},
                    "positive_vertices": len(out),
                    "active_volume": sum(graph.degree(i) for i in out),
                    "original_access": dict(state.oracle.counts),
                    "algorithm_counts": dict(state.counts),
                }
            )
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-core", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 3 <= args.max_core <= 8:
        parser.error("max_core must be 3 through 8")
    started = time.monotonic()
    counts = Counter()
    ledger = Counter()
    access = Counter()
    params = [
        (F(1, 3), F(1, 20)),
        (F(1, 1009), F(1, 200)),
        (F(1008, 1009), F(1, 20)),
        (F(1, 3), F(1, 4)),
    ]
    for k in range(3, args.max_core + 1):
        for pendants in itertools.combinations_with_replacement([0, 1, 4], k):
            for seed in range(k):
                for alpha, lam in params:
                    state = check_case(pendants, seed, alpha, lam, counts)
                    ledger.update(state.counts)
                    access.update(state.oracle.counts)
        print(
            json.dumps({"core_size": k, "cases": counts["exact_original_obstacle_comparisons"]}),
            flush=True,
        )
    ties = []
    for k in range(3, args.max_core + 1):
        alpha = F(1, 3)
        gamma = F(1, 2)
        d = k - 1
        state = check_case([0] * k, 0, alpha, gamma / (d * (d + gamma)), counts)
        assert set(state.oracle.rows) == {0}
        ties.append(
            {
                "kind": "first nonseed core birth equality",
                "k": k,
                "lambda": str(state.lam),
                "positive_vertices": 1,
            }
        )
        pendant = [2] + [1] * (k - 1)
        d = k + 1
        state = check_case(pendant, 0, alpha, gamma / (d * (1 + gamma)), counts)
        assert set(state.oracle.rows) == {0}
        ties.append(
            {
                "kind": "seed pendant birth equality",
                "k": k,
                "lambda": str(state.lam),
                "positive_vertices": 1,
            }
        )
        check_case(pendant, 0, alpha, F(1, d), counts)
    implicit = implicit_cases(counts)
    result = {
        "audit": "incremental_active_set_sdd.local_clique_pendants",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "promised clique core with private pendant leaves; explicit nondecreasing count tuples in {0,1,4} plus exact ties and huge implicit inactive rows",
        "max_core": args.max_core,
        "seed": "every core vertex in explicit cases; seed0 for ties/implicit cases",
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in params],
        "lambda_namespaces": "lambda=rho for exact obstacle/RPPR; lambda=eps_appr/2 for ACL",
        "stopping_rule": "first scalar affine fixed-point root before the next response breakpoint; exact zero gates stay inactive",
        "algorithm_scope": "Actual scalar sweep and local degree/adjacency access, no ambient scan or repeated coarse inverse. Exact-real word model on the promised family; no finite-precision or general OP3 claim.",
        "algorithm_counts": dict(ledger),
        "original_graph_access": dict(access),
        "audit_only": dict(counts),
        "tie_cases": ties,
        "implicit_cases": implicit,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["geometric_value_events", "local_sun_solver"]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
