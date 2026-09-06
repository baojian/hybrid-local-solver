"""Exact finite checks of sign separation and bounded normalized old errors.

These are finite diagnostics for the separately proved graph-limit theorem.
Canonical unit trees are represented radially only for offline verification.
Integer trajectory radii also certify the positivity of the exact kinetic
state after the proof's fixed, pair-dependent activation checkpoints.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from math import isqrt
from pathlib import Path
import time

from . import provenance
from .orthant_continuation import solve
from .quotient_ramp_probe import check_realization, radial
from .radial_ramp_counterexamples import exact_radial_ppr


def check_case(j, separation, window):
    t = 64
    alpha, eta = F(1, t * t), F(2 * t - 1, 2 * t)
    c, q0 = (1 - alpha) / 2, (1 + alpha) / 2
    gamma = c * c / (2 * q0 * q0 - c * c)
    desired = gamma / eta**separation
    branch = (2 * desired.numerator + desired.denominator) // (2 * desired.denominator)
    sizes, neighbors = radial([branch if i % 2 == 0 else 1 for i in range(2 * j + 4)])
    degree = check_realization(sizes, neighbors)
    volume = sum(size * d for size, d in zip(sizes, degree))
    bits = 2 * volume.bit_length() + 128
    denominator = 2**bits
    radius = 24 * (isqrt(volume) + 1) * t * t
    ppr = exact_radial_ppr(degree, neighbors, t)
    ppr_grid = [int(value * denominator) for value in ppr]
    front = solve([[q0, -c], [-c / 2, q0]], [F(1), F(0)])
    checkpoints = []
    for i in range(j):
        threshold = alpha**2 * gamma**i * min(front[0] ** 2, 2 * front[1] ** 2) / 64
        offset, power = 0, F(1)
        while power > threshold:
            offset += 1
            power *= eta
        checkpoint = i * separation + offset
        checkpoints.append(checkpoint)
        exact_r = eta**checkpoint / branch
        for level in (2 * i, 2 * i + 1):
            # The mathematical energy bound alone certifies positivity here
            # and at every later pre-freeze step, without numerical history.
            assert 4 * exact_r < sizes[level] * degree[level] * ppr[level] ** 2

    x, z = [0] * len(sizes), [0] * len(sizes)
    r = denominator // branch
    maximum_pairs = [F(0)] * (j + 1)
    positive_checks = 0
    horizon = j * separation + window
    for step in range(horizon + 1):
        assert r * 1024 * volume > denominator
        if step <= j * separation - 1:
            assert not any(x[2 * j :]) and not any(z[2 * j :])
        assert not any(x[2 * j + 2 :]) and not any(z[2 * j + 2 :])
        for i, checkpoint in enumerate(checkpoints):
            if step >= checkpoint:
                assert min(z[2 * i : 2 * i + 2]) > radius
                positive_checks += 2
        for i in range(j + 1):
            error = max(abs(ppr_grid[level] - x[level]) for level in (2 * i, 2 * i + 1))
            upper_num = error + radius + 1
            old = maximum_pairs[i]
            if upper_num * old.denominator > old.numerator * r:
                maximum_pairs[i] = F(upper_num, r)
        if step == horizon:
            break
        next_z = []
        for i, (d, row) in enumerate(zip(degree, neighbors)):
            neighbor_x = sum(count * x[k] for k, count in row)
            neighbor_z = sum(count * z[k] for k, count in row)
            numerator = (t - 1) * (d * z[i] + neighbor_z)
            numerator -= t * (t - 1) * (d * x[i] - neighbor_x)
            numerator += 2 * denominator * (i == 0) - 2 * d * r
            next_z.append(max(0, numerator // (2 * t * d)))
        x = [((t - 1) * a + b) // t for a, b in zip(x, next_z)]
        z = next_z
        r = ((2 * t - 1) * r) // (2 * t)
    return {
        "old_pairs": j,
        "separation": separation,
        "branch": str(branch),
        "window": window,
        "step_horizon": horizon,
        "original_volume": str(volume),
        "alpha": str(alpha),
        "grid_bits": bits,
        "positivity_checkpoints": checkpoints,
        "exact_kinetic_positivity_checks": positive_checks,
        "future_zero_checks": "all incoming states through the full stated horizon",
        "max_normalized_error_upper_bounds_by_pair": [str(value) for value in maximum_pairs],
        "max_normalized_error_upper_bounds_float_display": [
            float(value) for value in maximum_pairs
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", default="1,2,4")
    parser.add_argument("--separations", default="4000,6000,8000")
    parser.add_argument("--window", type=int, default=1000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_record = provenance(vars(args) | {"output": str(args.output)}, args.output)
    started = time.monotonic()
    rows = []
    for j in map(int, args.pairs.split(",")):
        for separation in map(int, args.separations.split(",")):
            row = check_case(j, separation, args.window)
            rows.append(row)
            print(
                json.dumps({k: v for k, v in row.items() if "bounds_by_pair" not in k}),
                flush=True,
            )
    record = {
        "provenance": source_record,
        "status": "passed",
        "scope": "Exact finite sign and normalized-error checks; asymptotic proof is in the note",
        "arithmetic": "integer trajectory with proved radii and rational reference checks",
        "case_count": len(rows),
        "elapsed_seconds": time.monotonic() - started,
        "cases": rows,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
