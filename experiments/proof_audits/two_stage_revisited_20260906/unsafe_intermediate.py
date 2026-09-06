"""Exact counterexample to interpreting cooling iterates as safe RPPR pushes."""

from fractions import Fraction as F
import json

import networkx as nx

from .orthant_continuation import ExactObstacle, mv
from .sparse_state import GraphOracle, SparseCooling


def main():
    graph = nx.path_graph(16)
    alpha = F(1, 4096)
    degrees = [graph.degree(i) for i in graph]
    matrix = [
        [
            (1 + alpha) / 2
            if i == j
            else -(1 - alpha) / (2 * degrees[i])
            if graph.has_edge(i, j)
            else F(0)
            for j in range(16)
        ]
        for i in range(16)
    ]
    source = [alpha] + [F(0)] * 15
    run = SparseCooling(GraphOracle(graph), 0, alpha, F(1, 1920))
    for _ in range(224):
        run.step()
        run.r = max(run.rho, run.eta * run.r)
    assert run.r == F(127, 128) ** 224
    primal = run.materialize()
    x = [primal.get(i, F(0)) for i in range(16)]
    slack = [q - b + alpha * run.r for q, b in zip(mv(matrix, x), source)]
    assert x[0] > 0
    assert F(9, 10**9) < slack[0] < F(1, 10**8)
    optimum, _ = ExactObstacle(matrix, source).at(alpha * run.r)
    assert all(a <= b for a, b in zip(x, optimum))
    print(
        json.dumps(
            {
                "status": "passed",
                "graph": "endpoint-seeded P16 with original degrees",
                "alpha": "1/4096",
                "eps_ppr": "1/1920",
                "step": 224,
                "r": "(127/128)^224",
                "normalized_positive_seed_slack_interval": ["9/10^9", "1/10^8"],
                "scope": "Not a safe RPPR subsolution; still below the current optimum",
                "arithmetic": "exact rational",
                "random_seed": None,
            }
        )
    )


if __name__ == "__main__":
    main()
