"""Exact audit of the conservative-envelope/ACL reduction and component gate.

The reverse direction uses the implemented cubic ACL producer, not an
assumed fast finder. Forward supplied solves use explicit dense reference
callbacks. Conservative optima, torsion and full residuals are validators.
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

from capped_component_exploration import explore
from conservative_local_producer import solve_local
from geometric_value_events import mv, obstacle, solve
from small_alpha_constant_shift import residual
from small_alpha_floor import LocalRows
from spectral_preconditioner_floor import laplacian
from supplied_envelope_alpha_floor import solve_supplied
from supplied_envelope_work import SuppliedRows, physical
import networkx as nx


def conservative_comparison(graph, seed, epsilon, counts):
    degrees = [graph.degree(i) for i in graph]
    assert sum(degrees) > 4 / epsilon
    lam, delta = epsilon / 2, epsilon / 8
    matrix, load, original = physical(graph, seed, F(0), epsilon)
    gradient = [a - b for a, b in zip(mv(matrix, original), load)]
    assert all(value >= 0 for value in original)
    assert all(g >= 0 and x * g == 0 for x, g in zip(original, gradient))
    actual = residual(graph, seed, F(0), original)
    assert all(0 <= r <= lam * degrees[i] for i, r in enumerate(actual))
    support = [i for i in graph if original[i] > 0]
    volume = sum(degrees[i] for i in support)
    assert len(support) < len(graph) and volume < 2 / epsilon
    assert max(original) <= len(support) <= volume
    torsion = [F(0)] * len(graph)
    if support:
        local = [[matrix[i][j] for j in support] for i in support]
        values = solve(local, [F(degrees[i]) for i in support])
        for i, value in zip(support, values):
            torsion[i] = value
        applied = mv(matrix, torsion)
        assert all(torsion[i] > 0 and applied[i] == degrees[i] for i in support)
        assert max(torsion) <= volume * len(support) <= volume**2
        for i, j in graph.edges:
            assert abs(torsion[i] - torsion[j]) <= volume
        counts["validator_Dirichlet_torsion_systems"] += 1
        counts["torsion_maximum_and_edge_bounds"] += 1
    t = epsilon**4 / 128
    alpha = t / (2 - t)
    assert 2 * alpha / (1 + alpha) == t
    _, perturbed_load, perturbed = physical(graph, seed, alpha, epsilon)
    assert load == perturbed_load
    difference = [x - y for x, y in zip(original, perturbed)]
    assert all(0 <= d <= t * max(original) * w for d, w in zip(difference, torsion))
    assert max(difference) < 8 * t / epsilon**3 == delta / 2
    assert all(perturbed[i] > 0 for i in graph if original[i] > delta)
    counts["validator_conservative_KKT_systems"] += 1
    counts["validator_same_load_small_positive_obstacles"] += 1
    counts["quantitative_conservative_parameter_comparisons"] += 1
    counts["empty_conservative_obstacles"] += not support
    return original, perturbed, alpha


def check_case(graph, seed, epsilon, counts, work):
    gate = explore(LocalRows(graph, work), seed, 4 / epsilon, work)
    if gate["complete"]:
        supplied = [node.label for node in gate["records"]]
        work["reduction_complete_gate_label_materialization"] += len(supplied)
        original = None
        counts["complete_small_component_reduction_cases"] += 1
    else:
        original, perturbed, alpha = conservative_comparison(graph, seed, epsilon, counts)
        weak, state = solve_local(LocalRows(graph, work), seed, alpha, epsilon / 2, work)
        assert weak["branch"] == "conservative_proper"
        vector = [F(0)] * len(graph)
        supplied = []
        for label, value in weak["records"]:
            vector[label] = value
            supplied.append(label)
            work["reduction_reverse_output_label_materialization"] += 1
        reverse_residual = residual(graph, seed, alpha, vector)
        assert all(
            0 <= r <= (epsilon / 2) * graph.degree(i) for i, r in enumerate(reverse_residual)
        )
        assert all(x >= y for x, y in zip(vector, perturbed))
        assert {i for i in graph if original[i] > epsilon / 8} <= set(supplied)
        assert sum(graph.degree(i) for i in supplied) < 4 / epsilon
        assert state.active_volume < 4 / epsilon
        counts["implemented_weak_ACL_reverse_envelopes"] += 1
        counts["reverse_supersolution_and_significant_containment_checks"] += 1
    for target_alpha in [F(1), F(1, 3), F(1, 2**80)]:
        _, _, target_optimum = physical(graph, seed, target_alpha, epsilon)
        counts["validator_original_target_obstacles"] += 1
        if original is not None:
            assert all(u <= u0 for u, u0 in zip(target_optimum, original))
            counts["conservative_to_target_same_load_monotonicity_checks"] += 1
        access = SuppliedRows(graph, supplied, seed, work)

        def numerical(prepared, confidence):
            assert confidence == F(1, 8)
            local = laplacian(len(prepared["labels"]), prepared["edges"])
            for i, h in enumerate(prepared["grounding"]):
                local[i][i] += h
            counts["explicit_dense_supplied_numerical_validator_callbacks"] += 1
            return obstacle(local, prepared["load"])

        result = solve_supplied(
            access, supplied, seed, target_alpha, epsilon, F(1, 8), numerical, work
        )
        assert result["abort"] is None
        vector = [F(0)] * len(graph)
        for label, value in result["records"]:
            vector[label] = value
        actual = residual(graph, seed, target_alpha, vector)
        assert all(0 <= r <= epsilon * graph.degree(i) for i, r in enumerate(actual))
        assert all(target_optimum[i] > 0 for i in graph if vector[i] > 0)
        assert sum(graph.degree(i) for i in graph if vector[i] > 0) < 2 / epsilon
        assert set(access.queried) <= set(supplied)
        if original is not None:
            assert result["branch"] != "full_support_constant_shift"
        counts["composed_original_target_ACL_certificates"] += 1
        counts["validator_original_target_residual_rows"] += len(graph)
        counts["forward_branch_" + result["branch"]] += 1


def audit_large_star_bound(counts, full):
    for k in range(4, 1025 if full else 17):
        epsilon = F(1, 2**k)
        leaves = 2 ** (k - 3)
        center_degree = leaves + 1
        assert leaves >= 1 / (16 * epsilon)
        assert epsilon * center_degree <= F(3, 16) < F(1, 3)
        # Conservative seed KKT and the leaf equation imply these bounds
        # regardless of the length of the extra path attached at the center.
        conservative_leaf_lower = F(1, center_degree) - epsilon
        assert conservative_leaf_lower > epsilon / 8
        counts["symbolic_conservative_envelope_leaf_output_bounds"] += 1
        for alpha in [F(1, 3), F(1, 2**k), F(1, 2**1024)]:
            gamma = (1 - alpha) / (1 + alpha)
            lower = F(1, center_degree) - epsilon
            assert gamma >= F(1, 2) and gamma * lower > epsilon
            counts["symbolic_large_ambient_original_ACL_leaf_obstructions"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= (6 if args.full else 3) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for epsilon in [F(1, 4), F(1, 2), F(3, 4)] if args.full else [F(1, 2)]:
                check_case(graph, seed, epsilon, counts, work)
    for k in [2, 4, 8, 12] if args.full else [2, 4]:
        check_case(nx.path_graph(4 * k + 1), 0, F(1, k), counts, work)
    if args.full:
        for k in [8, 16]:
            graph = nx.path_graph(4 * k + 1)
            for j in range(k // 8):
                graph.add_edge(0, len(graph))
            check_case(graph, 0, F(1, k), counts, work)
            counts["original_star_with_long_tail_reduction_cases"] += 1
    audit_large_star_bound(counts, args.full)
    result = {
        "audit": "incremental_active_set_sdd.conservative_envelope_reduction",
        "scope": "Capped component gate and exact reduction checks. The reverse test uses the implemented cubic local ACL producer; the forward supplied VWF solve is an explicit dense validator. No fast conservative finder is claimed.",
        "arithmetic": "exact fractions; word-work charges apply to implemented gate, weak producer and preparation only; dense validators are separately identified.",
        "parameters": {
            "full": args.full,
            "lambda": "eps_appr/2",
            "delta": "eps_appr/8",
            "comparison_bar_alpha": "eps_appr^4/128",
            "component_budget": "4/eps_appr",
            "source_failure_argument": "1/8",
            "random_seed": None,
        },
        "audit_only": dict(counts),
        "charged_implemented_interface_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "capped_component_exploration.py",
                "conservative_local_producer.py",
                "native_gap_push.py",
                "supplied_envelope_alpha_floor.py",
                "supplied_envelope_work.py",
                "geometric_value_events.py",
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
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
