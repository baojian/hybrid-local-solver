"""Exact named-coordinate queries through constant-size cluster recovery records.

The query starts at a known incident edge and follows supplied current parent
pointers. The audit builds these pointers by a full traversal, counted separately;
that builder is not an online hierarchy algorithm. A live callback implementation
can update at most two new helper records' child pointers per structural callback.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

import networkx as nx
from shifted_tree_clusters import ShiftedCase


def point_query(vertex, leaf, parent_of, root, port_values, counts):
    """O(height) affine pullback, constant-size live state, no subtree search."""
    assert leaf.kind == "edge" and vertex in leaf.ports
    counts["named_queries"] += 1
    node = leaf
    row = tuple(F(p == vertex) for p in node.ports) + (F(0),)
    height = 0
    while node is not root:
        parent = parent_of(node)
        counts["parent_pointer_reads"] += 1
        assert parent is not None
        k = len(parent.ports)
        known = {
            p: tuple(F(a == b) for a in range(k)) + (F(0),) for b, p in enumerate(parent.ports)
        }
        if parent.kind == "compress":
            middle, eta, zeta, shift = parent.recovery
            known[middle] = (eta, zeta, shift)
        elif parent.kind == "forget":
            far, eta, shift = parent.recovery
            known[far] = (eta, shift)
        else:
            assert parent.kind == "rake"
        assert any(child is node for child in parent.children)
        row = tuple(
            sum(row[j] * known[p][i] for j, p in enumerate(node.ports)) + (row[-1] if i == k else 0)
            for i in range(k + 1)
        )
        counts["affine_pullbacks"] += 1
        # At most 2 input coefficients, 3 outputs, and a constant-size map.
        counts["pullback_multiply_add_pairs"] += len(node.ports) * (k + 1)
        counts[f"through_{parent.kind}"] += 1
        height += 1
        node = parent
    counts["maximum_backend_parent_height"] = max(counts["maximum_backend_parent_height"], height)
    return sum(a * x for a, x in zip(row[:-1], port_values)) + row[-1]


def audit_index(root, counts):
    """Reference-only whole-hierarchy indexing; never part of query work."""
    parents, leaves, stack = {id(root): None}, {}, [root]
    while stack:
        node = stack.pop()
        counts["audit_index_cluster_visits"] += 1
        if node.kind == "edge":
            for vertex in node.ports:
                leaves.setdefault(vertex, node)
        for child in node.children:
            assert id(child) not in parents
            parents[id(child)] = node
            stack.append(child)
    return parents, leaves


class QueryCase(ShiftedCase):
    def __init__(self, *args):
        self.query_counts, self.index_counts = Counter(), Counter()
        super().__init__(*args)

    def check(self, snapshot, mask, exposed):
        super().check(snapshot, mask, exposed)
        if snapshot.summary is None:
            return
        root = snapshot.summary
        parents, leaves = audit_index(root, self.index_counts)
        # Include two unrelated port assignments: the query is a conditional
        # identity, not merely a match on one solved physical face.
        for values in [tuple(self.values[p] for p in root.ports), (F(3, 7),) * len(root.ports)]:
            recovered = self.adapter.backend.recover(root, values)
            for vertex, leaf in leaves.items():
                got = point_query(
                    vertex,
                    leaf,
                    lambda node: parents[id(node)],
                    root,
                    values,
                    self.query_counts,
                )
                assert got == recovered[vertex]
                self.counts["exact_named_coordinate_comparisons"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, queries, index = Counter(), Counter(), Counter()
    for n in range(2, args.max_n + 1):
        for raw in nx.nonisomorphic_trees(n):
            tree = nx.convert_node_labels_to_integers(raw, ordering="sorted")
            for seed in tree:
                distances = nx.single_source_shortest_path_length(tree, seed)
                far = max(tree, key=lambda i: (distances[i], i))
                for anchor in sorted({seed, far}):
                    for alpha in [F(1, 3), F(1, 1009)]:
                        case = QueryCase(tree, seed, anchor, alpha, counts)
                        old = case.enumerate(False)
                        root = case.expose(old)
                        for edge_index in sorted({0, len(case.edges) - 1}):
                            case.payload_refresh(root, edge_index)
                        case.check(root, case.full, True)
                        maximum = case.query_counts.pop("maximum_backend_parent_height", 0)
                        queries.update(case.query_counts)
                        queries["maximum_backend_parent_height"] = max(
                            queries["maximum_backend_parent_height"], maximum
                        )
                        index.update(case.index_counts)
                        counts["canonical_faces"] += 1
        print(json.dumps({"through_n": n, "faces": counts["canonical_faces"]}), flush=True)
    result = {
        "audit": "incremental_active_set_sdd.cluster_point_queries",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all nonisomorphic core trees through max_n, alternating small and large private-star boundary reports",
        "seed": "every core vertex; geometric anchor at seed and a farthest core vertex",
        "max_n": args.max_n,
        "alpha_lazy": ["1/3", "1/1009"],
        "lambda_rule": "bar_alpha/(12*(2*n)^n)",
        "eps_appr": "2*lambda",
        "stopping_rule": "conditional identities on valid clusters, solved face and arbitrary port assignments; no stopping decision",
        "scope": "query implementation uses supplied incident leaf and current parent pointers; full indexing and hierarchy enumeration are audit-only",
        "query_counts": dict(queries),
        "audit_index_counts": dict(index),
        "audit_only": dict(counts),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "shifted_tree_clusters",
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
