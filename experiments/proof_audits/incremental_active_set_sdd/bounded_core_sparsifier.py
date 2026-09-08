"""Capped fair-bit spectral sampling and supplied-tree core composition.

Production sampling uses paid resistance estimates. Dense resistances and
PSD matrices below are explicit validators. Low-stretch tree selection
remains a primary-source algorithm rather than an implemented primitive.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fair_bit_categorical import Categorical
from ordinary_solve_resistances import ResistancePreparation, ceiling_log2, exact_resistances
from spectral_preconditioner_floor import certify_psd, difference, laplacian
from weighted_corridor_routing import build
import networkx as nx


def connected(n, edges, work):
    """Union by size, without a hidden hash table or free graph traversal."""
    parent, sizes, components = list(range(n)), [1] * n, n
    work["connectivity_parent_size_words_and_copy_budget"] += 3 * n

    def root(v):
        while parent[v] != v:
            v = parent[v]
            work["connectivity_parent_reads_and_comparisons"] += 3
        work["connectivity_root_call_frame_and_final_test"] += 4
        return v

    for u, v, _ in edges:
        a, b = root(u), root(v)
        if a != b:
            if sizes[a] < sizes[b]:
                a, b = b, a
            parent[b] = a
            sizes[a] += sizes[b]
            components -= 1
            work["connectivity_size_union_operations"] += 8
        work["connectivity_edge_records_scanned"] += 3
    return components <= 1


def sample_from_estimates(n, edges, estimates, delta, fair_bit, work):
    """Estimator failure is budgeted delta/4 by the caller.

    The remaining delta/4 is matrix concentration, delta/2 is the capped
    sampler. All guards also apply when the estimate vector is incorrect.
    """
    assert 0 < delta < 1 and len(edges) == len(estimates)
    if n == 1:
        assert not edges
        return [], {"draws": 0, "cap": 0, "completed_draws": 0, "abort": None}
    assert n >= 2 and edges
    scores, total, weight_sum, minimum, valid = [], F(0), F(0), edges[0][2], True
    for (u, v, c), resistance in zip(edges, estimates):
        assert 0 <= u < n and 0 <= v < n and u != v and c > 0
        score = 2 * c * resistance
        scores.append(score)
        total += score
        weight_sum += c
        minimum = min(minimum, c)
        valid = valid and score > 0
        work["score_input_guard_arithmetic_and_copy_budget"] += 18
    if not valid or total > 4 * (n - 1):
        work["invalid_score_aborts_before_sampling"] += 1
        return None, {"draws": 0, "cap": 0, "completed_draws": 0, "abort": "score"}
    logarithm = ceiling_log2(8 * n / delta, work)
    target, draws = 27 * total * logarithm, 1
    while draws < target:
        draws *= 2
        work["sample_count_doubling_operations"] += 3
    sampler = Categorical(scores, work)
    cap = sampler.cap(draws, delta / 2)
    multiplicities = [0] * len(edges)
    work["sample_multiplicity_array_words"] += len(edges)
    for iteration in range(draws):
        draw = sampler.draw(fair_bit, cap)
        if draw.category is None:
            return None, {
                "draws": draws,
                "cap": cap,
                "completed_draws": iteration,
                "abort": "sampler",
            }
        multiplicities[draw.category] += 1
        work["sample_multiplicity_reads_and_updates"] += 3
    output, output_weight = [], F(0)
    for (u, v, c), score, multiplicity in zip(edges, scores, multiplicities):
        if multiplicity:
            weight = F(3, 2) * multiplicity * c * total / (draws * score)
            output.append((u, v, weight))
            output_weight += weight
            work["sample_output_arithmetic_records_and_copy_budget"] += 16
        work["sample_output_original_records_scanned"] += 6
    outcome = {"draws": draws, "cap": cap, "completed_draws": draws, "abort": None}
    if output_weight > 2 * weight_sum:
        outcome["abort"] = "weight"
        work["sample_output_weight_guard_aborts"] += 1
        return None, outcome
    if not connected(n, output, work):
        outcome["abort"] = "connectivity"
        work["sample_output_connectivity_guard_aborts"] += 1
        return None, outcome
    assert len(output) <= draws <= max(1, 216 * (n - 1) * logarithm)
    assert all(c >= F(3, 2) * minimum / draws for _, _, c in output)
    work["output_size_and_weight_floor_assertion_scan_budget"] += 6 * len(output)
    return output, outcome


def sparsify(n, edges, tree_ids, delta, fair_bit, work):
    prep = ResistancePreparation(n, edges, tree_ids, 0, work)
    estimates, estimate_outcome = prep.estimate(delta / 4, fair_bit)
    result, outcome = sample_from_estimates(n, edges, estimates, delta, fair_bit, work)
    outcome["resistance_estimator"] = estimate_outcome
    return result, outcome


def compose_from_tree(n, edges, tree_ids, root, j, delta, fair_bit, work, core_solver):
    """The supplied core_solver must realize the sparsifier contract.

    Full audits identify whether this callback uses the actual sketch or
    a dense effective-resistance validator. No source tree is chosen here.
    """
    routed = build(n, edges, tree_ids, root, work, j=j)
    roots = routed["roots"]
    positions = [-1] * n
    for i, vertex in enumerate(roots):
        positions[vertex] = i
    core = [(positions[u], positions[v], c) for u, v, c in routed["core"]]
    work["root_core_relabel_reads_words_and_copy_budget"] += 2 * n + 10 * len(core)
    sparse, outcome = core_solver(len(roots), core, delta, fair_bit, work)
    if sparse is None:
        return None, routed, outcome
    output = [(roots[u], roots[v], 3 * c) for u, v, c in sparse]
    work["sparse_core_root_lift_words_and_arithmetic"] += 10 * len(sparse)
    for i, edge in enumerate(tree_ids):
        if not routed["cuts"][i]:
            u, v, c = edges[edge]
            output.append((u, v, 3 * routed["kappa"] * c))
            work["final_forest_output_words_and_copy_budget"] += 10
        work["final_forest_original_edge_scans"] += 3
    outcome["core_vertices"] = len(roots)
    outcome["original_core_edges"] = len(core)
    outcome["sparse_core_edges"] = len(sparse)
    return output, routed, outcome


def audit_sample(n, edges, delta, profile, seed, counts, work):
    exact = exact_resistances(n, edges, counts)
    estimates = [r * (F(3, 4) if (i + profile) % 2 else F(5, 4)) for i, r in enumerate(exact)]
    rng = random.Random(seed)
    sampled, outcome = sample_from_estimates(
        n, edges, estimates, delta, lambda: rng.getrandbits(1), work
    )
    counts["seeded_valid_estimator_sampling_attempts"] += 1
    if sampled is None:
        assert outcome["abort"] in ("sampler", "weight", "connectivity")
        counts["allowed_seeded_sampling_abort_" + outcome["abort"]] += 1
        return
    original, result = laplacian(n, edges), laplacian(n, sampled)
    certify_psd(difference(result, original), counts)
    certify_psd(difference(original, result, F(1, 2)), counts)
    scores = [2 * c * r for (_, _, c), r in zip(edges, estimates)]
    total = sum(scores)
    for score, (_, _, c), resistance in zip(scores, edges, exact):
        assert c * resistance <= score <= 4 * c * resistance
        assert c * resistance * total / score <= total
        counts["whitened_rank_one_norm_certificates"] += 1
    logarithm = ceiling_log2(8 * n / delta, Counter())
    assert outcome["draws"] >= 27 * total * logarithm
    assert 2 * n * F(1, 2**logarithm) <= delta / 4
    assert F(outcome["draws"] * (len(edges) - 1), 2 ** outcome["cap"]) <= delta / 2
    assert sum(c for _, _, c in sampled) <= 2 * sum(c for _, _, c in edges)
    counts["capped_spectral_sampling_cases"] += 1
    counts["realized_exact_PSD_sandwiches"] += 2
    counts["prescribed_fair_bit_categorical_draws"] += outcome["draws"]
    counts["original_edges_omitted_by_spectral_sampling"] += len(edges) - len(sampled)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    graphs = [
        g
        for g in nx.graph_atlas_g()
        if 2 <= len(g) <= (5 if args.full else 3) and nx.is_connected(g)
    ]
    for graph_id, graph in enumerate(graphs):
        for exponent in [-80, 0, 80] if args.full else [0]:
            edges = [
                (u, v, F(2) ** exponent * F(1 + i % 3)) for i, (u, v) in enumerate(graph.edges())
            ]
            for profile, delta in enumerate([F(1, 2), F(1, 16)] if args.full else [F(1, 2)]):
                audit_sample(
                    len(graph),
                    edges,
                    delta,
                    profile,
                    908600 + 10 * graph_id + profile,
                    counts,
                    work,
                )
    if args.full:
        complete = list(nx.complete_graph(4).edges())
        for profile in range(2):
            powers = [-80, 80, -40, 0, 1, 2]
            original = [
                (u, v, F(2) ** powers[(i + profile) % 6]) for i, (u, v) in enumerate(complete)
            ]
            audit_sample(4, original, F(1, 16), profile, 908810 + profile, counts, work)
            counts["extreme_relative_weight_sampling_fixtures"] += 1
    edges = [(0, 1, F(1)), (1, 2, F(1))]
    for invalid in [[F(0), F(1)], [F(-1), F(1)], [F(2**100), F(1)]]:
        sampled, outcome = sample_from_estimates(3, edges, invalid, F(1, 4), lambda: 0, work)
        assert sampled is None and outcome["abort"] == "score" and outcome["completed_draws"] == 0
        counts["invalid_score_preallocation_aborts"] += 1
    bit_index = 0

    def boundary_bit():
        nonlocal bit_index
        result = bit_index % 2
        bit_index += 1
        return result

    sampled, outcome = sample_from_estimates(3, edges, [F(1, 2), F(1)], F(1, 4), boundary_bit, work)
    assert sampled is None and outcome["abort"] == "sampler" and bit_index == outcome["cap"]
    counts["forced_fair_bit_sampler_aborts"] += 1
    bit_index = 0

    def rare_then_common():
        nonlocal bit_index
        bit_index += 1
        return int(bit_index > 11)

    sampled, outcome = sample_from_estimates(
        3, edges, [F(1, 4096), F(2047, 4096)], F(1, 4), rare_then_common, work
    )
    assert sampled is None and outcome["abort"] == "weight"
    counts["wrong_estimator_total_weight_guard_aborts"] += 1
    sampled, outcome = sample_from_estimates(3, edges, [F(1, 4)] * 2, F(1, 4), lambda: 1, work)
    assert sampled is None and outcome["abort"] == "connectivity"
    counts["wrong_estimator_connectivity_guard_aborts"] += 1
    # Actual full sketches feed the actual capped sampler in these runs.
    for n, original, tree_ids in (
        [
            (1, [], []),
            (2, [(0, 1, F(2**80))], [0]),
            (3, [(0, 1, F(1)), (1, 2, F(2)), (0, 2, F(4))], [0, 1]),
        ]
        if args.full
        else [(1, [], []), (2, [(0, 1, F(1))], [0])]
    ):
        rng = random.Random(908620 + n)
        sampled, outcome = sparsify(
            n, original, tree_ids, F(1, 4), lambda: rng.getrandbits(1), work
        )
        assert sampled is not None
        result, matrix = laplacian(n, sampled), laplacian(n, original)
        certify_psd(difference(result, matrix), counts)
        certify_psd(difference(matrix, result, F(1, 2)), counts)
        counts["actual_sketch_to_sampler_complete_sparsifiers"] += 1
        counts["actual_integrated_resistance_groups"] += outcome["resistance_estimator"]["groups"]

    def reference_core(n, core, delta, fair_bit, local_work):
        exact = exact_resistances(n, core, counts)
        return sample_from_estimates(n, core, exact, delta, fair_bit, local_work)

    # Assembly uses exact core resistances as a labelled validator, while
    # the preceding runs independently exercise the full estimate pipeline.
    for n in [64, 128, 256] if args.full else [64]:
        for shape in ["path", "cycle", "chorded"] if args.full else ["path"]:
            original = [(v - 1, v, F(1)) for v in range(1, n)]
            if shape != "path":
                original.append((0, n - 1, F(1, n)))
            if shape == "chorded":
                original.extend((v, v + 8, F(1, 16)) for v in range(0, n - 8, 8))
            rng = random.Random(908700 + n)
            answer, routed, outcome = compose_from_tree(
                n,
                original,
                list(range(n - 1)),
                n // 2,
                n,
                F(1, 4),
                lambda: rng.getrandbits(1),
                work,
                reference_core,
            )
            assert answer is not None and outcome["core_vertices"] <= n
            matrix, result = laplacian(n, original), laplacian(n, answer)
            certify_psd(difference(result, matrix), counts)
            certify_psd(difference(matrix, result, F(1, 42) / routed["kappa"]), counts)
            counts["complete_supplied_tree_sparse_core_compositions"] += 1
            counts["compositions_with_nonempty_core"] += outcome["original_core_edges"] > 0
            counts["composition_original_core_edges"] += outcome["original_core_edges"]
            counts["composition_sparse_core_edges"] += outcome["sparse_core_edges"]
    result = {
        "audit": "incremental_active_set_sdd.bounded_core_sparsifier",
        "scope": "Capped fair-bit core sampling with production resistance-sketch integrations and supplied-tree routing composition. Exact resistance and PSD providers in other fixtures are explicitly labelled validators. No local OP3 theorem or implemented low-stretch tree selection.",
        "arithmetic": "exact fractions; exact-real word work, not bit complexity",
        "parameters": {
            "estimator_failure": "delta/4",
            "matrix_failure": "delta/4",
            "sampler_failure": "delta/2",
            "draw_rule": "dyadic upper of max(1,27*t*ceil_log2(8*n/delta))",
            "seed_base": 908600,
            "full": args.full,
        },
        "audit_only": dict(counts),
        "charged_construction_and_sampling_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "ordinary_solve_resistances.py",
                "weighted_cycle_solver.py",
                "fair_bit_categorical.py",
                "weighted_corridor_routing.py",
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
