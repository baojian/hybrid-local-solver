"""Exact selected conditional Green entries from cluster elimination records.

Each affine pullback adds an independent eliminated-coordinate variance.
Named responses use one parent walk; two saved noise traces give a selected
conditional covariance. Supplied parent indices and dense inverses are audit-only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

from cluster_point_queries import audit_index
from geometric_value_events import solve
import networkx as nx
from shifted_tree_clusters import ShiftedCase


@dataclass
class Response:
    root_id: int
    row: tuple
    variance: F
    noises: dict
    has_trace: bool


def response_trace(vertex, leaf, parent_of, root, backend, counts, keep_trace=True):
    assert leaf.kind == "edge" and vertex in leaf.ports
    row = tuple(F(p == vertex) for p in leaf.ports) + (F(0),)
    node, variance, noises, height = leaf, F(0), {}, 0
    counts["response_queries"] += 1
    while node is not root:
        parent = parent_of(node)
        counts["parent_pointer_reads"] += 1
        k = len(parent.ports)
        known = {
            p: tuple(F(a == b) for a in range(k)) + (F(0),) for b, p in enumerate(parent.ports)
        }
        eliminated, pivot = None, None
        if parent.kind == "compress":
            eliminated, eta, zeta, offset = parent.recovery
            known[eliminated] = (eta, zeta, offset)
            left, right = parent.children
            pivot = left.matrix[1][1] + right.matrix[0][0] - backend.original[eliminated][0]
        elif parent.kind == "forget":
            eliminated, eta, offset = parent.recovery
            known[eliminated] = (eta, offset)
            pivot = parent.children[0].matrix[1][1]
        else:
            assert parent.kind == "rake"
        assert any(child is node for child in parent.children)
        if eliminated is not None:
            coefficient = row[node.ports.index(eliminated)] if eliminated in node.ports else F(0)
            assert pivot > 0 and coefficient >= 0
            variance += coefficient * coefficient / pivot
            counts["elimination_variance_terms"] += 1
            if coefficient and keep_trace:
                noises[id(parent)] = (coefficient, 1 / pivot)
                counts["retained_noise_coefficients"] += 1
        row = tuple(
            sum(row[j] * known[p][i] for j, p in enumerate(node.ports)) + (row[-1] if i == k else 0)
            for i in range(k + 1)
        )
        counts["affine_pullbacks"] += 1
        height += 1
        node = parent
    counts["maximum_parent_height"] = max(counts["maximum_parent_height"], height)
    return Response(id(root), row, variance, noises, keep_trace)


def conditional_cross(left, right, counts):
    """Same conditional root; unrelated component independence is a caller fact."""
    assert left.has_trace and right.has_trace
    assert left.root_id == right.root_id
    if len(left.noises) > len(right.noises):
        left, right = right, left
    value = F(0)
    for key, (coefficient, inverse_pivot) in left.noises.items():
        counts["cross_noise_dictionary_reads"] += 1
        other = right.noises.get(key)
        if other is not None:
            assert other[1] == inverse_pivot
            value += coefficient * other[0] * inverse_pivot
            counts["cross_shared_noise_terms"] += 1
    counts["conditional_cross_queries"] += 1
    return value


class GreenCase(ShiftedCase):
    def __init__(self, *args):
        self.green_cache, self.green_counts, self.index_counts = {}, Counter(), Counter()
        super().__init__(*args)

    def dense_green(self, mask, ports):
        key = mask, ports
        if key in self.green_cache:
            return self.green_cache[key]
        vertices = self.masks[mask][0]
        interior = sorted(vertices - set(ports))
        edges = [edge for k, edge in enumerate(self.edges) if mask & (1 << k)]
        selected = {frozenset(edge) for edge in edges}
        degree = Counter(i for edge in edges for i in edge)

        def entry(i, j):
            return (
                self.original[i][0]
                if i == j
                else -self.gamma
                if frozenset((i, j)) in selected
                else F(0)
            )

        inner = [[entry(i, j) for j in interior] for i in interior]
        columns = [solve(inner, [F(i == j) for i in interior]) for j in interior]
        green = {
            (i, j): columns[b][a] for a, i in enumerate(interior) for b, j in enumerate(interior)
        }
        offset = solve(
            inner, [self.original[i][1] + self.gamma * self.shift * degree[i] for i in interior]
        )
        aa = [solve(inner, [-entry(i, p) for i in interior]) for p in ports]
        rows = {i: tuple(col[a] for col in aa) + (offset[a],) for a, i in enumerate(interior)}
        for k, p in enumerate(ports):
            rows[p] = tuple(F(k == j) for j in range(len(ports))) + (F(0),)
        self.counts["independent_conditional_inverse_matrices"] += 1
        self.counts["independent_inverse_columns"] += len(interior)
        out = vertices, green, rows
        self.green_cache[key] = out
        return out

    def check(self, snapshot, mask, exposed):
        super().check(snapshot, mask, exposed)
        if snapshot.summary is None:
            return
        root, backend = snapshot.summary, self.adapter.backend
        links, leaves = audit_index(root, self.index_counts)
        vertices, green, rows = self.dense_green(mask, root.ports)
        responses = {}
        for i in vertices:
            response = response_trace(
                i, leaves[i], lambda node: links[id(node)], root, backend, self.green_counts
            )
            assert response.row == rows[i]
            assert response.variance == green.get((i, i), F(0))
            compact = response_trace(
                i,
                leaves[i],
                lambda node: links[id(node)],
                root,
                backend,
                self.green_counts,
                keep_trace=False,
            )
            assert (
                compact.row == response.row
                and compact.variance == response.variance
                and not compact.noises
            )
            responses[i] = response
            self.counts["conditional_affine_and_variance_checks"] += 1
        for i in vertices:
            for j in vertices:
                assert conditional_cross(
                    responses[i], responses[j], self.green_counts
                ) == green.get((i, j), F(0))
                self.counts["conditional_covariance_pairs"] += 1


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
                        case = GreenCase(tree, seed, anchor, alpha, counts)
                        old = case.enumerate(False)
                        root = case.expose(old)
                        for edge_index in sorted({0, len(case.edges) - 1}):
                            case.payload_refresh(root, edge_index)
                        case.check(root, case.full, True)
                        for key, value in case.green_counts.items():
                            if key.startswith("maximum_"):
                                queries[key] = max(queries[key], value)
                            else:
                                queries[key] += value
                        index.update(case.index_counts)
                        counts["canonical_faces"] += 1
        print(json.dumps({"through_n": n, "faces": counts["canonical_faces"]}), flush=True)
    result = {
        "audit": "incremental_active_set_sdd.cluster_green_queries",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all nonisomorphic core trees through max_n with alternating small/large private-star reports",
        "max_n": args.max_n,
        "seed": "every physical seed; geometric anchor at seed and a farthest core vertex",
        "alpha_lazy": ["1/3", "1/1009"],
        "lambda_rule": "bar_alpha/(12*(2*n)^n)",
        "eps_appr": "2*lambda",
        "stopping_rule": "conditional inverse and affine identities, no stop or inverse-update algorithm claimed",
        "scope": "response and selected covariance queries use supplied parent links; full indices, hierarchy enumeration and dense conditional inverses are audit-only",
        "query_counts": dict(queries),
        "audit_only_index_counts": dict(index),
        "audit_only": dict(counts),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "cluster_point_queries",
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
