"""Exact cap and adaptive-confidence audit for the supplied recursion.

This is a resource-accounting model, not an implementation of the full
VWF recursion or of an imported low-stretch-tree algorithm. Payloads are
executed only after their whole resource reservation succeeds.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import time


class CapReached(Exception):
    pass


@dataclass(frozen=True)
class Request:
    work: int = 0
    words: int = 0
    depth_change: int = 0
    source_calls: int = 0
    node_mass: int = 0
    release: int = 0


class Resources:
    def __init__(self, work, words, depth, sources, mass):
        self.limits = (work, words, depth, sources, mass)
        self.work = self.words = self.depth = self.sources = self.mass = 0
        self.live = self.peak = self.attempts = self.executed = 0
        self.halted = False

    def perform(self, request, payload):
        if self.halted:
            raise CapReached("already halted")
        self.attempts += 1
        if (
            request.work < 0
            or request.words < 0
            or request.source_calls < 0
            or request.node_mass < 0
            or request.release < 0
            or request.release > self.live
            or self.depth + request.depth_change < 0
        ):
            self.halted = True
            raise CapReached("invalid request")
        # A zero-size instruction still incurs one unit. Word initialization
        # and release are paid separately from all requested payload work.
        after = (
            self.work + 1 + request.work + request.words + request.release,
            self.words + request.words,
            self.depth + request.depth_change,
            self.sources + request.source_calls,
            self.mass + request.node_mass,
        )
        if any(value > bound for value, bound in zip(after, self.limits)):
            self.halted = True
            raise CapReached("resource cap")
        self.work, self.words, self.depth, self.sources, self.mass = after
        self.live += request.words - request.release
        self.peak = max(self.peak, self.live)
        self.executed += 1
        # The callback is a bounded reference payload for this audit. The
        # theorem wraps individual RAM steps, not arbitrary opaque callbacks.
        return payload()


def reference_prefix(requests, limits):
    work = words = depth = sources = mass = live = 0
    for position, request in enumerate(requests):
        if (
            min(
                request.work,
                request.words,
                request.source_calls,
                request.node_mass,
                request.release,
            )
            < 0
        ):
            return position, (work, words, depth, sources, mass, live)
        if request.release > live or depth + request.depth_change < 0:
            return position, (work, words, depth, sources, mass, live)
        next_work = work + sum((1, request.work, request.words, request.release))
        next_words = words + request.words
        next_depth = depth + request.depth_change
        next_sources = sources + request.source_calls
        next_mass = mass + request.node_mass
        # Explicit coordinate comparisons are independent of the transaction
        # loop's tuple/zip implementation.
        if (
            next_work > limits[0]
            or next_words > limits[1]
            or next_depth > limits[2]
            or next_sources > limits[3]
            or next_mass > limits[4]
        ):
            return position, (work, words, depth, sources, mass, live)
        work, words, depth, sources, mass = (
            next_work,
            next_words,
            next_depth,
            next_sources,
            next_mass,
        )
        live += request.words - request.release
    return len(requests), (work, words, depth, sources, mass, live)


def audit_trace(requests, limits, counts):
    expected, state = reference_prefix(requests, limits)
    resources, payload_log = Resources(*limits), []
    for i, request in enumerate(requests):
        try:
            resources.perform(request, lambda i=i: payload_log.append(i))
        except CapReached:
            break
    assert payload_log == list(range(expected))
    assert (
        resources.work,
        resources.words,
        resources.depth,
        resources.sources,
        resources.mass,
        resources.live,
    ) == state
    assert resources.attempts == expected + (expected < len(requests))
    assert resources.executed <= resources.work <= limits[0]
    assert resources.words <= limits[1] and resources.peak <= resources.words
    counts["exact_transaction_prefix_checks"] += 1
    counts["accepted_and_rejected_requests_checked"] += resources.attempts
    counts["aborted_adversarial_traces"] += resources.halted
    return resources


def adaptive_failure_probability(calls, delta, profile, counts):
    """Enumerate a history-dependent conditional law, including early stops."""
    stack = [(0, 1, F(1), False)]
    bad_total, total_probability, leaves = F(0), F(0), 0
    while stack:
        depth, history, mass, bad = stack.pop()
        if depth == calls or (depth > 0 and (history + profile) % 7 == 0):
            bad_total += mass if bad else 0
            total_probability += mass
            leaves += 1
            continue
        probability = delta * F(1 + (history * 3 + profile) % 5, 5)
        assert 0 < probability <= delta
        stack.append((depth + 1, 2 * history, mass * (1 - probability), bad))
        stack.append((depth + 1, 2 * history + 1, mass * probability, True))
        counts["conditional_confidence_tree_nodes"] += 1
    assert total_probability == 1 and 0 <= bad_total <= calls * delta
    counts["exact_adaptive_conditional_union_bounds"] += 1
    counts["conditional_confidence_tree_leaves"] += leaves
    return bad_total


def audit_size_tree(mass, branching, counts):
    """Exact dyadic mass contraction; no graph or numerical solver implied."""
    pending, total, nodes, deepest = [(mass, 0)], 0, 0, 0
    while pending:
        current, depth = pending.pop()
        total += current
        nodes += 1
        deepest = max(deepest, depth)
        budget = current // 2
        children = []
        for slot in range(min(branching, budget)):
            value = budget // min(branching, budget) + (slot < budget % min(branching, budget))
            children.append(value)
        assert sum(children) <= F(current, 2) and all(child <= F(current, 2) for child in children)
        pending.extend((child, depth + 1) for child in children)
        counts["exact_recursive_mass_nodes"] += 1
    assert nodes <= total <= 2 * mass
    assert deepest <= mass.bit_length()
    counts["complete_recursive_mass_depth_call_bounds"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, rng = time.monotonic(), Counter(), random.Random(908900)
    instructions = [
        Request(),
        Request(work=2),
        Request(words=3),
        Request(depth_change=1, words=2),
        Request(depth_change=-1),
        Request(source_calls=1),
        Request(node_mass=4),
        Request(release=2),
    ]
    for length in range(5 if args.full else 3):
        for indices in itertools.product(range(len(instructions)), repeat=length):
            trace = [instructions[i] for i in indices]
            for limits in [(12, 7, 2, 2, 9), (7, 20, 1, 1, 4)]:
                audit_trace(trace, limits, counts)
    for _ in range(3000 if args.full else 100):
        trace = [rng.choice(instructions) for _ in range(rng.randrange(1, 65))]
        limits = tuple(rng.randrange(1, 60) for _ in range(5))
        audit_trace(trace, limits, counts)
    for exponent in [20, 80, 1024]:
        executed = []
        resources = Resources(100, 100, 3, 3, 100)
        try:
            resources.perform(Request(words=2**exponent), lambda: executed.append("allocated"))
        except CapReached:
            pass
        assert not executed and resources.words == resources.work == 0
        counts["huge_allocation_rejected_before_payload"] += 1
    for limit in [0, 1, 7, 100]:
        resources = audit_trace([Request()] * (limit + 2), (limit, 100, 4, 4, 100), counts)
        assert resources.executed == limit and resources.halted
        counts["zero_size_instruction_loops_capped"] += 1
    for limit in [3, 7, 20]:
        trace = [Request(words=3), Request(release=3)] * (limit + 1)
        resources = audit_trace(trace, (10000, limit, 4, 4, 100), counts)
        assert resources.peak == 3 and resources.words <= limit and resources.halted
        counts["released_storage_still_charged_cumulatively"] += 1
    for request in [
        Request(work=-1),
        Request(words=-1),
        Request(source_calls=-1),
        Request(release=1),
        Request(depth_change=-1),
    ]:
        audit_trace([request], (100, 100, 3, 3, 100), counts)
        counts["invalid_resource_requests_rejected"] += 1
    for calls in range(1, 13 if args.full else 5):
        for delta in [F(1, 2 * calls), F(1, 16 * calls), F(1, 2**80)]:
            for profile in range(7 if args.full else 2):
                adaptive_failure_probability(calls, delta, profile, counts)
    # Reusing a seed can invalidate a per-fixed-input failure argument:
    # a first answer exposes a uniform label U; an adaptive second input U
    # fails with certainty against the same seed, but only 1/N with fresh U'.
    for n in [4, 8, 16, 64]:
        shared_failures = fresh_failures = 0
        for fixed_query in range(n):
            assert F(sum(hidden == fixed_query for hidden in range(n)), n) == F(1, n)
            counts["exact_per_fixed_input_failure_bounds"] += 1
        for hidden in range(n):
            first_bad = hidden == 0
            adaptive_query = hidden
            shared_failures += first_bad or adaptive_query == hidden
            for fresh_hidden in range(n):
                fresh_failures += first_bad or fresh_hidden == hidden
        assert F(shared_failures, n) == 1 > F(2, n)
        assert F(fresh_failures, n * n) == F(2, n) - F(1, n * n)
        counts["reused_seed_conditional_confidence_counterexamples"] += 1
    for mass in [1, 2, 3, 7, 16, 100, 1024, 4096] if args.full else [1, 7, 100]:
        for branching in [1, 2, 3, 8, 32]:
            audit_size_tree(mass, branching, counts)
    # Parameter-level contraction with explicit constant placeholders:
    # R <= a sqrt(K)L, child <= b M L^4/K, K=A L^12.
    for exponent in range(1, 13):
        a, b, logarithm = 2**exponent, 2 ** (13 - exponent), F(exponent + 2)
        root_a = 4 * a * b
        coefficient = F(a * b, root_a) / logarithm
        assert coefficient <= F(1, 2)
        counts["symbolic_recursion_coefficient_contractions"] += 1
    result = {
        "audit": "incremental_active_set_sdd.supplied_recursion_caps",
        "scope": "Generic primitive reservation, adaptive conditional confidence, and recursive mass/depth/call accounting only. Not an implementation of the full VWF recursion or the source tree algorithm.",
        "arithmetic": "exact integers/fractions in reference; exact-real word model, not bit complexity",
        "parameters": {
            "seed": 908900,
            "full": args.full,
            "failed_check_accounting": "At most one rejected guard after the executed prefix; total guard work is O(cap+1).",
            "allocation_accounting": "All allocations are cumulative; releases do not restore the allocation budget.",
        },
        "audit_only": dict(counts),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
