"""Exact certificates for ramp decrease, PPR overshoot, and tracking above 6r.

The graphs are ordinary finite rooted unit trees. Equitable radial classes
are used only for offline verification. Dyadic integer trajectory errors are
bounded by the proved pairwise contraction; the tridiagonal PPR reference is
solved with rational arithmetic and its equations are checked exactly.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from math import isqrt
from pathlib import Path

from . import provenance
from .quotient_ramp_probe import check_realization, radial


def exact_radial_ppr(degree, neighbors, t):
    n = len(degree)
    alpha = F(1, t**2)
    lower = [F(0)] * n
    diagonal = [F(1 + alpha, 2)] * n
    upper = [F(0)] * n
    rhs = [F(alpha, degree[0])] + [F(0)] * (n - 1)
    for i, row in enumerate(neighbors):
        for j, count in row:
            value = -(1 - alpha) * count / (2 * degree[i])
            if j == i - 1:
                lower[i] = value
            elif j == i + 1:
                upper[i] = value
            else:
                raise AssertionError("The certificate expects a radial tree")
    for i in range(1, n):
        factor = lower[i] / diagonal[i - 1]
        diagonal[i] -= factor * upper[i - 1]
        rhs[i] -= factor * rhs[i - 1]
    answer = [F(0)] * n
    answer[-1] = rhs[-1] / diagonal[-1]
    for i in range(n - 2, -1, -1):
        answer[i] = (rhs[i] - upper[i] * answer[i + 1]) / diagonal[i]
    for i, row in enumerate(neighbors):
        value = (1 + alpha) * answer[i] / 2
        value -= (1 - alpha) * sum(count * answer[j] for j, count in row) / (2 * degree[i])
        assert value == (alpha / degree[0] if i == 0 else 0)
    return answer


def certify(branch, spacing, depth, t, horizon, target, bits=200):
    branches = [branch if i % spacing == 0 else 1 for i in range(depth)]
    sizes, neighbors = radial(branches)
    degree = check_realization(sizes, neighbors)
    n = len(sizes)
    volume = sum(size * d for size, d in zip(sizes, degree))
    denominator = 2**bits
    x, z = [0] * n, [0] * n
    r = denominator // degree[0]
    previous_x = x.copy()
    for _ in range(horizon):
        next_z = []
        for i, (d, row) in enumerate(zip(degree, neighbors)):
            neighbor_x = sum(count * x[j] for j, count in row)
            neighbor_z = sum(count * z[j] for j, count in row)
            numerator = (t - 1) * (d * z[i] + neighbor_z)
            numerator -= t * (t - 1) * (d * x[i] - neighbor_x)
            numerator += 2 * denominator * (i == 0) - 2 * d * r
            next_z.append(max(0, numerator // (2 * t * d)))
        previous_x = x
        x = [((t - 1) * a + b) // t for a, b in zip(x, next_z)]
        z = next_z
        r = ((2 * t - 1) * r) // (2 * t)
    alpha = F(1, t**2)
    exact_r = F(1, degree[0]) * F(2 * t - 1, 2 * t) ** horizon
    assert exact_r > F(1, 1024 * volume)
    error_bound = F(24 * (isqrt(volume) + 1) * t**2, denominator)
    ppr = exact_radial_ppr(degree, neighbors, t)
    assert sum(size * d * value for size, d, value in zip(sizes, degree, ppr)) == 1
    if target == "decrease":
        witness = max(range(n), key=lambda i: previous_x[i] - x[i])
        observed = F(previous_x[witness] - x[witness], denominator)
        lower, upper = observed - 2 * error_bound, observed + 2 * error_bound
        assert F(159, 10**13) < lower < upper < F(161, 10**13)
    elif target == "overshoot":
        witness = max(range(n), key=lambda i: F(x[i], denominator) - ppr[i])
        observed = F(x[witness], denominator) - ppr[witness]
        lower, upper = observed - error_bound, observed + error_bound
        assert lower > F(4, 10**13)
        assert upper < F(5, 10**13)
    elif target in ("tracking", "large_tracking"):
        witness = max(range(n), key=lambda i: abs(ppr[i] - F(x[i], denominator)))
        observed = abs(ppr[witness] - F(x[witness], denominator))
        lower, upper = (observed - error_bound) / exact_r, (observed + error_bound) / exact_r
        if target == "tracking":
            assert F(682360, 100000) < lower < upper < F(682361, 100000)
        else:
            assert 2_700_097_454_229_948 < lower < upper < 2_700_097_454_229_950
    else:
        raise ValueError(target)
    residual = []
    for i, (d, row) in enumerate(zip(degree, neighbors)):
        value = (alpha / d if i == 0 else F(0)) - (1 + alpha) * F(x[i], denominator) / 2
        value += (1 - alpha) * sum(count * x[j] for j, count in row) / (2 * d * denominator)
        residual.append(value)
    minimum_residual = min(residual)
    if target == "overshoot":
        assert -F(193, 10**16) < minimum_residual - error_bound
        assert minimum_residual + error_bound < -F(192, 10**16)
    return {
        "status": "passed",
        "target": target,
        "tree": {"branch": branch, "spacing": spacing, "depth": depth},
        "vertex_count": str(sum(sizes)),
        "original_volume": str(volume),
        "alpha": str(alpha),
        "theta": str(F(1, t)),
        "step": horizon,
        "regularizer": f"(1/{degree[0]})*({2 * t - 1}/{2 * t})^{horizon}",
        "frozen_target": f"1/(1024*{volume})",
        "witness_level": witness,
        "certified_quantity_interval_float_display": [float(lower), float(upper)],
        "strict_positivity_verified_exactly": lower > 0,
        "trajectory_density_error_bound": float(error_bound),
        "minimum_ppr_residual_density_upper_bound": float(minimum_residual + error_bound),
        "negative_ppr_residual_certified": minimum_residual + error_bound < 0,
        "grid_bits": bits,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_record = provenance({}, args.output)
    rows = [
        certify(10, 3, 12, 128, 2250, "decrease"),
        certify(10, 4, 128, 64, 3037, "overshoot"),
        certify(2, 4, 128, 64, 3498, "tracking"),
        certify(10, 2, 128, 64, 19129, "large_tracking", bits=700),
    ]
    record = {
        "provenance": source_record,
        "status": "passed",
        "arithmetic": "integer dyadic trajectory with proved error radius and exact rational PPR",
        "case_count": len(rows),
        "cases": rows,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record), flush=True)


if __name__ == "__main__":
    main()
