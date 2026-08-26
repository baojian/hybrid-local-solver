#!/usr/bin/env python3
"""Deterministic floating screen for the short-path terminal candidate.

The script writes no artifacts. It reconstructs the actual transported-center
admission chronology and uses the literal global residual range on the full
face. Its output is measured float64 evidence, not an exact proof.
"""

from __future__ import annotations

import argparse
import math

import numpy as np


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
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    """Replay one fixed-face step and one transported singleton per prefix."""
    q = 1.0 / (16.0 * edge_count)
    degrees = np.r_[1.0, np.full(edge_count - 1, 2.0), 1.0]
    p = np.zeros(1)
    v = np.zeros(1)
    for length in range(1, edge_count + 1):
        p_next, v_next, raw = one_step(p, v, degrees[:length], q)
        assert raw.min() >= -1.0e-14, f"projection active during admission {length}"
        r_next = residual(p_next, degrees[:length], q)
        delta = max(0.0, r_next.max() / (q * q))
        assert delta <= 1.0e-12, f"nonzero admission correction at prefix {length}"
        outside = -(1.0 - q * q) * p_next[-1] / (2.0 * degrees[length]) + q**3 / 5.0
        assert outside < -(q**3) / 5.0, f"next vertex not strongly admitted at prefix {length}"
        old_optimum = restricted_optimum(length, degrees, q)
        new_optimum = restricted_optimum(length + 1, degrees, q)
        p = np.r_[p_next, 0.0]
        v = np.r_[v_next, 0.0] + new_optimum - np.r_[old_optimum, 0.0]
    return q, degrees, p, v


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


def screen(edge_count: int, max_qk: float) -> None:
    q, degrees, p, v = full_face_entry(edge_count)
    r_zero = residual(p, degrees, q)
    packet = -(q * q / 2.0) * (1.0 - q) ** edge_count * binomial_probabilities(edge_count)
    packet_error = r_zero - packet

    p_one, _, raw_one = one_step(p, v, degrees, q)
    assert raw_one.min() > 0.0
    coefficient_zero = cosine_coefficients(r_zero, degrees)
    coefficient_one = cosine_coefficients(residual(p_one, degrees, q), degrees)
    band = max(
        1,
        int(math.sqrt(edge_count / max(1.0, math.log(edge_count)))),
    )
    relative_defects = []
    for index in range(1, band + 1):
        mode = 2 * index
        phi = mode * math.pi / (2.0 * edge_count)
        radius = (1.0 - q) * math.cos(phi)
        quadrature = (
            coefficient_one[mode] / radius - coefficient_zero[mode] * math.cos(phi)
        ) / math.sin(phi)
        endpoint_mass = math.ldexp(1.0, -edge_count)
        signed_ideal = (
            -(q * q / edge_count)
            * (1.0 - q) ** edge_count
            * ((-1.0) ** index * math.cos(phi) ** edge_count - endpoint_mass)
        )
        ideal_amplitude = abs(signed_ideal)
        relative_defects.append(
            max(
                abs(coefficient_zero[mode] - signed_ideal),
                abs(quadrature),
            )
            / ideal_amplitude
        )

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
        f"first_range_k={first_range_crossing} "
        f"qk_range={q * first_range_crossing:.9f} "
        f"first_certificate_k={first_certificate} "
        f"qk_certificate={q * first_certificate:.9f} "
        f"raw_margin/q2={min_raw_margin / q**2:.6g} "
        f"envelope_margin/q2={min_envelope_margin / q**2:.6g}"
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
    for edge_count in arguments.m:
        if edge_count < 2:
            raise ValueError("every screened path needs at least two edges")
        screen(edge_count, arguments.max_qk)


if __name__ == "__main__":
    main()
