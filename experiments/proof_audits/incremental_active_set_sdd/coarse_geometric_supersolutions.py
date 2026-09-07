"""Exact audit of a geometric-envelope supersolution obstruction.

Full-support positive obstacle faces are generated from an exact Green
column and a declared lambda. Independent original Schur elimination shows
that the true coordinate envelope eta*u+h can fail a one-sided coarse
residual test. This refutes that sufficient-test shortcut, not OP3.
All matrix solves and support selection are reference work.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

from geometric_value_events import solve
from local_cycle_rank_clusters import independent_schur
import networkx as nx


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 2 <= args.max_n <= 7:
        parser.error("max_n must be 2 through 7")
    started = time.monotonic()
    counts = Counter()
    witness = None
    alphas = [F(1, 3), F(1, 2), F(3, 4)]
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= args.max_n and nx.is_connected(g)]
    for graph in graphs:
        n = len(graph)
        for alpha in alphas:
            gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
            matrix = [
                [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
                for i in graph
            ]
            for seed in graph:
                source = [F(i == seed) for i in graph]
                green = solve(matrix, source)
                lam = bar * min(green) / 2
                epsilon = 2 * lam
                eta = F(5, 4)
                h = epsilon / (16 * gamma)
                assert 0 < epsilon < 1
                response = [x - lam / bar for x in green]
                load = [F(i == seed) - lam * graph.degree(i) for i in graph]
                assert all(x > 0 for x in response)
                assert all(sum(matrix[i][j] * response[j] for j in graph) == load[i] for i in graph)
                counts["independent_positive_full_faces"] += 1
                port_sets = {tuple(range(n)), (seed,)} | {
                    tuple(sorted((seed, i))) for i in graph if i != seed
                }
                for ports in sorted(port_sets):
                    coarse, rhs = independent_schur(matrix, load, set(graph), ports)
                    one = [sum(row) for row in coarse]
                    effective = [x / bar for x in one]
                    assert all(x > 0 for x in effective)
                    assert all(
                        rhs[k] == F(i == seed) - lam * effective[k] for k, i in enumerate(ports)
                    )
                    exact = [response[i] for i in ports]
                    upper = [eta * x + h for x in exact]
                    gap = [
                        rhs[k] - sum(coarse[k][j] * upper[j] for j in range(len(ports)))
                        for k in range(len(ports))
                    ]
                    prefactor = (eta - 1) * lam - h * bar
                    expected = [
                        (1 - eta) * F(i == seed) + prefactor * effective[k]
                        for k, i in enumerate(ports)
                    ]
                    assert gap == expected and all(upper[k] > exact[k] for k in range(len(ports)))
                    shifted = [x + lam / bar for x in exact]
                    assert all(
                        sum(coarse[k][j] * shifted[j] for j in range(len(ports))) == F(i == seed)
                        for k, i in enumerate(ports)
                    )
                    for k, i in enumerate(ports):
                        if i == seed:
                            continue
                        assert (gap[k] > 0) == (gamma > F(1, 3))
                        assert (gap[k] == 0) == (gamma == F(1, 3))
                        counts["failed_true_upper_envelope_rows"] += gap[k] > 0
                        counts["equality_boundary_rows"] += gap[k] == 0
                        counts["accepted_true_upper_envelope_rows"] += gap[k] < 0
                    if len(ports) == 1:
                        assert gap[0] < 0
                    counts["independent_original_schur_systems"] += 1
                    counts["geometric_envelope_identity_checks"] += 1
                    counts["positive_shift_source_identities"] += 1
                    if (
                        n == 3
                        and len(graph.edges) == 3
                        and alpha == F(1, 3)
                        and seed == 0
                        and len(ports) == 3
                    ):
                        witness = {
                            "edges": sorted(graph.edges),
                            "alpha_lazy": str(alpha),
                            "lambda": str(lam),
                            "eps_appr": str(epsilon),
                            "eta": str(eta),
                            "h": str(h),
                            "physical_response": [str(x) for x in exact],
                            "true_coordinate_upper_envelope": [str(x) for x in upper],
                            "coarse_supersolution_residual_f_minus_K_upper": [str(x) for x in gap],
                        }
        print(
            json.dumps(
                {
                    "vertices": n,
                    "edges": len(graph.edges),
                    "faces": counts["independent_positive_full_faces"],
                }
            ),
            flush=True,
        )
    result = {
        "audit": "incremental_active_set_sdd.coarse_geometric_supersolutions",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all connected simple atlas graphs through max_n; full support",
        "max_n": args.max_n,
        "graph_count": len(graphs),
        "seed": "every vertex",
        "alpha_lazy": [str(x) for x in alphas],
        "lambda": "bar_alpha * min_i (M^{-1} e_v)_i / 2; reference-only parameter selection guarantees full positive support",
        "eps_appr": "2*lambda",
        "ports": "singleton seed, every seed-containing pair, and all vertices",
        "stopping_rule": "not an algorithm; exact original Schur and geometric-envelope identities",
        "scope": "Representation-specific failure of testing K*(eta*u+h)>=f as a geometric upper-band certificate; no graph-uniform work lower bound",
        "audit_only": dict(counts),
        "triangle_witness": witness,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["geometric_value_events", "local_cycle_rank_clusters"]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
