#!/usr/bin/env python3
"""Trace the zero-start two-vertex PeelingLC obstruction.

This is a deterministic dense audit for the canonical unit edge with source
zero.  It records the exact peeling event word after both coordinates enter
the support and reports the scaled error/velocity/slack variables.  The code
is deliberately independent of the generic safe-box experiment so that its
event bookkeeping can be checked directly.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np


def operator(alpha: float) -> np.ndarray:
    diagonal = (1.0 + alpha) / 2.0
    off_diagonal = (1.0 - alpha) / 2.0
    return np.array([[diagonal, -off_diagonal], [-off_diagonal, diagonal]])


def peel(
    matrix: np.ndarray,
    residual: np.ndarray,
    direction: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, str, tuple[float, ...]]:
    """Return safe increment, final slack, event word, and hit times."""

    dimension = len(direction)
    increment = np.zeros(dimension)
    moving = {
        index for index in range(dimension) if direction[index] > 1.0e-15
    }
    elapsed = 0.0
    events: list[str] = []
    times: list[float] = []
    while moving and elapsed < 1.0 - 1.0e-14:
        moving_direction = np.zeros(dimension)
        indices = np.array(sorted(moving), dtype=int)
        moving_direction[indices] = direction[indices]
        pressure = matrix @ moving_direction
        slack = residual - matrix @ increment
        candidates = [
            (elapsed + max(0.0, float(slack[index])) / float(pressure[index]), index)
            for index in moving
            if pressure[index] > 1.0e-15
        ]
        if not candidates:
            increment += (1.0 - elapsed) * moving_direction
            elapsed = 1.0
            break
        hit_time = min(time for time, _ in candidates)
        if hit_time >= 1.0 - 1.0e-14:
            increment += (1.0 - elapsed) * moving_direction
            elapsed = 1.0
            break
        increment += (hit_time - elapsed) * moving_direction
        elapsed = hit_time
        hit = tuple(index for time, index in candidates if abs(time - hit_time) <= 1.0e-12)
        events.append("".join(map(str, hit)))
        times.append(hit_time)
        moving.difference_update(hit)
    final_slack = residual - matrix @ increment
    return increment, final_slack, ">".join(events) or "full", tuple(times)


def run(alpha: float, rho: float, rounds: int, snapshots: set[int]) -> dict[str, object]:
    root = math.sqrt(alpha)
    matrix = operator(alpha)
    load = alpha * np.array([1.0 - rho, -rho])
    optimum = np.array([0.5 - rho + alpha / 2.0, 0.5 - rho - alpha / 2.0])
    current = np.zeros(2)
    estimate = np.zeros(2)
    event_counts: dict[str, int] = {}
    records: list[dict[str, object]] = []
    for round_index in range(1, rounds + 1):
        trial = (current + root * estimate) / (1.0 + root)
        direction = trial - current
        residual = load - matrix @ current
        active = np.flatnonzero(current > 1.0e-13)
        increment = np.zeros(2)
        slack = residual.copy()
        event = "empty"
        times: tuple[float, ...] = ()
        if len(active):
            block = matrix[np.ix_(active, active)]
            block_increment, block_slack, event, times = peel(
                block,
                residual[active],
                direction[active],
            )
            increment[active] = block_increment
            slack[active] = block_slack
        safe = current + increment
        full_residual = load - matrix @ safe
        gradient_rows = set(map(int, np.flatnonzero(current > 1.0e-13)))
        gradient_rows.update(map(int, np.flatnonzero(full_residual > 1.0e-13)))
        pushed = np.zeros(2)
        if gradient_rows:
            rows = np.array(sorted(gradient_rows), dtype=int)
            pushed[rows] = full_residual[rows]
        next_current = safe + pushed
        next_estimate = (1.0 - root) * estimate + root * safe + pushed / root

        event_counts[event] = event_counts.get(event, 0) + 1
        if round_index in snapshots:
            error = optimum - current
            velocity = estimate - current
            next_error = optimum - next_current
            records.append(
                {
                    "round": round_index,
                    "event": event,
                    "hit_times": times,
                    "support": list(map(int, active)),
                    "error": error.tolist(),
                    "velocity": velocity.tolist(),
                    "residual": residual.tolist(),
                    "direction": direction.tolist(),
                    "increment": increment.tolist(),
                    "final_residual": full_residual.tolist(),
                    "error_ratio": (next_error / error).tolist(),
                    "error_over_alpha": (error / alpha).tolist(),
                    "velocity_over_alpha": (velocity / alpha).tolist(),
                    "residual_over_alpha_squared": (residual / alpha**2).tolist(),
                }
            )
        current, estimate = next_current, next_estimate
    return {
        "alpha": alpha,
        "root": root,
        "rho_fraction": rho,
        "rounds": rounds,
        "optimum": optimum.tolist(),
        "event_counts": event_counts,
        "snapshots": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=1.0e-4)
    parser.add_argument(
        "--rho",
        type=float,
        default=None,
        help="source threshold; defaults to 1/2-sqrt(alpha)",
    )
    parser.add_argument("--rounds", type=int, default=22000)
    parser.add_argument(
        "--snapshots",
        default="1,2,3,4,5,10,20,50,100,200,500,1000,2000,5000,10000,15000,20000,22000",
    )
    args = parser.parse_args()
    snapshots = {int(value) for value in args.snapshots.split(",")}
    rho = 0.5 - math.sqrt(args.alpha) if args.rho is None else args.rho
    print(json.dumps(run(args.alpha, rho, args.rounds, snapshots), indent=2))


if __name__ == "__main__":
    main()
