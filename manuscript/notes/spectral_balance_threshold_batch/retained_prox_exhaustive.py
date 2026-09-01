#!/usr/bin/env python3
"""Exhaustive small-graph audit for the enhanced retained-prox recurrence.

This enumerates connected labelled simple unit graphs.  It is a finite
floating-point regression, not a theorem for arbitrary graph size.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math

import numpy as np

from retained_prox_experiment import run_retained_prox
from source_clock_adversary_search import connected
from two_mask_experiments import graph


MAXIMUM_METRICS = (
    "maximum_omniscient_domination_deficit",
    "maximum_shadow_residual_cover_deficit",
    "maximum_growing_progress_domination_ratio",
    "maximum_growing_adjacent_shadow_ratio",
    "maximum_relevant_primal_domination_ratio",
    "maximum_relevant_extrapolate_domination_ratio",
    "maximum_growing_relevant_extrapolate_domination_ratio",
    "maximum_exterior_omniscient_extrapolate_ratio",
    "maximum_boundary_flux_gate_ratio",
    "maximum_boundary_layer_order_ratio",
    "maximum_masked_frontier_extrapolate_over_lower_ratio",
    "maximum_pre_push_lower_deficit_ratio",
    "maximum_phase_root_time",
)
MINIMUM_METRICS = (
    "minimum_active_raw_momentum_compatibility_ratio",
    "minimum_post_clamp_extrapolate_margin_ratio",
)
METRICS = MAXIMUM_METRICS + MINIMUM_METRICS


def parse_floats(value: str) -> tuple[float, ...]:
    return tuple(float(item) for item in value.split(","))


def edge_list(adjacency: np.ndarray) -> list[tuple[int, int]]:
    return [
        (left, right)
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left, right]
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=4)
    parser.add_argument("--alphas", default=".003,.01,.03,.1")
    parser.add_argument("--rho-fractions", default=".001,.03,.1,.3,.7,.95")
    parser.add_argument("--relative-width", type=float, default=1.0e-2)
    parser.add_argument("--maximum-phase-iterations", type=int, default=5000)
    parser.add_argument("--baseline", action="store_true")
    args = parser.parse_args()
    if args.vertices < 2 or args.vertices > 6:
        raise ValueError("the exhaustive driver is intentionally limited to 2--6 vertices")

    alphas = parse_floats(args.alphas)
    rho_fractions = parse_floats(args.rho_fractions)
    pairs = list(itertools.combinations(range(args.vertices), 2))
    worst: dict[str, dict[str, object]] = {
        metric: {"value": None} for metric in METRICS
    }
    connected_graphs = 0
    runs = 0
    skipped = 0

    for mask in range(1 << len(pairs)):
        adjacency = graph(
            args.vertices,
            [pairs[index] for index in range(len(pairs)) if mask >> index & 1],
        )
        if np.min(adjacency.sum(axis=1)) == 0 or not connected(adjacency):
            continue
        connected_graphs += 1
        source_degree = float(adjacency[0].sum())
        for alpha in alphas:
            for rho_fraction in rho_fractions:
                try:
                    result = run_retained_prox(
                        adjacency,
                        alpha,
                        rho_fraction / source_degree,
                        relative_width=args.relative_width,
                        maximum_phase_iterations=args.maximum_phase_iterations,
                        publication_floor=0.0,
                        positive_append=not args.baseline,
                        residual_push=not args.baseline,
                    )
                except (AssertionError, RuntimeError, np.linalg.LinAlgError):
                    skipped += 1
                    continue
                runs += 1
                for metric in METRICS:
                    value = float(result[metric])
                    previous_value = worst[metric]["value"]
                    if not math.isfinite(value):
                        continue
                    wants_minimum = metric in MINIMUM_METRICS
                    if previous_value is not None:
                        improves = (
                            value < float(previous_value)
                            if wants_minimum
                            else value > float(previous_value)
                        )
                        if not improves:
                            continue
                    worst[metric] = {
                        "value": value,
                        "alpha": alpha,
                        "rho_fraction": rho_fraction,
                        "edges": edge_list(adjacency),
                    }

    print(
        json.dumps(
            {
                "warning": "finite dense floating-point audit, not a theorem",
                "vertices": args.vertices,
                "connected_graphs": connected_graphs,
                "runs": runs,
                "skipped": skipped,
                "enhanced": not args.baseline,
                "alphas": alphas,
                "rho_fractions": rho_fractions,
                "relative_width": args.relative_width,
                "worst": worst,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
