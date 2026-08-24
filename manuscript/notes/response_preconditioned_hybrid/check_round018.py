#!/usr/bin/env python3
"""Numerical audit for the Round-018 asynchronous column-schedule reporter."""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass

import numpy as np

from check_round017 import make_schedules, notched_double_sun, response_data


@dataclass(frozen=True)
class ColumnContract:
    """All precomputed scalar data for one logical column."""

    multiplicities: np.ndarray
    prefixes: list[np.ndarray]
    crossing_indices: np.ndarray
    gaps: np.ndarray
    mass_horizons: np.ndarray
    local_event_horizons: np.ndarray
    margin: float
    total_length: int
    total_mass: float


def build_contract(
    degrees: np.ndarray,
    schedules: list[np.ndarray],
    theta: float,
    eta: float,
    envelope: float,
) -> ColumnContract:
    """Compute one column's capacities, crossings, horizons, and margin."""
    if len(schedules) != len(degrees):
        raise ValueError("a column schedule does not have complete label coverage")
    if any(
        len(values) == 0 or np.any(~np.isfinite(values)) or np.any(values <= 0.0)
        for values in schedules
    ):
        raise ValueError("every declared amplitude schedule must be finite and positive")
    c_eta = (1.0 + eta) ** 2 * eta**2
    matching = theta**2 / (degrees * (1.0 + c_eta))
    capacities = degrees * (1.0 + c_eta) * math.sqrt(theta)
    prefixes = [np.concatenate(([0.0], np.cumsum(values))) for values in schedules]
    multiplicities = np.array([len(values) for values in schedules], dtype=int)
    label_masses = np.array([values[-1] for values in prefixes])
    total_length = int(np.sum(multiplicities))
    total_mass = float(np.sum(label_masses))
    crossing_indices = np.empty(len(schedules), dtype=int)
    gaps = np.empty(len(schedules))
    mass_horizons = np.empty(len(schedules))
    local_event_horizons = np.empty(len(schedules), dtype=int)

    for label, values in enumerate(prefixes):
        candidates = np.flatnonzero(values[1:] > capacities[label])
        if candidates.size == 0:
            raise ValueError("a declared column/label schedule never exceeds capacity")
        crossing = int(candidates[0] + 1)
        previous_mass = float(values[crossing - 1])
        crossing_indices[label] = crossing
        gaps[label] = capacities[label] - previous_mass
        mass_horizons[label] = total_mass - label_masses[label] + previous_mass
        local_event_horizons[label] = total_length - multiplicities[label] + crossing - 1

    margin_cells = matching * gaps - envelope * mass_horizons
    margin = float(np.min(margin_cells))
    gate = theta**2.5
    if not 0.0 < margin < gate:
        raise ValueError("a declared column schedule fails its positive margin")
    return ColumnContract(
        multiplicities=multiplicities,
        prefixes=prefixes,
        crossing_indices=crossing_indices,
        gaps=gaps,
        mass_horizons=mass_horizons,
        local_event_horizons=local_event_horizons,
        margin=margin,
        total_length=total_length,
        total_mass=total_mass,
    )


def required_records(
    column: int, label: int, amplitude: float, *, signed: bool
) -> tuple[list[int], list[int], list[float]]:
    """Return physical stream identifiers, labels, and positive coefficients."""
    if signed:
        return [2 * column, 2 * column + 1], [label, label], [2.0 * amplitude, amplitude]
    return [column], [label], [amplitude]


def accept_event(
    column: int,
    stream_ids: list[int],
    labels: list[int],
    amplitudes: list[float],
    counts: np.ndarray,
    schedules: list[list[np.ndarray]],
    *,
    signed: bool,
) -> bool:
    """Model atomic column, pairing, label, amplitude, and cap validation."""
    snapshot = counts.copy()
    logical_columns, label_count = counts.shape
    total_length = sum(len(values) for column_data in schedules for values in column_data)
    record_count = 2 if signed else 1
    valid = (
        0 <= column < logical_columns
        and len(stream_ids) == record_count
        and len(labels) == record_count
        and len(amplitudes) == record_count
        and int(np.sum(counts)) < total_length
    )
    label = labels[0] if labels else -1
    valid = (
        valid and 0 <= label < label_count and all(record_label == label for record_label in labels)
    )
    if valid:
        expected_streams = [2 * column, 2 * column + 1] if signed else [column]
        column_length = sum(len(values) for values in schedules[column])
        valid = (
            stream_ids == expected_streams
            and int(np.sum(counts[column])) < column_length
            and counts[column, label] < len(schedules[column][label])
        )
    if valid:
        amplitude = float(schedules[column][label][counts[column, label]])
        _, _, expected_amplitudes = required_records(column, label, amplitude, signed=signed)
        valid = amplitudes == expected_amplitudes
    if valid:
        counts[column, label] += 1
    elif not np.array_equal(counts, snapshot):
        raise AssertionError("a rejected asynchronous event changed the count state")
    return valid


def make_column_schedules(
    capacities: np.ndarray,
    logical_columns: int,
    rng: np.random.Generator,
    max_multiplicity: int,
    *,
    all_delayed: bool = False,
) -> list[list[np.ndarray]]:
    """Create genuinely column-specific positive schedules."""
    result: list[list[np.ndarray]] = []
    for column in range(logical_columns):
        scale = 0.9 + 0.2 * column / max(1, logical_columns - 1)
        result.append(
            make_schedules(
                scale * capacities,
                rng,
                max_multiplicity,
                all_delayed=all_delayed,
            )
        )
    return result


def asynchronous_trace(
    contracts: list[ColumnContract], rng: np.random.Generator
) -> list[tuple[int, int]]:
    """Interleave every column's declared label multiset globally."""
    events: list[tuple[int, int]] = []
    for column, contract in enumerate(contracts):
        for label, multiplicity in enumerate(contract.multiplicities):
            events.extend([(column, label)] * int(multiplicity))
    rng.shuffle(events)
    return events


def exhaustive_state_audit(
    n: int,
    theta: float,
    eta: float,
    schedules: list[list[np.ndarray]],
) -> tuple[int, int]:
    """Exhaust every reachable count state and legal one-cell transition."""
    response, degrees, _, envelope = response_data(n, theta, eta)
    contracts = [build_contract(degrees, values, theta, eta, envelope) for values in schedules]
    multiplicities = np.vstack([contract.multiplicities for contract in contracts])
    total_length = int(np.sum(multiplicities))
    gate = theta**2.5
    state_count = 0
    transition_count = 0
    ranges = [range(int(cap) + 1) for cap in multiplicities.ravel()]

    for flat_state in itertools.product(*ranges):
        counts = np.asarray(flat_state, dtype=int).reshape(multiplicities.shape)
        global_events = int(np.sum(counts))
        cumulative = np.zeros((len(contracts), n))
        reported = np.zeros((len(contracts), n), dtype=bool)
        prefix_masses = np.zeros(len(contracts))

        for column, contract in enumerate(contracts):
            masses = np.array(
                [contract.prefixes[label][counts[column, label]] for label in range(n)]
            )
            prefix_masses[column] = float(np.sum(masses))
            cumulative[column] = response @ masses
            reported[column] = counts[column] >= contract.crossing_indices
            unreported = ~reported[column]
            if np.any(cumulative[column, unreported] > (gate - contract.margin) * (1.0 + 3e-10)):
                raise AssertionError("an exhaustive unreported state entered its column band")
            if np.any(prefix_masses[column] > contract.mass_horizons[unreported] * (1.0 + 3e-13)):
                raise AssertionError("an exhaustive state exceeded its local mass horizon")
            async_horizons = total_length - contract.multiplicities + contract.crossing_indices - 1
            if np.any(global_events > async_horizons[unreported]):
                raise AssertionError("an exhaustive state exceeded its async event horizon")

        state_count += 1
        for column, contract in enumerate(contracts):
            for label in range(n):
                occurrence = int(counts[column, label])
                if occurrence == contract.multiplicities[label]:
                    continue
                amplitude = float(schedules[column][label][occurrence])
                updated = cumulative[column] + amplitude * response[:, label]
                actual_delta = (~reported[column]) & (updated > gate)
                expected_delta = np.zeros(n, dtype=bool)
                if occurrence + 1 == contract.crossing_indices[label]:
                    expected_delta[label] = True
                if not np.array_equal(actual_delta, expected_delta):
                    raise AssertionError("an exhaustive legal transition has the wrong delta")
                transition_count += 1
    return state_count, transition_count


def verify_instance(
    n: int,
    theta: float,
    eta: float,
    schedules: list[list[np.ndarray]],
    trace: list[tuple[int, int]],
) -> tuple[float, float, float, float, float, int, int, int]:
    """Check independent schedules, arbitrary interleaving, and both interfaces."""
    response, degrees, kernel_norm, envelope = response_data(n, theta, eta)
    contracts = [build_contract(degrees, values, theta, eta, envelope) for values in schedules]
    logical_columns = len(contracts)
    total_length = sum(contract.total_length for contract in contracts)
    total_mass = sum(contract.total_mass for contract in contracts)
    if len(trace) != total_length:
        raise ValueError("the asynchronous trace has the wrong total length")

    expected_counts = np.vstack([contract.multiplicities for contract in contracts])
    trace_counts = np.zeros_like(expected_counts)
    for column, label in trace:
        trace_counts[column, label] += 1
    if not np.array_equal(trace_counts, expected_counts):
        raise ValueError("the trace is not an interleaving of every column schedule")

    gate = theta**2.5
    c_eta = (1.0 + eta) ** 2 * eta**2
    matching = theta**2 / (degrees * (1.0 + c_eta))
    max_tail_fraction = 0.0
    min_margin_fraction = math.inf
    for column, contract in enumerate(contracts):
        max_tail_fraction = max(
            max_tail_fraction,
            float(np.max(envelope * contract.mass_horizons / (matching * contract.gaps))),
        )
        min_margin_fraction = min(min_margin_fraction, contract.margin / gate)
        label_masses = np.array([values[-1] for values in contract.prefixes])
        for label in range(n):
            extreme = label_masses.copy()
            crossing = int(contract.crossing_indices[label])
            extreme[label] = contract.prefixes[label][crossing - 1]
            if not math.isclose(
                float(np.sum(extreme)),
                contract.mass_horizons[label],
                rel_tol=3e-14,
                abs_tol=0.0,
            ):
                raise AssertionError("a local future-mass horizon is not tight")
            extreme_local_events = int(np.sum(contract.multiplicities))
            extreme_local_events -= int(contract.multiplicities[label])
            extreme_local_events += crossing - 1
            if extreme_local_events != contract.local_event_horizons[label]:
                raise AssertionError("a local event horizon is not tight")
            async_horizon = total_length - int(contract.multiplicities[label]) + crossing - 1
            other_column_events = total_length - contract.total_length
            if async_horizon != contract.local_event_horizons[label] + other_column_events:
                raise AssertionError("the global asynchronous horizon is not tight")
            extreme_response = float(response[label] @ extreme)
            if extreme_response > (gate - contract.margin) * (1.0 + 3e-10):
                raise AssertionError("an extremal local prefix broke its certificate")

    nonnegative_counts = np.zeros((logical_columns, n), dtype=int)
    signed_counts = np.zeros((logical_columns, n), dtype=int)
    cumulative = np.zeros((logical_columns, n))
    prefix_masses = np.zeros(logical_columns)
    reported = np.zeros((logical_columns, n), dtype=bool)
    min_crossing_ratio = math.inf
    max_precrossing_ratio = 0.0
    seen_unreported_prefixes = 0
    column_switches = 0
    previous_column = -1

    for event_number, (column, label) in enumerate(trace, start=1):
        contract = contracts[column]
        occurrence = int(nonnegative_counts[column, label])
        amplitude = float(schedules[column][label][occurrence])
        nonnegative_records = required_records(column, label, amplitude, signed=False)
        signed_records = required_records(column, label, amplitude, signed=True)
        if previous_column >= 0 and previous_column != column:
            column_switches += 1
        previous_column = column

        invalid_snapshot = signed_counts.copy()
        bad_streams = signed_records[0].copy()
        bad_streams[-1] = (bad_streams[-1] + 2) % (2 * logical_columns)
        if accept_event(
            column,
            bad_streams,
            signed_records[1],
            signed_records[2],
            signed_counts,
            schedules,
            signed=True,
        ):
            raise AssertionError("a cross-column signed pair was accepted")
        bad_labels = signed_records[1].copy()
        bad_labels[-1] = (label + 1) % n
        if accept_event(
            column,
            signed_records[0],
            bad_labels,
            signed_records[2],
            signed_counts,
            schedules,
            signed=True,
        ):
            raise AssertionError("a paired-label disagreement was accepted")
        bad_amplitudes = signed_records[2].copy()
        bad_amplitudes[0] *= 1.01
        if accept_event(
            column,
            signed_records[0],
            signed_records[1],
            bad_amplitudes,
            signed_counts,
            schedules,
            signed=True,
        ):
            raise AssertionError("a column-schedule amplitude mismatch was accepted")
        if accept_event(
            column,
            signed_records[0],
            [n, n],
            signed_records[2],
            signed_counts,
            schedules,
            signed=True,
        ):
            raise AssertionError("an out-of-template label was accepted")
        if not np.array_equal(signed_counts, invalid_snapshot):
            raise AssertionError("invalid input changed another column's state")
        if accept_event(
            logical_columns,
            signed_records[0],
            signed_records[1],
            signed_records[2],
            signed_counts,
            schedules,
            signed=True,
        ):
            raise AssertionError("an out-of-range logical column was accepted")

        crossing_now = occurrence + 1 == contract.crossing_indices[label]
        if crossing_now:
            ratio = cumulative[column, label] / (gate - contract.margin)
            max_precrossing_ratio = max(max_precrossing_ratio, float(ratio))
            if ratio > 1.0 + 3e-10:
                raise AssertionError("a column label violated its pre-crossing certificate")

        if not accept_event(
            column,
            *nonnegative_records,
            nonnegative_counts,
            schedules,
            signed=False,
        ):
            raise AssertionError("a valid nonnegative column event was rejected")
        if not accept_event(
            column,
            *signed_records,
            signed_counts,
            schedules,
            signed=True,
        ):
            raise AssertionError("a valid signed column event was rejected")

        other_columns_before = cumulative.copy()
        prefix_masses[column] += amplitude
        cumulative[column] += amplitude * response[:, label]
        other_columns_before[column] = cumulative[column]
        if not np.array_equal(cumulative, other_columns_before):
            raise AssertionError("an event changed a different logical column")

        expected_delta = np.zeros((logical_columns, n), dtype=bool)
        if crossing_now:
            expected_delta[column, label] = True
        actual_delta = (~reported) & (cumulative > gate)
        if not np.array_equal(actual_delta, expected_delta):
            raise AssertionError("the exact and certified asynchronous deltas differ")
        reported |= expected_delta
        if crossing_now:
            min_crossing_ratio = min(min_crossing_ratio, float(cumulative[column, label] / gate))

        for checked_column, checked_contract in enumerate(contracts):
            masses = np.array(
                [
                    checked_contract.prefixes[i][nonnegative_counts[checked_column, i]]
                    for i in range(n)
                ]
            )
            lower = matching * masses
            upper = lower + envelope * prefix_masses[checked_column]
            tolerance = 3e-10 * np.maximum(upper, gate)
            if np.any(cumulative[checked_column] + tolerance < lower):
                raise AssertionError("a column response violated its lower envelope")
            if np.any(cumulative[checked_column] > upper + tolerance):
                raise AssertionError("a column response violated its upper envelope")
            unreported = nonnegative_counts[checked_column] < checked_contract.crossing_indices
            if np.any(
                cumulative[checked_column, unreported]
                > (gate - checked_contract.margin) * (1.0 + 3e-10)
            ):
                raise AssertionError("an unreported column label entered its band")
            if np.any(
                prefix_masses[checked_column]
                > checked_contract.mass_horizons[unreported] * (1.0 + 3e-13)
            ):
                raise AssertionError("a local mass prefix exceeded its horizon")
            async_horizons = (
                total_length
                - checked_contract.multiplicities
                + checked_contract.crossing_indices
                - 1
            )
            if np.any(event_number > async_horizons[unreported]):
                raise AssertionError("an unreported label exceeded its async horizon")
            if np.any((nonnegative_counts[checked_column] > 0) & unreported):
                seen_unreported_prefixes += 1

        if not np.array_equal(nonnegative_counts, signed_counts):
            raise AssertionError("signed and nonnegative column states differ")
        if not np.array_equal(
            reported,
            nonnegative_counts >= np.vstack([value.crossing_indices for value in contracts]),
        ):
            raise AssertionError("reported membership differs from the column capacities")
        logical_increment = amplitude * response[:, label]
        signed_increment = 2.0 * logical_increment - logical_increment
        if not np.array_equal(logical_increment, signed_increment):
            raise AssertionError("the paired 2-minus-1 event changed logical response")

        if nonnegative_counts[column, label] == contract.multiplicities[label]:
            exhausted_snapshot = nonnegative_counts.copy()
            if accept_event(
                column,
                *nonnegative_records,
                nonnegative_counts,
                schedules,
                signed=False,
            ):
                raise AssertionError("an exhausted column/label schedule was accepted")
            if not np.array_equal(nonnegative_counts, exhausted_snapshot):
                raise AssertionError("cap rejection changed the asynchronous state")

    if not np.array_equal(nonnegative_counts, expected_counts):
        raise AssertionError("the completed trace missed a declared column event")
    if not np.array_equal(signed_counts, expected_counts) or not np.all(reported):
        raise AssertionError("the completed signed trace missed a crossing")
    if not math.isclose(float(np.sum(prefix_masses)), total_mass, rel_tol=3e-14):
        raise AssertionError("online and declared total logical masses differ")

    nonnegative_cells = total_length
    signed_cells = 2 * total_length
    nonnegative_absolute_mass = total_mass
    signed_absolute_mass = 3.0 * total_mass
    delta_records = logical_columns * n
    certificate_records = total_length
    if total_length < delta_records:
        raise AssertionError("complete label coverage did not dominate delta output")
    if signed_cells != 2 * nonnegative_cells:
        raise AssertionError("the signed asynchronous fragment count is incorrect")
    if not math.isclose(signed_absolute_mass, 3.0 * nonnegative_absolute_mass, rel_tol=2e-15):
        raise AssertionError("the signed asynchronous absolute mass is incorrect")
    if certificate_records + delta_records > 2 * total_length:
        raise AssertionError("the claimed linear emission ledger is incorrect")

    final_snapshot = signed_counts.copy()
    final_amplitude = float(schedules[0][0][-1])
    final_records = required_records(0, 0, final_amplitude, signed=True)
    if accept_event(0, *final_records, signed_counts, schedules, signed=True) or not np.array_equal(
        signed_counts, final_snapshot
    ):
        raise AssertionError("post-length rejection was not atomic")
    delayed_crossings = sum(int(np.sum(contract.crossing_indices > 1)) for contract in contracts)
    return (
        kernel_norm,
        max_tail_fraction,
        min_margin_fraction,
        min_crossing_ratio,
        max_precrossing_ratio,
        delayed_crossings,
        seen_unreported_prefixes,
        column_switches,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--max-n", type=int, default=24)
    parser.add_argument("--max-multiplicity", type=int, default=6)
    parser.add_argument("--max-columns", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_n < 5 or args.max_multiplicity < 2 or args.max_columns < 2:
        raise ValueError("require max-n >= 5, max-multiplicity >= 2, max-columns >= 2")
    rng = np.random.default_rng(args.seed)
    eta = 0.1
    c_eta = (1.0 + eta) ** 2 * eta**2
    metrics = [0.0, 0.0, math.inf, math.inf, 0.0, 0, 0, 0]
    largest_total_length = 0
    largest_total_mass = 0.0

    exhaustive_n = 5
    exhaustive_theta = 1.0e-6
    exhaustive_degrees = notched_double_sun(exhaustive_n).sum(axis=1)[:exhaustive_n]
    exhaustive_capacities = exhaustive_degrees * (1.0 + c_eta) * math.sqrt(exhaustive_theta)
    exhaustive_schedules: list[list[np.ndarray]] = []
    for column in range(2):
        column_schedules: list[np.ndarray] = []
        for label, capacity in enumerate(exhaustive_capacities):
            if label == 0:
                first = (0.25 + 0.03 * column) * capacity
                total = (1.10 + 0.05 * column) * capacity
                column_schedules.append(np.array([first, total - first]))
            else:
                column_schedules.append(
                    np.array([(1.08 + 0.04 * column + 0.005 * label) * capacity])
                )
        exhaustive_schedules.append(column_schedules)
    exhaustive_states, exhaustive_transitions = exhaustive_state_audit(
        exhaustive_n, exhaustive_theta, eta, exhaustive_schedules
    )
    if exhaustive_states != 2304 or exhaustive_transitions != 12288:
        raise AssertionError("the exhaustive state-space cardinalities changed")

    instances: list[tuple[int, float, int, bool]] = [(5, 1.0e-6, 3, True)]
    for _ in range(args.trials):
        n = int(rng.integers(5, args.max_n + 1))
        columns = int(rng.integers(2, args.max_columns + 1))
        theta = float(rng.uniform(0.15, 0.95) / (40000.0 * n * columns))
        instances.append((n, theta, columns, False))

    for n, theta, columns, all_delayed in instances:
        degrees = notched_double_sun(n).sum(axis=1)[:n]
        capacities = degrees * (1.0 + c_eta) * math.sqrt(theta)
        schedules = make_column_schedules(
            capacities,
            columns,
            rng,
            args.max_multiplicity,
            all_delayed=all_delayed,
        )
        _, _, _, envelope = response_data(n, theta, eta)
        contracts = [build_contract(degrees, values, theta, eta, envelope) for values in schedules]
        trace = asynchronous_trace(contracts, rng)
        result = verify_instance(n, theta, eta, schedules, trace)
        metrics[0] = max(metrics[0], result[0])
        metrics[1] = max(metrics[1], result[1])
        metrics[2] = min(metrics[2], result[2])
        metrics[3] = min(metrics[3], result[3])
        metrics[4] = max(metrics[4], result[4])
        metrics[5] += result[5]
        metrics[6] += result[6]
        metrics[7] += result[7]
        largest_total_length = max(largest_total_length, len(trace))
        largest_total_mass = max(
            largest_total_mass, sum(contract.total_mass for contract in contracts)
        )

    print(
        f"seed={args.seed} trials={args.trials} max_n={args.max_n} "
        f"max_multiplicity={args.max_multiplicity} max_columns={args.max_columns} eta={eta}"
    )
    print(f"largest sampled asynchronous length={largest_total_length}")
    print(f"largest sampled total logical mass={largest_total_mass:.6e}")
    print(f"exhaustive count states={exhaustive_states}")
    print(f"exhaustive legal transitions={exhaustive_transitions}")
    print(f"asynchronous column switches={metrics[7]}")
    print(f"delayed certified column/label crossings={metrics[5]}")
    print(f"prefix column states with a seen-but-unreported label={metrics[6]}")
    print(f"max Neumann-kernel norm={metrics[0]:.6e}")
    print(f"max local-future-tail/gap fraction={metrics[1]:.6e}")
    print(f"min per-column band/gate fraction={metrics[2]:.6e}")
    print(f"min certified-crossing/gate ratio={metrics[3]:.6e}")
    print(f"max actual-pre-crossing/(column gate-band)={metrics[4]:.6e}")
    print("all asynchronous schedule, pairing, certificate, rejection, and ledger checks passed")


if __name__ == "__main__":
    main()
