#!/usr/bin/env python3
"""Check and summarize the saved literal two-stage benchmark columns."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

try:
    from .face_verifier import exact_face_verifier
    from .portfolio_benchmark import broom_graph, cycle_graph, normalized_matrix, path_graph
    from .structural_solvers import (
        factor_tree_or_unicyclic_principal,
        reused_structural_backsolve_work,
    )
except ImportError:  # Direct script execution.
    from face_verifier import exact_face_verifier
    from portfolio_benchmark import broom_graph, cycle_graph, normalized_matrix, path_graph
    from structural_solvers import (
        factor_tree_or_unicyclic_principal,
        reused_structural_backsolve_work,
    )


ROOT = Path(__file__).resolve().parent


def exhaustive_obstacle_support(
    adjacency: list[list[int]], alpha: float, rho: float, seed: int = 0
) -> np.ndarray:
    """Small dense KKT reference, independent of the structural verifier."""
    degree, matrix = normalized_matrix(adjacency, alpha)
    source = -alpha * rho * np.sqrt(degree)
    source[seed] += alpha / np.sqrt(degree[seed])
    size = len(adjacency)
    solutions: list[np.ndarray] = []
    for mask in range(1 << size):
        active = np.array([(mask >> vertex) & 1 for vertex in range(size)], dtype=bool)
        point = np.zeros(size)
        if active.any():
            principal = matrix[active][:, active].toarray()
            point[active] = np.linalg.solve(principal, source[active])
            if np.min(point[active]) <= 1e-10:
                continue
        residual = source - matrix @ point
        if np.max(np.abs(residual[active]), initial=0.0) > 2e-9:
            continue
        if np.max(residual[~active], initial=-np.inf) > 1e-10:
            continue
        solutions.append(active)
    assert len(solutions) == 1
    return solutions[0]


def interval_verifier_false_positive_audit() -> tuple[int, int, int]:
    """Enumerate every small candidate face and reject every false certificate."""
    rng = np.random.default_rng(20260831)
    cases = 0
    candidates = 0
    exact_certificates = 0
    for trial in range(36):
        size = int(rng.integers(5, 10))
        adjacency: list[list[int]] = [[] for _ in range(size)]

        def connect(left: int, right: int) -> None:
            adjacency[left].append(right)
            adjacency[right].append(left)

        if trial % 2 == 0:
            for vertex in range(1, size):
                connect(vertex, int(rng.integers(0, vertex)))
        else:
            cycle_size = int(rng.integers(3, min(size, 6) + 1))
            for vertex in range(cycle_size):
                connect(vertex, (vertex + 1) % cycle_size)
            for vertex in range(cycle_size, size):
                connect(vertex, int(rng.integers(0, vertex)))
        alpha = (0.07, 0.19, 0.43)[trial % 3]
        rho = (0.012, 0.037, 0.083, 0.14)[trial % 4]
        exact = exhaustive_obstacle_support(adjacency, alpha, rho)
        exact_seen = False
        for mask in range(1 << size):
            candidate = np.array([(mask >> vertex) & 1 for vertex in range(size)], dtype=bool)
            certified, _work, _volume, _minimum, _maximum = exact_face_verifier(
                adjacency, alpha, rho, 0, candidate
            )
            candidates += 1
            if certified:
                assert np.array_equal(candidate, exact)
                exact_seen = True
        if exact_seen:
            exact_certificates += 1
        cases += 1
    return cases, candidates, exact_certificates


def read(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def positive(value: str) -> bool:
    return float(value) > 0.0


def semantic_audit(rows: list[dict[str, str]]) -> None:
    for row in rows:
        value = row.get("semantic_error")
        if value in (None, "", "nan") or not math.isfinite(float(value)):
            continue
        assert float(value) <= float(row["epsilon"]) * (1.0 + 1e-6) + 2e-10


def factor_reuse_audit() -> tuple[list[tuple[str, int, int]], int]:
    """Factor once, solve the RPPR and ordinary-PPR right-hand sides, and audit both."""
    cases = [
        ("path", path_graph(17)),
        ("broom", broom_graph(9, 7)),
        ("cycle", cycle_graph(18)),
    ]
    rng = np.random.default_rng(20260830)
    for trial in range(80):
        size = int(rng.integers(6, 34))
        adjacency: list[list[int]] = [[] for _ in range(size)]

        def connect(left: int, right: int) -> None:
            adjacency[left].append(right)
            adjacency[right].append(left)

        if trial % 2 == 0:
            for vertex in range(1, size):
                connect(vertex, int(rng.integers(0, vertex)))
            name = "random-tree"
        else:
            cycle_size = int(rng.integers(3, min(size, 10) + 1))
            for vertex in range(cycle_size):
                connect(vertex, (vertex + 1) % cycle_size)
            for vertex in range(cycle_size, size):
                connect(vertex, int(rng.integers(0, vertex)))
            name = "random-unicyclic"
        cases.append((name, adjacency))
    summaries = []
    alpha = 0.07
    rho = 0.004
    for name, adjacency in cases:
        degree, matrix = normalized_matrix(adjacency, alpha)
        envelope = np.ones(len(adjacency), dtype=bool)
        factors = factor_tree_or_unicyclic_principal(
            adjacency,
            envelope,
            degree,
            alpha,
            0,
        )
        ppr_source = np.zeros(len(adjacency))
        ppr_source[0] = alpha / np.sqrt(degree[0])
        rppr_source = ppr_source - alpha * rho * np.sqrt(degree)
        expected_work = reused_structural_backsolve_work(adjacency, envelope)
        for source in (rppr_source, ppr_source):
            output, work = factors.solve(source)
            reference = np.asarray(spsolve(matrix, source))
            assert np.max(np.abs(output - reference)) <= 2e-11
            assert work == expected_work
        if len(summaries) < 3:
            summaries.append((name, len(adjacency), expected_work))
    return summaries, len(cases) - len(summaries)


def main() -> None:
    reuse_audit = factor_reuse_audit()
    verifier_audit = interval_verifier_false_positive_audit()
    appr = read("appr_exact_face_screen_results.csv")
    sor = read("sor_support_then_solve_results.csv")
    batch = read("batch_exact_active_set_results.csv")
    tree = read("tree_threshold_hybrid_results.csv")
    structural = read("structured_tail_results.csv")
    for rows in (appr, sor, batch, tree, structural):
        semantic_audit(rows)
    for rows in (appr, sor, batch):
        for row in rows:
            if "reused_stage2_work" not in row:
                continue
            assert float(row["reused_stage2_work"]) <= float(row["stage2_work"])

    appr_certified = [row for row in appr if row["certified"] == "True"]
    for row in appr_certified:
        assert float(row["minimum_active"]) > 0.0
        assert float(row["maximum_boundary_key"]) <= 0.0
    appr_nontrivial = [row for row in appr_certified if positive(row["direct_work"])]
    appr_counts = (
        len(appr_certified),
        len(appr_nontrivial),
        sum(
            float(row["raw_sequential_work"]) < float(row["direct_work"]) for row in appr_nontrivial
        ),
        sum(float(row["ratio"]) < 1.0 for row in appr_nontrivial),
        sum(
            float(row["strict_two_stage_work"]) < float(row["direct_work"])
            for row in appr_nontrivial
        ),
        sum(float(row["strict_ratio"]) < 1.0 for row in appr_nontrivial),
    )
    assert appr_counts == (28, 19, 9, 4, 4, 2)
    appr_reused = (
        sum(
            float(row["reused_two_stage_work"]) < float(row["direct_work"])
            for row in appr_nontrivial
        ),
        sum(float(row["reused_ratio"]) < 1.0 for row in appr_nontrivial),
    )
    assert appr_reused == (6, 2)

    sor_certified = [row for row in sor if row["certified"] == "True"]
    sor_counts = (
        len(sor_certified),
        sum(
            float(row["active_lane_work"]) < float(row["direct_work"])
            for row in sor_certified
            if positive(row["direct_work"])
        ),
        sum(float(row["ratio"]) < 1.0 for row in sor_certified if positive(row["direct_work"])),
        sum(
            float(row["strict_two_stage_work"]) < float(row["direct_work"])
            for row in sor_certified
            if positive(row["direct_work"])
        ),
        sum(
            float(row["strict_ratio"]) < 1.0
            for row in sor_certified
            if positive(row["direct_work"])
        ),
    )
    assert sor_counts == (75, 8, 5, 5, 5)
    sor_reused = (
        sum(
            float(row["reused_two_stage_work"]) < float(row["direct_work"])
            for row in sor_certified
            if positive(row["direct_work"])
        ),
        sum(
            float(row["reused_ratio"]) < 1.0
            for row in sor_certified
            if positive(row["direct_work"])
        ),
    )
    assert sor_reused == (7, 5)

    batch_exact = [
        row for row in batch if positive(row["support_nodes"]) or int(row["rounds"]) == 0
    ]
    batch_counts = (
        len(batch_exact),
        sum(row["exact_lane_wins"] == "True" for row in batch_exact),
        sum(float(row["ratio"]) < 1.0 for row in batch_exact if positive(row["direct_work"])),
        sum(
            float(row["strict_two_stage_work"]) < float(row["direct_work"])
            for row in batch_exact
            if positive(row["direct_work"])
        ),
        sum(
            float(row["strict_ratio"]) < 1.0 for row in batch_exact if positive(row["direct_work"])
        ),
    )
    assert batch_counts == (75, 43, 13, 33, 8)
    batch_reused = (
        sum(
            float(row["reused_two_stage_work"]) < float(row["direct_work"])
            for row in batch_exact
            if positive(row["direct_work"])
        ),
        sum(
            float(row["reused_ratio"]) < 1.0 for row in batch_exact if positive(row["direct_work"])
        ),
    )
    assert batch_reused == (37, 9)

    tree_certified = [row for row in tree if row["certified"] == "True"]
    tree_nontrivial = [row for row in tree_certified if positive(row["direct_work"])]
    tree_counts = (
        len(tree_certified),
        len(tree_nontrivial),
        sum(
            float(row["literal_two_stage_work"]) < float(row["direct_work"])
            for row in tree_nontrivial
        ),
        sum(float(row["literal_fair_ratio"]) < 1.0 for row in tree_nontrivial),
    )
    assert tree_counts == (60, 51, 27, 14)

    structural_success = [row for row in structural if row["succeeded"] == "True"]
    structural_counts = (
        len(structural_success),
        sum(
            float(row["total_work"]) < float(row["direct_work"])
            for row in structural_success
            if positive(row["direct_work"])
        ),
        sum(
            2.0 * float(row["total_work"]) < float(row["direct_work"])
            for row in structural_success
            if positive(row["direct_work"])
        ),
    )
    assert structural_counts == (56, 50, 35)

    structural_by_key = {(row["family"], row["alpha"], row["epsilon"]): row for row in structural}
    tree_three_way_wins = 0
    tree_three_way_sources = {"tree": 0, "green": 0}
    for row in tree_nontrivial:
        key = (row["family"], row["alpha"], row["epsilon"])
        candidates = [("tree", float(row["literal_two_stage_work"]))]
        green = structural_by_key[key]
        if green["succeeded"] == "True":
            candidates.append(("green", float(green["total_work"])))
        source, work = min(candidates, key=lambda item: item[1])
        if 3.0 * work < float(row["direct_work"]):
            tree_three_way_wins += 1
            tree_three_way_sources[source] += 1
    assert tree_three_way_wins == 23
    assert tree_three_way_sources == {"tree": 2, "green": 21}

    print("literal two-stage result consistency: PASS")
    print(f"reusable structural factors: {reuse_audit[0]}, randomized cases={reuse_audit[1]}")
    print(
        "interval verifier exhaustive randomized audit: "
        f"cases={verifier_audit[0]}, candidates={verifier_audit[1]}, "
        f"exact certified={verifier_audit[2]}"
    )
    print("lane | certified/nontrivial | early raw/fair | literal raw/fair")
    print(
        f"APPR proposal | {appr_counts[0]}/{appr_counts[1]} | {appr_counts[2]}/{appr_counts[3]} | {appr_counts[4]}/{appr_counts[5]}"
    )
    print(
        f"SOR proposal | {sor_counts[0]} | {sor_counts[1]}/{sor_counts[2]} | {sor_counts[3]}/{sor_counts[4]}"
    )
    print(
        f"exact batch | {batch_counts[0]} | {batch_counts[1]}/{batch_counts[2]} | {batch_counts[3]}/{batch_counts[4]}"
    )
    print(
        "factor reuse raw/fair | "
        f"APPR {appr_reused[0]}/{appr_reused[1]} | "
        f"SOR {sor_reused[0]}/{sor_reused[1]} | "
        f"batch {batch_reused[0]}/{batch_reused[1]}"
    )
    print(
        f"tree messages | {tree_counts[0]}/{tree_counts[1]} | -- | {tree_counts[2]}/{tree_counts[3]}"
    )
    print(
        f"Green structural | {structural_counts[0]} | -- | {structural_counts[1]}/{structural_counts[2]}"
    )
    print(
        f"direct + tree messages + Green | 51 | -- | --/{tree_three_way_wins} "
        f"(tree {tree_three_way_sources['tree']}, Green {tree_three_way_sources['green']})"
    )


if __name__ == "__main__":
    main()
