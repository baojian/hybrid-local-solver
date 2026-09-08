"""Exact categorical sampling from fair bits with a bounded failure event.

No common denominator or uniformly random real is supplied as a primitive.
Arithmetic is charged in the exact-real word model, not bit complexity.
Exhaustive dyadic interval partitions are independent audit work.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import time


@dataclass
class Draw:
    category: int | None
    bits: int
    numerator: int
    denominator: int


class Categorical:
    def __init__(self, weights, work):
        assert len(weights) > 0
        self.work, self.prefix, self.total = work, [], F(0)
        for weight in weights:
            assert weight > 0
            self.total += weight
            self.prefix.append(self.total)
            work["input_checks_prefix_arithmetic_and_copy_budget"] += 6
        work["categorical_header_words"] += 3

    def category_above(self, numerator, denominator):
        """First prefix strictly above the lower dyadic endpoint."""
        lo, hi = 0, len(self.prefix)
        lower = numerator * self.total
        self.work["lower_endpoint_multiplications"] += 1
        while lo < hi:
            middle = (lo + hi) // 2
            if self.prefix[middle] * denominator <= lower:
                lo = middle + 1
            else:
                hi = middle
            self.work["cdf_search_arithmetic_reads_and_comparisons"] += 7
        assert lo < len(self.prefix)
        return lo

    def draw(self, fair_bit, max_bits):
        assert max_bits >= 0
        numerator, denominator = 0, 1
        self.work["draw_state_words_and_setup"] += 5
        for used in range(max_bits + 1):
            category = self.category_above(numerator, denominator)
            contained = (numerator + 1) * self.total <= self.prefix[category] * denominator
            self.work["upper_endpoint_arithmetic_reads_and_comparisons"] += 6
            if contained:
                self.work["sample_output_record_words"] += 4
                return Draw(category, used, numerator, denominator)
            if used == max_bits:
                self.work["sample_output_record_words"] += 4
                self.work["ambiguous_capped_draws"] += 1
                return Draw(None, used, numerator, denominator)
            bit = fair_bit()
            assert bit in (0, 1)
            numerator, denominator = 2 * numerator + bit, 2 * denominator
            self.work["independent_fair_bits_consumed"] += 1
            self.work["dyadic_state_arithmetic_and_bit_checks"] += 6
        raise AssertionError("unreachable")

    def cap(self, draws, delta):
        assert draws >= 0 and 0 < delta < 1
        if len(self.prefix) == 1 or draws == 0:
            return 0
        target = F((len(self.prefix) - 1) * draws) / delta
        scale, bits = 1, 0
        self.work["cap_budget_setup_operations"] += 5
        while scale < target:
            scale *= 2
            bits += 1
            self.work["cap_budget_doubling_and_comparison_operations"] += 4
        return bits


class BitTape:
    """Finite validator input, never a producer-side random-real oracle."""

    def __init__(self, value, length):
        self.value, self.length, self.used = value, length, 0

    def bit(self):
        assert self.used < self.length
        self.used += 1
        return (self.value >> (self.length - self.used)) & 1


def intersections(weights, lower, upper):
    """Independent exact interval-overlap classifier; scans all categories."""
    total, previous, result = sum(weights), F(0), []
    for category, weight in enumerate(weights):
        boundary = previous + weight / total
        if lower < boundary and upper > previous:
            result.append(category)
        previous = boundary
    assert previous == 1
    return result


def validate_draw(weights, tape, draw, cap, counts):
    assert draw.bits == tape.used and draw.bits <= cap
    assert draw.numerator == tape.value >> (tape.length - tape.used)
    assert draw.denominator == 2**draw.bits
    lower, upper = F(draw.numerator, draw.denominator), F(draw.numerator + 1, draw.denominator)
    overlap = intersections(weights, lower, upper)
    if draw.category is None:
        assert draw.bits == cap and len(overlap) >= 2
        counts["validated_ambiguous_terminal_intervals"] += 1
    else:
        assert overlap == [draw.category]
        counts["validated_categorical_terminal_intervals"] += 1
    counts["independent_interval_intersection_tests"] += len(weights)


def exhaustive(weights, cap, counts, work):
    sampler = Categorical(weights, work)
    failures, categories, bits = 0, [0] * len(weights), 0
    for value in range(2**cap):
        tape = BitTape(value, cap)
        before = sum(work.values())
        draw = sampler.draw(tape.bit, cap)
        validate_draw(weights, tape, draw, cap, counts)
        assert sum(work.values()) - before <= 40 * (cap + 1) * (len(weights).bit_length() + 1)
        if draw.category is None:
            failures += 1
        else:
            categories[draw.category] += 1
        bits += draw.bits
    probabilities = [weight / sum(weights) for weight in weights]
    missing = [
        probability - F(count, 2**cap) for probability, count in zip(probabilities, categories)
    ]
    assert min(missing) >= 0 and sum(missing) == F(failures, 2**cap)
    assert failures <= len(weights) - 1
    assert F(bits, 2**cap) <= max(1, len(weights) - 1).bit_length() + 2
    counts["exhaustive_distribution_and_failure_checks"] += 1
    counts["dyadic_boundary_profiles"] += all(
        p.denominator & (p.denominator - 1) == 0 for p in probabilities
    )
    return failures, categories


def adaptive_pairs(cap, counts, work):
    """Second distribution depends on the first successful category."""
    first_weights = [F(1), F(2), F(4)]
    choices = [[F(1), F(1)], [F(1), F(2), F(1)], [F(5), F(1), F(3)]]
    first = Categorical(first_weights, work)
    seconds = [Categorical(weights, work) for weights in choices]
    failures = 0
    for left in range(2**cap):
        for right in range(2**cap):
            left_tape = BitTape(left, cap)
            a = first.draw(left_tape.bit, cap)
            validate_draw(first_weights, left_tape, a, cap, counts)
            if a.category is None:
                failures += 1
                continue
            right_tape = BitTape(right, cap)
            b = seconds[a.category].draw(right_tape.bit, cap)
            validate_draw(choices[a.category], right_tape, b, cap, counts)
            failures += b.category is None
            counts["adaptive_second_draws"] += 1
    assert F(failures, 2 ** (2 * cap)) <= F(4, 2**cap)
    counts["adaptive_two_draw_union_bounds"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work, rng = time.monotonic(), Counter(), Counter(), random.Random(908044)
    profiles = [[F(1)], [F(1), F(2)], [F(1), F(1), F(1)], [F(1), F(2), F(1)]]
    if args.full:
        profiles.extend([[F(1)] * n for n in [2, 4, 5, 7, 8, 13, 16]])
        profiles.extend([[F(i * i + 1) for i in range(n)] for n in [3, 7, 11]])
        profiles.extend([[F(2) ** -200, F(1), F(2) ** 200], [F(1), F(2) ** 200 - 1]])
    for weights in profiles:
        for cap in range(13 if args.full else 7):
            exhaustive(weights, cap, counts, work)
    for cap in range(7 if args.full else 4):
        adaptive_pairs(cap, counts, work)
    # Conditioning on nonfailure changes the distribution: only the upper
    # half of [0,1) is accepted at cap one for probabilities 1/3 and 2/3.
    failed, categories = exhaustive([F(1), F(2)], 1, counts, work)
    assert failed == 1 and categories == [0, 1]
    counts["conditional_distribution_counterexamples"] += 1
    for exponent in [1, 10, 80, 200, 1024] if args.full else [1, 10]:
        weights = [F(1), F(2) ** exponent - 1]
        sampler = Categorical(weights, work)
        for prefix in [0, 2 ** (exponent + 1) - 1]:
            tape = BitTape(prefix, exponent + 1)
            draw = sampler.draw(tape.bit, exponent + 1)
            validate_draw(weights, tape, draw, exponent + 1, counts)
            assert draw.category == int(prefix != 0)
            assert draw.bits == (exponent if prefix == 0 else 1)
            counts["rare_mass_exact_endpoint_cases"] += 1
    for n in [1, 2, 3, 16, 257] if args.full else [1, 3]:
        weights = [F(2) ** (((7 * i) % 17) - 8) for i in range(n)]
        sampler = Categorical(weights, work)
        for draws in [0, 1, 10, 10**6, 2**100]:
            for delta in [F(1, 4), F(1, 2**20), F(1, 2**300)]:
                cap = sampler.cap(draws, delta)
                assert F((n - 1) * draws, 2**cap) <= delta
                counts["explicit_total_draw_budget_checks"] += 1
        cap = sampler.cap(1000, F(1, 2**20))
        for _ in range(1000 if args.full else 50):
            draw = sampler.draw(lambda: rng.getrandbits(1), cap)
            assert draw.category is None or 0 <= draw.category < n
            counts["seeded_bounded_random_draws"] += 1
    result = {
        "audit": "incremental_active_set_sdd.fair_bit_categorical",
        "scope": "Implemented fair-bit categorical sampler with a capped failure event and explicit word work; no exact random-real or huge common-denominator primitive. Not a spectral solver or local OP3 algorithm.",
        "arithmetic": "exact fractions in reference; exact-real word work, not bit complexity",
        "audit_only": dict(counts),
        "charged_sampling_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
