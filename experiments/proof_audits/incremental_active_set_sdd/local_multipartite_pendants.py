"""Local multipartite-core obstacle solver with incremental scalar events.

Promise: a complete multipartite core of minimum core degree at least two,
private degree-one pendants, and a physical core seed. No partition, core
size, graph matrix or future support is supplied to the solver. Dense exact
original obstacle solves below are independent validators only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import heapq
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

# The registered runner uses -m; the existing exact helpers use sibling imports.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from geometric_value_events import obstacle
from local_sun_solver import Oracle
from multipartite_scalar_response import response
import networkx as nx


class LocalMultipartite:
    def __init__(self, oracle, seed, alpha, lam, validator=None):
        assert 0 < alpha < 1 and lam > 0
        self.oracle, self.seed, self.lam = oracle, seed, lam
        self.gamma = (1 - alpha) / (1 + alpha)
        self.counts = Counter()
        self.cached = {}
        self.core = []
        self.groups = []
        self.membership = {}
        self.pendants = {}
        self.kernels = {}
        self.minimum_core_degree = 2
        self.forced_seed = None
        self.anchor = seed
        self.current = []
        self.events = []
        self.serial = 0
        self.slope = self.offset = self.total = F(0)
        self.unknown = {}
        self.unknown_heap = []
        self.validator = validator

    def checkpoint(self, kind):
        if self.validator is not None:
            self.validator(self, kind)

    def read_core(self, i):
        assert i not in self.cached
        row = self.oracle.row(i)
        self.cached[i] = row
        core_neighbors = []
        for j in row:
            if self.oracle.degree(j) > 1:
                core_neighbors.append(j)
            self.counts["positive_row_neighbor_classifications"] += 1
        self.counts["cached_positive_row_words"] += len(row)
        self.counts["temporary_core_neighbor_words"] += len(core_neighbors)
        return core_neighbors

    def push_event(self, threshold, group, piece):
        self.serial += 1
        heapq.heappush(self.events, (threshold, self.serial, group, piece))
        self.counts["future_event_insertions"] += 1
        self.counts["event_heap_comparison_budget"] += max(1, len(self.events).bit_length())
        self.counts["event_heap_record_words"] += 5

    def make_kernel(self, i, core_degree):
        degree = self.oracle.degree(i)
        return F(degree), F(i == self.seed) - self.lam * degree, degree - core_degree

    def add_part(self, vertices):
        """Build this new part once, retaining all earlier event records."""
        group = len(self.groups)
        self.groups.append(vertices)
        self.current.append((F(0), F(0)))
        raw = []
        coefficients = {}
        core_degree = len(self.core) - len(vertices)
        assert core_degree >= self.minimum_core_degree
        for index, i in enumerate(vertices):
            assert i not in self.membership
            self.membership[i] = group
            degree, load, leaves = self.make_kernel(i, core_degree)
            assert leaves >= 0
            self.pendants[i] = leaves
            self.kernels[i] = degree, load, leaves
            self.counts["retained_kernel_words"] += 3
            coefficients[i] = (F(0), F(0))
            raw.append((-load, index, i, (F(1, degree), load / degree)))
            if leaves:
                denominator = degree - self.gamma * self.gamma * leaves
                raw.append(
                    (
                        degree * self.lam / self.gamma - load,
                        index,
                        i,
                        (1 / denominator, (load - self.gamma * self.lam * leaves) / denominator),
                    )
                )
            self.counts["new_part_coordinate_records"] += 1
            self.counts["new_part_coordinate_words"] += 8
        raw.sort(key=lambda row: (row[0], row[1]))
        self.counts["created_coordinate_events"] += len(raw)
        self.counts["new_part_sort_comparison_budget"] += len(raw) * max(1, len(raw).bit_length())
        self.counts["temporary_part_event_words"] += 5 * len(raw)
        a = b = F(0)
        for threshold, _, i, piece in raw:
            transformed = threshold / self.gamma + a * threshold + b
            old = coefficients[i]
            assert old[0] * threshold + old[1] == piece[0] * threshold + piece[1]
            a += piece[0] - old[0]
            b += piece[1] - old[1]
            coefficients[i] = piece
            changed = (self.gamma * a / (1 + self.gamma * a), b / (1 + self.gamma * a))
            if transformed <= self.total:
                self.current[group] = changed
                self.counts["past_new_part_events_consumed"] += 1
            else:
                self.push_event(transformed, group, changed)
            self.counts["part_breakpoint_transforms"] += 1
            self.counts["negative_transformed_events"] += transformed < 0
        self.slope += self.current[group][0]
        self.offset += self.current[group][1]
        self.counts["constant_aggregate_updates"] += 1
        self.counts["part_insertions"] += 1

    def solve_current(self):
        previous = self.total
        while True:
            assert 0 <= self.slope < 1
            root = self.offset / (1 - self.slope)
            assert root >= previous
            self.counts["scalar_root_candidates"] += 1
            self.counts["next_event_tests"] += 1
            if not self.events or root <= self.events[0][0]:
                self.total = root
                self.counts["exact_restricted_roots"] += 1
                self.checkpoint("restricted root")
                return
            at, _, group, piece = heapq.heappop(self.events)
            old = self.current[group]
            assert old[0] * at + old[1] == piece[0] * at + piece[1]
            self.slope += piece[0] - old[0]
            self.offset += piece[1] - old[1]
            self.current[group] = piece
            self.counts["crossed_global_events"] += 1
            self.counts["constant_aggregate_updates"] += 1
            self.counts["event_heap_comparison_budget"] += 2 * max(
                1, (len(self.events) + 1).bit_length()
            )

    def recover_core(self):
        values = {}
        for group, vertices in enumerate(self.groups):
            a, b = self.current[group]
            mass = a * self.total + b
            field = self.gamma * (self.total - mass)
            assert field >= 0
            for i in vertices:
                degree, load, leaves = self.kernels[i]
                values[i] = response(load + field, degree, leaves, self.gamma, self.lam)
                self.counts["final_kernel_word_reads"] += 3
                self.counts["final_core_value_words"] += 1
        return values

    def output(self, values):
        out = {}
        for i, value in values.items():
            self.counts["final_core_value_reads"] += 1
            if value <= 0:
                continue
            out[i] = value
            row = self.cached[i] if i in self.cached else self.oracle.row(i)
            leaf = max(F(0), self.gamma * value - self.lam)
            for j in row:
                self.counts["final_positive_core_incidence_reads"] += 1
                if j == self.forced_seed:
                    self.counts["distinguished_seed_incidence_skips"] += 1
                    continue
                if self.oracle.degree(j) == 1 and leaf > 0:
                    assert self.oracle.row(j) == [i]
                    out[j] = leaf
                    self.counts["positive_leaf_output_words"] += 1
        if self.forced_seed is not None:
            out[self.forced_seed] = 1 - self.lam + self.gamma * values.get(self.anchor, F(0))
            self.counts["distinguished_seed_recovery_words"] += 1
        self.counts["output_words"] += len(out)
        return out

    def run(self):
        degree = self.oracle.degree(self.seed)
        if self.lam * degree >= 1:
            self.counts["trivial_zero_stops"] += 1
            return {}
        seed_neighbors = self.read_core(self.seed)
        leaves = degree - len(seed_neighbors)
        seed_value = response(1 - self.lam * degree, degree, leaves, self.gamma, self.lam)
        chosen = None
        for i in seed_neighbors:
            self.counts["startup_original_gate_tests"] += 1
            if self.gamma * seed_value > self.lam * self.oracle.degree(i):
                if chosen is None or self.oracle.degree(i) < self.oracle.degree(chosen):
                    chosen = i
        if chosen is None:
            self.counts["exact_seed_star_stops"] += 1
            return self.output({self.seed: seed_value})
        return self.continue_core(self.seed, seed_neighbors, chosen)

    def continue_core(self, anchor, seed_neighbors, chosen):
        other_neighbors = self.read_core(chosen)
        first, second = set(seed_neighbors), set(other_neighbors)
        # Every core label appears in at least one of two adjacent core rows.
        self.core = list(dict.fromkeys([anchor, *seed_neighbors, *other_neighbors]))
        assert chosen in self.core
        seed_part = [i for i in self.core if i not in first]
        other_part = [i for i in self.core if i not in second]
        assert anchor in seed_part and chosen in other_part
        self.counts["startup_core_set_work"] += 4 * len(self.core) + len(first) + len(second)
        self.counts["enumerated_core_identifiers"] += len(self.core)
        self.add_part(seed_part)
        self.solve_current()
        self.add_part(other_part)
        self.solve_current()
        for index, i in enumerate(self.core):
            if i not in self.membership:
                self.unknown[i] = None
                heapq.heappush(
                    self.unknown_heap, (self.lam * self.oracle.degree(i) / self.gamma, index, i)
                )
                self.counts["unknown_heap_insertions"] += 1
                self.counts["unknown_heap_comparison_budget"] += max(
                    1, len(self.unknown_heap).bit_length()
                )
        while self.unknown:
            while self.unknown_heap[0][2] not in self.unknown:
                heapq.heappop(self.unknown_heap)
                self.counts["stale_unknown_heap_removals"] += 1
                self.counts["unknown_heap_comparison_budget"] += 2 * max(
                    1, (len(self.unknown_heap) + 1).bit_length()
                )
            threshold, _, chosen = self.unknown_heap[0]
            self.counts["unknown_minimum_original_gate_tests"] += 1
            if self.total <= threshold:
                self.counts["quiet_unknown_part_stops"] += 1
                self.counts["unread_unknown_core_vertices_at_stop"] += len(self.unknown)
                break
            self.checkpoint("positive unknown gate")
            neighbors = set(self.read_core(chosen))
            group = []
            self.counts["complement_snapshot_words"] += len(self.unknown)
            for i in list(self.unknown):
                self.counts["complement_membership_tests"] += 1
                if i in neighbors:
                    self.counts["complement_outside_incidence_charges"] += 1
                else:
                    group.append(i)
                    del self.unknown[i]
                    self.counts["complement_removed_identifier_charges"] += 1
            assert chosen in group
            self.counts["positive_part_representatives"] += 1
            self.counts["positive_representative_degree_budget"] += self.oracle.degree(chosen)
            self.add_part(group)
            self.solve_current()
        return self.output(self.recover_core())


def explicit_graph(sizes, pendants):
    graph = nx.complete_multipartite_graph(*sizes)
    n = sum(sizes)
    parent = {}
    for i, count in enumerate(pendants):
        for _ in range(count):
            graph.add_edge(i, n)
            parent[n] = i
            n += 1
    return graph, parent


class ReversedRows:
    def __init__(self, graph):
        self.graph = graph

    def degree(self, i):
        return self.graph.degree(i)

    def __getitem__(self, i):
        return list(reversed(list(self.graph[i])))


def audit_case(sizes, pendants, seed, alpha, lam, counts, reverse=False):
    graph, parent = explicit_graph(sizes, pendants)
    n, core_n = len(graph), sum(sizes)
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in graph]
    exact = obstacle(matrix, load)
    last_values = {}

    def validate(state, kind):
        known = set(state.membership)
        region = [i for i in graph if i in known or parent.get(i) in known]
        partial = obstacle(
            [[matrix[i][j] for j in region] for i in region], [load[i] for i in region]
        )
        expanded = dict(zip(region, partial))
        predicted = {}
        for g, vertices in enumerate(state.groups):
            a, b = state.current[g]
            mass = a * state.total + b
            field = gamma * (state.total - mass)
            for i in vertices:
                predicted[i] = response(
                    F(i == seed) - lam * graph.degree(i) + field,
                    graph.degree(i),
                    pendants[i],
                    gamma,
                    lam,
                )
        assert all(predicted[i] == expanded[i] for i in known)
        assert sum(predicted.values()) == state.total
        assert all(x <= exact[i] for i, x in expanded.items())
        assert all(expanded.get(i, F(0)) >= x for i, x in last_values.items())
        last_values.update(expanded)
        for i in range(core_n):
            if i not in known:
                original_gate = load[i] - sum(matrix[i][j] * x for j, x in expanded.items())
                assert original_gate == gamma * state.total - lam * graph.degree(i)
                counts["independent_unknown_original_gate_checks"] += 1
        counts["independent_restricted_obstacle_checks"] += 1
        counts["reference_original_matrix_words"] += len(region) ** 2
        counts["reference_recovered_core_values"] += len(predicted)
        counts["positive_gate_checkpoints"] += kind == "positive unknown gate"

    state = LocalMultipartite(
        Oracle(ReversedRows(graph) if reverse else graph), seed, alpha, lam, validate
    )
    out = state.run()
    assert [out.get(i, F(0)) for i in range(n)] == exact
    assert state.oracle.rows == set(out)
    assert state.oracle.counts["adjacency_entries_inspected"] == sum(graph.degree(i) for i in out)
    assert lam * sum(graph.degree(i) for i in out) < 1
    c = state.counts
    assert c["part_insertions"] == len(state.groups)
    assert c["new_part_coordinate_records"] == len(state.membership)
    assert c["created_coordinate_events"] <= 2 * len(state.membership)
    assert (
        c["future_event_insertions"] + c["past_new_part_events_consumed"]
        == c["created_coordinate_events"]
    )
    assert c["crossed_global_events"] <= c["future_event_insertions"]
    assert (
        c["complement_membership_tests"]
        == c["complement_outside_incidence_charges"] + c["complement_removed_identifier_charges"]
    )
    assert c["complement_outside_incidence_charges"] <= c["positive_representative_degree_budget"]
    assert c["complement_removed_identifier_charges"] <= core_n
    assert c["final_core_value_words"] == len(state.membership)
    counts["complete_original_obstacle_comparisons"] += 1
    counts["positive_only_original_row_certificates"] += 1
    counts["incremental_event_and_discovery_ledgers"] += 1
    return state


class ImplicitMultipartite:
    def __init__(self, sizes, pendants):
        self.sizes, self.pendants = sizes, pendants
        self.core_n = sum(sizes)
        self.membership = [g for g, size in enumerate(sizes) for _ in range(size)]

    def degree(self, i):
        if isinstance(i, tuple):
            return 1
        return self.core_n - self.sizes[self.membership[i]] + self.pendants[i]

    def __getitem__(self, i):
        if isinstance(i, tuple):
            return [i[0]]
        assert self.pendants[i] < 1000, "An enormous inactive pendant row must remain unread"
        return [j for j in range(self.core_n) if self.membership[j] != self.membership[i]] + [
            (i, j) for j in range(self.pendants[i])
        ]


def implicit_cases(counts):
    records = []
    families = [
        ([2, 2], [0, 2, 0, 10**12]),
        ([1, 2, 2], [0, 0, 2, 10**18, 10**18]),
        ([2, 2, 2], [0, 2, 0, 1, 0, 10**18]),
        ([1, 1, 2, 2], [0, 0, 10**12, 10**12, 2, 10**18]),
    ]
    for (sizes, pendants), alpha, reverse in itertools.product(
        families, [F(1, 3), F(1, 1009)], [False, True]
    ):
        graph = ImplicitMultipartite(sizes, pendants)
        state = LocalMultipartite(
            Oracle(ReversedRows(graph) if reverse else graph), 0, alpha, F(1, 40)
        )
        out = state.run()
        values = {i: out.get(i, F(0)) for i in range(graph.core_n)}
        masses = [
            sum(values[i] for i in range(graph.core_n) if graph.membership[i] == g)
            for g in range(len(sizes))
        ]
        total = sum(masses)
        for i, leaves in enumerate(pendants):
            value = values[i]
            leaf = max(F(0), state.gamma * value - state.lam)
            residual = (
                F(i == 0)
                - graph.degree(i) * value
                + state.gamma * (total - masses[graph.membership[i]] + leaves * leaf)
            )
            assert residual >= 0
            assert (
                residual == state.lam * graph.degree(i)
                if value > 0
                else residual <= state.lam * graph.degree(i)
            )
            if leaf > 0:
                assert all(out[(i, j)] == leaf for j in range(leaves))
            else:
                assert state.gamma * value <= state.lam
        assert state.oracle.rows == set(out)
        volume = sum(graph.degree(i) for i in out)
        assert state.lam * volume < 1
        assert state.oracle.counts["adjacency_entries_inspected"] == volume
        counts["implicit_original_kkt_certificates"] += 1
        records.append(
            {
                "part_sizes": sizes,
                "pendant_counts": pendants,
                "ambient_vertices": graph.core_n + sum(pendants),
                "seed": 0,
                "alpha_lazy": str(alpha),
                "lambda": str(state.lam),
                "reverse_rows": reverse,
                "positive_vertices": len(out),
                "original_volume": volume,
                "algorithm_counts": dict(state.counts),
                "original_graph_access": dict(state.oracle.counts),
            }
        )
    return records


def exact_ties(counts):
    cases = []
    for alpha, reverse in itertools.product([F(1, 3), F(1, 1009), F(1008, 1009)], [False, True]):
        gamma = (1 - alpha) / (1 + alpha)
        specs = [
            ("first core birth", [1, 2, 2], [0] * 5, gamma / (4 * (3 + gamma))),
            ("seed leaf birth", [2, 2], [2, 0, 0, 0], gamma / (4 * (1 + gamma))),
            ("unknown part gate", [1, 1, 1], [0, 0, 4], gamma / (12 - 2 * gamma)),
            ("initial zero gate", [2, 2], [0] * 4, F(1, 2)),
        ]
        for kind, sizes, pendants, lam in specs:
            state = audit_case(sizes, pendants, 0, alpha, lam, counts, reverse)
            if kind == "unknown part gate":
                assert state.unknown == {2: None}
                assert state.total == state.unknown_heap[0][0]
                assert 2 not in state.oracle.rows
            else:
                assert state.oracle.rows <= {0}
            cases.append(
                {
                    "kind": kind,
                    "alpha_lazy": str(alpha),
                    "lambda": str(lam),
                    "reverse_rows": reverse,
                    "algorithm_counts": dict(state.counts),
                }
            )
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, algorithm, accesses = Counter(), Counter(), Counter()
    sizes_list = [[2, 2], [1, 1, 1], [1, 2, 2], [2, 3]]
    if args.full:
        sizes_list += [[2, 2, 2], [1, 2, 3], [3, 3], [1, 1, 2, 2], [2, 2, 3], [1, 1, 1, 1, 1]]
    params = [
        (F(1, 3), F(1, 20)),
        (F(1, 1009), F(1, 200)),
        (F(1008, 1009), F(1, 20)),
        (F(1, 3), F(1, 4)),
    ]
    for sizes in sizes_list:
        n = sum(sizes)
        patterns = [[0] * n, [i % 3 for i in range(n)], [3 if i % 2 else 0 for i in range(n)]]
        if args.full:
            patterns += [[8 if i == j else i % 2 for i in range(n)] for j in range(n)]
        for pendant, seed, (alpha, lam), reverse in itertools.product(
            patterns, range(n), params, [False, True]
        ):
            state = audit_case(sizes, pendant, seed, alpha, lam, counts, reverse)
            algorithm.update(state.counts)
            accesses.update(state.oracle.counts)
    ties = exact_ties(counts)
    implicit = implicit_cases(counts)
    result = {
        "audit": "incremental_active_set_sdd.local_multipartite_pendants",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "part_size_patterns": sizes_list,
        "pendant_patterns": "zero, i mod3, alternating zero/three; full adds one eight-leaf core against alternating zero/one",
        "seed": "every core vertex",
        "row_orders": ["construction order", "reversed incidence order"],
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in params],
        "stopping_rule": "exact scalar root after all prior known-part events; nonpositive unknown minimum gate; seed-star and trivial zero exits",
        "accuracy_scope": "exact original lambda obstacle; lambda=rho gives RPPR, lambda=eps_appr/2 gives ACL",
        "access_scope": "Actual degree/adjacency-only solver under complete-multipartite core, minimum core degree>=2 and core seed promise. No supplied partition or full original matrix in the algorithm.",
        "algorithm_counts": dict(algorithm),
        "original_graph_access": dict(accesses),
        "audit_only": dict(counts),
        "exact_ties": ties,
        "implicit_cases": implicit,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "local_sun_solver",
                "multipartite_scalar_response",
                "geometric_value_events",
            ]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
