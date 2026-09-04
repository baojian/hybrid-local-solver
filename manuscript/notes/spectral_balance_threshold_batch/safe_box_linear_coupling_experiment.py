#!/usr/bin/env python3
"""Audit the persistent-estimate safe-box linear-coupling recurrence.

Unlike ``safe_box_gradient_experiment.py``, this recurrence does not reset the
estimate state after safeguarding the extrapolate.  Exact safe-box clipping
then preserves the standard accelerated potential even when the support
grows.  One-pass peeling obeys the same inequality with the explicit additive
term ``(1-s**2) zeta``.  Dense solves/full residuals are audit oracles only.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math

import networkx as nx
import numpy as np

from retained_prox_experiment import exact_obstacle_solution, normalized_operator


def safe_trial(
    matrix: np.ndarray,
    load: np.ndarray,
    current: np.ndarray,
    trial: np.ndarray,
    mode: str,
) -> tuple[np.ndarray, float]:
    support = np.flatnonzero(current > 1.0e-14)
    safe = np.zeros_like(current)
    if not len(support):
        return safe, 0.0
    block = matrix[np.ix_(support, support)]
    direction = trial[support] - current[support]
    if np.min(direction) < -2.0e-10:
        raise AssertionError("trial is below the current lower state")
    raw_residual = load[support] - block @ trial[support]

    if mode == "box":
        correction = exact_obstacle_solution(block, -raw_residual)
        safe[support] = trial[support] - correction
    else:
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
    correction = trial[support] - safe[support]
    if np.min(safe[support] - current[support]) < -3.0e-9:
        raise AssertionError("safe point fell below current")
    if np.min(trial[support] - safe[support]) < -3.0e-9:
        raise AssertionError("safe point left its box")
    if np.min(slack) < -3.0e-9:
        raise AssertionError("safe point is not a subsolution")
    zeta = max(0.0, float(correction @ slack))
    if mode == "box" and zeta > 3.0e-9:
        raise AssertionError("exact box complementarity failed")
    return safe, zeta


def run_candidate(
    adjacency: np.ndarray,
    alpha: float,
    rho_fraction: float,
    source: int,
    mode: str,
    relative_tolerance: float,
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
    tolerance = relative_tolerance * initial_gap
    root = math.sqrt(alpha)

    current = np.zeros(len(adjacency))
    estimate = np.zeros(len(adjacency))
    maximum_exact_contraction_ratio = 0.0
    maximum_peeling_remainder = -math.inf
    maximum_zeta_over_energy = 0.0
    maximum_energy_growth = 0.0
    maximum_zeta_over_objective_decrease = 0.0
    total_zeta = 0.0
    peeling_rounds = 0
    total_inner_passes = 0
    maximum_inner_passes = 0
    volume_work = 0.0
    support_events = 0

    def objective(state: np.ndarray) -> float:
        return float(0.5 * state @ matrix @ state - load @ state)

    def energy(primal: np.ndarray, auxiliary: np.ndarray) -> float:
        return objective(primal) - optimum_value + 0.5 * alpha * float(
            np.linalg.norm(auxiliary - optimum) ** 2
        )

    for round_index in range(maximum_rounds):
        old_energy = energy(current, estimate)
        trial = (current + root * estimate) / (1.0 + root)
        if np.min(trial - current) < -3.0e-9:
            raise AssertionError("linear-coupling trial is not above current")
        trial_mode = "box" if mode == "box" else "peel"
        safe, zeta = safe_trial(matrix, load, current, trial, trial_mode)
        inner_passes = 1
        if mode == "refine":
            while True:
                accepted = safe - current
                box_credit = 0.5 * float(accepted @ matrix @ accepted)
                box_credit += 0.5 * root * alpha * float(
                    np.linalg.norm(estimate - safe) ** 2
                )
                if (1.0 + root) * zeta <= box_credit + 2.0e-13 * max(
                    1.0, old_energy
                ):
                    break
                if inner_passes >= 10000:
                    raise RuntimeError("iterated peeling did not meet the box certificate")
                safe, zeta = safe_trial(matrix, load, safe, trial, "peel")
                inner_passes += 1
        total_inner_passes += inner_passes
        maximum_inner_passes = max(maximum_inner_passes, inner_passes)
        full_gradient = matrix @ safe - load
        active = set(map(int, np.flatnonzero(current > 1.0e-13)))
        active.update(map(int, np.flatnonzero(full_gradient < -1.0e-13)))
        rows = np.array(sorted(active), dtype=int)
        gradient = np.zeros(len(adjacency))
        if len(rows):
            gradient[rows] = full_gradient[rows]
        if len(rows) and np.max(gradient[rows]) > 3.0e-9:
            raise AssertionError("an included gradient is positive")
        if np.min(full_gradient - gradient) < -3.0e-9:
            raise AssertionError("an omitted gradient is negative")

        next_current = safe - gradient
        next_estimate = (
            (1.0 - root) * estimate
            + root * safe
            - gradient / root
        )
        if np.min(next_estimate - next_current) < -5.0e-9:
            raise AssertionError("estimate fell below primal")
        next_support = set(map(int, np.flatnonzero(next_current > 1.0e-13)))
        if not next_support.issubset(optimum_support):
            raise AssertionError("safe support left exact support")
        next_residual = load - matrix @ next_current
        if next_support:
            support_rows = np.array(sorted(next_support), dtype=int)
            if np.min(next_residual[support_rows]) < -5.0e-9:
                raise AssertionError("next primal is not a subsolution")

        new_energy = energy(next_current, next_estimate)
        objective_decrease = objective(current) - objective(next_current)
        stable_energy = old_energy > 1.0e-12 * max(1.0, initial_gap)
        exact_ratio = new_energy / max((1.0 - root) * old_energy, 1.0e-300)
        remainder = new_energy - (
            (1.0 - root) * old_energy + (1.0 - root * root) * zeta
        )
        if stable_energy:
            maximum_exact_contraction_ratio = max(
                maximum_exact_contraction_ratio, exact_ratio
            )
        maximum_peeling_remainder = max(maximum_peeling_remainder, remainder)
        maximum_zeta_over_energy = max(
            maximum_zeta_over_energy, zeta / max(old_energy, 1.0e-300)
        )
        maximum_energy_growth = max(
            maximum_energy_growth, new_energy / max(old_energy, 1.0e-300)
        )
        if zeta > 1.0e-18:
            peeling_rounds += 1
            maximum_zeta_over_objective_decrease = max(
                maximum_zeta_over_objective_decrease,
                zeta / max(objective_decrease, 1.0e-300),
            )
        if mode in ("box", "refine") and stable_energy and exact_ratio > 1.0 + 2.0e-7:
            raise AssertionError(
                "certified safe-box accelerated contraction failed: "
                f"round={round_index + 1}, ratio={exact_ratio}, "
                f"old_energy={old_energy}, new_energy={new_energy}, zeta={zeta}"
            )
        if remainder > 2.0e-8 * max(1.0, old_energy):
            raise AssertionError("peeling additive-potential inequality failed")
        total_zeta += zeta
        support_events += len(next_support - set(map(int, np.flatnonzero(current > 1.0e-13))))
        if next_support:
            volume_work += float(np.sum(degrees[np.array(sorted(next_support), dtype=int)]))

        certificate = 0.5 * float(np.max(np.maximum(next_residual, 0.0) / sqrt_degrees))
        current, estimate = next_current, next_estimate
        if certificate <= tolerance:
            return {
                "rounds": round_index + 1,
                "normalized_rounds": (round_index + 1) * root,
                "objective_gap": objective(current) - optimum_value,
                "certificate": certificate,
                "maximum_exact_contraction_ratio": maximum_exact_contraction_ratio,
                "maximum_peeling_remainder": maximum_peeling_remainder,
                "maximum_zeta_over_energy": maximum_zeta_over_energy,
                "maximum_energy_growth": maximum_energy_growth,
                "maximum_zeta_over_objective_decrease": (
                    maximum_zeta_over_objective_decrease
                ),
                "total_zeta": total_zeta,
                "peeling_rounds": peeling_rounds,
                "total_inner_passes": total_inner_passes,
                "maximum_inner_passes": maximum_inner_passes,
                "support_events": support_events,
                "final_support_size": len(optimum_support),
                "volume_work": volume_work,
            }
    raise RuntimeError("linear-coupling safe-box audit exceeded round limit")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=5, choices=(2, 3, 4, 5, 6))
    parser.add_argument(
        "--mode", choices=("box", "peel", "refine", "both", "all"), default="both"
    )
    parser.add_argument("--alphas", default=".3,.1,.03,.01,.003")
    parser.add_argument("--rho-fractions", default=".05,.2,.5,.8")
    parser.add_argument("--relative-tolerance", type=float, default=1.0e-8)
    parser.add_argument("--maximum-rounds", type=int, default=20000)
    args = parser.parse_args()
    if args.mode == "both":
        modes = ("box", "peel")
    elif args.mode == "all":
        modes = ("box", "peel", "refine")
    else:
        modes = (args.mode,)
    alphas = tuple(float(value) for value in args.alphas.split(","))
    rho_fractions = tuple(float(value) for value in args.rho_fractions.split(","))
    graphs = [
        graph
        for graph in nx.graph_atlas_g()
        if len(graph) == args.vertices and nx.is_connected(graph)
    ]
    extrema: dict[str, dict[str, object]] = {}
    cases = 0
    for graph_index, graph in enumerate(graphs):
        adjacency = nx.to_numpy_array(graph, nodelist=range(args.vertices))
        witness_base = {"graph_index": graph_index, "edges": list(map(list, graph.edges()))}
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
                **witness_base,
                "source": source,
                "alpha": alpha,
                "rho_fraction": rho_fraction,
                "mode": mode,
            }
            for key in (
                "normalized_rounds",
                "maximum_exact_contraction_ratio",
                "maximum_peeling_remainder",
                "maximum_zeta_over_energy",
                "maximum_energy_growth",
                "maximum_zeta_over_objective_decrease",
                "total_zeta",
                "peeling_rounds",
                "total_inner_passes",
                "maximum_inner_passes",
            ):
                if key not in extrema or float(result[key]) > float(extrema[key]["value"]):
                    extrema[key] = {"value": result[key], **witness}
    print(
        json.dumps(
            {
                "warning": "finite dense audit; exact box solve is not charged",
                "vertices": args.vertices,
                "connected_graphs": len(graphs),
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
