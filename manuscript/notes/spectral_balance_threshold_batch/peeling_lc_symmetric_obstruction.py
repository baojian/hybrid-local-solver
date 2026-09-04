#!/usr/bin/env python3
"""Reproduce the symmetric five-vertex obstruction for one-pass PeelingLC.

The graph is K_{3,2} plus the edge joining the two degree-four vertices.  The
source is one of those degree-four vertices.  Symmetry reduces the late-time
homogeneous recurrence to the three orbits (leaf, source, other hub).

This is a deterministic dense audit, not a sparse implementation.  It reports
zero-start stopping times for exact-box and one-pass peeling safeguards and
solves the stable one-event projective eigenray by a dependency-free damped
Newton method.  The limiting constants are

    lambda = 1 - 7 alpha + O(alpha^(3/2)),
    tau = sqrt(alpha) + O(alpha),

which explain the observed Theta(1/alpha) peeling tail.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np

from safe_box_linear_coupling_experiment import run_candidate


EDGES = ((0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4))
SOURCE = 3
RHO_FRACTION = 0.2


def adjacency() -> np.ndarray:
    matrix = np.zeros((5, 5))
    for left, right in EDGES:
        matrix[left, right] = 1.0
        matrix[right, left] = 1.0
    return matrix


def orbit_operator(root: float) -> np.ndarray:
    """Return Q on values constant on the three symmetry orbits."""

    diagonal = (1.0 + root * root) / 2.0
    half_walk = (1.0 - root * root) / 2.0
    leaf_hub = half_walk / (2.0 * math.sqrt(2.0))
    hub_hub = half_walk / 4.0
    return np.array(
        [
            [diagonal, -leaf_hub, -leaf_hub],
            [-3.0 * leaf_hub, diagonal, -hub_hub],
            [-3.0 * leaf_hub, -hub_hub, diagonal],
        ]
    )


def ray_residual(unknown: np.ndarray, root: float) -> np.ndarray:
    """Invariant-ray equations for the stable source-freezes-first regime."""

    leaf_error, other_error, leaf_velocity, source_velocity, other_velocity, rate = (
        unknown
    )
    error = np.array([leaf_error, 1.0, other_error])
    velocity = np.array([leaf_velocity, source_velocity, other_velocity])
    operator = orbit_operator(root)
    residual = operator @ error
    trial_increment = root * velocity / (1.0 + root)
    pressure = operator @ trial_increment
    freeze_time = residual[1] / pressure[1]
    safe_increment = trial_increment.copy()
    safe_increment[1] *= freeze_time
    final_slack = residual - operator @ safe_increment
    next_error = error - safe_increment - final_slack
    next_velocity = (1.0 - root) * (
        velocity - safe_increment + final_slack / root
    )
    return np.concatenate((next_error - rate * error, next_velocity - rate * velocity))


def solve_ray(initial: np.ndarray, root: float) -> tuple[np.ndarray, float]:
    """Solve the six homogeneous ray equations with damped finite-difference Newton."""

    state = initial.copy()
    for _ in range(100):
        value = ray_residual(state, root)
        norm = float(np.linalg.norm(value, ord=np.inf))
        if norm <= 2.0e-12:
            return state, norm
        jacobian = np.empty((6, 6))
        for column in range(6):
            step = 1.0e-6 * max(1.0, abs(float(state[column])))
            plus = state.copy()
            minus = state.copy()
            plus[column] += step
            minus[column] -= step
            jacobian[:, column] = (
                ray_residual(plus, root) - ray_residual(minus, root)
            ) / (2.0 * step)
        direction = np.linalg.lstsq(jacobian, -value, rcond=None)[0]
        best = state
        best_norm = norm
        for power in range(16):
            candidate = state + direction / (2**power)
            candidate_norm = float(np.linalg.norm(ray_residual(candidate, root)))
            if candidate_norm < best_norm:
                best = candidate
                best_norm = candidate_norm
            if candidate_norm < norm:
                break
        state = best
    return state, float(np.linalg.norm(ray_residual(state, root), ord=np.inf))


def projective_map(state: np.ndarray, root: float) -> np.ndarray:
    """Apply the stable event map and renormalize the source error to one."""

    leaf_error, other_error, leaf_velocity, source_velocity, other_velocity = state
    error = np.array([leaf_error, 1.0, other_error])
    velocity = np.array([leaf_velocity, source_velocity, other_velocity])
    operator = orbit_operator(root)
    residual = operator @ error
    trial_increment = root * velocity / (1.0 + root)
    freeze_time = residual[1] / (operator @ trial_increment)[1]
    safe_increment = trial_increment.copy()
    safe_increment[1] *= freeze_time
    final_slack = residual - operator @ safe_increment
    next_error = error - safe_increment - final_slack
    next_velocity = (1.0 - root) * (
        velocity - safe_increment + final_slack / root
    )
    scale = next_error[1]
    return np.array(
        [
            next_error[0] / scale,
            next_error[2] / scale,
            next_velocity[0] / scale,
            next_velocity[1] / scale,
            next_velocity[2] / scale,
        ]
    )


def projective_spectral_radius(solution: np.ndarray, root: float) -> float:
    """Return a finite-difference stability diagnostic for the ray."""

    state = solution[:5]
    jacobian = np.empty((5, 5))
    for column in range(5):
        step = 1.0e-6 * max(1.0, abs(float(state[column])))
        plus = state.copy()
        minus = state.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (
            projective_map(plus, root) - projective_map(minus, root)
        ) / (2.0 * step)
    return float(np.max(np.abs(np.linalg.eigvals(jacobian))))


def ray_report(solution: np.ndarray, root: float, equation_error: float) -> dict[str, float]:
    leaf_error, other_error, leaf_velocity, source_velocity, other_velocity, rate = (
        solution
    )
    error = np.array([leaf_error, 1.0, other_error])
    velocity = np.array([leaf_velocity, source_velocity, other_velocity])
    operator = orbit_operator(root)
    residual = operator @ error
    trial_increment = root * velocity / (1.0 + root)
    pressure = operator @ trial_increment
    freeze_time = residual[1] / pressure[1]
    safe_increment = trial_increment.copy()
    safe_increment[1] *= freeze_time
    final_slack = residual - operator @ safe_increment
    return {
        "alpha": root * root,
        "root": root,
        "equation_error": equation_error,
        "projective_spectral_radius": projective_spectral_radius(solution, root),
        "one_minus_rate_over_alpha": (1.0 - rate) / (root * root),
        "freeze_time_over_root": freeze_time / root,
        "leaf_error": leaf_error,
        "other_hub_error": other_error,
        "leaf_velocity_over_root": leaf_velocity / root,
        "source_velocity": source_velocity,
        "other_hub_velocity_over_root": other_velocity / root,
        "leaf_final_slack_over_root_cubed": final_slack[0] / root**3,
        "source_final_slack_over_alpha": final_slack[1] / root**2,
        "other_final_slack_over_root_cubed": final_slack[2] / root**3,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alphas", default=".03,.01,.003,.001,.0003,.0001")
    parser.add_argument("--relative-tolerance", type=float, default=1.0e-2)
    parser.add_argument("--maximum-rounds", type=int, default=100000)
    args = parser.parse_args()
    alphas = tuple(float(value) for value in args.alphas.split(","))
    graph = adjacency()
    stopping = []
    for alpha in alphas:
        row: dict[str, float | int] = {"alpha": alpha}
        for mode in ("box", "peel"):
            result = run_candidate(
                graph,
                alpha,
                RHO_FRACTION,
                SOURCE,
                mode,
                args.relative_tolerance,
                args.maximum_rounds,
            )
            rounds = int(result["rounds"])
            row[f"{mode}_rounds"] = rounds
            row[f"{mode}_alpha_times_rounds"] = alpha * rounds
            row[f"{mode}_root_alpha_times_rounds"] = math.sqrt(alpha) * rounds
        stopping.append(row)

    ray_state = np.array(
        [1.0 / math.sqrt(2.0), 1.0, 0.04, 3.3, 0.06, 0.999]
    )
    rays = []
    for root in (0.03, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005):
        ray_state, error = solve_ray(ray_state, root)
        if error > 5.0e-10:
            raise AssertionError(f"projective ray solve failed at root={root}: {error}")
        rays.append(ray_report(ray_state, root, error))

    print(
        json.dumps(
            {
                "warning": "dense deterministic audit; asymptotic constants are not by themselves an attraction proof",
                "edges": EDGES,
                "source": SOURCE,
                "rho_fraction": RHO_FRACTION,
                "relative_tolerance": args.relative_tolerance,
                "stopping_times": stopping,
                "stable_projective_rays": rays,
                "predicted_limits": {
                    "one_minus_rate_over_alpha": 7.0,
                    "freeze_time_over_root": 1.0,
                    "leaf_error": 1.0 / math.sqrt(2.0),
                    "other_hub_error": 1.0,
                    "leaf_velocity_over_root": 7.0 / math.sqrt(2.0),
                    "source_velocity": 3.5,
                    "other_hub_velocity_over_root": 7.0,
                    "source_final_slack_over_alpha": 3.5,
                    "scaled_leaf_final_slack_over_root_cubed": 14.0,
                    "other_final_slack_over_root_cubed": 14.0,
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
