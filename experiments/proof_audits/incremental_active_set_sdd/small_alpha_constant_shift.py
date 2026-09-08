"""Exact audit of a constant-shift full-support alpha-floor repair.

Only the native ACL vector is supplied by a numerical validator. The
full-support repair is implemented arithmetic on paid materialized rows;
it does not invoke a second solver or inspect the outside graph.
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

from small_alpha_floor import LocalRows, transfer
from supplied_envelope_work import physical
import networkx as nx


def full_support_shift(records, degrees, rows, seed, alpha, work):
    assert 0 < alpha <= 1
    gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
    labels = [row[0] for row in records]
    values = [row[1] for row in records]
    work["full_shift_supplied_record_reads_and_output_arrays"] += 4 * len(records) + 8

    def locate(label):
        lo, hi = 0, len(labels)
        while lo < hi:
            mid = (lo + hi) // 2
            if labels[mid] < label:
                lo = mid + 1
            else:
                hi = mid
            work["full_shift_neighbor_lookup_operations"] += 7
        work["full_shift_neighbor_lookup_final_comparison"] += 3
        assert lo < len(labels) and labels[lo] == label
        return lo

    normalized = []
    for i, (label, degree, row) in enumerate(zip(labels, degrees, rows)):
        total = F(0)
        for neighbor in row:
            total += values[locate(neighbor)]
            work["full_shift_adjacency_reads_and_sums"] += 3
        residual = F(label == seed) - degree * values[i] + gamma * total
        normalized.append(residual / degree)
        work["full_shift_original_residual_normalization"] += 10
    minimum = min(normalized)
    work["full_shift_minimum_and_domain_guard"] += 2 * len(normalized) + 4
    if minimum < 0:
        return None
    constant = minimum / bar
    output = [(label, value + constant) for label, value in records]
    work["full_shift_exact_constant_and_output_copy_budget"] += 6 * len(records) + 3
    return output


def shift_transfer(oracle, seed, alpha, epsilon, bound, failure, native, work):
    calls = []

    def arithmetic_callback(records, degrees, rows, target, accuracy, delta):
        assert target == alpha and accuracy == epsilon and delta == failure / 2
        calls.append(1)
        return full_support_shift(records, degrees, rows, seed, target, work)

    result = transfer(
        oracle, seed, alpha, epsilon, bound, failure, native, arithmetic_callback, work
    )
    if result.get("branch") == "whole_component_fallback":
        result["branch"] = "whole_component_constant_shift"
    assert len(calls) <= 1
    return result


def residual(graph, seed, alpha, vector):
    gamma = (1 - alpha) / (1 + alpha)
    return [
        F(i == seed) - graph.degree(i) * vector[i] + gamma * sum(vector[j] for j in graph[i])
        for i in graph
    ]


def audit_case(graph, seed, epsilon, counts, work, tiny_bits):
    bound, confidence = 4 / epsilon, F(1, 8)
    floor = epsilon / (4 * bound + epsilon)
    _, _, original = physical(graph, seed, floor, epsilon / 2)
    counts["validator_native_obstacle_solves"] += 1
    variants = [original]
    if original[seed] > 0:
        altered = original.copy()
        altered[seed] += epsilon / 32
        variants.append(altered)
    if min(original) > 0:
        bar = 2 * floor / (1 + floor)
        variants.append([value + epsilon / (32 * bar) for value in original])
    for vector in variants:
        native_residual = residual(graph, seed, floor, vector)
        assert all(0 <= r <= epsilon * graph.degree(i) / 2 for i, r in enumerate(native_residual))
        assert sum(graph.degree(i) for i in graph if vector[i] > 0) < bound
        gamma_floor = (1 - floor) / (1 + floor)
        assert gamma_floor * (max(vector) - min(vector)) <= len(graph) - 1
        counts["global_oscillation_bounds_including_full_support"] += 1
        for alpha in [floor, floor / 1024, F(1, 2**tiny_bits)]:
            assert alpha <= floor
            access = LocalRows(graph, work)

            def native(effective, accuracy, failure):
                assert effective == floor and accuracy == epsilon / 2 and failure == confidence / 2
                counts["native_reference_callback_returns"] += 1
                return [(i, vector[i]) for i in reversed(list(graph)) if vector[i] > 0]

            result = shift_transfer(access, seed, alpha, epsilon, bound, confidence, native, work)
            assert result["abort"] is None
            output = [F(0)] * len(graph)
            for label, value in result["records"]:
                output[label] = value
            target_residual = residual(graph, seed, alpha, output)
            assert all(0 <= r <= epsilon * graph.degree(i) for i, r in enumerate(target_residual))
            assert sum(graph.degree(i) for i in access.row_log) <= bound
            counts["original_ACL_output_certificates"] += 1
            counts["original_target_residual_rows"] += len(graph)
            counts["branch_" + result["branch"]] += 1
            if result["branch"] == "whole_component_constant_shift":
                assert min(vector) > 0 and set(access.row_log) == set(graph)
                constant = output[0] - vector[0]
                assert constant >= 0 and all(a - b == constant for a, b in zip(output, vector))
                before = residual(graph, seed, alpha, vector)
                before_normalized = [r / graph.degree(i) for i, r in enumerate(before)]
                after_normalized = [r / graph.degree(i) for i, r in enumerate(target_residual)]
                width = max(before_normalized) - min(before_normalized)
                assert min(after_normalized) == 0 and max(after_normalized) == width <= epsilon
                bar = 2 * alpha / (1 + alpha)
                assert 0 <= bar * sum(graph.degree(i) * output[i] for i in graph) <= 1
                counts["exact_constant_corrections_and_residual_widths"] += 1
                counts["normalized_output_mass_bounds"] += 1
                counts["largest_shift_numerator_bits"] = max(
                    counts["largest_shift_numerator_bits"], constant.numerator.bit_length()
                )
            else:
                assert output == vector


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
                audit_case(graph, seed, epsilon, counts, work, 1024 if args.full else 80)
    graph = nx.path_graph(2)
    for alpha in [F(1, 2**k) for k in [80, 1024, 4096]]:
        records = [(0, F(1000)), (1, F(1))]
        assert full_support_shift(records, [1, 1], [[1], [0]], 0, alpha, work) is None
        counts["negative_original_residual_guard_rejections"] += 1
    result = {
        "audit": "incremental_active_set_sdd.small_alpha_constant_shift",
        "scope": "Implemented deterministic arithmetic full-support repair for the conditional alpha floor. Native ACL output is an explicit dense reference; no envelope finder or near-linear native local producer is inferred.",
        "arithmetic": "exact fractions; exact-real word accounting, not bit complexity or floating-point stability",
        "parameters": {
            "full": args.full,
            "native_accuracy": "eps_appr/2",
            "native_reference_lambda": "eps_appr/4",
            "volume_bound": "B=4/eps_appr",
            "alpha_floor": "eps_appr/(4*B+eps_appr)",
            "constant_correction": "min_i((e_v-M_target*x)_i/d_i)/bar_alpha_target",
            "random_seed": None,
        },
        "audit_only": dict(counts),
        "charged_wrapper_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "small_alpha_floor.py",
                "supplied_envelope_work.py",
                "geometric_value_events.py",
                "local_gap_certificate.py",
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
