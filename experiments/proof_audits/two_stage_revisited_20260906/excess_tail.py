"""Exact residual-excess tail audit, including prefixes above the RPPR optimum.

Reference PPR points construct external handoff witnesses, not a free prefix
algorithm. The tail uses its actual residual queue and meters every incidence.
"""

from __future__ import annotations

import argparse
from collections import deque
from fractions import Fraction as F
import json
from pathlib import Path
import time

import networkx as nx

from . import provenance
from .directed_rounding import floor_grid
from .orthant_continuation import ExactObstacle, dot, mv, solve, sub


def check_case(graph, seed, alpha, mode, rounded):
    n = len(graph)
    degree = [graph.degree(i) for i in graph]
    q0, c = (1 + alpha) / 2, (1 - alpha) / 2
    theta = F(1, 2)
    while theta**2 > alpha:
        theta /= 2
    epsilon, rho = F(1, 65536), F(1, 131072)
    lam = alpha * rho
    matrix = [
        [q0 if i == j else -c / degree[i] if graph.has_edge(i, j) else F(0) for j in graph]
        for i in graph
    ]
    source = [alpha / degree[i] if i == seed else F(0) for i in graph]
    ppr = solve(matrix, source)
    optimum, _ = ExactObstacle(matrix, source).at(lam)
    if mode == "scaled_ppr":
        x = [(1 - theta / 8) * value for value in ppr]
    else:
        x = ppr.copy()
        x[seed] -= min(x[seed] / 2, alpha * theta / (8 * q0 * degree[seed]))
    grid = F(1, 2**50)
    if rounded:
        x = [floor_grid(value, grid) for value in x]
    initial = x.copy()
    residual = sub(source, mv(matrix, x))

    def excess():
        return sum(d * max(F(0), value - lam) for d, value in zip(degree, residual))

    initial_excess = excess()
    assert initial_excess <= alpha * theta
    initial_nonnegative = min(residual) >= 0
    above_rppr = any(value > u for value, u in zip(x, optimum))
    difference = sub(x, optimum)
    optimal_gradient = [value - b + lam for value, b in zip(mv(matrix, optimum), source)]
    gap = dot(degree, difference, mv(matrix, difference)) / 2
    gap += dot(degree, optimal_gradient, difference)
    queue = deque(i for i in graph if residual[i] > alpha * epsilon)
    queued = set(queue)
    incidences = updates = 0
    while queue:
        i = queue.popleft()
        queued.remove(i)
        if residual[i] <= alpha * epsilon:
            continue
        previous_excess = excess()
        ideal = (residual[i] - lam) / q0
        increment = floor_grid(ideal, grid) if rounded else ideal
        assert ideal / 2 <= increment <= ppr[i] - x[i]
        x[i] += increment
        residual[i] -= q0 * increment
        for neighbor in graph.neighbors(i):
            residual[neighbor] += c * increment / degree[neighbor]
            incidences += 1
            if residual[neighbor] > alpha * epsilon and neighbor not in queued:
                queued.add(neighbor)
                queue.append(neighbor)
        updates += 1
        assert excess() <= previous_excess - alpha * degree[i] * increment
        factor = 2 if rounded else 1
        assert incidences <= factor * q0 * initial_excess / (alpha**2 * (epsilon - rho))
        assert all(0 <= value <= u for value, u in zip(x, ppr))
    assert residual == sub(source, mv(matrix, x))
    assert max(residual) <= alpha * epsilon
    assert max(u - value for u, value in zip(ppr, x)) <= epsilon
    if initial_nonnegative:
        assert min(residual) >= 0
    return {
        "n": n,
        "seed": seed,
        "alpha": str(alpha),
        "eps_ppr": str(epsilon),
        "initial_mode": mode,
        "rounded": rounded,
        "initial_above_rppr_somewhere": above_rppr,
        "initial_residual_nonnegative": initial_nonnegative,
        "initial_excess_mass": str(initial_excess),
        "initial_objective_gap": float(gap),
        "gap_exceeds_old_handoff_budget": gap > alpha * theta**2 * rho / 2,
        "initialization_incidences": sum(d for d, value in zip(degree, initial) if value),
        "tail_incidences": incidences,
        "tail_updates": updates,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_record = provenance({}, args.output)
    started = time.monotonic()
    rows = []
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= 4 or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in (F(1, 4), F(1, 64)):
                for mode in ("scaled_ppr", "local_deficit"):
                    for rounded in (False, True):
                        row = check_case(graph, seed, alpha, mode, rounded)
                        row["atlas_id"] = atlas_id
                        rows.append(row)
    record = {
        "provenance": source_record,
        "status": "passed",
        "scope": "Exact handoff interface; reference-generated prefixes are not a prefix algorithm",
        "arithmetic": "exact rational with separately rounded coordinate tails",
        "case_count": len(rows),
        "above_rppr_cases": sum(row["initial_above_rppr_somewhere"] for row in rows),
        "larger_objective_gap_cases": sum(row["gap_exceeds_old_handoff_budget"] for row in rows),
        "nonempty_tail_cases": sum(row["tail_updates"] > 0 for row in rows),
        "elapsed_seconds": time.monotonic() - started,
        "cases": rows,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
