#!/usr/bin/env python3
"""Empirical audit of a single global source-amplitude ramp.

This is a candidate chronology experiment, not a theorem.  It runs the
dual-projected two-mask recurrence while increasing the point-source load
once from zero to its final value.  Every lower-certified admission remains
support-safe because the exact obstacle supports are monotone in the source
amplitude.
"""

from __future__ import annotations

import json
import math

import numpy as np

from two_mask_experiments import (
    alternating_layers,
    delayed_publication_graph,
    green_band_stress_graph,
    lollipop,
)


def run_source_ramp(
    adjacency: np.ndarray,
    alpha: float,
    rho: float,
    ramp_root_units: float,
    *,
    maximum_iterations: int = 10_000,
    publication_tolerance: float = 1.0e-14,
) -> dict[str, object]:
    """Run one persistent critical-NAG clock with a monotone source ramp."""
    vertex_count = len(adjacency)
    degrees = adjacency.sum(axis=1)
    sqrt_degrees = np.sqrt(degrees)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    q_matrix = diagonal * np.eye(vertex_count) - coupling * adjacency / np.outer(
        sqrt_degrees,
        sqrt_degrees,
    )
    final_load = -alpha * rho * sqrt_degrees
    final_load[0] += alpha / sqrt_degrees[0]

    root = math.sqrt(alpha)
    beta = (1.0 - root) / (1.0 + root)
    auxiliary_scale = (1.0 - root) / root
    ramp_iterations = (
        0 if ramp_root_units <= 0.0 else max(1, math.ceil(ramp_root_units / root))
    )

    scratch = np.array([0], dtype=int)
    certified = {0}
    current = np.zeros(vertex_count)
    previous = np.zeros(vertex_count)
    lower = np.zeros(vertex_count)
    event_iterations: list[int] = []
    event_source_scales: list[float] = []
    event_batches: list[list[int]] = []
    volume_work = 0.0

    for iteration in range(maximum_iterations):
        source_scale = (
            1.0
            if ramp_iterations == 0
            else min(1.0, (iteration + 1) / ramp_iterations)
        )
        load = -alpha * rho * sqrt_degrees
        load[0] += source_scale * alpha / sqrt_degrees[0]

        extrapolated = current[scratch] + beta * (
            current[scratch] - previous[scratch]
        )
        next_iterate = np.zeros(vertex_count)
        next_iterate[scratch] = (
            extrapolated
            + load[scratch]
            - q_matrix[np.ix_(scratch, scratch)] @ extrapolated
        )
        previous, current = current, next_iterate
        volume_work += float(degrees[scratch].sum())

        active_residual = (
            load[scratch]
            - q_matrix[np.ix_(scratch, scratch)] @ current[scratch]
        )
        stationary_direction = (
            q_matrix[np.ix_(scratch, scratch)] @ sqrt_degrees[scratch]
        )
        ratios = np.divide(
            -active_residual,
            stationary_direction,
            out=np.full_like(active_residual, -np.inf),
            where=stationary_direction > 0.0,
        )
        shift = max(0.0, float(np.max(ratios)))
        lower[scratch] = np.maximum(
            lower[scratch],
            current[scratch] - shift * sqrt_degrees[scratch],
        )

        auxiliary = current + auxiliary_scale * (current - previous)
        current[scratch] = np.maximum(current[scratch], lower[scratch])
        auxiliary[scratch] = np.maximum(auxiliary[scratch], lower[scratch])
        velocity = (auxiliary[scratch] - current[scratch]) / auxiliary_scale
        previous[scratch] = current[scratch] - velocity

        full_residual = load - q_matrix @ lower
        outside = np.array(
            sorted(set(range(vertex_count)) - certified),
            dtype=int,
        )
        batch = np.array([], dtype=int)
        if len(outside):
            batch = outside[full_residual[outside] > publication_tolerance]
        if len(batch):
            scratch_residual = (
                load[batch]
                - q_matrix[np.ix_(batch, scratch)] @ current[scratch]
            )
            assert np.min(scratch_residual) >= -1.0e-10
            scratch = np.sort(np.r_[scratch, batch])
            certified.update(map(int, batch))
            event_iterations.append(iteration)
            event_source_scales.append(source_scale)
            event_batches.append(list(map(int, batch)))

        if source_scale < 1.0 or len(batch):
            continue
        outside = np.array(
            sorted(set(range(vertex_count)) - certified),
            dtype=int,
        )
        exterior_quiet = (
            not len(outside)
            or np.max((final_load - q_matrix @ lower)[outside])
            <= publication_tolerance
        )
        active_residual = (
            final_load[scratch]
            - q_matrix[np.ix_(scratch, scratch)] @ lower[scratch]
        ) / sqrt_degrees[scratch]
        if exterior_quiet and np.linalg.norm(active_residual) <= max(
            1.0e-13,
            alpha * rho / 100.0,
        ):
            return {
                "terminated": True,
                "iterations": iteration + 1,
                "scaled_iterations": (iteration + 1) * root,
                "ramp_iterations": ramp_iterations,
                "ramp_root_units": ramp_iterations * root,
                "post_ramp_iterations": iteration + 1 - ramp_iterations,
                "post_ramp_root_units": (iteration + 1 - ramp_iterations) * root,
                "event_iterations": event_iterations,
                "event_source_scales": event_source_scales,
                "event_batches": event_batches,
                "scratch_size": len(scratch),
                "scratch_volume": float(degrees[scratch].sum()),
                "volume_work": volume_work,
            }

    return {
        "terminated": False,
        "iterations": maximum_iterations,
        "scaled_iterations": maximum_iterations * root,
        "ramp_iterations": ramp_iterations,
        "ramp_root_units": ramp_iterations * root,
        "post_ramp_iterations": maximum_iterations - ramp_iterations,
        "post_ramp_root_units": (maximum_iterations - ramp_iterations) * root,
        "event_iterations": event_iterations,
        "event_source_scales": event_source_scales,
        "event_batches": event_batches,
        "scratch_size": len(scratch),
        "scratch_volume": float(degrees[scratch].sum()),
        "volume_work": volume_work,
    }


def main() -> None:
    cases = [
        ("delayed34", delayed_publication_graph(), 1.0e-3, 1.0e-5),
        (
            "green40",
            green_band_stress_graph(),
            1.0e-3,
            16_294_035_977_595_616 / 10**22,
        ),
        ("layers", alternating_layers(10, 3), 1.0e-3, 1.0e-5),
        ("lollipop", lollipop(4, 72), 1.0e-3, 1.0e-5),
    ]
    results: dict[str, dict[str, object]] = {}
    for name, adjacency, alpha, rho_scale in cases:
        rho = rho_scale / adjacency[0].sum()
        results[name] = {}
        for ramp_root_units in (0.0, 1.0, 2.0, 4.0, 8.0):
            result = run_source_ramp(
                adjacency,
                alpha,
                rho,
                ramp_root_units,
            )
            last_event = max(result["event_iterations"], default=-1)
            results[name][str(ramp_root_units)] = {
                "terminated": result["terminated"],
                "scaled_iterations": result["scaled_iterations"],
                "ramp_root_units": result["ramp_root_units"],
                "post_ramp_root_units": result["post_ramp_root_units"],
                "events": len(result["event_iterations"]),
                "last_event_iteration": last_event,
                "scaled_event_horizon": (last_event + 1) * math.sqrt(alpha),
                "largest_event_source_scale": max(
                    result["event_source_scales"],
                    default=0.0,
                ),
                "scratch_size": result["scratch_size"],
                "scratch_volume": result["scratch_volume"],
                "volume_work": result["volume_work"],
            }
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
