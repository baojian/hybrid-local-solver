"""Nested solver using a computable tree-residual gap certificate to stop.

This preserves the fixed-length audit as an immutable separate baseline.
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

from bounded_vwf_compression import VWF
from compressed_forest_refinement import energy, residual
from generic_proximal_geometry import universal_policy
from nested_mixed_forest_solver import (
    CoarseAccelerated,
    accelerate,
    forest_refine,
    normalized_model,
    tree_oracle,
)
from recursive_vwf_ranges import graph_norm, graph_records
from spectral_preconditioner_floor import prune
from spectral_vwf_gap_certificate import tree_certificate
from vwf_forest_reference import PieceVWF
from vwf_quadratic_policy import minimum
import networkx as nx


class CertifiedCoarse(CoarseAccelerated):
    def solve(self, functions, eta):
        graph, inner, kappa, work, counts = (
            self.graph,
            self.inner,
            self.kappa,
            self.work,
            self.counts,
        )
        n = len(graph)
        y, z = [F(0)] * n, [F(0)] * n
        initial = energy(graph, functions, y, work)
        _, optimum = minimum(graph, functions, counts)
        gap = initial - optimum
        assert initial <= 0 and gap >= 0
        steps, pure_relative, doublings = universal_policy(kappa)
        relative, additive = pure_relative / 2, eta / (2**32 * kappa)
        work["certified_coarse_policy_doublings"] += doublings
        work["certified_coarse_initial_vector_words"] += 2 * n

        def accepted(candidate):
            value = energy(graph, functions, candidate, work)
            cert = tree_certificate(graph, inner, functions, candidate, kappa, work)
            assert value - optimum <= cert <= kappa * (value - optimum)
            decision = value + cert <= 2 * eta
            counts["certified_coarse_computable_stopping_checks"] += 1
            if decision:
                assert value <= optimum / 2 + eta
                counts["accepted_coarse_spectral_gap_checks"] += 1
            else:
                work["failed_coarse_spectral_gap_checks"] += 1
            return decision

        if accepted(y):
            counts["coarse_certificates_accepted_at_origin"] += 1
            counts["certified_complete_coarse_invocations"] += 1
            return y, optimum
        for k in range(steps):
            weight = F(k + 2, 2)
            center = [(1 - 1 / weight) * a + b / weight for a, b in zip(y, z)]
            model = normalized_model(graph, inner, functions, center, work)
            q, model_optimum = tree_oracle(inner, model, additive, k, work, counts)
            value = energy(inner, model, q, work)
            assert value <= model_optimum / (1 + relative) + additive
            assert graph_norm(inner, center) <= 64 * kappa**2 * (gap + eta)
            actual_gap = energy(graph, functions, q, counts) - optimum
            assert actual_gap <= (
                gap + additive if k == 0 else 8 * kappa * (gap + eta) / (k + 2) ** 2
            )
            z = [a + weight * (b - c) for a, b, c in zip(z, q, center)]
            y = q
            work["certified_coarse_iteration_vector_words"] += 6 * n
            counts["certified_coarse_accelerated_steps"] += 1
            if accepted(y):
                counts["certified_complete_coarse_invocations"] += 1
                counts["coarse_certified_steps_saved_against_fixed_policy"] += steps - k - 1
                return y, optimum
        assert energy(graph, functions, y, counts) - optimum <= (gap + eta) / 32
        counts["coarse_fixed_policy_fallbacks"] += 1
        counts["certified_complete_coarse_invocations"] += 1
        return y, optimum


def run_physical(profile, work, counts):
    graph = nx.Graph([(0, 1), (0, 2), (1, 2), (0, 3)])
    alpha, eps, seed = F(1, 3), F(1, 32), 3
    gamma = (1 - alpha) / (1 + alpha)
    bar = 1 - gamma
    for v, w in graph.edges():
        graph[v][w]["weight"] = gamma
    functions = []
    for v in graph:
        d = graph.degree(v)
        load = F(v == seed) - eps * d / 2
        functions.append(PieceVWF.from_atoms(VWF(F(0), F(0), -load, ((1 / bar, bar * d),))))
    base = [F(3) if profile == "beyond_cap" else F(0)] * len(graph)
    if profile == "beyond_cap":
        functions = residual(graph, functions, base, work)
    if profile == "tiny_signed":
        tiny = F(1, 2**100)
        functions = [
            PieceVWF.from_atoms(
                VWF(
                    -F(1),
                    F(0),
                    -F(1, 8) if v == seed else F(0),
                    ((-tiny, F(1)), (tiny, F(1)), (F(1), F(1))),
                )
            )
            for v in graph
        ]
    kept, _, _ = prune(len(graph), graph_records(graph), graph_records(graph), work)
    inner = nx.Graph()
    inner.add_nodes_from(range(len(graph)))
    inner.add_weighted_edges_from(kept)
    coarse = inner.subgraph([0, 1, 2]).copy()
    child = CertifiedCoarse(coarse, work, counts)

    def oracle(model, relative, additive, index):
        del index
        return forest_refine(inner, model, [0, 1, 2], relative, additive, child, work, counts)

    result, optimum = accelerate(
        graph, inner, functions, F(2), F(1, 16), oracle, work, counts, 0, True
    )
    physical = [a + x for a, x in zip(base, result)]
    assert all(x >= (-1 if profile == "tiny_signed" else 0) for x in physical)
    counts["negative_outer_signed_iterate_coordinates"] += sum(x < 0 for x in result)
    return {
        "profile": profile,
        "physical_seed": seed if profile != "tiny_signed" else None,
        "alpha": str(alpha) if profile != "tiny_signed" else "not applicable: generic VWF",
        "eps_appr": str(eps) if profile != "tiny_signed" else "not applicable: generic VWF",
        "vertices": len(graph),
        "edges": graph.number_of_edges(),
        "outer_quality": "2",
        "coarse_quality": "6",
        "eta": "1/16",
        "result": [str(x) for x in result],
        "physical_result": [str(x) for x in physical] if profile != "tiny_signed" else None,
        "reference_optimum": str(optimum),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started, work, counts = time.monotonic(), Counter(), Counter()
    records = []
    if args.full:
        for profile in ["original", "beyond_cap", "tiny_signed"]:
            previous_work, previous_counts = work.copy(), counts.copy()
            case_started = time.monotonic()
            record = run_physical(profile, work, counts)
            record["algorithm_counts"] = dict(work - previous_work)
            record["audit_counts"] = dict(counts - previous_counts)
            record["elapsed_seconds"] = round(time.monotonic() - case_started, 3)
            records.append(record)
        assert counts["nested_positive_compression_errors"] > 0
        assert counts["reference_forward_piece_advances"] > 0
    else:
        graph = nx.complete_graph(3)
        for v, w in graph.edges():
            graph[v][w]["weight"] = F(1)
        functions = [
            PieceVWF.from_atoms(
                VWF(-F(1), F(0), -F(1, 8) if v == 0 else F(0), ((F(1, 2**100), F(1)), (F(1), F(1))))
            )
            for v in graph
        ]
        child = CertifiedCoarse(graph, work, counts)
        values, optimum = child.solve(functions, F(1, 2**30))
        records.append(
            {
                "profile": "certified coarse smoke",
                "result": [str(x) for x in values],
                "reference_optimum": str(optimum),
            }
        )
    result = {
        "audit": "incremental_active_set_sdd.certified_nested_forest_solver",
        "arithmetic": "exact fractions with upward dyadic rounding",
        "random_seed": None,
        "input_family": "Same supplied physical and signed beyond-cap cases as fixed-length nested baseline",
        "stopping_rule": "Coarse calls use Phi(y)+C(y)<=2*eta with an exact persistent tree residual certificate; fixed worst-case APG count remains a fallback. No dense optimum chooses a stopping iteration.",
        "scope": "Implemented computable stopping variant of the supplied two-level nested solver; dense minima validate gaps only, tiny preconditioners are supplied reference families, and no general local OP3 claim is made.",
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
                "nested_mixed_forest_solver",
                "spectral_vwf_gap_certificate",
                "compressed_forest_refinement",
                "generic_proximal_geometry",
                "persistent_vwf_forest",
                "recursive_vwf_ranges",
                "spectral_preconditioner_floor",
                "vwf_forest_reference",
                "vwf_quadratic_policy",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
