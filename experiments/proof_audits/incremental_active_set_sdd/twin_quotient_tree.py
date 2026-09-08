"""Paid sparse original-twin descriptors on supplied legal positive batches.

This is a descriptor/gate reduction, not a fast local solver. BatchFrontier
and all dense graph/quotient solves in the driver are independent reference
work. The descriptor producer consumes only cached, already paid row data.
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
from batch_type_quotient import BatchFrontier, Trie, contains
from frontier_exact import AVLMap, audit_map
from frontier_neighborhood_types import blow_up
from geometric_value_events import solve
from small_alpha_floor import LocalRows
import networkx as nx


class KeyCell:
    def __init__(self):
        self.node = None


class PhysicalRecord:
    def __init__(self, vertex):
        self.vertex, self.active_type = vertex, None
        self.parent, self.special, self.seed_adjacent = None, False, False


class TypeNode:
    def __init__(self, identity, degree):
        self.identity, self.degree = identity, degree
        self.members, self.edges = [], []
        self.clique, self.seed = False, False
        self.diagonal, self.load = F(0), F(0)

    @property
    def size(self):
        return len(self.members)


class QuotientEdge:
    def __init__(self, left, right, gamma):
        self.left, self.right = left, right
        self.weight = gamma * left.size * right.size


class QuotientLedger:
    def __init__(self, seed, alpha, lam, work):
        self.seed, self.alpha, self.lam, self.work = seed, alpha, lam, work
        self.gamma, self.bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        self.opened, self.closed = Trie(work), Trie(work)
        self.physical, self.pairs = AVLMap(work), AVLMap(work)
        self.nodes, self.edges, self.seed_type = [], [], None
        self.volume, self.rounds, self.metrics = 0, 0, Counter()
        work["quotient_descriptor_headers_and_parameters"] += 35

    def record(self, vertex):
        def create():
            self.work["quotient_physical_record_words"] += 12
            return PhysicalRecord(vertex)

        return self.physical.get_or_create(vertex.label, create)

    def consume(self, blocks):
        batch, changed, enlarged = [], [], None
        for block in blocks:
            vertex = block.leader
            labels = [other.label for other in vertex.row]
            closure = []
            inserted = False
            for label in labels:
                if not inserted and vertex.label < label:
                    closure.append(vertex.label)
                    inserted = True
                closure.append(label)
                self.work["quotient_cached_closed_row_key_merge"] += 7
            if not inserted:
                closure.append(vertex.label)
            opened = self.opened.insert([vertex.degree] + labels, KeyCell)
            closed = self.closed.insert([vertex.degree] + closure, KeyCell)
            self.work["quotient_global_twin_key_arrays_and_cells"] += 5 * len(labels) + 14
            node = opened.node if opened.node is not None else closed.node
            assert opened.node is None or closed.node is None or opened.node is closed.node
            if node is None:
                node = TypeNode(len(self.nodes), vertex.degree)
                self.nodes.append(node)
                self.work["quotient_new_type_node_words"] += 20
                self.metrics["new_original_types"] += 1
            else:
                assert node.seed and node.size == 1 and enlarged is None
                node.clique = contains(node.members[0].row, vertex.label, self.work)
                enlarged = node
                self.metrics["source_type_enlargements"] += 1
            opened.node = closed.node = node
            if node.size == 0 and len(block.members) > 1:
                node.clique = contains(vertex.row, block.members[1].label, self.work)
            for member in block.members:
                record = self.record(member)
                assert record.active_type is None and member.degree == node.degree
                record.active_type = node
                node.members.append(member)
                batch.append(member)
                if member.label == self.seed:
                    node.seed, self.seed_type = True, node
                self.volume += member.degree
                self.work["quotient_original_member_and_source_records"] += 11
            node.diagonal = node.size * (node.degree - self.gamma * node.clique * (node.size - 1))
            node.load = F(node.seed) - self.lam * node.size * node.degree
            changed.append(node)
            self.work["quotient_diagonal_load_replacement"] += 15
        assert self.seed_type is not None and self.lam * self.volume < 1
        for vertex in batch:
            node = self.record(vertex).active_type
            for neighbor in vertex.row:
                record = self.record(neighbor)
                self.work["quotient_cached_original_incidence_dispatch"] += 6
                if vertex.label == self.seed:
                    record.seed_adjacent = True
                other = record.active_type
                if other is not None:
                    if other is node:
                        continue
                    key = (min(node.identity, other.identity), max(node.identity, other.identity))
                    self.work["quotient_edge_pair_key_operations"] += 7

                    def create(node=node, other=other):
                        edge = QuotientEdge(node, other, self.gamma)
                        self.edges.append(edge)
                        node.edges.append(edge)
                        other.edges.append(edge)
                        self.work["quotient_sparse_edge_and_incidence_words"] += 18
                        self.metrics["new_sparse_quotient_edges"] += 1
                        return edge

                    self.pairs.get_or_create(key, create)
                elif record.parent is None:
                    record.parent = node
                    self.work["quotient_first_parent_candidate_assignment"] += 3
                elif not record.special and record.parent is not node:
                    record.special = True
                    assert self.seed_type.size == 1 and neighbor.degree == self.seed_type.degree
                    self.metrics["second_parent_source_candidate_classifications"] += 1
                    self.work["quotient_second_parent_source_candidate_assignment"] += 6
        if enlarged is not None:
            assert len(enlarged.edges) <= enlarged.degree
            for edge in enlarged.edges:
                edge.weight = self.gamma * edge.left.size * edge.right.size
                self.work["quotient_source_incident_weight_refresh"] += 8
                self.metrics["source_incident_weights_refreshed"] += 1
        self.rounds += 1
        self.work["quotient_transaction_return_operations"] += 5
        return changed, enlarged


def canonical_types(graph):
    """Global graph inspection is validator-only."""
    groups = nx.utils.UnionFind(graph)
    opened, closed = {}, {}
    for i in graph:
        for key, table in [(frozenset(graph[i]), opened), (frozenset(graph[i]) | {i}, closed)]:
            if key in table:
                groups.union(i, table[key])
            else:
                table[key] = i
    partition = sorted([sorted(group) for group in groups.to_sets()])
    owner = {label: index for index, group in enumerate(partition) for label in group}
    quotient = nx.Graph()
    quotient.add_nodes_from(range(len(partition)))
    quotient.add_edges_from((owner[i], owner[j]) for i, j in graph.edges if owner[i] != owner[j])
    assert len(quotient) == 1 or nx.is_tree(quotient)
    return partition, owner


def check_prefix(graph, seed, state, ledger, partition, owner, counts):
    nodes = ledger.nodes
    size = len(nodes)
    original = [vertex for node in nodes for vertex in node.members]
    labels = [vertex.label for vertex in original]
    matrix = [
        [
            F(graph.degree(i)) if i == j else -ledger.gamma if graph.has_edge(i, j) else F(0)
            for j in labels
        ]
        for i in labels
    ]
    physical = solve(matrix, [F(int(i == seed)) - ledger.lam * graph.degree(i) for i in labels])
    exact = dict(zip(labels, physical))
    assert min(physical) > 0
    quotient = [[F(0)] * size for _ in nodes]
    represented = nx.Graph()
    represented.add_nodes_from(range(size))
    for node in nodes:
        quotient[node.identity][node.identity] = node.diagonal
        known = {owner[vertex.label] for vertex in node.members}
        assert len(known) == 1
        full = set(partition[next(iter(known))])
        assert node.size == len(full) or node.seed and node.size == 1
        assert node.seed == (seed in {vertex.label for vertex in node.members})
    for edge in ledger.edges:
        a, b = edge.left.identity, edge.right.identity
        assert edge.weight == ledger.gamma * edge.left.size * edge.right.size
        quotient[a][b] = quotient[b][a] = -edge.weight
        represented.add_edge(a, b)
    assert size == 1 or nx.is_tree(represented)
    assert len(ledger.edges) == max(0, size - 1)
    means = solve(quotient, [node.load for node in nodes])
    for node in nodes:
        i = node.identity
        assert sum(quotient[i]) >= ledger.bar * node.size * node.degree > 0
        actual_mean = sum(exact[vertex.label] for vertex in node.members) / node.size
        assert means[i] == actual_mean
        for vertex in node.members:
            contrast = (
                (F(int(vertex.label == seed)) - F(1, node.size))
                / (node.degree + ledger.gamma * node.clique)
                if node.seed
                else F(0)
            )
            assert means[i] + contrast == exact[vertex.label]
            counts["independent_original_mean_and_source_contrast_coordinates"] += 1
        counts["original_degree_weighted_SDD_rows"] += 1
    record_map = dict(audit_map(ledger.physical))
    parent_histogram = Counter()
    for label, record in record_map.items():
        if record.active_type is not None:
            continue
        parent_ids = {record_map[j].active_type.identity for j in graph[label] if j in exact}
        assert parent_ids
        residual = ledger.gamma * sum(exact.get(j, F(0)) for j in graph[label])
        degree = graph.degree(label)
        if record.special:
            root = ledger.seed_type
            assert owner[label] == owner[seed] and len(parent_ids) >= 2 and root.size == 1
            c = int(graph.has_edge(label, seed))
            assert c == record.seed_adjacent
            calculated = (
                (root.degree + ledger.gamma * c) * exact[seed] - 1 + ledger.lam * root.degree
            )
            assert residual == calculated
            threshold = (1 + state.kappa * root.degree) / (root.degree + ledger.gamma * c)
            assert (residual > (ledger.lam + state.kappa) * degree) == (exact[seed] > threshold)
            counts["special_seed_type_original_gate_identities"] += 1
            counts[
                "special_clique_seed_type_gates" if c else "special_independent_seed_type_gates"
            ] += 1
        else:
            parent = record.parent
            assert parent_ids == {parent.identity}
            assert residual == ledger.gamma * parent.size * means[parent.identity]
            if ledger.gamma:
                threshold = (ledger.lam + state.kappa) * degree / (ledger.gamma * parent.size)
                assert (residual > (ledger.lam + state.kappa) * degree) == (
                    means[parent.identity] > threshold
                )
            counts["one_parent_original_frontier_gate_identities"] += 1
        parent_histogram[len(parent_ids)] += 1
    assert set(record_map) == set(labels) | {j for i in labels for j in graph[i]}
    assert ledger.volume == state.volume < 1 / ledger.lam
    counts["independent_weighted_tree_quotient_prefixes"] += 1
    counts["validator_original_and_quotient_dense_solves"] += 2
    return means, quotient, parent_histogram


def check_case(graph, seed, alpha, lam, exact, counts, aggregate):
    partition, owner = canonical_types(graph)
    reference_work, descriptor_work = Counter(), Counter()
    state = BatchFrontier(
        LocalRows(graph, reference_work),
        seed,
        alpha,
        lam,
        F(0) if exact else lam / 2,
        reference_work,
    )
    ledger = QuotientLedger(seed, alpha, lam, descriptor_work)
    maximum_parents = 0

    def observe(current):
        nonlocal maximum_parents
        if current.history:
            assert len(current.history) == ledger.rounds + 1
            ledger.consume(current.history[-1].blocks)
            _, _, parents = check_prefix(graph, seed, current, ledger, partition, owner, counts)
            maximum_parents = max(maximum_parents, max(parents, default=0))

    result = state.run(observe)
    values = dict(result["records"])
    for i in graph:
        residual = (
            F(int(i == seed))
            - graph.degree(i) * values.get(i, F(0))
            + state.gamma * sum(values.get(j, F(0)) for j in graph[i])
        )
        assert 0 <= residual <= (state.lam + state.kappa) * graph.degree(i)
    assert ledger.metrics["source_type_enlargements"] <= 1
    assert ledger.metrics["source_incident_weights_refreshed"] <= graph.degree(seed)
    aggregate.update(descriptor_work)
    counts["completed_reference_local_outputs"] += 1
    counts[
        "completed_exact_obstacle_reference_outputs" if exact else "completed_ACL_reference_outputs"
    ] += 1
    counts["reference_original_residual_rows"] += len(graph)
    counts["observed_source_type_enlargements"] += ledger.metrics["source_type_enlargements"]
    return {
        "vertices": len(graph),
        "seed": seed,
        "alpha": str(alpha),
        "lambda": str(lam),
        "exact_gate": exact,
        "volume": ledger.volume,
        "active_original_types": len(ledger.nodes),
        "maximum_frontier_active_parents": maximum_parents,
        "descriptor_metrics": dict(ledger.metrics),
        "charged_descriptor_units": sum(descriptor_work.values()),
        "reference_dense_batch_work_excluded": sum(reference_work.values()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    counts, work, profiles = Counter(), Counter(), []
    for k in range(2, 6 if args.full else 4):
        for tree in nx.nonisomorphic_trees(k):
            tree = nx.convert_node_labels_to_integers(tree, ordering="sorted")
            for mask in range(2**k) if args.full else [0, 2**k - 1]:
                graph, partition = blow_up(tree, [2 + i % 2 for i in range(k)], mask)
                for seed in [members[-1] for members in partition]:
                    for alpha in [F(1, 3), F(1, 64)]:
                        for lam in [F(1, 16), F(1, 96), F(1, 16 * graph.number_of_edges())]:
                            for exact in [False, True]:
                                profile = check_case(graph, seed, alpha, lam, exact, counts, work)
                                if profile["maximum_frontier_active_parents"] >= 2:
                                    profiles.append(profile)
    for alpha in [F(1), F(1, 2**80), F(1, 2**1024)]:
        graph, _ = blow_up(nx.path_graph(3), [2, 3, 2], 5)
        profiles.append(check_case(graph, 2, alpha, F(1, 96), True, counts, work))
    result = {
        "description": __doc__,
        "full": args.full,
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all nonisomorphic tree blow-ups through 5 quotient vertices in full mode (3 otherwise), sizes 2+i%2, all clique masks in full mode and every type's last physical seed",
        "alpha_lazy": ["1/3", "1/64"],
        "lambda_values": ["1/16", "1/96", "1/(16*original_edges)"],
        "eps_appr_and_gates": "eps_appr=2*lambda; kappa=lambda/2 for ACL and kappa=0 for the separate exact obstacle run",
        "extra_cases": "path quotient sizes [2,3,2], clique mask 5, physical seed 2, lambda 1/96, exact gates, alpha 1, 2^-80, 2^-1024",
        "stopping_rule": "the complete eligible-batch reference reaches a quiet original frontier; the descriptor performs no numeric gate searches",
        "audit_only": dict(counts),
        "charged_descriptor_units": dict(work),
        "profiles": profiles,
        "scope": "Paid descriptors consume supplied legal cached-row batches; all dense local discovery, original/quotient solves and global type partitions are reference work. No fast local tree-quotient solver is claimed.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "batch_type_quotient.py",
                "frontier_exact.py",
                "frontier_neighborhood_types.py",
                "geometric_value_events.py",
                "small_alpha_floor.py",
            ]
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
