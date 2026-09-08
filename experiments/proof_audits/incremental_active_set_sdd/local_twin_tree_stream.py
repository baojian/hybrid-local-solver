"""Paid one-parent-heap discovery for a tree of original twin classes.

Stream owns only local graph discovery, heaps and sparse descriptor changes.
ReferenceReporter deliberately rebuilds a dense quotient and scans all heaps:
it is a separately counted numerical oracle, NOT the fast source hierarchy.
The full local work claim requires the proved weighted top-tree composition.
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
from batch_type_quotient import Trie, ordered
from frontier_exact import AVLMap, audit_map
from frontier_groups import DegreeHeap, Vertex
from frontier_neighborhood_types import PrivateDoubleStar, blow_up
from geometric_value_events import obstacle, solve
from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub
from twin_quotient_tree import QuotientLedger, canonical_types, check_prefix
import networkx as nx


class Bucket:
    def __init__(self, identity, node, work):
        self.identity, self.node, self.dirty_step = identity, node, -1
        self.heap = DegreeHeap(self, work)
        work["type_stream_bucket_header_words"] += 6


class Block:
    def __init__(self, vertex):
        self.leader, self.members = vertex, []


class TwinCell:
    def __init__(self):
        self.block = None


class Stream:
    """Local rows and heap state, with an explicit numeric-reporter interface."""

    def __init__(self, oracle, seed, alpha, lam, kappa, reporter, work):
        assert 0 < alpha <= 1 and lam > 0 and kappa >= 0
        self.oracle, self.seed, self.alpha, self.lam, self.kappa = oracle, seed, alpha, lam, kappa
        self.work, self.reporter = work, reporter
        self.gamma, self.bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        self.vertices = AVLMap(work)
        self.ledger = QuotientLedger(seed, alpha, lam, work)
        self.buckets, self.dirty, self.volume, self.step = [], [], 0, 0
        self.special = Bucket(-1, None, work)
        self.metrics = Counter()
        self.source = self.ensure(seed)
        work["type_stream_state_and_parameter_words"] += 40

    def ensure(self, label):
        def create():
            degree = self.oracle.degree(label)
            assert degree >= 1
            self.work["type_stream_original_vertex_degree_and_record"] += 22
            return Vertex(label, degree)

        return self.vertices.get_or_create(label, create)

    def touch(self, bucket):
        if bucket.dirty_step != self.step:
            bucket.dirty_step = self.step
            self.dirty.append(bucket)
            self.work["type_stream_distinct_changed_heap_records"] += 5
        self.work["type_stream_changed_heap_epoch_checks"] += 3

    def pop(self, bucket):
        vertex = bucket.heap.data[0]
        bucket.heap.remove(vertex)
        vertex.eliminated = True
        self.touch(bucket)
        self.work["type_stream_selected_original_member"] += 5
        return vertex

    def read_and_partition(self, batch):
        opened, closed, blocks = Trie(self.work), Trie(self.work), []
        for vertex in batch:
            row = [self.ensure(label) for label in self.oracle.row(vertex.label)]
            assert len(row) == vertex.degree
            vertex.row = ordered(row, lambda item: item.label, self.work)
            self.work["type_stream_paid_original_rows_and_buffers"] += 7 * vertex.degree + 5
        for vertex in batch:
            labels = [item.label for item in vertex.row]
            closure = ordered(labels + [vertex.label], lambda label: label, self.work)
            op = opened.insert([vertex.degree] + labels, TwinCell)
            cl = closed.insert([vertex.degree] + closure, TwinCell)
            assert op.block is None or cl.block is None or op.block is cl.block
            block = op.block if op.block is not None else cl.block
            if block is None:
                block = Block(vertex)
                blocks.append(block)
                self.work["type_stream_consumed_original_twin_block"] += 9
            op.block = cl.block = block
            block.members.append(vertex)
            self.work["type_stream_original_twin_keys_and_memberships"] += 5 * len(labels) + 14
        self.metrics["consumed_original_twin_blocks"] += len(blocks)
        return blocks

    def admit(self, batch, observe):
        addition = sum(vertex.degree for vertex in batch)
        self.work["type_stream_pre_row_volume_addition"] += 3 * len(batch) + 5
        assert batch and self.lam * (self.volume + addition) < 1
        self.volume += addition
        blocks = self.read_and_partition(batch)
        changed, enlarged = self.ledger.consume(blocks)
        new = []
        for node in changed:
            if node.identity == len(self.buckets):
                bucket = Bucket(node.identity, node, self.work)
                self.buckets.append(bucket)
                new.append(node)
                self.work["type_stream_new_quotient_bucket_locator"] += 6
            else:
                assert node is enlarged
            self.touch(self.buckets[node.identity])
        # Reinspect only newly paid row incidences, never all frontier records.
        for vertex in batch:
            for neighbor in vertex.row:
                self.work["type_stream_cached_incidence_heap_dispatch"] += 4
                if neighbor.eliminated:
                    continue
                record = self.ledger.record(neighbor)
                bucket = self.special if record.special else self.buckets[record.parent.identity]
                if neighbor.group is bucket:
                    continue
                if neighbor.group is not None:
                    old = neighbor.group
                    old.heap.remove(neighbor)
                    self.touch(old)
                    self.metrics["paid_second_parent_heap_moves"] += 1
                bucket.heap.insert(neighbor)
                self.touch(bucket)
                self.work["type_stream_first_or_exceptional_heap_assignment"] += 6
        self.reporter.sync(self, new, enlarged, self.dirty)
        self.metrics["completed_positive_batch_transactions"] += 1
        self.metrics["distinct_changed_heap_payloads"] += len(self.dirty)
        self.dirty = []
        if observe is not None:
            observe(self)

    def take(self):
        self.step += 1
        self.work["type_stream_checkpoint_and_special_gate_checks"] += 8
        if self.special.heap.size:
            root = self.ledger.seed_type
            assert root.size == 1
            first = self.special.heap.data[0]
            record = self.ledger.record(first)
            value = self.reporter.point(root.identity)
            self.metrics["special_source_gate_checks"] += 1
            if (
                root.degree + self.gamma * record.seed_adjacent
            ) * value > 1 + self.kappa * root.degree:
                out = []
                while self.special.heap.size:
                    out.append(self.pop(self.special))
                self.metrics["special_source_batch_admissions"] += 1
                return out
        identity = self.reporter.eligible(self)
        self.metrics["ordinary_global_reporter_queries"] += 1
        if identity is None:
            return []
        bucket = self.buckets[identity]
        point = self.reporter.point(identity)
        incoming = self.gamma * bucket.node.size * point
        self.work["type_stream_named_mean_and_batch_threshold"] += 8
        out = []
        while bucket.heap.size:
            vertex = bucket.heap.data[0]
            self.metrics["ordinary_heap_minimum_strict_checks"] += 1
            self.work["type_stream_ordinary_strict_degree_gate"] += 7
            if incoming <= (self.lam + self.kappa) * vertex.degree:
                break
            out.append(self.pop(bucket))
        assert out
        return out

    def run(self, observe=None):
        self.work["type_stream_initial_degree_only_gate"] += 5
        if 1 <= (self.lam + self.kappa) * self.source.degree:
            return []
        self.source.eliminated = True
        self.admit([self.source], observe)
        while True:
            batch = self.take()
            if not batch:
                break
            self.admit(batch, observe)
        means = self.reporter.materialize()
        output = []
        for node in self.ledger.nodes:
            mean = means[node.identity]
            for vertex in node.members:
                contrast = (
                    (F(vertex.label == self.seed) - F(1, node.size))
                    / (node.degree + self.gamma * node.clique)
                    if node.seed
                    else F(0)
                )
                value = mean + contrast
                assert value > 0
                output.append((vertex.label, value))
                self.work["type_stream_final_physical_contrast_and_output"] += 14
        return output


class ReferenceReporter:
    """Explicitly slow numerical oracle; receives no original graph object."""

    def __init__(self, counts, reverse=False):
        self.counts, self.reverse, self.means = counts, reverse, []

    def sync(self, stream, new, enlarged, changed):
        nodes, edges = stream.ledger.nodes, stream.ledger.edges
        n = len(nodes)
        matrix = [[F(0)] * n for _ in nodes]
        for node in nodes:
            matrix[node.identity][node.identity] = node.diagonal
        for edge in edges:
            i, j = edge.left.identity, edge.right.identity
            matrix[i][j] = matrix[j][i] = -edge.weight
        self.means = solve(matrix, [node.load for node in nodes])
        assert min(self.means) > 0
        self.counts["reference_dense_numeric_quotient_rebuilds"] += 1
        self.counts["reference_dense_matrix_words"] += n * n
        self.counts["interface_new_leaf_nodes"] += len(new)
        self.counts["interface_changed_heap_records"] += len(changed)
        if enlarged is not None:
            self.counts["interface_source_multiplicity_transactions"] += 1

    def point(self, identity):
        self.counts["reference_point_value_returns"] += 1
        return self.means[identity]

    def eligible(self, stream):
        sequence = reversed(stream.buckets) if self.reverse else stream.buckets
        for bucket in sequence:
            self.counts["reference_unpaid_global_heap_inspections"] += 1
            if bucket.heap.size:
                candidate = bucket.heap.data[0]
                incoming = stream.gamma * bucket.node.size * self.means[bucket.identity]
                if incoming > (stream.lam + stream.kappa) * candidate.degree:
                    return bucket.identity
        return None

    def materialize(self):
        self.counts["reference_final_mean_output_words"] += len(self.means)
        return self.means


def check_heaps(state, counts):
    memberships = set()
    original_records = dict(audit_map(state.ledger.physical))
    for bucket in state.buckets + [state.special]:
        heap = bucket.heap
        for i in range(heap.size):
            vertex = heap.data[i]
            assert vertex.position == i and vertex.group is bucket and not vertex.eliminated
            assert vertex.label not in memberships
            memberships.add(vertex.label)
            if i:
                parent = heap.data[(i - 1) // 2]
                assert (parent.degree, parent.label) <= (vertex.degree, vertex.label)
            record = original_records[vertex.label]
            assert (bucket is state.special) == record.special
            if not record.special:
                assert record.parent is bucket.node
            counts["independent_heap_membership_and_degree_order_checks"] += 1
    expected = {label for label, vertex in audit_map(state.vertices) if not vertex.eliminated}
    assert memberships == expected
    counts["independent_full_frontier_ownership_checks"] += 1


def check_case(graph, seed, alpha, lam, exact, reverse, counts, total_work, total_reference):
    work, reference = Counter(), Counter()
    state = Stream(
        LocalRows(graph, work),
        seed,
        alpha,
        lam,
        F(0) if exact else lam / 2,
        ReferenceReporter(reference, reverse),
        work,
    )
    partition, owner = canonical_types(graph)

    def observe(current):
        means, _, _ = check_prefix(graph, seed, current, current.ledger, partition, owner, counts)
        assert means == current.reporter.means
        check_heaps(current, counts)
        # A checkpoint must not split any nonseed type or the remaining source type.
        records = dict(audit_map(current.vertices))
        for members in partition:
            waiting = [records[i] for i in members if i in records and not records[i].eliminated]
            if waiting:
                assert len(waiting) == len(
                    [i for i in members if i not in records or not records[i].eliminated]
                )
                assert len({id(vertex.group) for vertex in waiting}) == 1
                counts["whole_original_type_discovery_and_heap_checks"] += 1

    output = dict(state.run(observe))
    for i in graph:
        residual = (
            F(i == seed)
            - graph.degree(i) * output.get(i, F(0))
            + state.gamma * sum(output.get(j, F(0)) for j in graph[i])
        )
        assert 0 <= residual <= (lam + state.kappa) * graph.degree(i)
        if i in output:
            assert residual == lam * graph.degree(i)
        counts["independent_original_final_residual_rows"] += 1
    if exact and len(graph) <= 9:
        ordered_vertices = list(graph)
        matrix = [
            [
                F(graph.degree(i)) if i == j else -state.gamma if graph.has_edge(i, j) else F(0)
                for j in ordered_vertices
            ]
            for i in ordered_vertices
        ]
        truth = obstacle(matrix, [F(i == seed) - lam * graph.degree(i) for i in ordered_vertices])
        assert [output.get(i, F(0)) for i in ordered_vertices] == truth
        counts["independent_enumerated_original_obstacles"] += 1
    assert len(state.oracle.row_log) == len(output)
    assert set(state.oracle.row_log) == set(output)
    assert len(set(state.oracle.degree_log)) == len(state.oracle.degree_log)
    total_work.update(work)
    total_reference.update(reference)
    counts["complete_exact_stream_outputs" if exact else "complete_ACL_stream_outputs"] += 1
    counts["completed_local_stream_batches"] += state.metrics[
        "completed_positive_batch_transactions"
    ]
    counts["special_source_batch_admissions"] += state.metrics["special_source_batch_admissions"]
    counts["paid_second_parent_heap_moves"] += state.metrics["paid_second_parent_heap_moves"]
    counts["source_type_enlargements"] += state.ledger.metrics["source_type_enlargements"]


def private_cases(counts, work, reference):
    profiles = []
    for exponent in [20, 80, 1024]:
        local, numeric = Counter(), Counter()
        oracle = MassiveHub(2**exponent, local)
        state = Stream(
            oracle, 0, F(1, 2**80), F(1, 16), F(1, 32), ReferenceReporter(numeric), local
        )
        out = dict(state.run())
        assert set(out) == {0} and oracle.rows == [0]
        assert 0 <= state.gamma * out[0] <= F(3, 32) * 2**exponent
        work.update(local)
        reference.update(numeric)
        counts["private_huge_hub_row_avoidance_certificates"] += 1
    for m in [4, 16, 64, 256]:
        local, numeric = Counter(), Counter()
        oracle = PrivateDoubleStar(m, 2**1024, local)
        state = Stream(
            oracle, 0, F(1, 2**80), F(1, 16 * m), F(1, 32 * m), ReferenceReporter(numeric), local
        )
        out = dict(state.run())
        assert set(out) == {0, *range(2, m + 2)}
        assert set(oracle.rows) == set(out) and 1 not in oracle.rows
        for label in out:
            neighbors = range(2, m + 2) if label == 0 else [0]
            degree = m + 1 if label == 0 else 1
            residual = (
                F(label == 0) - degree * out[label] + state.gamma * sum(out[j] for j in neighbors)
            )
            assert residual == state.lam * degree
        assert state.gamma * out[0] <= (state.lam + state.kappa) * (2**1024 + 1)
        assert (
            len(state.ledger.nodes) == 2
            and state.metrics["completed_positive_batch_transactions"] == 2
        )
        profiles.append(
            {
                "near_leaves": m,
                "volume": state.volume,
                "charged_stream_units": sum(local.values()),
                "reference_dense_numeric_matrix_words": numeric["reference_dense_matrix_words"],
                "local_row_count": len(oracle.rows),
            }
        )
        work.update(local)
        reference.update(numeric)
        counts["private_double_star_original_certificates"] += 1
    return profiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, work, reference = Counter(), Counter(), Counter()
    for k in range(2, 6 if args.full else 4):
        for tree in nx.nonisomorphic_trees(k):
            tree = nx.convert_node_labels_to_integers(tree, ordering="sorted")
            for mask in range(2**k) if args.full else [0, 2**k - 1]:
                graph, partition = blow_up(tree, [2 + i % 2 for i in range(k)], mask)
                for seed in [part[-1] for part in partition]:
                    for alpha in [F(1, 3), F(1, 64)]:
                        for lam in [F(1, 16), F(1, 96)]:
                            for exact in [False, True]:
                                check_case(
                                    graph,
                                    seed,
                                    alpha,
                                    lam,
                                    exact,
                                    (seed + mask) % 2 == 0,
                                    counts,
                                    work,
                                    reference,
                                )
    for alpha in [F(1), F(1, 2**80), F(1, 2**1024)]:
        graph, _ = blow_up(nx.path_graph(3), [2, 3, 2], 5)
        check_case(graph, 2, alpha, F(1, 96), True, True, counts, work, reference)
    graph, _ = blow_up(nx.path_graph(3), [2, 3, 2], 5)
    for offset in [0, 2**80, -(2**1024)]:
        mapping = {i: offset - 13 * i for i in graph}
        relabeled = nx.relabel_nodes(graph, mapping)
        check_case(relabeled, mapping[2], F(1, 64), F(1, 96), True, True, counts, work, reference)
        counts["arbitrary_signed_original_label_cases"] += 1
    for lam in [F(1, 2), F(1), F(3, 2)]:
        check_case(graph, 2, F(1, 64), lam, True, False, counts, work, reference)
        counts["high_penalty_degree_only_cases"] += 1
    profiles = private_cases(counts, work, reference)
    result = {
        "description": __doc__,
        "full": args.full,
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all nonisomorphic quotient trees through 5 vertices in full mode (3 otherwise), type sizes 2+i%2, all masks in full mode, every type last-member seed",
        "alpha_lazy": ["1/3", "1/64"],
        "lambda": ["1/16", "1/96"],
        "eps_appr_and_gates": "eps_appr=2*lambda; kappa=lambda/2 for ACL and 0 for exact obstacle",
        "stopping_rule": "initial degree-only quiet gate or both current ordinary reporter and special source gate quiet",
        "extra_cases": "path quotient [2,3,2], clique mask 5, seed 2, lambda 1/96 and alpha 1,2^-80,2^-1024; signed labels offset-13*i with offsets 0,2^80,-2^1024; high penalties 1/2,1,3/2; private huge hubs and four-type double stars with recorded profiles",
        "audit_only": dict(counts),
        "charged_local_stream_units": dict(work),
        "separately_counted_slow_numeric_reference": dict(reference),
        "private_profiles": profiles,
        "scope": "Heap discovery, original rows, twin maps and descriptors implemented. Dense numerical rebuilds and whole-heap numeric searches are explicit reference operations, not a fast source hierarchy.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "twin_quotient_tree.py",
                "batch_type_quotient.py",
                "frontier_groups.py",
                "frontier_exact.py",
                "frontier_neighborhood_types.py",
                "geometric_value_events.py",
                "small_alpha_floor.py",
                "supplied_envelope_work.py",
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
