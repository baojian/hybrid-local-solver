"""A paid native gap-threshold push and its deterministic alpha-floor repair.

Graph rows are cached once on first legal activation. A sorted dynamic
array charges all insertion shifts; repeated pushes follow stable record
pointers. Exact full-graph and obstacle calculations are validators only.
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

from small_alpha_constant_shift import residual, shift_transfer
from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub, physical
import networkx as nx


class Record:
    __slots__ = ("label", "degree", "value", "residual", "active", "queued", "next", "neighbors")

    def __init__(self, label, degree):
        self.label, self.degree = label, degree
        self.value, self.residual = F(0), F(0)
        self.active, self.queued = False, False
        self.next, self.neighbors = None, None


class SortedRecords:
    """Stable records in explicitly doubled, sorted pointer arrays."""

    def __init__(self, oracle, work):
        self.oracle, self.work, self.size, self.capacity = oracle, work, 0, 1
        self.array = [None]
        self.allocated_slots = 1
        work["graph_state_words_reserved"] += 10
        work["map_header_initialization"] += 10

    def position(self, label):
        lo, hi = 0, self.size
        while lo < hi:
            mid = (lo + hi) // 2
            if self.array[mid].label < label:
                lo = mid + 1
            else:
                hi = mid
            self.work["map_binary_lookup_operations"] += 7
        self.work["map_final_key_comparison"] += 3
        return lo

    def get(self, label):
        index = self.position(label)
        assert index < self.size and self.array[index].label == label
        return self.array[index]

    def ensure(self, label):
        index = self.position(label)
        if index < self.size and self.array[index].label == label:
            self.work["existing_stable_record_returns"] += 2
            return self.array[index]
        if self.size == self.capacity:
            target = [None] * (2 * self.capacity)
            self.work["graph_state_words_reserved"] += 2 * self.capacity
            self.work["map_array_initialization_and_copy"] += 3 * self.capacity
            self.allocated_slots += 2 * self.capacity
            for j in range(self.size):
                target[j] = self.array[j]
            self.array, self.capacity = target, 2 * self.capacity
        degree = self.oracle.degree(label)
        assert degree >= 1
        record = Record(label, degree)
        self.work["graph_state_words_reserved"] += 8
        self.work["new_record_field_initialization"] += 16
        for j in range(self.size, index, -1):
            self.array[j] = self.array[j - 1]
            self.work["sorted_map_insertion_pointer_shifts"] += 3
        self.array[index] = record
        self.size += 1
        self.work["new_record_map_insertion"] += 4
        return record


class NativePush:
    def __init__(self, oracle, seed, alpha, epsilon, work):
        assert 0 < alpha <= 1 and 0 < epsilon < 1
        self.oracle, self.seed, self.alpha, self.epsilon, self.work = (
            oracle,
            seed,
            alpha,
            epsilon,
            work,
        )
        self.gamma, self.bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        self.lam = epsilon / 2
        self.records = SortedRecords(oracle, work)
        self.head, self.tail = None, None
        self.mass, self.active_volume, self.active_count = F(1), 0, 0
        self.push_degree_work, self.push_count = 0, 0
        work["graph_state_words_reserved"] += 20
        work["native_header_and_parameter_operations"] += 32
        source = self.records.ensure(seed)
        source.residual = F(1)
        self.enqueue(source)

    def enqueue(self, record):
        self.work["queue_threshold_and_membership_checks"] += 6
        if record.residual > self.epsilon * record.degree and not record.queued:
            record.queued, record.next = True, None
            if self.tail is None:
                self.head = record
            else:
                self.tail.next = record
            self.tail = record
            self.work["intrusive_queue_link_updates"] += 6

    def activate(self, record):
        assert not record.active and record.neighbors is None
        record.active = True
        self.active_volume += record.degree
        self.active_count += 1
        # All old active residuals and this new legal residual already pay
        # this volume, before any degree-sized adjacency buffer is allocated.
        assert self.lam * self.active_volume < self.mass <= 1
        record.neighbors = [None] * record.degree
        self.work["graph_state_words_reserved"] += record.degree
        self.work["first_activation_and_exact_degree_buffer_initialization"] += record.degree + 10
        number = 0
        for label in self.oracle.row(record.label):
            assert number < record.degree
            record.neighbors[number] = self.records.ensure(label)
            number += 1
            self.work["first_row_stable_neighbor_pointer_writes"] += 4
        assert number == record.degree

    def run(self, validator=None):
        if validator is not None:
            validator(self)
        while self.head is not None:
            record = self.head
            self.head = record.next
            if self.head is None:
                self.tail = None
            record.queued, record.next = False, None
            self.work["intrusive_queue_pop_and_loop_operations"] += 10
            assert record.residual > self.epsilon * record.degree
            if not record.active:
                self.activate(record)
            increment = (record.residual - self.lam * record.degree) / record.degree
            assert increment > self.epsilon / 2
            record.value += increment
            record.residual = self.lam * record.degree
            self.mass -= self.bar * record.degree * increment
            self.push_count += 1
            self.push_degree_work += record.degree
            self.work["native_push_scalar_arithmetic_and_state_updates"] += 20
            for neighbor in record.neighbors:
                neighbor.residual += self.gamma * increment
                self.work["cached_neighbor_residual_read_modify_write"] += 5
                self.enqueue(neighbor)
            assert 0 <= self.mass <= 1
            if validator is not None:
                validator(self)
        output, position = [None] * self.active_count, 0
        self.work["graph_state_words_reserved"] += 3 * self.active_count
        self.work["final_output_initialization"] += self.active_count + 2
        for i in range(self.records.size):
            record = self.records.array[i]
            if record.active:
                output[position] = (record.label, record.value)
                position += 1
                self.work["final_positive_output_record_writes"] += 4
            self.work["final_discovered_record_scan"] += 3
        assert position == self.active_count
        return output


class CachedRows:
    def __init__(self, work):
        self.state, self.work = None, work

    def degree(self, label):
        self.work["cached_original_degree_reads"] += 1
        return self.state.records.get(label).degree

    def row(self, label):
        record = self.state.records.get(label)
        assert record.active and record.neighbors is not None
        self.work["cached_original_row_headers"] += 1
        for neighbor in record.neighbors:
            self.work["cached_original_adjacency_label_reads"] += 2
            yield neighbor.label


def solve_local(oracle, seed, alpha, epsilon, work, validator=None):
    floor = epsilon**2 / (16 + epsilon**2)
    effective = max(alpha, floor)
    cache = CachedRows(work)
    work["complete_local_floor_parameters_and_cache_header"] += 12

    def producer(native_alpha, native_epsilon, failure):
        assert native_alpha == effective and native_epsilon == epsilon / 2 and failure == F(1, 16)
        cache.state = NativePush(oracle, seed, native_alpha, native_epsilon, work)
        return cache.state.run(validator)

    result = shift_transfer(cache, seed, alpha, epsilon, 4 / epsilon, F(1, 8), producer, work)
    assert result["abort"] is None
    return result, cache.state


def validate_state(graph, seed, optimum, state, counts):
    mapping = state.records
    records = mapping.array[: mapping.size]
    assert all(records[i - 1].label < records[i].label for i in range(1, len(records)))
    assert all(record is None for record in mapping.array[mapping.size :])
    assert mapping.allocated_slots < 4 * (mapping.size + 1)
    vector = [F(0)] * len(graph)
    stored = {record.label: record for record in records}
    for record in records:
        vector[record.label] = record.value
        assert record.degree == graph.degree(record.label)
        assert record.active == (record.value > 0)
        assert record.value <= optimum[record.label]
        if record.active:
            assert len(record.neighbors) == record.degree
            assert {r.label for r in record.neighbors} == set(graph[record.label])
            assert all(stored[r.label] is r for r in record.neighbors)
    actual = residual(graph, seed, state.alpha, vector)
    assert all(r >= 0 for r in actual)
    assert all(actual[i] == (stored[i].residual if i in stored else 0) for i in graph)
    assert sum(actual) == state.mass
    volume = sum(record.degree for record in records if record.active)
    assert volume == state.active_volume and volume < 2 / state.epsilon
    assert state.lam * volume <= state.mass
    assert all(record.residual >= state.lam * record.degree for record in records if record.active)
    assert mapping.size <= 1 + volume
    seen, cursor = set(), state.head
    while cursor is not None:
        assert cursor.label not in seen and cursor.queued
        assert cursor.residual > state.epsilon * cursor.degree
        seen.add(cursor.label)
        cursor = cursor.next
    assert seen == {record.label for record in records if record.queued}
    assert seen == {
        record.label for record in records if record.residual > state.epsilon * record.degree
    }
    assert (state.tail is None) == (state.head is None)
    assert state.push_degree_work <= 2 / (state.bar * state.epsilon)
    counts["exact_native_prefix_invariant_checks"] += 1
    counts["validator_original_residual_rows"] += len(graph)
    counts["stable_map_queue_cache_and_volume_checks"] += 1


def audit_case(graph, seed, alpha, epsilon, counts, work):
    effective = max(alpha, epsilon**2 / (16 + epsilon**2))
    _, _, optimum = physical(graph, seed, effective, epsilon / 2)
    counts["validator_native_obstacle_solves"] += 1
    access = LocalRows(graph, work)

    def validator(state):
        validate_state(graph, seed, optimum, state, counts)

    before_words = work["graph_state_words_reserved"]
    result, state = solve_local(access, seed, alpha, epsilon, work, validator)
    vector = [F(0)] * len(graph)
    for label, value in result["records"]:
        vector[label] = value
    actual = residual(graph, seed, alpha, vector)
    assert all(0 <= r <= epsilon * graph.degree(i) for i, r in enumerate(actual))
    assert sum(graph.degree(i) for i in graph if vector[i] > 0) < 4 / epsilon
    assert len(set(access.row_log)) == len(access.row_log) == state.active_count
    assert len(set(access.degree_log)) == len(access.degree_log) == state.records.size
    assert work["graph_state_words_reserved"] - before_words <= 80 * (1 + state.active_volume)
    counts["complete_local_original_ACL_certificates"] += 1
    counts["original_rows_read_once_on_activation"] += len(access.row_log)
    counts["original_degrees_queried_once_per_discovery"] += len(access.degree_log)
    counts["native_pushes"] += state.push_count
    counts["native_degree_weighted_updates"] += state.push_degree_work
    counts["branch_" + result["branch"]] += 1
    counts["initial_native_threshold_ties"] += (epsilon / 2) * graph.degree(seed) == 1
    counts["empty_native_outputs"] += state.active_count == 0
    return {
        "vertices": len(graph),
        "edges": graph.number_of_edges(),
        "seed": seed,
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "native_pushes": state.push_count,
        "degree_weighted_updates": state.push_degree_work,
        "active_volume": state.active_volume,
        "discovered_labels": state.records.size,
        "branch": result["branch"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    stress_profiles = []
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= (5 if args.full else 3) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for epsilon in [F(1, 2), F(3, 4)] if args.full else [F(3, 4)]:
                for alpha in [F(1), F(1, 3), F(1, 2**80)] if args.full else [F(1, 2**80)]:
                    audit_case(graph, seed, alpha, epsilon, counts, work)
    if args.full:
        for graph, epsilon in [
            (nx.path_graph(2), F(1, 8)),
            (nx.path_graph(3), F(1, 4)),
            (nx.cycle_graph(8), F(1, 4)),
            (nx.path_graph(16), F(1, 4)),
        ]:
            stress_profiles.append(audit_case(graph, 0, F(1, 2**80), epsilon, counts, work))
    for degree in [2**20, 2**80, 2**1024]:
        access = MassiveHub(degree, work)
        result, state = solve_local(access, 0, F(1, 2**1024), F(1, 4), work)
        assert state.active_volume == 1 and state.push_count == 1 and access.rows == [0]
        assert result["records"] == [(0, F(15, 16))]
        counts["private_huge_hub_single_row_compositions"] += 1
    for k in range(1, 1025 if args.full else 17):
        epsilon = F(1, 2**k)
        floor = epsilon**2 / (16 + epsilon**2)
        bar = 2 * floor / (1 + floor)
        assert 2 / (bar * (epsilon / 2)) <= 36 / epsilon**3
        counts["exact_symbolic_uniform_update_budgets"] += 1
    result = {
        "audit": "incremental_active_set_sdd.native_gap_push",
        "scope": "Implemented local gap-threshold push, charged sorted map and cached rows, followed by deterministic alpha-floor arithmetic repair. Full-graph residuals and exact obstacles validate the computation; they are not production oracles.",
        "arithmetic": "exact fractions; abstract exact-real word work. Graph-state reservations are recorded separately; Python scalar-object allocation and bit complexity are not measured.",
        "parameters": {
            "full": args.full,
            "native_accuracy": "eps_appr/2",
            "native_lambda": "eps_appr/4",
            "alpha_floor": "eps_appr^2/(16+eps_appr^2)",
            "random_seed": None,
        },
        "audit_only": dict(counts),
        "stress_profiles": stress_profiles,
        "charged_native_and_wrapper_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "small_alpha_constant_shift.py",
                "small_alpha_floor.py",
                "supplied_envelope_work.py",
                "geometric_value_events.py",
                "local_gap_certificate.py",
            ]
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}, indent=2
        )
    )


if __name__ == "__main__":
    main()
