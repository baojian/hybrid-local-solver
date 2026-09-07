"""Exact supplied union/join core responses and complete-interval audits.

The decomposition, original degrees and private-leaf counts are supplied.
This is not a local graph-discovery solver. All retained response copies,
transforms, heap operations, queries and reconstruction steps are counted.
Independent original-matrix validators certify entire affine intervals.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import heapq
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from geometric_value_events import obstacle, solve
from multipartite_scalar_response import response
import networkx as nx


@dataclass(frozen=True)
class Node:
    kind: str
    children: tuple[int, ...] = ()
    vertex: int | None = None


class ModuleResponses:
    """Exact-real word reference, supplied reduced postorder decomposition."""

    def __init__(self, nodes, degrees, pendants, seed, alpha, lam):
        assert 0 < alpha < 1 and lam > 0
        self.nodes, self.degrees, self.pendants = nodes, degrees, pendants
        self.seed, self.lam = seed, lam
        self.gamma = (1 - alpha) / (1 + alpha)
        self.counts = Counter()
        self.curves = []
        self.join_inputs = {}
        self.sizes = []
        parents = Counter()
        leaves = set()
        for k, node in enumerate(nodes):
            self.counts["supplied_node_records"] += 1
            if node.kind == "leaf":
                assert not node.children and node.vertex not in leaves
                assert node.vertex in degrees and degrees[node.vertex] > 0
                leaves.add(node.vertex)
                size, curve = 1, self.leaf_curve(node.vertex)
            else:
                assert node.kind in {"union", "join"} and len(node.children) >= 2
                size = 0
                for child in node.children:
                    assert 0 <= child < k and nodes[child].kind != node.kind
                    parents[child] += 1
                    assert parents[child] == 1
                    size += self.sizes[child]
                    self.counts["supplied_child_records"] += 1
                self.counts[node.kind + "_module_size_sum"] += size
                streams = [self.curves[child] for child in node.children]
                self.counts["child_curve_reference_words"] += len(streams)
                if node.kind == "join":
                    streams = [self.join_input(curve) for curve in streams]
                    self.join_inputs[k] = streams
                    self.counts["retained_join_stream_references"] += len(streams)
                curve = self.merge(streams, node.kind == "join")
            self.sizes.append(size)
            self.curves.append(curve)
            self.counts["retained_curve_records"] += len(curve)
            self.counts["retained_curve_words"] += 3 * len(curve)
            assert len(curve) <= 2 * size
        assert leaves == set(degrees) and len(parents) == len(nodes) - 1
        assert len(nodes) - 1 not in parents

    def leaf_curve(self, i):
        d, q = self.degrees[i], self.pendants[i]
        assert 0 <= q <= d
        b = F(i == self.seed) - self.lam * d
        out = [(-b, F(1, d), b / d)]
        if q:
            denominator = d - self.gamma * self.gamma * q
            assert denominator > 0
            out.append(
                (
                    d * self.lam / self.gamma - b,
                    1 / denominator,
                    (b - self.gamma * self.lam * q) / denominator,
                )
            )
        self.counts["created_coordinate_events"] += len(out)
        self.counts["supplied_kernel_words"] += 3
        return out

    def join_input(self, curve):
        out = []
        previous = None
        for at, a, b in curve:
            z = at + self.gamma * (a * at + b)
            assert previous is None or z > previous
            previous = z
            den = 1 + self.gamma * a
            out.append((z, a / den, b / den))
            self.counts["child_join_event_transforms"] += 1
            self.counts["retained_join_input_words"] += 3
        return out

    def merge(self, streams, join):
        current = [(F(0), F(0)) for _ in streams]
        heap = []

        def push(g, pos):
            if pos < len(streams[g]):
                heapq.heappush(heap, (streams[g][pos][0], g, pos))
                self.counts["merge_heap_insertions"] += 1
                self.counts["merge_heap_comparison_budget"] += max(1, len(heap).bit_length())
                self.counts["temporary_heap_record_words"] += 3

        for g in range(len(streams)):
            push(g, 0)
        self.counts["temporary_current_piece_words"] += 2 * len(streams)
        a = b = F(0)
        out = []
        while heap:
            at = heap[0][0]
            threshold = at - self.gamma * (a * at + b) if join else at
            old_value = a * at + b
            tied = 0
            while heap and heap[0][0] == at:
                _, g, pos = heapq.heappop(heap)
                old_a, old_b = current[g]
                _, new_a, new_b = streams[g][pos]
                assert old_a * at + old_b == new_a * at + new_b
                a += new_a - old_a
                b += new_b - old_b
                current[g] = new_a, new_b
                self.counts["merge_event_consumptions"] += 1
                self.counts["constant_aggregate_updates"] += 1
                self.counts["merge_heap_comparison_budget"] += 2 * max(
                    1, (len(heap) + 1).bit_length()
                )
                tied += 1
                push(g, pos + 1)
            assert a * at + b == old_value
            den = 1 - self.gamma * a if join else F(1)
            assert den > 0
            changed = a / den, b / den
            assert not out or threshold > out[-1][0]
            assert not out or changed[0] >= out[-1][1]
            out.append((threshold, *changed))
            self.counts["parent_event_records_created"] += 1
            self.counts["parent_join_event_transforms"] += join
            self.counts["negative_parent_events"] += threshold < 0
            self.counts["simultaneous_child_events"] += tied > 1
        return out

    def evaluate(self, curve, field):
        lo, hi = 0, len(curve)
        while lo < hi:
            mid = (lo + hi) // 2
            self.counts["curve_query_comparisons"] += 1
            if curve[mid][0] <= field:
                lo = mid + 1
            else:
                hi = mid
        self.counts["curve_queries"] += 1
        if lo == 0:
            return F(0)
        _, a, b = curve[lo - 1]
        return a * field + b

    def recover(self, field=F(0), root=None):
        root = len(self.nodes) - 1 if root is None else root
        total = self.evaluate(self.curves[root], field)
        stack = [(root, field, total)]
        out = {}
        while stack:
            k, h, mass = stack.pop()
            node = self.nodes[k]
            self.counts["recovery_node_visits"] += 1
            self.counts["recovery_stack_words"] += 3
            if node.kind == "leaf":
                i = node.vertex
                b = F(i == self.seed) - self.lam * self.degrees[i]
                value = response(b + h, self.degrees[i], self.pendants[i], self.gamma, self.lam)
                assert value == mass
                out[i] = value
                self.counts["recovered_core_words"] += 1
            elif node.kind == "union":
                for child in node.children:
                    value = self.evaluate(self.curves[child], h)
                    stack.append((child, h, value))
            else:
                z = h + self.gamma * mass
                for child, curve in zip(node.children, self.join_inputs[k]):
                    value = self.evaluate(curve, z)
                    stack.append((child, z - self.gamma * value, value))
        assert sum(out.values()) == total
        return out


def supplied_decomposition(core):
    """Full-graph audit-only recognizer, explicitly outside the solver's work."""
    nodes, members, indices = [], [], {}
    stack = [(set(core), None, None)]
    while stack:
        vertices, kind, components = stack.pop()
        if kind is not None:
            node = Node(kind, tuple(indices[frozenset(part)] for part in components))
        elif len(vertices) == 1:
            node = Node("leaf", vertex=next(iter(vertices)))
        else:
            graph = core.subgraph(vertices)
            components = list(nx.connected_components(graph))
            kind = "union"
            if len(components) == 1:
                components = list(nx.connected_components(nx.complement(graph)))
                kind = "join"
            if len(components) == 1:
                raise ValueError("not a recursive union/join core")
            stack.append((vertices, kind, components))
            stack.extend((part, None, None) for part in reversed(components))
            continue
        index = len(nodes)
        nodes.append(node)
        members.append(set(vertices))
        indices[frozenset(vertices)] = index
    return nodes, members


def nonnegative_interval(a, b, left, right):
    if left is None:
        assert a <= 0
    else:
        assert a * left + b >= 0
    if right is None:
        assert a >= 0
    else:
        assert a * right + b >= 0


def check_case(core, pendants, seed, alpha, lam, counts, all_modules=True):
    nodes, members = supplied_decomposition(core)
    graph = core.copy()
    parents = {}
    next_vertex = len(core)
    for i, q in pendants.items():
        for _ in range(q):
            graph.add_edge(i, next_vertex)
            parents[next_vertex] = i
            next_vertex += 1
    degrees = {i: graph.degree(i) for i in core}
    state = ModuleResponses(nodes, degrees, pendants, seed, alpha, lam)
    n, edges = len(core), core.number_of_edges()
    c = state.counts
    assert c["join_module_size_sum"] <= 2 * edges
    assert c["union_module_size_sum"] <= n + c["join_module_size_sum"]
    internal_size = c["join_module_size_sum"] + c["union_module_size_sum"]
    assert internal_size <= n + 4 * edges
    assert c["retained_curve_records"] <= 2 * (n + internal_size)
    assert c["child_join_event_transforms"] <= 2 * c["join_module_size_sum"]
    assert c["merge_event_consumptions"] <= 2 * internal_size
    assert c["merge_heap_insertions"] == c["merge_event_consumptions"]
    counts["distinct_edge_accounting_checks"] += 1
    gamma = state.gamma
    target_nodes = range(len(nodes)) if all_modules else [len(nodes) - 1]
    for k in target_nodes:
        inside = members[k]
        labels = sorted(inside | {j for j, i in parents.items() if i in inside})
        matrix = [
            [
                F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0)
                for j in labels
            ]
            for i in labels
        ]
        load = [F(i == seed) - lam * graph.degree(i) for i in labels]
        forcing = [F(i in inside) for i in labels]
        curve = state.curves[k]
        thresholds = [row[0] for row in curve]
        for index in range(len(curve) + 1):
            left = thresholds[index - 1] if index else None
            right = thresholds[index] if index < len(curve) else None
            sample = (
                right - 1 if left is None else left + 1 if right is None else (left + right) / 2
            )
            exact = obstacle(matrix, [b + sample * f for b, f in zip(load, forcing)])
            face = [i for i, x in enumerate(exact) if x > 0]
            submatrix = [[matrix[i][j] for j in face] for i in face]
            intercept = solve(submatrix, [load[i] for i in face]) if face else []
            slope = solve(submatrix, [forcing[i] for i in face]) if face else []
            x0, x1 = [F(0)] * len(labels), [F(0)] * len(labels)
            for i, b, a in zip(face, intercept, slope):
                x0[i], x1[i] = b, a
                nonnegative_interval(a, b, left, right)
            for i in range(len(labels)):
                b = load[i] - sum(matrix[i][j] * x0[j] for j in face)
                a = forcing[i] - sum(matrix[i][j] * x1[j] for j in face)
                if i in face:
                    assert a == b == 0
                else:
                    nonnegative_interval(-a, -b, left, right)
            predicted_a, predicted_b = curve[index - 1][1:] if index else (F(0), F(0))
            assert predicted_a == sum(a for i, a in zip(labels, x1) if i in inside)
            assert predicted_b == sum(b for i, b in zip(labels, x0) if i in inside)
            recovered = state.recover(sample, k)
            assert all(recovered[i] == x for i, x in zip(labels, exact) if i in inside)
            counts["complete_original_affine_interval_certificates"] += 1
            counts["negative_field_samples"] += sample < 0
            counts["reference_principal_matrix_words"] += len(labels) ** 2
            counts["independent_coordinate_affine_certificates"] += len(labels)
        for h in [F(0), *thresholds]:
            exact = obstacle(matrix, [b + h * f for b, f in zip(load, forcing)])
            recovered = state.recover(h, k)
            assert all(recovered[i] == x for i, x in zip(labels, exact) if i in inside)
            counts["original_event_or_zero_field_comparisons"] += 1
        counts["audited_module_curves"] += 1
    counts["complete_supplied_graph_cases"] += 1
    return state


def structural_cases():
    records = []
    for n in [8, 16, 32, 64, 128]:
        for kind in ["alternating_comb", "balanced"]:
            if kind == "alternating_comb":
                graph = nx.empty_graph(n)
                for i in range(1, n):
                    if i % 2 or i == n - 1:
                        graph.add_edges_from((i, j) for j in range(i))
            else:

                def build(vertices, join):
                    if len(vertices) == 1:
                        return nx.empty_graph(vertices)
                    left = build(vertices[: len(vertices) // 2], not join)
                    right = build(vertices[len(vertices) // 2 :], not join)
                    out = nx.compose(left, right)
                    if join:
                        out.add_edges_from(itertools.product(left, right))
                    return out

                graph = build(list(range(n)), True)
            nodes, _ = supplied_decomposition(graph)
            q = {i: i % 3 for i in graph}
            d = {i: graph.degree(i) + q[i] for i in graph}
            state = ModuleResponses(nodes, d, q, 0, F(1, 1009), F(1, 200))
            c = state.counts
            edge_count = graph.number_of_edges()
            assert c["join_module_size_sum"] <= 2 * edge_count
            assert c["union_module_size_sum"] <= n + c["join_module_size_sum"]
            out = state.recover()
            for i, value in out.items():
                leaf = max(F(0), state.gamma * value - state.lam)
                gate = (
                    F(i == 0)
                    - state.lam * d[i]
                    + state.gamma * (sum(out[j] for j in graph[i]) + q[i] * leaf)
                    - d[i] * value
                )
                assert gate == 0 if value > 0 else gate <= 0
            records.append(
                {
                    "family": kind,
                    "core_vertices": n,
                    "core_edges": edge_count,
                    "counts": dict(c),
                    "root_curve_events": len(state.curves[-1]),
                }
            )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, operation_counts = Counter(), Counter()
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
    for core in cores:
        patterns = [{i: 0 for i in core}, {i: i % 3 for i in core}]
        for q, seed, (alpha, lam) in itertools.product(patterns, core, params):
            state = check_case(core, q, seed, alpha, lam, counts)
            operation_counts.update(state.counts)
    structural = structural_cases() if args.full else []
    result = {
        "audit": "incremental_active_set_sdd.recursive_module_response",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "core_family": "connected graph-atlas cores admitting recursive union/join decomposition",
        "max_core_vertices": 6 if args.full else 4,
        "distinct_atlas_cores": len(cores),
        "pendants": "zero or vertex index mod 3",
        "seed": "every core vertex",
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in params],
        "stopping_rule": "exact composed curve at supplied field; independent KKT certificates on every full affine interval and event",
        "scope": "Supplied reduced decomposition and original kernel metadata only. All-core-edge construction charge, not support-local discovery, arbitrary OP3 or bit complexity.",
        "algorithm_counts_including_repeated_validation_queries": dict(operation_counts),
        "audit_only": dict(counts),
        "structural_cases": structural,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["geometric_value_events", "multipartite_scalar_response"]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
