#!/usr/bin/env python3
"""Numerical audit for the Round-016 bounded-multiplicity reporter."""

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


def theta_threshold(horizon: int) -> float:
    """Return the exact positive-root threshold from the theorem."""
    denominator = math.sqrt(81.0 * horizon**2 + 3.0) + 9.0 * horizon
    return 1.0 / denominator**2


def accept_stream_event(
    labels: list[int],
    amplitudes: list[float],
    required_amplitudes: list[float],
    counts: np.ndarray,
    multiplicities: np.ndarray,
) -> bool:
    """Model the atomic common-label, amplitude, length, and cap check."""
    snapshot = counts.copy()
    n = len(multiplicities)
    total_budget = int(np.sum(multiplicities))
    if not labels or len(labels) != len(required_amplitudes):
        return False
    label = labels[0]
    valid = (
        int(np.sum(counts)) < total_budget
        and 0 <= label < n
        and all(stream_label == label for stream_label in labels)
        and amplitudes == required_amplitudes
        and counts[label] < multiplicities[label]
    )
    if valid:
        counts[label] += 1
    elif not np.array_equal(counts, snapshot):
        raise AssertionError("a rejected interaction changed the count state")
    return valid


def verify_instance(
    n: int,
    theta: float,
    eta: float,
    multiplicities: np.ndarray,
    trace: np.ndarray,
) -> tuple[float, float, float, float]:
    """Check one common multiset permutation and both stream modes."""
    if np.any(multiplicities < 1):
        raise ValueError("every declared multiplicity must be positive")
    total_length = int(np.sum(multiplicities))
    horizon = total_length - int(np.min(multiplicities))
    threshold = theta_threshold(horizon)
    if not 0.0 < theta <= threshold:
        raise ValueError("theta is outside the theorem's repetition scale")
    observed = np.bincount(trace, minlength=n)
    if len(trace) != total_length or not np.array_equal(observed, multiplicities):
        raise ValueError("the supplied trace is not the declared multiset")

    root_residual = 18.0 * horizon * math.sqrt(threshold) + 3.0 * threshold
    if not math.isclose(root_residual, 1.0, rel_tol=2e-13, abs_tol=2e-15):
        raise AssertionError("the closed-form scale is not the positive root")

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
    nonnegative_counts = np.zeros(n, dtype=int)
    signed_counts = np.zeros(n, dtype=int)
    nonnegative_amplitudes = [1.0, 1.0, 1.0]
    signed_amplitudes = [2.0, 1.0, 2.0, 1.0]
    max_tail_ratio = 0.0
    min_first_matching_ratio = math.inf
    max_seen_repeat_ratio = 0.0

    for prefix_length, raw_label in enumerate(trace, start=1):
        label = int(raw_label)
        other_label = (label + 1) % n
        signed_snapshot = signed_counts.copy()
        if accept_stream_event(
            [label, other_label, label, label],
            signed_amplitudes,
            signed_amplitudes,
            signed_counts,
            multiplicities,
        ):
            raise AssertionError("an inconsistent signed-stream label was accepted")
        if accept_stream_event(
            [label] * 4,
            [2.0, 1.0, 1.0, 2.0],
            signed_amplitudes,
            signed_counts,
            multiplicities,
        ):
            raise AssertionError("an incorrect signed-stream amplitude was accepted")
        if accept_stream_event(
            [n] * 4,
            signed_amplitudes,
            signed_amplitudes,
            signed_counts,
            multiplicities,
        ):
            raise AssertionError("an out-of-template label was accepted")
        if not np.array_equal(signed_counts, signed_snapshot):
            raise AssertionError("invalid stream rejection changed signed counts")

        was_seen = nonnegative_counts[label] > 0
        if not accept_stream_event(
            [label] * 3,
            nonnegative_amplitudes,
            nonnegative_amplitudes,
            nonnegative_counts,
            multiplicities,
        ):
            raise AssertionError("a valid nonnegative repeated event was rejected")
        if not accept_stream_event(
            [label] * 4,
            signed_amplitudes,
            signed_amplitudes,
            signed_counts,
            multiplicities,
        ):
            raise AssertionError("a valid signed repeated event was rejected")

        # The first attempted event beyond a label's exact multiplicity must
        # be rejected atomically.  Earlier duplicates remain legal repeats.
        if nonnegative_counts[label] == multiplicities[label]:
            exhausted_snapshot = nonnegative_counts.copy()
            if accept_stream_event(
                [label] * 3,
                nonnegative_amplitudes,
                nonnegative_amplitudes,
                nonnegative_counts,
                multiplicities,
            ):
                raise AssertionError("an exhausted per-label multiplicity was accepted")
            if not np.array_equal(nonnegative_counts, exhausted_snapshot):
                raise AssertionError("cap rejection changed the count state")

        cumulative += response[:, label]
        newly_emitted = (~emitted) & (cumulative > gate)
        expected = np.zeros(n, dtype=bool)
        if not was_seen:
            expected[label] = True
        if not np.array_equal(newly_emitted, expected):
            raise AssertionError("the repeated trace produced the wrong delta set")
        emitted |= newly_emitted

        if not was_seen:
            matching_ratio = float(cumulative[label] / gate)
            min_first_matching_ratio = min(min_first_matching_ratio, matching_ratio)
            if matching_ratio <= 1.0:
                raise AssertionError("a first matching event missed the strict gate")
        else:
            max_seen_repeat_ratio = max(max_seen_repeat_ratio, cumulative[label] / gate)

        signed_logical = 2.0 * cumulative - cumulative
        if not np.array_equal(signed_logical, cumulative):
            raise AssertionError("the signed 2-minus-1 logical response changed")

        analytic_tail = 9.0 * prefix_length * theta**3 / (1.0 - 3.0 * theta)
        unseen = nonnegative_counts == 0
        if np.any(unseen):
            if prefix_length > horizon:
                raise AssertionError("an unseen label survived beyond the proved horizon")
            actual_tail = float(np.max(cumulative[unseen]))
            if actual_tail > analytic_tail * (1.0 + 1e-10) + 1e-24:
                raise AssertionError("a repeated-prefix tail exceeded its certificate")
            if analytic_tail > 0.5 * gate * (1.0 + 1e-12):
                raise AssertionError("the multiplicity certificate entered the band")
            max_tail_ratio = max(max_tail_ratio, actual_tail / analytic_tail)

        expected_counts = np.bincount(trace[:prefix_length], minlength=n)
        if not np.array_equal(nonnegative_counts, expected_counts):
            raise AssertionError("the online nonnegative counts differ from the prefix")
        if not np.array_equal(signed_counts, expected_counts):
            raise AssertionError("the online signed counts differ from the prefix")
        if not np.array_equal(nonnegative_counts > 0, emitted):
            raise AssertionError("seen membership and emitted labels disagree")

    if not np.array_equal(nonnegative_counts, multiplicities):
        raise AssertionError("the accepted trace missed a declared multiplicity")
    if not np.array_equal(signed_counts, multiplicities) or not np.all(emitted):
        raise AssertionError("the completed common multiset trace is inconsistent")

    # The exact total length is authoritative even when every per-label cap is
    # already saturated; post-budget rejection must also be atomic.
    final_snapshot = nonnegative_counts.copy()
    if accept_stream_event(
        [0] * 3,
        nonnegative_amplitudes,
        nonnegative_amplitudes,
        nonnegative_counts,
        multiplicities,
    ):
        raise AssertionError("an event after the total length was accepted")
    if not np.array_equal(nonnegative_counts, final_snapshot):
        raise AssertionError("post-budget rejection changed the count state")

    return kernel_norm, max_tail_ratio, min_first_matching_ratio, max_seen_repeat_ratio


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--max-n", type=int, default=24)
    parser.add_argument("--max-multiplicity", type=int, default=6)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_n < 5:
        raise ValueError("--max-n must be at least 5")
    if args.max_multiplicity < 2:
        raise ValueError("--max-multiplicity must be at least 2")
    rng = np.random.default_rng(args.seed)
    eta = 0.1
    max_kernel_norm = 0.0
    max_tail_ratio = 0.0
    min_first_matching_ratio = math.inf
    max_seen_repeat_ratio = 0.0
    largest_theta_ratio = 0.0
    largest_total_length = 0

    for _ in range(args.trials):
        n = int(rng.integers(5, args.max_n + 1))
        multiplicities = rng.integers(1, args.max_multiplicity + 1, size=n)
        # Force at least one genuine repetition in every sampled trace.
        multiplicities[int(rng.integers(0, n))] = args.max_multiplicity
        total_length = int(np.sum(multiplicities))
        horizon = total_length - int(np.min(multiplicities))
        threshold = theta_threshold(horizon)
        theta_ratio = float(rng.uniform(0.05, 1.0))
        theta = theta_ratio * threshold
        trace = np.repeat(np.arange(n), multiplicities)
        rng.shuffle(trace)
        kernel_norm, tail_ratio, matching_ratio, repeat_ratio = verify_instance(
            n, theta, eta, multiplicities, trace
        )
        max_kernel_norm = max(max_kernel_norm, kernel_norm)
        max_tail_ratio = max(max_tail_ratio, tail_ratio)
        min_first_matching_ratio = min(min_first_matching_ratio, matching_ratio)
        max_seen_repeat_ratio = max(max_seen_repeat_ratio, repeat_ratio)
        largest_theta_ratio = max(largest_theta_ratio, theta_ratio)
        largest_total_length = max(largest_total_length, total_length)

    print(
        f"seed={args.seed} trials={args.trials} max_n={args.max_n} "
        f"max_multiplicity={args.max_multiplicity} eta={eta}"
    )
    print(f"largest sampled total length={largest_total_length}")
    print(f"largest theta/exact-envelope-threshold={largest_theta_ratio:.6e}")
    print(f"max Neumann-kernel norm={max_kernel_norm:.6e}")
    print(f"max actual/analytic unseen-tail ratio={max_tail_ratio:.6e}")
    print(f"min first-matching/gate ratio={min_first_matching_ratio:.6e}")
    print(f"max already-seen repeat/gate ratio={max_seen_repeat_ratio:.6e}")
    print("all multiplicity, rejection, signed-stream, certificate, and delta checks passed")


if __name__ == "__main__":
    main()
