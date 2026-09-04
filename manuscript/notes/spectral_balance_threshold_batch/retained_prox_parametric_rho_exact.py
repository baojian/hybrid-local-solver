#!/usr/bin/env python3
"""Exact piecewise-affine rho audit of stopped masked input residuals.

For a fixed graph, acceleration root, and relative outer tolerance, every
quantity in the retained-prox recurrence is affine in the source threshold
fraction ``tau = d_v rho`` until a comparison changes outcome.  The comparison
outcomes therefore cut ``0 < tau < 1`` into rational intervals.  This script
traces those intervals with ``Fraction`` arithmetic and checks on each one that
every *executed* masked product has a nonnegative input residual on its face.

This is a finite small-graph certificate, not a graph-uniform proof.  Boundary
points between trace cells are harmless for this particular property: all max
and zero-residual insertions are continuous, while equality in the quarter
stopping test suppresses rather than creates the following product.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Affine:
    """The exact function ``slope * tau + intercept``."""

    slope: F = F(0)
    intercept: F = F(0)

    @staticmethod
    def coerce(value: Affine | F | int) -> Affine:
        return value if isinstance(value, Affine) else Affine(F(0), F(value))

    def at(self, tau: F) -> F:
        return self.slope * tau + self.intercept

    def __add__(self, other: Affine | F | int) -> Affine:
        other = self.coerce(other)
        return Affine(self.slope + other.slope, self.intercept + other.intercept)

    __radd__ = __add__

    def __neg__(self) -> Affine:
        return Affine(-self.slope, -self.intercept)

    def __sub__(self, other: Affine | F | int) -> Affine:
        return self + (-self.coerce(other))

    def __rsub__(self, other: Affine | F | int) -> Affine:
        return self.coerce(other) - self

    def __mul__(self, other: Affine | F | int) -> Affine:
        other = self.coerce(other)
        if self.slope and other.slope:
            raise TypeError("product of two nonconstant affine functions")
        if other.slope:
            return other * self.intercept
        return Affine(self.slope * other.intercept, self.intercept * other.intercept)

    __rmul__ = __mul__

    def __truediv__(self, other: Affine | F | int) -> Affine:
        other = self.coerce(other)
        if other.slope or not other.intercept:
            raise TypeError("division is only defined by a nonzero constant")
        return Affine(self.slope / other.intercept, self.intercept / other.intercept)


ZERO = Affine()


class TraceOracle:
    """Evaluate comparisons at one sample and retain their exact trace cell."""

    def __init__(self, sample: F, low: F, high: F):
        assert low < sample < high
        self.sample = sample
        self.low = low
        self.high = high
        self.comparisons = 0

    def _impose_positive(self, value: Affine, positive: bool) -> None:
        """Intersect with value >= 0 if positive, and value <= 0 otherwise."""
        if not value.slope:
            return
        root = -value.intercept / value.slope
        if (value.slope > 0) == positive:
            self.low = max(self.low, root)
        else:
            self.high = min(self.high, root)

    def gt(self, left: Affine | F | int, right: Affine | F | int = 0) -> bool:
        value = Affine.coerce(left) - right
        answer = value.at(self.sample) > 0
        self.comparisons += 1
        self._impose_positive(value, answer)
        return answer

    def ge(self, left: Affine | F | int, right: Affine | F | int = 0) -> bool:
        value = Affine.coerce(left) - right
        answer = value.at(self.sample) >= 0
        self.comparisons += 1
        self._impose_positive(value, answer)
        return answer

    def le(self, left: Affine | F | int, right: Affine | F | int = 0) -> bool:
        return self.ge(right, left)

    def maximum(self, values: list[Affine]) -> Affine:
        assert values
        best = values[0]
        for value in values[1:]:
            if self.gt(value, best):
                best = value
        return best


def connected(neighbors: list[set[int]]) -> bool:
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in neighbors[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(neighbors)


def configure(root: F) -> dict[str, F]:
    if not 0 < root <= 1:
        raise ValueError("root must lie in (0,1]")
    alpha = root * root / (2 - root * root)
    return {
        "alpha": alpha,
        "sigma": alpha,
        "diagonal": (1 + 3 * alpha) / 2,
        "coupling": (1 - alpha) / 2,
        "lipschitz": 1 + alpha,
        "gap": 2 * alpha,
        "root": root,
        "momentum": (1 - root) / (1 + root),
        "auxiliary_scale": (1 - root) / root,
    }


def audit_trace(
    neighbors: list[set[int]],
    sample: F,
    low: F,
    high: F,
    root: F,
    relative_width: F,
) -> dict[str, object]:
    """Audit one exact comparison cell containing ``sample``."""
    constants = configure(root)
    alpha = constants["alpha"]
    sigma = constants["sigma"]
    diagonal = constants["diagonal"]
    coupling = constants["coupling"]
    lipschitz = constants["lipschitz"]
    gap = constants["gap"]
    momentum = constants["momentum"]
    auxiliary_scale = constants["auxiliary_scale"]
    oracle = TraceOracle(sample, low, high)
    vertex_count = len(neighbors)
    degrees = [len(row) for row in neighbors]
    if not all(degrees):
        raise ValueError("graph must be connected and have at least two vertices")

    def apply(state: list[Affine], vertex: int, face: set[int] | None = None) -> Affine:
        active = range(vertex_count) if face is None else face
        answer = diagonal * state[vertex]
        answer -= coupling / degrees[vertex] * sum(
            (state[other] for other in neighbors[vertex] if other in active), ZERO
        )
        return answer

    def residual(load: list[Affine], state: list[Affine]) -> list[Affine]:
        return [load[i] - apply(state, i) for i in range(vertex_count)]

    tau = Affine(F(1), F(0))
    rho = tau / degrees[0]
    original_load = [-alpha * rho for _ in range(vertex_count)]
    original_load[0] += alpha / degrees[0]
    lower = [ZERO for _ in range(vertex_count)]
    certified = {0}
    width = (1 - tau) / degrees[0]
    target = relative_width * width
    phases = 0
    products = 0
    events = 0
    minimum_input: tuple[F, int, int, int, Affine] | None = None
    input_claims: list[tuple[int, int, int, Affine]] = []

    while oracle.gt(width, target):
        if phases >= 60:
            raise AssertionError("too many outer phases")
        old_lower = lower[:]
        old_width = width
        shifted_load = [original_load[i] + sigma * old_lower[i] for i in range(vertex_count)]
        current = old_lower[:]
        previous = old_lower[:]
        auxiliary = old_lower[:]

        for iteration in range(100):
            starting_extrapolate = [
                (current[i] + root * auxiliary[i]) / (1 + root)
                for i in range(vertex_count)
            ]

            # The enhanced chronology admits every exterior vertex whose input
            # residual is positive before executing the masked product.
            full_input = residual(shifted_load, starting_extrapolate)
            input_batch = {
                vertex
                for vertex in range(vertex_count)
                if vertex not in certified and oracle.gt(full_input[vertex])
            }
            if input_batch:
                certified.update(input_batch)
                events += 1
            face = set(certified)

            input_extrapolate = [ZERO for _ in range(vertex_count)]
            for vertex in face:
                input_extrapolate[vertex] = current[vertex] + momentum * (
                    current[vertex] - previous[vertex]
                )
            input_residuals = {
                vertex: shifted_load[vertex] - apply(input_extrapolate, vertex, face)
                for vertex in face
            }
            for vertex, value in input_residuals.items():
                sampled = value.at(sample)
                if minimum_input is None or sampled < minimum_input[0]:
                    minimum_input = (sampled, phases, iteration + 1, vertex, value)
                if sampled < 0:
                    # This comparison is an assertion, not algorithmic
                    # control, so it must not narrow the trace cell.
                    return {
                        "ok": False,
                        "sample": sample,
                        "cell_low": oracle.low,
                        "cell_high": oracle.high,
                        "phase": phases,
                        "product": iteration + 1,
                        "vertex": vertex,
                        "input_residual": value,
                        "input_residual_at_sample": sampled,
                    }
                input_claims.append((phases, iteration + 1, vertex, value))

            following = [ZERO for _ in range(vertex_count)]
            for vertex in face:
                following[vertex] = (
                    input_extrapolate[vertex] + input_residuals[vertex] / lipschitz
                )
            previous, current = current, following

            # Uniform lowerization and monotone publication envelope.
            shifts = [ZERO]
            ones = [Affine(F(0), F(1)) for _ in range(vertex_count)]
            for vertex in face:
                row_residual = shifted_load[vertex] - apply(current, vertex, face)
                direction = apply(ones, vertex, face)
                assert direction.intercept > 0 and not direction.slope
                shifts.append(-row_residual / direction.intercept)
            shift = oracle.maximum(shifts)
            for vertex in face:
                candidate = current[vertex] - shift
                lower[vertex] = oracle.maximum([lower[vertex], candidate, ZERO])

            next_auxiliary = [ZERO for _ in range(vertex_count)]
            for vertex in face:
                next_auxiliary[vertex] = current[vertex] + auxiliary_scale * (
                    current[vertex] - previous[vertex]
                )
                current[vertex] = oracle.maximum([current[vertex], lower[vertex]])
                next_auxiliary[vertex] = oracle.maximum(
                    [next_auxiliary[vertex], lower[vertex]]
                )
                previous[vertex] = current[vertex] - (
                    next_auxiliary[vertex] - current[vertex]
                ) / auxiliary_scale
            auxiliary = next_auxiliary
            products += 1

            # One simultaneous diagonal residual push on the old face.
            pre_push_residual = residual(shifted_load, lower)
            for vertex in face:
                if oracle.gt(pre_push_residual[vertex]):
                    lower[vertex] += pre_push_residual[vertex] / diagonal
            full_residual = residual(shifted_load, lower)
            for vertex in face:
                current[vertex] = oracle.maximum([current[vertex], lower[vertex]])
                auxiliary[vertex] = oracle.maximum([auxiliary[vertex], lower[vertex]])
                previous[vertex] = current[vertex] - (
                    auxiliary[vertex] - current[vertex]
                ) / auxiliary_scale

            # Maximal exact-positive exterior append closure.
            while True:
                batch = {
                    vertex
                    for vertex in range(vertex_count)
                    if vertex not in certified and oracle.gt(full_residual[vertex])
                }
                if not batch:
                    break
                events += 1
                for vertex in batch:
                    lower[vertex] += full_residual[vertex] / diagonal
                    current[vertex] = lower[vertex]
                    auxiliary[vertex] = lower[vertex]
                    previous[vertex] = lower[vertex]
                certified.update(batch)
                full_residual = residual(shifted_load, lower)

            inner_width = oracle.maximum(
                [ZERO] + [value / gap for value in full_residual]
            )
            if oracle.le(inner_width, old_width / 4):
                width = old_width / 2 + inner_width
                break
        else:
            raise AssertionError("phase exceeded 100 products")
        phases += 1

    # Certify each claim at both endpoints of the trace cell.  The assertions
    # themselves never participated in constructing this cell.
    for phase, product, vertex, value in input_claims:
        endpoint_minimum = min(value.at(oracle.low), value.at(oracle.high))
        if endpoint_minimum < 0:
            return {
                "ok": False,
                "sample": sample,
                "cell_low": oracle.low,
                "cell_high": oracle.high,
                "phase": phase,
                "product": product,
                "vertex": vertex,
                "input_residual": value,
                "input_residual_at_sample": value.at(sample),
                "input_residual_at_cell_minimum": endpoint_minimum,
            }
    assert oracle.low <= sample <= oracle.high
    return {
        "ok": True,
        "sample": sample,
        "cell_low": max(low, oracle.low),
        "cell_high": min(high, oracle.high),
        "phases": phases,
        "products": products,
        "events": events,
        "comparisons": oracle.comparisons,
        "minimum_input": minimum_input,
    }


def audit_interval(
    neighbors: list[set[int]],
    root: F,
    relative_width: F,
    maximum_cells: int,
) -> dict[str, object]:
    """Cover the open unit interval by exact trace cells."""
    pending = [(F(0), F(1))]
    cells = 0
    products = 0
    comparisons = 0
    minimum_input: tuple[F, F, int, int, int, Affine] | None = None
    while pending:
        low, high = pending.pop()
        if not low < high:
            continue
        sample = (low + high) / 2
        result = audit_trace(neighbors, sample, low, high, root, relative_width)
        if not result["ok"]:
            return {"ok": False, "cells": cells, "witness": result}
        cell_low = result["cell_low"]
        cell_high = result["cell_high"]
        assert cell_low <= sample <= cell_high
        if cell_low == cell_high:
            # A sampled comparison root can select a zero-width trace.  A
            # one-third sample selects an adjacent full-dimensional trace.
            sample = (2 * low + high) / 3
            result = audit_trace(neighbors, sample, low, high, root, relative_width)
            if not result["ok"]:
                return {"ok": False, "cells": cells, "witness": result}
            cell_low = result["cell_low"]
            cell_high = result["cell_high"]
            assert cell_low < cell_high
        cells += 1
        products += int(result["products"])
        comparisons += int(result["comparisons"])
        local_minimum = result["minimum_input"]
        if local_minimum is not None:
            candidate = (local_minimum[0], sample, *local_minimum[1:])
            if minimum_input is None or candidate[0] < minimum_input[0]:
                minimum_input = candidate
        if cells > maximum_cells:
            raise AssertionError(f"trace partition exceeded {maximum_cells} cells")
        if low < cell_low:
            pending.append((low, cell_low))
        if cell_high < high:
            pending.append((cell_high, high))
    return {
        "ok": True,
        "cells": cells,
        "trace_products": products,
        "comparisons": comparisons,
        "minimum_input": minimum_input,
    }


def fraction_json(value: object) -> object:
    if isinstance(value, F):
        return str(value)
    if isinstance(value, Affine):
        return {"slope": str(value.slope), "intercept": str(value.intercept)}
    if isinstance(value, tuple):
        return [fraction_json(item) for item in value]
    if isinstance(value, dict):
        return {key: fraction_json(item) for key, item in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=3, choices=(2, 3, 4, 5))
    parser.add_argument("--root", default="3/10")
    parser.add_argument("--relative-width", default="1/32")
    parser.add_argument("--maximum-cells", type=int, default=20000)
    args = parser.parse_args()
    vertex_count = args.vertices
    root = F(args.root)
    relative_width = F(args.relative_width)
    edges = list(itertools.combinations(range(vertex_count), 2))
    graph_count = 0
    total_cells = 0
    total_products = 0
    total_comparisons = 0
    global_minimum: tuple[object, ...] | None = None
    maximum_cells = 0

    for edge_mask in range(1 << len(edges)):
        neighbors = [set() for _ in range(vertex_count)]
        selected_edges: list[tuple[int, int]] = []
        for index, (left, right) in enumerate(edges):
            if edge_mask & (1 << index):
                neighbors[left].add(right)
                neighbors[right].add(left)
                selected_edges.append((left, right))
        if not connected(neighbors):
            continue
        result = audit_interval(neighbors, root, relative_width, args.maximum_cells)
        graph_count += 1
        if not result["ok"]:
            print(
                json.dumps(
                    fraction_json(
                        {
                            "status": "counterexample",
                            "vertices": vertex_count,
                            "edges": selected_edges,
                            **result,
                        }
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
            raise SystemExit(1)
        total_cells += int(result["cells"])
        total_products += int(result["trace_products"])
        total_comparisons += int(result["comparisons"])
        maximum_cells = max(maximum_cells, int(result["cells"]))
        local_minimum = result["minimum_input"]
        if local_minimum is not None:
            candidate = (*local_minimum, selected_edges)
            if global_minimum is None or candidate[0] < global_minimum[0]:
                global_minimum = candidate

    print(
        json.dumps(
            fraction_json(
                {
                    "status": "pass",
                    "vertices": vertex_count,
                    "root": root,
                    "relative_width": relative_width,
                    "graphs": graph_count,
                    "trace_cells": total_cells,
                    "maximum_cells_per_graph": maximum_cells,
                    "trace_products": total_products,
                    "comparisons": total_comparisons,
                    "minimum_input": global_minimum,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
