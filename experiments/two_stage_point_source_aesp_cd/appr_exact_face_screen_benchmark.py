#!/usr/bin/env python3
"""Coarse APPR proposals followed by structural exact-face verification."""

from __future__ import annotations

import argparse
import csv
import heapq
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

try:
    from .face_verifier import exact_face_verifier
    from .leakage_screen_benchmark import direct_priority_ppr
    from .portfolio_benchmark import (
        binary_tree,
        broom_graph,
        cycle_graph,
        grid_graph,
        normalized_matrix,
        path_graph,
        star_graph,
    )
    from .structural_solvers import (
        reused_structural_backsolve_work,
        tree_or_unicyclic_principal_solve,
    )
except ImportError:  # Direct script execution.
    from face_verifier import exact_face_verifier
    from leakage_screen_benchmark import direct_priority_ppr
    from portfolio_benchmark import (
        binary_tree,
        broom_graph,
        cycle_graph,
        grid_graph,
        normalized_matrix,
        path_graph,
        star_graph,
    )
    from structural_solvers import (
        reused_structural_backsolve_work,
        tree_or_unicyclic_principal_solve,
    )


@dataclass(frozen=True)
class ExactFaceScreenRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    rho: float
    certified: bool
    checkpoint_factor: float
    candidate_kind: str
    support_nodes: int
    support_volume: int
    appr_work: int
    raced_appr_work: int
    verifier_work: int
    raw_sequential_work: int
    stage2_work: int
    strict_two_stage_work: int
    strict_raced_total: int
    strict_ratio: float
    reused_stage2_work: int
    reused_two_stage_work: int
    reused_raced_total: int
    reused_ratio: float
    semantic_error: float
    total_work: int
    direct_work: int
    ratio: float
    attempts: int
    minimum_active: float
    maximum_boundary_key: float


class PriorityAPPRStream:
    """Priority APPR state that can be resumed at decreasing thresholds."""

    def __init__(self, adjacency: list[list[int]], alpha: float, seed: int):
        self.adjacency = adjacency
        self.alpha = alpha
        self.seed = seed
        self.degree = np.asarray([len(row) for row in adjacency], dtype=float)
        self.diagonal_scale = (1.0 + alpha) / 2.0
        self.coupling = (1.0 - alpha) / 2.0
        self.vector = np.zeros(len(adjacency))
        self.residual = np.zeros(len(adjacency))
        self.residual[seed] = alpha
        self.versions = np.zeros(len(adjacency), dtype=np.int64)
        self.heap: list[tuple[float, int, int]] = [(-alpha / self.degree[seed], seed, 0)]
        self.work = 0

    def advance(self, threshold_parameter: float) -> np.ndarray:
        """Run until every normalized residual is below alpha*parameter."""
        target = self.alpha * threshold_parameter
        while self.heap:
            negative_key, vertex, version = heapq.heappop(self.heap)
            if version != self.versions[vertex] or self.residual[vertex] <= 0.0:
                continue
            if -negative_key <= target:
                heapq.heappush(self.heap, (negative_key, vertex, version))
                break
            value = self.residual[vertex]
            step = value / (self.diagonal_scale * self.degree[vertex])
            self.vector[vertex] += step
            self.residual[vertex] = 0.0
            self.versions[vertex] += 1
            self.work += int(self.degree[vertex])
            for neighbor in self.adjacency[vertex]:
                self.residual[neighbor] += self.coupling * step
                self.versions[neighbor] += 1
                heapq.heappush(
                    self.heap,
                    (
                        -self.residual[neighbor] / self.degree[neighbor],
                        neighbor,
                        int(self.versions[neighbor]),
                    ),
                )
        return self.vector > 0.0


def one_hop(adjacency: list[list[int]], support: np.ndarray) -> np.ndarray:
    expanded = support.copy()
    for vertex in np.flatnonzero(support):
        for neighbor in adjacency[int(vertex)]:
            expanded[neighbor] = True
    return expanded


def ordinary_ppr_stage2(
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int,
    candidate: np.ndarray,
) -> tuple[int, float]:
    """Run and audit a literal ordinary-PPR second stage on a certified face."""
    degree, matrix = normalized_matrix(adjacency, alpha)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / np.sqrt(degree[seed])
    if not candidate.any():
        output = np.zeros(len(adjacency))
        work = 0
    else:
        output, arithmetic, _kind = tree_or_unicyclic_principal_solve(
            adjacency, candidate, degree, alpha, source, seed
        )
        work = int(degree[candidate].sum()) + arithmetic
    reference = np.asarray(spsolve(matrix, source))
    error = float(np.max(np.abs((output - reference) / np.sqrt(degree))))
    if error > epsilon * (1.0 + 1e-7) + 2e-10:
        raise AssertionError((alpha, epsilon, error))
    return work, error


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> ExactFaceScreenRow:
    # The structural face solve is exact, so spend the full semantic budget
    # on RPPR screening rather than reserving an unused terminal half.
    rho = epsilon
    stream = PriorityAPPRStream(adjacency, alpha, seed)
    _direct, direct_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    verifier_work = 0
    attempts = 0
    tried: set[bytes] = set()
    last_minimum = float("nan")
    last_boundary = float("nan")
    for factor in (16.0, 8.0, 4.0, 2.0):
        support = stream.advance(factor * rho)
        for kind, candidate in (
            ("appr", support),
            ("appr-plus-boundary", one_hop(adjacency, support)),
        ):
            fingerprint = np.packbits(candidate).tobytes()
            if fingerprint in tried:
                continue
            tried.add(fingerprint)
            attempts += 1
            certified, charged, volume, minimum, maximum = exact_face_verifier(
                adjacency, alpha, rho, seed, candidate
            )
            verifier_work += charged
            last_minimum = minimum
            last_boundary = maximum
            if certified:
                # Verification and the continuing direct lane receive equal
                # quanta.  If direct APPR would finish before the accumulated
                # verifier work, the numerical lane wins the race instead.
                if verifier_work > direct_work:
                    break
                raced_appr_work = min(direct_work, max(stream.work, verifier_work))
                total = raced_appr_work + verifier_work
                stage2_work, semantic_error = ordinary_ppr_stage2(
                    adjacency, alpha, epsilon, seed, candidate
                )
                strict_work = stream.work + verifier_work + stage2_work
                strict_raced_total = 2 * min(strict_work, direct_work)
                reused_stage2 = reused_structural_backsolve_work(adjacency, candidate)
                reused_work = stream.work + verifier_work + reused_stage2
                reused_raced_total = 2 * min(reused_work, direct_work)
                return ExactFaceScreenRow(
                    family,
                    len(adjacency),
                    alpha,
                    epsilon,
                    rho,
                    True,
                    factor,
                    kind,
                    int(candidate.sum()),
                    volume,
                    stream.work,
                    raced_appr_work,
                    verifier_work,
                    stream.work + verifier_work,
                    stage2_work,
                    strict_work,
                    strict_raced_total,
                    strict_raced_total / direct_work if direct_work else 0.0,
                    reused_stage2,
                    reused_work,
                    reused_raced_total,
                    reused_raced_total / direct_work if direct_work else 0.0,
                    semantic_error,
                    total,
                    direct_work,
                    total / direct_work if direct_work else 0.0,
                    attempts,
                    minimum,
                    maximum,
                )
    # The direct lane wins no later than its normal endpoint, and the
    # verifier can consume at most the same amount of raced work.
    charged_verifier = min(verifier_work, direct_work)
    total = direct_work + charged_verifier
    return ExactFaceScreenRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        rho,
        False,
        0.0,
        "direct-fallback",
        0,
        0,
        stream.work,
        direct_work,
        charged_verifier,
        stream.work + verifier_work,
        0,
        stream.work + verifier_work,
        2 * direct_work,
        2.0 if direct_work else 0.0,
        0,
        stream.work + verifier_work,
        2 * direct_work,
        2.0 if direct_work else 0.0,
        float("nan"),
        total,
        direct_work,
        total / direct_work if direct_work else 0.0,
        attempts,
        last_minimum,
        last_boundary,
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
    nontrivial = [row for row in certified if row.direct_work]
    wins = [row for row in nontrivial if row.ratio < 1.0]
    strict_standalone = [row for row in nontrivial if row.strict_two_stage_work < row.direct_work]
    strict_fair = [row for row in strict_standalone if row.strict_ratio < 1.0]
    reused_standalone = [row for row in nontrivial if row.reused_two_stage_work < row.direct_work]
    reused_fair = [row for row in reused_standalone if row.reused_ratio < 1.0]
    print(
        f"rows={len(rows)} certified={len(certified)} early-wins={len(wins)} "
        f"literal-standalone/fair={len(strict_standalone)}/{len(strict_fair)} "
        f"reused-standalone/fair={len(reused_standalone)}/{len(reused_fair)} "
        f"median-certified="
        f"{np.median([row.ratio for row in nontrivial]):.6f}"
    )
    for row in sorted(certified, key=lambda item: item.ratio)[:30]:
        print(
            row.family,
            row.alpha,
            row.epsilon,
            row.checkpoint_factor,
            row.candidate_kind,
            f"ratio={row.ratio:.6f}",
            f"attempts={row.attempts}",
        )


if __name__ == "__main__":
    main()
