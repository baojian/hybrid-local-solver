"""Exact piece reference for signed-domain VWF Lift and valid forest passes.

The explicit curves are validators, not the claimed fast persistent engine.
All Lift constants are obtained by direct quadratic minimization.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
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

from bounded_vwf_compression import VWF
import networkx as nx


def polynomial_value(p, x):
    a, b, c = p
    return a * x * x + b * x + c


def compose_polynomial(p, slope, intercept):
    a, b, c = p
    return a * slope**2, 2 * a * slope * intercept + b * slope, a * intercept**2 + b * intercept + c


@dataclass(frozen=True)
class PieceVWF:
    lower: F
    splits: tuple
    pieces: tuple

    @classmethod
    def from_atoms(cls, vwf):
        splits, pieces = vwf.polynomials()
        return cls(vwf.lower, tuple(splits), tuple(pieces))

    def piece(self, x):
        assert x >= self.lower
        return self.pieces[bisect_right(self.splits, x)]

    def value(self, x):
        return polynomial_value(self.piece(x), x)

    def derivative(self, x):
        a, b, _ = self.piece(x)
        return 2 * a * x + b

    def lift(self, weight, parent_lower):
        assert weight > 0 and parent_lower <= 0
        first = self.lower + self.derivative(self.lower) / weight
        splits = [first] + [s + self.derivative(s) / weight for s in self.splits]
        pieces = [
            (weight / 2, -weight * self.lower, self.value(self.lower) + weight * self.lower**2 / 2)
        ]
        for a, b, c in self.pieces:
            denominator = weight + 2 * a
            pieces.append(
                (weight * a / denominator, weight * b / denominator, c - b * b / (2 * denominator))
            )
        assert all(a < b for a, b in zip(splits, splits[1:]))
        start = bisect_right(splits, parent_lower)
        return PieceVWF(parent_lower, tuple(splits[start:]), tuple(pieces[start:]))

    def minimum_point(self):
        assert self.pieces[-1][0] == 0 and self.pieces[-1][1] >= 0
        if self.derivative(self.lower) >= 0:
            return self.lower
        for index, p in enumerate(self.pieces):
            lo = self.lower if index == 0 else self.splits[index - 1]
            hi = self.splits[index] if index < len(self.splits) else None
            if p[0] > 0:
                root = -p[1] / (2 * p[0])
                if root >= lo and (hi is None or root <= hi):
                    return root
            elif p[1] == 0:
                return lo
        raise AssertionError("A finite VWF minimum was not located")


def add_functions(functions, lower):
    assert functions and all(f.lower <= lower for f in functions)
    splits = sorted({s for f in functions for s in f.splits if s > lower})
    pieces = []
    for x in [lower] + splits:
        pieces.append(tuple(sum((f.piece(x)[i] for f in functions), F(0)) for i in range(3)))
    return PieceVWF(lower, tuple(splits), tuple(pieces))


def certify_function(f, counts):
    assert f.lower <= 0 and f.value(F(0)) <= 0
    assert len(f.pieces) == len(f.splits) + 1
    assert all(s > f.lower for s in f.splits)
    assert all(a < b for a, b in zip(f.splits, f.splits[1:]))
    assert f.pieces[-1][0] == 0
    assert all(p[0] >= 0 for p in f.pieces)
    assert all(p[0] >= q[0] for p, q in zip(f.pieces, f.pieces[1:]))
    for s, p, q in zip(f.splits, f.pieces, f.pieces[1:]):
        assert polynomial_value(p, s) == polynomial_value(q, s)
        assert 2 * p[0] * s + p[1] == 2 * q[0] * s + q[1]
        counts["reference_continuous_value_and_derivative_boundaries"] += 1
    assert all(isinstance(t, F) for p in f.pieces for t in p)
    counts["reference_valid_VWFs"] += 1


def certify_lift(f, weight, lifted, counts):
    """Full polynomial identities and minimizer KKT on every entire interval."""
    certify_function(lifted, counts)
    boundary = f.lower + f.derivative(f.lower) / weight
    source_starts = [boundary] + [s + f.derivative(s) / weight for s in f.splits]
    for index, p in enumerate(lifted.pieces):
        lo = lifted.lower if index == 0 else lifted.splits[index - 1]
        hi = lifted.splits[index] if index < len(lifted.splits) else None
        source_index = bisect_right(source_starts, lo) - 1
        if source_index < 0:
            sy, ty = F(0), f.lower
            original = f.pieces[0]
            assert hi is not None and hi <= boundary
            # The boundary stationarity residual decreases linearly to zero.
            assert weight * (f.lower - hi) + f.derivative(f.lower) >= 0
            counts["reference_complete_boundary_Lift_pieces"] += 1
        else:
            original = f.pieces[source_index]
            a, b, _ = original
            sy, ty = weight / (weight + 2 * a), -b / (weight + 2 * a)
            original_lo = f.lower if source_index == 0 else f.splits[source_index - 1]
            original_hi = f.splits[source_index] if source_index < len(f.splits) else None
            assert sy * lo + ty >= original_lo
            if hi is not None:
                assert original_hi is None or sy * hi + ty <= original_hi
            else:
                assert original_hi is None
            assert weight * (sy - 1) + 2 * a * sy == 0
            assert weight * ty + 2 * a * ty + b == 0
            counts["reference_complete_interior_Lift_pieces"] += 1
        vertex = compose_polynomial(original, sy, ty)
        edge = weight * (1 - sy) ** 2 / 2, -weight * (1 - sy) * ty, weight * ty**2 / 2
        assert tuple(a + b for a, b in zip(vertex, edge)) == p
        # y=x-g_lift(x)/weight as a complete affine identity.
        assert sy == 1 - 2 * p[0] / weight and ty == -p[1] / weight
        counts["reference_complete_Lift_constant_and_recovery_identities"] += 1
    assert lifted.pieces[-1][1] == f.pieces[-1][1]


def random_function(rng, lower=None, constant_shift=F(0)):
    lower = -F(rng.randrange(0, 9), 3) if lower is None else lower
    possible = [lower + F(k, 3) for k in range(1, 22)]
    splits = sorted(rng.sample(possible, rng.randrange(0, 7)))
    atoms = tuple((s, F(rng.randrange(1, 9), rng.randrange(1, 7))) for s in splits)
    return PieceVWF.from_atoms(
        VWF(lower, -F(rng.randrange(0, 6), 3) + constant_shift, F(rng.randrange(-8, 7), 3), atoms)
    )


class ReferenceForest:
    def __init__(self, graph, functions, roots, counts):
        self.graph, self.functions, self.roots = graph, functions, tuple(roots)
        n = len(graph)
        self.parent, self.order = [-2] * n, []
        for root in self.roots:
            assert self.parent[root] == -2
            self.parent[root] = -1
            self.order.append(root)
            cursor = len(self.order) - 1
            while cursor < len(self.order):
                v = self.order[cursor]
                for w in graph[v]:
                    if w == self.parent[v] or w in self.roots:
                        continue
                    assert self.parent[w] == -2, "Only root-to-root nonforest edges are legal"
                    self.parent[w] = v
                    self.order.append(w)
                cursor += 1
        assert len(self.order) == n
        self.curves, self.lifted = {}, {}
        for v in reversed(self.order):
            parts = [functions[v]] + [self.lifted[w] for w in graph[v] if self.parent[w] == v]
            curve = add_functions(parts, functions[v].lower)
            certify_function(curve, counts)
            self.curves[v] = curve
            if self.parent[v] >= 0:
                c = graph[v][self.parent[v]]["weight"]
                lifted = curve.lift(c, functions[self.parent[v]].lower)
                certify_lift(curve, c, lifted, counts)
                self.lifted[v] = lifted

    def recover(self, root_values):
        values = dict(root_values)
        for v in self.order:
            if self.parent[v] >= 0:
                p = self.parent[v]
                c = self.graph[v][p]["weight"]
                values[v] = values[p] - self.lifted[v].derivative(values[p]) / c
        return [values[v] for v in range(len(self.graph))]


def certify_forest_solution(graph, functions, values, counts, retained=()):
    gradients = [f.derivative(x) for f, x in zip(functions, values)]
    energy = sum((f.value(x) for f, x in zip(functions, values)), F(0))
    for v, w, data in graph.edges(data=True):
        c = data["weight"]
        flow = c * (values[v] - values[w])
        gradients[v] += flow
        gradients[w] -= flow
        energy += c * (values[v] - values[w]) ** 2 / 2
    for v, (f, x, g) in enumerate(zip(functions, values, gradients)):
        assert x >= f.lower
        if v not in retained:
            assert g >= 0 and (x == f.lower or g == 0)
        counts["original_vertex_KKT_certificates"] += v not in retained
    return energy, gradients


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, rng, counts = time.monotonic(), random.Random(80291), Counter()
    for _ in range(3000 if args.full else 100):
        f = random_function(rng)
        certify_function(f, counts)
        weight = F(rng.randrange(1, 10), rng.randrange(1, 7))
        parent_lower = -F(rng.randrange(0, 13), 4)
        certify_lift(f, weight, f.lift(weight, parent_lower), counts)
        counts["scalar_Lift_cases"] += 1
    witness = PieceVWF(F(0), (), ((F(0), -F(1), F(0)),))
    assert witness.lift(F(1), F(0)).value(F(0)) == -F(1, 2)
    counts["printed_Lift_sign_counterexamples"] += 1
    records = []
    max_n = 6 if args.full else 4
    trees = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_tree(g)]
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
                forest = ReferenceForest(graph, functions, [root], counts)
                xroot = forest.curves[root].minimum_point()
                values = forest.recover({root: xroot})
                energy, _ = certify_forest_solution(graph, functions, values, counts)
                assert energy == forest.curves[root].value(xroot)
                positive_tail = sum(max(F(0), f.pieces[-1][1]) for f in functions)
                upper = max([F(0)] + [s for f in functions for s in f.splits])
                floor = min(data["weight"] for _, _, data in graph.edges(data=True))
                bound = upper + len(graph) * positive_tail / floor
                for v, curve in forest.curves.items():
                    children = [w for w in graph[v] if forest.parent[w] == v]
                    assert 2 * curve.pieces[0][0] <= 2 * functions[v].pieces[0][0] + sum(
                        graph[v][w]["weight"] for w in children
                    )
                    assert energy <= curve.value(F(0)) <= 0
                    assert all(s <= bound for s in curve.splits)
                    counts["forest_curvature_constant_and_range_certificates"] += 1
                for curve in forest.lifted.values():
                    assert energy <= curve.value(F(0)) <= 0
                    assert all(s <= bound for s in curve.splits)
                counts["complete_tree_reconstructions"] += 1
                counts["zero_total_tail_tree_reconstructions"] += profile == "zero_total_tail"
                records.append(
                    {
                        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                        "root": root,
                        "profile": profile,
                        "input_events": sum(len(f.splits) for f in functions),
                        "maximum_retained_events": max(
                            len(f.splits) for f in forest.curves.values()
                        ),
                    }
                )
    result = {
        "audit": "incremental_active_set_sdd.vwf_forest_reference",
        "arithmetic": "exact fractions",
        "random_seed": 80291,
        "max_n": max_n,
        "input_family": "Convex VWFs with concave derivatives, signed lower endpoints and terminal slopes; weighted atlas trees, every root; zero total terminal slopes",
        "alpha_eps_physical_seed": "not applicable: generic supplied VWF forest primitive",
        "stopping_rule": "Exact root derivative minimum and one downward recovery; complete Lift polynomial identities and original KKT",
        "scope": "Explicit reference validators, not a fast persistent engine or local OP3 solver",
        "audit_only": dict(counts),
        "tree_cases": records,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "bounded_vwf_compression": hashlib.sha256(
                Path(__file__).with_name("bounded_vwf_compression.py").read_bytes()
            ).hexdigest()
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
