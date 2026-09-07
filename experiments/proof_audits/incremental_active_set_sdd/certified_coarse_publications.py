"""Certified sparse coarse-response interface for geometric ACL publications.

The state machine stores no dense inverse. Sparse physical Schur assembly
and residual acceptance are implemented. The supplied-SDD solver is an
explicit source import: this exact audit substitutes a labelled dense
coarse reference provider that sends two bad candidates before a certified,
nonzero perturbation. Full original-face solves are validator-only.
Online hierarchy balancing remains the separately charged source import.
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

from cluster_green_queries import response_trace
from cluster_point_queries import audit_index, point_query
from coarse_publication_solver import PublicationState, SharedPairStar, boundary_view
from geometric_value_events import obstacle, point, solve
from local_cycle_rank_clusters import ComponentHierarchy, independent_schur
from local_sun_solver import Oracle
import networkx as nx


class SparseCoarse:
    def __init__(self, dimension, counts):
        self.rows = [{} for _ in range(dimension)]
        self.counts = counts
        counts["sparse_row_records"] += dimension

    def add(self, i, j, value):
        row = self.rows[i]
        row[j] = row.get(j, F(0)) + value
        if row[j] == 0:
            del row[j]
        self.counts["sparse_entry_read_modify_writes"] += 1

    def apply(self, vector):
        out = [F(0)] * len(self.rows)
        self.counts["sparse_matvec_output_words"] += len(out)
        for i, row in enumerate(self.rows):
            for j, value in row.items():
                out[i] += value * vector[j]
                self.counts["sparse_matvec_nonzero_visits"] += 1
        return out

    def certify(self, vector, load, budgets):
        residual = [b - z for b, z in zip(load, self.apply(vector))]
        self.counts["residual_certificate_coordinate_checks"] += len(residual)
        self.counts["residual_certificate_attempts"] += 1
        accepted = all(abs(r) <= budget for r, budget in zip(residual, budgets))
        self.counts[
            "accepted_coarse_certificates" if accepted else "rejected_coarse_certificates"
        ] += 1
        return accepted


def dense_reference_candidates(matrix, load, budgets, phase, counts):
    """Testing provider only: never a claimed nearly-linear SDD implementation."""
    n = len(load)
    dense = [[row.get(j, F(0)) for j in range(n)] for row in matrix.rows]
    counts["reference_coarse_dense_matrix_words"] += n * n
    counts["reference_coarse_dense_solves"] += 1
    exact = solve(dense, load)
    signs = [F(1 if (j + phase) % 2 else -1) for j in range(n)]
    direction = [sum(row[j] * signs[j] for j in range(n)) for row in dense]
    scale = min(budget / abs(x) for budget, x in zip(budgets, direction) if x)
    # Both errors are rejected by the algorithm's certificate, independently
    # of their coordinate signs. The accepted vector is never the exact one.
    for factor in [F(2), F(-2), F(1) if phase % 3 == 0 else F(1, 2)]:
        counts["reference_candidate_vector_words"] += n
        yield [x + factor * scale * s for x, s in zip(exact, signs)]


class CertifiedPublicationState(PublicationState):
    def __init__(self, *args, candidate_provider=dense_reference_candidates, **kwargs):
        super().__init__(*args, **kwargs)
        self.delta = min(self.h / 16, self.epsilon / 64)
        self.coarse_counts, self.provider_counts = Counter(), Counter()
        self.candidate_provider = candidate_provider
        self.coarse, self.physical_load = None, []
        self.certificate_generation = 0

    def records(self):
        minima = {
            i: (self.eta * self.ell[i] + self.h - self.delta - self.shift, i) for i in self.active
        }
        self.builder_counts["reference_publication_payload_reads"] += len(minima)
        records = {}
        for pid in self.pieces:
            builder = ComponentHierarchy(self, pid, minima)
            root = builder.build().summary
            records[pid] = builder.adapter.backend, root
            self.callback_counts.update(builder.adapter.counts)
        return records

    def admit(self, vertex):
        # No exact response, Green promotion, border inverse or temporary port
        # is needed. Readiness already guarantees the true face is positive.
        self._admit_metadata(vertex)
        self.ports = sorted(self.retained)
        self.port_index = {v: k for k, v in enumerate(self.ports)}
        p = len(self.ports)
        self.coarse_counts["current_port_index_words"] += 2 * p
        matrix = SparseCoarse(p, self.coarse_counts)
        shifted_load, multiplicity = [F(0)] * p, Counter()
        self.coarse_counts["coarse_load_initializations"] += p
        if len(self.active) == 1:
            degree, beta = self.original[vertex]
            matrix.add(0, 0, degree)
            shifted_load[0] = beta
        else:
            for _, root in self.records().values():
                for a, i in enumerate(root.ports):
                    k = self.port_index[i]
                    multiplicity[i] += 1
                    shifted_load[k] += root.load[a]
                    self.coarse_counts["component_load_additions"] += 1
                    for b, j in enumerate(root.ports):
                        matrix.add(k, self.port_index[j], root.matrix[a][b])
            for i, copies in multiplicity.items():
                degree, beta = self.original[i]
                k = self.port_index[i]
                matrix.add(k, k, -(copies - 1) * degree)
                shifted_load[k] -= (copies - 1) * beta
                self.coarse_counts["duplicate_port_corrections"] += 1
            for i, j in self.extra:
                a, b = self.port_index[i], self.port_index[j]
                matrix.add(a, b, -self.gamma)
                matrix.add(b, a, -self.gamma)
                shifted_load[a] += self.gamma * self.shift
                shifted_load[b] += self.gamma * self.shift
                self.coarse_counts["extra_edge_restorations"] += 1
        row_sums = matrix.apply([F(1)] * p)
        self.physical_load = [b + self.shift * s for b, s in zip(shifted_load, row_sums)]
        budgets = [self.delta * self.bar * self.original[i][0] for i in self.ports]
        self.coarse_counts["physical_load_and_budget_words"] += 4 * p
        self.coarse = matrix
        for candidate in self.candidate_provider(
            matrix, self.physical_load, budgets, len(self.active), self.provider_counts
        ):
            if matrix.certify(candidate, self.physical_load, budgets):
                self.means = candidate
                break
        else:
            raise RuntimeError("Supplied coarse candidates exhausted before certification")
        self.certificate_generation += 1
        self.coarse_counts["coarse_face_assemblies"] += 1
        self.coarse_counts["maximum_coarse_dimension"] = max(
            self.coarse_counts["maximum_coarse_dimension"], p
        )
        self.coarse_counts["maximum_coarse_nonzeros"] = max(
            self.coarse_counts["maximum_coarse_nonzeros"], sum(map(len, matrix.rows))
        )
        self.current, self.indices = {}, {}
        assert not self.inverse and not self.inverse_counts

    def producer_checkpoint(self):
        self.indices = {}
        self.publication_counts["producer_searches"] += 1
        if len(self.active) == 1:
            t = self.means[0]
            return (
                [(t - self.eta * self.ell[self.seed] - self.h + self.delta, self.seed)],
                {self.seed: t},
                None,
            )
        self.current, candidates = {}, []
        for pid, (backend, root) in self.records().items():
            values = tuple(self.means[self.port_index[i]] - self.shift for i in root.ports)
            self.current[pid] = backend, root, values
            candidate = (
                (values[0] - root.threshold[0], root.threshold[1])
                if len(root.ports) == 1
                else backend.arena.query(root.hull, values)
            )
            assert candidate is not None
            candidates.append(candidate)
            self.publication_counts["component_publication_queries"] += 1
            self.publication_counts["current_component_port_words_written"] += len(values)
            self.backend_counts.update(backend.counts)
            self.hull_counts.update(backend.arena.counts)
        return candidates, None, self.current

    def named_value(self, vertex):
        if vertex in self.port_index:
            self.coarse_counts["named_retained_value_reads"] += 1
            return self.means[self.port_index[vertex]]
        pid = self.home_piece[vertex]
        backend, root, values = self.current[pid]
        if pid not in self.indices:
            self.indices[pid] = audit_index(root, self.builder_counts)
        links, leaves = self.indices[pid]
        return (
            point_query(
                vertex,
                leaves[vertex],
                lambda node: links[id(node)],
                root,
                values,
                self.query_counts,
            )
            + self.shift
        )

    def publish(self, vertex, value):
        previous = self.ell[vertex]
        assert value > self.eta * previous + self.h - 2 * self.delta
        assert value <= 1 / (self.bar * self.oracle.degree(vertex))
        change = value - previous
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
            self.lower[neighbor] += self.gamma * change
            self.publication_counts["lower_signal_read_modify_writes"] += 1
            self.publication_counts["ready_threshold_checks"] += 1
            if self.lower[neighbor] > self.theta * self.oracle.degree(neighbor):
                self.publication_counts["ready_flag_reads"] += 1
                if neighbor not in self.queued:
                    self.queued.add(neighbor)
                    self.ready.append(neighbor)
                    self.publication_counts["ready_queue_insertions"] += 1

    def run(self, validator=None):
        if self.epsilon * self.oracle.degree(self.seed) >= 1:
            self.counts["trivial_acl_zero_stops"] += 1
            return {}
        self.admit(self.seed)
        while True:
            candidates, singleton, record = self.producer_checkpoint()
            if validator:
                validator(self, candidates, singleton, record)
            self.publication_counts["candidate_rows_inspected"] += len(candidates)
            due = next((item for item in candidates if item[0] > 0), None)
            if due is not None:
                self.publish(due[1], self.named_value(due[1]) - self.delta)
                continue
            self.publication_counts["producer_quiet_certificates"] += 1
            self.publication_counts["ready_queue_empty_checks"] += 1
            if not self.ready:
                self.publication_counts["terminal_acl_certificates"] += 1
                if singleton is not None:
                    self.counts["final_output_words"] += 1
                    return {self.seed: max(F(0), singleton[self.seed] - self.delta)}
                out = {}
                for backend, root, values in record.values():
                    before = backend.counts["recovery_cluster_visits"]
                    for i, w in backend.recover(root, values).items():
                        value = max(F(0), w + self.shift - self.delta)
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
            self.admit(vertex)


def reference_recovery(state, singleton, record, counts):
    if singleton is not None:
        return singleton
    values = {}
    for backend, root, ports in record.values():
        before = backend.counts.copy()
        for i, w in backend.recover(root, ports).items():
            if i in values:
                assert values[i] == w + state.shift
            values[i] = w + state.shift
        counts["reference_current_recovery_visits"] += (
            backend.counts["recovery_cluster_visits"] - before["recovery_cluster_visits"]
        )
        backend.counts = before
    return values


def make_validator(matrix, load, optimum, boundary, degree, counts):
    previous = [F(0)] * len(matrix)
    face, last_size, previous_q = None, 0, 0
    frozen, generation = None, 0

    def validate(state, candidates, singleton, record):
        nonlocal previous, face, last_size, previous_q, frozen, generation
        approximate = reference_recovery(state, singleton, record, counts)
        if len(state.active) != last_size:
            face = point(matrix, load, state.active)
            assert all(previous[i] <= face[i] <= optimum[i] for i in range(len(matrix)))
            assert all(face[i] > state.epsilon / 20 for i in state.active)
            exact_k, exact_f = independent_schur(matrix, load, state.active, state.ports)
            p = len(state.ports)
            dense = [[row.get(j, F(0)) for j in range(p)] for row in state.coarse.rows]
            assert dense == exact_k and state.physical_load == exact_f
            assert sum(map(len, state.coarse.rows)) <= p + 2 * len(state.pieces) + 2 * len(
                state.extra
            )
            for k, i in enumerate(state.ports):
                assert sum(dense[k]) >= state.bar * degree(i)
                assert dense[k][k] <= degree(i)
                assert all(dense[k][j] <= 0 for j in range(p) if j != k)
                assert exact_f[k] <= (1 if i == state.seed else 0)
            energy = sum(f * face[i] for i, f in zip(state.ports, exact_f))
            assert 0 < energy <= 1 / state.bar
            if record is not None:
                for backend, root, _ in record.values():
                    links, leaves = audit_index(root, counts)
                    for i, leaf in leaves.items():
                        row = response_trace(
                            i,
                            leaf,
                            lambda node: links[id(node)],
                            root,
                            backend,
                            counts,
                            keep_trace=False,
                        ).row
                        assert all(a >= 0 for a in row[:-1]) and sum(row[:-1]) <= 1
                        counts["conditional_substochastic_row_checks"] += 1
            frozen = (
                tuple(tuple(sorted(row.items())) for row in state.coarse.rows),
                tuple(state.physical_load),
                tuple(state.means),
            )
            generation = state.certificate_generation
            counts["independent_coarse_schur_and_load_checks"] += 1
            counts["independent_positive_face_solves"] += 1
            previous, last_size = face, len(state.active)
        else:
            assert frozen == (
                tuple(tuple(sorted(row.items())) for row in state.coarse.rows),
                tuple(state.physical_load),
                tuple(state.means),
            )
            assert generation == state.certificate_generation
            counts["publication_only_coarse_state_unchanged_checks"] += 1
        assert all(abs(approximate[i] - face[i]) <= state.delta for i in state.active)
        assert all(0 <= state.ell[i] <= face[i] for i in state.active)
        due = {
            i
            for i in state.active
            if approximate[i] + state.delta > state.eta * state.ell[i] + state.h
        }
        assert bool(due) == any(value > 0 for value, _ in candidates)
        assert all(label in due for value, label in candidates if value > 0)
        counts["independent_approximate_due_signs"] += len(state.active)
        counts["uniform_original_coordinate_error_checks"] += len(state.active)
        if not due:
            assert all(face[i] <= state.eta * state.ell[i] + state.h for i in state.active)
            counts["independent_true_quiet_band_checks"] += 1
        expected = boundary(state.active)
        actual = boundary_view(state)
        assert set(expected) == set(actual)
        assert all(set(actual[j]) == set(parents) for j, parents in expected.items())
        r = (
            sum(matrix[i][j] != 0 for i in state.active for j in state.active if i < j)
            - len(state.active)
            + 1
        )
        assert r == len(state.extra)
        q = r + sum(len(parents) - 1 for parents in expected.values())
        assert state.q == q >= previous_q
        previous_q = q
        signals = {
            j: state.gamma * sum(state.ell[i] for i in parents) for j, parents in expected.items()
        }
        assert signals == state.lower
        assert state.queued == {j for j in signals if signals[j] > state.theta * degree(j)}
        assert len(state.ready) == len(state.queued) and set(state.ready) == state.queued
        for j, parents in expected.items():
            residual = state.gamma * sum(face[i] for i in parents)
            assert signals[j] <= residual
            if not due:
                assert residual <= state.eta * signals[j] + state.gamma * state.h * degree(j)
        counts["independent_original_boundary_band_checks"] += len(signals)
        assert not state.inverse and not state.inverse_counts and not state.green_counts

    return validate


def check_final(state, got, matrix, load, optimum, boundary, degree, counts):
    face = point(matrix, load, state.active)
    assert set(got) == state.active and all(value > 0 for value in got.values())
    assert all(0 <= face[i] - got[i] <= 2 * state.delta for i in got)
    assert all(face[i] <= optimum[i] for i in range(len(matrix)))
    volume = sum(degree(i) for i in got)
    assert state.lam * volume < 1 and state.oracle.rows == state.active
    assert state.oracle.counts["adjacency_entries_inspected"] == volume
    vector = [got.get(i, F(0)) for i in range(len(matrix))]
    residual = [
        F(i == state.seed) - sum(matrix[i][j] * vector[j] for j in range(len(matrix)))
        for i in range(len(matrix))
    ]
    assert all(0 <= residual[i] <= state.epsilon * degree(i) for i in range(len(matrix)))
    # Implicit graphs store only their core matrix. Check every discovered
    # exterior row separately; all further private leaves see only zero hubs.
    for j, parents in boundary(state.active).items():
        assert state.gamma * sum(got[i] for i in parents) <= 3 * state.epsilon * degree(j) / 4
    assert state.publication_counts["cached_delivery_incidence_reads"] == sum(
        degree(i) * c for i, c in state.publications_by_vertex.items()
    )
    assert (
        state.publication_counts["parent_buffer_growth_copy_words"]
        <= 2 * state.publication_counts["parent_buffer_append_writes"]
    )
    assert (
        state.publication_counts["parent_buffer_zero_initializations"]
        <= 4 * state.publication_counts["parent_buffer_append_writes"]
    )
    assert state.coarse_counts["coarse_face_assemblies"] == len(got)
    assert state.coarse_counts["accepted_coarse_certificates"] == len(got)
    assert state.coarse_counts["rejected_coarse_certificates"] == 2 * len(got)
    assert state.publication_counts["producer_searches"] == state.publication_counts[
        "publications"
    ] + len(got)
    assert not state.inverse and not state.inverse_counts and not state.history
    for i, c in state.publications_by_vertex.items():
        assert (state.h / 2) * state.eta ** (c - 1) < 1 / (state.bar * degree(i))
    counts["complete_original_acl_checks"] += 1
    counts["strictly_downward_repaired_nonzero_outputs"] += bool(got)
    return residual


def check_case(graph, seed, alpha, epsilon, policy, counts):
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - epsilon * graph.degree(i) / 2 for i in graph]
    optimum = obstacle(matrix, load)

    def boundary(active):
        return {
            j: tuple(i for i in graph[j] if i in active)
            for j in graph
            if j not in active and any(i in active for i in graph[j])
        }

    state = CertifiedPublicationState(Oracle(graph), seed, alpha, epsilon, reverse_policy=policy)
    got = state.run(make_validator(matrix, load, optimum, boundary, graph.degree, counts))
    check_final(state, got, matrix, load, optimum, boundary, graph.degree, counts)
    return state


def record(state):
    return {
        "seed": state.seed,
        "alpha_lazy": str(state.alpha),
        "eps_appr": str(state.epsilon),
        "delta": str(state.delta),
        "admissions": state.admissions,
        "active_cycle_rank": len(state.extra),
        "revealed_cycle_rank": state.q,
        "coarse": dict(state.coarse_counts),
        "publications": dict(state.publication_counts),
        "original_access": dict(state.oracle.counts),
        "audit_only_provider": dict(state.provider_counts),
        "audit_only_builder": dict(state.builder_counts),
    }


def structured(counts, maximum):
    results = []
    families = [
        nx.cycle_graph(10),
        nx.wheel_graph(10),
        nx.ladder_graph(7),
        nx.complete_graph(7),
        nx.barbell_graph(4, 5),
        nx.balanced_tree(2, 4),
    ]
    for graph in families:
        for alpha in [F(1, 3), F(1, 1009), F(1008, 1009)]:
            for policy in [False, True]:
                state = check_case(graph, 0, alpha, F(1, 50), policy, counts)
                results.append(
                    {
                        "kind": "structured explicit",
                        "vertices": len(graph),
                        "edges": len(graph.edges),
                        **record(state),
                    }
                )
    for k in [2, 4, 8, 16, 32]:
        if k > maximum:
            continue
        for alpha in [F(1, 3), F(1, 1009)]:
            gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
            lam = gamma / (4 * k * (k + gamma))
            upper = 4 / (bar * lam)
            degree = (upper.numerator + upper.denominator - 1) // upper.denominator
            graph = SharedPairStar(k, degree)
            n = k + 1
            matrix = [
                [F(k) if i == j else -gamma if (i == 0) != (j == 0) else F(0) for j in range(n)]
                for i in range(n)
            ]
            load = [F(i == 0) - lam * k for i in range(n)]
            optimum = solve(matrix, load)

            def boundary(active):
                candidates = (set(range(n)) | set(graph.pairs)) - active
                return {
                    j: tuple(i for i in (graph.pairs[j] if j >= n else graph[j]) if i in active)
                    for j in candidates
                    if any(i in active for i in (graph.pairs[j] if j >= n else graph[j]))
                }

            for policy in [False, True]:
                state = CertifiedPublicationState(
                    Oracle(graph), 0, alpha, 2 * lam, reverse_policy=policy
                )
                got = state.run(
                    make_validator(matrix, load, optimum, boundary, graph.degree, counts)
                )
                check_final(state, got, matrix, load, optimum, boundary, graph.degree, counts)
                assert set(got) == set(range(n)) and not state.extra
                assert state.q == k * (k - 1) // 2
                results.append(
                    {
                        "kind": "implicit shared-pair star",
                        "k": k,
                        "ambient_vertices": n + len(graph.pairs) * (degree - 1),
                        **record(state),
                    }
                )
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--shared-star-max", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 2 <= args.max_n <= 7:
        parser.error("max_n must be between 2 and 7")
    started = time.monotonic()
    counts = Counter()
    ledgers = {
        key: Counter()
        for key in [
            "counts",
            "coarse_counts",
            "publication_counts",
            "provider_counts",
            "builder_counts",
            "query_counts",
        ]
    }
    access = Counter()
    params = [
        (F(1, 3), F(1, 10)),
        (F(1, 7), F(1, 50)),
        (F(1, 1009), F(1, 50)),
        (F(1, 3), F(1, 2)),
        (F(1008, 1009), F(1, 50)),
    ]
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= args.max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed in graph:
            for alpha, epsilon in params:
                for policy in [False, True]:
                    state = check_case(graph, seed, alpha, epsilon, policy, counts)
                    for key, ledger in ledgers.items():
                        for name, value in getattr(state, key).items():
                            ledger[name] = (
                                max(ledger[name], value)
                                if name.startswith("maximum_")
                                else ledger[name] + value
                            )
                    access.update(state.oracle.counts)
        print(
            json.dumps(
                {
                    "graph_n": len(graph),
                    "edges": len(graph.edges),
                    "cases": counts["complete_original_acl_checks"],
                }
            ),
            flush=True,
        )
    cases = structured(counts, args.shared_star_max) if args.structured else []
    dependencies = [
        "coarse_publication_solver",
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
        "geometric_value_events",
    ]
    result = {
        "audit": "incremental_active_set_sdd.certified_coarse_publications",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "max_n": args.max_n,
        "graph_count": len(graphs),
        "graph": "all connected simple atlas graphs through max_n",
        "seed": "every vertex",
        "parameters_alpha_epsilon": [[str(a), str(e)] for a, e in params],
        "policies": ["FIFO/first tree parent", "LIFO/last tree parent"],
        "lambda": "eps_appr/2",
        "delta": "min(eps_appr/(256*gamma),eps_appr/64)",
        "initial_zero_test": "eps_appr*d_v>=1",
        "stopping_rule": "all approximate upper-band reporters quiet and lower-signal ready queue empty; return downward repaired current response",
        "source_interface": "Sparse SDD solver explicitly imported; the exact audit uses a dense coarse provider with two rejected signed perturbations followed by an accepted nonzero perturbation. This is not a fast numerical solver implementation.",
        "hierarchy_scope": "Per-search full rebuilds and parent index builds are separately charged reference work; online top-tree balancing remains imported.",
        "accuracy_scope": "Original ACL residual only; no exact obstacle/RPPR or OP2 result",
        "atlas_ledgers": {k: dict(v) for k, v in ledgers.items()},
        "original_graph_access": dict(access),
        "audit_only": dict(counts),
        "structured_cases": cases,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in dependencies
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
