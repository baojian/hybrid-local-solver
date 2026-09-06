"""Exact audit of the RPPR-relative deficit handoff and reserved GS tail.

Dense reference arrays supply external invariant checks. This verifies the
coordinate sequence and adjacency ledger, not a local-runtime implementation.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction as F
import json

import networkx as nx

from .directed_rounding import floor_grid
from .orthant_continuation import ExactObstacle, dot, mv, solve, sub


def run_case(graph, seed, alpha, epsilon, initial_mode, rounded):
    n = len(graph)
    degree = [graph.degree(i) for i in range(n)]
    q0, c = (1 + alpha) / 2, (1 - alpha) / 2
    rho = epsilon / 2
    lam = alpha * rho
    theta = F(1, 2)
    while theta**2 > alpha:
        theta /= 2
    matrix = [
        [q0 if i == j else -c / degree[i] if graph.has_edge(i, j) else F(0) for j in range(n)]
        for i in range(n)
    ]
    source = [alpha / degree[i] if i == seed else F(0) for i in range(n)]
    optimum, _ = ExactObstacle(matrix, source).at(lam)
    ppr = solve(matrix, source)
    x = optimum.copy()
    if initial_mode == "scale":
        x = [value / 2 for value in x]
    elif initial_mode == "drop_seed":
        x[seed] -= min(x[seed] / 2, theta / (2 * degree[seed]))
    elif initial_mode == "cycle_certificate":
        assert n == 16 and alpha == F(1, 64) and epsilon == F(1, 65536)
        x = [value - F(1, 32768) for value in x]
        assert all(value > 0 for value in x)
    else:
        raise ValueError(initial_mode)
    grid = F(1, 2**40)
    while grid > alpha * (epsilon - rho) / (2 * q0):
        grid /= 2
    if rounded:
        x = [floor_grid(value, grid) for value in x]
    initial = x.copy()
    error = sub(optimum, initial)
    deficit = dot(degree, error, [F(1)] * n)
    gap = dot(degree, error, mv(matrix, error)) / 2
    assert deficit**2 <= 2 * gap / (alpha * rho)
    initial_semantic = max(abs(a - b) for a, b in zip(ppr, initial))
    if initial_mode == "cycle_certificate":
        assert gap <= alpha * theta**2 * rho / 2
        assert initial_semantic > epsilon
    residual = {seed: source[seed]}
    counts = Counter(input_cells=sum(value > 0 for value in x), degree_queries=1)
    known_degrees = {seed}

    def degree_reply(label):
        if label not in known_degrees:
            known_degrees.add(label)
            counts["degree_queries"] += 1
        return degree[label]

    for i, value in enumerate(x):
        if value <= 0:
            continue
        degree_reply(i)
        residual[i] = residual.get(i, F(0)) - q0 * value
        for j in graph.neighbors(i):
            residual[j] = residual.get(j, F(0)) + c * value / degree_reply(j)
            counts["initialization_incidences"] += 1
    initial_nonnegative = all(value >= 0 for value in residual.values())
    queue = deque(i for i, value in residual.items() if value > alpha * epsilon)
    queued = set(queue)
    while queue:
        i = queue.popleft()
        queued.remove(i)
        if residual[i] <= alpha * epsilon:
            continue
        ideal = (residual[i] - lam) / q0
        increment = floor_grid(ideal, grid) if rounded else ideal
        assert increment > 0
        assert not rounded or increment >= ideal / 2
        assert increment <= optimum[i] - x[i]
        x[i] += increment
        residual[i] -= q0 * increment
        assert lam <= residual[i] < alpha * epsilon
        counts["coordinate_updates"] += 1
        for j in graph.neighbors(i):
            residual[j] = residual.get(j, F(0)) + c * increment / degree_reply(j)
            counts["tail_incidences"] += 1
            if residual[j] > alpha * epsilon and j not in queued:
                queued.add(j)
                queue.append(j)
                counts["queue_insertions"] += 1
        assert all(0 <= value <= u for value, u in zip(x, optimum))
        if n <= 4 or counts["coordinate_updates"] % 64 == 0:
            exact_residual = sub(source, mv(matrix, x))
            assert exact_residual == [residual.get(j, F(0)) for j in range(n)]
        bound = (2 if rounded else 1) * q0 * deficit / (alpha * (epsilon - rho))
        assert counts["tail_incidences"] <= bound
    exact_residual = sub(source, mv(matrix, x))
    assert exact_residual == [residual.get(j, F(0)) for j in range(n)]
    assert max(exact_residual) <= alpha * epsilon
    if initial_nonnegative:
        assert min(exact_residual) >= 0
    final_semantic = max(abs(a - b) for a, b in zip(ppr, x))
    assert final_semantic <= epsilon
    return {
        "n": n,
        "seed": seed,
        "alpha": str(alpha),
        "eps_ppr": str(epsilon),
        "initial_mode": initial_mode,
        "rounded_tail": rounded,
        "initial_mass_deficit": float(deficit),
        "initial_rppr_gap": float(gap),
        "initial_semantic_error": float(initial_semantic),
        "final_semantic_error": float(final_semantic),
        "initial_residual_nonnegative": initial_nonnegative,
        "objective_handoff_certified": gap <= alpha * theta**2 * rho / 2,
        "counts": dict(counts),
    }


def main():
    rows = []
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= 4 or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in (F(1, 4), F(1, 64)):
                for mode in ("scale", "drop_seed"):
                    for rounded in (False, True):
                        row = run_case(graph, seed, alpha, F(1, 32), mode, rounded)
                        row["atlas_id"] = atlas_id
                        rows.append(row)
    witnesses = [
        run_case(nx.cycle_graph(16), 0, F(1, 64), F(1, 65536), "cycle_certificate", rounded)
        for rounded in (False, True)
    ]
    print(
        json.dumps(
            {
                "status": "passed",
                "arithmetic": "exact rational and exact grid floors",
                "case_count": len(rows),
                "signed_initial_residual_cases": sum(
                    not r["initial_residual_nonnegative"] for r in rows
                ),
                "scope": "Tail interface audit; initial comparison optima are external reference data, not a free prefix solver",
                "nontrivial_objective_handoff_witnesses": witnesses,
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
