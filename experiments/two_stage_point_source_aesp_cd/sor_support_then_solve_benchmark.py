#!/usr/bin/env python3
"""Positive-residual SOR support discovery with geometric face checks."""

from __future__ import annotations

import argparse
import csv
import heapq
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from appr_exact_face_screen_benchmark import (
    exact_face_verifier,
    ordinary_ppr_stage2,
)
from leakage_screen_benchmark import direct_priority_ppr
from portfolio_benchmark import (
    binary_tree,
    broom_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    star_graph,
)
from structural_solvers import reused_structural_backsolve_work


@dataclass(frozen=True)
class SORSupportRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    rho: float
    certified: bool
    support_nodes: int
    support_volume: int
    sor_work: int
    verifier_work: int
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
    checks: int
    pushes: int


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> SORSupportRow:
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    # Exact fixed-face completion needs no terminal error allocation.
    rho = epsilon
    cap = 2.0 / epsilon
    diagonal = (1.0 + alpha) * degree / 2.0
    coupling = (1.0 - alpha) / 2.0
    residual = -alpha * rho * degree
    residual[seed] += alpha
    vector = np.zeros(len(adjacency))
    versions = np.zeros(len(adjacency), dtype=np.int64)
    heap: list[tuple[float, int, int]] = [(-residual[seed] / degree[seed], seed, 0)]
    candidate = residual > 0.0
    candidate_volume = int(degree[candidate].sum())
    checked_fingerprints: set[bytes] = set()
    next_check_work = max(1, int(degree[seed]))
    sor_work = 0
    verifier_work = 0
    checks = 0
    pushes = 0
    certified = False
    support_volume = 0

    def try_verify() -> bool:
        nonlocal verifier_work, checks, support_volume
        fingerprint = np.packbits(candidate).tobytes()
        if fingerprint in checked_fingerprints:
            return False
        checked_fingerprints.add(fingerprint)
        checks += 1
        passes, charged, volume, _minimum, _maximum = exact_face_verifier(
            adjacency, alpha, rho, seed, candidate
        )
        verifier_work += charged
        if passes:
            support_volume = volume
        return passes

    while heap and candidate_volume <= cap:
        _negative_key, vertex, version = heapq.heappop(heap)
        if version != versions[vertex] or residual[vertex] <= 1e-14:
            continue
        value = residual[vertex]
        step = value / diagonal[vertex]
        vector[vertex] += step
        residual[vertex] = 0.0
        versions[vertex] += 1
        sor_work += int(degree[vertex])
        pushes += 1
        for neighbor in adjacency[vertex]:
            residual[neighbor] += coupling * step
            versions[neighbor] += 1
            if residual[neighbor] > 1e-14:
                heapq.heappush(
                    heap,
                    (
                        -residual[neighbor] / degree[neighbor],
                        neighbor,
                        int(versions[neighbor]),
                    ),
                )
                if not candidate[neighbor]:
                    candidate[neighbor] = True
                    candidate_volume += int(degree[neighbor])
        if sor_work >= next_check_work:
            certified = try_verify()
            while next_check_work <= sor_work:
                next_check_work *= 2
            if certified:
                break
    if not certified and candidate_volume <= cap:
        certified = try_verify()

    active_work = sor_work + verifier_work
    _direct, direct_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    if certified:
        stage2_work, semantic_error = ordinary_ppr_stage2(
            adjacency, alpha, epsilon, seed, candidate
        )
        reused_stage2 = reused_structural_backsolve_work(adjacency, candidate)
    else:
        stage2_work, semantic_error = 0, float("nan")
        reused_stage2 = 0
    strict_work = active_work + stage2_work
    strict_raced_total = 2 * min(strict_work, direct_work)
    reused_work = active_work + reused_stage2
    reused_raced_total = 2 * min(reused_work, direct_work)
    exact_lane_wins = certified and active_work < direct_work
    raced_total = 2 * active_work if exact_lane_wins else 2 * direct_work
    return SORSupportRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        rho,
        certified,
        int(candidate.sum()) if certified else 0,
        support_volume if certified else 0,
        sor_work,
        verifier_work,
        active_work,
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
        checks,
        pushes,
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
    certified = [row for row in rows if row.certified]
    lane_wins = [
        row for row in certified if row.direct_work and row.active_lane_work < row.direct_work
    ]
    portfolio_wins = [row for row in lane_wins if row.direct_work and row.ratio < 1.0]
    strict_standalone = [
        row for row in certified if row.direct_work and row.strict_two_stage_work < row.direct_work
    ]
    strict_fair = [row for row in strict_standalone if row.strict_ratio < 1.0]
    reused_standalone = [
        row for row in certified if row.direct_work and row.reused_two_stage_work < row.direct_work
    ]
    reused_fair = [row for row in reused_standalone if row.reused_ratio < 1.0]
    print(
        f"rows={len(rows)} certified={len(certified)} "
        f"early-standalone/fair={len(lane_wins)}/{len(portfolio_wins)} "
        f"literal-standalone/fair={len(strict_standalone)}/{len(strict_fair)} "
        f"reused-standalone/fair={len(reused_standalone)}/{len(reused_fair)}"
    )
    for row in sorted(lane_wins, key=lambda item: item.active_lane_work / max(1, item.direct_work))[
        :35
    ]:
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"lane/direct={row.active_lane_work / row.direct_work:.6f}",
            f"race={row.ratio:.6f}",
            f"checks={row.checks}",
            f"pushes={row.pushes}",
        )


if __name__ == "__main__":
    main()
