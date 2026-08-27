"""Exact post-lock warmup screen for the fixed endpoint-path face.

This verifier is deliberately independent of the Fable implementation.  It
works in the rational ``hat`` coordinates used by that implementation.  For
a supplied full endpoint path face it constructs

    M = kappa D (Qt + kappa D)^(-1)

exactly.  Starting with an arbitrary nonnegative residual column, ``J`` pure
proximal solves give the two residual states ``M^(J-1) y`` and ``M^J y``.
The first momentum trigger and every later trigger are propagated as exact
rational matrices.  A negative matrix entry is therefore an exact witness
against a cone-uniform warmup claim: choose the corresponding basis column.

The finite horizon is a falsification screen, not an asymptotic proof that a
passing ``J`` remains safe forever and not a reachability claim for the
literal changing-face RPPR trajectory.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

Rat = Fraction
Matrix = list[list[Rat]]


def zeros(n: int) -> Matrix:
    return [[Rat(0) for _ in range(n)] for _ in range(n)]


def identity(n: int) -> Matrix:
    out = zeros(n)
    for i in range(n):
        out[i][i] = Rat(1)
    return out


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    out = zeros(n)
    for i in range(n):
        for k, aik in enumerate(a[i]):
            if aik == 0:
                continue
            for j, bkj in enumerate(b[k]):
                if bkj != 0:
                    out[i][j] += aik * bkj
    return out


def lincomb(a: Rat, x: Matrix, b: Rat, y: Matrix) -> Matrix:
    return [[a * xij + b * yij for xij, yij in zip(xrow, yrow)] for xrow, yrow in zip(x, y)]


def inverse(a: Matrix) -> Matrix:
    n = len(a)
    aug = [row[:] + eye for row, eye in zip(a, identity(n))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col or aug[row][col] == 0:
                continue
            factor = aug[row][col]
            aug[row] = [
                value - factor * pivot_value for value, pivot_value in zip(aug[row], aug[col])
            ]
    return [row[n:] for row in aug]


def endpoint_path_map(n: int, q: Rat) -> Matrix:
    """Return exact M in hat coordinates on the supplied full path P_n."""
    alpha = q * q / (1 + q * q)
    kappa = 1 - 2 * alpha
    degrees = [Rat(1)] + [Rat(2)] * (n - 2) + [Rat(1)]
    qt = zeros(n)
    for i, degree in enumerate(degrees):
        qt[i][i] = degree * (1 + alpha) / 2
    edge = -(1 - alpha) / 2
    for i in range(n - 1):
        qt[i][i + 1] = edge
        qt[i + 1][i] = edge
    shifted = [row[:] for row in qt]
    for i, degree in enumerate(degrees):
        shifted[i][i] += kappa * degree
    inv = inverse(shifted)
    out = zeros(n)
    for i, degree in enumerate(degrees):
        for j in range(n):
            out[i][j] = kappa * degree * inv[i][j]
    return out


def first_negative(matrix: Matrix) -> tuple[int, int, Rat] | None:
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value < 0:
                return i, j, value
    return None


def audit(n: int, q: Rat, warmup: int, horizon: int) -> dict[str, object]:
    if warmup < 1:
        raise ValueError("warmup must include at least one stable-face prox solve")
    m = endpoint_path_map(n, q)
    beta = (1 - q) / (1 + q)
    previous = identity(n)
    for _ in range(warmup - 1):
        previous = matmul(m, previous)
    current = matmul(m, previous)
    trigger_previous = previous
    trigger = lincomb(1 + beta, current, -beta, previous)
    witness = first_negative(trigger)
    if witness is not None:
        return {
            "n": n,
            "q": str(q),
            "warmup": warmup,
            "safe_through": -1,
            "first_bad_time": 0,
            "row": witness[0],
            "column": witness[1],
            "value": str(witness[2]),
        }
    for time in range(1, horizon + 1):
        next_trigger = matmul(m, lincomb(1 + beta, trigger, -beta, trigger_previous))
        witness = first_negative(next_trigger)
        if witness is not None:
            return {
                "n": n,
                "q": str(q),
                "warmup": warmup,
                "safe_through": time - 1,
                "first_bad_time": time,
                "row": witness[0],
                "column": witness[1],
                "value": str(witness[2]),
            }
        trigger_previous, trigger = trigger, next_trigger
    return {
        "n": n,
        "q": str(q),
        "warmup": warmup,
        "safe_through": horizon,
        "first_bad_time": None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[4, 6, 8, 10, 12])
    parser.add_argument("--horizon", type=int, default=32)
    parser.add_argument("--max-warmup", type=int, default=8)
    parser.add_argument(
        "--q-scale",
        type=int,
        default=2,
        help="use q=1/(q_scale*n)",
    )
    args = parser.parse_args()
    for n in args.sizes:
        q = Rat(1, args.q_scale * n)
        first_pass = None
        records = []
        for warmup in range(1, args.max_warmup + 1):
            record = audit(n, q, warmup, args.horizon)
            records.append(record)
            if record["first_bad_time"] is None:
                first_pass = warmup
                break
        print(
            {
                "n": n,
                "q": str(q),
                "horizon": args.horizon,
                "first_finite_horizon_pass": first_pass,
                "records": records,
            }
        )


if __name__ == "__main__":
    main()
