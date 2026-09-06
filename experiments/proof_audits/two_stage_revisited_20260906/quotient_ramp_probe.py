"""Floating diagnostics on large canonical graphs represented by equitable classes.

This is an offline falsification search, never a local graph-access algorithm.
Integer class sizes and edge multiplicities certify a simple unweighted graph
realization. Tiny regularizers are excluded from tracking-ratio statistics
when floating-point reference or state resolution is inadequate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

from . import provenance


def blowup(sizes, links, cliques):
    neighbors = [[] for _ in sizes]
    for i, is_clique in enumerate(cliques):
        if is_clique and sizes[i] > 1:
            neighbors[i].append((i, sizes[i] - 1))
    for i, j in links:
        neighbors[i].append((j, sizes[j]))
        neighbors[j].append((i, sizes[i]))
    return sizes, neighbors


def radial(branches):
    sizes = [1]
    for branch in branches:
        sizes.append(sizes[-1] * branch)
    neighbors = []
    for i in range(len(sizes)):
        row = [(i - 1, 1)] if i else []
        if i < len(branches):
            row.append((i + 1, branches[i]))
        neighbors.append(row)
    return sizes, neighbors


def cases(random_cases):
    for depth in (8, 32, 128):
        for branch in (2, 10, 64):
            yield f"radial-{branch}-{depth}", radial([branch] * depth)
            alternating = [branch if i % 4 == 0 else 1 for i in range(depth)]
            yield f"radial-sparsebranch-{branch}-{depth}", radial(alternating)
            bottleneck = [
                branch if i < depth // 3 or i >= 2 * depth // 3 else 1 for i in range(depth)
            ]
            yield f"radial-bottleneck-{branch}-{depth}", radial(bottleneck)
    for exponent in (4, 12, 24, 40):
        for length in (8, 32, 128):
            sizes = [1] + [2**exponent] * (length - 1)
            links = [(i, i + 1) for i in range(length - 1)]
            yield f"clique-chain-{exponent}-{length}", blowup(sizes, links, [True] * length)
            sizes = [1] + [2 ** (exponent if i % 3 == 0 else 0) for i in range(1, length)]
            yield f"bottleneck-chain-{exponent}-{length}", blowup(sizes, links, [True] * length)
    for index in range(random_cases):
        rng = np.random.default_rng(20260906 + index)
        length = (8, 16, 32, 64)[index % 4]
        sizes = [1] + [2 ** int(e) for e in rng.integers(0, 33, size=length - 1)]
        links = {(int(rng.integers(i)), i) for i in range(1, length)}
        for _ in range(length // 3):
            i, j = sorted(map(int, rng.choice(length, size=2, replace=False)))
            links.add((i, j))
        cliques = [bool(value) for value in rng.integers(0, 2, size=length)]
        yield f"random-blowup-{index}", blowup(sizes, sorted(links), cliques)


def check_realization(sizes, neighbors):
    assert sizes[0] == 1 and all(size >= 1 for size in sizes)
    for i, row in enumerate(neighbors):
        assert len({j for j, _ in row}) == len(row)
        for j, count in row:
            assert 0 < count <= sizes[j] - (i == j)
            reverse = next((value for k, value in neighbors[j] if k == i), 0)
            assert sizes[i] * count == sizes[j] * reverse
    return [sum(count for _, count in row) for row in neighbors]


def run(sizes, neighbors, alpha, rho_factor):
    degree = check_realization(sizes, neighbors)
    n = len(sizes)
    volume = sum(size * d for size, d in zip(sizes, degree))
    matrix = sparse.lil_matrix((n, n))
    for i, row in enumerate(neighbors):
        matrix[i, i] = (1 + alpha) / 2
        for j, count in row:
            matrix[i, j] -= (1 - alpha) * count / (2 * degree[i])
    matrix = matrix.tocsr()
    source = np.zeros(n)
    source[0] = alpha / degree[0]
    ppr = spsolve(matrix, source)
    residual_bound = float(np.max(np.abs(matrix @ ppr - source)) / alpha)
    numerical_floor = max(64 * residual_bound, 1e5 * np.finfo(float).eps * np.max(np.abs(ppr)))
    theta = 0.5
    while theta**2 > alpha:
        theta /= 2
    chi, eta = 1 - theta, 1 - theta / 2
    x, z = np.zeros(n), np.zeros(n)
    r, rho = 1 / degree[0], 1 / (rho_factor * volume)
    steps = 0
    max_ratio, max_overshoot, max_decrease = 0.0, 0.0, 0.0
    ratio_step, decrease_step, overshoot_step = 0, 0, 0
    ratio_coordinate = None
    resolved_steps = 0
    while r > max(rho, numerical_floor):
        y = (x + theta * z) / (1 + theta)
        raw = chi * z + theta * y - (matrix @ y - source + alpha * r) / theta
        z = np.maximum(raw, 0)
        next_x = chi * x + theta * z
        steps += 1
        decrease = float(np.max(x - next_x))
        if decrease > max_decrease:
            max_decrease, decrease_step = decrease, steps
        x = next_x
        r = max(rho, eta * r)
        overshoot = float(np.max(x - ppr))
        if overshoot > max_overshoot:
            max_overshoot, overshoot_step = overshoot, steps
        if r >= numerical_floor:
            resolved_steps += 1
            ratio = float(np.max(np.abs(ppr - x)) / r)
            if ratio > max_ratio:
                max_ratio, ratio_step = ratio, steps
                ratio_coordinate = int(np.argmax(np.abs(ppr - x)))
    return {
        "class_count": n,
        "vertex_count": str(sum(sizes)),
        "original_volume": str(volume),
        "sizes": [str(size) for size in sizes],
        "neighbors": neighbors,
        "alpha": alpha,
        "theta": theta,
        "target_rho": rho,
        "last_r": r,
        "numerical_floor": float(numerical_floor),
        "reference_density_residual_bound": residual_bound,
        "steps": steps,
        "resolved_steps": resolved_steps,
        "max_semantic_error_over_r": max_ratio,
        "max_ratio_step": ratio_step,
        "max_ratio_coordinate": ratio_coordinate,
        "max_coordinate_decrease": max_decrease,
        "max_decrease_step": decrease_step,
        "max_ppr_overshoot": max_overshoot,
        "max_overshoot_step": overshoot_step,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--random-cases", type=int, default=4)
    parser.add_argument("--alpha-powers", default="4,8")
    parser.add_argument("--rho-factor", type=int, default=1024)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = last_progress = time.monotonic()
    source_record = provenance(vars(args) | {"output": str(args.output)}, args.output)
    rows = []

    def save(status):
        record = {
            "provenance": source_record,
            "status": status,
            "scope": "Floating-point falsification only; quotient access is not a solver primitive",
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
            args.output.write_text(json.dumps(record, indent=2) + "\n")
        return record

    for name, (sizes, neighbors) in cases(args.random_cases):
        for power in map(int, args.alpha_powers.split(",")):
            row = run(sizes, neighbors, 2.0 ** (-power), args.rho_factor)
            row["graph_id"] = name
            rows.append(row)
            if time.monotonic() - last_progress >= 30:
                record = save("running")
                print(
                    json.dumps(
                        {k: v for k, v in record.items() if k not in ("cases", "provenance")}
                    ),
                    flush=True,
                )
                last_progress = time.monotonic()
    record = save("finished")
    print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
