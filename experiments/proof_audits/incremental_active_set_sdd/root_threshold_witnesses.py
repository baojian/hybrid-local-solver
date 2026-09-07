"""Canonical tree witnesses for root-threshold shortcuts and group counts.

Every computation is an exact audit oracle. The large family is represented
by original degree data on a backbone and implicit inactive pendant stars.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

from geometric_value_events import solve
import networkx as nx
from root_threshold_order import Reference, witness


def acl_witness():
    graph = nx.Graph()
    graph.add_nodes_from(range(15))
    graph.add_edges_from(
        [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 6), (4, 7), (3, 8), (6, 9)]
        + [(8, i) for i in range(10, 14)]
        + [(9, 14)]
    )
    alpha, lam = F(1, 1009), F(2, 51)
    counts = Counter()
    ref = Reference(graph, 0, alpha, 2 * lam, counts)
    face, trace, gates = ref.face({0}), [0], []
    target = set(range(7))
    while face.labels != target:
        legal = [i for i, (a, b, _) in face.rows.items() if i in target and a * face.root + b > 0]
        assert legal
        i = min(legal)
        gates.append({"admitted": i, "gate": str(face.rows[i][0] * face.root + face.rows[i][1])})
        after = ref.face(face.labels | {i})
        ref.update(face, after, i)
        trace.append(i)
        face = after
    assert [i for i, (a, b, _) in face.rows.items() if a * face.root + b > 0] == [7]
    assert face.rows[8][2] < face.rows[9][2]
    after = ref.face(face.labels | {7})
    _, factors = ref.update(face, after, 7)
    ga = after.rows[8][0] * after.root + after.rows[8][1]
    gb = after.rows[9][0] * after.root + after.rows[9][1]
    assert ga < 0 and gb > lam * graph.degree(9)
    result = witness(
        ref,
        "smallest legal target-prefix label, then unique positive",
        trace,
        face,
        after,
        7,
        (8, 9),
        factors,
    )
    result["prefix_admission_gates"] = gates
    result["physical_residual_at_missed_vertex"] = str(gb + lam * graph.degree(9))
    result["acl_tolerance_at_missed_vertex"] = str(2 * lam * graph.degree(9))
    result["acl_violation_ratio"] = str((gb + lam * graph.degree(9)) / (2 * lam * graph.degree(9)))
    result["acl_violation_ratio_decimal"] = float(F(result["acl_violation_ratio"]))
    result["reference_counts"] = dict(counts)
    return result


def path_solve(diagonal, gamma, rhs):
    """Independent tridiagonal elimination, used only by this audit."""
    pivots, loads = list(diagonal), list(rhs)
    for i in range(1, len(pivots)):
        pivots[i] -= gamma * gamma / pivots[i - 1]
        loads[i] += gamma * loads[i - 1] / pivots[i - 1]
    out = [F(0)] * len(pivots)
    out[-1] = loads[-1] / pivots[-1]
    for i in reversed(range(len(pivots) - 1)):
        out[i] = (loads[i] + gamma * out[i + 1]) / pivots[i]
    return out


def many_group_case(m):
    alpha, bar = F(1, 1009), F(1, 505)
    gamma, lam = 1 - bar, bar / (12 * 6**m)
    epsilon, report_degree = 2 * lam, 12 * 6**m * 505**2
    degree = [F(2)] + [F(3)] * (m - 1) + [F(1)]
    counts, last = Counter(), None
    for k in range(m + 1):
        labels = list(range(k + 1))
        diagonal = degree[: k + 1]
        src = [F(i == 0) for i in labels]
        load = [src[i] - lam * degree[i] for i in labels]
        values = path_solve(diagonal, gamma, load)
        assert min(values) > 0
        if k < m:
            next_flux = gamma * values[-1]
            assert next_flux > F(3, 4) * epsilon * degree[k + 1]
            counts["forced_next_ready_checks"] += 1
        for i in range(min(k + 1, m)):
            assert gamma * values[i] < lam * report_degree
            counts["quiet_report_checks"] += 1
        harmonic = (
            [F(1)] + path_solve(diagonal[1:], gamma, [gamma] + [F(0)] * (k - 1)) if k else [F(1)]
        )
        resistance = [F(0)]
        for i in range(1, k + 1):
            resistance.append(resistance[-1] + 1 / (gamma * harmonic[i - 1] * harmonic[i]))
        if last is not None:
            old_h, old_r, old_values = last
            q = k - 1
            # The old interior Green diagonal is H_q^2 R_q.
            pivot = degree[k] - gamma * gamma * old_h[q] ** 2 * old_r[q]
            assert pivot > 0
            kappa = gamma * gamma * old_h[q] ** 2 / pivot
            factors = [1 / (1 + kappa * old_r[i]) for i in range(k)]
            assert all(a > b for a, b in zip(factors, factors[1:]))
            assert len(set(factors)) == k
            for i in range(k):
                assert harmonic[i] == old_h[i] * (1 + kappa * old_r[i])
                assert resistance[i] == old_r[i] / (1 + kappa * old_r[i])
                assert values[i] > old_values[i]
            counts["distinct_group_maps"] += k
            counts["nonidentity_group_maps"] += k - 1
            counts["harmonic_and_resistance_checks"] += k
        if m <= 8 or k in {0, m // 2, m}:
            matrix = [
                [diagonal[i] if i == j else -gamma if abs(i - j) == 1 else F(0) for j in labels]
                for i in labels
            ]
            assert solve(matrix, load) == values
            counts["independent_dense_face_comparisons"] += 1
        last = (harmonic, resistance, values)
    assert counts["nonidentity_group_maps"] == m * (m - 1) // 2
    final_residuals = [
        F(i == 0)
        - degree[i] * values[i]
        + gamma * sum(values[j] for j in [i - 1, i + 1] if 0 <= j <= m)
        for i in range(m + 1)
    ]
    assert final_residuals == [lam * d for d in degree]
    return {
        "backbone_edges": m,
        "ambient_vertices": m * report_degree + m + 1,
        "report_degree": report_degree,
        "alpha_lazy": str(alpha),
        "eps_appr": str(epsilon),
        "lambda": str(lam),
        "positive_vertices": m + 1,
        "support_volume": int(sum(degree)),
        "maximum_distinct_maps": m,
        "reference_counts": dict(counts),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    result = {
        "audit": "incremental_active_set_sdd.root_threshold_witnesses",
        "arithmetic": "exact fractions",
        "seed": 0,
        "random_seed": None,
        "cost_scope": "all computations are audit-only; no local solver implementation claimed",
        "acl_shortcut_witness": acl_witness(),
        "many_group_family": [many_group_case(m) for m in [4, 8, 16, 32]],
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reference_backend_sha256": hashlib.sha256(
            Path(__file__).with_name("root_threshold_order.py").read_bytes()
        ).hexdigest(),
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
