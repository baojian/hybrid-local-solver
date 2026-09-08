"""Two genuinely nested accelerated levels with persistent tree base solves.

The supplied tiny preconditioners are explicit reference families. Dense
minima verify gaps but are never used to choose accelerated outputs.
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

from bounded_vwf_compression import VWF
from compressed_forest_refinement import atoms, energy, residual
from generic_proximal_geometry import normalize, universal_policy
from global_vwf_compression import compress_global
from persistent_vwf_forest import IntegralArena, PersistentForest
from recursive_vwf_ranges import graph_norm, graph_records, ranges
from spectral_preconditioner_floor import certify_psd, difference, laplacian, prune
from vwf_forest_reference import PieceVWF, certify_forest_solution
from vwf_quadratic_policy import minimum
import networkx as nx


def normalized_model(graph, inner, functions, center, work):
    shift = [F(0)] * len(graph)
    work["normalized_shift_vector_words_allocated"] += len(graph)
    for sign, supplied in [(F(1), graph), (-F(1), inner)]:
        for v, w, c in graph_records(supplied):
            flow = sign * c * (center[v] - center[w])
            shift[v] += flow
            shift[w] -= flow
            work["normalized_gradient_edge_visits"] += 1
    result = []
    for f, s in zip(functions, shift):
        anchor = f.value(F(0))
        result.append(
            PieceVWF(f.lower, f.splits, tuple((a, b + s, c - anchor) for a, b, c in f.pieces))
        )
        work["normalized_piece_words_allocated"] += 3 * len(f.pieces) + len(f.splits) + 1
        work["normalized_anchor_queries"] += 1
    return result


def upward_candidate(graph, functions, exact, allowance, index, work, counts):
    """Explicit global-gradient bound; perturbation is intentional audit stress."""
    state = ranges(functions)
    radius = max([F(1)] + [abs(x) for x in exact])
    weight = sum(c for _, _, c in graph_records(graph))
    bound = state["A"] + (4 * weight + state["C"]) * (radius + 1)
    assert allowance > 0 and bound > 0
    step = F(1, 2)
    while 2 * step * bound > allowance / 4:
        step /= 2
        work["rounding_grid_halvings"] += 1
    candidate = []
    for x in exact:
        scaled = x / step
        integer = -((-scaled.numerator) // scaled.denominator)
        candidate.append(integer * step)
        counts["reference_upward_integer_roundings"] += 1
    candidate[index % len(graph)] += step
    assert all(0 <= q - x <= 2 * step for q, x in zip(candidate, exact))
    exact_value = energy(graph, functions, exact, counts)
    candidate_value = energy(graph, functions, candidate, work)
    assert candidate_value - exact_value <= 2 * step * bound <= allowance / 4
    counts["complete_upward_energy_rounding_certificates"] += 1
    work["rounding_state_piece_records_scanned"] += sum(len(f.pieces) for f in functions)
    work["rounding_state_graph_records_scanned"] += graph.number_of_edges()
    work["rounded_candidate_words_allocated"] += len(graph)
    return normalize(candidate, state["U"], work)


def tree_oracle(graph, functions, additive, index, work, counts):
    arena = IntegralArena()
    tree = PersistentForest(graph, functions, [0], arena)
    root = tree.curves[0].minimum_point()
    exact = tree.recover({0: root})
    optimum_value = tree.curves[0].value(root)
    checked, _ = certify_forest_solution(graph, functions, exact, counts)
    assert checked == optimum_value
    work.update(arena.counts)
    q = upward_candidate(graph, functions, exact, additive, index, work, counts)
    value = energy(graph, functions, q, work)
    assert 0 <= value - optimum_value <= additive / 4
    counts["nonzero_tree_base_errors"] += value > optimum_value
    work["complete_persistent_tree_base_calls"] += 1
    return q, optimum_value


def accelerate(graph, inner, functions, kappa, eta, oracle, work, counts, level, progress=False):
    n = len(graph)
    initial = energy(graph, functions, [F(0)] * n, work)
    _, optimum = minimum(graph, functions, counts)
    gap = initial - optimum
    assert initial <= 0 and gap >= 0
    steps, pure_relative, doublings = universal_policy(kappa)
    relative, additive = pure_relative / 2, eta / (2**32 * kappa)
    y, z = [F(0)] * n, [F(0)] * n
    work["accelerated_policy_doublings"] += doublings
    work["accelerated_initial_vector_words_allocated"] += 2 * n
    started = time.monotonic()
    for k in range(steps):
        weight = F(k + 2, 2)
        x = [(1 - 1 / weight) * a + b / weight for a, b in zip(y, z)]
        model = normalized_model(graph, inner, functions, x, work)
        q, model_optimum = oracle(model, relative, additive, k)
        value = energy(inner, model, q, work)
        assert value <= model_optimum / (1 + relative) + additive
        assert graph_norm(inner, x) <= 64 * kappa**2 * (gap + eta)
        assert 0 <= value - model_optimum <= (gap + eta) / (2**30 * kappa)
        actual_gap = energy(graph, functions, q, counts) - optimum
        assert actual_gap <= (gap + additive if k == 0 else 8 * kappa * (gap + eta) / (k + 2) ** 2)
        assert actual_gap <= 2 * kappa * (gap + eta)
        z = [a + weight * (b - c) for a, b, c in zip(z, q, x)]
        y = q
        work["accelerated_iteration_vector_words_allocated"] += 6 * n
        counts[f"level_{level}_complete_accelerated_step_certificates"] += 1
        if progress:
            print(
                json.dumps(
                    {
                        "progress": "outer iteration",
                        "iteration": k + 1,
                        "total": steps,
                        "elapsed_seconds": round(time.monotonic() - started, 2),
                        "tree_base_calls": work["complete_persistent_tree_base_calls"],
                    }
                ),
                file=sys.stderr,
                flush=True,
            )
    final = energy(graph, functions, y, work)
    assert final - optimum <= (gap + eta) / 32
    assert final <= optimum / 2 + eta
    counts[f"level_{level}_complete_accelerated_invocations"] += 1
    return y, optimum


class CoarseAccelerated:
    def __init__(self, graph, work, counts):
        assert len(graph) == 3 and graph.number_of_edges() == 3
        c = graph[0][1]["weight"]
        assert all(w == c for _, _, w in graph_records(graph))
        raw = [(0, 1, 3 * c), (0, 2, 3 * c)]
        kept, _, _ = prune(3, graph_records(graph), raw, work)
        self.inner = nx.Graph()
        self.inner.add_nodes_from(range(3))
        self.inner.add_weighted_edges_from(kept)
        self.graph, self.kappa, self.work, self.counts = graph, F(6), work, counts
        g, h = laplacian(3, graph_records(graph)), laplacian(3, kept)
        certify_psd(difference(h, g), counts)
        certify_psd(difference(g, h, F(1, 6)), counts)

    def solve(self, functions, eta):
        def oracle(model, relative, additive, index):
            del relative
            return tree_oracle(self.inner, model, additive, index, self.work, self.counts)

        return accelerate(
            self.graph, self.inner, functions, self.kappa, eta, oracle, self.work, self.counts, 1
        )


def compressed_oracle(graph, functions, xi, coarse_solver, work, counts):
    state = ranges(functions)
    target = xi / 2
    tau = min(F(1), target / state["C"]) if state["C"] else F(1)
    compressed, error = [], F(0)
    for f in functions:
        new, e, _, operations, _, _ = compress_global(atoms(f, work), tau)
        work.update(operations)
        compressed.append(PieceVWF.from_atoms(new))
        error += e
    assert error <= target
    result, compressed_optimum = coarse_solver.solve(compressed, xi)
    q = [x / 2 for x in result]
    _, optimum = minimum(graph, functions, counts)
    assert compressed_optimum <= optimum
    assert energy(graph, functions, q, counts) <= optimum / 4 + xi
    counts["nested_compression_embeddings"] += 1
    counts["nested_positive_compression_errors"] += error > 0
    work["compressed_child_calls"] += 1
    work["compressed_child_piece_words_allocated"] += sum(
        3 * len(f.pieces) + len(f.splits) + 1 for f in compressed
    )
    work["scaled_coarse_candidate_words_allocated"] += len(q)
    return q


def forest_refine(graph, functions, roots, relative, additive, coarse_solver, work, counts):
    arena = IntegralArena()
    forest = PersistentForest(graph, functions, roots, arena)
    coarse = coarse_solver.graph
    assert sorted(forest.coarse_edges) == sorted(graph_records(coarse))
    exported = [PieceVWF.from_atoms(forest.curves[v].export()) for v in roots]
    _, optimum = minimum(coarse, exported, counts)
    a = [F(0)] * len(roots)
    current = energy(coarse, exported, a, work)
    initial_gap = current - optimum
    contraction = F(1)
    rounds = 0
    while contraction > relative / (1 + relative):
        contraction *= F(3, 4)
        rounds += 1
        work["refinement_round_budget_multiplications"] += 1
    upper = ranges(exported)["U"]
    for k in range(rounds):
        shifted = residual(coarse, exported, a, work)
        q = compressed_oracle(coarse, shifted, additive / 4, coarse_solver, work, counts)
        candidate = normalize([x + y for x, y in zip(a, q)], upper, work)
        value = energy(coarse, exported, candidate, work)
        assert value - optimum <= F(3, 4) * (current - optimum) + additive / 4
        if value <= current:
            a, current = candidate, value
            work["accepted_nested_refinement_candidates"] += 1
        else:
            work["failed_nested_refinement_guards"] += 1
        assert current - optimum <= F(3, 4) ** (k + 1) * initial_gap + additive
        counts["nested_refinement_gap_certificates"] += 1
    assert current <= optimum / (1 + relative) + additive
    result = forest.recover(dict(zip(roots, a)))
    checked, _ = certify_forest_solution(graph, functions, result, counts, roots)
    assert checked == current
    work.update(arena.counts)
    counts["nested_exact_forest_recoveries"] += 1
    return result, optimum


def physical_case(profile, work, counts):
    graph = nx.Graph([(0, 1), (0, 2), (1, 2), (0, 3)])
    alpha, eps, seed = F(1, 3), F(1, 32), 3
    gamma = (1 - alpha) / (1 + alpha)
    bar = 1 - gamma
    for v, w in graph.edges():
        graph[v][w]["weight"] = gamma
    functions = []
    for v in graph:
        d = graph.degree(v)
        b = F(v == seed) - eps * d / 2
        functions.append(PieceVWF.from_atoms(VWF(F(0), F(0), -b, ((1 / bar, bar * d),))))
    base = [F(3) if profile == "beyond_cap" else F(0)] * len(graph)
    if profile == "beyond_cap":
        functions = residual(graph, functions, base, work)
    kept, _, _ = prune(len(graph), graph_records(graph), graph_records(graph), work)
    inner = nx.Graph()
    inner.add_nodes_from(range(len(graph)))
    inner.add_weighted_edges_from(kept)
    coarse = inner.subgraph([0, 1, 2]).copy()
    child = CoarseAccelerated(coarse, work, counts)

    def oracle(model, relative, additive, index):
        del index
        return forest_refine(inner, model, [0, 1, 2], relative, additive, child, work, counts)

    result, optimum = accelerate(
        graph, inner, functions, F(2), F(1, 16), oracle, work, counts, 0, True
    )
    physical = [a + x for a, x in zip(base, result)]
    assert all(x >= 0 for x in physical)
    counts["negative_outer_signed_iterate_coordinates"] += sum(x < 0 for x in result)
    return {
        "profile": profile,
        "physical_seed": seed,
        "alpha": str(alpha),
        "eps_appr": str(eps),
        "vertices": len(graph),
        "edges": graph.number_of_edges(),
        "outer_quality": "2",
        "coarse_quality": "6",
        "eta": "1/16",
        "result": [str(x) for x in result],
        "physical_result": [str(x) for x in physical],
        "reference_optimum": str(optimum),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started, work, counts = time.monotonic(), Counter(), Counter()
    records = []
    if args.full:
        for profile in ["original", "beyond_cap"]:
            records.append(physical_case(profile, work, counts))
    else:
        graph = nx.complete_graph(3)
        for v, w in graph.edges():
            graph[v][w]["weight"] = F(1)
        functions = [
            PieceVWF.from_atoms(
                VWF(-F(1), F(0), -F(1, 8) if v == 0 else F(0), ((F(1, 2**100), F(1)), (F(1), F(1))))
            )
            for v in graph
        ]
        child = CoarseAccelerated(graph, work, counts)
        result, optimum = child.solve(functions, F(1, 2**30))
        records.append(
            {
                "profile": "coarse accelerated smoke",
                "result": [str(x) for x in result],
                "reference_optimum": str(optimum),
            }
        )
    result = {
        "audit": "incremental_active_set_sdd.nested_mixed_forest_solver",
        "arithmetic": "exact fractions with deliberate upward dyadic rounding",
        "random_seed": None,
        "input_family": "Three-root uniform core and pendant physical seed; original and signed beyond-cap residuals; fast mode is one coarse accelerated invocation",
        "stopping_rule": "Explicit mixed APG step count and beta=4 refinement budget at each supplied level; exact persistent single-root tree minima at the base",
        "scope": "Implemented two nested accelerated levels, persistent forest elimination/recovery and compression/refinement. Tiny supplied preconditioners are explicit families; dense minima and KKT are validators. This is not a general fast constructor or local OP3 solver.",
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
                "compressed_forest_refinement",
                "generic_proximal_geometry",
                "global_vwf_compression",
                "persistent_vwf_forest",
                "recursive_vwf_ranges",
                "spectral_preconditioner_floor",
                "vwf_forest_reference",
                "vwf_quadratic_policy",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
