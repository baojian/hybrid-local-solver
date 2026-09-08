"""Charged supplied-tree indexing, weighted pieces and corridor routing.

The construction receives the whole positive-weight graph and a spanning
tree. It does not choose a low-stretch tree, sparsify the core, or discover
a local graph. NetworkX paths and dense PSD tests are validators only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from local_gap_certificate import sort_records
from spectral_preconditioner_floor import certify_psd, difference, laplacian
from weighted_tree_ownership import Piece, memberships, ownership, refine
import networkx as nx


class TreeIndex:
    def __init__(self, n, original, tree_ids, root, counts):
        assert n >= 1 and len(tree_ids) == n - 1 and 0 <= root < n
        self.n, self.counts = n, counts
        self.edges, self.resistance, self.adjacency = [], [], [[] for _ in range(n)]
        self.parent, self.parent_edge = [-1] * n, [-1] * n
        self.depth, self.prefix, self.order = [0] * n, [F(0)] * n, [root]
        counts["tree_index_base_array_words"] += 6 * n
        for edge, original_id in enumerate(tree_ids):
            u, v, c = original[original_id]
            assert 0 <= u < n and 0 <= v < n and u != v and c > 0
            self.edges.append((u, v))
            self.resistance.append(1 / c)
            self.adjacency[u].append((v, edge))
            self.adjacency[v].append((u, edge))
            counts["tree_input_and_adjacency_words_with_copy_budget"] += 18
        self.parent[root] = root
        for vertex in self.order:
            for neighbor, edge in self.adjacency[vertex]:
                counts["tree_index_traversal_incidence_operations"] += 4
                if neighbor == self.parent[vertex]:
                    continue
                assert self.parent[neighbor] == -1
                self.parent[neighbor], self.parent_edge[neighbor] = vertex, edge
                self.depth[neighbor] = self.depth[vertex] + 1
                self.prefix[neighbor] = self.prefix[vertex] + self.resistance[edge]
                self.order.append(neighbor)
                counts["tree_index_parent_prefix_and_order_operations"] += 12
        assert len(self.order) == n
        self.levels = max(1, n.bit_length())
        self.ancestors = [self.parent.copy()]
        counts["binary_ancestor_words_and_copy_budget"] += 2 * n
        for _ in range(1, self.levels):
            previous = self.ancestors[-1]
            self.ancestors.append([previous[previous[v]] for v in range(n)])
            counts["binary_ancestor_words_and_copy_budget"] += 4 * n
        differences = [F(0)] * n
        self.stretches, self.loads = [], [F(0)] * n
        counts["congestion_load_array_words"] += 2 * n
        for u, v, c in original:
            assert 0 <= u < n and 0 <= v < n and u != v and c > 0
            ancestor = self.lca(u, v)
            stretch = c * (self.prefix[u] + self.prefix[v] - 2 * self.prefix[ancestor])
            self.stretches.append(stretch)
            self.loads[u] += stretch
            self.loads[v] += stretch
            differences[u] += c
            differences[v] += c
            differences[ancestor] -= 2 * c
            counts["original_edge_stretch_load_and_difference_operations"] += 28
        self.total_stretch = sum(self.stretches, F(0))
        self.congestion = [F(0)] * (n - 1)
        counts["stretch_sum_and_congestion_array_operations"] += len(original) + n - 1
        for vertex in reversed(self.order[1:]):
            self.congestion[self.parent_edge[vertex]] = differences[vertex]
            differences[self.parent[vertex]] += differences[vertex]
            counts["postorder_congestion_operations_including_order_copy"] += 9
        assert differences[root] == 0
        counts["released_congestion_difference_words"] += n

    def lca(self, u, v):
        counts = self.counts
        counts["lca_query_setup_operations"] += 4
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        gap = self.depth[u] - self.depth[v]
        for level in range(self.levels):
            counts["lca_level_operations"] += 3
            if gap & (1 << level):
                u = self.ancestors[level][u]
                counts["lca_ancestor_reads"] += 1
        if u == v:
            return u
        for level in reversed(range(self.levels)):
            counts["lca_level_operations"] += 4
            left, right = self.ancestors[level][u], self.ancestors[level][v]
            if left != right:
                u, v = left, right
        return self.parent[u]

    def corridor(self, u, v):
        ancestor, edges = self.lca(u, v), []
        for vertex in (u, v):
            while vertex != ancestor:
                edges.append(self.parent_edge[vertex])
                vertex = self.parent[vertex]
                self.counts["corridor_parent_reads_and_output_copy_budget"] += 6
        return edges


@dataclass
class RootedPart:
    piece: int
    root: int
    edges: list[int]
    vertices: list[int]


def build(n, original, tree_ids, root, counts, *, j=None, theta=None):
    assert (j is None) != (theta is None)
    if j is not None:
        assert 1 <= j <= n
    index = TreeIndex(n, original, tree_ids, root, counts)
    if j is not None and (j < 64 or n == 1):
        pieces = [Piece(list(range(n - 1)), list(range(n)), root)]
        counts["single_piece_edge_owner_words"] += 2 * n - 1
        multiplicity = memberships(n, index.edges, pieces, counts)
    else:
        theta = F(64) * index.total_stretch / j if j is not None else theta
        pieces, multiplicity = ownership(n, index.edges, index.loads, theta, root, counts)
        pieces, multiplicity = refine(n, index.edges, pieces, multiplicity, counts)
    owner = [-1] * n
    assigned = [[] for _ in pieces]
    counts["owner_assignment_array_words"] += n + len(pieces)
    for p, piece in enumerate(pieces):
        for vertex in piece.owners:
            assert owner[vertex] == -1
            owner[vertex] = p
            counts["owner_map_writes_and_checks"] += 2
    for e, (u, v, _) in enumerate(original):
        assigned[owner[u]].append(e)
        if owner[u] != owner[v]:
            assigned[owner[v]].append(e)
        counts["edge_owner_reads_and_assigned_list_copy_budget"] += 10
    roots = [v for v in range(n) if multiplicity[v] > 1] if len(pieces) > 1 else [root]
    counts["root_membership_reads_and_list_copy_budget"] += 3 * n
    is_root = [False] * n
    for vertex in roots:
        is_root[vertex] = True
    cuts, corridors, cut_of, boundaries = [False] * (n - 1), [], [], []
    counts["root_and_cut_array_words"] += 2 * n - 1
    for piece in pieces:
        boundary = [v for v in piece.vertices if is_root[v]]
        assert 1 <= len(boundary) <= 2
        boundaries.append(boundary)
        counts["piece_boundary_scans_and_copy_budget"] += len(piece.vertices) + 3 * len(boundary)
        corridor, cut = [], -1
        if len(boundary) == 2:
            corridor = index.corridor(*boundary)
            for edge in corridor:
                counts["minimum_congestion_comparison_operations"] += 4
                if cut == -1 or (index.congestion[edge], edge) < (index.congestion[cut], cut):
                    cut = edge
            assert cut >= 0 and not cuts[cut]
            cuts[cut] = True
        corridors.append(corridor)
        cut_of.append(cut)
        counts["corridor_header_and_cut_record_words"] += 3
    assert sum(cuts) + 1 == len(roots)
    local_index, parts = [-1] * n, []
    counts["rooted_part_global_index_words"] += n
    for p, piece in enumerate(pieces):
        vertices = piece.vertices
        for local, vertex in enumerate(vertices):
            local_index[vertex] = local
        adjacency = [[] for _ in vertices]
        for edge in piece.edges:
            if edge == cut_of[p]:
                continue
            u, v = (local_index[v] for v in index.edges[edge])
            adjacency[u].append((v, edge))
            adjacency[v].append((u, edge))
            counts["rooted_part_local_adjacency_words_and_copy_budget"] += 8
        seen = [False] * len(vertices)
        counts["rooted_part_local_array_and_index_operations"] += 3 * len(vertices)
        for boundary in boundaries[p]:
            start = local_index[boundary]
            assert not seen[start]
            seen[start], queue, part_edges = True, [start], []
            for vertex in queue:
                for neighbor, edge in adjacency[vertex]:
                    counts["rooted_part_traversal_incidence_operations"] += 3
                    if seen[neighbor]:
                        continue
                    seen[neighbor] = True
                    queue.append(neighbor)
                    part_edges.append(edge)
                    counts["rooted_part_queue_and_edge_copy_budget"] += 7
            parts.append(RootedPart(p, boundary, part_edges, [vertices[v] for v in queue]))
            counts["rooted_part_header_and_vertex_words"] += 4 + 3 * len(queue)
        assert all(seen)
        counts["released_rooted_part_arrays_and_coverage_checks"] += 3 * len(vertices)
    root_of, queue = [-1] * n, roots.copy()
    counts["forest_root_array_and_queue_words"] += n + 3 * len(roots)
    for vertex in roots:
        root_of[vertex] = vertex
    for vertex in queue:
        for neighbor, edge in index.adjacency[vertex]:
            counts["forest_root_label_incidence_operations"] += 4
            if cuts[edge]:
                continue
            if root_of[neighbor] == -1:
                root_of[neighbor] = root_of[vertex]
                queue.append(neighbor)
                counts["forest_root_label_writes_and_copy_budget"] += 4
            else:
                assert root_of[neighbor] == root_of[vertex]
    assert all(root >= 0 for root in root_of)
    kappa = (
        F(1)
        if n == 1
        else F(256) * index.total_stretch / j
        if j is not None
        else max(F(1), 4 * theta)
    )
    assert kappa >= 1
    core_records = []
    for u, v, c in original:
        a, b = root_of[u], root_of[v]
        if a != b:
            core_records.append(((min(a, b), max(a, b)), c))
            counts["core_record_words_and_copy_budget"] += 8
        counts["core_original_edge_and_root_reads"] += 5
    core_records = sort_records(core_records, counts)
    core = []
    for pair, c in core_records:
        if core and core[-1][:2] == pair:
            u, v, old = core[-1]
            core[-1] = (u, v, old + c)
            counts["parallel_core_conductance_additions"] += 1
        else:
            core.append((*pair, c))
        counts["core_merge_and_record_allocation_operations"] += 8
    q = [(u, v, 3 * c) for u, v, c in core]
    for edge, original_id in enumerate(tree_ids):
        if not cuts[edge]:
            u, v, c = original[original_id]
            q.append((u, v, 3 * kappa * c))
        counts["forest_output_reads_arithmetic_and_copy_budget"] += 12
    counts["core_output_reads_arithmetic_and_copy_budget"] += 10 * len(core)
    counts["released_or_retained_record_reference_budget"] += len(core_records) + n
    return {
        "index": index,
        "pieces": pieces,
        "owner": owner,
        "assigned": assigned,
        "roots": roots,
        "root_of": root_of,
        "cuts": cuts,
        "cut_of": cut_of,
        "corridors": corridors,
        "parts": parts,
        "kappa": kappa,
        "core": core,
        "q": q,
    }


def validator_path(tree, u, v):
    vertices = nx.shortest_path(tree, u, v)
    return [tree[a][b]["index"] for a, b in zip(vertices, vertices[1:])]


def validate(n, original, tree_ids, result, counts, dense):
    index, pieces = result["index"], result["pieces"]
    tree, forest = nx.Graph(), nx.Graph()
    tree.add_nodes_from(range(n))
    forest.add_nodes_from(range(n))
    for e, (u, v) in enumerate(index.edges):
        tree.add_edge(u, v, index=e)
        if not result["cuts"][e]:
            forest.add_edge(u, v, index=e)
    paths = [validator_path(tree, u, v) for u, v, _ in original]
    for e, ((_, _, c), path) in enumerate(zip(original, paths)):
        assert c * sum((index.resistance[f] for f in path), F(0)) == index.stretches[e]
        counts["independent_tree_stretch_checks"] += 1
    actual_congestion = [F(0)] * (n - 1)
    for (_, _, c), path in zip(original, paths):
        for f in path:
            actual_congestion[f] += c
    assert actual_congestion == index.congestion
    counts["independent_all_tree_congestion_checks"] += n - 1
    components = list(nx.connected_components(forest))
    for component in components:
        roots = set(result["roots"]) & component
        assert len(roots) == 1
        assert all(result["root_of"][v] in roots for v in component)
    assert len(components) == len(result["roots"])
    part_of, pieces_of_edge = {}, {}
    for p, piece in enumerate(pieces):
        for f in piece.edges:
            pieces_of_edge[f] = p
    for b, part in enumerate(result["parts"]):
        assert part.root in part.vertices
        assert all(result["root_of"][v] == part.root for v in part.vertices)
        for f in part.edges:
            assert f not in part_of
            part_of[f] = b
    assert set(part_of) == {e for e in range(n - 1) if not result["cuts"][e]}
    for left, right in itertools.combinations(result["parts"], 2):
        shared = set(left.vertices) & set(right.vertices)
        assert not shared or left.root == right.root and shared == {left.root}
        counts["independent_rooted_part_intersection_checks"] += 1
    local = [F(0)] * len(result["parts"])
    for e, (u, v, c) in enumerate(original):
        if result["root_of"][u] == result["root_of"][v]:
            route = validator_path(forest, u, v)
        else:
            route = validator_path(forest, u, result["root_of"][u])
            route += validator_path(forest, v, result["root_of"][v])
        blocks = [b for b, _ in itertools.groupby(part_of[f] for f in route)]
        assert len(blocks) <= 2 and len(blocks) == len(set(blocks))
        piece_lengths = Counter()
        for f in route:
            local[part_of[f]] += c * index.resistance[f]
            piece_lengths[pieces_of_edge[f]] += index.resistance[f]
        for p, length in piece_lengths.items():
            assert e in result["assigned"][p]
            assert set(paths[e]) & set(pieces[p].edges)
            cut, corridor = result["cut_of"][p], result["corridors"][p]
            if cut == -1 or cut not in paths[e]:
                assert c * length <= index.stretches[e]
                counts["corrected_no_cut_routing_cases"] += 1
            else:
                extra = sum((index.resistance[f] for f in corridor if f not in paths[e]), F(0))
                assert c * length <= index.stretches[e] + c * extra
                counts["corrected_cut_routing_cases"] += 1
    for p, piece in enumerate(pieces):
        assigned_mass = sum((index.stretches[e] for e in result["assigned"][p]), F(0))
        assert assigned_mass <= sum((index.loads[v] for v in piece.owners), F(0))
        for b, part in enumerate(result["parts"]):
            if part.piece == p:
                assert local[b] <= 2 * assigned_mass
                assert local[b] <= result["kappa"]
                counts["rooted_piece_load_checks"] += 1
        corridor, cut = result["corridors"][p], result["cut_of"][p]
        if cut != -1:
            assigned = set(result["assigned"][p])
            restricted = [
                sum(
                    (c for e, (_, _, c) in enumerate(original) if e in assigned and f in paths[e]),
                    F(0),
                )
                for f in corridor
            ]
            offsets = [index.congestion[f] - load for f, load in zip(corridor, restricted)]
            assert len(set(offsets)) == 1 and offsets[0] >= 0
            assert restricted[corridor.index(cut)] == min(restricted)
            resistance = sum((index.resistance[f] for f in corridor), F(0))
            assert resistance * min(restricted) <= assigned_mass
            counts["common_offset_corridor_checks"] += 1
            counts["positive_common_offset_corridors"] += offsets[0] > 0
            counts["multiple_edge_corridors"] += len(corridor) > 1
    if dense:
        g, q = laplacian(n, original), laplacian(n, result["q"])
        certify_psd(difference(q, g), counts)
        certify_psd(difference(g, q, F(1, 21) / result["kappa"]), counts)
        counts["weighted_spectral_compositions"] += 1
    counts["supplied_routing_cases"] += 1
    counts["nonunit_weight_cases"] += any(c != 1 for _, _, c in original)
    counts["shared_root_multiple_parts"] += len(result["parts"]) - len(result["roots"])


def audit_case(n, original, tree_ids, root, counts, work, *, j=None, theta=None, dense=True):
    local_work = Counter()
    result = build(n, original, tree_ids, root, local_work, j=j, theta=theta)
    validate(n, original, tree_ids, result, counts, dense)
    if j is not None:
        assert len(result["roots"]) <= j
        assert len(result["pieces"]) <= j / 4 if j >= 64 else len(result["pieces"]) == 1
        counts["actual_j_budget_constructions"] += 1
    budget = (n + len(original)) * max(1, (n + len(original)).bit_length())
    assert sum(local_work.values()) <= 5000 * budget
    work.update(local_work)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work, rng = time.monotonic(), Counter(), Counter(), random.Random(908040)
    audit_case(1, [], [], 0, counts, work, j=1)
    for graph in nx.graph_atlas_g():
        n = len(graph)
        if not 2 <= n <= (5 if args.full else 4) or not nx.is_connected(graph):
            continue
        edges = list(graph.edges())
        profiles = [[F(1)] * len(edges)]
        if args.full:
            profiles += [[F(2) ** ([-80, 80, 0, 1][i % 4]) for i in range(len(edges))]]
        for tree_ids in itertools.combinations(range(len(edges)), n - 1):
            tree = nx.Graph()
            tree.add_nodes_from(range(n))
            tree.add_edges_from(edges[e] for e in tree_ids)
            if not nx.is_tree(tree):
                continue
            for weights in profiles:
                original = [(u, v, c) for (u, v), c in zip(edges, weights)]
                total = sum(
                    c
                    * sum(
                        1 / weights[next(i for i in tree_ids if set(edges[i]) == {a, b})]
                        for a, b in nx.utils.pairwise(nx.shortest_path(tree, u, v))
                    )
                    for u, v, c in original
                )
                for root in range(n) if args.full else [0]:
                    for theta in [total / (2 * n), total / n, total / 2, total, 2 * total]:
                        audit_case(n, original, tree_ids, root, counts, work, theta=theta)
                    audit_case(n, original, tree_ids, root, counts, work, j=n)
    for n in [64, 128, 512] if args.full else [64]:
        for shape in ("star", "path", "random"):
            tree = (
                nx.star_graph(n - 1)
                if shape == "star"
                else nx.path_graph(n)
                if shape == "path"
                else nx.from_prufer_sequence([rng.randrange(n) for _ in range(n - 2)])
            )
            edges = list(tree.edges())
            for _ in range(n):
                u, v = rng.sample(range(n), 2)
                edges.append((u, v))
            original = [(u, v, F(2) ** ([-80, 80, 0, 1][e % 4])) for e, (u, v) in enumerate(edges)]
            for root in [0, n // 2, n - 1]:
                for j in [1, 63, 64, n]:
                    audit_case(
                        n, original, list(range(n - 1)), root, counts, work, j=j, dense=False
                    )
    assert counts["common_offset_corridor_checks"] > 0
    assert counts["corrected_cut_routing_cases"] > 0
    result = {
        "audit": "incremental_active_set_sdd.weighted_corridor_routing",
        "scope": "Supplied positive-weight graph and supplied spanning tree; charged indexing, ownership, corridor cuts and spectral assembly only. No low-stretch tree selection, core sparsification or local OP3 algorithm.",
        "arithmetic": "exact fractions; charged exact-real word model, not bit complexity",
        "audit_only": dict(counts),
        "charged_construction": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "weighted_tree_ownership.py",
                "local_gap_certificate.py",
                "spectral_preconditioner_floor.py",
            ]
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
