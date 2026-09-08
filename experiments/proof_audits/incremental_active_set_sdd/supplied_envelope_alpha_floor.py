"""Exact alpha-independent work reduction for a supplied target envelope.

The numerical VWF solver is a callback, exercised by a dense validator.
Production preparation, original-degree access, clipping, volume guards
and the full-support constant correction are implemented and charged.
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
from geometric_value_events import obstacle
from small_alpha_constant_shift import full_support_shift, residual
from small_alpha_floor import inspect_candidate
from spectral_preconditioner_floor import laplacian
from supplied_envelope_work import MassiveHub, SuppliedRows, physical, prepare
import networkx as nx


def solve_supplied(oracle, labels, seed, alpha, epsilon, failure, numerical, work):
    assert 0 < alpha <= 1 and 0 < epsilon < 1 and 0 < failure < 1
    bound, delta, native_accuracy = 2 / epsilon, epsilon / 8, 7 * epsilon / 8
    floor = epsilon**2 / (32 + epsilon**2)
    effective = max(alpha, floor)
    work["effective_alpha_and_reserved_residual_margin"] += 15
    prepared = prepare(
        oracle, labels, seed, effective, epsilon, work, gate_accuracy=native_accuracy
    )
    if prepared["abort"]:
        return prepared
    if "shortcut" in prepared:
        native = prepared["shortcut"]
    else:
        raw = numerical(prepared, failure)
        work["numerical_callback_output_shape_check"] += 4
        if raw is None or len(raw) != len(prepared["labels"]):
            return {"abort": "numerical_failure"}
        native = []
        for label, value in zip(prepared["labels"], raw):
            if value < 0:
                return {"abort": "numerical_infeasibility"}
            clipped = max(F(0), min(prepared["cap"], value) - delta)
            if clipped:
                native.append((label, clipped))
                work["native_sparse_output_record_copy_budget"] += 5
            work["native_boxing_clipping_and_sign_checks"] += 8
    result = inspect_candidate(oracle, native, bound, alpha < floor, work)
    if result["abort"]:
        return result
    if alpha >= floor or not native:
        result["branch"] = "effective_equals_target_or_empty"
    elif result["closure"] is False:
        result["branch"] = "proper_same_potential"
    else:
        corrected = full_support_shift(
            result["records"], result["degrees"], result["rows"], seed, alpha, work
        )
        if corrected is None:
            return {"abort": "negative_target_residual"}
        # The correction preserves every full-support label and its order.
        result["records"] = corrected
        result["branch"] = "full_support_constant_shift"
    result["effective_alpha"], result["native_records"] = effective, native
    work["final_supplied_envelope_output_fields"] += 6
    return result


def audit_case(graph, seed, alpha, epsilon, counts, work):
    _, _, original = physical(graph, seed, alpha, epsilon)
    counts["validator_original_target_obstacle_solves"] += 1
    floor = epsilon**2 / (32 + epsilon**2)
    effective = max(alpha, floor)
    _, _, effective_optimum = physical(graph, seed, effective, epsilon)
    assert all(a <= b for a, b in zip(effective_optimum, original))
    counts["same_lambda_obstacle_parameter_monotonicity_checks"] += 1
    delta = epsilon / 8
    required = {i for i in graph if original[i] > delta}
    optional = [i for i in graph if i not in required]
    for supplied in [required, set(graph), required | set(optional[::2])]:
        access = SuppliedRows(graph, supplied, seed, work)
        degree_reads_before = work["original_degree_queries"]

        def numerical(prepared, confidence):
            assert confidence == F(1, 8)
            local = laplacian(len(prepared["labels"]), prepared["edges"])
            for i, h in enumerate(prepared["grounding"]):
                local[i][i] += h
            optimum = obstacle(local, prepared["load"])
            energy = objective(local, prepared["load"], optimum)
            # A deliberately nonzero feasible error tests the reserved margin.
            step = delta / 2
            while True:
                output = optimum.copy()
                output[0] += step
                if objective(local, prepared["load"], output) - energy <= prepared["target"]:
                    break
                step /= 2
                counts["validator_absolute_error_halvings"] += 1
            counts["validator_supplied_numerical_callbacks"] += 1
            return output

        result = solve_supplied(
            access, list(reversed(sorted(supplied))), seed, alpha, epsilon, F(1, 8), numerical, work
        )
        assert result["abort"] is None
        native, actual = [F(0)] * len(graph), [F(0)] * len(graph)
        for label, value in result["native_records"]:
            native[label] = value
        for label, value in result["records"]:
            actual[label] = value
        assert all(value >= 0 for value in actual)
        nr = residual(graph, seed, effective, native)
        assert all(0 <= r <= 7 * epsilon * graph.degree(i) / 8 for i, r in enumerate(nr))
        target_residual = residual(graph, seed, alpha, actual)
        assert all(0 <= r <= epsilon * graph.degree(i) for i, r in enumerate(target_residual))
        assert all(original[i] > 0 for i in graph if actual[i] > 0)
        assert sum(graph.degree(i) for i in graph if actual[i] > 0) < 2 / epsilon
        assert set(access.queried) <= supplied
        assert sum(graph.degree(i) for i in access.queried) <= 2 * sum(
            graph.degree(i) for i in supplied
        )
        assert work["original_degree_queries"] - degree_reads_before <= 2 * len(supplied) + 2
        counts["native_reserved_margin_certificates"] += 1
        counts["original_target_ACL_and_support_certificates"] += 1
        counts["original_target_residual_rows"] += len(graph)
        counts["branch_" + result["branch"]] += 1
        if result["branch"] == "full_support_constant_shift":
            assert min(native) > 0
            shift = actual[0] - native[0]
            assert all(x - y == shift for x, y in zip(actual, native))
            counts["largest_shift_numerator_bits"] = max(
                counts["largest_shift_numerator_bits"], shift.numerator.bit_length()
            )


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
                for alpha in (
                    [F(1, 2**1024), F(1, 2**80), F(1, 3), 1 - F(1, 2**80)]
                    if args.full
                    else [F(1, 2**80)]
                ):
                    audit_case(graph, seed, alpha, epsilon, counts, work)
    for n in [16, 32, 64] if args.full else [12]:
        for graph in [nx.path_graph(n), nx.cycle_graph(n)]:
            audit_case(graph, 0, F(1, 2**80), F(1, 4), counts, work)
    for ambient_degree in [2**20, 2**80, 2**1024]:
        access = MassiveHub(ambient_degree, work)

        def scalar(prepared, confidence):
            assert confidence == F(1, 8) and prepared["labels"] == [0]
            assert prepared["grounding"] == [F(1)]
            return [F(7, 8)]

        result = solve_supplied(access, [0], 0, F(1, 2**1024), F(1, 4), F(1, 8), scalar, work)
        assert result["abort"] is None and result["branch"] == "proper_same_potential"
        assert result["records"] == [(0, F(27, 32))]
        assert access.rows == [0, 0]
        counts["private_huge_ambient_and_tiny_alpha_compositions"] += 1
    result = {
        "audit": "incremental_active_set_sdd.supplied_envelope_alpha_floor",
        "scope": "Paid target-envelope preparation at an effective alpha, preserving the original lambda and significant-potential tolerance. Numerical VWF solve is an explicit dense callback; final constant correction is implemented arithmetic.",
        "arithmetic": "exact fractions; exact-real word model, not bit complexity",
        "parameters": {
            "full": args.full,
            "lambda": "eps_appr/2",
            "delta": "eps_appr/8",
            "native_error_budget": "7*eps_appr/8",
            "alpha_floor": "eps_appr^2/(32+eps_appr^2)",
            "random_seed": None,
        },
        "audit_only": dict(counts),
        "charged_preparation_and_wrapper_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "supplied_envelope_work.py",
                "small_alpha_floor.py",
                "small_alpha_constant_shift.py",
                "geometric_value_events.py",
                "diffusion_accuracy_bridge.py",
                "spectral_preconditioner_floor.py",
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
