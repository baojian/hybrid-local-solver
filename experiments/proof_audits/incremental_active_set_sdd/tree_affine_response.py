"""Exact algebra audit for an ACT-based supplied-tree obstacle solver candidate.

Curves here are explicit lists. This audits the affine recurrence and a logical
operation ledger, NOT an implemented affine composition tree or local discovery.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from geometric_value_events import obstacle
import networkx as nx


@dataclass
class Curve:
    points: list[tuple[F, F]]
    left: F
    right: F
    intercept: F = F(0)

    def value(self, x):
        if not self.points:
            return self.left * x + self.intercept
        k = bisect_right([p[0] for p in self.points], x)
        if k == 0:
            a, b = self.points[0]
            return b + self.left * (x - a)
        if k == len(self.points):
            a, b = self.points[-1]
            return b + self.right * (x - a)
        a, b = self.points[k - 1]
        c, d = self.points[k]
        return b + (d - b) * (x - a) / (c - a)

    def inverse(self, y):
        assert self.left > 0 and self.right > 0
        if not self.points:
            return (y - self.intercept) / self.left
        k = bisect_right([p[1] for p in self.points], y)
        if k == 0:
            a, b = self.points[0]
            return a + (y - b) / self.left
        if k == len(self.points):
            a, b = self.points[-1]
            return a + (y - b) / self.right
        a, b = self.points[k - 1]
        c, d = self.points[k]
        return a + (c - a) * (y - b) / (d - b)

    def affine(self, a, b, c, d, tx, ty, counts):
        """Dense reference for the single O(1) logical ACT affine operation."""
        counts["logical_affine_maps"] += 1
        counts["dense_affine_points_visited"] += len(self.points) + 1
        assert a * d - b * c != 0
        assert a + b * self.left > 0 and a + b * self.right > 0
        left = (c + d * self.left) / (a + b * self.left)
        right = (c + d * self.right) / (a + b * self.right)
        points = [(a * x + b * y + tx, c * x + d * y + ty) for x, y in self.points]
        assert all(x < xx and y < yy for (x, y), (xx, yy) in zip(points, points[1:]))
        x0, y0 = b * self.intercept + tx, d * self.intercept + ty
        return Curve(points, left, right, y0 - left * x0)


def add_curves(big, small, counts):
    # ACT addition charges the smaller-child breakpoints and logarithmic searches.
    counts["logical_small_merge_points"] += len(small.points) + 1
    xs = sorted({x for x, _ in big.points} | {x for x, _ in small.points})
    counts["dense_sum_points_materialized"] += len(xs)
    points = [(x, big.value(x) + small.value(x)) for x in xs]
    return Curve(
        points, big.left + small.left, big.right + small.right, big.intercept + small.intercept
    )


def supplied_tree(graph, seed, alpha, lam, degrees=None):
    """Full supplied-tree reference; original degree data may include grounding."""
    deg = dict(graph.degree()) if degrees is None else degrees
    gamma = 1 - 2 * alpha / (1 + alpha)
    assert gamma > 0
    parent = {seed: None}
    order = [seed]
    for i in order:
        for j in graph[i]:
            if j != parent[i]:
                assert j not in parent
                parent[j] = i
                order.append(j)
    curves, sizes = {}, {}
    counts = Counter(
        cases=1, supplied_vertices=len(graph), supplied_incidence_reads=2 * graph.number_of_edges()
    )
    root_h = None
    for i in reversed(order):
        children = [j for j in graph[i] if j != parent[i]]
        sizes[i] = 1 + sum(sizes[j] for j in children)
        children.sort(key=lambda j: sizes[j], reverse=True)
        total = curves[children[0]] if children else Curve([], F(0), F(0))
        for j in children[1:]:
            total = add_curves(total, curves[j], counts)
        load = F(int(i == seed)) - lam * deg[i]
        # H_i(x) = d_i x - load_i - sum_child mu_child(x).
        # We store nu_child(x)=x+mu_child(x), hence this is one affine map.
        h = total.affine(F(1), F(0), F(deg[i] + len(children)), F(-1), F(0), -load, counts)
        assert h.left > 0 and h.right > 0
        assert h.value(F(0)) == -load
        if i == seed:
            root_h = h
            continue
        nu = h.affine(F(0), 1 / gamma, gamma, 1 / gamma, F(0), F(0), counts)
        threshold = -load / gamma
        assert threshold > 0 and all(x > threshold for x, _ in nu.points)
        # Add the zero-response branch; nu(t)=t on the whole left ray.
        nu.points.insert(0, (threshold, threshold))
        nu.left = F(1)
        slopes = [nu.left]
        slopes.extend((yy - y) / (xx - x) for (x, y), (xx, yy) in zip(nu.points, nu.points[1:]))
        slopes.append(nu.right)
        assert all(a <= b for a, b in zip(slopes, slopes[1:]))
        assert nu.value(F(0)) == 0
        counts["logical_zero_branch_insertions"] += 1
        curves[i] = nu
    answer = {seed: max(F(0), root_h.inverse(F(0)))}
    for i in order[1:]:
        t = answer[parent[i]]
        answer[i] = (curves[i].value(t) - t) / gamma
        assert answer[i] >= 0
    counts["terminal_curve_queries"] += len(graph)
    counts["stored_reference_breakpoints"] = sum(len(c.points) for c in curves.values())
    return answer, counts


def check_case(graph, seed, alpha, lam, grounding):
    deg = {i: graph.degree(i) + (i % 3 if grounding else 0) for i in graph}
    gamma = 1 - 2 * alpha / (1 + alpha)
    answer, counts = supplied_tree(graph, seed, alpha, lam, deg)
    labels = list(graph)
    matrix = [
        [F(deg[i]) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in labels]
        for i in labels
    ]
    load = [F(int(i == seed)) - lam * deg[i] for i in labels]
    exact = obstacle(matrix, load)
    assert [answer[i] for i in labels] == exact
    counts["reference_support"] += sum(x > 0 for x in exact)
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.time()
    totals = Counter()
    trees = [g for n in range(2, args.max_n + 1) for g in nx.nonisomorphic_trees(n)]
    alphas, lambdas = [F(2, 3), F(1, 7), F(1, 101)], [F(1, 5), F(1, 31), F(1, 1009)]
    for graph in trees:
        for seed, alpha, lam, grounding in itertools.product(graph, alphas, lambdas, [False, True]):
            totals.update(check_case(graph, seed, alpha, lam, grounding))
    rows = []
    if args.structured:
        for n in [16, 32, 64, 128]:
            for name, graph in [("path", nx.path_graph(n)), ("star", nx.star_graph(n - 1))]:
                answer, counts = supplied_tree(graph, 0, F(1, 1009), F(1, 1009))
                rows.append(
                    {
                        "family": name,
                        "n": n,
                        "counts": dict(counts),
                        "support": sum(x > 0 for x in answer.values()),
                    }
                )
    # Componentwise inversion is NOT inversion of a sum of response curves.
    f, g = Curve([], F(1), F(1)), Curve([], F(2), F(2))
    total = add_curves(f, g, Counter())
    assert total.inverse(F(1)) == F(1, 3)
    assert f.inverse(F(1)) + g.inverse(F(1)) == F(3, 2)
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.tree_affine_response",
        "arithmetic": "exact fractions",
        "trees": len(trees),
        "max_n": args.max_n,
        "alpha_lazy": list(map(str, alphas)),
        "lambda_degree_load": list(map(str, lambdas)),
        "grounding_cases": ["original tree degrees", "degree plus label modulo three"],
        "random_seed": None,
        "counts": dict(totals),
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
        "limitation": "Full supplied tree and explicit curve lists. Logical ACT operations are not an ACT implementation or a local discovery algorithm.",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
