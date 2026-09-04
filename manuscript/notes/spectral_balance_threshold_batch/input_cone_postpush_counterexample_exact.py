#!/usr/bin/env python3
"""Exact obstruction to proving InputCone from the post-push cone alone.

The graph is a universal hub joined to one leaf and to a six-vertex clique.
At s=1/100, a nonnegative residual in the one-step post-push cone produces a
negative next NAG input residual while the quarter-width rule still executes.
This is not asserted to be a complete zero-start retained-prox history.
"""

from __future__ import annotations

import json
from fractions import Fraction


Rational = Fraction
Vector = list[Rational]
Matrix = list[Vector]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum((entry * value for entry, value in zip(row, vector, strict=True)), Rational())
        for row in matrix
    ]


def add(left: Vector, right: Vector) -> Vector:
    return [x + y for x, y in zip(left, right, strict=True)]


def scale(factor: Rational, vector: Vector) -> Vector:
    return [factor * value for value in vector]


def main() -> None:
    vertices = 8
    hub = 0
    leaf = 1
    core = tuple(range(2, vertices))
    edges = [(hub, index) for index in range(1, vertices)]
    edges.extend(
        (left, right)
        for offset, left in enumerate(core)
        for right in core[offset + 1 :]
    )
    adjacency = [[Rational() for _ in range(vertices)] for _ in range(vertices)]
    for left, right in edges:
        adjacency[left][right] = Rational(1)
        adjacency[right][left] = Rational(1)
    degrees = [sum(row) for row in adjacency]

    root = Rational(1, 100)
    diagonal = (1 + root**2) / 2
    coupling = (1 - root**2) / 2
    theta = (1 - root) / (1 + root)
    kappa = root / (1 + root)
    walk = [
        [adjacency[row][column] / degrees[row] for column in range(vertices)]
        for row in range(vertices)
    ]
    identity = [
        [Rational(row == column) for column in range(vertices)]
        for row in range(vertices)
    ]
    off_diagonal = [scale(coupling, row) for row in walk]
    remainder = [
        add(scale(1 - diagonal, identity[row]), off_diagonal[row])
        for row in range(vertices)
    ]
    normalized_matrix = [
        add(scale(diagonal, identity[row]), scale(-1, off_diagonal[row]))
        for row in range(vertices)
    ]

    prior_residual = [Rational(index == hub) for index in range(vertices)]
    prior_push = scale(1 / diagonal, matvec(remainder, prior_residual))
    raw_residual = matvec(off_diagonal, prior_push)
    normalizer = max(raw_residual)
    residual = scale(1 / normalizer, raw_residual)

    push = scale(1 / diagonal, matvec(remainder, residual))
    post_push_residual = matvec(off_diagonal, push)
    momentum = [
        max(theta * value - kappa * pushed, Rational())
        for value, pushed in zip(residual, push, strict=True)
    ]
    next_input = [
        value - correction
        for value, correction in zip(
            post_push_residual,
            matvec(normalized_matrix, momentum),
            strict=True,
        )
    ]

    assert residual[hub] == Rational(2, 7)
    assert residual[leaf] == 1
    assert all(residual[index] == Rational(11, 36) for index in core)
    assert all(value > 0 for value in momentum)
    assert max(post_push_residual) - Rational(1, 4) == Rational(
        4007369027, 39203920000
    )
    assert next_input[leaf] == Rational(-33165, 16161616)
    assert all(next_input[index] > 0 for index in range(vertices) if index != leaf)

    def strings(vector: Vector) -> list[str]:
        return [str(value) for value in vector]

    print(
        json.dumps(
            {
                "vertices": vertices,
                "edges": edges,
                "root": str(root),
                "diagonal": str(diagonal),
                "coupling": str(coupling),
                "prior_residual": strings(prior_residual),
                "post_push_cone_residual": strings(residual),
                "current_push": strings(push),
                "post_push_residual": strings(post_push_residual),
                "momentum": strings(momentum),
                "next_input_residual": strings(next_input),
                "quarter_rule_margin": str(
                    max(post_push_residual) - Rational(1, 4)
                ),
                "negative_leaf_input": str(next_input[leaf]),
                "scope": (
                    "post-push-cone obstruction only; not a complete "
                    "zero-start retained-prox history"
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
