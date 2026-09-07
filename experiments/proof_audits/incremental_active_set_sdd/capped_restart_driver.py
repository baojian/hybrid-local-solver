"""Exact audit of a gap-certified restarted driver on a supplied original graph.

The driver calls a relative proximal oracle. This audit substitutes dense
exact piece solves and controlled perturbations, whose work is explicitly
validator-only. No fast inner oracle or unknown-support discovery is claimed.
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

from capped_proximal_budget import capped_energy, dense_laplacian, instance, trajectory
from diffusion_accuracy_bridge import objective
from geometric_value_events import obstacle
from local_gap_certificate import RestrictedRows, certificate
import networkx as nx


def rational_record(value):
    numerator, denominator = abs(value.numerator), value.denominator
    nb, db = numerator.bit_length(), denominator.bit_length()
    if max(nb, db) < 12000:
        return str(value)
    raw_n = numerator.to_bytes((nb + 7) // 8, "big")
    raw_d = denominator.to_bytes((db + 7) // 8, "big")
    payload = len(raw_n).to_bytes(8, "big") + raw_n + raw_d
    return {
        "sign": -1 if value < 0 else 1,
        "numerator_bits": nb,
        "denominator_bits": db,
        "absolute_fraction_bytes_sha256": hashlib.sha256(payload).hexdigest(),
        "encoding": "8-byte big-endian numerator-byte-length, unsigned numerator bytes, unsigned denominator bytes",
    }


def driver_case(graph, seed, alpha, eps, kappa, counts, work, proximal_work):
    n, bar, ge, he, grounding, load = instance(graph, seed, alpha, eps, kappa)
    g = dense_laplacian(n, ge)
    matrix = [row.copy() for row in g]
    for i in graph:
        matrix[i][i] += grounding[i]
    exact = obstacle(matrix, load)
    minimum = objective(matrix, load, exact)
    gamma, cap = 1 - bar, 1 / bar
    threshold = bar * (eps / 8) ** 2 / 2
    floor = bar * threshold / (1 + gamma)
    upper, maximum_calls = 1 / (2 * bar), 0
    while upper > floor:
        upper /= 32
        maximum_calls += 1
        work["maximum_call_budget_divisions"] += 1
    work["supplied_input_vertex_records"] += n
    work["supplied_input_edge_records"] += len(ge) + len(he)
    current, calls = [F(0)] * n, 0
    work["initial_zero_vector_entries"] += n
    while True:
        sparse = [(i, t) for i, t in enumerate(current) if t > 0]
        access = RestrictedRows(graph, [i for i, _ in sparse])
        cert = certificate(access, sparse, seed, alpha, eps)
        work.update(cert["counts"])
        work.update(access.counts)
        work["sparse_candidate_entries_emitted"] += 2 * len(sparse)
        gap = objective(matrix, load, current) - minimum
        assert 0 <= gap <= cert["value"] <= (1 + gamma) * gap / bar
        assert capped_energy(g, grounding, cap, load, current) == minimum + gap <= 0
        counts["original_guard_gap_sandwiches"] += 1
        if cert["accepted"]:
            repaired = dict(cert["repaired"])
            for i in graph:
                residual = F(i == seed) - sum(
                    a * repaired.get(j, 0) for j, a in enumerate(matrix[i])
                )
                assert 0 <= residual <= eps * graph.degree(i)
                assert repaired.get(i, 0) == 0 or exact[i] > 0
            counts["complete_original_ACL_certificates"] += 1
            break
        assert gap > floor
        counts["failed_guards_with_known_positive_gap_floor"] += 1
        assert calls < maximum_calls
        candidate, _ = trajectory(
            graph,
            seed,
            alpha,
            eps,
            kappa,
            "relative",
            counts,
            proximal_work,
            initial=current,
            gap_floor=floor,
        )
        boxed = [min(cap, t) for t in candidate]
        counts["post_run_boxed_coordinates"] += sum(a != b for a, b in zip(candidate, boxed))
        assert objective(matrix, load, boxed) <= capped_energy(g, grounding, cap, load, candidate)
        assert objective(matrix, load, boxed) - minimum <= gap / 32
        work["boxed_restart_entries_allocated"] += n
        current = boxed
        calls += 1
    counts["complete_gap_certified_drivers"] += 1
    counts["drivers_requiring_multiple_runs"] += calls > 1
    return {
        "vertices": n,
        "edges": len(ge),
        "physical_seed": seed,
        "alpha": str(alpha),
        "eps_appr": str(eps),
        "kappa": str(kappa),
        "actual_accelerated_runs": calls,
        "known_maximum_runs": maximum_calls,
        "known_gap_floor": str(floor),
        "accepted_certificate_value": rational_record(cert["value"]),
        "certificate_threshold": str(threshold),
        "output_support_size": len(cert["repaired"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work, proximal_work = time.monotonic(), Counter(), Counter(), Counter()
    max_n = 5 if args.full else 3
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_connected(g)]
    histogram = Counter()
    for graph in graphs:
        for seed in graph:
            for alpha, kappa in (
                [(F(1, 3), F(9, 4)), (F(1, 1009), F(4))] if args.full else [(F(1, 1009), F(4))]
            ):
                result = driver_case(
                    graph,
                    seed,
                    alpha,
                    F(1, 8 * sum(dict(graph.degree()).values())),
                    kappa,
                    counts,
                    work,
                    proximal_work,
                )
                histogram[result["actual_accelerated_runs"]] += 1
    structured = []
    for graph in (
        [nx.path_graph(5), nx.star_graph(4), nx.cycle_graph(5)] if args.full else [nx.path_graph(3)]
    ):
        structured.append(
            driver_case(graph, 0, F(1, 1009), F(1, 2**30), F(16), counts, work, proximal_work)
        )
    result = {
        "audit": "incremental_active_set_sdd.capped_restart_driver",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "max_n": max_n,
        "distinct_atlas_graphs": len(graphs),
        "graph_family": "connected atlas graphs through max_n, every physical seed; tiny-epsilon path/star/cycle restart cases",
        "parameter_profiles": "eps=1/(8*volume), (alpha,kappa)=(1/3,9/4),(1/1009,4); fast uses second. Structured alpha=1/1009,kappa=16,eps=2^-30.",
        "stopping_rule": "Original local gap certificate <=bar*(eps/8)^2/2; otherwise its sandwich supplies floor=bar*threshold/(1+gamma). Run fixed-original-objective APG with that known floor, box at 1/bar and restart. Every failed guard, sparse record, positive row and supplied-graph oracle call is charged.",
        "scope": "Conditional supplied-graph outer driver with an implemented original stopping rule. Relative proximal candidates are dense exact validators; no fast inner oracle, preconditioner constructor, recursive solver or local OP3 complexity theorem is asserted.",
        "audit_only": dict(counts),
        "driver_counts": dict(work),
        "supplied_proximal_counts": dict(proximal_work),
        "atlas_run_count_histogram": dict(histogram),
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "capped_proximal_budget",
                "diffusion_accuracy_bridge",
                "geometric_value_events",
                "local_gap_certificate",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
