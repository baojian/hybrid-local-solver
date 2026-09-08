"""Exact supplied significant-potential envelopes and original ACL repair.

Dense obstacle solves enumerate supplied envelopes; they are validators and
do not implement the missing local envelope discovery procedure.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from geometric_value_events import mv, obstacle
import networkx as nx


def check(graph, seed, alpha, epsilon, counts, full):
    n = len(graph)
    degrees = [graph.degree(i) for i in graph]
    gamma = (1 - alpha) / (1 + alpha)
    lam, delta = epsilon / 2, epsilon / 8
    matrix = [
        [F(degrees[i]) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    source = [F(i == seed) for i in graph]
    load = [source[i] - lam * degrees[i] for i in graph]
    optimum = obstacle(matrix, load)
    counts["dense_full_obstacle_solves"] += 1
    mandatory = {i for i in graph if optimum[i] > delta}
    optional = sorted(set(graph) - mandatory)
    masks = range(1 << len(optional)) if full else [0, (1 << len(optional)) - 1]
    for mask in masks:
        labels = sorted(mandatory | {v for k, v in enumerate(optional) if mask & (1 << k)})
        restricted = obstacle(
            [[matrix[i][j] for j in labels] for i in labels], [load[i] for i in labels]
        )
        v = [F(0)] * n
        for i, x in zip(labels, restricted):
            v[i] = x
        counts["dense_restricted_obstacle_solves"] += 1
        counts["dense_principal_matrix_entries"] += len(labels) ** 2
        assert all(0 <= b <= a and a - b <= delta for a, b in zip(optimum, v))
        counts["omitted_positive_coordinates"] += sum(
            optimum[i] > 0 for i in graph if i not in labels
        )
        counts["extra_inactive_coordinates"] += sum(optimum[i] == 0 for i in labels)
        counts["empty_envelopes"] += not labels
        counts["threshold_ties"] += sum(x == delta for x in optimum)
        errors = itertools.product([-delta, F(0), delta], repeat=len(labels))
        for errors_at in errors:
            w = [F(0)] * n
            for i, error in zip(labels, errors_at):
                w[i] = max(F(0), v[i] + error)
            x = [max(F(0), t - delta) for t in w]
            assert all(0 <= t <= b <= a for t, b, a in zip(x, v, optimum))
            assert max(a - t for a, t in zip(optimum, x)) <= 3 * delta
            residual = [s - y for s, y in zip(source, mv(matrix, x))]
            assert all(0 <= r <= epsilon * d for r, d in zip(residual, degrees))
            support_volume = sum(degrees[i] for i in graph if x[i] > 0)
            assert support_volume < 1 / lam
            counts["original_ACL_repair_certificates"] += 1
            counts["original_full_row_entries_checked"] += n + 2 * graph.number_of_edges()
        counts["supplied_envelopes"] += 1
    counts["physical_input_cases"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts = time.monotonic(), Counter()
    for graph in nx.graph_atlas_g():
        if not (2 <= len(graph) <= (5 if args.full else 3)) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in [F(1, 3), F(1, 17)]:
                for epsilon in [F(1, 4), F(1, 2), F(3, 4), F(1)]:
                    check(graph, seed, alpha, epsilon, counts, args.full)
    # On a two-vertex graph at alpha=1/3, epsilon=16/27 makes the
    # nonseed optimum exactly epsilon/8. Strict containment may omit it.
    check(nx.path_graph(2), 0, F(1, 3), F(16, 27), counts, args.full)
    assert counts["threshold_ties"] and counts["omitted_positive_coordinates"]
    result = {
        "audit": "incremental_active_set_sdd.significant_envelope_bridge",
        "arithmetic": "exact fractions",
        "input_family": "All connected graph-atlas graphs through five vertices in full mode, every physical seed, two alpha values, four ACL tolerances, every admissible supplied envelope and endpoint/zero coordinate perturbation; exact threshold-tie case",
        "stopping_rule": "Finite exhaustive validation; no local discovery algorithm",
        "scope": "Original full-degree principal obstacles and original residual ACL certificates; supplied envelope and dense solves are validator inputs/work",
        "audit_only": dict(counts),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "geometric_value_events.py": hashlib.sha256(
                Path(__file__).with_name("geometric_value_events.py").read_bytes()
            ).hexdigest()
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
