#!/usr/bin/env python3
"""Exact coefficient certificate for the explicit five-frontier cutoff."""

from __future__ import annotations

from fractions import Fraction
import math


Poly = list[Fraction]
BiPolynomial = dict[tuple[int, int], Fraction]


def trim(values: Poly) -> Poly:
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return values


def add(left: Poly, right: Poly) -> Poly:
    result = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return trim(result)


def scale(value: Fraction, polynomial: Poly) -> Poly:
    return trim([value * coefficient for coefficient in polynomial])


def multiply(left: Poly, right: Poly) -> Poly:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return trim(result)


def power(polynomial: Poly, exponent: int) -> Poly:
    result = [Fraction(1)]
    for _ in range(exponent):
        result = multiply(result, polynomial)
    return result


def shift(polynomial: Poly, exponent: int = 1) -> Poly:
    return [Fraction(0)] * exponent + polynomial


def bi_clean(polynomial: BiPolynomial) -> BiPolynomial:
    return {key: value for key, value in polynomial.items() if value}


def bi_add(left: BiPolynomial, right: BiPolynomial) -> BiPolynomial:
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, Fraction(0)) + value
    return bi_clean(result)


def bi_scale(value: Fraction, polynomial: BiPolynomial) -> BiPolynomial:
    return bi_clean({key: value * coefficient for key, coefficient in polynomial.items()})


def bi_multiply(left: BiPolynomial, right: BiPolynomial) -> BiPolynomial:
    result: BiPolynomial = {}
    for (left_q, left_t), left_value in left.items():
        for (right_q, right_t), right_value in right.items():
            key = (left_q + right_q, left_t + right_t)
            result[key] = result.get(key, Fraction(0)) + left_value * right_value
    return bi_clean(result)


def bi_derivative_t(polynomial: BiPolynomial) -> BiPolynomial:
    return bi_clean(
        {
            (q_degree, t_degree - 1): t_degree * value
            for (q_degree, t_degree), value in polynomial.items()
            if t_degree
        }
    )


class BiRational:
    """Unreduced exact rational function in the formal variables q,t."""

    def __init__(self, numerator: BiPolynomial, denominator: BiPolynomial | None = None) -> None:
        self.numerator = bi_clean(numerator)
        self.denominator = {(0, 0): Fraction(1)} if denominator is None else bi_clean(denominator)

    @staticmethod
    def constant(value: int | Fraction) -> BiRational:
        return BiRational({(0, 0): Fraction(value)})

    def plus(self, other: BiRational) -> BiRational:
        return BiRational(
            bi_add(
                bi_multiply(self.numerator, other.denominator),
                bi_multiply(other.numerator, self.denominator),
            ),
            bi_multiply(self.denominator, other.denominator),
        )

    def scaled(self, value: int | Fraction) -> BiRational:
        return BiRational(bi_scale(Fraction(value), self.numerator), self.denominator)

    def minus(self, other: BiRational) -> BiRational:
        return self.plus(other.scaled(-1))

    def times(self, other: BiRational) -> BiRational:
        return BiRational(
            bi_multiply(self.numerator, other.numerator),
            bi_multiply(self.denominator, other.denominator),
        )

    def divided_by(self, other: BiRational) -> BiRational:
        return BiRational(
            bi_multiply(self.numerator, other.denominator),
            bi_multiply(self.denominator, other.numerator),
        )

    def derivative_t(self) -> BiRational:
        return BiRational(
            bi_add(
                bi_multiply(bi_derivative_t(self.numerator), self.denominator),
                bi_scale(
                    -1,
                    bi_multiply(self.numerator, bi_derivative_t(self.denominator)),
                ),
            ),
            bi_multiply(self.denominator, self.denominator),
        )


def bi_power(value: BiRational, exponent: int) -> BiRational:
    result = BiRational.constant(1)
    for _ in range(exponent):
        result = result.times(value)
    return result


def assert_rational_identity(left: BiRational, right: BiRational) -> None:
    assert bi_multiply(left.numerator, right.denominator) == bi_multiply(
        right.numerator, left.denominator
    )


class RationalTransfer:
    """A polynomial numerator divided by (1-z/2)^power."""

    denominator = [Fraction(1), Fraction(-1, 2)]

    def __init__(self, numerator: Poly, denominator_power: int = 0) -> None:
        self.numerator = trim(numerator)
        self.denominator_power = denominator_power

    def to_power(self, target: int) -> RationalTransfer:
        assert target >= self.denominator_power
        return RationalTransfer(
            multiply(
                self.numerator,
                power(self.denominator, target - self.denominator_power),
            ),
            target,
        )

    def plus(self, other: RationalTransfer) -> RationalTransfer:
        target = max(self.denominator_power, other.denominator_power)
        left = self.to_power(target)
        right = other.to_power(target)
        return RationalTransfer(add(left.numerator, right.numerator), target)

    def scaled(self, value: Fraction) -> RationalTransfer:
        return RationalTransfer(scale(value, self.numerator), self.denominator_power)

    def times_poly(self, polynomial: Poly) -> RationalTransfer:
        return RationalTransfer(multiply(self.numerator, polynomial), self.denominator_power)

    def divided_by_denominator(self) -> RationalTransfer:
        return RationalTransfer(self.numerator, self.denominator_power + 1)

    def divided_by_z(self) -> RationalTransfer:
        assert self.numerator[0] == 0
        return RationalTransfer(self.numerator[1:], self.denominator_power)

    def coefficient(self, index: int) -> Fraction:
        total = Fraction(0)
        for power_index, value in enumerate(self.numerator):
            residual = index - power_index
            if residual < 0:
                continue
            if self.denominator_power == 0:
                total += value * int(residual == 0)
            else:
                total += (
                    value
                    * math.comb(residual + self.denominator_power - 1, self.denominator_power - 1)
                    / 2**residual
                )
        return total

    def value_at_one(self) -> Fraction:
        return sum(self.numerator, Fraction(0)) * 2**self.denominator_power

    def derivative_at_one(self) -> Fraction:
        numerator_value = sum(self.numerator, Fraction(0))
        numerator_derivative = sum(index * value for index, value in enumerate(self.numerator))
        return 2**self.denominator_power * (
            numerator_derivative + self.denominator_power * numerator_value
        )


def transfer_rows(source: str) -> list[RationalTransfer]:
    assert source in {"nu", "a"}
    one = RationalTransfer([Fraction(1)])
    zero = RationalTransfer([Fraction(0)])
    nu = one if source == "nu" else zero
    forcing_a = one if source == "a" else zero
    coefficients = [Fraction(0)] + [
        -Fraction(4, 3) + Fraction((-1) ** distance, 3 * 2**distance) for distance in range(1, 8)
    ]

    y = [zero for _ in range(8)]
    numerator = (
        nu.scaled(-1)
        .plus(forcing_a.scaled(-coefficients[1]))
        .times_poly([Fraction(0), Fraction(1)])
    )
    y[1] = numerator.divided_by_denominator()

    numerator = (
        y[1]
        .times_poly([Fraction(4), Fraction(-1)])
        .plus(forcing_a.times_poly([Fraction(0), coefficients[1]]))
        .times_poly([Fraction(0), Fraction(1)])
        .scaled(Fraction(1, 4))
        .plus(forcing_a.times_poly([Fraction(0), -coefficients[2]]))
    )
    y[2] = numerator.divided_by_denominator()

    for distance in range(3, 8):
        frontier = (
            y[distance - 1]
            .times_poly([Fraction(4), Fraction(-1)])
            .plus(y[distance - 2].times_poly([Fraction(2), Fraction(-2)]))
            .plus(y[distance - 3].times_poly([Fraction(0), Fraction(-1)]))
            .plus(
                forcing_a.times_poly(
                    [
                        Fraction(0),
                        coefficients[distance - 1]
                        + 2 * coefficients[distance - 2]
                        + coefficients[distance - 3],
                    ]
                )
            )
            .times_poly([Fraction(0), Fraction(1)])
            .scaled(Fraction(1, 4))
            .plus(forcing_a.times_poly([Fraction(0), -coefficients[distance]]))
        )
        y[distance] = frontier.divided_by_denominator()

    ell = [zero for _ in range(6)]
    for distance in range(1, 6):
        ell[distance] = (
            y[distance]
            .plus(y[distance + 1].divided_by_z().scaled(-1))
            .plus(forcing_a.scaled(-coefficients[distance + 1]))
        )
    return [
        ell[1],
        ell[2],
        ell[3].plus(ell[1].scaled(Fraction(-1, 4))),
        ell[4].plus(ell[2].scaled(Fraction(-1, 4))),
        ell[5].plus(ell[3].scaled(Fraction(-1, 4))),
    ]


def newton_coefficients(transfer: RationalTransfer, start: int) -> list[Fraction]:
    values = [
        transfer.coefficient(start + offset) * 2 ** (start + offset)
        for offset in range(transfer.denominator_power + 1)
    ]
    result = []
    while values:
        result.append(values[0])
        values = [right - left for left, right in zip(values, values[1:])]
    return result


def absolute_mass_and_moment(
    transfer: RationalTransfer, tail_start: int
) -> tuple[Fraction, Fraction]:
    newton = newton_coefficients(transfer, tail_start)
    assert all(value >= 0 for value in newton) or all(value <= 0 for value in newton)
    tail_sign = 1 if newton[0] >= 0 else -1
    finite_values = [transfer.coefficient(index) for index in range(tail_start)]
    finite_mass = sum((abs(value) for value in finite_values), Fraction(0))
    finite_moment = sum(
        (index * abs(value) for index, value in enumerate(finite_values)),
        Fraction(0),
    )
    finite_signed = sum(finite_values, Fraction(0))
    finite_signed_moment = sum(
        (index * value for index, value in enumerate(finite_values)),
        Fraction(0),
    )
    mass = finite_mass + tail_sign * (transfer.value_at_one() - finite_signed)
    moment = finite_moment + tail_sign * (transfer.derivative_at_one() - finite_signed_moment)
    return mass, moment


def check_raw_input_polynomials() -> None:
    """Expand the four finite-q rational errors from their defining formulas."""

    one = BiRational.constant(1)
    q_variable = BiRational({(1, 0): Fraction(1)})
    t_variable = BiRational({(0, 1): Fraction(1)})
    delta = one.minus(q_variable)
    q_plus = one.plus(q_variable)
    chi = delta.divided_by(q_plus)
    eta = one.minus(bi_power(q_variable, 2)).scaled(Fraction(1, 2))

    def p_q(argument: BiRational) -> BiRational:
        argument_squared = bi_power(argument, 2)
        first = argument.times(one.plus(argument.scaled(Fraction(1, 5)))).divided_by(delta)
        second = argument.minus(BiRational.constant(Fraction(1, 5))).divided_by(q_plus)
        return first.plus(second).scaled(2).divided_by(one.plus(argument_squared))

    def p_zero(argument: BiRational) -> BiRational:
        numerator = bi_power(argument, 2).plus(argument.scaled(10)).minus(one)
        return numerator.scaled(Fraction(2, 5)).divided_by(one.plus(bi_power(argument, 2)))

    def e_zero(argument: BiRational) -> BiRational:
        numerator = bi_power(argument, 2).minus(argument.scaled(10)).plus(BiRational.constant(3))
        return numerator.scaled(Fraction(1, 10)).divided_by(one.plus(bi_power(argument, 2)))

    chi_t = chi.times(t_variable)
    a_zero = (
        e_zero(chi_t)
        .minus(q_variable.scaled(Fraction(1, 10)))
        .divided_by(delta)
        .minus(e_zero(t_variable).minus(q_variable.scaled(Fraction(1, 10))))
        .divided_by(q_variable)
    )

    f_value = (
        bi_power(t_variable, 4)
        .minus(bi_power(t_variable, 3).scaled(30))
        .plus(bi_power(t_variable, 2).scaled(12))
        .plus(t_variable.scaled(10))
        .plus(BiRational.constant(3))
        .scaled(Fraction(1, 10))
        .divided_by(bi_power(one.plus(bi_power(t_variable, 2)), 2))
    )
    g_value = (
        bi_power(t_variable, 4)
        .minus(bi_power(t_variable, 3).scaled(10))
        .plus(bi_power(t_variable, 2).scaled(6))
        .plus(t_variable.scaled(10))
        .plus(one)
        .scaled(Fraction(1, 5))
        .divided_by(bi_power(one.plus(bi_power(t_variable, 2)), 2))
    )

    def mass_ratio(argument: BiRational) -> BiRational:
        argument_squared = bi_power(argument, 2)
        numerator = (
            one.minus(argument_squared)
            .scaled(2)
            .divided_by(one.plus(argument_squared))
            .minus(q_variable.scaled(3))
            .plus(bi_power(q_variable, 3))
        )
        return numerator.divided_by(one.minus(bi_power(q_variable, 2)))

    ratio = mass_ratio(chi_t)
    s_value = eta.scaled(2).minus(q_variable.times(ratio))
    nu_zero = (
        p_q(t_variable)
        .times(ratio)
        .scaled(Fraction(1, 4))
        .plus(delta.times(s_value).plus(eta.scaled(2)).divided_by(eta.times(delta).scaled(10)))
    )

    d_q = p_q(t_variable).minus(p_q(chi_t)).divided_by(q_variable)
    d_zero = t_variable.times(p_zero(t_variable).derivative_t()).scaled(2)

    pa = {
        (2, 5): -15,
        (2, 4): 5,
        (2, 3): -10,
        (2, 2): 6,
        (2, 1): 5,
        (2, 0): 1,
        (1, 5): 40,
        (1, 4): -14,
        (1, 3): -40,
        (1, 2): 4,
        (1, 0): 2,
        (0, 5): -25,
        (0, 4): 13,
        (0, 3): 50,
        (0, 2): -2,
        (0, 1): -5,
        (0, 0): 1,
    }
    pnu = {
        (2, 6): 1,
        (2, 5): -20,
        (2, 4): 11,
        (2, 2): 11,
        (2, 1): 20,
        (2, 0): 1,
        (1, 6): -2,
        (1, 5): 50,
        (1, 4): -24,
        (1, 3): -100,
        (1, 2): 14,
        (1, 1): 10,
        (1, 0): 4,
        (0, 6): 1,
        (0, 5): -30,
        (0, 4): 21,
        (0, 3): 100,
        (0, 2): -9,
        (0, 1): -30,
        (0, 0): 3,
    }
    pp = {(1, 2): 2, (1, 1): 20, (1, 0): -2, (0, 2): 2, (0, 0): 2}
    pd = {
        (3, 5): -40,
        (3, 4): 16,
        (3, 2): 16,
        (3, 1): 40,
        (2, 5): 80,
        (2, 4): -32,
        (2, 3): -160,
        (2, 2): 32,
        (2, 1): 80,
        (0, 5): -40,
        (0, 4): 32,
        (0, 3): 240,
        (0, 2): -32,
        (0, 1): -40,
    }
    pa = {key: Fraction(value) for key, value in pa.items()}
    pnu = {key: Fraction(value) for key, value in pnu.items()}
    pp = {key: Fraction(value) for key, value in pp.items()}
    pd = {key: Fraction(value) for key, value in pd.items()}

    one_plus_t_squared = one.plus(bi_power(t_variable, 2))
    bracket = delta.times(delta).times(bi_power(t_variable, 2)).plus(q_plus.times(q_plus))
    common = bi_power(one_plus_t_squared, 2).times(bracket)
    expected_a = q_variable.times(BiRational(pa)).divided_by(delta.times(common).scaled(5))
    expected_nu = q_variable.times(BiRational(pnu)).divided_by(delta.times(common).scaled(10))
    expected_p = q_variable.times(BiRational(pp)).divided_by(
        one.minus(bi_power(q_variable, 2)).times(one_plus_t_squared).scaled(5)
    )
    expected_d = q_variable.times(BiRational(pd)).divided_by(
        one.minus(bi_power(q_variable, 2)).times(common).scaled(5)
    )
    assert_rational_identity(a_zero.minus(f_value), expected_a)
    assert_rational_identity(nu_zero.minus(g_value), expected_nu)
    assert_rational_identity(p_q(t_variable).minus(p_zero(t_variable)), expected_p)
    assert_rational_identity(d_q.minus(d_zero), expected_d)

    assert sum(abs(value) for value in pa.values()) == 238
    assert sum(abs(value) for value in pnu.values()) == 462
    assert sum(abs(value) for value in pp.values()) == 28
    assert sum(abs(value) for value in pd.values()) == 880
    assert sum(t_degree * abs(value) for (_, t_degree), value in pa.items()) == 862
    assert sum(t_degree * abs(value) for (_, t_degree), value in pnu.items()) == 1476
    print("frontier_cutoff_raw_polynomials=PASS l1=238,462,28,880 t_derivative_l1=862,1476")


def check_transfer_kernels() -> None:
    expected_mass = {
        "nu": [Fraction(1), Fraction(3, 2), Fraction(9, 8), Fraction(11, 8), Fraction(79, 64)],
        "a": [Fraction(2), Fraction(19, 8), Fraction(63, 32), Fraction(31, 16), Fraction(123, 64)],
    }
    expected_moment = {
        "nu": [Fraction(4), Fraction(13, 2), Fraction(63, 8), Fraction(321, 32), Fraction(375, 32)],
        "a": [
            Fraction(7),
            Fraction(91, 8),
            Fraction(451, 32),
            Fraction(557, 32),
            Fraction(333, 16),
        ],
    }
    expected_signed = {
        "nu": [Fraction(1), Fraction(3, 2), Fraction(1), Fraction(1), Fraction(1)],
        "a": [
            Fraction(-2),
            Fraction(-19, 8),
            Fraction(-13, 8),
            Fraction(-27, 16),
            Fraction(-53, 32),
        ],
    }
    for source in ("nu", "a"):
        transfers = transfer_rows(source)
        for index, transfer in enumerate(transfers):
            assert transfer.value_at_one() == expected_signed[source][index]
            mass, moment = absolute_mass_and_moment(transfer, 2 * (index + 1))
            assert mass == expected_mass[source][index]
            assert moment == expected_moment[source][index]
    print("frontier_cutoff_transfer=PASS l1_masses=exact first_moments=exact")


def check_input_and_endpoint_constants() -> None:
    q_max = Fraction(1, 1024)
    # Coefficient-l1 bounds for the exact rational errors
    # (a0-f)/q, (nu0-g)/q, (p_q-p0)/q, and (Dp-D0)/q.
    assert Fraction(238, 5) / (1 - q_max) < 48
    assert Fraction(462, 10) / (1 - q_max) < 47
    assert Fraction(28, 5) / (1 - q_max**2) < 6
    assert Fraction(880, 5) / (1 - q_max**2) < 177
    # Derivative numerators plus a denominator-log-derivative bound four.
    assert Fraction(96, 5) + q_max * Fraction(862 + 4 * 238, 5) / (1 - q_max) < 20
    assert Fraction(96, 5) + q_max * Fraction(1476 + 4 * 462, 10) / (1 - q_max) < 20
    assert Fraction(16, 15) * (Fraction(28, 5) + 48 * q_max) < 7
    assert Fraction(16, 15) * (Fraction(28, 5) + 47 * q_max) < 7
    # Adjacent A and t changes then give the safe common bound 51q.
    assert Fraction(16, 15) / (1 - q_max) * 7 + Fraction(16, 15) * 40 < 51

    locality = Fraction(375, 32) * 57 + Fraction(333, 16) * 129
    assert locality < 3353
    local_error = Fraction(3, 2) * 47 + Fraction(19, 8) * 48
    assert local_error == Fraction(369, 2) < 185

    h_predivision = (
        Fraction(177, 2) + q_max * Fraction(21, 2) + (3 + q_max) * 26 / 2 + 2 + Fraction(1, 5)
    )
    assert h_predivision < 130
    h_error = (h_predivision + 20) / (1 + q_max)
    assert h_error < 150
    endpoint_recurrence_error = 150 + 86 + 20
    assert endpoint_recurrence_error == 256
    assert 2 * endpoint_recurrence_error + 1 == 513
    assert Fraction(2, q_max**2 * 2**63) < q_max

    b_local_error = Fraction(177 + 6, 4) + q_max * Fraction(20 + 2, 4)
    assert b_local_error < 46
    z_coefficient_error = Fraction(513, 2) + 20 * q_max
    assert z_coefficient_error < 257
    b_error = b_local_error + Fraction(1, 5) + z_coefficient_error + 1
    assert b_error < 305
    assert b_error / 4 < 77
    assert 3353 + 185 + 77 + 24 < 3654
    print("frontier_cutoff_inputs=PASS adjacent_a_nu<=51q endpoint_B<=305q total_forcing<3654q")


def homogeneous_step(previous: list[Fraction], current: list[Fraction]) -> list[Fraction]:
    """One zero-forcing step of the seven-coordinate frontier system."""

    following = [Fraction(0)] * 8
    following[1] = current[1] / 2
    following[2] = (2 * current[2] + 4 * current[1] - previous[1]) / 4
    for distance in range(3, 8):
        following[distance] = (
            2 * current[distance]
            + 4 * current[distance - 1]
            + 2 * current[distance - 2]
            - previous[distance - 1]
            - 2 * previous[distance - 2]
            - previous[distance - 3]
        ) / 4
    return following


def homogeneous_outputs(
    previous: list[Fraction], current: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    following = homogeneous_step(previous, current)
    local = [Fraction(0)] * 6
    for distance in range(1, 6):
        local[distance] = current[distance] - following[distance + 1]
    combined = [
        local[1],
        local[2],
        local[3] - local[1] / 4,
        local[4] - local[2] / 4,
        local[5] - local[3] / 4,
    ]
    return combined, following


def check_homogeneous_transient() -> None:
    """Reconstruct all fourteen basis transfers over (1-z/2)^7."""

    denominator_seven = [
        Fraction(math.comb(7, exponent) * (-1) ** exponent, 2**exponent) for exponent in range(8)
    ]
    weighted_numerator_norms = [Fraction(0)] * 5
    maximum_numerator_degree = 0
    sample_count = 30

    previous_seed = [Fraction(0)] * 8
    previous_seed[1] = Fraction(1)
    seed_outputs, _ = homogeneous_outputs(previous_seed, [Fraction(0)] * 8)
    assert seed_outputs == [
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(3, 16),
        Fraction(-1, 8),
        Fraction(-1, 16),
    ]

    for state_name in ("previous", "current"):
        for coordinate in range(1, 8):
            previous = [Fraction(0)] * 8
            current = [Fraction(0)] * 8
            (previous if state_name == "previous" else current)[coordinate] = Fraction(1)
            coefficient_sequences = [[] for _ in range(5)]
            for _ in range(sample_count):
                outputs, following = homogeneous_outputs(previous, current)
                for output_index, value in enumerate(outputs):
                    coefficient_sequences[output_index].append(value)
                previous, current = current, following

            for output_index, sequence in enumerate(coefficient_sequences):
                numerator = []
                for lag in range(sample_count):
                    numerator.append(
                        sum(
                            (
                                denominator_seven[exponent] * sequence[lag - exponent]
                                for exponent in range(min(7, lag) + 1)
                            ),
                            Fraction(0),
                        )
                    )
                nonzero = [index for index, value in enumerate(numerator) if value]
                if nonzero:
                    maximum_numerator_degree = max(maximum_numerator_degree, max(nonzero))
                assert all(value == 0 for value in numerator[11:])
                weighted_numerator_norms[output_index] += sum(
                    (2**index * abs(value) for index, value in enumerate(numerator[:11])),
                    Fraction(0),
                )

    assert maximum_numerator_degree == 10
    assert weighted_numerator_norms == [
        Fraction(64),
        Fraction(176),
        Fraction(987, 4),
        Fraction(2743, 8),
        Fraction(477),
    ]
    print(
        "frontier_cutoff_transient=PASS bases=14 denominator_power=7 "
        "weighted_numerator_norms=64,176,987/4,2743/8,477"
    )


def check_transient_and_cutoff() -> None:
    def transient(edge_count: int) -> Fraction:
        lag = edge_count - 7
        q = Fraction(1, 16 * edge_count)
        return Fraction(100, 1) / q * 477 * math.comb(lag + 6, 6) / 2**lag

    assert transient(80) < Fraction(1, 1000)
    # The ratio at m+1 over m is (m+1)/(2(m-6)), hence decreases for m>=80.
    assert Fraction(81, 2 * 74) < 1

    lower_denominator = Fraction(113, 64)
    delta_and_terminal_loss = (
        Fraction(51, 2) / lower_denominator**3 * Fraction(2, 1) / (1 - 2 * Fraction(1, 1024))
        + Fraction(251, 40) / lower_denominator**2
    )
    assert delta_and_terminal_loss < 24

    cutoff = 8192
    total_error = Fraction(3654, 16 * cutoff) + Fraction(1, 1000)
    assert total_error < Fraction(1, 12)
    assert Fraction(1, 3) - total_error > 0
    print(f"frontier_cutoff_margin=PASS cutoff={cutoff} error<{total_error} baseline>=1/3")


def main() -> None:
    check_transfer_kernels()
    check_raw_input_polynomials()
    check_input_and_endpoint_constants()
    check_homogeneous_transient()
    check_transient_and_cutoff()
    print("terminal_static_frontier_cutoff=PASS m_ge_8192=PROVED")


if __name__ == "__main__":
    main()
