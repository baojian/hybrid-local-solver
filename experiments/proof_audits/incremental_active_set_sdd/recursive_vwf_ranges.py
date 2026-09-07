"""Exact local-step audit of simultaneous recursive VWF range bounds.

Graph constructors and dense minima are references. No unimplemented
recursive running time is inferred from these finite checks.
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
from compressed_forest_refinement import atoms, energy, residual
from generic_proximal_geometry import normalize
from global_vwf_compression import compress_global
from persistent_vwf_forest import IntegralArena, PersistentForest
from spectral_preconditioner_floor import certify_psd, difference, laplacian, prune
from vwf_forest_reference import PieceVWF, random_function
from vwf_quadratic_policy import minimum
import networkx as nx


def ranges(functions):
    return {
        "S": sum(max(F(0), f.pieces[-1][1]) for f in functions),
        "C": sum(2 * f.pieces[0][0] for f in functions),
        "R": max([F(1)] + [-f.lower for f in functions] + [s for f in functions for s in f.splits]),
        "U": max([F(0)] + [s for f in functions for s in f.splits]),
        "A": sum(abs(f.derivative(F(0))) for f in functions),
    }


def graph_records(graph):
    return [(v, w, d["weight"]) for v, w, d in graph.edges(data=True)]


def matrix_product(matrix, values):
    return [sum((a * b for a, b in zip(row, values)), F(0)) for row in matrix]


def graph_norm(graph, values):
    return sum((c * (values[v] - values[w]) ** 2 for v, w, c in graph_records(graph)), F(0))


def audit_case(n, profile, scale, center_factor, rng, counts, work):
    graph = nx.complete_graph(n)
    for v, w in graph.edges():
        graph[v][w]["weight"] = scale
    original = graph_records(graph)
    supplied = [(0, v, n * scale) for v in range(1, n)]
    supplied.append((1, 2, scale / (4 * n * (n - 1))))
    kept, _, _ = prune(n, original, supplied, work)
    inner = nx.Graph()
    inner.add_nodes_from(range(n))
    inner.add_weighted_edges_from(kept)
    kappa = F(2 * (n + 1))
    g, h = laplacian(n, original), laplacian(n, kept)
    certify_psd(difference(h, g), counts)
    certify_psd(difference(g, h, 1 / kappa), counts)
    if profile in ["tiny", "zero_gap"]:
        tiny = F(1, 2**100)
        functions = [
            PieceVWF.from_atoms(
                VWF(
                    -F(1),
                    F(0),
                    -scale / 8 if v == 0 and profile == "tiny" else F(0),
                    ((-tiny, scale), (tiny, scale), (F(1), scale)),
                )
            )
            for v in range(n)
        ]
    else:
        functions = [random_function(rng) for _ in range(n)]
        total = sum(f.pieces[-1][1] for f in functions)
        change = -total if profile == "zero_tail" else max(F(0), 1 - total)
        f = functions[0]
        functions[0] = PieceVWF(
            f.lower, f.splits, tuple((a, b + change, c) for a, b, c in f.pieces)
        )
        functions = [
            PieceVWF(
                f.lower, f.splits, tuple((scale * a, scale * b, scale * c) for a, b, c in f.pieces)
            )
            for f in functions
        ]
    data = ranges(functions)
    optimum, optimum_value = minimum(graph, functions, counts)
    bound, eta = -optimum_value, scale / 8
    initial = energy(graph, functions, [F(0)] * n, counts)
    assert 0 <= initial - optimum_value <= bound
    center = [center_factor * x + F(2**100) for x in optimum]
    assert graph_norm(inner, center) <= 64 * kappa**2 * (bound + eta)
    shift = matrix_product(difference(g, h), center)
    model = [
        PieceVWF(f.lower, f.splits, tuple((a, b + s, c - f.value(F(0))) for a, b, c in f.pieces))
        for f, s in zip(functions, shift)
    ]
    model_ranges = ranges(model)
    weight = sum(c for _, _, c in original)
    inner_weight = sum(c for _, _, c in kept)
    inner_floor = min(c for _, _, c in kept)
    assert max(F(0), model_ranges["S"] - data["S"]) ** 2 <= 32**2 * kappa**3 * weight * (
        bound + eta
    )
    assert model_ranges["C"] == data["C"] and model_ranges["R"] == data["R"]
    arena = IntegralArena()
    forest = PersistentForest(inner, model, [0, 1, 2], arena)
    coarse = nx.Graph()
    coarse.add_nodes_from([0, 1, 2])
    coarse.add_weighted_edges_from(forest.coarse_edges)
    exported = [PieceVWF.from_atoms(forest.curves[v].export()) for v in [0, 1, 2]]
    coarse_optimum, coarse_value = minimum(coarse, exported, counts)
    inner_bound = -coarse_value
    assert inner_bound <= 33 * kappa**2 * (bound + eta)
    out = ranges(exported)
    assert out["S"] <= model_ranges["S"]
    assert out["C"] <= model_ranges["C"] + inner_weight
    assert out["U"] <= model_ranges["U"] + n * model_ranges["S"] / inner_floor
    assert all(-inner_bound <= f.value(F(0)) <= 0 for f in exported)
    counts["complete_proximal_and_exact_forest_range_steps"] += 1
    counts["zero_initial_gap_range_cases"] += initial == optimum_value
    counts["negative_individual_model_final_slopes"] += sum(f.pieces[-1][1] < 0 for f in model)
    coarse_weight = sum(c for _, _, c in forest.coarse_edges)
    coarse_floor = min(c for _, _, c in forest.coarse_edges)
    path_constant = F(2) / coarse_floor
    for fraction in [F(0), F(1, 4), F(3, 4), F(1)]:
        a = normalize([fraction * x for x in coarse_optimum], out["U"], work)
        value = energy(coarse, exported, a, counts)
        assert value <= 0 and graph_norm(coarse, a) <= 8 * inner_bound
        shifted = residual(coarse, exported, a, work)
        state = ranges(shifted)
        assert max(F(0), state["S"] - out["S"]) ** 2 <= 32 * coarse_weight * inner_bound
        assert max(F(0), state["R"] - 2 * out["R"]) ** 2 <= 8 * path_constant * inner_bound
        assert state["C"] == out["C"]
        residual_value = energy(coarse, shifted, [x - y for x, y in zip(coarse_optimum, a)], counts)
        assert residual_value == coarse_value - value >= -inner_bound
        xi_target = eta / (2**35 * kappa)
        tau = min(F(1), xi_target / state["C"]) if state["C"] else F(1)
        compressed, xi = [], F(0)
        for f in shifted:
            converted, error, _, operations, _, _ = compress_global(atoms(f, work), tau)
            compressed.append(PieceVWF.from_atoms(converted))
            xi += error
            work.update(operations)
        child = ranges(compressed)
        _, child_value = minimum(coarse, compressed, counts)
        assert xi <= xi_target
        assert -child_value <= 2 * inner_bound + 2 * xi
        assert child["S"] == state["S"] and child["C"] <= state["C"]
        assert child["R"] <= 2 * state["R"]
        assert -sum(f.value(F(0)) for f in compressed) <= xi
        assert child["A"] <= 2 * child["S"] + child["C"] * child["R"]
        counts["complete_residual_and_compressed_child_range_steps"] += 1
        counts["positive_compression_errors_in_range_steps"] += xi > 0
        counts["negative_shifted_domain_range_steps"] += any(f.lower < 0 for f in shifted)
    work.update(arena.counts)
    return {
        "n": n,
        "profile": profile,
        "energy_scale": str(scale),
        "center_factor": str(center_factor),
        "source_gap_zero": initial == optimum_value,
        "input_radius": str(data["R"]),
        "coarse_radius": str(out["R"]),
        "original_negative_optimum": str(bound),
        "inner_negative_optimum": str(inner_bound),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, rng, counts, work = time.monotonic(), random.Random(80317), Counter(), Counter()
    records = []
    for n in [4, 6, 8] if args.full else [4]:
        for profile in ["random", "zero_tail", "tiny", "zero_gap"]:
            for scale in [F(1, 2**40), F(1), F(2**40)] if args.full else [F(1)]:
                for factor in [-F(4), F(0), F(4)] if args.full else [F(4)]:
                    records.append(audit_case(n, profile, scale, factor, rng, counts, work))
    assert counts["positive_compression_errors_in_range_steps"]
    result = {
        "audit": "incremental_active_set_sdd.recursive_vwf_ranges",
        "arithmetic": "exact fractions",
        "random_seed": 80317,
        "input_family": "Complete graphs with pruned star preconditioners and retained three-root cores, signed VWFs, zero gap/tail, tiny signed events and common energy scales",
        "alpha_eps_physical_seed": "not applicable: generic supplied recursive interface",
        "stopping_rule": "Exact complete proximal/forest/residual/compression range contracts; no production recursive stopping rule claimed",
        "scope": "Local-step mathematical range validators and implemented paid forest/compression/floor operations; source graph construction and dense minima are references, not a local or fast recursive solver",
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
                "global_vwf_compression",
                "persistent_vwf_forest",
                "spectral_preconditioner_floor",
                "vwf_quadratic_policy",
                "vwf_forest_reference",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
