"""Supplied multipartite scalar-response audit, not a local solver.

Part membership and degrees are supplied to this algebraic reference.
It verifies the common scalar coordinate, transformed breakpoints and
monotone positive-gate insertion of parts against full original obstacle
solutions. Adjacency-only startup and online part-discovery accounting
remain a separate unimplemented proposal.
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
import time

from geometric_value_events import obstacle
import networkx as nx


def response(z, degree, pendants, gamma, lam):
    if z <= 0:
        return F(0)
    if gamma * z <= degree * lam:
        return z / degree
    return (z - gamma * lam * pendants) / (degree - gamma * gamma * pendants)


def part_curve(group, degrees, pendants, seed, gamma, lam, counts):
    events = []
    coefficients = {i: (F(0), F(0)) for i in group}
    for i in group:
        d = degrees[i]
        t = pendants[i]
        b = F(i == seed) - lam * d
        events.append((-b, i, (F(1, d), b / d)))
        if t:
            events.append(
                (
                    d * lam / gamma - b,
                    i,
                    (1 / (d - gamma * gamma * t), (b - gamma * lam * t) / (d - gamma * gamma * t)),
                )
            )
    events.sort(key=lambda row: (row[0], row[1]))
    a = b = F(0)
    out = []
    last_s = None
    for threshold, i, updated in events:
        old = coefficients[i]
        assert old[0] * threshold + old[1] == updated[0] * threshold + updated[1]
        transformed = threshold / gamma + a * threshold + b
        a += updated[0] - old[0]
        b += updated[1] - old[1]
        coefficients[i] = updated
        assert last_s is None or transformed >= last_s
        last_s = transformed
        out.append((transformed, (gamma * a / (1 + gamma * a), b / (1 + gamma * a))))
        counts["transformed_breakpoint_checks"] += 1
        counts["negative_transformed_breakpoints"] += transformed < 0
    return out


def supplied_solve(groups, degrees, pendants, seed, gamma, lam, counts):
    current = {}
    future = []
    curves = {}
    for g, group in enumerate(groups):
        curves[g] = part_curve(group, degrees, pendants, seed, gamma, lam, counts)
        current[g] = (F(0), F(0))
        for s, piece in curves[g]:
            if s <= 0:
                current[g] = piece
            else:
                future.append((s, g, piece))
    future.sort(key=lambda row: (row[0], row[1]))
    a = sum(x[0] for x in current.values())
    b = sum(x[1] for x in current.values())
    cursor = 0
    while True:
        assert 0 <= a < 1 and b >= 0
        root = b / (1 - a)
        if cursor == len(future) or root <= future[cursor][0]:
            break
        at, g, piece = future[cursor]
        cursor += 1
        old = current[g]
        assert old[0] * at + old[1] == piece[0] * at + piece[1]
        a += piece[0] - old[0]
        b += piece[1] - old[1]
        current[g] = piece
        counts["global_crossed_breakpoints"] += 1
    values = {}
    for g, group in enumerate(groups):
        mass = current[g][0] * root + current[g][1]
        input_value = gamma * (root - mass)
        assert input_value >= 0
        for i in group:
            z = F(i == seed) - lam * degrees[i] + input_value
            values[i] = response(z, degrees[i], pendants[i], gamma, lam)
        assert sum(values[i] for i in group) == mass
    assert sum(values.values()) == root
    counts["supplied_scalar_fixed_points"] += 1
    return root, values


def check_case(sizes, pendants, seed, alpha, lam, counts):
    n = sum(sizes)
    gamma = (1 - alpha) / (1 + alpha)
    groups = []
    start = 0
    for size in sizes:
        groups.append(list(range(start, start + size)))
        start += size
    membership = {i: g for g, group in enumerate(groups) for i in group}
    degrees = {i: n - sizes[membership[i]] + pendants[i] for i in range(n)}
    root, values = supplied_solve(groups, degrees, pendants, seed, gamma, lam, counts)
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(
        (i, j) for i in range(n) for j in range(i + 1, n) if membership[i] != membership[j]
    )
    next_vertex = n
    parents = {}
    for i, t in enumerate(pendants):
        for _ in range(t):
            graph.add_edge(i, next_vertex)
            parents[next_vertex] = i
            next_vertex += 1
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in graph]
    exact = obstacle(matrix, load)
    assert all(values[i] == exact[i] for i in range(n))
    assert all(exact[j] == max(F(0), gamma * values[i] - lam) for j, i in parents.items())
    # Reference-only part discovery: the partition lookup below is supplied,
    # and each solve rebuilds curves. Neither is the proposed fast local code.
    known = {membership[seed]}
    last_root = F(0)
    old = {}
    while True:
        partial = [groups[g] for g in sorted(known)]
        s, u = supplied_solve(partial, degrees, pendants, seed, gamma, lam, counts)
        assert s >= last_root and all(u[i] >= x for i, x in old.items())
        candidates = [i for i in range(n) if membership[i] not in known]
        if not candidates or gamma * s <= min(lam * degrees[i] for i in candidates):
            assert s == root and all(u.get(i, F(0)) == values[i] for i in range(n))
            break
        chosen = min(candidates, key=lambda i: (degrees[i], i))
        assert gamma * s - lam * degrees[chosen] > 0 and exact[chosen] > 0
        group = membership[chosen]
        inside = sum(membership[i] == group for i in candidates)
        assert len(candidates) - inside <= degrees[chosen]
        counts["positive_part_insertion_checks"] += 1
        counts["paid_complement_scan_identity_checks"] += 1
        known.add(group)
        last_root = s
        old = u
    counts["full_original_obstacle_comparisons"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts = Counter()
    sizes_list = [[1, 1, 1], [2, 2], [2, 3], [1, 2, 2], [2, 2, 2], [1, 2, 3]]
    params = [(F(1, 3), F(1, 20)), (F(1, 1009), F(1, 200)), (F(1008, 1009), F(1, 20))]
    for sizes in sizes_list:
        n = sum(sizes)
        patterns = [[0] * n, [i % 3 for i in range(n)], [3 if i % 2 else 0 for i in range(n)]]
        for pendant, seed, (alpha, lam) in itertools.product(patterns, range(n), params):
            check_case(sizes, pendant, seed, alpha, lam, counts)
    result = {
        "audit": "incremental_active_set_sdd.multipartite_scalar_response",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "part_sizes": sizes_list,
        "pendant_patterns": "all zero, i mod 3, or alternating zero/three",
        "seed": "every core vertex",
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in params],
        "stopping_rule": "supplied transformed-breakpoint scalar fixed point; reference part insertion stops at original nonpositive unknown-part gates",
        "scope": "Algebraic supplied-part reference and original-matrix validation only. Local two-positive-row startup, implicit part discovery and incremental curve insertion are not implemented and remain Conditional/Open. No end-to-end local theorem is asserted.",
        "audit_only": dict(counts),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "geometric_value_events": hashlib.sha256(
                Path(__file__).with_name("geometric_value_events.py").read_bytes()
            ).hexdigest()
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
