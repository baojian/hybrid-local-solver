"""Conservative local discovery, upward-alpha transfer and a paid closed solve.

Zero teleportation is only an internal discovery parameter. All outputs
solve the original positive-target-alpha ACL problem. Whole-component
LDL elimination is implemented and charged; global residual and flux
calculations below are independent validators, never production access.
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

from native_gap_push import NativePush
from small_alpha_constant_shift import residual
from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub
import networkx as nx


def solve_closed(state, seed, alpha, work):
    """Exact target PageRank on already cached, certified whole support."""
    records = state.records
    size = records.size
    assert size == state.active_count and size >= 2 and 0 < alpha <= 1
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [[F(0)] * size for _ in range(size)]
    forward, answer = [F(0)] * size, [F(0)] * size
    work["closed_matrix_and_vector_words_reserved"] += size * size + 3 * size + 12
    work["closed_matrix_and_vector_initialization"] += size * size + 3 * size + 16
    for i in range(size):
        record = records.array[i]
        matrix[i][i] = F(record.degree)
        forward[i] = F(record.label == seed)
        work["closed_original_degree_and_seed_rhs_reads"] += 7
        for neighbor in record.neighbors:
            j = records.position(neighbor.label)
            assert j < size and records.array[j] is neighbor
            matrix[i][j] = -gamma
            work["closed_cached_original_entry_and_matrix_write"] += 6
    # In-place lower LDL^T: store multipliers strictly below the diagonal,
    # and the Schur pivots on the diagonal. Upper entries are not reused.
    for k in range(size):
        pivot = matrix[k][k]
        assert pivot > 0
        work["closed_positive_pivot_checks"] += 4
        for i in range(k + 1, size):
            matrix[i][k] /= pivot
            work["closed_factor_multiplier_updates"] += 5
        for i in range(k + 1, size):
            for j in range(k + 1, i + 1):
                matrix[i][j] -= matrix[i][k] * pivot * matrix[j][k]
                work["closed_schur_scalar_updates"] += 10
    for i in range(size):
        for j in range(i):
            forward[i] -= matrix[i][j] * forward[j]
            work["closed_forward_triangular_updates"] += 8
    for i in range(size):
        forward[i] /= matrix[i][i]
        work["closed_diagonal_solve_updates"] += 5
    for i in range(size - 1, -1, -1):
        value = forward[i]
        for j in range(i + 1, size):
            value -= matrix[j][i] * answer[j]
            work["closed_backward_triangular_updates"] += 8
        assert value >= 0
        answer[i] = value
        work["closed_solution_guard_and_write"] += 5
    output = [None] * size
    work["closed_output_words_reserved"] += 3 * size + 2
    for i in range(size):
        output[i] = (records.array[i].label, answer[i])
        work["closed_output_label_and_value_writes"] += 4
    work["closed_target_systems_solved"] += 1
    return output


def solve_local(oracle, seed, alpha, epsilon, work, validator=None):
    assert 0 < alpha <= 1 and 0 < epsilon < 1
    bar = 2 * alpha / (1 + alpha)
    conservative = bar <= epsilon * epsilon / 4
    work["conservative_regime_and_parameter_operations"] += 10
    state = NativePush(
        oracle, seed, F(0) if conservative else alpha, epsilon, work, allow_zero=conservative
    )
    output = state.run(validator, stop_on_full_support=True)
    work["terminal_full_support_counter_comparisons"] += 3
    if state.active_count == state.records.size:
        output = solve_closed(state, seed, alpha, work)
        branch = "conservative_full_exact" if conservative else "damped_full_exact"
    else:
        branch = "conservative_proper" if conservative else "damped_native"
    return {"records": output, "branch": branch}, state


def validate_prefix(graph, seed, state, counts):
    records = state.records.array[: state.records.size]
    vector = [F(0)] * len(graph)
    stored = {record.label: record for record in records}
    assert list(stored) == sorted(stored)
    for record in records:
        vector[record.label] = record.value
        assert record.degree == graph.degree(record.label)
        assert record.active == (record.value > 0)
        if record.active:
            assert {r.label for r in record.neighbors} == set(graph[record.label])
            assert all(stored[r.label] is r for r in record.neighbors)
    actual = residual(graph, seed, state.alpha, vector)
    assert all(r >= 0 for r in actual)
    assert actual == [stored[i].residual if i in stored else 0 for i in graph]
    assert sum(actual) == state.mass
    active = {i for i in graph if vector[i] > 0}
    volume = sum(graph.degree(i) for i in active)
    assert volume == state.active_volume < 2 / state.epsilon
    assert state.active_count == len(active)
    assert len(stored) <= 1 + volume
    assert all(actual[i] >= state.lam * graph.degree(i) for i in active)
    if active:
        assert seed in active and nx.is_connected(graph.subgraph(active))
    seen, cursor = set(), state.head
    while cursor is not None:
        assert cursor.queued and cursor.label not in seen
        seen.add(cursor.label)
        cursor = cursor.next
    assert seen == {r.label for r in records if r.queued}
    assert seen == {r.label for r in records if r.residual > state.epsilon * r.degree}
    assert (state.active_count == state.records.size) == (len(active) == len(graph))
    if state.alpha == 0:
        assert state.mass == 1
        assert max(vector) < 2 / state.epsilon
        assert state.push_degree_work < 8 / state.epsilon**3
        assert all(abs(vector[i] - vector[j]) <= 1 for i, j in graph.edges)
        for threshold in set(vector):
            upper = {i for i in graph if vector[i] > threshold}
            if not upper:
                continue
            flux = sum(vector[i] - vector[j] for i in upper for j in graph[i] if j not in upper)
            assert flux == F(seed in upper) - sum(actual[i] for i in upper)
            assert 0 < flux <= 1
            counts["conservative_strict_superlevel_fluxes"] += 1
        counts["conservative_prefix_value_work_and_edge_bounds"] += 1
    else:
        assert state.push_degree_work <= 2 / (state.bar * state.epsilon)
    counts["exact_prefix_queue_map_residual_and_closure_checks"] += 1
    counts["validator_prefix_original_residual_rows"] += len(graph)


def audit_case(graph, seed, alpha, epsilon, counts, work):
    access = LocalRows(graph, work)

    def validator(state):
        validate_prefix(graph, seed, state, counts)

    before_work = sum(work.values())
    output, state = solve_local(access, seed, alpha, epsilon, work, validator)
    vector = [F(0)] * len(graph)
    for label, value in output["records"]:
        assert value > 0
        vector[label] = value
    actual = residual(graph, seed, alpha, vector)
    assert all(0 <= r <= epsilon * graph.degree(i) for i, r in enumerate(actual))
    assert sum(graph.degree(i) for i in graph if vector[i] > 0) < 2 / epsilon
    if output["branch"].endswith("full_exact"):
        assert all(r == 0 for r in actual)
        assert len(output["records"]) == len(graph)
        counts["implemented_closed_LDL_exact_target_certificates"] += 1
    assert len(access.row_log) == len(set(access.row_log)) == state.active_count
    assert len(access.degree_log) == len(set(access.degree_log)) == state.records.size
    assert state.push_degree_work < 8 / epsilon**3
    assert sum(work.values()) - before_work <= 10000 * (1 + epsilon**-3)
    counts["complete_original_target_ACL_certificates"] += 1
    counts["validator_terminal_original_residual_rows"] += len(graph)
    counts["branch_" + output["branch"]] += 1
    counts["native_pushes"] += state.push_count
    counts["native_degree_weighted_updates"] += state.push_degree_work
    counts["original_rows_queried_once"] += len(access.row_log)
    counts["original_degrees_queried_once"] += len(access.degree_log)
    return {
        "vertices": len(graph),
        "edges": graph.number_of_edges(),
        "seed": seed,
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "native_pushes": state.push_count,
        "degree_weighted_updates": state.push_degree_work,
        "active_volume": state.active_volume,
        "branch": output["branch"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= (5 if args.full else 3) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for epsilon in [F(1, 4), F(1, 2), F(3, 4)] if args.full else [F(3, 4)]:
                boundary = epsilon**2 / (8 - epsilon**2)
                values = [F(1), F(1, 3), boundary, 2 * boundary, F(1, 2**80)]
                for alpha in values if args.full else [boundary, F(1, 2**80)]:
                    audit_case(graph, seed, alpha, epsilon, counts, work)
    stress = []
    for graph, epsilon in [
        (nx.path_graph(2), F(1, 8)),
        (nx.path_graph(3), F(1, 4)),
        (nx.cycle_graph(8), F(1, 4)),
        (nx.path_graph(16), F(1, 4)),
    ]:
        stress.append(audit_case(graph, 0, F(1, 2**80), epsilon, counts, work))
    if args.full:
        for graph, epsilon in [
            (nx.path_graph(8), F(1, 16)),
            (nx.cycle_graph(6), F(1, 16)),
            (nx.complete_graph(8), F(1, 128)),
        ]:
            for alpha in [F(1, 3), F(1, 2**1024)]:
                stress.append(audit_case(graph, 0, alpha, epsilon, counts, work))
    for degree in [2**20, 2**80, 2**1024]:
        access = MassiveHub(degree, work)
        result, state = solve_local(access, 0, F(1, 2**1024), F(1, 4), work)
        assert access.rows == [0] and state.active_volume == 1 and state.push_count == 1
        assert result["records"] == [(0, F(7, 8))]
        counts["private_huge_hub_single_row_compositions"] += 1
    result = {
        "audit": "incremental_active_set_sdd.conservative_local_producer",
        "scope": "Implemented conservative/damped local push, first-full-support stop, upward-alpha residual transfer and fully charged exact whole-component LDL solve. No numerical solve is a production oracle.",
        "arithmetic": "exact fractions; charged exact-real word model. No bit or Python scalar-allocation complexity claim.",
        "parameters": {
            "full": args.full,
            "native_epsilon": "eps_appr",
            "native_lambda": "eps_appr/2",
            "conservative_regime": "bar_alpha <= eps_appr^2/4",
            "random_seed": None,
        },
        "audit_only": dict(counts),
        "stress_profiles": stress,
        "charged_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "native_gap_push.py",
                "small_alpha_constant_shift.py",
                "small_alpha_floor.py",
                "supplied_envelope_work.py",
            ]
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
