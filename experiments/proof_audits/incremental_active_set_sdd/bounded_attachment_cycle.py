"""Local exact cycle solver with bounded attached trees and no size advice.

Only degree/row access is used. Bounded probes may inspect inactive vertices;
their work is charged explicitly. Settled prefixes are eliminated eagerly;
2*q*q bounds each retained arm for actual attachment size q. This is a
scoped exact-real research audit, with a seed promised to lie on the cycle.
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
from local_sun_solver import check_solution, make_sun
import networkx as nx
from persistent_affine_tree import Arena, solve_tree


class LocalOracle:
    def __init__(self, graph):
        self._graph = graph
        self.degrees, self.rows = {}, {}
        self.counts = Counter()

    def degree(self, i):
        self.counts["degree_cache_lookups"] += 1
        if i not in self.degrees:
            self.degrees[i] = self._graph.degree(i)
            self.counts["degree_replies"] += 1
        return self.degrees[i]

    def row(self, i):
        self.counts["row_accesses"] += 1
        if i not in self.rows:
            self.rows[i] = tuple(self._graph[i])
            self.counts["row_exposures"] += 1
            self.counts["new_adjacency_entries"] += len(self.rows[i])
        self.counts["adjacency_entries_read"] += len(self.rows[i])
        return self.rows[i]


@dataclass
class Module:
    curves: dict
    parent: dict
    nodes: list


@dataclass
class Center:
    label: int
    degree: int
    ports: list
    modules: list
    knots: list
    cursor: int = 0


@dataclass
class Site:
    center: Center
    delta: F
    a: F
    b: F


@dataclass
class Arm:
    candidate: int
    window: list = field(default_factory=list)
    committed: list = field(default_factory=list)


def classify_and_build(oracle, center, q, alpha, lam):
    """Bounded classification never scans a probe row with degree > q."""
    neighbors = oracle.row(center)
    neighbor_set = set(neighbors)
    ports, modules, knots = set(), [], []
    for start in neighbors:
        if start in ports:
            continue
        seen, queue = {start}, [start]
        large = False
        for i in queue:
            oracle.counts["classification_vertices"] += 1
            if oracle.degree(i) > q:
                large = True
                break
            for j in oracle.row(i):
                if j == center:
                    continue
                if j in neighbor_set and j != start:
                    ports.add(j)
                    large = True
                    break
                if j not in seen:
                    seen.add(j)
                    if len(seen) > q:
                        large = True
                        break
                    queue.append(j)
            if large:
                break
        if large:
            ports.add(start)
            continue
        graph = nx.Graph()
        graph.add_edge(center, start)
        for i in seen:
            for j in oracle.row(i):
                assert j == center or j in seen
                graph.add_edge(i, j)
                oracle.counts["module_graph_record_writes"] += 1
        degrees = {i: oracle.degree(i) for i in graph}
        _, curves, _, parent, counts = solve_tree(graph, center, alpha, lam, degrees)
        for name, number in counts.items():
            oracle.counts["module_" + name] += number
        curve = curves[start]
        observer = Arena()
        points = list(observer.points(curve.root))
        for name, number in observer.counts.items():
            oracle.counts["module_knot_" + name] += number
        previous = F(1)
        for index, (x, y) in enumerate(points):
            slope = (
                (points[index + 1][1] - y) / (points[index + 1][0] - x)
                if index + 1 < len(points)
                else curve.right_slope
            )
            increment = slope - previous
            assert increment >= 0
            if increment:
                knots.append((x, increment))
                oracle.counts["module_knot_records"] += 1
            previous = slope
        modules.append(Module(curves, parent, [i for i in parent if i != center]))
        assert len(seen) <= q and len(points) <= q
    assert len(ports) >= 2, "The seed/center is not on a promised cycle."
    if len(ports) > 2:
        return None
    # The sort is not a free heap: the conservative comparison units are kept.
    oracle.counts["knot_sort_comparison_bound"] += len(knots) * max(1, len(knots).bit_length())
    knots.sort()
    oracle.counts["center_records"] += 1
    return Center(center, oracle.degree(center), sorted(ports), modules, knots)


def discover_center(oracle, label, alpha, lam):
    limit = 1
    while True:
        oracle.counts["classification_attempts"] += 1
        center = classify_and_build(oracle, label, limit, alpha, lam)
        if center is not None:
            return center
        limit *= 2


def tridiagonal_responses(sites, gamma, counts):
    """Two affine right-hand sides; fresh linear work only inside the window."""
    n = len(sites)
    counts["window_factor_rows"] += n
    counts["window_rhs_words"] += 2 * n
    if not n:
        return []
    delta, aa, bb = [], [], []
    for i, site in enumerate(sites):
        pivot, a, b = site.delta, site.a, site.b
        if i:
            pivot -= gamma * gamma / delta[-1]
            a += gamma * aa[-1] / delta[-1]
            b += gamma * bb[-1] / delta[-1]
        assert pivot > 0
        delta.append(pivot)
        aa.append(a)
        bb.append(b)
    out = [None] * n
    a_next = b_next = F(0)
    for i in reversed(range(n)):
        a_next = (aa[i] + gamma * a_next) / delta[i]
        b_next = (bb[i] + gamma * b_next) / delta[i]
        out[i] = a_next, b_next
    counts["window_reverse_rows"] += n
    return out


def local_bounded_cycle(oracle, seed, alpha, lam):
    gamma = 1 - 2 * alpha / (1 + alpha)
    assert 0 < gamma < 1 and lam > 0
    degree = oracle.degree(seed)
    if lam * degree >= 1:
        return {}, {"events": 0, "closure": False, "maximum_window": 0}
    root_center = discover_center(oracle, seed, alpha, lam)
    root = Site(root_center, F(degree), F(0), 1 - lam * degree)
    centers, sites_by_label = {seed: root_center}, {seed: root}
    arms = [Arm(j) for j in root_center.ports]
    q_seen = max([len(module.nodes) for module in root_center.modules] + [1])
    packed_a = packed_b = current = F(0)
    block = None
    maximum_window = events = 0

    def expose(label, a=F(0)):
        nonlocal q_seen
        assert label not in centers
        center = discover_center(oracle, label, alpha, lam)
        q_seen = max([len(module.nodes) for module in center.modules] + [q_seen])
        centers[label] = center
        site = Site(center, F(center.degree), a, -lam * center.degree)
        sites_by_label[label] = site
        return site

    def settle_prefixes():
        nonlocal packed_a, packed_b
        for arm in arms:
            while len(arm.window) > 1:
                old = arm.window[0]
                if old.center.cursor != len(old.center.knots):
                    break
                arm.window.pop(0)
                successor = arm.window[0]
                packed_a += old.a * old.a / old.delta
                packed_b += old.a * old.b / old.delta
                successor.delta -= gamma * gamma / old.delta
                successor.a += gamma * old.a / old.delta
                successor.b += gamma * old.b / old.delta
                arm.committed.append(old)
                oracle.counts["committed_records"] += 1
                oracle.counts["window_shift_words"] += len(arm.window)

    while True:
        oracle.counts["states"] += 1
        chains = [block] if block is not None else [arm.window for arm in arms]
        responses, choices = {seed: (F(1), F(0))}, []
        slope, offset = root.delta - packed_a, -root.b - packed_b
        window_size = sum(len(chain) for chain in chains)
        maximum_window = max(maximum_window, window_size)
        assert window_size <= 4 * q_seen * q_seen + 1
        for chain in chains:
            values = tridiagonal_responses(chain, gamma, oracle.counts)
            for site, (aa, bb) in zip(chain, values):
                responses[site.center.label] = aa, bb
                slope -= site.a * aa
                offset -= site.a * bb
                oracle.counts["window_event_sites_read"] += 1
                center = site.center
                if center.cursor < len(center.knots):
                    assert aa > 0
                    threshold = center.knots[center.cursor][0]
                    choices.append(((threshold - bb) / aa, "module", center.label))
        if root_center.cursor < len(root_center.knots):
            choices.append((root_center.knots[root_center.cursor][0], "module", seed))
        if block is None:
            tip_values = [
                responses[arm.window[-1].center.label] if arm.window else (F(1), F(0))
                for arm in arms
            ]
            if arms[0].candidate == arms[1].candidate:
                label = arms[0].candidate
                aa = sum(value[0] for value in tip_values)
                bb = sum(value[1] for value in tip_values)
                event = (lam * oracle.degree(label) / gamma - bb) / aa
                choices.append((event, "close", label))
            else:
                for index, (arm, (aa, bb)) in enumerate(zip(arms, tip_values)):
                    event = (lam * oracle.degree(arm.candidate) / gamma - bb) / aa
                    choices.append((event, "advance", index))
        oracle.counts["event_candidates_inspected"] += len(choices)
        assert slope > 0 and all(item[0] >= current for item in choices)
        terminal = -offset / slope
        assert terminal >= current
        first = min(choices) if choices else None
        if first is None or terminal <= first[0]:
            current = terminal
            break
        current, kind, label = first
        events += 1
        oracle.counts["events_" + kind] += 1
        if kind == "module":
            site = sites_by_label[label]
            center = site.center
            threshold = center.knots[center.cursor][0]
            while center.cursor < len(center.knots) and center.knots[center.cursor][0] == threshold:
                _, increment = center.knots[center.cursor]
                site.delta -= increment
                site.b -= increment * threshold
                center.cursor += 1
                oracle.counts["module_knots_consumed"] += 1
            assert site.delta > 0
        elif kind == "advance":
            arm = arms[label]
            parent = arm.window[-1].center.label if arm.window else seed
            site = expose(arm.candidate, gamma if not arm.window else F(0))
            assert parent in site.center.ports
            arm.candidate = next(j for j in site.center.ports if j != parent)
            assert arm.candidate not in centers
            arm.window.append(site)
        elif kind == "close":
            endpoints = [arm.window[-1].center.label if arm.window else seed for arm in arms]
            site = expose(label, gamma * sum(not arm.window for arm in arms))
            assert set(site.center.ports) == set(endpoints)
            block = [*arms[0].window, site, *reversed(arms[1].window)]
            oracle.counts["closing_path_words"] += len(block)
        else:
            raise AssertionError(kind)
        if block is None:
            settle_prefixes()
            for arm in arms:
                assert len(arm.window) <= 2 * q_seen * q_seen, "Settlement-width bound failed."

    values = {i: aa * current + bb for i, (aa, bb) in responses.items()}
    for arm in arms:
        following = values[arm.window[0].center.label] if arm.window else F(0)
        for site in reversed(arm.committed):
            following = (site.a * current + site.b + gamma * following) / site.delta
            values[site.center.label] = following
            oracle.counts["committed_reverse_reads"] += 1
    for i, center in centers.items():
        assert values[i] > 0
        for module in center.modules:
            observer = Arena()
            for j in module.nodes:
                parent_value = values.get(module.parent[j], F(0))
                curve = module.curves[j].with_arena(observer)
                value = (curve.value(parent_value) - parent_value) / gamma
                assert value >= 0
                if value:
                    values[j] = value
            for name, number in observer.counts.items():
                oracle.counts["terminal_module_" + name] += number
            oracle.counts["terminal_module_records_read"] += len(module.nodes)
    oracle.counts["output_words"] += len(values)
    return values, {
        "events": events,
        "closure": block is not None,
        "maximum_window": maximum_window,
        "maximum_attachment_seen": q_seen,
    }


def make_hairy_cycle(lengths):
    graph = nx.cycle_graph(len(lengths))
    label = len(lengths)
    for i, length in enumerate(lengths):
        parent = i
        for _ in range(length):
            graph.add_edge(parent, label)
            parent, label = label, label + 1
    return graph


def make_branching_cycle(pattern):
    graph = nx.cycle_graph(len(pattern))
    label = len(pattern)
    for i, kind in enumerate(pattern):
        if kind == 4:
            graph.add_edges_from([(i, label), (label, label + 1), (label, label + 2)])
            label += 3
        else:
            parent = i
            for _ in range(kind):
                graph.add_edge(parent, label)
                parent, label = label, label + 1
    return graph


def audit_saturation_bound():
    checks = 0
    for q in range(1, 7):
        trees = [nx.empty_graph(1)] if q == 1 else list(nx.nonisomorphic_trees(q))
        for tree in trees:
            for attach, gamma in itertools.product(tree, [F(1, 10), F(3, 4), F(1008, 1009)]):
                degrees = {i: tree.degree(i) + int(i == attach) for i in tree}
                matrix = [
                    [
                        F(degrees[i]) if i == j else -gamma if tree.has_edge(i, j) else F(0)
                        for j in tree
                    ]
                    for i in tree
                ]
                discounts = solve(matrix, [gamma * int(i == attach) for i in tree])
                assert min(discounts) > gamma ** (2 * q * q)
                checks += 1
    return checks


def exact_reference(graph, seed, alpha, lam):
    gamma = 1 - 2 * alpha / (1 + alpha)
    labels = list(graph)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in labels]
        for i in labels
    ]
    optimum = obstacle(matrix, [F(int(i == seed)) - lam * graph.degree(i) for i in labels])
    return dict(zip(labels, optimum))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-cycle", type=int, default=3)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--branching", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.time()
    cases, totals, rows = 0, Counter(), []
    alphas = [F(1, 7), F(1, 1009)]
    lambdas = [F(1, 5), F(1, 1009)]

    def check(graph, q, alpha, lam, dense=True):
        nonlocal cases
        oracle = LocalOracle(graph)
        answer, info = local_bounded_cycle(oracle, 0, alpha, lam)
        assert info.get("maximum_attachment_seen", 0) <= q
        check_solution(graph, 0, alpha, lam, answer)
        assert sum(graph.degree(i) for i in answer) <= 1 / lam
        if dense:
            expected = exact_reference(graph, 0, alpha, lam)
            assert {i: x for i, x in expected.items() if x} == answer
        cases += 1
        totals.update(oracle.counts)
        return answer, info, oracle

    for cycle in range(3, args.max_cycle + 1):
        for lengths in itertools.product(range(3), repeat=cycle):
            graph = make_hairy_cycle(lengths)
            for alpha, lam in itertools.product(alphas, lambdas):
                try:
                    check(graph, 2, alpha, lam)
                except Exception:
                    print(
                        json.dumps(
                            {"failed_lengths": lengths, "alpha": str(alpha), "lambda": str(lam)}
                        ),
                        flush=True,
                    )
                    raise
    # Previous late-attachment witness, plus unequal leaf groups as q=1.
    witness = nx.cycle_graph(12)
    witness.add_edges_from([(1, 12), (12, 13), (2, 14)])
    check(witness, 2, F(1, 7), F(1, 1000))
    check(make_sun((2, 0, 5, 1, 3)), 1, F(1, 1009), F(1, 1009))
    if args.branching:
        for pattern in itertools.product(range(5), repeat=3):
            for alpha, lam in itertools.product(alphas, lambdas):
                check(make_branching_cycle(pattern), 3, alpha, lam)
        extreme_graph = make_branching_cycle([4, 3, 0, 2, 1, 4, 3, 2])
        for alpha in [F(2, 3), F(15, 16), F(1, 1000003)]:
            check(extreme_graph, 3, alpha, F(1, 1000003))
    if args.structured:
        for n in [24, 64, 256]:
            for q in [2, 3]:
                graph = make_hairy_cycle([(i * i + 3 * i + 1) % (q + 1) for i in range(n)])
                alpha, lam = F(1, 1009), F(1, 1009)
                before = time.time()
                answer, info, oracle = check(graph, q, alpha, lam, dense=False)
                rows.append(
                    {
                        "cycle_vertices": n,
                        "ambient_vertices": len(graph),
                        "q": q,
                        "alpha": str(alpha),
                        "lambda": str(lam),
                        "support_vertices": len(answer),
                        "support_volume": sum(graph.degree(i) for i in answer),
                        "counts": dict(oracle.counts),
                        "info": info,
                        "elapsed_seconds_including_kkt": round(time.time() - before, 3),
                    }
                )
        for n in [32, 128]:
            graph = make_branching_cycle([(i * i + 3 * i + 1) % 5 for i in range(n)])
            alpha, lam = F(1, n**3 + 1), F(1, 64 * n)
            before = time.time()
            answer, info, oracle = check(graph, 3, alpha, lam, dense=False)
            rows.append(
                {
                    "family": "unequal_branching_trees",
                    "regime": "full_cycle",
                    "cycle_vertices": n,
                    "ambient_vertices": len(graph),
                    "q": 3,
                    "alpha": str(alpha),
                    "lambda": str(lam),
                    "support_vertices": len(answer),
                    "support_volume": sum(graph.degree(i) for i in answer),
                    "counts": dict(oracle.counts),
                    "info": info,
                    "elapsed_seconds_including_kkt": round(time.time() - before, 3),
                }
            )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.bounded_attachment_cycle",
        "arithmetic": "exact fractions; retained cycle solves are tridiagonal",
        "cases": cases,
        "dense_reference_comparisons": cases - len(rows),
        "large_kkt_only_cases": len(rows),
        "max_cycle": args.max_cycle,
        "small_attachment_lengths": [0, 1, 2],
        "branching_patterns_checked": args.branching,
        "extra_branching_alpha_lazy": ["2/3", "15/16", "1/1000003"] if args.branching else [],
        "extra_branching_lambda": "1/1000003" if args.branching else None,
        "saturation_checks": audit_saturation_bound(),
        "alpha_lazy": list(map(str, alphas)),
        "lambda_degree_load": list(map(str, lambdas)),
        "seed": "cycle vertex zero",
        "random_seed": None,
        "solver_counts": dict(totals),
        "structured_rows": rows,
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
        "limitation": "Promised cycle with attached trees, cycle seed; q is discovered and only appears in the work analysis. Full KKT/reference passes are audit-only. General OP3 and coefficient-bit bounds are not claimed.",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
