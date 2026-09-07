"""Exact local coarse inverse updates with conditional Green port promotion.

Admission decisions use a maintained inverse and physical port values; no
coarse factorization is used by the algorithm. Component hierarchy rebuilding
and parent-index construction remain explicitly separate reference work, as
in local_cycle_rank_clusters. Full original Schur matrices certify J*K=I only
inside the validator and cannot affect admissions.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

from cluster_green_queries import conditional_cross, response_trace
from cluster_point_queries import audit_index, point_query
from geometric_value_events import obstacle, point, solve
from local_cycle_rank_clusters import ComponentHierarchy, CycleRankState, independent_schur
from local_sun_solver import Oracle
from local_unicyclic_clusters import ImplicitPrivateStars
import networkx as nx


class InverseState(CycleRankState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports, self.port_index, self.inverse, self.means = [], {}, [], []
        self.current, self.indices = {}, {}
        self.inverse_counts, self.green_counts = Counter(), Counter()
        # The only dense inverse is current; historical roots store port means only.

    def entry(self, matrix, i, j):
        self.inverse_counts["inverse_entry_reads"] += 1
        return matrix[i][j]

    def allocate(self, n):
        self.inverse_counts["inverse_zero_initializations"] += n * n
        return [[F(0)] * n for _ in range(n)]

    def put(self, matrix, i, j, value):
        matrix[i][j] = value
        self.inverse_counts["inverse_entry_writes"] += 1

    def response(self, vertex, old_homes, keep_trace):
        """Query one old current version, with at most two coarse coefficients."""
        if vertex in self.port_index:
            k = self.port_index[vertex]
            self.inverse_counts["direct_retained_mean_reads"] += 1
            return {k: F(1)}, F(0), self.means[k], None, None
        pid = old_homes[vertex]
        backend, root, values = self.current[pid]
        if pid not in self.indices:
            self.indices[pid] = audit_index(root, self.builder_counts)
        links, leaves = self.indices[pid]
        response = response_trace(
            vertex,
            leaves[vertex],
            lambda node: links[id(node)],
            root,
            backend,
            self.green_counts,
            keep_trace=keep_trace,
        )
        row = {self.port_index[p]: c for p, c in zip(root.ports, response.row[:-1]) if c}
        value = response.row[-1] + sum(c * values[k] for k, c in enumerate(response.row[:-1]))
        self.inverse_counts["physical_response_evaluations"] += 1
        return row, response.variance, value + self.shift, response, pid

    def rank_one(self, matrix, z, delta):
        n = len(matrix)
        out = self.allocate(n)
        scale = self.gamma * self.gamma / delta
        for i in range(n):
            for j in range(n):
                self.put(out, i, j, self.entry(matrix, i, j) + scale * z[i] * z[j])
                self.inverse_counts["rank_one_entry_arithmetic"] += 3
        self.inverse_counts["rank_one_updates"] += 1
        return out

    def admit(self, vertex):
        degree = self.oracle.degree(vertex)
        if not self.active:
            assert vertex == self.seed
            self.ports, self.port_index = [vertex], {vertex: 0}
            self.inverse = self.allocate(1)
            self.put(self.inverse, 0, 0, F(1, degree))
            self.means = [(1 - self.lam * degree) / degree]
            super().admit(vertex)
            return
        parents = self.boundary[vertex]
        if len(parents) == 1:
            row, variance, value, _, _ = self.response(parents[0], self.home_piece, False)
            z = [
                sum(self.entry(self.inverse, i, k) * c for k, c in row.items())
                for i in range(len(self.ports))
            ]
            full_variance = variance + sum(c * z[k] for k, c in row.items())
            delta = degree - self.gamma * self.gamma * full_variance
            gate = self.gamma * value - self.lam * degree
            assert gate > 0 and delta >= self.bar * degree
            new_value = gate / delta
            self.inverse = self.rank_one(self.inverse, z, delta)
            self.means = [
                value + self.gamma * z[i] * new_value for i, value in enumerate(self.means)
            ]
            self.inverse_counts["ordinary_inverse_updates"] += 1
            self.inverse_counts["vector_read_write_arithmetic_units"] += 12 * len(z) + 12
            super().admit(vertex)
        else:
            # New metadata may be computed, but these old roots, homes, J and
            # means stay intact until all promoted responses have been read.
            old_homes = dict(self.home_piece)
            self.inverse_counts["cycle_birth_home_map_copy_words"] += 2 * len(old_homes)
            old_ports = self.ports
            old_retained = set(old_ports)
            self.inverse_counts["cycle_birth_port_set_copy_words"] += len(old_ports)
            super().admit(vertex)
            assert old_retained <= self.retained and vertex in self.retained
            promoted = sorted(
                (self.retained - old_retained - {vertex}) | (set(parents) - old_retained)
            )
            transient = set(promoted) - self.retained
            assert len(transient) <= 1 and transient <= {self.parent[vertex]}
            responses = {i: self.response(i, old_homes, True) for i in promoted}
            ports = old_ports + promoted
            p, n = len(old_ports), len(ports)
            index = {i: k for k, i in enumerate(ports)}
            augmented = self.allocate(n)
            for a in range(p):
                for b in range(p):
                    self.put(augmented, a, b, self.entry(self.inverse, a, b))
            for a, i in enumerate(promoted, p):
                row_i, var_i, _, trace_i, pid_i = responses[i]
                for b in range(p):
                    value = sum(c * self.entry(self.inverse, k, b) for k, c in row_i.items())
                    self.put(augmented, a, b, value)
                    self.put(augmented, b, a, value)
                for b, j in enumerate(promoted, p):
                    row_j, _, _, trace_j, pid_j = responses[j]
                    conditional = (
                        var_i
                        if i == j
                        else (
                            conditional_cross(trace_i, trace_j, self.green_counts)
                            if pid_i == pid_j
                            else F(0)
                        )
                    )
                    value = conditional + sum(
                        ci * self.entry(self.inverse, ki, kj) * cj
                        for ki, ci in row_i.items()
                        for kj, cj in row_j.items()
                    )
                    self.put(augmented, a, b, value)
                    self.inverse_counts["promoted_pair_queries"] += 1
            means = self.means + [responses[i][2] for i in promoted]
            z = [sum(self.entry(augmented, a, index[i]) for i in parents) for a in range(n)]
            delta = degree - self.gamma * self.gamma * sum(z[index[i]] for i in parents)
            gate = self.gamma * sum(means[index[i]] for i in parents) - self.lam * degree
            assert gate > 0 and delta >= self.bar * degree
            new_value = gate / delta
            # Allocate the border directly: no hidden matrix copies or full inverse history.
            bordered = self.allocate(n + 1)
            scale = self.gamma * self.gamma / delta
            for a in range(n):
                for b in range(n):
                    self.put(bordered, a, b, self.entry(augmented, a, b) + scale * z[a] * z[b])
                    self.inverse_counts["rank_one_entry_arithmetic"] += 3
                self.put(bordered, a, n, self.gamma * z[a] / delta)
                self.put(bordered, n, a, self.gamma * z[a] / delta)
            self.put(bordered, n, n, 1 / delta)
            means = [value + self.gamma * z[a] * new_value for a, value in enumerate(means)] + [
                new_value
            ]
            index[vertex] = n
            self.ports = sorted(self.retained)
            # Restrict the INVERSE, including when only reordering is needed.
            self.inverse = self.allocate(len(self.ports))
            for a, i in enumerate(self.ports):
                for b, j in enumerate(self.ports):
                    self.put(self.inverse, a, b, self.entry(bordered, index[i], index[j]))
                    self.inverse_counts["inverse_restriction_copy_words"] += 1
            self.means = [means[index[i]] for i in self.ports]
            self.port_index = {i: k for k, i in enumerate(self.ports)}
            self.inverse_counts["cycle_birth_inverse_borders"] += 1
            self.inverse_counts["promoted_old_vertex_occurrences"] += len(promoted)
            self.inverse_counts["permanent_old_promotions"] += len(promoted) - len(transient)
            self.inverse_counts["transient_parent_drops"] += len(transient)
            self.inverse_counts["cycle_births_without_old_promotions"] += not promoted
            endpoints = {i for edge in self.extra for i in edge}
            self.inverse_counts["promoted_steiner_junctions"] += sum(
                i in self.retained and i not in endpoints and i != self.seed for i in promoted
            )
            self.inverse_counts["maximum_promoted_batch_size"] = max(
                self.inverse_counts["maximum_promoted_batch_size"], len(promoted)
            )
            self.inverse_counts["maximum_border_parent_count"] = max(
                self.inverse_counts["maximum_border_parent_count"], len(parents)
            )
            self.inverse_counts["vector_read_write_arithmetic_units"] += 20 * (
                n + 1
            ) + 12 * n * len(parents)
            self.inverse_counts["maximum_augmented_dimension"] = max(
                self.inverse_counts["maximum_augmented_dimension"], n + 1
            )
        assert set(self.ports) == self.retained and self.port_index == {
            i: k for k, i in enumerate(self.ports)
        }
        self.inverse_counts["maximum_current_inverse_dimension"] = max(
            self.inverse_counts["maximum_current_inverse_dimension"], len(self.ports)
        )

    def checkpoint(self):
        self.indices = {}
        if len(self.active) == 1:
            value = self.means[0]
            minimum = self.minimum(self.seed, self.counts)
            ordinary = (value - self.shift - minimum[0], minimum[1]) if minimum else None
            return [ordinary] if ordinary else [], [], {self.seed: value}, None
        minima = {i: self.minimum(i, self.builder_counts) for i in self.active}
        self.current = {}
        ordinary, exceptional = [], []
        for pid in self.pieces:
            builder = ComponentHierarchy(self, pid, minima)
            root = builder.build().summary
            backend = builder.adapter.backend
            values = tuple(self.means[self.port_index[p]] - self.shift for p in root.ports)
            self.current[pid] = (backend, root, values)
            self.callback_counts.update(builder.adapter.counts)
            if len(root.ports) == 1:
                candidate = (
                    (values[0] - root.threshold[0], root.threshold[1]) if root.threshold else None
                )
            else:
                candidate = backend.arena.query(root.hull, values)
            if candidate is not None:
                ordinary.append(candidate)
            self.counts["component_reporter_queries"] += 1
            self.backend_counts.update(backend.counts)
            self.hull_counts.update(backend.arena.counts)
        for label in sorted(self.exceptions):
            total = sum(
                self.response(parent, self.home_piece, False)[2] for parent in self.boundary[label]
            )
            gate = self.gamma * total - self.lam * self.oracle.degree(label)
            exceptional.append((gate, label))
            self.counts["exceptional_gate_queries"] += 1
            self.counts["quiet_exceptional_gate_queries"] += gate <= 0
        self.history.append(self.current)
        self.counts["historical_root_and_port_words"] += sum(
            3 + len(root.ports) for _, root, _ in self.current.values()
        )
        return (
            ordinary,
            exceptional,
            None,
            (self.current, self.ports, None, None, [value - self.shift for value in self.means]),
        )


def certificate(state, matrix, load, exact, record, counts):
    """Independent original-matrix certificate; never called by decisions."""
    ports = state.ports
    coarse, _ = independent_schur(matrix, load, state.active, ports)
    for a in range(len(ports)):
        for b in range(len(ports)):
            assert sum(state.inverse[a][k] * coarse[k][b] for k in range(len(ports))) == F(a == b)
            counts["independent_inverse_identity_entries"] += 1
    assert all(state.means[k] == exact[i] for k, i in enumerate(ports))
    counts["independent_inverse_identity_certificates"] += 1
    if record is not None:
        seen, edge_owners, row_owners = set(), Counter(), Counter()
        for pid, (backend, root, values) in record[0].items():
            piece = state.pieces[pid]
            assert set(root.ports) == piece.vertices & state.retained
            recovered = backend.recover(root, values)
            assert set(recovered) == piece.vertices
            assert all(value + state.shift == exact[i] for i, value in recovered.items())
            seen.update(recovered)
            for edge in piece.edges:
                edge_owners[edge] += 1
                for i in edge:
                    row_owners[i] += state.home[i] == edge
            counts["independent_full_component_recoveries"] += 1
        assert seen == state.active and all(value == 1 for value in edge_owners.values())
        assert set(edge_owners) == {state.home[i] for i in state.active if i != state.seed}
        assert all(row_owners[i] == 1 for i in state.active)


def check_case(graph, seed, alpha, lam, policy, counts):
    n = len(graph)
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in graph]
    optimum, previous, previous_q = obstacle(matrix, load), [F(0)] * n, 0

    def validate(state, ordinary, exceptional, singleton, record):
        nonlocal previous, previous_q
        exact = point(matrix, load, state.active)
        assert all(previous[i] <= exact[i] <= optimum[i] for i in graph)
        assert all(exact[i] > 0 for i in state.active)
        certificate(state, matrix, load, exact, record, counts)
        boundary = {
            j: tuple(i for i in graph[j] if i in state.active)
            for j in graph
            if j not in state.active and any(i in state.active for i in graph[j])
        }
        r = graph.subgraph(state.active).number_of_edges() - len(state.active) + 1
        q = r + sum(len(parents) - 1 for parents in boundary.values())
        assert state.q == q >= previous_q and r == len(state.extra)
        assert set(state.boundary) == set(boundary)
        assert all(set(state.boundary[j]) == set(parents) for j, parents in boundary.items())
        assert state.exceptions == {j for j in boundary if len(boundary[j]) >= 2}
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
        if singleton is not None:
            assert singleton[seed] == exact[seed]
        previous, previous_q = exact, q
        counts["independent_face_solves"] += 1

    state = InverseState(Oracle(graph), seed, alpha, lam, reverse_parent=policy)
    got = state.run(validate, prefer_exception=policy)
    assert [got.get(i, F(0)) for i in graph] == optimum
    volume = sum(graph.degree(i) for i in got)
    assert not got or lam * volume < 1
    assert state.oracle.rows == set(got)
    assert state.oracle.counts["adjacency_entries_inspected"] == volume
    residual = [F(i == seed) - sum(matrix[i][j] * got.get(j, F(0)) for j in graph) for i in graph]
    assert all(0 <= residual[i] <= lam * graph.degree(i) for i in graph)
    counts["exact_obstacle_acl_comparisons"] += 1
    for saved in state.history[:: max(1, len(state.history) // 3)]:
        for backend, root, values in saved.values():
            links, leaves = audit_index(root, counts)
            recovered = backend.recover(root, values)
            for i, leaf in leaves.items():
                assert (
                    point_query(i, leaf, lambda node: links[id(node)], root, values, counts)
                    == recovered[i]
                )
            counts["retained_root_rechecks"] += 1
    return state


def state_record(state):
    return {
        "seed": state.seed,
        "alpha_lazy": str(state.alpha),
        "lambda": str(state.lam),
        "eps_appr": str(2 * state.lam),
        "admission_order": state.admissions,
        "final_ports": state.ports,
        "state_machine_counts": dict(state.counts),
        "inverse_update_counts": dict(state.inverse_counts),
        "green_query_counts": dict(state.green_counts),
        "original_graph_access": dict(state.oracle.counts),
    }


def triangle_witness(counts):
    state = check_case(nx.complete_graph(3), 0, F(1, 3), F(1, 20), True, counts)
    assert state.admissions == [0, 1, 2] and state.ports == [0, 2]
    assert state.inverse == [[F(3, 5), F(1, 5)], [F(1, 5), F(3, 5)]]
    assert state.means == [F(1, 2), F(1, 10)]
    assert state.inverse_counts["transient_parent_drops"] == 1
    return {
        "kind": "triangle transient insertion parent",
        **state_record(state),
        "final_inverse": [[str(x) for x in row] for row in state.inverse],
        "final_physical_means": [str(x) for x in state.means],
    }


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
        exact = solve(matrix, load)
        assert min(exact) > 0
        assert all(gamma * exact[i] < lam * implicit.degree(n + i) for i in graph)
        state = InverseState(Oracle(implicit), seed, alpha, lam, reverse_parent=True)

        def validate_implicit(current, ordinary, exceptional, singleton, record):
            face = point(matrix, load, current.active)
            certificate(current, matrix, load, face, record, counts)
            boundary = {
                j: tuple(i for i in graph[j] if i in current.active)
                for j in graph
                if j not in current.active and any(i in current.active for i in graph[j])
            }
            boundary.update({n + i: (i,) for i in current.active})
            assert set(boundary) == set(current.boundary)
            assert all(set(current.boundary[j]) == set(parents) for j, parents in boundary.items())
            exceptional_map = {label: gate for gate, label in exceptional}
            gates = {
                j: gamma * sum(face[i] for i in parents) - lam * implicit.degree(j)
                for j, parents in boundary.items()
            }
            assert all(exceptional_map[j] == gates[j] for j in boundary if len(boundary[j]) >= 2)
            assert any(gates[j] > 0 for j in boundary if len(boundary[j]) == 1) == any(
                gate > 0 for gate, _ in ordinary
            )
            assert all(gates[j] > 0 for gate, j in ordinary + exceptional if gate > 0)
            counts["implicit_original_gate_checks"] += len(gates)

        got = state.run(validate_implicit, prefer_exception=True)
        assert [got.get(i, F(0)) for i in graph] == exact
        assert state.oracle.rows == set(graph)
        volume = sum(implicit.degree(i) for i in graph)
        assert state.oracle.counts["adjacency_entries_inspected"] == volume
        counts["implicit_private_star_exact_comparisons"] += 1
        records.append(
            {
                "kind": "implicit finite private stars on " + name,
                "core_edges": sorted(graph.edges),
                "core_vertices": n,
                "ambient_vertices": n + sum(implicit.degree(n + i) for i in graph),
                "active_volume": volume,
                "inactive_hub_rows_scanned": 0,
                **state_record(state),
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
    counts, ledgers = (
        Counter(),
        {
            key: Counter()
            for key in [
                "counts",
                "inverse_counts",
                "green_counts",
                "builder_counts",
                "callback_counts",
                "backend_counts",
                "hull_counts",
            ]
        },
    )
    access = Counter()
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
                    "cases": counts["exact_obstacle_acl_comparisons"],
                }
            ),
            flush=True,
        )
    witness = triangle_witness(counts)
    structured = structured_cases(counts) if args.structured else []
    result = {
        "audit": "incremental_active_set_sdd.maintained_coarse_inverse",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all connected simple atlas graphs through max_n",
        "max_n": args.max_n,
        "graph_count": len(graphs),
        "seed": "every vertex",
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in parameters],
        "eps_appr": "2*lambda",
        "policies": [
            "ordinary first, first-discovered spanning parent",
            "exceptional first, last-discovered spanning parent",
        ],
        "stopping_rule": "all component ordinary reporters and all exceptional original gates nonpositive; strictly positive admissions",
        "scope": "Maintained current coarse inverse and port means; no coarse solve used for admissions. Every checkpoint independently certifies J*K=I using full original Schur elimination. Reference hierarchy rebuilding and parent-index construction do not implement the published online balancing algorithm.",
        "history_scope": "Immutable component roots and old port values retained; dense inverse histories not retained.",
        "atlas_ledgers": {key: dict(value) for key, value in ledgers.items()},
        "original_graph_access": dict(access),
        "audit_only": dict(counts),
        "triangle_transient_witness": witness,
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
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
