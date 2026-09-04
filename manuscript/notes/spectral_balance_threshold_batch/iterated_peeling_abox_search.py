#!/usr/bin/env python3
"""Search the certified approximate-box test after repeated peeling passes.

This is a dense floating-point counterexample search, not a charged solver.
It samples genuine positive SafeBoxLC input states on canonical simple unit
graphs and repeatedly peels toward one fixed momentum-box endpoint.
"""

from __future__ import annotations

import argparse
import json
import math

import networkx as nx
import numpy as np

from retained_prox_experiment import exact_obstacle_solution, normalized_operator
from safe_box_linear_coupling_experiment import safe_trial


def canonical_instance(
    adjacency: np.ndarray, alpha: float, source: int, rho_fraction: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    matrix, degrees = normalized_operator(adjacency, alpha)
    roots = np.sqrt(degrees)
    rho = rho_fraction / degrees[source]
    load = -alpha * rho * roots
    load[source] += alpha / roots[source]
    optimum = exact_obstacle_solution(matrix, load)
    return matrix, load, optimum


def sample_state(
    matrix: np.ndarray,
    optimum: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    size = len(optimum)
    slack = np.exp(rng.uniform(-5.0, 2.0, size=size))
    response = np.linalg.solve(matrix, slack)
    scale = 0.8 * float(np.min(optimum / response))
    scale *= math.exp(rng.uniform(-7.0, 0.0))
    current = optimum - scale * response
    displacement = np.exp(rng.uniform(-6.0, 3.0, size=size))
    displacement *= math.exp(rng.uniform(-7.0, 2.0))
    estimate = current + displacement
    return current, estimate


def landscape_state(
    matrix: np.ndarray,
    roots: np.ndarray,
    root: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Realize an arbitrary first-pass freeze field with Perron direction."""
    freeze = rng.random(len(roots))
    direction = roots.copy()
    slack = np.array(
        [
            (matrix @ (np.minimum(time, freeze) * direction))[index]
            for index, time in enumerate(freeze)
        ]
    )
    current = np.full(len(roots), 100.0)
    load = matrix @ current + slack
    estimate = current + ((1.0 + root) / root) * direction
    return load, current, estimate


def audit(args: argparse.Namespace) -> dict[str, object]:
    rng = np.random.default_rng(args.seed)
    alphas = tuple(float(item) for item in args.alphas.split(","))
    worst_ratio = -math.inf
    witness: dict[str, object] = {}
    maximum_passes = 0
    failures = 0
    cases = 0

    for _ in range(args.graphs):
        seed = int(rng.integers(0, 2**32))
        graph = nx.random_labeled_tree(args.vertices, seed=seed)
        for left in range(args.vertices):
            for right in range(left + 1, args.vertices):
                if not graph.has_edge(left, right) and rng.random() < args.edge_probability:
                    graph.add_edge(left, right)
        adjacency = nx.to_numpy_array(graph, nodelist=range(args.vertices))
        edges = list(map(list, graph.edges()))

        for alpha in alphas:
            root = math.sqrt(alpha)
            source = int(rng.integers(0, args.vertices))
            matrix, load, optimum = canonical_instance(
                adjacency, alpha, source, args.rho_fraction
            )
            if np.min(optimum) <= 1.0e-10:
                continue
            for _ in range(args.states):
                current, estimate = sample_state(matrix, optimum, rng)
                trial = (current + root * estimate) / (1.0 + root)
                safe = current
                passed = False
                ratio = math.inf
                for pass_index in range(1, args.maximum_passes + 1):
                    safe, gap = safe_trial(matrix, load, safe, trial, "peel")
                    accepted = safe - current
                    credit = 0.5 * float(accepted @ matrix @ accepted)
                    credit += 0.5 * root * alpha * float(
                        np.linalg.norm(estimate - safe) ** 2
                    )
                    ratio = (1.0 + root) * gap / max(credit, 1.0e-300)
                    if pass_index == 2 and ratio > worst_ratio:
                        worst_ratio = ratio
                        witness = {
                            "vertices": args.vertices,
                            "edges": edges,
                            "alpha": alpha,
                            "source": source,
                            "rho_fraction": args.rho_fraction,
                            "current": current.tolist(),
                            "estimate": estimate.tolist(),
                            "trial": trial.tolist(),
                            "second_safe": safe.tolist(),
                            "second_ratio": ratio,
                        }
                    if ratio <= 1.0 + 5.0e-10:
                        maximum_passes = max(maximum_passes, pass_index)
                        passed = True
                        break
                cases += 1
                if not passed:
                    failures += 1
                    maximum_passes = max(maximum_passes, args.maximum_passes + 1)

            roots = np.sqrt(adjacency.sum(axis=1))
            for _ in range(args.landscapes):
                landscape_load, current, estimate = landscape_state(
                    matrix, roots, root, rng
                )
                trial = (current + root * estimate) / (1.0 + root)
                safe = current
                first_ratio = math.inf
                second_ratio = math.inf
                passed = False
                for pass_index in range(1, args.maximum_passes + 1):
                    safe, gap = safe_trial(
                        matrix, landscape_load, safe, trial, "peel"
                    )
                    accepted = safe - current
                    credit = 0.5 * float(accepted @ matrix @ accepted)
                    credit += 0.5 * root * alpha * float(
                        np.linalg.norm(estimate - safe) ** 2
                    )
                    ratio = (1.0 + root) * gap / max(credit, 1.0e-300)
                    if pass_index == 1:
                        first_ratio = ratio
                    if pass_index == 2:
                        second_ratio = ratio
                        if first_ratio > 1.0 and ratio > worst_ratio:
                            worst_ratio = ratio
                            witness = {
                                "kind": "prescribed-freeze-landscape",
                                "vertices": args.vertices,
                                "edges": edges,
                                "alpha": alpha,
                                "first_ratio": first_ratio,
                                "second_ratio": second_ratio,
                            }
                    if ratio <= 1.0 + 5.0e-10:
                        maximum_passes = max(maximum_passes, pass_index)
                        passed = True
                        break
                cases += 1
                if not passed:
                    failures += 1
                    maximum_passes = max(maximum_passes, args.maximum_passes + 1)

    return {
        "warning": "dense floating-point search only",
        "seed": args.seed,
        "cases": cases,
        "failures": failures,
        "maximum_passes": maximum_passes,
        "worst_second_pass_ratio": worst_ratio,
        "witness": witness,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=8)
    parser.add_argument("--graphs", type=int, default=100)
    parser.add_argument("--states", type=int, default=200)
    parser.add_argument("--landscapes", type=int, default=0)
    parser.add_argument("--alphas", default=".3,.1,.03,.01,.003,.001")
    parser.add_argument("--rho-fraction", type=float, default=1.0e-5)
    parser.add_argument("--edge-probability", type=float, default=0.25)
    parser.add_argument("--maximum-passes", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260904)
    args = parser.parse_args()
    print(json.dumps(audit(args), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
