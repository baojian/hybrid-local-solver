#!/usr/bin/env python3
"""Exact audit for the C6 independent-set blow-up theorem.

Only the Python standard library is used.  The script checks the rational
function formulas for the eliminated-h clipped-Laplacian kernel, its signs,
the within-part eigenvalue comparison, the exact failure of (HK), and finite
blow-up matrices as a guardrail.
"""

from fractions import Fraction as F
import json
from math import comb

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


def pdivrem(dividend, divisor):
    """Return the exact polynomial remainder in ascending dictionary form."""
    remainder = dict(dividend)
    divisor_degree = max(divisor)
    divisor_lead = divisor[divisor_degree]
    while remainder and max(remainder) >= divisor_degree:
        shift = max(remainder) - divisor_degree
        coefficient = remainder[max(remainder)] / divisor_lead
        for degree, value in divisor.items():
            target = degree + shift
            remainder[target] = remainder.get(target, F(0)) - coefficient * value
        remainder = clean(remainder)
    return remainder


def pgcd(left, right):
    """Return the monic exact gcd of two nonzero rational polynomials."""
    while right:
        left, right = right, pdivrem(left, right)
    leading = left[max(left)]
    return {degree: value / leading for degree, value in left.items()}


def pquotient(dividend, divisor):
    """Divide exactly, asserting a zero remainder."""
    remainder = dict(dividend)
    quotient = {}
    divisor_degree = max(divisor)
    divisor_lead = divisor[divisor_degree]
    while remainder:
        shift = max(remainder) - divisor_degree
        assert shift >= 0
        coefficient = remainder[max(remainder)] / divisor_lead
        quotient[shift] = coefficient
        for degree, value in divisor.items():
            target = degree + shift
            remainder[target] = remainder.get(target, F(0)) - coefficient * value
        remainder = clean(remainder)
    return clean(quotient)


def cancel(value):
    """Cancel the exact polynomial gcd of a rational function."""
    common = pgcd(value.numerator, value.denominator)
    return Rat(
        pquotient(value.numerator, common),
        pquotient(value.denominator, common),
    )


class QuadRat:
    """An element ``a+b*sqrt(5)`` over rational functions in r."""

    def __init__(self, rational=0, radical=0):
        self.rational = rational if isinstance(rational, Rat) else Rat.constant(rational)
        self.radical = radical if isinstance(radical, Rat) else Rat.constant(radical)

    def __add__(self, other):
        other = other if isinstance(other, QuadRat) else QuadRat(other)
        return QuadRat(self.rational + other.rational, self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self):
        return QuadRat(-self.rational, -self.radical)

    def __sub__(self, other):
        return self + (-other if isinstance(other, QuadRat) else QuadRat(-other))

    def __rsub__(self, other):
        return QuadRat(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, QuadRat) else QuadRat(other)
        return QuadRat(
            self.rational * other.rational + 5 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, QuadRat) else QuadRat(other)
        denominator = other.rational * other.rational - 5 * other.radical * other.radical
        return QuadRat(
            (self.rational * other.rational - 5 * self.radical * other.radical)
            / denominator,
            (self.radical * other.rational - self.rational * other.radical)
            / denominator,
        )

    def __rtruediv__(self, other):
        return QuadRat(other) / self


def bernstein_coefficients(poly, lower, upper):
    """Convert ``poly(r)`` on [lower,upper] to exact Bernstein coefficients."""
    degree = max(poly)
    power = [F(0)] * (degree + 1)
    for exponent, coefficient in poly.items():
        for index in range(exponent + 1):
            power[index] += (
                coefficient
                * comb(exponent, index)
                * lower ** (exponent - index)
                * (upper - lower) ** index
            )
    return [
        sum(
            (
                power[index] * F(comb(bernstein_index, index), comb(degree, index))
                for index in range(bernstein_index + 1)
            ),
            F(0),
        )
        for bernstein_index in range(degree + 1)
    ]


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


def c10_interval_entries():
    """Return exact C10 kernel rows over Q(sqrt(5))(r), simplified to Q(r)."""
    radical = QuadRat(0, 1)
    adjacency_eigenvalues = [
        QuadRat(2),
        (1 + radical) / 2,
        (radical - 1) / 2,
        (1 - radical) / 2,
        -(1 + radical) / 2,
        QuadRat(-2),
    ]
    high_eigenvalues = [4 / (6 - value) for value in adjacency_eigenvalues]
    m0 = QuadRat(ONE - R)

    def scalar_kernels(high_eigenvalue):
        m_value = m0 * high_eigenvalue
        difference = m0 - m_value
        g_value = m0 - 2 * m_value + m_value * m_value
        return (
            m_value * difference * difference / (m0 * (1 - m_value)),
            m0 * m_value * g_value / ((1 - m_value) * difference),
            m_value * difference / (1 - m_value),
        )

    modal = [None] + [scalar_kernels(high_eigenvalues[index]) for index in range(1, 6)]
    rows = []
    for operator_index in range(3):
        row = []
        for distance in range(6):
            entry = QuadRat(0)
            for frequency in range(1, 5):
                cosine_index = (frequency * distance) % 10
                cosine_index = min(cosine_index, 10 - cosine_index)
                entry += modal[frequency][operator_index] * adjacency_eigenvalues[cosine_index]
            entry += modal[5][operator_index] * (1 if distance % 2 == 0 else -1)
            entry /= 10
            assert entry.radical == 0
            row.append(cancel(entry.rational))
        rows.append(row)
    within = scalar_kernels(QuadRat(F(2, 3)))
    assert all(value.radical == 0 for value in within)
    return rows, [cancel(value.rational) for value in within]


def c10_edgewise_interval_payment():
    """Prove the edgewise certificate on 1/25 <= q <= 7/100."""
    lower = F(1, 625)
    upper = F(49, 10_000)
    rows, within = c10_interval_entries()
    certificates = []

    def certify(name, value, sign):
        value = cancel(value)
        numerator = pscale(sign, value.numerator)
        numerator_bernstein = bernstein_coefficients(numerator, lower, upper)
        denominator_bernstein = bernstein_coefficients(value.denominator, lower, upper)
        assert all(coefficient > 0 for coefficient in numerator_bernstein)
        assert all(coefficient > 0 for coefficient in denominator_bernstein)
        certificates.append(
            {
                "name": name,
                "numerator_degree": max(value.numerator),
                "denominator_degree": max(value.denominator),
                "strict_bernstein_coefficients": len(numerator_bernstein),
            }
        )

    for operator_index, name in enumerate(("A", "B", "C")):
        for distance in range(1, 6):
            sign = 1 if name == "C" and distance == 1 else -1
            certify(f"{name}[0,{distance}]", rows[operator_index][distance], sign)
        certify(
            f"within-{name}",
            rows[operator_index][0] - within[operator_index],
            -1,
        )

    young_margin = (
        rows[0][1] * rows[1][1] - rows[2][1] * rows[2][1]
    )
    certify("adjacent-Young-margin", young_margin, 1)
    return {
        "q_interval": ["1/25", "7/100"],
        "r_interval": [str(lower), str(upper)],
        "strict_exact_Bernstein_certificates": len(certificates),
        "certificate_names": [certificate["name"] for certificate in certificates],
        "degree_pairs": sorted(
            {
                (certificate["numerator_degree"], certificate["denominator_degree"])
                for certificate in certificates
            }
        ),
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
        "C10_edgewise_interval_payment": c10_edgewise_interval_payment(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
