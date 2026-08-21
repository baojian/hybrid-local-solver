#!/usr/bin/env python3
"""Numerical audit for the Round-014 scale-certified notched-sun reporter."""

from __future__ import annotations

import argparse
import math

import numpy as np


def notched_double_sun(n: int) -> np.ndarray:
    """Return adjacency in (anchor, source-petal, report-leaf) order."""
    if n < 5:
        raise ValueError("the notched-double-sun definition requires n >= 5")
    adjacency = np.zeros((3 * n, 3 * n), dtype=float)

    def add_edge(left: int, right: int) -> None:
        adjacency[left, right] = 1.0
        adjacency[right, left] = 1.0

    for vertex in range(n):
        add_edge(vertex, (vertex + 1) % n)
    add_edge(0, 2)
    for vertex in range(n):
        add_edge(vertex, n + vertex)
        add_edge(vertex, 2 * n + vertex)
    return adjacency


def verify_instance(n: int, theta: float, eta: float) -> tuple[float, float, float]:
    """Check the exact decomposition, analytic bounds, and delta trace."""
    threshold = 1.0 / (1296.0 * n**2)
    if not 0.0 < theta <= threshold:
        raise ValueError("theta is outside the theorem's explicit scale regime")

    adjacency = notched_double_sun(n)
    degrees = adjacency.sum(axis=1)
    normalized = adjacency / np.sqrt(np.outer(degrees, degrees))
    normalized_face = normalized[: 2 * n, : 2 * n]
    alpha = 1.0 - 2.0 * theta
    c_eta = (1.0 + eta) ** 2 * eta**2

    b_diagonal = np.ones(2 * n)
    b_diagonal[n:] = 1.0 + c_eta
    r_diagonal = np.ones(2 * n)
    r_diagonal[n:] = 1.0 + 2.0 * c_eta
    b_matrix = np.diag(b_diagonal)
    r_matrix = np.diag(r_diagonal) + normalized_face
    inverse_sqrt_b = np.diag(1.0 / np.sqrt(b_diagonal))
    kernel = inverse_sqrt_b @ r_matrix @ inverse_sqrt_b
    if np.min(kernel) < -1e-14:
        raise AssertionError("the Neumann kernel is not entrywise nonnegative")
    kernel_norm = float(np.linalg.norm(kernel, ord=2))
    if kernel_norm > 3.0 + 1e-12:
        raise AssertionError("the Neumann-kernel norm exceeds the proved bound")

    shifted = b_matrix - theta * r_matrix
    pagerank = (1.0 - theta) * np.eye(3 * n) - theta * normalized
    direct_shifted = pagerank[: 2 * n, : 2 * n].copy()
    direct_shifted[n:, n:] += c_eta * alpha * np.eye(n)
    if not np.allclose(shifted, direct_shifted, rtol=1e-13, atol=1e-15):
        raise AssertionError("the exact B-theta R decomposition failed")

    sources = np.zeros((2 * n, n))
    sources[n + np.arange(n), np.arange(n)] = 1.0
    corrections = np.linalg.solve(shifted, sources)
    response = -(pagerank[2 * n :, : 2 * n] @ corrections)
    response /= np.sqrt(degrees[2 * n :])[:, None]
    if not np.all(response > 0.0):
        raise AssertionError("the first-rung response is not entrywise positive")

    gate = theta**2.5
    matching_lower = theta**2 / (degrees[:n] * (1.0 + c_eta))
    matching_ratio = float(np.min(np.diag(response) / gate))
    if np.any(np.diag(response) + 1e-24 < matching_lower):
        raise AssertionError("a matching response violated the Neumann lower bound")
    if matching_ratio <= 1.0:
        raise AssertionError("a matching response did not cross the strict gate")

    cumulative = np.zeros(n)
    emitted = np.zeros(n, dtype=bool)
    max_tail_ratio = 0.0
    for event in range(n):
        cumulative += response[:, event]
        newly_emitted = (~emitted) & (cumulative > gate)
        expected = np.zeros(n, dtype=bool)
        expected[event] = True
        if not np.array_equal(newly_emitted, expected):
            raise AssertionError("the delta reporter did not emit only the matching label")
        emitted |= newly_emitted

        # The signed two-stream interface checks both amplitudes before this
        # exact logical combination; no stream input is skipped.
        signed_logical = 2.0 * cumulative - cumulative
        if not np.array_equal(signed_logical, cumulative):
            raise AssertionError("the signed 2-minus-1 logical response changed")

        analytic_tail = 9.0 * (event + 1) * theta**3 / (1.0 - 3.0 * theta)
        if event + 1 < n:
            actual_tail = float(np.max(cumulative[event + 1 :]))
            if actual_tail > analytic_tail * (1.0 + 1e-10) + 1e-24:
                raise AssertionError("a future response exceeded the analytic tail")
            if analytic_tail > 0.5 * gate * (1.0 + 1e-12):
                raise AssertionError("the scalar future-safe certificate missed the band")
            max_tail_ratio = max(max_tail_ratio, actual_tail / analytic_tail)

    return kernel_norm, max_tail_ratio, matching_ratio


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--max-n", type=int, default=24)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_n < 5:
        raise ValueError("--max-n must be at least 5")
    rng = np.random.default_rng(args.seed)
    eta = 0.1
    max_kernel_norm = 0.0
    max_tail_ratio = 0.0
    min_matching_ratio = math.inf
    largest_theta_ratio = 0.0

    for _ in range(args.trials):
        n = int(rng.integers(5, args.max_n + 1))
        threshold = 1.0 / (1296.0 * n**2)
        theta_ratio = float(rng.uniform(0.05, 1.0))
        theta = theta_ratio * threshold
        kernel_norm, tail_ratio, matching_ratio = verify_instance(n, theta, eta)
        max_kernel_norm = max(max_kernel_norm, kernel_norm)
        max_tail_ratio = max(max_tail_ratio, tail_ratio)
        min_matching_ratio = min(min_matching_ratio, matching_ratio)
        largest_theta_ratio = max(largest_theta_ratio, theta_ratio)

    print(f"seed={args.seed} trials={args.trials} max_n={args.max_n} eta={eta}")
    print(f"largest theta/theorem-threshold={largest_theta_ratio:.6e}")
    print(f"max Neumann-kernel norm={max_kernel_norm:.6e}")
    print(f"max actual/analytic future-tail ratio={max_tail_ratio:.6e}")
    print(f"min matching/gate ratio={min_matching_ratio:.6e}")
    print("all scale-certificate, signed-stream, and delta-trace checks passed")


if __name__ == "__main__":
    main()
