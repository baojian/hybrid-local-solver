#!/usr/bin/env python3
"""Random parameter sweep for the enhanced retained-prox local gates.

This is a dense floating-point regression, not a history theorem.  It records
whether each worst witness occurred while omniscient support was still absent
from the materialized face.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np

from retained_prox_experiment import run_retained_prox
from two_mask_experiments import random_connected_graph


MAXIMUM_METRICS = (
    "maximum_boundary_layer_order_ratio",
    "maximum_boundary_flux_gate_ratio",
    "maximum_exterior_omniscient_extrapolate_ratio",
    "maximum_pre_push_lower_deficit_ratio",
    "maximum_omniscient_domination_deficit",
    "maximum_shadow_residual_cover_deficit",
)
MINIMUM_METRICS = (
    "minimum_active_raw_momentum_compatibility_ratio",
    "minimum_post_clamp_extrapolate_margin_ratio",
)


def edges(adjacency: np.ndarray) -> list[list[int]]:
    return [
        [left, right]
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left, right]
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=500)
    parser.add_argument("--minimum-vertices", type=int, default=6)
    parser.add_argument("--maximum-vertices", type=int, default=30)
    parser.add_argument("--relative-width", type=float, default=1.0e-2)
    parser.add_argument("--seed", type=int, default=2026090113)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    extrema: dict[str, dict[str, object] | None] = {
        metric: None for metric in MAXIMUM_METRICS + MINIMUM_METRICS
    }
    completed = 0
    skipped = 0
    growing = 0

    for trial in range(args.runs):
        vertex_count = int(
            rng.integers(args.minimum_vertices, args.maximum_vertices + 1)
        )
        probability = float(rng.uniform(1.1, 4.5) / vertex_count)
        adjacency = random_connected_graph(rng, vertex_count, probability)
        alpha = float(10 ** rng.uniform(-5.0, -0.5))
        rho_fraction = float(10 ** rng.uniform(-3.0, math.log10(0.95)))
        try:
            result = run_retained_prox(
                adjacency,
                alpha,
                rho_fraction / adjacency[0].sum(),
                relative_width=args.relative_width,
                maximum_phase_iterations=100_000,
                publication_floor=0.0,
                positive_append=True,
                residual_push=True,
            )
        except (AssertionError, RuntimeError, np.linalg.LinAlgError):
            skipped += 1
            continue

        completed += 1
        is_growing = bool(result["maximum_missing_omniscient_after_closure"])
        growing += int(is_growing)
        for metric in MAXIMUM_METRICS + MINIMUM_METRICS:
            value = float(result[metric])
            if not math.isfinite(value):
                continue
            previous = extrema[metric]
            wants_minimum = metric in MINIMUM_METRICS
            improves = previous is None or (
                value < float(previous["value"])
                if wants_minimum
                else value > float(previous["value"])
            )
            if improves:
                extrema[metric] = {
                    "value": value,
                    "trial": trial,
                    "vertices": vertex_count,
                    "alpha": alpha,
                    "rho_fraction": rho_fraction,
                    "growing": is_growing,
                    "edges": edges(adjacency),
                }

    print(
        json.dumps(
            {
                "warning": "finite dense floating-point sweep, not a theorem",
                "requested_runs": args.runs,
                "completed_runs": completed,
                "skipped_runs": skipped,
                "growing_face_runs": growing,
                "seed": args.seed,
                "relative_width": args.relative_width,
                "extrema": extrema,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
