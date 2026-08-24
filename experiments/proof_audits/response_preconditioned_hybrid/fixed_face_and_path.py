#!/usr/bin/env python3
"""Seeded numerical checks for the Round-012 fixed-face and path claims."""

from __future__ import annotations

import argparse
import math

import numpy as np


def pagerank_matrix(adjacency: np.ndarray, alpha: float) -> tuple[np.ndarray, np.ndarray]:
    degrees = adjacency.sum(axis=1)
    if np.any(degrees <= 0):
        raise ValueError("the check requires a graph without isolated vertices")
    normalized = adjacency / np.sqrt(np.outer(degrees, degrees))
    identity = np.eye(adjacency.shape[0])
    matrix = alpha * identity + 0.5 * (1.0 - alpha) * (identity - normalized)
    return matrix, degrees


def random_connected_graph(rng: np.random.Generator, n: int) -> np.ndarray:
    adjacency = np.zeros((n, n), dtype=float)
    for vertex in range(n - 1):
        adjacency[vertex, vertex + 1] = 1.0
        adjacency[vertex + 1, vertex] = 1.0
    for left in range(n):
        for right in range(left + 2, n):
            if rng.random() < 0.2:
                adjacency[left, right] = 1.0
                adjacency[right, left] = 1.0
    return adjacency


def shifted_ladder(alpha: float, eta: float) -> list[float]:
    current = eta * math.sqrt(alpha)
    shifts: list[float] = []
    while current < 1.0 / eta:
        current *= 1.0 + eta
        shifts.append(current * current)
    return shifts


def log_cosh(value: float) -> float:
    magnitude = abs(value)
    return magnitude - math.log(2.0) + math.log1p(math.exp(-2.0 * magnitude))


def chebyshev_residual_action(
    matrix: np.ndarray,
    vector: np.ndarray,
    steps: int,
    lower: float,
    upper: float,
) -> np.ndarray:
    if steps == 0:
        return vector.copy()
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    midpoint = 0.5 * (upper + lower)
    halfwidth = 0.5 * (upper - lower)
    mapped = np.clip((midpoint - eigenvalues) / halfwidth, -1.0, 1.0)
    numerator = np.cos(steps * np.arccos(mapped))
    denominator_log = log_cosh(steps * math.acosh(midpoint / halfwidth))
    ratios = numerator * math.exp(-denominator_log)
    return eigenvectors @ (ratios * (eigenvectors.T @ vector))


def required_steps(kappa: float, residual_norm: float, target: float) -> int:
    if residual_norm == 0.0:
        return 0
    theta = (math.sqrt(kappa) - 1.0) / (math.sqrt(kappa) + 1.0)
    if theta == 0.0:
        return 1
    ratio = 2.0 * residual_norm / target
    if ratio <= 1.0:
        return 0
    return math.ceil(math.log(ratio) / (-math.log(theta)))


def aggregate_flush_checks(seed: int, trials: int) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    max_energy_ratio = 0.0
    max_interval_ratio = 0.0
    max_residual_ratio = 0.0
    eta = 0.1

    for _ in range(trials):
        n = int(rng.integers(8, 15))
        adjacency = random_connected_graph(rng, n)
        alpha = float(10.0 ** rng.uniform(-3.0, -0.2))
        matrix, degrees = pagerank_matrix(adjacency, alpha)
        permutation = rng.permutation(n)
        face_size = int(rng.integers(3, n - 1))
        face = np.sort(permutation[:face_size])
        exterior = np.sort(permutation[face_size:])
        frontier_size = max(1, face_size // 3)
        frontier_local = np.arange(face_size - frontier_size, face_size)
        face_matrix = matrix[np.ix_(face, face)]
        shifts = shifted_ladder(alpha, eta)
        columns = 2
        aggregates: list[np.ndarray] = []

        for shift_index, _shift in enumerate(shifts):
            debt = np.zeros((face_size, columns), dtype=float)
            if shift_index % 4 == 0:
                mask = rng.random((face_size, columns)) < 0.35
                debt[mask] = rng.uniform(0.01, 1.0, size=int(mask.sum()))
            aggregates.append(debt)

        for column in range(columns):
            masses = [float(np.linalg.norm(debt[:, column])) for debt in aggregates]
            total_mass = sum(masses)
            if total_mass == 0.0:
                continue
            delta = 1.0e-6 * max(1.0, total_mass)
            exact = np.zeros(face_size)
            approximate = np.zeros(face_size)

            for shift, debt, mass in zip(shifts, aggregates, masses, strict=True):
                if mass == 0.0:
                    continue
                shifted = face_matrix.copy()
                shifted[frontier_local, frontier_local] += shift
                exact_part = np.linalg.solve(shifted, debt[:, column])
                exact += exact_part
                rung_delta = delta * mass / total_mass
                kappa = (1.0 + shift) / alpha
                steps = required_steps(kappa, mass, rung_delta * math.sqrt(alpha))
                residual = chebyshev_residual_action(
                    shifted,
                    debt[:, column],
                    steps,
                    alpha,
                    1.0 + shift,
                )
                residual_ratio = float(np.linalg.norm(residual)) / (rung_delta * math.sqrt(alpha))
                max_residual_ratio = max(max_residual_ratio, residual_ratio)
                approximate += np.linalg.solve(shifted, debt[:, column] - residual)

            error = exact - approximate
            energy_ratio = math.sqrt(float(error @ face_matrix @ error)) / delta
            max_energy_ratio = max(max_energy_ratio, energy_ratio)
            if exterior.size:
                dual_error = matrix[np.ix_(exterior, face)] @ error
                interval_ratio = (
                    float(np.max(np.abs(dual_error) / np.sqrt(degrees[exterior]))) / delta
                )
                max_interval_ratio = max(max_interval_ratio, interval_ratio)

        root_sum = sum(math.sqrt(1.0 + shift) for shift in shifts)
        shift_bound = len(shifts) + (1.0 + eta) ** 2 / eta**2
        if root_sum > shift_bound * (1.0 + 1.0e-12):
            raise AssertionError("geometric shift-sum bound failed")

    tolerance = 1.0 + 5.0e-8
    if max_residual_ratio > tolerance:
        raise AssertionError(f"Chebyshev residual ratio {max_residual_ratio} exceeds one")
    if max_energy_ratio > tolerance:
        raise AssertionError(f"summed energy ratio {max_energy_ratio} exceeds one")
    if max_interval_ratio > tolerance:
        raise AssertionError(f"normalized interval ratio {max_interval_ratio} exceeds one")
    return max_energy_ratio, max_interval_ratio, max_residual_ratio


def one_edge_scaling_check() -> list[tuple[float, int, float]]:
    eta = 0.1
    c_eta = (1.0 + eta) ** 2 * eta**2
    rows: list[tuple[float, int, float]] = []
    for alpha in (1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6):
        diagonal = 0.5 * (1.0 + alpha)
        off_diagonal = -0.5 * (1.0 - alpha)
        shift = c_eta * alpha
        matrix = np.array(
            [[diagonal, off_diagonal], [off_diagonal, diagonal + shift]],
            dtype=float,
        )
        kappa = (1.0 + shift) / alpha
        steps = required_steps(kappa, 1.0, 0.25)
        residual = chebyshev_residual_action(
            matrix,
            np.array([0.0, 1.0]),
            steps,
            alpha,
            1.0 + shift,
        )
        if float(np.linalg.norm(residual)) > 0.25 * (1.0 + 1.0e-9):
            raise AssertionError("one-edge factor-four residual check failed")
        rows.append((alpha, steps, math.sqrt(alpha) * steps))
    return rows


def path_family_check(alpha: float = 0.2) -> tuple[float, float]:
    smallest_rho = math.inf
    largest_rho = 0.0
    for n in range(4, 17):
        adjacency = np.zeros((n, n), dtype=float)
        for vertex in range(n - 1):
            adjacency[vertex, vertex + 1] = 1.0
            adjacency[vertex + 1, vertex] = 1.0
        matrix, degrees = pagerank_matrix(adjacency, alpha)
        load = np.zeros(n)
        load[0] = alpha
        thresholds: list[float] = []

        for last in range(n):
            face = np.arange(last + 1)
            principal = matrix[np.ix_(face, face)]
            zero_state = np.linalg.solve(principal, load[face])
            slope_state = np.linalg.solve(principal, alpha * np.sqrt(degrees[face]))
            for value, slope in zip(zero_state, slope_state, strict=True):
                if slope > 0.0:
                    thresholds.append(float(value / slope))
            if last < n - 1:
                boundary = last + 1
                zero_demand = -float(matrix[boundary, face] @ zero_state)
                demand_slope = -alpha * math.sqrt(degrees[boundary]) + float(
                    matrix[boundary, face] @ slope_state
                )
                if demand_slope < 0.0:
                    thresholds.append(zero_demand / (-demand_slope))

        rho = 0.5 * min(thresholds)
        if not rho > 0.0:
            raise AssertionError("failed to construct a positive path rho")
        smallest_rho = min(smallest_rho, rho)
        largest_rho = max(largest_rho, rho)

        for last in range(n):
            face = np.arange(last + 1)
            principal = matrix[np.ix_(face, face)]
            shifted_load = load[face] - alpha * rho * np.sqrt(degrees[face])
            state = np.linalg.solve(principal, shifted_load)
            if float(np.min(state)) <= 0.0:
                raise AssertionError("path restricted state lost strict positivity")
            if last < n - 1:
                boundary = last + 1
                demand = -alpha * rho * math.sqrt(degrees[boundary]) - float(
                    matrix[boundary, face] @ state
                )
                if demand <= 0.0:
                    raise AssertionError("path singleton boundary demand is not strict")
    return smallest_rho, largest_rho


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--trials", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    energy, interval, residual = aggregate_flush_checks(args.seed, args.trials)
    scaling = one_edge_scaling_check()
    rho_min, rho_max = path_family_check()
    print(f"seed={args.seed} trials={args.trials}")
    print(f"max ratios: energy={energy:.6f} interval={interval:.6f} residual={residual:.6f}")
    print("one-edge sqrt(alpha)*steps:")
    for alpha, steps, scaled in scaling:
        print(f"  alpha={alpha:.0e} steps={steps} scaled={scaled:.6f}")
    print(f"path rho range for n=4..16 at alpha=0.2: [{rho_min:.6e}, {rho_max:.6e}]")


if __name__ == "__main__":
    main()
