#!/usr/bin/env python3
"""One degree-shock leakage attempt before the certified Green endpoint."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from green_ball_high_accuracy_benchmark import green_radius
from leakage_screen_benchmark import direct_priority_ppr, fixed_cg_to_error
from mass_capture_diagnostic import distances
from portfolio_benchmark import (
    appr_envelope,
    binary_tree,
    broom_graph,
    cycle_graph,
    grid_graph,
    normalized_matrix,
    path_graph,
    star_graph,
)
from single_ball_leakage_oracle import leakage_upper


@dataclass(frozen=True)
class DegreeShockRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    shock_radius: int
    green_radius: int
    shock_attempted: bool
    shock_passed: bool
    envelope_volume: int
    exposure_work: int
    shock_cg_iterations: int
    shock_work: int
    final_cg_iterations: int
    final_work: int
    total_work: int
    direct_work: int
    ratio: float
    semantic_error: float


def first_degree_shock(adjacency: list[list[int]], distance: np.ndarray, final_radius: int) -> int:
    """Return the radius immediately before the first 8x degree jump."""
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    for radius in range(final_radius):
        current = distance <= radius
        following = distance == radius + 1
        if not np.any(following):
            break
        typical = float(np.median(degree[current]))
        if float(np.max(degree[following])) >= max(8.0, 8.0 * typical):
            return radius
    return -1


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> DegreeShockRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    reference = np.asarray(spsolve(matrix, source))
    _fifo, _support, fifo_work, _pushes = appr_envelope(adjacency, alpha, epsilon, seed)
    _priority, priority_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    direct_work = min(fifo_work, priority_work)
    cap = max(1, int(np.floor(2.0 / epsilon)))
    distance = distances(adjacency, seed)
    certified_radius = green_radius(alpha, epsilon / 2.0)
    maximum_radius = min(certified_radius, int(np.max(distance)))
    final_envelope = distance <= maximum_radius
    final_volume = int(degree[final_envelope].sum())
    if final_volume > cap:
        # The executable portfolio abandons this lane before the cap.  The
        # direct lane remains independently certified.
        return DegreeShockRow(
            family,
            len(adjacency),
            alpha,
            epsilon,
            -1,
            certified_radius,
            False,
            False,
            0,
            cap,
            0,
            0,
            0,
            0,
            cap + direct_work,
            direct_work,
            (cap + direct_work) / direct_work,
            float("nan"),
        )

    shock_radius = first_degree_shock(adjacency, distance, maximum_radius)
    shock_attempted = shock_radius >= 0
    shock_passed = False
    shock_iterations = shock_work = 0
    shock_candidate = None
    shock_envelope = None
    if shock_attempted:
        shock_envelope = distance <= shock_radius
        shock_indices = np.flatnonzero(shock_envelope)
        shock_principal = matrix[shock_indices][:, shock_indices]
        shock_candidate, shock_iterations, error_bar = fixed_cg_to_error(
            shock_principal,
            source[shock_indices],
            alpha,
            epsilon / 2.0,
            np.zeros(len(shock_indices)),
        )
        maximum, boundary_work = leakage_upper(
            adjacency,
            degree,
            shock_envelope,
            shock_candidate,
            error_bar,
            alpha,
        )
        shock_volume = int(degree[shock_envelope].sum())
        shock_work = shock_iterations * shock_volume + boundary_work
        shock_passed = maximum <= alpha * epsilon / 2.0 * (1 + 1e-10)
        if shock_passed:
            output = np.zeros(len(adjacency))
            output[shock_indices] = shock_candidate
            error = float(np.max(np.abs((output - reference) / root_degree)))
            if error > epsilon * (1 + 1e-7):
                raise AssertionError("degree-shock leakage certificate failed")
            total = shock_volume + shock_work
            return DegreeShockRow(
                family,
                len(adjacency),
                alpha,
                epsilon,
                shock_radius,
                certified_radius,
                True,
                True,
                shock_volume,
                shock_volume,
                shock_iterations,
                shock_work,
                0,
                0,
                total,
                direct_work,
                total / direct_work,
                error,
            )

    final_indices = np.flatnonzero(final_envelope)
    initial = np.zeros(len(final_indices))
    if shock_candidate is not None and shock_envelope is not None:
        final_position = {int(vertex): offset for offset, vertex in enumerate(final_indices)}
        for offset, vertex in enumerate(np.flatnonzero(shock_envelope)):
            initial[final_position[int(vertex)]] = shock_candidate[offset]
    candidate, final_iterations, _bar = fixed_cg_to_error(
        matrix[final_indices][:, final_indices],
        source[final_indices],
        alpha,
        epsilon / 2.0,
        initial,
    )
    output = np.zeros(len(adjacency))
    output[final_indices] = candidate
    error = float(np.max(np.abs((output - reference) / root_degree)))
    if error > epsilon * (1 + 1e-7):
        raise AssertionError("degree-shock Green endpoint missed target")
    final_work = final_iterations * final_volume
    total = final_volume + shock_work + final_work
    return DegreeShockRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        shock_radius,
        certified_radius,
        shock_attempted,
        shock_passed,
        final_volume,
        final_volume,
        shock_iterations,
        shock_work,
        final_iterations,
        final_work,
        total,
        direct_work,
        total / direct_work,
        error,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    graphs = [
        ("path-96", path_graph(96)),
        ("cycle-96", cycle_graph(96)),
        ("star-96", star_graph(95)),
        ("binary-depth-7", binary_tree(7)),
        ("broom-48-47", broom_graph(48, 47)),
        ("grid-12x12", grid_graph(12, 12)),
    ]
    rows = [
        run_case(family, graph, alpha, epsilon)
        for family, graph in graphs
        for alpha in (0.01, 0.04, 0.16)
        for epsilon in (0.0001, 0.0005, 0.001, 0.002, 0.005)
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=asdict(rows[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    wins = [row for row in rows if row.ratio < 1]
    shocks = [row for row in rows if row.shock_attempted]
    passes = [row for row in shocks if row.shock_passed]
    print(
        f"rows={len(rows)} shocks={len(shocks)} passes={len(passes)} "
        f"wins={len(wins)} median={np.median([row.ratio for row in rows]):.6f}"
    )
    for row in sorted(wins, key=lambda item: item.ratio):
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"ratio={row.ratio:.6f}",
            f"shock={row.shock_radius}",
            f"passed={row.shock_passed}",
        )


if __name__ == "__main__":
    main()
