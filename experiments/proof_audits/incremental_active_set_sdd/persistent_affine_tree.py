"""Persistent AVL affine response curves for the supplied-tree OP3 probe.

Every node is immutable. A whole-curve map copies one root; updates copy only
search paths. This is an implemented supplied-tree solver, not local discovery.
The main routine is an exact falsification audit, not a production benchmark.
"""

from __future__ import annotations

import argparse
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
from tree_affine_response import supplied_tree as explicit_tree


IDENTITY = (F(1), F(0), F(0), F(1), F(0), F(0))


@dataclass(frozen=True, slots=True)
class Node:
    x: F
    y: F
    left: Node | None
    right: Node | None
    height: int
    size: int
    pending: tuple


def height(node):
    return node.height if node else 0


def size(node):
    return node.size if node else 0


class Arena:
    def __init__(self):
        self.counts = Counter()

    def point(self, transform, x, y):
        self.counts["affine_point_evaluations"] += 1
        a, b, c, d, tx, ty = transform
        return a * x + b * y + tx, c * x + d * y + ty

    def compose(self, outer, inner):
        self.counts["affine_compositions"] += 1
        a, b, c, d, tx, ty = outer
        e, f, g, h, ux, uy = inner
        return (
            a * e + b * g,
            a * f + b * h,
            c * e + d * g,
            c * f + d * h,
            a * ux + b * uy + tx,
            c * ux + d * uy + ty,
        )

    def node(self, x, y, left=None, right=None, pending=IDENTITY):
        self.counts["node_allocations"] += 1
        return Node(
            x,
            y,
            left,
            right,
            1 + max(height(left), height(right)),
            1 + size(left) + size(right),
            pending,
        )

    def apply(self, node, transform):
        if node is None:
            return None
        self.counts["tagged_subtree_roots"] += 1
        x, y = self.point(transform, node.x, node.y)
        return self.node(x, y, node.left, node.right, self.compose(transform, node.pending))

    def push(self, node):
        if node.pending == IDENTITY:
            return node
        self.counts["lazy_tag_pushes"] += 1
        return self.node(
            node.x,
            node.y,
            self.apply(node.left, node.pending),
            self.apply(node.right, node.pending),
        )

    def rotate_right(self, node):
        self.counts["rotations"] += 1
        node = self.push(node)
        child = self.push(node.left)
        right = self.node(node.x, node.y, child.right, node.right)
        return self.node(child.x, child.y, child.left, right)

    def rotate_left(self, node):
        self.counts["rotations"] += 1
        node = self.push(node)
        child = self.push(node.right)
        left = self.node(node.x, node.y, node.left, child.left)
        return self.node(child.x, child.y, left, child.right)

    def balance(self, node):
        if height(node.left) > height(node.right) + 1:
            if height(node.left.left) < height(node.left.right):
                node = self.node(node.x, node.y, self.rotate_left(node.left), node.right)
            return self.rotate_right(node)
        if height(node.right) > height(node.left) + 1:
            if height(node.right.right) < height(node.right.left):
                node = self.node(node.x, node.y, node.left, self.rotate_right(node.right))
            return self.rotate_left(node)
        return node

    def insert(self, node, x, y):
        if node is None:
            self.counts["new_breakpoints"] += 1
            return self.node(x, y)
        self.counts["insert_path_visits"] += 1
        node = self.push(node)
        if x == node.x:
            assert y == node.y
            self.counts["existing_breakpoint_hits"] += 1
            return node
        if x < node.x:
            return self.balance(self.node(node.x, node.y, self.insert(node.left, x, y), node.right))
        return self.balance(self.node(node.x, node.y, node.left, self.insert(node.right, x, y)))

    def suffix_hinge(self, node, threshold, coefficient):
        if node is None:
            return None
        self.counts["suffix_path_visits"] += 1
        node = self.push(node)
        if node.x < threshold:
            return self.node(
                node.x, node.y, node.left, self.suffix_hinge(node.right, threshold, coefficient)
            )
        shear = (F(1), F(0), coefficient, F(1), F(0), -coefficient * threshold)
        return self.node(
            node.x,
            node.y + coefficient * (node.x - threshold),
            self.suffix_hinge(node.left, threshold, coefficient),
            self.apply(node.right, shear),
        )

    def bracket(self, node, value, axis):
        lower = upper = None
        carry = IDENTITY
        while node:
            self.counts["query_path_visits"] += 1
            point = self.point(carry, node.x, node.y)
            if point[axis] == value:
                return point, point
            carry = self.compose(carry, node.pending)
            if point[axis] < value:
                lower, node = point, node.right
            else:
                upper, node = point, node.left
        return lower, upper

    def points(self, root):
        # Streaming traversal visits each smaller-curve node once. It does not
        # materialize or modify any larger curve or retained old version.
        stack = []
        node, carry = root, IDENTITY
        while node or stack:
            while node:
                self.counts["iterator_node_visits"] += 1
                point = self.point(carry, node.x, node.y)
                child_carry = self.compose(carry, node.pending)
                stack.append((node, point, child_carry))
                node, carry = node.left, child_carry
            node, point, carry = stack.pop()
            yield point
            node = node.right


@dataclass(frozen=True)
class Curve:
    arena: Arena
    root: Node | None
    left_slope: F
    right_slope: F
    empty_intercept: F = F(0)

    def with_arena(self, arena):
        """Bind an audit observer without charging audit reads to solver work."""
        return Curve(arena, self.root, self.left_slope, self.right_slope, self.empty_intercept)

    def value(self, x):
        self.arena.counts["value_queries"] += 1
        if self.root is None:
            return self.left_slope * x + self.empty_intercept
        lo, hi = self.arena.bracket(self.root, x, 0)
        if lo is None:
            return hi[1] + self.left_slope * (x - hi[0])
        if hi is None:
            return lo[1] + self.right_slope * (x - lo[0])
        if lo == hi:
            return lo[1]
        return lo[1] + (hi[1] - lo[1]) * (x - lo[0]) / (hi[0] - lo[0])

    def inverse(self, y):
        self.arena.counts["inverse_queries"] += 1
        assert self.left_slope > 0 and self.right_slope > 0
        if self.root is None:
            return (y - self.empty_intercept) / self.left_slope
        lo, hi = self.arena.bracket(self.root, y, 1)
        if lo is None:
            return hi[0] + (y - hi[1]) / self.left_slope
        if hi is None:
            return lo[0] + (y - lo[1]) / self.right_slope
        if lo == hi:
            return lo[0]
        return lo[0] + (hi[0] - lo[0]) * (y - lo[1]) / (hi[1] - lo[1])

    def affine(self, transform):
        self.arena.counts["whole_curve_maps"] += 1
        a, b, c, d, tx, ty = transform
        assert a * d - b * c != 0
        assert a + b * self.left_slope > 0 and a + b * self.right_slope > 0
        left = (c + d * self.left_slope) / (a + b * self.left_slope)
        right = (c + d * self.right_slope) / (a + b * self.right_slope)
        x0, y0 = b * self.empty_intercept + tx, d * self.empty_intercept + ty
        return Curve(
            self.arena, self.arena.apply(self.root, transform), left, right, y0 - left * x0
        )

    def insert(self, x, y):
        return Curve(
            self.arena,
            self.arena.insert(self.root, x, y),
            self.left_slope,
            self.right_slope,
            self.empty_intercept,
        )

    def add_hinge(self, threshold, coefficient):
        assert coefficient >= 0
        if coefficient == 0:
            return self
        self.arena.counts["positive_hinges"] += 1
        inserted = self.insert(threshold, self.value(threshold))
        root = self.arena.suffix_hinge(inserted.root, threshold, coefficient)
        return Curve(
            self.arena, root, self.left_slope, self.right_slope + coefficient, self.empty_intercept
        )

    def add_response(self, small):
        """Add nu(t)=t+sum c*(t-threshold)_+ from a smaller child subtree."""
        assert self.arena is small.arena and small.left_slope == 1
        result = self.affine((F(1), F(0), F(1), F(1), F(0), F(0)))
        previous_slope = F(1)
        points = self.arena.points(small.root)
        previous = next(points, None)
        for following in points:
            slope = (following[1] - previous[1]) / (following[0] - previous[0])
            self.arena.counts["merge_breakpoints_visited"] += 1
            result = result.add_hinge(previous[0], slope - previous_slope)
            previous, previous_slope = following, slope
        if previous:
            self.arena.counts["merge_breakpoints_visited"] += 1
            result = result.add_hinge(previous[0], small.right_slope - previous_slope)
        return result

    def prepend_zero_response(self, threshold):
        inserted = self.insert(threshold, threshold)
        return Curve(self.arena, inserted.root, F(1), inserted.right_slope)


def solve_tree(graph, seed, alpha, lam, degrees=None):
    """Exact solver on an entirely supplied tree, with persistent child curves."""
    deg = dict(graph.degree()) if degrees is None else degrees
    gamma = 1 - 2 * alpha / (1 + alpha)
    assert gamma > 0
    arena = Arena()
    parent, children, order = {seed: None}, {seed: []}, [seed]
    for i in order:
        for j in graph[i]:
            arena.counts["supplied_incidence_reads"] += 1
            if j != parent[i]:
                assert j not in parent
                parent[j], children[j] = i, []
                children[i].append(j)
                order.append(j)
    arena.counts["supplied_degree_reads"] += len(order)
    curves, sizes = {}, {}
    root_h = None
    for i in reversed(order):
        child = children[i]
        arena.counts["child_record_reads"] += 3 * len(child)
        sizes[i] = 1 + sum(sizes[j] for j in child)
        heavy = max(child, key=sizes.__getitem__) if child else None
        total = curves[heavy] if child else Curve(arena, None, F(0), F(0))
        for j in child:
            if j != heavy:
                total = total.add_response(curves[j])
        load = F(int(i == seed)) - lam * deg[i]
        h = total.affine((F(1), F(0), F(deg[i] + len(child)), F(-1), F(0), -load))
        assert h.left_slope > 0 and h.right_slope > 0
        if i == seed:
            root_h = h
        else:
            nu = h.affine((F(0), 1 / gamma, gamma, 1 / gamma, F(0), F(0)))
            curves[i] = nu.prepend_zero_response(-load / gamma)
    answer = {seed: max(F(0), root_h.inverse(F(0)))}
    for i in order[1:]:
        t = answer[parent[i]]
        answer[i] = (curves[i].value(t) - t) / gamma
        assert answer[i] >= 0
    arena.counts["output_words"] += len(answer)
    return answer, curves, root_h, parent, dict(arena.counts)


def audit_curve(curve):
    observer = Arena()
    observed = curve.with_arena(observer)
    points = list(observer.points(curve.root))
    assert all(x < xx and y < yy for (x, y), (xx, yy) in zip(points, points[1:]))
    stack = [curve.root] if curve.root else []
    while stack:
        node = stack.pop()
        assert abs(height(node.left) - height(node.right)) <= 1
        assert node.height == 1 + max(height(node.left), height(node.right))
        assert node.size == 1 + size(node.left) + size(node.right)
        stack.extend(child for child in [node.left, node.right] if child)
    xs = [F(-1), F(0), F(1), F(7)] + [x for x, _ in points]
    xs += [(a[0] + b[0]) / 2 for a, b in zip(points, points[1:])]
    for x in xs:
        assert observed.inverse(observed.value(x)) == x
    return len(xs)


def check_case(graph, seed, alpha, lam, grounding):
    deg = {i: graph.degree(i) + (i % 3 if grounding else 0) for i in graph}
    answer, curves, root_h, parent, counts = solve_tree(graph, seed, alpha, lam, deg)
    expected, _ = explicit_tree(graph, seed, alpha, lam, deg)
    assert answer == expected
    audit_queries = sum(audit_curve(c) for c in [*curves.values(), root_h])
    gamma = 1 - 2 * alpha / (1 + alpha)
    version_queries = 0
    for i, curve in curves.items():
        subtree = [i]
        for j in subtree:
            subtree.extend(k for k in graph[j] if k != parent[j])
        matrix = [
            [F(deg[j]) if j == k else -gamma if graph.has_edge(j, k) else F(0) for k in subtree]
            for j in subtree
        ]
        threshold = lam * deg[i] / gamma
        for t in [F(0), threshold, 2 * threshold, F(3)]:
            load = [-lam * deg[j] + (gamma * t if j == i else 0) for j in subtree]
            exact = obstacle(matrix, load)
            observed = curve.with_arena(Arena())
            assert (observed.value(t) - t) / gamma == exact[0]
            version_queries += 1
    return counts, audit_queries, version_queries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--largest", type=int, default=512)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.time()
    totals, cases, roundtrips, versions = Counter(), 0, 0, 0
    trees = [g for n in range(2, args.max_n + 1) for g in nx.nonisomorphic_trees(n)]
    alphas, lambdas = [F(2, 3), F(1, 7), F(1, 101)], [F(1, 5), F(1, 31), F(1, 1009)]
    for graph in trees:
        for seed, alpha, lam, grounding in itertools.product(graph, alphas, lambdas, [False, True]):
            counts, qs, vs = check_case(graph, seed, alpha, lam, grounding)
            totals.update(counts)
            cases, roundtrips, versions = cases + 1, roundtrips + qs, versions + vs
    rows = []
    if args.structured:
        n = 16
        while n <= args.largest:
            binary = nx.balanced_tree(2, (n.bit_length() - 1) - 1)
            comb = nx.path_graph(n // 2)
            comb.add_edges_from((i, n // 2 + i) for i in range(n // 2))
            for name, graph in [
                ("path", nx.path_graph(n)),
                ("star", nx.star_graph(n - 1)),
                ("binary", binary),
                ("comb", comb),
            ]:
                before = time.time()
                answer, curves, root_h, _, counts = solve_tree(graph, 0, F(1, 1009), F(1, 1009))
                row = {
                    "family": name,
                    "n": len(graph),
                    "counts": counts,
                    "support": sum(x > 0 for x in answer.values()),
                    "max_curve_height": max(
                        [height(c.root) for c in curves.values()] + [height(root_h.root)]
                    ),
                    "elapsed_seconds": round(time.time() - before, 3),
                }
                rows.append(row)
                print(
                    json.dumps(
                        {
                            "structured": name,
                            "n": len(graph),
                            "allocations": counts.get("node_allocations", 0),
                            "elapsed_seconds": row["elapsed_seconds"],
                        }
                    ),
                    flush=True,
                )
            n *= 2
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.persistent_affine_tree",
        "arithmetic": "exact fractions; deterministic persistent AVL",
        "trees": len(trees),
        "cases": cases,
        "max_n": args.max_n,
        "alpha_lazy": list(map(str, alphas)),
        "lambda_degree_load": list(map(str, lambdas)),
        "grounding_cases": ["tree degrees", "degree plus label modulo three"],
        "random_seed": None,
        "solver_counts": dict(totals),
        "audit_inverse_roundtrips": roundtrips,
        "retained_version_obstacle_queries": versions,
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
        "limitation": "Entire tree is supplied. Counts price actual AVL visits and copies; scalar bit complexity and local support discovery are not claimed. Audit-only reads are excluded from solver counts.",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
