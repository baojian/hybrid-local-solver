#!/usr/bin/env python3
"""Exact stop to using chronological flux alone for the input-cone proof.

The three-vertex path is written in degree coordinates.  The starting
residual is a nonnegative chronological-flux residual from two batches, but
it is not asserted to be reachable from the canonical point-source outer
history.  One retained-prox product leaves residual width above one quarter
while the following input residual is negative.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


def fraction_json(values: list[F] | F) -> list[str] | str:
    if isinstance(values, list):
        return [str(value) for value in values]
    return str(values)


def main() -> None:
    root = F(1, 10)
    beta = (1 - root * root) / 2
    diagonal = 1 - beta
    momentum = (1 - root) / (1 + root)
    coupling_scale = root / (1 + root)
    neighbors = [{2}, {2}, {0, 1}]
    degrees = [1, 1, 2]

    def coupling(vector: list[F]) -> list[F]:
        return [
            sum((beta * vector[j] / degrees[i] for j in neighbors[i]), F(0))
            for i in range(3)
        ]

    def retained(vector: list[F]) -> list[F]:
        mixed = coupling(vector)
        return [beta * vector[i] + mixed[i] for i in range(3)]

    def shifted_operator(vector: list[F]) -> list[F]:
        mixed = coupling(vector)
        return [diagonal * vector[i] - mixed[i] for i in range(3)]

    # Batch times (1,0,0) and nonnegative diagonal increments below give
    # r_i=sum_{j:time(j)>=time(i)} K_ij u_j exactly.
    batch_times = [1, 0, 0]
    increments = [F(20, 99), F(20, 99), F(200, 99)]
    residual = []
    for i in range(3):
        residual.append(
            sum(
                (
                    beta * increments[j] / degrees[i]
                    for j in neighbors[i]
                    if batch_times[j] >= batch_times[i]
                ),
                F(0),
            )
        )
    assert residual == [F(0), F(1), F(1, 10)]

    push = [value / diagonal for value in retained(residual)]
    post_push_residual = coupling(push)
    next_momentum = [
        max(F(0), momentum * residual[i] - coupling_scale * push[i])
        for i in range(3)
    ]
    operator_momentum = shifted_operator(next_momentum)
    next_input_residual = [
        post_push_residual[i] - operator_momentum[i] for i in range(3)
    ]

    assert max(post_push_residual) > F(1, 4) * max(residual)
    assert next_input_residual[1] < 0
    print(
        json.dumps(
            {
                "status": "counterexample",
                "scope": "chronological-flux cone only; not canonical reachability",
                "root": fraction_json(root),
                "beta": fraction_json(beta),
                "diagonal": fraction_json(diagonal),
                "batch_times": batch_times,
                "increments": fraction_json(increments),
                "input_residual": fraction_json(residual),
                "push": fraction_json(push),
                "post_push_residual": fraction_json(post_push_residual),
                "next_momentum": fraction_json(next_momentum),
                "next_input_residual": fraction_json(next_input_residual),
                "quarter_threshold": fraction_json(max(residual) / 4),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
