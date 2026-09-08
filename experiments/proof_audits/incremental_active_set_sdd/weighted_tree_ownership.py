"""Charged weighted tree ownership and refinement to two-boundary pieces.

This is a supplied-tree construction. It does not find a low-stretch tree
or discover a local graph. All input and output lists are explicit; linked
remainders avoid copying a subtree once per ancestor.
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
import time

import networkx as nx


@dataclass
class Chain:
    head: int = -1
    tail: int = -1
    size: int = 0


class Arena:
    def __init__(self, counts):
        self.values, self.next = [], []
        self.counts = counts

    def singleton(self, value):
        index = len(self.values)
        self.values.append(value)
        self.next.append(-1)
        self.counts["linked_node_words_allocated"] += 2
        self.counts["arena_append_and_copy_budget"] += 4
        return Chain(index, index, 1)

    def join(self, first, second):
        self.counts["constant_time_list_splices"] += 1
        if second.size == 0:
            return first
        if first.size == 0:
            return second
        self.next[first.tail] = second.head
        self.counts["linked_pointer_writes"] += 1
        return Chain(first.head, second.tail, first.size + second.size)

    def materialize(self, chain):
        result, current = [], chain.head
        while current != -1:
            result.append(self.values[current])
            current = self.next[current]
            self.counts["linked_node_reads"] += 2
            self.counts["materialized_list_words_and_copy_budget"] += 3
        assert len(result) == chain.size
        return result


@dataclass
class Bag:
    edges: Chain
    owners: Chain
    mass: F
    top: int


@dataclass
class Piece:
    edges: list[int]
    owners: list[int]
    top: int
    vertices: list[int] | None = None


def memberships(n, edges, pieces, counts):
    stamp, multiplicity = [-1] * n, [0] * n
    counts["membership_array_words_allocated"] += 2 * n
    for index, piece in enumerate(pieces):
        vertices = []
        endpoints = itertools.chain.from_iterable(edges[e] for e in piece.edges)
        for vertex in itertools.chain([piece.top], endpoints):
            counts["membership_stamp_checks"] += 1
            if stamp[vertex] != index:
                stamp[vertex] = index
                multiplicity[vertex] += 1
                vertices.append(vertex)
                counts["membership_words_and_copy_budget"] += 3
        piece.vertices = vertices
    counts["released_membership_scratch_words"] += n
    return multiplicity


def ownership(n, edges, loads, theta, root, counts):
    assert n >= 1 and len(edges) == n - 1 and theta > 0
    assert len(loads) == n and all(load >= 0 for load in loads)
    adjacency = [[] for _ in range(n)]
    counts["original_tree_array_words_allocated"] += n
    for index, (u, v) in enumerate(edges):
        adjacency[u].append((v, index))
        adjacency[v].append((u, index))
        counts["original_tree_edge_reads"] += 1
        counts["tree_adjacency_record_words_and_copy_budget"] += 8
    parents, parent_edges, order = [-1] * n, [-1] * n, [root]
    parents[root] = root
    counts["traversal_array_words_allocated"] += 3 * n
    for vertex in order:
        for neighbor, edge in adjacency[vertex]:
            counts["tree_traversal_incidence_reads"] += 1
            if neighbor == parents[vertex]:
                continue
            assert parents[neighbor] == -1
            parents[neighbor], parent_edges[neighbor] = vertex, edge
            order.append(neighbor)
    assert len(order) == n
    edge_arena, owner_arena = Arena(counts), Arena(counts)
    remainder, finished = [None] * n, []
    counts["remainder_array_words_allocated"] += n
    for vertex in reversed(order):
        owner = owner_arena.singleton(vertex)
        counts["vertex_load_reads_and_comparisons"] += 2
        if loads[vertex] >= theta:
            finished.append(Bag(Chain(), owner, loads[vertex], vertex))
            pending = Bag(Chain(), Chain(), F(0), vertex)
            counts["heavy_singleton_owner_pieces"] += 1
        else:
            pending = Bag(Chain(), owner, loads[vertex], vertex)
        counts["bag_header_words_allocated"] += 8
        for neighbor, _ in adjacency[vertex]:
            counts["postorder_incidence_reads"] += 1
            if parents[neighbor] != vertex:
                continue
            child = remainder[neighbor]
            child_edges = edge_arena.join(child.edges, edge_arena.singleton(parent_edges[neighbor]))
            pending = Bag(
                edge_arena.join(pending.edges, child_edges),
                owner_arena.join(pending.owners, child.owners),
                pending.mass + child.mass,
                vertex,
            )
            counts["bag_header_words_allocated"] += 8
            counts["mass_additions_and_threshold_comparisons"] += 2
            if pending.mass >= theta:
                assert pending.mass < 2 * theta
                finished.append(pending)
                pending = Bag(Chain(), Chain(), F(0), vertex)
                counts["bag_header_words_allocated"] += 8
                counts["threshold_flushed_pieces"] += 1
        assert pending.mass < theta
        remainder[vertex] = pending
    final = remainder[root]
    if final.edges.size or final.owners.size:
        finished.append(final)
        counts["root_remainder_pieces"] += 1
    pieces = [
        Piece(edge_arena.materialize(bag.edges), owner_arena.materialize(bag.owners), bag.top)
        for bag in finished
    ]
    counts["materialized_piece_header_words"] += 4 * len(pieces)
    counts["released_linked_arena_words"] += 2 * (len(edges) + n)
    counts["released_traversal_and_remainder_words"] += 4 * n
    multiplicity = memberships(n, edges, pieces, counts)
    return pieces, multiplicity


def refine(n, edges, pieces, multiplicity, counts):
    local_index, used_edge = [-1] * n, [False] * len(edges)
    counts["refinement_global_scratch_words_allocated"] += n + len(edges)
    output = []
    for piece in pieces:
        vertices = piece.vertices
        boundary = [multiplicity[v] > 1 for v in vertices]
        counts["boundary_multiplicity_reads"] += len(vertices)
        if sum(boundary) <= 2:
            output.append(piece)
            counts["intact_piece_header_moves"] += 1
            continue
        size = len(vertices)
        for local, vertex in enumerate(vertices):
            local_index[vertex] = local
            counts["global_to_local_index_writes"] += 1
        adjacency = [[] for _ in vertices]
        for edge in piece.edges:
            u, v = (local_index[x] for x in edges[edge])
            adjacency[u].append((v, edge))
            adjacency[v].append((u, edge))
            counts["local_adjacency_words_and_copy_budget"] += 8
        degree = [len(row) for row in adjacency]
        active, peeled_parent, anchor = [True] * size, [-1] * size, list(range(size))
        queue = [v for v in range(size) if degree[v] <= 1 and not boundary[v]]
        order, head = [], 0
        counts["local_refinement_array_words_allocated"] += 10 * size
        while head < len(queue):
            vertex, head = queue[head], head + 1
            active[vertex] = False
            parent = -1
            for neighbor, _ in adjacency[vertex]:
                counts["peeling_incidence_reads"] += 1
                if active[neighbor]:
                    assert parent == -1
                    parent = neighbor
            assert parent != -1
            peeled_parent[vertex] = parent
            degree[parent] -= 1
            if degree[parent] == 1 and not boundary[parent]:
                queue.append(parent)
            order.append(vertex)
            counts["peeling_queue_and_array_operations"] += 8
        marked = [boundary[v] or (active[v] and degree[v] >= 3) for v in range(size)]
        assert sum(marked) <= 2 * sum(boundary) - 2
        for vertex in reversed(order):
            anchor[vertex] = anchor[peeled_parent[vertex]]
            counts["anchor_array_reads_and_writes"] += 3
        vertex_piece, hanging_piece = [-1] * size, [-1] * size
        first_new = len(output)
        for start in range(size):
            if not marked[start]:
                continue
            for next_vertex, first_edge in adjacency[start]:
                counts["corridor_start_incidence_reads"] += 1
                if not active[next_vertex] or used_edge[first_edge]:
                    continue
                index = len(output)
                output.append(Piece([], [], vertices[start]))
                previous, current, edge = start, next_vertex, first_edge
                if vertex_piece[start] == -1:
                    vertex_piece[start] = index
                while True:
                    assert not used_edge[edge]
                    used_edge[edge] = True
                    output[index].edges.append(edge)
                    counts["corridor_edge_records_and_copy_budget"] += 3
                    if marked[current]:
                        if vertex_piece[current] == -1:
                            vertex_piece[current] = index
                        break
                    vertex_piece[current] = index
                    candidates = []
                    for neighbor, candidate_edge in adjacency[current]:
                        counts["corridor_internal_incidence_reads"] += 1
                        if active[neighbor] and neighbor != previous:
                            candidates.append((neighbor, candidate_edge))
                            counts["corridor_candidate_words_and_copy_budget"] += 3
                    assert len(candidates) == 1
                    previous, current = current, candidates[0][0]
                    edge = candidates[0][1]
        for edge in piece.edges:
            counts["hanging_edge_classification_reads"] += 1
            if used_edge[edge]:
                continue
            u, v = (local_index[x] for x in edges[edge])
            attachment = anchor[u if not active[u] else v]
            assert active[attachment]
            if marked[attachment]:
                if hanging_piece[attachment] == -1:
                    hanging_piece[attachment] = len(output)
                    output.append(Piece([], [], vertices[attachment]))
                index = hanging_piece[attachment]
            else:
                index = vertex_piece[attachment]
            assert index >= first_new
            output[index].edges.append(edge)
            counts["hanging_edge_records_and_copy_budget"] += 3
        for vertex in piece.owners:
            local = local_index[vertex]
            if active[local]:
                index = vertex_piece[local]
            else:
                attachment = anchor[local]
                index = (
                    hanging_piece[attachment] if marked[attachment] else vertex_piece[attachment]
                )
            assert index >= first_new
            output[index].owners.append(vertex)
            counts["refined_owner_words_and_copy_budget"] += 3
        assert len(output) - first_new <= 4 * sum(boundary) - 5
        counts["refined_piece_header_words_allocated"] += 4 * (len(output) - first_new)
        counts["released_local_refinement_array_words"] += 10 * size
        counts["pieces_requiring_steiner_refinement"] += 1
    counts["released_refinement_global_scratch_words"] += n + len(edges)
    refined_multiplicity = memberships(n, edges, output, counts)
    return output, refined_multiplicity


def validate(n, edges, loads, theta, pieces, multiplicity, counts, refined):
    owners = [v for piece in pieces for v in piece.owners]
    allocated_edges = [edge for piece in pieces for edge in piece.edges]
    assert sorted(owners) == list(range(n))
    assert sorted(allocated_edges) == list(range(n - 1))
    actual = Counter(v for piece in pieces for v in piece.vertices)
    assert [actual[v] for v in range(n)] == multiplicity
    boundary_incidences = sum(value for value in multiplicity if value > 1)
    if len(pieces) > 1:
        assert boundary_incidences <= 2 * (len(pieces) - 1)
    else:
        assert boundary_incidences == 0
    for piece in pieces:
        graph = nx.Graph()
        graph.add_nodes_from(piece.vertices)
        graph.add_edges_from(edges[edge] for edge in piece.edges)
        assert nx.is_tree(graph)
        assert set(piece.owners) <= set(piece.vertices)
        mass = sum(loads[v] for v in piece.owners)
        if len(piece.vertices) > 1:
            assert mass < 2 * theta
        if refined:
            assert sum(multiplicity[v] > 1 for v in piece.vertices) <= 2
        counts["validated_piece_connectivity_and_loads"] += 1
    for left, right in itertools.combinations(pieces, 2):
        assert len(set(left.vertices) & set(right.vertices)) <= 1
        counts["validator_piece_intersection_checks"] += 1
    counts["validated_ownership_edge_partition_cases"] += 1


def audit_case(tree, loads, theta, root, counts, aggregate_work):
    n, edges, work = len(tree), list(tree.edges()), Counter()
    old, old_multiplicity = ownership(n, edges, loads, theta, root, work)
    validate(n, edges, loads, theta, old, old_multiplicity, counts, False)
    assert len(old) <= sum(loads) / theta + 1
    new, multiplicity = refine(n, edges, old, old_multiplicity, work)
    validate(n, edges, loads, theta, new, multiplicity, counts, True)
    if len(old) > 1:
        assert len(new) <= 8 * (len(old) - 1)
    else:
        assert len(new) == 1
    assert sum(work.values()) <= 2000 * (n + len(old) + len(new))
    aggregate_work.update(work)
    counts["supplied_tree_cases"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, rng, counts, work = time.monotonic(), random.Random(908031), Counter(), Counter()
    for n in range(1, 10 if args.full else 6):
        trees = [nx.empty_graph(1)] if n == 1 else nx.nonisomorphic_trees(n)
        for tree in trees:
            tree = nx.convert_node_labels_to_integers(tree)
            for root in tree:
                profiles = [[F(1)] * n, [F(0) if v % 2 else F(5) for v in tree]]
                if args.full:
                    profiles.append([F(2) ** ([-80, 80, 0, 1][v % 4]) for v in tree])
                for loads in profiles:
                    for theta in [F(1), F(2), F(3), max(F(1), sum(loads) / 5)]:
                        audit_case(tree, loads, theta, root, counts, work)
    for n in [32, 128, 512] if args.full else [16]:
        for shape in ("star", "path", "random"):
            if shape == "star":
                tree = nx.star_graph(n - 1)
            elif shape == "path":
                tree = nx.path_graph(n)
            else:
                tree = nx.from_prufer_sequence([rng.randrange(n) for _ in range(n - 2)])
            for root in [0, n // 2, n - 1]:
                loads = [F(rng.randrange(9)) for _ in tree]
                for theta in [F(7), F(64) * max(F(1), sum(loads)) / n]:
                    audit_case(tree, loads, theta, root, counts, work)
    assert work["pieces_requiring_steiner_refinement"] > 0
    result = {
        "audit": "incremental_active_set_sdd.weighted_tree_ownership",
        "scope": "Charged supplied-tree nonnegative-load ownership and refinement only; does not implement low-stretch tree selection, graph discovery or OP3",
        "arithmetic": "exact fractions",
        "audit_only": dict(counts),
        "charged_construction": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
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
