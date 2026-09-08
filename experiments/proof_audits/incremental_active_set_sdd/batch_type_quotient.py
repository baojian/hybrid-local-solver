"""Paid eligible batches and full-original-row twin quotients.

All exact dense reference inverses, graph partitions and historical member
snapshots below are validators. The producer factors only its paid quotient.
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
from frontier_exact import AVLMap, audit_map
from frontier_group_branching import PrivateBinaryTree, parameters, radial_face
from frontier_groups import DegreeHeap
from frontier_neighborhood_types import PrivateDoubleStar, blow_up
from geometric_value_events import obstacle, solve
from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub
import networkx as nx


def ordered(values, key, work):
    """Charged stable merge sort, including every temporary buffer."""
    data = list(values)
    work["batch_sort_initial_copy"] += 3 * len(data) + 5
    width = 1
    while width < len(data):
        target = [None] * len(data)
        work["batch_sort_full_buffer_allocation"] += 2 * len(data) + 3
        for start in range(0, len(data), 2 * width):
            middle, end = min(start + width, len(data)), min(start + 2 * width, len(data))
            left, right = start, middle
            for out in range(start, end):
                if right == end or (left < middle and key(data[left]) <= key(data[right])):
                    target[out] = data[left]
                    left += 1
                else:
                    target[out] = data[right]
                    right += 1
                work["batch_sort_comparisons_keys_indices_and_writes"] += 16
        data = target
        width *= 2
    return data


class Trie:
    def __init__(self, work):
        self.children, self.terminal, self.work = AVLMap(work), None, work
        work["batch_trie_header_words"] += 5

    def insert(self, symbols, create):
        node = self
        for symbol in symbols:
            node = node.children.get_or_create(symbol, lambda: Trie(self.work))
            self.work["batch_trie_symbol_steps"] += 4
        if node.terminal is None:
            node.terminal = create()
        self.work["batch_trie_terminal_operations"] += 4
        return node.terminal


class Vertex:
    def __init__(self, label, degree):
        self.label, self.degree = label, degree
        self.group, self.position, self.eliminated = None, -1, False
        self.row, self.value, self.block = None, F(0), -1
        self.touched_step, self.neighbors = -1, []


class Group:
    def __init__(self, identity, q, work):
        self.identity, self.index, self.base, self.q = identity, -1, None, q
        self.heap, self.mask, self.value_sum = DegreeHeap(self, work), [], F(0)
        work["batch_response_group_header_words"] += 14


class Block:
    def __init__(self, members, work):
        self.members, self.leader, self.size = members, members[0], len(members)
        self.parent, self.z, self.coefficients = self.leader.group, F(0), []
        work["batch_twin_block_header_words"] += 12


class Transaction:
    def __init__(self, blocks, future, splits, fresh, work):
        self.blocks, self.future, self.splits, self.fresh = blocks, future, splits, fresh
        work["batch_transaction_header_words"] += 8


def contains(row, label, work):
    left, right = 0, len(row)
    while left < right:
        middle = (left + right) // 2
        other = row[middle].label
        work["batch_paid_original_row_binary_search"] += 8
        if other < label:
            left = middle + 1
        else:
            right = middle
    work["batch_paid_original_row_search_result"] += 5
    return left < len(row) and row[left].label == label


def factor(matrix, work):
    size = len(matrix)
    lower = [[F(int(i == j)) for j in range(size)] for i in range(size)]
    diagonal = [F(0)] * size
    work["batch_quotient_factor_arrays"] += 5 * size * size + 3 * size + 5
    for i in range(size):
        for j in range(i):
            value = matrix[i][j]
            for k in range(j):
                value -= lower[i][k] * diagonal[k] * lower[j][k]
                work["batch_quotient_factor_off_diagonal_products"] += 11
            lower[i][j] = value / diagonal[j]
            work["batch_quotient_factor_divisions_and_writes"] += 6
        value = matrix[i][i]
        for k in range(i):
            value -= lower[i][k] * lower[i][k] * diagonal[k]
            work["batch_quotient_factor_diagonal_products"] += 10
        assert value > 0
        diagonal[i] = value
        work["batch_quotient_positive_pivot_operations"] += 5
    return lower, diagonal


def factored_solve(decomposition, rhs, work):
    lower, diagonal = decomposition
    size = len(rhs)
    answer = list(rhs)
    work["batch_quotient_rhs_and_solution_arrays"] += 3 * size + 4
    for i in range(size):
        for j in range(i):
            answer[i] -= lower[i][j] * answer[j]
            work["batch_quotient_forward_substitution"] += 9
    for i in range(size):
        answer[i] /= diagonal[i]
        work["batch_quotient_diagonal_substitution"] += 4
    for i in reversed(range(size)):
        for j in range(i + 1, size):
            answer[i] -= lower[j][i] * answer[j]
            work["batch_quotient_reverse_substitution"] += 9
    return answer


class BatchFrontier:
    def __init__(self, oracle, seed, alpha, lam, kappa, work):
        assert 0 < alpha <= 1 and lam > 0 and kappa >= 0
        self.oracle, self.seed, self.alpha, self.lam, self.kappa, self.work = (
            oracle,
            seed,
            alpha,
            lam,
            kappa,
            work,
        )
        self.gamma = (1 - alpha) / (1 + alpha)
        self.bar = 1 - self.gamma
        self.vertices = AVLMap(work)
        self.groups, self.history, self.matrix = [], [], [[F(0)]]
        self.next_group, self.step, self.volume = 0, 0, 0
        self.metrics = Counter()
        group = self.new_group(F(1))
        group.index = 0
        group.heap.insert(self.ensure(seed))
        self.groups = [group]
        work["batch_state_headers_and_parameters"] += 42

    def ensure(self, label):
        def create():
            degree = self.oracle.degree(label)
            assert degree >= 1
            self.work["batch_vertex_record_degree_reply_and_initialization"] += 24
            return Vertex(label, degree)

        return self.vertices.get_or_create(label, create)

    def new_group(self, q):
        group = Group(self.next_group, q, self.work)
        self.next_group += 1
        self.work["batch_group_identity_assignment"] += 4
        return group

    def take_batch(self):
        batch, volume = [], 0
        for group in self.groups:
            group.base, group.mask = group.index, []
            self.work["batch_old_group_metadata_reset"] += 5
            while group.heap.size:
                vertex = group.heap.data[0]
                self.work["batch_minimum_degree_strict_gate"] += 9
                self.metrics["strict_degree_gate_checks"] += 1
                if group.q <= (self.lam + self.kappa) * vertex.degree:
                    break
                group.heap.remove(vertex)
                vertex.eliminated = True
                batch.append(vertex)
                volume += vertex.degree
                self.work["batch_selected_vertex_and_volume_operations"] += 8
        if batch:
            assert self.lam * (self.volume + volume) < 1
            self.volume += volume
            self.step += 1
            self.metrics["complete_eligible_batches"] += 1
        self.work["batch_pre_row_volume_guard"] += 8
        return batch

    def read_rows_and_partition(self, batch):
        work = self.work
        for vertex in batch:
            row = [self.ensure(label) for label in self.oracle.row(vertex.label)]
            assert len(row) == vertex.degree
            vertex.row = ordered(row, lambda x: x.label, work)
            work["batch_original_row_entry_checks_and_buffers"] += 6 * vertex.degree + 5
        roots, sizes = list(range(len(batch))), [1] * len(batch)
        work["batch_disjoint_set_arrays"] += 5 * len(batch) + 5

        def root(i):
            while roots[i] != i:
                i = roots[i]
                work["batch_union_find_parent_steps"] += 4
            work["batch_union_find_root_result"] += 3
            return i

        def unite(i, j):
            a, b = root(i), root(j)
            if a != b:
                if sizes[a] < sizes[b]:
                    a, b = b, a
                roots[b] = a
                sizes[a] += sizes[b]
            work["batch_union_by_size_operations"] += 12

        opened, closed = Trie(work), Trie(work)
        for i, vertex in enumerate(batch):
            prefix = [vertex.group.identity, vertex.degree]
            labels = [neighbor.label for neighbor in vertex.row]
            closure = ordered(labels + [vertex.label], lambda x: x, work)
            work["batch_full_row_twin_key_words"] += 6 + 3 * len(labels)
            unite(i, opened.insert(prefix + labels, lambda i=i: i))
            unite(i, closed.insert(prefix + closure, lambda i=i: i))
        buckets = [None] * len(batch)
        members = []
        for i, vertex in enumerate(batch):
            leader = root(i)
            if buckets[leader] is None:
                buckets[leader] = []
                members.append(buckets[leader])
            buckets[leader].append(vertex)
            work["batch_twin_partition_bucket_operations"] += 10
        blocks = [Block(group, work) for group in members]
        for i, block in enumerate(blocks):
            for vertex in block.members:
                vertex.block = i
                work["batch_twin_class_vertex_assignment"] += 3
        self.metrics["consumed_exact_original_twin_classes"] += len(blocks)
        self.metrics["maximum_batch_vertices"] = max(
            self.metrics["maximum_batch_vertices"], len(batch)
        )
        self.metrics["maximum_batch_quotient_order"] = max(
            self.metrics["maximum_batch_quotient_order"], len(blocks)
        )
        return blocks

    def refine_future(self, batch):
        touched, children, splits, fresh = [], [], [], []
        for vertex in batch:
            for neighbor in vertex.row:
                self.work["batch_cached_incidence_partition_inspection"] += 5
                if neighbor.eliminated:
                    continue
                if neighbor.touched_step != self.step:
                    neighbor.touched_step, neighbor.neighbors = self.step, []
                    touched.append(neighbor)
                    self.work["batch_touched_candidate_headers"] += 7
                neighbor.neighbors.append(vertex.block)
                self.work["batch_candidate_class_incidence_word"] += 3
        trie = Trie(self.work)
        for vertex in touched:
            sequence = ordered(vertex.neighbors, lambda x: x, self.work)
            mask = []
            for index in sequence:
                if not mask or mask[-1] != index:
                    mask.append(index)
                self.work["batch_neighbor_signature_deduplication"] += 5
            parent = vertex.group
            key = [-1 if parent is None else parent.identity] + mask
            self.work["batch_refinement_key_buffer_words"] += 2 * len(key) + 5

            def create(parent=parent, mask=mask):
                child = self.new_group(F(0) if parent is None else parent.q)
                child.base = None if parent is None else parent.index
                child.mask = mask
                children.append(child)
                if parent is None:
                    fresh.append(child)
                else:
                    splits.append((parent, child))
                self.work["batch_split_and_fresh_history_words"] += 12
                return child

            child = trie.insert(key, create)
            if parent is not None:
                parent.heap.remove(vertex)
                self.metrics["old_candidate_heap_moves"] += 1
            child.heap.insert(vertex)
        future = [group for group in self.groups + children if group.heap.size]
        self.work["batch_future_group_filter_and_buffers"] += (
            5 * (len(self.groups) + len(children)) + 5
        )
        self.metrics["maximum_completed_frontier_groups"] = max(
            self.metrics["maximum_completed_frontier_groups"], len(future)
        )
        self.metrics["original_incidence_group_splits"] += len(splits)
        return future, splits, fresh

    def advance(self, batch):
        blocks = self.read_rows_and_partition(batch)
        future, splits, fresh = self.refine_future(batch)
        size, width = len(blocks), len(future)
        matrix = [[F(0)] * size for _ in blocks]
        rhs = [F(0)] * size
        self.work["batch_symmetric_quotient_arrays"] += 2 * size * size + 2 * size + 5
        for a, block in enumerate(blocks):
            leader = block.leader
            rhs[a] = block.size * (block.parent.q - self.lam * leader.degree)
            for b, other in enumerate(blocks):
                if a == b:
                    adjacent = len(block.members) > 1 and contains(
                        leader.row, block.members[1].label, self.work
                    )
                    raw = leader.degree - self.gamma * adjacent * (block.size - 1)
                else:
                    adjacent = contains(leader.row, other.leader.label, self.work)
                    raw = -self.gamma * adjacent * other.size
                raw -= self.matrix[block.parent.index][other.parent.index] * other.size
                matrix[a][b] = block.size * raw
                self.work["batch_symmetric_quotient_coefficient_operations"] += 17
        decomposition = factor(matrix, self.work)
        values = factored_solve(decomposition, rhs, self.work)
        assert all(value > 0 for value in values)
        weights = [[F(0)] * width for _ in blocks]
        self.work["batch_quotient_frontier_coupling_array"] += 2 * size * width + 4
        for t, group in enumerate(future):
            marker = [False] * size
            for index in group.mask:
                marker[index] = True
            self.work["batch_frontier_mask_marker_array_and_writes"] += (
                3 * size + 3 * len(group.mask) + 5
            )
            for a, block in enumerate(blocks):
                base = F(0) if group.base is None else self.matrix[block.parent.index][group.base]
                weights[a][t] = base + self.gamma * marker[a]
                self.work["batch_quotient_frontier_coupling_operations"] += 8
            column = factored_solve(
                decomposition,
                [block.size * weights[a][t] for a, block in enumerate(blocks)],
                self.work,
            )
            self.work["batch_weighted_quotient_rhs_words"] += 4 * size + 3
            for a, block in enumerate(blocks):
                block.coefficients.append(column[a])
                self.work["batch_lift_coefficient_history_words"] += 3
        new_matrix = [[F(0)] * width for _ in future]
        self.work["batch_shared_matrix_allocation"] += 2 * width * width + 4
        for t, group in enumerate(future):
            for a, block in enumerate(blocks):
                group.q += block.size * weights[a][t] * values[a]
                self.work["batch_shared_load_quotient_products"] += 9
            for u, other in enumerate(future):
                value = (
                    F(0)
                    if group.base is None or other.base is None
                    else self.matrix[group.base][other.base]
                )
                for a, block in enumerate(blocks):
                    value += block.size * weights[a][t] * block.coefficients[u]
                    self.work["batch_shared_fill_quotient_products"] += 10
                    self.metrics["shared_fill_quotient_products"] += 1
                new_matrix[t][u] = value
                self.work["batch_shared_fill_base_and_result_operations"] += 6
        for a, block in enumerate(blocks):
            block.z = values[a]
        for index, group in enumerate(future):
            group.index = index
            self.work["batch_new_dense_matrix_indices"] += 3
        self.matrix, self.groups = new_matrix, future
        self.history.append(Transaction(blocks, future, splits, fresh, self.work))
        self.metrics["sum_quotient_cubic_ledger"] += (
            size**3 + size**2 * width + size * width**2 + width**2 + width + 1
        )
        self.work["batch_transaction_commit_operations"] += 10 + size

    def lift(self, validator=None):
        records, probabilities = [], []
        for transaction in reversed(self.history):
            for block in transaction.blocks:
                value = block.z
                for coefficient, group in zip(block.coefficients, transaction.future):
                    value += coefficient * group.value_sum
                    self.work["batch_reverse_quotient_aggregate_products"] += 8
                for vertex in block.members:
                    vertex.value = value
                    records.append((vertex.label, value))
                    probabilities.append((vertex.label, self.bar * vertex.degree * value))
                    self.work["batch_reverse_original_coordinate_output_words"] += 12
                    self.metrics["reverse_original_coordinate_writes"] += 1
            for parent, child in reversed(transaction.splits):
                parent.value_sum += child.value_sum
                child.value_sum = F(0)
                self.work["batch_reverse_split_merge_and_clear"] += 6
            for group in transaction.fresh:
                group.value_sum = F(0)
                self.work["batch_reverse_fresh_clear"] += 3
            for block in transaction.blocks:
                block.parent.value_sum += block.size * block.leader.value
                self.work["batch_reverse_consumed_class_parent_sum"] += 5
            if validator is not None:
                validator(self, transaction)
        return {"records": records, "probabilities": probabilities, "volume": self.volume}

    def run(self, validator=None, lift_validator=None):
        if validator is not None:
            validator(self)
        while batch := self.take_batch():
            self.advance(batch)
            if validator is not None:
                validator(self)
        return self.lift(lift_validator)


def validators(graph, seed, alpha, lam, counts, partition=None):
    labels = sorted(graph)
    index = {label: i for i, label in enumerate(labels)}
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in labels]
        for i in labels
    ]
    load = [F(int(i == seed)) - lam * graph.degree(i) for i in labels]
    optimum = obstacle(matrix, load)
    snapshots = []
    counts["validator_original_obstacle_solves"] += 1

    def forward(state):
        vertices = [vertex for _, vertex in audit_map(state.vertices)]
        face = [
            vertex
            for transaction in state.history
            for block in transaction.blocks
            for vertex in block.members
        ]
        indices = [index[vertex.label] for vertex in face]
        local = [[matrix[i][j] for j in indices] for i in indices]
        values = solve(local, [load[i] for i in indices])
        assert all(0 < value <= optimum[i] for value, i in zip(values, indices))
        columns = [
            solve(local, [F(int(i == j)) for i in range(len(indices))]) for j in range(len(indices))
        ]
        inverse = [[columns[j][i] for j in range(len(indices))] for i in range(len(indices))]
        remaining = [vertex for vertex in vertices if not vertex.eliminated]
        covered, distinct_columns = set(), set()
        for k, group in enumerate(state.groups):
            assert group.index == k and group.heap.size > 0
            signatures = set()
            for j, vertex in enumerate(group.heap.data[: group.heap.size]):
                assert vertex.position == j and vertex.group is group and not vertex.eliminated
                assert vertex not in covered
                covered.add(vertex)
                signatures.add(tuple(graph.has_edge(vertex.label, old.label) for old in face))
                if j:
                    parent = group.heap.data[(j - 1) // 2]
                    assert (parent.degree, parent.label) <= (vertex.degree, vertex.label)
            assert len(signatures) == 1
            signature = next(iter(signatures))
            assert signature not in distinct_columns
            distinct_columns.add(signature)
            assert not state.history or any(signature)
            assert all(vertex is None for vertex in group.heap.data[group.heap.size :])
        assert covered == set(remaining)
        if state.history:
            assert (
                len(state.groups) <= 2 ** state.metrics["consumed_exact_original_twin_classes"] - 1
            )
            counts["distinct_nonzero_frontier_columns_and_local_type_bounds"] += 1
        for left in remaining:
            i = index[left.label]
            h = load[i] - sum(matrix[i][j] * value for j, value in zip(indices, values))
            assert left.group.q - lam * left.degree == h
            for right in remaining:
                j = index[right.label]
                fill = sum(
                    matrix[i][indices[a]] * inverse[a][b] * matrix[indices[b]][j]
                    for a in range(len(indices))
                    for b in range(len(indices))
                )
                assert state.matrix[left.group.index][right.group.index] == fill
        if state.history:
            for block in state.history[-1].blocks:
                for u in block.members:
                    for v in block.members:
                        assert u.degree == v.degree
                        assert set(graph[u.label]) - {v.label} == set(graph[v.label]) - {u.label}
        assert state.volume == sum(vertex.degree for vertex in face) < 1 / lam
        assert state.vertices.size <= 1 + state.volume
        if partition is not None:
            k = len(partition)
            assert len(state.history) <= k + 1
            assert state.metrics["consumed_exact_original_twin_classes"] <= k + 1
            assert len(state.groups) <= k if state.history else len(state.groups) == 1
            present = {vertex.label: vertex for vertex in vertices}
            admitted = {vertex.label for vertex in face}
            for group in partition:
                members = set(group) - {seed}
                live = members - admitted
                known = [present[label] for label in live if label in present]
                assert not known or len(known) == len(live)
                assert len({vertex.group for vertex in known}) <= 1
            counts["unsupplied_global_type_batch_and_frontier_invariants"] += 1
        snapshots.append(
            {
                group: [vertex.label for vertex in group.heap.data[: group.heap.size]]
                for group in state.groups
            }
        )
        counts["independent_batch_prefix_Schur_heap_and_true_twin_checks"] += 1
        counts["validator_dense_face_inverse_column_solves"] += 1 + len(face)

    def backward(state, transaction):
        slot = next(i for i, other in enumerate(state.history) if other is transaction)
        face = [
            vertex for entry in state.history for block in entry.blocks for vertex in block.members
        ]
        positions = [index[vertex.label] for vertex in face]
        local = [[matrix[i][j] for j in positions] for i in positions]
        values = solve(local, [load[i] for i in positions])
        exact = dict(zip((vertex.label for vertex in face), values))
        for block in transaction.blocks:
            for vertex in block.members:
                assert vertex.value == exact[vertex.label]
                counts["independent_reverse_original_coordinate_checks"] += 1
        for group, members in snapshots[slot].items():
            assert group.value_sum == sum(exact.get(label, F(0)) for label in members)
            counts["independent_historical_group_sum_checks"] += 1

    return forward, backward


def check_case(graph, seed, alpha, epsilon, counts, work, exact=False, partition=None, dense=True):
    ledger = Counter()
    oracle = LocalRows(graph, ledger)
    lam = epsilon / 2
    state = BatchFrontier(oracle, seed, alpha, lam, F(0) if exact else epsilon / 4, ledger)
    callbacks = validators(graph, seed, alpha, lam, counts, partition) if dense else (None, None)
    result = state.run(*callbacks)
    values = dict(result["records"])
    for i in graph:
        residual = (
            F(int(i == seed))
            - graph.degree(i) * values.get(i, F(0))
            + state.gamma * sum(values.get(j, F(0)) for j in graph[i])
        )
        assert 0 <= residual <= (lam + state.kappa) * graph.degree(i)
        assert i not in values or residual == lam * graph.degree(i)
    if exact:
        labels = sorted(graph)
        matrix = [
            [
                F(graph.degree(i)) if i == j else -state.gamma if graph.has_edge(i, j) else F(0)
                for j in labels
            ]
            for i in labels
        ]
        reference = obstacle(matrix, [F(int(i == seed)) - lam * graph.degree(i) for i in labels])
        assert [values.get(i, F(0)) for i in labels] == reference
        counts["independent_exact_batch_obstacle_outputs"] += 1
    else:
        counts["original_batch_ACL_outputs"] += 1
    assert result["volume"] < 1 / lam
    assert len(oracle.degree_log) == len(set(oracle.degree_log))
    assert len(oracle.row_log) == len(set(oracle.row_log)) == len(values)
    assert all(p == state.bar * graph.degree(i) * values[i] for i, p in result["probabilities"])
    assert state.metrics["old_candidate_heap_moves"] <= result["volume"]
    counts["original_final_residual_rows"] += len(graph)
    counts["executed_batches"] += len(state.history)
    counts["consumed_quotient_classes"] += state.metrics["consumed_exact_original_twin_classes"]
    work.update(ledger)
    return {
        "n": len(graph),
        "seed": seed,
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "exact_obstacle": exact,
        "volume": result["volume"],
        "metrics": dict(state.metrics),
        "charged_units": sum(ledger.values()),
    }


def binary_prefix(radius, counts, aggregate):
    ledger = Counter()
    lam, t, alpha = parameters(radius)
    oracle = PrivateBinaryTree(4 * radius + 8, ledger)
    state = BatchFrontier(oracle, 1, alpha, lam, lam / 2, ledger)
    last_factor_products = 0
    for depth in range(radius + 1):
        batch = state.take_batch()
        assert {vertex.label for vertex in batch} == set(range(2**depth, 2 ** (depth + 1)))
        before = ledger["batch_quotient_factor_off_diagonal_products"]
        state.advance(batch)
        last_factor_products = (
            ledger["batch_quotient_factor_off_diagonal_products"] - before
        ) // 11
        assert len(state.history[-1].blocks) == 2**depth
        counts["executed_private_binary_level_batches"] += 1
    order = 2**radius
    assert last_factor_products == order * (order - 1) * (order - 2) // 6
    result = state.lift()
    _, _, exact = radial_face(radius, 1 - t, lam)
    for label, value in result["records"]:
        assert value == exact[label.bit_length() - 1]
        counts["independent_binary_prefix_lifted_coordinates"] += 1
    assert state.volume == 3 * 2 ** (radius + 1) - 4
    assert len(oracle.row_log) == len(set(oracle.row_log)) == 2 ** (radius + 1) - 1
    assert all(group.q > (lam + lam / 2) * group.heap.data[0].degree for group in state.groups)
    assert len(state.groups) == 2**radius
    counts["nonterminal_binary_batch_prefixes_not_ACL_outputs"] += 1
    aggregate.update(ledger)
    return {
        "family": "nonterminal_private_binary_prefix",
        "radius": radius,
        "ambient_depth": 4 * radius + 8,
        "alpha": str(alpha),
        "epsilon": str(2 * lam),
        "volume": state.volume,
        "last_quotient_order": order,
        "last_factor_off_diagonal_products": last_factor_products,
        "metrics": dict(state.metrics),
        "charged_units": sum(ledger.values()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, work, profiles = Counter(), Counter(), []
    for graph in nx.graph_atlas_g():
        if len(graph) < 2 or len(graph) > (6 if args.full else 4) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in [F(1), F(1, 3), F(1, 64)]:
                for epsilon in [F(1, 4), F(1, 8), F(1, 32)]:
                    for exact in [False, True]:
                        check_case(graph, seed, alpha, epsilon, counts, work, exact=exact)
    for quotient in nx.graph_atlas_g():
        k = len(quotient)
        if k < 2 or k > (4 if args.full else 3) or not nx.is_connected(quotient):
            continue
        for mask in range(2**k) if args.full else [0, 2**k - 1]:
            sizes = [2 + i % 2 for i in range(k)]
            graph, partition = blow_up(quotient, sizes, mask)
            for seed in [members[-1] for members in partition]:
                profiles.append(
                    check_case(
                        graph,
                        seed,
                        F(1, 64),
                        F(1, 4 * len(graph)),
                        counts,
                        work,
                        partition=partition,
                    )
                )
    for multiplicity in [4, 16, 64] if args.full else [4]:
        graph, partition = blow_up(nx.path_graph(4), [multiplicity] * 4, 5)
        profile = check_case(
            graph,
            0,
            F(1, 3),
            F(1, 2**16 * graph.number_of_edges()),
            counts,
            work,
            partition=partition,
            dense=False,
        )
        assert profile["metrics"]["consumed_exact_original_twin_classes"] <= 5
        assert profile["metrics"]["complete_eligible_batches"] <= 5
        profile.update(family="fixed_four_type_multiplicity_growth", multiplicity=multiplicity)
        profiles.append(profile)
        counts["large_fixed_type_output_and_batch_count_cases"] += 1
    graph = nx.path_graph(5)
    ledger = Counter()
    state = BatchFrontier(LocalRows(graph, ledger), 2, F(1, 3), F(1, 64), F(1, 128), ledger)
    state.advance(state.take_batch())
    batch = state.take_batch()
    assert {vertex.label for vertex in batch} == {1, 3}
    state.advance(batch)
    assert len(state.history[-1].blocks) == 2
    assert len(state.groups) == 2
    assert state.matrix[0][0] - state.matrix[0][1] == state.gamma**2 / 2
    counts["induced_only_twin_quotient_contrast_witness"] += 1
    work.update(ledger)
    for power in [8, 80, 256, 1024] if args.full else [8, 80]:
        for exact in [False, True]:
            profiles.append(
                check_case(nx.path_graph(2), 0, F(1, 2**power), F(1, 4), counts, work, exact=exact)
            )
    for power in [8, 80, 256, 1024] if args.full else [8, 80]:
        for sign in [-1, 1]:
            profile = check_case(
                nx.path_graph(2),
                0,
                F(1, 3),
                2 * (F(1, 3) + sign * F(1, 2**power)),
                counts,
                work,
                exact=True,
            )
            assert profile["metrics"]["reverse_original_coordinate_writes"] == (
                2 if sign < 0 else 1
            )
            profile.update(family="tiny_signed_batch_gate", offset_power=power, sign=sign)
            profiles.append(profile)
            counts["tiny_signed_exact_batch_gate_cases"] += 1
    renamed = nx.relabel_nodes(
        nx.path_graph(5), {0: -(2**1024), 1: -17, 2: 0, 3: 10**30, 4: 2**1024}
    )
    for seed in renamed:
        check_case(renamed, seed, F(1, 3), F(1, 8), counts, work, exact=True)
        counts["arbitrary_signed_label_batch_cases"] += 1
    for leaves in [4, 16, 64, 256] if args.full else [4, 16]:
        ledger = Counter()
        oracle = PrivateDoubleStar(leaves, 2**1024, ledger)
        state = BatchFrontier(oracle, 0, F(1, 3), F(1, 16 * leaves), F(1, 32 * leaves), ledger)
        result = state.run()
        values = dict(result["records"])
        assert set(values) == {0} | set(range(2, leaves + 2))
        assert state.metrics["complete_eligible_batches"] == 2
        assert state.metrics["consumed_exact_original_twin_classes"] == 2
        assert state.volume == 2 * leaves + 1 and 1 not in oracle.rows
        for vertex in [
            v
            for transaction in state.history
            for block in transaction.blocks
            for v in block.members
        ]:
            residual = (
                F(int(vertex.label == 0))
                - vertex.degree * vertex.value
                + state.gamma * sum(values.get(neighbor.label, F(0)) for neighbor in vertex.row)
            )
            assert residual == state.lam * vertex.degree
        assert state.gamma * values[0] <= (state.lam + state.kappa) * (2**1024 + 1)
        work.update(ledger)
        counts["private_four_type_two_batch_large_ambient_certificates"] += 1
        profiles.append(
            {
                "family": "private_double_star",
                "leaves": leaves,
                "ambient_remote_leaves": "2^1024",
                "volume": state.volume,
                "metrics": dict(state.metrics),
                "charged_units": sum(ledger.values()),
            }
        )
    for power in [20, 128, 1024] if args.full else [20]:
        ledger = Counter()
        oracle = MassiveHub(2**power, ledger)
        state = BatchFrontier(oracle, 0, F(1, 3), F(1, 16), F(1, 32), ledger)
        result = state.run()
        assert result["records"] == [(0, F(15, 16))] and oracle.rows == [0]
        work.update(ledger)
        counts["private_huge_hub_only_leaf_row_certificates"] += 1
    for radius in range(1, 7 if args.full else 4):
        profiles.append(binary_prefix(radius, counts, work))
    result = {
        "description": __doc__,
        "full": args.full,
        "audit_only": dict(counts),
        "charged_implementation_units": dict(work),
        "profiles": profiles,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "frontier_exact.py",
                "frontier_group_branching.py",
                "frontier_groups.py",
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
