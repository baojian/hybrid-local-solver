"""Falsification audit for an OPEN path-extremal discounted-hitting claim.

For a q-vertex tree attached to an absorbing center, test
E_i[gamma**tau] >= 1/T_q(1/gamma). This is not used by the proved conservative
bounded-attachment algorithm. All reference systems here are dense.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import cache
import hashlib
import json
from math import comb
from pathlib import Path
import subprocess
import time

from geometric_value_events import solve
import networkx as nx


def chebyshev(q, x):
    previous, value = F(1), x
    for _ in range(1, q):
        previous, value = value, 2 * x * value - previous
    return value


def subtract(left, right):
    result = list(left) + [0] * max(0, len(right) - len(left))
    for i, coefficient in enumerate(right):
        result[i] -= coefficient
    return tuple(result)


def multiply(left, right):
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return tuple(result)


def coefficient_audit(tree, attach):
    """Exact integer polynomial check; it covers all gamma for this finite tree.

    Forest determinants use their matching expansion with ORIGINAL degrees.
    The tree cofactor is the determinant after deleting the unique endpoint
    path. The returned determinant/cofactors are cross-checked against the
    independent rational systems in main.
    """
    q = len(tree)
    degrees = {i: tree.degree(i) + int(i == attach) for i in tree}

    @cache
    def determinant(mask):
        if not mask:
            return (1,)
        i = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << i)
        result = (0,) + tuple(degrees[i] * a for a in determinant(rest))
        for j in tree[i]:
            if rest & (1 << j):
                result = subtract(result, determinant(rest ^ (1 << j)))
        return result

    previous, tc = (1,), (0, 1)
    for _ in range(1, q):
        previous, tc = tc, subtract((0,) + tuple(2 * a for a in tc), previous)
    full = (1 << q) - 1
    det = determinant(full)
    cofactors = []
    for i in tree:
        path_mask = sum(1 << j for j in nx.shortest_path(tree, attach, i))
        cofactor = determinant(full ^ path_mask)
        difference = subtract(multiply(tc, cofactor), det)
        shifted = [
            sum(comb(j, k) * difference[j] for j in range(k, len(difference)))
            for k in range(len(difference))
        ]
        assert all(a >= 0 for a in shifted), (q, list(tree.edges()), attach, i, shifted)
        cofactors.append(cofactor)
    return det, cofactors


def evaluate(coefficients, x):
    result = F(0)
    for coefficient in reversed(coefficients):
        result = result * x + coefficient
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-q", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.time()
    cases = coordinates = sharp = polynomial_checks = 0
    rows = []
    gammas = [F(1, 10), F(3, 4), F(1008, 1009)]
    for q in range(1, args.max_q + 1):
        trees = [nx.empty_graph(1)] if q == 1 else list(nx.nonisomorphic_trees(q))
        for tree in trees:
            for attach in tree:
                det, cofactors = coefficient_audit(tree, attach)
                polynomial_checks += q
                for gamma in gammas:
                    degrees = {i: tree.degree(i) + int(i == attach) for i in tree}
                    matrix = [
                        [
                            F(degrees[i]) if i == j else -gamma if tree.has_edge(i, j) else F(0)
                            for j in tree
                        ]
                        for i in tree
                    ]
                    discounts = solve(matrix, [gamma * int(i == attach) for i in tree])
                    assert discounts == [
                        evaluate(cofactor, 1 / gamma) / evaluate(det, 1 / gamma)
                        for cofactor in cofactors
                    ]
                    threshold = 1 / chebyshev(q, 1 / gamma)
                    assert min(discounts) >= threshold, (q, list(tree.edges()), attach, gamma)
                    if min(discounts) == threshold:
                        assert max(dict(tree.degree()).values()) <= 2
                        assert tree.degree(attach) <= 1
                        sharp += 1
                    cases += 1
                    coordinates += len(discounts)
        rows.append({"q": q, "tree_shapes": len(trees), "cumulative_cases": cases})
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.discounted_attachment_extremal",
        "claim_status": "Open; finite exact checks do not prove the path-extremal inequality",
        "arithmetic": "exact fractions and integer polynomial coefficients; audit only",
        "max_q": args.max_q,
        "gamma": list(map(str, gammas)),
        "alpha_lazy": [str((1 - g) / (1 + g)) for g in gammas],
        "lambda": "not applicable to this dimensionless hitting transform",
        "seed": "absorbing center attached at every possible tree vertex",
        "random_seed": None,
        "cases": cases,
        "coordinate_inequalities": coordinates,
        "sharp_path_cases": sharp,
        "nonnegative_polynomial_checks": polynomial_checks,
        "polynomial_scope": "all gamma in (0,1) for the enumerated finite rooted trees only",
        "rows": rows,
        "git_commit": subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
        ).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(
                ["git", "-C", str(repo), "status", "--porcelain"], text=True
            ).strip()
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.time() - started, 3),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
