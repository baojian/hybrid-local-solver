"""Exact uniform-shift audit for rooted clusters with an interior physical seed.

The constant C=1/bar_alpha makes every edge-induced cluster load negative:
b_C'=e_seed-lambda*d-C*(d-gamma*degree_C). Per-edge gamma*C additions
implement this without changing every incident edge when an active degree grows.
This is an algebra/application audit, not a unicyclic solver implementation.
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
import time

from geometric_value_events import solve
import networkx as nx
from path_cluster_reporter import Backend
from top_tree_callback_adapter import Adapter, AuditCase


class ShiftedBackend(Backend):
    def __init__(self, original, gamma, shift):
        super().__init__(original, gamma)
        self.shift = shift

    def edge(self, parent, child, rows):
        out = super().edge(parent, child, rows)
        self.counts["shifted_edge_load_words"] += 2
        return replace(out, load=tuple(value + self.gamma * self.shift for value in out.load))


class ShiftedCase(AuditCase):
    def __init__(self, tree, physical_seed, anchor, alpha, counts):
        super().__init__(tree, anchor, alpha, counts)
        self.physical_seed, self.anchor = physical_seed, anchor
        self.shift = 1 / self.bar
        self.unshifted_load = {
            i: F(i == physical_seed) - self.lam * (tree.degree(i) + 1) for i in tree
        }
        self.original = {
            i: (F(tree.degree(i) + 1), self.unshifted_load[i] - self.shift * (tree.degree(i) + 1))
            for i in tree
        }
        # Small reports yield positive gates on this legal, unfinished core face;
        # large reports remain quiet. Both signs of reporter intercept occur.
        self.report_degrees = {i: F(1) if i % 2 == 0 else d for i, d in self.report_degrees.items()}
        self.rows = {
            i: (self.lam * self.report_degrees[i] / self.gamma - self.shift, self.n + i)
            for i in tree
        }
        self.payload = {
            k: [(i, *self.rows[i]) for i in tree if self.home[i] == k]
            for k in range(len(self.edges))
        }
        matrix = [
            [
                self.original[i][0] if i == j else -self.gamma if j in tree[i] else F(0)
                for j in range(self.n)
            ]
            for i in range(self.n)
        ]
        original_values = solve(matrix, [self.unshifted_load[i] for i in range(self.n)])
        assert min(original_values) > 0 and max(original_values) < self.shift
        shifted_load = [
            self.original[i][1] + self.gamma * self.shift * tree.degree(i) for i in range(self.n)
        ]
        assert max(shifted_load) < 0
        self.values = solve(matrix, shifted_load)
        assert all(self.values[i] + self.shift == original_values[i] for i in tree)
        self.adapter = Adapter(anchor, self.depth, self.original, self.gamma)
        self.adapter.backend = ShiftedBackend(self.original, self.gamma, self.shift)
        self.oracle_cache.clear()
        self.counts["whole_face_shift_identities"] += 1

    def oracle(self, mask, ports):
        key = mask, ports
        if key in self.oracle_cache:
            return self.oracle_cache[key]
        vertices = self.masks[mask][0]
        interior = sorted(vertices - set(ports))
        chosen = [edge for k, edge in enumerate(self.edges) if mask & (1 << k)]
        selected = {frozenset(edge) for edge in chosen}
        degree = Counter(i for edge in chosen for i in edge)

        def entry(i, j):
            return (
                self.original[i][0]
                if i == j
                else -self.gamma
                if frozenset((i, j)) in selected
                else F(0)
            )

        def load(i):
            out = self.original[i][1] + self.gamma * self.shift * degree[i]
            assert out < 0
            return out

        inner = [[entry(i, j) for j in interior] for i in interior]
        offset = dict(zip(interior, solve(inner, [load(i) for i in interior])))
        original_offset = dict(
            zip(interior, solve(inner, [self.unshifted_load[i] for i in interior]))
        )
        coefficients = {i: [] for i in vertices}
        for p in ports:
            col = solve(inner, [-entry(i, p) for i in interior])
            for i, value in zip(interior, col):
                coefficients[i].append(value)
        for k, p in enumerate(ports):
            coefficients[p] = [F(k == j) for j in range(len(ports))]
            offset[p] = original_offset[p] = F(0)
        for i in vertices:
            assert offset[i] == original_offset[i] + self.shift * (sum(coefficients[i]) - 1)
            self.counts["conditional_shift_identities"] += 1
        matrix = tuple(
            tuple(
                entry(i, j) + sum(entry(i, h) * coefficients[h][k] for h in interior)
                for k, j in enumerate(ports)
            )
            for i in ports
        )
        rhs = tuple(load(i) - sum(entry(i, h) * offset[h] for h in interior) for i in ports)
        raw = []
        for k, rows in self.payload.items():
            if not mask & (1 << k):
                continue
            for home, threshold, label in rows:
                aa = coefficients[home]
                cc = offset[home] - threshold
                assert min(aa) >= 0 and sum(aa) > 0
                original_constant = original_offset[home] - (threshold + self.shift)
                assert cc == original_constant + self.shift * sum(aa)
                self.counts["positive_intercept_rows"] += cc > 0
                self.counts["negative_intercept_rows"] += cc < 0
                raw.append((aa[0], cc, sum(aa), label) if len(ports) == 2 else (-cc / aa[0], label))
        self.counts["valid_clusters_with_physical_seed_interior"] += self.physical_seed in interior
        self.counts["independent_schur_oracles"] += 1
        self.counts["independent_owned_rows"] += len(raw)
        result = matrix, rhs, raw
        self.oracle_cache[key] = result
        return result


def closure_witnesses():
    """Exact two-port cycle restoration, including an interior physical seed."""
    cases = [
        ([(0, 1), (1, 2), (2, 0)], 0, (0, 2), F(1, 3), F(1, 20)),
        ([(0, 1), (1, 2), (2, 3), (3, 1)], 0, (1, 3), F(1, 7), F(1, 100)),
    ]
    results = []
    for edges, physical_seed, extra, alpha, lam in cases:
        graph = nx.Graph(edges)
        tree = graph.copy()
        tree.remove_edge(*extra)
        n = len(graph)
        gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        shift = 1 / bar
        original = {
            i: (
                F(graph.degree(i)),
                F(i == physical_seed) - lam * graph.degree(i) - shift * graph.degree(i),
            )
            for i in graph
        }
        backend = ShiftedBackend(original, gamma, shift)
        if n == 3:
            left, right = backend.edge(0, 1, []), backend.edge(1, 2, [])
            root = backend.compress(left, right)
        else:
            source_side = backend.forget(backend.edge(1, 0, []))
            left = backend.rake(source_side, backend.edge(1, 2, []))
            root = backend.compress(left, backend.edge(2, 3, []))
        assert root.ports == extra
        closed = [list(row) for row in root.matrix]
        closed[0][1] -= gamma
        closed[1][0] -= gamma
        rhs = [x + gamma * shift for x in root.load]
        port_values = solve(closed, rhs)
        shifted = backend.recover(root, port_values)
        got = [shifted[i] + shift for i in range(n)]
        matrix = [
            [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in range(n)]
            for i in range(n)
        ]
        load = [F(i == physical_seed) - lam * graph.degree(i) for i in range(n)]
        exact = solve(matrix, load)
        assert got == exact and min(got) > 0
        tree_matrix = [
            [F(graph.degree(i)) if i == j else -gamma if j in tree[i] else F(0) for j in range(n)]
            for i in range(n)
        ]
        unclosed = solve(tree_matrix, load)
        out = {
            "edges": edges,
            "physical_seed": physical_seed,
            "extra_edge_ports": extra,
            "alpha_lazy": str(alpha),
            "lambda": str(lam),
            "eps_appr": str(2 * lam),
            "full_face_values": [str(x) for x in got],
            "uncorrected_spanning_tree_values": [str(x) for x in unclosed],
            "physical_seed_eliminated_inside_cluster": physical_seed not in extra,
        }
        if n == 3:
            old = solve([row[:2] for row in matrix[:2]], load[:2])
            two_parent_gate = gamma * sum(old) - lam * graph.degree(2)
            only_tree_parent_gate = gamma * old[1] - lam * graph.degree(2)
            assert gamma * load[0] / graph.degree(0) - lam * graph.degree(1) > 0
            assert two_parent_gate > 0 > only_tree_parent_gate and unclosed[2] < 0
            assert exact == [F(1, 2), F(1, 10), F(1, 10)]
            out.update(
                legal_prefix=[0, 1],
                two_parent_gate=str(two_parent_gate),
                single_tree_parent_gate=str(only_tree_parent_gate),
            )
        results.append(out)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, callbacks, backend, hull = Counter(), Counter(), Counter(), Counter()
    for n in range(2, args.max_n + 1):
        for tree0 in nx.nonisomorphic_trees(n):
            tree = nx.convert_node_labels_to_integers(tree0, ordering="sorted")
            for physical_seed in tree:
                distances = nx.single_source_shortest_path_length(tree, physical_seed)
                farthest = max(tree, key=lambda i: (distances[i], i))
                for anchor in sorted({physical_seed, farthest}):
                    for alpha in [F(1, 3), F(1, 1009)]:
                        case = ShiftedCase(tree, physical_seed, anchor, alpha, counts)
                        old = case.enumerate(False)
                        out = case.expose(old)
                        case.check(out, case.full, True)
                        callbacks.update(case.adapter.counts)
                        backend.update(case.adapter.backend.counts)
                        hull.update(case.adapter.backend.arena.counts)
                        counts["canonical_positive_faces"] += 1
        print(json.dumps({"through_n": n, "faces": counts["canonical_positive_faces"]}), flush=True)
    assert counts["positive_intercept_rows"] > 0
    assert counts["valid_clusters_with_physical_seed_interior"] > 0
    result = {
        "audit": "incremental_active_set_sdd.shifted_tree_clusters",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all nonisomorphic core trees through max_n; one private-star report per core vertex; alternating report degree one and large",
        "physical_seed": "every core vertex",
        "geometric_anchor": "physical seed and a farthest core vertex",
        "max_n": args.max_n,
        "alpha_lazy": ["1/3", "1/1009"],
        "lambda_rule": "bar_alpha/(12*(2*n)^n)",
        "eps_appr": "2*lambda",
        "shift_rule": "C=1/bar_alpha; w=u-C; constant base load e_seed-lambda*d-C*d; gamma*C per edge endpoint",
        "stopping_rule": "unfinished positive core faces; exact cluster sign queries checked without claiming a stop or unicyclic algorithm",
        "scope": "uniform-shift and application-callback audit; supplied hierarchies and dense oracles are reference-only",
        "cycle_closure_witnesses": closure_witnesses(),
        "audit_only": dict(counts),
        "adapter_counts": dict(callbacks),
        "backend_counts": dict(backend),
        "hull_counts": dict(hull),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "top_tree_callback_adapter",
                "path_cluster_reporter",
                "projective_hull_rope",
            ]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
