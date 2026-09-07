"""Persistent derivative-integral VWFs and exact supplied forest elimination.

Immutable affine AVL roots retain exact trapezoid integrals. The implementation
charges every path, smaller-curve stream, prefix deletion and new node. Explicit
polynomial curves and original KKT are independent validation work.
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
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from module_curve_removal import RemovalArena
from bounded_vwf_compression import VWF
from persistent_affine_tree import Curve, IDENTITY, height, size
from vwf_forest_reference import (
    PieceVWF,
    ReferenceForest,
    add_functions,
    certify_forest_solution,
    random_function,
)
import networkx as nx


def trapezoid(left, right):
    return (right[0] - left[0]) * (left[1] + right[1]) / 2


@dataclass(frozen=True, slots=True)
class IntegralNode:
    x: F
    y: F
    left: IntegralNode | None
    right: IntegralNode | None
    height: int
    size: int
    pending: tuple
    first: tuple
    last: tuple
    area: F


class IntegralArena(RemovalArena):
    def node(self, x, y, left=None, right=None, pending=IDENTITY):
        assert pending == IDENTITY
        point = (x, y)
        area = F(0)
        if left:
            area += left.area + trapezoid(left.last, point)
        if right:
            area += trapezoid(point, right.first) + right.area
        self.counts["node_allocations"] += 1
        self.counts["aggregate_reconstructions"] += 1
        return IntegralNode(
            x,
            y,
            left,
            right,
            1 + max(height(left), height(right)),
            1 + size(left) + size(right),
            IDENTITY,
            left.first if left else point,
            right.last if right else point,
            area,
        )

    def transformed_aggregate(self, transform, first, last, area):
        a, b, c, d, _, ty = transform
        x0, y0 = first
        x1, y1 = last
        new_area = (
            (a * d - b * c) * area
            + b * c * (x1 * y1 - x0 * y0)
            + a * c * (x1 * x1 - x0 * x0) / 2
            + b * d * (y1 * y1 - y0 * y0) / 2
            + ty * (a * (x1 - x0) + b * (y1 - y0))
        )
        self.counts["affine_integral_transformations"] += 1
        return self.point(transform, *first), self.point(transform, *last), new_area

    def apply(self, node, transform):
        if node is None:
            return None
        self.counts["tagged_subtree_roots"] += 1
        self.counts["node_allocations"] += 1
        x, y = self.point(transform, node.x, node.y)
        first, last, area = self.transformed_aggregate(transform, node.first, node.last, node.area)
        return IntegralNode(
            x,
            y,
            node.left,
            node.right,
            node.height,
            node.size,
            self.compose(transform, node.pending),
            first,
            last,
            area,
        )

    def readonly_aggregate(self, node, carry):
        self.counts["readonly_aggregate_visits"] += 1
        if carry == IDENTITY:
            return node.first, node.last, node.area
        return self.transformed_aggregate(carry, node.first, node.last, node.area)

    def prefix_integral(self, node, x, carry=IDENTITY):
        first, last, area = self.readonly_aggregate(node, carry)
        self.counts["prefix_integral_path_visits"] += 1
        if x <= first[0]:
            return F(0)
        if x >= last[0]:
            return area
        point = self.point(carry, node.x, node.y)
        child_carry = self.compose(carry, node.pending)
        if x <= point[0]:
            assert node.left is not None
            _, left_last, left_area = self.readonly_aggregate(node.left, child_carry)
            if x <= left_last[0]:
                return self.prefix_integral(node.left, x, child_carry)
            y = left_last[1] + (point[1] - left_last[1]) * (x - left_last[0]) / (
                point[0] - left_last[0]
            )
            return left_area + trapezoid(left_last, (x, y))
        partial = F(0)
        if node.left:
            _, left_last, left_area = self.readonly_aggregate(node.left, child_carry)
            partial = left_area + trapezoid(left_last, point)
        assert node.right is not None
        right_first, _, _ = self.readonly_aggregate(node.right, child_carry)
        if x <= right_first[0]:
            y = point[1] + (right_first[1] - point[1]) * (x - point[0]) / (
                right_first[0] - point[0]
            )
            return partial + trapezoid(point, (x, y))
        return (
            partial
            + trapezoid(point, right_first)
            + self.prefix_integral(node.right, x, child_carry)
        )


@dataclass(frozen=True)
class IntegralVWF:
    arena: IntegralArena
    lower: F
    value_at_lower: F
    root: IntegralNode
    tail_curvature: F = F(0)

    @classmethod
    def from_pieces(cls, arena, f):
        points = []
        for x, (a, b, _) in zip([f.lower] + list(f.splits), f.pieces):
            points.append((x, 2 * a * x + b))
            arena.counts["input_piece_records_read"] += 1
        arena.counts["input_point_words_allocated"] += 2 * len(points)

        def build(lo, hi):
            if lo == hi:
                return None
            mid = (lo + hi) // 2
            return arena.node(*points[mid], build(lo, mid), build(mid + 1, hi))

        arena.counts["curve_descriptors_allocated"] += 1
        return cls(arena, f.lower, f.value(f.lower), build(0, len(points)))

    def with_arena(self, arena):
        return IntegralVWF(arena, self.lower, self.value_at_lower, self.root, self.tail_curvature)

    def derivative(self, x):
        assert x >= self.lower
        self.arena.counts["derivative_queries"] += 1
        return Curve(self.arena, self.root, F(0), self.tail_curvature).value(x)

    def value(self, x):
        assert x >= self.lower
        self.arena.counts["function_value_queries"] += 1
        last_x, last_y = self.root.last
        if x >= last_x:
            distance = x - last_x
            return (
                self.value_at_lower
                + self.root.area
                + last_y * distance
                + self.tail_curvature * distance**2 / 2
            )
        return self.value_at_lower + self.arena.prefix_integral(self.root, x)

    def lift(self, weight, parent_lower):
        assert weight > 0 and parent_lower <= 0 and self.tail_curvature == 0
        arena = self.arena
        root = arena.apply(self.root, (F(1), 1 / weight, F(0), F(1), F(0), F(0)))
        if parent_lower <= root.first[0]:
            value = self.value_at_lower + weight * (parent_lower - self.lower) ** 2 / 2
            if parent_lower < root.first[0]:
                root = arena.insert(root, parent_lower, weight * (parent_lower - self.lower))
                arena.counts["new_Lift_domain_endpoints"] += 1
            arena.counts["boundary_Lift_endpoint_evaluations"] += 1
        else:
            derivative = Curve(arena, root, F(0), F(0)).value(parent_lower)
            minimizing_y = parent_lower - derivative / weight
            value = self.value(minimizing_y) + derivative**2 / (2 * weight)
            while root is not None and root.first[0] <= parent_lower:
                _, root = arena.pop_first(root)
                arena.counts["Lift_prefix_points_removed"] += 1
            root = arena.insert(root, parent_lower, derivative)
            arena.counts["new_Lift_domain_endpoints"] += 1
            arena.counts["interior_Lift_endpoint_evaluations"] += 1
        arena.counts["curve_descriptors_allocated"] += 1
        arena.counts["complete_Lift_operations"] += 1
        return IntegralVWF(arena, parent_lower, value, root)

    def minimum_point(self):
        assert self.tail_curvature == 0 and self.root.last[1] >= 0
        self.arena.counts["root_minimum_queries"] += 1
        if self.root.first[1] >= 0:
            return self.lower
        lo, hi = self.arena.bracket(self.root, F(0), 1)
        assert hi is not None
        if lo == hi:
            return hi[0]
        assert lo is not None and lo[1] < 0 <= hi[1]
        return lo[0] - lo[1] * (hi[0] - lo[0]) / (hi[1] - lo[1])

    def export(self):
        """Read-only canonical curvature atoms for the global compressor."""
        assert self.tail_curvature == 0
        constant, slope = self.value(F(0)), self.derivative(F(0))
        points = self.arena.points(self.root)
        first, previous = next(points), next(points, None)
        self.arena.counts["exported_derivative_points_streamed"] += 1 + (previous is not None)
        curvature = (previous[1] - first[1]) / (previous[0] - first[0]) if previous else F(0)
        knots = []
        if previous is not None:
            for following in points:
                self.arena.counts["exported_derivative_points_streamed"] += 1
                next_curvature = (following[1] - previous[1]) / (following[0] - previous[0])
                drop = curvature - next_curvature
                assert drop >= 0
                if drop:
                    knots.append((previous[0], drop))
                previous, curvature = following, next_curvature
            if curvature:
                knots.append((previous[0], curvature))
        self.arena.counts["exported_canonical_words_allocated"] += 3 + 2 * len(knots)
        return VWF(self.lower, constant, slope, tuple(knots))


def add_vwf(base, smaller):
    assert base.arena is smaller.arena and base.lower == smaller.lower
    assert base.tail_curvature == smaller.tail_curvature == 0
    arena = base.arena
    points = arena.points(smaller.root)
    first, following = next(points), next(points, None)
    arena.counts["smaller_curve_points_streamed"] += 1 + (following is not None)
    curvature = (following[1] - first[1]) / (following[0] - first[0]) if following else F(0)
    root = arena.apply(
        base.root, (F(1), F(0), curvature, F(1), F(0), first[1] - curvature * first[0])
    )
    constant = base.value_at_lower + smaller.value_at_lower
    result = IntegralVWF(arena, base.lower, constant, root, curvature)
    arena.counts["curve_descriptors_allocated"] += 1
    previous, previous_curvature = following, curvature
    if previous is not None:
        for after in points:
            arena.counts["smaller_curve_points_streamed"] += 1
            next_curvature = (after[1] - previous[1]) / (after[0] - previous[0])
            result = add_curvature_drop(result, previous[0], next_curvature - previous_curvature)
            previous, previous_curvature = after, next_curvature
        result = add_curvature_drop(result, previous[0], -previous_curvature)
    assert result.tail_curvature == 0
    arena.counts["complete_VWF_additions"] += 1
    return result


def add_curvature_drop(curve, at, change):
    assert change <= 0
    if change == 0:
        curve.arena.counts["skipped_zero_curvature_drops"] += 1
        return curve
    arena = curve.arena
    value = curve.derivative(at)
    root = arena.insert(curve.root, at, value)
    root = arena.suffix_hinge(root, at, change)
    arena.counts["curve_descriptors_allocated"] += 1
    arena.counts["streamed_negative_curvature_hinges"] += 1
    return IntegralVWF(
        arena, curve.lower, curve.value_at_lower, root, curve.tail_curvature + change
    )


class PersistentForest:
    def __init__(self, graph, functions, roots, arena):
        n = len(graph)
        self.arena, self.graph, self.functions, self.roots = arena, graph, functions, tuple(roots)
        self.parent, self.order = [-2] * n, []
        self.parent_weight = [None] * n
        self.coarse_edges = []
        is_root = [False] * n
        for root in roots:
            is_root[root] = True
            arena.counts["supplied_root_ids_read"] += 1
        arena.counts["topology_array_words_allocated"] += 4 * n
        for root in roots:
            assert self.parent[root] == -2
            self.parent[root] = -1
            self.order.append(root)
            cursor = len(self.order) - 1
            while cursor < len(self.order):
                v = self.order[cursor]
                for w, edge in graph[v].items():
                    arena.counts["supplied_graph_incidence_visits"] += 1
                    if w == self.parent[v]:
                        continue
                    if is_root[w]:
                        assert is_root[v], "An eliminated vertex cannot have another root incidence"
                        if v < w:
                            self.coarse_edges.append((v, w, edge["weight"]))
                            arena.counts["coarse_edge_records_allocated"] += 1
                            arena.counts["supplied_edge_weight_queries"] += 1
                        continue
                    assert self.parent[w] == -2, (
                        "Nonforest incidences at eliminated vertices are not allowed"
                    )
                    self.parent[w] = v
                    self.parent_weight[w] = edge["weight"]
                    arena.counts["supplied_edge_weight_queries"] += 1
                    arena.counts["forest_edge_weight_records_stored"] += 1
                    self.order.append(w)
                cursor += 1
        assert len(self.order) == n
        self.curves, self.lifted, self.mass = [None] * n, [None] * n, [0] * n
        arena.counts["response_array_words_allocated"] += 3 * n
        for v in reversed(self.order):
            own = IntegralVWF.from_pieces(arena, functions[v])
            parts = [(len(functions[v].splits) + 2, own)]
            for w in graph[v]:
                arena.counts["supplied_graph_incidence_visits"] += 1
                if self.parent[w] == v:
                    parts.append((self.mass[w], self.lifted[w]))
            arena.counts["merge_descriptor_words_allocated"] += 2 * len(parts)
            largest = max(range(len(parts)), key=lambda j: parts[j][0])
            arena.counts["largest_mass_selection_records"] += len(parts)
            result = parts[largest][1]
            for j, (_, part) in enumerate(parts):
                if j != largest:
                    result = add_vwf(result, part)
            self.curves[v], self.mass[v] = result, sum(m for m, _ in parts)
            assert result.root.size <= self.mass[v]
            if self.parent[v] >= 0:
                p = self.parent[v]
                arena.counts["stored_Lift_weight_reads"] += 1
                self.lifted[v] = result.lift(self.parent_weight[v], functions[p].lower)
        arena.counts["retained_curve_versions"] += 2 * n - len(roots)

    def recover(self, root_values):
        values = [None] * len(self.graph)
        self.arena.counts["output_vector_words_allocated"] += len(values)
        for v, x in root_values.items():
            values[v] = x
            self.arena.counts["supplied_root_values_read"] += 1
        for v in self.order:
            if self.parent[v] >= 0:
                p = self.parent[v]
                c = self.parent_weight[v]
                self.arena.counts["stored_reconstruction_weight_reads"] += 1
                values[v] = values[p] - self.lifted[v].derivative(values[p]) / c
        return values


def certify_curve(actual, expected, counts):
    """All derivative pieces and function constants, plus every stored aggregate."""
    observer = IntegralArena()
    curve = actual.with_arena(observer)
    assert curve.lower == expected.lower and curve.tail_curvature == 0
    exported = PieceVWF.from_atoms(curve.export())
    points = list(observer.points(curve.root))
    splits = sorted({curve.lower, *expected.splits, *(p[0] for p in points)})
    for lo, hi in zip(splits, splits[1:] + [None]):
        right = lo + 1 if hi is None else hi
        midpoint = (lo + right) / 2
        assert curve.derivative(lo) == expected.derivative(lo)
        assert curve.derivative(midpoint) == expected.derivative(midpoint)
        # Derivatives are affine on the full overlay interval. One anchored
        # value and exact integral then certify complete quadratic equality.
        assert curve.value(lo) == expected.value(lo)
        assert curve.value(midpoint) == expected.value(midpoint)
        assert exported.piece(midpoint) == expected.piece(midpoint)
        counts["complete_derivative_and_quadratic_overlay_intervals"] += 1
    stack = [curve.root]
    while stack:
        node = stack.pop()
        assert abs(height(node.left) - height(node.right)) <= 1
        assert node.height == 1 + max(height(node.left), height(node.right))
        assert node.size == 1 + size(node.left) + size(node.right)
        materialized = list(observer.points(node))
        assert node.first == materialized[0] and node.last == materialized[-1]
        assert node.area == sum(
            (trapezoid(a, b) for a, b in zip(materialized, materialized[1:])), F(0)
        )
        counts["immutable_AVL_and_integral_aggregate_certificates"] += 1
        stack.extend(child for child in [node.left, node.right] if child)
    assert observer.counts["node_allocations"] == 0
    counts["complete_curve_and_old_version_certificates"] += 1


def retained_root_cases(full, rng, counts, work):
    records = []
    for branches in [2, 5, 11] if full else [2]:
        graph = nx.complete_graph(3)
        roots = [0, 1, 2]
        for root in roots:
            previous = root
            for _ in range(branches):
                vertex = len(graph)
                graph.add_edge(previous, vertex)
                previous = vertex
        for index, (v, w) in enumerate(graph.edges()):
            graph[v][w]["weight"] = F(1 + index % 7, 1 + index % 3)
        functions = [random_function(rng, -F(2) if v in roots else None) for v in graph]
        arena = IntegralArena()
        forest = PersistentForest(graph, functions, roots, arena)
        for root in roots:
            exported = forest.curves[root].export()
            assert exported.constant <= 0
        reference = ReferenceForest(graph, functions, roots, counts)
        for v in graph:
            certify_curve(forest.curves[v], reference.curves[v], counts)
            if v not in roots:
                certify_curve(forest.lifted[v], reference.lifted[v], counts)
        for scale in [-F(1), F(0), F(1, 3), F(3), F(16)]:
            fixed = {v: scale + F(v, 4) for v in roots}
            values = forest.recover(fixed)
            energy, gradients = certify_forest_solution(graph, functions, values, counts, roots)
            reduced_energy = sum(forest.curves[v].value(fixed[v]) for v in roots)
            reduced_gradients = {v: forest.curves[v].derivative(fixed[v]) for v in roots}
            for v, w, c in forest.coarse_edges:
                reduced_energy += c * (fixed[v] - fixed[w]) ** 2 / 2
                reduced_gradients[v] += c * (fixed[v] - fixed[w])
                reduced_gradients[w] -= c * (fixed[v] - fixed[w])
            assert reduced_energy == energy
            assert all(gradients[v] == reduced_gradients[v] for v in roots)
            counts["retained_root_conditional_energy_and_gradient_certificates"] += 1
        work.update(arena.counts)
        records.append(
            {
                "family": "three retained roots with a triangle and separate path attachments",
                "vertices": len(graph),
                "branch_length": branches,
                "root_fields": ["-1+v/4", "v/4", "1/3+v/4", "3+v/4", "16+v/4"],
                "solver_counts": dict(arena.counts),
            }
        )
    return records


def structured_cases(full, counts, work):
    records = []
    for n in [32, 128, 512] if full else [16]:
        graphs = {
            "path": nx.path_graph(n),
            "star": nx.star_graph(n - 1),
            "binary": nx.Graph([(v, (v - 1) // 2) for v in range(1, n)]),
        }
        for name, graph in graphs.items():
            # Explicitly relabel to a contiguous supplied vertex array.
            graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
            for index, (v, w) in enumerate(graph.edges()):
                graph[v][w]["weight"] = F(1 + index % 3, 1 + index % 2)
            functions = [
                PieceVWF.from_atoms(
                    VWF(
                        F(0),
                        F(0),
                        -F(4) if v == 0 else F(0),
                        ((F(1) + F(v, 2 * n), F(1) + F(v % 5, 4)),),
                    )
                )
                for v in range(n)
            ]
            arena = IntegralArena()
            forest = PersistentForest(graph, functions, [0], arena)
            forest.curves[0].export()
            values = forest.recover({0: forest.curves[0].minimum_point()})
            energy, _ = certify_forest_solution(graph, functions, values, counts)
            observer = IntegralArena()
            assert energy == forest.curves[0].with_arena(observer).value(values[0])
            mass = 3 * n
            assert arena.counts["Lift_prefix_points_removed"] <= 3 * n - 1
            assert arena.counts["smaller_curve_points_streamed"] <= mass * mass.bit_length()
            record = {
                "family": name,
                "vertices": n,
                "root": 0,
                "input_events": n,
                "mass": mass,
                "largest_curve_points": max(f.root.size for f in forest.curves),
                "maximum_AVL_height": max(f.root.height for f in forest.curves),
                "positive_output_coordinates": sum(x > 0 for x in values),
                "solver_counts": dict(arena.counts),
            }
            records.append(record)
            work.update(arena.counts)
            counts["structured_original_KKT_reconstructions"] += 1
    return records


def affine_aggregate_cases(full, rng, counts, work):
    for _ in range(1000 if full else 40):
        arena = IntegralArena()
        curve = IntegralVWF.from_pieces(arena, random_function(rng))
        observer = IntegralArena()
        root = curve.root
        points = list(observer.points(root))
        retained = [(root, points)]
        transforms = [
            (F(2), F(1, 3), -F(2, 7), F(3, 2), -F(4), F(5, 3)),
            (F(3, 5), F(0), F(7, 11), -F(5, 3), F(2), -F(9, 4)),
        ]
        for transform in transforms:
            root = arena.apply(root, transform)
            a, b, c, d, tx, ty = transform
            points = [(a * x + b * y + tx, c * x + d * y + ty) for x, y in points]
            retained.append((root, points))
        for saved_root, expected in retained:
            assert list(observer.points(saved_root)) == expected
            assert saved_root.area == sum(
                (trapezoid(a, b) for a, b in zip(expected, expected[1:])), F(0)
            )
            accumulated = F(0)
            for left, right in zip(expected, expected[1:]):
                middle = ((left[0] + right[0]) / 2, (left[1] + right[1]) / 2)
                assert observer.prefix_integral(saved_root, middle[0]) == accumulated + trapezoid(
                    left, middle
                )
                accumulated += trapezoid(left, right)
                assert observer.prefix_integral(saved_root, right[0]) == accumulated
                counts["general_affine_complete_segment_and_prefix_integrals"] += 1
            counts["general_affine_aggregate_and_retained_versions"] += 1
        assert observer.counts["node_allocations"] == 0
        work.update(arena.counts)


def invalid_topology_cases(counts, work):
    for graph, roots in [
        (nx.path_graph(3), [0, 2]),
        (nx.cycle_graph(4), [0]),
        (nx.complete_graph(4), [0, 1]),
    ]:
        for v, w in graph.edges():
            graph[v][w]["weight"] = F(1)
        functions = [PieceVWF(F(0), (), ((F(0), F(1), F(0)),)) for _ in graph]
        arena = IntegralArena()
        try:
            PersistentForest(graph, functions, roots, arena)
        except AssertionError:
            counts["invalid_elimination_topologies_rejected"] += 1
        else:
            raise AssertionError("A nonforest eliminated incidence was silently discarded")
        work.update(arena.counts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started, rng, counts, work = time.monotonic(), random.Random(80293), Counter(), Counter()
    affine_aggregate_cases(args.full, rng, counts, work)
    invalid_topology_cases(counts, work)
    for _ in range(1000 if args.full else 40):
        arena = IntegralArena()
        original = random_function(rng)
        actual = IntegralVWF.from_pieces(arena, original)
        weight, lower = F(rng.randrange(1, 9), rng.randrange(1, 7)), -F(rng.randrange(0, 13), 4)
        lifted = actual.lift(weight, lower)
        reference = original.lift(weight, lower)
        certify_curve(lifted, reference, counts)
        other = random_function(rng, lower)
        addition = add_vwf(lifted, IntegralVWF.from_pieces(arena, other))
        certify_curve(addition, add_functions([reference, other], lower), counts)
        certify_curve(actual, original, counts)
        certify_curve(lifted, reference, counts)
        work.update(arena.counts)
        counts["scalar_Lift_addition_and_persistence_cases"] += 1
    max_n = 6 if args.full else 4
    trees = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_tree(g)]
    records = []
    for tree in trees:
        graph = tree.copy()
        for i, (v, w) in enumerate(graph.edges()):
            graph[v][w]["weight"] = F(1 + i % 5, 1 + (v + w) % 3)
        for root in graph:
            for profile in ["zero_lower", "signed_lower", "zero_total_tail"]:
                functions = [
                    random_function(rng, F(0) if profile == "zero_lower" else None) for _ in graph
                ]
                total = sum(f.pieces[-1][1] for f in functions)
                correction = -total if profile == "zero_total_tail" else max(F(0), 1 - total)
                old = functions[root]
                functions[root] = PieceVWF(
                    old.lower, old.splits, tuple((a, b + correction, c) for a, b, c in old.pieces)
                )
                arena = IntegralArena()
                forest = PersistentForest(graph, functions, [root], arena)
                forest.curves[root].export()
                values = forest.recover({root: forest.curves[root].minimum_point()})
                reference = ReferenceForest(graph, functions, [root], counts)
                for v in graph:
                    certify_curve(forest.curves[v], reference.curves[v], counts)
                    if v != root:
                        certify_curve(forest.lifted[v], reference.lifted[v], counts)
                energy, _ = certify_forest_solution(graph, functions, values, counts)
                assert energy == reference.curves[root].value(
                    reference.curves[root].minimum_point()
                )
                initial_points = sum(1 + len(f.splits) for f in functions)
                assert arena.counts["Lift_prefix_points_removed"] <= initial_points + len(graph) - 1
                mass = sum(len(f.splits) + 2 for f in functions)
                assert arena.counts["smaller_curve_points_streamed"] <= mass * mass.bit_length()
                counts["complete_persistent_tree_reconstructions"] += 1
                work.update(arena.counts)
                records.append(
                    {
                        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                        "root": root,
                        "profile": profile,
                        "mass": mass,
                        "solver_counts": dict(arena.counts),
                    }
                )
    retained_records = retained_root_cases(args.full, rng, counts, work)
    structured_records = structured_cases(args.full, counts, work)
    result = {
        "audit": "incremental_active_set_sdd.persistent_vwf_forest",
        "arithmetic": "exact fractions",
        "random_seed": 80293,
        "max_n": max_n,
        "input_family": "Generic signed-domain VWFs and weighted atlas trees, every root; zero and positive total terminal slopes",
        "alpha_eps_physical_seed": "not applicable: generic supplied forest primitive",
        "stopping_rule": "Exact root derivative minimum, one recovery and independent complete curve/original KKT checks",
        "scope": "Implemented persistent supplied-forest primitive; explicit piece curves and all KKT/aggregate certificates are validators. No recursive coarse solver or local OP3 theorem.",
        "audit_only": dict(counts),
        "solver_counts": dict(work),
        "tree_cases": records,
        "retained_root_cases": retained_records,
        "structured_cases": structured_records,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["persistent_affine_tree", "module_curve_removal", "vwf_forest_reference"]
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
