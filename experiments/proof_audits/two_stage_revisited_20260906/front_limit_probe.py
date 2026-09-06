"""High-precision diagnostic for the proposed separated-front limit.

The transfer-function gain is checked exactly. Finite unit-tree trajectories
use certified integer approximations. The limiting profile uses Decimal
arithmetic; agreement is evidence for, not proof of, the open limit lemma.
"""

from __future__ import annotations

import argparse
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
from math import isqrt, nextafter, ulp
from pathlib import Path

from . import provenance
from .orthant_continuation import solve
from .quotient_ramp_probe import check_realization, radial
from .radial_ramp_counterexamples import exact_radial_ppr


def exact_gain():
    def add(a, b):
        return a[0] + b[0], a[1] + b[1]

    def mul(a, b):
        return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]

    def scale(a, value):
        return a[0] * value, a[1] * value

    def div(a, b):
        return scale(mul(a, (b[0], -b[1])), 1 / (b[0] ** 2 + b[1] ** 2))

    theta = F(1, 64)
    alpha, eta, beta = theta**2, 1 - theta / 2, (1 - theta) / (1 + theta)
    c = (1 - alpha) / 2
    z = scale((F(12, 13), F(5, 13)), eta)
    a = scale(add((1 + beta, F(0)), scale(div((beta, F(0)), z), -1)), c)
    difference = add(z, scale(a, -1))
    numerator = mul(a, a)
    denominator = add(scale(mul(difference, difference), 2), scale(numerator, -1))
    gain = div(numerator, denominator)
    squared = gain[0] ** 2 + gain[1] ** 2
    assert squared > 9
    return {
        "gain_squared": str(squared),
        "gain_squared_float": float(squared),
        "strictly_above_nine": True,
    }


def limit_profile(j, window, precision=80):
    theta = F(1, 64)
    alpha, eta, beta = theta**2, 1 - theta / 2, (1 - theta) / (1 + theta)
    c, q0 = (1 - alpha) / 2, (1 + alpha) / 2
    front_ppr = solve([[q0, -c], [-c / 2, q0]], [F(1), F(0)])
    n = 2 * j
    operator = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        operator[i][i] = c
        if i % 2 == 0:
            operator[i][i + 1] = c
        else:
            operator[i][i - 1] = c / 2
            if i + 1 < n:
                operator[i][i + 1] = c / 2
    g = 1 + beta - beta / eta
    constant = solve(
        [[(eta if i == k else 0) - g * operator[i][k] for k in range(n)] for i in range(n)],
        [alpha] * n,
    )
    forcing = [F(0)] * n
    forcing[-1] = alpha * c * front_ppr[0] / 2
    past = solve(
        [[(1 if i == k else 0) - operator[i][k] for k in range(n)] for i in range(n)],
        forcing,
    )
    with localcontext() as context:
        context.prec = precision

        def dec(value):
            return D(value.numerator) / D(value.denominator)

        th, al, et, be, cc, qq = map(dec, (theta, alpha, eta, beta, c, q0))
        t_front = list(map(dec, front_ppr))
        x, z = [D(0)] * 2, [D(0)] * 2
        lam = D(1)
        current = [dec(a + b) for a, b in zip(constant, past)]
        previous = [dec(a + eta * b) for a, b in zip(constant, past)]
        front_current = al * t_front[0]
        front_previous = et * front_current
        op = [[(i, dec(value)) for i, value in enumerate(row) if value] for row in operator]
        rows = []
        for tau in range(window + 1):
            rows.append(current[0])
            product = [sum(value * current[i] for i, value in row) for row in op]
            previous_product = [sum(value * previous[i] for i, value in row) for row in op]
            product[-1] += cc * front_current / 2
            previous_product[-1] += cc * front_previous / 2
            following = [
                (1 + be) * a / et - be * b / et**2 + al / et
                for a, b in zip(product, previous_product)
            ]
            y = [(a + th * b) / (1 + th) for a, b in zip(x, z)]
            gradient = [qq * y[0] - cc * y[1] - 1 + lam, qq * y[1] - cc * y[0] / 2 + lam]
            new_z = [
                max(D(0), (1 - th) * b + th * a - grad / th) for a, b, grad in zip(y, z, gradient)
            ]
            x = [(1 - th) * a + th * b for a, b in zip(x, new_z)]
            z = new_z
            lam *= et
            previous, current = current, following
            front_previous, front_current = front_current, al * (t_front[0] - x[0]) / lam
        return rows


def finite_profile(j, separation, window):
    t = 64
    alpha, eta = F(1, t**2), F(2 * t - 1, 2 * t)
    c, q0 = (1 - alpha) / 2, (1 + alpha) / 2
    gamma = c**2 / (2 * q0**2 - c**2)
    desired = gamma / eta**separation
    branch = (2 * desired.numerator + desired.denominator) // (2 * desired.denominator)
    depth = 2 * j + 4
    sizes, neighbors = radial([branch if i % 2 == 0 else 1 for i in range(depth)])
    degree = check_realization(sizes, neighbors)
    volume = sum(size * d for size, d in zip(sizes, degree))
    bits = 2 * volume.bit_length() + 128
    denominator = 2**bits
    radius = 24 * (isqrt(volume) + 1) * t**2
    ppr_root = int(exact_radial_ppr(degree, neighbors, t)[0] * denominator)
    x, z = [0] * len(sizes), [0] * len(sizes)
    r = denominator // degree[0]
    output = []
    for step in range(j * separation + window + 1):
        if step >= j * separation:
            assert r * 1024 * volume > denominator
            error = ppr_root - x[0]
            center = error / r
            uncertainty = (radius + 1) / r + abs(center) * (2 * t) / r
            uncertainty = nextafter(uncertainty + 4 * ulp(center), float("inf"))
            output.append((center, uncertainty))
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
    return branch, output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", type=int, default=800)
    parser.add_argument("--pairs", default="1,2,3,4")
    parser.add_argument("--separations", default="400,800,1200,1600")
    parser.add_argument("--limit-only", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_record = provenance(vars(args) | {"output": str(args.output)}, args.output)
    gain = exact_gain()
    rows = []
    for j in map(int, args.pairs.split(",")):
        limit = limit_profile(j, args.window)
        higher = limit_profile(j, args.window, precision=100)
        discrepancy = max(abs(a - b) for a, b in zip(limit, higher))
        maximum = max(map(abs, limit))
        assert discrepancy < D("1e-50") * max(D(1), maximum)
        if args.limit_only:
            row = {
                "old_pairs": j,
                "max_limit_absolute_value": float(maximum),
                "max_limit_temporal_difference": float(
                    max(abs(a - b) for a, b in zip(limit, limit[1:]))
                ),
                "max_precision_discrepancy": str(discrepancy),
            }
            rows.append(row)
            print(json.dumps(row), flush=True)
            continue
        for separation in map(int, args.separations.split(",")):
            branch, observed = finite_profile(j, separation, args.window)
            errors = [
                abs(center - float(reference)) for (center, _), reference in zip(observed, limit)
            ]
            row = {
                "old_pairs": j,
                "separation": separation,
                "branch": branch,
                "max_difference_from_limit": max(errors),
                "finite_trajectory_max_certificate_radius": max(radius for _, radius in observed),
                "max_limit_absolute_value": float(max(map(abs, limit))),
                "worst_tau": errors.index(max(errors)),
            }
            rows.append(row)
            print(json.dumps(row), flush=True)
    record = {
        "provenance": source_record,
        "status": "finished",
        "scope": "Exact gain plus high-precision diagnostic of an open limiting argument",
        "exact_transfer_gain": gain,
        "case_count": len(rows),
        "cases": rows,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: value for key, value in record.items() if key != "cases"}), flush=True)


if __name__ == "__main__":
    main()
