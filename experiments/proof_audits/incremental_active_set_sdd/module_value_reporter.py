"""Strict original-coordinate reporting on fixed supplied module responses.

Targets are positive, may change arbitrarily, and queries may use any real
common core field. Indexed heaps retain no stale history. This does not
maintain a decomposition or response curve under actual graph admissions.
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
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from geometric_value_events import obstacle
from persistent_affine_tree import Arena
from persistent_module_response import PersistentModules
from recursive_module_response import supplied_decomposition
import networkx as nx


class IndexedMin:
    """A fixed-membership indexed heap; every comparison and swap is counted."""

    def __init__(self, entries, counts):
        self.counts = counts
        self.heap = list(entries)
        self.position = [0] * len(self.heap)
        for i, key in enumerate(self.heap):
            self.position[key[2]] = i
        counts["heap_initial_records"] += len(self.heap)
        assert len(self.position) == len(self.heap)
        for i in reversed(range(len(self.heap) // 2)):
            self.down(i)

    def less(self, i, j):
        self.counts["heap_comparisons"] += 1
        return self.heap[i] < self.heap[j]

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i][2]] = i
        self.position[self.heap[j][2]] = j
        self.counts["heap_swaps"] += 1
        self.counts["heap_index_writes"] += 2

    def down(self, i):
        while 2 * i + 1 < len(self.heap):
            j = 2 * i + 1
            if j + 1 < len(self.heap) and self.less(j + 1, j):
                j += 1
            if not self.less(j, i):
                break
            self.swap(i, j)
            i = j

    def replace(self, key):
        i = self.position[key[2]]
        self.heap[i] = key
        self.counts["heap_replacements"] += 1
        if i and self.less(i, (i - 1) // 2):
            while i and self.less(i, (i - 1) // 2):
                parent = (i - 1) // 2
                self.swap(i, parent)
                i = parent
        else:
            self.down(i)

    def first(self):
        self.counts["heap_minimum_reads"] += 1
        return self.heap[0]


class ModuleReporter:
    """Mutable targets, immutable responses, and degree-paid coordinate paths."""

    def __init__(self, state, targets):
        self.state = state
        self.arena = Arena()
        self.counts = self.arena.counts
        self.targets = dict(targets)
        assert set(targets) == set(state.degrees) and all(t > 0 for t in targets.values())
        self.parents = [None] * len(state.nodes)
        self.leaves = {}
        self.heaps = [None] * len(state.nodes)
        self.join_sums = [None] * len(state.nodes)
        self.tau, self.winner = [], []
        self.counts["target_records"] += len(targets)
        for k, node in enumerate(state.nodes):
            self.counts["reporter_node_initializations"] += 1
            if node.kind == "leaf":
                self.leaves[node.vertex] = k
                threshold, winner = self.leaf_threshold(node.vertex), node.vertex
            else:
                entries = []
                for slot, child in enumerate(node.children):
                    self.parents[child] = k, slot
                    self.counts["parent_index_records"] += 1
                    entries.append(self.child_key(k, child))
                self.heaps[k] = IndexedMin(entries, self.counts)
                if node.kind == "join":
                    g = state.gamma
                    self.join_sums[k] = (
                        state.curves[k]
                        .with_arena(self.arena)
                        .affine((F(1), g, F(0), F(1), F(0), F(0)))
                    )
                    self.counts["retained_join_sum_versions"] += 1
                threshold, winner = self.parent_threshold(k)
            self.tau.append(threshold)
            self.winner.append(winner)
            self.counts["threshold_and_winner_records"] += 1
        self.initial_counts = self.counts.copy()

    def value(self, curve, field):
        return curve.with_arena(self.arena).value(field)

    def leaf_threshold(self, i):
        d, q, t = self.state.degrees[i], self.state.pendants[i], self.targets[i]
        g, lam = self.state.gamma, self.state.lam
        b = F(i == self.state.seed) - lam * d
        self.counts["leaf_threshold_evaluations"] += 1
        return d * t - g * q * max(F(0), g * t - lam) - b

    def child_key(self, parent, child):
        threshold = self.tau[child]
        if self.state.nodes[parent].kind == "join":
            threshold += self.state.gamma * self.value(self.state.curves[child], threshold)
        self.counts["child_key_evaluations"] += 1
        return threshold, self.winner[child], self.parents[child][1]

    def parent_threshold(self, k):
        threshold, winner, _ = self.heaps[k].first()
        if self.state.nodes[k].kind == "join":
            threshold -= self.state.gamma * self.value(self.join_sums[k], threshold)
        self.counts["parent_threshold_evaluations"] += 1
        return threshold, winner

    def set_target(self, i, target):
        assert target > 0
        self.targets[i] = target
        k = self.leaves[i]
        self.tau[k] = self.leaf_threshold(i)
        self.counts["target_updates"] += 1
        self.counts["target_update_degree_charge"] += 1 + self.state.degrees[i]
        self.counts["target_path_visits"] += 1
        while self.parents[k] is not None:
            parent, _ = self.parents[k]
            self.heaps[parent].replace(self.child_key(parent, k))
            self.tau[parent], self.winner[parent] = self.parent_threshold(parent)
            k = parent
            self.counts["target_path_visits"] += 1

    def due(self, field):
        self.counts["root_due_queries"] += 1
        return self.winner[-1] if field > self.tau[-1] else None

    def coordinate(self, i, field):
        k = self.leaves[i]
        path = []
        while self.parents[k] is not None:
            parent, slot = self.parents[k]
            path.append((parent, slot, k))
            k = parent
            self.counts["coordinate_path_stack_records"] += 1
        mass = self.value(self.state.curves[k], field)
        self.counts["coordinate_path_visits"] += 1
        for parent, slot, child in reversed(path):
            if self.state.nodes[parent].kind == "union":
                mass = self.value(self.state.curves[child], field)
            else:
                z = field + self.state.gamma * mass
                mass = self.value(self.state.join_inputs[parent][slot], z)
                field = z - self.state.gamma * mass
            self.counts["coordinate_path_visits"] += 1
        self.counts["coordinate_queries"] += 1
        self.counts["coordinate_query_degree_charge"] += 1 + self.state.degrees[i]
        return mass


def verify_heap(heap):
    assert len(heap.position) == len(heap.heap)
    for i, key in enumerate(heap.heap):
        assert heap.position[key[2]] == i
        if i:
            assert heap.heap[(i - 1) // 2] <= key


def original_problem(core, q, seed, gamma, lam):
    graph = core.copy()
    parents = {}
    for i in core:
        for _ in range(q[i]):
            j = len(graph)
            graph.add_edge(i, j)
            parents[j] = i
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in graph]
    return graph, parents, matrix, load


def check_reporter(core, q, seed, alpha, lam, counts):
    nodes, _ = supplied_decomposition(core)
    degrees = {i: core.degree(i) + q[i] for i in core}
    state = PersistentModules(nodes, degrees, q, seed, alpha, lam)
    reporter = ModuleReporter(state, {i: F(1, 100 * degrees[i]) for i in core})
    graph, _, matrix, load = original_problem(core, q, seed, state.gamma, lam)
    old_curves = [(c.root, tuple(Arena().points(c.root))) for c in state.curves]
    old_allocations = reporter.counts["node_allocations"]
    for i in core:
        k, joins, unions, depth = reporter.leaves[i], 0, 0, 0
        while reporter.parents[k] is not None:
            k, _ = reporter.parents[k]
            joins += nodes[k].kind == "join"
            unions += nodes[k].kind == "union"
            depth += 1
        assert joins <= core.degree(i) and unions <= joins + 1
        assert depth <= 2 * core.degree(i) + 1 <= 2 * degrees[i] + 1
        counts["original_degree_depth_certificates"] += 1

    # Include exact simultaneous targets from a known all-positive field.
    tied_field = F(2)
    tied = obstacle(matrix, [b + tied_field * (i in core) for i, b in enumerate(load)])
    scenarios = [None]
    scenarios += [(i, tied[i]) for i in core]
    scenarios += [(i, tied[i] + F(1, 10)) for i in reversed(list(core))]
    scenarios += [(i, F(1, 200 * degrees[i])) for i in core]
    for update in scenarios:
        if update:
            reporter.set_target(*update)
        threshold = reporter.tau[-1]
        counts["negative_root_thresholds"] += threshold < 0
        for field in [threshold - F(1, 1000), threshold, threshold + F(1, 1000), F(0)]:
            exact = obstacle(matrix, [b + field * (i in core) for i, b in enumerate(load)])
            due = reporter.due(field)
            violations = [i for i in core if exact[i] > reporter.targets[i]]
            assert (due is not None) == bool(violations)
            if due is not None:
                assert due in violations
                assert reporter.coordinate(due, field) == exact[due]
                counts["reported_original_coordinate_matches"] += 1
            else:
                counts["quiet_original_matrix_certificates"] += 1
            if field == threshold:
                assert exact[reporter.winner[-1]] == reporter.targets[reporter.winner[-1]]
                counts["strict_equality_not_due_certificates"] += 1
            counts["original_matrix_reporter_queries"] += 1
        for heap in reporter.heaps:
            if heap is None:
                continue
            verify_heap(heap)
            counts["indexed_heap_certificates"] += 1
        counts["target_states"] += 1
    # At the end all targets were decreased; exercise arbitrary field order too.
    for i in core:
        assert reporter.coordinate(i, F(0)) == obstacle(matrix, load)[i]
    for curve, (root, points) in zip(state.curves, old_curves):
        assert curve.root is root and tuple(Arena().points(root)) == points
        counts["unchanged_saved_curve_versions"] += 1
    assert reporter.counts["node_allocations"] == old_allocations
    assert sum(len(h.heap) for h in reporter.heaps if h is not None) == len(nodes) - 1
    assert (
        reporter.counts["target_path_visits"] <= 2 * reporter.counts["target_update_degree_charge"]
    )
    assert (
        reporter.counts["coordinate_path_visits"]
        <= 2 * reporter.counts["coordinate_query_degree_charge"]
    )
    counts["complete_original_graph_cases"] += 1
    counts["reference_matrix_words"] += len(graph) ** 2
    return reporter


def structural_cases(full):
    rows = []
    for n in [16, 64, 256, 512] if full else [16]:
        for family in ["alternating_comb", "clique", "star", "root_union", "singleton"]:
            if family == "singleton" and n != 16:
                continue
            if family == "clique":
                core = nx.complete_graph(n)
            elif family == "star":
                core = nx.star_graph(n - 1)
            elif family == "root_union":
                core = nx.disjoint_union(nx.complete_graph(n // 2), nx.empty_graph(n // 2))
            elif family == "singleton":
                core = nx.empty_graph(1)
            else:
                core = nx.empty_graph(n)
                for i in range(1, n):
                    if i % 2 or i == n - 1:
                        core.add_edges_from((i, j) for j in range(i))
            q = {i: 1 + i % 3 for i in core}
            degrees = {i: core.degree(i) + q[i] for i in core}
            nodes, _ = supplied_decomposition(core)
            state = PersistentModules(nodes, degrees, q, 0, F(1, 1009), F(1, 200))
            rep = ModuleReporter(state, {i: F(1, 100 * degrees[i]) for i in core})
            for i in core:
                rep.set_target(i, F(1, 50 * degrees[i]))
            total_depth = 0
            for i in core:
                k, depth = rep.leaves[i], 0
                while rep.parents[k] is not None:
                    k, _ = rep.parents[k]
                    depth += 1
                assert depth <= 2 * core.degree(i) + 1
                total_depth += depth
            # Independent KKT check for one full reconstruction; path check uses it.
            field = rep.tau[-1] + F(1, 1000)
            values = state.recover(field, observer=Arena())
            for i, u in values.items():
                gate = F(i == 0) - state.lam * degrees[i] + field
                gate += state.gamma * (
                    sum(values[j] for j in core[i]) + q[i] * max(F(0), state.gamma * u - state.lam)
                )
                gate -= degrees[i] * u
                assert gate == 0 if u else gate <= 0
            due = rep.due(field)
            assert due is not None and values[due] > rep.targets[due]
            assert rep.coordinate(due, field) == values[due]
            rows.append(
                {
                    "family": family,
                    "core_vertices": len(core),
                    "core_edges": core.number_of_edges(),
                    "total_leaf_depth": total_depth,
                    "reporter_counts": dict(rep.counts),
                    "initialization_counts": dict(rep.initial_counts),
                }
            )
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, operations, initial = Counter(), Counter(), Counter()
    cores = []
    for core in nx.graph_atlas_g():
        if not 2 <= len(core) <= (6 if args.full else 4) or not nx.is_connected(core):
            continue
        try:
            supplied_decomposition(core)
        except ValueError:
            continue
        cores.append(core)
    params = [(F(1, 3), F(1, 20)), (F(1, 1009), F(1, 200)), (F(1008, 1009), F(1, 4))]
    for graph in cores:
        patterns = [{i: 0 for i in graph}, {i: i % 3 for i in graph}]
        for q, seed, (alpha, lam) in itertools.product(patterns, graph, params):
            reporter = check_reporter(graph, q, seed, alpha, lam, counts)
            operations.update(reporter.counts)
            initial.update(reporter.initial_counts)
    result = {
        "audit": "incremental_active_set_sdd.module_value_reporter",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "core_family": "all connected union/join graph-atlas cores through max_n",
        "max_n": 6 if args.full else 4,
        "distinct_cores": len(cores),
        "pendants": "zero or vertex index mod 3",
        "seed": "every core vertex",
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in params],
        "targets": "positive degree-scaled, exact simultaneous field-2 coordinates, increases and decreases",
        "stopping_rule": "strict original coordinate > current target; root equality is quiet",
        "scope": "Fixed supplied responses and original degrees. Arbitrary common fields and positive target updates. No graph-admission or local decomposition claim.",
        "audit_only": dict(counts),
        "reporter_counts_including_initialization": dict(operations),
        "initialization_counts": dict(initial),
        "structural_cases": structural_cases(args.full),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "persistent_module_response",
                "persistent_affine_tree",
                "recursive_module_response",
                "geometric_value_events",
            ]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
