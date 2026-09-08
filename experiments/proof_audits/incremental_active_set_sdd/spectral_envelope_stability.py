"""Exact validators for sharp spectral stability of obstacle envelopes.

Perturbed-matrix certificates are labelled separately from original ACL
certificates. All dense and prefix solves are proof validators. No general
local discovery algorithm or spectral factorization backend is implemented.
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

from conservative_parameter_obstruction import path_matrix
from geometric_value_events import mv, obstacle, solve
import networkx as nx


def quadratic(matrix, values):
    return sum(x * y for x, y in zip(values, mv(matrix, values)))


def certificate(matrix, values, degrees, seed, lam):
    applied = mv(matrix, values)
    for i, (x, a, d) in enumerate(zip(values, applied, degrees)):
        r = F(int(i == seed)) - a
        assert x >= 0 and 0 <= r <= lam * d
        assert x * (lam * d - r) == 0


def check_pair(matrix, changed, degrees, seed, epsilon, eta, counts, original=None):
    assert 0 < eta <= F(1, 2)
    assert sum(degrees) > 4 / epsilon
    lam, delta = epsilon / 2, epsilon / 8
    load = [F(int(i == seed)) - lam * d for i, d in enumerate(degrees)]
    u = obstacle(matrix, load) if original is None else original
    v = obstacle(changed, load)
    certificate(matrix, u, degrees, seed, lam)
    certificate(changed, v, degrees, seed, lam)
    su = [i for i, x in enumerate(u) if x > 0]
    sv = [i for i, x in enumerate(v) if x > 0]
    union = sorted(set(su) | set(sv))
    vu = sum(degrees[i] for i in su)
    vv = sum(degrees[i] for i in sv)
    volume = sum(degrees[i] for i in union)
    assert vu <= 2 / epsilon and vv <= 2 / epsilon
    assert volume <= 4 / epsilon < sum(degrees)
    difference = [y - x for x, y in zip(u, v)]
    energy = quadratic(matrix, difference)
    initial_energy = quadratic(matrix, u)
    assert (1 - eta) ** 2 * energy <= eta**2 * initial_energy
    assert initial_energy == sum(b * x for b, x in zip(load, u)) <= max(u) <= 2 * vu
    assert (1 - eta) ** 2 * max(x * x for x in difference) <= 32 * eta**2 / epsilon**2
    if union:
        local = [[matrix[i][j] for j in union] for i in union]
        maximum = max(range(len(union)), key=lambda k: abs(difference[union[k]]))
        rhs = [F(int(i == maximum)) for i in range(len(union))]
        green = solve(local, rhs)
        assert green[maximum] <= 2 * volume <= 8 / epsilon
        assert difference[union[maximum]] ** 2 <= green[maximum] * energy
        counts["exact_union_Dirichlet_diagonal_validators"] += 1
    else:
        assert not any(u) and not any(v)
        counts["empty_obstacle_pairs"] += 1
    if eta <= epsilon**2 / 192:
        assert max(abs(x) for x in difference) <= epsilon / 16
        assert all(v[i] > 0 for i, x in enumerate(u) if x > delta)
        counts["safe_accuracy_squared_envelope_containments"] += 1
    counts["same_load_obstacle_pairs"] += 1
    counts["original_matrix_KKT_and_residual_certificates"] += 1
    counts["perturbed_matrix_KKT_and_residual_certificates"] += 1
    counts["variational_energy_and_coordinate_stability_checks"] += 1
    return u, v


def graph_pair(graph, t, eta, rng, one_sided):
    n = len(graph)
    degrees = [graph.degree(i) for i in graph]
    base = [[F(0)] * n for _ in range(n)]
    changed = [[F(0)] * n for _ in range(n)]
    for i, j in graph.edges:
        multiplier = 1 + eta * F(rng.choice([0, 1, 2] if one_sided else [-2, -1, 0, 1, 2]), 2)
        assert 1 - eta <= multiplier <= 1 + eta
        for matrix, weight in [(base, 1 - t), (changed, (1 - t) * multiplier)]:
            matrix[i][i] += weight
            matrix[j][j] += weight
            matrix[i][j] -= weight
            matrix[j][i] -= weight
    for i, d in enumerate(degrees):
        multiplier = 1 + eta * F(rng.choice([0, 1, 2] if one_sided else [-2, -1, 0, 1, 2]), 2)
        base[i][i] += t * d
        changed[i][i] += t * d * multiplier
    assert all(sum(row) >= 0 for row in changed)
    assert all(changed[i][j] <= 0 for i in range(n) for j in range(n) if i != j)
    return base, changed, degrees


def weighted_prefix(rhs, conductances):
    """Audit-only weighted Dirichlet path inverse with zero endpoints."""
    assert len(conductances) == len(rhs) + 1
    cumulative = F(0)
    numerator = F(0)
    denominator = F(0)
    for j, conductance in enumerate(conductances):
        numerator += cumulative / conductance
        denominator += 1 / conductance
        if j < len(rhs):
            cumulative += rhs[j]
    flow = numerator / denominator
    value = F(0)
    answer = []
    for j, conductance in enumerate(conductances):
        value += flow / conductance
        if j < len(rhs):
            answer.append(value)
            flow -= rhs[j]
    assert value == 0
    return answer


def path_obstruction(n, counts, dense=False):
    lam = F(2 * n, 8 * n * n + 1)
    epsilon, delta = 2 * lam, lam / 4
    eta, t = F(1, n * n), epsilon**4 / 128
    relative = eta / (1 - t)
    first = (1 - lam * (4 * n - 2 + eta * (n - 1))) / (2 + eta)
    assert first - lam == (1 - 2 * eta * n * n) / ((2 + eta) * (8 * n * n + 1)) < 0
    assert F(1, 8 * n * n + 1) <= first < lam
    conductances = [F(1)] * n + [1 + eta] * n
    flows = [first + 2 * lam * (i - 1) - int(i > n) for i in range(1, 2 * n + 1)]
    assert all(x > 0 for x in flows[:n]) and all(x < 0 for x in flows[n:])
    value = F(0)
    local = []
    for flow, conductance in zip(flows, conductances):
        value += flow / conductance
        local.append(value)
    assert local[-1] == 0 and all(x > 0 for x in local[:-1])
    rhs = [F(int(i == n)) - 2 * lam for i in range(1, 2 * n)]
    assert weighted_prefix(rhs, conductances) == local[:-1]
    z = [F(0)] + local + [F(0)] * (6 * n)
    assert len(z) == 8 * n + 1
    edge_weights = [1 + eta if n < i <= 2 * n else F(1) for i in range(1, 8 * n + 1)]
    for i, x in enumerate(z):
        original_degree = 1 if i in [0, 8 * n] else 2
        laplacian_value = F(0)
        neighbor_sum = F(0)
        if i:
            laplacian_value += edge_weights[i - 1] * (x - z[i - 1])
            neighbor_sum += z[i - 1]
        if i < 8 * n:
            laplacian_value += edge_weights[i] * (x - z[i + 1])
            neighbor_sum += z[i + 1]
        b = F(int(i == n)) - lam * original_degree
        gradient = laplacian_value - b
        assert gradient >= 0 and x * gradient == 0
        assert laplacian_value + t * neighbor_sum >= b
    assert 0 < relative < F(2, n * n)
    assert 4 < relative / epsilon**2 < 5
    assert lam / 2 == 2 * delta and z[0] == 0
    counts["weighted_path_obstacle_KKT_certificates"] += 1
    counts["weighted_path_original_degree_load_rows"] += len(z)
    counts["positive_target_zero_endpoint_supersolutions"] += 1
    counts["exact_weighted_prefix_Dirichlet_validators"] += 1
    counts["accuracy_squared_spectral_obstructions"] += 1
    if dense:
        base = path_matrix(len(z), t)
        changed = [list(row) for row in base]
        for i in range(n, 2 * n):
            changed[i][i] += eta
            changed[i + 1][i + 1] += eta
            changed[i][i + 1] -= eta
            changed[i + 1][i] -= eta
        degrees = [1] + [2] * (8 * n - 1) + [1]
        u, v = check_pair(base, changed, degrees, n, epsilon, relative, counts)
        assert u[0] > 3 * delta / 2 and v[0] == 0
        assert all(x <= y for x, y in zip(v, z))
        counts["independent_dense_spectral_endpoint_obstructions"] += 1
    return {
        "N": n,
        "epsilon": str(epsilon),
        "relative_spectral_error": str(relative),
        "error_over_epsilon_squared": str(relative / epsilon**2),
        "weighted_endpoint": str(z[0]),
        "original_conservative_endpoint": str(lam / 2),
    }


def sign_obstruction(m, eta, counts):
    gamma, lam = F(1, 2), F(3, 4)
    graph = nx.star_graph(m)
    base, _, degrees = graph_pair(graph, 1 - gamma, eta, random.Random(0), True)
    clique = [[F(0)] * (m + 1) for _ in range(m + 1)]
    pivot = [F(m)] + [-gamma] * m
    for i in range(1, m + 1):
        for j in range(1, m + 1):
            clique[i][j] = gamma**2 * (F(int(i == j)) - F(1, m))
    changed = [[base[i][j] - eta * clique[i][j] for j in range(m + 1)] for i in range(m + 1)]
    for i in range(m + 1):
        assert sum(changed[i]) == sum(base[i]) > 0
        for j in range(m + 1):
            grounding = 1 - gamma**2 if i == j and i > 0 else F(0)
            assert base[i][j] == pivot[i] * pivot[j] / m + grounding + clique[i][j]
    assert changed[1][2] == eta * gamma**2 / m > 0
    x = [F(0)] * (m + 1)
    x[1] = (1 - lam) / changed[1][1]
    applied = mv(changed, x)
    load = [F(int(i == 1)) - lam * d for i, d in enumerate(degrees)]
    assert all(a - b >= 0 and value * (a - b) == 0 for a, b, value in zip(applied, load, x))
    assert -applied[2] < 0
    counts["spectral_factor_product_sign_counterexamples"] += 1
    counts["exact_single_leaf_KKT_with_negative_outside_residual"] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    counts = Counter()
    rng = random.Random(20260908)
    for graph in nx.graph_atlas_g():
        if len(graph) < 2 or len(graph) > (6 if args.full else 4) or not nx.is_connected(graph):
            continue
        for epsilon in [F(1, 2), F(3, 4)]:
            if sum(dict(graph.degree()).values()) <= 4 / epsilon:
                continue
            for seed in graph:
                for t in [F(0), F(1, 3), F(1)]:
                    original = None
                    for eta in [epsilon**2 / 192, F(1, 16), F(1, 2)]:
                        for one_sided in [False, True]:
                            matrix, changed, degrees = graph_pair(graph, t, eta, rng, one_sided)
                            u, _ = check_pair(
                                matrix, changed, degrees, seed, epsilon, eta, counts, original
                            )
                            original = u
                            counts[
                                "one_sided_edge_grounding_perturbations"
                                if one_sided
                                else "two_sided_edge_grounding_perturbations"
                            ] += 1
    sizes = (
        sorted(set(range(4, 129)) | {255, 256, 511, 512, 1024, 2048, 4096})
        if args.full
        else [4, 8, 16]
    )
    examples = []
    for n in sizes:
        result = path_obstruction(n, counts, dense=n in [4, 5, 8])
        if n in [4, 8, 128, 1024, 4096]:
            examples.append(result)
    for m in [3, 4, 8, 16]:
        for eta in [F(1, 2), F(1, 16), F(1, 1024)]:
            sign_obstruction(m, eta, counts)
    result = {
        "audit": "incremental_active_set_sdd.spectral_envelope_stability",
        "scope": "Exact same-load matrix-replacement stability, weighted-path support obstruction and missing sign-condition certificates. No running-time lower bound or general local solver is claimed.",
        "arithmetic": "All dense and prefix computations are explicitly proof validators; perturbed-matrix residuals are not called original ACL certificates.",
        "parameters": {
            "full": args.full,
            "lambda": "eps_appr/2",
            "delta": "eps_appr/8",
            "safe_relative_spectral_accuracy": "eps_appr^2/192",
            "path_bar_alpha": "eps_appr^4/128",
            "path_extra_edge_weight": "1/N^2",
            "random_seed": 20260908,
            "stopping_rule": "Exact obstacle KKT or explicit prefix certificate, followed by row and energy validation",
        },
        "audit_only": dict(counts),
        "examples": examples,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ["geometric_value_events.py", "conservative_parameter_obstruction.py"]
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
