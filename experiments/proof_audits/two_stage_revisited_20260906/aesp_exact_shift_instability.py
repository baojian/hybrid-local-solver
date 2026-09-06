"""Exact diagnostics for the ideal exact-inner AESP residual-mass obstruction.

This is not an implementation or counterexample for a thresholded AESP inner
solver. Finite regular rooted trees are represented by their equitable level
mass equations, with every original degree and transition checked explicitly.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .orthant_continuation import mv, solve, sub


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def multiply(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def scale(a, value):
    return a[0] * value, a[1] * value


def squared(a):
    return a[0] ** 2 + a[1] ** 2


def exact_frequency():
    s = 64
    beta, contraction = F(s - 1, s + 1), 1 - F(1, s * s)
    denominator = (F(27, 13), F(-5, 13))
    g = scale((denominator[0], -denominator[1]), 2 * contraction / squared(denominator))
    a, b = scale(g, 1 + beta), scale(g, beta)
    schur_expression = add(a, scale(multiply((a[0], -a[1]), b), -1))
    defect = squared(schur_expression) - (1 - squared(b)) ** 2
    assert squared(b) < 1 and defect > 0
    previous, current = (F(1), F(0)), g
    profiles = []
    for step in range(2, 257):
        previous, current = current, add(multiply(a, current), scale(multiply(b, previous), -1))
        if step in (16, 32, 64, 128, 256):
            value = squared(current)
            lower = isqrt(value.numerator // value.denominator)
            assert value > lower**2
            profiles.append({"stage": step, "strict_modulus_lower_integer": lower})
    return {
        "alpha": str(F(1, s * s + 1)),
        "frequency": "(12+5i)/13",
        "g_real": str(g[0]),
        "g_imaginary": str(g[1]),
        "pole_product_modulus_squared": str(squared(b)),
        "strict_unit_disk_defect": str(defect),
        "profiles": profiles,
    }


class IntegerTreeResolvent:
    """Apply an integer adjugate in linear work by exact elimination."""

    def __init__(self, branch, depth):
        self.branch, self.depth = branch, depth
        self.n = depth + 1
        self.diagonal = 3 * (branch + 1)
        self.lower = [-(branch + 1)] + [-branch] * (depth - 1)
        self.upper = [-1] * (depth - 1) + [-(branch + 1)]
        self.determinants = [1, self.diagonal]
        for i in range(1, self.n):
            self.determinants.append(
                self.diagonal * self.determinants[-1]
                - self.lower[i - 1] * self.upper[i - 1] * self.determinants[-2]
            )
        self.determinant = self.determinants[-1]
        assert self.determinant > 0
        # The matrix is (b+1)(3I-P), for the exact level-mass random walk.
        for column in range(self.n):
            total = self.diagonal
            if column:
                total += self.upper[column - 1]
            if column < depth:
                total += self.lower[column]
            assert total == 2 * (branch + 1)

    def adjugate(self, rhs):
        transformed = [rhs[0]]
        for i in range(1, self.n):
            transformed.append(self.determinants[i] * rhs[i] - self.lower[i - 1] * transformed[-1])
        result = [0] * self.n
        result[-1] = transformed[-1]
        for i in range(self.n - 2, -1, -1):
            numerator = (
                self.determinant * transformed[i]
                - self.upper[i] * self.determinants[i] * result[i + 1]
            )
            result[i], remainder = divmod(numerator, self.determinants[i + 1])
            assert remainder == 0
        return result

    def verify(self, rhs):
        result = self.adjugate(rhs)
        for i in range(self.n):
            value = self.diagonal * result[i]
            if i:
                value += self.lower[i - 1] * result[i - 1]
            if i < self.depth:
                value += self.upper[i] * result[i + 1]
            assert value == self.determinant * rhs[i]


def exact_tree(branch, depth, stages, lower_bound):
    s = 64
    resolvent = IntegerTreeResolvent(branch, depth)
    resolvent.verify([(-1) ** i * (i + 1) for i in range(depth + 1)])
    scalar = 2 * (s * s - 1) * (branch + 1)
    denominator = s * s * resolvent.determinant
    common = (s + 1) * denominator
    column_mass = (s * s - 1) * resolvent.determinant

    def numerator_operator(rhs):
        return [scalar * value for value in resolvent.adjugate(rhs)]

    previous = [1] + [0] * depth
    current = [(s + 1) * value for value in numerator_operator(previous)]
    power = common
    previous_mass, current_mass = 1, (s + 1) * column_mass
    for _ in range(2, stages + 1):
        rhs = [2 * s * x - (s - 1) * common * y for x, y in zip(current, previous)]
        previous, current = current, numerator_operator(rhs)
        previous_mass, current_mass = (
            current_mass,
            2 * s * column_mass * current_mass - (s - 1) * common * column_mass * previous_mass,
        )
        power *= common
        assert sum(current) == current_mass
    absolute_mass = sum(map(abs, current))
    assert absolute_mass > lower_bound * power
    assert min(current) < 0 < max(current)
    integer_bound = absolute_mass // power
    assert absolute_mass > integer_bound * power
    volumes = [
        branch**i * (branch if i == 0 else 1 if i == depth else branch + 1)
        for i in range(depth + 1)
    ]
    reserve_denominator = 65536
    excess_numerator = sum(
        max(0, reserve_denominator * abs(value) - power * volume)
        for value, volume in zip(current, volumes)
    )
    if (branch, depth, stages) == (10, 64, 213):
        assert excess_numerator == 0
    fingerprint = hashlib.sha256(
        absolute_mass.to_bytes((absolute_mass.bit_length() + 7) // 8, "big")
    ).hexdigest()
    return {
        "branch": branch,
        "depth": depth,
        "vertices": (branch ** (depth + 1) - 1) // (branch - 1),
        "stages": stages,
        "strict_residual_mass_over_alpha_lower_integer": integer_bound,
        "absolute_numerator_bit_length": absolute_mass.bit_length(),
        "denominator_bit_length": power.bit_length(),
        "absolute_numerator_sha256": fingerprint,
        "original_degree_rule": "root b, internal b+1, leaves 1",
        "excess_reserve": "1/65536",
        "excess_is_exactly_zero": excess_numerator == 0,
        "excess_at_most_alpha_over_64": 64 * excess_numerator <= reserve_denominator * power,
        "scope": "ideal exact-inner shifted recurrence; offline equitable equations",
    }


def check_small_realization(branch, depth, stages=6):
    """Compare the level polynomial with actual dense shifted solves."""
    graph = nx.balanced_tree(branch, depth)
    degree = [graph.degree(i) for i in graph]
    level = nx.single_source_shortest_path_length(graph, 0)
    s = 64
    alpha, kappa, beta = F(1, s * s + 1), F(s * s - 1, s * s + 1), F(s - 1, s + 1)
    matrix = [
        [
            (1 + alpha) / 2
            if i == j
            else -(1 - alpha) / (2 * degree[j])
            if graph.has_edge(i, j)
            else F(0)
            for j in graph
        ]
        for i in graph
    ]
    shifted = [
        [value + (kappa if i == j else 0) for j, value in enumerate(row)]
        for i, row in enumerate(matrix)
    ]
    source = [alpha] + [F(0)] * (len(graph) - 1)
    previous_point, point = [F(0)] * len(graph), [F(0)] * len(graph)
    resolvent = IntegerTreeResolvent(branch, depth)
    scale_factor = 2 * (s * s - 1) * (branch + 1)
    common = (s + 1) * s * s * resolvent.determinant
    old_numerator = [1] + [0] * depth
    numerator = [(s + 1) * scale_factor * value for value in resolvent.adjugate(old_numerator)]
    power = common
    for _ in range(stages):
        center = [(1 + beta) * x - beta * y for x, y in zip(point, previous_point)]
        previous_point, point = (
            point,
            solve(shifted, [b + kappa * y for b, y in zip(source, center)]),
        )
        residual = sub(source, mv(matrix, point))
        observed = [
            sum(residual[i] / alpha for i in graph if level[i] == ell) for ell in range(depth + 1)
        ]
        assert observed == [F(value, power) for value in numerator]
        rhs = [2 * s * x - (s - 1) * common * y for x, y in zip(numerator, old_numerator)]
        old_numerator, numerator = (
            numerator,
            [scale_factor * value for value in resolvent.adjugate(rhs)],
        )
        power *= common
    return {
        "branch": branch,
        "depth": depth,
        "vertices": len(graph),
        "stages": stages,
        "scope": "materialized unit graph versus exact level equations",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extended", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_record = provenance(vars(args) | {"output": str(args.output)}, args.output)
    started = time.monotonic()
    frequency = exact_frequency()
    parameters = [(2, 32, 74, 260), (10, 32, 98, 135688)]
    if args.extended:
        parameters.append((10, 64, 213, 138610690000))
    cases = [exact_tree(*values) for values in parameters]
    realizations = [check_small_realization(*values) for values in ((2, 2), (2, 3), (3, 2))]
    record = {
        "provenance": source_record,
        "status": "passed",
        "arithmetic": "exact rational complex frequency and integer finite-tree recurrence",
        "scope": "ideal exact-inner AESP only; no thresholded-inner locality conclusion",
        "case_count": len(cases),
        "frequency": frequency,
        "cases": cases,
        "small_graph_realization_cases": len(realizations),
        "small_graph_realizations": realizations,
        "elapsed_seconds": time.monotonic() - started,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "provenance"}), flush=True)


if __name__ == "__main__":
    main()
