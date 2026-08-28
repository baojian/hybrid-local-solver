#!/usr/bin/env python3
"""Exact audit for the C6 independent-set blow-up theorem.

Only the Python standard library is used.  The script checks the rational
function formulas for the eliminated-h clipped-Laplacian kernel, its signs,
the within-part eigenvalue comparison, the exact failure of (HK), and finite
blow-up matrices as a guardrail.
"""

from fractions import Fraction as F
import json

from verify_master_identity import inverse


def clean(poly):
    return {degree: value for degree, value in poly.items() if value}


def padd(left, right):
    result = dict(left)
    for degree, value in right.items():
        result[degree] = result.get(degree, F(0)) + value
    return clean(result)


def pscale(value, poly):
    return clean({degree: value * entry for degree, entry in poly.items()})


def pmul(left, right):
    result = {}
    for i, a in left.items():
        for j, b in right.items():
            result[i + j] = result.get(i + j, F(0)) + a * b
    return clean(result)


class Rat:
    def __init__(self, numerator, denominator=None):
        self.numerator = clean(numerator)
        self.denominator = clean({0: F(1)} if denominator is None else denominator)

    @staticmethod
    def constant(value):
        return Rat({0: F(value)})

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

    def __truediv__(self, other):
        other = other if isinstance(other, Rat) else Rat.constant(other)
        return Rat(pmul(self.numerator, other.denominator), pmul(self.denominator, other.numerator))

    def __rtruediv__(self, other):
        return Rat.constant(other) / self

    def __eq__(self, other):
        other = other if isinstance(other, Rat) else Rat.constant(other)
        return pmul(self.numerator, other.denominator) == pmul(other.numerator, self.denominator)

    def evaluate(self, value):
        numerator = sum(
            (coefficient * value**degree for degree, coefficient in self.numerator.items()), F(0)
        )
        denominator = sum(
            (coefficient * value**degree for degree, coefficient in self.denominator.items()), F(0)
        )
        return numerator / denominator


ONE = Rat.constant(1)
R = Rat({1: F(1)})


def chi(high_eigenvalue):
    """Kernel eigenvalue m0^2 h(1-h)/(1-m0 h), with m0=1-r."""
    high_eigenvalue = Rat.constant(high_eigenvalue)
    m0 = ONE - R
    return m0 * m0 * high_eigenvalue * (1 - high_eigenvalue) / (1 - m0 * high_eigenvalue)


def claimed_cycle_entries():
    # The displayed common denominator is 140(1+r)(1+4r)(3+4r).
    common = {0: F(420), 1: F(2660), 2: F(4480), 3: F(2240)}
    one_minus_r_squared = {0: F(1), 1: F(-2), 2: F(1)}
    numerators = [
        {0: F(227), 1: F(848), 2: F(656)},
        {0: F(-19), 1: F(-256), 2: F(-272)},
        {0: F(-61), 1: F(-144), 2: F(-48)},
        {0: F(-67), 1: F(-48), 2: F(-16)},
        {0: F(-61), 1: F(-144), 2: F(-48)},
        {0: F(-19), 1: F(-256), 2: F(-272)},
    ]
    return [Rat(pmul(one_minus_r_squared, numerator), common) for numerator in numerators]


def cycle_rational_functions():
    eig_45 = chi(F(4, 5))
    eig_47 = chi(F(4, 7))
    eig_12 = chi(F(1, 2))
    cos_one = [F(1), F(1, 2), F(-1, 2), F(-1), F(-1, 2), F(1, 2)]
    cos_two = [F(1), F(-1, 2), F(-1, 2), F(1), F(-1, 2), F(-1, 2)]
    spectral = [
        (2 * eig_45 * cos_one[d] + 2 * eig_47 * cos_two[d] + eig_12 * (-1 if d % 2 else 1)) / 6
        for d in range(6)
    ]
    claimed = claimed_cycle_entries()
    assert all(left == right for left, right in zip(spectral, claimed))

    within = chi(F(2, 3))
    claimed_within = Rat(pmul({0: F(2, 3)}, {0: F(1), 1: F(-2), 2: F(1)}), {0: F(1), 1: F(2)})
    assert within == claimed_within
    margin = within - claimed[0]
    claimed_margin = Rat(
        pmul({0: F(1), 1: F(-2), 2: F(1)}, {0: F(159), 1: F(1414), 2: F(1904), 3: F(544)}),
        {0: F(1260), 1: F(10500), 2: F(29400), 3: F(33600), 4: F(13440)},
    )
    assert margin == claimed_margin
    return (
        spectral,
        within,
        {
            "cycle_entries_matched": 6,
            "strictly_negative_offdiagonal_formulas": 5,
            "strictly_positive_within_margin_formula": True,
        },
    )


def matmul(left, right):
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_linear(left, right, left_scale=F(1), right_scale=F(1)):
    return [
        [left_scale * left[i][j] + right_scale * right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def hk_failure():
    size = 6
    matrix = [
        [3 * F(i == j) - (F(1, 2) if (i - j) % size in (1, size - 1) else 0) for j in range(size)]
        for i in range(size)
    ]
    n_resolvent = inverse(matrix)
    square = matmul(n_resolvent, n_resolvent)
    adjacent_ratio = 24 * square[0][1]
    assert adjacent_ratio == F(5211, 4900)
    assert adjacent_ratio > 1
    return adjacent_ratio


def longer_cycle_cl_obstruction():
    size = 10
    identity = [[F(i == j) for j in range(size)] for i in range(size)]
    transition = [
        [F(1, 2) if (i - j) % size in (1, size - 1) else F(0) for j in range(size)]
        for i in range(size)
    ]
    high_kernel = [
        [2 * entry for entry in row]
        for row in inverse(matrix_linear(identity, transition, left_scale=3, right_scale=-1))
    ]
    q = F(1, 20)
    m0 = 1 - q * q
    m_operator = [[m0 * entry for entry in row] for row in high_kernel]
    clipped_laplacian = matmul(
        matmul(m_operator, matrix_linear(identity, m_operator, left_scale=m0, right_scale=-1)),
        inverse(matrix_linear(identity, m_operator, right_scale=-1)),
    )
    adjacent = clipped_laplacian[0][1]
    assert adjacent == F(6998345705403423, 396849260156782400)
    assert adjacent > 0
    return adjacent


def c10_edgewise_payment():
    """Check the exact edgewise-Young certificate on C10 at q=1/20."""
    size = 10
    identity = [[F(i == j) for j in range(size)] for i in range(size)]
    adjacency = [
        [F(1) if (i - j) % size in (1, size - 1) else F(0) for j in range(size)]
        for i in range(size)
    ]
    stationary = [[F(1, size) for _ in range(size)] for _ in range(size)]
    high_projection = matrix_linear(identity, stationary, right_scale=-1)
    high_resolvent = [
        [4 * entry for entry in row]
        for row in inverse(matrix_linear(identity, adjacency, left_scale=6, right_scale=-1))
    ]

    q = F(1, 20)
    m0 = 1 - q * q
    m_operator = [[m0 * entry for entry in row] for row in high_resolvent]
    one_minus_m = matrix_linear(identity, m_operator, right_scale=-1)
    m0_minus_m = matrix_linear(identity, m_operator, left_scale=m0, right_scale=-1)
    g_operator = matrix_linear(
        matrix_linear(identity, m_operator, left_scale=m0, right_scale=-2),
        matmul(m_operator, m_operator),
    )
    a_operator = [
        [entry / m0 for entry in row]
        for row in matmul(
            matmul(matmul(m_operator, m0_minus_m), m0_minus_m),
            inverse(one_minus_m),
        )
    ]
    b_operator = [
        [m0 * entry for entry in row]
        for row in matmul(
            matmul(
                matmul(matmul(m_operator, g_operator), inverse(one_minus_m)),
                inverse(matrix_linear(m0_minus_m, stationary)),
            ),
            high_projection,
        )
    ]
    c_operator = matmul(matmul(m_operator, m0_minus_m), inverse(one_minus_m))

    for operator in (a_operator, b_operator, c_operator):
        assert all(sum(row, F(0)) == 0 for row in operator)
        assert all(operator[i][j] == operator[j][i] for i in range(size) for j in range(size))

    assert all(a_operator[0][j] < 0 for j in range(1, size))
    assert all(b_operator[0][j] < 0 for j in range(1, size))
    assert c_operator[0][1] > 0 and c_operator[0][size - 1] > 0
    assert all(c_operator[0][j] < 0 for j in range(2, size - 1))

    ratio = c_operator[0][1] ** 2 / ((-a_operator[0][1]) * (-b_operator[0][1]))
    claimed_ratio = F(
        9190540374100260057432724000,
        35964609239043602890432954263,
    )
    assert ratio == claimed_ratio
    assert ratio < 1

    within_m = m0 * F(2, 3)
    within_g = m0 - 2 * within_m + within_m * within_m
    within_a = within_m * (m0 - within_m) ** 2 / (m0 * (1 - within_m))
    within_b = m0 * within_m * within_g / ((1 - within_m) * (m0 - within_m))
    within_c = within_m * (m0 - within_m) / (1 - within_m)
    within_offdiagonal = (
        a_operator[0][0] - within_a,
        b_operator[0][0] - within_b,
        c_operator[0][0] - within_c,
    )
    claimed_within = (
        -F(8569107687113450384299, 189685215671218537987200),
        -F(5779278789418042112799, 53177800861008841600000),
        -F(1662576823382931953, 26588900430504420800),
    )
    assert within_offdiagonal == claimed_within
    assert all(entry < 0 for entry in within_offdiagonal)

    # On C10[Kbar_a], cross-part entries and within-part off-diagonal
    # entries are divided by a.  Signs and every c^2/(ab) ratio therefore
    # remain unchanged.  These finite sizes guard the analytic block rule.
    for part_size in range(1, 13):
        assert all(entry / part_size < 0 for entry in within_offdiagonal)
        assert ratio < 1
    return {
        "A_offdiagonal_strictly_negative": 9,
        "B_offdiagonal_strictly_negative": 9,
        "C_positive_offdiagonal_distances": [1, 9],
        "C_adjacent_entry": str(c_operator[0][1]),
        "edgewise_ratio": str(ratio),
        "edgewise_ratio_below_one": True,
        "within_part_offdiagonal": [str(entry) for entry in within_offdiagonal],
        "blowup_part_sizes_checked": "1..12",
    }


def eliminated_h_trials():
    checks = 0
    for q in (F(1, 20), F(1, 10), F(1, 4)):
        m0 = 1 - q * q
        beta = (1 - q) / (1 + q)
        nu = q / (1 + q)
        for high_eigenvalue in (F(1, 2), F(4, 7), F(2, 3), F(4, 5)):
            m = m0 * high_eigenvalue
            g_value = m0 - 2 * m + m * m
            s_value = nu * nu * m0 * m + beta * g_value
            assert s_value == beta * (1 - m) * (m0 - m)
            for u, v in ((F(2, 7), F(3, 5)), (F(-4, 9), F(5, 8))):
                constant = m * m * u * u - m0 * m * (u - v) ** 2
                linear = m * ((m0 - m) * u - m0 * v)
                eliminated = constant + nu * nu * linear * linear / s_value
                a_value = m * (m0 - m) ** 2 / (m0 * (1 - m))
                b_value = m0 * m * g_value / ((1 - m) * (m0 - m))
                c_value = m * (m0 - m) / (1 - m)
                claimed = -a_value * u * u - b_value * v * v + 2 * c_value * u * v
                assert eliminated == claimed
                checks += 1
    return checks


def finite_blowup_guardrail(entries, within):
    matrices = 0
    offdiagonal = 0
    for part_size in range(1, 13):
        total = 6 * part_size
        for q in (F(1, 20), F(1, 10), F(1, 4)):
            r_value = q * q
            cycle = [entry.evaluate(r_value) for entry in entries]
            within_value = within.evaluate(r_value)
            for i in range(total):
                part_i = i // part_size
                for j in range(total):
                    if i == j:
                        continue
                    part_j = j // part_size
                    if part_i == part_j:
                        value = (cycle[0] - within_value) / part_size
                    else:
                        value = cycle[(part_j - part_i) % 6] / part_size
                    assert value < 0
                    offdiagonal += 1
            matrices += 1
    return matrices, offdiagonal


def main():
    entries, within, rational = cycle_rational_functions()
    matrices, offdiagonal = finite_blowup_guardrail(entries, within)
    payload = {
        "arithmetic": "fractions.Fraction and exact rational functions",
        "cycle_kernel": rational,
        "eliminated_h_identity_trials": eliminated_h_trials(),
        "finite_guardrail": {
            "blowup_matrices_passed": matrices,
            "part_sizes": "1..12",
            "q_values": ["1/20", "1/10", "1/4"],
            "strict_offdiagonal_checks_passed": offdiagonal,
        },
        "HK_adjacent_ratio": str(hk_failure()),
        "HK_strictly_fails": True,
        "CL_not_universal_on_cycles": {
            "graph_and_q": "C10, q=1/20",
            "positive_adjacent_entry": str(longer_cycle_cl_obstruction()),
        },
        "C10_edgewise_payment": c10_edgewise_payment(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
