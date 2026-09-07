"""Persistent supplied recursive-module responses, without all-core-edge work.

Reuses the implemented immutable affine AVL primitives. Merges stream only
non-largest child curves, chosen by physical module size, and retain old
versions for reconstruction. No local decomposition oracle is asserted.
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

from persistent_affine_tree import Arena, Curve, height, size
from recursive_module_response import check_case, supplied_decomposition
import networkx as nx


def add_zero_left_response(large, small):
    """Add a convex curve with a zero left ray by streaming only its knots."""
    assert large.arena is small.arena and small.left_slope == 0
    result = large
    previous_slope = F(0)
    points = small.arena.points(small.root)
    previous = next(points, None)
    assert previous is None or previous[1] == 0
    for following in points:
        slope = (following[1] - previous[1]) / (following[0] - previous[0])
        small.arena.counts["merged_light_knots"] += 1
        result = result.add_hinge(previous[0], slope - previous_slope)
        previous, previous_slope = following, slope
    if previous:
        small.arena.counts["merged_light_knots"] += 1
        result = result.add_hinge(previous[0], small.right_slope - previous_slope)
    return result


class PersistentModules:
    def __init__(self, nodes, degrees, pendants, seed, alpha, lam):
        assert 0 < alpha < 1 and lam > 0
        self.nodes, self.degrees, self.pendants = nodes, degrees, pendants
        self.seed, self.lam = seed, lam
        self.gamma = (1 - alpha) / (1 + alpha)
        self.arena = Arena()
        self.curves, self.sizes, self.join_inputs = [], [], {}
        parents, leaves = Counter(), set()
        c = self.arena.counts
        for k, node in enumerate(nodes):
            c["supplied_node_records"] += 1
            if node.kind == "leaf":
                i = node.vertex
                assert not node.children and i not in leaves
                d, q = degrees[i], pendants[i]
                assert d > 0 and 0 <= q <= d
                leaves.add(i)
                b = F(i == seed) - lam * d
                curve = Curve(self.arena, None, F(0), F(0)).add_hinge(-b, F(1, d))
                if q:
                    slope = 1 / (d - self.gamma * self.gamma * q) - F(1, d)
                    curve = curve.add_hinge(d * lam / self.gamma - b, slope)
                module_size = 1
                c["supplied_kernel_words"] += 3
                c["created_coordinate_events"] += 1 + bool(q)
            else:
                assert node.kind in {"union", "join"} and len(node.children) >= 2
                module_size = 0
                for child in node.children:
                    assert 0 <= child < k and nodes[child].kind != node.kind
                    parents[child] += 1
                    assert parents[child] == 1
                    module_size += self.sizes[child]
                    c["supplied_child_records"] += 1
                streams = [self.curves[child] for child in node.children]
                c["temporary_child_curve_references"] += len(streams)
                if node.kind == "join":
                    transform = (F(1), self.gamma, F(0), F(1), F(0), F(0))
                    streams = [curve.affine(transform) for curve in streams]
                    self.join_inputs[k] = streams
                    c["retained_join_input_versions"] += len(streams)
                heavy = max(range(len(streams)), key=lambda g: self.sizes[node.children[g]])
                c["largest_child_comparisons"] += len(streams) - 1
                curve = streams[heavy]
                for g, small in enumerate(streams):
                    if g != heavy:
                        child_size = self.sizes[node.children[g]]
                        assert 2 * child_size <= module_size
                        c["light_child_vertex_charges"] += child_size
                        c["light_child_merges"] += 1
                        curve = add_zero_left_response(curve, small)
                if node.kind == "join":
                    curve = curve.affine((F(1), -self.gamma, F(0), F(1), F(0), F(0)))
                c[node.kind + "_nodes"] += 1
            assert curve.left_slope == 0 and size(curve.root) <= 2 * module_size
            self.sizes.append(module_size)
            self.curves.append(curve)
            c["retained_module_curve_versions"] += 1
        assert leaves == set(degrees) and len(parents) == len(nodes) - 1
        assert len(nodes) - 1 not in parents
        n = len(leaves)
        assert c["light_child_vertex_charges"] <= n * max(0, n.bit_length() - 1)
        assert c["merged_light_knots"] <= 2 * c["light_child_vertex_charges"]

    def recover(self, field=F(0), root=None, observer=None):
        arena = self.arena if observer is None else observer

        def value(curve, h):
            return curve.with_arena(arena).value(h)

        root = len(self.nodes) - 1 if root is None else root
        total = value(self.curves[root], field)
        stack = [(root, field, total)]
        out = {}
        while stack:
            k, h, mass = stack.pop()
            node = self.nodes[k]
            arena.counts["recovery_node_visits"] += 1
            arena.counts["recovery_stack_words"] += 3
            if node.kind == "leaf":
                out[node.vertex] = mass
                arena.counts["output_core_words"] += 1
            elif node.kind == "union":
                for child in node.children:
                    stack.append((child, h, value(self.curves[child], h)))
            else:
                z = h + self.gamma * mass
                for child, curve in zip(node.children, self.join_inputs[k]):
                    child_mass = value(curve, z)
                    stack.append((child, z - self.gamma * child_mass, child_mass))
        assert sum(out.values()) == total
        return out


def compare_curve(curve, expected, counts, observer):
    """Read retained snapshots with an audit-only arena; certify every piece."""
    points = list(observer.points(curve.root))
    assert len(points) == len(expected)
    assert curve.left_slope == 0
    for index, ((x, y), (at, a, b)) in enumerate(zip(points, expected)):
        assert x == at and y == a * at + b
        slope = (
            (points[index + 1][1] - y) / (points[index + 1][0] - x)
            if index + 1 < len(points)
            else curve.right_slope
        )
        assert slope == a
        counts["retained_complete_affine_piece_matches"] += 1
    stack = [curve.root] if curve.root else []
    while stack:
        node = stack.pop()
        assert abs(height(node.left) - height(node.right)) <= 1
        assert node.height == 1 + max(height(node.left), height(node.right))
        assert node.size == 1 + size(node.left) + size(node.right)
        stack.extend(child for child in [node.left, node.right] if child)
        counts["retained_avl_node_certificates"] += 1
    counts["retained_curve_versions_checked"] += 1


def check_persistent(core, q, seed, alpha, lam, counts, reference_counts):
    reference = check_case(core, q, seed, alpha, lam, reference_counts)
    state = PersistentModules(reference.nodes, reference.degrees, q, seed, alpha, lam)
    observer = Arena()
    for k, (curve, expected) in enumerate(zip(state.curves, reference.curves)):
        compare_curve(curve, expected, counts, observer)
        fields = [F(0), *[row[0] for row in expected]]
        fields += [(a[0] + b[0]) / 2 for a, b in zip(expected, expected[1:])]
        fields += [expected[0][0] - 1, expected[-1][0] + 1]
        for field in fields:
            assert state.recover(field, k, observer) == reference.recover(field, k)
            counts["persistent_module_coordinate_recoveries"] += 1
    for k, curves in state.join_inputs.items():
        for curve, expected in zip(curves, reference.join_inputs[k]):
            compare_curve(curve, expected, counts, observer)
    before = state.arena.counts["node_allocations"]
    assert state.recover() == reference.recover()
    assert state.arena.counts["node_allocations"] == before
    counts["complete_original_graph_cases"] += 1
    return state


def structural_cases(full):
    records = []
    for n in [16, 32, 64, 128, 256, 512] if full else [16]:
        for family in ["alternating_comb", "clique", "star"]:
            if family == "clique":
                graph = nx.complete_graph(n)
            elif family == "star":
                graph = nx.star_graph(n - 1)
            else:
                graph = nx.empty_graph(n)
                for i in range(1, n):
                    if i % 2 or i == n - 1:
                        graph.add_edges_from((i, j) for j in range(i))
            nodes, _ = supplied_decomposition(graph)
            q = {i: i % 3 for i in graph}
            degrees = {i: graph.degree(i) + q[i] for i in graph}
            state = PersistentModules(nodes, degrees, q, 0, F(1, 1009), F(1, 200))
            out = state.recover()
            for i, u in out.items():
                leaf = max(F(0), state.gamma * u - state.lam)
                gate = (
                    F(i == 0)
                    - state.lam * degrees[i]
                    + state.gamma * (sum(out[j] for j in graph[i]) + q[i] * leaf)
                    - degrees[i] * u
                )
                assert gate == 0 if u > 0 else gate <= 0
            records.append(
                {
                    "family": family,
                    "core_vertices": n,
                    "core_edges": graph.number_of_edges(),
                    "root_curve_events": size(state.curves[-1].root),
                    "algorithm_counts": dict(state.arena.counts),
                }
            )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, references, operations = Counter(), Counter(), Counter()
    cores = []
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= (6 if args.full else 4) or not nx.is_connected(graph):
            continue
        try:
            supplied_decomposition(graph)
        except ValueError:
            continue
        cores.append(graph)
    params = [(F(1, 3), F(1, 20)), (F(1, 1009), F(1, 200)), (F(1008, 1009), F(1, 4))]
    for graph in cores:
        patterns = [{i: 0 for i in graph}, {i: i % 3 for i in graph}]
        for q, seed, (alpha, lam) in itertools.product(patterns, graph, params):
            state = check_persistent(graph, q, seed, alpha, lam, counts, references)
            operations.update(state.arena.counts)
    structural = structural_cases(args.full)
    result = {
        "audit": "incremental_active_set_sdd.persistent_module_response",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "core_family": "all connected union/join graph-atlas cores through max_n",
        "max_n": 6 if args.full else 4,
        "distinct_cores": len(cores),
        "pendants": "zero or vertex index mod 3",
        "seed": "every core vertex",
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in params],
        "stopping_rule": "exact persistent response at h=0; full saved versions match independently certified original affine intervals",
        "scope": "Supplied reduced decomposition, original degrees and pendant counts. Persistent O(N log^2 N) word construction candidate; no local discovery or bit-cost claim.",
        "algorithm_counts_construction_and_one_final_recovery": dict(operations),
        "audit_only": dict(counts),
        "independent_original_matrix_reference": dict(references),
        "structural_cases": structural,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "persistent_affine_tree",
                "recursive_module_response",
                "geometric_value_events",
                "multipartite_scalar_response",
                "tree_affine_response",
            ]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
