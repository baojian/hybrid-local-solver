"""Persistent upper convex chains with lazy projective port pullbacks.

Homogeneous row (X,Y,W,label) represents the point (X/W,Y/W), with W>0,
where a two-port gate is X*u_left+(W-X)*u_right+Y. This finite chart includes
both endpoint strata. Merges require separated x intervals. All state is
immutable and every copied node, tag operation and bridge search is counted.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import time


IDENTITY = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))


@dataclass(frozen=True, slots=True)
class Node:
    point: tuple
    left: Node | None
    right: Node | None
    height: int
    size: int
    pending: tuple


def height(node):
    return node.height if node else 0


def size(node):
    return node.size if node else 0


def port_map(matrix, offset):
    """Homogeneous action induced by old_ports = matrix*new_ports + offset."""
    (a, b), (c, d) = matrix
    u, v = offset
    assert min(a, b, c, d) >= 0 and a * d - b * c > 0
    assert a + b > 0 and c + d > 0 and max(u, v) <= 0
    return ((a - c, F(0), c), (u - v, F(1), v), (a + b - c - d, F(0), c + d))


def cartesian(point):
    x, y, w, label = point
    assert w > 0
    return x / w, y / w, label


def orientation(a, b, c):
    ax, ay, aw, _ = a
    bx, by, bw, _ = b
    cx, cy, cw, _ = c
    return ax * (by * cw - bw * cy) - ay * (bx * cw - bw * cx) + aw * (bx * cy - by * cx)


def static_upper(points):
    """Independent materialized hull, strictly audit-only."""
    ordered = sorted(points, key=lambda p: (F(p[0], p[2]), -F(p[1], p[2]), p[3]))
    unique = []
    for p in ordered:
        if not unique or p[0] * unique[-1][2] != unique[-1][0] * p[2]:
            unique.append(p)
    out = []
    for p in unique:
        while len(out) >= 2 and orientation(out[-2], out[-1], p) >= 0:
            out.pop()
        out.append(p)
    return out


class Arena:
    def __init__(self):
        self.counts = Counter()

    def compose(self, outer, inner):
        self.counts["projective_tag_compositions"] += 1
        return tuple(
            tuple(sum(outer[i][k] * inner[k][j] for k in range(3)) for j in range(3))
            for i in range(3)
        )

    def transform_point(self, transform, point):
        self.counts["projective_point_evaluations"] += 1
        q = tuple(sum(transform[i][j] * point[j] for j in range(3)) for i in range(3)) + (point[3],)
        assert q[2] > 0
        return q

    def node(self, point, left=None, right=None, pending=IDENTITY):
        self.counts["node_allocations"] += 1
        return Node(
            point,
            left,
            right,
            1 + max(height(left), height(right)),
            1 + size(left) + size(right),
            pending,
        )

    def apply(self, node, transform):
        if node is None:
            return None
        self.counts["tagged_roots"] += 1
        return self.node(
            self.transform_point(transform, node.point),
            node.left,
            node.right,
            self.compose(transform, node.pending),
        )

    def push(self, node):
        if node.pending == IDENTITY:
            return node
        self.counts["lazy_tag_pushes"] += 1
        return self.node(
            node.point, self.apply(node.left, node.pending), self.apply(node.right, node.pending)
        )

    def balance(self, p, left, right):
        if height(left) > height(right) + 1:
            left = self.push(left)
            if height(left.left) >= height(left.right):
                return self.node(left.point, left.left, self.node(p, left.right, right))
            middle = self.push(left.right)
            return self.node(
                middle.point,
                self.node(left.point, left.left, middle.left),
                self.node(p, middle.right, right),
            )
        if height(right) > height(left) + 1:
            right = self.push(right)
            if height(right.right) >= height(right.left):
                return self.node(right.point, self.node(p, left, right.left), right.right)
            middle = self.push(right.left)
            return self.node(
                middle.point,
                self.node(p, left, middle.left),
                self.node(right.point, middle.right, right.right),
            )
        return self.node(p, left, right)

    def join(self, left, p, right):
        self.counts["join_path_visits"] += 1
        if height(left) > height(right) + 1:
            left = self.push(left)
            return self.balance(left.point, left.left, self.join(left.right, p, right))
        if height(right) > height(left) + 1:
            right = self.push(right)
            return self.balance(right.point, self.join(left, p, right.left), right.right)
        return self.node(p, left, right)

    def split(self, node, k):
        self.counts["split_path_visits"] += 1
        assert 0 <= k <= size(node)
        if k == 0:
            return None, node
        if k == size(node):
            return node, None
        node = self.push(node)
        left_size = size(node.left)
        if k <= left_size:
            left, middle = self.split(node.left, k)
            return left, self.join(middle, node.point, node.right)
        middle, right = self.split(node.right, k - left_size - 1)
        return self.join(node.left, node.point, middle), right

    def get(self, node, k):
        assert 0 <= k < size(node)
        carry = IDENTITY
        while node:
            self.counts["select_path_visits"] += 1
            ls = size(node.left)
            if k == ls:
                return self.transform_point(carry, node.point)
            carry = self.compose(carry, node.pending)
            if k < ls:
                node = node.left
            else:
                k -= ls + 1
                node = node.right
        raise AssertionError("invalid rank")

    def concat(self, left, right):
        if not left:
            return right
        if not right:
            return left
        first, rest = self.split(right, 1)
        return self.join(left, first.point, rest)

    def slope(self, a, b):
        self.counts["bridge_slope_evaluations"] += 1
        denominator = b[0] * a[2] - a[0] * b[2]
        assert denominator > 0
        return (b[1] * a[2] - a[1] * b[2]) / denominator

    def right_tangent(self, p, right):
        low, high = 0, size(right) - 1
        while low < high:
            middle = (low + high) // 2
            if self.slope(p, self.get(right, middle)) <= self.slope(p, self.get(right, middle + 1)):
                low = middle + 1
            else:
                high = middle
        return low, self.slope(p, self.get(right, low))

    def merge(self, left, right):
        self.counts["separated_merges"] += 1
        if not left:
            return right
        if not right:
            return left
        a, b = self.get(left, size(left) - 1), self.get(right, 0)
        assert a[0] * b[2] <= b[0] * a[2]
        if a[0] * b[2] == b[0] * a[2]:
            # One endpoint row survives; use its label for exact coordinate ties.
            if a[1] * b[2] < b[1] * a[2] or (a[1] * b[2] == b[1] * a[2] and a[3] > b[3]):
                left, _ = self.split(left, size(left) - 1)
            else:
                _, right = self.split(right, 1)
            if not left:
                return right
            if not right:
                return left
        low, high = 0, size(left) - 1
        while low < high:
            middle = (low + high) // 2
            p = self.get(left, middle)
            _, slope = self.right_tangent(p, right)
            if self.slope(p, self.get(left, middle + 1)) > slope:
                low = middle + 1
            else:
                high = middle
        j, _ = self.right_tangent(self.get(left, low), right)
        prefix, _ = self.split(left, low + 1)
        _, suffix = self.split(right, j)
        return self.concat(prefix, suffix)

    def argmax_ratio(self, node, numerator, denominator):
        """Positive y coefficient; positive denominator affine in x alone."""
        self.counts["ratio_queries"] += 1
        if not node:
            return None
        assert numerator[1] > 0 and denominator[1] == 0

        def value(p):
            self.counts["ratio_point_evaluations"] += 1
            den = sum(denominator[i] * p[i] for i in range(3))
            assert den > 0
            return sum(numerator[i] * p[i] for i in range(3)) / den

        value(self.get(node, 0))
        value(self.get(node, size(node) - 1))
        low, high = 0, size(node) - 1
        while low < high:
            middle = (low + high) // 2
            if value(self.get(node, middle)) <= value(self.get(node, middle + 1)):
                low = middle + 1
            else:
                high = middle
        p = self.get(node, low)
        return value(p), p[3]

    def query(self, node, ports):
        left, right = ports
        return self.argmax_ratio(node, (left - right, F(1), right), (F(0), F(0), F(1)))

    def one_port(self, node, multipliers, offsets):
        a, b = multipliers
        u, v = offsets
        result = self.argmax_ratio(node, (u - v, F(1), v), (a - b, F(0), b))
        return (-result[0], result[1]) if result else None


def audit_chain(root, points, counts):
    observer = Arena()
    got = [cartesian(observer.get(root, i)) for i in range(size(root))]
    want = [cartesian(p) for p in static_upper(points)]
    assert got == want

    def check(n):
        if n is None:
            return
        assert abs(height(n.left) - height(n.right)) <= 1
        assert n.height == 1 + max(height(n.left), height(n.right))
        assert n.size == 1 + size(n.left) + size(n.right)
        check(n.left)
        check(n.right)

    check(root)
    counts["independent_static_chain_comparisons"] += 1
    counts["retained_point_comparisons"] += len(got)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    rng = random.Random(20260908)
    arena = Arena()
    audit = Counter()
    retained = []

    def transformed(points, t):
        return [
            tuple(sum(t[i][j] * p[j] for j in range(3)) for i in range(3)) + (p[3],) for p in points
        ]

    for n in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
        points = [(F(i, n), F(-1) - F(i * i, n * n), F(1), i) for i in range(n + 1)]
        root = None
        for p in points:
            root = arena.merge(root, arena.node(p))
        audit_chain(root, points, audit)
        retained.append((root, points))
        for step in range(12):
            a, b, c, d = (
                F(rng.randrange(1, 8)),
                F(rng.randrange(0, 3)),
                F(rng.randrange(0, 3)),
                F(rng.randrange(1, 8)),
            )
            if a * d <= b * c:
                a += 4
                d += 4
            offsets = (-F(rng.randrange(4), 7), -F(rng.randrange(4), 9))
            t = port_map(((a, b), (c, d)), offsets)
            before = arena.counts["node_allocations"]
            new = arena.apply(root, t)
            assert arena.counts["node_allocations"] - before == 1
            points = transformed(points, t)
            root = new
            audit_chain(root, points, audit)
            for _ in range(3):
                ports = (F(rng.randrange(-8, 20), 7), F(rng.randrange(-8, 20), 9))
                got = arena.query(root, ports)
                want = max(
                    (p[0] * ports[0] + (p[2] - p[0]) * ports[1] + p[1]) / p[2] for p in points
                )
                assert got[0] == want
                audit["exact_extreme_queries"] += 1
                multipliers = (F(rng.randrange(1, 10), 7), F(rng.randrange(1, 10), 5))
                off = (-F(rng.randrange(4), 3), -F(rng.randrange(4), 5))
                scalar = arena.one_port(root, multipliers, off)
                ratios = [
                    -(p[1] + p[0] * off[0] + (p[2] - p[0]) * off[1])
                    / (p[0] * multipliers[0] + (p[2] - p[0]) * multipliers[1])
                    for p in points
                ]
                assert scalar[0] == min(ratios)
                audit["exact_one_port_queries"] += 1
            k = rng.randrange(size(root) + 1)
            left, right = arena.split(root, k)
            joined = arena.concat(left, right)
            audit_chain(joined, points, audit)
            root = joined
            retained.append((root, points))
        for old, old_points in retained[-4:]:
            audit_chain(old, old_points, audit)
    # Canonical compress views have separated intervals including equal endpoints.
    for case in range(96):
        eta, zeta = F(rng.randrange(1, 9), 11), F(rng.randrange(1, 9), 13)
        shift = -F(rng.randrange(1, 7), 17)
        left_points = [
            (F(i, 16), -F(rng.randrange(1, 200), 31), F(1), 1000 + 32 * case + i) for i in range(17)
        ]
        right_points = [
            (F(i, 16), -F(rng.randrange(1, 200), 31), F(1), 20000 + 32 * case + i)
            for i in range(17)
        ]

        def build(points):
            root = None
            for p in points:
                root = arena.merge(root, arena.node(p))
            return root

        left, right = build(left_points), build(right_points)
        tl = port_map(((F(1), F(0)), (eta, zeta)), (F(0), shift))
        tr = port_map(((eta, zeta), (F(0), F(1))), (shift, F(0)))
        lp, rp = transformed(left_points, tl), transformed(right_points, tr)
        assert max(p[0] / p[2] for p in rp) <= min(p[0] / p[2] for p in lp)
        merged = arena.merge(arena.apply(right, tr), arena.apply(left, tl))
        audit_chain(merged, rp + lp, audit)
        audit["compress_separation_checks"] += 1
    for root, points in retained:
        audit_chain(root, points, audit)
    result = {
        "audit": "incremental_active_set_sdd.projective_hull_rope",
        "arithmetic": "exact fractions",
        "random_seed": 20260908,
        "scope": "persistent separated convex-chain primitive, not graph solver",
        "counts": dict(arena.counts),
        "audit_only": dict(audit),
        "retained_versions": len(retained),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
