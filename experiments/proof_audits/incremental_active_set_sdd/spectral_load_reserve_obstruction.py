"""Exact certificates against coarse spectral replacement plus fixed reserve.

Large trees are specified symbolically and checked through proved local
identities and invariant bounds. Only small trees are materialized for
independent dense Green solves. No general local algorithm or work lower
bound is claimed; every solve here is a proof validator.
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


Q, K = F(3, 17), F(17, 31)


def next_ground(value):
    return F(3, 2) + F(1, 2) * value / (F(1, 2) + value) + F(3, 4) * value / (F(3, 4) + value)


def check_base_identities(counts):
    h0 = F(1, 2)
    h1, h2 = next_ground(h0), next_ground(next_ground(h0))
    assert h1 == F(41, 20)
    assert h2 == F(3, 2) + F(41, 102) + F(123, 224) == F(28001, 11424)
    assert h2 > F(83, 34) and F(1, 2) / (F(1, 2) + h2) < F(17, 100)
    assert next_ground(h2) > h2 > h1 > h0
    assert 3 - F(1, 2) / Q - Q == -F(1, 102)
    assert K * (2 - Q) == 1 and 4 * Q - 2 < 0
    assert 8 * 289**64 < 300**64 and 403 < 408
    counts["rational_subsolution_and_two_step_message_identities"] += 1
    counts["uniform_dyadic_reserve_induction_base"] += 1


def check_symbolic(k, counts):
    reserve, radius = 2**k, 64 * (k + 1)
    depth = 4 * radius
    volume = 2 ** (depth + 2) - 4
    qnumerator, qdenominator = 3**radius, 17**radius
    assert volume * 17 * qnumerator > 248 * qdenominator
    assert 403 * reserve * 289**radius < 51 * 300**radius
    assert radius <= depth - 2
    assert F(13, 4) * F(17, 100) ** radius < 3 * (K * Q**radius / 4) / reserve
    counts["symbolic_large_ambient_original_volume_certificates"] += 1
    counts["symbolic_reserved_penalty_endpoint_omission_certificates"] += 1
    counts["dyadic_reserve_cases"] += 1
    return {
        "reserve_log2": k,
        "radius": radius,
        "tree_depth": depth,
        "original_vertex_count_formula": f"2^{depth + 1}-1",
        "epsilon_formula": f"(17/62)*(3/17)^{radius}",
        "original_alpha": "1/3",
        "original_significant_lower_bound_over_lambda": "2",
        "perturbed_reserved_obstacle_endpoint": "0",
    }


def materialized_green(depth, counts):
    size = 2 ** (depth + 1) - 1
    matrix = [[F(0)] * size for _ in range(size)]
    degrees = []
    for i in range(size):
        degree = int(i > 0) + (2 if 2 * i + 1 < size else 0)
        degrees.append(degree)
        matrix[i][i] += F(degree, 2)
        for child, conductance in [(2 * i + 1, F(1, 2)), (2 * i + 2, F(3, 4))]:
            if child < size:
                matrix[i][i] += conductance
                matrix[child][child] += conductance
                matrix[i][child] -= conductance
                matrix[child][i] -= conductance
    assert [sum(row) for row in matrix] == [F(d, 2) for d in degrees]
    rhs = [F(int(i == 0)) for i in range(size)]
    exact = solve(matrix, rhs)
    assert mv(matrix, exact) == rhs and min(exact) > 0
    ground = [F(0)] * size
    for i in reversed(range(size)):
        ground[i] = F(degrees[i], 2)
        for child, conductance in [(2 * i + 1, F(1, 2)), (2 * i + 2, F(3, 4))]:
            if child < size:
                ground[i] += conductance * ground[child] / (conductance + ground[child])
    lifted = [F(0)] * size
    lifted[0] = 1 / ground[0]
    assert lifted[0] <= 1
    for i in range(size):
        level = (i + 1).bit_length() - 1
        if level <= depth - 2 and i:
            assert ground[i] >= F(28001, 11424)
        for child, conductance in [(2 * i + 1, F(1, 2)), (2 * i + 2, F(3, 4))]:
            if child < size:
                lifted[child] = conductance * lifted[i] / (conductance + ground[child])
    assert lifted == exact
    for level in range(1, max(1, depth - 1)):
        index = 2**level - 1
        assert exact[index] <= F(17, 100) ** level
        assert matrix[index][index] == F(13, 4)
        assert (
            sum(-matrix[index][j] * exact[j] for j in range(size) if j != index)
            == F(13, 4) * exact[index]
        )
        counts["independent_dense_all_left_transfer_bounds"] += 1
    counts["independent_materialized_tree_Green_solves"] += 1
    counts["independent_materialized_tree_Green_rows"] += size
    counts["independent_tree_Schur_and_lifting_identities"] += size


def polynomial_reserve(power, counts):
    radius = 64
    while 403 * (radius + 1) ** power * 289**radius >= 51 * 300**radius:
        radius *= 2
    reserve = (radius + 1) ** power
    assert 403 * reserve * 289**radius < 51 * 300**radius
    counts["explicit_polynomial_in_log_accuracy_reserve_obstructions"] += 1
    return {"power": power, "radius": radius, "reserve_formula": f"(R+1)^{power}"}


def radial_original(radius, counts):
    """Exact original obstacle via the symmetry quotient; proof validator."""
    depth = 4 * radius
    lam = K * Q**radius / 4
    counts_at_level = [2**i for i in range(depth + 1)]
    degree_at_level = [2] + [3] * (depth - 1) + [1]
    matrix = [[F(0)] * (depth + 1) for _ in range(depth + 1)]
    for i in range(depth + 1):
        matrix[i][i] = F(counts_at_level[i] * degree_at_level[i])
        if i < depth:
            matrix[i][i + 1] = matrix[i + 1][i] = -F(counts_at_level[i + 1], 2)
    load = [
        F(int(i == 0)) - lam * count * degree
        for i, (count, degree) in enumerate(zip(counts_at_level, degree_at_level))
    ]
    exact = obstacle(matrix, load)
    candidate = [max(K * Q**i - 2 * lam, F(0)) for i in range(depth + 1)]
    assert all(x <= y for x, y in zip(candidate, exact))
    assert candidate[radius] == 2 * lam > lam / 4 and candidate[radius + 1] == 0
    applied = mv(matrix, exact)
    sub_applied = mv(matrix, candidate)
    for i, (x, a, b, count, degree) in enumerate(
        zip(exact, applied, load, counts_at_level, degree_at_level)
    ):
        assert x >= 0 and a - b >= 0 and x * (a - b) == 0
        residual_per_vertex = (F(int(i == 0)) - a) / count
        assert 0 <= residual_per_vertex <= lam * degree
        if candidate[i] > 0:
            assert sub_applied[i] <= b
    counts["independent_radial_original_obstacle_validators"] += 1
    counts["exact_radial_KKT_and_subsolution_rows"] += depth + 1
    counts["original_significant_depth_R_certificates"] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    counts = Counter()
    check_base_identities(counts)
    examples = []
    for k in range(257 if args.full else 5):
        result = check_symbolic(k, counts)
        if k in [0, 4, 16, 64, 256]:
            examples.append(result)
    polynomial_examples = [polynomial_reserve(power, counts) for power in [0, 1, 2, 4, 8, 16, 32]]
    for depth in range(2, 7 if args.full else 5):
        materialized_green(depth, counts)
    for radius in [1, 2, 4, 8, 16] if args.full else [1, 2, 4]:
        radial_original(radius, counts)
    result = {
        "audit": "incremental_active_set_sdd.spectral_load_reserve_obstruction",
        "scope": "Rule-specific finite-tree obstruction to direct constant-quality spectral matrix replacement with any fixed penalty reserve; no OP3 work lower bound and no general local solver.",
        "arithmetic": "Exact rational identities, symbolic whole-family certificates and explicitly separate small dense validators. Huge trees are not materialized.",
        "parameters": {
            "full": args.full,
            "graph": "Complete binary tree of depth 4R",
            "seed": "root",
            "alpha": "1/3",
            "bar_alpha": "1/2",
            "lambda": "(17/124)*(3/17)^R",
            "eps_appr": "2lambda",
            "delta": "lambda/4",
            "reserve": "C=2^k",
            "radius": "64(k+1)",
            "spectral_quality": "M <= M_hat <= (3/2)M",
            "original_maximum_degree": 3,
            "random_seed": None,
            "stopping_rule": "Explicit local subsolution, two-step Schur invariant and exact endpoint KKT exclusion inequality",
        },
        "audit_only": dict(counts),
        "examples": examples,
        "polynomial_reserve_examples": polynomial_examples,
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
