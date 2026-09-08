"""Finite binary-tree obstruction to the implemented first-eligible group order.

Huge ambient trees are private lazy oracles. Executed capped prefixes are
explicitly nonterminal and are not reported as completed ACL outputs.
Radial systems and symbolic inequalities are independent proof validators.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontier_groups import GroupFrontier
from geometric_value_events import mv, solve


class PrivateBinaryTree:
    def __init__(self, depth, work):
        self._depth, self.work = depth, work
        self.degree_log, self.row_log = [], []

    def degree(self, label):
        assert 1 <= label < 2 ** (self._depth + 1)
        self.work["private_tree_original_degree_queries"] += 1
        self.degree_log.append(label)
        if label == 1:
            return 2
        return 1 if label >= 2**self._depth else 3

    def row(self, label):
        self.work["private_tree_original_row_queries"] += 1
        self.row_log.append(label)
        if label != 1:
            self.work["private_tree_original_adjacency_entries"] += 1
            yield label // 2
        if label < 2**self._depth:
            self.work["private_tree_original_adjacency_entries"] += 2
            yield 2 * label
            yield 2 * label + 1


def parameters(radius):
    lam = F(1, 64 * 2**radius)
    t = F(1, 48 * radius)
    return lam, t, t / (2 - t)


def radial_matrix(depth, gamma):
    """Validator-only quotient of the original-degree Dirichlet ball."""
    matrix = [[F(0)] * (depth + 1) for _ in range(depth + 1)]
    for i in range(depth + 1):
        matrix[i][i] = F(2 if i == 0 else 3)
        if i:
            matrix[i][i - 1] = -gamma
        if i < depth:
            matrix[i][i + 1] = -2 * gamma
    return matrix


def radial_face(depth, gamma, lam):
    matrix = radial_matrix(depth, gamma)
    load = [F(int(i == 0)) - lam * (2 if i == 0 else 3) for i in range(depth + 1)]
    values = solve(matrix, load)
    assert mv(matrix, values) == load and min(values) > 0
    return matrix, load, values


def symbolic(radius, counts):
    lam, t, alpha = parameters(radius)
    depth = 4 * radius + 8
    volume = 2 ** (depth + 2) - 4
    assert volume > 4 / (2 * lam)
    assert (1 - alpha) / (1 + alpha) == 1 - t
    q = (1 - 3 * t) / 2
    assert alpha == F(1, 96 * radius - 1)
    assert 3 - (1 - t) / q - 2 * (1 - t) * q == -3 * t * t * (5 - 3 * t) / (1 - 3 * t) < 0
    assert q**radius >= F(15, 16 * 2**radius)
    assert (1 - t) * F(3, 16 * 2**radius) > F(9, 128 * 2**radius)
    assert 3 * 2**radius * lam <= F(3, 64)
    assert 3 * 2 ** (radius + 1) - 4 < 1 / lam
    counts["symbolic_finite_ambient_volume_and_parameter_certificates"] += 1
    counts["symbolic_uniform_radial_gate_and_cubic_count_certificates"] += 1


def radial_checks(radius, counts):
    lam, t, _ = parameters(radius)
    for depth in range(radius):
        matrix0, load, original = radial_face(depth, F(1), lam)
        matrix, _, damped = radial_face(depth, 1 - t, lam)
        volume = 3 * 2 ** (depth + 1) - 4
        degrees = [F(2 if i == 0 else 3) for i in range(depth + 1)]
        explicit = [
            sum((1 - lam * (3 * 2 ** (k + 1) - 4)) / 2 ** (k + 1) for k in range(i, depth + 1))
            for i in range(depth + 1)
        ]
        assert original == explicit and max(original) < 1
        assert original[-1] == (1 - lam * volume) / 2 ** (depth + 1)
        assert min(original) == original[-1] >= F(61, 64 * 2**radius)
        source = [F(int(i == 0)) for i in range(depth + 1)]
        green = solve(matrix, source)
        torsion0 = solve(matrix0, degrees)
        torsion = solve(matrix, degrees)
        explicit_torsion = [
            3 * (depth + 1 - i) - 4 * (F(1, 2**i) - F(1, 2 ** (depth + 1)))
            for i in range(depth + 1)
        ]
        assert torsion0 == explicit_torsion
        assert all(
            0 < w <= w0 <= 3 * (depth + 1 - i) for i, (w, w0) in enumerate(zip(torsion, torsion0))
        )
        q = (1 - 3 * t) / 2
        lower_green = [F(1, 2) * (q**i - q ** (depth + 1)) for i in range(depth + 1)]
        assert all(a <= b for a, b in zip(mv(matrix, lower_green), source))
        assert all(0 < a <= b for a, b in zip(lower_green, green))
        assert q**depth >= F(15, 16 * 2**depth)
        lower_face = [y - lam * w for y, w in zip(lower_green, torsion0)]
        assert all(a >= F(3 * (depth + 1 - i), 16 * 2**radius) for i, a in enumerate(lower_face))
        assert all(a <= b <= c for a, b, c in zip(lower_face, damped, original))
        assert damped == [g - lam * w for g, w in zip(green, torsion)]
        assert (1 - t) * damped[-1] > F(9, 128 * 2**radius)
        counts["independent_conservative_and_damped_radial_faces"] += 2
        counts["independent_radial_Green_and_torsion_solves"] += 3
        counts["rational_Green_subsolution_and_positive_face_checks"] += 1
        counts["original_degree_radial_rows_checked"] += 2 * (depth + 1)


def implemented_prefix(radius, counts, aggregate):
    start = time.monotonic()
    depth = 4 * radius + 8
    lam, t, alpha = parameters(radius)
    work = Counter()
    oracle = PrivateBinaryTree(depth, work)
    state = GroupFrontier(oracle, 1, alpha, 2 * lam, work)
    pivots = 2 ** (radius + 1) - 1
    level_updates = 0
    for label in range(1, pivots + 1):
        vertex = state.eligible()
        assert vertex is not None and vertex.label == label
        before = state.metrics["shared_matrix_updates"]
        if label >= 2**radius:
            assert state.live_count >= 2 ** (radius - 1)
        state.advance(vertex)
        if label >= 2**radius:
            level_updates += state.metrics["shared_matrix_updates"] - before
        counts["executed_exact_breadth_first_positive_prefix_pivots"] += 1
    assert state.metrics.get("original_row_partition_splits", 0) == 0
    assert state.live_count == 2**radius
    assert state.next_group == 2 ** (radius + 1)
    assert state.volume == 3 * 2 ** (radius + 1) - 4 < 1 / lam
    assert level_updates >= 2 ** (3 * radius - 3)
    assert oracle.row_log == list(range(1, pivots + 1))
    assert oracle.degree_log == list(range(1, 2 * pivots + 2))
    assert state.metrics["maximum_transient_response_groups"] == 2**radius + 1
    # The prefix is intentionally stopped with further legal admissions.
    next_vertex = state.eligible()
    assert next_vertex is not None and next_vertex.label == pivots + 1
    state.lift()
    _, _, exact = radial_face(radius, 1 - t, lam)
    for pivot in state.history:
        label = pivot.vertex.label
        assert pivot.vertex.value == exact[label.bit_length() - 1]
        counts["independent_prefix_radial_coordinate_checks"] += 1
    assert (1 - t) * exact[-1] > (state.lam + state.kappa) * 3
    group = state.head
    while group is not None:
        assert group.heap.size == 2
        a, b = sorted(vertex.label for vertex in group.heap.data[: group.heap.size])
        assert a % 2 == 0 and b == a + 1
        group = group.next
        counts["exact_terminal_prefix_sibling_group_checks"] += 1
    aggregate.update(work)
    counts["nonterminal_capped_producer_prefixes"] += 1
    return {
        "radius": radius,
        "finite_ambient_depth": depth,
        "ambient_vertices_formula": f"2^{depth + 1}-1",
        "seed": 1,
        "alpha": str(alpha),
        "epsilon": str(2 * lam),
        "completed_ACL_solve": False,
        "stop": f"explicit audit cap after {pivots} positive pivots",
        "further_legal_vertex": next_vertex.label,
        "original_active_volume": state.volume,
        "discovered_labels": state.vertices.size,
        "live_sibling_groups": state.live_count,
        "level_R_shared_matrix_updates": level_updates,
        "proved_level_R_lower_bound": 2 ** (3 * radius - 3),
        "metrics": dict(state.metrics),
        "charged_units": sum(work.values()),
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    counts, work, profiles = Counter(), Counter(), []
    for radius in range(1, 1025 if args.full else 33):
        symbolic(radius, counts)
    for radius in range(1, 13 if args.full else 5):
        radial_checks(radius, counts)
    for radius in range(1, 7 if args.full else 4):
        profile = implemented_prefix(radius, counts, work)
        profiles.append(profile)
        print(
            json.dumps(
                {
                    "prefix_radius": radius,
                    "seconds": profile["elapsed_seconds"],
                    "shared_updates": profile["metrics"]["shared_matrix_updates"],
                }
            ),
            flush=True,
        )
    result = {
        "description": __doc__,
        "full": args.full,
        "audit_only": dict(counts),
        "charged_prefix_implementation_units": dict(work),
        "profiles": profiles,
        "producer_randomness": "none",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ["frontier_groups.py", "frontier_exact.py", "geometric_value_events.py"]
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
