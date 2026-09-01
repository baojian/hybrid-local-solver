#!/usr/bin/env python3
"""Fraction-exact finite audit of the stopped two-push fixed-face route.

The audit enumerates every connected labelled simple graph on four vertices
and every nonzero binary initial residual.  Both recurrences are initialized
at zero on the supplied full face.  The masked recurrence performs two
simultaneous positive-residual diagonal pushes after each retracted NAG
product; the omniscient recurrence is unpushed.  We check only products that
are actually executed before the masked residual first crosses one quarter
of its initial maximum.

This is a deterministic finite audit, not a graph-uniform theorem.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction as F


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


def minimum(
    record: dict[str, object] | None,
    value: F,
    witness: dict[str, object],
) -> dict[str, object]:
    if record is None or value < record["value"]:
        return {"value": value, **witness}
    return record


def audit(
    neighbors: list[set[int]],
    initial_residual: tuple[F, ...],
    root: F,
    maximum_products: int,
) -> dict[str, object]:
    size = len(neighbors)
    alpha = root * root / (2 - root * root)
    diagonal = (1 + 3 * alpha) / 2
    coupling = (1 - alpha) / 2
    lipschitz = 1 + alpha
    momentum = (1 - root) / (1 + root)
    auxiliary_scale = (1 - root) / root
    degrees = [len(row) for row in neighbors]
    matrix = [[F(0) for _ in range(size)] for _ in range(size)]
    for vertex in range(size):
        matrix[vertex][vertex] = diagonal
        for neighbor in neighbors[vertex]:
            matrix[vertex][neighbor] = -coupling / degrees[vertex]

    def matvec(vector: list[F]) -> list[F]:
        return [sum(matrix[i][j] * vector[j] for j in range(size)) for i in range(size)]

    def residual(vector: list[F]) -> list[F]:
        applied = matvec(vector)
        return [initial_residual[i] - applied[i] for i in range(size)]

    direction = matvec([F(1) for _ in range(size)])
    assert all(value == 2 * alpha for value in direction)

    def advance(
        current: list[F],
        previous: list[F],
        lower: list[F],
    ) -> tuple[list[F], list[F], list[F], list[F], F]:
        extrapolate = [current[i] + momentum * (current[i] - previous[i]) for i in range(size)]
        input_residual = residual(extrapolate)
        following = [extrapolate[i] + input_residual[i] / lipschitz for i in range(size)]
        old_current = current
        current = following
        raw_residual = residual(current)
        shift = max([F(0)] + [-raw_residual[i] / direction[i] for i in range(size)])
        lower = [max(lower[i], current[i] - shift, F(0)) for i in range(size)]
        auxiliary = [
            current[i] + auxiliary_scale * (current[i] - old_current[i]) for i in range(size)
        ]
        current = [max(current[i], lower[i]) for i in range(size)]
        auxiliary = [max(auxiliary[i], lower[i]) for i in range(size)]
        previous = [current[i] - (auxiliary[i] - current[i]) / auxiliary_scale for i in range(size)]
        return current, previous, lower, auxiliary, min(raw_residual)

    zero = [F(0) for _ in range(size)]
    lower = zero[:]
    current = zero[:]
    previous = zero[:]
    omniscient_lower = zero[:]
    omniscient_current = zero[:]
    omniscient_previous = zero[:]
    extrema: dict[str, dict[str, object] | None] = {
        "executed_temporal_lead": None,
        "same_time_lower_gap": None,
        "same_time_extrapolate_gap": None,
        "masked_raw_residual": None,
    }
    threshold = max(initial_residual) / 4

    for product in range(1, maximum_products + 1):
        starting_lower = lower[:]
        (
            current,
            previous,
            lower,
            auxiliary,
            raw_residual_minimum,
        ) = advance(current, previous, lower)
        (
            omniscient_current,
            omniscient_previous,
            omniscient_lower,
            omniscient_auxiliary,
            _,
        ) = advance(
            omniscient_current,
            omniscient_previous,
            omniscient_lower,
        )

        witness = {"product": product}
        extrema["masked_raw_residual"] = minimum(
            extrema["masked_raw_residual"],
            raw_residual_minimum,
            witness,
        )
        if product > 1:
            gaps = [starting_lower[i] - omniscient_lower[i] for i in range(size)]
            vertex = min(range(size), key=gaps.__getitem__)
            extrema["executed_temporal_lead"] = minimum(
                extrema["executed_temporal_lead"],
                gaps[vertex],
                {**witness, "vertex": vertex},
            )

        for _ in range(2):
            lower_residual = residual(lower)
            increment = [max(lower_residual[i], F(0)) / diagonal for i in range(size)]
            lower = [lower[i] + increment[i] for i in range(size)]
            current = [max(current[i], lower[i]) for i in range(size)]
            auxiliary = [max(auxiliary[i], lower[i]) for i in range(size)]
            previous = [
                current[i] - (auxiliary[i] - current[i]) / auxiliary_scale for i in range(size)
            ]

        lower_gaps = [lower[i] - omniscient_lower[i] for i in range(size)]
        lower_vertex = min(range(size), key=lower_gaps.__getitem__)
        extrema["same_time_lower_gap"] = minimum(
            extrema["same_time_lower_gap"],
            lower_gaps[lower_vertex],
            {**witness, "vertex": lower_vertex},
        )
        masked_extrapolate = [(current[i] + root * auxiliary[i]) / (1 + root) for i in range(size)]
        omniscient_extrapolate = [
            (omniscient_current[i] + root * omniscient_auxiliary[i]) / (1 + root)
            for i in range(size)
        ]
        extrapolate_gaps = [masked_extrapolate[i] - omniscient_extrapolate[i] for i in range(size)]
        extrapolate_vertex = min(range(size), key=extrapolate_gaps.__getitem__)
        extrema["same_time_extrapolate_gap"] = minimum(
            extrema["same_time_extrapolate_gap"],
            extrapolate_gaps[extrapolate_vertex],
            {**witness, "vertex": extrapolate_vertex},
        )

        post_residual = residual(lower)
        if max([F(0)] + post_residual) <= threshold:
            return {"products": product, "extrema": extrema}

    raise AssertionError("quarter-residual stop was not reached")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", default="1/2,1/10,1/50")
    parser.add_argument("--levels", default="0,1")
    parser.add_argument("--maximum-products", type=int, default=300)
    args = parser.parse_args()
    roots = tuple(F(value) for value in args.roots.split(","))
    levels = tuple(F(value) for value in args.levels.split(","))
    if F(0) not in levels or max(levels) != 1 or min(levels) < 0:
        raise ValueError("levels must be nonnegative, include 0, and have max 1")
    size = 4
    edges = tuple(itertools.combinations(range(size), 2))
    profiles = tuple(
        tuple(F(value) for value in values)
        for values in itertools.product(levels, repeat=size)
        if any(values)
    )
    global_extrema: dict[str, dict[str, object] | None] = {
        "executed_temporal_lead": None,
        "same_time_lower_gap": None,
        "same_time_extrapolate_gap": None,
        "masked_raw_residual": None,
    }
    graphs = 0
    runs = 0
    maximum_products = 0
    for mask in range(1 << len(edges)):
        neighbors = [set() for _ in range(size)]
        selected_edges = []
        for bit, (left, right) in enumerate(edges):
            if mask & (1 << bit):
                neighbors[left].add(right)
                neighbors[right].add(left)
                selected_edges.append((left, right))
        if not connected(neighbors):
            continue
        graphs += 1
        for root in roots:
            for profile in profiles:
                result = audit(
                    neighbors,
                    profile,
                    root,
                    args.maximum_products,
                )
                runs += 1
                maximum_products = max(maximum_products, result["products"])
                for name, record in result["extrema"].items():
                    if record is None:
                        continue
                    global_extrema[name] = minimum(
                        global_extrema[name],
                        record["value"],
                        {
                            "root": root,
                            "edges": tuple(selected_edges),
                            "initial_residual": profile,
                            **{k: v for k, v in record.items() if k != "value"},
                        },
                    )

    for name in (
        "executed_temporal_lead",
        "same_time_lower_gap",
        "same_time_extrapolate_gap",
        "masked_raw_residual",
    ):
        record = global_extrema[name]
        if record is not None:
            assert record["value"] >= 0, (name, record)

    def encode(value: object) -> object:
        if isinstance(value, F):
            return str(value)
        if isinstance(value, tuple):
            return [encode(item) for item in value]
        return value

    print(
        json.dumps(
            {
                "warning": "finite Fraction-exact audit, not a theorem",
                "vertices": size,
                "connected_graphs": graphs,
                "residual_profiles_per_graph": len(profiles),
                "residual_levels": [str(level) for level in levels],
                "roots": [str(root) for root in roots],
                "runs": runs,
                "maximum_products": maximum_products,
                "minimum_exact_margins": {
                    name: {key: encode(value) for key, value in record.items()}
                    if record is not None
                    else None
                    for name, record in global_extrema.items()
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
