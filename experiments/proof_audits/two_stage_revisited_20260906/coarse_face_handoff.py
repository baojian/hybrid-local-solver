"""Exact audit of the coarse face certificate and a nontrivial reserved GS tail.

Exact face elimination proposes a dyadic candidate which must pass the same
residual test as the imported randomized solver. This does not implement or
measure that randomized primitive. Global reference optima verify the face,
handoff, and output; every coordinate-delivery incidence is metered.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction as F
import json
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .directed_rounding import floor_grid
from .orthant_continuation import ExactObstacle, dot, mv, solve, sub


def check_case(graph, seed, alpha, epsilon, excess_handoff=False):
    n = len(graph)
    degrees = [graph.degree(i) for i in range(n)]
    q0, c = (1 + alpha) / 2, (1 - alpha) / 2
    theta = F(1, 2)
    while theta**2 > alpha:
        theta /= 2
    rho, lam = epsilon / 2, alpha * epsilon / 2
    budget = alpha * theta**2 * rho / 2
    source_budget = budget / 2
    delta = F(1, 2)
    while delta**2 > budget * rho / 4:
        delta /= 2
    threshold = F(1)
    while threshold**2 > alpha * rho * source_budget / 64:
        threshold /= 2
    nu = threshold / 4
    power, blocks = 1, 0
    while power * source_budget < 64:
        power *= 2
        blocks += 1
    cap = blocks * int(1 / theta)
    matrix = [
        [q0 if i == j else -c / degrees[i] if graph.has_edge(i, j) else F(0) for j in range(n)]
        for i in range(n)
    ]
    source = [alpha / degrees[i] if i == seed else F(0) for i in range(n)]
    full_optimum, _ = ExactObstacle(matrix, source).at(lam)
    ppr = solve(matrix, source)

    def objective(x):
        return dot(degrees, x, mv(matrix, x)) / 2 - dot(degrees, sub(source, [lam] * n), x)

    full_value = objective(full_optimum)
    face = {seed}
    counts = Counter()
    for phase in range(cap + 1):
        labels = sorted(face)
        volume = sum(degrees[i] for i in labels)
        principal = [[matrix[i][j] for j in labels] for i in labels]
        face_point = solve(principal, [source[i] - lam for i in labels])
        assert all(value > 0 for value in face_point)
        assert all(value <= full_optimum[i] for i, value in zip(labels, face_point))
        grid = F(1)
        while grid > min(delta, nu * theta / (4 * volume)):
            grid /= 2
        z = [F(0)] * n
        for i, value in zip(labels, face_point):
            z[i] = floor_grid(value, grid)
        full_gradient = [value - load + lam for value, load in zip(mv(matrix, z), source)]
        face_residual_squared = sum(degrees[i] * full_gradient[i] ** 2 for i in labels)
        assert face_residual_squared <= nu**2 * alpha
        candidate = [max(F(0), value - delta) for value in z]
        assert all(0 <= x <= u for x, u in zip(candidate, full_optimum))
        residual = sub(source, mv(matrix, candidate))
        assert min(residual) >= 0
        kkt_squared = sum(
            d * (abs(value - lam) if x > 0 else max(F(0), value - lam)) ** 2
            for d, value, x in zip(degrees, residual, candidate)
        )
        certificate = kkt_squared / (2 * alpha)
        excess_mass = sum(d * max(F(0), value - lam) for d, value in zip(degrees, residual))
        reference_deficit = sum(
            d * (u - value) for d, u, value in zip(degrees, full_optimum, candidate)
        )
        assert reference_deficit <= excess_mass / alpha
        gap = objective(candidate) - full_value
        assert 0 <= gap <= certificate
        counts["accepted_face_solves"] += 1
        counts["face_build_incidences"] += volume
        counts["face_certificate_incidences"] += 3 * volume
        batch = {
            i
            for i in range(n)
            if i not in face
            and full_gradient[i] < 0
            and degrees[i] * full_gradient[i] ** 2 > threshold**2 / 4
        }
        if certificate <= budget:
            reason = "coarse_kkt_certificate"
            break
        if excess_handoff and excess_mass <= alpha * theta:
            reason = "residual_excess_certificate"
            break
        if not batch or phase == cap:
            assert gap <= budget
            reason = "source_algorithm_return"
            break
        assert all(full_optimum[i] > 0 for i in batch)
        face.update(batch)
    else:
        raise AssertionError("Prefix exceeded the source phase cap")
    assert gap <= budget or (excess_handoff and excess_mass <= alpha * theta)
    x = candidate
    counts["tail_updates"] += 0
    counts["tail_incidences"] += 0
    initial_semantic = max(abs(u - value) for u, value in zip(ppr, x))
    initial_max_residual = max(residual)
    deficit = sum(d * (u - value) for d, u, value in zip(degrees, full_optimum, x))
    assert deficit**2 <= 2 * gap / (alpha * rho)
    assert deficit <= theta
    tail_grid = grid
    while tail_grid > alpha * (epsilon - rho) / (2 * q0):
        tail_grid /= 2
    queue = deque(i for i, value in enumerate(residual) if value > alpha * epsilon)
    queued = set(queue)
    counts["tail_initialization_incidences"] = sum(
        degrees[i] for i, value in enumerate(x) if value > 0
    )
    while queue:
        i = queue.popleft()
        queued.remove(i)
        if residual[i] <= alpha * epsilon:
            continue
        ideal = (residual[i] - lam) / q0
        increment = floor_grid(ideal, tail_grid)
        assert ideal / 2 <= increment <= full_optimum[i] - x[i]
        x[i] += increment
        residual[i] -= q0 * increment
        assert lam <= residual[i] < alpha * epsilon
        counts["tail_updates"] += 1
        for j in graph.neighbors(i):
            residual[j] += c * increment / degrees[j]
            counts["tail_incidences"] += 1
            if residual[j] > alpha * epsilon and j not in queued:
                queued.add(j)
                queue.append(j)
        assert counts["tail_incidences"] <= 2 * q0 * deficit / (alpha * (epsilon - rho))
    assert residual == sub(source, mv(matrix, x))
    assert all(0 <= value <= alpha * epsilon for value in residual)
    assert all(0 <= value <= u for value, u in zip(x, full_optimum))
    final_semantic = max(abs(u - value) for u, value in zip(ppr, x))
    assert final_semantic <= epsilon
    return {
        "n": n,
        "seed": seed,
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "prefix_objective_budget": str(budget),
        "source_objective_budget": str(source_budget),
        "prefix_gap": float(gap),
        "prefix_kkt_certificate": float(certificate),
        "prefix_residual_excess_mass": float(excess_mass),
        "residual_excess_handoff_enabled": excess_handoff,
        "prefix_stop_reason": reason,
        "source_phase_cap": cap,
        "face_vertex_count": len(face),
        "face_volume": volume,
        "full_optimal_support_vertex_count": sum(value > 0 for value in full_optimum),
        "initial_semantic_error": float(initial_semantic),
        "initial_max_residual_density": float(initial_max_residual),
        "final_semantic_error": float(final_semantic),
        "tail_grid": str(tail_grid),
        "counts": dict(counts),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extended", action="store_true")
    parser.add_argument("--excess-handoff", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    source_record = provenance(
        {"extended": args.extended, "excess_handoff": args.excess_handoff}, args.output
    )
    rows = []
    sizes = (16, 32, 64, 128) if args.extended else (32, 64)
    alphas = (F(1, 4), F(1, 64), F(1, 1024)) if args.extended else (F(1, 64),)
    powers = (12, 24, 40) if args.extended else (24,)
    for n in sizes:
        for alpha in alphas:
            for power in powers:
                row = check_case(nx.path_graph(n), 0, alpha, F(1, 2**power), args.excess_handoff)
                rows.append(row)
                print(
                    json.dumps(
                        {
                            "passed": len(rows),
                            "last_n": n,
                            "tail_updates": row["counts"]["tail_updates"],
                        }
                    ),
                    flush=True,
                )
    record = {
        "provenance": source_record,
        "status": "passed",
        "scope": "Certified face-solve interface audit; the randomized SDD primitive is not implemented",
        "arithmetic": "exact rational references, accepted dyadic face candidates, dyadic GS tail",
        "case_count": len(rows),
        "elapsed_seconds": time.monotonic() - started,
        "nonempty_tail_cases": sum(row["counts"]["tail_updates"] > 0 for row in rows),
        "cases": rows,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
