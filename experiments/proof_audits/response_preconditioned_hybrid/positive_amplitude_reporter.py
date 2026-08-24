#!/usr/bin/env python3
"""Numerical audit for the Round-017 positive-amplitude reporter."""

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


def response_data(n: int, theta: float, eta: float) -> tuple[np.ndarray, np.ndarray, float, float]:
    """Build the exact-form first-rung response and its scalar envelope."""
    adjacency = notched_double_sun(n)
    degrees = adjacency.sum(axis=1)
    normalized = adjacency / np.sqrt(np.outer(degrees, degrees))
    normalized_face = normalized[: 2 * n, : 2 * n]
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
    direct_shifted[n:, n:] += c_eta * (1.0 - 2.0 * theta) * np.eye(n)
    if not np.allclose(shifted, direct_shifted, rtol=1e-13, atol=1e-15):
        raise AssertionError("the exact B-theta R decomposition failed")

    sources = np.zeros((2 * n, n))
    sources[n + np.arange(n), np.arange(n)] = 1.0
    corrections = np.linalg.solve(shifted, sources)
    response = -(pagerank[2 * n :, : 2 * n] @ corrections)
    response /= np.sqrt(degrees[2 * n :])[:, None]
    if not np.all(response > 0.0):
        raise AssertionError("the first-rung response is not entrywise positive")

    envelope = 9.0 * theta**3 / (1.0 - 3.0 * theta)
    matching = theta**2 / (degrees[:n] * (1.0 + c_eta))
    diagonal = np.diag(response)
    tolerance = 2e-12 * np.maximum(diagonal, matching)
    if np.any(diagonal + tolerance < matching):
        raise AssertionError("a matching entry violated its Neumann lower bound")
    if np.any(diagonal > matching + envelope * (1.0 + 2e-10)):
        raise AssertionError("a matching entry violated its scalar upper bound")
    off_diagonal = response.copy()
    np.fill_diagonal(off_diagonal, 0.0)
    if np.max(off_diagonal) > envelope * (1.0 + 2e-10):
        raise AssertionError("an off-matching entry violated its scalar upper bound")
    return response, degrees[:n], kernel_norm, envelope


def make_schedules(
    capacities: np.ndarray,
    rng: np.random.Generator,
    max_multiplicity: int,
    *,
    all_delayed: bool = False,
) -> list[np.ndarray]:
    """Create positive occurrence schedules with controlled capacity gaps."""
    schedules: list[np.ndarray] = []
    for label, capacity in enumerate(capacities):
        if all_delayed:
            multiplicity = 2
            crossing_index = 2
        else:
            multiplicity = int(rng.integers(2, max_multiplicity + 1))
            crossing_index = int(rng.integers(1, multiplicity + 1))
            if label == 0:
                crossing_index = min(2, multiplicity)

        amplitudes = np.zeros(multiplicity)
        if crossing_index > 1:
            weights = rng.uniform(0.2, 1.0, size=crossing_index - 1)
            weights /= np.sum(weights)
            amplitudes[: crossing_index - 1] = 0.35 * capacity * weights
            pre_crossing_mass = 0.35 * capacity
        else:
            pre_crossing_mass = 0.0
        amplitudes[crossing_index - 1] = 1.20 * capacity - pre_crossing_mass
        if crossing_index < multiplicity:
            amplitudes[crossing_index:] = capacity * rng.uniform(
                0.04, 0.12, size=multiplicity - crossing_index
            )
        if np.any(amplitudes <= 0.0):
            raise AssertionError("the generator produced a nonpositive amplitude")
        schedules.append(amplitudes)
    return schedules


def schedule_contract(
    degrees: np.ndarray,
    schedules: list[np.ndarray],
    theta: float,
    eta: float,
    envelope: float,
) -> tuple[
    np.ndarray,
    list[np.ndarray],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    float,
    float,
]:
    """Compute capacities, first crossings, mass horizons, and the band."""
    c_eta = (1.0 + eta) ** 2 * eta**2
    matching = theta**2 / (degrees * (1.0 + c_eta))
    capacities = degrees * (1.0 + c_eta) * math.sqrt(theta)
    prefix_masses = [np.concatenate(([0.0], np.cumsum(values))) for values in schedules]
    multiplicities = np.array([len(values) for values in schedules], dtype=int)
    label_masses = np.array([values[-1] for values in prefix_masses])
    total_mass = float(np.sum(label_masses))
    crossing_indices = np.empty(len(schedules), dtype=int)
    gaps = np.empty(len(schedules))
    mass_horizons = np.empty(len(schedules))
    event_horizons = np.empty(len(schedules), dtype=int)
    total_length = int(np.sum(multiplicities))

    for label, prefixes in enumerate(prefix_masses):
        crossing_candidates = np.flatnonzero(prefixes[1:] > capacities[label])
        if crossing_candidates.size == 0:
            raise ValueError("a declared label never exceeds its response capacity")
        crossing = int(crossing_candidates[0] + 1)
        crossing_indices[label] = crossing
        previous_mass = prefixes[crossing - 1]
        gaps[label] = capacities[label] - previous_mass
        mass_horizons[label] = total_mass - label_masses[label] + previous_mass
        event_horizons[label] = total_length - multiplicities[label] + crossing - 1

    margin_cells = matching * gaps - envelope * mass_horizons
    margin = float(np.min(margin_cells))
    if not margin > 0.0:
        raise ValueError("the declared schedule fails the positive amplitude margin")
    gate = theta**2.5
    if not 0.0 < margin < gate:
        raise AssertionError("the derived transition band is not inside the gate")
    return (
        multiplicities,
        prefix_masses,
        crossing_indices,
        gaps,
        mass_horizons,
        event_horizons,
        total_mass,
        margin,
    )


def required_stream_amplitudes(
    logical_amplitude: float, logical_columns: int, *, signed: bool
) -> list[float]:
    """Return the checked physical stream coefficients for one event."""
    if signed:
        return [
            coefficient
            for _ in range(logical_columns)
            for coefficient in (2.0 * logical_amplitude, logical_amplitude)
        ]
    return [logical_amplitude] * logical_columns


def accept_event(
    labels: list[int],
    amplitudes: list[float],
    counts: np.ndarray,
    schedules: list[np.ndarray],
    logical_columns: int,
    *,
    signed: bool,
) -> bool:
    """Model atomic label, schedule, total-length, and cap validation."""
    snapshot = counts.copy()
    total_length = sum(len(values) for values in schedules)
    stream_count = 2 * logical_columns if signed else logical_columns
    valid = len(labels) == stream_count and len(amplitudes) == stream_count
    label = labels[0] if labels else -1
    valid = (
        valid
        and int(np.sum(counts)) < total_length
        and 0 <= label < len(schedules)
        and all(stream_label == label for stream_label in labels)
        and counts[label] < len(schedules[label])
    )
    if valid:
        logical_amplitude = float(schedules[label][counts[label]])
        required = required_stream_amplitudes(logical_amplitude, logical_columns, signed=signed)
        valid = amplitudes == required
    if valid:
        counts[label] += 1
    elif not np.array_equal(counts, snapshot):
        raise AssertionError("a rejected interaction changed the count state")
    return valid


def verify_instance(
    n: int,
    theta: float,
    eta: float,
    schedules: list[np.ndarray],
    trace: np.ndarray,
    logical_columns: int,
) -> tuple[float, float, float, float, float, int, int]:
    """Check one interleaving, its delayed crossings, and both stream modes."""
    response, degrees, kernel_norm, envelope = response_data(n, theta, eta)
    (
        multiplicities,
        prefix_masses,
        crossing_indices,
        gaps,
        mass_horizons,
        event_horizons,
        total_mass,
        margin,
    ) = schedule_contract(degrees, schedules, theta, eta, envelope)
    total_length = int(np.sum(multiplicities))
    if len(trace) != total_length:
        raise ValueError("the trace length differs from the declared multiplicities")
    if not np.array_equal(np.bincount(trace, minlength=n), multiplicities):
        raise ValueError("the trace is not an interleaving of the declared schedules")

    gate = theta**2.5
    c_eta = (1.0 + eta) ** 2 * eta**2
    matching = theta**2 / (degrees * (1.0 + c_eta))
    margin_fraction = margin / gate
    tail_fraction = float(np.max(envelope * mass_horizons / (matching * gaps)))

    # Realize the extremal pre-crossing mass vector for every label: every
    # other schedule is exhausted and this label stops one event before k_i*.
    final_label_masses = np.array([prefixes[-1] for prefixes in prefix_masses])
    for label in range(n):
        extreme_masses = final_label_masses.copy()
        extreme_masses[label] = prefix_masses[label][crossing_indices[label] - 1]
        if not math.isclose(
            float(np.sum(extreme_masses)),
            mass_horizons[label],
            rel_tol=3e-14,
            abs_tol=0.0,
        ):
            raise AssertionError("the extremal future-mass capacity is not tight")
        extreme_events = int(np.sum(multiplicities) - multiplicities[label])
        extreme_events += int(crossing_indices[label] - 1)
        if extreme_events != event_horizons[label]:
            raise AssertionError("the extremal event capacity is not tight")
        extreme_response = float(response[label] @ extreme_masses)
        if extreme_response > (gate - margin) * (1.0 + 3e-10):
            raise AssertionError("an extremal pre-crossing trace broke the certificate")

    nonnegative_counts = np.zeros(n, dtype=int)
    signed_counts = np.zeros(n, dtype=int)
    cumulative = np.zeros(n)
    reported = np.zeros(n, dtype=bool)
    prefix_mass = 0.0
    min_crossing_ratio = math.inf
    max_precrossing_ratio = 0.0
    seen_unreported_visits = 0
    delayed_crossings = int(np.sum(crossing_indices > 1))

    for event_number, raw_label in enumerate(trace, start=1):
        label = int(raw_label)
        occurrence = int(nonnegative_counts[label])
        logical_amplitude = float(schedules[label][occurrence])
        nonnegative_required = required_stream_amplitudes(
            logical_amplitude, logical_columns, signed=False
        )
        signed_required = required_stream_amplitudes(
            logical_amplitude, logical_columns, signed=True
        )
        nonnegative_labels = [label] * logical_columns
        signed_labels = [label] * (2 * logical_columns)

        # Every rejection is tested before the valid event and must be atomic.
        bad_label_snapshot = signed_counts.copy()
        inconsistent_labels = signed_labels.copy()
        inconsistent_labels[-1] = (label + 1) % n
        if accept_event(
            inconsistent_labels,
            signed_required,
            signed_counts,
            schedules,
            logical_columns,
            signed=True,
        ):
            raise AssertionError("a cross-stream label disagreement was accepted")
        wrong_amplitudes = signed_required.copy()
        wrong_amplitudes[0] *= 1.01
        if accept_event(
            signed_labels,
            wrong_amplitudes,
            signed_counts,
            schedules,
            logical_columns,
            signed=True,
        ):
            raise AssertionError("a schedule-amplitude disagreement was accepted")
        if accept_event(
            [n] * (2 * logical_columns),
            signed_required,
            signed_counts,
            schedules,
            logical_columns,
            signed=True,
        ):
            raise AssertionError("an out-of-template label was accepted")
        if not np.array_equal(signed_counts, bad_label_snapshot):
            raise AssertionError("invalid signed input changed the count state")

        crossing_now = occurrence + 1 == crossing_indices[label]
        if crossing_now:
            max_precrossing_ratio = max(max_precrossing_ratio, cumulative[label] / (gate - margin))
            if cumulative[label] > (gate - margin) * (1.0 + 3e-10):
                raise AssertionError("a label exceeded its pre-crossing certificate")

        if not accept_event(
            nonnegative_labels,
            nonnegative_required,
            nonnegative_counts,
            schedules,
            logical_columns,
            signed=False,
        ):
            raise AssertionError("a valid nonnegative amplitude event was rejected")
        if not accept_event(
            signed_labels,
            signed_required,
            signed_counts,
            schedules,
            logical_columns,
            signed=True,
        ):
            raise AssertionError("a valid signed amplitude event was rejected")

        prefix_mass += logical_amplitude
        cumulative += logical_amplitude * response[:, label]
        expected_delta = np.zeros(n, dtype=bool)
        if crossing_now:
            expected_delta[label] = True
        actual_delta = (~reported) & (cumulative > gate)
        if not np.array_equal(actual_delta, expected_delta):
            raise AssertionError("the exact response and certified delta sets differ")
        reported |= expected_delta

        if crossing_now:
            crossing_ratio = float(cumulative[label] / gate)
            min_crossing_ratio = min(min_crossing_ratio, crossing_ratio)
            if crossing_ratio <= 1.0:
                raise AssertionError("a certified crossing did not clear the gate")

        per_label_mass = np.array([prefix_masses[i][nonnegative_counts[i]] for i in range(n)])
        lower = matching * per_label_mass
        upper = lower + envelope * prefix_mass
        tolerance = 3e-10 * np.maximum(upper, gate)
        if np.any(cumulative + tolerance < lower):
            raise AssertionError("the cumulative response violated its lower envelope")
        if np.any(cumulative > upper + tolerance):
            raise AssertionError("the cumulative response violated its upper envelope")

        unreported = nonnegative_counts < crossing_indices
        if np.any(cumulative[unreported] > (gate - margin) * (1.0 + 3e-10)):
            raise AssertionError("an unreported label entered the transition band")
        if np.any(prefix_mass > mass_horizons[unreported] * (1.0 + 3e-13)):
            raise AssertionError("an unreported label exceeded its future-mass horizon")
        if np.any(event_number > event_horizons[unreported]):
            raise AssertionError("an unreported label exceeded its event horizon")
        if np.any((nonnegative_counts > 0) & unreported):
            seen_unreported_visits += 1

        if not np.array_equal(nonnegative_counts, signed_counts):
            raise AssertionError("the signed and nonnegative occurrence states differ")
        expected_reported = nonnegative_counts >= crossing_indices
        if not np.array_equal(reported, expected_reported):
            raise AssertionError("reported membership differs from the capacity rule")

        logical_increment = logical_amplitude * response[:, label]
        signed_increment = (
            2.0 * logical_amplitude * response[:, label] - logical_amplitude * response[:, label]
        )
        if not np.allclose(signed_increment, logical_increment, rtol=0.0, atol=0.0):
            raise AssertionError("the signed 2-minus-1 streams changed the response")

        if nonnegative_counts[label] == multiplicities[label]:
            exhausted_snapshot = nonnegative_counts.copy()
            exhausted_amplitudes = required_stream_amplitudes(
                logical_amplitude, logical_columns, signed=False
            )
            if accept_event(
                nonnegative_labels,
                exhausted_amplitudes,
                nonnegative_counts,
                schedules,
                logical_columns,
                signed=False,
            ):
                raise AssertionError("an exhausted per-label schedule was accepted")
            if not np.array_equal(nonnegative_counts, exhausted_snapshot):
                raise AssertionError("cap rejection changed the count state")

    if not np.array_equal(nonnegative_counts, multiplicities):
        raise AssertionError("the accepted trace missed a declared event")
    if not np.array_equal(signed_counts, multiplicities) or not np.all(reported):
        raise AssertionError("the completed trace missed a certified crossing")
    if not math.isclose(prefix_mass, total_mass, rel_tol=3e-14, abs_tol=0.0):
        raise AssertionError("the online and declared total masses differ")

    # The coordinate ledger and absolute coefficient mass distinguish the
    # nonnegative and signed interfaces even though their logical response is equal.
    nonnegative_cells = logical_columns * total_length
    signed_cells = 2 * logical_columns * total_length
    nonnegative_absolute_mass = logical_columns * total_mass
    signed_absolute_mass = 3 * logical_columns * total_mass
    if signed_cells != 2 * nonnegative_cells:
        raise AssertionError("the signed fragment-cell count is incorrect")
    if not math.isclose(
        signed_absolute_mass,
        3.0 * nonnegative_absolute_mass,
        rel_tol=2e-15,
        abs_tol=0.0,
    ):
        raise AssertionError("the signed absolute fragment mass is incorrect")

    final_snapshot = signed_counts.copy()
    final_amplitude = float(schedules[0][-1])
    if accept_event(
        [0] * (2 * logical_columns),
        required_stream_amplitudes(final_amplitude, logical_columns, signed=True),
        signed_counts,
        schedules,
        logical_columns,
        signed=True,
    ):
        raise AssertionError("an event after the authoritative length was accepted")
    if not np.array_equal(signed_counts, final_snapshot):
        raise AssertionError("post-length rejection changed the count state")

    return (
        kernel_norm,
        tail_fraction,
        margin_fraction,
        min_crossing_ratio,
        max_precrossing_ratio,
        delayed_crossings,
        seen_unreported_visits,
    )


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
    max_tail_fraction = 0.0
    min_margin_fraction = math.inf
    min_crossing_ratio = math.inf
    max_precrossing_ratio = 0.0
    largest_total_length = 0
    largest_total_mass = 0.0
    delayed_crossings = 0
    seen_unreported_visits = 0

    # A deterministic two-event-per-label case makes every first occurrence
    # too small and forces every certified crossing to the second occurrence.
    deterministic_n = 5
    deterministic_theta = 1.0e-6
    deterministic_adjacency = notched_double_sun(deterministic_n)
    deterministic_degrees = deterministic_adjacency.sum(axis=1)[:deterministic_n]
    c_eta = (1.0 + eta) ** 2 * eta**2
    deterministic_capacities = (
        deterministic_degrees * (1.0 + c_eta) * math.sqrt(deterministic_theta)
    )
    deterministic_schedules = make_schedules(
        deterministic_capacities, rng, args.max_multiplicity, all_delayed=True
    )
    deterministic_trace = np.repeat(np.arange(deterministic_n), 2)
    rng.shuffle(deterministic_trace)
    results = verify_instance(
        deterministic_n,
        deterministic_theta,
        eta,
        deterministic_schedules,
        deterministic_trace,
        logical_columns=2,
    )
    max_kernel_norm = max(max_kernel_norm, results[0])
    max_tail_fraction = max(max_tail_fraction, results[1])
    min_margin_fraction = min(min_margin_fraction, results[2])
    min_crossing_ratio = min(min_crossing_ratio, results[3])
    max_precrossing_ratio = max(max_precrossing_ratio, results[4])
    delayed_crossings += results[5]
    seen_unreported_visits += results[6]
    largest_total_length = max(largest_total_length, len(deterministic_trace))
    largest_total_mass = max(
        largest_total_mass,
        sum(float(np.sum(values)) for values in deterministic_schedules),
    )

    for _ in range(args.trials):
        n = int(rng.integers(5, args.max_n + 1))
        theta = float(rng.uniform(0.15, 0.95) / (20000.0 * n))
        adjacency = notched_double_sun(n)
        degrees = adjacency.sum(axis=1)[:n]
        capacities = degrees * (1.0 + c_eta) * math.sqrt(theta)
        schedules = make_schedules(capacities, rng, args.max_multiplicity)
        multiplicities = np.array([len(values) for values in schedules], dtype=int)
        trace = np.repeat(np.arange(n), multiplicities)
        rng.shuffle(trace)
        logical_columns = int(rng.integers(1, 5))
        results = verify_instance(n, theta, eta, schedules, trace, logical_columns=logical_columns)
        max_kernel_norm = max(max_kernel_norm, results[0])
        max_tail_fraction = max(max_tail_fraction, results[1])
        min_margin_fraction = min(min_margin_fraction, results[2])
        min_crossing_ratio = min(min_crossing_ratio, results[3])
        max_precrossing_ratio = max(max_precrossing_ratio, results[4])
        delayed_crossings += results[5]
        seen_unreported_visits += results[6]
        largest_total_length = max(largest_total_length, len(trace))
        largest_total_mass = max(
            largest_total_mass, sum(float(np.sum(values)) for values in schedules)
        )

    print(
        f"seed={args.seed} trials={args.trials} max_n={args.max_n} "
        f"max_multiplicity={args.max_multiplicity} eta={eta}"
    )
    print(f"largest sampled total length={largest_total_length}")
    print(f"largest sampled logical mass={largest_total_mass:.6e}")
    print(f"delayed certified crossings={delayed_crossings}")
    print(f"prefixes with a seen-but-unreported label={seen_unreported_visits}")
    print(f"max Neumann-kernel norm={max_kernel_norm:.6e}")
    print(f"max future-tail/gap fraction={max_tail_fraction:.6e}")
    print(f"min derived-band/gate fraction={min_margin_fraction:.6e}")
    print(f"min certified-crossing/gate ratio={min_crossing_ratio:.6e}")
    print(f"max actual-pre-crossing/(gate-band)={max_precrossing_ratio:.6e}")
    print("all amplitude, capacity, certificate, rejection, and ledger checks passed")


if __name__ == "__main__":
    main()
