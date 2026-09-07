"""Exact audit of accelerated relative-plus-additive proximal contracts.

This validates an explicit mixed tolerance and its zero-gap behavior. Dense
piece oracles are references; their costs remain outside a fast solver claim.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from diffusion_accuracy_bridge import quadratic
from generic_proximal_geometry import AffineVWF, TranslatedCapped, normalize, universal_policy
import networkx as nx


def run_case(data, eta, counts, work):
    n, kappa = data.n, data.kappa
    zero = [F(0)] * n
    initial, optimum = data.energy(zero), data.energy(data.optimum)
    gap = initial - optimum
    assert eta > 0 and gap >= 0 and initial <= 0
    enlarged = gap + eta
    steps, original_relative, doublings = universal_policy(kappa)
    relative, additive = original_relative / 2, eta / (2**32 * kappa)
    internal = enlarged / (2**30 * kappa)
    radius = F(1)
    while radius * radius > additive:
        radius /= 2
        counts["reference_additive_perturbation_scale_halvings"] += 1
    y, z, previous = zero.copy(), zero.copy(), None
    work["policy_step_doublings"] += doublings
    work["initial_vector_entries_allocated"] += 2 * n
    errors, positive_models = [], 0
    trajectory_hash = hashlib.sha256()
    for k in range(steps):
        weight = F(k + 2, 2)
        x = [(1 - 1 / weight) * a + b / weight for a, b in zip(y, z)]
        if k:
            assert x == [a + F(k - 1, k + 2) * (a - b) for a, b in zip(y, previous)]
        assert quadratic(data.h, x) <= 64 * kappa**2 * enlarged
        counts["mixed_infeasible_centers"] += any(t < lo for t, lo in zip(x, data.lower))
        base, model_optimum = data.oracle(x, relative / 2, counts)
        model0 = initial + (quadratic(data.h, x) - quadratic(data.g, x)) / 2

        def normalized(v):
            d = [a - b for a, b in zip(v, x)]
            return data.energy(v) + (quadratic(data.h, d) - quadratic(data.g, d)) / 2 - model0

        step = radius
        while True:
            raw = base.copy()
            raw[k % n] += step
            if normalized(raw) <= model_optimum / (1 + relative) + additive:
                break
            step /= 2
            counts["reference_mixed_candidate_backtracks"] += 1
        q = normalize(raw, data.upper_split, work)
        value = normalized(q)
        assert value <= normalized(raw) <= model_optimum / (1 + relative) + additive
        assert data.energy(q) <= data.energy(raw)
        error = value - model_optimum
        assert 0 <= error <= relative * (-value) + (1 + relative) * additive <= internal
        assert -value <= 33 * kappa**2 * enlarged
        actual_gap = data.energy(q) - optimum
        if k == 0:
            assert actual_gap <= gap + additive
        else:
            assert actual_gap <= 8 * kappa * enlarged / (k + 2) ** 2
        assert actual_gap <= 2 * kappa * enlarged
        distance = [a - b for a, b in zip(q, data.optimum)]
        assert quadratic(data.h, distance) <= 2 * kappa * actual_gap
        assert quadratic(data.g, q) <= 12 * kappa * enlarged
        counts["mixed_relative_and_additive_step_certificates"] += 1
        counts["positive_normalized_model_outputs"] += value > 0
        counts["outputs_using_additive_allowance"] += value > model_optimum / (1 + relative)
        counts["nonzero_errors_with_zero_initial_gap"] += gap == 0 and error > 0
        counts["negative_feasible_mixed_iterates"] += min(q) < 0
        positive_models += value > 0
        errors.append(error)
        new_z = [a + weight * (b - c) for a, b, c in zip(z, q, x)]
        assert new_z == [weight * a - (weight - 1) * b for a, b in zip(q, y)]
        previous, y, z = y, q, new_z
        for t in y:
            for integer in [t.numerator, t.denominator]:
                b = abs(integer).to_bytes((abs(integer).bit_length() + 7) // 8, "big")
                trajectory_hash.update(bytes([integer < 0]) + len(b).to_bytes(8, "big") + b)
        work["mixed_reference_oracle_calls"] += 1
        work["iteration_vector_entries_allocated"] += 6 * n
        work["supplied_gradient_edge_budget"] += len(data.ge) + len(data.he)
        work["normalized_vertex_descriptor_budget"] += n
    final_gap = data.energy(y) - optimum
    assert final_gap <= (gap + eta) / 32
    assert data.energy(y) <= optimum / 2 + eta
    counts["complete_mixed_accelerated_invocations"] += 1
    counts["zero_gap_mixed_invocations"] += gap == 0
    counts["zero_total_tail_mixed_invocations"] += sum(data.terminal) == 0
    return {
        **data.metadata,
        "eta": str(eta),
        "relative_tolerance": str(relative),
        "inner_additive_tolerance": str(additive),
        "steps": steps,
        "positive_normalized_models": positive_models,
        "nonzero_model_errors": sum(e > 0 for e in errors),
        "trajectory_fraction_bytes_sha256": trajectory_hash.hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    max_n = 4 if args.full else 3
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_connected(g)]
    etas = [F(1, 8), F(1, 2**30)] if args.full else [F(1, 2**12)]
    for graph in graphs:
        for seed in graph:
            for profile in ["half_optimum", "beyond_cap"] if args.full else ["half_optimum"]:
                for eta in etas:
                    run_case(
                        TranslatedCapped(graph, seed, F(1, 3), F(9, 4), profile), eta, counts, work
                    )
        for eta in etas:
            data = TranslatedCapped(graph, 0, F(1, 1009), F(4), "zero_gap")
            data.constant = F(0)
            run_case(data, eta, counts, work)
    structured = []
    for zero_gap in [False, True]:
        for eta in etas:
            data = AffineVWF(nx.path_graph(4 if args.full else 3), F(4), zero_gap, 512)
            data.constant = F(0)
            structured.append(run_case(data, eta, counts, work))
    for power in [-40, 0, 40] if args.full else [0]:
        scale = F(2) ** power
        data = TranslatedCapped(nx.path_graph(3), 0, F(1, 1009), F(4), "beyond_cap", scale)
        structured.append(run_case(data, scale / 8, counts, work))
    assert counts["positive_normalized_model_outputs"] > 0
    assert counts["outputs_using_additive_allowance"] > 0
    assert counts["nonzero_errors_with_zero_initial_gap"] > 0
    result = {
        "audit": "incremental_active_set_sdd.mixed_proximal_accuracy",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "max_n": max_n,
        "input_family": "Translated capped VWF graph objectives, signed domains, zero gap, zero total final slope, large nullspace shifts and common energy scales",
        "parameter_profiles": "Atlas alpha=1/3,kappa=9/4,eps=1/(8*volume); zero-gap alpha=1/1009,kappa=4. Explicit structured profiles are recorded.",
        "stopping_rule": "Least dyadic T with T^2>=256*kappa; normalized mixed contract with relative 1/(66*2^30*kappa^3) and additive eta/(2^32*kappa); certify every step and final (gap+eta)/32 bound",
        "scope": "Mixed accuracy induction and implemented canonicalization/source updates. Dense reference candidates and matrix checks are validators; sparse edge counts are a supplied-interface budget. No recursive fast oracle or local OP3 solver.",
        "audit_only": dict(counts),
        "supplied_interface_counts": dict(work),
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["generic_proximal_geometry", "diffusion_accuracy_bridge"]
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
