#!/usr/bin/env python3
"""Experiment with the retained constant bracket and a growing-face prox solve.

This is candidate evidence, not a work theorem.  Each outer phase asks for a
certified lower approximation to the shifted obstacle prox.  Inside a phase,
projected NAG is continued through safe maximal face expansions without a
restart.  The observable shifted residual bracket decides when the phase is
finished.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np

from two_mask_experiments import (
    alternating_layers,
    delayed_publication_graph,
    graph,
    green_band_stress_graph,
    lollipop,
    random_connected_graph,
)


LAG30_EDGES = (
    (0, 1),
    (0, 2),
    (0, 7),
    (0, 22),
    (0, 29),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 14),
    (2, 19),
    (2, 22),
    (3, 9),
    (3, 16),
    (3, 23),
    (3, 28),
    (4, 10),
    (4, 17),
    (5, 6),
    (7, 8),
    (7, 9),
    (7, 10),
    (7, 21),
    (7, 25),
    (7, 29),
    (8, 11),
    (8, 12),
    (8, 15),
    (9, 10),
    (9, 16),
    (10, 18),
    (10, 28),
    (11, 12),
    (11, 13),
    (11, 15),
    (13, 18),
    (13, 20),
    (13, 24),
    (13, 29),
    (14, 22),
    (17, 28),
    (18, 27),
    (19, 26),
    (20, 22),
    (22, 25),
    (22, 26),
    (23, 24),
    (23, 25),
    (24, 25),
    (25, 28),
)


def normalized_operator(adjacency: np.ndarray, alpha: float) -> tuple[np.ndarray, np.ndarray]:
    degrees = adjacency.sum(axis=1)
    sqrt_degrees = np.sqrt(degrees)
    normalized_adjacency = adjacency / np.outer(sqrt_degrees, sqrt_degrees)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    return diagonal * np.eye(len(adjacency)) - coupling * normalized_adjacency, degrees


def exact_obstacle_solution(matrix: np.ndarray, load: np.ndarray) -> np.ndarray:
    face = list(map(int, np.flatnonzero(load > 0.0)))
    solution = np.zeros(len(load))
    while face:
        solution[:] = 0.0
        block = matrix[np.ix_(face, face)]
        solution[face] = np.linalg.solve(block, load[face])
        if np.min(solution[face]) < -1.0e-9:
            raise AssertionError("the monotone active-set solve lost positivity")
        exterior = np.array(sorted(set(range(len(load))) - set(face)), dtype=int)
        if not len(exterior):
            break
        scores = load[exterior] - matrix[np.ix_(exterior, face)] @ solution[face]
        batch = exterior[scores > 1.0e-12]
        if not len(batch):
            break
        face.extend(map(int, batch))
    return solution


def run_retained_prox(
    adjacency: np.ndarray,
    alpha: float,
    rho: float,
    *,
    relative_width: float = 1.0e-6,
    maximum_phase_iterations: int = 100_000,
    publication_floor: float = 2.0e-13,
    positive_append: bool = False,
    block_append: bool = False,
    residual_push: bool = False,
    block_residual_push: bool = False,
    residual_push_rounds: int = 1,
    post_append_residual_push: bool = False,
    input_residual_append: bool = False,
) -> dict[str, object]:
    if residual_push_rounds < 1:
        raise ValueError("residual_push_rounds must be positive")
    q_matrix, degrees = normalized_operator(adjacency, alpha)
    edge_left, edge_right = np.nonzero(np.triu(adjacency, k=1))
    sqrt_degrees = np.sqrt(degrees)
    source = 0
    load = -alpha * rho * sqrt_degrees
    load[source] += alpha / sqrt_degrees[source]
    optimum = exact_obstacle_solution(q_matrix, load)
    final_support = np.flatnonzero(optimum > 1.0e-10)
    final_volume = float(degrees[final_support].sum())

    lower = np.zeros(len(adjacency))
    certified = {source}
    bracket_width = 1.0 / degrees[source] - rho
    initial_width = bracket_width
    target_width = relative_width * initial_width
    sigma = alpha
    shifted_gap = alpha + sigma
    lipschitz = 1.0 + sigma
    normalized_gap = shifted_gap / lipschitz
    root = math.sqrt(normalized_gap)
    momentum = (1.0 - root) / (1.0 + root)
    contraction = sigma / shifted_gap
    requested_fraction = (1.0 - contraction) / 2.0

    phase_records: list[dict[str, object]] = []
    total_volume_work = 0.0
    total_residual_push_work = 0.0
    total_positive_append_work = 0.0
    total_post_append_push_work = 0.0
    total_iterations = 0
    total_events = 0
    maximum_omniscient_domination_deficit = 0.0
    maximum_signed_omniscient_domination_deficit = -math.inf
    maximum_progress_omniscient_domination_deficit = -math.inf
    maximum_progress_omniscient_domination_ratio = -math.inf
    maximum_growing_progress_domination_ratio = -math.inf
    maximum_omniscient_domination_ratio = 0.0
    maximum_lag_one_domination_deficit = 0.0
    maximum_signed_lag_one_domination_deficit = -math.inf
    maximum_lag_one_primal_deficit = 0.0
    maximum_lag_one_auxiliary_deficit = 0.0
    maximum_lag_one_extrapolate_deficit = 0.0
    maximum_lag_primal_over_lower_deficit = 0.0
    maximum_lag_extrapolate_over_lower_deficit = 0.0
    maximum_missing_omniscient_after_closure = 0
    maximum_same_time_primal_deficit = -math.inf
    maximum_same_time_auxiliary_deficit = -math.inf
    maximum_same_time_extrapolate_deficit = -math.inf
    maximum_relevant_primal_domination_ratio = -math.inf
    maximum_relevant_extrapolate_domination_ratio = -math.inf
    maximum_growing_relevant_extrapolate_domination_ratio = -math.inf
    maximum_exterior_omniscient_primal_ratio = -math.inf
    maximum_exterior_omniscient_auxiliary_ratio = -math.inf
    maximum_exterior_omniscient_extrapolate_ratio = -math.inf
    maximum_boundary_flux_gate_ratio = -math.inf
    maximum_boundary_raw_gate_ratio = -math.inf
    maximum_boundary_layer_order_ratio = -math.inf
    maximum_masked_frontier_extrapolate_over_lower_ratio = -math.inf
    minimum_clamp_extrapolate_change_ratio = math.inf
    minimum_post_clamp_extrapolate_margin_ratio = math.inf
    minimum_active_raw_momentum_compatibility_ratio = math.inf
    maximum_shadow_residual_cover_deficit = -math.inf
    maximum_shadow_residual_cover_ratio = -math.inf
    maximum_pre_push_lower_deficit_ratio = -math.inf
    maximum_shadow_increment_over_starting_lower_ratio = -math.inf
    maximum_relevant_shadow_increment_over_starting_lower_ratio = -math.inf
    minimum_one_step_current_lead_ratio = math.inf
    minimum_one_step_auxiliary_lead_ratio = math.inf
    minimum_one_step_extrapolate_lead_ratio = math.inf
    maximum_post_push_current_over_lower_ratio = -math.inf
    maximum_post_push_auxiliary_over_lower_ratio = -math.inf
    maximum_masked_retraction_shift_ratio = -math.inf
    minimum_residual_velocity_credit_ratio = math.inf
    minimum_masked_input_residual_ratio = math.inf
    maximum_omniscient_over_one_jacobi_ratio = -math.inf
    maximum_omniscient_over_two_jacobi_ratio = -math.inf
    maximum_adjacent_shadow_deficit = -math.inf
    maximum_adjacent_shadow_ratio = -math.inf
    maximum_growing_adjacent_shadow_ratio = -math.inf
    omniscient_domination_witness: dict[str, object] = {}
    lag_one_domination_witness: dict[str, object] = {}
    progress_domination_witness: dict[str, object] = {}
    growing_progress_domination_witness: dict[str, object] = {}
    exterior_omniscient_state_witness: dict[str, object] = {}
    boundary_flux_gate_witness: dict[str, object] = {}
    boundary_layer_order_witness: dict[str, object] = {}
    masked_frontier_witness: dict[str, object] = {}
    clamp_extrapolate_witness: dict[str, object] = {}
    pre_push_lower_witness: dict[str, object] = {}
    shadow_increment_witness: dict[str, object] = {}
    omniscient_jacobi_cap_witness: dict[str, object] = {}
    maximum_estimate_potential_contraction_ratio = -math.inf
    estimate_potential_witness: dict[str, object] = {}

    while bracket_width > target_width:
        old_lower = lower.copy()
        old_width = bracket_width
        old_original_residual = load - q_matrix @ old_lower
        old_residual_width = float(
            np.max(np.maximum(old_original_residual, 0.0) / (alpha * sqrt_degrees))
        )
        assert old_residual_width <= 2.0 * old_width + 5.0e-7
        shifted_load = load + sigma * old_lower
        shifted_matrix = q_matrix + sigma * np.eye(len(adjacency))
        shifted_diagonal = np.diag(shifted_matrix)
        shifted_coupling = np.diag(shifted_diagonal) - shifted_matrix
        exact_prox = exact_obstacle_solution(shifted_matrix, shifted_load)
        omniscient_face = np.flatnonzero(exact_prox > 1.0e-12)
        requested_inner_width = requested_fraction * old_width

        scratch = np.array(sorted(certified), dtype=int)
        current = old_lower.copy()
        previous = old_lower.copy()
        omniscient_current = old_lower.copy()
        omniscient_previous = old_lower.copy()
        omniscient_lower = old_lower.copy()
        lagged_omniscient_lower = old_lower.copy()
        lagged_omniscient_current = old_lower.copy()
        lagged_omniscient_auxiliary = old_lower.copy()
        phase_events: list[dict[str, object]] = []
        inner_width = math.inf
        auxiliary_scale = (1.0 - root) / root

        for iteration in range(maximum_phase_iterations):
            product_scratch = scratch.copy()
            starting_masked_lower = lower.copy()
            starting_masked_current = current.copy()
            starting_masked_previous = previous.copy()
            starting_masked_auxiliary = starting_masked_current + auxiliary_scale * (
                starting_masked_current - starting_masked_previous
            )
            starting_masked_extrapolate = (
                starting_masked_current + root * starting_masked_auxiliary
            ) / (1.0 + root)
            exact_objective = (
                0.5 * exact_prox @ shifted_matrix @ exact_prox - shifted_load @ exact_prox
            )

            def estimate_potential(primal: np.ndarray, estimate: np.ndarray) -> float:
                objective_gap = (
                    0.5 * primal @ shifted_matrix @ primal - shifted_load @ primal - exact_objective
                )
                estimate_error = estimate - exact_prox
                return float(objective_gap + 0.5 * shifted_gap * (estimate_error @ estimate_error))

            starting_estimate_potential = estimate_potential(
                starting_masked_current, starting_masked_auxiliary
            )
            starting_omniscient_lower = omniscient_lower.copy()
            starting_omniscient_lower_residual = (
                shifted_load - shifted_matrix @ starting_omniscient_lower
            )
            omniscient_one_jacobi_cap = (
                starting_omniscient_lower
                + np.maximum(starting_omniscient_lower_residual, 0.0) / shifted_diagonal
            )
            one_jacobi_residual = shifted_load - shifted_matrix @ omniscient_one_jacobi_cap
            omniscient_two_jacobi_cap = (
                omniscient_one_jacobi_cap + np.maximum(one_jacobi_residual, 0.0) / shifted_diagonal
            )
            starting_current = current.copy()
            starting_omniscient_current = omniscient_current.copy()
            starting_omniscient_previous = omniscient_previous.copy()
            if input_residual_append:
                full_input_extrapolate = np.zeros(len(adjacency))
                full_input_extrapolate[scratch] = current[scratch] + momentum * (
                    current[scratch] - previous[scratch]
                )
                full_input_residual = shifted_load - shifted_matrix @ full_input_extrapolate
                outside = np.array(sorted(set(range(len(adjacency))) - certified), dtype=int)
                input_batch = np.array([], dtype=int)
                if len(outside):
                    scale = shifted_gap * sqrt_degrees[outside] * old_width
                    numerical_floor = publication_floor * np.maximum(1.0, scale)
                    input_batch = outside[full_input_residual[outside] > numerical_floor]
                if len(input_batch):
                    # Under MaskedInputResidual, comparison with the exact
                    # obstacle solution proves that this tentative zero-state
                    # admission is support-safe.  Keep the assertion explicit
                    # in the dense audit.
                    if not set(map(int, input_batch)).issubset(set(map(int, omniscient_face))):
                        raise AssertionError(
                            "positive input-residual admission left the exact prox face"
                        )
                    phase_events.append(
                        {
                            "iteration": iteration + 1,
                            "batch": list(map(int, input_batch)),
                            "face_size": len(certified) + len(input_batch),
                            "input_residual": True,
                        }
                    )
                    certified.update(map(int, input_batch))
                    scratch = np.array(sorted(certified), dtype=int)
                    product_scratch = scratch.copy()
            extrapolated = current[scratch] + momentum * (current[scratch] - previous[scratch])
            next_iterate = np.zeros(len(adjacency))
            block = shifted_matrix[np.ix_(scratch, scratch)]
            masked_input_residual = shifted_load[scratch] - block @ extrapolated
            if len(scratch):
                minimum_masked_input_residual_ratio = min(
                    minimum_masked_input_residual_ratio,
                    float(np.min(masked_input_residual) / old_width),
                )
            next_iterate[scratch] = extrapolated + masked_input_residual / lipschitz
            previous, current = current, next_iterate
            masked_raw_next = current.copy()
            masked_raw_auxiliary = masked_raw_next + auxiliary_scale * (
                masked_raw_next - starting_current
            )
            total_volume_work += float(degrees[scratch].sum())

            omniscient_block = shifted_matrix[np.ix_(omniscient_face, omniscient_face)]
            omniscient_extrapolated = omniscient_current[omniscient_face] + momentum * (
                omniscient_current[omniscient_face] - omniscient_previous[omniscient_face]
            )
            omniscient_input_extrapolate = np.zeros(len(adjacency))
            omniscient_input_extrapolate[omniscient_face] = omniscient_extrapolated
            omniscient_next = np.zeros(len(adjacency))
            omniscient_next[omniscient_face] = (
                omniscient_extrapolated
                + (shifted_load[omniscient_face] - omniscient_block @ omniscient_extrapolated)
                / lipschitz
            )
            omniscient_previous, omniscient_current = (
                omniscient_current,
                omniscient_next,
            )
            omniscient_raw_next = omniscient_current.copy()
            omniscient_raw_auxiliary = omniscient_raw_next + auxiliary_scale * (
                omniscient_raw_next - starting_omniscient_current
            )
            raw_momentum_compatibility = 2.0 * (
                masked_raw_next[scratch] - omniscient_current[scratch]
            ) - (1.0 - root) * (starting_current[scratch] - starting_omniscient_current[scratch])
            if len(scratch):
                minimum_active_raw_momentum_compatibility_ratio = min(
                    minimum_active_raw_momentum_compatibility_ratio,
                    float(np.min(raw_momentum_compatibility) / old_width),
                )

            omniscient_residual = (
                shifted_load[omniscient_face]
                - omniscient_block @ omniscient_current[omniscient_face]
            )
            omniscient_direction = omniscient_block @ sqrt_degrees[omniscient_face]
            omniscient_ratios = np.divide(
                -omniscient_residual,
                omniscient_direction,
                out=np.full_like(omniscient_residual, -np.inf),
                where=omniscient_direction > 0.0,
            )
            omniscient_shift = max(0.0, float(np.max(omniscient_ratios)))
            omniscient_candidate = (
                omniscient_current[omniscient_face]
                - omniscient_shift * sqrt_degrees[omniscient_face]
            )
            omniscient_lower[omniscient_face] = np.maximum(
                omniscient_lower[omniscient_face],
                np.maximum(omniscient_candidate, 0.0),
            )
            omniscient_auxiliary = omniscient_current + auxiliary_scale * (
                omniscient_current - omniscient_previous
            )
            omniscient_current[omniscient_face] = np.maximum(
                omniscient_current[omniscient_face],
                omniscient_lower[omniscient_face],
            )
            omniscient_auxiliary[omniscient_face] = np.maximum(
                omniscient_auxiliary[omniscient_face],
                omniscient_lower[omniscient_face],
            )
            omniscient_velocity = (
                omniscient_auxiliary[omniscient_face] - omniscient_current[omniscient_face]
            ) / auxiliary_scale
            omniscient_previous[omniscient_face] = (
                omniscient_current[omniscient_face] - omniscient_velocity
            )
            if iteration > 0:
                new_omniscient_extrapolate = (omniscient_current + root * omniscient_auxiliary) / (
                    1.0 + root
                )
                one_step_rows = np.array(sorted(map(int, omniscient_face)), dtype=int)
                minimum_one_step_current_lead_ratio = min(
                    minimum_one_step_current_lead_ratio,
                    float(
                        np.min(
                            starting_masked_current[one_step_rows]
                            - omniscient_current[one_step_rows]
                        )
                        / old_width
                    ),
                )
                minimum_one_step_auxiliary_lead_ratio = min(
                    minimum_one_step_auxiliary_lead_ratio,
                    float(
                        np.min(
                            starting_masked_auxiliary[one_step_rows]
                            - omniscient_auxiliary[one_step_rows]
                        )
                        / old_width
                    ),
                )
                minimum_one_step_extrapolate_lead_ratio = min(
                    minimum_one_step_extrapolate_lead_ratio,
                    float(
                        np.min(
                            starting_masked_extrapolate[one_step_rows]
                            - new_omniscient_extrapolate[one_step_rows]
                        )
                        / old_width
                    ),
                )
            omniscient_jacobi_cap_gap = omniscient_lower - omniscient_one_jacobi_cap
            omniscient_jacobi_cap_ratio = float(np.max(omniscient_jacobi_cap_gap) / old_width)
            if omniscient_jacobi_cap_ratio > maximum_omniscient_over_one_jacobi_ratio:
                cap_vertex = int(np.argmax(omniscient_jacobi_cap_gap))
                omniscient_jacobi_cap_witness = {
                    "phase": len(phase_records),
                    "iteration": iteration + 1,
                    "vertex": cap_vertex,
                    "ratio": omniscient_jacobi_cap_ratio,
                    "old_width": old_width,
                    "starting_lower": float(starting_omniscient_lower[cap_vertex]),
                    "starting_positive_residual": float(
                        max(starting_omniscient_lower_residual[cap_vertex], 0.0)
                    ),
                    "one_jacobi_cap": float(omniscient_one_jacobi_cap[cap_vertex]),
                    "new_omniscient_lower": float(omniscient_lower[cap_vertex]),
                    "raw_current": float(omniscient_raw_next[cap_vertex]),
                }
            maximum_omniscient_over_one_jacobi_ratio = max(
                maximum_omniscient_over_one_jacobi_ratio,
                omniscient_jacobi_cap_ratio,
            )
            maximum_omniscient_over_two_jacobi_ratio = max(
                maximum_omniscient_over_two_jacobi_ratio,
                float(np.max(omniscient_lower - omniscient_two_jacobi_cap) / old_width),
            )

            active_residual = shifted_load[scratch] - block @ current[scratch]
            constant_direction = block @ sqrt_degrees[scratch]
            ratios = np.divide(
                -active_residual,
                constant_direction,
                out=np.full_like(active_residual, -np.inf),
                where=constant_direction > 0.0,
            )
            shift = max(0.0, float(np.max(ratios)))
            maximum_masked_retraction_shift_ratio = max(
                maximum_masked_retraction_shift_ratio,
                shift / old_width,
            )
            candidate = current[scratch] - shift * sqrt_degrees[scratch]
            lower[scratch] = np.maximum(lower[scratch], np.maximum(candidate, 0.0))

            if auxiliary_scale > 0.0:
                auxiliary = current + auxiliary_scale * (current - previous)
                current[scratch] = np.maximum(current[scratch], lower[scratch])
                auxiliary[scratch] = np.maximum(auxiliary[scratch], lower[scratch])
                velocity = (auxiliary[scratch] - current[scratch]) / auxiliary_scale
                previous[scratch] = current[scratch] - velocity
            else:
                current[scratch] = np.maximum(current[scratch], lower[scratch])
                previous[scratch] = current[scratch]

            lower_before_push = lower.copy()
            full_residual = shifted_load - shifted_matrix @ lower
            residual_before_push = full_residual.copy()
            old_exterior = np.array(
                sorted(set(map(int, omniscient_face)) - set(map(int, scratch))),
                dtype=int,
            )
            if len(old_exterior) and len(scratch):
                old_exterior = old_exterior[
                    np.any(adjacency[np.ix_(old_exterior, scratch)] > 0.0, axis=1)
                ]
            if len(old_exterior):
                boundary_layer = np.array(
                    sorted(
                        {
                            int(neighbor)
                            for vertex in old_exterior
                            for neighbor in np.flatnonzero(adjacency[vertex] > 0.0)
                            if int(neighbor) in set(map(int, scratch))
                        }
                    ),
                    dtype=int,
                )
                if len(boundary_layer):
                    boundary_layer_gap = (
                        omniscient_input_extrapolate[boundary_layer]
                        - lower_before_push[boundary_layer]
                    )
                    boundary_layer_ratio = float(np.max(boundary_layer_gap) / old_width)
                    if boundary_layer_ratio > maximum_boundary_layer_order_ratio:
                        boundary_layer_vertex = int(
                            boundary_layer[int(np.argmax(boundary_layer_gap))]
                        )
                        boundary_layer_order_witness = {
                            "phase": len(phase_records),
                            "iteration": iteration + 1,
                            "vertex": boundary_layer_vertex,
                            "ratio": boundary_layer_ratio,
                            "old_width": old_width,
                            "masked_lower": float(lower_before_push[boundary_layer_vertex]),
                            "omniscient_input_extrapolate": float(
                                omniscient_input_extrapolate[boundary_layer_vertex]
                            ),
                            "mask_size": len(scratch),
                        }
                    maximum_boundary_layer_order_ratio = max(
                        maximum_boundary_layer_order_ratio,
                        boundary_layer_ratio,
                    )
            zero_history_exterior = old_exterior[
                (np.abs(starting_omniscient_current[old_exterior]) <= 1.0e-12 * old_width)
                & (np.abs(starting_omniscient_previous[old_exterior]) <= 1.0e-12 * old_width)
            ]
            if len(zero_history_exterior):
                boundary_flux = shifted_coupling[
                    np.ix_(zero_history_exterior, range(len(adjacency)))
                ] @ (omniscient_input_extrapolate - lower_before_push)
                boundary_raw_gate = (
                    lipschitz * omniscient_raw_next[zero_history_exterior]
                    - residual_before_push[zero_history_exterior]
                )
                assert np.max(np.abs(boundary_flux - boundary_raw_gate)) <= (
                    2.0e-10 * max(1.0, old_width)
                )
                flux_ratio = float(np.max(boundary_flux) / old_width)
                raw_ratio = float(np.max(boundary_raw_gate) / old_width)
                if flux_ratio > maximum_boundary_flux_gate_ratio:
                    flux_vertex = int(zero_history_exterior[int(np.argmax(boundary_flux))])
                    flux_neighbors = list(map(int, np.flatnonzero(adjacency[flux_vertex] > 0.0)))
                    boundary_flux_gate_witness = {
                        "phase": len(phase_records),
                        "iteration": iteration + 1,
                        "vertex": flux_vertex,
                        "ratio": flux_ratio,
                        "raw_gate_ratio": float(
                            boundary_raw_gate[int(np.argmax(boundary_flux))] / old_width
                        ),
                        "old_width": old_width,
                        "masked_lower": float(lower_before_push[flux_vertex]),
                        "omniscient_input_extrapolate": float(
                            omniscient_input_extrapolate[flux_vertex]
                        ),
                        "masked_residual": float(residual_before_push[flux_vertex]),
                        "omniscient_raw_current": float(omniscient_raw_next[flux_vertex]),
                        "mask_size": len(scratch),
                        "neighbor_rows": [
                            {
                                "vertex": neighbor,
                                "in_mask": neighbor in set(map(int, scratch)),
                                "masked_lower": float(lower_before_push[neighbor]),
                                "omniscient_input_extrapolate": float(
                                    omniscient_input_extrapolate[neighbor]
                                ),
                            }
                            for neighbor in flux_neighbors
                        ],
                    }
                maximum_boundary_flux_gate_ratio = max(maximum_boundary_flux_gate_ratio, flux_ratio)
                maximum_boundary_raw_gate_ratio = max(maximum_boundary_raw_gate_ratio, raw_ratio)
            shadow_residual_cover_deficits = shifted_diagonal * (
                omniscient_lower - lower_before_push
            ) - np.maximum(residual_before_push, 0.0)
            maximum_shadow_residual_cover_deficit = max(
                maximum_shadow_residual_cover_deficit,
                float(np.max(shadow_residual_cover_deficits)),
            )
            shadow_deficits_before_push = omniscient_lower - lower_before_push
            if iteration > 0:
                shadow_increment_ratio = float(
                    np.max(omniscient_lower - starting_masked_lower) / old_width
                )
                if shadow_increment_ratio > maximum_shadow_increment_over_starting_lower_ratio:
                    shadow_increment_vertex = int(
                        np.argmax(omniscient_lower - starting_masked_lower)
                    )
                    shadow_increment_witness = {
                        "phase": len(phase_records),
                        "iteration": iteration + 1,
                        "vertex": shadow_increment_vertex,
                        "ratio": shadow_increment_ratio,
                        "old_width": old_width,
                        "starting_masked_lower": float(
                            starting_masked_lower[shadow_increment_vertex]
                        ),
                        "omniscient_lower": float(omniscient_lower[shadow_increment_vertex]),
                        "pre_push_masked_lower": float(lower_before_push[shadow_increment_vertex]),
                    }
                maximum_shadow_increment_over_starting_lower_ratio = max(
                    maximum_shadow_increment_over_starting_lower_ratio,
                    shadow_increment_ratio,
                )
                relevant_shadow = omniscient_lower > old_lower + 1.0e-12 * old_width
                if np.any(relevant_shadow):
                    maximum_relevant_shadow_increment_over_starting_lower_ratio = max(
                        maximum_relevant_shadow_increment_over_starting_lower_ratio,
                        float(
                            np.max((omniscient_lower - starting_masked_lower)[relevant_shadow])
                            / old_width
                        ),
                    )
            pre_push_lower_ratio = float(np.max(shadow_deficits_before_push) / old_width)
            if pre_push_lower_ratio > maximum_pre_push_lower_deficit_ratio:
                pre_push_vertex = int(np.argmax(shadow_deficits_before_push))
                pre_push_lower_witness = {
                    "phase": len(phase_records),
                    "iteration": iteration + 1,
                    "vertex": pre_push_vertex,
                    "ratio": pre_push_lower_ratio,
                    "old_width": old_width,
                    "masked_lower": float(lower_before_push[pre_push_vertex]),
                    "omniscient_lower": float(omniscient_lower[pre_push_vertex]),
                    "positive_residual": float(max(residual_before_push[pre_push_vertex], 0.0)),
                    "diagonal_cover": float(
                        shifted_diagonal[pre_push_vertex]
                        * shadow_deficits_before_push[pre_push_vertex]
                    ),
                }
            maximum_pre_push_lower_deficit_ratio = max(
                maximum_pre_push_lower_deficit_ratio,
                pre_push_lower_ratio,
            )
            if len(edge_left):
                maximum_adjacent_shadow_deficit = max(
                    maximum_adjacent_shadow_deficit,
                    float(
                        np.max(
                            np.minimum(
                                shadow_deficits_before_push[edge_left],
                                shadow_deficits_before_push[edge_right],
                            )
                        )
                    ),
                )
                shadow_progress = omniscient_lower - old_lower
                progressed_edges = (shadow_progress[edge_left] > 1.0e-12 * old_width) & (
                    shadow_progress[edge_right] > 1.0e-12 * old_width
                )
                if np.any(progressed_edges):
                    left = edge_left[progressed_edges]
                    right = edge_right[progressed_edges]
                    adjacent_ratios = np.minimum(
                        shadow_deficits_before_push[left] / shadow_progress[left],
                        shadow_deficits_before_push[right] / shadow_progress[right],
                    )
                    adjacent_ratio = float(np.max(adjacent_ratios))
                    maximum_adjacent_shadow_ratio = max(
                        maximum_adjacent_shadow_ratio, adjacent_ratio
                    )
                    if len(certified) < len(omniscient_face):
                        maximum_growing_adjacent_shadow_ratio = max(
                            maximum_growing_adjacent_shadow_ratio, adjacent_ratio
                        )
            cover_progress = omniscient_lower > old_lower + 1.0e-12 * old_width
            if np.any(cover_progress):
                cover_denominator = (
                    shifted_diagonal[cover_progress]
                    * (omniscient_lower - old_lower)[cover_progress]
                )
                cover_ratios = shadow_residual_cover_deficits[cover_progress] / cover_denominator
                maximum_shadow_residual_cover_ratio = max(
                    maximum_shadow_residual_cover_ratio,
                    float(np.max(cover_ratios)),
                )
            if residual_push or block_residual_push:
                rounds = 1 if block_residual_push else residual_push_rounds
                for _ in range(rounds):
                    increment = np.zeros(len(adjacency))
                    positive = scratch[full_residual[scratch] > 0.0]
                    if not len(positive):
                        break
                    if block_residual_push:
                        increment[positive] = np.linalg.solve(
                            shifted_matrix[np.ix_(positive, positive)],
                            full_residual[positive],
                        )
                    else:
                        increment[positive] = full_residual[positive] / shifted_diagonal[positive]
                        total_residual_push_work += float(degrees[positive].sum())
                    lower += increment
                    full_residual -= shifted_matrix @ increment
                    current[scratch] = np.maximum(current[scratch], lower[scratch])
                    auxiliary[scratch] = np.maximum(auxiliary[scratch], lower[scratch])
                    velocity = (auxiliary[scratch] - current[scratch]) / auxiliary_scale
                    previous[scratch] = current[scratch] - velocity
            while True:
                outside = np.array(sorted(set(range(len(adjacency))) - certified), dtype=int)
                batch = np.array([], dtype=int)
                if len(outside):
                    scale = shifted_gap * sqrt_degrees[outside] * old_width
                    numerical_floor = publication_floor * np.maximum(1.0, scale)
                    batch = outside[full_residual[outside] > numerical_floor]
                if not len(batch):
                    break
                phase_events.append(
                    {
                        "iteration": iteration + 1,
                        "batch": list(map(int, batch)),
                        "face_size": len(certified) + len(batch),
                    }
                )
                certified.update(map(int, batch))
                if not (positive_append or block_append):
                    break
                increment = np.zeros(len(adjacency))
                if block_append:
                    increment[batch] = np.linalg.solve(
                        shifted_matrix[np.ix_(batch, batch)], full_residual[batch]
                    )
                else:
                    increment[batch] = full_residual[batch] / shifted_diagonal[batch]
                    total_positive_append_work += float(degrees[batch].sum())
                lower += increment
                full_residual -= shifted_matrix @ increment
                current[batch] = lower[batch]
                auxiliary[batch] = lower[batch]
                previous[batch] = lower[batch]
            scratch = np.array(sorted(certified), dtype=int)
            if post_append_residual_push and len(scratch):
                cleanup_positive = scratch[full_residual[scratch] > 0.0]
                if len(cleanup_positive):
                    cleanup_increment = np.zeros(len(adjacency))
                    cleanup_increment[cleanup_positive] = (
                        full_residual[cleanup_positive] / shifted_diagonal[cleanup_positive]
                    )
                    lower += cleanup_increment
                    full_residual -= shifted_matrix @ cleanup_increment
                    total_post_append_push_work += float(degrees[cleanup_positive].sum())
                    current[scratch] = np.maximum(current[scratch], lower[scratch])
                    auxiliary[scratch] = np.maximum(auxiliary[scratch], lower[scratch])
                    velocity = (auxiliary[scratch] - current[scratch]) / auxiliary_scale
                    previous[scratch] = current[scratch] - velocity

                # Cleanup may make another exterior layer positive.  Preserve
                # the exact-positive no-miss invariant with one more cascade.
                while True:
                    outside = np.array(sorted(set(range(len(adjacency))) - certified), dtype=int)
                    batch = np.array([], dtype=int)
                    if len(outside):
                        scale = shifted_gap * sqrt_degrees[outside] * old_width
                        numerical_floor = publication_floor * np.maximum(1.0, scale)
                        batch = outside[full_residual[outside] > numerical_floor]
                    if not len(batch):
                        break
                    phase_events.append(
                        {
                            "iteration": iteration + 1,
                            "batch": list(map(int, batch)),
                            "face_size": len(certified) + len(batch),
                            "post_cleanup": True,
                        }
                    )
                    certified.update(map(int, batch))
                    if not (positive_append or block_append):
                        break
                    increment = np.zeros(len(adjacency))
                    if block_append:
                        increment[batch] = np.linalg.solve(
                            shifted_matrix[np.ix_(batch, batch)],
                            full_residual[batch],
                        )
                    else:
                        increment[batch] = full_residual[batch] / shifted_diagonal[batch]
                        total_positive_append_work += float(degrees[batch].sum())
                    lower += increment
                    full_residual -= shifted_matrix @ increment
                    current[batch] = lower[batch]
                    auxiliary[batch] = lower[batch]
                    previous[batch] = lower[batch]
                scratch = np.array(sorted(certified), dtype=int)
            if len(scratch):
                maximum_post_push_current_over_lower_ratio = max(
                    maximum_post_push_current_over_lower_ratio,
                    float(np.max(current[scratch] - lower[scratch]) / old_width),
                )
                maximum_post_push_auxiliary_over_lower_ratio = max(
                    maximum_post_push_auxiliary_over_lower_ratio,
                    float(np.max(auxiliary[scratch] - lower[scratch]) / old_width),
                )
                residual_velocity_credit = full_residual[scratch] - root / (
                    1.0 + root
                ) * shifted_diagonal[scratch] * (auxiliary[scratch] - lower[scratch])
                minimum_residual_velocity_credit_ratio = min(
                    minimum_residual_velocity_credit_ratio,
                    float(np.min(residual_velocity_credit) / old_width),
                )
            ending_estimate_potential = estimate_potential(current, auxiliary)
            potential_scale = shifted_gap * old_width * old_width * max(1.0, final_volume)
            if starting_estimate_potential > 1.0e-10 * potential_scale:
                contraction_ratio = ending_estimate_potential / (
                    (1.0 - root) * starting_estimate_potential
                )
                if contraction_ratio > maximum_estimate_potential_contraction_ratio:
                    maximum_estimate_potential_contraction_ratio = contraction_ratio
                    estimate_potential_witness = {
                        "phase": len(phase_records),
                        "iteration": iteration + 1,
                        "ratio": contraction_ratio,
                        "starting_potential": starting_estimate_potential,
                        "ending_potential": ending_estimate_potential,
                    }
            maximum_missing_omniscient_after_closure = max(
                maximum_missing_omniscient_after_closure,
                len(set(map(int, omniscient_face)) - certified),
            )

            domination_deficit = float(np.max(omniscient_lower - lower))
            same_time_primal_deficit = float(np.max(omniscient_current - current))
            same_time_auxiliary_deficit = float(np.max(omniscient_auxiliary - auxiliary))
            masked_same_time_extrapolate = (current + root * auxiliary) / (1.0 + root)
            omniscient_same_time_extrapolate = (
                omniscient_current + root * omniscient_auxiliary
            ) / (1.0 + root)
            same_time_extrapolate_deficit = float(
                np.max(omniscient_same_time_extrapolate - masked_same_time_extrapolate)
            )
            maximum_same_time_primal_deficit = max(
                maximum_same_time_primal_deficit, same_time_primal_deficit
            )
            maximum_same_time_auxiliary_deficit = max(
                maximum_same_time_auxiliary_deficit,
                same_time_auxiliary_deficit,
            )
            maximum_same_time_extrapolate_deficit = max(
                maximum_same_time_extrapolate_deficit,
                same_time_extrapolate_deficit,
            )
            raw_output_extrapolate_gap = (
                (masked_raw_next + root * masked_raw_auxiliary)
                - (omniscient_raw_next + root * omniscient_raw_auxiliary)
            ) / (1.0 + root)
            post_clamp_extrapolate_gap = (
                masked_same_time_extrapolate - omniscient_same_time_extrapolate
            )
            common_active = np.array(
                sorted(set(map(int, product_scratch)) & set(map(int, omniscient_face))),
                dtype=int,
            )
            if len(common_active):
                clamp_changes = (
                    post_clamp_extrapolate_gap[common_active]
                    - raw_output_extrapolate_gap[common_active]
                ) / old_width
                post_clamp_margins = post_clamp_extrapolate_gap[common_active] / old_width
                clamp_change = float(np.min(clamp_changes))
                post_clamp_margin = float(np.min(post_clamp_margins))
                if clamp_change < minimum_clamp_extrapolate_change_ratio:
                    clamp_vertex = int(common_active[int(np.argmin(clamp_changes))])
                    clamp_extrapolate_witness = {
                        "phase": len(phase_records),
                        "iteration": iteration + 1,
                        "vertex": clamp_vertex,
                        "change_ratio": clamp_change,
                        "post_margin_ratio": float(
                            post_clamp_extrapolate_gap[clamp_vertex] / old_width
                        ),
                        "raw_margin_ratio": float(
                            raw_output_extrapolate_gap[clamp_vertex] / old_width
                        ),
                        "masked_raw_current": float(masked_raw_next[clamp_vertex]),
                        "omniscient_raw_current": float(omniscient_raw_next[clamp_vertex]),
                        "masked_raw_auxiliary": float(masked_raw_auxiliary[clamp_vertex]),
                        "omniscient_raw_auxiliary": float(omniscient_raw_auxiliary[clamp_vertex]),
                        "masked_lower_after_push": float(lower[clamp_vertex]),
                        "omniscient_lower": float(omniscient_lower[clamp_vertex]),
                    }
                minimum_clamp_extrapolate_change_ratio = min(
                    minimum_clamp_extrapolate_change_ratio, clamp_change
                )
                minimum_post_clamp_extrapolate_margin_ratio = min(
                    minimum_post_clamp_extrapolate_margin_ratio,
                    post_clamp_margin,
                )
            exterior = np.array(sorted(set(map(int, omniscient_face)) - certified), dtype=int)
            if len(exterior):
                exterior_primal = omniscient_current[exterior] / old_width
                exterior_auxiliary = omniscient_auxiliary[exterior] / old_width
                exterior_extrapolate = omniscient_same_time_extrapolate[exterior] / old_width
                maximum_exterior_omniscient_primal_ratio = max(
                    maximum_exterior_omniscient_primal_ratio,
                    float(np.max(exterior_primal)),
                )
                maximum_exterior_omniscient_auxiliary_ratio = max(
                    maximum_exterior_omniscient_auxiliary_ratio,
                    float(np.max(exterior_auxiliary)),
                )
                exterior_extrapolate_ratio = float(np.max(exterior_extrapolate))
                if exterior_extrapolate_ratio > maximum_exterior_omniscient_extrapolate_ratio:
                    exterior_vertex = int(exterior[int(np.argmax(exterior_extrapolate))])
                    exterior_omniscient_state_witness = {
                        "phase": len(phase_records),
                        "iteration": iteration + 1,
                        "vertex": exterior_vertex,
                        "ratio": exterior_extrapolate_ratio,
                        "old_width": old_width,
                        "omniscient_lower": float(omniscient_lower[exterior_vertex]),
                        "omniscient_current": float(omniscient_current[exterior_vertex]),
                        "omniscient_auxiliary": float(omniscient_auxiliary[exterior_vertex]),
                        "omniscient_extrapolate": float(
                            omniscient_same_time_extrapolate[exterior_vertex]
                        ),
                        "exterior_shifted_residual": float(full_residual[exterior_vertex]),
                        "mask_size": len(certified),
                        "omniscient_face_size": len(omniscient_face),
                    }
                maximum_exterior_omniscient_extrapolate_ratio = max(
                    maximum_exterior_omniscient_extrapolate_ratio,
                    exterior_extrapolate_ratio,
                )
                active_frontier = np.array(
                    sorted(
                        {
                            int(neighbor)
                            for vertex in exterior
                            for neighbor in np.flatnonzero(adjacency[vertex] > 0.0)
                            if int(neighbor) in certified
                        }
                    ),
                    dtype=int,
                )
                if len(active_frontier):
                    frontier_gaps = (
                        masked_same_time_extrapolate[active_frontier] - lower[active_frontier]
                    ) / old_width
                    frontier_ratio = float(np.max(frontier_gaps))
                    if frontier_ratio > maximum_masked_frontier_extrapolate_over_lower_ratio:
                        frontier_vertex = int(active_frontier[int(np.argmax(frontier_gaps))])
                        masked_frontier_witness = {
                            "phase": len(phase_records),
                            "iteration": iteration + 1,
                            "vertex": frontier_vertex,
                            "ratio": frontier_ratio,
                            "old_width": old_width,
                            "masked_lower": float(lower[frontier_vertex]),
                            "masked_extrapolate": float(
                                masked_same_time_extrapolate[frontier_vertex]
                            ),
                            "remaining_exterior_size": len(exterior),
                        }
                    maximum_masked_frontier_extrapolate_over_lower_ratio = max(
                        maximum_masked_frontier_extrapolate_over_lower_ratio,
                        frontier_ratio,
                    )
            state_relevant = (omniscient_lower > old_lower + 1.0e-8 * old_width) | (
                omniscient_current > old_lower + 1.0e-8 * old_width
            )
            if np.any(state_relevant):
                relevant_primal_ratio = float(
                    np.max((omniscient_current - current)[state_relevant] / old_width)
                )
                relevant_extrapolate_ratio = float(
                    np.max(
                        (omniscient_same_time_extrapolate - masked_same_time_extrapolate)[
                            state_relevant
                        ]
                        / old_width
                    )
                )
                maximum_relevant_primal_domination_ratio = max(
                    maximum_relevant_primal_domination_ratio,
                    relevant_primal_ratio,
                )
                maximum_relevant_extrapolate_domination_ratio = max(
                    maximum_relevant_extrapolate_domination_ratio,
                    relevant_extrapolate_ratio,
                )
                if len(certified) < len(omniscient_face):
                    maximum_growing_relevant_extrapolate_domination_ratio = max(
                        maximum_growing_relevant_extrapolate_domination_ratio,
                        relevant_extrapolate_ratio,
                    )
            lag_one_deficit = float(np.max(lagged_omniscient_lower - lower))
            maximum_signed_omniscient_domination_deficit = max(
                maximum_signed_omniscient_domination_deficit, domination_deficit
            )
            maximum_signed_lag_one_domination_deficit = max(
                maximum_signed_lag_one_domination_deficit, lag_one_deficit
            )
            progressed = omniscient_lower > old_lower + 1.0e-12 * old_width
            if np.any(progressed):
                maximum_progress_omniscient_domination_deficit = max(
                    maximum_progress_omniscient_domination_deficit,
                    float(np.max((omniscient_lower - lower)[progressed])),
                )
                progress_indices = np.flatnonzero(progressed)
                progress_ratios = (omniscient_lower - lower)[progressed] / (
                    omniscient_lower - old_lower
                )[progressed]
                progress_ratio = float(np.max(progress_ratios))
                if progress_ratio > maximum_progress_omniscient_domination_ratio:
                    progress_vertex = int(progress_indices[np.argmax(progress_ratios)])
                    progress_domination_witness = {
                        "phase": len(phase_records),
                        "iteration": iteration + 1,
                        "vertex": progress_vertex,
                        "ratio": progress_ratio,
                        "old_lower": float(old_lower[progress_vertex]),
                        "masked_lower": float(lower[progress_vertex]),
                        "omniscient_lower": float(omniscient_lower[progress_vertex]),
                        "pre_push_lower": float(lower_before_push[progress_vertex]),
                        "pre_push_residual": float(residual_before_push[progress_vertex]),
                        "masked_current": float(current[progress_vertex]),
                        "omniscient_current": float(omniscient_current[progress_vertex]),
                        "omniscient_candidate": float(
                            omniscient_candidate[
                                list(map(int, omniscient_face)).index(progress_vertex)
                            ]
                        )
                        if progress_vertex in set(map(int, omniscient_face))
                        else 0.0,
                    }
                maximum_progress_omniscient_domination_ratio = max(
                    maximum_progress_omniscient_domination_ratio, progress_ratio
                )
                if len(certified) < len(omniscient_face):
                    if progress_ratio > maximum_growing_progress_domination_ratio:
                        growing_vertex = int(progress_indices[np.argmax(progress_ratios)])
                        growing_progress_domination_witness = {
                            "phase": len(phase_records),
                            "iteration": iteration + 1,
                            "vertex": growing_vertex,
                            "ratio": progress_ratio,
                            "old_lower": float(old_lower[growing_vertex]),
                            "masked_lower": float(lower[growing_vertex]),
                            "omniscient_lower": float(omniscient_lower[growing_vertex]),
                            "pre_push_lower": float(lower_before_push[growing_vertex]),
                            "pre_push_residual": float(residual_before_push[growing_vertex]),
                            "in_mask": growing_vertex in certified,
                            "mask_size": len(certified),
                            "omniscient_face_size": len(omniscient_face),
                        }
                    maximum_growing_progress_domination_ratio = max(
                        maximum_growing_progress_domination_ratio, progress_ratio
                    )
            lag_one_primal_deficit = float(np.max(lagged_omniscient_current - current))
            lag_one_auxiliary_deficit = float(np.max(lagged_omniscient_auxiliary - auxiliary))
            masked_extrapolate = (current + root * auxiliary) / (1.0 + root)
            lagged_omniscient_extrapolate = (
                lagged_omniscient_current + root * lagged_omniscient_auxiliary
            ) / (1.0 + root)
            lag_one_extrapolate_deficit = float(
                np.max(lagged_omniscient_extrapolate - masked_extrapolate)
            )
            lag_primal_over_lower_deficit = float(np.max(lagged_omniscient_current - lower))
            lag_extrapolate_over_lower_deficit = float(
                np.max(lagged_omniscient_extrapolate - lower)
            )
            lag_vertex = int(np.argmax(lagged_omniscient_lower - lower))
            if lag_one_deficit > maximum_lag_one_domination_deficit:
                lag_one_domination_witness = {
                    "phase": len(phase_records),
                    "iteration": iteration + 1,
                    "vertex": lag_vertex,
                    "masked_lower": float(lower[lag_vertex]),
                    "lagged_omniscient_lower": float(lagged_omniscient_lower[lag_vertex]),
                    "old_width": old_width,
                    "in_mask": lag_vertex in certified,
                }
            maximum_lag_one_domination_deficit = max(
                maximum_lag_one_domination_deficit,
                lag_one_deficit,
            )
            maximum_lag_one_primal_deficit = max(
                maximum_lag_one_primal_deficit,
                lag_one_primal_deficit,
            )
            maximum_lag_one_auxiliary_deficit = max(
                maximum_lag_one_auxiliary_deficit,
                lag_one_auxiliary_deficit,
            )
            maximum_lag_one_extrapolate_deficit = max(
                maximum_lag_one_extrapolate_deficit,
                lag_one_extrapolate_deficit,
            )
            maximum_lag_primal_over_lower_deficit = max(
                maximum_lag_primal_over_lower_deficit,
                lag_primal_over_lower_deficit,
            )
            maximum_lag_extrapolate_over_lower_deficit = max(
                maximum_lag_extrapolate_over_lower_deficit,
                lag_extrapolate_over_lower_deficit,
            )
            domination_vertex = int(np.argmax(omniscient_lower - lower))
            if domination_deficit > maximum_omniscient_domination_deficit:
                omniscient_domination_witness = {
                    "phase": len(phase_records),
                    "iteration": iteration + 1,
                    "vertex": domination_vertex,
                    "masked_lower": float(lower[domination_vertex]),
                    "omniscient_lower": float(omniscient_lower[domination_vertex]),
                    "old_width": old_width,
                    "in_mask": domination_vertex in certified,
                }
            maximum_omniscient_domination_deficit = max(
                maximum_omniscient_domination_deficit,
                domination_deficit,
            )
            maximum_omniscient_domination_ratio = max(
                maximum_omniscient_domination_ratio,
                domination_deficit / old_width,
            )
            lagged_omniscient_lower = omniscient_lower.copy()
            lagged_omniscient_current = omniscient_current.copy()
            lagged_omniscient_auxiliary = omniscient_auxiliary.copy()

            inner_width = float(
                np.max(np.maximum(full_residual, 0.0) / (shifted_gap * sqrt_degrees))
            )
            if inner_width <= requested_inner_width * (1.0 + 2.0e-10):
                break
        else:
            raise RuntimeError("a retained-prox phase exceeded its iteration limit")

        phase_iterations = iteration + 1
        bracket_width = contraction * old_width + inner_width
        new_original_residual = load - q_matrix @ lower
        new_residual_width = float(
            np.max(np.maximum(new_original_residual, 0.0) / (alpha * sqrt_degrees))
        )
        total_iterations += phase_iterations
        total_events += len(phase_events)

        assert np.min(lower - old_lower) >= -3.0e-8
        assert np.min(exact_prox - lower) >= -3.0e-7
        assert np.min(optimum - lower) >= -3.0e-7
        assert np.max((optimum - lower) / sqrt_degrees) <= bracket_width + 5.0e-7
        assert set(np.flatnonzero(lower > 1.0e-10)).issubset(set(final_support))
        assert new_residual_width <= 2.0 * bracket_width + 8.0e-7

        phase_records.append(
            {
                "phase": len(phase_records),
                "old_width": old_width,
                "inner_width": inner_width,
                "old_residual_width": old_residual_width,
                "new_residual_width": new_residual_width,
                "new_width": bracket_width,
                "iterations": phase_iterations,
                "root_time": phase_iterations * root,
                "events": phase_events,
                "face_size": len(certified),
                "face_volume": float(degrees[list(certified)].sum()),
            }
        )

    if residual_push and not block_residual_push:
        assert total_residual_push_work <= (residual_push_rounds * total_volume_work + 1.0e-8)
    if positive_append and not block_append:
        assert total_positive_append_work <= final_volume + 1.0e-8

    return {
        "alpha": alpha,
        "rho": rho,
        "vertices": len(adjacency),
        "final_support_size": len(final_support),
        "final_volume": final_volume,
        "phases": len(phase_records),
        "total_iterations": total_iterations,
        "total_root_time": total_iterations * root,
        "maximum_phase_root_time": max(
            (float(record["root_time"]) for record in phase_records),
            default=0.0,
        ),
        "maximum_eventful_phase_root_time": max(
            (float(record["root_time"]) for record in phase_records if len(record["events"])),
            default=0.0,
        ),
        "events": total_events,
        "final_width": bracket_width,
        "target_width": target_width,
        "total_volume_work": total_volume_work,
        "root_work_ratio": total_volume_work * math.sqrt(alpha) / max(final_volume, 1.0),
        "total_residual_push_work": total_residual_push_work,
        "residual_push_rounds": residual_push_rounds,
        "total_positive_append_work": total_positive_append_work,
        "total_post_append_push_work": total_post_append_push_work,
        "input_residual_append": input_residual_append,
        "total_charged_volume_work": (
            total_volume_work
            + total_residual_push_work
            + total_positive_append_work
            + total_post_append_push_work
        ),
        "charged_root_work_ratio": (
            (
                total_volume_work
                + total_residual_push_work
                + total_positive_append_work
                + total_post_append_push_work
            )
            * math.sqrt(alpha)
            / max(final_volume, 1.0)
        ),
        "contains_uncharged_block_solve": bool(block_append or block_residual_push),
        "maximum_omniscient_domination_deficit": maximum_omniscient_domination_deficit,
        "maximum_signed_omniscient_domination_deficit": (
            maximum_signed_omniscient_domination_deficit
        ),
        "maximum_progress_omniscient_domination_deficit": (
            maximum_progress_omniscient_domination_deficit
        ),
        "maximum_progress_omniscient_domination_ratio": (
            maximum_progress_omniscient_domination_ratio
        ),
        "progress_domination_witness": progress_domination_witness,
        "maximum_growing_progress_domination_ratio": (maximum_growing_progress_domination_ratio),
        "growing_progress_domination_witness": (growing_progress_domination_witness),
        "maximum_omniscient_domination_ratio": maximum_omniscient_domination_ratio,
        "omniscient_domination_witness": omniscient_domination_witness,
        "maximum_lag_one_domination_deficit": maximum_lag_one_domination_deficit,
        "maximum_signed_lag_one_domination_deficit": (maximum_signed_lag_one_domination_deficit),
        "lag_one_domination_witness": lag_one_domination_witness,
        "maximum_lag_one_primal_deficit": maximum_lag_one_primal_deficit,
        "maximum_lag_one_auxiliary_deficit": maximum_lag_one_auxiliary_deficit,
        "maximum_lag_one_extrapolate_deficit": maximum_lag_one_extrapolate_deficit,
        "maximum_lag_primal_over_lower_deficit": maximum_lag_primal_over_lower_deficit,
        "maximum_lag_extrapolate_over_lower_deficit": (maximum_lag_extrapolate_over_lower_deficit),
        "maximum_missing_omniscient_after_closure": (maximum_missing_omniscient_after_closure),
        "maximum_same_time_primal_deficit": maximum_same_time_primal_deficit,
        "maximum_same_time_auxiliary_deficit": maximum_same_time_auxiliary_deficit,
        "maximum_same_time_extrapolate_deficit": (maximum_same_time_extrapolate_deficit),
        "maximum_relevant_primal_domination_ratio": (maximum_relevant_primal_domination_ratio),
        "maximum_relevant_extrapolate_domination_ratio": (
            maximum_relevant_extrapolate_domination_ratio
        ),
        "maximum_growing_relevant_extrapolate_domination_ratio": (
            maximum_growing_relevant_extrapolate_domination_ratio
        ),
        "maximum_exterior_omniscient_primal_ratio": (maximum_exterior_omniscient_primal_ratio),
        "maximum_exterior_omniscient_auxiliary_ratio": (
            maximum_exterior_omniscient_auxiliary_ratio
        ),
        "maximum_exterior_omniscient_extrapolate_ratio": (
            maximum_exterior_omniscient_extrapolate_ratio
        ),
        "exterior_omniscient_state_witness": exterior_omniscient_state_witness,
        "maximum_boundary_flux_gate_ratio": maximum_boundary_flux_gate_ratio,
        "maximum_boundary_raw_gate_ratio": maximum_boundary_raw_gate_ratio,
        "boundary_flux_gate_witness": boundary_flux_gate_witness,
        "maximum_boundary_layer_order_ratio": maximum_boundary_layer_order_ratio,
        "boundary_layer_order_witness": boundary_layer_order_witness,
        "maximum_masked_frontier_extrapolate_over_lower_ratio": (
            maximum_masked_frontier_extrapolate_over_lower_ratio
        ),
        "masked_frontier_witness": masked_frontier_witness,
        "minimum_clamp_extrapolate_change_ratio": (minimum_clamp_extrapolate_change_ratio),
        "minimum_post_clamp_extrapolate_margin_ratio": (
            minimum_post_clamp_extrapolate_margin_ratio
        ),
        "clamp_extrapolate_witness": clamp_extrapolate_witness,
        "minimum_active_raw_momentum_compatibility_ratio": (
            minimum_active_raw_momentum_compatibility_ratio
        ),
        "maximum_shadow_residual_cover_deficit": (maximum_shadow_residual_cover_deficit),
        "maximum_shadow_residual_cover_ratio": (maximum_shadow_residual_cover_ratio),
        "maximum_pre_push_lower_deficit_ratio": (maximum_pre_push_lower_deficit_ratio),
        "pre_push_lower_witness": pre_push_lower_witness,
        "maximum_shadow_increment_over_starting_lower_ratio": (
            maximum_shadow_increment_over_starting_lower_ratio
        ),
        "maximum_relevant_shadow_increment_over_starting_lower_ratio": (
            maximum_relevant_shadow_increment_over_starting_lower_ratio
        ),
        "minimum_one_step_current_lead_ratio": (minimum_one_step_current_lead_ratio),
        "minimum_one_step_auxiliary_lead_ratio": (minimum_one_step_auxiliary_lead_ratio),
        "minimum_one_step_extrapolate_lead_ratio": (minimum_one_step_extrapolate_lead_ratio),
        "maximum_post_push_current_over_lower_ratio": (maximum_post_push_current_over_lower_ratio),
        "maximum_post_push_auxiliary_over_lower_ratio": (
            maximum_post_push_auxiliary_over_lower_ratio
        ),
        "maximum_masked_retraction_shift_ratio": (maximum_masked_retraction_shift_ratio),
        "minimum_residual_velocity_credit_ratio": (minimum_residual_velocity_credit_ratio),
        "minimum_masked_input_residual_ratio": (minimum_masked_input_residual_ratio),
        "shadow_increment_witness": shadow_increment_witness,
        "maximum_omniscient_over_one_jacobi_ratio": (maximum_omniscient_over_one_jacobi_ratio),
        "maximum_omniscient_over_two_jacobi_ratio": (maximum_omniscient_over_two_jacobi_ratio),
        "maximum_estimate_potential_contraction_ratio": (
            maximum_estimate_potential_contraction_ratio
        ),
        "estimate_potential_witness": estimate_potential_witness,
        "omniscient_jacobi_cap_witness": omniscient_jacobi_cap_witness,
        "maximum_adjacent_shadow_deficit": maximum_adjacent_shadow_deficit,
        "maximum_adjacent_shadow_ratio": maximum_adjacent_shadow_ratio,
        "maximum_growing_adjacent_shadow_ratio": (maximum_growing_adjacent_shadow_ratio),
        "phase_records": phase_records,
    }


def named_graph(name: str, size: int, seed: int) -> np.ndarray:
    if name == "delayed":
        return delayed_publication_graph()
    if name == "green40":
        return green_band_stress_graph()
    if name == "lag4":
        return graph(4, [(0, 1), (0, 2), (1, 2), (1, 3)])
    if name == "lag30":
        return graph(30, LAG30_EDGES)
    if name == "layers":
        return alternating_layers(max(2, size // 4), 4)
    if name == "lollipop":
        return lollipop(max(3, size // 3), max(2, size - size // 3))
    if name == "path":
        return graph(size, [(vertex, vertex + 1) for vertex in range(size - 1)])
    if name == "random":
        rng = np.random.default_rng(seed)
        return random_connected_graph(rng, size, 2.0 / max(size, 2))
    raise ValueError(f"unknown graph {name!r}")


def compact(result: dict[str, object]) -> dict[str, object]:
    keys = (
        "alpha",
        "rho",
        "vertices",
        "final_support_size",
        "final_volume",
        "phases",
        "total_iterations",
        "total_root_time",
        "maximum_phase_root_time",
        "maximum_eventful_phase_root_time",
        "events",
        "final_width",
        "target_width",
        "total_volume_work",
        "root_work_ratio",
        "total_residual_push_work",
        "residual_push_rounds",
        "total_positive_append_work",
        "total_post_append_push_work",
        "input_residual_append",
        "total_charged_volume_work",
        "charged_root_work_ratio",
        "contains_uncharged_block_solve",
        "maximum_omniscient_domination_deficit",
        "maximum_omniscient_domination_ratio",
        "maximum_lag_one_domination_deficit",
        "lag_one_domination_witness",
        "maximum_lag_one_primal_deficit",
        "maximum_lag_one_auxiliary_deficit",
        "maximum_lag_one_extrapolate_deficit",
        "maximum_lag_primal_over_lower_deficit",
        "maximum_lag_extrapolate_over_lower_deficit",
        "minimum_masked_input_residual_ratio",
        "maximum_estimate_potential_contraction_ratio",
    )
    return {key: result[key] for key in keys}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph",
        choices=(
            "delayed",
            "green40",
            "lag4",
            "lag30",
            "layers",
            "lollipop",
            "path",
            "random",
            "suite",
        ),
        default="suite",
    )
    parser.add_argument("--size", type=int, default=48)
    parser.add_argument("--alpha", type=float, default=1.0e-3)
    parser.add_argument("--rho", type=float, default=1.0e-5)
    parser.add_argument("--relative-width", type=float, default=1.0e-5)
    parser.add_argument("--publication-floor", type=float, default=2.0e-13)
    parser.add_argument("--positive-append", action="store_true")
    parser.add_argument("--block-append", action="store_true")
    parser.add_argument("--residual-push", action="store_true")
    parser.add_argument("--residual-push-rounds", type=int, default=1)
    parser.add_argument("--post-append-residual-push", action="store_true")
    parser.add_argument("--input-residual-append", action="store_true")
    parser.add_argument("--block-residual-push", action="store_true")
    parser.add_argument("--seed", type=int, default=20260901)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()

    names = (
        ("delayed", "green40", "layers", "lollipop", "path")
        if args.graph == "suite"
        else (args.graph,)
    )
    results = {}
    for name in names:
        adjacency = named_graph(name, args.size, args.seed)
        result = run_retained_prox(
            adjacency,
            args.alpha,
            args.rho,
            relative_width=args.relative_width,
            publication_floor=args.publication_floor,
            positive_append=args.positive_append,
            block_append=args.block_append,
            residual_push=args.residual_push,
            block_residual_push=args.block_residual_push,
            residual_push_rounds=args.residual_push_rounds,
            post_append_residual_push=args.post_append_residual_push,
            input_residual_append=args.input_residual_append,
        )
        results[name] = result if args.full else compact(result)
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
