"""Exact local parametric RPPR on a cycle with arbitrary pendant-leaf counts.

The algorithm receives only degree/row access and an arbitrary seed. It
does not know the cycle size or future leaf counts. Two tips suffice before
closure; at most three cycle variables remain in the closing Schur system.
This is a scoped research implementation, not an arbitrary-graph OP3 solver.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from geometric_value_events import obstacle, solve
import networkx as nx


class Oracle:
    def __init__(self, graph):
        self._graph = graph
        self.degrees = {}
        self.rows = set()
        self.counts = Counter()

    def degree(self, i):
        self.counts["degree_cache_lookups"] += 1
        if i not in self.degrees:
            self.degrees[i] = self._graph.degree(i)
            self.counts["degree_queries"] += 1
        return self.degrees[i]

    def row(self, i):
        assert i not in self.rows
        self.rows.add(i)
        neighbors = list(self._graph[i])
        self.counts["row_scans"] += 1
        self.counts["adjacency_entries_inspected"] += len(neighbors)
        return neighbors


@dataclass
class Center:
    label: int
    degree: int
    leaves: list[int]
    ports: list[int]


@dataclass
class Tip:
    center: Center
    delta: F
    a: F
    b: F
    settled: bool


@dataclass
class Arm:
    candidate: int
    tip: Tip | None = None
    committed: list[Tip] = field(default_factory=list)


def local_sun(oracle, seed, alpha, lam):
    gamma = 1 - 2 * alpha / (1 + alpha)
    assert 0 < gamma < 1 and lam > 0
    d_seed = oracle.degree(seed)
    if lam * d_seed >= 1:
        return {}, {"events": 0, "closure": False}
    source_leaf = None
    root_label = seed
    root_delta, root_load = F(d_seed), 1 - lam * d_seed
    if d_seed == 1:
        source_leaf = seed
        root_label = oracle.row(seed)[0]
        d_root = oracle.degree(root_label)
        assert d_root >= 2
        root_delta = d_root - gamma * gamma
        root_load = gamma * (1 - lam) - lam * d_root
        if root_load <= 0:
            oracle.counts["output_words"] += 1
            return {seed: 1 - lam}, {"events": 0, "closure": False}
    else:
        assert d_seed >= 2
    centers = {}

    def expose(i):
        leaves, ports = [], []
        for j in oracle.row(i):
            if j == source_leaf:
                continue
            (leaves if oracle.degree(j) == 1 else ports).append(j)
        assert len(ports) == 2, "Outside the promised cycle-with-leaves class."
        center = Center(i, oracle.degree(i), leaves, ports)
        centers[i] = center
        return center

    root = expose(root_label)
    arms = [Arm(j) for j in root.ports]
    root_settled = not root.leaves
    packed_a = packed_b = F(0)
    current = F(0)
    block = None
    events = 0
    closure = False

    def tip_response(arm):
        if arm.tip is None:
            return F(1), F(0)
        return arm.tip.a / arm.tip.delta, arm.tip.b / arm.tip.delta

    def block_response():
        assert 1 <= len(block["tips"]) <= 3
        oracle.counts["tiny_sdd_calls"] += 2
        oracle.counts["tiny_sdd_cubic_units"] += 2 * len(block["tips"]) ** 3
        return solve(block["matrix"], block["a"]), solve(block["matrix"], block["b"])

    while True:
        oracle.counts["state_iterations"] += 1
        choices = []
        slope, offset = root_delta - packed_a, -root_load - packed_b
        if block is None:
            for index, arm in enumerate(arms):
                tip = arm.tip
                if tip:
                    slope -= tip.a * tip.a / tip.delta
                    offset -= tip.a * tip.b / tip.delta
                    if not tip.settled:
                        aa, bb = tip_response(arm)
                        choices.append(((lam / gamma - bb) / aa, "tip_leaves", index))
            if arms[0].candidate == arms[1].candidate:
                j = arms[0].candidate
                aa0, bb0 = tip_response(arms[0])
                aa1, bb1 = tip_response(arms[1])
                t = (lam * oracle.degree(j) - gamma * (bb0 + bb1)) / (gamma * (aa0 + aa1))
                choices.append((t, "close", j))
            else:
                for index, arm in enumerate(arms):
                    aa, bb = tip_response(arm)
                    t = (lam * oracle.degree(arm.candidate) / gamma - bb) / aa
                    choices.append((t, "advance", index))
        else:
            block_a, block_b = block_response()
            slope -= sum(a * x for a, x in zip(block["a"], block_a))
            offset -= sum(a * x for a, x in zip(block["a"], block_b))
            for index, tip in enumerate(block["tips"]):
                if not tip.settled:
                    assert block_a[index] > 0
                    choices.append(
                        ((lam / gamma - block_b[index]) / block_a[index], "block_leaves", index)
                    )
        if not root_settled:
            choices.append((lam / gamma, "root_leaves", root_label))
        oracle.counts["event_candidates_inspected"] += len(choices)
        assert len(choices) <= 5 and slope > 0
        terminal = -offset / slope
        assert terminal >= current
        event = min(choices) if choices else None
        if event is None or terminal <= event[0]:
            current = terminal
            break
        current, kind, label = event
        events += 1
        oracle.counts["events_" + kind] += 1
        if kind == "root_leaves":
            k = len(root.leaves)
            root_delta -= k * gamma * gamma
            root_load -= k * gamma * lam
            root_settled = True
        elif kind == "tip_leaves":
            tip = arms[label].tip
            k = len(tip.center.leaves)
            tip.delta -= k * gamma * gamma
            tip.b -= k * gamma * lam
            tip.settled = True
            assert tip.delta > 0
        elif kind == "advance":
            arm = arms[label]
            previous = arm.tip
            if previous:
                # A one-sided next-cycle gate needs u_tip >= 2 lambda/gamma,
                # so this tip's degree-one leaf group was already settled.
                assert previous.settled
                packed_a += previous.a * previous.a / previous.delta
                packed_b += previous.a * previous.b / previous.delta
                arm.committed.append(previous)
                oracle.counts["committed_record_writes"] += 1
            center = expose(arm.candidate)
            parent_label = previous.center.label if previous else root_label
            assert parent_label in center.ports
            next_label = next(j for j in center.ports if j != parent_label)
            assert next_label not in centers
            delta, a, b = F(center.degree), gamma, -lam * center.degree
            if previous:
                delta -= gamma * gamma / previous.delta
                a = gamma * previous.a / previous.delta
                b += gamma * previous.b / previous.delta
            assert delta > 0
            arm.tip = Tip(center, delta, a, b, not center.leaves)
            arm.candidate = next_label
        elif kind == "close":
            assert root_settled
            center = expose(label)
            tips = [arm.tip for arm in arms if arm.tip]
            endpoints = [arm.tip.center.label if arm.tip else root_label for arm in arms]
            assert set(center.ports) == set(endpoints)
            last = Tip(
                center,
                F(center.degree),
                gamma * sum(arm.tip is None for arm in arms),
                -lam * center.degree,
                not center.leaves,
            )
            tips.append(last)
            matrix = [[F(0)] * len(tips) for _ in tips]
            for j, tip in enumerate(tips):
                matrix[j][j] = tip.delta
                if j != len(tips) - 1:
                    matrix[j][-1] = matrix[-1][j] = -gamma
            block = {
                "tips": tips,
                "matrix": matrix,
                "a": [tip.a for tip in tips],
                "b": [tip.b for tip in tips],
            }
            closure = True
            oracle.counts["closing_block_dimension"] = len(tips)
        elif kind == "block_leaves":
            tip = block["tips"][label]
            k = len(tip.center.leaves)
            block["matrix"][label][label] -= k * gamma * gamma
            block["b"][label] -= k * gamma * lam
            tip.settled = True
        else:
            raise AssertionError(kind)

    values = {root_label: current}
    if source_leaf is not None:
        values[source_leaf] = 1 - lam + gamma * current
    if block:
        # Reuse the already computed coefficients from this last state.
        for tip, aa, bb in zip(block["tips"], block_a, block_b):
            values[tip.center.label] = aa * current + bb
    else:
        for arm in arms:
            if arm.tip:
                aa, bb = tip_response(arm)
                values[arm.tip.center.label] = aa * current + bb
    for arm in arms:
        next_value = values[arm.tip.center.label] if arm.tip else F(0)
        for tip in reversed(arm.committed):
            next_value = (tip.a * current + tip.b + gamma * next_value) / tip.delta
            values[tip.center.label] = next_value
            oracle.counts["reverse_record_reads"] += 1
    for i, center in centers.items():
        assert values[i] > 0
        leaf_value = max(F(0), gamma * values[i] - lam)
        for j in center.leaves:
            oracle.counts["terminal_leaf_records_read"] += 1
            if leaf_value > 0:
                values[j] = leaf_value
    oracle.counts["output_words"] += len(values)
    return values, {"events": events, "closure": closure}


def make_sun(leaves):
    graph = nx.cycle_graph(len(leaves))
    label = len(leaves)
    for i, k in enumerate(leaves):
        for _ in range(k):
            graph.add_edge(i, label)
            label += 1
    return graph


def check_solution(graph, seed, alpha, lam, answer):
    gamma = 1 - 2 * alpha / (1 + alpha)
    for i in graph:
        x = answer.get(i, F(0))
        gradient = (
            graph.degree(i) * x
            - gamma * sum(answer.get(j, F(0)) for j in graph[i])
            - F(int(i == seed))
            + lam * graph.degree(i)
        )
        assert x >= 0 and gradient >= 0 and x * gradient == 0


def audit_attachment_witness():
    """Audit-only refutation of automatically settling longer attachments."""
    graph = nx.cycle_graph(12)
    graph.add_edges_from([(1, 12), (12, 13), (2, 14)])
    gamma, lam = F(3, 4), F(1, 1000)
    ids = list(range(1, 15))
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in ids]
        for i in ids
    ]
    states = []
    for t in [F(39, 2000), F(1, 20)]:
        load = [-lam * graph.degree(i) + (gamma * t if graph.has_edge(i, 0) else F(0)) for i in ids]
        values = dict(zip(ids, obstacle(matrix, load)))
        values[0] = t
        root_derivative = (
            graph.degree(0) * t
            - gamma * sum(values[j] for j in graph[0])
            - 1
            + lam * graph.degree(0)
        )
        assert root_derivative < 0
        if not states:
            assert values[1] == 4 * lam and values[2] == 0
            assert values[12] == lam / 2 and values[13] == 0
            assert gamma * (values[1] + values[3]) == lam * graph.degree(2)
        else:
            assert values[2] > 0 and values[13] > 0
        states.append(
            {
                "root_potential": str(t),
                "root_derivative": str(root_derivative),
                "values": {str(i): str(values[i]) for i in graph},
            }
        )
    return {
        "claim_refuted": "Every nontrivial pendant tree has a fixed response when its center's next one-sided cycle neighbor activates.",
        "graph_edges": list(graph.edges()),
        "seed": 0,
        "alpha_lazy": "1/7",
        "lambda_degree_load": str(lam),
        "states": states,
        "scope": "Audit-only dense conditional solves on a graph outside the promised leaf-attachment class; this is a representation obstruction, not a lower bound.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-cycle", type=int, default=3)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.time()
    cases, totals, closed, postclosure = 0, Counter(), 0, 0
    alphas, lambdas = [F(2, 3), F(1, 7), F(1, 1009)], [F(1, 5), F(1, 31), F(1, 1009)]
    for cycle in range(3, args.max_cycle + 1):
        for leaves in itertools.product(range(3), repeat=cycle):
            graph = make_sun(leaves)
            seeds = [0, cycle] if leaves[0] else [0]
            for seed, alpha, lam in itertools.product(seeds, alphas, lambdas):
                oracle = Oracle(graph)
                try:
                    answer, info = local_sun(oracle, seed, alpha, lam)
                    check_solution(graph, seed, alpha, lam, answer)
                    assert all(answer.get(i, 0) > 0 for i in oracle.rows)
                    assert sum(graph.degree(i) for i in answer) <= 1 / lam
                    gamma = 1 - 2 * alpha / (1 + alpha)
                    matrix = [
                        [
                            F(graph.degree(i))
                            if i == j
                            else -gamma
                            if graph.has_edge(i, j)
                            else F(0)
                            for j in graph
                        ]
                        for i in graph
                    ]
                    exact = obstacle(
                        matrix, [F(int(i == seed)) - lam * graph.degree(i) for i in graph]
                    )
                    assert [answer.get(i, F(0)) for i in graph] == exact
                except Exception:
                    print(
                        json.dumps(
                            {
                                "failed_leaves": leaves,
                                "seed": seed,
                                "alpha": str(alpha),
                                "lambda": str(lam),
                                "counts": dict(oracle.counts),
                            }
                        ),
                        flush=True,
                    )
                    raise
                totals.update(oracle.counts)
                cases += 1
                closed += info["closure"]
                postclosure += oracle.counts["events_block_leaves"] > 0
    rows = []
    if args.structured:
        for n in [32, 128, 512, 2048]:
            leaves = [(i * i + 3 * i + 1) % 5 for i in range(n)]
            graph = make_sun(leaves)
            variants = [("local", F(1, 1009), F(1, 1009))]
            if n <= 128:
                variants.append(("full", F(1, n**3 + 1), F(1, 32 * n)))
            for regime, alpha, lam in variants:
                before = time.time()
                oracle = Oracle(graph)
                answer, info = local_sun(oracle, 0, alpha, lam)
                check_solution(graph, 0, alpha, lam, answer)
                rows.append(
                    {
                        "cycle_vertices": n,
                        "ambient_vertices": len(graph),
                        "regime": regime,
                        "alpha": str(alpha),
                        "lambda": str(lam),
                        "support_vertices": len(answer),
                        "support_volume": sum(graph.degree(i) for i in answer),
                        "counts": dict(oracle.counts),
                        "closure": info["closure"],
                        "elapsed_seconds": round(time.time() - before, 3),
                    }
                )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.local_sun_solver",
        "arithmetic": "exact fractions; all algorithmic systems have dimension at most three",
        "cases": cases,
        "max_cycle": args.max_cycle,
        "leaf_counts": [0, 1, 2],
        "seed": "cycle label zero and one leaf at zero when present; all ordered leaf-count patterns are enumerated",
        "alpha_lazy": list(map(str, alphas)),
        "lambda_degree_load": list(map(str, lambdas)),
        "random_seed": None,
        "closed_cases": closed,
        "postclosure_leaf_cases": postclosure,
        "solver_counts": dict(totals),
        "structured_rows": rows,
        "attachment_settling_counterexample": audit_attachment_witness(),
        "git_commit": subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
        ).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(
                ["git", "-C", str(repo), "status", "--porcelain"], text=True
            ).strip()
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.time() - started, 3),
        "limitation": "Promised cycle-with-pendant-leaves graph, arbitrary seed. Full-graph KKT checks and dense obstacle references are audit-only; coefficient bit complexity and arbitrary cyclic graphs are not claimed.",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
