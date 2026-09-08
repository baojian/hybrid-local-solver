"""Exact combinatorial audit of bounded-cycle original-type frontier quotas.

All graphs, type partitions and connected active subsets are validator input.
This is not a local producer or a fast weighted cyclic numerical algorithm.
The five-cycle calculation audits a nonterminal legal positive prefix and a
false seed-twin identity, not an incorrect terminal ACL output.
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
from frontier_neighborhood_types import blow_up
from geometric_value_events import solve
import networkx as nx


def types(graph):
    union = nx.utils.UnionFind(graph)
    opened, closed = {}, {}
    for i in graph:
        for key, table in [(frozenset(graph[i]), opened), (frozenset(graph[i]) | {i}, closed)]:
            if key in table:
                union.union(i, table[key])
            else:
                table[key] = i
    partition = sorted([sorted(members) for members in union.to_sets()])
    owner = {i: c for c, members in enumerate(partition) for i in members}
    quotient = nx.Graph()
    quotient.add_nodes_from(range(len(partition)))
    quotient.add_edges_from((owner[i], owner[j]) for i, j in graph.edges if owner[i] != owner[j])
    return partition, owner, quotient


def check_graph(graph, counts):
    partition, owner, quotient = types(graph)
    q = len(partition)
    rank = quotient.number_of_edges() - q + 1
    assert rank >= 0 and nx.is_connected(quotient)
    for bits in range(1, 2**q):
        active_types = {i for i in quotient if bits & (1 << i)}
        sub = quotient.subgraph(active_types)
        if not nx.is_connected(sub):
            continue
        active_rank = sub.number_of_edges() - len(sub) + 1
        remaining = rank - active_rank
        new_parents = {
            i: set(quotient[i]) & active_types for i in quotient if i not in active_types
        }
        excess = sum(max(0, len(parents) - 1) for parents in new_parents.values())
        assert excess <= remaining
        counts["independent_new_type_cycle_excess_inequalities"] += 1
        for root in active_types:
            for partial in [False, True] if len(partition[root]) > 1 else [False]:
                seed = partition[root][0]
                physical = {
                    i
                    for c in active_types
                    for i in ([seed] if partial and c == root else partition[c])
                }
                groups = set()
                known = 0
                for j in graph:
                    if j in physical:
                        continue
                    parents = {owner[i] for i in graph[j] if i in physical}
                    if not parents:
                        continue
                    known += 1
                    if len(parents) >= 2:
                        groups.add(tuple(sorted(parents)))
                    if owner[j] != root:
                        assert len(parents) <= remaining + 1
                    if len(parents) > remaining + 1:
                        assert partial and owner[j] == root
                        counts["high_parent_count_forces_source_type_cases"] += 1
                    counts["original_inactive_vertex_parent_quota_checks"] += 1
                assert len(groups) <= remaining + int(partial)
                counts["bounded_multi_parent_response_group_states"] += 1
                counts["known_original_frontier_records"] += known
                counts["source_incomplete_states" if partial else "source_complete_states"] += 1
    counts["original_blow_up_graphs"] += 1


def five_cycle(counts):
    graph = nx.cycle_graph(5)
    gamma = F(1, 2)
    lam = F(1, 64)
    kappa = F(1, 128)
    previous = None
    profiles = []
    for labels in [[0], [0, 1, 4], [0, 1, 4, 2]]:
        if previous is not None:
            for i in set(labels) - set(previous):
                assert gamma * sum(previous.get(j, F(0)) for j in graph[i]) > (lam + kappa) * 2
        matrix = [
            [F(2) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in labels]
            for i in labels
        ]
        values = dict(zip(labels, solve(matrix, [F(i == 0) - 2 * lam for i in labels])))
        assert min(values.values()) > 0
        residual = {
            i: F(i == 0)
            - 2 * values.get(i, F(0))
            + gamma * sum(values.get(j, F(0)) for j in graph[i])
            for i in graph
        }
        for i in labels:
            assert residual[i] == 2 * lam
        assert min(residual.values()) >= 0
        profiles.append(
            {
                "active_original_vertices": labels,
                "values": {str(i): str(x) for i, x in values.items()},
                "original_residuals": {str(i): str(x) for i, x in residual.items()},
            }
        )
        previous = values
    partition, owner, quotient = types(graph)
    assert len(partition) == 5 and quotient.number_of_edges() == 5
    assert owner[3] != owner[0]
    wrong = 2 * values[0] - 1 + 2 * lam
    assert wrong - residual[3] == F(365, 6688) > 0
    assert residual[3] > (lam + kappa) * 2
    counts["nonterminal_five_cycle_positive_prefixes"] += 3
    counts["false_tree_only_source_twin_identity_witnesses"] += 1
    return {
        "alpha_lazy": "1/3",
        "lambda": "1/64",
        "kappa": "1/128",
        "eps_appr": "1/32",
        "seed": 0,
        "graph": "cycle 0-1-2-3-4-0",
        "prefixes": profiles,
        "true_candidate_3_residual": str(residual[3]),
        "incorrect_seed_twin_formula": str(wrong),
        "identity_gap": "365/6688",
        "scope": "both true and incorrect gates are positive here; this is an identity/classification obstruction, not a wrong-output claim",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts = Counter()
    for base in nx.graph_atlas_g():
        n = len(base)
        if n < 2 or n > (6 if args.full else 4) or not nx.is_connected(base):
            continue
        if base.number_of_edges() - n + 1 > 3:
            continue
        for mask in sorted({0, 2**n - 1, sum(1 << i for i in base if i % 2 == 0)}):
            graph, _ = blow_up(base, [2 + i % 2 for i in range(n)], mask)
            check_graph(graph, counts)
    witness = five_cycle(counts)
    result = {
        "description": __doc__,
        "full": args.full,
        "arithmetic": "exact fractions and integer set identities",
        "random_seed": None,
        "graph": "all connected graph-atlas base graphs through 6 vertices in full mode (4 otherwise), base cycle rank at most 3, sizes 2+i%2 and independent/clique/alternating masks; canonical original twin types recomputed independently",
        "active_states": "every connected canonical quotient subset, every active source type, complete source type or source singleton",
        "alpha_and_accuracy": "not applicable to combinatorial quotas; five-cycle parameters are recorded in its witness",
        "stopping_rule": "exhaust prescribed finite combinatorial states and three nonterminal positive numerical prefixes",
        "audit_only": dict(counts),
        "five_cycle_witness": witness,
        "scope": "Only combinatorial quotas and the stated identity obstruction. No local numeric algorithm or work bound is asserted.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ["frontier_neighborhood_types.py", "geometric_value_events.py"]
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
