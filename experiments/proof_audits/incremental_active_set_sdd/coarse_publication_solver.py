"""Exact coarse-response producer for geometric ACL value publications.

Only active rows are discovered. Original rows are then cached for charged
geometric delivery. Component reporters find due active values without an
active-value scan, and a monotone ready queue supplies admissions. The
returned ACL point need not be the exact lambda-obstacle optimum.

Application hierarchy rebuilding remains a separately charged reference
driver, not an implementation of the published fast online top-tree source.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import subprocess
import time

from cluster_point_queries import audit_index, point_query
from geometric_value_events import obstacle, point, solve
from local_cycle_rank_clusters import ComponentHierarchy, Piece
from local_sun_solver import Oracle
from local_unicyclic_clusters import ImplicitPrivateStars
from maintained_coarse_inverse import InverseState, certificate
import networkx as nx


class ParentBuffer:
    """Geometric capacity growth, with all allocation/copy/append words paid."""

    def __init__(self, counts):
        self.data, self.size, self.counts = [], 0, counts
        counts["parent_buffer_records"] += 1

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        assert 0 <= index < self.size
        self.counts["parent_buffer_reads"] += 1
        return self.data[index]

    def __iter__(self):
        for index in range(self.size):
            yield self[index]

    def append(self, vertex):
        if self.size == len(self.data):
            capacity = max(1, 2 * len(self.data))
            grown = [None] * capacity
            self.counts["parent_buffer_zero_initializations"] += capacity
            for i in range(self.size):
                grown[i] = self.data[i]
            self.counts["parent_buffer_growth_copy_words"] += self.size
            self.counts["parent_buffer_growth_read_words"] += self.size
            self.data = grown
        self.data[self.size] = vertex
        self.size += 1
        self.counts["parent_buffer_append_writes"] += 1


class PublicationState(InverseState):
    def __init__(self, oracle, seed, alpha, epsilon, reverse_policy=False):
        assert 0 < alpha < 1 and 0 < epsilon < 1
        super().__init__(oracle, seed, alpha, epsilon / 2, reverse_parent=reverse_policy)
        self.epsilon, self.eta = epsilon, F(5, 4)
        self.h, self.theta = epsilon / (16 * self.gamma), 11 * epsilon / 20
        self.ell, self.lower, self.cached = {}, {}, {}
        self.ready, self.queued = deque(), set()
        self.publication_counts, self.publications_by_vertex = Counter(), Counter()
        self.audit_snapshots = []

    def _admit_metadata(self, vertex):
        """No ordinary boundary heaps or per-checkpoint exceptional scans."""
        if self.active:
            buffer = self.boundary.pop(vertex)
            parents = list(buffer)
            self.publication_counts["admitted_parent_copy_words"] += len(parents)
            if self.reverse_parent:
                parents.reverse()
                self.publication_counts["admitted_parent_reverse_words"] += len(parents)
            assert self.lower.pop(vertex) > self.theta * self.oracle.degree(vertex)
            self.queued.remove(vertex)
            self.publication_counts["admitted_candidate_record_deletions"] += 3
        else:
            parents = []
        self.exceptions.discard(vertex)
        closing = len(parents) >= 2
        self.active.add(vertex)
        self.ell[vertex] = F(0)
        degree = self.oracle.degree(vertex)
        self.original[vertex] = (
            F(degree),
            F(vertex == self.seed) - self.lam * degree - self.shift * degree,
        )
        parent = parents[0] if parents else None
        self.parent[vertex], self.depth[vertex] = parent, self.depth[parent] + 1 if parents else 0
        if parent is None:
            self.pieces[0] = Piece((self.seed,), vertices={self.seed})
            self.home_piece[self.seed] = 0
        else:
            edge = parent, vertex
            self.home[vertex] = edge
            if len(self.active) == 2:
                self.home[self.seed] = edge
            pid = self.home_piece[parent]
            self.home_piece[vertex] = pid
            self.pieces[pid].append(edge)
            self.counts["ordinary_component_edge_appends"] += not closing
        self.extra.extend((old, vertex) for old in parents[1:])
        self.counts["new_extra_edge_records"] += max(0, len(parents) - 1)
        self.counts["multi_cycle_births"] += len(parents) >= 3
        self.counts["maximum_admitted_parent_count"] = max(
            self.counts["maximum_admitted_parent_count"], len(parents)
        )
        neighbors = self.oracle.row(vertex)
        self.cached[vertex] = neighbors
        self.publication_counts["cached_original_row_words"] += len(neighbors)
        seen_active = []
        for neighbor in neighbors:
            self.counts["active_membership_reads"] += 1
            if neighbor in self.active:
                seen_active.append(neighbor)
                continue
            self.oracle.degree(neighbor)
            old = self.boundary.get(neighbor)
            self.counts["boundary_record_reads"] += 1
            if old is None:
                old = ParentBuffer(self.publication_counts)
                self.boundary[neighbor] = old
                self.lower[neighbor] = F(0)
                self.publication_counts["first_discovered_signal_records"] += 1
            else:
                self.q += 1
                self.exceptions.add(neighbor)
                self.counts["exception_births"] += len(old) == 1
            old.append(vertex)
        assert set(seen_active) == set(parents)
        self.publication_counts["active_parent_consistency_words"] += len(seen_active) + len(
            parents
        )
        self.admissions.append(vertex)
        if closing:
            self.repartition()
        self.counts["admissions"] += 1
        self.counts["maximum_exposed_cycle_rank"] = max(
            self.counts["maximum_exposed_cycle_rank"], self.q
        )
        self.counts["maximum_active_cycle_rank"] = max(
            self.counts["maximum_active_cycle_rank"], len(self.extra)
        )
        self.counts["maximum_exceptional_candidates"] = max(
            self.counts["maximum_exceptional_candidates"], len(self.exceptions)
        )

    def producer_checkpoint(self):
        self.indices = {}
        self.publication_counts["producer_searches"] += 1
        if len(self.active) == 1:
            value = self.means[0]
            return (
                [(value - self.eta * self.ell[self.seed] - self.h, self.seed)],
                {self.seed: value},
                None,
            )
        # Reference-only whole-hierarchy rebuild, not a physical-value scan.
        minima = {i: (self.eta * self.ell[i] + self.h - self.shift, i) for i in self.active}
        self.builder_counts["reference_publication_payload_reads"] += len(minima)
        self.current = {}
        candidates = []
        for pid in self.pieces:
            builder = ComponentHierarchy(self, pid, minima)
            root = builder.build().summary
            backend = builder.adapter.backend
            values = tuple(self.means[self.port_index[p]] - self.shift for p in root.ports)
            self.current[pid] = backend, root, values
            self.callback_counts.update(builder.adapter.counts)
            if len(root.ports) == 1:
                assert root.threshold is not None
                candidate = values[0] - root.threshold[0], root.threshold[1]
            else:
                candidate = backend.arena.query(root.hull, values)
            assert candidate is not None
            candidates.append(candidate)
            self.publication_counts["component_publication_queries"] += 1
            self.publication_counts["current_component_port_words_written"] += len(values)
            self.backend_counts.update(backend.counts)
            self.hull_counts.update(backend.arena.counts)
        return (
            candidates,
            None,
            (self.current, self.ports, None, None, [u - self.shift for u in self.means]),
        )

    def publish(self, vertex, value):
        previous = self.ell[vertex]
        assert value > self.eta * previous + self.h
        assert value <= 1 / (self.bar * self.oracle.degree(vertex))
        delta = value - previous
        self.ell[vertex] = value
        self.publication_counts["publications"] += 1
        self.publications_by_vertex[vertex] += 1
        self.publication_counts["home_edge_payload_changes"] += len(self.active) > 1
        for neighbor in self.cached[vertex]:
            self.publication_counts["cached_delivery_incidence_reads"] += 1
            self.publication_counts["delivery_active_flag_reads"] += 1
            if neighbor in self.active:
                self.publication_counts["delivery_skips_to_active_vertices"] += 1
                continue
            self.lower[neighbor] += self.gamma * delta
            self.publication_counts["lower_signal_read_modify_writes"] += 1
            self.publication_counts["ready_threshold_checks"] += 1
            if self.lower[neighbor] > self.theta * self.oracle.degree(neighbor):
                self.publication_counts["ready_flag_reads"] += 1
                if neighbor not in self.queued:
                    self.queued.add(neighbor)
                    self.ready.append(neighbor)
                    self.publication_counts["ready_queue_insertions"] += 1
        # No inverse or mean writes occur during a publication.

    def run(self, validator=None):
        if self.lam * self.oracle.degree(self.seed) >= 1:
            self.counts["trivial_stops"] += 1
            return {}
        self.admit(self.seed)
        while True:
            candidates, singleton, record = self.producer_checkpoint()
            if validator is not None:
                validator(self, candidates, singleton, record)
            self.publication_counts["candidate_rows_inspected"] += len(candidates)
            due = next((item for item in candidates if item[0] > 0), None)
            if due is not None:
                vertex = due[1]
                value = self.response(vertex, self.home_piece, False)[2]
                self.publish(vertex, value)
                continue
            self.publication_counts["producer_quiet_certificates"] += 1
            self.publication_counts["ready_queue_empty_checks"] += 1
            if not self.ready:
                self.publication_counts["terminal_acl_certificates"] += 1
                if singleton is not None:
                    self.counts["final_output_words"] += 1
                    return singleton
                out = {}
                for backend, root, values in record[0].values():
                    before = backend.counts["recovery_cluster_visits"]
                    for i, w in backend.recover(root, values).items():
                        value = w + self.shift
                        if i in out:
                            assert out[i] == value
                            self.counts["final_shared_coordinate_checks"] += 1
                        else:
                            out[i] = value
                    self.counts["final_recovery_record_visits"] += (
                        backend.counts["recovery_cluster_visits"] - before
                    )
                self.counts["final_output_words"] += len(out)
                return out
            vertex = self.ready.pop() if self.reverse_parent else self.ready.popleft()
            self.publication_counts["ready_queue_deletions"] += 1
            assert vertex in self.queued and self.lower[vertex] > self.theta * self.oracle.degree(
                vertex
            )
            self.admit(vertex)


def boundary_view(state):
    """Reference reads bypass the algorithm's charged ParentBuffer iterator."""
    return {j: tuple(buffer.data[: buffer.size]) for j, buffer in state.boundary.items()}


def make_validator(matrix, load, optimum, expected_boundary, degree, counts):
    previous = [F(0)] * len(matrix)
    face, inverse, means, last_size, previous_q = None, None, None, 0, 0

    def validate(state, candidates, singleton, record):
        nonlocal previous, face, inverse, means, last_size, previous_q
        if len(state.active) != last_size:
            face = point(matrix, load, state.active)
            assert all(previous[i] <= face[i] <= optimum[i] for i in range(len(matrix)))
            assert all(face[i] > 0 for i in state.active)
            certificate(state, matrix, load, face, record, counts)
            inverse, means = tuple(tuple(row) for row in state.inverse), tuple(state.means)
            previous, last_size = face, len(state.active)
            counts["independent_admission_face_solves"] += 1
            if record is not None:
                if len(state.audit_snapshots) < 3:
                    state.audit_snapshots.append(record[0])
                else:
                    state.audit_snapshots[-1] = record[0]
                counts["audit_snapshot_root_and_port_words"] += sum(
                    3 + len(root.ports) for _, root, _ in record[0].values()
                )
        else:
            assert tuple(tuple(row) for row in state.inverse) == inverse
            assert tuple(state.means) == means
            counts["publication_only_inverse_unchanged_checks"] += 1
        assert all(0 <= state.ell[i] <= face[i] for i in state.active)
        due = {i for i in state.active if face[i] > state.eta * state.ell[i] + state.h}
        assert bool(due) == any(value > 0 for value, _ in candidates)
        assert all(label in due for value, label in candidates if value > 0)
        counts["independent_publication_due_signs"] += len(state.active)
        counts["independent_producer_quiet_checks"] += not due
        boundary = expected_boundary(state.active)
        actual = boundary_view(state)
        assert set(boundary) == set(actual)
        assert all(set(actual[j]) == set(parents) for j, parents in boundary.items())
        assert state.exceptions == {j for j in boundary if len(boundary[j]) >= 2}
        r = (
            sum(matrix[i][j] != 0 for i in state.active for j in state.active if i < j)
            - len(state.active)
            + 1
        )
        assert r == len(state.extra)
        q = r + sum(len(parents) - 1 for parents in boundary.values())
        assert state.q == q >= previous_q
        previous_q = q
        signals = {
            j: state.gamma * sum(state.ell[i] for i in parents) for j, parents in boundary.items()
        }
        assert signals == state.lower
        assert state.queued == {j for j in signals if signals[j] > state.theta * degree(j)}
        assert len(state.ready) == len(state.queued) and set(state.ready) == state.queued
        counts["independent_lower_signal_checks"] += len(signals)
        for j, parents in boundary.items():
            residual = state.gamma * sum(face[i] for i in parents)
            assert signals[j] <= residual
            if not due:
                assert residual <= state.eta * signals[j] + state.gamma * state.h * degree(j)
            counts["independent_original_boundary_bounds"] += 1
        if singleton is not None:
            assert singleton[state.seed] == face[state.seed]

    return validate


def check_final(state, got, matrix, load, optimum, boundary, degree, counts):
    n = len(matrix)
    exact = point(matrix, load, state.active) if state.active else [F(0)] * n
    assert [got.get(i, F(0)) for i in range(n)] == exact
    assert all(exact[i] <= optimum[i] for i in range(n))
    assert set(got) == state.active == state.oracle.rows
    volume = sum(degree(i) for i in got)
    assert not got or state.lam * volume < 1
    assert state.oracle.counts["adjacency_entries_inspected"] == volume
    residual = [
        F(i == state.seed) - sum(matrix[i][j] * got.get(j, F(0)) for j in range(n))
        for i in range(n)
    ]
    for i in range(n):
        assert 0 <= residual[i] <= state.epsilon * degree(i)
        if i in got:
            assert residual[i] == state.lam * degree(i)
        elif got:
            assert residual[i] <= 3 * state.epsilon * degree(i) / 4
    for j, parents in boundary(state.active).items():
        residual_j = state.gamma * sum(got[i] for i in parents)
        assert 0 <= residual_j <= 3 * state.epsilon * degree(j) / 4
        counts["terminal_original_exterior_acl_checks"] += 1
    assert state.publication_counts["cached_delivery_incidence_reads"] == sum(
        degree(i) * count for i, count in state.publications_by_vertex.items()
    )
    assert (
        state.publication_counts["parent_buffer_growth_copy_words"]
        <= 2 * state.publication_counts["parent_buffer_append_writes"]
    )
    assert (
        state.publication_counts["parent_buffer_zero_initializations"]
        <= 4 * state.publication_counts["parent_buffer_append_writes"]
    )
    assert state.counts["exceptional_gate_queries"] == 0
    assert state.counts["coarse_solve_calls"] == 0
    assert not state.history
    if got:
        assert state.publication_counts["producer_quiet_certificates"] == len(got)
        assert state.publication_counts["producer_searches"] == state.publication_counts[
            "publications"
        ] + len(got)
    for i, count in state.publications_by_vertex.items():
        # A count-only geometric lower bound, independent of the event loop.
        assert state.h * state.eta ** (count - 1) < 1 / (state.bar * degree(i))
        counts["independent_geometric_count_bounds"] += 1
    counts["exact_face_acl_comparisons"] += 1
    if exact != optimum:
        counts["terminal_points_before_obstacle_optimum"] += 1
    for saved in state.audit_snapshots:
        for backend, root, values in saved.values():
            links, leaves = audit_index(root, counts)
            recovered = backend.recover(root, values)
            for i, leaf in leaves.items():
                assert (
                    point_query(i, leaf, lambda node: links[id(node)], root, values, counts)
                    == recovered[i]
                )
            counts["old_publication_payload_rechecks"] += 1
    return exact, residual


def check_case(graph, seed, alpha, epsilon, policy, counts):
    gamma, lam = (1 - alpha) / (1 + alpha), epsilon / 2
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in graph]
    optimum = obstacle(matrix, load)

    def boundary(active):
        return {
            j: tuple(i for i in graph[j] if i in active)
            for j in graph
            if j not in active and any(i in active for i in graph[j])
        }

    state = PublicationState(Oracle(graph), seed, alpha, epsilon, reverse_policy=policy)
    validate = make_validator(matrix, load, optimum, boundary, graph.degree, counts)
    got = state.run(validate)
    exact, residual = check_final(state, got, matrix, load, optimum, boundary, graph.degree, counts)
    state.audit_early_witness = None
    if exact != optimum:
        state.audit_early_witness = {
            "edges": sorted(graph.edges),
            "seed": seed,
            "alpha_lazy": str(alpha),
            "eps_appr": str(epsilon),
            "policy_reversed": policy,
            "admission_order": state.admissions,
            "physical_output": [str(x) for x in exact],
            "exact_lambda_obstacle": [str(x) for x in optimum],
            "original_residual": [str(x) for x in residual],
            "degrees": [graph.degree(i) for i in graph],
        }
    return state


def state_record(state):
    return {
        "seed": state.seed,
        "alpha_lazy": str(state.alpha),
        "eps_appr": str(state.epsilon),
        "lambda": str(state.lam),
        "h": str(state.h),
        "theta": str(state.theta),
        "admission_order": state.admissions,
        "active_cycle_rank": len(state.extra),
        "revealed_cycle_rank": state.q,
        "final_ports": state.ports,
        "state_machine_counts": dict(state.counts),
        "publication_counts": dict(state.publication_counts),
        "publications_by_vertex": dict(state.publications_by_vertex),
        "inverse_update_counts": dict(state.inverse_counts),
        "green_query_counts": dict(state.green_counts),
        "original_graph_access": dict(state.oracle.counts),
        "audit_only_hierarchy_builder_counts": dict(state.builder_counts),
    }


class SharedPairStar:
    """A finite star with pair-sharing hubs and unmaterialized private leaves."""

    def __init__(self, k, degree):
        self.k, self.hub_degree = k, degree
        self.pairs = dict(enumerate(itertools.combinations(range(1, k + 1), 2), k + 1))
        self.incident = {i: [] for i in range(1, k + 1)}
        for hub, pair in self.pairs.items():
            for i in pair:
                self.incident[i].append(hub)

    def degree(self, i):
        return self.k if i <= self.k else self.hub_degree

    def __getitem__(self, i):
        assert 0 <= i <= self.k, "An inactive shared hub row must never be scanned"
        return list(range(1, self.k + 1)) if i == 0 else [0] + self.incident[i]

    def boundary(self, active):
        out = {i: (0,) for i in range(1, self.k + 1) if i not in active} if 0 in active else {}
        out.update(
            {
                j: tuple(i for i in pair if i in active)
                for j, pair in self.pairs.items()
                if any(i in active for i in pair)
            }
        )
        return out


def shared_pair_star_cases(counts, maximum):
    records = []
    for k in [value for value in [2, 3, 4, 8, 16, 32] if value <= maximum]:
        for alpha in [F(1, 3), F(1, 1009)]:
            gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
            lam = gamma / (4 * k * (k + gamma))
            hub_degree = -((-4 / (bar * lam)).__floor__())
            graph = SharedPairStar(k, hub_degree)
            matrix = [
                [F(k) if i == j else -gamma if i == 0 or j == 0 else F(0) for j in range(k + 1)]
                for i in range(k + 1)
            ]
            load = [F(i == 0) - lam * k for i in range(k + 1)]
            optimum = [(1 - lam * k * (1 + gamma)) / (k - gamma * gamma)] + [
                3 * gamma / (4 * k * (k - gamma * gamma))
            ] * k
            assert solve(matrix, load) == optimum and min(optimum) > 0
            assert 2 * gamma * optimum[1] < lam * hub_degree
            for policy in [False, True]:
                state = PublicationState(Oracle(graph), 0, alpha, 2 * lam, reverse_policy=policy)
                validate = make_validator(
                    matrix, load, optimum, graph.boundary, graph.degree, counts
                )
                got = state.run(validate)
                check_final(state, got, matrix, load, optimum, graph.boundary, graph.degree, counts)
                assert [got.get(i, F(0)) for i in range(k + 1)] == optimum
                assert state.q == comb(k, 2) and not state.extra and state.ports == [0]
                assert state.oracle.counts["adjacency_entries_inspected"] == k * (k + 1)
                assert state.publication_counts["ready_queue_insertions"] == k
                assert state.counts["exceptional_gate_queries"] == 0
                # Same source-valid graph and lambda, with the previous direct gate checker.
                direct = InverseState(Oracle(graph), 0, alpha, lam, reverse_parent=policy)
                direct_got = direct.run(prefer_exception=policy)
                assert direct_got == got
                assert direct.counts["exceptional_gate_queries"] == comb(k + 1, 3)
                counts["shared_pair_star_comparisons"] += 1
                records.append(
                    {
                        "kind": "implicit star with pair-sharing inactive hubs",
                        "k": k,
                        "hub_degree": hub_degree,
                        "hub_count": comb(k, 2),
                        "ambient_vertices": (k + 1) + comb(k, 2) * (hub_degree - 1),
                        "active_volume": k * (k + 1),
                        "charged_volume": (k + 1) ** 2,
                        "inactive_hub_rows_scanned": 0,
                        "previous_direct_exceptional_gate_queries": direct.counts[
                            "exceptional_gate_queries"
                        ],
                        "previous_direct_named_response_queries": direct.green_counts[
                            "response_queries"
                        ],
                        **state_record(state),
                    }
                )
    return records


def structured_cases(counts):
    families = []
    graph = nx.path_graph(18)
    graph.add_edges_from([(2, 5), (8, 11), (13, 16)])
    families.append(("separated cycles and a long path", graph))
    graph = nx.balanced_tree(2, 3)
    graph.add_edges_from([(7, 8), (9, 10), (11, 12), (13, 14)])
    families.append(("four cycles on branched attachments", graph))
    graph = nx.path_graph(14)
    graph.add_edges_from([(1, 5), (1, 8), (5, 8), (4, 10)])
    families.append(("overlapping cycles with shared endpoints", graph))
    graph = nx.complete_bipartite_graph(3, 5)
    graph.add_edges_from((i, i + 8) for i in range(8))
    families.append(("many simultaneous shared candidates", graph))
    graph = nx.complete_graph(7)
    graph.add_edges_from((i, i + 7) for i in range(7))
    families.append(("dense core with pendant leaves", graph))
    records = []
    for name, graph in families:
        for seed in sorted({0, len(graph) - 1}):
            for alpha, epsilon in [(F(1, 3), F(1, 500)), (F(1, 1009), F(1, 5000))]:
                state = check_case(graph, seed, alpha, epsilon, True, counts)
                records.append({"kind": name, "edges": sorted(graph.edges), **state_record(state)})
        n, alpha, seed = len(graph), F(1, 1009), len(graph) - 1
        bar, gamma = 2 * alpha / (1 + alpha), (1 - alpha) / (1 + alpha)
        lam = bar / (12 * (2 * n) ** n)
        hub_degree = -((-2 / (bar * lam)).__floor__())
        implicit = ImplicitPrivateStars(graph, hub_degree)
        matrix = [
            [F(implicit.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
            for i in graph
        ]
        load = [F(i == seed) - lam * implicit.degree(i) for i in graph]
        optimum = solve(matrix, load)
        assert min(optimum) > 0
        assert all(gamma * optimum[i] < lam * implicit.degree(n + i) for i in graph)

        def boundary(active):
            out = {
                j: tuple(i for i in graph[j] if i in active)
                for j in graph
                if j not in active and any(i in active for i in graph[j])
            }
            out.update({n + i: (i,) for i in active})
            return out

        state = PublicationState(Oracle(implicit), seed, alpha, 2 * lam, reverse_policy=True)
        validate = make_validator(matrix, load, optimum, boundary, implicit.degree, counts)
        got = state.run(validate)
        check_final(state, got, matrix, load, optimum, boundary, implicit.degree, counts)
        counts["implicit_private_star_comparisons"] += 1
        records.append(
            {
                "kind": "implicit private stars on " + name,
                "core_edges": sorted(graph.edges),
                "core_vertices": n,
                "ambient_vertices": n + sum(implicit.degree(n + i) for i in graph),
                "active_volume": sum(implicit.degree(i) for i in got),
                "inactive_hub_rows_scanned": 0,
                **state_record(state),
            }
        )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--shared-star-max", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 2 <= args.max_n <= 7:
        parser.error("graph atlas enumeration requires 2 <= max_n <= 7")
    started = time.monotonic()
    counts, ledgers = (
        Counter(),
        {
            name: Counter()
            for name in [
                "counts",
                "publication_counts",
                "inverse_counts",
                "green_counts",
                "builder_counts",
                "callback_counts",
                "backend_counts",
                "hull_counts",
            ]
        },
    )
    access, early = Counter(), None
    parameters = [
        (F(1, 3), F(1, 10)),
        (F(1, 7), F(1, 50)),
        (F(1, 1009), F(1, 50)),
        (F(1, 3), F(1, 2)),
    ]
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= args.max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed in graph:
            for alpha, epsilon in parameters:
                for policy in [False, True]:
                    state = check_case(graph, seed, alpha, epsilon, policy, counts)
                    early = early or state.audit_early_witness
                    for name, target in ledgers.items():
                        for key, value in getattr(state, name).items():
                            target[key] = (
                                max(target[key], value)
                                if key.startswith("maximum_")
                                else target[key] + value
                            )
                    access.update(state.oracle.counts)
        print(
            json.dumps(
                {
                    "graph_n": len(graph),
                    "edges": len(graph.edges),
                    "cases": counts["exact_face_acl_comparisons"],
                }
            ),
            flush=True,
        )
    structured = structured_cases(counts) if args.structured else []
    shared = shared_pair_star_cases(counts, args.shared_star_max)
    result = {
        "audit": "incremental_active_set_sdd.coarse_publication_solver",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all connected simple atlas graphs through max_n",
        "max_n": args.max_n,
        "graph_count": len(graphs),
        "seed": "every vertex",
        "parameters_alpha_epsilon": [[str(a), str(eps)] for a, eps in parameters],
        "constants": {
            "lambda": "eps_appr/2",
            "h": "eps_appr/(16*gamma)",
            "eta": "5/4",
            "theta": "11*eps_appr/20",
        },
        "policies": [
            "FIFO readiness queue, first-discovered spanning parent",
            "LIFO readiness queue, last-discovered spanning parent",
        ],
        "stopping_rule": "component producer quiet at every active coordinate and monotone ready queue empty",
        "accuracy_scope": "Original ACL residual, not exact lambda-obstacle or RPPR objective accuracy; the published trace can stop before the obstacle optimum.",
        "implementation_scope": "Complete publication/admission state machine, cached incidence delivery and paid parent buffers. Current inverse updated only on admissions. Per-search hierarchy rebuilds and whole-hierarchy parent indices are reference-only; the published fast online balancing source is not implemented.",
        "history_scope": "Only current roots, port values and dense inverse in the algorithm; at most three extra root/value snapshots in the separate validator; immutable source application histories may be retained under the theorem's explicit ledger.",
        "atlas_ledgers": {name: dict(value) for name, value in ledgers.items()},
        "original_graph_access": dict(access),
        "audit_only": dict(counts),
        "early_stop_witness": early,
        "structured_cases": structured,
        "shared_pair_star_cases": shared,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "maintained_coarse_inverse",
                "cluster_green_queries",
                "cluster_point_queries",
                "local_cycle_rank_clusters",
                "local_unicyclic_clusters",
                "shifted_tree_clusters",
                "top_tree_callback_adapter",
                "path_cluster_reporter",
                "projective_hull_rope",
                "local_sun_solver",
            ]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
