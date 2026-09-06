"""Certified finite-horizon tracking search beyond floating-point resolution.

Each case is a finite canonical rooted unit tree, represented by equitable
classes only for offline verification. All trajectory and comparison work
uses integers. The exact rational PPR reference is floored once to the same
grid, and uniform pairwise-contraction error radii certify every saved ratio.
No quotient oracle or ambient volume is used by the proposed local solver.
"""

from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path
import time

from . import provenance
from .quotient_ramp_probe import check_realization, radial
from .radial_ramp_counterexamples import exact_radial_ppr


def run_case(branch, spacing, depth, t):
    sizes, neighbors = radial([branch if i % spacing == 0 else 1 for i in range(depth)])
    degree = check_realization(sizes, neighbors)
    volume = sum(size * d for size, d in zip(sizes, degree))
    bits = 2 * volume.bit_length() + 2 * t.bit_length() + 100
    denominator = 2**bits
    radius = 24 * (isqrt(volume) + 1) * t**2
    ppr = [int(value * denominator) for value in exact_radial_ppr(degree, neighbors, t)]
    x, z = [0] * len(sizes), [0] * len(sizes)
    r = denominator // degree[0]
    best_num, best_den, best_upper_num, best_upper_den = 0, 1, 0, 1
    best_step, best_coordinate = 0, 0
    steps = 0
    maximum_certified_overshoot = 0
    maximum_certified_decrease = 0
    while r * 1024 * volume > denominator:
        next_z = []
        for i, (d, row) in enumerate(zip(degree, neighbors)):
            neighbor_x = sum(count * x[j] for j, count in row)
            neighbor_z = sum(count * z[j] for j, count in row)
            numerator = (t - 1) * (d * z[i] + neighbor_z)
            numerator -= t * (t - 1) * (d * x[i] - neighbor_x)
            numerator += 2 * denominator * (i == 0) - 2 * d * r
            next_z.append(max(0, numerator // (2 * t * d)))
        next_x = [((t - 1) * a + b) // t for a, b in zip(x, next_z)]
        decrease = max(a - b for a, b in zip(x, next_x)) - 2 * radius
        maximum_certified_decrease = max(maximum_certified_decrease, decrease)
        x, z = next_x, next_z
        r = ((2 * t - 1) * r) // (2 * t)
        steps += 1
        if r * 1024 * volume <= denominator:
            break
        differences = [abs(a - b) for a, b in zip(ppr, x)]
        coordinate = max(range(len(sizes)), key=differences.__getitem__)
        error = differences[coordinate]
        # PPR floor error <= 1 grid unit, state error <= radius grid units,
        # regularizer floor error <= 2t grid units. All ratios are rational.
        lower_num, lower_den = max(0, error - radius - 1), r + 2 * t
        upper_num, upper_den = error + radius + 1, r
        if lower_num * best_den > best_num * lower_den:
            best_num, best_den = lower_num, lower_den
            best_step, best_coordinate = steps, coordinate
        if upper_num * best_upper_den > best_upper_num * upper_den:
            best_upper_num, best_upper_den = upper_num, upper_den
        overshoot = max(b - a for a, b in zip(ppr, x)) - radius - 1
        maximum_certified_overshoot = max(maximum_certified_overshoot, overshoot)
    assert best_num * best_upper_den <= best_upper_num * best_den
    return {
        "tree": {"branch": branch, "spacing": spacing, "depth": depth},
        "theta_denominator": t,
        "alpha": f"1/{t * t}",
        "original_volume": str(volume),
        "vertex_count": str(sum(sizes)),
        "grid_bits": bits,
        "steps": steps,
        "tracking_steps_checked": steps - 1,
        "best_step": best_step,
        "best_level": best_coordinate,
        "certified_max_ratio_interval_float_display": [
            best_num / best_den,
            best_upper_num / best_upper_den,
        ],
        "certified_lower_ratio": [str(best_num), str(best_den)],
        "certified_upper_ratio": [str(best_upper_num), str(best_upper_den)],
        "certified_ppr_overshoot_lower_bound": maximum_certified_overshoot / denominator,
        "certified_coordinate_decrease_lower_bound": maximum_certified_decrease / denominator,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branches", default="2,10")
    parser.add_argument("--spacings", default="4")
    parser.add_argument("--depths", default="32,64,128")
    parser.add_argument("--t-values", default="32,64,128")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    source_record = provenance(vars(args) | {"output": str(args.output)}, args.output)
    rows = []

    def save(status):
        record = {
            "provenance": source_record,
            "status": status,
            "scope": "Certified finite-horizon search, not an asymptotic bound or local implementation",
            "case_count": len(rows),
            "elapsed_seconds": time.monotonic() - started,
            "maximum_certified_lower_ratio": max(
                (r["certified_max_ratio_interval_float_display"][0] for r in rows), default=0
            ),
            "cases": rows,
        }
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(record, indent=2) + "\n")
        return record

    for depth in map(int, args.depths.split(",")):
        for branch in map(int, args.branches.split(",")):
            for spacing in map(int, args.spacings.split(",")):
                for t in map(int, args.t_values.split(",")):
                    row = run_case(branch, spacing, depth, t)
                    rows.append(row)
                    record = save("running")
                    print(
                        json.dumps(
                            {k: v for k, v in record.items() if k not in ("cases", "provenance")}
                        ),
                        flush=True,
                    )
    record = save("passed")
    print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
