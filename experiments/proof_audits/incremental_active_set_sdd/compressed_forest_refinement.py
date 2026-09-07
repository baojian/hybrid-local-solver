"""Mixed-accuracy compression, refinement and exact forest recovery audit.

Persistent elimination, moment compression, residual construction and guards
are implemented. Dense forward-piece coarse solves supply reference oracles.
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

from bounded_vwf_compression import VWF
from global_vwf_compression import compress_global, validate_global
from persistent_vwf_forest import IntegralArena, PersistentForest
from vwf_forest_reference import PieceVWF, certify_forest_solution, random_function
from vwf_quadratic_policy import minimum
import networkx as nx


def energy(graph, functions, values, work):
    result = sum((f.value(x) for f, x in zip(functions, values)), F(0))
    work["objective_vertex_value_queries"] += len(functions)
    for v, w, data in graph.edges(data=True):
        result += data["weight"] * (values[v] - values[w]) ** 2 / 2
        work["objective_edge_visits"] += 1
    return result


def residual(graph, functions, at, work):
    gx = [F(0)] * len(graph)
    work["residual_vector_words_allocated"] += len(graph)
    for v, w, data in graph.edges(data=True):
        flow = data["weight"] * (at[v] - at[w])
        gx[v] += flow
        gx[w] -= flow
        work["residual_gradient_edge_visits"] += 1
    shifted = []
    for f, x, g in zip(functions, at, gx):
        anchor = f.value(x)
        pieces = tuple(
            (a, 2 * a * x + b + g, a * x * x + b * x + c - anchor) for a, b, c in f.pieces
        )
        value = PieceVWF(f.lower - x, tuple(s - x for s in f.splits), pieces)
        assert value.lower <= 0 and value.value(F(0)) == 0
        shifted.append(value)
        work["residual_piece_words_allocated"] += 3 * len(pieces) + len(f.splits) + 1
        work["residual_anchor_value_queries"] += 1
    return shifted


def atoms(f, work):
    knots = tuple(
        (s, 2 * (p[0] - q[0])) for s, p, q in zip(f.splits, f.pieces, f.pieces[1:]) if p[0] > q[0]
    )
    work["canonical_piece_records_read"] += len(f.pieces)
    work["canonical_atom_words_allocated"] += 3 + 2 * len(knots)
    return VWF(f.lower, f.value(F(0)), f.derivative(F(0)), knots)


def compressed_four_plus(graph, functions, additive, counts, work):
    assert additive > 0
    total_curvature = sum(2 * f.pieces[0][0] for f in functions)
    tau = min(F(1), additive / (2 * total_curvature)) if total_curvature else F(1)
    compressed, error = [], F(0)
    for f in functions:
        original = atoms(f, work)
        output, xi, _, operations, _, _ = compress_global(original, tau)
        work.update(operations)
        error += xi
        compressed.append(PieceVWF.from_atoms(output))
        work["compressed_piece_words_allocated"] += (
            3 * (len(output.knots) + 1) + len(output.knots) + 1
        )
        # Independent complete-interval validation of these newly translated
        # functions; the duplicate reference construction is validator work.
        validate_global(original, tau, counts, Counter())
    assert error <= additive / 2
    optimum, optimum_value = minimum(graph, compressed, counts)
    base = [x / 2 for x in optimum]
    assert energy(graph, compressed, base, counts) <= optimum_value / 2
    step = F(1)
    while step * step > additive:
        step /= 2
        counts["reference_coarse_perturbation_scale_halvings"] += 1
    while True:
        output = []
        for x in base:
            ratio = x / step
            upper_integer = -((-ratio.numerator) // ratio.denominator)
            output.append(upper_integer * step)
            counts["reference_upward_dyadic_coordinate_roundings"] += 1
        output[0] += step
        output_value = energy(graph, compressed, output, counts)
        if output_value <= optimum_value / 2 + additive:
            break
        step /= 2
        counts["reference_coarse_perturbation_backtracks"] += 1
    assert all(x >= f.lower for x, f in zip(output, compressed))
    assert all(x.denominator & (x.denominator - 1) == 0 for x in output)
    q = [x / 2 for x in output]
    original_value = energy(graph, functions, q, counts)
    assert original_value <= output_value / 2 + error
    counts["complete_mixed_compression_energy_embeddings"] += 1
    counts["coarse_outputs_using_additive_allowance"] += output_value > optimum_value / 2
    work["compressed_coarse_oracle_calls"] += 1
    work["coarse_candidate_and_scaled_words_allocated"] += 2 * len(q)
    return q, error, optimum_value


def refine(graph, functions, relative, additive, optimum, counts, work):
    assert relative > 0 and additive > 0
    remaining, rounds = F(1), 0
    while remaining > relative / (1 + relative):
        remaining *= F(3, 4)
        rounds += 1
        work["refinement_budget_multiplications"] += 1
    at = [F(0)] * len(graph)
    current = energy(graph, functions, at, work)
    assert optimum <= current <= 0
    upper = max([F(0)] + [s for f in functions for s in f.splits])
    work["canonical_upper_split_records_read"] += sum(len(f.splits) for f in functions)
    initial_gap, error_budget = current - optimum, additive / 4
    rejected = 0
    for step in range(rounds):
        old_gap = current - optimum
        shifted = residual(graph, functions, at, work)
        q, error, compressed_optimum = compressed_four_plus(
            graph, shifted, error_budget, counts, work
        )
        residual_value = energy(graph, shifted, q, counts)
        assert compressed_optimum <= -old_gap
        assert residual_value <= -old_gap / 4 + error_budget
        candidate = [a + b for a, b in zip(at, q)]
        before_canonical = energy(graph, functions, candidate, counts)
        assert before_canonical == current + residual_value
        shift = max(F(0), min(candidate) - upper)
        candidate = [x - shift for x in candidate]
        work["canonical_minimum_entries_scanned"] += len(candidate)
        work["refinement_candidate_words_allocated"] += 2 * len(candidate)
        candidate_value = energy(graph, functions, candidate, work)
        assert candidate_value <= before_canonical
        assert all(x >= f.lower for x, f in zip(candidate, functions))
        if candidate_value <= current:
            at, current = candidate, candidate_value
            work["accepted_refinement_candidates"] += 1
        else:
            rejected += 1
            work["failed_refinement_improvement_guards"] += 1
        assert current - optimum <= F(3, 4) * old_gap + error_budget
        assert current - optimum <= F(3, 4) ** (step + 1) * initial_gap + additive
        counts["complete_mixed_refinement_gap_recurrences"] += 1
        counts["strictly_positive_compression_errors"] += error > 0
    assert current <= optimum / (1 + relative) + additive
    counts["complete_mixed_relative_refinements"] += 1
    counts["zero_gap_refinements"] += initial_gap == 0
    return at, {
        "relative_accuracy": str(relative),
        "additive_accuracy": str(additive),
        "refinement_rounds": rounds,
        "failed_improvement_guards": rejected,
    }


def build_case(root_count, depth, profile, rng):
    graph = nx.complete_graph(root_count)
    roots = list(range(root_count))
    for root in roots:
        previous = root
        for _ in range(depth):
            vertex = len(graph)
            graph.add_edge(previous, vertex)
            previous = vertex
    for index, (v, w) in enumerate(graph.edges()):
        graph[v][w]["weight"] = F(1 + index % 5, 1 + index % 3)
    if profile == "zero_gap":
        functions = [PieceVWF(F(0), (), ((F(0), F(0), F(0)),)) for _ in graph]
    elif profile in ["tiny_events", "tiny_zero_gap"]:
        tiny = F(1, 2**100)
        functions = [
            PieceVWF.from_atoms(
                VWF(
                    -F(1),
                    F(0),
                    -F(1, 8) if v == 0 and profile == "tiny_events" else F(0),
                    ((-tiny, F(1)), (tiny, F(1)), (F(1), F(1))),
                )
            )
            for v in graph
        ]
    else:
        functions = [random_function(rng) for _ in graph]
        total = sum(f.pieces[-1][1] for f in functions)
        correction = -total if profile == "zero_total_tail" else max(F(0), 1 - total)
        f = functions[0]
        functions[0] = PieceVWF(
            f.lower, f.splits, tuple((a, b + correction, c) for a, b, c in f.pieces)
        )
    return graph, functions, roots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, rng, counts, work = time.monotonic(), random.Random(80309), Counter(), Counter()
    records = []
    for root_count in [2, 3, 4] if args.full else [2]:
        for depth in [1, 3] if args.full else [1]:
            for profile in (
                ["random", "zero_total_tail", "zero_gap", "tiny_events", "tiny_zero_gap"]
                if args.full
                else ["random", "zero_gap", "tiny_zero_gap"]
            ):
                graph, functions, roots = build_case(root_count, depth, profile, rng)
                arena = IntegralArena()
                forest = PersistentForest(graph, functions, roots, arena)
                coarse = nx.Graph()
                coarse.add_nodes_from(roots)
                for v, w, c in forest.coarse_edges:
                    coarse.add_edge(v, w, weight=c)
                work["coarse_graph_record_words_allocated"] += len(roots) + 3 * len(
                    forest.coarse_edges
                )
                core_functions = [PieceVWF.from_atoms(forest.curves[v].export()) for v in roots]
                work["exported_coarse_piece_words_allocated"] += sum(
                    3 * len(f.pieces) + len(f.splits) + 1 for f in core_functions
                )
                core_optimum, optimum_value = minimum(coarse, core_functions, counts)
                # Independent original KKT for the exact coarse reference optimum.
                exact_values = [None] * len(graph)
                for v, x in zip(roots, core_optimum):
                    exact_values[v] = x
                observer = IntegralArena()
                for v in forest.order:
                    p = forest.parent[v]
                    if p >= 0:
                        g = forest.lifted[v].with_arena(observer).derivative(exact_values[p])
                        exact_values[v] = exact_values[p] - g / forest.parent_weight[v]
                true_value, _ = certify_forest_solution(graph, functions, exact_values, counts)
                assert true_value == optimum_value
                tolerances = (
                    [(F(1, 8), F(1, 16)), (F(1, 256), F(1, 2**20))]
                    if args.full
                    else [(F(1, 8), F(1, 16))]
                )
                if args.full and root_count == 2 and depth == 1 and profile == "tiny_events":
                    tolerances.append((1 / (66 * F(2**30) * F(4) ** 3), F(1, 2**37)))
                for relative, additive in tolerances:
                    at, record = refine(
                        coarse, core_functions, relative, additive, optimum_value, counts, work
                    )
                    recovered = forest.recover(dict(zip(roots, at)))
                    original_value, _ = certify_forest_solution(
                        graph, functions, recovered, counts, roots
                    )
                    assert original_value == energy(coarse, core_functions, at, counts)
                    assert original_value <= optimum_value / (1 + relative) + additive
                    counts["complete_compressed_forest_refinement_recoveries"] += 1
                    records.append(
                        {
                            "root_count": root_count,
                            "attachment_depth": depth,
                            "profile": profile,
                            "vertices": len(graph),
                            "original_edges": graph.number_of_edges(),
                            "coarse_edges": coarse.number_of_edges(),
                            "input_splits": sum(len(f.splits) for f in functions),
                            "coarse_splits": sum(len(f.splits) for f in core_functions),
                            **record,
                        }
                    )
                work.update(arena.counts)
    assert counts["coarse_outputs_using_additive_allowance"] > 0
    assert work["failed_refinement_improvement_guards"] > 0
    assert counts["strictly_positive_compression_errors"] > 0
    result = {
        "audit": "incremental_active_set_sdd.compressed_forest_refinement",
        "arithmetic": "exact fractions",
        "random_seed": 80309,
        "input_family": "Complete retained-root cores with separate path attachments; signed-domain random VWFs, zero total final slope and zero-gap affine cases",
        "alpha_eps_physical_seed": "not applicable: generic supplied VWF numerical interface",
        "stopping_rule": "Exact forest elimination once; beta=4 refinement with per-call additive zeta/4, shared moment-compression budget and paid nonincrease guard; exact final forest recovery",
        "scope": "Implemented forest/compression/residual/guard pipeline with dense exact coarse reference oracles. All oracle work is retained as reference work, not a fast recursive or local OP3 solver claim.",
        "reference_precision_policy": "Round coarse reference candidates upward to a dyadic grid and refine that grid until the exact mixed energy contract passes. This avoids uncontrolled rational denominator growth in repeated reference calls; integer rounding and backtracking are validator work, not a claimed production bit-complexity bound.",
        "audit_only": dict(counts),
        "algorithm_counts": dict(work),
        "cases": records,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "global_vwf_compression",
                "persistent_vwf_forest",
                "vwf_forest_reference",
                "vwf_quadratic_policy",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
