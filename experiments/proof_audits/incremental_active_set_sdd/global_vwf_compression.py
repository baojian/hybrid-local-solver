"""Global VWF compression by curvature-moment regularization of tiny splits.

The result removes dependence on the smallest split and preserves the final
derivative. Upper split and curvature bounds in a recursive solver remain
separate obligations; exponentially small curvature weights may remain.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bounded_vwf_compression import (
    VWF,
    generated_case,
    nonnegative,
    polynomial_at,
    quadratic_value,
)


def compress_global(vwf, tau):
    assert vwf.lower <= 0 and vwf.constant <= 0 and tau > 0
    counts = Counter()
    radius = tau
    for s, q in vwf.knots:
        assert q > 0
        radius = max(radius, abs(s))
        counts["range_scan_events"] += 1
    grid = [tau]
    while grid[-1] < radius:
        grid.append(2 * grid[-1])
        counts["dyadic_grid_multiplications"] += 1
    negative, positive = [F(0)] * len(grid), [F(0)] * len(grid)
    counts["grid_and_bin_words_allocated"] += 3 * len(grid)
    zero, error, negative_shift = F(0), F(0), F(0)
    neg_index, pos_index, previous = len(grid) - 1, 0, None
    for s, q in vwf.knots:
        assert s > vwf.lower and (previous is None or previous < s)
        previous = s
        counts["compression_scan_events"] += 1
        if abs(s) < tau:
            fraction = abs(s) / tau
            zero += q * (1 - fraction)
            loss = q * abs(s) * (tau - abs(s)) / 2
            error += loss
            if s < 0:
                negative[0] += q * fraction
                negative_shift += loss
            elif s > 0:
                positive[0] += q * fraction
            counts["moment_regularized_events"] += 1
        elif s < 0:
            while neg_index > 0 and grid[neg_index - 1] >= -s:
                neg_index -= 1
                counts["negative_grid_pointer_moves"] += 1
            negative[neg_index] += q * (-s) / grid[neg_index]
            counts["negative_bin_additions"] += 1
        else:
            while grid[pos_index] < s:
                pos_index += 1
                counts["positive_grid_pointer_moves"] += 1
            positive[pos_index] += q * s / grid[pos_index]
            counts["positive_bin_additions"] += 1
    knots = []
    for index in reversed(range(len(grid))):
        if negative[index] and -grid[index] > vwf.lower:
            knots.append((-grid[index], negative[index]))
        counts["output_bin_visits"] += 1
    if zero and vwf.lower < 0:
        knots.append((F(0), zero))
    for s, q in zip(grid, positive):
        if q:
            knots.append((s, q))
        counts["output_bin_visits"] += 1
    counts["output_event_words_allocated"] += 2 * len(knots)
    output = VWF(vwf.lower, vwf.constant - negative_shift, vwf.slope, tuple(knots))
    assert len(knots) <= 2 * len(grid) + 1
    assert error <= sum((q for _, q in vwf.knots), F(0)) * tau**2 / 8
    return output, error, negative_shift, counts, len(grid), radius


def regularized_reference(vwf, tau):
    events, shift = {}, F(0)
    for s, q in vwf.knots:
        if abs(s) < tau:
            ratio = abs(s) / tau
            replacements = [(F(0), q * (1 - ratio))]
            if s:
                replacements.append((tau if s > 0 else -tau, q * ratio))
            if s < 0:
                shift += q * (-s) * (tau + s) / 2
        else:
            replacements = [(s, q)]
        for t, weight in replacements:
            if weight and t > vwf.lower:
                events[t] = events.get(t, F(0)) + weight
    return VWF(vwf.lower, vwf.constant - shift, vwf.slope, tuple(sorted(events.items())))


def final_derivative(vwf):
    return vwf.slope + sum(q * s for s, q in vwf.knots if s > 0)


def validate_global(vwf, tau, counts, work):
    output, error, shift, operations, bins, radius = compress_global(vwf, tau)
    regular = regularized_reference(vwf, tau)
    assert final_derivative(vwf) == final_derivative(regular) == final_derivative(output)
    assert sum(q for _, q in output.knots) <= sum(q for _, q in vwf.knots)
    assert output.constant == regular.constant and output.slope == vwf.slope
    cuts = {vwf.lower, F(0)}
    for function in [vwf, regular, output]:
        cuts.update(s for s, _ in function.knots if s >= vwf.lower)
    cuts.update(2 * s for s, _ in vwf.knots if 2 * s >= vwf.lower)
    cuts = sorted(cuts)
    fc, rc, oc = vwf.polynomials(), regular.polynomials(), output.polynomials()
    # The final interval includes the whole infinite ray, not a chosen radius.
    intervals = list(zip(cuts, cuts[1:])) + [(cuts[-1], None)]
    for left, right in intervals:
        middle = (left + right) / 2 if right is not None else left + 1
        original = polynomial_at(fc, middle)
        reg = polynomial_at(rc, middle)
        compressed = polynomial_at(oc, middle)
        a, b, c = polynomial_at(fc, middle / 2)
        twice_half = (a / 2, b, 2 * c)
        inequalities = []
        inequalities.append(tuple(x - y for x, y in zip(original, compressed)))
        lower = [x - y for x, y in zip(compressed, twice_half)]
        lower[2] += 2 * error
        inequalities.append(lower)
        regularization = [x - y for x, y in zip(original, reg)]
        inequalities.append(regularization)
        upper_error = [-x for x in regularization]
        upper_error[2] += error
        inequalities.append(upper_error)
        for polynomial in inequalities:
            if right is None:
                assert polynomial[0] == polynomial[1] == 0
                assert polynomial[2] >= 0
                counts["infinite_ray_certificates"] += 1
            else:
                nonnegative(polynomial, left, right, counts)
        counts["complete_global_overlay_intervals"] += 1
    for function, cache in [(vwf, fc), (regular, rc), (output, oc)]:
        for x in [vwf.lower, F(0), radius, 1000 * radius]:
            assert function.value(x) == quadratic_value(polynomial_at(cache, x), x)
            counts["independent_atom_value_checks"] += 1
    assert operations["range_scan_events"] == len(vwf.knots)
    assert operations["compression_scan_events"] == len(vwf.knots)
    assert operations["positive_grid_pointer_moves"] <= bins - 1
    assert operations["negative_grid_pointer_moves"] <= bins - 1
    work.update(operations)
    counts["complete_global_compressions"] += 1
    counts["preserved_terminal_derivatives"] += 1
    counts["nonzero_negative_regularization_shifts"] += shift > 0
    return {
        "input_events": len(vwf.knots),
        "output_events": len(output.knots),
        "dyadic_grid_size": bins,
        "largest_input_split_or_tau": str(radius),
        "tau": str(tau),
        "global_regularization_error_bound": str(error),
        "negative_constant_shift": str(shift),
        "unchanged_final_derivative": str(final_derivative(output)),
        "minimum_positive_output_curvature": str(min((q for _, q in output.knots), default=F(0))),
        "algorithm_counts": dict(operations),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    rng, counts, work = random.Random(73127), Counter(), Counter()
    for index in range(1200 if args.full else 60):
        vwf, _, tau = generated_case(rng, index)
        validate_global(vwf, tau, counts, work)
    structured = []
    for power in [16, 64, 256, 2048] if args.full else [16, 64]:
        for sign in [-1, 1]:
            vwf = VWF(F(-1), F(0), F(-1), ((sign * F(1, 2**power), F(1)),))
            structured.append(validate_global(vwf, F(1, 1024), counts, work))
    for size in [16, 64, 256, 512] if args.full else [16, 64]:
        knots = tuple((F(1, 2**j), F(1, size)) for j in reversed(range(1, size + 1)))
        structured.append(validate_global(VWF(F(-1), F(0), F(1), knots), F(1, 1024), counts, work))
    result = {
        "audit": "incremental_active_set_sdd.global_vwf_compression",
        "arithmetic": "exact fractions",
        "random_seed": 73127,
        "input_family": "supplied sorted signed VWF curvature events; tiny positive and negative splits through 2^-2048; many-event tails",
        "graph_alpha_epsilon": "not a graph solver; primitive input is VWF and threshold tau",
        "stopping_rule": "two charged event scans and a dyadic grid based on largest split/tau; exact complete quadratic intervals and the infinite ray certify F>=compressed>=2*F(x/2)-2*xi",
        "random_instances": 1200 if args.full else 60,
        "tau": "generated R/8,R/64,R/1024; structured 1/1024",
        "scope": "Global-domain compression removes smallest-split and evaluation-radius dependence. Recursive upper-split, curvature and error budgets remain open. Very small nonzero curvature weights may remain; no all-number range or local solver theorem is asserted.",
        "audit_only": dict(counts),
        "algorithm_counts": dict(work),
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "bounded_vwf_compression": hashlib.sha256(
                Path(__file__).with_name("bounded_vwf_compression.py").read_bytes()
            ).hexdigest()
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
