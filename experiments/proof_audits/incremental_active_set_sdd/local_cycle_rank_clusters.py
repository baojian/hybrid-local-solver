"""Exact local cycle-rank solver audit with a small coupled Schur system.

The insertion tree, permanent row homes and component partition are maintained
from scanned active rows. A cycle birth rebuilds the partition. Application
hierarchies are rebuilt at every checkpoint only as a separately charged
reference driver; the published fast online balancing algorithm is not here.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction as F
import hashlib
import heapq
import json
from pathlib import Path
import subprocess
import time
from types import SimpleNamespace

from cluster_point_queries import audit_index, point_query
from geometric_value_events import obstacle, point, solve
from local_sun_solver import Oracle
from local_unicyclic_clusters import ImplicitPrivateStars, ReferenceHierarchy
import networkx as nx


@dataclass
class Piece:
    ports: tuple
    edges: set = field(default_factory=set)
    vertices: set = field(default_factory=set)

    def append(self, edge):
        assert edge not in self.edges
        self.edges.add(edge)
        self.vertices.update(edge)


class ComponentHierarchy(ReferenceHierarchy):
    def __init__(self, state, pid, minima):
        self.global_state, self.pid = state, pid
        piece = state.pieces[pid]
        parents = {child: parent for parent, child in piece.edges}
        parents[piece.ports[0]] = None
        view = SimpleNamespace(
            builder_counts=state.builder_counts,
            anchor=piece.ports[0],
            depth=state.depth,
            original=state.original,
            gamma=state.gamma,
            shift=state.shift,
            active=piece.vertices,
            parent=parents,
            extra=piece.ports if len(piece.ports) == 2 else None,
            minimum=lambda vertex, ledger: minima[vertex],
        )
        super().__init__(view)

    def edge(self, parent, child, ports):
        rows = []
        for vertex in (parent, child):
            if self.global_state.home[vertex] == (parent, child):
                minimum = self.minimum[vertex]
                if minimum is not None:
                    rows.append((vertex, *minimum))
        return self.adapter.create((parent, child), ports, rows)


class CycleRankState:
    def __init__(self, oracle, seed, alpha, lam, reverse_parent=False):
        self.oracle, self.seed, self.alpha, self.lam = oracle, seed, alpha, lam
        self.gamma, self.bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        self.shift, self.reverse_parent = 1 / self.bar, reverse_parent
        self.active, self.boundary, self.exceptions, self.heaps = set(), {}, set(), {}
        self.parent, self.depth, self.original, self.home = {}, {}, {}, {}
        self.extra, self.admissions, self.pieces, self.home_piece = [], [], {}, {}
        self.q, self.retained = 0, {seed}
        self.counts, self.builder_counts, self.query_counts = Counter(), Counter(), Counter()
        self.callback_counts, self.backend_counts, self.hull_counts = (
            Counter(),
            Counter(),
            Counter(),
        )
        self.history = []

    def minimum(self, parent, ledger):
        heap = self.heaps[parent]
        ledger["heap_minimum_calls"] += 1
        while heap:
            threshold, label = heap[0]
            ledger["heap_live_record_reads"] += 1
            if self.boundary.get(label) == (parent,):
                return threshold, label
            heapq.heappop(heap)
            ledger["lazy_heap_deletions"] += 1
        return None

    def repartition(self):
        """O(active tree size + extra edges) logical work, explicitly charged."""
        assert self.extra
        self.counts["cycle_birth_repartitions"] += 1
        marks = {self.seed}
        for a, b in self.extra:
            marks.update((a, b))
            self.counts["partition_extra_edge_reads"] += 1
        marked_below = {i: i in marks for i in self.admissions}
        kchildren = {i: [] for i in self.admissions}
        kdegree = Counter()
        for child in reversed(self.admissions[1:]):
            self.counts["partition_bottom_up_vertex_reads"] += 1
            parent = self.parent[child]
            if marked_below[child]:
                marked_below[parent] = True
                kchildren[parent].append(child)
                kdegree[parent] += 1
                kdegree[child] += 1
        self.retained = marks | {i for i in kdegree if kdegree[i] >= 3}
        pieces, edge_piece = {}, {}
        for anchor in sorted(self.retained):
            for first in sorted(kchildren[anchor]):
                edges, current, previous = [], first, anchor
                while True:
                    edges.append((previous, current))
                    self.counts["partition_steiner_edge_reads"] += 1
                    if current in self.retained:
                        break
                    assert len(kchildren[current]) == 1
                    previous, current = current, kchildren[current][0]
                pid = len(pieces)
                piece = Piece((anchor, current))
                for edge in edges:
                    piece.append(edge)
                    edge_piece[edge] = pid
                pieces[pid] = piece
        assert len(pieces) == len(self.retained) - 1
        assert len(self.retained) <= 2 * len(marks) - 2
        seed_home = self.home[self.seed]
        seed_piece = edge_piece.get(seed_home)
        if seed_piece is None:
            seed_piece = min(pid for pid, piece in pieces.items() if self.seed in piece.ports)
        home_piece = {self.seed: seed_piece}
        for child in self.admissions[1:]:
            edge = self.home[child]
            self.counts["partition_home_edge_reads"] += 1
            if edge not in edge_piece:
                pid = home_piece[self.parent[child]]
                pieces[pid].append(edge)
                edge_piece[edge] = pid
            home_piece[child] = edge_piece[edge]
        self.pieces, self.home_piece = pieces, home_piece
        self.counts["partition_component_records"] += len(pieces)
        self.counts["partition_edge_records_copied"] += len(self.active) - 1
        self.counts["partition_vertex_copies"] += sum(
            len(piece.vertices) for piece in pieces.values()
        )
        self.counts["partition_home_map_writes"] += len(home_piece)

    def admit(self, vertex):
        parents = self.boundary.pop(vertex) if self.active else ()
        self.exceptions.discard(vertex)
        if self.reverse_parent:
            parents = tuple(reversed(parents))
        closing = len(parents) >= 2
        self.active.add(vertex)
        self.heaps[vertex] = []
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
            edge = (parent, vertex)
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
        changed = {parent} if parent is not None else set()
        seen_active = []
        for neighbor in self.oracle.row(vertex):
            self.counts["active_membership_reads"] += 1
            if neighbor in self.active:
                seen_active.append(neighbor)
                continue
            neighbor_degree = self.oracle.degree(neighbor)
            old = self.boundary.get(neighbor, ())
            self.counts["boundary_record_reads"] += 1
            self.boundary[neighbor] = old + (vertex,)
            # Tuple copying is explicit in this implementation; a resizable
            # incidence list is also possible. The conservative q*V bound pays it.
            self.counts["boundary_tuple_words_copied"] += len(old) + 1
            if old:
                self.q += 1
                self.exceptions.add(neighbor)
                if len(old) == 1:
                    changed.add(old[0])
                    self.counts["exception_births"] += 1
            else:
                heapq.heappush(
                    self.heaps[vertex],
                    (self.lam * neighbor_degree / self.gamma - self.shift, neighbor),
                )
                self.counts["ordinary_heap_insertions"] += 1
        assert set(seen_active) == set(parents)
        self.counts["changed_old_home_payloads"] += len(changed)
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

    def checkpoint(self):
        if len(self.active) == 1:
            value = (1 - self.lam * self.oracle.degree(self.seed)) / self.oracle.degree(self.seed)
            minimum = self.minimum(self.seed, self.counts)
            ordinary = (value - self.shift - minimum[0], minimum[1]) if minimum else None
            return [ordinary] if ordinary else [], [], {self.seed: value}, None
        minima = {i: self.minimum(i, self.builder_counts) for i in self.active}
        records = {}
        for pid in self.pieces:
            builder = ComponentHierarchy(self, pid, minima)
            root = builder.build().summary
            records[pid] = (builder.adapter.backend, root)
            self.callback_counts.update(builder.adapter.counts)
        ports = sorted(self.retained)
        index = {i: k for k, i in enumerate(ports)}
        dim = len(ports)
        matrix, load, multiplicity = [[F(0)] * dim for _ in ports], [F(0)] * dim, Counter()
        self.counts["coarse_matrix_initialized_words"] += dim * dim + dim
        for _, root in records.values():
            for a, i in enumerate(root.ports):
                multiplicity[i] += 1
                load[index[i]] += root.load[a]
                for b, j in enumerate(root.ports):
                    matrix[index[i]][index[j]] += root.matrix[a][b]
                    self.counts["coarse_component_entry_additions"] += 1
        for i, count in multiplicity.items():
            degree, beta = self.original[i]
            matrix[index[i]][index[i]] -= (count - 1) * degree
            load[index[i]] -= (count - 1) * beta
            self.counts["shared_port_duplicate_corrections"] += count - 1
        for i, j in self.extra:
            matrix[index[i]][index[j]] -= self.gamma
            matrix[index[j]][index[i]] -= self.gamma
            load[index[i]] += self.gamma * self.shift
            load[index[j]] += self.gamma * self.shift
            self.counts["restored_extra_edges"] += 1
        values = solve(matrix, load)
        self.counts["coarse_solve_calls"] += 1
        self.counts["coarse_solve_matrix_copy_words"] += dim * (dim + 1)
        self.counts["coarse_elimination_cubic_units"] += dim**3
        self.counts["maximum_coarse_dimension"] = max(self.counts["maximum_coarse_dimension"], dim)
        ordinary, exceptional = [], []
        saved, indices = {}, {}
        for pid, (backend, root) in records.items():
            local_values = tuple(values[index[p]] for p in root.ports)
            saved[pid] = (backend, root, local_values)
            if len(root.ports) == 1:
                candidate = (
                    (local_values[0] - root.threshold[0], root.threshold[1])
                    if root.threshold
                    else None
                )
            else:
                candidate = backend.arena.query(root.hull, local_values)
            if candidate is not None:
                ordinary.append(candidate)
            self.counts["component_reporter_queries"] += 1
            self.backend_counts.update(backend.counts)
            self.hull_counts.update(backend.arena.counts)
        for label in sorted(self.exceptions):
            total = F(0)
            for parent in self.boundary[label]:
                pid = self.home_piece[parent]
                backend, root, local_values = saved[pid]
                if pid not in indices:
                    indices[pid] = audit_index(root, self.builder_counts)
                links, leaves = indices[pid]
                total += (
                    point_query(
                        parent,
                        leaves[parent],
                        lambda node: links[id(node)],
                        root,
                        local_values,
                        self.query_counts,
                    )
                    + self.shift
                )
            gate = self.gamma * total - self.lam * self.oracle.degree(label)
            exceptional.append((gate, label))
            self.counts["exceptional_gate_queries"] += 1
            self.counts["quiet_exceptional_gate_queries"] += gate <= 0
        self.history.append(saved)
        self.counts["historical_root_and_port_words"] += sum(
            3 + len(root.ports) for _, root, _ in saved.values()
        )
        return ordinary, exceptional, None, (saved, ports, matrix, load, values)

    def run(self, validator=None, prefer_exception=False):
        if self.lam * self.oracle.degree(self.seed) >= 1:
            self.counts["trivial_stops"] += 1
            return {}
        self.admit(self.seed)
        while True:
            ordinary, exceptional, singleton, record = self.checkpoint()
            if validator is not None:
                validator(self, ordinary, exceptional, singleton, record)
            choices = exceptional + ordinary if prefer_exception else ordinary + exceptional
            self.counts["candidate_list_words_inspected"] += len(choices)
            chosen = next((item for item in choices if item[0] > 0), None)
            if chosen is None:
                self.counts["final_quiet_certificates"] += 1
                if singleton is not None:
                    self.counts["final_output_words"] += 1
                    return singleton
                out = {}
                for backend, root, local_values in record[0].values():
                    before = backend.counts["recovery_cluster_visits"]
                    for i, value in backend.recover(root, local_values).items():
                        value += self.shift
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
            self.admit(chosen[1])


def independent_schur(matrix, load, active, ports):
    interior = sorted(active - set(ports))
    inner = [[matrix[i][j] for j in interior] for i in interior]
    offset = solve(inner, [load[i] for i in interior])
    responses = [solve(inner, [-matrix[i][p] for i in interior]) for p in ports]
    out = [
        [
            matrix[i][j] + sum(matrix[i][h] * responses[b][k] for k, h in enumerate(interior))
            for b, j in enumerate(ports)
        ]
        for i in ports
    ]
    rhs = [load[i] - sum(matrix[i][h] * offset[k] for k, h in enumerate(interior)) for i in ports]
    return out, rhs


def check_case(graph, seed, alpha, lam, policy, counts):
    n = len(graph)
    gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in range(n)]
        for i in range(n)
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in range(n)]
    optimum, previous, previous_q = obstacle(matrix, load), [F(0)] * n, 0

    def validate(state, ordinary, exceptional, singleton, record):
        nonlocal previous, previous_q
        exact = point(matrix, load, state.active)
        assert all(previous[i] <= exact[i] <= optimum[i] for i in range(n))
        assert all(exact[i] > 0 for i in state.active)
        counts["independent_face_solves"] += 1
        counts["maximum_original_vertex_degree"] = max(
            counts["maximum_original_vertex_degree"], max(dict(graph.degree()).values())
        )
        r = graph.subgraph(state.active).number_of_edges() - len(state.active) + 1
        boundary = {
            j: tuple(i for i in graph[j] if i in state.active)
            for j in graph
            if j not in state.active and any(i in state.active for i in graph[j])
        }
        q = r + sum(len(parents) - 1 for parents in boundary.values())
        assert state.q == q >= previous_q and r == len(state.extra)
        assert sum(len(state.boundary[j]) for j in state.exceptions) <= 2 * q
        assert set(boundary) == set(state.boundary)
        assert all(set(parents) == set(state.boundary[j]) for j, parents in boundary.items())
        assert state.exceptions == {j for j in boundary if len(boundary[j]) >= 2}
        if singleton is None:
            saved, ports, coarse, rhs, values = record
            shifted = [load[i] - sum(matrix[i][j] for j in state.active) / bar for i in range(n)]
            oracle_matrix, oracle_rhs = independent_schur(matrix, shifted, state.active, ports)
            assert coarse == oracle_matrix and rhs == oracle_rhs
            assert all(values[k] + state.shift == exact[p] for k, p in enumerate(ports))
            counts["independent_coarse_schur_comparisons"] += 1
            edge_owners, row_owners, seen = Counter(), Counter(), set()
            for pid, (backend, root, local_values) in saved.items():
                piece = state.pieces[pid]
                assert set(root.ports) == piece.vertices & state.retained
                assert len(piece.edges) + 1 == len(piece.vertices)
                for edge in piece.edges:
                    edge_owners[edge] += 1
                    for i in edge:
                        row_owners[i] += state.home[i] == edge
                recovered = backend.recover(root, local_values)
                assert set(recovered) == piece.vertices
                assert all(value + state.shift == exact[i] for i, value in recovered.items())
                counts["audit_only_component_recoveries"] += 1
                seen.update(recovered)
            assert seen == state.active
            assert all(value == 1 for value in edge_owners.values())
            assert set(edge_owners) == {state.home[i] for i in state.active if i != seed}
            assert all(row_owners[i] == 1 for i in state.active)
            assert sum(len(piece.vertices) for piece in state.pieces.values()) == len(
                state.active
            ) - 1 + len(state.pieces)
            counts["unique_edge_and_row_home_checks"] += len(state.active)
        else:
            assert singleton[seed] == exact[seed]
        exceptional_map = {label: value for value, label in exceptional}
        positive_ordinary = False
        for label, parents in boundary.items():
            gate = gamma * sum(exact[i] for i in parents) - lam * graph.degree(label)
            if len(parents) >= 2:
                assert exceptional_map[label] == gate
            else:
                positive_ordinary |= gate > 0
            counts["independent_original_gate_checks"] += 1
        assert positive_ordinary == any(value > 0 for value, _ in ordinary)
        for value, label in ordinary + exceptional:
            if value > 0:
                assert (
                    gamma * sum(exact[i] for i in boundary[label]) - lam * graph.degree(label) > 0
                )
        previous, previous_q = exact, q

    state = CycleRankState(Oracle(graph), seed, alpha, lam, reverse_parent=policy)
    got = state.run(validate, prefer_exception=policy)
    assert [got.get(i, F(0)) for i in range(n)] == optimum
    volume = sum(graph.degree(i) for i in got)
    assert not got or lam * volume < 1
    assert state.oracle.rows == set(got)
    assert state.oracle.counts["adjacency_entries_inspected"] == volume
    residual = [
        F(i == seed) - sum(matrix[i][j] * got.get(j, F(0)) for j in range(n)) for i in range(n)
    ]
    assert all(0 <= residual[i] <= lam * graph.degree(i) for i in range(n))
    counts["exact_obstacle_acl_comparisons"] += 1
    for saved in state.history[:: max(1, len(state.history) // 3)]:
        for backend, root, local_values in saved.values():
            links, leaves = audit_index(root, counts)
            recovered = backend.recover(root, local_values)
            for i, leaf in leaves.items():
                assert (
                    point_query(i, leaf, lambda node: links[id(node)], root, local_values, counts)
                    == recovered[i]
                )
            counts["retained_component_root_rechecks"] += 1
    return state


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
            for alpha, lam in [(F(1, 3), F(1, 1000)), (F(1, 1009), F(1, 10000))]:
                state = check_case(graph, seed, alpha, lam, True, counts)
                records.append(
                    {
                        "kind": name,
                        "edges": sorted(graph.edges),
                        "seed": seed,
                        "alpha_lazy": str(alpha),
                        "lambda": str(lam),
                        "eps_appr": str(2 * lam),
                        "admission_order": state.admissions,
                        "state_machine_counts": dict(state.counts),
                        "original_graph_access": dict(state.oracle.counts),
                        "audit_only_hierarchy_builder_counts": dict(state.builder_counts),
                    }
                )
        n, alpha, seed = len(graph), F(1, 1009), len(graph) - 1
        bar, gamma = 2 * alpha / (1 + alpha), (1 - alpha) / (1 + alpha)
        lam = bar / (12 * (2 * n) ** n)
        hub_degree = -((-2 / (bar * lam)).__floor__())
        implicit = ImplicitPrivateStars(graph, hub_degree)
        matrix = [
            [F(implicit.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
            for i in graph
        ]
        exact = solve(matrix, [F(i == seed) - lam * implicit.degree(i) for i in graph])
        assert min(exact) > 0
        assert all(gamma * exact[i] < lam * implicit.degree(n + i) for i in graph)
        state = CycleRankState(Oracle(implicit), seed, alpha, lam, reverse_parent=True)
        got = state.run(prefer_exception=True)
        assert [got.get(i, F(0)) for i in graph] == exact
        assert state.oracle.rows == set(graph)
        volume = sum(implicit.degree(i) for i in graph)
        assert state.oracle.counts["adjacency_entries_inspected"] == volume
        counts["implicit_private_star_exact_comparisons"] += 1
        records.append(
            {
                "kind": "implicit finite private stars on " + name,
                "core_edges": sorted(graph.edges),
                "seed": seed,
                "alpha_lazy": str(alpha),
                "lambda": str(lam),
                "eps_appr": str(2 * lam),
                "core_vertices": n,
                "ambient_vertices": n + sum(implicit.degree(n + i) for i in graph),
                "active_volume": volume,
                "admission_order": state.admissions,
                "state_machine_counts": dict(state.counts),
                "original_graph_access": dict(state.oracle.counts),
                "inactive_hub_rows_scanned": 0,
            }
        )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 2 <= args.max_n <= 7:
        parser.error("graph atlas enumeration requires 2 <= max_n <= 7")
    started = time.monotonic()
    counts, operations, query, builders, callbacks, backends, hulls, access = (
        Counter() for _ in range(8)
    )
    parameters = [
        (F(1, 3), F(1, 20)),
        (F(1, 7), F(1, 100)),
        (F(1, 1009), F(1, 100)),
        (F(1, 3), F(1, 4)),
    ]
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= args.max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed in graph:
            for alpha, lam in parameters:
                for policy in [False, True]:
                    state = check_case(graph, seed, alpha, lam, policy, counts)
                    for source, target in [
                        (state.counts, operations),
                        (state.query_counts, query),
                        (state.builder_counts, builders),
                        (state.callback_counts, callbacks),
                        (state.backend_counts, backends),
                        (state.hull_counts, hulls),
                        (state.oracle.counts, access),
                    ]:
                        for key, value in source.items():
                            if key.startswith("maximum_"):
                                target[key] = max(target[key], value)
                            else:
                                target[key] += value
        print(
            json.dumps(
                {
                    "graph_n": len(graph),
                    "edges": len(graph.edges),
                    "cases": counts["exact_obstacle_acl_comparisons"],
                }
            ),
            flush=True,
        )
    structured = structured_cases(counts) if args.structured else []
    result = {
        "audit": "incremental_active_set_sdd.local_cycle_rank_clusters",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all connected simple atlas graphs through max_n",
        "max_n": args.max_n,
        "graph_count": len(graphs),
        "seed": "every vertex",
        "parameters_alpha_lambda": [[str(alpha), str(lam)] for alpha, lam in parameters],
        "eps_appr": "2*lambda",
        "policies": [
            "ordinary gate first and first-discovered spanning parent",
            "exceptional gate first and last-discovered spanning parent",
        ],
        "stopping_rule": "all component ordinary reporters and all exceptional original gates nonpositive; strict positive admissions only",
        "scope": "local state and cycle-birth partition changes implemented; per-checkpoint hierarchy reconstruction and full validation separately charged as reference work; published fast online hierarchy not implemented",
        "state_machine_counts": dict(operations),
        "original_graph_access": dict(access),
        "named_query_counts": dict(query),
        "audit_only_hierarchy_builder_counts": dict(builders),
        "rebuilt_callback_counts": dict(callbacks),
        "rebuilt_backend_counts": dict(backends),
        "rebuilt_hull_counts": dict(hulls),
        "audit_only": dict(counts),
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "cluster_point_queries",
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
