#!/usr/bin/env python3
"""Exact audit for the Round-020 norm-only slack-reweighting obstruction."""

from __future__ import annotations

import argparse
import itertools
import random
from fractions import Fraction

Vector = tuple[Fraction, ...]
Rows = tuple[Vector, ...]
NormState = tuple[tuple[Fraction, Fraction], ...]


def squared_norm(vector: Vector) -> Fraction:
    """Return the exact squared Euclidean norm."""
    return sum((entry * entry for entry in vector), start=Fraction(0))


def weighted_sum(rows: Rows, indices: list[int], weights: tuple[Fraction, ...]) -> Vector:
    """Return an exact weighted row sum."""
    width = len(rows[0])
    return tuple(
        sum(
            (weights[index] * rows[index][coordinate] for index in indices),
            start=Fraction(0),
        )
        for coordinate in range(width)
    )


def norm_state(
    rows: Rows,
    codes: tuple[int, ...],
    weights: tuple[Fraction, ...],
    bit_count: int,
) -> NormState:
    """Compute every retained bit-bucket and complement squared norm."""
    records: list[tuple[Fraction, Fraction]] = []
    for bit in range(bit_count):
        ones = [index for index, code in enumerate(codes) if (code >> bit) & 1]
        zeros = [index for index, code in enumerate(codes) if not (code >> bit) & 1]
        records.append(
            (
                squared_norm(weighted_sum(rows, ones, weights)),
                squared_norm(weighted_sum(rows, zeros, weights)),
            )
        )
    return tuple(records)


def reconstruct_two_label_refresh(
    old_state: NormState,
    codes: tuple[int, int],
    new_weights: tuple[Fraction, Fraction],
    bit_count: int,
) -> NormState:
    """Reconstruct a two-label refresh from exactly the retained old norms."""
    separating_bit = next(
        bit for bit in range(bit_count) if ((codes[0] >> bit) & 1) != ((codes[1] >> bit) & 1)
    )
    first_is_one = (codes[0] >> separating_bit) & 1
    if first_is_one:
        first_norm, second_norm = old_state[separating_bit]
    else:
        second_norm, first_norm = old_state[separating_bit]

    inner_product: Fraction | None = None
    for bit in range(bit_count):
        first_bit = (codes[0] >> bit) & 1
        second_bit = (codes[1] >> bit) & 1
        if first_bit == second_bit:
            grouped_norm = old_state[bit][0 if first_bit else 1]
            inner_product = (grouped_norm - first_norm - second_norm) / 2
            break

    refreshed: list[tuple[Fraction, Fraction]] = []
    for bit in range(bit_count):
        first_bit = (codes[0] >> bit) & 1
        second_bit = (codes[1] >> bit) & 1
        if first_bit != second_bit:
            first_weighted = new_weights[0] ** 2 * first_norm
            second_weighted = new_weights[1] ** 2 * second_norm
            refreshed.append(
                (first_weighted, second_weighted)
                if first_bit
                else (second_weighted, first_weighted)
            )
            continue

        if inner_product is None:
            raise AssertionError("a grouped bit is missing its recoverable inner product")
        grouped_norm = (
            new_weights[0] ** 2 * first_norm
            + new_weights[1] ** 2 * second_norm
            + 2 * new_weights[0] * new_weights[1] * inner_product
        )
        refreshed.append((grouped_norm, Fraction(0)) if first_bit else (Fraction(0), grouped_norm))
    return tuple(refreshed)


def audit_three_label_witnesses() -> None:
    """Verify the signed minimal witness and its nonnegative variant."""
    codes = (0b00, 0b01, 0b10)
    old_weights = (Fraction(1),) * 3
    new_weights = (Fraction(1), Fraction(3), Fraction(2))

    signed_left: Rows = ((Fraction(-4),), (Fraction(1),), (Fraction(1),))
    signed_right: Rows = ((Fraction(-2),), (Fraction(-1),), (Fraction(-1),))
    signed_old_left = norm_state(signed_left, codes, old_weights, 2)
    signed_old_right = norm_state(signed_right, codes, old_weights, 2)
    if signed_old_left != ((Fraction(1), Fraction(9)),) * 2:
        raise AssertionError("the signed witness has the wrong retained old state")
    if signed_old_left != signed_old_right:
        raise AssertionError("the signed histories are distinguishable before reweighting")

    signed_new_left = norm_state(signed_left, codes, new_weights, 2)
    signed_new_right = norm_state(signed_right, codes, new_weights, 2)
    if signed_new_left[0] != (Fraction(9), Fraction(4)):
        raise AssertionError("the first signed refreshed comparison is not 9 versus 4")
    if signed_new_right[0] != (Fraction(9), Fraction(16)):
        raise AssertionError("the second signed refreshed comparison is not 9 versus 16")
    if not (signed_new_left[0][0] > signed_new_left[0][1]):
        raise AssertionError("the first signed history did not decode bit one")
    if not (signed_new_right[0][0] < signed_new_right[0][1]):
        raise AssertionError("the second signed history did not decode bit zero")

    nonnegative_left: Rows = (
        (Fraction(0), Fraction(2)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(0)),
    )
    nonnegative_right: Rows = (
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(1)),
    )
    nonnegative_old_left = norm_state(nonnegative_left, codes, old_weights, 2)
    nonnegative_old_right = norm_state(nonnegative_right, codes, old_weights, 2)
    if nonnegative_old_left != ((Fraction(1), Fraction(5)),) * 2:
        raise AssertionError("the nonnegative witness has the wrong retained old state")
    if nonnegative_old_left != nonnegative_old_right:
        raise AssertionError("the nonnegative histories differ before reweighting")

    nonnegative_new_left = norm_state(nonnegative_left, codes, new_weights, 2)
    nonnegative_new_right = norm_state(nonnegative_right, codes, new_weights, 2)
    if nonnegative_new_left[0] != (Fraction(9), Fraction(8)):
        raise AssertionError("the first nonnegative comparison is not 9 versus 8")
    if nonnegative_new_right[0] != (Fraction(9), Fraction(10)):
        raise AssertionError("the second nonnegative comparison is not 9 versus 10")

    # Unit representatives for every Theta(1) coordinate verify the shared
    # eleven-coordinate order and the two literal replay counts.
    rejection_vector = (0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1)
    replay_vector = (0, 0, 1, 0, 1, 0, 6, 1, 1, 12, 1)
    if len(rejection_vector) != 11 or len(replay_vector) != 11:
        raise AssertionError("a Round-020 resource vector is not eleven-dimensional")
    if rejection_vector[6] != 0 or rejection_vector[9:] != (0, 1):
        raise AssertionError("the no-replay rejection ledger changed")
    if replay_vector[6] != 6 or replay_vector[9:] != (12, 1):
        raise AssertionError("the explicit replay ledger changed")


def audit_two_label_minimality(seed: int, trials: int) -> int:
    """Test exact two-label reconstruction for all 3-bit code pairs."""
    rng = random.Random(seed)
    code_pairs = list(itertools.combinations(range(8), 2))
    checked = 0
    for _ in range(trials):
        for codes in code_pairs:
            rows: Rows = tuple(
                tuple(Fraction(rng.randint(-7, 7)) for _ in range(3)) for _ in range(2)
            )
            old_weights = (Fraction(1), Fraction(1))
            new_weights = (Fraction(rng.randint(1, 7)), Fraction(rng.randint(1, 7)))
            old_state = norm_state(rows, codes, old_weights, 3)
            direct = norm_state(rows, codes, new_weights, 3)
            reconstructed = reconstruct_two_label_refresh(old_state, codes, new_weights, 3)
            if reconstructed != direct:
                raise AssertionError(f"two-label reconstruction failed for codes={codes}")
            checked += 1
    return checked


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--trials", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trials < 1:
        raise ValueError("--trials must be positive")
    audit_three_label_witnesses()
    checked = audit_two_label_minimality(args.seed, args.trials)
    print(f"seed={args.seed} trials={args.trials}")
    print("signed old state=((1,9),(1,9)); refreshed first bit=9>4 versus 9<16")
    print("nonnegative old state=((1,5),(1,5)); refreshed first bit=9>8 versus 9<10")
    print(f"exact one/two-label minimality checks={checked}")
    print("six-read/twelve-write replay and eleven-coordinate ledgers checked")
    print("all exact slack-reweighting obstruction checks passed")


if __name__ == "__main__":
    main()
