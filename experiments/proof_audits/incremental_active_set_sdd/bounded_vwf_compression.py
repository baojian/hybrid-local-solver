"""Exact bounded-domain VWF compression with a signed small-split budget.

The supplied evaluation radius is an explicit hypothesis. This does not
prove bounds on recursive solver queries or cumulative graph-local work.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import time


def atom(s, x):
    if s <= 0:
        return min(F(0), x - s) ** 2 / 2
    return x * x / 2 if x <= s else s * x - s * s / 2


@dataclass(frozen=True)
class VWF:
    lower: F
    constant: F
    slope: F
    knots: tuple

    def value(self, x):
        assert x >= self.lower
        return self.constant + self.slope * x + sum(q * atom(s, x) for s, q in self.knots)

    def polynomials(self):
        """Independent full quadratic-piece expansion for validation."""
        a = sum((q for _, q in self.knots), F(0)) / 2
        b = self.slope - sum(q * s for s, q in self.knots if s < 0)
        c = self.constant + sum(q * s * s / 2 for s, q in self.knots if s < 0)
        pieces = [(a, b, c)]
        for s, q in self.knots:
            a -= q / 2
            b += q * s
            c -= q * s * s / 2
            pieces.append((a, b, c))
        assert a == 0
        assert all(isinstance(coefficient, F) for piece in pieces for coefficient in piece)
        return [s for s, _ in self.knots], pieces


def compress(vwf, radius, tau):
    """Sorted supplied curvature events; no logarithm or hash-table oracle."""
    assert vwf.lower <= 0 and vwf.constant <= 0 and 0 < tau <= radius
    counts = Counter()
    grid = [tau]
    while grid[-1] < radius:
        grid.append(2 * grid[-1])
        counts["dyadic_grid_multiplications"] += 1
    negative, positive = [F(0)] * len(grid), [F(0)] * len(grid)
    counts["grid_and_bin_words_allocated"] += 3 * len(grid)
    neg_index, pos_index = len(grid) - 1, 0
    zero, error = F(0), F(0)
    previous = None
    for s, q in vwf.knots:
        assert q > 0 and s > vwf.lower and (previous is None or previous < s)
        previous = s
        counts["input_event_visits"] += 1
        if s <= -radius:
            counts["outside_negative_box_events"] += 1
            continue
        if s > radius:
            s = radius
            counts["outside_positive_box_events"] += 1
        if abs(s) < tau:
            zero += q
            error += radius * q * abs(s)
            counts["small_events_snapped_to_zero"] += 1
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
    output = VWF(vwf.lower, vwf.constant - error, vwf.slope, tuple(knots))
    assert len(knots) <= 2 * len(grid) + 1
    assert sum(q for _, q in knots) <= sum(q for _, q in vwf.knots)
    assert all(s == 0 or tau <= abs(s) <= 2 * radius for s, _ in knots)
    return output, error, counts, len(grid)


def reference_snap(vwf, radius, tau):
    events = {}
    for s, q in vwf.knots:
        if s <= -radius:
            continue
        s = min(s, radius)
        if abs(s) < tau:
            s = F(0)
        if s > vwf.lower:
            events[s] = events.get(s, F(0)) + q
    return VWF(vwf.lower, vwf.constant, vwf.slope, tuple(sorted(events.items())))


def polynomial_at(cache, x):
    knots, pieces = cache
    return pieces[bisect_right(knots, x)]


def quadratic_value(poly, x):
    a, b, c = poly
    return a * x * x + b * x + c


def nonnegative(poly, left, right, counts):
    points = [left, right]
    a, b, _ = poly
    if a > 0 and left < -b / (2 * a) < right:
        points.append(-b / (2 * a))
        counts["interior_quadratic_minima_checked"] += 1
    assert all(quadratic_value(poly, x) >= 0 for x in points), (poly, left, right)
    counts["complete_interval_nonnegativity_certificates"] += 1


def validate(vwf, radius, tau, counts, work):
    output, error, operations, bins = compress(vwf, radius, tau)
    snapped = reference_snap(vwf, radius, tau)
    assert error <= radius * tau * sum(q for _, q in vwf.knots)
    lower = max(vwf.lower, -radius)
    cuts = {lower, radius}
    for function in [vwf, snapped, output]:
        cuts.update(s for s, _ in function.knots if lower < s < radius)
    cuts.update(2 * s for s, _ in vwf.knots if lower < 2 * s < radius)
    cuts = sorted(cuts)
    fc, sc, oc = vwf.polynomials(), snapped.polynomials(), output.polynomials()
    for left, right in zip(cuts, cuts[1:]):
        middle = (left + right) / 2
        original = polynomial_at(fc, middle)
        snap = polynomial_at(sc, middle)
        compressed = polynomial_at(oc, middle)
        a, b, c = polynomial_at(fc, middle / 2)
        twice_half = (a / 2, b, 2 * c)
        upper = tuple(x - y for x, y in zip(original, compressed))
        lower_poly = [x - y for x, y in zip(compressed, twice_half)]
        lower_poly[2] += 3 * error
        nonnegative(upper, left, right, counts)
        nonnegative(lower_poly, left, right, counts)
        difference = [x - y for x, y in zip(snap, original)]
        for sign in [-1, 1]:
            bound = [sign * x for x in difference]
            bound[2] += error
            nonnegative(bound, left, right, counts)
        counts["complete_overlay_intervals"] += 1
    for function, cache in [(vwf, fc), (snapped, sc), (output, oc)]:
        for x in [lower, (lower + radius) / 2, F(0), radius]:
            assert function.value(x) == quadratic_value(polynomial_at(cache, x), x)
            counts["independent_atom_value_checks"] += 1
    assert operations["input_event_visits"] == len(vwf.knots)
    assert operations["positive_grid_pointer_moves"] <= bins - 1
    assert operations["negative_grid_pointer_moves"] <= bins - 1
    work.update(operations)
    counts["complete_function_compressions"] += 1
    counts["functions_with_zero_output_event"] += any(s == 0 for s, _ in output.knots)
    return {
        "input_events": len(vwf.knots),
        "output_events": len(output.knots),
        "dyadic_grid_size": bins,
        "radius": str(radius),
        "tau": str(tau),
        "certified_additive_error": str(error),
        "algorithm_counts": dict(operations),
    }


def generated_case(rng, index):
    radius = rng.choice([F(1, 8), F(1), F(17)])
    lower = rng.choice([-4 * radius, -radius, -radius / 3, F(0)])
    tau = radius / rng.choice([8, 64, 1024])
    events = {}
    for _ in range(1 + index % 23):
        exponent = rng.randint(-40, 8)
        s = radius * F(2) ** exponent * rng.choice([F(-3, 2), F(-1), F(0), F(1), F(3, 2)])
        if s <= lower:
            continue
        q = F(rng.randint(1, 13), rng.randint(1, 17))
        events[s] = events.get(s, F(0)) + q
    f = VWF(
        lower, -F(rng.randint(0, 11), 7), F(rng.randint(-12, 12), 5), tuple(sorted(events.items()))
    )
    return f, radius, tau


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    rng, counts, work = random.Random(73126), Counter(), Counter()
    for index in range(1200 if args.full else 60):
        validate(*generated_case(rng, index), counts, work)
    structured = []
    for size in [16, 64, 256, 512] if args.full else [16, 64]:
        knots = tuple((F(1, 2**j), F(1, size)) for j in reversed(range(1, size + 1)))
        function = VWF(F(-1), F(0), F(-1), knots)
        structured.append(validate(function, F(1), F(1, 1024), counts, work))
    for sign in [-1, 1]:
        function = VWF(F(-1), F(-1), F(2), ((sign * F(1, 2**2048), F(1)),))
        structured.append(validate(function, F(1), F(1, 1024), counts, work))
    deletion_failures = []
    for power in [4, 10, 30, 100]:
        tau, x = F(1, 2**power), F(-1)
        original = atom(-tau / 2, x)
        assert original > tau
        assert abs(atom(F(0), x) - original) <= tau
        deletion_failures.append(
            {
                "tau": str(tau),
                "split": str(-tau / 2),
                "field": "-1",
                "deletion_error": str(original),
                "snapping_error": str(abs(atom(F(0), x) - original)),
                "claimed_budget": str(tau),
            }
        )
    result = {
        "audit": "incremental_active_set_sdd.bounded_vwf_compression",
        "arithmetic": "exact fractions",
        "random_seed": 73126,
        "input_family": "supplied sorted signed curvature events of convex VWFs with concave derivative and constant final derivative",
        "graph_alpha_epsilon": "not a graph solver; primitive inputs are lower domain, radius R and split threshold tau",
        "stopping_rule": "one charged event scan; dyadic grid ends at its first value >= R; complete quadratic intervals certify F>=compressed>=2*F(x/2)-3*xi on the supplied box",
        "random_instances": 1200 if args.full else 60,
        "radius": ["1/8", "1", "17"],
        "tau": "R/8, R/64 or R/1024; structured R=1,tau=1/1024",
        "scope": "Supplied-domain scalar compression only. Evaluation radius, curvature bounds and cumulative errors in any recursive local solver remain separate obligations. Source geometric idea is re-proved by convex perspective with a dyadic grid and explicit zero handling.",
        "audit_only": dict(counts),
        "algorithm_counts": dict(work),
        "structured_cases": structured,
        "refuted_tiny_event_deletion": deletion_failures,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
