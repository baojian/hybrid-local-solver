"""Local multipartite-plus-pendants obstacle solver for every physical seed.

Canonical non-leaf core discovery removes the minimum core degree promise.
A forced-positive leaf seed is eliminated at its already certified positive
neighbor, preserving original degrees in all penalties and certificates.
The incremental part/event engine is shared with the narrow core-seed solver.
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

# Support both the registered -m entry point and direct audit execution.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from geometric_value_events import obstacle
from local_multipartite_pendants import (
    ImplicitMultipartite,
    LocalMultipartite,
    ReversedRows,
    explicit_graph,
)
from local_sun_solver import Oracle
from multipartite_scalar_response import response


class CanonicalMultipartite(LocalMultipartite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minimum_core_degree = 1

    def make_kernel(self, i, core_degree):
        degree = self.oracle.degree(i)
        special = self.forced_seed is not None and i == self.anchor
        diagonal = degree - self.gamma * self.gamma * special
        load = (self.gamma * (1 - self.lam) if special else F(i == self.seed)) - self.lam * degree
        leaves = degree - core_degree - special
        assert diagonal > 0 and leaves >= 0
        return diagonal, load, leaves

    def run(self):
        degree = self.oracle.degree(self.seed)
        if self.lam * degree >= 1:
            self.counts["trivial_zero_stops"] += 1
            return {}
        if degree == 1:
            row = self.oracle.row(self.seed)
            self.cached[self.seed] = row
            self.counts["source_leaf_row_words"] += 1
            self.anchor = row[0]
            gate = self.gamma * (1 - self.lam) - self.lam * self.oracle.degree(self.anchor)
            self.counts["source_leaf_original_gate_tests"] += 1
            if gate <= 0:
                self.counts["exact_source_leaf_stops"] += 1
                self.counts["output_words"] += 1
                return {self.seed: 1 - self.lam}
            self.forced_seed = self.seed
            self.counts["positive_source_leaf_eliminations"] += 1
        neighbors = self.read_core(self.anchor)
        diagonal, load, leaves = self.make_kernel(self.anchor, len(neighbors))
        value = response(load, diagonal, leaves, self.gamma, self.lam)
        assert value > 0
        chosen = None
        for i in neighbors:
            self.counts["startup_original_gate_tests"] += 1
            if self.gamma * value > self.lam * self.oracle.degree(i):
                if chosen is None or self.oracle.degree(i) < self.oracle.degree(chosen):
                    chosen = i
        if chosen is None:
            self.counts["exact_anchor_star_stops"] += 1
            return self.output({self.anchor: value})
        return self.continue_core(self.anchor, neighbors, chosen)


def audit_case(sizes, pendants, seed, alpha, lam, counts, reverse):
    graph, _ = explicit_graph(sizes, pendants)
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in graph]
        for i in graph
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in graph]
    exact = obstacle(matrix, load)
    last = {}

    def validate(state, kind):
        known = set(state.membership)
        region = sorted(known | {j for i in known for j in graph[i] if graph.degree(j) == 1})
        partial = obstacle(
            [[matrix[i][j] for j in region] for i in region], [load[i] for i in region]
        )
        expanded = dict(zip(region, partial))
        predicted = {}
        for g, vertices in enumerate(state.groups):
            a, b = state.current[g]
            mass = a * state.total + b
            field = gamma * (state.total - mass)
            for i in vertices:
                diagonal, rhs, leaves = state.kernels[i]
                predicted[i] = response(rhs + field, diagonal, leaves, gamma, lam)
        assert all(predicted[i] == expanded[i] for i in known)
        assert sum(predicted.values()) == state.total
        assert all(x <= exact[i] for i, x in expanded.items())
        assert all(expanded.get(i, F(0)) >= x for i, x in last.items())
        last.update(expanded)
        if state.forced_seed is not None:
            assert expanded[seed] == 1 - lam + gamma * expanded[state.anchor]
            counts["independent_forced_seed_recoveries"] += 1
        for i in graph:
            if graph.degree(i) > 1 and i not in known:
                gate = load[i] - sum(matrix[i][j] * x for j, x in expanded.items())
                assert gate == gamma * state.total - lam * graph.degree(i)
                counts["independent_unknown_original_gate_checks"] += 1
        counts["independent_restricted_obstacle_checks"] += 1
        counts["reference_original_matrix_words"] += len(region) ** 2
        counts["reference_recovered_core_values"] += len(predicted)
        counts["positive_unknown_gate_checkpoints"] += kind == "positive unknown gate"

    state = CanonicalMultipartite(
        Oracle(ReversedRows(graph) if reverse else graph), seed, alpha, lam, validate
    )
    out = state.run()
    assert [out.get(i, F(0)) for i in graph] == exact
    assert state.oracle.rows == set(out)
    volume = sum(graph.degree(i) for i in out)
    assert lam * volume < 1
    assert state.oracle.counts["adjacency_entries_inspected"] == volume
    c = state.counts
    assert c["new_part_coordinate_records"] == len(state.membership)
    assert c["created_coordinate_events"] <= 2 * len(state.membership)
    assert (
        c["future_event_insertions"] + c["past_new_part_events_consumed"]
        == c["created_coordinate_events"]
    )
    assert c["crossed_global_events"] <= c["future_event_insertions"]
    assert (
        c["complement_membership_tests"]
        == c["complement_outside_incidence_charges"] + c["complement_removed_identifier_charges"]
    )
    assert c["complement_outside_incidence_charges"] <= c["positive_representative_degree_budget"]
    assert c["final_core_value_words"] == len(state.membership)
    counts["complete_original_obstacle_comparisons"] += 1
    counts["physical_leaf_seed_cases"] += graph.degree(seed) == 1
    counts["original_core_degree_one_cases"] += min(sum(sizes) - size for size in sizes) == 1
    counts["positive_only_original_row_certificates"] += 1
    return state


def implicit_cases(counts):
    families = [
        ([1, 2], [0, 0, 10**18]),
        ([1, 1], [0, 10**18]),
        ([1, 2, 2], [2, 0, 2, 10**18, 10**18]),
        ([2, 2, 2], [2, 2, 0, 1, 0, 10**18]),
    ]
    records = []
    for (sizes, pendants), alpha, reverse in itertools.product(
        families, [F(1, 3), F(1, 1009)], [False, True]
    ):
        graph = ImplicitMultipartite(sizes, pendants)
        seeds = [0] + [(i, 0) for i, t in enumerate(pendants) if t]
        for seed in seeds:
            state = CanonicalMultipartite(
                Oracle(ReversedRows(graph) if reverse else graph), seed, alpha, F(1, 40)
            )
            out = state.run()
            core = {i: out.get(i, F(0)) for i in range(graph.core_n)}
            masses = [
                sum(core[i] for i in range(graph.core_n) if graph.membership[i] == g)
                for g in range(len(sizes))
            ]
            total = sum(masses)
            for i, leaves in enumerate(pendants):
                value = core[i]
                ordinary = max(F(0), state.gamma * value - state.lam)
                special = isinstance(seed, tuple) and seed[0] == i
                leaf_sum = leaves * ordinary
                if special:
                    seeded = 1 - state.lam + state.gamma * value
                    assert out[seed] == seeded
                    leaf_sum += seeded - ordinary
                residual = (
                    F(i == seed)
                    - graph.degree(i) * value
                    + state.gamma * (total - masses[graph.membership[i]] + leaf_sum)
                )
                assert residual >= 0
                assert (
                    residual == state.lam * graph.degree(i)
                    if value > 0
                    else residual <= state.lam * graph.degree(i)
                )
                if ordinary > 0:
                    assert all(out[(i, j)] == ordinary for j in range(leaves) if (i, j) != seed)
                else:
                    assert state.gamma * value <= state.lam
            assert state.oracle.rows == set(out)
            volume = sum(graph.degree(i) for i in out)
            assert (
                state.lam * volume < 1
                and state.oracle.counts["adjacency_entries_inspected"] == volume
            )
            counts["implicit_original_kkt_certificates"] += 1
            records.append(
                {
                    "part_sizes": sizes,
                    "pendant_counts": pendants,
                    "ambient_vertices": graph.core_n + sum(pendants),
                    "seed": seed,
                    "alpha_lazy": str(alpha),
                    "lambda": str(state.lam),
                    "reverse_rows": reverse,
                    "positive_vertices": len(out),
                    "original_volume": volume,
                    "algorithm_counts": dict(state.counts),
                    "original_graph_access": dict(state.oracle.counts),
                }
            )
    return records


def exact_ties(counts):
    records = []
    for alpha, reverse in itertools.product([F(1, 3), F(1, 1009), F(1008, 1009)], [False, True]):
        gamma = (1 - alpha) / (1 + alpha)
        specs = [
            ("leaf-to-anchor zero gate", [1, 1], [1, 0], 2, gamma / (2 + gamma), {2}),
            (
                "ordinary leaf birth after forced seed",
                [1, 1],
                [1, 0],
                2,
                gamma * gamma / (2 * (1 + gamma)),
                {0, 2},
            ),
            (
                "forced-seed unknown-part gate",
                [1, 1, 1],
                [1, 0, 4],
                3,
                gamma * gamma * (2 + gamma) / (36 + 12 * gamma - 11 * gamma * gamma - gamma**3),
                {0, 1, 3},
            ),
            ("physical source zero gate", [1, 1], [0, 0], 0, F(1), set()),
        ]
        for kind, sizes, pendants, seed, lam, expected_rows in specs:
            state = audit_case(sizes, pendants, seed, alpha, lam, counts, reverse)
            assert state.oracle.rows == expected_rows
            if kind == "forced-seed unknown-part gate":
                assert state.unknown == {2: None}
                assert state.total == state.unknown_heap[0][0]
            records.append(
                {
                    "kind": kind,
                    "alpha_lazy": str(alpha),
                    "lambda": str(lam),
                    "seed": seed,
                    "reverse_rows": reverse,
                    "positive_rows": sorted(expected_rows),
                    "algorithm_counts": dict(state.counts),
                }
            )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, algorithm, access = Counter(), Counter(), Counter()
    sizes_list = [[1, 1], [1, 2], [1, 3], [1, 1, 1], [2, 2]]
    if args.full:
        sizes_list += [[1, 2, 2], [2, 2, 2], [1, 1, 2, 2], [1, 5], [1, 1, 1, 1]]
    params = [
        (F(1, 3), F(1, 20)),
        (F(1, 1009), F(1, 200)),
        (F(1008, 1009), F(1, 20)),
        (F(1, 3), F(1, 4)),
    ]
    for sizes in sizes_list:
        n = sum(sizes)
        patterns = [[0] * n, [i % 3 for i in range(n)], [3 if i % 2 else 0 for i in range(n)]]
        if args.full:
            patterns += [[4 if i == j else 0 for i in range(n)] for j in range(n)]
        for pendants in patterns:
            for seed, (alpha, lam), reverse in itertools.product(
                range(n + sum(pendants)), params, [False, True]
            ):
                state = audit_case(sizes, pendants, seed, alpha, lam, counts, reverse)
                algorithm.update(state.counts)
                access.update(state.oracle.counts)
    ties = exact_ties(counts)
    implicit = implicit_cases(counts)
    result = {
        "audit": "incremental_active_set_sdd.canonical_multipartite_pendants",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "part_size_patterns": sizes_list,
        "pendant_patterns": "zero, i mod3, alternating zero/three; full adds every single four-leaf attachment",
        "seed": "every original vertex, including private and unadorned core leaves",
        "row_orders": ["construction", "reversed"],
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in params],
        "stopping_rule": "exact original source-leaf/anchor-star exits or exact restricted scalar root with nonpositive original unknown-part gates",
        "scope": "Degree/adjacency-only solver on promised complete multipartite cores with private leaves, every physical seed, no minimum core degree. Canonical core/partition not supplied. Exact-real words, not finite-precision or arbitrary-graph OP3.",
        "algorithm_counts": dict(algorithm),
        "original_graph_access": dict(access),
        "audit_only": dict(counts),
        "implicit_cases": implicit,
        "exact_ties": ties,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "local_multipartite_pendants",
                "multipartite_scalar_response",
                "local_sun_solver",
                "geometric_value_events",
            ]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
