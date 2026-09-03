#!/usr/bin/env python3
"""Deterministic audit of a direct safe-box gradient/NAG candidate.

The candidate is deliberately simpler than the retained-prox implementation:
it safeguards the ordinary momentum trial inside the already certified
support, admits every positive exterior residual, and then takes one
unit-smooth gradient step.  ``box`` uses the exact greatest safe point;
``peel`` uses the support-linear one-pass approximation.

Dense solves and full residuals are used only for small-instance ground truth
and auditing.  They are not charged implementations of the local algorithm.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math

import networkx as nx
import numpy as np

from retained_prox_experiment import exact_obstacle_solution, normalized_operator


def exact_safe_box(
    matrix: np.ndarray,
    load: np.ndarray,
    previous: np.ndarray,
    current: np.ndarray,
    momentum: float,
) -> tuple[np.ndarray, float]:
    trial = current + momentum * (current - previous)
    support = np.flatnonzero(current > 1.0e-14)
    safe = np.zeros_like(current)
    if not len(support):
        return safe, 0.0
    block = matrix[np.ix_(support, support)]
    raw_residual = load[support] - block @ trial[support]
    correction = exact_obstacle_solution(block, -raw_residual)
    safe[support] = trial[support] - correction
    slack = load[support] - block @ safe[support]
    complementarity_gap = float(correction @ slack)
    if np.min(safe[support] - current[support]) < -2.0e-10:
        raise AssertionError("exact safe-box point fell below the current lower bracket")
    if np.min(slack) < -2.0e-10:
        raise AssertionError("exact safe-box point is not a subsolution")
    if abs(complementarity_gap) > 2.0e-9:
        raise AssertionError("exact safe-box correction is not complementary")
    return safe, max(0.0, complementarity_gap)


def peeling_safe_box(
    matrix: np.ndarray,
    load: np.ndarray,
    previous: np.ndarray,
    current: np.ndarray,
    momentum: float,
) -> tuple[np.ndarray, float]:
    trial = current + momentum * (current - previous)
    support = np.flatnonzero(current > 1.0e-14)
    safe = np.zeros_like(current)
    if not len(support):
        return safe, 0.0

    block = matrix[np.ix_(support, support)]
    direction = trial[support] - current[support]
    starting_slack = load[support] - block @ current[support]
    increment = np.zeros(len(support))
    moving = set(map(int, np.flatnonzero(direction > 1.0e-15)))
    elapsed = 0.0
    while moving and elapsed < 1.0 - 1.0e-14:
        moving_direction = np.zeros(len(support))
        moving_indices = np.array(sorted(moving), dtype=int)
        moving_direction[moving_indices] = direction[moving_indices]
        pressure = block @ moving_direction
        slack = starting_slack - block @ increment
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
        scale = max(1.0, float(np.max(np.abs(starting_slack))))
        for time, index in candidates:
            if abs(time - hit_time) <= 1.0e-12 * scale:
                moving.discard(index)

    safe[support] = current[support] + increment
    correction = trial[support] - safe[support]
    slack = load[support] - block @ safe[support]
    if np.min(safe[support] - current[support]) < -2.0e-10:
        raise AssertionError("peeling point fell below the current lower bracket")
    if np.min(trial[support] - safe[support]) < -2.0e-10:
        raise AssertionError("peeling point left the momentum box")
    if np.min(slack) < -2.0e-9:
        raise AssertionError("peeling point is not a subsolution")
    return safe, max(0.0, float(correction @ slack))


def run_candidate(
    adjacency: np.ndarray,
    alpha: float,
    rho_fraction: float,
    source: int,
    mode: str,
    relative_objective_tolerance: float,
    maximum_rounds: int,
) -> dict[str, object]:
    matrix, degrees = normalized_operator(adjacency, alpha)
    sqrt_degrees = np.sqrt(degrees)
    rho = rho_fraction / degrees[source]
    load = -alpha * rho * sqrt_degrees
    load[source] += alpha / sqrt_degrees[source]
    optimum = exact_obstacle_solution(matrix, load)
    optimum_support = set(map(int, np.flatnonzero(optimum > 1.0e-11)))
    optimum_value = float(0.5 * optimum @ matrix @ optimum - load @ optimum)
    initial_gap = -optimum_value
    tolerance = relative_objective_tolerance * initial_gap

    root = math.sqrt(alpha)
    momentum = (1.0 - root) / (1.0 + root)
    previous = np.zeros(len(adjacency))
    current = np.zeros(len(adjacency))
    volume_work = 0.0
    total_peeling_gap = 0.0
    maximum_gap_charge_ratio = 0.0
    support_events = 0
    minimum_active_residual = math.inf
    cumulative_weighted_support_injection = 0.0
    maximum_normalized_support_injection = 0.0
    optimum_support_rows = np.array(sorted(optimum_support), dtype=int)

    safeguard = exact_safe_box if mode == "box" else peeling_safe_box
    for round_index in range(maximum_rounds):
        previous_signed_residual = load - matrix @ previous
        current_signed_residual = load - matrix @ current
        previous_negative_slack = np.maximum(-previous_signed_residual, 0.0)
        current_negative_slack = np.maximum(-current_signed_residual, 0.0)
        if np.max(current_negative_slack - previous_negative_slack) > 3.0e-9:
            raise AssertionError("inactive negative slack is not monotone")
        support_injection = np.maximum(
            momentum * previous_negative_slack - (1.0 + momentum) * current_negative_slack,
            0.0,
        )
        if len(optimum_support_rows):
            cumulative_weighted_support_injection += float(
                sqrt_degrees[optimum_support_rows] @ support_injection[optimum_support_rows]
            )
            if momentum * alpha * rho > 0.0:
                maximum_normalized_support_injection = max(
                    maximum_normalized_support_injection,
                    float(
                        np.max(
                            support_injection[optimum_support_rows]
                            / sqrt_degrees[optimum_support_rows]
                        )
                        / (momentum * alpha * rho)
                    ),
                )
        safe_input, peeling_gap = safeguard(
            matrix,
            load,
            previous,
            current,
            momentum,
        )
        input_residual = load - matrix @ safe_input
        positive_rows = set(map(int, np.flatnonzero(input_residual > 1.0e-13)))
        if not positive_rows.issubset(optimum_support):
            raise AssertionError("a positive input residual left the true support")
        active_rows = set(map(int, np.flatnonzero(safe_input > 1.0e-14))) | positive_rows
        if active_rows:
            minimum_active_residual = min(
                minimum_active_residual,
                float(np.min(input_residual[np.array(sorted(active_rows), dtype=int)])),
            )
        next_current = safe_input + np.maximum(input_residual, 0.0)
        next_residual = load - matrix @ next_current
        next_support = set(map(int, np.flatnonzero(next_current > 1.0e-13)))
        if not next_support.issubset(optimum_support):
            raise AssertionError("the safe gradient step left the true support")
        if next_support:
            active_next = np.array(sorted(next_support), dtype=int)
            if np.min(next_residual[active_next]) < -3.0e-9:
                raise AssertionError("the safe gradient output is not a subsolution")

        old_value = float(0.5 * previous @ matrix @ previous - load @ previous)
        next_value = float(0.5 * next_current @ matrix @ next_current - load @ next_current)
        two_step_decrease = old_value - next_value
        if peeling_gap > 1.0e-16:
            maximum_gap_charge_ratio = max(
                maximum_gap_charge_ratio,
                peeling_gap / max(momentum * two_step_decrease, 1.0e-300),
            )
        total_peeling_gap += peeling_gap
        support_events += len(next_support - set(map(int, np.flatnonzero(current > 1.0e-13))))
        if next_support:
            volume_work += float(np.sum(degrees[np.array(sorted(next_support), dtype=int)]))

        gap = next_value - optimum_value
        certificate = 0.5 * float(np.max(np.maximum(next_residual, 0.0) / sqrt_degrees))
        previous, current = current, next_current
        if certificate <= tolerance:
            if cumulative_weighted_support_injection > momentum * alpha + 3.0e-8:
                raise AssertionError("support-injection bank exceeded theta*alpha")
            if maximum_normalized_support_injection > 1.0 + 3.0e-8:
                raise AssertionError("a support injection exceeded theta*alpha*rho*h_i")
            normalized_rounds = (round_index + 1) * root / max(
                1.0,
                math.log(max(initial_gap / max(gap, 1.0e-300), 1.0)),
            )
            return {
                "rounds": round_index + 1,
                "normalized_rounds": normalized_rounds,
                "objective_gap": gap,
                "certificate": certificate,
                "support_events": support_events,
                "final_support_size": len(optimum_support),
                "volume_work": volume_work,
                "total_peeling_gap": total_peeling_gap,
                "maximum_gap_charge_ratio": maximum_gap_charge_ratio,
                "minimum_active_input_residual": minimum_active_residual,
                "cumulative_weighted_support_injection": (
                    cumulative_weighted_support_injection
                ),
                "maximum_normalized_support_injection": (
                    maximum_normalized_support_injection
                ),
            }
    raise RuntimeError("safe-box gradient audit exceeded its round limit")


def graph_from_edges(vertex_count: int, edges: list[tuple[int, int]]) -> np.ndarray:
    adjacency = np.zeros((vertex_count, vertex_count))
    for left, right in edges:
        adjacency[left, right] = adjacency[right, left] = 1.0
    return adjacency


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=5, choices=(2, 3, 4, 5, 6))
    parser.add_argument("--mode", choices=("box", "peel", "both"), default="both")
    parser.add_argument("--alphas", default=".3,.1,.03,.01,.003")
    parser.add_argument("--rho-fractions", default=".05,.2,.5,.8")
    parser.add_argument("--relative-tolerance", type=float, default=1.0e-8)
    parser.add_argument("--maximum-rounds", type=int, default=20000)
    args = parser.parse_args()

    alphas = tuple(float(value) for value in args.alphas.split(","))
    rho_fractions = tuple(float(value) for value in args.rho_fractions.split(","))
    modes = ("box", "peel") if args.mode == "both" else (args.mode,)
    atlas_graphs = [
        atlas_graph
        for atlas_graph in nx.graph_atlas_g()
        if len(atlas_graph) == args.vertices and nx.is_connected(atlas_graph)
    ]

    cases = 0
    extrema: dict[str, dict[str, object]] = {}
    for graph_index, atlas_graph in enumerate(atlas_graphs):
        adjacency = nx.to_numpy_array(atlas_graph, nodelist=range(args.vertices))
        edge_list = [list(edge) for edge in atlas_graph.edges()]
        for source, alpha, rho_fraction, mode in itertools.product(
            range(args.vertices), alphas, rho_fractions, modes
        ):
            result = run_candidate(
                adjacency,
                alpha,
                rho_fraction,
                source,
                mode,
                args.relative_tolerance,
                args.maximum_rounds,
            )
            cases += 1
            witness = {
                "graph_index": graph_index,
                "edges": edge_list,
                "source": source,
                "alpha": alpha,
                "rho_fraction": rho_fraction,
                "mode": mode,
            }
            for key in (
                "normalized_rounds",
                "maximum_gap_charge_ratio",
                "total_peeling_gap",
                "cumulative_weighted_support_injection",
                "maximum_normalized_support_injection",
            ):
                if key not in extrema or float(result[key]) > float(extrema[key]["value"]):
                    extrema[key] = {"value": result[key], **witness}
            key = "minimum_active_input_residual"
            if key not in extrema or float(result[key]) < float(extrema[key]["value"]):
                extrema[key] = {"value": result[key], **witness}

    print(
        json.dumps(
            {
                "warning": "deterministic finite audit, not a graph-uniform theorem",
                "vertices": args.vertices,
                "connected_graphs": len(atlas_graphs),
                "cases": cases,
                "modes": modes,
                "alphas": alphas,
                "rho_fractions": rho_fractions,
                "relative_tolerance": args.relative_tolerance,
                "extrema": extrema,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
