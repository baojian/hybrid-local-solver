"""Exact sparse Schur downdate and changing-port determinant-budget audit.

An observer checks original-matrix Schur systems along actual exact-gate
and geometric-publication executions. Its dense eliminations, determinants
and selected queries are reference work and never affect admissions.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from math import prod
from pathlib import Path
import subprocess
import time

from cluster_green_queries import response_trace
from cluster_point_queries import audit_index
from coarse_publication_solver import PublicationState
from geometric_value_events import obstacle, point, solve
from local_cycle_rank_clusters import independent_schur
from local_sun_solver import Oracle
from maintained_coarse_inverse import InverseState
import networkx as nx


def determinant(matrix, counts):
    work, n, out = [list(row) for row in matrix], len(matrix), F(1)
    counts["reference_determinant_matrix_copy_words"] += n * n
    for k in range(n):
        pivot = work[k][k]
        assert pivot > 0
        out *= pivot
        for i in range(k + 1, n):
            coefficient = work[i][k] / pivot
            for j in range(k + 1, n):
                work[i][j] -= coefficient * work[k][j]
                counts["reference_determinant_entry_updates"] += 1
            work[i][k] = F(0)
    counts["reference_determinants"] += 1
    return out


class DowndateObserver:
    def schur(self, active, ports):
        self.audit_counts["independent_original_schur_systems"] += 1
        return independent_schur(self.audit_matrix, self.audit_load, active, ports)

    def normalized_determinant(self, matrix, ports):
        return determinant(matrix, self.audit_counts) / (
            self.bar ** len(ports) * prod(self.audit_matrix[i][i] for i in ports)
        )

    def old_conditional_response(self, vertex):
        if vertex in self.port_index:
            row = [F(i == vertex) for i in self.ports]
            return row, F(0), F(0)
        backend, root, _ = self.current[self.home_piece[vertex]]
        links, leaves = audit_index(root, self.audit_query_counts)
        response = response_trace(
            vertex,
            leaves[vertex],
            lambda node: links[id(node)],
            root,
            backend,
            self.audit_query_counts,
            keep_trace=False,
        )
        row = [F(0)] * len(self.ports)
        for i, coefficient in zip(root.ports, response.row[:-1]):
            row[self.port_index[i]] = coefficient
        zeta = response.row[-1] + self.shift * (1 - sum(row))
        return row, response.variance, zeta

    def admit(self, vertex):
        old_active, old_ports = set(self.active), list(self.ports)
        old_point = self.audit_last_point
        if old_active:
            parent_record = self.boundary[vertex]
            # A reference observer reads buffers directly, without charging
            # validator iteration as algorithmic parent-buffer accesses.
            parents = (
                tuple(parent_record.data[: parent_record.size])
                if hasattr(parent_record, "data")
                else tuple(parent_record)
            )
            old_matrix, old_load = self.schur(old_active, old_ports)
            old_phi = self.normalized_determinant(old_matrix, old_ports)
            if len(parents) == 1:
                row, variance, zeta = self.old_conditional_response(parents[0])
                old_j = [list(entries) for entries in self.inverse]
        super().admit(vertex)
        current_matrix, current_load = self.schur(self.active, self.ports)
        phi = self.normalized_determinant(current_matrix, self.ports)
        assert phi >= 1
        assert phi <= (1 / self.bar) ** len(self.ports)
        current_point = point(self.audit_matrix, self.audit_load, self.active)
        assert all(
            old_point[i] <= current_point[i] <= self.audit_optimum[i]
            for i in range(len(current_point))
        )
        assert all(current_point[i] > 0 for i in self.active)
        assert all(self.means[k] == current_point[i] for k, i in enumerate(self.ports))
        self.audit_last_point = current_point
        self.audit_counts["independent_source_face_comparisons"] += 1
        if not old_active:
            self.audit_injection_product = 1 / self.bar
            self.audit_drop_product = F(1)
            self.audit_transients = 0
            self.audit_injection_count = 1
            self.audit_large_updates = 0
            assert phi == 1 / self.bar
        elif len(parents) == 1:
            p, degree = len(old_ports), self.audit_matrix[vertex][vertex]
            tau = degree - self.gamma * self.gamma * variance
            c = -self.lam * degree + self.gamma * zeta
            assert tau >= self.bar * degree and c < 0 and zeta <= 0
            nonzero = sum(value != 0 for value in row)
            assert 1 <= nonzero <= 2
            assert self.ports == old_ports
            expected_matrix = [
                [
                    old_matrix[a][b] - self.gamma * self.gamma * row[a] * row[b] / tau
                    for b in range(p)
                ]
                for a in range(p)
            ]
            expected_load = [old_load[a] + self.gamma * c * row[a] / tau for a in range(p)]
            assert current_matrix == expected_matrix and current_load == expected_load
            assert all(current_load[a] <= old_load[a] for a in range(p))
            chi = (
                self.gamma
                * self.gamma
                * sum(row[a] * old_j[a][b] * row[b] for a in range(p) for b in range(p))
                / tau
            )
            delta = degree - self.gamma * self.gamma * (
                variance + sum(row[a] * old_j[a][b] * row[b] for a in range(p) for b in range(p))
            )
            assert 0 < chi < 1 and delta == tau * (1 - chi)
            assert delta >= self.bar * degree
            assert phi == old_phi * (1 - chi)
            assert (
                current_point[vertex]
                == (self.gamma * old_point[parents[0]] - self.lam * degree) / delta
            )
            self.audit_drop_product *= tau / delta
            self.audit_large_updates += chi >= F(1, 4)
            self.audit_counts["ordinary_sparse_matrix_and_load_checks"] += 1
            self.audit_counts["two_port_sparse_downdates"] += nonzero == 2
            self.audit_counts["ordinary_determinant_ratio_checks"] += 1
            self.audit_counts["ordinary_updates_chi_at_least_quarter"] += chi >= F(1, 4)
        else:
            promoted = sorted(
                (set(self.ports) - set(old_ports) - {vertex}) | (set(parents) - set(old_ports))
            )
            transient = set(promoted) - set(self.ports)
            assert len(transient) <= 1
            ports, previous_matrix, previous_phi = list(old_ports), old_matrix, old_phi
            for i in promoted:
                ports.append(i)
                promoted_matrix, _ = self.schur(old_active, ports)
                promoted_phi = self.normalized_determinant(promoted_matrix, ports)
                injection = promoted_matrix[-1][-1] / (self.bar * self.audit_matrix[i][i])
                assert 1 <= injection <= 1 / self.bar
                assert promoted_phi == previous_phi * injection
                self.audit_injection_product *= injection
                self.audit_injection_count += 1
                self.audit_counts["old_port_promotion_potential_checks"] += 1
                previous_matrix, previous_phi = promoted_matrix, promoted_phi
            indicator = [F(i in parents) for i in ports]
            selected = solve(previous_matrix, indicator)
            delta = self.audit_matrix[vertex][vertex] - self.gamma * self.gamma * sum(
                a * b for a, b in zip(indicator, selected)
            )
            ports.append(vertex)
            bordered_matrix, _ = self.schur(self.active, ports)
            bordered_phi = self.normalized_determinant(bordered_matrix, ports)
            injection = delta / (self.bar * self.audit_matrix[vertex][vertex])
            assert 1 <= injection <= 1 / self.bar
            assert bordered_phi == previous_phi * injection
            self.audit_injection_product *= injection
            self.audit_injection_count += 1
            self.audit_counts["new_vertex_border_potential_checks"] += 1
            if transient:
                i = next(iter(transient))
                drop = bordered_matrix[ports.index(i)][ports.index(i)] / (
                    self.bar * self.audit_matrix[i][i]
                )
                assert 1 <= drop <= 1 / self.bar
                assert phi == bordered_phi / drop
                self.audit_drop_product *= drop
                self.audit_transients += 1
                self.audit_counts["transient_elimination_potential_checks"] += 1
            else:
                assert phi == bordered_phi
        assert self.audit_injection_count == len(self.ports) + self.audit_transients
        assert phi == self.audit_injection_product / self.audit_drop_product
        bound = (1 / self.bar) ** (len(self.ports) + self.audit_transients)
        assert self.audit_drop_product <= self.audit_injection_product <= bound
        assert (
            self.audit_transients
            <= self.inverse_counts["cycle_birth_inverse_borders"]
            <= len(self.ports) - 1
        )
        assert F(4, 3) ** self.audit_large_updates <= bound
        self.audit_counts["global_exact_product_budget_checks"] += 1
        self.audit_counts["global_large_update_count_checks"] += 1


class ObservedExact(DowndateObserver, InverseState):
    pass


class ObservedPublication(DowndateObserver, PublicationState):
    pass


def check_case(graph, seed, alpha, epsilon, policy, published, counts, queries):
    gamma, lam = (1 - alpha) / (1 + alpha), epsilon / 2
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in graph]
    optimum = obstacle(matrix, load)
    if published:
        state = ObservedPublication(Oracle(graph), seed, alpha, epsilon, reverse_policy=policy)
    else:
        state = ObservedExact(Oracle(graph), seed, alpha, lam, reverse_parent=policy)
    state.audit_matrix, state.audit_load, state.audit_optimum = matrix, load, optimum
    state.audit_counts, state.audit_query_counts = counts, queries
    state.audit_last_point = [F(0)] * len(graph)
    got = state.run() if published else state.run(prefer_exception=policy)
    output = [got.get(i, F(0)) for i in graph]
    assert output == state.audit_last_point
    if not published:
        assert output == optimum
    residual = [F(i == seed) - sum(matrix[i][j] * output[j] for j in graph) for i in graph]
    assert all(0 <= residual[i] <= epsilon * graph.degree(i) for i in graph)
    assert state.oracle.rows == set(got)
    assert state.oracle.counts["adjacency_entries_inspected"] == sum(graph.degree(i) for i in got)
    counts["publication_traces" if published else "exact_gate_traces"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 2 <= args.max_n <= 7:
        parser.error("graph atlas enumeration requires 2 <= max_n <= 7")
    started, counts, queries = time.monotonic(), Counter(), Counter()
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= args.max_n and nx.is_connected(g)]
    parameters = [(F(1, 3), F(1, 10)), (F(1, 1009), F(1, 50))]
    for graph in graphs:
        for seed in graph:
            for alpha, epsilon in parameters:
                for policy in [False, True]:
                    for published in [False, True]:
                        check_case(graph, seed, alpha, epsilon, policy, published, counts, queries)
        print(
            json.dumps(
                {
                    "graph_n": len(graph),
                    "edges": len(graph.edges),
                    "traces": counts["exact_gate_traces"] + counts["publication_traces"],
                }
            ),
            flush=True,
        )
    result = {
        "audit": "incremental_active_set_sdd.coarse_schur_downdates",
        "arithmetic": "exact fractions, including determinant products; no logarithmic rounding",
        "random_seed": None,
        "graph": "all connected simple atlas graphs through max_n",
        "max_n": args.max_n,
        "graph_count": len(graphs),
        "seed": "every vertex",
        "parameters_alpha_epsilon": [[str(a), str(eps)] for a, eps in parameters],
        "lambda": "eps_appr/2",
        "policies": [
            "first tree parent, ordinary-first exact gate or FIFO publication queue",
            "last tree parent, exceptional-first exact gate or LIFO publication queue",
        ],
        "stopping_rule": "inherited original exact-gate or geometric-publication ACL certificate",
        "scope": "Reference observer only; no proposed fast approximate inverse or factor maintenance. All Schur/determinant calculations are independent original-matrix validation and cannot affect admissions.",
        "audit_only": dict(counts),
        "audit_only_selected_query_counts": dict(queries),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
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
            ]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
