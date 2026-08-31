#!/usr/bin/env python3
"""Dynamic rooted-tree threshold messages followed by one fixed face solve."""

from __future__ import annotations

import argparse
import csv
import heapq
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from appr_exact_face_screen_benchmark import exact_face_verifier
from leakage_screen_benchmark import direct_priority_ppr
from portfolio_benchmark import (
    binary_tree,
    broom_graph,
    normalized_matrix,
    path_graph,
    star_graph,
)
from structural_solvers import tree_or_unicyclic_principal_solve


@dataclass(frozen=True)
class TreeThresholdRow:
    family: str
    vertices: int
    alpha: float
    epsilon: float
    rho: float
    certified: bool
    support_nodes: int
    support_volume: int
    admissions: int
    adjacency_work: int
    route_work: int
    verifier_work: int
    total_work: int
    stage2_work: int
    literal_two_stage_work: int
    direct_work: int
    ratio: float
    fair_ratio: float
    literal_ratio: float
    literal_fair_ratio: float
    semantic_error: float


class TreeThresholdMessages:
    """Incremental exact-formula messages on one rooted unweighted tree."""

    def __init__(
        self,
        adjacency: list[list[int]],
        alpha: float,
        rho: float,
        root: int,
    ):
        self.adjacency = adjacency
        self.alpha = alpha
        self.rho = rho
        self.root = root
        self.degree = np.full(len(adjacency), np.nan)
        self.parent = np.full(len(adjacency), -2, dtype=np.int64)
        self.parent[root] = -1
        self.children: list[list[int]] = [[] for _ in adjacency]

        self.diagonal_scale = (1.0 + alpha) / 2.0
        self.beta = (1.0 - alpha) / 2.0
        self.load = np.full(len(adjacency), np.nan)
        self.active = np.zeros(len(adjacency), dtype=bool)
        self.a = np.zeros(len(adjacency))
        self.b = np.zeros(len(adjacency))
        self.s = np.zeros(len(adjacency))
        self.r = np.zeros(len(adjacency))
        self.tau = np.full(len(adjacency), np.inf)
        self.label = np.full(len(adjacency), -1, dtype=np.int64)
        self.child_versions = np.zeros(len(adjacency), dtype=np.int64)
        self.heaps: list[list[tuple[float, int, int, int]]] = [[] for _ in adjacency]
        self.adjacency_work = 0
        self.route_work = 0
        self.admissions = 0
        self._ensure_metadata(root)
        if self.load[root] > 0.0:
            self._initialize_active(root)

    def _ensure_metadata(self, vertex: int) -> None:
        """Read a named vertex's degree/load without exposing its row."""
        if not np.isnan(self.degree[vertex]):
            return
        degree = len(self.adjacency[vertex])
        if degree == 0:
            raise ValueError("the threshold-message graph contains an isolate")
        self.degree[vertex] = degree
        self.load[vertex] = -self.alpha * self.rho * degree
        if vertex == self.root:
            self.load[vertex] += self.alpha

    def _push_child_record(self, parent: int, child: int) -> None:
        version = int(self.child_versions[child])
        if self.active[child]:
            if self.label[child] >= 0:
                heapq.heappush(
                    self.heaps[parent],
                    (
                        float(self.tau[child]),
                        int(self.label[child]),
                        child,
                        version,
                    ),
                )
        else:
            heapq.heappush(
                self.heaps[parent],
                (
                    float(-self.load[child] / self.beta),
                    child,
                    child,
                    version,
                ),
            )

    def _refresh_candidate(self, vertex: int) -> None:
        heap = self.heaps[vertex]
        while heap:
            threshold, label, child, version = heap[0]
            if version != self.child_versions[child]:
                heapq.heappop(heap)
                continue
            if self.active[child] and self.label[child] < 0:
                heapq.heappop(heap)
                continue
            if self.active[child] and (
                label != self.label[child] or abs(threshold - self.tau[child]) > 1e-12
            ):
                heapq.heappop(heap)
                continue
            self.tau[vertex] = threshold
            self.label[vertex] = label
            return
        self.tau[vertex] = np.inf
        self.label[vertex] = -1

    def _initialize_active(self, vertex: int) -> None:
        self._ensure_metadata(vertex)
        self.active[vertex] = True
        self.a[vertex] = self.diagonal_scale * self.degree[vertex]
        self.b[vertex] = self.load[vertex]
        self.heaps[vertex] = []
        children = []
        for neighbor in self.adjacency[vertex]:
            if neighbor == self.parent[vertex]:
                continue
            self._ensure_metadata(neighbor)
            if self.parent[neighbor] == -2:
                self.parent[neighbor] = vertex
            elif self.parent[neighbor] != vertex:
                raise ValueError("the exposed threshold-message graph has a cycle")
            children.append(neighbor)
        self.children[vertex] = children
        self.heaps[vertex] = [
            (
                float(-self.load[child] / self.beta),
                child,
                child,
                int(self.child_versions[child]),
            )
            for child in children
        ]
        heapq.heapify(self.heaps[vertex])
        self._refresh_candidate(vertex)
        if vertex != self.root:
            self.s[vertex] = self.beta * self.beta / self.a[vertex]
            self.r[vertex] = self.beta * self.b[vertex] / self.a[vertex]
            if self.label[vertex] >= 0:
                self.tau[vertex] = (self.a[vertex] * self.tau[vertex] - self.b[vertex]) / self.beta
        self.adjacency_work += int(self.degree[vertex])

    def _update_ancestor(self, vertex: int, old_s: float, old_r: float) -> None:
        """Replace one changed child response, then propagate to the root."""
        current = vertex
        child_old_s = old_s
        child_old_r = old_r
        while current != self.root:
            parent = int(self.parent[current])
            parent_old_s = self.s[parent]
            parent_old_r = self.r[parent]
            self.a[parent] += child_old_s - self.s[current]
            self.b[parent] += self.r[current] - child_old_r
            if self.a[parent] <= 0.0:
                raise AssertionError("tree response lost a positive Schur pivot")
            self.child_versions[current] += 1
            self._push_child_record(parent, current)
            self._refresh_candidate(parent)
            if parent != self.root:
                self.s[parent] = self.beta * self.beta / self.a[parent]
                self.r[parent] = self.beta * self.b[parent] / self.a[parent]
                if self.label[parent] >= 0:
                    self.tau[parent] = (
                        self.a[parent] * self.tau[parent] - self.b[parent]
                    ) / self.beta
            self.route_work += max(1, math.ceil(math.log2(2 + len(self.children[parent]))))
            current = parent
            child_old_s = parent_old_s
            child_old_r = parent_old_r

    def step(self) -> bool:
        """Admit one exact positive frontier label, or report global KKT."""
        if not self.active[self.root]:
            return False
        root_value = self.b[self.root] / self.a[self.root]
        label = int(self.label[self.root])
        if label < 0 or not root_value > self.tau[self.root] + 1e-13:
            return False
        parent = int(self.parent[label])
        old_s = 0.0
        old_r = 0.0
        self._initialize_active(label)
        self._update_ancestor(label, old_s, old_r)
        if parent < 0:
            raise AssertionError("the root cannot be readmitted")
        self.admissions += 1
        return True

    def run(self) -> np.ndarray:
        while self.step():
            pass
        return self.active.copy()


def run_case(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    epsilon: float,
    seed: int = 0,
) -> TreeThresholdRow:
    # The structural Stage II solve is exact, so it needs no terminal error
    # budget.  Spend the full semantic allowance on the RPPR screen.
    rho = epsilon
    messages = TreeThresholdMessages(adjacency, alpha, rho, seed)
    support = messages.run()
    if support.any():
        certified, verifier_work, volume, _minimum, _maximum = exact_face_verifier(
            adjacency, alpha, rho, seed, support
        )
    else:
        # The off-root loads are negative.  If the root load is nonpositive,
        # zero itself satisfies every obstacle KKT inequality.
        certified = messages.load[seed] <= 0.0
        verifier_work = 0
        volume = 0
    total = messages.adjacency_work + messages.route_work + verifier_work

    degree, matrix = normalized_matrix(adjacency, alpha)
    ppr_source = np.zeros(len(adjacency))
    ppr_source[seed] = alpha / np.sqrt(degree[seed])
    stage2_point = np.zeros(len(adjacency))
    if support.any():
        stage2_point, arithmetic, _kind = tree_or_unicyclic_principal_solve(
            adjacency, support, degree, alpha, ppr_source, seed
        )
        stage2_work = volume + arithmetic
    else:
        stage2_work = 0
    # The message gate itself certifies the face.  A literal set-only lane
    # therefore replaces (rather than duplicates) the independent RPPR audit
    # solve by this ordinary-PPR solve.
    literal_two_stage_work = messages.adjacency_work + messages.route_work + stage2_work
    full_ppr = spsolve(matrix, ppr_source)
    semantic_error = float(np.max(np.abs(stage2_point - full_ppr) / np.sqrt(degree)))
    if semantic_error > epsilon + 2e-9:
        raise AssertionError((family, alpha, epsilon, semantic_error))

    _direct, direct_work = direct_priority_ppr(adjacency, alpha, epsilon, seed)
    ratio = total / direct_work if direct_work else (0.0 if total == 0 else float("inf"))
    fair_ratio = (
        2 * min(total, direct_work) / direct_work if direct_work else (0.0 if total == 0 else 1.0)
    )
    literal_ratio = (
        literal_two_stage_work / direct_work
        if direct_work
        else (0.0 if literal_two_stage_work == 0 else float("inf"))
    )
    literal_fair_ratio = (
        2 * min(literal_two_stage_work, direct_work) / direct_work
        if direct_work
        else (0.0 if literal_two_stage_work == 0 else 1.0)
    )
    return TreeThresholdRow(
        family,
        len(adjacency),
        alpha,
        epsilon,
        rho,
        certified,
        int(support.sum()),
        volume,
        messages.admissions,
        messages.adjacency_work,
        messages.route_work,
        verifier_work,
        total,
        stage2_work,
        literal_two_stage_work,
        direct_work,
        ratio,
        fair_ratio,
        literal_ratio,
        literal_fair_ratio,
        semantic_error,
    )


def audit_random_trees() -> int:
    """Independent deterministic KKT stress test on 1,890 small trees."""
    generator = np.random.default_rng(20260830)
    checked = 0
    for size in range(2, 65):
        for _repeat in range(10):
            adjacency: list[list[int]] = [[] for _ in range(size)]
            for vertex in range(1, size):
                parent = int(generator.integers(vertex))
                adjacency[vertex].append(parent)
                adjacency[parent].append(vertex)
            seed = int(generator.integers(size))
            for alpha in (0.01, 0.07, 0.3):
                rho = float(10 ** generator.uniform(-5.0, -1.5))
                messages = TreeThresholdMessages(adjacency, alpha, rho, seed)
                support = messages.run()
                if support.any():
                    certified, *_rest = exact_face_verifier(adjacency, alpha, rho, seed, support)
                else:
                    certified = messages.load[seed] <= 0.0
                if not certified:
                    raise AssertionError((size, alpha, rho, seed, int(support.sum())))
                checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-audit", action="store_true")
    args = parser.parse_args()
    graphs = [
        ("path-1024", path_graph(1024)),
        ("star-1024", star_graph(1023)),
        ("binary-depth-10", binary_tree(10)),
        ("broom-512-511", broom_graph(512, 511)),
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
    wins = [row for row in rows if row.direct_work and row.ratio < 1.0]
    fair_wins = [row for row in rows if row.direct_work and row.fair_ratio < 1.0]
    literal_wins = [row for row in rows if row.direct_work and row.literal_ratio < 1.0]
    literal_fair_wins = [row for row in rows if row.direct_work and row.literal_fair_ratio < 1.0]
    print(
        f"rows={len(rows)} certified={sum(row.certified for row in rows)} "
        f"early-wins={len(wins)}/{len(fair_wins)} "
        f"literal-wins={len(literal_wins)}/{len(literal_fair_wins)}"
    )
    for row in sorted(rows, key=lambda item: item.ratio)[:30]:
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"ratio={row.ratio:.6f}",
            f"fair={row.fair_ratio:.6f}",
            f"literal={row.literal_ratio:.6f}",
            f"S={row.support_nodes}",
            f"route={row.route_work}",
        )
    if args.random_audit:
        print(f"random-certified={audit_random_trees()}")


if __name__ == "__main__":
    main()
