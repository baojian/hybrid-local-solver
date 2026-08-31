#!/usr/bin/env python3
"""Exact positive-boundary batches with a direct-APPR fair fallback."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from leakage_screen_benchmark import direct_priority_ppr
from appr_exact_face_screen_benchmark import ordinary_ppr_stage2
from portfolio_benchmark import (
    binary_tree,
    broom_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    star_graph,
)
from structural_solvers import (
    principal_residual,
    reused_structural_backsolve_work,
    tree_or_unicyclic_principal_solve,
)


@dataclass(frozen=True)
class BatchExactRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    rho: float
    exact_lane_wins: bool
    rounds: int
    support_nodes: int
    support_volume: int
    active_lane_work: int
    stage2_work: int
    strict_two_stage_work: int
    strict_raced_total: int
    strict_ratio: float
    reused_stage2_work: int
    reused_two_stage_work: int
    reused_raced_total: int
    reused_ratio: float
    semantic_error: float
    direct_work: int
    raced_total_work: int
    ratio: float
    batch_word: str


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> BatchExactRow:
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    # Exact fixed-face completion needs no terminal error allocation.
    rho = epsilon
    cap = 2.0 / epsilon
    source = -alpha * rho * np.sqrt(degree)
    source[seed] += alpha / np.sqrt(degree[seed])
    coupling = (1.0 - alpha) / 2.0
    if source[seed] <= 0.0:
        _direct, direct_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
        exact_wins = direct_work > 0
        empty = np.zeros(len(adjacency), dtype=bool)
        stage2_work, semantic_error = ordinary_ppr_stage2(adjacency, alpha, epsilon, seed, empty)
        return BatchExactRow(
            family,
            len(adjacency),
            alpha,
            epsilon,
            rho,
            exact_wins,
            0,
            0,
            0,
            0,
            stage2_work,
            stage2_work,
            2 * min(stage2_work, direct_work),
            (2 * min(stage2_work, direct_work) / direct_work) if direct_work else 0.0,
            0,
            0,
            0,
            0.0,
            semantic_error,
            direct_work,
            0,
            0.0,
            "",
        )
    candidate = np.zeros(len(adjacency), dtype=bool)
    candidate[seed] = True
    work = 0
    rounds = 0
    batches: list[int] = []
    exact = False
    while float(degree[candidate].sum()) <= cap:
        try:
            point, arithmetic, _kind = tree_or_unicyclic_principal_solve(
                adjacency, candidate, degree, alpha, source, seed
            )
        except ValueError:
            break
        volume = int(degree[candidate].sum())
        work += arithmetic + volume
        rounds += 1
        active = np.flatnonzero(candidate)
        retained_residual = principal_residual(
            adjacency,
            candidate,
            degree,
            alpha,
            source,
            point,
        )
        error_bar = float(np.linalg.norm(retained_residual[active]) / alpha)
        rounding = 2e-12 * max(
            1.0,
            float(np.max(np.abs(source))),
            float(np.max(np.abs(point[active]))),
        )
        if np.min(point[active] - error_bar - rounding) <= 0.0:
            break
        boundary = {
            neighbor
            for vertex in active
            for neighbor in adjacency[int(vertex)]
            if not candidate[neighbor]
        }
        positive: list[int] = []
        uncertain = False
        for vertex in boundary:
            key = source[vertex]
            for neighbor in adjacency[vertex]:
                if candidate[neighbor]:
                    key += coupling * point[neighbor] / np.sqrt(degree[vertex] * degree[neighbor])
            row_norm = coupling * np.sqrt(
                sum(
                    1.0 / (degree[vertex] * degree[neighbor])
                    for neighbor in adjacency[vertex]
                    if candidate[neighbor]
                )
            )
            lower_key = float(key) - row_norm * error_bar - rounding
            upper_key = float(key) + row_norm * error_bar + rounding
            if lower_key > 0.0:
                positive.append(vertex)
            elif upper_key > 0.0:
                uncertain = True
        if uncertain:
            break
        if not positive:
            exact = True
            break
        batches.append(len(positive))
        candidate[positive] = True

    _direct, direct_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    exact_wins = exact and work < direct_work
    if exact:
        stage2_work, semantic_error = ordinary_ppr_stage2(
            adjacency, alpha, epsilon, seed, candidate
        )
        reused_stage2 = reused_structural_backsolve_work(adjacency, candidate)
    else:
        stage2_work, semantic_error = 0, float("nan")
        reused_stage2 = 0
    strict_work = work + stage2_work
    strict_raced_total = 2 * min(strict_work, direct_work)
    reused_work = work + reused_stage2
    reused_raced_total = 2 * min(reused_work, direct_work)
    raced_total = 2 * min(work, direct_work)
    if not exact_wins:
        raced_total = 2 * direct_work
    support_volume = int(degree[candidate].sum()) if exact else 0
    return BatchExactRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        rho,
        exact_wins,
        rounds,
        int(candidate.sum()) if exact else 0,
        support_volume,
        work,
        stage2_work,
        strict_work,
        strict_raced_total,
        strict_raced_total / direct_work if direct_work else 0.0,
        reused_stage2,
        reused_work,
        reused_raced_total,
        reused_raced_total / direct_work if direct_work else 0.0,
        semantic_error,
        direct_work,
        raced_total,
        raced_total / direct_work if direct_work else 0.0,
        ",".join(str(size) for size in batches),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    graphs = [
        ("path-1024", path_graph(1024)),
        ("cycle-1024", cycle_graph(1024)),
        ("star-1024", star_graph(1023)),
        ("binary-depth-10", binary_tree(10)),
        ("broom-512-511", broom_graph(512, 511)),
        ("grid-32x32", grid_graph(32, 32)),
    ]
    rows = [
        run_case(family, graph, alpha, epsilon)
        for family, graph in graphs
        for alpha in (0.01, 0.04, 0.16)
        for epsilon in (0.0001, 0.0005, 0.001, 0.002, 0.005)
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=asdict(rows[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    standalone_wins = [row for row in rows if row.exact_lane_wins]
    fair_wins = [row for row in rows if row.direct_work and row.ratio < 1.0]
    exact = [row for row in rows if row.support_nodes or row.rounds == 0]
    strict_standalone = [
        row for row in exact if row.direct_work and row.strict_two_stage_work < row.direct_work
    ]
    strict_fair = [row for row in strict_standalone if row.strict_ratio < 1.0]
    reused_standalone = [
        row for row in exact if row.direct_work and row.reused_two_stage_work < row.direct_work
    ]
    reused_fair = [row for row in reused_standalone if row.reused_ratio < 1.0]
    print(
        f"rows={len(rows)} exact={len(exact)} "
        f"early-standalone/fair={len(standalone_wins)}/{len(fair_wins)} "
        f"literal-standalone/fair={len(strict_standalone)}/{len(strict_fair)} "
        f"reused-standalone/fair={len(reused_standalone)}/{len(reused_fair)}"
    )
    for row in sorted(standalone_wins, key=lambda item: item.active_lane_work / item.direct_work):
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"lane/direct={row.active_lane_work / row.direct_work:.6f}",
            f"race={row.ratio:.6f}",
            f"rounds={row.rounds}",
            f"batches={row.batch_word}",
        )


if __name__ == "__main__":
    main()
