"""A finite original-tree witness against a degree-filtered BFS envelope.

The large original tree is validated through its supplied symmetry quotient.
This is not a local algorithm with free access to quotient information.
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

from capped_restart_driver import rational_record
import networkx as nx


def positive_face_tree_reference(graph, degrees, load, counts):
    """Repeated exact tree principal solves; all scans are validator work."""
    order = list(nx.bfs_tree(graph, 0))
    parent = {0: None}
    for i in order:
        for j in graph[i]:
            if j != parent[i]:
                parent[j] = i
    face, values = {0}, [F(0)] * len(graph)
    for _ in range(len(graph)):
        diagonal = {i: F(degrees[i]) for i in face}
        rhs = {i: load[i] for i in face}
        for i in reversed(order[1:]):
            if i not in face:
                continue
            p = parent[i]
            assert p in face and diagonal[i] > 0
            weight = graph[i][p]["weight"]
            diagonal[p] -= weight**2 / diagonal[i]
            rhs[p] += weight * rhs[i] / diagonal[i]
            counts["reference_scalar_tree_eliminations"] += 1
        assert diagonal[0] > 0
        candidate = [F(0)] * len(graph)
        candidate[0] = rhs[0] / diagonal[0]
        for i in order[1:]:
            if i in face:
                p = parent[i]
                candidate[i] = (rhs[i] + graph[i][p]["weight"] * candidate[p]) / diagonal[i]
                counts["reference_scalar_tree_recoveries"] += 1
        assert all(b >= a >= 0 for a, b in zip(values, candidate))
        values = candidate
        new = set()
        for i in graph:
            residual = (
                load[i]
                - degrees[i] * values[i]
                + sum(graph[i][j]["weight"] * values[j] for j in graph[i])
            )
            if i in face:
                assert residual == 0
            elif residual > 0:
                new.add(i)
        counts["reference_full_quotient_rows_scanned"] += len(graph)
        counts["reference_quotient_vector_words_allocated"] += len(graph)
        counts["reference_face_tree_solves"] += 1
        if not new:
            return values
        face |= new
    raise AssertionError("Positive-face growth exceeded the finite vertex budget")


def witness(height, path_length, exponent):
    start, counts = time.monotonic(), Counter()
    lam, alpha = F(1, 2**exponent), F(1, 10**9)
    epsilon, gamma = 2 * lam, (1 - alpha) / (1 + alpha)
    bar, delta = 1 - gamma, epsilon / 8
    n = 1 + height + path_length
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    degrees = [3] + [3 * 2**k if k < height else 2**k for k in range(1, height + 1)]
    degrees += [2] * (path_length - 1) + [1]
    for k in range(1, height + 1):
        graph.add_edge(k - 1, k, weight=gamma * 2**k)
    for k in range(1, path_length + 1):
        graph.add_edge(0 if k == 1 else height + k - 1, height + k, weight=gamma)
    load_vector = [F(i == 0) - lam * degree for i, degree in enumerate(degrees)]
    values = positive_face_tree_reference(graph, degrees, load_vector, counts)
    assert all(0 <= x <= 1 / bar for x in values)
    # Check the original per-vertex KKT, by dividing quotient residuals
    # by each orbit multiplicity. This uses all original diagonal degrees.
    support_volume = 0
    for i in graph:
        operator = degrees[i] * values[i] - sum(graph[i][j]["weight"] * values[j] for j in graph[i])
        load = F(i == 0) - lam * degrees[i]
        assert operator >= load and (values[i] == 0 or operator == load)
        support_volume += degrees[i] * (values[i] > 0)
        counts["original_orbit_KKT_certificates"] += 1
    assert lam * support_volume < 1
    budget = 16 / lam
    candidates = []
    for distance in range(2, min(height, path_length)):
        # Even to discover distance k, BFS must query its parent at k-1.
        # All distance <k-1 rows must precede that, regardless of layer ties.
        preceding_cost = 3 + 3 * (2 ** (distance - 1) - 2) + 2 * (distance - 2)
        if preceding_cost > budget and values[height + distance] > delta:
            candidates.append((distance, preceding_cost, values[height + distance]))
    assert candidates
    distance, cost, value = candidates[0]
    return {
        "alpha": str(alpha),
        "eps_appr": str(epsilon),
        "physical_seed": 0,
        "binary_height": height,
        "path_length": path_length,
        "ambient_vertices": 2 ** (height + 1) - 1 + path_length,
        "maximum_original_degree": 3,
        "quotient_vertices": n,
        "original_positive_support_volume": support_volume,
        "row_degree_budget": str(budget),
        "missed_path_distance": distance,
        "necessary_work_even_before_discovery": cost,
        "significant_threshold": str(delta),
        "missed_path_potential": rational_record(value),
        "missed_potential_float_for_display_only": float(value),
        "all_quotient_potentials": [rational_record(x) for x in values],
        "audit_only": dict(counts),
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    cases = [witness(24, 512, 12)]
    if args.full:
        cases += [witness(20, 256, 10), witness(28, 1024, 14)]
    result = {
        "audit": "incremental_active_set_sdd.breadth_first_envelope_witness",
        "arithmetic": "exact fractions; floating value is display only",
        "input_family": "Unweighted finite tree: seed joins a path and two binary branches, all original degrees at most three",
        "stopping_rule": "Finite supplied-quotient KKT certificate and exact original BFS layer-work inequality",
        "scope": "Refutes this degree-filtered FIFO BFS budget rule only. Supplied symmetry and quotient construction are validator conveniences, not local access. No general OP3 lower bound.",
        "cases": cases,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ["capped_restart_driver.py"]
        },
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
