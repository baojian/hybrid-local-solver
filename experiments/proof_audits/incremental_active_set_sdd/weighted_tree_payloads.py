"""Weighted tree callbacks and simultaneous endpoint-payload refresh.

The production helper receives current hierarchy parent pointers and changed
edge leaves. Whole hierarchy enumeration/indexing and physical dense solves
are independent validators, not an online balancing or local discovery code.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontier_exact import AVLMap
from frontier_neighborhood_types import blow_up
from geometric_value_events import solve
from path_cluster_reporter import Backend
from top_tree_callback_adapter import Adapter, AuditCase
import networkx as nx


class Weight:
    def __init__(self, value):
        self.value = value


class WeightedBackend(Backend):
    def __init__(self, original, weights, work):
        super().__init__(original, F(1))
        self.weights, self.work = AVLMap(work), work
        for edge, weight in weights:
            assert weight > 0
            self.weights.get_or_create(tuple(sorted(edge)), lambda weight=weight: Weight(weight))
            work["weighted_edge_parameter_initialization"] += 7

    def edge(self, parent, child, rows):
        out = super().edge(parent, child, rows)

        def absent():
            raise AssertionError("Unprovided weighted tree edge")

        weight = self.weights.get_or_create(tuple(sorted((parent, child))), absent).value
        self.work["weighted_base_edge_lookup_and_scalar_replacement"] += 12
        return replace(out, matrix=((out.matrix[0][0], -weight), (-weight, out.matrix[1][1])))

    def replace_weight(self, edge, value):
        assert value > 0

        def absent():
            raise AssertionError("Unprovided replacement edge")

        self.weights.get_or_create(tuple(sorted(edge)), absent).value = value
        self.work["weighted_edge_scalar_replacement"] += 7


class Dirty:
    def __init__(self):
        self.marked = False


def refresh_many(root, leaves, parent_of, change_payloads, create, join, rows_for, work):
    """Mark current ancestors first, then rebuild only marked nodes bottom up."""
    dirty = AVLMap(work)
    marked = 0
    for leaf in leaves:
        node = leaf
        while node is not None:
            record = dirty.get_or_create(id(node), Dirty)
            work["bulk_payload_dirty_identity_and_cell_operations"] += 7
            if record.marked:
                break
            record.marked = True
            marked += 1
            node = parent_of(node)
            work["bulk_payload_parent_pointer_mark_steps"] += 6
    change_payloads()

    def rebuild(node):
        record = dirty.get_or_create(id(node), Dirty)
        work["bulk_payload_rebuild_identity_and_cell_operations"] += 7
        if not record.marked:
            return node
        work["bulk_payload_recomputed_hierarchy_records"] += 1
        if not node.children:
            return create(node.edge, node.ports, rows_for(node.edge))
        left, right = node.children
        return join(rebuild(left), rebuild(right), node.ports)

    out = rebuild(root)
    return out, marked


class WeightedCase(AuditCase):
    """Reference construction and exhaustive oracle metadata are audit-only."""

    def __init__(self, tree, seed, mask, alpha, counts):
        self.tree, self.seed, self.alpha, self.counts = tree, seed, alpha, counts
        self.n = len(tree)
        self.gamma, self.bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        self.sizes = [2 + i % 3 for i in range(self.n)]
        self.graph, self.partition = blow_up(tree, self.sizes, mask)
        self.physical_seed = self.partition[seed][-1]
        self.clique = [bool(mask & (1 << i)) for i in range(self.n)]
        physical_n = len(self.graph)
        self.lam = self.bar / (12 * (2 * physical_n) ** physical_n)
        self.parent, self.depth = {seed: None}, {seed: 0}
        order = [seed]
        for i in order:
            for j in sorted(tree[i]):
                if j != self.parent[i]:
                    self.parent[j], self.depth[j] = i, self.depth[i] + 1
                    order.append(j)
        self.edges = [(self.parent[i], i) for i in order[1:]]
        self.full = (1 << len(self.edges)) - 1
        initial = list(self.sizes)
        initial[seed] = 1
        self.original, self.weight_values, self.values = self.data(initial)
        self.active_sizes = initial
        self.rows = {
            i: (self.values[i] * [F(1, 2), F(1), F(2)][i % 3], physical_n + i) for i in tree
        }
        root_home = min(tree[seed])
        self.home = {
            i: next(k for k, e in enumerate(self.edges) if e == (self.parent[i], i))
            for i in tree
            if i != seed
        }
        self.home[seed] = next(k for k, e in enumerate(self.edges) if e == (seed, root_home))
        self.payload = {
            k: [(i, *self.rows[i]) for i in tree if self.home[i] == k]
            for k in range(len(self.edges))
        }
        self.payload_work = Counter()
        self.adapter = Adapter(seed, self.depth, self.original, self.gamma)
        self.adapter.backend = WeightedBackend(
            self.original, list(self.weight_values.items()), self.payload_work
        )
        self.meta, self.oracle_cache, self.masks = {}, {}, {}
        for mask0 in range(1, self.full + 1):
            chosen = [e for k, e in enumerate(self.edges) if mask0 & (1 << k)]
            vertices = {i for e in chosen for i in e}
            if len(vertices) != len(chosen) + 1:
                continue
            degree = Counter(i for e in chosen for i in e)
            ordinary = {i for i in vertices if degree[i] < tree.degree(i)}
            self.masks[mask0] = (vertices, ordinary)

    def data(self, active):
        original = {
            i: (
                active[i]
                * (
                    self.graph.degree(self.partition[i][0])
                    - self.gamma * self.clique[i] * (active[i] - 1)
                ),
                F(i == self.seed) - self.lam * active[i] * self.graph.degree(self.partition[i][0]),
            )
            for i in self.tree
        }
        weights = {
            tuple(sorted((i, j))): self.gamma * active[i] * active[j] for i, j in self.tree.edges
        }
        selected = []
        for i in self.tree:
            selected.extend(
                [self.physical_seed] if i == self.seed and active[i] == 1 else self.partition[i]
            )
        matrix = [
            [
                F(self.graph.degree(i))
                if i == j
                else -self.gamma
                if self.graph.has_edge(i, j)
                else F(0)
                for j in selected
            ]
            for i in selected
        ]
        physical = solve(
            matrix, [F(i == self.physical_seed) - self.lam * self.graph.degree(i) for i in selected]
        )
        assert min(physical) > 0
        values_by_label = dict(zip(selected, physical))
        means = [
            sum(values_by_label.get(j, F(0)) for j in self.partition[i]) / active[i]
            for i in range(self.n)
        ]
        quotient = [
            [
                original[i][0]
                if i == j
                else -weights[tuple(sorted((i, j)))]
                if self.tree.has_edge(i, j)
                else F(0)
                for j in range(self.n)
            ]
            for i in range(self.n)
        ]
        assert solve(quotient, [original[i][1] for i in range(self.n)]) == means
        for i in self.tree:
            assert (
                sum(quotient[i])
                >= self.bar * active[i] * self.graph.degree(self.partition[i][0])
                > 0
            )
        self.counts["independent_physical_quotient_mean_systems"] += 1
        self.counts["independent_physical_source_coordinates"] += len(selected)
        return original, weights, means

    def oracle(self, mask, ports):
        key = mask, ports
        if key in self.oracle_cache:
            return self.oracle_cache[key]
        vertices = self.masks[mask][0]
        interior = sorted(vertices - set(ports))
        assert self.seed not in interior
        selected = {tuple(sorted(e)) for k, e in enumerate(self.edges) if mask & (1 << k)}

        def entry(i, j):
            if i == j:
                return self.original[i][0]
            key = tuple(sorted((i, j)))
            return -self.weight_values[key] if key in selected else F(0)

        inner = [[entry(i, j) for j in interior] for i in interior]
        offset = dict(zip(interior, solve(inner, [self.original[i][1] for i in interior])))
        coefficients = {i: [] for i in vertices}
        for p in ports:
            col = solve(inner, [-entry(i, p) for i in interior])
            for i, value in zip(interior, col):
                coefficients[i].append(value)
        for k, p in enumerate(ports):
            coefficients[p] = [F(k == j) for j in range(len(ports))]
            offset[p] = F(0)
        matrix = tuple(
            tuple(
                entry(i, j) + sum(entry(i, h) * coefficients[h][k] for h in interior)
                for k, j in enumerate(ports)
            )
            for i in ports
        )
        rhs = tuple(
            self.original[i][1] - sum(entry(i, h) * offset[h] for h in interior) for i in ports
        )
        raw = []
        for k, rows in self.payload.items():
            if not mask & (1 << k):
                continue
            for home, threshold, label in rows:
                aa = coefficients[home]
                cc = offset[home] - threshold
                assert min(aa) >= 0 and sum(aa) > 0 and cc < 0
                raw.append((aa[0], cc, sum(aa), label) if len(ports) == 2 else (-cc / aa[0], label))
        result = matrix, rhs, raw
        self.oracle_cache[key] = result
        self.counts["independent_weighted_schur_oracles"] += 1
        return result

    def simultaneous_root_refresh(self, root):
        parents = {id(root): None}
        leaves = {}
        stack = [root]
        while stack:
            node = stack.pop()
            self.counts["validator_only_full_hierarchy_index_visits"] += 1
            if node.edge is not None:
                leaves[tuple(sorted(node.edge))] = node
            for child in node.children:
                assert id(child) not in parents
                parents[id(child)] = node
                stack.append(child)
        affected = [e for e in self.weight_values if self.seed in e]
        old_original, old_weights, old_values, old_payload = (
            self.original,
            self.weight_values,
            self.values,
            self.payload,
        )
        old_root_data = old_original[self.seed]
        new_original, new_weights, new_values = self.data(self.sizes)
        new_payload = {
            k: [
                (i, threshold / self.sizes[self.seed] if i == self.seed else threshold, label)
                for i, threshold, label in rows
            ]
            for k, rows in old_payload.items()
        }

        def change():
            self.original, self.weight_values, self.values, self.payload = (
                new_original,
                new_weights,
                new_values,
                new_payload,
            )
            # The provided update changes one original node record and its incident edges.
            self.adapter.backend.original[self.seed] = new_original[self.seed]
            for edge in affected:
                self.adapter.backend.replace_weight(edge, new_weights[edge])
            self.payload_work["bulk_root_diagonal_load_and_home_threshold_writes"] += 8
            self.oracle_cache.clear()

        edge_indices = {tuple(sorted(e)): k for k, e in enumerate(self.edges)}

        def create(edge, ports, rows):
            out = self.adapter.create(edge, ports, rows)
            return self.register(out, 1 << edge_indices[tuple(sorted(edge))])

        def join(a, b, ports):
            return self.register(
                self.adapter.join(a, b, ports), self.meta[id(a)] | self.meta[id(b)]
            )

        before = self.payload_work["bulk_payload_recomputed_hierarchy_records"]
        new, marked = refresh_many(
            root,
            [leaves[e] for e in affected],
            lambda node: parents[id(node)],
            change,
            create,
            join,
            lambda e: self.payload[edge_indices[tuple(sorted(e))]],
            self.payload_work,
        )
        assert self.payload_work["bulk_payload_recomputed_hierarchy_records"] - before == marked
        self.check(new, self.full, True)
        assert new.summary.load[0] / new.summary.matrix[0][0] == self.values[self.seed]
        self.counts["simultaneous_source_class_payload_refreshes"] += 1
        self.counts["marked_union_only_recomputed_records"] += marked
        # The backend shared the old node map during the transaction.
        old_original[self.seed] = old_root_data
        self.original, self.weight_values, self.values, self.payload = (
            old_original,
            old_weights,
            old_values,
            old_payload,
        )
        self.adapter.backend.original = self.original
        for edge in affected:
            self.adapter.backend.replace_weight(edge, old_weights[edge])
        self.oracle_cache.clear()
        self.check(root, self.full, True)
        self.counts["retained_old_weighted_root_checks"] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, work, callbacks, backend, hull = Counter(), Counter(), Counter(), Counter(), Counter()
    for n in range(2, args.max_n + 1):
        for tree in nx.nonisomorphic_trees(n):
            tree = nx.convert_node_labels_to_integers(tree, ordering="sorted")
            for seed in tree:
                for mask in sorted({0, 2**n - 1, sum(1 << i for i in tree if i % 2 == 0)}):
                    for alpha in [F(1, 3), F(1, 1009)]:
                        case = WeightedCase(tree, seed, mask, alpha, counts)
                        old = case.enumerate(False)
                        root = case.expose(old)
                        case.simultaneous_root_refresh(root)
                        counts["weighted_physical_source_cases"] += 1
                        work.update(case.payload_work)
                        callbacks.update(case.adapter.counts)
                        backend.update(case.adapter.backend.counts)
                        hull.update(case.adapter.backend.arena.counts)
    counts["recovered_quotient_mean_coordinates"] = counts.pop("recovered_original_coordinates", 0)
    result = {
        "description": __doc__,
        "max_n": args.max_n,
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all nonisomorphic quotient trees of orders 2 through max_n, all seed classes, sizes 2+i%3 and independent/clique/alternating type masks",
        "alpha_lazy": ["1/3", "1/1009"],
        "lambda_rule": "bar_alpha / (12*(2*physical_n)^physical_n)",
        "accuracy_namespace": "physical obstacle lambda; no terminal ACL approximation is claimed by this callback audit",
        "stopping_rule": "exhaust all prescribed positive faces and callback transactions; virtual positive thresholds include exact ties",
        "audit_only": dict(counts),
        "charged_weight_and_bulk_payload_units": dict(work),
        "executed_callback_counts": dict(callbacks),
        "executed_numerical_backend_counts": dict(backend),
        "executed_hull_primitive_counts": dict(hull),
        "scope": "Callbacks and dirty-ancestor refresh are implemented; supplied exhaustive hierarchy construction/indexing and physical dense validation are not a fast online balancing or local producer.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "frontier_exact.py",
                "frontier_neighborhood_types.py",
                "geometric_value_events.py",
                "path_cluster_reporter.py",
                "top_tree_callback_adapter.py",
                "projective_hull_rope.py",
            ]
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
