#!/usr/bin/env python3
"""Exact semantic-stop constants and measured certificate-separation replay."""

from __future__ import annotations

import argparse
import math
from fractions import Fraction

import numpy as np

import verify


def exact_semantic_stop_checks() -> None:
    semantic_time = Fraction(15, 4)
    exponential_partial_sum = sum(
        (semantic_time**exponent / math.factorial(exponent) for exponent in range(9)),
        Fraction(0),
    )
    assert exponential_partial_sum == Fraction(2459867141, 58720256)
    lower_threshold = Fraction(1331, 32)
    upper_threshold = Fraction(651, 16)
    assert exponential_partial_sum - lower_threshold == Fraction(17471493, 58720256)
    assert exponential_partial_sum - upper_threshold == Fraction(70686725, 58720256)

    # The scalar envelopes are decreasing on s>=15/4.
    lower_envelope = Fraction(157, 20) + semantic_time / 8
    assert Fraction(1, 8) - lower_envelope < 0
    assert 7 - 8 * semantic_time < 0

    # Prefix volume m^2 plus the terminal scan upper bound.
    assert Fraction(1, 256) + Fraction(15, 32) == Fraction(121, 256)
    print(
        "semantic_stop_constants=PASS s=15/4 "
        "exp_partial=2459867141/58720256 "
        "lower_slack=17471493/58720256 "
        "upper_slack=70686725/58720256 total_leading=121/256"
    )


def measured_screen(edge_count: int, max_qk: float) -> None:
    q, degrees, p, v, *_ = verify.full_face_entry(edge_count)
    optimum = verify.restricted_optimum(edge_count + 1, degrees, q)
    first_semantic: int | None = None
    first_certificate: int | None = None
    semantic_minimum = math.nan
    semantic_maximum = math.nan
    maximum_steps = math.ceil(max_qk / q)

    for step in range(1, maximum_steps + 1):
        p, v, raw = verify.one_step(p, v, degrees, q)
        assert float(raw.min()) > 0.0
        residual = verify.residual(p, degrees, q)
        delta = max(0.0, float(residual.max()) / (q * q))
        assert float((p - delta).min()) > 0.0

        error = p - optimum
        if first_semantic is None and float(np.max(np.abs(error))) <= q / 5.0:
            first_semantic = step
            semantic_minimum = float(error.min() / q)
            semantic_maximum = float(error.max() / q)

        corrected_minimum = float(residual.min()) - max(0.0, float(residual.max()))
        if first_certificate is None and corrected_minimum >= -(q**3) / 5.0:
            first_certificate = step

        if first_semantic is not None and first_certificate is not None:
            break

    assert first_semantic is not None
    assert first_certificate is not None
    print(
        "MEASURED_FLOAT64 "
        f"m={edge_count} qk_semantic={q * first_semantic:.9f} "
        f"qk_certificate={q * first_certificate:.9f} "
        f"semantic_crossing_error_over_q=[{semantic_minimum:.9f},{semantic_maximum:.9f}]"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("m", nargs="*", type=int, default=[64, 128, 256, 512, 1024])
    parser.add_argument("--max-qk", type=float, default=6.0)
    arguments = parser.parse_args()
    exact_semantic_stop_checks()
    for edge_count in arguments.m:
        if edge_count < 64:
            raise ValueError("the semantic screen is scoped to m>=64")
        measured_screen(edge_count, arguments.max_qk)


if __name__ == "__main__":
    main()
