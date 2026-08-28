"""Exact reachable post-lock witnesses on leaf-seeded unit stars.

The other leaves are permutation symmetric, so the literal obstacle-prox
trajectory reduces to the three types ``center``, ``seed leaf``, and ``other
leaf``.  Every calculation below uses :class:`fractions.Fraction`; the
reduction changes neither an active-set decision nor a trigger sign.

For a B-arm star we use q=1/(2(B+1)) and rho=1/(4B).  The full face first
appears at state x_4.  We then run J pure stable-face solves and switch to
beta=(1-q)/(1+q).  The registered B=50,J=6 example realizes the asymptotic
second-trigger obstruction from the accompanying theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations

Rat = Fraction
Vector = list[Rat]
Matrix = list[list[Rat]]

CENTER, SEED, OTHER = range(3)


def solve(a: Matrix, b: Vector) -> Vector:
    """Solve a nonsingular rational linear system by exact elimination."""
    n = len(b)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if aug[row][column] != 0)
        aug[column], aug[pivot] = aug[pivot], aug[column]
        scale = aug[column][column]
        aug[column] = [value / scale for value in aug[column]]
        for row in range(n):
            if row == column or aug[row][column] == 0:
                continue
            factor = aug[row][column]
            aug[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(aug[row], aug[column])
            ]
    return [row[-1] for row in aug]


def star_instance(arms: int) -> tuple[Vector, Matrix, Vector, Rat, Rat, str, str]:
    """Return the exact three-class unit-star instance."""
    if arms < 2:
        raise ValueError("the star must have at least two arms")
    q = Rat(1, 2 * (arms + 1))
    rho = Rat(1, 4 * arms)
    alpha = q * q / (1 + q * q)
    kappa = 1 - 2 * alpha
    beta = (1 - q) / (1 + q)
    edge = -(1 - alpha) / 2
    diagonal = (1 + alpha) / 2
    degrees = [Rat(arms), Rat(1), Rat(1)]
    qt = [
        [arms * diagonal, edge, (arms - 1) * edge],
        [edge, diagonal, Rat(0)],
        [edge, Rat(0), diagonal],
    ]
    ct = [
        -alpha * rho * arms,
        alpha * (1 - rho),
        -alpha * rho,
    ]
    return degrees, qt, ct, kappa, beta, str(q), str(rho)


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [sum(value * vector[j] for j, value in enumerate(row)) for row in matrix]


def obstacle_solve(
    degrees: Vector,
    qt: Matrix,
    ct: Vector,
    kappa: Rat,
    lower_center: Vector,
) -> Vector:
    """Solve the three-class shifted obstacle problem by mask enumeration."""
    rhs = [ct[i] + kappa * degrees[i] * lower_center[i] for i in range(3)]
    hessian = [
        [qt[i][j] + (kappa * degrees[i] if i == j else 0) for j in range(3)]
        for i in range(3)
    ]
    candidates: list[Vector] = []
    for size in range(4):
        for active_tuple in combinations(range(3), size):
            active = list(active_tuple)
            x = [Rat(0)] * 3
            if active:
                reduced = [[hessian[i][j] for j in active] for i in active]
                values = solve(reduced, [rhs[i] for i in active])
                if any(value <= 0 for value in values):
                    continue
                for i, value in zip(active, values):
                    x[i] = value
            gradient = [value - rhs[i] for i, value in enumerate(matvec(hessian, x))]
            if all(gradient[i] == 0 for i in active) and all(
                gradient[i] >= 0 for i in range(3) if i not in active
            ):
                candidates.append(x)
    if len(candidates) != 1:
        raise AssertionError(f"expected one LCP solution, found {len(candidates)}")
    return candidates[0]


def support(x: Vector) -> tuple[int, ...]:
    return tuple(i for i, value in enumerate(x) if value > 0)


def expanded_face_size(x: Vector, arms: int) -> int:
    return int(x[CENTER] > 0) + int(x[SEED] > 0) + (arms - 1) * int(x[OTHER] > 0)


def run(arms: int = 50, warmup: int = 6) -> dict[str, object]:
    """Replay one exact reachable star schedule through its first bad trigger."""
    degrees, qt, ct, kappa, full_beta, q, rho = star_instance(arms)
    previous = [Rat(0)] * 3
    current = [Rat(0)] * 3
    records: list[dict[str, object]] = []
    output_supports: list[tuple[int, ...]] = []
    momentum_start = 4 + warmup
    for stage in range(momentum_start + 8):
        beta = Rat(0) if stage < momentum_start else full_beta
        velocity = [current[i] - previous[i] for i in range(3)]
        trial = [current[i] + beta * velocity[i] for i in range(3)]
        face = support(trial)
        residual = [ct[i] - value for i, value in enumerate(matvec(qt, trial))]
        negative = [(i, residual[i]) for i in face if residual[i] < 0]
        records.append(
            {
                "stage": stage,
                "beta": str(beta),
                "face_size": expanded_face_size(trial, arms),
                "minimum_trigger": str(min((residual[i] for i in face), default=Rat(0))),
            }
        )
        if negative:
            row, value = negative[0]
            assert output_supports[:4] == [
                (CENTER, SEED),
                (CENTER, SEED),
                (CENTER, SEED),
                (CENTER, SEED, OTHER),
            ]
            return {
                "arms": arms,
                "q": q,
                "rho": rho,
                "seed_leaf": 1,
                "first_full_face_state": 4,
                "warmup": warmup,
                "first_bad_stage": stage,
                "row_type": ("center", "seed", "other")[row],
                "value": str(value),
                "records": records,
            }
        next_state = obstacle_solve(degrees, qt, ct, kappa, trial)
        output_supports.append(support(next_state))
        previous, current = current, next_state
    raise AssertionError("no negative trigger within the registered horizon")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arms", type=int, default=50)
    parser.add_argument("--warmup", type=int, default=6)
    args = parser.parse_args()
    result = run(args.arms, args.warmup)
    expected = Rat(
        -147824969167474143070830622648108443644686306420711,
        5876713986025144219355264603664195883039449023398155386880,
    )
    if (args.arms, args.warmup) == (50, 6):
        assert result["first_bad_stage"] == 11
        assert result["row_type"] == "seed"
        assert Rat(result["value"]) == expected
    print(result)


if __name__ == "__main__":
    main()
