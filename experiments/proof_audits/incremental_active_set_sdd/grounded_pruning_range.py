"""Exact range witness on a fully positive physical face and safe edge pruning.

The witness concerns the exact local quadratic Schur piece, not a trace of
the CPW algorithm. Pruning is a supplied-matrix accuracy primitive only.
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


def tridiagonal(diagonal, off, load):
    pivots, rhs = list(map(F, diagonal)), list(map(F, load))
    for i in range(1, len(pivots)):
        multiplier = off / pivots[i - 1]
        pivots[i] -= multiplier * off
        rhs[i] -= multiplier * rhs[i - 1]
        assert pivots[i] > 0
    out = [F(0)] * len(pivots)
    for i in reversed(range(len(out))):
        out[i] = (rhs[i] - (off * out[i + 1] if i + 1 < len(out) else 0)) / pivots[i]
    return out


def hub_path(n):
    gamma, bar, lam = F(1, 2), F(1, 2), F(1, 48 * n)
    degrees = [n] + [2] + [3] * (n - 2) + [2]
    y = tridiagonal(degrees[1:], -gamma, [F(1)] * n)
    hub_green = 1 / (n - gamma * gamma * sum(y))
    green = [hub_green] + [gamma * hub_green * t for t in y]
    values = [t - lam / bar for t in green]
    assert all(t > 0 for t in values)
    assert all(t >= F(1, 8 * n) for t in values[1:])
    for i in range(n + 1):
        neighbors = list(range(1, n + 1)) if i == 0 else [0]
        if i > 1:
            neighbors.append(i - 1)
        if 0 < i < n:
            neighbors.append(i + 1)
        residual = F(i == 0) - degrees[i] * values[i] + gamma * sum(values[j] for j in neighbors)
        assert residual == lam * degrees[i]
    determinant_before, determinant = F(1), F(3)
    for _ in range(2, n - 1):
        determinant_before, determinant = (
            determinant,
            3 * determinant - gamma**2 * determinant_before,
        )
    assert determinant >= F(11, 4) ** (n - 2)
    coupling = gamma ** (n - 1) / determinant
    assert coupling <= F(1, 2) * F(2, 11) ** (n - 2)
    dense_match = False
    if n <= 16:
        matrix = [[F(0)] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            matrix[i][i] = F(degrees[i])
        for i in range(1, n + 1):
            matrix[0][i] = matrix[i][0] = -gamma
        for i in range(1, n):
            matrix[i][i + 1] = matrix[i + 1][i] = -gamma
        remaining = list(range(n + 1))
        for k in range(2, n):
            remaining.remove(k)
            pivot = matrix[k][k]
            for i, j in itertools.product(remaining, repeat=2):
                matrix[i][j] -= matrix[i][k] * matrix[k][j] / pivot
        assert matrix[1][n] == -coupling
        dense_match = True
    return {
        "path_vertices": n,
        "physical_vertices": n + 1,
        "original_total_volume": sum(degrees),
        "physical_seed": 0,
        "alpha": "1/3",
        "lambda": str(lam),
        "eps_appr": str(2 * lam),
        "all_original_coordinates_positive": True,
        "minimum_coordinate": str(min(values)),
        "retained_ports": [0, 1, n],
        "eliminated_internal_vertices": n - 2,
        "exact_endpoint_schur_coupling": str(coupling),
        "coupling_denominator_bit_length": coupling.denominator.bit_length(),
        "exponential_upper_bound": str(F(1, 2) * F(2, 11) ** (n - 2)),
        "dense_elimination_matches": dense_match,
    }


def certify_pruning(original, pruned, load, mu, delta, total_removed, counts):
    u, v = obstacle(original, load), obstacle(pruned, load)
    assert max(u + v) <= 1 / mu
    gap = objective(original, load, v) - objective(original, load, u)
    assert 0 <= gap <= total_removed / (2 * mu * mu)
    error_squared = max((a - b) ** 2 for a, b in zip(u, v))
    assert error_squared <= total_removed / mu**3 <= delta**2
    counts["exact_pruning_energy_and_coordinate_bounds"] += 1
    counts["changed_obstacle_supports"] += {i for i, x in enumerate(u) if x} != {
        i for i, x in enumerate(v) if x
    }
    tolerance = mu * delta**2 / 4
    assert total_removed <= mu**3 * delta**2 / 2
    for i in range(len(load)):
        step = 2 / mu
        while True:
            raw = v.copy()
            raw[i] += step
            boxed = [min(t, 1 / mu) for t in raw]
            capped_energy = objective(pruned, load, raw) - sum(
                sum(row) * max(F(0), t - 1 / mu) ** 2 / 2 for row, t in zip(pruned, raw)
            )
            assert objective(pruned, load, boxed) <= capped_energy <= objective(pruned, load, raw)
            counts["two_piece_VWF_capping_certificates"] += 1
            counts["upper_box_energy_monotonicity_checks"] += 1
            if objective(pruned, load, boxed) - objective(pruned, load, v) <= tolerance:
                break
            step /= 2
            counts["reference_approximation_halvings"] += 1
        combined_gap = objective(original, load, boxed) - objective(original, load, u)
        assert combined_gap <= tolerance + total_removed / (2 * mu * mu) <= mu * delta**2 / 2
        assert max((a - b) ** 2 for a, b in zip(boxed, u)) <= delta**2
        counts["boxed_approximate_pruning_certificates"] += 1


def pruning_case(graph, seed, mu, profile, counts):
    n, delta = len(graph), F(1, 32)
    degrees = [graph.degree(i) for i in graph]
    edge_list = list(graph.edges())
    budget = mu**3 * delta**2
    threshold = budget / len(edge_list)
    original = [[F(0)] * n for _ in range(n)]
    pruned = [[F(0)] * n for _ in range(n)]
    for i, d in enumerate(degrees):
        original[i][i] = pruned[i][i] = mu * d
    total_removed = F(0)
    for index, (i, j) in enumerate(edge_list):
        weight = threshold / 2 if profile == "all_tiny" or index % 2 else F(1)
        for matrix in [original] + ([pruned] if weight >= threshold else []):
            matrix[i][i] += weight
            matrix[j][j] += weight
            matrix[i][j] -= weight
            matrix[j][i] -= weight
        if weight < threshold:
            total_removed += weight
            counts["deleted_auxiliary_edges"] += 1
    load = [F(i == seed) - F(d, 16 * sum(degrees)) for i, d in enumerate(degrees)]
    assert sum(max(F(0), x) for x in load) <= 1
    assert all(sum(row) == mu * d for row, d in zip(pruned, degrees))
    assert total_removed <= budget
    counts["row_margin_preservation_checks"] += n
    certify_pruning(original, pruned, load, mu, delta, total_removed, counts)


def support_flip(mu, counts):
    delta = F(1, 32)
    edge = mu**3 * delta**2 / 4
    original = [[mu + edge, -edge], [-edge, mu + edge]]
    pruned = [[mu, F(0)], [F(0), mu]]
    load = [F(1), -edge / (2 * mu)]
    assert obstacle(original, load)[1] > 0
    assert obstacle(pruned, load)[1] == 0
    certify_pruning(original, pruned, load, mu, delta, edge, counts)
    counts["designed_strict_support_changes"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started, counts = time.monotonic(), Counter()
    max_n = 5 if args.full else 3
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed, mu, profile in itertools.product(
            graph, [F(1, 2), F(1, 1024)], ["mixed", "all_tiny"]
        ):
            pruning_case(graph, seed, mu, profile, counts)
    for mu in [F(1, 2), F(1, 1024)]:
        support_flip(mu, counts)
    result = {
        "audit": "incremental_active_set_sdd.grounded_pruning_range",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "range_graph_family": "universal physical seed joined to a path; original graph simple and unweighted",
        "range_stopping_rule": "verify full positive original obstacle KKT and exact local Schur quadratic coupling",
        "pruning_graph_family": "supplied grounded auxiliary matrices on all connected atlas graphs through max_n, every seed, mixed or all-tiny edge weights",
        "max_n": max_n,
        "distinct_pruning_graphs": len(graphs),
        "grounding_mu": ["1/2", "1/1024"],
        "coordinate_delta": "1/32",
        "pruning_threshold": "mu^3*delta^2/m; positive load mass at most one",
        "pruning_load": "e_seed-original_degree/(16*original_total_volume)",
        "additional_support_flip_cases": {
            "vertices": 2,
            "grounding_mu": ["1/2", "1/1024"],
            "edge_weight": "mu^3*delta^2/4",
            "load": "(1,-edge_weight/(2*mu))",
            "expected_support_change": "second coordinate positive before deletion and zero afterwards",
        },
        "scope": "Range witness is an exact constrained-Schur local piece on a fully positive physical face, not a CPW execution. Two-piece capped VWFs preserve the grounded optimum after boxing. Pruning is a supplied-matrix energy/coordinate primitive, not a source compression replacement or local graph solver.",
        "audit_only": dict(counts),
        "range_witnesses": [
            hub_path(n) for n in ([3, 4, 8, 16, 32, 64, 128, 256] if args.full else [3, 4, 8])
        ],
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
