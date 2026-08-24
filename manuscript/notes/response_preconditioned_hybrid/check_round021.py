#!/usr/bin/env python3
"""Exact audit for the Round-021 pivot and co-side Gram refresh results."""

from __future__ import annotations

import argparse
import math
import random
from fractions import Fraction

Vector = tuple[Fraction, ...]
Rows = tuple[Vector, ...]
ThreeState = tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
DecoderState = tuple[Fraction, Fraction, Fraction, Fraction]
GramKey = tuple[int, int]
GramState = dict[GramKey, Fraction]


def dot(left: Vector, right: Vector) -> Fraction:
    """Return an exact inner product."""
    if len(left) != len(right):
        raise AssertionError("inner-product widths differ")
    return sum((x * y for x, y in zip(left, right, strict=True)), Fraction(0))


def add_vectors(*vectors: Vector) -> Vector:
    """Return an exact vector sum."""
    if not vectors:
        return ()
    width = len(vectors[0])
    if any(len(vector) != width for vector in vectors):
        raise AssertionError("vector-sum widths differ")
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))


def scale(weight: Fraction, vector: Vector) -> Vector:
    """Scale a vector exactly."""
    return tuple(weight * entry for entry in vector)


def squared_norm(vector: Vector) -> Fraction:
    """Return the exact squared Euclidean norm."""
    return dot(vector, vector)


def concatenate_rows(old_rows: Rows, new_rows: Rows) -> Rows:
    """Concatenate a new source block to each existing label row."""
    if len(old_rows) != len(new_rows):
        raise AssertionError("row counts differ")
    return tuple(old + new for old, new in zip(old_rows, new_rows, strict=True))


def three_label_state(rows: Rows) -> ThreeState:
    """Return the canonical unweighted pivot state for codes 00, 01, 10."""
    if len(rows) != 3:
        raise AssertionError("the pivot state requires exactly three rows")
    z0, z1, z2 = rows
    return (
        squared_norm(z0),
        squared_norm(z1),
        squared_norm(add_vectors(z0, z2)),
        squared_norm(z2),
        squared_norm(add_vectors(z0, z1)),
    )


def pivot_refresh(state: ThreeState, weights: tuple[Fraction, Fraction, Fraction]) -> DecoderState:
    """Refresh the four decoder norms from the five canonical scalars."""
    p0, a1, c1, a2, c2 = state
    w0, w1, w2 = weights
    g02 = (c1 - p0 - a2) / 2
    g01 = (c2 - p0 - a1) / 2
    return (
        w1**2 * a1,
        w0**2 * p0 + w2**2 * a2 + 2 * w0 * w2 * g02,
        w2**2 * a2,
        w0**2 * p0 + w1**2 * a1 + 2 * w0 * w1 * g01,
    )


def direct_decoder(rows: Rows, weights: tuple[Fraction, ...], bit_count: int) -> DecoderState:
    """Compute the two-bit decoder norms directly from weighted rows."""
    if bit_count != 2 or len(rows) not in (3, 4):
        raise AssertionError("this helper audits only the two-bit witnesses")
    records: list[Fraction] = []
    for bit in range(bit_count):
        ones = [scale(weights[index], row) for index, row in enumerate(rows) if (index >> bit) & 1]
        zeros = [
            scale(weights[index], row) for index, row in enumerate(rows) if not ((index >> bit) & 1)
        ]
        records.extend((squared_norm(add_vectors(*ones)), squared_norm(add_vectors(*zeros))))
    return tuple(records)  # type: ignore[return-value]


def weighted_append_measurements(
    rows: Rows, weights: tuple[Fraction, Fraction, Fraction]
) -> tuple[Vector, Vector, Vector]:
    """Form the ordinary total and two bit measurements for one new block."""
    z0, z1, z2 = rows
    w0, w1, w2 = weights
    m1 = scale(w1, z1)
    m2 = scale(w2, z2)
    m0 = add_vectors(scale(w0, z0), m1, m2)
    return m0, m1, m2


def recover_unweighted_append(
    measurements: tuple[Vector, Vector, Vector],
    weights: tuple[Fraction, Fraction, Fraction],
) -> Rows:
    """Recover the three unweighted rows before updating canonical state."""
    m0, m1, m2 = measurements
    w0, w1, w2 = weights
    if min(weights) <= 0:
        raise AssertionError("refresh weights must be positive")
    z1 = scale(1 / w1, m1)
    z2 = scale(1 / w2, m2)
    z0 = scale(1 / w0, add_vectors(m0, scale(-1, m1), scale(-1, m2)))
    return z0, z1, z2


def add_three_states(left: ThreeState, right: ThreeState) -> ThreeState:
    """Add canonical increments from disjoint source-coordinate blocks."""
    return tuple(a + b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def random_rows(rng: random.Random, count: int, width: int) -> Rows:
    """Draw small exact-rational rows."""
    return tuple(
        tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(width))
        for _ in range(count)
    )


def random_weights(rng: random.Random, count: int) -> tuple[Fraction, ...]:
    """Draw strictly positive exact-rational row weights."""
    return tuple(Fraction(rng.randint(1, 9), rng.randint(1, 5)) for _ in range(count))


def audit_three_label_refreshes(rng: random.Random, trials: int) -> int:
    """Check two genuine refreshes and two weighted appends per history."""
    unit = (Fraction(1), Fraction(1), Fraction(1))
    first = (Fraction(1), Fraction(3), Fraction(2))
    second = (Fraction(1), Fraction(1), Fraction(4))
    refresh_checks = 0

    for _ in range(trials):
        rows = random_rows(rng, 3, rng.randint(1, 5))
        state = three_label_state(rows)
        if pivot_refresh(state, unit) != direct_decoder(rows, unit, 2):
            raise AssertionError("the canonical unit-weight decoder is wrong")

        for weights in (first, second):
            if pivot_refresh(state, weights) != direct_decoder(rows, weights, 2):
                raise AssertionError("a named pivot refresh is not exact")
            refresh_checks += 1

            append_rows = random_rows(rng, 3, rng.randint(1, 5))
            measurements = weighted_append_measurements(append_rows, weights)
            recovered = recover_unweighted_append(measurements, weights)
            if recovered != append_rows:
                raise AssertionError("a weighted append was not converted to canonical rows")
            state = add_three_states(state, three_label_state(recovered))
            rows = concatenate_rows(rows, append_rows)
            if state != three_label_state(rows):
                raise AssertionError("canonical append increments did not accumulate exactly")
            if pivot_refresh(state, weights) != direct_decoder(rows, weights, 2):
                raise AssertionError("the post-append decoder is not exact")

        arbitrary = random_weights(rng, 3)
        if pivot_refresh(state, arbitrary) != direct_decoder(rows, arbitrary, 2):
            raise AssertionError("an arbitrary positive refresh is not exact")
        refresh_checks += 1

    refresh_vector = (0, 0, 1, 0, 1, 0, 0, 1, 1, 4, 1)
    if len(refresh_vector) != 11:
        raise AssertionError("the Round-021 refresh vector is not eleven-dimensional")
    if refresh_vector[6] != 0 or refresh_vector[9:] != (4, 1):
        raise AssertionError("the four-write/one-output refresh ledger changed")
    return refresh_checks


def audit_four_label_stop() -> None:
    """Verify the exact one-pivot four-label indistinguishability witness."""
    left: Rows = tuple((Fraction(value),) for value in (-6, -5, -5, 4))
    right: Rows = tuple((Fraction(value),) for value in (-6, -5, -5, 6))
    unit = (Fraction(1),) * 4
    refreshed = (Fraction(1), Fraction(1), Fraction(1), Fraction(3))

    left_old = direct_decoder(left, unit, 2)
    right_old = direct_decoder(right, unit, 2)
    if left_old != (Fraction(1), Fraction(121), Fraction(1), Fraction(121)):
        raise AssertionError("the four-label witness has the wrong old decoder state")
    if left_old != right_old or squared_norm(left[0]) != squared_norm(right[0]):
        raise AssertionError("the histories are distinguishable in the named five-cell state")

    left_new = direct_decoder(left, refreshed, 2)
    right_new = direct_decoder(right, refreshed, 2)
    if left_new[:2] != (Fraction(49), Fraction(121)):
        raise AssertionError("the first refreshed comparison is not 49 versus 121")
    if right_new[:2] != (Fraction(169), Fraction(121)):
        raise AssertionError("the second refreshed comparison is not 169 versus 121")
    if not (left_new[0] < left_new[1] and right_new[0] > right_new[1]):
        raise AssertionError("the exact first-bit decision did not flip")


def codes_share_side(first: int, second: int, bit_count: int) -> bool:
    """Return whether two codes occur together on at least one bit side."""
    return any(((first >> bit) & 1) == ((second >> bit) & 1) for bit in range(bit_count))


def co_side_state(rows: Rows, codes: tuple[int, ...], bit_count: int) -> GramState:
    """Build the exact canonical co-side Gram state."""
    state: GramState = {}
    for index, row in enumerate(rows):
        state[index, index] = squared_norm(row)
    for first in range(len(rows)):
        for second in range(first + 1, len(rows)):
            if codes_share_side(codes[first], codes[second], bit_count):
                state[first, second] = dot(rows[first], rows[second])
    return state


def reconstruct_co_side_norms(
    state: GramState,
    codes: tuple[int, ...],
    weights: tuple[Fraction, ...],
    bit_count: int,
) -> tuple[tuple[Fraction, Fraction], ...]:
    """Reconstruct every weighted bit-side norm from co-side entries."""
    records: list[tuple[Fraction, Fraction]] = []
    for bit in range(bit_count):
        sides: list[Fraction] = []
        for side in (1, 0):
            members = [index for index, code in enumerate(codes) if ((code >> bit) & 1) == side]
            value = sum(
                (weights[index] ** 2 * state[index, index] for index in members), Fraction(0)
            )
            for offset, first in enumerate(members):
                for second in members[offset + 1 :]:
                    key = (min(first, second), max(first, second))
                    value += 2 * weights[first] * weights[second] * state[key]
            sides.append(value)
        records.append((sides[0], sides[1]))
    return tuple(records)


def direct_side_norms(
    rows: Rows,
    codes: tuple[int, ...],
    weights: tuple[Fraction, ...],
    bit_count: int,
) -> tuple[tuple[Fraction, Fraction], ...]:
    """Compute every weighted bit-side norm directly."""
    records: list[tuple[Fraction, Fraction]] = []
    for bit in range(bit_count):
        sides: list[Fraction] = []
        for side in (1, 0):
            vectors = [
                scale(weights[index], rows[index])
                for index, code in enumerate(codes)
                if ((code >> bit) & 1) == side
            ]
            sides.append(squared_norm(add_vectors(*vectors)) if vectors else Fraction(0))
        records.append((sides[0], sides[1]))
    return tuple(records)


def add_gram_states(left: GramState, right: GramState) -> GramState:
    """Add Gram increments from disjoint source blocks."""
    if left.keys() != right.keys():
        raise AssertionError("co-side state keys differ")
    return {key: left[key] + right[key] for key in left}


def coefficient_rank(matrix: list[list[Fraction]]) -> int:
    """Compute exact row rank by Gaussian elimination."""
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next((row for row in range(pivot_row, row_count) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale_factor = work[pivot_row][column]
        work[pivot_row] = [entry / scale_factor for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def audit_measurement_deficiency() -> None:
    """Check a representative k>L+1 ordinary coded measurement map."""
    bit_count = 3
    codes = tuple(range(8))
    matrix = [[Fraction(1) for _ in codes]]
    matrix.extend([Fraction((code >> bit) & 1) for code in codes] for bit in range(bit_count))
    rank = coefficient_rank(matrix)
    if rank > bit_count + 1 or rank >= len(codes):
        raise AssertionError("the ordinary coded block unexpectedly identifies every row")


def audit_co_side_reconstruction(rng: random.Random, trials: int) -> tuple[int, int]:
    """Check arbitrary-code reconstruction, dimension, and append updates."""
    checked = 0
    largest_dimension = 0
    for _ in range(max(1, trials // 3)):
        bit_count = rng.randint(1, 5)
        universe_size = 1 << bit_count
        label_count = rng.randint(1, min(universe_size, 10))
        codes = tuple(rng.sample(range(universe_size), label_count))
        rows = random_rows(rng, label_count, rng.randint(1, 6))
        weights = random_weights(rng, label_count)
        state = co_side_state(rows, codes, bit_count)

        complement_pairs = sum(
            1
            for first in range(label_count)
            for second in range(first + 1, label_count)
            if codes[first] ^ codes[second] == universe_size - 1
        )
        expected_dimension = label_count + math.comb(label_count, 2) - complement_pairs
        if len(state) != expected_dimension:
            raise AssertionError("the co-side state has the wrong exact dimension")
        if complement_pairs > label_count // 2:
            raise AssertionError("complement pairs do not form a matching")

        reconstructed = reconstruct_co_side_norms(state, codes, weights, bit_count)
        direct = direct_side_norms(rows, codes, weights, bit_count)
        if reconstructed != direct:
            raise AssertionError("co-side state did not reconstruct every decoder norm")

        appended = random_rows(rng, label_count, rng.randint(1, 5))
        updated = add_gram_states(state, co_side_state(appended, codes, bit_count))
        combined = concatenate_rows(rows, appended)
        if updated != co_side_state(combined, codes, bit_count):
            raise AssertionError("co-side Gram append increments are not exact")
        if reconstruct_co_side_norms(updated, codes, weights, bit_count) != direct_side_norms(
            combined, codes, weights, bit_count
        ):
            raise AssertionError("the post-append co-side decoder is not exact")

        largest_dimension = max(largest_dimension, expected_dimension)
        checked += 1

    audit_measurement_deficiency()
    return checked, largest_dimension


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260822)
    parser.add_argument("--trials", type=int, default=2000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trials < 1:
        raise ValueError("--trials must be positive")
    rng = random.Random(args.seed)
    refresh_checks = audit_three_label_refreshes(rng, args.trials)
    audit_four_label_stop()
    co_side_checks, largest_dimension = audit_co_side_reconstruction(rng, args.trials)
    print(f"seed={args.seed} trials={args.trials}")
    print(
        f"three-label exact refresh checks={refresh_checks}; "
        f"weighted append traces={2 * args.trials}"
    )
    print("four-label one-pivot STOP: common (P0,A1,C1,A2,C2)=(36,1,121,1,121)")
    print("refreshed first bit=49<121 versus 169>121")
    print(
        f"co-side exact reconstruction/append checks={co_side_checks}; "
        f"largest sampled state dimension={largest_dimension}"
    )
    print("ordinary k>L+1 measurement-rank deficiency checked exactly")
    print("all exact Round-021 pivot and co-side Gram checks passed")


if __name__ == "__main__":
    main()
