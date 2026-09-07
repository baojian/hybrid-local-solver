"""Exact dynamic upper hull using AVL points and persistent AVL hull ropes.

The deliberately conservative bound is O(log^4 n) per point update and
O(log^2 n) per nonnegative-direction extreme query. No bulk affine pullback
or arbitrary interleaved hull meld is offered. This is a research primitive.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess


def height(node):
    return node.height if node else 0


def size(node):
    return node.size if node else 0


@dataclass(frozen=True, slots=True)
class Rope:
    point: tuple
    left: Rope | None
    right: Rope | None
    height: int
    size: int


@dataclass(frozen=True, slots=True)
class PointNode:
    point: tuple
    left: PointNode | None
    right: PointNode | None
    height: int
    hull: Rope


class HullArena:
    def __init__(self):
        self.counts = Counter()

    def node(self, p, left=None, right=None):
        self.counts["rope_allocations"] += 1
        return Rope(
            p, left, right, 1 + max(height(left), height(right)), 1 + size(left) + size(right)
        )

    def balance(self, p, left, right):
        if height(left) > height(right) + 1:
            if height(left.left) >= height(left.right):
                return self.node(left.point, left.left, self.node(p, left.right, right))
            middle = left.right
            return self.node(
                middle.point,
                self.node(left.point, left.left, middle.left),
                self.node(p, middle.right, right),
            )
        if height(right) > height(left) + 1:
            if height(right.right) >= height(right.left):
                return self.node(right.point, self.node(p, left, right.left), right.right)
            middle = right.left
            return self.node(
                middle.point,
                self.node(p, left, middle.left),
                self.node(right.point, middle.right, right.right),
            )
        return self.node(p, left, right)

    def join(self, left, p, right):
        self.counts["rope_join_visits"] += 1
        if height(left) > height(right) + 1:
            return self.balance(left.point, left.left, self.join(left.right, p, right))
        if height(right) > height(left) + 1:
            return self.balance(right.point, self.join(left, p, right.left), right.right)
        return self.node(p, left, right)

    def split(self, node, k):
        self.counts["rope_split_visits"] += 1
        if k == 0:
            return None, node
        if k == size(node):
            return node, None
        left_size = size(node.left)
        if k <= left_size:
            left, middle = self.split(node.left, k)
            return left, self.join(middle, node.point, node.right)
        middle, right = self.split(node.right, k - left_size - 1)
        return self.join(node.left, node.point, middle), right

    def get(self, node, k):
        assert 0 <= k < size(node)
        while node:
            self.counts["rope_select_visits"] += 1
            left_size = size(node.left)
            if k == left_size:
                return node.point
            if k < left_size:
                node = node.left
            else:
                k -= left_size + 1
                node = node.right
        raise AssertionError("invalid rope rank")

    def concat(self, left, right):
        if not left:
            return right
        if not right:
            return left
        first, rest = self.split(right, 1)
        return self.join(left, first.point, rest)

    def slope(self, a, b):
        self.counts["slope_comparisons"] += 1
        assert a[0] < b[0]
        return (b[1] - a[1]) / (b[0] - a[0])

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
        self.counts["separated_hull_merges"] += 1
        if not left:
            return right
        if not right:
            return left
        a, b = self.get(left, size(left) - 1), self.get(right, 0)
        assert a[0] <= b[0]
        if a[0] == b[0]:
            if a[1] <= b[1]:
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


class DynamicUpperHull:
    def __init__(self):
        self.arena = HullArena()
        self.root = None
        self.points = {}

    @property
    def counts(self):
        return self.arena.counts

    def node(self, p, left=None, right=None):
        self.counts["point_node_allocations"] += 1
        hull = self.arena.merge(left.hull if left else None, self.arena.node(p))
        hull = self.arena.merge(hull, right.hull if right else None)
        return PointNode(p, left, right, 1 + max(height(left), height(right)), hull)

    def balance(self, p, left, right):
        if height(left) > height(right) + 1:
            if height(left.left) >= height(left.right):
                return self.node(left.point, left.left, self.node(p, left.right, right))
            middle = left.right
            return self.node(
                middle.point,
                self.node(left.point, left.left, middle.left),
                self.node(p, middle.right, right),
            )
        if height(right) > height(left) + 1:
            if height(right.right) >= height(right.left):
                return self.node(right.point, self.node(p, left, right.left), right.right)
            middle = right.left
            return self.node(
                middle.point,
                self.node(p, left, middle.left),
                self.node(right.point, middle.right, right.right),
            )
        return self.node(p, left, right)

    def insert(self, node, point):
        self.counts["point_tree_visits"] += 1
        if not node:
            return self.node(point)
        if point < node.point:
            return self.balance(node.point, self.insert(node.left, point), node.right)
        assert point > node.point
        return self.balance(node.point, node.left, self.insert(node.right, point))

    def erase(self, node, point):
        self.counts["point_tree_visits"] += 1
        assert node
        if point < node.point:
            return self.balance(node.point, self.erase(node.left, point), node.right)
        if point > node.point:
            return self.balance(node.point, node.left, self.erase(node.right, point))
        if not node.left:
            return node.right
        if not node.right:
            return node.left
        successor = node.right
        while successor.left:
            self.counts["point_tree_visits"] += 1
            successor = successor.left
        return self.balance(successor.point, node.left, self.erase(node.right, successor.point))

    def delete(self, label):
        self.counts["point_deletions"] += 1
        self.root = self.erase(self.root, self.points.pop(label))

    def set(self, label, coordinates):
        self.counts["point_sets"] += 1
        if label in self.points:
            self.delete(label)
        point = (*coordinates, label)
        self.root = self.insert(self.root, point)
        self.points[label] = point

    def extreme(self, direction):
        self.counts["extreme_queries"] += 1
        assert min(direction) >= 0
        if not self.root:
            return None
        hull = self.root.hull
        low, high = 0, size(hull) - 1

        def value(i):
            p = self.arena.get(hull, i)
            return direction[0] * p[0] + direction[1] * p[1]

        while low < high:
            middle = (low + high) // 2
            if value(middle) <= value(middle + 1):
                low = middle + 1
            else:
                high = middle
        return self.arena.get(hull, low)[2], value(low)


def audit_chain(hull, reference):
    """Independent static scan; never used by the dynamic primitive."""
    expected = []
    by_x = {}
    for x, y in reference.values():
        by_x[x] = max(by_x.get(x, y), y)
    for p in sorted(by_x.items()):
        while len(expected) > 1:
            a, b = expected[-2:]
            turn = (b[0] - a[0]) * (p[1] - b[1]) - (b[1] - a[1]) * (p[0] - b[0])
            if turn < 0:
                break
            expected.pop()
        expected.append(p)

    def walk(node):
        if not node:
            return []
        left, right = walk(node.left), walk(node.right)
        assert abs(height(node.left) - height(node.right)) <= 1
        assert node.height == 1 + max(height(node.left), height(node.right))
        assert node.size == 1 + len(left) + len(right)
        return left + [node.point[:2]] + right

    actual = walk(hull.root.hull) if hull.root else []
    assert actual == expected, (actual, expected)


def main():
    rng = random.Random(73021)
    hull = DynamicUpperHull()
    reference = {}
    queries = 0
    for step in range(1600):
        label = rng.randrange(160)
        if label in reference and rng.randrange(3) == 0:
            hull.delete(label)
            del reference[label]
        else:
            point = (F(rng.randrange(23), 7), F(rng.randrange(29), 11))
            hull.set(label, point)
            reference[label] = point
        for direction in [(F(0), F(1)), (F(1), F(0)), (F(rng.randrange(13)), F(rng.randrange(17)))]:
            answer = hull.extreme(direction)
            expected = max(
                (sum(a * b for a, b in zip(p, direction)) for p in reference.values()), default=None
            )
            assert (None if answer is None else answer[1]) == expected, (
                step,
                direction,
                answer,
                expected,
            )
            queries += 1
        audit_chain(hull, reference)
    structured = []
    for n in [32, 128, 512]:
        curved = DynamicUpperHull()
        points = {}
        for i in range(n):
            p = (F(i), F(n * n - i * i))
            points[i] = p
            curved.set(i, p)
        audit_chain(curved, points)
        for i in range(0, n, 2):
            curved.delete(i)
            del points[i]
            direction = (F(rng.randrange(2 * n)), F(1))
            answer = curved.extreme(direction)
            expected = max(sum(a * b for a, b in zip(p, direction)) for p in points.values())
            assert answer[1] == expected
            queries += 1
        audit_chain(curved, points)
        structured.append(
            {"initial_points": n, "remaining_points": len(points), "counts": dict(curved.counts)}
        )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.dynamic_upper_hull",
        "arithmetic": "exact fractions; nonnegative query directions",
        "randomized_operations": 1600,
        "exact_extreme_comparisons": queries,
        "random_seed": 73021,
        "counts": dict(hull.counts),
        "static_chain_comparisons": 1606,
        "structured_rows": structured,
        "git_commit": subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
        ).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(
                ["git", "-C", str(repo), "status", "--porcelain"], text=True
            ).strip()
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = repo / "results/raw/op3_dynamic_upper_hull.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
