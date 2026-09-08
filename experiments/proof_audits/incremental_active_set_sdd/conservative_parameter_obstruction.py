"""Exact path certificates for a rule-specific fourth-power obstruction.

All computations here are proof validators, not a proposed general local
solver. Prefix Dirichlet solves make large certificates inexpensive; small
cases independently use the existing dense obstacle reference. No running-
time lower bound for OP3 follows from this support-containment obstruction.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from geometric_value_events import mv, obstacle, solve


def adjacent(values):
    return [
        (values[i - 1] if i else F(0)) + (values[i + 1] if i + 1 < len(values) else F(0))
        for i in range(len(values))
    ]


def prefix_dirichlet(rhs, counts):
    """Audit-only exact inverse of tridiagonal (2,-1,-1), with zero ends."""
    size = len(rhs)
    step = sum((size - j) * value for j, value in enumerate(rhs)) / (size + 1)
    value = F(0)
    answer = []
    for load in rhs:
        value += step
        answer.append(value)
        step -= load
    assert value + step == 0
    applied = [2 * x - y for x, y in zip(answer, adjacent(answer))]
    assert applied == rhs
    counts["exact_prefix_Dirichlet_solves"] += 1
    counts["prefix_solve_rows_checked"] += size
    return answer


def path_matrix(size, t):
    return [
        [
            F(1 if i in (0, size - 1) else 2) if i == j else t - 1 if abs(i - j) == 1 else F(0)
            for j in range(size)
        ]
        for i in range(size)
    ]


def check_case(n, counts, dense=False):
    assert n >= 4
    lam = F(2 * n, 8 * n * n + 1)
    epsilon, delta = 2 * lam, lam / 4
    t = F(1, n**4)
    lazy = t / (2 - t)
    assert 2 * lazy / (1 + lazy) == t
    assert 16 * n > 4 / epsilon and 4 * n - 1 < 1 / lam
    original = [
        n - lam * (4 * n * n - i * i)
        if i <= n
        else (2 * n - i) * (1 - lam * (2 * n + i))
        if i <= 2 * n
        else F(0)
        for i in range(8 * n + 1)
    ]
    assert original[0] == lam / 2 == 2 * delta
    assert original[2 * n - 1] == lam * (1 + F(1, 2 * n)) <= 2 * lam
    assert all(x > 0 for x in original[: 2 * n])
    assert not any(original[2 * n :])
    degrees = [1] + [2] * (8 * n - 1) + [1]
    load = [F(int(i == n)) - lam * d for i, d in enumerate(degrees)]
    av = adjacent(original)
    for i, (x, neighbor_sum, d, b) in enumerate(zip(original, av, degrees, load)):
        gradient = d * x - neighbor_sum - b
        assert gradient >= 0 and x * gradient == 0
        residual = F(int(i == n)) - d * x + neighbor_sum
        assert 0 <= residual <= lam * d
    counts["exact_conservative_obstacle_KKT_certificates"] += 1
    counts["original_conservative_residual_rows"] += len(original)

    v = [F(min(i, 2 * n - i), 2) - lam * i * (2 * n - i) for i in range(1, 2 * n)]
    w = [F(i * (2 * n - i)) for i in range(1, 2 * n)]
    assert [2 * x - y for x, y in zip(v, adjacent(v))] == load[1 : 2 * n]
    assert [2 * x - y for x, y in zip(w, adjacent(w))] == [2] * len(w)
    assert max(v) <= F(n, 3) and max(w) == n * n
    assert all(x / y >= v[0] / w[0] >= F(1, 9 * n * n) for x, y in zip(v, w))
    assert sum(v) == F(n * n * (8 * n * n + 7), 6 * (8 * n * n + 1)) >= F(n * n, 6)
    assert v[0] - lam == F(1, 2 * (8 * n * n + 1)) <= F(1, 16 * n * n)
    assert v[0] <= F(3, 8 * n)

    h = prefix_dirichlet(adjacent(v), counts)
    k = prefix_dirichlet(adjacent(h), counts)
    assert all(F(0) <= y <= F(n, 3) * z for y, z in zip(h, w))
    assert h[0] == sum(v) - v[0] >= F(n * n, 8)
    assert max(h) <= F(n**3, 3) and max(k) <= F(n**5, 3)
    assert k[0] <= F(2 * n**4, 3)
    z = [x - t * y + t * t * q for x, y, q in zip(v, h, k)]
    assert all(x - t * y > 0 for x, y in zip(v, h))
    assert z == list(reversed(z))
    assert z[0] - lam <= -F(1, 16 * n * n) + F(2, 3 * n**4) < 0
    ak = adjacent(k)
    applied = [2 * x - (1 - t) * y for x, y in zip(z, adjacent(z))]
    assert applied == [b + t**3 * q for b, q in zip(load[1 : 2 * n], ak)]
    assert all(F(0) <= t**3 * q <= F(2, 3 * n**7) < 2 * lam for q in ak)
    candidate = [F(0)] + z + [F(0)] * (6 * n + 1)
    assert len(candidate) == len(original)
    neighbors = adjacent(candidate)
    for i, (x, neighbor_sum, d) in enumerate(zip(candidate, neighbors, degrees)):
        residual = F(int(i == n)) - d * x + (1 - t) * neighbor_sum
        assert F(0) <= residual <= lam * d
    assert candidate[0] == 0 and original[0] > delta
    assert sum(d for d, x in zip(degrees, candidate) if x > 0) == 4 * n - 2 < 1 / lam
    assert t / epsilon**4 == F((8 * n * n + 1) ** 4, 256 * n**8) > 16
    counts["exact_positive_target_ACL_certificates"] += 1
    counts["original_positive_target_residual_rows"] += len(original)
    counts["significant_endpoint_omissions"] += 1
    counts["path_cases"] += 1

    if dense:
        local = [
            [F(2) if i == j else F(-1) if abs(i - j) == 1 else F(0) for j in range(len(v))]
            for i in range(len(v))
        ]
        assert solve(local, adjacent(v)) == h
        assert solve(local, adjacent(h)) == k
        counts["independent_dense_Dirichlet_validators"] += 2
        for parameter in [epsilon**4 / 128, t, 2 * t, F(1, n * n), F(1)]:
            matrix = path_matrix(len(original), parameter)
            target = obstacle(matrix, load)
            gradient = [a - b for a, b in zip(mv(matrix, target), load)]
            assert all(x >= 0 and g >= 0 and x * g == 0 for x, g in zip(target, gradient))
            assert all(x <= y for x, y in zip(target, original))
            if parameter == epsilon**4 / 128:
                assert target[0] > delta / 2
                assert all(x - y < delta / 2 for x, y in zip(original, target))
                counts["safe_fourth_power_parameter_containments"] += 1
            else:
                assert target[0] == 0
                counts["independent_dense_obstacle_endpoint_omissions"] += 1
            if parameter == t:
                assert all(x <= y for x, y in zip(target, candidate))
            counts["independent_dense_original_obstacle_validators"] += 1

    return {
        "N": n,
        "epsilon": str(epsilon),
        "bar_alpha": str(t),
        "bar_alpha_over_epsilon_fourth": str(t / epsilon**4),
        "conservative_endpoint": str(original[0]),
        "significance_threshold": str(delta),
        "candidate_endpoint": str(candidate[0]),
        "first_positive_value_margin": str(lam - z[0]),
        "original_output_volume": 4 * n - 2,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    counts = Counter()
    sizes = (
        sorted(set(range(4, 129)) | {255, 256, 511, 512, 1023, 1024, 2047, 2048, 4095, 4096})
        if args.full
        else [4, 5, 8, 16]
    )
    examples = []
    for n in sizes:
        result = check_case(n, counts, dense=n in [4, 5, 8])
        if n in [4, 8, 128, 1024, 4096]:
            examples.append(result)
    result = {
        "audit": "incremental_active_set_sdd.conservative_parameter_obstruction",
        "scope": "Exact path supersolution and original ACL certificates; a rule-specific obstruction to replacing the fourth-power conservative-support comparison scale. Not an OP3 work lower bound.",
        "arithmetic": "Exact fractions; all computations, including linear prefix solves and small dense obstacle comparisons, are proof validators.",
        "parameters": {
            "full": args.full,
            "graph": "Original path 0,...,8N, seeded at N; N>=4",
            "lambda": "2N/(8N^2+1)",
            "eps_appr": "2lambda",
            "ACL_accuracy_of_counterexample": "lambda",
            "delta": "lambda/4",
            "bar_alpha": "1/N^4",
            "alpha": "bar_alpha/(2-bar_alpha)",
            "random_seed": None,
            "stopping_rule": "Explicit closed-form/prefix certificate followed by exact original row validation",
        },
        "audit_only": dict(counts),
        "examples": examples,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "geometric_value_events.py": hashlib.sha256(
                Path(__file__).with_name("geometric_value_events.py").read_bytes()
            ).hexdigest()
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
