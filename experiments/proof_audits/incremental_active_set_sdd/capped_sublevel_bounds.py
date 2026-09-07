"""Original capped-objective coercivity and a degree-only ACL shortcut.

The sublevel bound controls feasible points of the original capped
objective, not arbitrary recursive or extrapolated solver queries.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from diffusion_accuracy_bridge import objective
from geometric_value_events import obstacle
import networkx as nx


class DegreeOnly:
    def __init__(self, seed, degree):
        self.seed, self.original_degree, self.counts = seed, degree, Counter()

    def degree(self, i):
        assert i == self.seed
        self.counts["original_seed_degree_queries"] += 1
        return self.original_degree

    def row(self, _):
        raise AssertionError("The shortcut must not read adjacency")


def seed_shortcut(oracle, seed, alpha, eps):
    degree = oracle.degree(seed)
    if eps * degree >= 1:
        return [], "zero"
    gamma = (1 - alpha) / (1 + alpha)
    if gamma <= eps * degree:
        return [(seed, F(1, degree))], "seed_only"
    return None, "continue"


def capped_value(matrix, load, degrees, bar, x):
    cap = 1 / bar
    return objective(matrix, load, x) - sum(
        bar * d * max(F(0), t - cap) ** 2 / 2 for d, t in zip(degrees, x)
    )


def case(graph, seed, alpha, eps, rng, counts):
    gamma = (1 - alpha) / (1 + alpha)
    bar, lam = 1 - gamma, eps / 2
    degrees = [graph.degree(i) for i in graph]
    oracle = DegreeOnly(seed, degrees[seed])
    result, branch = seed_shortcut(oracle, seed, alpha, eps)
    assert oracle.counts["original_seed_degree_queries"] == 1
    counts["shortcut_" + branch] += 1
    if result is None:
        assert gamma > eps * degrees[seed] >= eps
    else:
        vector = dict(result)
        for i in graph:
            residual = (
                F(i == seed)
                - degrees[i] * vector.get(i, 0)
                + gamma * sum(vector.get(j, 0) for j in graph[i])
            )
            assert 0 <= residual <= eps * degrees[i]
        counts["shortcut_original_ACL_certificates"] += 1
    matrix = [
        [F(degrees[i]) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * d for i, d in enumerate(degrees)]
    cap = 1 / bar
    for i, (d, b) in enumerate(zip(degrees, load)):
        # Exact minimum of q_i(x)-lambda*x over its quadratic interval and ray.
        coefficient = b + lam
        minimizer = max(F(0), min(cap, coefficient / (bar * d)))
        minimum = bar * d * minimizer**2 / 2 - coefficient * minimizer
        tail_slope = bar * d * cap - coefficient
        assert tail_slope >= 0
        assert minimum >= (-1 / (2 * bar) if i == seed else 0)
        counts["complete_capped_vertex_sublevel_bounds"] += 1
    exact = obstacle(matrix, load)
    vectors = [[F(0)] * len(graph), exact]
    vectors += [
        [rng.choice([F(0), F(1, 2), F(1), F(2), F(8)]) * cap for _ in graph] for _ in range(8)
    ]
    for x in vectors:
        energy = capped_value(matrix, load, degrees, bar, x)
        assert energy >= lam * sum(x) - 1 / (2 * bar)
        counts["original_capped_energy_coercivity_checks"] += 1
        if energy <= 0:
            assert sum(x) <= 1 / (2 * bar * lam)
            counts["feasible_nonpositive_energy_coordinate_bounds"] += 1
    counts["complete_original_graph_cases"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started, rng, counts = time.monotonic(), random.Random(73128), Counter()
    max_n = 5 if args.full else 3
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed, alpha in itertools.product(graph, [F(1, 3), F(1, 1009), F(1008, 1009)]):
            degree = graph.degree(seed)
            for eps in [
                F(1, degree),
                F(1, 2 * degree),
                F(1, degree + 1),
                F(1, 8 * sum(dict(graph.degree()).values())),
            ]:
                case(graph, seed, alpha, eps, rng, counts)
    implicit = []
    for leaves in [16, 10**12, 10**30]:
        oracle = DegreeOnly(0, leaves)
        eps, alpha = F(1, 2 * leaves), F(1, 3)
        result, branch = seed_shortcut(oracle, 0, alpha, eps)
        assert branch == "seed_only" and result == [(0, F(1, leaves))]
        assert F(1, 2 * leaves) <= eps
        implicit.append(
            {
                "graph": "star with the center as physical seed",
                "ambient_leaves": leaves,
                "alpha": str(alpha),
                "eps_appr": str(eps),
                "physical_seed_value": str(result[0][1]),
                "original_degree_queries": 1,
                "adjacency_entries_read": 0,
                "certificate": "seed residual zero, every leaf residual exactly eps_appr",
            }
        )
    output = {
        "audit": "incremental_active_set_sdd.capped_sublevel_bounds",
        "arithmetic": "exact fractions",
        "random_seed": 73128,
        "graph_family": "all connected graph-atlas graphs through max_n, every physical seed; implicit center-seeded stars",
        "max_n": max_n,
        "distinct_explicit_graphs": len(graphs),
        "alpha": ["1/3", "1/1009", "1008/1009"],
        "eps_appr": "1/d_seed,1/(2*d_seed),1/(d_seed+1),1/(8*total_volume)",
        "stopping_rule": "degree-only zero or seed-only ACL certificate when applicable; otherwise gamma>eps_appr*d_seed. Exact capped vertex minima and ray slopes certify the sublevel inequality.",
        "capped_potential": "1/bar_alpha",
        "coercivity_bound": "E_cap(x)>=lambda*sum(x)-1/(2*bar_alpha), x>=0, lambda=eps_appr/2",
        "scope": "Implemented constant-work original-graph shortcut and a feasible original-objective bound. It does not bound all recursive or accelerated solver inputs or establish general OP3.",
        "audit_only": dict(counts),
        "implicit_shortcut_certificates": implicit,
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
        args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
