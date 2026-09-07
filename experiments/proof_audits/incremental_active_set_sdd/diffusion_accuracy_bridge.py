"""Exact diffusion accuracy-to-ACL bridge and a path curvature diagnostic.

The objective conversion does not supply a local constrained solver. The
unit-weight path refutes interpreting minimum edge weight as a universal
Dirichlet curvature bound; it does not assert a lower bound for OP3.
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

from geometric_value_events import obstacle
import networkx as nx


def quadratic(matrix, x):
    return sum(x[i] * sum(a * y for a, y in zip(row, x)) for i, row in enumerate(matrix))


def objective(matrix, b, x):
    return quadratic(matrix, x) / 2 - sum(a * y for a, y in zip(b, x))


def path_curvature(m):
    graph = nx.path_graph(m + 2)
    matrix = [
        [F(graph.degree(i)) if i == j else F(-1) if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    source_mass = F(2 * m + 1, 2)
    load = [source_mass * F(i == 0) - 1 for i in graph]
    x = [F((m - i) ** 2, 2) if i < m else F(0) for i in graph]
    slack = [sum(a * y for a, y in zip(row, x)) - b for row, b in zip(matrix, load)]
    assert all(s == 0 if value else s >= 0 for s, value in zip(slack, x))
    assert slack[m] == F(1, 2)
    principal = [row[:m] for row in matrix[:m]]
    z = [F(m - i) for i in range(m)]
    rayleigh = quadratic(principal, z) / sum(t * t for t in z)
    assert rayleigh == F(6, (m + 1) * (2 * m + 1))
    assert 2 * rayleigh < 1
    return {
        "active_vertices": m,
        "ambient_vertices": m + 2,
        "source_mass": str(source_mass),
        "sink_capacity_each_vertex": 1,
        "minimum_edge_weight": 1,
        "first_inactive_slack": str(slack[m]),
        "rayleigh_for_L_hessian": str(rayleigh),
        "rayleigh_for_2L_hessian": str(2 * rayleigh),
    }


def bridge_case(graph, seed, alpha, eps, counts):
    degrees = [graph.degree(i) for i in graph]
    gamma = (1 - alpha) / (1 + alpha)
    bar, lam = 1 - gamma, eps / 2
    assert eps * degrees[seed] < 1
    matrix = [
        [F(degrees[i]) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * degrees[i] for i in graph]
    exact = obstacle(matrix, load)
    optimum = objective(matrix, load, exact)
    singleton = [F(0)] * len(graph)
    singleton[seed] = load[seed] / degrees[seed]
    assert optimum <= objective(matrix, load, singleton) < -eps / 8
    assert -optimum <= 1 / (2 * bar)
    delta = eps / 8
    eta = bar * bar * delta * delta
    for i, sign in itertools.product(graph, [-1, 1]):
        step = F(1)
        while True:
            candidate = exact.copy()
            candidate[i] = max(F(0), candidate[i] + sign * step)
            energy = objective(matrix, load, candidate)
            gap = energy - optimum
            error = [a - b for a, b in zip(candidate, exact)]
            assert gap >= quadratic(matrix, error) / 2
            assert quadratic(matrix, error) >= bar * sum(d * e * e for d, e in zip(degrees, error))
            counts["convexity_and_grounding_gap_checks"] += 1
            if energy <= optimum / (1 + eta):
                break
            step /= 2
            counts["reference_perturbation_halvings"] += 1
        assert gap <= eta * (-optimum) / (1 + eta) <= bar * delta * delta / 2
        assert max(abs(e) for e in error) <= delta
        repaired = [max(F(0), t - delta) for t in candidate]
        assert all(0 <= u - t <= 2 * delta for u, t in zip(exact, repaired))
        residuals = [
            F(i == seed) - sum(a * y for a, y in zip(row, repaired)) for i, row in enumerate(matrix)
        ]
        assert all(0 <= r <= eps * d for r, d in zip(residuals, degrees))
        assert all(u > 0 for u, t in zip(exact, repaired) if t > 0)
        counts["multiplicative_energy_to_original_ACL_certificates"] += 1
        counts["clipped_inactive_candidate_coordinates"] += sum(
            u == 0 and t > 0 for u, t in zip(exact, candidate)
        )
    counts["complete_original_graph_cases"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts = Counter()
    graphs = [
        g
        for g in nx.graph_atlas_g()
        if 2 <= len(g) <= (5 if args.full else 3) and nx.is_connected(g)
    ]
    alphas = [F(1, 3), F(1, 1009), F(1008, 1009)]
    for graph in graphs:
        for seed, alpha in itertools.product(graph, alphas):
            d = graph.degree(seed)
            for eps in [F(1, 2 * d), F(1, d + 1), F(1, 8 * sum(dict(graph.degree()).values()))]:
                bridge_case(graph, seed, alpha, eps, counts)
    result = {
        "audit": "incremental_active_set_sdd.diffusion_accuracy_bridge",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph_family": "all connected graph-atlas graphs through max_n",
        "max_n": 5 if args.full else 3,
        "distinct_graphs": len(graphs),
        "physical_seed": "every vertex",
        "alpha": list(map(str, alphas)),
        "eps_appr": "1/(2*d_seed), 1/(d_seed+1), or 1/(8*original_total_volume)",
        "lambda": "eps_appr/2",
        "delta": "eps_appr/8",
        "relative_diffusion_eta": "bar_alpha^2*delta^2",
        "stopping_rule": "feasible candidate energy <= optimum/(1+eta); downward clip candidate-delta and verify every original ACL residual",
        "scope": "Accuracy conversion only; candidate generation uses exact reference optimum and halving and is not a local algorithm or imported source implementation.",
        "audit_only": dict(counts),
        "unit_weight_path_curvature": [path_curvature(m) for m in [3, 4, 8, 16, 32, 64, 128]],
        "curvature_scope": "Rayleigh upper bound disproves minimum-edge-weight curvature for both L and 2L Hessian conventions; no algorithmic lower bound or assertion about an unspecified source parameter.",
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "geometric_value_events": hashlib.sha256(
                Path(__file__).with_name("geometric_value_events.py").read_bytes()
            ).hexdigest()
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
