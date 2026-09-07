"""Dense exact forward-piece validator for supplied convex VWF graph problems.

This policy is reference computation. It certifies every temporary-bound QP
and the final original nonlinear KKT conditions, including flat graph modes.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
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

from geometric_value_events import mv, obstacle
from persistent_vwf_forest import IntegralArena, PersistentForest
from vwf_forest_reference import (
    PieceVWF,
    certify_forest_solution,
    certify_function,
    random_function,
)
import networkx as nx


def dense_laplacian(graph):
    matrix = [[F(0)] * len(graph) for _ in graph]
    for v, w, data in graph.edges(data=True):
        c = data["weight"]
        matrix[v][v] += c
        matrix[w][w] += c
        matrix[v][w] -= c
        matrix[w][v] -= c
    return matrix


def minimum(graph, functions, counts):
    assert nx.is_connected(graph)
    assert sum(f.pieces[-1][1] for f in functions) >= 0
    n, laplacian = len(graph), dense_laplacian(graph)
    indices = [0] * n
    previous = [f.lower for f in functions]
    counts["reference_graph_matrix_entries_allocated"] += n * n
    total_splits = sum(len(f.splits) for f in functions)
    for _ in range(total_splits + 1):
        pieces = [f.pieces[index] for f, index in zip(functions, indices)]
        curvature = [2 * p[0] for p in pieces]
        matrix = [row.copy() for row in laplacian]
        for v in range(n):
            matrix[v][v] += curvature[v]
        load = [
            -g - r * x - p[1]
            for g, r, x, p in zip(mv(laplacian, previous), curvature, previous, pieces)
        ]
        if not any(curvature):
            assert sum(load) <= 0
            counts["reference_weak_Laplacian_bound_QPs"] += 1
        movement = obstacle(matrix, load)
        counts["reference_bound_QP_calls"] += 1
        counts["reference_quadratic_matrix_entries_allocated"] += n * n
        x = [a + b for a, b in zip(previous, movement)]
        gradient = [g + r * t + p[1] for g, r, t, p in zip(mv(laplacian, x), curvature, x, pieces)]
        assert all(a <= b for a, b in zip(previous, x))
        for i in range(n):
            assert gradient[i] >= 0 and (x[i] == previous[i] or gradient[i] == 0)
            assert x[i] == functions[i].lower or gradient[i] == 0
            counts["reference_temporary_bound_and_original_constraint_KKT"] += 1
            counts["reference_artificial_bounds_certified_inactive"] += (
                previous[i] > functions[i].lower
            )
        updated = [bisect_right(f.splits, t) for f, t in zip(functions, x)]
        assert all(a <= b for a, b in zip(indices, updated))
        counts["reference_forward_piece_advances"] += sum(b - a for a, b in zip(indices, updated))
        if updated == indices:
            energy, _ = certify_forest_solution(graph, functions, x, counts)
            counts["reference_complete_nonlinear_KKT_minima"] += 1
            return x, energy
        counts["reference_exact_piece_boundary_ties"] += sum(
            t in f.splits for f, t in zip(functions, x)
        )
        indices, previous = updated, x
    raise AssertionError("The forward piece count did not bound the policy")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, rng, counts = time.monotonic(), random.Random(80303), Counter()
    maximum = 5 if args.full else 3
    graphs = [g for g in nx.graph_atlas_g() if 1 <= len(g) <= maximum and nx.is_connected(g)]
    cases = []
    for raw in graphs:
        graph = raw.copy()
        for i, (v, w) in enumerate(graph.edges()):
            graph[v][w]["weight"] = F(1 + i % 5, 1 + (v + w) % 3)
        for sample in range(12 if args.full else 2):
            for zero_total in [False, True]:
                functions = [random_function(rng) for _ in graph]
                total = sum(f.pieces[-1][1] for f in functions)
                correction = -total if zero_total else max(F(0), 1 - total)
                f = functions[0]
                functions[0] = PieceVWF(
                    f.lower, f.splits, tuple((a, b + correction, c) for a, b, c in f.pieces)
                )
                for f in functions:
                    certify_function(f, counts)
                before = counts["reference_bound_QP_calls"]
                values, energy = minimum(graph, functions, counts)
                if nx.is_tree(graph):
                    forest = PersistentForest(graph, functions, [0], IntegralArena())
                    tree_values = forest.recover({0: forest.curves[0].minimum_point()})
                    tree_energy, _ = certify_forest_solution(graph, functions, tree_values, counts)
                    assert tree_energy == energy
                    counts["independent_persistent_tree_minimum_comparisons"] += 1
                cases.append(
                    {
                        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                        "sample": sample,
                        "zero_total_terminal_slope": zero_total,
                        "vertices": len(graph),
                        "input_splits": sum(len(f.splits) for f in functions),
                        "reference_bound_QP_calls": counts["reference_bound_QP_calls"] - before,
                        "nonboundary_output_coordinates": sum(
                            t > f.lower for t, f in zip(values, functions)
                        ),
                    }
                )
    # Exact ties, an affine zero mode and a very small edge weight.
    structured = []
    for scale in [F(1), F(1, 2**80), F(2**80)]:
        graph = nx.path_graph(3)
        for v, w in graph.edges():
            graph[v][w]["weight"] = scale
        functions = [PieceVWF(-F(1), (), ((F(0), scale * b, -scale),)) for b in [-F(1), F(0), F(1)]]
        values, energy = minimum(graph, functions, counts)
        structured.append(
            {
                "edge_and_energy_scale": str(scale),
                "values": [str(t) for t in values],
                "energy": str(energy),
            }
        )
    assert len({tuple(item["values"]) for item in structured}) == 1
    counts["reference_common_scale_invariance_checks"] += 2
    result = {
        "audit": "incremental_active_set_sdd.vwf_quadratic_policy",
        "arithmetic": "exact fractions",
        "random_seed": 80303,
        "max_n": maximum,
        "input_family": "All connected atlas graphs through max_n, random signed-domain VWFs, zero/positive total final slopes, independent tree comparisons and common energy scales 2^-80 to 2^80",
        "alpha_eps_physical_seed": "not applicable: generic supplied coarse validator",
        "stopping_rule": "Advance right-continuous scalar piece indices until stable; certify each temporary-bound QP and all final original nonlinear KKT equations",
        "scope": "Dense exact reference policy, not a fast coarse oracle or local OP3 solver",
        "audit_only": dict(counts),
        "cases": cases,
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["geometric_value_events", "persistent_vwf_forest", "vwf_forest_reference"]
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
