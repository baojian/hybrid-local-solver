#!/usr/bin/env python3
"""Bounded floating search for the next paired-leaf zero-root extension.

This is a candidate finder only.  Every hit must be replayed by the
Fraction-exact tracer and receive the full equality/continuity audit before
it can enter the counterexample atlas.
"""

from __future__ import annotations

import argparse
import json

import numpy as np

from beta_stopped_input_cone_zero_root_search import evaluate_zero_root
from stopped_masked_input_residual_beta_04890_twelve_leaf_zero_root_limit_audit_exact import (
    BETA_04890_TWELVE_LEAF_ZERO_ROOT_EDGES,
    BETA_04890_TWELVE_LEAF_ZERO_ROOT_VERTICES,
)
from stopped_masked_input_residual_beta_04892_sixteen_leaf_zero_root_limit_audit_exact import (
    BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES,
    BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_VERTICES,
)


E14_ADDITIONS = ((2, 39), (20, 40))


def adjacency_from_edges(vertices: int, edges: tuple[tuple[int, int], ...]) -> np.ndarray:
    adjacency = np.zeros((vertices, vertices), dtype=np.float64)
    for left, right in edges:
        adjacency[left, right] = 1.0
        adjacency[right, left] = 1.0
    return adjacency


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        choices=("e12", "e14", "e16"),
        default="e12",
    )
    parser.add_argument("--beta", type=float, default=0.489)
    parser.add_argument("--rho-low", type=float, default=0.012)
    parser.add_argument("--rho-high", type=float, default=0.0135)
    parser.add_argument("--rho-count", type=int, default=151)
    parser.add_argument("--keep", type=int, default=30)
    args = parser.parse_args()

    if args.base == "e12":
        base_vertices = BETA_04890_TWELVE_LEAF_ZERO_ROOT_VERTICES
        base_edges = BETA_04890_TWELVE_LEAF_ZERO_ROOT_EDGES
    elif args.base == "e14":
        base_vertices = BETA_04890_TWELVE_LEAF_ZERO_ROOT_VERTICES + 2
        base_edges = tuple(
            sorted(
                set(BETA_04890_TWELVE_LEAF_ZERO_ROOT_EDGES)
                | set(E14_ADDITIONS)
            )
        )
    else:
        base_vertices = BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_VERTICES
        base_edges = BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES
    vertices = base_vertices + 2
    base = adjacency_from_edges(
        vertices,
        base_edges,
    )
    rho_values = np.linspace(args.rho_low, args.rho_high, args.rho_count)

    hits: list[dict[str, float | int]] = []
    evaluations = 0
    for left in range(1, base_vertices):
        for right in range(left, base_vertices):
            adjacency = base.copy()
            adjacency[left, base_vertices] = 1.0
            adjacency[base_vertices, left] = 1.0
            adjacency[right, base_vertices + 1] = 1.0
            adjacency[base_vertices + 1, right] = 1.0
            for rho_scale in rho_values:
                result = evaluate_zero_root(adjacency, rho_scale, args.beta)
                evaluations += 1
                status, failure, phase, product, vertex, lower, upper, total, _ = result
                if status != 1 or not (lower <= args.beta < upper):
                    continue
                hits.append(
                    {
                        "left_port": left,
                        "right_port": right,
                        "rho_scale": float(rho_scale),
                        "lower": float(lower),
                        "upper": float(upper),
                        "failure": float(failure),
                        "phase": phase,
                        "product": product,
                        "vertex": vertex,
                        "total_products": total,
                    }
                )

    hits.sort(key=lambda item: (item["upper"], -abs(item["failure"])), reverse=True)
    print(
        json.dumps(
            {
                "status": "floating-candidate-search-only",
                "base": args.base,
                "base_vertices": base_vertices,
                "target_beta": args.beta,
                "rho_range": [args.rho_low, args.rho_high, args.rho_count],
                "evaluations": evaluations,
                "hit_count": len(hits),
                "best_hits": hits[: args.keep],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
