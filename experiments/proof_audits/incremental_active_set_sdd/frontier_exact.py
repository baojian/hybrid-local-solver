"""Charged exact live-frontier elimination reference for original ACL output.

The producer uses deterministic AVL maps and intrusive incidence lists.
Dense face, Schur and obstacle calculations below are validators only.
The fill-dependent bound is not the conjectured general nearly-linear rate.
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

from geometric_value_events import obstacle, solve
from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub
import networkx as nx


class MapNode:
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key, value):
        self.key, self.value = key, value
        self.left = self.right = None
        self.height = 1


class AVLMap:
    def __init__(self, work):
        work["frontier_map_header_words"] += 4
        self.root, self.size, self.work = None, 0, work

    def height(self, node):
        self.work["frontier_map_height_reads"] += 1
        return node.height if node else 0

    def refresh(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        self.work["frontier_map_height_arithmetic_and_write"] += 3

    def rotate_left(self, node):
        child = node.right
        assert child is not None
        node.right, child.left = child.left, node
        self.work["frontier_map_rotation_pointer_operations"] += 6
        self.refresh(node)
        self.refresh(child)
        return child

    def rotate_right(self, node):
        child = node.left
        assert child is not None
        node.left, child.right = child.right, node
        self.work["frontier_map_rotation_pointer_operations"] += 6
        self.refresh(node)
        self.refresh(child)
        return child

    def insert(self, node, key, create):
        self.work["frontier_map_recursive_frame_words_and_branches"] += 12
        if node is None:
            self.work["frontier_map_node_words_and_initialization"] += 12
            value = create()
            self.size += 1
            return MapNode(key, value), value
        self.work["frontier_map_key_word_comparisons"] += 8
        if key == node.key:
            return node, node.value
        if key < node.key:
            node.left, value = self.insert(node.left, key, create)
        else:
            node.right, value = self.insert(node.right, key, create)
        self.work["frontier_map_child_pointer_and_return_operations"] += 4
        self.refresh(node)
        balance = self.height(node.left) - self.height(node.right)
        self.work["frontier_map_balance_arithmetic_and_comparisons"] += 4
        if balance > 1:
            assert node.left is not None
            if self.height(node.left.left) < self.height(node.left.right):
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node), value
        if balance < -1:
            assert node.right is not None
            if self.height(node.right.right) < self.height(node.right.left):
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node), value
        return node, value

    def get_or_create(self, key, create):
        self.root, value = self.insert(self.root, key, create)
        self.work["frontier_map_root_and_result_operations"] += 3
        return value


class Vertex:
    __slots__ = (
        "label",
        "index",
        "degree",
        "diagonal",
        "load",
        "head",
        "live_degree",
        "queued",
        "queue_next",
        "eliminated",
        "original_row",
        "pivot",
        "coefficients",
        "value",
    )

    def __init__(self, label, index, degree, load):
        self.label, self.index, self.degree = label, index, degree
        self.diagonal, self.load = F(degree), load
        self.head, self.live_degree = None, 0
        self.queued, self.queue_next, self.eliminated = False, None, False
        self.original_row, self.pivot, self.coefficients, self.value = None, F(0), None, F(0)


class Incidence:
    __slots__ = ("edge", "owner", "other", "previous", "next")

    def __init__(self, edge, owner, other):
        self.edge, self.owner, self.other = edge, owner, other
        self.previous, self.next = None, owner.head
        if owner.head is not None:
            owner.head.previous = self
        owner.head = self
        owner.live_degree += 1


class Edge:
    __slots__ = ("a", "b", "weight", "ia", "ib", "active")

    def __init__(self, a, b):
        self.a, self.b, self.weight, self.active = a, b, F(0), True
        self.ia, self.ib = Incidence(self, a, b), Incidence(self, b, a)


class ExactFrontier:
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
        self.bar = 1 - self.gamma
        self.lam, self.kappa = epsilon / 2, epsilon / 4
        self.vertices, self.edges = AVLMap(work), AVLMap(work)
        self.queue_head = self.queue_tail = None
        self.history, self.volume, self.live_edges = [], 0, 0
        self.metrics = Counter()
        work["frontier_state_header_and_parameter_operations"] += 40
        self.check_gate(self.ensure(seed))

    def ensure(self, label):
        def create():
            self.work["frontier_vertex_words_reserved_and_initialized"] += 32
            degree = self.oracle.degree(label)
            assert degree >= 1
            self.work["frontier_original_degree_and_load_arithmetic"] += 6
            return Vertex(
                label, self.vertices.size, degree, F(int(label == self.seed)) - self.lam * degree
            )

        return self.vertices.get_or_create(label, create)

    def check_gate(self, vertex):
        self.work["frontier_load_gate_and_queue_flag_checks"] += 7
        if not vertex.eliminated and not vertex.queued and vertex.load > self.kappa * vertex.degree:
            vertex.queued = True
            if self.queue_tail is None:
                self.queue_head = vertex
            else:
                self.queue_tail.queue_next = vertex
            self.queue_tail = vertex
            self.work["frontier_intrusive_queue_link_operations"] += 6
            self.metrics["queue_insertions"] += 1
        else:
            self.metrics["unsuccessful_or_already_queued_gate_checks"] += 1

    def add_edge(self, a, b, increment, kind):
        assert a is not b and not a.eliminated and not b.eliminated and increment > 0
        if a.index > b.index:
            a, b = b, a
        self.work["frontier_pair_key_arithmetic_and_words"] += 6

        def create():
            self.work["frontier_pair_and_two_incidence_words"] += 20
            self.work["frontier_pair_and_incidence_initialization_links"] += 30
            self.live_edges += 1
            self.metrics["distinct_historical_pairs"] += 1
            self.metrics["maximum_live_pairs"] = max(
                self.metrics["maximum_live_pairs"], self.live_edges
            )
            return Edge(a, b)

        edge = self.edges.get_or_create((a.index, b.index), create)
        assert edge.active
        edge.weight += increment
        self.work["frontier_pair_weight_read_add_write"] += 3
        self.metrics[kind + "_conductance_updates"] += 1

    def unlink(self, edge):
        assert edge.active
        for incidence in [edge.ia, edge.ib]:
            if incidence.previous is None:
                incidence.owner.head = incidence.next
            else:
                incidence.previous.next = incidence.next
            if incidence.next is not None:
                incidence.next.previous = incidence.previous
            incidence.owner.live_degree -= 1
            incidence.previous = incidence.next = None
            self.work["frontier_incidence_unlink_pointer_operations"] += 13
        edge.active = False
        self.live_edges -= 1
        self.work["frontier_pair_retirement_operations"] += 4

    def expose_and_eliminate(self, vertex):
        assert not vertex.eliminated and vertex.load > self.kappa * vertex.degree
        assert self.lam * (self.volume + vertex.degree) < 1
        self.volume += vertex.degree
        self.work["frontier_pre_row_original_volume_guard"] += 7
        if self.gamma:
            self.work["frontier_full_original_row_degree_charged"] += vertex.degree
            self.work["frontier_original_row_buffer_words_and_initialization"] += 2 * vertex.degree
            vertex.original_row = [None] * vertex.degree
            length = 0
            for label in self.oracle.row(vertex.label):
                assert length < vertex.degree
                neighbor = self.ensure(label)
                vertex.original_row[length] = neighbor
                length += 1
                self.work["frontier_original_incidence_record_and_flag_operations"] += 7
                if not neighbor.eliminated:
                    self.add_edge(vertex, neighbor, self.gamma, "original")
            assert length == vertex.degree
        else:
            vertex.original_row = []
            self.work["frontier_zero_coupling_row_skip"] += 2

        count = vertex.live_degree
        self.work["frontier_neighbor_and_lifting_buffers_reserved"] += 7 * count + 4
        neighbors, vertex.coefficients = [None] * count, [None] * count
        incidence = vertex.head
        for j in range(count):
            assert incidence is not None and incidence.edge.active
            neighbors[j] = (incidence.other, incidence.edge.weight, incidence.edge)
            incidence = incidence.next
            self.work["frontier_live_incidence_gather_operations"] += 7
        assert incidence is None and vertex.diagonal > 0
        vertex.pivot = vertex.load / vertex.diagonal
        self.work["frontier_pivot_scalar_operations"] += 4
        for j, (neighbor, weight, _) in enumerate(neighbors):
            vertex.coefficients[j] = (neighbor, weight / vertex.diagonal)
            neighbor.diagonal -= weight * weight / vertex.diagonal
            neighbor.load += weight * vertex.pivot
            assert neighbor.diagonal > 0
            self.work["frontier_diagonal_load_and_lifting_coefficient_updates"] += 13
            self.metrics["positive_load_publications"] += 1
            self.check_gate(neighbor)
        for j in range(count):
            a, wa, _ = neighbors[j]
            for k in range(j + 1, count):
                b, wb, _ = neighbors[k]
                self.work["frontier_fill_pair_loop_and_arithmetic"] += 8
                self.add_edge(a, b, wa * wb / vertex.diagonal, "fill")
        for _, _, edge in neighbors:
            self.unlink(edge)
        assert vertex.head is None and vertex.live_degree == 0
        vertex.eliminated = True
        self.history.append(vertex)
        self.work["frontier_history_vector_growth_and_elimination_fields"] += 10
        self.metrics["pivots"] += 1
        self.metrics["sum_effective_neighbor_counts"] += count
        self.metrics["sum_squared_effective_neighbor_counts_plus_one"] += (count + 1) ** 2
        self.metrics["maximum_effective_pivot_degree"] = max(
            self.metrics["maximum_effective_pivot_degree"], count
        )

    def run(self, validator=None):
        if validator is not None:
            validator(self)
        while self.queue_head is not None:
            vertex = self.queue_head
            self.queue_head = vertex.queue_next
            if self.queue_head is None:
                self.queue_tail = None
            vertex.queue_next, vertex.queued = None, False
            self.work["frontier_queue_pop_and_loop_operations"] += 8
            self.expose_and_eliminate(vertex)
            if validator is not None:
                validator(self)
        for vertex in reversed(self.history):
            vertex.value = vertex.pivot
            self.work["frontier_final_lift_vertex_operations"] += 3
            for neighbor, coefficient in vertex.coefficients:
                vertex.value += coefficient * neighbor.value
                self.work["frontier_final_lift_coefficient_operations"] += 5
            assert vertex.value > 0
        self.work["frontier_output_buffers_and_fields"] += 5 + 8 * len(self.history)
        records = [(vertex.label, vertex.value) for vertex in self.history]
        probabilities = [
            (vertex.label, self.bar * vertex.degree * vertex.value) for vertex in self.history
        ]
        return {"records": records, "probabilities": probabilities, "volume": self.volume}


def audit_map(mapping):
    """Validator-only traversal; never used by the producer."""
    entries = []

    def visit(node):
        if node is None:
            return 0
        left = visit(node.left)
        entries.append((node.key, node.value))
        right = visit(node.right)
        assert node.height == 1 + max(left, right) and abs(left - right) <= 1
        return node.height

    visit(mapping.root)
    assert len(entries) == mapping.size
    assert all(entries[i][0] < entries[i + 1][0] for i in range(len(entries) - 1))
    return entries


def prefix_validator(graph, seed, alpha, epsilon, counts):
    labels = sorted(graph)
    index = {label: i for i, label in enumerate(labels)}
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in labels]
        for i in labels
    ]
    load = [F(int(i == seed)) - epsilon * graph.degree(i) / 2 for i in labels]
    optimum = obstacle(matrix, load)
    counts["validator_original_obstacle_solves"] += 1

    def validate(state):
        vertex_entries = audit_map(state.vertices)
        edge_entries = audit_map(state.edges)
        vertices = {label: vertex for label, vertex in vertex_entries}
        face = [index[vertex.label] for vertex in state.history]
        local = [[matrix[i][j] for j in face] for i in face]
        values = solve(local, [load[i] for i in face])
        assert all(0 < x <= optimum[i] for i, x in zip(face, values))
        assert state.volume == sum(graph.degree(labels[i]) for i in face) < 2 / epsilon
        inverse_columns = [
            solve(local, [F(int(j == k)) for j in range(len(face))]) for k in range(len(face))
        ]
        inverses = [[inverse_columns[j][i] for j in range(len(face))] for i in range(len(face))]
        remaining = [vertex for _, vertex in vertex_entries if not vertex.eliminated]
        for vertex in remaining:
            j = index[vertex.label]
            expected_load = load[j] - sum(matrix[j][i] * x for i, x in zip(face, values))
            expected_diagonal = matrix[j][j] - sum(
                matrix[j][face[a]] * inverses[a][b] * matrix[face[b]][j]
                for a in range(len(face))
                for b in range(len(face))
            )
            assert vertex.load == expected_load and vertex.diagonal == expected_diagonal > 0
        active_pairs = {
            (edge.a.label, edge.b.label): edge for _, edge in edge_entries if edge.active
        }
        for j, left in enumerate(remaining):
            a = index[left.label]
            for right in remaining[j + 1 :]:
                b = index[right.label]
                expected = sum(
                    matrix[a][face[i]] * inverses[i][j] * matrix[face[j]][b]
                    for i in range(len(face))
                    for j in range(len(face))
                )
                key = (
                    (left.label, right.label)
                    if left.index < right.index
                    else (right.label, left.label)
                )
                edge = active_pairs.get(key)
                assert (edge.weight if edge else F(0)) == expected
        for vertex in vertices.values():
            incidence, previous, degree = vertex.head, None, 0
            while incidence is not None:
                assert incidence.owner is vertex and incidence.previous is previous
                assert incidence.edge.active and not incidence.other.eliminated
                previous, incidence = incidence, incidence.next
                degree += 1
            assert degree == vertex.live_degree
            if vertex.eliminated:
                assert degree == 0
        assert state.live_edges == len(active_pairs)
        queued = []
        vertex = state.queue_head
        while vertex is not None:
            assert vertex.queued and not vertex.eliminated and vertex not in queued
            queued.append(vertex)
            vertex = vertex.queue_next
        assert set(queued) == {
            vertex for vertex in remaining if vertex.load > state.kappa * vertex.degree
        }
        assert (state.queue_tail is None) == (not queued)
        assert not queued or state.queue_tail is queued[-1]
        assert state.vertices.size <= 1 + state.volume
        counts["exact_prefix_face_Schur_AVL_queue_and_incidence_checks"] += 1
        counts["validator_dense_face_and_inverse_column_solves"] += 1 + len(face)

    return validate


def check_case(graph, seed, alpha, epsilon, counts, aggregate, prefixes=True):
    work = Counter()
    oracle = LocalRows(graph, work)
    state = ExactFrontier(oracle, seed, alpha, epsilon, work)
    initial = state.vertices.root.value
    if initial.load == state.kappa * initial.degree:
        counts["initial_exact_gate_ties"] += 1
    validator = prefix_validator(graph, seed, alpha, epsilon, counts) if prefixes else None
    result = state.run(validator)
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
    counts["terminal_unadmitted_exact_gate_ties"] += sum(
        vertex.load == state.kappa * vertex.degree
        for _, vertex in audit_map(state.vertices)
        if not vertex.eliminated
    )
    assert state.metrics["original_conductance_updates"] <= sum(graph.degree(i) for i in values)
    assert (
        state.metrics["fill_conductance_updates"]
        == (
            state.metrics["sum_squared_effective_neighbor_counts_plus_one"]
            - 3 * state.metrics["sum_effective_neighbor_counts"]
            - state.metrics["pivots"]
        )
        // 2
    )
    aggregate.update(work)
    counts["original_ACL_output_certificates"] += 1
    counts["original_final_residual_rows"] += len(graph)
    counts["one_time_original_row_queries"] += len(oracle.row_log)
    counts["one_time_original_degree_queries"] += len(oracle.degree_log)
    for key in [
        "pivots",
        "fill_conductance_updates",
        "positive_load_publications",
        "sum_squared_effective_neighbor_counts_plus_one",
    ]:
        counts["implemented_" + key] += state.metrics[key]
    return {
        "vertices": len(graph),
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
    counts, work = Counter(), Counter()
    for graph in nx.graph_atlas_g():
        if len(graph) < 2 or len(graph) > (6 if args.full else 4) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in [F(1), F(1, 3), F(1, 64)]:
                for epsilon in [F(1, 8), F(1, 2), F(2, 3)]:
                    check_case(graph, seed, alpha, epsilon, counts, work)
    profiles = []
    for k in [4, 8, 16, 32, 64] if args.full else [4, 8]:
        graph = nx.path_graph(8 * k + 1)
        for _ in range(k):
            graph.add_edge(0, len(graph))
        profiles.append(
            {
                "family": "star_with_long_tail",
                "leaves": k,
                **check_case(graph, 0, F(1, 3), F(1, 4 * k), counts, work, False),
            }
        )
        profiles.append(
            {
                "family": "cycle",
                **check_case(
                    nx.cycle_graph(2 * k + 1), 0, F(1, 2**32), F(1, 4 * k), counts, work, False
                ),
            }
        )
        profiles.append(
            {
                "family": "path",
                **check_case(
                    nx.path_graph(4 * k + 1), 0, F(1, 2**32), F(1, 2 * k), counts, work, False
                ),
            }
        )
    if args.full:
        for size in [16, 32, 64]:
            profiles.append(
                {
                    "family": "seeded_cubic_regular_graph",
                    "graph_generation_seed": 20260908 + size,
                    **check_case(
                        nx.random_regular_graph(3, size, seed=20260908 + size),
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
        profiles.append({"family": "star_leaf_threshold_ties", **tied})
    for exponent in [8, 80, 256, 1024] if args.full else [8, 80]:
        profiles.append(
            {
                "family": "full_two_vertex",
                **check_case(nx.path_graph(2), 0, F(1, 2**exponent), F(1, 8), counts, work),
            }
        )
    for exponent in [20, 128, 1024]:
        degree = 2**exponent
        oracle = MassiveHub(degree, work)
        state = ExactFrontier(oracle, 0, F(1, 3), F(1, 8), work)
        result = state.run()
        assert result["records"] == [(0, F(15, 16))]
        assert F(1, 2) * F(15, 16) <= F(degree, 8)
        assert state.vertices.size == 2 and state.volume == 1
        counts["private_huge_hub_one_row_certificates"] += 1
    result = {
        "audit": "incremental_active_set_sdd.frontier_exact",
        "scope": "Implemented deterministic AVL/pair-list exact live-frontier producer; dense original face, Schur and obstacle calculations are validators only. Fill-dependent work is not the conjectured general near-linear rate.",
        "parameters": {
            "full": args.full,
            "lambda": "eps_appr/2",
            "kappa": "eps_appr/4",
            "stopping_rule": "No exact unadmitted transformed load exceeds kappa times original degree",
            "arithmetic": "Exact real word model; rational audit does not imply a bit or floating-point bound",
            "random_seed": None,
        },
        "audit_only": dict(counts),
        "charged_work": dict(work),
        "profiles": profiles,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
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
