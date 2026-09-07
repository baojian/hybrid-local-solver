"""Exact audit of fixed-lambda root-threshold changes on canonical trees.

All face solves, frontier scans, LCA construction and coefficient recomputation
are reference work. This script does not implement a fast local producer.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

from geometric_value_events import obstacle, point, solve
import networkx as nx


@dataclass
class Face:
    labels: frozenset
    interior: list
    matrix: list
    harmonic: dict
    offset: dict
    resistance: dict
    root: F
    values: list
    rows: dict


class Reference:
    def __init__(self, graph, seed, alpha, epsilon, counts):
        self.graph, self.seed, self.alpha, self.epsilon = graph, seed, alpha, epsilon
        self.gamma, self.lam = (1 - alpha) / (1 + alpha), epsilon / 2
        self.deg = dict(graph.degree())
        self.matrix = [
            [
                F(self.deg[i]) if i == j else -self.gamma if j in graph[i] else F(0)
                for j in range(len(graph))
            ]
            for i in range(len(graph))
        ]
        self.load = [F(i == seed) - self.lam * self.deg[i] for i in range(len(graph))]
        self.parent, self.depth = {seed: None}, {seed: 0}
        queue = [seed]
        for i in queue:
            for j in graph[i]:
                if j != self.parent[i]:
                    self.parent[j], self.depth[j] = i, self.depth[i] + 1
                    queue.append(j)
        self.counts, self.cache = counts, {}
        self.optimum = obstacle(self.matrix, self.load)
        counts["reference_obstacle_solves"] += 1

    def lca(self, i, j):
        while i != j:
            self.counts["reference_lca_ancestor_visits"] += 1
            if self.depth[i] >= self.depth[j]:
                i = self.parent[i]
            else:
                j = self.parent[j]
        return i

    def face(self, labels):
        key = frozenset(labels)
        if key in self.cache:
            self.counts["reference_face_cache_hits"] += 1
            return self.cache[key]
        seed, gamma, graph = self.seed, self.gamma, self.graph
        e = sorted(key - {seed})
        he = [[self.matrix[i][j] for j in e] for i in e]
        harmonic = dict(zip(e, solve(he, [gamma if seed in graph[i] else F(0) for i in e])))
        offset = dict(zip(e, solve(he, [self.load[i] for i in e])))
        harmonic[seed], offset[seed] = F(1), F(0)
        resistance = {seed: F(0)}
        for i in sorted(e, key=lambda j: self.depth[j]):
            p = self.parent[i]
            resistance[i] = resistance[p] + 1 / (gamma * harmonic[p] * harmonic[i])
        root = (self.load[seed] + gamma * sum(offset[i] for i in graph[seed] if i in key)) / (
            self.deg[seed] - gamma * sum(harmonic[i] for i in graph[seed] if i in key)
        )
        values = point(self.matrix, self.load, key)
        for i in key:
            assert values[i] == harmonic[i] * root + offset[i] > 0
            assert values[i] <= self.optimum[i]
        boundary = sorted({j for i in key for j in graph[i] if j not in key})
        rows = {}
        for j in boundary:
            p = self.parent[j]
            assert p in key and set(graph[j]) & key == {p}
            a, b = gamma * harmonic[p], self.load[j] + gamma * offset[p]
            assert a > 0 and b < 0
            assert a * root + b == gamma * values[p] - self.lam * self.deg[j]
            rows[j] = (a, b, -b / a)
        out = Face(key, e, he, harmonic, offset, resistance, root, values, rows)
        self.cache[key] = out
        self.counts["reference_distinct_faces"] += 1
        self.counts["reference_gaussian_solves"] += 3
        self.counts["reference_elimination_cubic_proxy"] += 2 * len(e) ** 3 + len(key) ** 3
        self.counts["reference_frontier_rows"] += len(rows)
        return out

    def update(self, before, after, w):
        q, gamma, seed = self.parent[w], self.gamma, self.seed
        column = dict(
            zip(before.interior, solve(before.matrix, [F(i == q) for i in before.interior]))
        )
        column[seed] = F(0)
        pivot = self.deg[w] - gamma * gamma * column[q]
        assert pivot > 0
        aw, bw, tauw = before.rows[w]
        kappa = gamma * gamma * before.harmonic[q] ** 2 / pivot
        for p in before.labels:
            ancestor = self.lca(p, q)
            rp, rl = before.resistance[p], before.resistance[ancestor]
            multiplier = 1 + kappa * rl
            assert column[p] == before.harmonic[p] * before.harmonic[q] * rl
            assert after.harmonic[p] == before.harmonic[p] * multiplier
            assert after.offset[p] == before.offset[p] + gamma * column[p] * bw / pivot
            assert after.resistance[p] == rl / multiplier + (rp - rl) / multiplier**2
            self.counts["reference_green_resistance_checks"] += 1
            self.counts["reference_harmonic_offset_updates"] += 1
            self.counts["reference_resistance_updates"] += 1
        groups, factors = {}, {}
        for j in before.rows.keys() & after.rows.keys():
            p = self.parent[j]
            c = gamma * gamma * column[p] / pivot
            a, b, tau = before.rows[j]
            aa, bb, tt = after.rows[j]
            assert aa == a + c * aw and bb == b + c * bw
            assert min(tau, tauw) <= tt <= max(tau, tauw)
            ratio = c * aw / a
            ancestor = self.lca(p, q)
            assert ratio == kappa * before.resistance[ancestor]
            if ancestor in groups:
                assert groups[ancestor] == ratio
                self.counts["reference_same_lca_factor_checks"] += 1
            else:
                groups[ancestor] = ratio
            factor = 1 / (1 + ratio)
            assert tt == factor * tau + (1 - factor) * tauw
            factors[j] = (ancestor, factor)
            self.counts["reference_schur_row_checks"] += 1
        self.counts["reference_green_column_solves"] += 1
        self.counts["reference_group_transforms"] += len(groups)
        self.counts["maximum_groups_one_admission"] = max(
            self.counts["maximum_groups_one_admission"], len(groups)
        )
        return pivot, factors


def witness(ref, policy, trace, before, after, w, pair, factors):
    def row(face, j):
        a, b, tau = face.rows[j]
        return {
            "a": str(a),
            "b": str(b),
            "threshold": str(tau),
            "gate_at_actual_root": str(a * face.root + b),
        }

    return {
        "vertices": len(ref.graph),
        "edges": sorted([sorted(e) for e in ref.graph.edges]),
        "seed": ref.seed,
        "alpha_lazy": str(ref.alpha),
        "eps_appr": str(ref.epsilon),
        "lambda": str(ref.lam),
        "policy": policy,
        "admission_prefix": trace[:],
        "face_before": sorted(before.labels),
        "admitted": w,
        "positive_before": [j for j, (a, b, _) in before.rows.items() if a * before.root + b > 0],
        "root_before": str(before.root),
        "root_after": str(after.root),
        "admitted_row_before": row(before, w),
        "pair": [
            {
                "label": j,
                "before": row(before, j),
                "after": row(after, j),
                "lca_group": factors[j][0],
                "affine_slope": str(factors[j][1]),
            }
            for j in pair
        ],
    }


def run_trace(ref, policy, counts, witnesses):
    counts["traces"] += 1
    if ref.load[ref.seed] <= 0:
        assert not any(ref.optimum)
        counts["empty_traces"] += 1
        return
    face = ref.face({ref.seed})
    trace, ready, queued = [ref.seed], deque(), set()
    published = {ref.seed: F(0)}
    while True:
        gates = {j: a * face.root + b for j, (a, b, _) in face.rows.items()}
        if policy.startswith("band"):
            for i in face.labels:
                published.setdefault(i, F(0))
                flux = ref.gamma * face.values[i]
                if flux > F(5, 4) * published[i] + ref.epsilon / 16:
                    published[i] = flux
                    counts["reference_band_publications"] += 1
            due = [
                j
                for j in face.rows
                if published[ref.parent[j]] > F(11, 20) * ref.epsilon * ref.deg[j]
            ]
        else:
            due = [j for j, gate in gates.items() if gate > 0]
        for j in sorted(due):
            if j not in queued:
                ready.append(j)
                queued.add(j)
        if policy == "minimum":
            if not due:
                break
            w = min(due, key=lambda j: (face.rows[j][2], j))
        else:
            if not ready:
                break
            w = ready.pop() if policy.endswith("lifo") else ready.popleft()
        assert gates[w] > 0
        after = ref.face(face.labels | {w})
        assert after.root > face.root
        assert all(x <= y for x, y in zip(face.values, after.values))
        _, factors = ref.update(face, after, w)
        quiet = [j for j in face.rows if gates[j] <= 0]
        for j, k in combinations(quiet, 2):
            old_delta = face.rows[j][2] - face.rows[k][2]
            new_delta = after.rows[j][2] - after.rows[k][2]
            counts["quiet_pair_comparisons"] += 1
            if old_delta * new_delta < 0:
                counts["strict_quiet_order_flips"] += 1
                witnesses.setdefault(
                    "quiet_order_flip", witness(ref, policy, trace, face, after, w, (j, k), factors)
                )
        if quiet:
            j = min(quiet, key=lambda i: (face.rows[i][2], i))
            aa, bb, _ = after.rows[j]
            if aa * after.root + bb <= 0:
                for k in quiet:
                    a, b, _ = after.rows[k]
                    if a * after.root + b > 0:
                        counts["old_quiet_minimum_misses_positive"] += 1
                        witnesses.setdefault(
                            "old_quiet_minimum_miss",
                            witness(ref, policy, trace, face, after, w, (j, k), factors),
                        )
                        if sum(g > 0 for g in gates.values()) == 1:
                            counts["only_previous_positive_minimum_misses"] += 1
                            witnesses.setdefault(
                                "only_previous_positive_minimum_miss",
                                witness(ref, policy, trace, face, after, w, (j, k), factors),
                            )
                        if a * after.root + b > ref.lam * ref.deg[k]:
                            counts["old_quiet_minimum_misses_acl"] += 1
                            witnesses.setdefault(
                                "old_quiet_minimum_acl_miss",
                                witness(ref, policy, trace, face, after, w, (j, k), factors),
                            )
        counts["legal_admissions"] += 1
        face = after
        trace.append(w)
    for i in ref.graph:
        residual = F(i == ref.seed) - sum(ref.matrix[i][j] * face.values[j] for j in ref.graph)
        assert F(0) <= residual <= ref.epsilon * ref.deg[i]
    if not policy.startswith("band"):
        assert face.values == ref.optimum
        counts["exact_obstacle_final_comparisons"] += 1
    counts["acl_final_checks"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, witnesses = Counter(), {}
    parameters = [
        (F(1, 3), F(1, 5)),
        (F(1, 3), F(1, 20)),
        (F(1, 7), F(1, 20)),
        (F(1, 7), F(1, 50)),
        (F(1, 1009), F(1, 50)),
        (F(1, 1009), F(1, 1009)),
    ]
    policies = ["minimum", "fifo", "lifo", "band_fifo", "band_lifo"]
    for n in range(2, args.max_n + 1):
        for graph0 in nx.nonisomorphic_trees(n):
            graph = nx.convert_node_labels_to_integers(graph0, ordering="sorted")
            for seed in graph:
                for alpha, epsilon in parameters:
                    ref = Reference(graph, seed, alpha, epsilon, counts)
                    for policy in policies:
                        run_trace(ref, policy, counts, witnesses)
        print(
            json.dumps(
                {
                    "through_n": n,
                    "traces": counts["traces"],
                    "flips": counts["strict_quiet_order_flips"],
                    "misses": counts["old_quiet_minimum_misses_positive"],
                    "strong_misses": counts["only_previous_positive_minimum_misses"],
                }
            ),
            flush=True,
        )
    result = {
        "audit": "incremental_active_set_sdd.root_threshold_order",
        "arithmetic": "exact fractions",
        "graph": "all nonisomorphic trees through max_n",
        "max_n": args.max_n,
        "seed": "every vertex",
        "random_seed": None,
        "parameters_alpha_epsilon": [[str(a), str(e)] for a, e in parameters],
        "policies": policies,
        "stopping_rule": "exact obstacle quietness or original-physical finite-band ACL stop",
        "cost_scope": "all computations are reference-only; no fast local producer claimed",
        "counts": dict(counts),
        "witnesses": witnesses,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reference_backend_sha256": hashlib.sha256(
            Path(__file__).with_name("geometric_value_events.py").read_bytes()
        ).hexdigest(),
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"counts": dict(counts), "witnesses": witnesses}, indent=2))


if __name__ == "__main__":
    main()
