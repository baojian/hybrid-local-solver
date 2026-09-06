"""Numerical falsification probe for stronger ramp-only hypotheses.

This is a global floating-point diagnostic, not a certified local solver.
It asks whether the ramp is monotone, stays below exact PPR, and tracks PPR
within a constant multiple of its current regularizer. None is assumed by
the proved two-phase algorithm. A linear-solve residual is recorded so that
small-alpha reference inaccuracies remain visible.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import networkx as nx
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

from . import provenance


def graph_cases(random_cases, largest_n):
    for n in (8, 16, 32, 64, 128, 256, 512, 1024):
        if n > largest_n:
            continue
        families = {
            "path": nx.path_graph(n),
            "cycle": nx.cycle_graph(n),
            "lollipop": nx.lollipop_graph(max(2, n // 4), n - max(2, n // 4)),
            "barbell": nx.barbell_graph(max(2, n // 4), n - 2 * max(2, n // 4)),
            "star": nx.star_graph(n - 1),
        }
        for name, graph in families.items():
            for seed in sorted({0, n // 2, n - 1}):
                yield f"{name}-{n}", graph, seed
    for index in range(random_cases):
        n = min(largest_n, (16, 32, 64, 128, 256, 512)[index % 6])
        random_seed = 20260906 + index
        if index % 3 == 0:
            graph = nx.barabasi_albert_graph(n, 1 + (index // 3) % 4, seed=random_seed)
            family = "ba"
        elif index % 3 == 1:
            graph = nx.watts_strogatz_graph(n, 4, 0.05 + (index % 5) / 10, seed=random_seed)
            if not nx.is_connected(graph):
                continue
            family = "ws"
        else:
            rng = np.random.default_rng(random_seed)
            graph = nx.from_prufer_sequence(rng.integers(0, n, size=n - 2))
            family = "tree"
        for seed in sorted({0, n - 1}):
            yield f"{family}-{n}-seed{random_seed}", graph, seed


def run_case(graph, seed, alpha, rho_factor):
    n = len(graph)
    adjacency = nx.to_scipy_sparse_array(graph, nodelist=range(n), dtype=float, format="csr")
    degree = np.array([graph.degree(i) for i in range(n)], dtype=float)
    matrix = sparse.diags(np.full(n, (1 + alpha) / 2), format="csr")
    matrix -= (1 - alpha) / 2 * sparse.diags(1 / degree) @ adjacency
    source = np.zeros(n)
    source[seed] = alpha / degree[seed]
    ppr = spsolve(matrix, source)
    residual_error_bound = float(np.max(np.abs(matrix @ ppr - source)) / alpha)
    theta = 0.5
    while theta * theta > alpha:
        theta *= 0.5
    chi, eta = 1 - theta, 1 - theta / 2
    r = 1 / degree[seed]
    rho = 1 / (rho_factor * degree.sum())
    x = np.zeros(n)
    z = np.zeros(n)
    largest_error_ratio = 0.0
    largest_overshoot = 0.0
    largest_decrease = 0.0
    worst_ratio_step = 0
    worst_decrease_step = 0
    maximum_step_volume_ratio = 0.0
    steps = 0
    while r > rho:
        y = (x + theta * z) / (1 + theta)
        raw = chi * z + theta * y - (matrix @ y - source + alpha * r) / theta
        z = np.maximum(raw, 0)
        next_x = chi * x + theta * z
        decrease = float(np.max(x - next_x))
        if decrease > largest_decrease:
            largest_decrease, worst_decrease_step = decrease, steps + 1
        maximum_step_volume_ratio = max(maximum_step_volume_ratio, float(degree[z > 0].sum() * r))
        x = next_x
        r = max(rho, eta * r)
        steps += 1
        error_ratio = float(np.max(np.abs(ppr - x)) / r)
        if error_ratio > largest_error_ratio:
            largest_error_ratio, worst_ratio_step = error_ratio, steps
        largest_overshoot = max(largest_overshoot, float(np.max(x - ppr)))
    return {
        "n": n,
        "seed": seed,
        "alpha": alpha,
        "rho": rho,
        "rho_factor": rho_factor,
        "steps": steps,
        "max_semantic_error_over_r": largest_error_ratio,
        "max_error_ratio_step": worst_ratio_step,
        "max_coordinate_decrease": largest_decrease,
        "max_decrease_step": worst_decrease_step,
        "max_ppr_overshoot": largest_overshoot,
        "reference_semantic_residual_bound": residual_error_bound,
        "max_single_step_kinetic_volume_times_r": maximum_step_volume_ratio,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--largest-n", type=int, default=32)
    parser.add_argument("--random-cases", type=int, default=2)
    parser.add_argument("--alpha-powers", default="4,8")
    parser.add_argument("--rho-factor", type=int, default=128)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    last_progress = started
    source_record = provenance(vars(args) | {"output": str(args.output)}, args.output)
    rows = []

    def record(status):
        result = {
            "provenance": source_record,
            "status": status,
            "scope": "Floating-point diagnostics for open stronger hypotheses, not theorem certification",
            "case_count": len(rows),
            "elapsed_seconds": time.monotonic() - started,
            "max_semantic_error_over_r": max(
                (r["max_semantic_error_over_r"] for r in rows), default=0
            ),
            "max_coordinate_decrease": max((r["max_coordinate_decrease"] for r in rows), default=0),
            "cases": rows,
        }
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2) + "\n")
        return result

    for name, graph, seed in graph_cases(args.random_cases, args.largest_n):
        for power in map(int, args.alpha_powers.split(",")):
            row = run_case(graph, seed, 2.0 ** (-power), args.rho_factor)
            row["graph_id"] = name
            rows.append(row)
            now = time.monotonic()
            if now - last_progress >= 30:
                last_progress = now
                snapshot = record("in_progress")
                print(
                    json.dumps(
                        {k: v for k, v in snapshot.items() if k not in ("provenance", "cases")}
                    ),
                    flush=True,
                )
    final = record("finished")
    print(json.dumps({k: v for k, v in final.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
