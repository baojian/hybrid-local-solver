"""Exact OP3 output quantifiers, degree-only gates and local cycle witnesses.

The fixed-parameter star formula is imported from the problem-definition
note. Dense solves independently validate its lazy/nonlazy translation.
The cycle algorithm sees only the seed and charged adjacency-list queries.
The ambient cycle size is private to its oracle; no full graph is built.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from geometric_value_events import mv, solve
import networkx as nx


class CycleOracle:
    def __init__(self, size, seed, counts):
        self._size = size
        self._seen = {seed}
        self.counts = counts

    def degree(self, label):
        assert label in self._seen
        self.counts["degree_queries"] += 1
        return 2

    def neighbor(self, label, index):
        assert label in self._seen and 0 <= index < 2
        self.counts["adjacency_queries"] += 1
        result = (label + (1 if index else -1)) % self._size
        if result not in self._seen:
            self.counts["oracle_discovered_label_words"] += 1
            self._seen.add(result)
        return result


class LinearMap:
    """A deterministic map that charges every scanned label comparison."""

    def __init__(self, counts):
        self.entries = []
        self.counts = counts

    def get(self, key):
        for label, value in self.entries:
            self.counts["map_label_comparisons"] += 1
            if label == key:
                self.counts["map_value_reads"] += 1
                return value
        return None

    def set(self, key, value):
        for index, (label, _) in enumerate(self.entries):
            self.counts["map_label_comparisons"] += 1
            if label == key:
                self.entries[index] = key, value
                self.counts["map_value_writes"] += 1
                return
        self.entries.append((key, value))
        self.counts["allocated_map_entry_words"] += 2
        # A geometric-capacity array pays amortized constant append work.
        self.counts["map_array_append_and_copy_budget"] += 4


def truncated_walk(oracle, seed, gamma, epsilon, counts):
    """General discovered-label walk truncation, with all repeated work paid."""
    rows, potential = LinearMap(counts), LinearMap(counts)
    current, residual_mass = LinearMap(counts), F(1)
    current.set(seed, F(1))
    while residual_mass > epsilon:
        counts["stopping_comparisons"] += 1
        following = LinearMap(counts)
        for vertex, mass in current.entries:
            counts["current_entry_reads"] += 1
            row = rows.get(vertex)
            if row is None:
                degree = oracle.degree(vertex)
                neighbors = tuple(oracle.neighbor(vertex, i) for i in range(degree))
                row = degree, neighbors
                rows.set(vertex, row)
                counts["allocated_row_words"] += degree + 2
            degree, neighbors = row
            increment = mass / degree
            counts["arithmetic_operations"] += 1
            old = potential.get(vertex)
            potential.set(vertex, (F(0) if old is None else old) + increment)
            counts["arithmetic_operations"] += 1
            share = gamma * increment
            counts["arithmetic_operations"] += 1
            for neighbor in neighbors:
                counts["cached_neighbor_reads"] += 1
                old = following.get(neighbor)
                following.set(neighbor, (F(0) if old is None else old) + share)
                counts["arithmetic_operations"] += 1
        counts["released_map_entry_words"] += 2 * len(current.entries)
        current = following
        residual_mass *= gamma
        counts["arithmetic_operations"] += 1
        counts["walk_rounds"] += 1
    counts["stopping_comparisons"] += 1
    output = []
    for vertex, value in potential.entries:
        output.append((vertex, (1 - gamma) * rows.get(vertex)[0] * value))
        counts["output_coordinate_reads"] += 1
        counts["arithmetic_operations"] += 3
        counts["emitted_words"] += 2
        counts["output_array_append_and_copy_budget"] += 4
    # Freeing the final temporary state and row cache is also charged.
    counts["released_map_entry_words"] += 2 * (
        len(current.entries) + len(potential.entries) + len(rows.entries)
    )
    counts["released_row_words"] += sum(degree + 2 for _, (degree, _) in rows.entries)
    return potential.entries, output, current.entries


def cycle_case(k, audit_counts):
    size, seed = 2 ** (2 * k + 2), 0
    epsilon, gamma = F(1, 2**k), F(1, 2)
    paid = Counter()
    oracle = CycleOracle(size, seed, paid)
    value_entries, output_entries, residual_entries = truncated_walk(
        oracle, seed, gamma, epsilon, paid
    )
    # Audit-only lookup structures; the algorithm uses the charged linear maps.
    values, output, walk_residual = (
        dict(value_entries),
        dict(output_entries),
        dict(residual_entries),
    )
    # Independent original-row certificate. This validator may use the
    # private ambient size; the algorithm above may not.
    boundary = set(values)
    for vertex in values:
        boundary.update(((vertex - 1) % size, (vertex + 1) % size))
    assert set(walk_residual) <= boundary
    for vertex in boundary:
        residual = (
            F(vertex == seed)
            - 2 * values.get(vertex, F(0))
            + gamma * values.get((vertex - 1) % size, F(0))
            + gamma * values.get((vertex + 1) % size, F(0))
        )
        assert residual == walk_residual.get(vertex, F(0))
        assert 0 <= residual <= 2 * epsilon
        audit_counts["original_cycle_residual_rows"] += 1
    assert sum(walk_residual.values()) == epsilon
    assert sum(output.values()) == 1 - epsilon
    assert paid["walk_rounds"] == k
    assert paid["degree_queries"] == 2 * k - 1
    assert paid["adjacency_queries"] == 4 * k - 2
    assert len(values) == 2 * k - 1
    assert len(oracle._seen) == 2 * k + 1
    total = sum(paid.values())
    assert total <= 100 * (k + 1) ** 3
    audit_counts["local_cycle_cases"] += 1
    return {
        "k": k,
        "ambient_vertices": size,
        "eps_appr": str(epsilon),
        "lazy_alpha": "1/3",
        "mass_over_degree": "1/2",
        "mass_over_degree_divided_by_epsilon": 2 ** (k - 1),
        "output_coordinates": len(output),
        "paid_operations_and_words": dict(paid),
        "total_charged_units": total,
    }


def star_formula_and_quantifiers(full, counts):
    for leaves in range(2, 13 if full else 5):
        graph = nx.star_graph(leaves)
        degrees = [graph.degree(i) for i in graph]
        for alpha in [F(1), F(1, 3), F(1, 17), F(1, 2**30)]:
            gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
            matrix = [
                [
                    F(degrees[i]) if i == j else -gamma if graph.has_edge(i, j) else F(0)
                    for j in graph
                ]
                for i in graph
            ]
            exact_u = solve(matrix, [F(i == 0) for i in graph])
            exact_p = [bar * degrees[i] * exact_u[i] for i in graph]
            assert exact_p == [(1 + alpha) / 2] + [(1 - alpha) / (2 * leaves)] * leaves
            counts["dense_star_formula_validators"] += 1
            for epsilon in [F(1, 8 * leaves), F(1, 2 * leaves), F(1, leaves)]:
                candidate = [max(F(0), F(1, leaves) - epsilon)] + [F(0)] * leaves
                residual = [F(i == 0) - value for i, value in enumerate(mv(matrix, candidate))]
                accepted = all(0 <= r <= epsilon * d for r, d in zip(residual, degrees))
                assert accepted == (epsilon * leaves >= (1 - alpha) / 2)
                if accepted:
                    approximation = [bar * degrees[i] * candidate[i] for i in graph]
                    assert all(
                        0 <= (a - b) / d <= epsilon
                        for a, b, d in zip(exact_p, approximation, degrees)
                    )
                counts["star_exact_seed_only_thresholds"] += 1
    for exponent in range(4, 81 if full else 9):
        epsilon = F(1, 2**exponent)
        leaves = (F(1, 8) / epsilon).__floor__()
        for alpha in [F(1, 3), F(1, 17), F(1, 2 ** (2 * exponent))]:
            mass = (1 - alpha) / (2 * leaves)
            assert mass > epsilon and leaves >= 1 / (16 * epsilon)
            counts["uniform_alpha_output_lower_bound_cases"] += 1


def degree_gate(full, counts):
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= (5 if full else 3) or not nx.is_connected(graph):
            continue
        degrees = [graph.degree(i) for i in graph]
        for seed in graph:
            for alpha in [F(1), F(1, 3), F(1, 17)]:
                gamma = (1 - alpha) / (1 + alpha)
                gate = gamma / ((1 + gamma) * degrees[seed])
                for epsilon in {gate, (gate + F(1, degrees[seed])) / 2, F(1, degrees[seed])}:
                    if epsilon == 0:
                        continue
                    seed_u = max(F(0), F(1, degrees[seed]) - epsilon)
                    for vertex in graph:
                        residual = (
                            F(1) - degrees[seed] * seed_u
                            if vertex == seed
                            else gamma * seed_u
                            if graph.has_edge(vertex, seed)
                            else F(0)
                        )
                        assert 0 <= residual <= epsilon * degrees[vertex]
                        counts["original_degree_only_gate_rows"] += 1
                    counts["original_degree_only_gate_cases"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts = time.monotonic(), Counter()
    star_formula_and_quantifiers(args.full, counts)
    degree_gate(args.full, counts)
    exponents = list(range(1, 33)) + [48, 64, 96, 128] if args.full else [1, 4, 16]
    cases = [cycle_case(k, counts) for k in exponents]
    result = {
        "audit": "incremental_active_set_sdd.lower_bound_quantifiers",
        "arithmetic": "exact fractions; all graph labels discovered through charged queries",
        "scope": "Validates accuracy-scale output lower bounds, a stronger degree-only ACL gate, and a cycle counterexample to an instancewise mass-over-error lower bound. Does not refute an existential worst-graph bound or prove OP3.",
        "formal_import": "problem_definitions/open_conjectures_proof_attempt.md, Proposition 5: fixed-nonlazy-parameter star formula and sparse-output argument",
        "audit_only": dict(counts),
        "cycle_cases": cases,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "geometric_value_events.py": hashlib.sha256(
                Path(__file__).with_name("geometric_value_events.py").read_bytes()
            ).hexdigest()
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
