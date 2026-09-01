#!/usr/bin/env python3
"""Empirical audit for the conditional two-mask NAG chronology.

This script is deliberately separate from ``witnesses.py``: it explores a
candidate algorithm and does not certify a theorem.  It uses dense matrices
and exact full-row scans, so its results are evidence about activation clocks,
not an output-local implementation bound.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np


def graph(vertex_count: int, edges: list[tuple[int, int]]) -> np.ndarray:
    adjacency = np.zeros((vertex_count, vertex_count), dtype=float)
    for left, right in edges:
        if left != right:
            adjacency[left, right] = 1.0
            adjacency[right, left] = 1.0
    return adjacency


def lollipop(clique_size: int, tail_length: int) -> np.ndarray:
    edges = [(left, right) for left in range(clique_size) for right in range(left + 1, clique_size)]
    previous = 0
    for vertex in range(clique_size, clique_size + tail_length):
        edges.append((previous, vertex))
        previous = vertex
    return graph(clique_size + tail_length, edges)


def alternating_layers(depth: int, width: int) -> np.ndarray:
    widths = ([1, width] * depth)[:depth]
    offsets = np.cumsum([0] + widths)
    edges: list[tuple[int, int]] = []
    for layer in range(len(widths) - 1):
        edges.extend(
            (left, right)
            for left in range(offsets[layer], offsets[layer + 1])
            for right in range(offsets[layer + 1], offsets[layer + 2])
        )
    return graph(int(offsets[-1]), edges)


def delayed_publication_graph() -> np.ndarray:
    """Simple-unit witness separating scratch readiness from publication dwell."""
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (2, 20),
        (3, 4),
        (3, 9),
        (3, 18),
        (4, 5),
        (4, 11),
        (4, 13),
        (4, 17),
        (5, 6),
        (5, 11),
        (5, 19),
        (6, 7),
        (6, 22),
        (7, 8),
        (8, 9),
        (8, 33),
        (9, 10),
        (9, 12),
        (9, 24),
        (9, 33),
        (10, 11),
        (10, 15),
        (10, 25),
        (11, 12),
        (11, 19),
        (11, 20),
        (12, 13),
        (12, 16),
        (12, 17),
        (13, 14),
        (13, 19),
        (13, 24),
        (14, 15),
        (14, 16),
        (14, 18),
        (14, 26),
        (15, 26),
        (15, 30),
        (16, 17),
        (16, 28),
        (17, 20),
        (18, 19),
        (18, 25),
        (19, 20),
        (19, 32),
        (20, 21),
        (20, 28),
        (21, 22),
        (21, 30),
        (22, 23),
        (22, 29),
        (23, 25),
        (23, 30),
        (24, 25),
        (24, 32),
        (25, 26),
        (25, 27),
        (26, 27),
        (27, 28),
        (27, 29),
        (27, 32),
        (28, 29),
        (29, 30),
        (30, 31),
        (31, 32),
        (32, 33),
    ]
    return graph(34, edges)


def green_band_stress_graph() -> np.ndarray:
    """Search witness with several root-scale gaps and small packet release."""
    edges = [
        (0, 1),
        (0, 2),
        (0, 10),
        (0, 11),
        (0, 23),
        (0, 24),
        (0, 38),
        (1, 3),
        (1, 5),
        (1, 6),
        (2, 30),
        (2, 31),
        (2, 34),
        (3, 4),
        (3, 11),
        (3, 15),
        (3, 25),
        (4, 8),
        (4, 16),
        (4, 17),
        (4, 34),
        (5, 7),
        (5, 12),
        (6, 9),
        (6, 14),
        (7, 19),
        (8, 10),
        (8, 14),
        (9, 13),
        (9, 20),
        (9, 21),
        (9, 38),
        (11, 23),
        (12, 17),
        (13, 16),
        (13, 18),
        (14, 37),
        (15, 22),
        (16, 26),
        (16, 29),
        (17, 24),
        (17, 32),
        (18, 30),
        (18, 35),
        (19, 24),
        (19, 28),
        (21, 32),
        (21, 37),
        (22, 33),
        (23, 39),
        (25, 27),
        (27, 34),
        (27, 36),
        (29, 34),
        (37, 39),
    ]
    return graph(40, edges)


def random_connected_graph(
    rng: np.random.Generator,
    vertex_count: int,
    extra_edge_probability: float,
) -> np.ndarray:
    edges: list[tuple[int, int]] = []
    for vertex in range(1, vertex_count):
        edges.append((vertex, int(rng.integers(vertex))))
    for left in range(vertex_count):
        for right in range(left + 1, vertex_count):
            if (left, right) not in edges and (right, left) not in edges:
                if rng.random() < extra_edge_probability:
                    edges.append((left, right))
    return graph(vertex_count, edges)


def run_two_mask(
    adjacency: np.ndarray,
    alpha: float,
    rho: float,
    *,
    maximum_iterations: int = 10_000,
    publication_tolerance: float = 1.0e-14,
) -> dict[str, object]:
    vertex_count = len(adjacency)
    degrees = adjacency.sum(axis=1)
    sqrt_degrees = np.sqrt(degrees)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    q_matrix = diagonal * np.eye(vertex_count) - coupling * adjacency / np.outer(
        sqrt_degrees, sqrt_degrees
    )
    load = -alpha * rho * sqrt_degrees
    load[0] += alpha / sqrt_degrees[0]
    beta = (1.0 - math.sqrt(alpha)) / (1.0 + math.sqrt(alpha))

    scratch = np.array([0], dtype=int)
    certified = {0}
    pending = np.array([], dtype=int)
    current = np.zeros(vertex_count)
    previous = np.zeros(vertex_count)
    lower = np.zeros(vertex_count)
    waits: list[int] = []
    publication_scratch_minima: list[float] = []
    publication_history_deficits: list[float] = []
    pending_start: int | None = None
    volume_work = 0.0

    for iteration in range(maximum_iterations):
        extrapolated = current[scratch] + beta * (current[scratch] - previous[scratch])
        next_iterate = np.zeros(vertex_count)
        next_iterate[scratch] = (
            extrapolated + load[scratch] - q_matrix[np.ix_(scratch, scratch)] @ extrapolated
        )
        previous, current = current, next_iterate
        volume_work += float(degrees[scratch].sum())

        active_residual = load[scratch] - q_matrix[np.ix_(scratch, scratch)] @ current[scratch]
        stationary_direction = q_matrix[np.ix_(scratch, scratch)] @ sqrt_degrees[scratch]
        ratios = np.divide(
            -active_residual,
            stationary_direction,
            out=np.full_like(active_residual, -np.inf),
            where=stationary_direction > 0.0,
        )
        shift = max(0.0, float(np.max(ratios)))
        lower[scratch] = np.maximum(
            lower[scratch],
            np.maximum(current[scratch] - shift * sqrt_degrees[scratch], 0.0),
        )

        if len(pending):
            pending_residual = load[pending] - q_matrix[np.ix_(pending, scratch)] @ current[scratch]
            if np.all(pending_residual >= -1.0e-14):
                scratch = np.sort(np.r_[scratch, pending])
                waits.append(iteration - int(pending_start))
                pending = np.array([], dtype=int)
                pending_start = None
        else:
            full_residual = load - q_matrix @ lower
            outside = np.array(sorted(set(range(vertex_count)) - certified), dtype=int)
            if len(outside):
                batch = outside[full_residual[outside] > publication_tolerance]
                if len(batch):
                    scratch_now = load[batch] - q_matrix[np.ix_(batch, scratch)] @ current[scratch]
                    publication_scratch_minima.append(float(np.min(scratch_now)))
                    publication_history_deficits.append(
                        float(np.max(lower[scratch] - current[scratch]))
                    )
                    pending = batch
                    certified.update(map(int, batch))
                    pending_start = iteration

        if not len(pending):
            full_residual = load - q_matrix @ lower
            outside = np.array(sorted(set(range(vertex_count)) - certified), dtype=int)
            exterior_quiet = (
                not len(outside) or np.max(full_residual[outside]) <= publication_tolerance
            )
            scaled_active_residual = (
                load[scratch] - q_matrix[np.ix_(scratch, scratch)] @ lower[scratch]
            ) / sqrt_degrees[scratch]
            if exterior_quiet and np.linalg.norm(scaled_active_residual) <= max(
                1.0e-13, alpha * rho / 100.0
            ):
                return {
                    "iterations": iteration + 1,
                    "scaled_iterations": (iteration + 1) * math.sqrt(alpha),
                    "events": len(waits),
                    "maximum_wait": max(waits, default=0),
                    "minimum_scratch_residual_at_publication": min(
                        publication_scratch_minima, default=0.0
                    ),
                    "maximum_history_deficit_at_publication": max(
                        publication_history_deficits, default=0.0
                    ),
                    "all_batches_ready_at_publication": all(
                        value >= -1.0e-14 for value in publication_scratch_minima
                    ),
                    "scaled_total_wait": sum(waits) * math.sqrt(alpha),
                    "scratch_size": len(scratch),
                    "scratch_volume": float(degrees[scratch].sum()),
                    "volume_work": volume_work,
                    "terminated": True,
                }

    return {
        "iterations": maximum_iterations,
        "scaled_iterations": maximum_iterations * math.sqrt(alpha),
        "events": len(waits),
        "maximum_wait": max(waits, default=0),
        "minimum_scratch_residual_at_publication": min(publication_scratch_minima, default=0.0),
        "maximum_history_deficit_at_publication": max(publication_history_deficits, default=0.0),
        "all_batches_ready_at_publication": all(
            value >= -1.0e-14 for value in publication_scratch_minima
        ),
        "scaled_total_wait": sum(waits) * math.sqrt(alpha),
        "scratch_size": len(scratch),
        "scratch_volume": float(degrees[scratch].sum()),
        "volume_work": volume_work,
        "terminated": False,
    }


def run_projected_estimate_nag(
    adjacency: np.ndarray,
    alpha: float,
    rho: float,
    *,
    maximum_iterations: int = 10_000,
    publication_tolerance: float = 1.0e-14,
    adaptive_gap: bool = False,
) -> dict[str, object]:
    """Run the dual-dominance projected estimate-sequence candidate.

    Both the physical primal state ``x`` and the physical auxiliary state
    ``x+a(x-x_previous)`` are projected above the historical lower
    subsolution.  The projection is implementable without knowing the exact
    face center.  Dense exact centers are computed here only to audit the
    proved potential inequalities; they are not used by the iteration.
    """
    vertex_count = len(adjacency)
    degrees = adjacency.sum(axis=1)
    sqrt_degrees = np.sqrt(degrees)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    q_matrix = diagonal * np.eye(vertex_count) - coupling * adjacency / np.outer(
        sqrt_degrees, sqrt_degrees
    )
    load = -alpha * rho * sqrt_degrees
    load[0] += alpha / sqrt_degrees[0]
    normalized_adjacency = adjacency / np.outer(sqrt_degrees, sqrt_degrees)

    scratch = np.array([0], dtype=int)
    certified = {0}
    current = np.zeros(vertex_count)
    previous = np.zeros(vertex_count)
    lower = np.zeros(vertex_count)
    volume_work = 0.0
    events = 0
    projection_ratios: list[float] = []
    event_debt_slacks: list[float] = []
    companion_held_ratios: list[float] = []
    companion_projection_ratios: list[float] = []
    companion_event_slacks: list[float] = []
    publication_scratch_minima: list[float] = []
    event_iterations: list[int] = []
    event_batches: list[list[int]] = []
    center_increment_energies: list[float] = []
    exact_gate_squares: list[float] = []
    face_volumes_at_events: list[float] = []
    certificate_history: list[dict[str, float | int]] = []
    adaptive_root_clock = 0.0
    minimum_subgradient_norms: list[float] = []

    def landscape_certificate(mask: np.ndarray) -> float:
        internal_degree = adjacency[np.ix_(mask, mask)].sum(axis=1)
        exposed_fraction = (degrees[mask] - internal_degree) / degrees[mask]
        return float(alpha + coupling * np.min(exposed_fraction))

    def dyadic_floor(value: float) -> float:
        if value <= alpha:
            return alpha
        level = math.floor(math.log(value / alpha, 2.0) + 1.0e-12)
        return min(1.0, alpha * (2.0**level))

    current_mu = dyadic_floor(landscape_certificate(scratch)) if adaptive_gap else alpha
    square_root = math.sqrt(current_mu)
    beta = (1.0 - square_root) / (1.0 + square_root)
    auxiliary_scale = (1.0 - square_root) / square_root
    certificate_history.append(
        {"iteration": -1, "raw": landscape_certificate(scratch), "mu": current_mu}
    )

    def lower_clock(new_mu: float) -> None:
        """Lower the certified root while preserving the physical auxiliary point."""
        nonlocal current_mu, square_root, beta, auxiliary_scale, previous
        assert new_mu <= current_mu * (1.0 + 1.0e-12)
        if new_mu >= current_mu * (1.0 - 1.0e-14):
            return
        auxiliary = current + auxiliary_scale * (current - previous)
        current_mu = new_mu
        square_root = math.sqrt(current_mu)
        beta = (1.0 - square_root) / (1.0 + square_root)
        auxiliary_scale = (1.0 - square_root) / square_root
        previous = current - (auxiliary - current) / auxiliary_scale

    def exact_center(mask: np.ndarray) -> np.ndarray:
        center = np.zeros(vertex_count)
        center[mask] = np.linalg.solve(q_matrix[np.ix_(mask, mask)], load[mask])
        return center

    def estimate_potential(
        mask: np.ndarray,
        center: np.ndarray,
        state: np.ndarray,
        prior: np.ndarray,
    ) -> float:
        h = state[mask] - center[mask]
        velocity = state[mask] - prior[mask]
        auxiliary_error = h + auxiliary_scale * velocity
        block = q_matrix[np.ix_(mask, mask)]
        return float(0.5 * h @ block @ h + 0.5 * current_mu * auxiliary_error @ auxiliary_error)

    def companion_potential(
        mask: np.ndarray,
        center: np.ndarray,
        state: np.ndarray,
        prior: np.ndarray,
    ) -> float:
        """Full-spectrum certified-gap ``F_mu`` Lyapunov."""
        h = state[mask] - center[mask]
        auxiliary = state[mask] + auxiliary_scale * (state[mask] - prior[mask])
        w = square_root * (auxiliary - center[mask])
        block = q_matrix[np.ix_(mask, mask)]
        s_block = normalized_adjacency[np.ix_(mask, mask)]
        f_mu = (
            diagonal * coupling * np.eye(len(mask))
            - coupling * (current_mu - alpha) * s_block
            - coupling**2 * (s_block @ s_block)
        )
        return float(h @ block @ h + w @ w + w @ f_mu @ w)

    center = exact_center(scratch)
    for iteration in range(maximum_iterations):
        adaptive_root_clock += square_root
        companion_before_step = companion_potential(scratch, center, current, previous)
        extrapolated = current[scratch] + beta * (current[scratch] - previous[scratch])
        next_iterate = np.zeros(vertex_count)
        next_iterate[scratch] = (
            extrapolated + load[scratch] - q_matrix[np.ix_(scratch, scratch)] @ extrapolated
        )
        previous, current = current, next_iterate
        volume_work += float(degrees[scratch].sum())

        companion_after_held = companion_potential(scratch, center, current, previous)
        if companion_before_step > 1.0e-28:
            companion_held_ratios.append(
                companion_after_held / ((1.0 - square_root) * companion_before_step)
            )

        active_residual = load[scratch] - q_matrix[np.ix_(scratch, scratch)] @ current[scratch]
        stationary_direction = q_matrix[np.ix_(scratch, scratch)] @ sqrt_degrees[scratch]
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

        potential_before_projection = estimate_potential(scratch, center, current, previous)
        companion_before_projection = companion_potential(scratch, center, current, previous)
        if auxiliary_scale > 0.0:
            auxiliary = current + auxiliary_scale * (current - previous)
            current[scratch] = np.maximum(current[scratch], lower[scratch])
            auxiliary[scratch] = np.maximum(auxiliary[scratch], lower[scratch])
            velocity = auxiliary[scratch] - current[scratch]
            velocity /= auxiliary_scale
            previous[scratch] = current[scratch] - velocity
        else:
            current[scratch] = np.maximum(current[scratch], lower[scratch])
            previous[scratch] = current[scratch]
        potential_after_projection = estimate_potential(scratch, center, current, previous)
        companion_after_projection = companion_potential(scratch, center, current, previous)
        if potential_before_projection > 0.0:
            projection_ratios.append(potential_after_projection / potential_before_projection)
        if companion_before_projection > 1.0e-28:
            companion_projection_ratios.append(
                companion_after_projection / companion_before_projection
            )

        full_residual = load - q_matrix @ lower
        outside = np.array(sorted(set(range(vertex_count)) - certified), dtype=int)
        batch = np.array([], dtype=int)
        if len(outside):
            batch = outside[full_residual[outside] > publication_tolerance]
        if len(batch):
            scratch_now = load[batch] - q_matrix[np.ix_(batch, scratch)] @ current[scratch]
            publication_scratch_minima.append(float(np.min(scratch_now)))

            old_scratch = scratch
            old_center = center
            prospective_scratch = np.sort(np.r_[scratch, batch])
            raw_certificate = landscape_certificate(prospective_scratch)
            new_mu = min(current_mu, dyadic_floor(raw_certificate)) if adaptive_gap else alpha
            root_changed = new_mu < current_mu * (1.0 - 1.0e-14)
            lower_clock(new_mu)
            if root_changed:
                certificate_history.append(
                    {
                        "iteration": iteration,
                        "raw": raw_certificate,
                        "mu": current_mu,
                    }
                )
            old_companion = companion_potential(old_scratch, old_center, current, previous)
            old_potential = estimate_potential(old_scratch, old_center, current, previous)
            scratch = prospective_scratch
            certified.update(map(int, batch))
            center = exact_center(scratch)
            new_companion = companion_potential(scratch, center, current, previous)
            new_potential = estimate_potential(scratch, center, current, previous)
            center_increment = center - old_center
            center_energy = float(center_increment @ q_matrix @ center_increment)
            center_increment_energies.append(center_energy)
            face_volumes_at_events.append(float(degrees[scratch].sum()))
            combined_jump = new_potential - old_potential - center_energy
            historical_room = old_center - lower
            proved_bank = float(current_mu * historical_room @ center_increment)
            event_debt_slacks.append(proved_bank - combined_jump)

            center_increment = center - old_center
            exact_gate = (
                load[batch] - q_matrix[np.ix_(batch, old_scratch)] @ old_center[old_scratch]
            )
            exact_gate_squares.append(float(exact_gate @ exact_gate))
            auxiliary = current + auxiliary_scale * (current - previous)
            old_w = square_root * (auxiliary[old_scratch] - old_center[old_scratch])
            cut = -q_matrix[np.ix_(batch, old_scratch)]
            cut_w = cut @ old_w
            old_room = old_center - lower
            event_upper = (
                -0.5 * float(cut_w @ cut_w)
                + (2.0 + current_mu) * center_energy
                + 2.0 * current_mu * float(old_room @ center_increment)
                + 2.0 * current_mu * float(exact_gate @ exact_gate)
            )
            companion_event_slacks.append(event_upper - (new_companion - old_companion))
            events += 1
            event_iterations.append(iteration)
            event_batches.append([int(vertex) for vertex in batch])

        smooth_gradient = q_matrix @ current - load
        minimum_subgradient = smooth_gradient.copy()
        zero_coordinates = current <= 1.0e-15
        minimum_subgradient[zero_coordinates] = np.minimum(
            minimum_subgradient[zero_coordinates],
            0.0,
        )
        minimum_subgradient_norms.append(float(np.linalg.norm(minimum_subgradient)))

        if not len(batch):
            outside = np.array(sorted(set(range(vertex_count)) - certified), dtype=int)
            exterior_quiet = (
                not len(outside) or np.max(full_residual[outside]) <= publication_tolerance
            )
            scaled_active_residual = (
                load[scratch] - q_matrix[np.ix_(scratch, scratch)] @ lower[scratch]
            ) / sqrt_degrees[scratch]
            if exterior_quiet and np.linalg.norm(scaled_active_residual) <= max(
                1.0e-13, alpha * rho / 100.0
            ):
                inter_event_gaps = [
                    later - earlier
                    for earlier, later in zip(event_iterations, event_iterations[1:])
                ]
                remaining_event_energies = np.cumsum(
                    np.asarray(center_increment_energies[::-1], dtype=float)
                )[::-1]
                release_fractions = [
                    energy / remaining
                    for energy, remaining in zip(
                        center_increment_energies,
                        remaining_event_energies,
                    )
                    if remaining > 0.0
                ]
                long_window_threshold = 0.5 / math.sqrt(alpha)
                long_window_release_fractions = [
                    center_increment_energies[index] / remaining_event_energies[index]
                    for index in range(1, len(center_increment_energies))
                    if event_iterations[index] - event_iterations[index - 1]
                    >= long_window_threshold
                    and remaining_event_energies[index] > 0.0
                ]
                delayed_burst_starts = [
                    index
                    for index in range(1, len(center_increment_energies))
                    if event_iterations[index] - event_iterations[index - 1]
                    >= long_window_threshold
                ]
                delayed_burst_release_fractions = []
                for start_index, next_start in zip(
                    delayed_burst_starts,
                    delayed_burst_starts[1:] + [len(center_increment_energies)],
                ):
                    remaining = remaining_event_energies[start_index]
                    if remaining > 0.0:
                        released = sum(center_increment_energies[start_index:next_start])
                        delayed_burst_release_fractions.append(released / remaining)
                h_matrix = np.diag(sqrt_degrees) @ q_matrix @ np.diag(sqrt_degrees)
                final_green = np.zeros(vertex_count)
                final_green[scratch] = np.linalg.solve(
                    h_matrix[np.ix_(scratch, scratch)],
                    alpha * (scratch == 0).astype(float),
                )
                final_solution_amplitude = center / sqrt_degrees
                green_amplitude_drop_ratios: list[float] = []
                solution_amplitude_drop_ratios: list[float] = []
                face_growth_ratios: list[float] = []
                face_before = {0}
                for event_batch in event_batches:
                    remaining_before = sorted(set(map(int, scratch)) - face_before)
                    amplitude_before = max(
                        (final_green[vertex] for vertex in remaining_before),
                        default=0.0,
                    )
                    solution_amplitude_before = max(
                        (
                            final_solution_amplitude[vertex]
                            for vertex in remaining_before
                        ),
                        default=0.0,
                    )
                    volume_before = float(degrees[list(face_before)].sum())
                    face_before.update(event_batch)
                    remaining_after = sorted(set(map(int, scratch)) - face_before)
                    amplitude_after = max(
                        (final_green[vertex] for vertex in remaining_after),
                        default=0.0,
                    )
                    solution_amplitude_after = max(
                        (
                            final_solution_amplitude[vertex]
                            for vertex in remaining_after
                        ),
                        default=0.0,
                    )
                    volume_after = float(degrees[list(face_before)].sum())
                    green_amplitude_drop_ratios.append(
                        amplitude_after / amplitude_before if amplitude_before > 0.0 else 0.0
                    )
                    solution_amplitude_drop_ratios.append(
                        (
                            solution_amplitude_after / solution_amplitude_before
                            if solution_amplitude_before > 0.0
                            else 0.0
                        )
                    )
                    face_growth_ratios.append(volume_after / volume_before)
                delayed_dichotomy_progress = [
                    max(
                        face_growth_ratios[index],
                        (
                            1.0 / green_amplitude_drop_ratios[index]
                            if green_amplitude_drop_ratios[index] > 0.0
                            else float("inf")
                        ),
                    )
                    for index in range(1, len(event_iterations))
                    if event_iterations[index] - event_iterations[index - 1]
                    >= long_window_threshold
                    and green_amplitude_drop_ratios[index] > 0.0
                ]
                delayed_solution_dichotomy_progress = [
                    max(
                        face_growth_ratios[index],
                        (
                            1.0 / solution_amplitude_drop_ratios[index]
                            if solution_amplitude_drop_ratios[index] > 0.0
                            else float("inf")
                        ),
                    )
                    for index in range(1, len(event_iterations))
                    if event_iterations[index] - event_iterations[index - 1]
                    >= long_window_threshold
                    and solution_amplitude_drop_ratios[index] > 0.0
                ]
                return {
                    "iterations": iteration + 1,
                    "scaled_iterations": (iteration + 1) * math.sqrt(alpha),
                    "adaptive_root_clock": adaptive_root_clock,
                    "final_mu": current_mu,
                    "certificate_history": certificate_history,
                    "events": events,
                    "event_iterations": event_iterations,
                    "event_batches": event_batches,
                    "last_event_iteration": max(event_iterations, default=-1),
                    "scaled_event_horizon": (
                        (max(event_iterations, default=-1) + 1) * math.sqrt(alpha)
                    ),
                    "center_increment_energies": center_increment_energies,
                    "effective_packet_eigenvalues": [
                        gate_square / energy
                        for gate_square, energy in zip(
                            exact_gate_squares,
                            center_increment_energies,
                        )
                        if energy > 0.0
                    ],
                    "effective_packet_root_sum": sum(
                        math.sqrt(energy / gate_square)
                        for gate_square, energy in zip(
                            exact_gate_squares,
                            center_increment_energies,
                        )
                        if gate_square > 0.0
                    ),
                    "face_volumes_at_events": face_volumes_at_events,
                    "green_amplitude_drop_ratios": green_amplitude_drop_ratios,
                    "solution_amplitude_drop_ratios": solution_amplitude_drop_ratios,
                    "face_growth_ratios": face_growth_ratios,
                    "minimum_delayed_dichotomy_progress": min(
                        delayed_dichotomy_progress,
                        default=1.0,
                    ),
                    "minimum_delayed_solution_dichotomy_progress": min(
                        delayed_solution_dichotomy_progress,
                        default=1.0,
                    ),
                    "minimum_event_release_fraction": min(release_fractions, default=1.0),
                    "minimum_long_window_release_fraction": min(
                        long_window_release_fractions,
                        default=1.0,
                    ),
                    "minimum_delayed_burst_release_fraction": min(
                        delayed_burst_release_fractions,
                        default=1.0,
                    ),
                    "delayed_bursts": len(delayed_burst_starts),
                    "maximum_inter_event_gap": max(inter_event_gaps, default=0),
                    "maximum_root_scaled_inter_event_gap": (
                        max(inter_event_gaps, default=0) * math.sqrt(alpha)
                    ),
                    "maximum_projection_potential_ratio": max(projection_ratios, default=0.0),
                    "maximum_companion_held_ratio": max(companion_held_ratios, default=0.0),
                    "maximum_companion_projection_ratio": max(
                        companion_projection_ratios, default=0.0
                    ),
                    "minimum_companion_event_slack": min(companion_event_slacks, default=0.0),
                    "minimum_event_debt_slack": min(event_debt_slacks, default=0.0),
                    "minimum_scratch_residual_at_publication": min(
                        publication_scratch_minima, default=0.0
                    ),
                    "initial_minimum_subgradient_norm": minimum_subgradient_norms[0],
                    "final_minimum_subgradient_norm": minimum_subgradient_norms[-1],
                    "maximum_minimum_subgradient_growth": max(
                        (
                            later / earlier
                            for earlier, later in zip(
                                minimum_subgradient_norms,
                                minimum_subgradient_norms[1:],
                            )
                            if earlier > 1.0e-30
                        ),
                        default=0.0,
                    ),
                    "all_batches_ready_at_publication": all(
                        value >= -1.0e-12 for value in publication_scratch_minima
                    ),
                    "scratch_size": len(scratch),
                    "scratch_volume": float(degrees[scratch].sum()),
                    "volume_work": volume_work,
                    "terminated": True,
                }

    inter_event_gaps = [
        later - earlier for earlier, later in zip(event_iterations, event_iterations[1:])
    ]
    remaining_event_energies = np.cumsum(np.asarray(center_increment_energies[::-1], dtype=float))[
        ::-1
    ]
    release_fractions = [
        energy / remaining
        for energy, remaining in zip(center_increment_energies, remaining_event_energies)
        if remaining > 0.0
    ]
    long_window_threshold = 0.5 / math.sqrt(alpha)
    long_window_release_fractions = [
        center_increment_energies[index] / remaining_event_energies[index]
        for index in range(1, len(center_increment_energies))
        if event_iterations[index] - event_iterations[index - 1] >= long_window_threshold
        and remaining_event_energies[index] > 0.0
    ]
    delayed_burst_starts = [
        index
        for index in range(1, len(center_increment_energies))
        if event_iterations[index] - event_iterations[index - 1] >= long_window_threshold
    ]
    delayed_burst_release_fractions = []
    for start_index, next_start in zip(
        delayed_burst_starts,
        delayed_burst_starts[1:] + [len(center_increment_energies)],
    ):
        remaining = remaining_event_energies[start_index]
        if remaining > 0.0:
            released = sum(center_increment_energies[start_index:next_start])
            delayed_burst_release_fractions.append(released / remaining)
    h_matrix = np.diag(sqrt_degrees) @ q_matrix @ np.diag(sqrt_degrees)
    final_green = np.zeros(vertex_count)
    final_green[scratch] = np.linalg.solve(
        h_matrix[np.ix_(scratch, scratch)],
        alpha * (scratch == 0).astype(float),
    )
    final_solution_amplitude = center / sqrt_degrees
    green_amplitude_drop_ratios: list[float] = []
    solution_amplitude_drop_ratios: list[float] = []
    face_growth_ratios: list[float] = []
    face_before = {0}
    for event_batch in event_batches:
        remaining_before = sorted(set(map(int, scratch)) - face_before)
        amplitude_before = max(
            (final_green[vertex] for vertex in remaining_before),
            default=0.0,
        )
        solution_amplitude_before = max(
            (final_solution_amplitude[vertex] for vertex in remaining_before),
            default=0.0,
        )
        volume_before = float(degrees[list(face_before)].sum())
        face_before.update(event_batch)
        remaining_after = sorted(set(map(int, scratch)) - face_before)
        amplitude_after = max(
            (final_green[vertex] for vertex in remaining_after),
            default=0.0,
        )
        solution_amplitude_after = max(
            (final_solution_amplitude[vertex] for vertex in remaining_after),
            default=0.0,
        )
        volume_after = float(degrees[list(face_before)].sum())
        green_amplitude_drop_ratios.append(
            amplitude_after / amplitude_before if amplitude_before > 0.0 else 0.0
        )
        solution_amplitude_drop_ratios.append(
            (
                solution_amplitude_after / solution_amplitude_before
                if solution_amplitude_before > 0.0
                else 0.0
            )
        )
        face_growth_ratios.append(volume_after / volume_before)
    delayed_dichotomy_progress = [
        max(
            face_growth_ratios[index],
            (
                1.0 / green_amplitude_drop_ratios[index]
                if green_amplitude_drop_ratios[index] > 0.0
                else float("inf")
            ),
        )
        for index in range(1, len(event_iterations))
        if event_iterations[index] - event_iterations[index - 1] >= long_window_threshold
        and green_amplitude_drop_ratios[index] > 0.0
    ]
    delayed_solution_dichotomy_progress = [
        max(
            face_growth_ratios[index],
            (
                1.0 / solution_amplitude_drop_ratios[index]
                if solution_amplitude_drop_ratios[index] > 0.0
                else float("inf")
            ),
        )
        for index in range(1, len(event_iterations))
        if event_iterations[index] - event_iterations[index - 1] >= long_window_threshold
        and solution_amplitude_drop_ratios[index] > 0.0
    ]
    return {
        "iterations": maximum_iterations,
        "scaled_iterations": maximum_iterations * math.sqrt(alpha),
        "adaptive_root_clock": adaptive_root_clock,
        "final_mu": current_mu,
        "certificate_history": certificate_history,
        "events": events,
        "event_iterations": event_iterations,
        "event_batches": event_batches,
        "last_event_iteration": max(event_iterations, default=-1),
        "scaled_event_horizon": ((max(event_iterations, default=-1) + 1) * math.sqrt(alpha)),
        "center_increment_energies": center_increment_energies,
        "effective_packet_eigenvalues": [
            gate_square / energy
            for gate_square, energy in zip(
                exact_gate_squares,
                center_increment_energies,
            )
            if energy > 0.0
        ],
        "effective_packet_root_sum": sum(
            math.sqrt(energy / gate_square)
            for gate_square, energy in zip(
                exact_gate_squares,
                center_increment_energies,
            )
            if gate_square > 0.0
        ),
        "face_volumes_at_events": face_volumes_at_events,
        "green_amplitude_drop_ratios": green_amplitude_drop_ratios,
        "solution_amplitude_drop_ratios": solution_amplitude_drop_ratios,
        "face_growth_ratios": face_growth_ratios,
        "minimum_delayed_dichotomy_progress": min(
            delayed_dichotomy_progress,
            default=1.0,
        ),
        "minimum_delayed_solution_dichotomy_progress": min(
            delayed_solution_dichotomy_progress,
            default=1.0,
        ),
        "minimum_event_release_fraction": min(release_fractions, default=1.0),
        "minimum_long_window_release_fraction": min(
            long_window_release_fractions,
            default=1.0,
        ),
        "minimum_delayed_burst_release_fraction": min(
            delayed_burst_release_fractions,
            default=1.0,
        ),
        "delayed_bursts": len(delayed_burst_starts),
        "maximum_inter_event_gap": max(inter_event_gaps, default=0),
        "maximum_root_scaled_inter_event_gap": (
            max(inter_event_gaps, default=0) * math.sqrt(alpha)
        ),
        "maximum_projection_potential_ratio": max(projection_ratios, default=0.0),
        "maximum_companion_held_ratio": max(companion_held_ratios, default=0.0),
        "maximum_companion_projection_ratio": max(companion_projection_ratios, default=0.0),
        "minimum_companion_event_slack": min(companion_event_slacks, default=0.0),
        "minimum_event_debt_slack": min(event_debt_slacks, default=0.0),
        "minimum_scratch_residual_at_publication": min(publication_scratch_minima, default=0.0),
        "initial_minimum_subgradient_norm": minimum_subgradient_norms[0],
        "final_minimum_subgradient_norm": minimum_subgradient_norms[-1],
        "maximum_minimum_subgradient_growth": max(
            (
                later / earlier
                for earlier, later in zip(
                    minimum_subgradient_norms,
                    minimum_subgradient_norms[1:],
                )
                if earlier > 1.0e-30
            ),
            default=0.0,
        ),
        "all_batches_ready_at_publication": all(
            value >= -1.0e-12 for value in publication_scratch_minima
        ),
        "scratch_size": len(scratch),
        "scratch_volume": float(degrees[scratch].sum()),
        "volume_work": volume_work,
        "terminated": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260831)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    structured: list[dict[str, object]] = []
    for name, adjacency in [
        ("lollipop-4-128", lollipop(4, 128)),
        ("alternating-16-16", alternating_layers(16, 16)),
    ]:
        for alpha in [1.0e-2, 1.0e-3, 1.0e-4]:
            rho = 1.0e-4 / adjacency[0].sum()
            result = run_two_mask(adjacency, alpha, rho)
            result.update({"name": name, "alpha": alpha, "rho": rho})
            structured.append(result)

    random_records: list[dict[str, object]] = []
    for trial in range(args.trials):
        vertex_count = int(rng.integers(5, 45))
        probability = float(10.0 ** rng.uniform(-2.2, -0.5))
        adjacency = random_connected_graph(rng, vertex_count, probability)
        alpha = float(10.0 ** rng.uniform(-4.0, -0.35))
        rho = float(10.0 ** rng.uniform(-6.0, -0.2) / adjacency[0].sum())
        result = run_two_mask(
            adjacency,
            alpha,
            rho,
            maximum_iterations=3_000,
        )
        result.update(
            {
                "trial": trial,
                "vertices": vertex_count,
                "alpha": alpha,
                "rho": rho,
                "extra_edge_probability": probability,
            }
        )
        random_records.append(result)

    delayed_records: list[dict[str, object]] = []
    delayed_adaptive_records: list[dict[str, object]] = []
    delayed_graph = delayed_publication_graph()
    for alpha in [1.0e-2, 3.0e-3, 1.0e-3, 3.0e-4, 1.0e-4]:
        rho = 1.0e-5 / delayed_graph[0].sum()
        result = run_projected_estimate_nag(
            delayed_graph,
            alpha,
            rho,
            maximum_iterations=6_000,
            publication_tolerance=1.0e-13,
        )
        result.update({"alpha": alpha, "rho": rho})
        delayed_records.append(result)
        adaptive_result = run_projected_estimate_nag(
            delayed_graph,
            alpha,
            rho,
            maximum_iterations=6_000,
            publication_tolerance=1.0e-13,
            adaptive_gap=True,
        )
        adaptive_result.update({"alpha": alpha, "rho": rho})
        delayed_adaptive_records.append(adaptive_result)

    stress_graph = green_band_stress_graph()
    stress_alpha = 1.0e-3
    stress_rho = 1.6294035977595616e-6 / stress_graph[0].sum()
    stress_result = run_projected_estimate_nag(
        stress_graph,
        stress_alpha,
        stress_rho,
        maximum_iterations=3_000,
        publication_tolerance=1.0e-13,
    )
    stress_result.update({"alpha": stress_alpha, "rho": stress_rho})

    print(
        json.dumps(
            {
                "warning": "empirical candidate audit, not a theorem",
                "structured": structured,
                "delayed_projected_publication": delayed_records,
                "delayed_gap_adaptive_publication": delayed_adaptive_records,
                "green_band_stress": stress_result,
                "random_summary": {
                    "trials": args.trials,
                    "maximum_wait": max(int(record["maximum_wait"]) for record in random_records),
                    "maximum_scaled_iterations": max(
                        float(record["scaled_iterations"]) for record in random_records
                    ),
                    "all_terminated": all(bool(record["terminated"]) for record in random_records),
                    "all_batches_ready_at_publication": all(
                        bool(record["all_batches_ready_at_publication"])
                        for record in random_records
                    ),
                    "maximum_history_deficit_at_publication": max(
                        float(record["maximum_history_deficit_at_publication"])
                        for record in random_records
                    ),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
