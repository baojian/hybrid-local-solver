"""Exact algebra and sampling audit for an explicit spectral confidence wrapper.

Effective resistances and adversarial estimator vectors are references.
The matrix Chernoff probability statement remains a primary-source import.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from geometric_value_events import solve
from spectral_preconditioner_floor import certify_psd, difference, laplacian
import networkx as nx


def ceiling_log2(value, work):
    power, exponent = F(1), 0
    while power < value:
        power *= 2
        exponent += 1
        work["confidence_grid_doublings"] += 1
    return exponent


def resistances(n, edges, counts):
    matrix = laplacian(n, edges)
    reduced = [row[1:] for row in matrix[1:]]
    values = []
    for v, w, c in edges:
        load = [F((i == v) - (i == w)) for i in range(n)]
        result = [F(0)] + solve(reduced, load[1:])
        value = result[v] - result[w]
        assert value > 0
        values.append(value)
        counts["reference_grounded_resistance_solves"] += 1
    assert sum(c * r for (_, _, c), r in zip(edges, values)) == n - 1
    counts["exact_total_leverage_identities"] += 1
    return values


def robust_overestimates(edges, vectors, work):
    repetitions = len(vectors)
    assert repetitions % 2 == 1 and all(len(row) == len(edges) for row in vectors)
    result = []
    for i, (_, _, weight) in enumerate(edges):
        values = sorted(row[i] for row in vectors)
        result.append(2 * weight * values[repetitions // 2])
        work["estimator_values_sorted"] += repetitions
        work["median_comparison_budget"] += repetitions * ceiling_log2(F(repetitions), Counter())
        work["median_buffer_words_allocated"] += repetitions
    work["leverage_overestimate_words_allocated"] += len(result)
    return result


def sample(n, edges, overestimates, delta, rng, work, counts):
    total, positive = F(0), True
    for value in overestimates:
        total += value
        positive = positive and value > 0
        work["sampling_score_guard_entries_scanned"] += 1
    if not positive or total > 4 * (n - 1):
        work["invalid_estimator_sampling_aborts"] += 1
        return None
    logarithm = ceiling_log2(4 * n / delta, work)
    rational_count = 27 * total * logarithm
    draws = (
        rational_count.numerator + rational_count.denominator - 1
    ) // rational_count.denominator
    assert 2 * n * F(1, 2**logarithm) <= delta / 2
    probabilities = [t / total for t in overestimates]
    assert sum(probabilities) == 1 and all(p > 0 for p in probabilities)
    # Integer CDF sampling is exact in the rational reference; integer bit
    # operations are not claimed to be constant-time production primitives.
    denominator = math.lcm(*(p.denominator for p in probabilities))
    prefix = []
    cumulative = 0
    for p in probabilities:
        cumulative += p.numerator * (denominator // p.denominator)
        prefix.append(cumulative)
        counts["reference_integer_CDF_entries"] += 1
    assert cumulative == denominator
    multiplicities = [0] * len(edges)
    for _ in range(draws):
        value = rng.randrange(denominator)
        counts["reference_exact_integer_random_draws"] += 1
        lo, hi = 0, len(prefix)
        while lo < hi:
            mid = (lo + hi) // 2
            if value < prefix[mid]:
                hi = mid
            else:
                lo = mid + 1
            work["sample_CDF_comparisons"] += 1
        multiplicities[lo] += 1
        work["sample_multiplicity_updates"] += 1
    output = []
    for (v, w, c), p, multiplicity in zip(edges, probabilities, multiplicities):
        if multiplicity:
            output.append((v, w, F(3, 2) * multiplicity * c / (p * draws)))
            work["sampled_output_edge_records_allocated"] += 1
        work["sample_output_records_scanned"] += 1
    work["sample_state_words_allocated"] += 3 * len(edges) + draws
    return output, draws, logarithm


def audit_case(graph, scale, delta, rng, counts, work):
    n = len(graph)
    edges = [(v, w, scale * F(1 + (v + 2 * w) % 5, 1 + (v + w) % 3)) for v, w in graph.edges()]
    exact = resistances(n, edges, counts)
    exponent = ceiling_log2(2 / delta, work)
    repetitions = 8 * exponent + 1
    # Deliberately use the smallest possible good majority, stronger than
    # a typical successful estimator run; this is conditional median QA.
    good = repetitions // 2 + 1
    vectors = []
    for k in range(repetitions):
        if k < good:
            row = [r * F(rng.randrange(3, 6), 4) for r in exact]
        else:
            row = [F(0) if (i + k) % 2 else r * 2**100 for i, r in enumerate(exact)]
        vectors.append(row)
        counts["reference_adversarial_estimator_vector_words"] += len(row)
    rng.shuffle(vectors)
    estimates = robust_overestimates(edges, vectors, work)
    total = sum(estimates)
    for (_, _, c), r, p in zip(edges, exact, estimates):
        assert c * r <= p <= 4 * c * r
        assert (c * r) / (p / total) <= total
        counts["whitened_rank_one_eigenvalue_bounds"] += 1
    assert total <= 4 * (n - 1)
    counts["complete_majority_and_leverage_certificates"] += 1
    # This exact expectation identity avoids a matrix square root.
    expected = [[F(0)] * n for _ in range(n)]
    for (v, w, c), over in zip(edges, estimates):
        probability = over / total
        atom = laplacian(n, [(v, w, c / probability)])
        for i in range(n):
            for j in range(n):
                expected[i][j] += probability * atom[i][j]
    original = laplacian(n, edges)
    assert expected == original
    counts["complete_sample_expectation_matrix_identities"] += 1
    for invalid in [[F(0)] * len(edges), [-F(1)] * len(edges), [F(2**100)] * len(edges)]:
        previous = counts["reference_exact_integer_random_draws"]
        assert sample(n, edges, invalid, delta, rng, work, counts) is None
        assert counts["reference_exact_integer_random_draws"] == previous
        counts["invalid_estimator_aborts_before_any_sampling"] += 1
    sampled_result = sample(n, edges, estimates, delta, rng, work, counts)
    assert sampled_result is not None
    output, draws, logarithm = sampled_result
    sampled = laplacian(n, output)
    valid = True
    try:
        certify_psd(difference(sampled, original), counts)
        certify_psd(difference(original, sampled, F(1, 2)), counts)
    except AssertionError:
        # A finite-sample failure is permitted by the probabilistic theorem;
        # preserve it rather than changing the seed until every sample passes.
        valid = False
    counts["sampled_spectral_successes"] += valid
    counts["sampled_spectral_failures"] += not valid
    counts["complete_confidence_wrapper_cases"] += 1
    return {
        "vertices": n,
        "edges": len(edges),
        "energy_scale": str(scale),
        "requested_failure": str(delta),
        "estimator_repetitions": repetitions,
        "good_reference_vectors": good,
        "samples": draws,
        "natural_log_upper_bound": logarithm,
        "sample_failure_bound": str(2 * n * F(1, 2**logarithm)),
        "sample_spectrum_in_interval": valid,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started, rng, counts, work = time.monotonic(), random.Random(80329), Counter(), Counter()
    cases = []
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= (5 if args.full else 3) or not nx.is_connected(graph):
            continue
        for scale in [F(1, 2**40), F(1), F(2**40)] if args.full else [F(1)]:
            for delta in [F(1, 8), F(1, 2**20)] if args.full else [F(1, 8)]:
                cases.append(audit_case(graph, scale, delta, rng, counts, work))
    result = {
        "audit": "incremental_active_set_sdd.spectral_confidence_wrapper",
        "arithmetic": "exact fractions and exact integer sampling reference",
        "random_seed": 80329,
        "input_family": "Weighted connected atlas graphs, common scales and two confidence levels, adversarial strict-majority resistance-estimator vectors",
        "alpha_eps_physical_seed": "not applicable: supplied spectral primitive",
        "stopping_rule": "Explicit median repetition budget and 27*t*ceil(log2(4*n/delta)) leverage-sampling budget",
        "scope": "Implemented median and sampling wrapper with exact expectation/leverage/PSD validators; fast effective-resistance estimation and matrix Chernoff probability are source imports, not implemented or proved by empirical sampling. No local OP3 theorem.",
        "audit_only": dict(counts),
        "algorithm_counts": dict(work),
        "cases": cases,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["geometric_value_events", "spectral_preconditioner_floor"]
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
