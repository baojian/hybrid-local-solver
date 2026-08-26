#!/usr/bin/env python3
"""Deterministic floating screen for the short-path terminal candidate.

The script writes no artifacts. It reconstructs the actual transported-center
admission chronology and uses the literal global residual range on the full
face. Its output is measured float64 evidence, not an exact proof.
"""

from __future__ import annotations

import argparse
import math
from fractions import Fraction

import numpy as np


def _fraction_h_apply(
    z: list[Fraction],
    degrees: list[Fraction],
    q: Fraction,
) -> list[Fraction]:
    """Apply the normalized path operator in exact rational arithmetic."""
    a = (1 + q * q) / 2
    eta = (1 - q * q) / 2
    out = [a * value for value in z]
    for index in range(1, len(z)):
        out[index] -= eta * z[index - 1] / degrees[index]
    for index in range(len(z) - 1):
        out[index] -= eta * z[index + 1] / degrees[index]
    return out


def _fraction_load(length: int, q: Fraction) -> list[Fraction]:
    out = [-(q**3) / 5 for _ in range(length)]
    out[0] += q * q
    return out


def _fraction_residual(
    z: list[Fraction],
    degrees: list[Fraction],
    q: Fraction,
) -> list[Fraction]:
    return [
        left - right
        for left, right in zip(
            _fraction_h_apply(z, degrees, q),
            _fraction_load(len(z), q),
            strict=True,
        )
    ]


def _fraction_optimum(
    length: int,
    degrees: list[Fraction],
    q: Fraction,
) -> list[Fraction]:
    """Exact Thomas solve for a restricted optimum."""
    a = (1 + q * q) / 2
    eta = (1 - q * q) / 2
    right = _fraction_load(length, q)
    diagonal = [a for _ in range(length)]
    upper = [-eta / degrees[index] for index in range(length - 1)]
    lower = [-eta / degrees[index] for index in range(1, length)]
    for index in range(1, length):
        multiplier = lower[index - 1] / diagonal[index - 1]
        diagonal[index] -= multiplier * upper[index - 1]
        right[index] -= multiplier * right[index - 1]
    answer = [Fraction(0) for _ in range(length)]
    answer[-1] = right[-1] / diagonal[-1]
    for index in range(length - 2, -1, -1):
        answer[index] = (right[index] - upper[index] * answer[index + 1]) / diagonal[index]
    return answer


def _fraction_step(
    p: list[Fraction],
    v: list[Fraction],
    degrees: list[Fraction],
    q: Fraction,
) -> tuple[list[Fraction], list[Fraction]]:
    y = [(left + q * right) / (1 + q) for left, right in zip(p, v, strict=True)]
    residual_y = _fraction_residual(y, degrees, q)
    raw = [left - right for left, right in zip(y, residual_y, strict=True)]
    assert min(raw) >= 0
    v_next = [
        current + (1 - q) * (current - previous) / q
        for current, previous in zip(raw, p, strict=True)
    ]
    return raw, v_next


def _fraction_stencil(
    values: list[Fraction],
    length: int,
    coefficient: Fraction,
) -> list[Fraction]:
    padded = values + [Fraction(0) for _ in range(length - len(values))]
    return [
        coefficient
        * (
            2 * padded[index]
            + (padded[index - 1] if index else 0)
            + (padded[index + 1] if index + 1 < length else 0)
        )
        for index in range(length)
    ]


def _polynomial_add(
    left: dict[int, Fraction],
    right: dict[int, Fraction],
    right_scale: Fraction = Fraction(1),
) -> dict[int, Fraction]:
    out = dict(left)
    for exponent, coefficient in right.items():
        out[exponent] = out.get(exponent, Fraction(0)) + right_scale * coefficient
        if out[exponent] == 0:
            del out[exponent]
    return out


def _polynomial_product(
    left: dict[int, Fraction],
    right: dict[int, Fraction],
) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            out[exponent] = out.get(exponent, Fraction(0)) + left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in out.items() if coefficient}


def _even_polynomial(values: list[Fraction]) -> dict[int, Fraction]:
    out = {0: values[0]}
    for index, value in enumerate(values[1:], start=1):
        if value:
            out[index] = value
            out[-index] = value
    return {exponent: coefficient for exponent, coefficient in out.items() if coefficient}


def exact_boundary_source_checks() -> None:
    """Check the sparse source and its formal transform over the rationals."""
    edge_count = 8
    q = Fraction(1, 16 * edge_count)
    rho = q / 5
    eta = (1 - q * q) / 2
    a = (1 + q * q) / 2
    chi = (1 - q) / (1 + q)
    degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]

    def f(index: int) -> Fraction:
        return chi**index + chi ** (-index)

    def b(index: int) -> Fraction:
        if index == 0:
            return (rho - q) / 2
        return (rho - q * chi**index) / (chi**index + chi ** (-index))

    entries: dict[int, list[Fraction]] = {}
    optima: dict[int, list[Fraction]] = {}
    residuals: dict[int, list[Fraction]] = {}
    p = [Fraction(0)]
    v = [Fraction(0)]
    for length in range(1, edge_count + 1):
        optimum = _fraction_optimum(length, degrees, q)
        entries[length] = p
        optima[length] = optimum
        residuals[length] = _fraction_residual(p, degrees[:length], q)
        p_next, v_next = _fraction_step(p, v, degrees[:length], q)
        new_optimum = _fraction_optimum(length + 1, degrees, q)
        p = p_next + [Fraction(0)]
        v = v_next + [Fraction(0)]
        v = [
            value + new_value - old_value
            for value, new_value, old_value in zip(
                v,
                new_optimum,
                optimum + [Fraction(0)],
                strict=True,
            )
        ]
    entries[edge_count + 1] = p
    optima[edge_count + 1] = _fraction_optimum(edge_count + 1, degrees, q)
    residuals[edge_count + 1] = _fraction_residual(p, degrees, q)

    c1 = (1 - q) / 2
    c2 = (1 - q) ** 2 / 4
    r_plus = {0: c1, 1: c1}
    r_minus = {0: c1, -1: c1}
    first_operator = _polynomial_add(r_plus, r_minus)
    second_operator = _polynomial_product(r_plus, r_minus)

    for prefix in (4, 6, 7, edge_count):
        length = prefix + 1
        first = _fraction_stencil(residuals[prefix], length, c1)
        second = _fraction_stencil(residuals[prefix - 1], length, c2)
        defect = [
            residuals[length][index] - first[index] + second[index] for index in range(length)
        ]
        delta = b(prefix) - b(prefix - 1)
        p_frontier = optima[prefix][-1]
        previous_frontier = optima[prefix - 1][-1]
        u_value = q * eta**2 / (4 * (1 + q)) * (previous_frontier - 2 * q * rho / eta)
        assert 0 < u_value <= Fraction(3, 40) * q**3
        expected: dict[int, Fraction] = {
            0: c1 * residuals[prefix][1] - c2 * residuals[prefix - 1][1],
            prefix - 2: u_value,
            prefix - 1: 2 * u_value,
        }
        if prefix < edge_count:
            next_delta = b(prefix + 1) - b(prefix)
            w_value = (
                u_value
                + c1 * p_frontier
                - a * delta * f(prefix) / (1 + q)
                + eta / 2 * (delta / (1 + q) - next_delta) * f(prefix + 1)
            )
            s_value = f(prefix - 1) / f(prefix)
            d_value = 2 * q * q * rho / eta
            mass = w_value + 3 * u_value
            exact_mass = (
                q * (1 - q) / 4 * (2 * eta - s_value) * previous_frontier
                + q / 4 * ((1 - q) * s_value + 2 * eta) * d_value
            )
            assert mass == exact_mass
            assert abs(mass) <= Fraction(3, 2) * q**4
        else:
            w_value = (
                c1 * residuals[prefix][-1]
                + (1 - q) ** 2 / 2 * p_frontier
                - eta * (1 - q) ** 2 / 4 * previous_frontier
                - delta * eta**2 / (1 + q) * (f(prefix - 1) + f(prefix - 2) / 2)
                + q**3 / 5
            )
        expected[prefix] = w_value
        assert all(value == expected.get(index, Fraction(0)) for index, value in enumerate(defect))

        formal_defect = _even_polynomial(residuals[length])
        formal_defect = _polynomial_add(
            formal_defect,
            _polynomial_product(first_operator, _even_polynomial(residuals[prefix])),
            Fraction(-1),
        )
        formal_defect = _polynomial_add(
            formal_defect,
            _polynomial_product(
                second_operator,
                _even_polynomial(residuals[prefix - 1]),
            ),
        )
        expected_even: dict[int, Fraction] = {}
        for index in (prefix - 2, prefix - 1, prefix):
            expected_even[index] = expected[index]
            expected_even[-index] = expected[index]
        assert formal_defect == expected_even

        if prefix < edge_count:
            factored_positive = {
                prefix - 2: u_value,
                prefix - 1: 2 * u_value,
                prefix: mass - 3 * u_value,
            }
            assert factored_positive[prefix] == w_value

    print(
        "exact_boundary_source_checks=m=8 n=4,6,7,8 "
        "support=pass entries=pass formal_transform=pass arithmetic=Fraction"
    )


def h_apply(z: np.ndarray, degrees: np.ndarray, q: float) -> np.ndarray:
    """Apply D^(-1/2) Q D^(1/2) in normalized path coordinates."""
    a = (1.0 + q * q) / 2.0
    eta = (1.0 - q * q) / 2.0
    out = a * z.copy()
    out[1:] -= eta * z[:-1] / degrees[1:]
    out[:-1] -= eta * z[1:] / degrees[:-1]
    return out


def normalized_load(length: int, q: float) -> np.ndarray:
    """Return the affine RPPR load with rho=q/5 and endpoint seed zero."""
    out = np.full(length, -(q**3) / 5.0)
    out[0] += q * q
    return out


def residual(z: np.ndarray, degrees: np.ndarray, q: float) -> np.ndarray:
    return h_apply(z, degrees, q) - normalized_load(len(z), q)


def restricted_optimum(length: int, degrees: np.ndarray, q: float) -> np.ndarray:
    """Thomas solve for one normalized restricted optimum."""
    a = (1.0 + q * q) / 2.0
    eta = (1.0 - q * q) / 2.0
    right = normalized_load(length, q)
    diagonal = np.full(length, a)
    upper = -eta / degrees[: length - 1]
    lower = -eta / degrees[1:length]
    for index in range(1, length):
        multiplier = lower[index - 1] / diagonal[index - 1]
        diagonal[index] -= multiplier * upper[index - 1]
        right[index] -= multiplier * right[index - 1]
    answer = np.empty(length)
    answer[-1] = right[-1] / diagonal[-1]
    for index in range(length - 2, -1, -1):
        answer[index] = (right[index] - upper[index] * answer[index + 1]) / diagonal[index]
    return answer


def one_step(
    p: np.ndarray,
    v: np.ndarray,
    degrees: np.ndarray,
    q: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    y = (p + q * v) / (1.0 + q)
    raw = y - residual(y, degrees, q)
    p_next = np.maximum(raw, 0.0)
    v_next = p_next + (1.0 - q) * (p_next - p) / q
    return p_next, v_next, raw


def full_face_entry(
    edge_count: int,
) -> tuple[
    float,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    list[np.ndarray],
    float,
    float,
]:
    """Replay one fixed-face step and one transported singleton per prefix."""
    q = 1.0 / (16.0 * edge_count)
    degrees = np.r_[1.0, np.full(edge_count - 1, 2.0), 1.0]
    p = np.zeros(1)
    v = np.zeros(1)
    prefix_residuals = []
    last_proper_error = None
    last_proper_frontier = None
    for length in range(1, edge_count + 1):
        prefix_residuals.append(residual(p, degrees[:length], q))
        p_next, v_next, raw = one_step(p, v, degrees[:length], q)
        assert raw.min() >= -1.0e-14, f"projection active during admission {length}"
        r_next = residual(p_next, degrees[:length], q)
        delta = max(0.0, r_next.max() / (q * q))
        assert delta <= 1.0e-12, f"nonzero admission correction at prefix {length}"
        outside = -(1.0 - q * q) * p_next[-1] / (2.0 * degrees[length]) + q**3 / 5.0
        assert outside < -(q**3) / 5.0, f"next vertex not strongly admitted at prefix {length}"
        old_optimum = restricted_optimum(length, degrees, q)
        new_optimum = restricted_optimum(length + 1, degrees, q)
        if length == edge_count:
            last_proper_error = float(p[-1] - old_optimum[-1])
            last_proper_frontier = float(old_optimum[-1])
        p = np.r_[p_next, 0.0]
        v = np.r_[v_next, 0.0] + new_optimum - np.r_[old_optimum, 0.0]
    prefix_residuals.append(residual(p, degrees, q))
    assert last_proper_error is not None
    assert last_proper_frontier is not None
    return (
        q,
        degrees,
        p,
        v,
        prefix_residuals,
        last_proper_error,
        last_proper_frontier,
    )


def cosine_coefficients(r: np.ndarray, degrees: np.ndarray) -> np.ndarray:
    """Return coefficients in the degree-weighted path cosine basis."""
    edge_count = len(r) - 1
    vertices = np.arange(edge_count + 1)
    coefficients = np.empty(edge_count + 1)
    for mode in range(edge_count + 1):
        norm = 2.0 * edge_count if mode in (0, edge_count) else edge_count
        cosine = np.cos(math.pi * mode * vertices / edge_count)
        coefficients[mode] = np.dot(degrees * r, cosine) / norm
    return coefficients


def binomial_probabilities(edge_count: int) -> np.ndarray:
    """Compute a stable Binomial(edge_count, 1/2) probability vector."""
    return np.array(
        [
            math.exp(
                math.lgamma(edge_count + 1)
                - math.lgamma(index + 1)
                - math.lgamma(edge_count - index + 1)
                - edge_count * math.log(2.0)
            )
            for index in range(edge_count + 1)
        ]
    )


def five_piece_decomposition(
    prefix_residuals: list[np.ndarray],
    proper_error_last: float,
    proper_frontier: float,
    q: float,
) -> tuple[dict[str, float], dict[str, float]]:
    """Measure the exact linear five-piece split at the first even mode."""
    edge_count = len(prefix_residuals) - 1
    theta = 2.0 * math.pi / edge_count
    phi = theta / 2.0
    first_coefficient = 2.0 * (1.0 - q) * math.cos(phi) ** 2
    second_coefficient = (1.0 - q) ** 2 * math.cos(phi) ** 2
    transforms: list[float | None] = [None]
    for values in prefix_residuals:
        transforms.append(
            float(values[0])
            + 2.0
            * sum(float(values[index]) * math.cos(theta * index) for index in range(1, len(values)))
        )

    names = ("base", "constant_u", "delta_u", "mass", "endpoint")
    components = {name: [0.0, 0.0, 0.0] for name in names}
    components["base"][1] = float(transforms[1])
    components["base"][2] = float(transforms[2])
    constant_u = 3.0 * q**3 / 40.0

    def stencil(values: np.ndarray, length: int, coefficient: float) -> np.ndarray:
        padded = np.zeros(length)
        padded[: len(values)] = values
        return coefficient * (2.0 * padded + np.r_[0.0, padded[:-1]] + np.r_[padded[1:], 0.0])

    for prefix in range(2, edge_count + 1):
        source = {
            "base": 0.0,
            "constant_u": 0.0,
            "delta_u": 0.0,
            "mass": 0.0,
            "endpoint": 0.0,
        }
        full_source = (
            float(transforms[prefix + 1])
            - first_coefficient * float(transforms[prefix])
            + second_coefficient * float(transforms[prefix - 1])
        )
        if prefix <= 3:
            source["base"] = full_source
        elif prefix < edge_count:
            defect = (
                prefix_residuals[prefix]
                - stencil(
                    prefix_residuals[prefix - 1],
                    prefix + 1,
                    (1.0 - q) / 2.0,
                )
                + stencil(
                    prefix_residuals[prefix - 2],
                    prefix + 1,
                    (1.0 - q) ** 2 / 4.0,
                )
            )
            u_value = float(defect[prefix - 2])
            mass = float(defect[prefix] + 3.0 * u_value)

            def u_transform(value: float) -> float:
                return (
                    2.0
                    * value
                    * (
                        math.cos((prefix - 2) * theta)
                        + 2.0 * math.cos((prefix - 1) * theta)
                        - 3.0 * math.cos(prefix * theta)
                    )
                )

            source["constant_u"] = u_transform(constant_u)
            source["delta_u"] = u_transform(u_value - constant_u)
            source["mass"] = 2.0 * mass * math.cos(prefix * theta)
            assert abs(full_source - sum(source.values())) <= 1.0e-12
        else:
            source["endpoint"] = full_source

        for name in names:
            components[name].append(
                first_coefficient * components[name][prefix]
                - second_coefficient * components[name][prefix - 1]
                + source[name]
            )

    ideal = (
        -(q * q)
        * (1.0 - q) ** edge_count
        * (-(math.cos(phi) ** edge_count) - math.ldexp(1.0, -edge_count))
    )
    final_endpoint = float(prefix_residuals[-1][-1])
    position = {name: components[name][edge_count + 1] / q**2 for name in names}
    position["base"] -= ideal / q**2
    position["endpoint"] -= final_endpoint / q**2

    velocity = {
        name: (components[name][edge_count + 1] - (1.0 - q) * components[name][edge_count]) / q**3
        for name in names
    }
    velocity["base"] += ideal / (5.0 * q**2)
    eta = (1.0 - q * q) / 2.0
    kappa = eta * proper_frontier - q**3 / 5.0
    velocity["endpoint"] += (-final_endpoint + kappa + (1.0 - q) * eta * proper_error_last) / q**3
    return position, velocity


def check_signed_green_formula() -> None:
    """Check the closed constant-U Green sums and their fixed-mode limits."""

    for edge_count in (5, 8, 17, 32, 65, 257):
        q = 1.0 / (16.0 * edge_count)
        eta = (1.0 - q**2) / 2.0
        chi = (1.0 - q) / (1.0 + q)
        constant_u = 3.0 * q**3 / 40.0
        u_values = []
        for prefix in range(4, edge_count):
            t_value = chi ** (prefix - 1)
            previous_frontier = (
                q**2
                * 2.0
                / (1.0 + q)
                * (t_value * (1.0 + t_value / 5.0) / chi + t_value - 1.0 / 5.0)
                / (1.0 + t_value**2)
            )
            u_values.append(
                q * eta**2 / (4.0 * (1.0 + q)) * (previous_frontier - 2.0 * q**2 / (5.0 * eta))
            )
        assert all(left >= right for left, right in zip(u_values, u_values[1:]))
        assert max(constant_u - value for value in u_values) <= q**3 / 150.0
        total_variation = sum(abs(right - left) for left, right in zip(u_values, u_values[1:]))
        assert total_variation <= q**3 / 150.0

    def finite_sums(edge_count: int, mode_index: int) -> tuple[float, float, float, float]:
        q = 1.0 / (16.0 * edge_count)
        gamma = 1.0 - q
        theta = 2.0 * math.pi * mode_index / edge_count
        phi = theta / 2.0
        z_value = complex(math.cos(theta), math.sin(theta))
        root = gamma * (1.0 + z_value) / 2.0
        constant_u = 3.0 * q**3 / 40.0

        def sigma_sum(value: complex, length: int) -> complex:
            return value * (1.0 - value**length) / (1.0 - value)

        def gamma_sum(value: complex, length: int) -> complex:
            return (1.0 - value ** (length + 1)) / (1.0 - value)

        closed_position = (
            2.0
            * constant_u
            * (
                (1.0 + 3.0 * z_value)
                * (
                    z_value**-2 * sigma_sum(root * z_value**-2, edge_count - 4)
                    - z_value**-1 * sigma_sum(root * z_value**-1, edge_count - 4)
                )
            ).real
        )
        closed_previous = (
            2.0
            * constant_u
            * (
                (1.0 + 3.0 * z_value)
                * (
                    z_value**-3 * gamma_sum(root * z_value**-2, edge_count - 5)
                    - z_value**-2 * gamma_sum(root * z_value**-1, edge_count - 5)
                )
            ).real
        )

        radius = gamma * math.cos(phi)
        direct_position = 0.0
        direct_previous = 0.0
        for prefix in range(4, edge_count):
            source = (
                2.0
                * constant_u
                * (z_value ** (prefix - 2) * (1.0 - z_value) * (1.0 + 3.0 * z_value)).real
            )
            lag = edge_count - prefix
            direct_position += source * radius**lag * math.sin((lag + 1) * phi) / math.sin(phi)
            direct_previous += source * radius ** (lag - 1) * math.sin(lag * phi) / math.sin(phi)
        return closed_position, closed_previous, direct_position, direct_previous

    cells = 0
    for edge_count in (8, 17, 32, 65):
        for mode_index in range(1, min(4, (edge_count - 1) // 2) + 1):
            closed_position, closed_previous, direct_position, direct_previous = finite_sums(
                edge_count, mode_index
            )
            scale = (1.0 / (16.0 * edge_count)) ** 3
            assert abs(closed_position - direct_position) <= 2.0e-11 * scale
            assert abs(closed_previous - direct_previous) <= 2.0e-11 * scale
            cells += 1

    edge_count = 262_144
    a_value = 1.0 / 16.0
    exponential = math.exp(-a_value)
    for mode_index in (1, 2, 3):
        closed_position, closed_previous, _, _ = finite_sums(edge_count, mode_index)
        q = 1.0 / (16.0 * edge_count)
        sigma = (-1.0) ** mode_index
        b_value = math.pi * mode_index
        position_limit = (
            3.0
            * a_value
            * (sigma * exponential - 1.0)
            / 80.0
            * (1.0 / (a_value**2 + b_value**2) - 1.0 / (a_value**2 + 9.0 * b_value**2))
        )
        velocity_limit = (
            3.0
            * sigma
            * b_value**2
            * (exponential - sigma)
            / 5.0
            * (1.0 / (a_value**2 + b_value**2) + 3.0 / (a_value**2 + 9.0 * b_value**2))
        )
        observed_position = closed_position / q**2
        observed_velocity = (closed_position - (1.0 - q) * closed_previous) / q**3
        assert abs(observed_position - position_limit) <= 3.0e-7
        assert abs(observed_velocity - velocity_limit) <= 2.0e-4

    print(
        f"signed_green_formula_checks=6 variation cells + {cells} finite cells "
        "+ 3 fixed-mode limits"
    )


def screen(edge_count: int, max_qk: float) -> None:
    (
        q,
        degrees,
        p,
        v,
        prefix_residuals,
        proper_error_last,
        proper_frontier,
    ) = full_face_entry(edge_count)
    r_zero = residual(p, degrees, q)
    packet = -(q * q / 2.0) * (1.0 - q) ** edge_count * binomial_probabilities(edge_count)
    packet_error = r_zero - packet

    p_one, _, raw_one = one_step(p, v, degrees, q)
    assert raw_one.min() > 0.0
    r_one = residual(p_one, degrees, q)
    coefficient_zero = cosine_coefficients(r_zero, degrees)
    coefficient_velocity = cosine_coefficients(residual(v, degrees, q), degrees)
    coefficient_one = cosine_coefficients(r_one, degrees)
    band = min(
        (edge_count - 1) // 2,
        max(1, int(math.sqrt(edge_count / max(1.0, math.log(edge_count))))),
    )
    lemma_band = int(math.sqrt(edge_count / (64.0 * math.log(16.0 * edge_count))))
    relative_defects = []
    position_profiles = []
    velocity_correction_profiles = []
    combined_lemma_defects = []
    lemma_position_profiles = []
    lemma_velocity_correction_profiles = []
    quadrature_consistency = []
    first_position_signed = None
    first_velocity_correction_signed = None
    first_quadrature_relative = None
    for index in range(1, band + 1):
        mode = 2 * index
        phi = mode * math.pi / (2.0 * edge_count)
        radius = (1.0 - q) * math.cos(phi)
        quadrature_from_first_step = (
            coefficient_one[mode] / radius - coefficient_zero[mode] * math.cos(phi)
        ) / math.sin(phi)
        quadrature = q * coefficient_velocity[mode] / math.tan(phi)
        endpoint_mass = math.ldexp(1.0, -edge_count)
        signed_ideal = (
            -(q * q / edge_count)
            * (1.0 - q) ** edge_count
            * ((-1.0) ** index * math.cos(phi) ** edge_count - endpoint_mass)
        )
        ideal_amplitude = abs(signed_ideal)
        position_profile = edge_count * abs(coefficient_zero[mode] - signed_ideal) / q**2
        velocity_correction_profile = (
            edge_count * abs(coefficient_velocity[mode] + signed_ideal / 5.0) / q**2
        )
        position_profiles.append(position_profile)
        velocity_correction_profiles.append(velocity_correction_profile)
        quadrature_consistency.append(
            abs(quadrature - quadrature_from_first_step) / ideal_amplitude
        )
        if index == 1:
            first_position_signed = edge_count * (coefficient_zero[mode] - signed_ideal) / q**2
            first_velocity_correction_signed = (
                edge_count * (coefficient_velocity[mode] + signed_ideal / 5.0) / q**2
            )
            first_quadrature_relative = quadrature / signed_ideal
        relative_defects.append(
            max(
                abs(coefficient_zero[mode] - signed_ideal),
                abs(quadrature),
            )
            / ideal_amplitude
        )
        if index <= lemma_band:
            lemma_position_profiles.append(position_profile)
            lemma_velocity_correction_profiles.append(velocity_correction_profile)
            combined_lemma_defects.append(
                (abs(coefficient_zero[mode] - signed_ideal) + abs(quadrature)) / ideal_amplitude
            )

    if combined_lemma_defects:
        maximum_combined_lemma_defect = max(combined_lemma_defects)
        assert maximum_combined_lemma_defect <= 1.0 / 64.0
        lemma_check = f"{maximum_combined_lemma_defect:.6g}<=1/64"
        maximum_lemma_position_profile = max(lemma_position_profiles)
        maximum_lemma_velocity_profile = max(lemma_velocity_correction_profiles)
        assert maximum_lemma_position_profile <= 1.0 / 256.0
        assert maximum_lemma_velocity_profile <= 1.0 / 4.0
        profile_check = (
            f"C={maximum_lemma_position_profile:.6g}<=1/256 "
            f"V={maximum_lemma_velocity_profile:.6g}<=1/4"
        )
    else:
        lemma_check = "vacuous(H_m=0)"
        profile_check = "vacuous(H_m=0)"

    maximum_quadrature_consistency = max(quadrature_consistency)
    assert maximum_quadrature_consistency <= 1.0e-6

    first_range_crossing = None
    first_certificate = None
    min_raw_margin = math.inf
    min_envelope_margin = math.inf
    maximum_steps = math.ceil(max_qk / q)
    for step in range(1, maximum_steps + 1):
        p_next, v_next, raw = one_step(p, v, degrees, q)
        r_next = residual(p_next, degrees, q)
        delta = max(0.0, r_next.max() / (q * q))
        min_raw_margin = min(min_raw_margin, float(raw.min()))
        min_envelope_margin = min(
            min_envelope_margin,
            float((p_next - delta).min()),
        )
        assert raw.min() > 0.0, f"projection activated at terminal step {step}"
        assert (p_next - delta).min() > 0.0, f"safe subtraction clipped at terminal step {step}"
        if first_range_crossing is None and np.ptp(r_next) <= q**3 / 5.0:
            first_range_crossing = step
        corrected_minimum = float(r_next.min()) - max(0.0, float(r_next.max()))
        if corrected_minimum >= -(q**3) / 5.0:
            first_certificate = step
            break
        p, v = p_next, v_next
    assert first_certificate is not None, (
        "no literal safe-envelope certificate in requested horizon"
    )
    assert first_range_crossing is not None

    weighted_l1 = float(np.dot(degrees, np.abs(r_zero)))
    weighted_packet_error = float(np.dot(degrees, np.abs(packet_error)))
    l_r_zero = (r_zero - h_apply(r_zero, degrees, q)) / (1.0 - q * q)
    velocity_source = r_one / (1.0 - q) - l_r_zero
    print(
        f"m={edge_count:5d} q={q:.9g} alpha={q * q:.9g} "
        f"rho=tau={q / 5.0:.9g} graph=P_m seed=v0 "
        "stop=min(r)-max(0,max(r))>=-q^3/5 arithmetic=float64"
    )
    print(
        f"  entry_L1D/q2={weighted_l1 / q**2:.9f} "
        f"entry_range/q^(5/2)={np.ptp(r_zero) / q**2.5:.9f} "
        f"packet_error_L1D/q2={weighted_packet_error / q**2:.9f}"
    )
    print(
        f"  modal_band={band} "
        f"max_even_modal_defect={max(relative_defects):.6g} "
        f"lemma_band={lemma_band} combined_lemma_check={lemma_check} "
        f"first_range_k={first_range_crossing} "
        f"qk_range={q * first_range_crossing:.9f} "
        f"first_certificate_k={first_certificate} "
        f"qk_certificate={q * first_certificate:.9f} "
        f"raw_margin/q2={min_raw_margin / q**2:.6g} "
        f"envelope_margin/q2={min_envelope_margin / q**2:.6g}"
    )
    print(
        f"  wider_profile_C={max(position_profiles):.6g} "
        f"wider_profile_VplusG5={max(velocity_correction_profiles):.6g} "
        f"profile_lemma_check={profile_check} "
        f"first_signed_C={first_position_signed:.6g} "
        f"first_signed_VplusG5={first_velocity_correction_signed:.6g} "
        f"first_D_over_G={first_quadrature_relative:.6g} "
        f"velocity_identity_relerr={maximum_quadrature_consistency:.3g}"
    )
    print(
        f"  measured_c_over_q3=[{packet_error.min() / q**3:.6g},"
        f"{packet_error.max() / q**3:.6g}] "
        f"measured_w_over_q3=[{velocity_source.min() / q**3:.6g},"
        f"{velocity_source.max() / q**3:.6g}] "
        f"weighted_mean_w_over_q3={np.dot(degrees, velocity_source) / q**3:.6g}"
    )
    position_pieces, velocity_pieces = five_piece_decomposition(
        prefix_residuals,
        proper_error_last,
        proper_frontier,
        q,
    )
    piece_names = ("base", "constant_u", "delta_u", "mass", "endpoint")
    position_text = ",".join(f"{name}:{position_pieces[name]:.6g}" for name in piece_names)
    velocity_text = ",".join(f"{name}:{velocity_pieces[name]:.6g}" for name in piece_names)
    print(
        f"  measured_five_piece_C=[{position_text}] "
        f"sum={sum(position_pieces.values()):.6g} "
        f"measured_five_piece_V=[{velocity_text}] "
        f"sum={sum(velocity_pieces.values()):.6g}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "m",
        nargs="*",
        type=int,
        default=[128, 256, 512, 1024],
        help="path edge counts",
    )
    parser.add_argument(
        "--max-qk",
        type=float,
        default=8.0,
        help="maximum normalized terminal horizon",
    )
    arguments = parser.parse_args()
    exact_boundary_source_checks()
    check_signed_green_formula()
    for edge_count in arguments.m:
        if edge_count < 3:
            raise ValueError("every screened path needs at least three edges")
        screen(edge_count, arguments.max_qk)


if __name__ == "__main__":
    main()
