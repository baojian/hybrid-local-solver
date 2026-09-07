"""Sparse coarse residual epochs, with a source-valid forced-refresh family.

An ordinary admission updates at most two residual coordinates for fixed
certified port values. Reuse is permitted only while the exact absolute
certificate remains valid. This is an optional implementation refinement,
not a new graph-uniform work theorem. Supplied solves and hierarchy balancing
remain explicitly labelled source imports/reference providers.
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

from certified_coarse_publications import (
    CertifiedPublicationState,
    make_validator,
    reference_recovery,
)
from cluster_green_queries import response_trace
from cluster_point_queries import audit_index
from geometric_value_events import obstacle, point, solve
from local_sun_solver import Oracle
import networkx as nx


class ResidualEpochState(CertifiedPublicationState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.epoch_counts, self.epoch_query_counts = Counter(), Counter()
        self.residual, self.budgets, self.last_transition = [], [], None

    def reset_residual(self):
        applied = self.coarse.apply(self.means)
        self.residual = [b - y for b, y in zip(self.physical_load, applied)]
        self.budgets = [self.delta * self.bar * self.original[i][0] for i in self.ports]
        self.epoch_counts["residual_reset_coordinate_words"] += 3 * len(self.ports)
        self.epoch_counts["complete_refreshed_port_vector_words"] += len(self.ports)
        self.epoch_counts["coarse_refreshes"] += 1

    def admit(self, vertex):
        if not self.active or len(self.boundary[vertex]) > 1:
            super().admit(vertex)
            self.reset_residual()
            self.epoch_counts["initial_or_cycle_full_assemblies"] += 1
            self.last_transition = {"vertex": vertex, "kind": "initial_or_cycle"}
            return
        parent = self.boundary[vertex][0]
        degree = self.oracle.degree(vertex)
        retained = parent in self.port_index
        if retained:
            a, variance, zeta = {self.port_index[parent]: F(1)}, F(0), F(0)
            self.epoch_counts["direct_retained_conditional_rows"] += 1
        else:
            pid = self.home_piece[parent]
            backend, root, values = self.current[pid]
            if pid not in self.indices:
                self.indices[pid] = audit_index(root, self.builder_counts)
            links, leaves = self.indices[pid]
            response = response_trace(
                parent,
                leaves[parent],
                lambda node: links[id(node)],
                root,
                backend,
                self.epoch_query_counts,
                keep_trace=False,
            )
            a = {self.port_index[i]: c for i, c in zip(root.ports, response.row[:-1]) if c}
            variance = response.variance
            zeta = response.row[-1] + self.shift * (1 - sum(a.values()))
        assert 1 <= len(a) <= 2 and zeta <= 0
        approximate_parent = zeta + sum(c * self.means[i] for i, c in a.items())
        tau = degree - self.gamma * self.gamma * variance
        c = -self.lam * degree + self.gamma * zeta
        approximate_gate = self.gamma * approximate_parent - self.lam * degree
        assert tau >= self.bar * degree and c < 0 and approximate_gate > 0
        increments = {}
        for i, ai in a.items():
            for j, aj in a.items():
                self.coarse.add(i, j, -self.gamma * self.gamma * ai * aj / tau)
            self.physical_load[i] += self.gamma * c * ai / tau
            increments[i] = self.gamma * approximate_gate * ai / tau
            self.residual[i] += increments[i]
            self.epoch_counts["sparse_load_and_residual_coordinate_updates"] += 2
        self.epoch_counts["ordinary_sparse_transactions"] += 1
        self.epoch_counts["two_coordinate_transactions"] += len(a) == 2
        self._admit_metadata(vertex)
        assert len(self.retained) == len(self.ports)
        acceptable = all(self.residual[i] <= self.budgets[i] for i in a)
        self.epoch_counts["changed_upper_budget_checks"] += len(a)
        forced_leaf = (
            degree == 1
            and retained
            and self.gamma >= F(1, 2)
            and self.bar * self.oracle.degree(parent) <= 1
        )
        if forced_leaf:
            k = self.port_index[parent]
            assert increments[k] > 2 * self.budgets[k]
            assert not acceptable
            self.epoch_counts["forced_retained_leaf_refreshes"] += 1
        self.last_transition = {
            "vertex": vertex,
            "parent": parent,
            "retained_parent": retained,
            "old_port_count": len(self.ports),
            "changed_coordinates": len(a),
            "forced_leaf": forced_leaf,
            "kind": "reuse" if acceptable else "refresh",
        }
        if acceptable:
            self.epoch_counts["reused_certified_port_vectors"] += 1
        else:
            self.epoch_counts["failed_sparse_epoch_certificates"] += 1
            for candidate in self.candidate_provider(
                self.coarse,
                self.physical_load,
                self.budgets,
                len(self.active),
                self.provider_counts,
            ):
                if self.coarse.certify(candidate, self.physical_load, self.budgets):
                    self.means = candidate
                    break
            else:
                raise RuntimeError("Source candidates exhausted")
            self.certificate_generation += 1
            self.reset_residual()
        self.current, self.indices = {}, {}


def residual_check(state, counts):
    exact_residual = [
        b - sum(value * state.means[j] for j, value in row.items())
        for row, b in zip(state.coarse.rows, state.physical_load)
    ]
    assert exact_residual == state.residual
    assert all(abs(g) <= b for g, b in zip(state.residual, state.budgets))
    counts["independent_maintained_residual_checks"] += 1
    counts["independent_residual_coordinate_checks"] += len(exact_residual)


def finish(state, got, degree, neighbors, vertices, counts):
    assert state.active == set(got) and all(x > 0 for x in got.values())
    assert state.oracle.rows == state.active
    volume = sum(degree(i) for i in got)
    assert state.lam * volume < 1
    assert state.oracle.counts["adjacency_entries_inspected"] == volume
    for i in vertices:
        residual = (
            F(i == state.seed)
            - degree(i) * got.get(i, F(0))
            + state.gamma * sum(got.get(j, F(0)) for j in neighbors(i))
        )
        assert 0 <= residual <= state.epsilon * degree(i)
    assert state.publication_counts["cached_delivery_incidence_reads"] == sum(
        degree(i) * c for i, c in state.publications_by_vertex.items()
    )
    assert state.publication_counts["producer_searches"] == state.publication_counts[
        "publications"
    ] + len(got)
    assert (
        state.coarse_counts["accepted_coarse_certificates"]
        == state.epoch_counts["coarse_refreshes"]
    )
    assert state.epoch_counts["coarse_refreshes"] + state.epoch_counts[
        "reused_certified_port_vectors"
    ] == len(got)
    assert (
        state.coarse_counts["rejected_coarse_certificates"]
        == 2 * state.epoch_counts["coarse_refreshes"]
    )
    assert not state.inverse and not state.inverse_counts and not state.history
    counts["complete_original_acl_checks"] += 1


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

    check = make_validator(matrix, load, optimum, boundary, graph.degree, counts)
    last_size, previous_means = 0, None

    def validate(state, candidates, singleton, record):
        nonlocal last_size, previous_means
        check(state, candidates, singleton, record)
        if len(state.active) != last_size:
            residual_check(state, counts)
            if state.last_transition["kind"] == "reuse":
                assert tuple(state.means) == previous_means
                counts["independent_reused_vector_checks"] += 1
            previous_means = tuple(state.means)
            last_size = len(state.active)

    state = ResidualEpochState(Oracle(graph), seed, alpha, epsilon, reverse_policy=policy)
    got = state.run(validate)
    exact = point(matrix, load, state.active)
    assert all(0 <= exact[i] - got[i] <= 2 * state.delta for i in got)
    finish(state, got, graph.degree, lambda i: graph[i], graph, counts)
    return state


def clique_family(k, t, counts):
    graph = nx.complete_graph(k)
    parent = {}
    for i in range(k):
        for j in range(t):
            leaf = k + i * t + j
            parent[leaf] = i
            graph.add_edge(i, leaf)
    d = k - 1 + t
    alpha = F(1, 8 * d - 1)
    epsilon = F(1, 8 * d * d)
    state = ResidualEpochState(Oracle(graph), 0, alpha, epsilon)
    faces, last_size, exact, previous, events = 0, 0, {}, {}, []

    def validate(state, candidates, singleton, record):
        nonlocal faces, last_size, exact, previous
        approximate = reference_recovery(state, singleton, record, counts)
        if len(state.active) != last_size:
            core = sorted(set(range(k)) & state.active)
            index = {i: j for j, i in enumerate(core)}
            leaves = Counter(parent[j] for j in state.active if j >= k)
            matrix = [
                [F(d) - state.gamma**2 * leaves[i] if i == j else -state.gamma for j in core]
                for i in core
            ]
            load = [F(i == 0) - state.lam * d - state.gamma * state.lam * leaves[i] for i in core]
            values = solve(matrix, load)
            exact = {i: values[index[i]] for i in core}
            exact.update(
                {j: state.gamma * exact[parent[j]] - state.lam for j in state.active if j >= k}
            )
            assert all(x > 0 for x in exact.values())
            assert all(exact[i] >= x for i, x in previous.items())
            # Independently test the original equations, not only the reduced
            # symmetric core formula. All such accesses are reference-only.
            for i in state.active:
                assert graph.degree(i) * exact[i] - state.gamma * sum(
                    exact.get(j, F(0)) for j in graph[i]
                ) == F(i == 0) - state.lam * graph.degree(i)
            if len(core) == k:
                assert state.ports == list(range(k))
                dense = [[row.get(j, F(0)) for j in range(k)] for row in state.coarse.rows]
                assert dense == matrix and state.physical_load == load
            if k <= 4:
                full = [
                    [
                        F(graph.degree(i)) if i == j else -state.gamma if j in graph[i] else F(0)
                        for j in graph
                    ]
                    for i in graph
                ]
                rhs = [F(i == 0) - state.lam * graph.degree(i) for i in graph]
                reference = point(full, rhs, state.active)
                assert all(exact[i] == reference[i] for i in state.active)
                counts["independent_dense_family_face_checks"] += 1
            residual_check(state, counts)
            events.append(state.last_transition.copy())
            previous = exact.copy()
            last_size = len(state.active)
            faces += 1
            counts["independent_pendant_elimination_faces"] += 1
        assert all(abs(approximate[i] - exact[i]) <= state.delta for i in state.active)
        assert all(0 <= state.ell[i] <= exact[i] for i in state.active)
        due = {
            i
            for i in state.active
            if approximate[i] + state.delta > state.eta * state.ell[i] + state.h
        }
        assert bool(due) == any(x > 0 for x, _ in candidates)
        assert all(i in due for x, i in candidates if x > 0)
        if not due:
            assert all(exact[i] <= state.eta * state.ell[i] + state.h for i in state.active)
        signals = {
            j: state.gamma * sum(state.ell[i] for i in graph[j] if i in state.active)
            for j in graph
            if j not in state.active and any(i in state.active for i in graph[j])
        }
        assert signals == state.lower
        assert state.queued == {j for j, g in signals.items() if g > state.theta * graph.degree(j)}
        counts["independent_family_band_checks"] += len(state.active)

    got = state.run(validate)
    finish(state, got, graph.degree, lambda i: graph[i], graph, counts)
    assert set(got) == set(graph) and state.admissions[:k] == list(range(k))
    assert all(0 <= exact[i] - got[i] <= 2 * state.delta for i in got)
    leaf_events = [e for e in events if e["vertex"] >= k]
    assert len(leaf_events) == k * t
    assert all(
        e["kind"] == "refresh" and e["forced_leaf"] and e["old_port_count"] == k
        for e in leaf_events
    )
    assert state.epoch_counts["forced_retained_leaf_refreshes"] == k * t
    counts["canonical_clique_family_checks"] += 1
    return {
        "k": k,
        "t": t,
        "vertices": len(graph),
        "original_core_degree": d,
        "alpha_lazy": str(alpha),
        "eps_appr": str(epsilon),
        "active_volume": sum(dict(graph.degree()).values()),
        "charged_volume": sum(1 + graph.degree(i) for i in graph),
        "active_cycle_rank": len(state.extra),
        "port_count": len(state.ports),
        "full_core_admitted_before_leaves": True,
        "leaf_admissions": k * t,
        "forced_leaf_refreshes": len(leaf_events),
        "mandatory_leaf_port_vector_writes": k * k * t,
        "all_refreshed_port_vector_writes": state.epoch_counts[
            "complete_refreshed_port_vector_words"
        ],
        "inverse_epsilon": str(1 / epsilon),
        "mandatory_writes_times_epsilon": str(k * k * t * epsilon),
        "epoch_counts": dict(state.epoch_counts),
        "coarse_counts": dict(state.coarse_counts),
        "provider_reference_counts": dict(state.provider_counts),
        "original_graph_access": dict(state.oracle.counts),
        "admission_order": state.admissions,
        "faces": faces,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--clique-max", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 2 <= args.max_n <= 7:
        parser.error("max_n must lie between 2 and 7")
    started = time.monotonic()
    counts = Counter()
    ledgers = {
        name: Counter()
        for name in ["epoch_counts", "coarse_counts", "epoch_query_counts", "provider_counts"]
    }
    params = [(F(1, 3), F(1, 10)), (F(1, 1009), F(1, 50)), (F(1008, 1009), F(1, 50))]
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= args.max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed in graph:
            for alpha, epsilon in params:
                for policy in [False, True]:
                    state = check_case(graph, seed, alpha, epsilon, policy, counts)
                    for name, ledger in ledgers.items():
                        for key, value in getattr(state, name).items():
                            ledger[key] = (
                                max(ledger[key], value)
                                if key.startswith("maximum_")
                                else ledger[key] + value
                            )
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
    reuse_paths = []
    for alpha, epsilon in [
        (F(1, 3), F(1, 2**20)),
        (F(1, 3), F(1, 2**30)),
        (F(1, 7), F(1, 2**20)),
    ]:
        for policy in [False, True]:
            state = check_case(nx.path_graph(32), 0, alpha, epsilon, policy, counts)
            assert state.epoch_counts["reused_certified_port_vectors"] > 0
            reuse_paths.append(
                {
                    "vertices": 32,
                    "seed": 0,
                    "alpha_lazy": str(alpha),
                    "eps_appr": str(epsilon),
                    "reversed_policy": policy,
                    "positive_vertices": len(state.active),
                    "epoch_counts": dict(state.epoch_counts),
                    "original_access": dict(state.oracle.counts),
                }
            )
    families = [clique_family(k, k, counts) for k in [3, 4, 6, 8, 12, 16] if k <= args.clique_max]
    deps = [
        "certified_coarse_publications",
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
        "audit": "incremental_active_set_sdd.coarse_residual_epochs",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "connected simple atlas graphs and explicit clique-with-pendant-leaves family",
        "max_n": args.max_n,
        "graph_count": len(graphs),
        "seed": "every atlas vertex; clique core vertex 0",
        "parameters_alpha_epsilon": [[str(a), str(e)] for a, e in params],
        "policies": ["FIFO/first parent", "LIFO/last parent"],
        "stopping_rule": "certified finite-band producer quiet and lower-signal queue empty; downward ACL repair",
        "epoch_rule": "update at most two residual coordinates on ordinary admission; reuse fixed ports only when upper budgets remain valid; full source solve on failure or cycle birth",
        "accuracy_scope": "ACL only; no exact RPPR or general OP3 bound",
        "implementation_scope": "Sparse residual epochs are implemented; dense coarse candidate provider and full hierarchy rebuilds remain separately charged reference substitutions for source imports.",
        "atlas_ledgers": {k: dict(v) for k, v in ledgers.items()},
        "audit_only": dict(counts),
        "accepted_reuse_path_cases": reuse_paths,
        "clique_families": families,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in deps
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
