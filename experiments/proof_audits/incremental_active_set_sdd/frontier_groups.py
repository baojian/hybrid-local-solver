"""Paid exact frontier response groups, with dense validators kept separate.

Groups share their original adjacency into the admitted set, not original
degree. Partition refinement follows only newly read original incidences.
One reverse aggregate replay lifts all final physical coordinates.
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
from geometric_value_events import obstacle, solve
from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub
import networkx as nx


class Vertex:
    __slots__ = ("label", "degree", "group", "position", "eliminated", "row", "value")

    def __init__(self, label, degree):
        self.label, self.degree = label, degree
        self.group, self.position, self.eliminated = None, -1, False
        self.row, self.value = None, F(0)


class DegreeHeap:
    def __init__(self, group, work):
        self.group, self.work = group, work
        self.data, self.size = [], 0
        work["group_heap_header_words"] += 5

    def less(self, a, b):
        self.work["group_heap_degree_label_comparisons"] += 6
        return (a.degree, a.label) < (b.degree, b.label)

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.data[i].position, self.data[j].position = i, j
        self.work["group_heap_swap_and_stable_position_operations"] += 10

    def up(self, i):
        while i:
            p = (i - 1) // 2
            self.work["group_heap_up_arithmetic_and_branches"] += 4
            if not self.less(self.data[i], self.data[p]):
                break
            self.swap(i, p)
            i = p

    def down(self, i):
        while 2 * i + 1 < self.size:
            child = 2 * i + 1
            self.work["group_heap_down_arithmetic_and_branches"] += 7
            if child + 1 < self.size and self.less(self.data[child + 1], self.data[child]):
                child += 1
            if not self.less(self.data[child], self.data[i]):
                break
            self.swap(i, child)
            i = child

    def insert(self, vertex):
        assert vertex.position == -1
        if self.size == len(self.data):
            capacity = max(1, 2 * len(self.data))
            buffer = [None] * capacity
            for j in range(self.size):
                buffer[j] = self.data[j]
            self.work["group_heap_capacity_reserved_initialized_and_copied"] += (
                2 * capacity + 3 * self.size + 6
            )
            self.data = buffer
        vertex.group, vertex.position = self.group, self.size
        self.data[self.size] = vertex
        self.size += 1
        self.work["group_heap_insert_fields_and_operations"] += 8
        self.up(self.size - 1)

    def remove(self, vertex):
        i = vertex.position
        assert 0 <= i < self.size and self.data[i] is vertex
        self.size -= 1
        last = self.data[self.size]
        self.data[self.size] = None
        vertex.position = -1
        self.work["group_heap_remove_fields_and_operations"] += 9
        if i < self.size:
            self.data[i] = last
            last.position = i
            self.work["group_heap_remove_replacement_operations"] += 4
            if i and self.less(last, self.data[(i - 1) // 2]):
                self.up(i)
            else:
                self.down(i)


class Group:
    __slots__ = (
        "index",
        "q",
        "heap",
        "previous",
        "next",
        "live",
        "split_step",
        "split_child",
        "neighbor_step",
        "value_sum",
    )

    def __init__(self, index, q, work):
        self.index, self.q = index, q
        self.heap = DegreeHeap(self, work)
        self.previous, self.next, self.live = None, None, True
        self.split_step, self.split_child, self.neighbor_step = -1, None, -1
        self.value_sum = F(0)


class Cell:
    __slots__ = ("value",)

    def __init__(self):
        self.value = F(0)


class Pivot:
    __slots__ = ("vertex", "parent", "z", "coefficients", "splits", "fresh")

    def __init__(self, vertex, parent, z, coefficients, splits, fresh):
        self.vertex, self.parent, self.z = vertex, parent, z
        self.coefficients, self.splits, self.fresh = coefficients, splits, fresh


class GroupFrontier:
    def __init__(self, oracle, seed, alpha, epsilon, work):
        assert 0 < alpha <= 1 and 0 < epsilon < 1
        self.oracle, self.seed, self.alpha, self.epsilon, self.work = (
            oracle,
            seed,
            alpha,
            epsilon,
            work,
        )
        self.gamma = (1 - alpha) / (1 + alpha)
        self.bar, self.lam, self.kappa = 1 - self.gamma, epsilon / 2, epsilon / 4
        self.vertices, self.matrix = AVLMap(work), AVLMap(work)
        self.head = self.tail = None
        self.live_count, self.next_group, self.step, self.volume = 0, 0, 0, 0
        self.history, self.metrics = [], Counter()
        work["group_state_headers_and_parameter_operations"] += 45
        vertex = self.ensure(seed)
        self.new_group(F(1)).heap.insert(vertex)

    def ensure(self, label):
        def create():
            self.work["group_vertex_words_and_initialization"] += 20
            degree = self.oracle.degree(label)
            self.work["group_original_degree_reply_operations"] += 4
            assert degree >= 1
            return Vertex(label, degree)

        return self.vertices.get_or_create(label, create)

    def new_group(self, q):
        group = Group(self.next_group, q, self.work)
        self.next_group += 1
        group.previous = self.tail
        if self.tail is None:
            self.head = group
        else:
            self.tail.next = group
        self.tail = group
        self.live_count += 1
        self.work["group_record_words_initialization_and_live_links"] += 36
        self.metrics["historical_response_groups"] += 1
        return group

    def retire(self, group):
        assert group.live and group.heap.size == 0
        if group.previous is None:
            self.head = group.next
        else:
            group.previous.next = group.next
        if group.next is None:
            self.tail = group.previous
        else:
            group.next.previous = group.previous
        group.live = False
        group.previous = group.next = None
        self.live_count -= 1
        self.work["group_empty_record_retirement_operations"] += 14
        self.metrics["empty_group_retirements"] += 1

    def cell(self, a, b):
        i, j = sorted((a.index, b.index))
        self.work["group_matrix_pair_key_words_and_operations"] += 8

        def create():
            self.work["group_matrix_scalar_cell_words_and_initialization"] += 4
            self.metrics["historical_matrix_cells"] += 1
            return Cell()

        return self.matrix.get_or_create((i, j), create)

    def clone(self, parent):
        child = self.new_group(parent.q)
        other = self.head
        while other is not None:
            value = self.cell(parent, parent if other is child else other).value
            self.cell(child, other).value = value
            self.work["group_response_clone_scalar_and_list_operations"] += 6
            self.metrics["response_clone_interactions"] += 1
            other = other.next
        return child

    def eligible(self):
        group = self.head
        while group is not None:
            assert group.live and group.heap.size
            vertex = group.heap.data[0]
            self.work["group_minimum_degree_gate_and_live_scan_operations"] += 9
            self.metrics["group_gate_checks"] += 1
            if group.q > (self.lam + self.kappa) * vertex.degree:
                return vertex
            group = group.next
        return None

    def advance(self, vertex):
        parent = vertex.group
        assert not vertex.eliminated and parent.q > (self.lam + self.kappa) * vertex.degree
        assert self.lam * (self.volume + vertex.degree) < 1
        self.volume += vertex.degree
        sigma = vertex.degree - self.cell(parent, parent).value
        assert sigma > 0
        z = (parent.q - self.lam * vertex.degree) / sigma
        parent.heap.remove(vertex)
        self.step += 1
        self.work["group_volume_guard_pivot_and_removal_operations"] += 18
        splits, fresh = [], None
        if self.gamma:
            self.work["group_full_original_row_degree_charged"] += vertex.degree
            self.work["group_original_row_buffer_words_and_initialization"] += 2 * vertex.degree
            vertex.row = [None] * vertex.degree
            count = 0
            for label in self.oracle.row(vertex.label):
                assert count < vertex.degree
                neighbor = self.ensure(label)
                vertex.row[count] = neighbor
                count += 1
                self.work["group_original_incidence_and_membership_checks"] += 8
                if neighbor.eliminated:
                    continue
                if neighbor.group is None:
                    if fresh is None:
                        fresh = self.new_group(F(0))
                        fresh.neighbor_step = self.step
                    fresh.heap.insert(neighbor)
                    self.metrics["new_discovered_heap_members"] += 1
                else:
                    old = neighbor.group
                    if old.split_step != self.step:
                        child = self.clone(old)
                        old.split_step, old.split_child = self.step, child
                        child.neighbor_step = self.step
                        splits.append((old, child))
                        self.work["group_split_history_words_and_operations"] += 10
                        self.metrics["original_row_partition_splits"] += 1
                    old.heap.remove(neighbor)
                    old.split_child.heap.insert(neighbor)
                    self.metrics["old_neighbor_heap_membership_moves"] += 1
                self.work["group_neighbor_membership_branch_operations"] += 7
            assert count == vertex.degree
        else:
            vertex.row = []
            self.work["group_zero_coupling_row_skip"] += 2

        transient_count = self.live_count
        self.metrics["maximum_transient_response_groups"] = max(
            self.metrics["maximum_transient_response_groups"], transient_count
        )
        self.metrics["sum_squared_transient_groups_plus_one"] += (transient_count + 1) ** 2
        group = self.head
        while group is not None:
            following = group.next
            if group.heap.size == 0:
                self.retire(group)
            self.work["group_empty_record_scan_operations"] += 5
            group = following
        groups, weights, coefficients = [None] * self.live_count, [None] * self.live_count, []
        self.work["group_snapshot_and_lift_buffers_reserved"] += 7 * self.live_count + 6
        group = self.head
        for j in range(self.live_count):
            groups[j] = group
            weights[j] = self.cell(parent, group).value
            if group.neighbor_step == self.step:
                weights[j] += self.gamma
            coefficients.append((group, weights[j] / sigma))
            self.work["group_effective_coupling_and_lift_snapshot_operations"] += 10
            group = group.next
        assert group is None
        for j, group in enumerate(groups):
            group.q += weights[j] * z
            self.work["group_shared_load_publication_operations"] += 4
            self.metrics["shared_load_publications"] += 1
            for k in range(j, len(groups)):
                self.cell(group, groups[k]).value += weights[j] * weights[k] / sigma
                self.work["group_shared_fill_diagonal_pair_operations"] += 7
                self.metrics["shared_matrix_updates"] += 1
        for group in groups:
            assert group.heap.data[0].degree > self.cell(group, group).value
            self.work["group_post_update_positive_diagonal_check"] += 4
        vertex.eliminated = True
        self.history.append(Pivot(vertex, parent, z, coefficients, splits, fresh))
        self.work["group_pivot_history_words_growth_and_initialization"] += 22
        self.metrics["pivots"] += 1

    def lift(self, validator=None):
        for pivot in reversed(self.history):
            vertex = pivot.vertex
            vertex.value = pivot.z
            for group, coefficient in pivot.coefficients:
                vertex.value += coefficient * group.value_sum
                self.work["group_reverse_coefficient_aggregate_operations"] += 5
            assert vertex.value > 0
            for old, child in reversed(pivot.splits):
                old.value_sum += child.value_sum
                child.value_sum = F(0)
                self.work["group_reverse_partition_merge_operations"] += 5
                self.metrics["reverse_group_merges"] += 1
            if pivot.fresh is not None:
                pivot.fresh.value_sum = F(0)
                self.work["group_reverse_discovery_aggregate_retirement"] += 2
            pivot.parent.value_sum += vertex.value
            self.work["group_reverse_pivot_and_parent_aggregate_operations"] += 7
            self.metrics["reverse_coordinate_writes"] += 1
            if validator is not None:
                validator(self, pivot)

    def run(self, validator=None, lift_validator=None):
        if validator is not None:
            validator(self)
        while (vertex := self.eligible()) is not None:
            self.advance(vertex)
            if validator is not None:
                validator(self)
        self.lift(lift_validator)
        self.work["group_final_output_buffers_and_conversion_operations"] += 5 + 9 * len(
            self.history
        )
        return {
            "records": [(p.vertex.label, p.vertex.value) for p in self.history],
            "probabilities": [
                (p.vertex.label, self.bar * p.vertex.degree * p.vertex.value) for p in self.history
            ],
            "volume": self.volume,
        }


def prefix_validator(graph, seed, alpha, epsilon, counts):
    """All dense matrices, dictionaries and membership snapshots here are validators."""
    labels = sorted(graph)
    index = {label: i for i, label in enumerate(labels)}
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in labels]
        for i in labels
    ]
    load = [F(int(i == seed)) - epsilon * graph.degree(i) / 2 for i in labels]
    optimum = obstacle(matrix, load)
    snapshots = []
    counts["validator_original_obstacle_solves"] += 1

    def validate(state):
        vertices = [vertex for _, vertex in audit_map(state.vertices)]
        cells = {key: cell.value for key, cell in audit_map(state.matrix)}

        def c(a, b):
            return cells.get(tuple(sorted((a.index, b.index))), F(0))

        face = [index[p.vertex.label] for p in state.history]
        local = [[matrix[i][j] for j in face] for i in face]
        values = solve(local, [load[i] for i in face])
        assert all(0 < value <= optimum[i] for i, value in zip(face, values))
        assert state.volume == sum(graph.degree(labels[i]) for i in face) < 2 / epsilon
        columns = [
            solve(local, [F(int(j == k)) for j in range(len(face))]) for k in range(len(face))
        ]
        inverse = [[columns[j][i] for j in range(len(face))] for i in range(len(face))]
        remaining = [vertex for vertex in vertices if not vertex.eliminated]
        group, previous, groups, members = state.head, None, [], set()
        while group is not None:
            assert group.live and group.previous is previous and group.heap.size
            groups.append(group)
            heap = group.heap
            for i in range(heap.size):
                vertex = heap.data[i]
                assert vertex.group is group and vertex.position == i and vertex not in members
                assert not vertex.eliminated
                members.add(vertex)
                if i:
                    parent = heap.data[(i - 1) // 2]
                    assert (parent.degree, parent.label) <= (vertex.degree, vertex.label)
            assert all(item is None for item in heap.data[heap.size :])
            signatures = {
                tuple(graph.has_edge(vertex.label, labels[i]) for i in face)
                for vertex in heap.data[: heap.size]
            }
            assert len(signatures) == 1
            previous, group = group, group.next
        assert len(groups) == state.live_count and state.tail is previous
        assert members == set(remaining)
        for vertex in remaining:
            j = index[vertex.label]
            h = load[j] - sum(matrix[j][i] * value for i, value in zip(face, values))
            fill_self = sum(
                matrix[j][face[a]] * inverse[a][b] * matrix[face[b]][j]
                for a in range(len(face))
                for b in range(len(face))
            )
            assert vertex.group.q - state.lam * vertex.degree == h
            assert c(vertex.group, vertex.group) == fill_self
            assert vertex.degree - fill_self > 0
        for a, left in enumerate(remaining):
            j = index[left.label]
            for right in remaining[a + 1 :]:
                k = index[right.label]
                fill = sum(
                    matrix[j][face[u]] * inverse[u][v] * matrix[face[v]][k]
                    for u in range(len(face))
                    for v in range(len(face))
                )
                assert c(left.group, right.group) == fill
        assert state.vertices.size <= 1 + state.volume
        assert state.next_group <= 1 + state.volume
        snapshots.append(
            {
                group: [vertex.label for vertex in group.heap.data[: group.heap.size]]
                for group in groups
            }
        )
        counts["exact_prefix_face_Schur_AVL_heap_partition_checks"] += 1
        counts["validator_dense_face_and_inverse_column_solves"] += 1 + len(face)

    def lift_validate(state, pivot):
        j = next(i for i, p in enumerate(state.history) if p is pivot)
        final_face = [index[p.vertex.label] for p in state.history]
        local = [[matrix[i][k] for k in final_face] for i in final_face]
        solution = solve(local, [load[i] for i in final_face])
        exact = dict(zip((labels[i] for i in final_face), solution))
        assert pivot.vertex.value == exact[pivot.vertex.label]
        for group, members in snapshots[j].items():
            assert group.value_sum == sum(exact.get(label, F(0)) for label in members)
        counts["independent_reverse_coordinate_and_membership_aggregate_checks"] += 1

    return validate, lift_validate


def check_case(graph, seed, alpha, epsilon, counts, aggregate, prefixes=True):
    work = Counter()
    oracle = LocalRows(graph, work)
    state = GroupFrontier(oracle, seed, alpha, epsilon, work)
    if state.head.q == (state.lam + state.kappa) * state.head.heap.data[0].degree:
        counts["initial_exact_gate_ties"] += 1
    validators = prefix_validator(graph, seed, alpha, epsilon, counts) if prefixes else (None, None)
    result = state.run(*validators)
    values = dict(result["records"])
    for i in graph:
        residual = (
            F(int(i == seed))
            - graph.degree(i) * values.get(i, F(0))
            + state.gamma * sum(values.get(j, F(0)) for j in graph[i])
        )
        assert 0 <= residual <= F(3, 4) * epsilon * graph.degree(i)
        if i in values:
            assert residual == epsilon * graph.degree(i) / 2
    assert all(p == state.bar * graph.degree(i) * values[i] for i, p in result["probabilities"])
    assert result["volume"] < 2 / epsilon
    assert len(oracle.row_log) == len(set(oracle.row_log))
    assert len(oracle.degree_log) == len(set(oracle.degree_log))
    assert set(oracle.row_log) <= set(values)
    assert state.next_group <= 1 + result["volume"]
    assert state.metrics["old_neighbor_heap_membership_moves"] <= result["volume"]
    counts["terminal_unadmitted_exact_gate_ties"] += sum(
        vertex.group.q == (state.lam + state.kappa) * vertex.degree
        for _, vertex in audit_map(state.vertices)
        if not vertex.eliminated
    )
    assert state.metrics["reverse_group_merges"] == state.metrics["original_row_partition_splits"]
    assert state.metrics["reverse_coordinate_writes"] == len(values)
    aggregate.update(work)
    counts["original_ACL_output_certificates"] += 1
    counts["original_final_residual_rows"] += len(graph)
    counts["one_time_original_row_queries"] += len(oracle.row_log)
    counts["one_time_original_degree_queries"] += len(oracle.degree_log)
    for key in [
        "pivots",
        "shared_load_publications",
        "shared_matrix_updates",
        "response_clone_interactions",
        "old_neighbor_heap_membership_moves",
        "original_row_partition_splits",
        "sum_squared_transient_groups_plus_one",
    ]:
        counts["implemented_" + key] += state.metrics[key]
    return {
        "vertices": len(graph),
        "seed": seed,
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "original_active_volume": result["volume"],
        "discovered_labels": state.vertices.size,
        "metrics": dict(state.metrics),
        "charged_units": sum(work.values()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    counts, work, profiles = Counter(), Counter(), []
    for graph in nx.graph_atlas_g():
        if len(graph) < 2 or len(graph) > (6 if args.full else 4) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in [F(1), F(1, 3), F(1, 64)]:
                for epsilon in [F(1, 8), F(1, 2), F(2, 3)]:
                    check_case(graph, seed, alpha, epsilon, counts, work)
    for k in [4, 8, 16, 32, 64, 128, 256] if args.full else [4, 8]:
        graph = nx.path_graph(8 * k + 1)
        for _ in range(k):
            graph.add_edge(0, len(graph))
        profile = check_case(graph, 0, F(1, 3), F(1, 4 * k), counts, work, False)
        assert profile["metrics"]["maximum_transient_response_groups"] <= 2
        assert profile["metrics"].get("original_row_partition_splits", 0) == 0
        profiles.append({"family": "star_with_long_tail", "leaves": k, **profile})
        for family, graph, epsilon in [
            ("cycle", nx.cycle_graph(2 * k + 1), F(1, 4 * k)),
            ("endpoint_path", nx.path_graph(4 * k + 1), F(1, 2 * k)),
        ]:
            profiles.append(
                {
                    "family": family,
                    **check_case(graph, 0, F(1, 2**32), epsilon, counts, work, False),
                }
            )
    if args.full:
        for size in [16, 32, 64]:
            graph_seed = 20260908 + size
            profiles.append(
                {
                    "family": "seeded_cubic_regular_graph",
                    "graph_generation_seed": graph_seed,
                    **check_case(
                        nx.random_regular_graph(3, size, seed=graph_seed),
                        0,
                        F(1, 3),
                        F(1, 2 * size),
                        counts,
                        work,
                        False,
                    ),
                }
            )
        graph = nx.cycle_graph(6)
        mapping = {i: -(2**80 + 104729 * i) for i in graph}
        check_case(nx.relabel_nodes(graph, mapping), mapping[3], F(1, 64), F(1, 8), counts, work)
        counts["permuted_large_signed_label_cases"] += 1
        graph = nx.path_graph(65)
        for _ in range(8):
            graph.add_edge(0, len(graph))
        tied = check_case(graph, 0, F(1, 3), F(1, 18), counts, work, False)
        assert tied["metrics"]["pivots"] == 1
        profiles.append({"family": "exact_leaf_gate_tie", **tied})

    for power in [8, 80, 256, 1024] if args.full else [8, 80]:
        profiles.append(
            {
                "family": "tiny_alpha_full_two_vertex",
                **check_case(nx.path_graph(2), 0, F(1, 2**power), F(1, 8), counts, work),
            }
        )
    for power in [20, 128, 1024] if args.full else [20]:
        ledger = Counter()
        oracle = MassiveHub(2**power, ledger)
        state = GroupFrontier(oracle, 0, F(1, 3), F(1, 8), ledger)
        result = state.run()
        assert result["records"] == [(0, F(15, 16))]
        assert oracle.rows == [0] and state.vertices.size == 2 and state.volume == 1
        assert F(1, 2) * F(15, 16) <= F(2**power, 8)
        work.update(ledger)
        counts["private_huge_hub_one_row_certificates"] += 1
    result = {
        "description": __doc__,
        "full": args.full,
        "parameters": {
            "accuracy_namespace": "original ACL eps_appr",
            "lambda": "eps_appr/2",
            "strict_transformed_load_gate": "h > eps_appr*d/4",
            "producer_randomness": "none",
            "group_selection": "first eligible live group; minimum original degree then label",
        },
        "audit_only": dict(counts),
        "charged_implementation_units": dict(work),
        "profiles": profiles,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "frontier_exact.py",
                "geometric_value_events.py",
                "small_alpha_floor.py",
                "supplied_envelope_work.py",
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
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
