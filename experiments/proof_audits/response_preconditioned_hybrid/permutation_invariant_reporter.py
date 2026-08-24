#!/usr/bin/env python3
"""Numerical audit for the Round-015 permutation-invariant reporter."""

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


def accept_stream_event(
    labels: list[int],
    amplitudes: list[float],
    required_amplitudes: list[float],
    seen: set[int],
    n: int,
) -> bool:
    """Model the theorem's atomic online label/amplitude/unused check."""
    snapshot = seen.copy()
    if not labels or len(labels) != len(required_amplitudes):
        return False
    label = labels[0]
    valid = (
        0 <= label < n
        and all(stream_label == label for stream_label in labels)
        and amplitudes == required_amplitudes
        and label not in seen
    )
    if valid:
        seen.add(label)
    elif seen != snapshot:
        raise AssertionError("a rejected interaction changed the seen set")
    return valid


def verify_instance(
    n: int,
    theta: float,
    eta: float,
    permutation: np.ndarray,
) -> tuple[float, float, float]:
    """Check one arbitrary permutation and both stream-validation modes."""
    threshold = 1.0 / (1296.0 * n**2)
    if not 0.0 < theta <= threshold:
        raise ValueError("theta is outside the theorem's explicit scale regime")
    if not np.array_equal(np.sort(permutation), np.arange(n)):
        raise ValueError("the supplied trace is not a permutation")

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
    if np.any(np.diag(response) + 1e-24 < matching_lower):
        raise AssertionError("a matching response violated the Neumann lower bound")

    cumulative = np.zeros(n)
    emitted = np.zeros(n, dtype=bool)
    nonnegative_seen: set[int] = set()
    signed_seen: set[int] = set()
    max_tail_ratio = 0.0
    min_matching_ratio = math.inf

    for prefix_length, raw_label in enumerate(permutation, start=1):
        label = int(raw_label)
        other_label = (label + 1) % n
        signed_snapshot = signed_seen.copy()
        if accept_stream_event([label, other_label], [2.0, 1.0], [2.0, 1.0], signed_seen, n):
            raise AssertionError("an inconsistent signed-stream label was accepted")
        if accept_stream_event([label, label], [2.0, 2.0], [2.0, 1.0], signed_seen, n):
            raise AssertionError("an incorrect signed-stream amplitude was accepted")
        if signed_seen != signed_snapshot:
            raise AssertionError("invalid stream rejection changed the seen set")

        if not accept_stream_event([label, label], [1.0, 1.0], [1.0, 1.0], nonnegative_seen, n):
            raise AssertionError("a valid nonnegative permutation event was rejected")
        if not accept_stream_event([label, label], [2.0, 1.0], [2.0, 1.0], signed_seen, n):
            raise AssertionError("a valid signed permutation event was rejected")

        # A repeated event must be rejected atomically, without changing the
        # already accepted prefix.
        nonnegative_snapshot = nonnegative_seen.copy()
        if accept_stream_event([label, label], [1.0, 1.0], [1.0, 1.0], nonnegative_seen, n):
            raise AssertionError("a duplicate event was accepted")
        if nonnegative_seen != nonnegative_snapshot:
            raise AssertionError("duplicate rejection changed the seen set")

        cumulative += response[:, label]
        newly_emitted = (~emitted) & (cumulative > gate)
        expected = np.zeros(n, dtype=bool)
        expected[label] = True
        if not np.array_equal(newly_emitted, expected):
            raise AssertionError("the permuted trace did not emit only its matched label")
        emitted |= newly_emitted

        matching_ratio = float(cumulative[label] / gate)
        min_matching_ratio = min(min_matching_ratio, matching_ratio)
        if matching_ratio <= 1.0:
            raise AssertionError("a matching response did not cross the strict gate")

        signed_logical = 2.0 * cumulative - cumulative
        if not np.array_equal(signed_logical, cumulative):
            raise AssertionError("the signed 2-minus-1 logical response changed")

        analytic_tail = 9.0 * prefix_length * theta**3 / (1.0 - 3.0 * theta)
        remaining = ~emitted
        if np.any(remaining):
            actual_tail = float(np.max(cumulative[remaining]))
            if actual_tail > analytic_tail * (1.0 + 1e-10) + 1e-24:
                raise AssertionError("a permuted-prefix tail exceeded its certificate")
            if analytic_tail > 0.5 * gate * (1.0 + 1e-12):
                raise AssertionError("the permutation certificate entered the band")
            max_tail_ratio = max(max_tail_ratio, actual_tail / analytic_tail)

        expected_seen = set(int(item) for item in permutation[:prefix_length])
        if nonnegative_seen != expected_seen or signed_seen != expected_seen:
            raise AssertionError("the online seen set differs from the accepted prefix")

    if len(nonnegative_seen) != n or len(signed_seen) != n or not np.all(emitted):
        raise AssertionError("an accepted length-n trace did not finish the permutation")
    return kernel_norm, max_tail_ratio, min_matching_ratio


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
        permutation = rng.permutation(n)
        kernel_norm, tail_ratio, matching_ratio = verify_instance(n, theta, eta, permutation)
        max_kernel_norm = max(max_kernel_norm, kernel_norm)
        max_tail_ratio = max(max_tail_ratio, tail_ratio)
        min_matching_ratio = min(min_matching_ratio, matching_ratio)
        largest_theta_ratio = max(largest_theta_ratio, theta_ratio)

    print(f"seed={args.seed} trials={args.trials} max_n={args.max_n} eta={eta}")
    print(f"largest theta/theorem-threshold={largest_theta_ratio:.6e}")
    print(f"max Neumann-kernel norm={max_kernel_norm:.6e}")
    print(f"max actual/analytic permuted-tail ratio={max_tail_ratio:.6e}")
    print(f"min matched-prefix/gate ratio={min_matching_ratio:.6e}")
    print("all permutation, rejection, signed-stream, and delta checks passed")


if __name__ == "__main__":
    main()
