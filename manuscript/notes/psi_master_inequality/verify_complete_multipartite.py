#!/usr/bin/env python3
"""Exact certificate for the complete-multipartite (HK-N) theorem.

The script uses only the standard library.  It verifies the rational-function
identity behind the continuous part-fraction inequality by exact bivariate
polynomial arithmetic, checks that its Bernstein coefficients are
nonnegative, and performs a finite exact census as an additional guardrail.
"""

from fractions import Fraction as F
from math import factorial
import json

from verify_master_identity import inverse


def clean(poly):
    return {key: value for key, value in poly.items() if value}


def padd(left, right):
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, F(0)) + value
    return clean(result)


def pscale(value, poly):
    return clean({key: value * entry for key, entry in poly.items()})


def psub(left, right):
    return padd(left, pscale(-1, right))


def pmul(left, right):
    result = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            key = (i + k, j + ell)
            result[key] = result.get(key, F(0)) + a * b
    return clean(result)


def ppow(poly, exponent):
    result = {(0, 0): F(1)}
    for _ in range(exponent):
        result = pmul(result, poly)
    return result


ONE = {(0, 0): F(1)}
PVAR = {(1, 0): F(1)}
SVAR = {(0, 1): F(1)}
RVAR = psub(psub(ONE, PVAR), SVAR)


class Rat:
    def __init__(self, numerator, denominator=ONE):
        self.numerator = clean(numerator)
        self.denominator = clean(denominator)

    @staticmethod
    def constant(value):
        return Rat({(0, 0): F(value)})

    def __add__(self, other):
        other = other if isinstance(other, Rat) else Rat.constant(other)
        return Rat(
            padd(pmul(self.numerator, other.denominator), pmul(other.numerator, self.denominator)),
            pmul(self.denominator, other.denominator),
        )

    __radd__ = __add__

    def __neg__(self):
        return Rat(pscale(-1, self.numerator), self.denominator)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Rat) else Rat.constant(-other))

    def __rsub__(self, other):
        return Rat.constant(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Rat) else Rat.constant(other)
        return Rat(pmul(self.numerator, other.numerator), pmul(self.denominator, other.denominator))

    __rmul__ = __mul__

    def inverse(self):
        return Rat(self.denominator, self.numerator)

    def __truediv__(self, other):
        other = other if isinstance(other, Rat) else Rat.constant(other)
        return self * other.inverse()

    def __rtruediv__(self, other):
        return Rat.constant(other) / self


P_COEFFICIENT_ROWS = [
    [F(81), F(54), F(459, 14), F(243, 14), F(54, 7), F(81, 28), F(27, 28), F(0), F(0)],
    [F(54), F(2025, 56), F(1247, 56), F(3399, 280), F(1587, 280), F(65, 28), F(27, 28), F(0)],
    [F(459, 14), F(1247, 56), F(2977, 210), F(4581, 560), F(869, 210), F(13, 7), F(27, 28)],
    [F(243, 14), F(3399, 280), F(4581, 560), F(1457, 280), F(85, 28), F(3, 2)],
    [F(54, 7), F(1587, 280), F(869, 210), F(85, 28), F(81, 35)],
    [F(81, 28), F(65, 28), F(13, 7), F(3, 2)],
    [F(27, 28), F(27, 28), F(27, 28)],
    [F(0), F(0)],
    [F(0)],
]

L_COEFFICIENT_ROWS = [
    [F(9), F(7), F(4), F(0)],
    [F(7), F(17, 3), F(4)],
    [F(4), F(4)],
    [F(0)],
]


def bernstein_polynomial(rows):
    degree = len(rows) - 1
    result = {}
    for i, row in enumerate(rows):
        for j, coefficient in enumerate(row):
            k = degree - i - j
            multiplier = F(factorial(degree), factorial(i) * factorial(j) * factorial(k))
            basis = pmul(pmul(ppow(PVAR, i), ppow(SVAR, j)), ppow(RVAR, k))
            result = padd(result, pscale(coefficient * multiplier, basis))
    return result


def continuous_certificate():
    p = Rat(PVAR)
    s = Rat(SVAR)
    r = Rat(RVAR)
    x = 2 / (3 - 2 * p)
    y = 2 / (3 - 2 * s)
    wp = p * (1 - p)
    ws = s * (1 - s)
    lower_m = (wp * x + ws * y + F(2, 3) * r) / (wp + ws + r)
    left = 4 * lower_m - x * y * (F(20, 3) - x - y - 4 / (3 * lower_m))

    p_certificate = bernstein_polynomial(P_COEFFICIENT_ROWS)
    l_certificate = bernstein_polynomial(L_COEFFICIENT_ROWS)
    l_monomial = padd(
        padd(
            padd(pscale(2, pmul(pmul(PVAR, PVAR), SVAR)), pscale(-3, pmul(PVAR, PVAR))),
            padd(pscale(2, pmul(PVAR, pmul(SVAR, SVAR))), pscale(4, pmul(PVAR, SVAR))),
        ),
        padd(
            padd(pscale(-6, PVAR), pscale(-3, pmul(SVAR, SVAR))),
            padd(pscale(-6, SVAR), pscale(9, ONE)),
        ),
    )
    assert l_certificate == l_monomial

    denominator = pmul(
        pmul(
            pscale(3, ppow(psub(pscale(3, ONE), pscale(2, PVAR)), 2)),
            ppow(psub(pscale(3, ONE), pscale(2, SVAR)), 2),
        ),
        pmul(psub(ONE, padd(ppow(PVAR, 2), ppow(SVAR, 2))), l_certificate),
    )
    right = Rat(pscale(32, p_certificate), denominator)
    assert pmul(left.numerator, right.denominator) == pmul(right.numerator, left.denominator)

    flat_p = [entry for row in P_COEFFICIENT_ROWS for entry in row]
    flat_l = [entry for row in L_COEFFICIENT_ROWS for entry in row]
    assert all(entry >= 0 for entry in flat_p)
    assert all(entry >= 0 for entry in flat_l)
    return {
        "rational_identity": True,
        "P_degree": 8,
        "P_coefficients": len(flat_p),
        "P_nonnegative": sum(entry >= 0 for entry in flat_p),
        "P_zero": sum(entry == 0 for entry in flat_p),
        "L_degree": 3,
        "L_coefficients": len(flat_l),
        "L_nonnegative": sum(entry >= 0 for entry in flat_l),
        "L_zero": sum(entry == 0 for entry in flat_l),
    }


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for first in range(minimum, total + 1):
        for rest in partitions(total - first, first):
            yield (first,) + rest


def closed_n(part_sizes):
    total = sum(part_sizes)
    owner = [part for part, size in enumerate(part_sizes) for _ in range(size)]
    degree_by_part = [total - size for size in part_sizes]
    c_by_part = [3 * total - 2 * size for size in part_sizes]
    cap = 1 - sum(F(size, c_by_part[part]) for part, size in enumerate(part_sizes))
    matrix = [[F(0) for _ in range(total)] for _ in range(total)]
    for i in range(total):
        part_i = owner[i]
        for j in range(total):
            part_j = owner[j]
            matrix[i][j] = (
                F(int(i == j), 3)
                + F(1, c_by_part[part_i]) * F(degree_by_part[part_j], 1) / (cap * c_by_part[part_j])
                - (F(1, 3 * c_by_part[part_i]) if part_i == part_j else 0)
            )
    degree = [F(degree_by_part[owner[i]]) for i in range(total)]
    return matrix, owner, degree


def direct_n(part_sizes):
    total = sum(part_sizes)
    owner = [part for part, size in enumerate(part_sizes) for _ in range(size)]
    degree = [F(total - part_sizes[part]) for part in owner]
    matrix = [[F(0) for _ in range(total)] for _ in range(total)]
    for i in range(total):
        matrix[i][i] = 3 * degree[i]
        for j in range(total):
            if owner[i] != owner[j]:
                matrix[i][j] = -1
    matrix_inv = inverse(matrix)
    return [[matrix_inv[i][j] * degree[j] for j in range(total)] for i in range(total)]


def matmul(left, right):
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def finite_census(max_n=14, direct_max_n=9):
    families = 0
    direct_formulas = 0
    offdiagonal = 0
    max_ratio = F(0)
    argmax = None
    for total in range(2, max_n + 1):
        for part_sizes in partitions(total):
            if len(part_sizes) < 2:
                continue
            closed, owner, degree = closed_n(part_sizes)
            if total <= direct_max_n:
                assert closed == direct_n(part_sizes)
                direct_formulas += 1
            square = matmul(closed, closed)
            volume = sum(degree)
            for i in range(total):
                for j in range(total):
                    if i == j:
                        continue
                    ratio = 4 * volume * square[i][j] / degree[j]
                    assert ratio <= 1, (part_sizes, i, j, ratio)
                    if ratio > max_ratio:
                        max_ratio = ratio
                        argmax = [list(part_sizes), i, j, owner[i], owner[j], str(ratio)]
                    offdiagonal += 1
            families += 1
    return {
        "max_n": max_n,
        "part_vectors_passed": families,
        "direct_closed_resolvents_passed": direct_formulas,
        "offdiagonal_HK_checks_passed": offdiagonal,
        "maximum_ratio": str(max_ratio),
        "maximum_witness": argmax,
    }


def main():
    payload = {
        "arithmetic": "fractions.Fraction",
        "continuous_certificate": continuous_certificate(),
        "finite_guardrail": finite_census(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
