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
from math import comb

Rat = Fraction
Vector = list[Rat]
Matrix = list[list[Rat]]

CENTER, SEED, OTHER = range(3)


def _poly_desc(coefficients: list[int]) -> list[int]:
    """Convert displayed descending coefficients to ascending order."""
    return list(reversed(coefficients))


def _poly_add(left: list[int], right: list[int], scale: int = 1) -> list[int]:
    size = max(len(left), len(right))
    result = [0] * size
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += scale * value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _poly_mul(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return result


def _poly_pow(base: list[int], exponent: int) -> list[int]:
    result = [1]
    for _ in range(exponent):
        result = _poly_mul(result, base)
    return result


def _shift_by_two(poly: list[int]) -> list[int]:
    """Return coefficients of ``poly(b+2)`` in ascending powers of b."""
    result = [0] * len(poly)
    for power, value in enumerate(poly):
        for shifted_power in range(power + 1):
            result[shifted_power] += (
                value * comb(power, shifted_power) * 2 ** (power - shifted_power)
            )
    return result


def exact_residual_margin_certificate() -> None:
    """Prove the rational margins for all integer ``B>=2``.

    Clearing the positive denominators and substituting ``B=b+2`` reduces
    each assertion to a polynomial with nonnegative coefficients and a
    positive constant term.
    """
    pc = _poly_desc([22032, 124208, 264196, 256084, 99850, -1354, -8271, -710, -33, -2])
    ps = _poly_desc(
        [
            55296,
            344592,
            851760,
            1042180,
            617428,
            100938,
            -63850,
            -29439,
            -2870,
            -33,
            -2,
        ]
    )
    po = _poly_desc([18576, 94512, 144036, 1172, -189830, -171434, -52207, -3238, -17, -2])
    pt = _poly_desc([24624, 140176, 300428, 299772, 142142, 39778, 18459, 6510, 117, -6])
    b_poly = [0, 1]
    factor = [3, 8, 4]  # (2B+1)(2B+3)
    d0 = _poly_mul(_poly_pow([1, 1], 8), _poly_pow([-1, 9], 3))

    # The displayed leaf-mean formula equals S+(B-1)O identically.
    leaf_sum = _poly_add(ps, _poly_mul([-1, 1], po))
    assert leaf_sum == _poly_mul(_poly_mul([3], b_poly), pt)

    numerators = {
        "C": _poly_mul(factor, pc),
        "1-C": _poly_add(_poly_mul([512], d0), _poly_mul(factor, pc), -1),
        "S": _poly_mul(factor, ps),
        "O": _poly_mul(factor, po),
        "leaf mean": _poly_mul(factor, pt),
        "1-leaf mean": _poly_add(_poly_mul([512], d0), _poly_mul(factor, pt), -1),
        "S-O-3/20": _poly_add(
            _poly_mul([20], _poly_mul(factor, _poly_add(ps, po, -1))),
            _poly_mul([4608], _poly_mul(b_poly, d0)),
            -1,
        ),
    }
    for name, numerator in numerators.items():
        shifted = _shift_by_two(numerator)
        assert shifted[0] > 0, name
        assert all(coefficient >= 0 for coefficient in shifted), name


def residual_parameters(arms: int) -> tuple[Rat, Rat, Rat]:
    """Return exact ``(C_B,S_B,O_B)`` for alpha^-1 D^-1/2 Y_4."""
    b = arms
    d0 = (b + 1) ** 8 * (9 * b - 1) ** 3
    factor = (2 * b + 1) * (2 * b + 3)
    pc = (
        22032 * b**9
        + 124208 * b**8
        + 264196 * b**7
        + 256084 * b**6
        + 99850 * b**5
        - 1354 * b**4
        - 8271 * b**3
        - 710 * b**2
        - 33 * b
        - 2
    )
    ps = (
        55296 * b**10
        + 344592 * b**9
        + 851760 * b**8
        + 1042180 * b**7
        + 617428 * b**6
        + 100938 * b**5
        - 63850 * b**4
        - 29439 * b**3
        - 2870 * b**2
        - 33 * b
        - 2
    )
    po = (
        18576 * b**9
        + 94512 * b**8
        + 144036 * b**7
        + 1172 * b**6
        - 189830 * b**5
        - 171434 * b**4
        - 52207 * b**3
        - 3238 * b**2
        - 17 * b
        - 2
    )
    return (
        Rat(factor * pc, 512 * d0),
        Rat(factor * ps, 1536 * b * d0),
        Rat(factor * po, 1536 * b * d0),
    )


def second_trigger_margin(arms: int, warmup: int) -> Rat:
    """Return the seeded second-trigger value divided by alpha_B."""
    q = Rat(1, 2 * (arms + 1))
    beta = (1 - q) / (1 + q)
    m0 = 1 - q * q

    def trigger_polynomial(mode: Rat) -> Rat:
        return mode**warmup * ((1 + beta) ** 2 * mode - beta * (2 + beta))

    f_plus = trigger_polynomial(m0)
    f_zero = trigger_polynomial(Rat(2, 3) * m0)
    f_minus = trigger_polynomial(Rat(1, 2) * m0)
    center, seed, other = residual_parameters(arms)
    leaf_mean = seed + (arms - 1) * other
    return (
        (f_plus - f_minus) * center / (2 * arms)
        + (f_plus + f_minus) * leaf_mean / (2 * arms)
        + Rat(arms - 1, arms) * (seed - other) * f_zero
    )


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
                value - factor * pivot_value for value, pivot_value in zip(aug[row], aug[column])
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
        [qt[i][j] + (kappa * degrees[i] if i == j else 0) for j in range(3)] for i in range(3)
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


def check_residual_parameters(arms: int) -> None:
    """Match the closed residual formulas to the literal four-stage LCP."""
    degrees, qt, ct, kappa, _, q_text, _ = star_instance(arms)
    current = [Rat(0)] * 3
    supports = []
    for _ in range(4):
        current = obstacle_solve(degrees, qt, ct, kappa, current)
        supports.append(support(current))
    assert supports == [
        (CENTER, SEED),
        (CENTER, SEED),
        (CENTER, SEED),
        (CENTER, SEED, OTHER),
    ]
    residual = [ct[i] - value for i, value in enumerate(matvec(qt, current))]
    q = Rat(q_text)
    alpha = q * q / (1 + q * q)
    assert tuple(value / alpha for value in residual) == residual_parameters(arms)


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
    exact_residual_margin_certificate()
    check_residual_parameters(args.arms)
    result = run(args.arms, args.warmup)
    expected = Rat(
        -147824969167474143070830622648108443644686306420711,
        5876713986025144219355264603664195883039449023398155386880,
    )
    if (args.arms, args.warmup) == (50, 6):
        assert result["first_bad_stage"] == 11
        assert result["row_type"] == "seed"
        assert Rat(result["value"]) == expected
        # A non-vacuous exact instance of the matching logarithmic lower bound.
        assert second_trigger_margin(10_000, 6) <= Rat(-2, 10_000)
    print(result)


if __name__ == "__main__":
    main()
