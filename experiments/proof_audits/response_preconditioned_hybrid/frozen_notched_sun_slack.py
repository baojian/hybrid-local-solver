#!/usr/bin/env python3
"""Numerical audit for the Round-013 frozen notched-sun slack-vector STOP."""

from __future__ import annotations

import argparse
import math

import numpy as np


def notched_double_sun(n: int) -> np.ndarray:
    """Return the adjacency matrix in (anchor, source-petal, report-leaf) order."""
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


def pagerank_matrix(adjacency: np.ndarray, alpha: float) -> tuple[np.ndarray, np.ndarray]:
    degrees = adjacency.sum(axis=1)
    normalized = adjacency / np.sqrt(np.outer(degrees, degrees))
    theta = 0.5 * (1.0 - alpha)
    matrix = (1.0 - theta) * np.eye(adjacency.shape[0]) - theta * normalized
    return matrix, degrees


def frozen_response(n: int, alpha: float, eta: float) -> tuple[np.ndarray, np.ndarray]:
    adjacency = notched_double_sun(n)
    matrix, degrees = pagerank_matrix(adjacency, alpha)
    face = np.arange(2 * n)
    frontier = np.arange(n, 2 * n)
    reports = np.arange(2 * n, 3 * n)
    shifted = matrix[np.ix_(face, face)].copy()
    c_eta = (1.0 + eta) ** 2 * eta**2
    shifted[frontier, frontier] += c_eta * alpha
    sources = np.zeros((2 * n, n), dtype=float)
    sources[frontier, np.arange(n)] = 1.0
    corrections = np.linalg.solve(shifted, sources)
    response = -(matrix[np.ix_(reports, face)] @ corrections) / np.sqrt(degrees[reports])[:, None]
    return response, degrees


def verify_trace(n: int, theta: float, eta: float) -> tuple[float, float, float]:
    alpha = 1.0 - 2.0 * theta
    response, degrees = frozen_response(n, alpha, eta)
    if not np.all(response > 0.0):
        raise AssertionError("the exact first-rung response is not entrywise positive")
    expected_degrees = np.full(n, 4.0)
    expected_degrees[[0, 2]] = 5.0
    if not np.array_equal(degrees[:n], expected_degrees):
        raise AssertionError("anchor degrees do not match the notched-double-sun definition")

    diagonal = np.diag(response)
    off_diagonal = response.copy()
    off_diagonal[np.arange(n), np.arange(n)] = 0.0
    gate = theta**2.5
    band = 0.5 * gate
    cumulative = np.zeros(n)
    emitted = np.zeros(n, dtype=bool)

    for event in range(n):
        cumulative += response[:, event]
        newly_emitted = (~emitted) & (cumulative > gate)
        expected = np.zeros(n, dtype=bool)
        expected[event] = True
        if not np.array_equal(newly_emitted, expected):
            raise AssertionError(
                f"event {event + 1} did not emit exactly its matching report label"
            )
        emitted |= newly_emitted
        if event + 1 < n:
            sleeping = ~emitted
            if np.any(cumulative[sleeping] > gate - band):
                raise AssertionError("an unreported label entered the transition band")

    c_eta = (1.0 + eta) ** 2 * eta**2
    leading = 1.0 / (degrees[:n] * (1.0 + c_eta))
    diagonal_ratio = float(np.max(np.abs(diagonal / theta**2 - leading)))
    off_ratio = float(np.max(off_diagonal) / theta**3)
    matching_margin = float(np.min(diagonal) / gate)
    return diagonal_ratio, off_ratio, matching_margin


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
    max_diagonal_error = 0.0
    max_off_ratio = 0.0
    min_matching_margin = math.inf
    largest_theta = 0.0

    for _ in range(args.trials):
        n = int(rng.integers(5, args.max_n + 1))
        # This range is small enough for the separated fixed-n regime at the
        # audited sizes while remaining far above underflow in binary64.
        theta = float(10.0 ** rng.uniform(-5.0, -3.5))
        diagonal_error, off_ratio, matching_margin = verify_trace(n, theta, eta)
        max_diagonal_error = max(max_diagonal_error, diagonal_error)
        max_off_ratio = max(max_off_ratio, off_ratio)
        min_matching_margin = min(min_matching_margin, matching_margin)
        largest_theta = max(largest_theta, theta)

    print(f"seed={args.seed} trials={args.trials} max_n={args.max_n} eta={eta}")
    print(f"largest vartheta={largest_theta:.6e}")
    print(f"max diagonal-leading error={max_diagonal_error:.6e}")
    print(f"max off/vartheta^3={max_off_ratio:.6e}")
    print(f"min matching/gate margin={min_matching_margin:.6e}")
    print("all dense-response and one-new-delta-label checks passed")


if __name__ == "__main__":
    main()
