"""Exact parameter-interval audit of minimum-root-threshold tree traces.

The selected next label is independent of lambda until stopping. This supplied
whole-tree oracle explores that sequence and verifies possible witnesses with
independent dense rational face solves. No fast local algorithm is claimed.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

import networkx as nx
from root_threshold_order import Reference, witness


def tree_solve(graph, labels, seed, gamma, rhs, counts):
    parent, order = {seed: None}, [seed]
    for i in order:
        for j in graph[i]:
            counts["reference_adjacency_reads"] += 1
            if j in labels and j != parent[i]:
                parent[j] = i
                order.append(j)
    pivots, loads = {i: F(graph.degree(i)) for i in labels}, dict(rhs)
    for i in reversed(order[1:]):
        p = parent[i]
        pivots[p] -= gamma * gamma / pivots[i]
        loads[p] += gamma * loads[i] / pivots[i]
    out = {seed: loads[seed] / pivots[seed]}
    for i in order[1:]:
        out[i] = (loads[i] + gamma * out[parent[i]]) / pivots[i]
    counts["reference_tree_solves"] += 1
    counts["reference_tree_pivots"] += len(labels)
    return out


def check(graph, seed, alpha, counts, witnesses):
    gamma = (1 - alpha) / (1 + alpha)
    parent, order = {seed: None}, [seed]
    for i in order:
        for j in graph[i]:
            if j != parent[i]:
                parent[j] = i
                order.append(j)

    def data(labels):
        src = tree_solve(graph, labels, seed, gamma, {i: F(i == seed) for i in labels}, counts)
        dr = tree_solve(graph, labels, seed, gamma, {i: F(graph.degree(i)) for i in labels}, counts)
        boundary = sorted({j for i in labels for j in graph[i] if j not in labels})
        cutoffs = {
            j: gamma * src[parent[j]] / (graph.degree(j) + gamma * dr[parent[j]]) for j in boundary
        }
        return src, dr, cutoffs

    labels, prefix = {seed}, [seed]
    cap = F(1, graph.degree(seed))
    _, _, old = data(labels)
    counts["parameter_independent_traces"] += 1
    while old:
        w = min(old, key=lambda j: (-old[j], j))
        cap = min(cap, old[w], F(1, 2))
        new_src, new_dr, new = data(labels | {w})
        others = sorted(set(old) - {w}, key=lambda j: (-old[j], j))

        def save(kind, j, k, low, high):
            counts[kind] += 1
            if kind in witnesses:
                return
            lam = (low + high) / 2
            for denominator in range(1, 10001):
                candidate = F((low * denominator).__floor__() + 1, denominator)
                if candidate < high:
                    lam = candidate
                    break
            ref = Reference(graph, seed, alpha, 2 * lam, Counter())
            face = ref.face({seed})
            for nxt in prefix[1:]:
                assert min(face.rows, key=lambda j: (face.rows[j][2], j)) == nxt
                assert face.rows[nxt][0] * face.root + face.rows[nxt][1] > 0
                face = ref.face(face.labels | {nxt})
            assert face.labels == labels
            assert min(face.rows, key=lambda j: (face.rows[j][2], j)) == w
            assert face.rows[w][0] * face.root + face.rows[w][1] > 0
            after = ref.face(labels | {w})
            _, factors = ref.update(face, after, w)
            record = witness(ref, "minimum", prefix, face, after, w, (j, k), factors)
            record["valid_lambda_interval"] = [str(low), str(high)]
            record["old_lambda_cutoffs"] = {i: str(x) for i, x in old.items()}
            record["new_lambda_cutoffs"] = {i: str(x) for i, x in new.items()}
            witnesses[kind] = record

        for j, k in combinations(others, 2):
            counts["surviving_pair_order_checks"] += 1
            if old[j] > old[k] and new[j] < new[k]:
                counts["algebraic_strict_order_flips"] += 1
                low = max(old[j], old[k])
                if low < cap:
                    save("legal_quiet_order_flip", j, k, low, cap)
        if others:
            j = others[0]
            for k in others[1:]:
                low = max(old[j], new[j])
                high = min(cap, new[k])
                if low < high:
                    save("legal_stale_minimum_miss", j, k, low, high)
                acl_cutoff = (
                    gamma * new_src[parent[k]] / (2 * graph.degree(k) + gamma * new_dr[parent[k]])
                )
                high = min(cap, acl_cutoff)
                if low < high:
                    save("legal_stale_minimum_acl_miss", j, k, low, high)
        # Select the same label for every lambda below the updated prefix cap.
        labels.add(w)
        prefix.append(w)
        old = new
        counts["symbolic_admissions"] += 1
    assert labels == set(graph)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, witnesses = Counter(), {}
    parameters = [F(1, 3), F(1, 7), F(1, 1009)]
    for n in range(2, args.max_n + 1):
        for graph0 in nx.nonisomorphic_trees(n):
            graph = nx.convert_node_labels_to_integers(graph0, ordering="sorted")
            for seed in graph:
                for alpha in parameters:
                    check(graph, seed, alpha, counts, witnesses)
        print(
            json.dumps(
                {
                    "through_n": n,
                    "traces": counts["parameter_independent_traces"],
                    "algebraic_flips": counts["algebraic_strict_order_flips"],
                    "witness_types": list(witnesses),
                }
            ),
            flush=True,
        )
    result = {
        "audit": "incremental_active_set_sdd.minimum_root_threshold",
        "graph": "all nonisomorphic trees through max_n",
        "max_n": args.max_n,
        "seed": "every vertex",
        "random_seed": None,
        "alpha_lazy": [str(a) for a in parameters],
        "epsilon": "eps_appr=2 lambda; exact intervals inside (0,1/2) tested",
        "policy": "minimum current root threshold; vertex-label ties",
        "stopping_rule": "symbolic complete minimum sequence; each witness stops at its named prefix",
        "arithmetic": "exact fractions",
        "cost_scope": "supplied full-tree audit only",
        "counts": dict(counts),
        "witnesses": witnesses,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reference_backend_sha256": hashlib.sha256(
            Path(__file__).with_name("root_threshold_order.py").read_bytes()
        ).hexdigest(),
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
