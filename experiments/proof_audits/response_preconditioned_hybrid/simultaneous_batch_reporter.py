#!/usr/bin/env python3
"""Numerical audit for the Round-019 simultaneous-batch reporter."""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass, replace

import numpy as np

from experiments.proof_audits.response_preconditioned_hybrid.asynchronous_column_reporter import (
    build_contract,
    make_column_schedules,
)
from experiments.proof_audits.response_preconditioned_hybrid.positive_amplitude_reporter import (
    notched_double_sun,
    response_data,
)


@dataclass(frozen=True)
class LogicalRecord:
    """One tagged logical occurrence and its positive physical records."""

    column: int
    label: int
    occurrence: int
    stream_ids: tuple[int, ...]
    physical_labels: tuple[int, ...]
    amplitudes: tuple[float, ...]


@dataclass(frozen=True)
class BatchMetrics:
    """Extrema and counts from one complete batched epoch."""

    kernel_norm: float
    max_tail_fraction: float
    min_margin_fraction: float
    min_crossing_ratio: float
    max_precrossing_ratio: float
    batches: int
    affected_column_certificates: int
    max_batch_size: int
    mixed_column_batches: int
    multicrossing_batches: int
    jumped_cell_crossings: int
    delayed_crossings: int
    seen_unreported_boundaries: int


def make_record(
    column: int,
    label: int,
    occurrence: int,
    schedules: list[list[np.ndarray]],
    *,
    signed: bool,
) -> LogicalRecord:
    """Construct the declared physical representation of one occurrence."""
    amplitude = float(schedules[column][label][occurrence - 1])
    if signed:
        return LogicalRecord(
            column=column,
            label=label,
            occurrence=occurrence,
            stream_ids=(2 * column, 2 * column + 1),
            physical_labels=(label, label),
            amplitudes=(2.0 * amplitude, amplitude),
        )
    return LogicalRecord(
        column=column,
        label=label,
        occurrence=occurrence,
        stream_ids=(column,),
        physical_labels=(label,),
        amplitudes=(amplitude,),
    )


def accept_batch(
    batch: list[LogicalRecord],
    counts: np.ndarray,
    schedules: list[list[np.ndarray]],
    *,
    signed: bool,
) -> bool:
    """Atomically validate and commit an unordered batch of tagged records."""
    snapshot = counts.copy()
    logical_columns, label_count = counts.shape
    total_length = sum(len(values) for column in schedules for values in column)
    expected_width = 2 if signed else 1
    valid = bool(batch) and int(np.sum(counts)) + len(batch) <= total_length
    blocks: dict[tuple[int, int], list[int]] = {}

    for record in batch:
        valid = valid and 0 <= record.column < logical_columns
        valid = valid and 0 <= record.label < label_count
        valid = valid and len(record.stream_ids) == expected_width
        valid = valid and len(record.physical_labels) == expected_width
        valid = valid and len(record.amplitudes) == expected_width
        if not valid:
            break
        schedule = schedules[record.column][record.label]
        valid = 1 <= record.occurrence <= len(schedule)
        if not valid:
            break
        expected = make_record(
            record.column,
            record.label,
            record.occurrence,
            schedules,
            signed=signed,
        )
        valid = record == expected
        if not valid:
            break
        blocks.setdefault((record.column, record.label), []).append(record.occurrence)

    if valid:
        for (column, label), occurrences in blocks.items():
            start = int(counts[column, label]) + 1
            expected_occurrences = list(range(start, start + len(occurrences)))
            if sorted(occurrences) != expected_occurrences:
                valid = False
                break
            if expected_occurrences[-1] > len(schedules[column][label]):
                valid = False
                break

    if valid:
        for (column, label), occurrences in blocks.items():
            counts[column, label] += len(occurrences)
    elif not np.array_equal(counts, snapshot):
        raise AssertionError("a rejected simultaneous batch changed persistent counts")
    return valid


def tagged_events(
    multiplicities: np.ndarray,
    rng: np.random.Generator,
) -> list[tuple[int, int, int]]:
    """Return a random legal serialization with explicit occurrence tags."""
    cells: list[tuple[int, int]] = []
    for column in range(multiplicities.shape[0]):
        for label in range(multiplicities.shape[1]):
            cells.extend([(column, label)] * int(multiplicities[column, label]))
    rng.shuffle(cells)
    counts = np.zeros_like(multiplicities)
    result: list[tuple[int, int, int]] = []
    for column, label in cells:
        counts[column, label] += 1
        result.append((column, label, int(counts[column, label])))
    return result


def partition_events(
    events: list[tuple[int, int, int]],
    rng: np.random.Generator,
    max_batch_size: int,
) -> list[list[tuple[int, int, int]]]:
    """Partition a legal serialization and forget each batch's internal order."""
    result: list[list[tuple[int, int, int]]] = []
    offset = 0
    while offset < len(events):
        width = int(rng.integers(1, min(max_batch_size, len(events) - offset) + 1))
        batch = events[offset : offset + width]
        rng.shuffle(batch)
        result.append(batch)
        offset += width
    return result


def atomic_validation_audit(
    schedules: list[list[np.ndarray]],
) -> int:
    """Exercise gap, duplicate, replay, split-pair, and order checks exactly."""
    label = next(label for label, values in enumerate(schedules[0]) if len(values) >= 2)
    checks = 0
    counts = np.zeros((len(schedules), len(schedules[0])), dtype=int)

    second = make_record(0, label, 2, schedules, signed=True)
    if accept_batch([second], counts, schedules, signed=True):
        raise AssertionError("a gap in the next-occurrence block was accepted")
    checks += 1

    first = make_record(0, label, 1, schedules, signed=True)
    if accept_batch([first, first], counts, schedules, signed=True):
        raise AssertionError("a duplicate occurrence tag was accepted")
    checks += 1

    split = replace(
        first,
        stream_ids=first.stream_ids[:1],
        physical_labels=first.physical_labels[:1],
        amplitudes=first.amplitudes[:1],
    )
    if accept_batch([split], counts, schedules, signed=True):
        raise AssertionError("a split signed pair was accepted")
    checks += 1

    wrong_stream = replace(first, stream_ids=(2, 3))
    if accept_batch([wrong_stream], counts, schedules, signed=True):
        raise AssertionError("a cross-column physical pair was accepted")
    checks += 1

    wrong_amplitude = replace(first, amplitudes=(first.amplitudes[0] * 1.01, first.amplitudes[1]))
    if accept_batch([wrong_amplitude], counts, schedules, signed=True):
        raise AssertionError("a physical amplitude mismatch was accepted")
    checks += 1

    if not accept_batch([second, first], counts, schedules, signed=True):
        raise AssertionError("an unordered gap-free two-occurrence block was rejected")
    checks += 1

    snapshot = counts.copy()
    if accept_batch([first], counts, schedules, signed=True):
        raise AssertionError("a replayed occurrence was accepted")
    if not np.array_equal(counts, snapshot):
        raise AssertionError("replay rejection was not atomic")
    checks += 1

    if accept_batch([], counts, schedules, signed=True):
        raise AssertionError("an empty batch was accepted")
    checks += 1
    return checks


def exhaustive_batch_state_audit(
    n: int,
    theta: float,
    eta: float,
    schedules: list[list[np.ndarray]],
) -> tuple[int, int, int]:
    """Exhaust every count state and every nonempty legal simultaneous jump."""
    response, degrees, _, envelope = response_data(n, theta, eta)
    contracts = [build_contract(degrees, column, theta, eta, envelope) for column in schedules]
    multiplicities = np.vstack([contract.multiplicities for contract in contracts])
    crossings = np.vstack([contract.crossing_indices for contract in contracts])
    gate = theta**2.5
    state_count = 0
    transition_count = 0
    max_crossings = 0
    state_ranges = [range(int(cap) + 1) for cap in multiplicities.ravel()]

    for flat_state in itertools.product(*state_ranges):
        counts = np.asarray(flat_state, dtype=int).reshape(multiplicities.shape)
        masses = np.zeros_like(counts, dtype=float)
        cumulative = np.zeros_like(counts, dtype=float)
        for column, contract in enumerate(contracts):
            masses[column] = [contract.prefixes[label][counts[column, label]] for label in range(n)]
            cumulative[column] = response @ masses[column]
        reported = counts >= crossings
        state_count += 1

        remaining = (multiplicities - counts).ravel()
        increment_ranges = [range(int(value) + 1) for value in remaining]
        for flat_increment in itertools.product(*increment_ranges):
            if not any(flat_increment):
                continue
            increments = np.asarray(flat_increment, dtype=int).reshape(multiplicities.shape)
            updated_counts = counts + increments
            updated = np.zeros_like(cumulative)
            for column, contract in enumerate(contracts):
                updated_masses = np.array(
                    [contract.prefixes[label][updated_counts[column, label]] for label in range(n)]
                )
                updated[column] = response @ updated_masses
                unreported = updated_counts[column] < contract.crossing_indices
                if np.any(updated[column, unreported] > (gate - contract.margin) * (1.0 + 3e-10)):
                    raise AssertionError("an exhaustive batch endpoint entered its band")

            expected_delta = (counts < crossings) & (updated_counts >= crossings)
            actual_delta = (~reported) & (updated > gate)
            if not np.array_equal(actual_delta, expected_delta):
                raise AssertionError("an exhaustive simultaneous jump has the wrong delta set")
            max_crossings = max(max_crossings, int(np.sum(expected_delta)))
            transition_count += 1
    return state_count, transition_count, max_crossings


def verify_batched_instance(
    n: int,
    theta: float,
    eta: float,
    schedules: list[list[np.ndarray]],
    batches: list[list[tuple[int, int, int]]],
    rng: np.random.Generator,
) -> BatchMetrics:
    """Verify atomic batches, endpoint deltas/certificates, and the full ledger."""
    response, degrees, kernel_norm, envelope = response_data(n, theta, eta)
    contracts = [build_contract(degrees, column, theta, eta, envelope) for column in schedules]
    logical_columns = len(contracts)
    multiplicities = np.vstack([contract.multiplicities for contract in contracts])
    crossings = np.vstack([contract.crossing_indices for contract in contracts])
    total_length = int(np.sum(multiplicities))
    total_mass = sum(contract.total_mass for contract in contracts)
    if not batches or sum(len(batch) for batch in batches) != total_length:
        raise ValueError("the batches do not contain the complete declared event family")

    gate = theta**2.5
    c_eta = (1.0 + eta) ** 2 * eta**2
    matching = theta**2 / (degrees * (1.0 + c_eta))
    max_tail_fraction = max(
        float(np.max(envelope * contract.mass_horizons / (matching * contract.gaps)))
        for contract in contracts
    )
    min_margin_fraction = min(contract.margin / gate for contract in contracts)
    counts = np.zeros_like(multiplicities)
    signed_counts = np.zeros_like(multiplicities)
    cumulative = np.zeros((logical_columns, n))
    prefix_masses = np.zeros(logical_columns)
    reported = np.zeros_like(multiplicities, dtype=bool)
    min_crossing_ratio = math.inf
    max_precrossing_ratio = 0.0
    affected_column_certificates = 0
    max_batch_size = 0
    mixed_column_batches = 0
    multicrossing_batches = 0
    jumped_cell_crossings = 0
    seen_unreported_boundaries = 0
    nonnegative_fragment_cells = 0
    signed_fragment_cells = 0
    nonnegative_absolute_mass = 0.0
    signed_absolute_mass = 0.0

    for tagged_batch in batches:
        nonnegative_batch = [
            make_record(column, label, occurrence, schedules, signed=False)
            for column, label, occurrence in tagged_batch
        ]
        signed_batch = [
            make_record(column, label, occurrence, schedules, signed=True)
            for column, label, occurrence in tagged_batch
        ]
        nonnegative_fragment_cells += sum(len(record.amplitudes) for record in nonnegative_batch)
        signed_fragment_cells += sum(len(record.amplitudes) for record in signed_batch)
        nonnegative_absolute_mass += sum(sum(record.amplitudes) for record in nonnegative_batch)
        signed_absolute_mass += sum(sum(record.amplitudes) for record in signed_batch)
        before_counts = counts.copy()
        before_response = cumulative.copy()
        before_reported = reported.copy()

        order_check = signed_counts.copy()
        reordered = signed_batch.copy()
        rng.shuffle(reordered)
        if not accept_batch(reordered, order_check, schedules, signed=True):
            raise AssertionError("an internal permutation of a valid batch was rejected")

        invalid_snapshot = signed_counts.copy()
        duplicate = signed_batch + [signed_batch[0]]
        if accept_batch(duplicate, signed_counts, schedules, signed=True):
            raise AssertionError("a duplicate tagged record was accepted")
        bad = replace(
            signed_batch[0],
            amplitudes=(signed_batch[0].amplitudes[0] * 1.01, signed_batch[0].amplitudes[1]),
        )
        if accept_batch([bad, *signed_batch[1:]], signed_counts, schedules, signed=True):
            raise AssertionError("a batch amplitude mismatch was accepted")
        if not np.array_equal(signed_counts, invalid_snapshot):
            raise AssertionError("an invalid batch changed persistent state")

        if not accept_batch(nonnegative_batch, counts, schedules, signed=False):
            raise AssertionError("a valid nonnegative simultaneous batch was rejected")
        if not accept_batch(signed_batch, signed_counts, schedules, signed=True):
            raise AssertionError("a valid signed simultaneous batch was rejected")
        if not np.array_equal(counts, signed_counts) or not np.array_equal(counts, order_check):
            raise AssertionError("batch order or physical mode changed the count endpoint")

        affected_columns = {column for column, _, _ in tagged_batch}
        affected_column_certificates += len(affected_columns)
        max_batch_size = max(max_batch_size, len(tagged_batch))
        if len(affected_columns) > 1:
            mixed_column_batches += 1

        increment = np.zeros_like(cumulative)
        cell_widths: dict[tuple[int, int], int] = {}
        for column, label, occurrence in tagged_batch:
            amplitude = float(schedules[column][label][occurrence - 1])
            increment[column] += amplitude * response[:, label]
            prefix_masses[column] += amplitude
            cell_widths[(column, label)] = cell_widths.get((column, label), 0) + 1
        cumulative += increment
        for column in range(logical_columns):
            if column not in affected_columns and not np.array_equal(
                cumulative[column], before_response[column]
            ):
                raise AssertionError("a batch changed an unaffected response column")

        expected_delta = (before_counts < crossings) & (counts >= crossings)
        actual_delta = (~before_reported) & (cumulative > gate)
        if not np.array_equal(actual_delta, expected_delta):
            raise AssertionError("the exact and certified batch-boundary deltas differ")
        delta_count = int(np.sum(expected_delta))
        if delta_count > 1:
            multicrossing_batches += 1
        for column, label in np.argwhere(expected_delta):
            pre_ratio = before_response[column, label] / (gate - contracts[column].margin)
            max_precrossing_ratio = max(max_precrossing_ratio, float(pre_ratio))
            if pre_ratio > 1.0 + 3e-10:
                raise AssertionError("a cell was already in-band before its crossing batch")
            min_crossing_ratio = min(
                min_crossing_ratio,
                float(cumulative[column, label] / gate),
            )
            if cell_widths[(int(column), int(label))] > 1:
                jumped_cell_crossings += 1
        reported |= expected_delta

        for column, contract in enumerate(contracts):
            masses = np.array(
                [contract.prefixes[label][counts[column, label]] for label in range(n)]
            )
            lower = matching * masses
            upper = lower + envelope * prefix_masses[column]
            tolerance = 3e-10 * np.maximum(upper, gate)
            if np.any(cumulative[column] + tolerance < lower):
                raise AssertionError("a batch response violated its lower envelope")
            if np.any(cumulative[column] > upper + tolerance):
                raise AssertionError("a batch response violated its upper envelope")
            unreported = counts[column] < contract.crossing_indices
            if np.any(cumulative[column, unreported] > (gate - contract.margin) * (1.0 + 3e-10)):
                raise AssertionError("an unreported batch endpoint entered its band")
            if np.any(prefix_masses[column] > contract.mass_horizons[unreported] * (1 + 3e-13)):
                raise AssertionError("a batch endpoint exceeded its local mass horizon")
            if np.any((counts[column] > 0) & unreported):
                seen_unreported_boundaries += 1

        if not np.array_equal(reported, counts >= crossings):
            raise AssertionError("reported membership differs from batch endpoint counts")

    if not np.array_equal(counts, multiplicities) or not np.all(reported):
        raise AssertionError("the completed batch family missed a declared crossing")
    if not math.isclose(float(np.sum(prefix_masses)), total_mass, rel_tol=3e-14):
        raise AssertionError("the batch and declared logical masses differ")

    batch_count = len(batches)
    delta_records = logical_columns * n
    certificate_records = affected_column_certificates
    if not batch_count <= certificate_records <= total_length:
        raise AssertionError("the affected-column certificate ledger is inconsistent")
    if delta_records > total_length:
        raise AssertionError("complete schedules do not dominate the delta count")
    if nonnegative_fragment_cells != total_length:
        raise AssertionError("the nonnegative physical fragment ledger is inconsistent")
    if signed_fragment_cells != 2 * total_length:
        raise AssertionError("the signed physical fragment ledger is inconsistent")
    if not math.isclose(nonnegative_absolute_mass, total_mass, rel_tol=2e-15):
        raise AssertionError("the nonnegative absolute physical mass is inconsistent")
    if not math.isclose(signed_absolute_mass, 3.0 * total_mass, rel_tol=2e-15):
        raise AssertionError("the signed absolute physical mass is inconsistent")

    final_snapshot = signed_counts.copy()
    replay = make_record(0, 0, 1, schedules, signed=True)
    if accept_batch([replay], signed_counts, schedules, signed=True):
        raise AssertionError("a post-completion replay batch was accepted")
    if not np.array_equal(signed_counts, final_snapshot):
        raise AssertionError("post-completion rejection changed state")

    delayed_crossings = int(np.sum(crossings > 1))
    return BatchMetrics(
        kernel_norm=kernel_norm,
        max_tail_fraction=max_tail_fraction,
        min_margin_fraction=min_margin_fraction,
        min_crossing_ratio=min_crossing_ratio,
        max_precrossing_ratio=max_precrossing_ratio,
        batches=batch_count,
        affected_column_certificates=certificate_records,
        max_batch_size=max_batch_size,
        mixed_column_batches=mixed_column_batches,
        multicrossing_batches=multicrossing_batches,
        jumped_cell_crossings=jumped_cell_crossings,
        delayed_crossings=delayed_crossings,
        seen_unreported_boundaries=seen_unreported_boundaries,
    )


def parse_args() -> argparse.Namespace:
    """Parse the reproducible audit controls."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--max-n", type=int, default=24)
    parser.add_argument("--max-multiplicity", type=int, default=6)
    parser.add_argument("--max-columns", type=int, default=4)
    parser.add_argument("--max-batch-size", type=int, default=16)
    return parser.parse_args()


def main() -> None:
    """Run exhaustive small-state and randomized full-template audits."""
    args = parse_args()
    if (
        args.max_n < 5
        or args.max_multiplicity < 2
        or args.max_columns < 2
        or args.max_batch_size < 2
    ):
        raise ValueError(
            "require max-n >= 5, max-multiplicity >= 2, max-columns >= 2, max-batch-size >= 2"
        )
    rng = np.random.default_rng(args.seed)
    eta = 0.1
    c_eta = (1.0 + eta) ** 2 * eta**2

    exhaustive_n = 5
    exhaustive_theta = 1.0e-6
    degrees = notched_double_sun(exhaustive_n).sum(axis=1)[:exhaustive_n]
    capacities = degrees * (1.0 + c_eta) * math.sqrt(exhaustive_theta)
    exhaustive_schedules: list[list[np.ndarray]] = []
    for column in range(2):
        column_schedules: list[np.ndarray] = []
        for label, capacity in enumerate(capacities):
            if label == 0:
                first = (0.25 + 0.03 * column) * capacity
                total = (1.10 + 0.05 * column) * capacity
                column_schedules.append(np.array([first, total - first]))
            else:
                column_schedules.append(
                    np.array([(1.08 + 0.04 * column + 0.005 * label) * capacity])
                )
        exhaustive_schedules.append(column_schedules)
    atomic_checks = atomic_validation_audit(exhaustive_schedules)
    states, transitions, exhaustive_max_crossings = exhaustive_batch_state_audit(
        exhaustive_n,
        exhaustive_theta,
        eta,
        exhaustive_schedules,
    )
    if states != 2304 or transitions != 233892 or exhaustive_max_crossings != 10:
        raise AssertionError("the exhaustive simultaneous-transition cardinalities changed")

    max_kernel_norm = 0.0
    max_tail_fraction = 0.0
    min_margin_fraction = math.inf
    min_crossing_ratio = math.inf
    max_precrossing_ratio = 0.0
    total_batches = 0
    total_certificates = 0
    largest_batch = 0
    mixed_batches = 0
    multicrossing_batches = 0
    jumped_crossings = 0
    delayed_crossings = 0
    seen_unreported = 0
    largest_total_length = 0
    largest_total_mass = 0.0

    instances: list[tuple[int, float, int, bool, bool]] = [(5, 1.0e-6, 3, True, True)]
    for _ in range(args.trials):
        n = int(rng.integers(5, args.max_n + 1))
        columns = int(rng.integers(2, args.max_columns + 1))
        theta = float(rng.uniform(0.15, 0.95) / (40000.0 * n * columns))
        instances.append((n, theta, columns, False, False))

    for n, theta, columns, all_delayed, one_batch in instances:
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
        contracts = [build_contract(degrees, column, theta, eta, envelope) for column in schedules]
        multiplicities = np.vstack([contract.multiplicities for contract in contracts])
        events = tagged_events(multiplicities, rng)
        batches = [events] if one_batch else partition_events(events, rng, args.max_batch_size)
        metrics = verify_batched_instance(n, theta, eta, schedules, batches, rng)

        max_kernel_norm = max(max_kernel_norm, metrics.kernel_norm)
        max_tail_fraction = max(max_tail_fraction, metrics.max_tail_fraction)
        min_margin_fraction = min(min_margin_fraction, metrics.min_margin_fraction)
        min_crossing_ratio = min(min_crossing_ratio, metrics.min_crossing_ratio)
        max_precrossing_ratio = max(max_precrossing_ratio, metrics.max_precrossing_ratio)
        total_batches += metrics.batches
        total_certificates += metrics.affected_column_certificates
        largest_batch = max(largest_batch, metrics.max_batch_size)
        mixed_batches += metrics.mixed_column_batches
        multicrossing_batches += metrics.multicrossing_batches
        jumped_crossings += metrics.jumped_cell_crossings
        delayed_crossings += metrics.delayed_crossings
        seen_unreported += metrics.seen_unreported_boundaries
        largest_total_length = max(largest_total_length, len(events))
        largest_total_mass = max(
            largest_total_mass,
            sum(contract.total_mass for contract in contracts),
        )

    print(
        f"seed={args.seed} trials={args.trials} max_n={args.max_n} "
        f"max_multiplicity={args.max_multiplicity} max_columns={args.max_columns} "
        f"max_batch_size={args.max_batch_size} eta={eta}"
    )
    print(f"exhaustive count states={states}")
    print(f"exhaustive legal nonempty batch transitions={transitions}")
    print(f"exhaustive maximum simultaneous crossings={exhaustive_max_crossings}")
    print(f"atomic rejection/order checks={atomic_checks}")
    print(f"largest sampled logical length={largest_total_length}")
    print(f"largest sampled total logical mass={largest_total_mass:.6e}")
    print(f"accepted batch interactions={total_batches}")
    print(f"affected-column certificate records={total_certificates}")
    print(f"largest accepted batch={largest_batch}")
    print(f"mixed-column batches={mixed_batches}")
    print(f"multiple-crossing batches={multicrossing_batches}")
    print(f"crossings inside multi-occurrence cell jumps={jumped_crossings}")
    print(f"delayed declared crossings={delayed_crossings}")
    print(f"batch boundaries with a seen-but-unreported cell={seen_unreported}")
    print(f"max Neumann-kernel norm={max_kernel_norm:.6e}")
    print(f"max local-future-tail/gap fraction={max_tail_fraction:.6e}")
    print(f"min per-column band/gate fraction={min_margin_fraction:.6e}")
    print(f"min certified batch-crossing/gate ratio={min_crossing_ratio:.6e}")
    print(f"max pre-batch response/(column gate-band)={max_precrossing_ratio:.6e}")
    print("all simultaneous-batch certificate, atomicity, and ledger checks passed")


if __name__ == "__main__":
    main()
