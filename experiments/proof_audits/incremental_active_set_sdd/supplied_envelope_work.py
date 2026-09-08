"""Paid original-degree preparation for a supplied significant envelope.

The envelope and numerical solver are not discovered or implemented here.
Dense physical/restricted optima are explicit validators. Construction
queries rows only in the supplied set and preserves original cut degrees.
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

from diffusion_accuracy_bridge import objective
from geometric_value_events import mv, obstacle
from local_gap_certificate import sort_records
from spectral_preconditioner_floor import laplacian
import networkx as nx


class SuppliedRows:
    def __init__(self, graph, allowed, seed, counts):
        self.graph, self.allowed, self.seed, self.counts = graph, set(allowed), seed, counts
        self.queried = []

    def degree(self, vertex):
        assert vertex in self.allowed or vertex == self.seed
        self.counts["original_degree_queries"] += 1
        return self.graph.degree(vertex)

    def row(self, vertex):
        assert vertex in self.allowed
        self.queried.append(vertex)
        self.counts["original_rows_queried"] += 1
        for neighbor in self.graph[vertex]:
            self.counts["original_adjacency_entries"] += 1
            yield neighbor


def prepare(oracle, labels, seed, alpha, epsilon, work, volume_cap=None):
    assert 0 < alpha <= 1 and 0 < epsilon < 1
    gamma = (1 - alpha) / (1 + alpha)
    bar, lam, delta = 1 - gamma, epsilon / 2, epsilon / 8
    seed_degree = oracle.degree(seed)
    work["seed_gate_arithmetic_reads_and_comparisons"] += 10
    if epsilon * seed_degree >= gamma / (1 + gamma):
        value = max(F(0), F(1, seed_degree) - epsilon)
        work["seed_gate_output_words_and_arithmetic"] += 6
        return {"shortcut": [(seed, value)] if value else [], "abort": None}
    assert gamma > epsilon
    records = [(v,) for v in labels]
    work["supplied_label_records_and_copy_budget"] += 4 * len(labels)
    records = sort_records(records, work)
    ordered = [row[0] for row in records]
    work["ordered_label_output_words"] += len(ordered)
    for i in range(1, len(ordered)):
        assert ordered[i - 1] < ordered[i]
        work["distinct_supplied_label_checks"] += 1

    def index(vertex):
        lo, hi = 0, len(ordered)
        while lo < hi:
            mid = (lo + hi) // 2
            if ordered[mid] < vertex:
                lo = mid + 1
            else:
                hi = mid
            work["label_membership_search_operations"] += 7
        work["label_membership_final_comparison"] += 3
        return lo if lo < len(ordered) and ordered[lo] == vertex else None

    seed_index = index(seed)
    if seed_index is None:
        return {"abort": "missing_seed"}
    degrees, volume = [], 0
    for v in ordered:
        degree = seed_degree if v == seed else oracle.degree(v)
        assert degree >= 1
        degrees.append(degree)
        volume += degree
        work["original_degree_storage_sum_and_copy_budget"] += 6
        if volume_cap is not None and volume > volume_cap:
            return {"abort": "volume"}
    n, inside, edges, adjacency = len(ordered), [0] * len(ordered), [], [[] for _ in ordered]
    work["induced_degree_and_adjacency_header_words"] += 3 * n
    for i, v in enumerate(ordered):
        entries = 0
        for neighbor in oracle.row(v):
            entries += 1
            j = index(neighbor)
            if j is not None:
                inside[i] += 1
                adjacency[i].append(j)
                work["induced_incidence_words_and_copy_budget"] += 5
                if i < j:
                    edges.append((i, j, gamma))
                    work["induced_edge_records_and_copy_budget"] += 9
            work["original_row_scan_state_operations"] += 3
        assert entries == degrees[i]
    seen, stack, component = [False] * n, [seed_index], []
    seen[seed_index] = True
    work["component_visit_and_stack_header_words"] += n + 2
    while stack:
        vertex = stack.pop()
        component.append(vertex)
        for neighbor in adjacency[vertex]:
            if not seen[neighbor]:
                seen[neighbor] = True
                stack.append(neighbor)
                work["component_discovery_words_and_copy_budget"] += 5
            work["component_incidence_reads_and_checks"] += 2
        work["component_output_words_and_copy_budget"] += 4
    remap = [-1] * n
    for j, vertex in enumerate(component):
        remap[vertex] = j
    work["component_relabel_array_and_assignments"] += n + len(component)
    comp_edges = []
    for i, j, c in edges:
        if remap[i] >= 0:
            assert remap[j] >= 0
            comp_edges.append((remap[i], remap[j], c))
            work["component_edge_words_and_copy_budget"] += 9
        work["component_edge_selection_reads"] += 4
    comp_labels, grounding, load, comp_degrees = [], [], [], []
    for vertex in component:
        v, degree = ordered[vertex], degrees[vertex]
        h = degree - gamma * inside[vertex]
        assert h >= bar * degree > 0
        comp_labels.append(v)
        comp_degrees.append(degree)
        grounding.append(h)
        load.append(F(v == seed) - lam * degree)
        work["physical_coefficient_arithmetic_and_copy_budget"] += 20
    cap, target, bound = 1 / bar, bar * delta * delta / 2, 1 / (2 * bar)
    final_slopes = [h * cap - f for h, f in zip(grounding, load)]
    assert all(s >= 0 for s in final_slopes)
    parameter = 1 + volume + 1 / bar + 1 / epsilon
    z = 256 * parameter**4
    quantities = {
        "radius": max(F(1), cap),
        "terminal_positive_mass": sum(final_slopes, F(0)),
        "largest_curvature_sum": sum(grounding, F(0)),
        "graph_weight_sum": sum((c for _, _, c in comp_edges), F(0)),
        "inverse_minimum_graph_weight": 1 / gamma if comp_edges else F(1),
        "energy_bound_plus_one": bound + 1,
        "inverse_absolute_target": 1 / target,
    }
    assert all(0 <= value <= z for value in quantities.values())
    work["two_piece_embedding_range_arithmetic_and_output_words"] += 20 * len(component) + 60
    return {
        "abort": None,
        "labels": comp_labels,
        "degrees": comp_degrees,
        "grounding": grounding,
        "load": load,
        "edges": comp_edges,
        "cap": cap,
        "target": target,
        "energy_bound": bound,
        "volume": volume,
        "Z": z,
        "range_quantities": quantities,
    }


def physical(graph, seed, alpha, epsilon):
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - epsilon * graph.degree(i) / 2 for i in graph]
    return matrix, load, obstacle(matrix, load)


def audit_case(graph, seed, alpha, epsilon, counts, work):
    matrix, _, exact = physical(graph, seed, alpha, epsilon)
    counts["validator_full_physical_obstacle_solves"] += 1
    delta = epsilon / 8
    mandatory = {i for i in graph if exact[i] > delta}
    optional = [i for i in graph if i not in mandatory]
    profiles = [mandatory, set(graph), mandatory | set(optional[::2])]
    for supplied in profiles:
        access = SuppliedRows(graph, supplied, seed, work)
        before_rows = work["original_adjacency_entries"]
        result = prepare(access, list(reversed(sorted(supplied))), seed, alpha, epsilon, work)
        assert result["abort"] is None
        counts["supplied_envelope_preparations"] += 1
        if "shortcut" in result:
            actual = [F(0)] * len(graph)
            for vertex, value in result["shortcut"]:
                actual[vertex] = value
            assert work["original_adjacency_entries"] == before_rows
            counts["one_degree_shortcuts_before_envelope_reads"] += 1
        else:
            labels = result["labels"]
            expected_component = nx.node_connected_component(graph.subgraph(supplied), seed)
            assert set(labels) == expected_component
            assert set(access.queried) == supplied
            assert work["original_adjacency_entries"] - before_rows == sum(
                graph.degree(i) for i in supplied
            )
            assert len(access.queried) == len(supplied)
            local = laplacian(len(labels), result["edges"])
            for i, h in enumerate(result["grounding"]):
                local[i][i] += h
            assert local == [[matrix[i][j] for j in labels] for i in labels]
            counts["original_degree_principal_matrix_identities"] += 1
            counts["cut_grounding_positive_vertices"] += sum(
                result["grounding"][i] > (2 * alpha / (1 + alpha)) * graph.degree(v)
                for i, v in enumerate(labels)
            )
            counts["off_seed_component_coordinates_discarded"] += len(supplied) - len(labels)
            v = obstacle(local, result["load"])
            optimum = objective(local, result["load"], v)
            assert -result["energy_bound"] <= optimum <= 0
            assert all(0 <= x <= result["cap"] for x in v)
            # A dense numerical provider is only a validator. Choose a
            # nonzero feasible error and halve until the absolute gap passes.
            step = delta / 2
            while True:
                candidate = v.copy()
                candidate[0] += step
                gap = objective(local, result["load"], candidate) - optimum
                if gap <= result["target"]:
                    break
                step /= 2
                counts["validator_absolute_error_halvings"] += 1
            boxed = [min(result["cap"], x) for x in candidate]
            assert objective(local, result["load"], boxed) - optimum <= result["target"]
            assert max(abs(a - b) for a, b in zip(boxed, v)) <= delta
            actual = [F(0)] * len(graph)
            for vertex, value in zip(labels, boxed):
                actual[vertex] = max(F(0), value - delta)
            counts["supplied_absolute_solver_reference_compositions"] += 1
            counts["global_parameter_bound_quantities_checked"] += len(result["range_quantities"])
        residual = [F(i == seed) - y for i, y in enumerate(mv(matrix, actual))]
        assert all(0 <= r <= epsilon * graph.degree(i) for i, r in enumerate(residual))
        counts["original_ACL_certificates_after_preparation"] += 1
        counts["validator_full_original_residual_rows"] += len(graph)


class MassiveHub:
    """A private huge star, with the source at a leaf; no graph is built."""

    def __init__(self, degree, counts):
        self._degree, self.counts, self.rows = degree, counts, []

    def degree(self, vertex):
        self.counts["original_degree_queries"] += 1
        assert vertex in (0, 1)
        return 1 if vertex == 0 else self._degree

    def row(self, vertex):
        assert vertex == 0, "The huge outside hub row must never be read."
        self.rows.append(vertex)
        self.counts["original_rows_queried"] += 1
        self.counts["original_adjacency_entries"] += 1
        yield 1


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
            for alpha in (
                [F(1), F(1, 3), F(1, 17), F(1, 2**80), 1 - F(1, 2**80)] if args.full else [F(1, 3)]
            ):
                for epsilon in [F(1, 4), F(1, 2), F(3, 4)] if args.full else [F(1, 4), F(3, 4)]:
                    audit_case(graph, seed, alpha, epsilon, counts, work)
    for degree in [2**20, 2**80, 2**1024]:
        access = MassiveHub(degree, work)
        result = prepare(access, [0], 0, F(1, 3), F(1, 4), work)
        assert result["labels"] == [0] and result["grounding"] == [F(1)]
        assert result["volume"] == 1 and access.rows == [0]
        # The supplied envelope is valid on this family: only the seed is
        # positive at lambda=1/8, and the hub's original KKT row is slack.
        value = F(7, 8)
        assert F(1, 2) * value <= F(1, 8) * degree
        counts["private_huge_ambient_star_envelopes"] += 1
        counts["ambient_size_independent_parameter_bounds"] += 1
        limited = MassiveHub(degree, work)
        aborted = prepare(limited, [0, 1], 0, F(1, 3), F(1, 4), work, volume_cap=16)
        assert aborted["abort"] == "volume" and not limited.rows
        counts["excess_volume_rejected_before_any_row"] += 1
    for n in [16, 32] if args.full else [12]:
        for shape in ["path", "cycle"]:
            graph = nx.path_graph(n) if shape == "path" else nx.cycle_graph(n)
            audit_case(graph, 0, F(1, 1000003), F(1, 4), counts, work)
    result = {
        "audit": "incremental_active_set_sdd.supplied_envelope_work",
        "scope": "Paid original-degree induced-component preparation, parameter bounds and ACL repair from a supplied significant envelope. Dense numerical solutions are validators; no envelope finder or full source-backed VWF solver is implemented.",
        "arithmetic": "exact fractions; exact-real word work, not bit complexity",
        "parameters": {
            "full": args.full,
            "lambda": "eps_appr/2",
            "delta": "eps_appr/8",
            "absolute_gap": "bar_alpha*delta^2/2",
            "Z": "256*(1+V+1/bar_alpha+1/eps_appr)^4",
            "random_seed": None,
        },
        "audit_only": dict(counts),
        "charged_preparation_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "geometric_value_events.py",
                "diffusion_accuracy_bridge.py",
                "local_gap_certificate.py",
                "spectral_preconditioner_floor.py",
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
