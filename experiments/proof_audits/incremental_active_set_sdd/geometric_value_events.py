"""Exact falsification audit for the OP3 geometric-value-event reduction.

Dense rational face solves supply an explicitly unimplemented change oracle.
Only its *delivered* events are output-sensitive. The audit charges and reports
the dense reference work separately; it is not an OP3 algorithm or benchmark.
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

import networkx as nx


def solve(matrix, rhs):
    """Exact Gaussian elimination; proof oracle only, never a local backend."""
    n = len(rhs)
    a = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    for k in range(n):
        assert a[k][k] > 0
        for i in range(k + 1, n):
            q = a[i][k] / a[k][k]
            for j in range(k, n + 1):
                a[i][j] -= q * a[k][j]
    x = [F(0)] * n
    for i in reversed(range(n)):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x


def mv(matrix, x):
    return [sum(a * b for a, b in zip(row, x)) for row in matrix]


def point(matrix, load, face):
    labels = sorted(face)
    y = solve([[matrix[i][j] for j in labels] for i in labels], [load[i] for i in labels])
    out = [F(0)] * len(load)
    for i, value in zip(labels, y):
        out[i] = value
    return out


def obstacle(matrix, load):
    face = {i for i, value in enumerate(load) if value > 0}
    while face:
        x = point(matrix, load, face)
        residual = [b - a for a, b in zip(mv(matrix, x), load)]
        new = {i for i, value in enumerate(residual) if value > 0 and i not in face}
        if not new:
            assert all(value >= 0 for value in x)
            return x
        face |= new
    return [F(0)] * len(load)


def check_case(graph, seed, alpha, epsilon, policy):
    n = len(graph)
    deg = [graph.degree(i) for i in range(n)]
    bar_alpha = 2 * alpha / (1 + alpha)
    gamma = 1 - bar_alpha
    lam, gate, ratio = epsilon / 2, 11 * epsilon / 20, F(5, 4)
    matrix = [
        [F(deg[i]) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in range(n)]
        for i in range(n)
    ]
    source = [F(int(i == seed)) for i in range(n)]
    load = [source[i] - lam * deg[i] for i in range(n)]
    if lam * deg[seed] >= 1:
        assert source[seed] <= epsilon * deg[seed]
        return Counter(cases=1, trivial=1), F(1, deg[seed]) / epsilon
    optimum = obstacle(matrix, load)
    face = {seed}
    last_batch = {seed}
    old = [F(0)] * n
    published = [F(0)] * n
    levels = [-1] * n
    lower_signal = [F(0)] * n
    event_counts = Counter()
    counts = Counter(cases=1)
    floor = epsilon / (16 * gamma) if gamma else F(1)

    while True:
        u = point(matrix, load, face)
        counts["dense_reference_faces"] += 1
        counts["dense_reference_coordinate_reads"] += len(face)
        counts["dense_reference_volume"] += sum(deg[i] for i in face)
        counts["dense_reference_elimination_cubic_proxy"] += len(face) ** 3
        assert all(old[i] <= u[i] <= optimum[i] for i in range(n))
        assert all(u[i] > 0 for i in face)
        residual = [source[i] - v for i, v in enumerate(mv(matrix, u))]
        assert min(residual) >= 0
        assert all(residual[i] == lam * deg[i] for i in face)
        assert (
            lam * sum(deg[i] for i in face)
            + bar_alpha * sum(deg[i] * u[i] for i in face)
            + sum(residual[i] for i in range(n) if i not in face)
            == 1
        )

        # This loop is the missing oracle, implemented by a charged dense scan.
        for i in sorted(face):
            previous = published[i]
            if published[i] == 0 and u[i] >= floor:
                published[i], levels[i] = floor, 0
                counts["bucket_level_operations"] += 1
            while published[i] > 0 and ratio * published[i] <= u[i]:
                published[i] *= ratio
                levels[i] += 1
                counts["bucket_level_operations"] += 1
            if published[i] != previous:
                assert published[i] >= (F(11, 10) * previous if previous else floor / 2)
                counts["delivered_events"] += 1
                counts["delivered_event_volume"] += deg[i]
                event_counts[i] += 1
                if old[i] > 0:
                    counts["old_coordinate_events"] += 1
                    counts["old_coordinate_event_volume"] += deg[i]
                for j in graph[i]:
                    lower_signal[j] += gamma * (published[i] - previous)
            if gamma:
                assert published[i] <= u[i] < ratio * published[i] + floor
        assert all(event_counts[i] <= levels[i] + 1 for i in face)

        for j in range(n):
            if j not in face:
                assert lower_signal[j] == gamma * sum(published[i] for i in graph[j])
                assert lower_signal[j] <= residual[j]
                assert residual[j] <= ratio * lower_signal[j] + epsilon * deg[j] / 16

        candidates = [i for i in range(n) if i not in face and lower_signal[i] > gate * deg[i]]
        assert all(residual[i] > lam * deg[i] and optimum[i] > 0 for i in candidates)
        if policy == "batch":
            counts["admissions_without_neighbor_in_latest_batch"] += sum(
                not (set(graph[i]) & last_batch) for i in candidates
            )
        if not candidates:
            assert all(residual[i] <= 3 * epsilon * deg[i] / 4 for i in range(n) if i not in face)
            assert sum(deg[i] for i in face) <= 2 / epsilon
            counts["final_volume"] += sum(deg[i] for i in face)
            counts["final_coordinates"] += len(face)
            # One-sided terminal repair under adverse certified solve errors.
            z, delta = [bar_alpha * value for value in u], bar_alpha * epsilon / 16
            labels = sorted(face)
            if n <= 4:
                patterns = itertools.product([-1, 1], repeat=len(labels))
            else:
                patterns = [
                    [1] * len(labels),
                    [-1] * len(labels),
                    [(-1) ** j for j in labels],
                    [(-1) ** (j + 1) for j in labels],
                ]
            maximum = F(0)
            for pattern in patterns:
                repaired = [F(0)] * n
                for i, sign in zip(labels, pattern):
                    approximate = z[i] + sign * delta
                    repaired[i] = max(F(0), approximate - delta)
                out_residual = [
                    source[i] - v / bar_alpha for i, v in enumerate(mv(matrix, repaired))
                ]
                assert all(0 <= out_residual[i] <= epsilon * deg[i] for i in range(n))
                assert all(0 <= repaired[i] <= z[i] for i in range(n))
                maximum = max(maximum, max(out_residual[i] / (epsilon * deg[i]) for i in range(n)))
                counts["terminal_repair_patterns"] += 1
            return counts, maximum
        if policy == "singleton":
            candidates = [min(candidates)]
        counts["admitted_after_seed"] += len(candidates)
        face.update(candidates)
        last_batch = set(candidates)
        old = u


def homotopy_check(graph, seed, rho, old_t):
    n = len(graph)
    deg = [graph.degree(i) for i in range(n)]
    load = [F(int(i == seed)) - rho * deg[i] for i in range(n)]
    points = []
    for t in [old_t, old_t / 2]:
        a = [
            [F(deg[i]) * (1 + t) if i == j else -F(int(graph.has_edge(i, j))) for j in range(n)]
            for i in range(n)
        ]
        points.append(obstacle(a, load))
    assert all(x <= y for x, y in zip(*points))
    return sum(x == 0 < y for x, y in zip(*points))


def overlapping_interval_checks():
    """Audit the finite-band policy, including equality and asymmetric errors."""
    h, ratio, growth = F(1), F(5, 4), F(11, 10)
    count = 0
    for level in range(-1, 10):
        old = F(0) if level == -1 else h * growth**level / 2
        values = [old + shift * h for shift in [F(0), F(1, 10), F(1, 2), F(1), F(10), F(100)]]
        values += [
            ratio * old + h + shift * h for shift in [F(-1, 4), F(-1, 16), F(0), F(1, 16), F(1, 4)]
        ]
        for value, left_error in itertools.product(values, [F(0), F(1, 16), F(1, 8), F(1, 4)]):
            low, high = value - left_error, value + h / 4 - left_error
            assert old <= value and low <= value <= high
            new = old
            if high > ratio * old + h:
                new = h / 2
                while growth * new <= low:
                    new *= growth
                assert new >= (growth * old if old else h / 2)
            assert old <= new <= value <= high <= ratio * new + h
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--structured", action="store_true")
    args = parser.parse_args()
    started = time.time()
    totals = Counter()
    totals["overlapping_interval_policy_checks"] = overlapping_interval_checks()
    maximum = F(0)
    alphas = [F(1), F(2, 3), F(1, 7), F(1, 101)]
    epsilons = [F(1, 5), F(2, 3), F(1, 31)]
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= args.max_n and nx.is_connected(g)]
    for graph_index, graph in enumerate(graphs):
        for seed, alpha, epsilon, policy in itertools.product(
            range(len(graph)), alphas, epsilons, ["batch", "singleton"]
        ):
            counts, mx = check_case(graph, seed, alpha, epsilon, policy)
            totals.update(counts)
            maximum = max(maximum, mx)
        for seed in graph:
            for rho in [F(1, 5), F(1, 31)]:
                totals["homotopy_births"] += homotopy_check(graph, seed, rho, F(3, 2))
                totals["homotopy_cases"] += 1
        if (graph_index + 1) % 25 == 0:
            print(
                json.dumps(
                    {
                        "graphs_done": graph_index + 1,
                        "cases": totals["cases"],
                        "elapsed_seconds": round(time.time() - started, 2),
                    }
                ),
                flush=True,
            )
    # Exact new-support counterexample to a multiplicative alpha-homotopy bracket.
    p3 = nx.path_graph(3)
    assert homotopy_check(p3, 0, F(1, 5), F(3, 2)) == 1
    structured_rows = []
    if args.structured:
        ladder = nx.ladder_graph(12)
        ladder.add_edges_from([(1, 16), (5, 21), (8, 18)])
        families = [
            ("path_32", nx.path_graph(32)),
            ("asymmetric_ladder_24", ladder),
            ("grid_5x6", nx.convert_node_labels_to_integers(nx.grid_2d_graph(5, 6))),
            ("barbell_5_14", nx.barbell_graph(5, 14)),
        ]
        for name, graph in families:
            for alpha, epsilon in itertools.product(
                [F(1, 1009), F(1, 1000003)], [F(1, 7), F(1, 13), F(3, 31)]
            ):
                counts, mx = check_case(graph, 0, alpha, epsilon, "batch")
                totals.update(counts)
                maximum = max(maximum, mx)
                structured_rows.append(
                    {
                        "graph": name,
                        "seed": 0,
                        "alpha": str(alpha),
                        "epsilon": str(epsilon),
                        "counts": dict(counts),
                        "maximum_residual_ratio": str(mx),
                    }
                )
                print(
                    json.dumps(
                        {
                            "structured_done": len(structured_rows),
                            "graph": name,
                            "elapsed_seconds": round(time.time() - started, 2),
                        }
                    ),
                    flush=True,
                )
    repo = Path(__file__).resolve().parents[3]

    def git(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()

    payload = {
        "audit": "incremental_active_set_sdd.geometric_value_events",
        "arithmetic": "exact fractions",
        "graph_family": "all connected graph-atlas representatives, every seed",
        "max_n": args.max_n,
        "graphs": len(graphs),
        "alpha_lazy": list(map(str, alphas)),
        "epsilon_acl": list(map(str, epsilons)),
        "random_seed": None,
        "policies": ["batch", "singleton"],
        "stopping_rule": "all current geometric buckets delivered and every exterior lower signal <= 11 epsilon d / 20",
        "counts": dict(totals),
        "structured_rows": structured_rows,
        "maximum_final_residual_over_epsilon_degree": str(maximum),
        "git_commit": git("rev-parse", "HEAD"),
        "dirty_worktree": bool(git("status", "--porcelain")),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.time() - started, 3),
        "limitation": "Dense reference solves and full scans supply the unimplemented event oracle; event counts alone are not runtime.",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
