"""Exact superlevel-potential and conditional small-alpha wrapper audit.

The native ACL producer and whole-graph numerical fallback are callbacks.
Dense obstacle/Neumann vectors are explicitly identified validators. The
production wrapper pays sparse maps, original degrees and support rows.
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

from geometric_value_events import mv
from local_gap_certificate import sort_records
from supplied_envelope_work import physical
import networkx as nx


def inspect_candidate(oracle, candidate, bound, need_closure, work):
    """The supplied callback promises positive sparse entries; reject bad ones."""
    work["candidate_header_and_word_cap_check"] += 3
    if candidate is None:
        return {"abort": "native_failure"}
    if len(candidate) > bound:
        return {"abort": "word_count"}
    records = sort_records(candidate, work)
    work["candidate_record_input_reads"] += 2 * len(records)
    for j, (label, value) in enumerate(records):
        work["sparse_value_and_distinctness_checks"] += 4
        if value <= 0 or (j and records[j - 1][0] >= label):
            return {"abort": "sparse_format"}
    labels = [row[0] for row in records]
    work["sorted_support_label_words"] += len(labels)

    def member(label):
        lo, hi = 0, len(labels)
        while lo < hi:
            mid = (lo + hi) // 2
            if labels[mid] < label:
                lo = mid + 1
            else:
                hi = mid
            work["support_membership_operations"] += 7
        work["support_membership_final_check"] += 3
        return lo < len(labels) and labels[lo] == label

    degrees, volume = [], 0
    for label in labels:
        degree = oracle.degree(label)
        assert degree >= 1
        degrees.append(degree)
        volume += degree
        work["degree_volume_pass_and_storage"] += 6
        if volume > bound:
            return {"abort": "volume"}
    result = {"abort": None, "records": records, "degrees": degrees, "volume": volume}
    if not need_closure or not labels:
        result["closure"] = None
        return result
    # The entire degree pass precedes the first adjacency query. A single
    # outside neighbor certifies proper support, so that scan can stop early.
    rows = []
    for label in labels:
        row = []
        for neighbor in oracle.row(label):
            if not member(neighbor):
                result["closure"] = False
                return result
            row.append(neighbor)
            work["materialized_internal_entry_copy_budget"] += 3
        rows.append(row)
        work["materialized_internal_row_headers"] += 2
    result["closure"], result["rows"] = True, rows
    return result


def transfer(oracle, seed, alpha, epsilon, bound, failure, native, fallback, work):
    assert 0 < alpha <= 1 and 0 < epsilon < 1 and bound >= 1 and 0 < failure < 1
    floor = epsilon / (4 * bound + epsilon)
    effective = max(alpha, floor)
    work["alpha_floor_arithmetic_and_callback_parameters"] += 10
    candidate = native(effective, epsilon / 2, failure / 2)
    result = inspect_candidate(oracle, candidate, bound, alpha < floor, work)
    if result["abort"]:
        return result
    result["effective_alpha"] = effective
    if alpha >= floor or not result["records"]:
        result["branch"] = "native"
        return result
    if result["closure"] is False:
        result["branch"] = "proper_transfer"
        return result
    # Every row and original degree of the connected ambient graph is now
    # supplied to this numerical callback. No further graph oracle is used.
    output = fallback(
        result["records"], result["degrees"], result["rows"], alpha, epsilon, failure / 2
    )
    work["whole_component_callback_and_output_header"] += 6
    if output is None:
        return {"abort": "fallback_failure"}
    if len(output) > len(result["records"]):
        return {"abort": "fallback_word_count"}
    output = sort_records(output, work)
    degrees, cursor = [], 0
    for index, (label, value) in enumerate(output):
        if value <= 0 or (index and output[index - 1][0] >= label):
            return {"abort": "fallback_sparse_format"}
        while cursor < len(result["records"]) and result["records"][cursor][0] < label:
            cursor += 1
            work["fallback_original_degree_map_merge"] += 4
        if cursor == len(result["records"]) or result["records"][cursor][0] != label:
            return {"abort": "fallback_unknown_label"}
        degrees.append(result["degrees"][cursor])
        work["fallback_output_validation_and_degree_copy"] += 12
    result = {
        "abort": None,
        "records": output,
        "degrees": degrees,
        "volume": sum(degrees),
        "effective_alpha": effective,
        "branch": "whole_component_fallback",
    }
    work["fallback_final_output_fields_and_volume_sum"] += 12 + 2 * len(degrees)
    return result


class LocalRows:
    def __init__(self, graph, work):
        self.graph, self.work, self.degree_log, self.row_log = graph, work, [], []

    def degree(self, vertex):
        self.degree_log.append(vertex)
        self.work["original_degree_queries"] += 1
        return self.graph.degree(vertex)

    def row(self, vertex):
        self.row_log.append(vertex)
        self.work["original_row_queries"] += 1
        for neighbor in self.graph[vertex]:
            self.work["original_adjacency_entries"] += 1
            yield neighbor


def check_potential(graph, seed, gamma, values, counts):
    residual = [
        F(i == seed) - graph.degree(i) * values[i] + gamma * sum(values[j] for j in graph[i])
        for i in graph
    ]
    assert all(value >= 0 for value in values) and all(r >= 0 for r in residual)
    support = {i for i in graph if values[i] > 0}
    for level in sorted(set([F(0)] + values)):
        above = {i for i in graph if values[i] > level}
        if not above:
            continue
        assert seed in above and nx.is_connected(graph.subgraph(above))
        flux = gamma * sum(values[i] - values[j] for i in above for j in graph[i] if j not in above)
        mass = (1 - gamma) * sum(graph.degree(i) * values[i] for i in above)
        assert 0 <= mass + flux == F(seed in above) - sum(residual[i] for i in above) <= 1
        counts["strict_superlevel_flux_and_connectivity_identities"] += 1
    for i, j in graph.edges:
        assert gamma * abs(values[i] - values[j]) <= 1
        counts["unit_source_edge_gradient_bounds"] += 1
    if len(support) < len(graph):
        assert max(values, default=F(0)) <= len(support) / gamma
        counts["proper_support_alpha_independent_maximum_bounds"] += 1
    counts["nonnegative_residual_potentials"] += 1
    return residual


def audit_case(graph, seed, alpha, epsilon, counts, work):
    bound, failure = 4 / epsilon, F(1, 8)
    access = LocalRows(graph, work)
    native_vector = []

    def native(effective, native_epsilon, delta):
        assert native_epsilon == epsilon / 2 and delta == failure / 2
        _, _, vector = physical(graph, seed, effective, native_epsilon)
        native_vector.extend(vector)
        counts["validator_native_dense_obstacle_solves"] += 1
        gamma = (1 - effective) / (1 + effective)
        residual = check_potential(graph, seed, gamma, vector, counts)
        assert all(r <= native_epsilon * graph.degree(i) for i, r in enumerate(residual))
        assert sum(graph.degree(i) for i in graph if vector[i] > 0) < bound
        return [(i, vector[i]) for i in reversed(list(graph)) if vector[i] > 0]

    def fallback(records, degrees, rows, target, target_epsilon, delta):
        labels = [label for label, _ in records]
        assert set(labels) == set(graph)
        assert degrees == [graph.degree(i) for i in labels]
        assert all(set(row) == set(graph[label]) for label, row in zip(labels, rows))
        assert target == alpha and target_epsilon == epsilon and delta == failure / 2
        _, _, vector = physical(graph, seed, target, target_epsilon)
        counts["validator_full_component_dense_fallbacks"] += 1
        return [(i, vector[i]) for i in graph if vector[i] > 0]

    result = transfer(access, seed, alpha, epsilon, bound, failure, native, fallback, work)
    assert result["abort"] is None
    output = [F(0)] * len(graph)
    for label, value in result["records"]:
        output[label] = value
    assert result["degrees"] == [graph.degree(label) for label, _ in result["records"]]
    matrix, _, _ = physical(graph, seed, alpha, epsilon)
    counts["validator_target_dense_systems"] += 1
    residual = [F(i == seed) - x for i, x in enumerate(mv(matrix, output))]
    assert all(0 <= r <= epsilon * graph.degree(i) for i, r in enumerate(residual))
    if result["branch"] == "proper_transfer":
        assert output == native_vector
        effective_gamma = (1 - result["effective_alpha"]) / (1 + result["effective_alpha"])
        target_gamma = (1 - alpha) / (1 + alpha)
        assert (target_gamma - effective_gamma) * bound / effective_gamma <= epsilon / 2
        counts["proper_same_vector_parameter_transfer_bounds"] += 1
    assert sum(graph.degree(i) for i in access.row_log) <= bound
    counts["original_ACL_output_certificates"] += 1
    counts["original_target_residual_rows"] += len(graph)
    counts["branch_" + result["branch"]] += 1


class HiddenHub:
    def __init__(self, degree, work):
        self._degree, self.work, self.rows = degree, work, []

    def degree(self, label):
        assert label in (0, 1)
        self.work["original_degree_queries"] += 1
        return 2 if label == 0 else self._degree

    def row(self, label):
        self.rows.append(label)
        raise AssertionError("The volume guard must reject before any row.")


def audit_guards(counts, work):
    for degree in [2**20, 2**80, 2**1024]:
        oracle = HiddenHub(degree, work)
        result = inspect_candidate(oracle, [(0, F(1)), (1, F(1))], F(16), True, work)
        assert result["abort"] == "volume" and oracle.rows == []
        counts["huge_degree_rejections_before_any_row"] += 1
    oracle = HiddenHub(2**80, work)
    for records, bound, expected in [
        (None, 4, "native_failure"),
        ([(0, F(1))] * 5, 4, "word_count"),
        ([(0, F(1)), (0, F(1))], 4, "sparse_format"),
        ([(0, F(0))], 4, "sparse_format"),
        ([(0, F(-1))], 4, "sparse_format"),
    ]:
        assert inspect_candidate(oracle, records, F(bound), True, work)["abort"] == expected
        counts["malformed_native_output_guards"] += 1
    assert not oracle.rows


def large_floor_subsolution(size, counts):
    """Analytic private path has 4*N^2+1 vertices; never materialize it."""
    n, epsilon = size, F(1, size**2)
    lam, gamma = epsilon / 4, 1 - epsilon

    def value(i):
        return F((n - i) ** 2, 4 * n) if 0 <= i < n else F(0)

    assert value(0) - gamma * value(1) <= 1 - lam
    for i in range(1, n):
        row = 2 * value(i) - gamma * (value(i - 1) + value(i + 1))
        assert row == -F(1, 2 * n) + F((n - i) ** 2 + 1, 2 * n**3)
        assert row <= -2 * lam
        counts["larger_floor_private_path_positive_subsolution_rows"] += 1
    # Full support would have volume 8*N^2, larger than 1/lambda=4*N^2.
    # At the seed, the target residual increases by delta_gamma*u_1.
    target_gamma = 1 - F(1, n**4)
    assert lam + (target_gamma - gamma) * value(1) > epsilon
    counts["larger_floor_proper_support_same_vector_obstructions"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= (5 if args.full else 3) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for epsilon in [F(1, 8), F(1, 4), F(3, 4)] if args.full else [F(1, 4)]:
                floor = epsilon / (16 / epsilon + epsilon)
                for alpha in (
                    [floor / 1024, floor, 2 * floor, F(1, 3)] if args.full else [floor / 16]
                ):
                    audit_case(graph, seed, alpha, epsilon, counts, work)
            gamma = F(1, 2)
            vector = [F(0)] * len(graph)
            for _ in range(8 if args.full else 3):
                vector = [
                    (F(i == seed) + gamma * sum(vector[j] for j in graph[i])) / graph.degree(i)
                    for i in graph
                ]
                check_potential(graph, seed, gamma, vector, counts)
                counts["validator_truncated_Neumann_vectors"] += 1
    for size in [16, 32, 64, 128, 256, 512] if args.full else [16]:
        large_floor_subsolution(size, counts)
    # The proper-support hypothesis cannot be dropped, even when r=0.
    graph, gamma = nx.path_graph(2), F(255, 256)
    vector = [1 / (1 - gamma**2), gamma / (1 - gamma**2)]
    check_potential(graph, 0, gamma, vector, counts)
    assert min(vector) > len(graph) / gamma
    counts["full_support_constant_component_counterexamples"] += 1
    audit_guards(counts, work)
    result = {
        "audit": "incremental_active_set_sdd.small_alpha_floor",
        "scope": "Exact superlevel bounds and paid conditional wrapper. Native ACL and supplied whole-component numerical callbacks remain explicit; dense references do not implement an OP3 local producer.",
        "arithmetic": "exact fractions; exact-real word accounting, not bit complexity",
        "parameters": {
            "full": args.full,
            "native_accuracy": "eps_appr/2",
            "native_reference_lambda": "eps_appr/4",
            "support_volume_bound": "B=4/eps_appr for the exact obstacle reference",
            "alpha_floor": "eps_appr/(4*B+eps_appr)",
            "failure_budget": "p/2 to each callback",
            "random_seed": None,
        },
        "audit_only": dict(counts),
        "charged_wrapper_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "geometric_value_events.py",
                "local_gap_certificate.py",
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
    print(
        json.dumps(
            {"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}, indent=2
        )
    )


if __name__ == "__main__":
    main()
