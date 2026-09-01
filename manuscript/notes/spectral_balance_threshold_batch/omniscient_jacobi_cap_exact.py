#!/usr/bin/env python3
"""Exact canonical stop for a one-Jacobi omniscient-envelope cap.

On the two-vertex unit edge, alpha=1/7 makes the retained NAG root exactly
1/2.  Starting from zero with the canonical single-source load at rho=1/10,
the fourth retracted omniscient lower envelope exceeds one positive-residual
Jacobi push from the preceding envelope by exactly 1/3200 in both rows.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


def matvec(matrix: tuple[tuple[F, ...], ...], vector: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        for row in range(len(vector))
    )


def main() -> None:
    alpha = F(1, 7)
    rho = F(1, 10)
    root = F(1, 2)
    lipschitz = 1 + alpha
    momentum = (1 - root) / (1 + root)
    auxiliary_scale = (1 - root) / root
    matrix = ((F(5, 7), F(-3, 7)), (F(-3, 7), F(5, 7)))
    load = (alpha * (1 - rho), -alpha * rho)
    direction = matvec(matrix, (F(1), F(1)))

    current = (F(0), F(0))
    previous = current
    lower = current
    records = []

    for iteration in range(1, 5):
        starting_lower = lower
        starting_residual = tuple(
            load[i] - matvec(matrix, starting_lower)[i] for i in range(2)
        )
        jacobi_cap = tuple(
            starting_lower[i]
            + max(starting_residual[i], F(0)) / matrix[i][i]
            for i in range(2)
        )

        extrapolate = tuple(
            current[i] + momentum * (current[i] - previous[i])
            for i in range(2)
        )
        product = matvec(matrix, extrapolate)
        next_current = tuple(
            extrapolate[i] + (load[i] - product[i]) / lipschitz
            for i in range(2)
        )
        previous, current = current, next_current

        current_residual = tuple(
            load[i] - matvec(matrix, current)[i] for i in range(2)
        )
        shift = max(
            F(0),
            *(-current_residual[i] / direction[i] for i in range(2)),
        )
        candidate = tuple(current[i] - shift for i in range(2))
        lower = tuple(max(lower[i], candidate[i], F(0)) for i in range(2))

        auxiliary = tuple(
            current[i] + auxiliary_scale * (current[i] - previous[i])
            for i in range(2)
        )
        current = tuple(max(current[i], lower[i]) for i in range(2))
        auxiliary = tuple(max(auxiliary[i], lower[i]) for i in range(2))
        previous = tuple(
            current[i] - (auxiliary[i] - current[i]) / auxiliary_scale
            for i in range(2)
        )

        gap = tuple(lower[i] - jacobi_cap[i] for i in range(2))
        records.append(
            {
                "iteration": iteration,
                "lower": [str(value) for value in lower],
                "one_jacobi_cap": [str(value) for value in jacobi_cap],
                "lower_minus_cap": [str(value) for value in gap],
            }
        )

    assert records[-1]["lower_minus_cap"] == ["1/3200", "1/3200"]
    print(
        json.dumps(
            {
                "graph": "two vertices joined by one unit edge",
                "alpha": str(alpha),
                "rho": str(rho),
                "retained_root": str(root),
                "records": records,
                "conclusion": (
                    "OneJacobiEnvelopeCap fails exactly at iteration 4; "
                    "this does not refute the enhanced paired-history route."
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
