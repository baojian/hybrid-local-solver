#!/usr/bin/env python3
"""Evolutionary counterexample search for the projected two-mask root clock.

The search is empirical only.  It mutates connected simple unit graphs and
maximizes total root-scaled iterations, with a secondary objective given by
the largest root-scaled inter-publication gap.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np

from retained_prox_experiment import run_retained_prox
from source_ramp_experiment import run_source_ramp
from two_mask_experiments import graph, run_projected_estimate_nag


def connected(adjacency: np.ndarray) -> bool:
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in np.flatnonzero(adjacency[vertex]):
            neighbor = int(neighbor)
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(adjacency)


def random_graph(rng: np.random.Generator, n: int, probability: float) -> np.ndarray:
    edges = [(vertex, int(rng.integers(vertex))) for vertex in range(1, n)]
    adjacency = graph(n, edges)
    for left in range(n):
        for right in range(left + 1, n):
            if adjacency[left, right] == 0 and rng.random() < probability:
                adjacency[left, right] = adjacency[right, left] = 1
    return adjacency


def path_like_graph(rng: np.random.Generator, n: int) -> np.ndarray:
    """A path backbone with a few chords, preserving a long publication front."""
    adjacency = graph(n, [(vertex, vertex + 1) for vertex in range(n - 1)])
    chord_count = int(rng.integers(0, max(2, n // 6)))
    for _ in range(chord_count):
        left = int(rng.integers(n))
        right = int(rng.integers(n - 1))
        if right >= left:
            right += 1
        if left > right:
            left, right = right, left
        adjacency[left, right] = adjacency[right, left] = 1
    return adjacency


def fixed_face_stop_seed(rng: np.random.Generator, n: int) -> np.ndarray:
    """Seed from the exact generic fixed-face lead stop, with optional tail."""
    base_edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (2, 9),
        (3, 4),
        (3, 9),
        (4, 5),
        (5, 6),
        (5, 8),
        (6, 7),
        (7, 8),
        (8, 9),
    ]
    if n < 10:
        raise ValueError("the fixed-stop seed requires at least 10 vertices")
    edges = list(base_edges)
    for vertex in range(10, n):
        edges.append((vertex - 1, vertex))
    adjacency = graph(n, edges)
    # Diversify the initial population without erasing the exact-stop core.
    return mutate(rng, adjacency, int(rng.integers(0, max(2, n // 8))))


def mutate(rng: np.random.Generator, adjacency: np.ndarray, flips: int) -> np.ndarray:
    candidate = adjacency.copy()
    n = len(candidate)
    for _ in range(flips):
        left = int(rng.integers(n))
        right = int(rng.integers(n - 1))
        if right >= left:
            right += 1
        if left > right:
            left, right = right, left
        candidate[left, right] = candidate[right, left] = 1 - candidate[left, right]
    if np.min(candidate.sum(axis=1)) == 0 or not connected(candidate):
        return adjacency.copy()
    return candidate


def evaluate(
    adjacency: np.ndarray,
    alpha: float,
    rho_scale: float,
    limit: int,
    objective: str,
    ramp_root_units: float,
    positive_append: bool = False,
    block_append: bool = False,
    residual_push: bool = False,
    residual_push_rounds: int = 1,
    input_residual_append: bool = False,
):
    rho = rho_scale / adjacency[0].sum()
    if objective.startswith("prox-"):
        full_result = run_retained_prox(
            adjacency,
            alpha,
            rho,
            relative_width=1.0e-3,
            maximum_phase_iterations=limit,
            publication_floor=0.0,
            positive_append=positive_append,
            block_append=block_append,
            residual_push=residual_push,
            residual_push_rounds=residual_push_rounds,
            input_residual_append=input_residual_append,
        )
        result = {key: value for key, value in full_result.items() if key != "phase_records"}
        phase_time = float(result["maximum_phase_root_time"])
        eventful_phase_time = float(result["maximum_eventful_phase_root_time"])
        domination_deficit = float(result["maximum_omniscient_domination_deficit"])
        domination_ratio = float(result["maximum_omniscient_domination_ratio"])
        progress_domination = float(result["maximum_progress_omniscient_domination_deficit"])
        growing_progress_domination_ratio = float(
            result["maximum_growing_progress_domination_ratio"]
        )
        shadow_residual_cover_deficit = float(result["maximum_shadow_residual_cover_deficit"])
        shadow_residual_cover_ratio = float(result["maximum_shadow_residual_cover_ratio"])
        pre_push_lower_deficit_ratio = float(result["maximum_pre_push_lower_deficit_ratio"])
        omniscient_over_one_jacobi_ratio = float(result["maximum_omniscient_over_one_jacobi_ratio"])
        shadow_increment_over_starting_lower_ratio = float(
            result["maximum_shadow_increment_over_starting_lower_ratio"]
        )
        relevant_shadow_increment_over_starting_lower_ratio = float(
            result["maximum_relevant_shadow_increment_over_starting_lower_ratio"]
        )
        adjacent_shadow_ratio = float(result["maximum_adjacent_shadow_ratio"])
        growing_adjacent_shadow_ratio = float(result["maximum_growing_adjacent_shadow_ratio"])
        relevant_primal_domination_ratio = float(result["maximum_relevant_primal_domination_ratio"])
        auxiliary_domination_deficit = float(result["maximum_same_time_auxiliary_deficit"])
        relevant_extrapolate_domination_ratio = float(
            result["maximum_relevant_extrapolate_domination_ratio"]
        )
        growing_relevant_extrapolate_domination_ratio = float(
            result["maximum_growing_relevant_extrapolate_domination_ratio"]
        )
        exterior_omniscient_primal_ratio = float(result["maximum_exterior_omniscient_primal_ratio"])
        exterior_omniscient_auxiliary_ratio = float(
            result["maximum_exterior_omniscient_auxiliary_ratio"]
        )
        exterior_omniscient_extrapolate_ratio = float(
            result["maximum_exterior_omniscient_extrapolate_ratio"]
        )
        boundary_flux_gate_ratio = float(result["maximum_boundary_flux_gate_ratio"])
        boundary_raw_gate_ratio = float(result["maximum_boundary_raw_gate_ratio"])
        boundary_layer_order_ratio = float(result["maximum_boundary_layer_order_ratio"])
        masked_frontier_extrapolate_over_lower_ratio = float(
            result["maximum_masked_frontier_extrapolate_over_lower_ratio"]
        )
        clamp_extrapolate_loss = -float(result["minimum_clamp_extrapolate_change_ratio"])
        post_clamp_extrapolate_violation = -float(
            result["minimum_post_clamp_extrapolate_margin_ratio"]
        )
        raw_momentum_compatibility_violation = -float(
            result["minimum_active_raw_momentum_compatibility_ratio"]
        )
        lag_one_deficit = float(result["maximum_lag_one_domination_deficit"])
        lag_one_primal = float(result["maximum_lag_one_primal_deficit"])
        lag_one_auxiliary = float(result["maximum_lag_one_auxiliary_deficit"])
        lag_primal_over_lower = float(result["maximum_lag_primal_over_lower_deficit"])
        lag_extrapolate_over_lower = float(result["maximum_lag_extrapolate_over_lower_deficit"])
        masked_retraction_shift_ratio = float(result["maximum_masked_retraction_shift_ratio"])
        post_push_current_over_lower_ratio = float(
            result["maximum_post_push_current_over_lower_ratio"]
        )
        masked_input_residual_violation = -float(result["minimum_masked_input_residual_ratio"])
        first_negative_input_witness = result.get(
            "first_negative_masked_input_residual_witness", {}
        )
        first_negative_predecessor_width_ratio = float(
            first_negative_input_witness.get("preceding_inner_width_ratio", -math.inf)
        )
        work_ratio = float(result["root_work_ratio"])
        events = float(result["events"])
        if objective == "prox-phase":
            score = (phase_time, work_ratio, events)
        elif objective == "prox-event-phase":
            score = (eventful_phase_time, phase_time, events)
        elif objective == "prox-domination":
            score = (domination_ratio, domination_deficit, events)
        elif objective == "prox-progress-domination":
            score = (growing_progress_domination_ratio, progress_domination, events)
        elif objective == "prox-residual-cover":
            score = (
                shadow_residual_cover_ratio,
                shadow_residual_cover_deficit,
                events,
            )
        elif objective == "prox-pre-push-deficit":
            score = (
                pre_push_lower_deficit_ratio,
                shadow_residual_cover_ratio,
                events,
            )
        elif objective == "prox-jacobi-cap":
            score = (
                omniscient_over_one_jacobi_ratio,
                pre_push_lower_deficit_ratio,
                events,
            )
        elif objective == "prox-one-step-lead":
            score = (
                relevant_shadow_increment_over_starting_lower_ratio,
                shadow_increment_over_starting_lower_ratio,
                pre_push_lower_deficit_ratio,
            )
        elif objective == "prox-masked-shave":
            score = (
                masked_retraction_shift_ratio,
                post_push_current_over_lower_ratio,
                relevant_shadow_increment_over_starting_lower_ratio,
            )
        elif objective == "prox-masked-input-residual":
            score = (
                masked_input_residual_violation,
                masked_retraction_shift_ratio,
                relevant_shadow_increment_over_starting_lower_ratio,
            )
        elif objective == "prox-masked-input-failure-width":
            score = (
                first_negative_predecessor_width_ratio,
                masked_input_residual_violation,
                masked_retraction_shift_ratio,
            )
        elif objective == "prox-adjacent-shadow":
            score = (
                growing_adjacent_shadow_ratio,
                adjacent_shadow_ratio,
                shadow_residual_cover_ratio,
            )
        elif objective == "prox-state-domination":
            score = (
                growing_relevant_extrapolate_domination_ratio,
                relevant_extrapolate_domination_ratio,
                relevant_primal_domination_ratio,
            )
        elif objective == "prox-auxiliary-domination":
            score = (
                auxiliary_domination_deficit,
                growing_relevant_extrapolate_domination_ratio,
                relevant_extrapolate_domination_ratio,
            )
        elif objective == "prox-momentum-compatibility":
            score = (
                raw_momentum_compatibility_violation,
                growing_relevant_extrapolate_domination_ratio,
                relevant_extrapolate_domination_ratio,
            )
        elif objective == "prox-exterior-state":
            score = (
                exterior_omniscient_extrapolate_ratio,
                exterior_omniscient_primal_ratio,
                exterior_omniscient_auxiliary_ratio,
            )
        elif objective == "prox-exterior-flux":
            score = (
                boundary_flux_gate_ratio,
                boundary_raw_gate_ratio,
                exterior_omniscient_extrapolate_ratio,
            )
        elif objective == "prox-boundary-layer":
            score = (
                boundary_layer_order_ratio,
                boundary_flux_gate_ratio,
                exterior_omniscient_extrapolate_ratio,
            )
        elif objective == "prox-frontier-shield":
            score = (
                masked_frontier_extrapolate_over_lower_ratio,
                boundary_layer_order_ratio,
                boundary_flux_gate_ratio,
            )
        elif objective == "prox-clamp-compatibility":
            score = (
                post_clamp_extrapolate_violation,
                clamp_extrapolate_loss,
                relevant_extrapolate_domination_ratio,
            )
        elif objective == "prox-lag-domination":
            score = (lag_one_deficit, domination_ratio, events)
        elif objective == "prox-lag-state":
            score = (lag_one_primal, lag_one_auxiliary, events)
        elif objective == "prox-lag-lower-state":
            score = (lag_extrapolate_over_lower, lag_primal_over_lower, events)
        else:
            score = (work_ratio, phase_time, events)
        return score, result
    if objective.startswith("ramp-"):
        result = run_source_ramp(
            adjacency,
            alpha,
            rho,
            ramp_root_units,
            maximum_iterations=limit,
            publication_tolerance=1.0e-13,
        )
        event_iterations = list(map(int, result["event_iterations"]))
        inter_event_gaps = [
            later - earlier for earlier, later in zip(event_iterations, event_iterations[1:])
        ]
        result["events"] = len(event_iterations)
        result["last_event_iteration"] = max(event_iterations, default=-1)
        result["scaled_event_horizon"] = (max(event_iterations, default=-1) + 1) * np.sqrt(alpha)
        result["maximum_root_scaled_inter_event_gap"] = max(inter_event_gaps, default=0) * np.sqrt(
            alpha
        )
    else:
        result = run_projected_estimate_nag(
            adjacency,
            alpha,
            rho,
            maximum_iterations=limit,
            publication_tolerance=1.0e-13,
        )
    scaled_total = float(result["scaled_iterations"])
    scaled_gap = float(result["maximum_root_scaled_inter_event_gap"])
    scaled_horizon = float(result["scaled_event_horizon"])
    scaled_work = float(result["volume_work"]) * np.sqrt(alpha) / float(result["scratch_volume"])
    logarithmic_accuracy = max(1.0, float(np.log(100.0 / rho)))
    normalized_work = scaled_work / logarithmic_accuracy
    events = float(result["events"])
    if objective in ("gap", "ramp-gap"):
        score = (scaled_gap, scaled_total, events)
    elif objective in ("horizon", "ramp-horizon"):
        score = (scaled_horizon, scaled_gap, events)
    elif objective in ("work", "ramp-work"):
        score = (scaled_work, scaled_total, events)
    elif objective == "work-ratio":
        score = (normalized_work, scaled_work, events)
    elif objective == "burst-count":
        score = (
            float(result["delayed_bursts"]),
            -float(result["minimum_delayed_burst_release_fraction"]),
            scaled_gap,
        )
    elif objective == "burst-release":
        score = (
            -float(result["minimum_delayed_burst_release_fraction"]),
            float(result["delayed_bursts"]),
            scaled_gap,
        )
    elif objective == "green-dichotomy":
        score = (
            -float(result["minimum_delayed_dichotomy_progress"]),
            float(result["delayed_bursts"]),
            scaled_gap,
        )
    elif objective == "solution-dichotomy":
        score = (
            -float(result["minimum_delayed_solution_dichotomy_progress"]),
            float(result["delayed_bursts"]),
            scaled_gap,
        )
    else:
        score = (scaled_total, scaled_gap, events)
    return score, result


def edge_list(adjacency: np.ndarray) -> list[list[int]]:
    return [
        [left, right]
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left, right]
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=34)
    parser.add_argument(
        "--initial-family", choices=("random", "path", "fixed-stop"), default="random"
    )
    parser.add_argument("--alpha", type=float, default=1.0e-3)
    parser.add_argument("--rho-scale", type=float, default=1.0e-5)
    parser.add_argument("--optimize-rho", action="store_true")
    parser.add_argument(
        "--objective",
        choices=(
            "total",
            "gap",
            "horizon",
            "work",
            "work-ratio",
            "burst-count",
            "burst-release",
            "green-dichotomy",
            "solution-dichotomy",
            "ramp-total",
            "ramp-gap",
            "ramp-horizon",
            "ramp-work",
            "prox-phase",
            "prox-event-phase",
            "prox-domination",
            "prox-progress-domination",
            "prox-residual-cover",
            "prox-pre-push-deficit",
            "prox-jacobi-cap",
            "prox-one-step-lead",
            "prox-masked-shave",
            "prox-masked-input-residual",
            "prox-masked-input-failure-width",
            "prox-adjacent-shadow",
            "prox-state-domination",
            "prox-auxiliary-domination",
            "prox-momentum-compatibility",
            "prox-exterior-state",
            "prox-exterior-flux",
            "prox-boundary-layer",
            "prox-frontier-shield",
            "prox-clamp-compatibility",
            "prox-lag-domination",
            "prox-lag-state",
            "prox-lag-lower-state",
            "prox-work",
        ),
        default="total",
    )
    parser.add_argument("--population", type=int, default=12)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--limit", type=int, default=3000)
    parser.add_argument("--ramp-root-units", type=float, default=1.0)
    parser.add_argument("--positive-append", action="store_true")
    parser.add_argument("--block-append", action="store_true")
    parser.add_argument("--residual-push", action="store_true")
    parser.add_argument("--residual-push-rounds", type=int, default=1)
    parser.add_argument("--input-residual-append", action="store_true")
    parser.add_argument("--seed", type=int, default=20260901)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    population = []
    for _ in range(args.population):
        if args.initial_family == "path":
            adjacency = path_like_graph(rng, args.vertices)
        elif args.initial_family == "fixed-stop":
            adjacency = fixed_face_stop_seed(rng, args.vertices)
        else:
            adjacency = random_graph(rng, args.vertices, float(10 ** rng.uniform(-2.2, -0.6)))
        rho_scale = float(10 ** rng.uniform(-9.0, -0.05)) if args.optimize_rho else args.rho_scale
        population.append((adjacency, rho_scale))
    best_score = (-float("inf"), -float("inf"), -float("inf"))
    best_graph = population[0]
    best_graph = best_graph[0]
    best_rho_scale = args.rho_scale
    best_result: dict[str, object] = {}

    for generation in range(args.generations):
        ranked = []
        for adjacency, rho_scale in population:
            score, result = evaluate(
                adjacency,
                args.alpha,
                rho_scale,
                args.limit,
                args.objective,
                args.ramp_root_units,
                args.positive_append,
                args.block_append,
                args.residual_push,
                args.residual_push_rounds,
                args.input_residual_append,
            )
            ranked.append((score, adjacency, rho_scale, result))
            if score > best_score:
                best_score = score
                best_graph = adjacency.copy()
                best_rho_scale = rho_scale
                best_result = result
        ranked.sort(key=lambda item: item[0], reverse=True)
        elites = ranked[: max(2, args.population // 4)]
        population = [(item[1].copy(), item[2]) for item in elites]
        while len(population) < args.population:
            parent = elites[int(rng.integers(len(elites)))]
            flips = int(rng.integers(1, max(2, args.vertices // 5)))
            rho_scale = parent[2]
            if args.optimize_rho:
                rho_scale = float(np.clip(rho_scale * 10 ** rng.normal(0.0, 0.7), 1e-12, 0.99))
            population.append((mutate(rng, parent[1], flips), rho_scale))

        if generation % 10 == 0 or generation + 1 == args.generations:
            print(
                json.dumps(
                    {
                        "generation": generation,
                        "best_score": best_score,
                        "best_edges": int(best_graph.sum() // 2),
                        "best_rho_scale": best_rho_scale,
                        "best_result": best_result,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    print(
        json.dumps(
            {
                "warning": "empirical adversary search, not a theorem",
                "alpha": args.alpha,
                "rho_scale": best_rho_scale,
                "objective": args.objective,
                "initial_family": args.initial_family,
                "vertices": args.vertices,
                "score": best_score,
                "result": best_result,
                "alpha_crosscheck": {
                    str(alpha): evaluate(
                        best_graph,
                        alpha,
                        best_rho_scale,
                        max(args.limit, int(80 / np.sqrt(alpha))),
                        args.objective,
                        args.ramp_root_units,
                        args.positive_append,
                        args.block_append,
                        args.residual_push,
                        args.residual_push_rounds,
                        args.input_residual_append,
                    )[1]
                    for alpha in (1.0e-2, 3.0e-3, 1.0e-3, 3.0e-4, 1.0e-4)
                },
                "edges": edge_list(best_graph),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
