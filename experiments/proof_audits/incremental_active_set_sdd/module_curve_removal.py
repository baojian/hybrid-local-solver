"""Persistent removal of a known convex zero-left summand in a shared field.

The remaining sum must be convex. Signed hinges are locally certified and
zero jumps are deleted, preventing redundant-knot history growth. This is
an algebraic primitive, not a bound for graph-admission curve replacement.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from persistent_affine_tree import Arena, Curve, IDENTITY, height, size
from persistent_module_response import PersistentModules, add_zero_left_response
from recursive_module_response import supplied_decomposition
import networkx as nx


class RemovalArena(Arena):
    def pop_first(self, node):
        self.counts["delete_path_visits"] += 1
        node = self.push(node)
        if node.left is None:
            return (node.x, node.y), node.right
        point, left = self.pop_first(node.left)
        return point, self.balance(self.node(node.x, node.y, left, node.right))

    def delete(self, node, x):
        assert node is not None
        self.counts["delete_path_visits"] += 1
        node = self.push(node)
        if x < node.x:
            return self.balance(self.node(node.x, node.y, self.delete(node.left, x), node.right))
        if x > node.x:
            return self.balance(self.node(node.x, node.y, node.left, self.delete(node.right, x)))
        self.counts["deleted_zero_jump_knots"] += 1
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        (sx, sy), right = self.pop_first(node.right)
        return self.balance(self.node(sx, sy, node.left, right))

    def strict_neighbor(self, node, x, lower):
        result, carry = None, IDENTITY
        while node:
            self.counts["strict_neighbor_path_visits"] += 1
            point = self.point(carry, node.x, node.y)
            carry = self.compose(carry, node.pending)
            if (point[0] < x) if lower else (point[0] > x):
                result = point
                node = node.right if lower else node.left
            else:
                node = node.left if lower else node.right
        return result


def remove_hinge(curve, x, coefficient):
    assert curve.left_slope == 0 and coefficient >= 0
    if coefficient == 0:
        return curve
    arena = curve.arena
    lo, hi = arena.bracket(curve.root, x, 0)
    assert lo == hi and lo is not None and lo[0] == x
    y = lo[1]
    previous = arena.strict_neighbor(curve.root, x, True)
    following = arena.strict_neighbor(curve.root, x, False)
    left = (y - previous[1]) / (x - previous[0]) if previous else curve.left_slope
    right = (following[1] - y) / (following[0] - x) if following else curve.right_slope
    jump = right - left
    assert 0 < coefficient <= jump
    arena.counts["certified_negative_hinges"] += 1
    root = arena.suffix_hinge(curve.root, x, -coefficient)
    if coefficient == jump:
        root = arena.delete(root, x)
    # All uses have zero left ray. This remains correct even if the last
    # knot disappears: the empty curve is then identically zero.
    return Curve(arena, root, F(0), curve.right_slope - coefficient, F(0))


def remove_response(total, child):
    assert total.arena is child.arena
    assert total.left_slope == child.left_slope == 0
    result, previous_slope = total, F(0)
    points = child.arena.points(child.root)
    previous = next(points, None)
    assert previous is None or previous[1] == 0
    for following in points:
        slope = (following[1] - previous[1]) / (following[0] - previous[0])
        child.arena.counts["removed_child_knots_streamed"] += 1
        result = remove_hinge(result, previous[0], slope - previous_slope)
        previous, previous_slope = following, slope
    if previous:
        child.arena.counts["removed_child_knots_streamed"] += 1
        result = remove_hinge(result, previous[0], child.right_slope - previous_slope)
    return result


def certify(curve, expected, counts):
    """Complete affine-piece identity, convexity, AVL shape and knot minimality."""
    observer = Arena()
    actual_points = list(observer.points(curve.root))
    expected_points = list(observer.points(expected.root))
    assert actual_points == expected_points
    assert (curve.left_slope, curve.right_slope, curve.empty_intercept) == (
        expected.left_slope,
        expected.right_slope,
        expected.empty_intercept,
    )
    slopes = [curve.left_slope]
    slopes += [(y - a) / (x - b) for (b, a), (x, y) in zip(actual_points, actual_points[1:])]
    slopes += [curve.right_slope] if actual_points else []
    assert all(a < b for a, b in zip(slopes, slopes[1:]))
    stack = [curve.root] if curve.root else []
    while stack:
        node = stack.pop()
        assert abs(height(node.left) - height(node.right)) <= 1
        assert node.height == 1 + max(height(node.left), height(node.right))
        assert node.size == 1 + size(node.left) + size(node.right)
        stack.extend(child for child in [node.left, node.right] if child)
        counts["avl_node_certificates"] += 1
    counts["complete_affine_piece_identities"] += len(actual_points) + 1
    counts["curve_identities"] += 1


def synthetic_cases(full, counts, operations):
    rng = random.Random(73081)
    for case in range(2000 if full else 100):
        arena = RemovalArena()
        components = []
        for _ in range(rng.randrange(1, 7)):
            curve = Curve(arena, None, F(0), F(0))
            for _ in range(rng.randrange(1, 18)):
                curve = curve.add_hinge(F(rng.randrange(-20, 21), 3), F(rng.randrange(1, 7), 11))
            components.append(curve)
        # A common positive horizontal shear retains convexity and exercises
        # inherited lazy tags; it is applied before taking the shared sum.
        transform = (F(1), F(case % 5, 7), F(0), F(1), F(0), F(0))
        components = [c.affine(transform) for c in components]
        total = Curve(arena, None, F(0), F(0))
        for component in components:
            total = add_zero_left_response(total, component)
        original = total
        order = list(range(len(components)))
        rng.shuffle(order)
        remaining = set(order)
        for index in order:
            remaining.remove(index)
            total = remove_response(total, components[index])
            reference_arena = Arena()
            expected = Curve(reference_arena, None, F(0), F(0))
            for j in sorted(remaining):
                expected = add_zero_left_response(
                    expected, components[j].with_arena(reference_arena)
                )
            certify(total, expected, counts)
        assert total.root is None and total.value(F(3)) == 0
        # Old sum still equals a fresh sum after all removals.
        reference_arena = Arena()
        expected = Curve(reference_arena, None, F(0), F(0))
        for c in components:
            expected = add_zero_left_response(expected, c.with_arena(reference_arena))
        certify(original, expected, counts)
        counts["complete_synthetic_removal_sequences"] += 1
        operations.update(arena.counts)


def module_cases(full, counts, operations):
    cores = []
    for core in nx.graph_atlas_g():
        if not 2 <= len(core) <= (6 if full else 4) or not nx.is_connected(core):
            continue
        try:
            nodes, _ = supplied_decomposition(core)
        except ValueError:
            continue
        cores.append(core)
        q = {i: i % 3 for i in core}
        degrees = {i: core.degree(i) + q[i] for i in core}
        for seed in core:
            state = PersistentModules(nodes, degrees, q, seed, F(1, 1009), F(1, 200))
            for k, node in enumerate(nodes):
                if node.kind == "leaf":
                    continue
                for slot in range(len(node.children)):
                    arena, ref = RemovalArena(), Arena()
                    total = state.curves[k].with_arena(arena)
                    streams = [state.curves[j] for j in node.children]
                    if node.kind == "join":
                        total = total.affine((F(1), state.gamma, F(0), F(1), F(0), F(0)))
                        streams = state.join_inputs[k]
                    child = streams[slot].with_arena(arena)
                    remaining = remove_response(total, child)
                    expected = Curve(ref, None, F(0), F(0))
                    for j, stream in enumerate(streams):
                        if j != slot:
                            expected = add_zero_left_response(expected, stream.with_arena(ref))
                    certify(remaining, expected, counts)
                    if node.kind == "join":
                        transform = (F(1), -state.gamma, F(0), F(1), F(0), F(0))
                        certify(remaining.affine(transform), expected.affine(transform), counts)
                        counts["join_sibling_response_reconstructions"] += 1
                    # Add back the exact saved child and recover the whole curve.
                    restored = add_zero_left_response(remaining, child)
                    certify(restored, total, counts)
                    assert arena.counts["removed_child_knots_streamed"] == size(child.root)
                    operations.update(arena.counts)
                    counts["supplied_module_child_extractions"] += 1
    return len(cores)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, operations = Counter(), Counter()
    synthetic_cases(args.full, counts, operations)
    cores = module_cases(args.full, counts, operations)
    result = {
        "audit": "incremental_active_set_sdd.module_curve_removal",
        "arithmetic": "exact fractions",
        "random_seed": 73081,
        "synthetic_family": "positive rational hinges, coincident knots, shared shears, random complete removal orders",
        "graph_family": "all connected supplied union/join graph-atlas cores through max_n",
        "max_n": 6 if args.full else 4,
        "distinct_cores": cores,
        "alpha": "1/1009",
        "lambda": "1/200",
        "seed": "every core vertex",
        "pendants": "vertex index mod 3",
        "stopping_rule": "complete affine identity after each removal, sibling reconstruction and restoration",
        "scope": "Known convex zero-left summand in a common field; convex remainder. O(k_child log(2+k_total)) word removal. No bound on the child sizes changed by graph admissions.",
        "audit_only": dict(counts),
        "operation_counts": dict(operations),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "persistent_affine_tree",
                "persistent_module_response",
                "recursive_module_response",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
