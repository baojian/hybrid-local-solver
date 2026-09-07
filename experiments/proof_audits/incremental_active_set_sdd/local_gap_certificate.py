"""Exact local computable energy-gap certificate for the physical obstacle.

Only positive candidate rows are read. Original matrices and exact optima
are independent validators; this certificate does not produce a candidate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from diffusion_accuracy_bridge import objective
from geometric_value_events import obstacle
import networkx as nx


def sort_records(records, counts):
    """Bottom-up mergesort with one reusable buffer and explicit copies."""
    size = len(records)
    buffer = [None] * size
    counts["sort_buffer_words_allocated"] += size
    width = 1
    while width < size:
        for start in range(0, size, 2 * width):
            middle = min(start + width, size)
            end = min(start + 2 * width, size)
            i, j = start, middle
            for k in range(start, end):
                take_left = j == end
                if i < middle and j < end:
                    counts["label_comparisons"] += 1
                    take_left = records[i][0] <= records[j][0]
                if i < middle and take_left:
                    buffer[k] = records[i]
                    i += 1
                else:
                    buffer[k] = records[j]
                    j += 1
                counts["sort_reference_writes"] += 1
        records, buffer = buffer, records
        width *= 2
    return records


def certificate(oracle, candidate, seed, alpha, eps):
    """Candidate is a sparse iterable of distinct labels and positive values."""
    gamma = (1 - alpha) / (1 + alpha)
    bar, lam, delta = 1 - gamma, eps / 2, eps / 8
    counts = Counter()
    records = [(seed, F(0), F(1), None)]
    for i, value in candidate:
        assert value > 0
        degree = oracle.degree(i)
        records.append((i, value, -degree * value, degree))
        counts["candidate_words_read"] += 2
        for j in oracle.row(i):
            records.append((j, F(0), gamma * value, None))
            counts["neighbor_contribution_records"] += 1
    counts["record_words_allocated"] += 4 * len(records)
    records = sort_records(records, counts)
    total, repaired, terms = F(0), [], []
    for i, group in itertools.groupby(records, key=lambda r: r[0]):
        value, residual, degree, positives = F(0), F(0), None, 0
        for _, w, r, d in group:
            value += w
            residual += r
            if d is not None:
                degree = d
                positives += 1
            counts["grouped_record_visits"] += 1
        assert positives <= 1
        if degree is None:
            degree = oracle.degree(i)
        gradient, curvature = lam * degree - residual, bar * degree
        if gradient <= curvature * value:
            term = gradient * gradient / (2 * curvature)
            counts["interior_surrogate_minima"] += 1
        else:
            term = gradient * value - curvature * value * value / 2
            counts["zero_surrogate_minima"] += 1
        assert term >= 0
        total += term
        terms.append((i, value, residual, term))
        counts["certificate_record_words_allocated"] += 4
        if value > delta:
            repaired.append((i, value - delta))
            counts["clipped_output_words_allocated"] += 2
    threshold = bar * delta * delta / 2
    return {
        "value": total,
        "accepted": total <= threshold,
        "repaired": repaired,
        "terms": terms,
        "counts": counts,
    }


class RestrictedRows:
    def __init__(self, graph, allowed):
        self.graph, self.allowed = graph, set(allowed)
        self.counts = Counter()

    def degree(self, i):
        self.counts["original_degree_queries"] += 1
        return self.graph.degree(i)

    def row(self, i):
        assert i in self.allowed
        self.counts["positive_candidate_rows"] += 1
        for j in self.graph[i]:
            self.counts["original_adjacency_entries"] += 1
            yield j


def check_candidate(graph, matrix, b, exact, optimum, seed, alpha, eps, w, counts, work):
    gamma = (1 - alpha) / (1 + alpha)
    bar, smooth = 1 - gamma, 1 + gamma
    sparse = [(i, x) for i, x in enumerate(w) if x > 0]
    oracle = RestrictedRows(graph, [i for i, _ in sparse])
    cert = certificate(oracle, sparse, seed, alpha, eps)
    gap = objective(matrix, b, w) - optimum
    assert gap <= cert["value"] <= smooth * gap / bar
    assert (cert["value"] == 0) == (w == exact)
    touched = {seed}
    for i, _ in sparse:
        touched.add(i)
        touched.update(graph[i])
    assert oracle.counts["original_degree_queries"] == len(touched)
    assert oracle.counts["positive_candidate_rows"] == len(sparse)
    assert oracle.counts["original_adjacency_entries"] == sum(graph.degree(i) for i, _ in sparse)
    for i, value, residual, _ in cert["terms"]:
        assert value == w[i]
        assert residual == F(i == seed) - sum(a * x for a, x in zip(matrix[i], w))
    counts["independent_objective_gap_sandwiches"] += 1
    counts["complete_graph_access_certificates"] += 1
    if cert["accepted"]:
        out = dict(cert["repaired"])
        for i in graph:
            residual = F(i == seed) - sum(a * out.get(j, 0) for j, a in enumerate(matrix[i]))
            assert 0 <= residual <= eps * graph.degree(i)
            if out.get(i, 0):
                assert exact[i] > 0
        counts["accepted_original_ACL_certificates"] += 1
    else:
        counts["charged_failed_certificates"] += 1
    work.update(cert["counts"])
    work.update(oracle.counts)
    return cert


def run_case(graph, seed, alpha, eps, counts, work):
    gamma = (1 - alpha) / (1 + alpha)
    bar, smooth, lam, delta = 1 - gamma, 1 + gamma, eps / 2, eps / 8
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    b = [F(i == seed) - lam * graph.degree(i) for i in graph]
    exact = obstacle(matrix, b)
    optimum = objective(matrix, b, exact)
    eta = bar**3 * delta**2 / smooth
    for w in [[F(0)] * len(graph), exact, [x / 2 for x in exact], [2 * x for x in exact]]:
        check_candidate(graph, matrix, b, exact, optimum, seed, alpha, eps, w, counts, work)
    for i, sign in itertools.product(graph, [-1, 1]):
        step = F(1)
        while True:
            w = exact.copy()
            w[i] = max(F(0), w[i] + sign * step)
            if objective(matrix, b, w) <= optimum / (1 + eta):
                break
            step /= 2
            counts["reference_candidate_halvings"] += 1
        cert = check_candidate(graph, matrix, b, exact, optimum, seed, alpha, eps, w, counts, work)
        assert cert["accepted"]
        counts["relative_accuracy_guarantees_acceptance"] += 1
    counts["complete_original_graph_cases"] += 1


class ImplicitStar:
    """Vertex zero is a leaf seed; vertex one is an unread huge center."""

    def __init__(self, leaves):
        self.leaves, self.counts = leaves, Counter()

    def degree(self, i):
        assert i in [0, 1]
        self.counts["original_degree_queries"] += 1
        return self.leaves if i == 1 else 1

    def row(self, i):
        assert i == 0, "The huge center row must never be requested"
        self.counts["positive_candidate_rows"] += 1
        self.counts["original_adjacency_entries"] += 1
        return iter([1])


def implicit_cases():
    results = []
    for leaves in [16, 10**6, 10**12, 10**30]:
        oracle = ImplicitStar(leaves)
        alpha, eps, value = F(1, 3), F(1, 4), F(7, 8)
        cert = certificate(oracle, [(0, value)], 0, alpha, eps)
        assert cert["value"] == 0 and cert["accepted"]
        repaired = dict(cert["repaired"])[0]
        assert 0 <= 1 - repaired <= eps
        assert 0 <= repaired / 2 <= eps * leaves
        assert oracle.counts["original_adjacency_entries"] == 1
        results.append(
            {
                "ambient_leaves": leaves,
                "candidate_positive_volume": 1,
                "certificate": str(cert["value"]),
                "repaired_seed_value": str(repaired),
                "original_graph_access": dict(oracle.counts),
                "algorithm_counts": dict(cert["counts"]),
                "full_graph_validator": "Exact singleton KKT; center residual <= lambda*degree; all other leaves have zero residual. No center row requested.",
            }
        )
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, work = Counter(), Counter()
    max_n = 5 if args.full else 3
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed, alpha in itertools.product(graph, [F(1, 3), F(1, 1009), F(1008, 1009)]):
            d = graph.degree(seed)
            for eps in [F(1, 2 * d), F(1, d + 1), F(1, 8 * sum(dict(graph.degree()).values()))]:
                run_case(graph, seed, alpha, eps, counts, work)
    result = {
        "audit": "incremental_active_set_sdd.local_gap_certificate",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph_family": "all connected graph-atlas graphs of orders 2 through max_n; implicit huge-center stars",
        "max_n": max_n,
        "distinct_explicit_graphs": len(graphs),
        "physical_seed": "every explicit vertex; a leaf for the implicit stars",
        "alpha": ["1/3", "1/1009", "1008/1009"],
        "eps_appr": "1/(2*d_seed), 1/(d_seed+1), or 1/(8*original_total_volume); implicit eps=1/4",
        "stopping_rule": "computable separable gap upper bound <= bar_alpha*(eps_appr/8)^2/2",
        "relative_source_eta_for_guaranteed_acceptance": "bar_alpha^3*(eps_appr/8)^2/(1+gamma)",
        "scope": "Implemented local candidate certificate, not a candidate-producing local solver. Every positive candidate row, including false positives, is charged. Exact original matrices and candidate generation are validators.",
        "audit_only": dict(counts),
        "certificate_algorithm_and_access_counts": dict(work),
        "implicit_certificates": implicit_cases(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["diffusion_accuracy_bridge", "geometric_value_events"]
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
