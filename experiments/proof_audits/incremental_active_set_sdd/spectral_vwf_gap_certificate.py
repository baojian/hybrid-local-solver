"""Computable spectral residual certificates for nongrounded VWF gaps."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compressed_forest_refinement import energy, residual
from nested_mixed_forest_solver import upward_candidate
from persistent_vwf_forest import IntegralArena, PersistentForest
from recursive_vwf_ranges import graph_records
from spectral_preconditioner_floor import certify_psd, difference, laplacian
from vwf_forest_reference import PieceVWF, random_function
from vwf_quadratic_policy import minimum
import networkx as nx


def certificate(graph, preconditioner, functions, at, kappa, beta, xi, oracle, work):
    shifted = residual(graph, functions, at, work)
    candidate = oracle(shifted, beta, xi)
    value = energy(preconditioner, shifted, candidate, work)
    result = kappa * beta * (xi - value)
    assert result >= 0
    work["complete_spectral_gap_oracle_calls"] += 1
    return result


def tree_certificate(graph, tree, functions, at, kappa, work):
    shifted = residual(graph, functions, at, work)
    arena = IntegralArena()
    forest = PersistentForest(tree, shifted, [0], arena)
    point = forest.curves[0].minimum_point()
    value = forest.curves[0].value(point)
    assert value <= 0
    work.update(arena.counts)
    work["tree_minimum_value_certificates_without_reconstruction"] += 1
    return -kappa * value


def audit_case(graph, h, kappa, functions, counts, work, rng):
    n = len(graph)
    g_matrix, h_matrix = laplacian(n, graph_records(graph)), laplacian(n, graph_records(h))
    certify_psd(difference(h_matrix, g_matrix), counts)
    certify_psd(difference(g_matrix, h_matrix, 1 / kappa), counts)
    optimum, optimum_value = minimum(graph, functions, counts)
    states = [
        [F(0)] * n,
        optimum,
        [x / 2 for x in optimum],
        [f.lower + rng.randrange(1, 20) for f in functions],
    ]
    for at in states:
        current = energy(graph, functions, at, counts)
        gap = current - optimum_value
        shifted = residual(graph, functions, at, Counter())
        h_optimum, h_value = minimum(h, shifted, counts)
        assert -gap <= h_value <= -gap / kappa
        if nx.is_tree(h):
            value = tree_certificate(graph, h, functions, at, kappa, work)
            assert value == -kappa * h_value and gap <= value <= kappa * gap
            counts["complete_exact_tree_gap_certificates"] += 1
        for beta in [F(1), F(2), F(4)]:
            for xi in [F(0), F(1, 2**20)]:

                def oracle(model, b, additive):
                    base = [x / b for x in h_optimum]
                    assert energy(h, model, base, counts) <= h_value / b
                    q = (
                        upward_candidate(h, model, base, additive, 0, Counter(), counts)
                        if additive
                        else base
                    )
                    value = energy(h, model, q, counts)
                    assert value <= h_value / b + additive
                    counts["positive_gap_oracle_errors"] += value > h_value
                    return q

                cert = certificate(graph, h, functions, at, kappa, beta, xi, oracle, work)
                assert gap <= cert <= kappa * beta * (gap + xi)
                counts["complete_mixed_spectral_gap_certificates"] += 1
                counts["zero_gap_spectral_certificates"] += gap == 0
                counts["positive_original_energy_certificate_states"] += current > 0
                counts["signed_lower_endpoint_certificate_states"] += any(
                    f.lower < 0 for f in functions
                )
                for target in [F(1, 2**20), F(1), F(16)]:
                    if cert <= target:
                        assert gap <= target
                        counts["accepted_fixed_absolute_targets"] += 1
                    else:
                        counts["rejected_fixed_absolute_targets"] += 1
                    if gap <= target / (2 * kappa * beta) and xi <= target / (2 * kappa * beta):
                        assert cert <= target
                        counts["absolute_acceptance_sufficiency_certificates"] += 1
                eta = max(F(0), (current + cert) / 2)
                assert current + cert <= 2 * eta
                assert current <= optimum_value / 2 + eta
                counts["computable_two_relative_acceptance_certificates"] += 1
    counts["complete_spectral_gap_input_cases"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, rng, counts, work = time.monotonic(), random.Random(80323), Counter(), Counter()
    records = []
    for n in range(2, 7 if args.full else 4):
        for scale in [F(1, 2**40), F(1), F(2**40)] if args.full else [F(1)]:
            graph = nx.complete_graph(n)
            for v, w in graph.edges():
                graph[v][w]["weight"] = scale
            h = nx.star_graph(n - 1)
            for v, w in h.edges():
                h[v][w]["weight"] = n * scale
            for profile in ["random", "zero_tail", "zero_gap", "affine"]:
                functions = [random_function(rng) for _ in graph]
                if profile == "zero_gap":
                    functions = [PieceVWF(-F(1), (), ((F(0), F(0), F(0)),)) for _ in graph]
                elif profile == "affine":
                    functions = [
                        PieceVWF(
                            -F(3), (), ((F(0), scale * (F(-1) if v == 0 else F(1, n - 1)), F(0)),)
                        )
                        for v in graph
                    ]
                else:
                    total = sum(f.pieces[-1][1] for f in functions)
                    correction = -total if profile == "zero_tail" else max(F(0), 1 - total)
                    f = functions[0]
                    functions[0] = PieceVWF(
                        f.lower, f.splits, tuple((a, b + correction, c) for a, b, c in f.pieces)
                    )
                    functions = [
                        PieceVWF(
                            f.lower,
                            f.splits,
                            tuple((scale * a, scale * b, scale * c) for a, b, c in f.pieces),
                        )
                        for f in functions
                    ]
                audit_case(graph, h, F(n), functions, counts, work, rng)
                records.append(
                    {
                        "vertices": n,
                        "energy_scale": str(scale),
                        "profile": profile,
                        "quality": str(n),
                        "states": 4,
                        "mixed_oracles_per_state": 6,
                    }
                )
    result = {
        "audit": "incremental_active_set_sdd.spectral_vwf_gap_certificate",
        "arithmetic": "exact fractions",
        "random_seed": 80323,
        "input_family": "Complete graphs with non-edgewise scaled-star spectral preconditioners, signed VWFs, zero final slope/gap, common energy scales and positive-energy feasible states",
        "alpha_eps_physical_seed": "not applicable: generic supplied VWF gap certificate",
        "stopping_rule": "Compute kappa*beta*(xi-R_H(q)); accept the requested absolute or mixed guarantee only through its proved inequality",
        "scope": "Implemented sparse residual/energy certificate and exact persistent tree minimum-value variant; dense minima and deliberately perturbed mixed oracles are validators. No general preconditioner constructor or local OP3 theorem.",
        "audit_only": dict(counts),
        "algorithm_counts": dict(work),
        "cases": records,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "compressed_forest_refinement",
                "nested_mixed_forest_solver",
                "persistent_vwf_forest",
                "recursive_vwf_ranges",
                "spectral_preconditioner_floor",
                "vwf_forest_reference",
                "vwf_quadratic_policy",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
