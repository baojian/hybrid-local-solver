"""Local ACL solver: growing branching core and original-edge flux events.

Retain the seed and every admitted vertex of degree >=3. Eliminate other
admitted vertices. Each unfinished path has one retained endpoint, so its
flux is an affine function of one core potential. Scalar queues report
geometric changes without rounding an accumulated negative Schur load.
The exact dense inverse costs O(r^2) per admission; general OP3 stays open.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass, field
from fractions import Fraction as F
import hashlib
import heapq
import json
from pathlib import Path
import subprocess
import time

from bounded_attachment_cycle import LocalOracle, exact_reference
from geometric_value_events import solve
import networkx as nx


@dataclass
class FluxArm:
    target: int
    endpoint: int
    core: int
    slope: F
    intercept: F
    lower: F = F(0)
    live: bool = True
    publications: int = 0


@dataclass
class Candidate:
    degree: int
    diagonal: F
    arms: list = field(default_factory=list)
    lower: F = F(0)
    queued: bool = False


def local_branch_core(oracle, seed, alpha, epsilon, audit_hook=None):
    """No ambient iteration. The optional full-state hook is audit-only."""
    gamma, lam = (1 - alpha) / (1 + alpha), epsilon / 2
    assert 0 < gamma < 1 and epsilon > 0
    floor, ratio, gate = epsilon / 16, F(5, 4), 11 * epsilon / 20
    degree = oracle.degree(seed)
    if lam * degree >= 1:
        return {}, {"admissions": 0, "cores": [], "publications": 0}
    core, active = [seed], {seed}
    inverse = [[F(1, degree)]]
    values = [(1 - lam * degree) / degree]
    boundary, arms, records, seen_edges = {}, [], [], set()
    heaps, ready = [[]], deque()
    counts = Counter(admissions=1)

    def ensure(label):
        counts["candidate_accesses"] += 1
        if label not in boundary:
            d = oracle.degree(label)
            boundary[label] = Candidate(d, F(d))
            counts["candidate_creations"] += 1
        return boundary[label]

    def add_arm(label, endpoint, slot, slope, intercept):
        candidate = ensure(label)
        arm = FluxArm(label, endpoint, slot, slope, intercept)
        assert slope > 0 and intercept <= 0
        identifier = len(arms)
        arms.append(arm)
        candidate.arms.append(identifier)
        threshold = (floor - intercept) / slope
        heapq.heappush(heaps[slot], (threshold, identifier))
        counts["arm_creations"] += 1
        counts["heap_pushes"] += 1

    def new_edges(label):
        for other in oracle.row(label):
            counts["edge_dictionary_checks"] += 1
            edge = tuple(sorted((label, other)))
            if edge in seen_edges:
                continue
            seen_edges.add(edge)
            assert other not in active
            yield other

    for other in new_edges(seed):
        add_arm(other, seed, 0, gamma, F(0))

    while True:
        counts["event_rounds"] += 1
        for slot, heap in enumerate(heaps):
            counts["core_queue_visits"] += 1
            while heap:
                counts["heap_top_checks"] += 1
                threshold, identifier = heap[0]
                arm = arms[identifier]
                if not arm.live:
                    heapq.heappop(heap)
                    counts["heap_pops"] += 1
                    counts["stale_heap_pops"] += 1
                    continue
                if values[slot] <= threshold:
                    break
                heapq.heappop(heap)
                counts["heap_pops"] += 1
                flux = arm.slope * values[slot] + arm.intercept
                assert flux > ratio * arm.lower + floor
                candidate = boundary[arm.target]
                candidate.lower += flux - arm.lower
                arm.lower = flux
                arm.publications += 1
                counts["publications"] += 1
                if candidate.lower > gate * candidate.degree and not candidate.queued:
                    candidate.queued = True
                    ready.append(arm.target)
                    counts["ready_pushes"] += 1
                threshold = (ratio * flux + floor - arm.intercept) / arm.slope
                heapq.heappush(heap, (threshold, identifier))
                counts["heap_pushes"] += 1
        if audit_hook:
            audit_hook(active, core, inverse, values, boundary, arms, records)
        if not ready:
            counts["quiet_certificates"] += 1
            break
        label = ready.popleft()
        counts["ready_pops"] += 1
        candidate = boundary.pop(label)
        coupling, load = {}, -lam * candidate.degree
        for identifier in candidate.arms:
            arm = arms[identifier]
            assert arm.live
            arm.live = False
            load += arm.intercept
            coupling[arm.core] = coupling.get(arm.core, F(0)) + arm.slope
            counts["consumed_arm_records"] += 1
        surplus = load + sum(a * values[i] for i, a in coupling.items())
        assert surplus > 0 and candidate.lower > gate * candidate.degree
        r = len(core)
        response = [sum(inverse[i][j] * a for j, a in coupling.items()) for i in range(r)]
        counts["inverse_vector_terms"] += r * len(coupling)
        pivot = candidate.diagonal - sum(a * response[i] for i, a in coupling.items())
        assert pivot > 0
        new_value = surplus / pivot
        values = [x + v * new_value for x, v in zip(values, response)]
        counts["core_value_updates"] += r
        for i in range(r):
            for j in range(r):
                inverse[i][j] += response[i] * response[j] / pivot
                counts["inverse_entry_updates"] += 1
        active.add(label)
        counts["admissions"] += 1
        if candidate.degree >= 3:
            for i in range(r):
                inverse[i].append(response[i] / pivot)
            inverse.append([v / pivot for v in response] + [1 / pivot])
            counts["inverse_entry_allocations"] += 2 * r + 1
            core.append(label)
            heaps.append([])
            values.append(new_value)
            for other in new_edges(label):
                add_arm(other, label, r, gamma, F(0))
        else:
            successors = list(new_edges(label))
            assert len(successors) <= 1 and len(coupling) <= 2
            if successors:
                assert len(candidate.arms) == 1 and len(coupling) == 1
                other = successors[0]
                successor = ensure(other)
                successor.diagonal -= gamma * gamma / candidate.diagonal
                slot, a = next(iter(coupling.items()))
                add_arm(
                    other,
                    label,
                    slot,
                    gamma * a / candidate.diagonal,
                    gamma * load / candidate.diagonal,
                )
            records.append((label, candidate.diagonal, load, coupling, successors))
            counts["reverse_records_stored"] += 1
    answer = dict(zip(core, values))
    for label, diagonal, load, coupling, successors in reversed(records):
        answer[label] = (
            load
            + sum(a * values[i] for i, a in coupling.items())
            + gamma * sum(answer.get(other, F(0)) for other in successors)
        ) / diagonal
        assert answer[label] > 0
        counts["reverse_records_read"] += 1
    counts["output_words"] += len(answer)
    counts["maximum_arm_publications"] = max((arm.publications for arm in arms), default=0)
    counts["final_boundary_records"] = len(boundary)
    return answer, {**dict(counts), "cores": core}


def check_acl(graph, seed, alpha, epsilon, answer):
    gamma, lam = (1 - alpha) / (1 + alpha), epsilon / 2
    for i in graph:
        residual = (
            F(int(i == seed))
            - graph.degree(i) * answer.get(i, F(0))
            + gamma * sum(answer.get(j, F(0)) for j in graph[i])
        )
        assert 0 <= residual <= epsilon * graph.degree(i)
        if i in answer:
            assert answer[i] > 0 and residual == lam * graph.degree(i)
        elif i != seed:
            assert residual <= 3 * epsilon * graph.degree(i) / 4
    assert sum(graph.degree(i) for i in answer) <= 2 / epsilon


def face_reference(graph, seed, alpha, epsilon, active):
    labels = sorted(active)
    gamma = (1 - alpha) / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in labels]
        for i in labels
    ]
    load = [F(int(i == seed)) - epsilon * graph.degree(i) / 2 for i in labels]
    return dict(zip(labels, solve(matrix, load)))


def trace_checker(graph, seed, alpha, epsilon, counts):
    gamma = (1 - alpha) / (1 + alpha)
    previous = {}

    def check(active, core, inverse, values, boundary, arms, records):
        nonlocal previous
        exact = face_reference(graph, seed, alpha, epsilon, active)
        assert all(exact[i] > 0 and exact[i] >= previous.get(i, F(0)) for i in exact)
        assert all(exact[i] == x for i, x in zip(core, values))
        labels = sorted(active)
        matrix = [
            [
                F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0)
                for j in labels
            ]
            for i in labels
        ]
        for j, core_label in enumerate(core):
            column = dict(zip(labels, solve(matrix, [F(int(i == core_label)) for i in labels])))
            assert all(inverse[i][j] == column[label] for i, label in enumerate(core))
            counts["dense_inverse_entry_checks"] += len(core)
        for arm in arms:
            if not arm.live:
                continue
            flux = gamma * exact[arm.endpoint]
            assert flux == arm.slope * values[arm.core] + arm.intercept
            assert arm.lower <= flux <= 5 * arm.lower / 4 + epsilon / 16
            counts["physical_flux_checks"] += 1
        for label, candidate in boundary.items():
            assert candidate.lower == sum(arms[i].lower for i in candidate.arms)
            assert len(candidate.arms) == sum(i in active for i in graph[label])
            counts["shared_gate_checks"] += 1
        previous = exact
        counts["dense_trace_faces"] += 1

    return check


def subdivided_core(r, length):
    base = nx.cycle_graph(r)
    base.add_edges_from((i, (i + r // 2) % r) for i in range(r // 2))
    graph = nx.Graph()
    graph.add_nodes_from(range(r))
    for i, j in base.edges:
        previous = i
        for _ in range(length - 1 + (i + 2 * j) % 3):
            label = len(graph)
            graph.add_edge(previous, label)
            previous = label
        graph.add_edge(previous, j)
    return graph


def mixed_quiet_reports(r, n):
    graph = nx.complete_graph(r)
    for j in range(n):
        target = len(graph)
        graph.add_node(target)
        for i in range(r):
            previous = i
            for _ in range(1 + (i + j) % 3):
                label = len(graph)
                graph.add_edge(previous, label)
                previous = label
            graph.add_edge(previous, target)
        for _ in range(100 * r * n + j):
            graph.add_edge(target, len(graph))
    return graph


def cancellation_case(length):
    other = length + (length + 39) // 40
    gamma = 1 - F(1, (length + other + 3) ** 4)
    alpha = (1 - gamma) / (1 + gamma)
    epsilon = F(2 * (length + 1), (length + other + 2) * (length + other + 3))
    return (
        nx.path_graph(length + other + 5),
        "previous_schur_cancellation",
        {"length": length, "other_length": other, "seed": length + 2},
        alpha,
        epsilon,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--trace-max-n", type=int, default=4)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.time()
    totals, trace_counts, rows, cases = Counter(), Counter(), [], 0
    parameters = [
        (F(1, 3), F(1, 5)),
        (F(1, 1009), F(1, 1009)),
        (F(1, 7), F(1, 50)),
        (F(1, 1000003), F(1, 1000003)),
    ]
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha, epsilon in parameters:
                oracle = LocalOracle(graph)
                hook = (
                    trace_checker(graph, seed, alpha, epsilon, trace_counts)
                    if len(graph) <= args.trace_max_n
                    else None
                )
                answer, info = local_branch_core(oracle, seed, alpha, epsilon, hook)
                check_acl(graph, seed, alpha, epsilon, answer)
                assert answer == face_reference(graph, seed, alpha, epsilon, answer)
                optimum = exact_reference(graph, seed, alpha, epsilon / 2)
                assert all(0 < value <= optimum[i] for i, value in answer.items())
                assert set(oracle.rows) == set(answer)
                assert len(info["cores"]) == sum(i == seed or graph.degree(i) >= 3 for i in answer)
                totals.update(
                    {
                        k: v
                        for k, v in info.items()
                        if isinstance(v, int) and not k.startswith("maximum_")
                    }
                )
                totals["maximum_arm_publications"] = max(
                    totals["maximum_arm_publications"], info.get("maximum_arm_publications", 0)
                )
                totals.update(oracle.counts)
                cases += 1
    if args.structured:
        for graph, family, metadata, alpha, epsilon in [
            *[
                (
                    subdivided_core(r, length),
                    "subdivided_growing_core",
                    {"r": r, "length": length},
                    F(1, 1000003),
                    F(1, 1000003),
                )
                for r in [4, 8, 16]
                for length in [2, 8]
            ],
            *[
                (
                    mixed_quiet_reports(r, n),
                    "mixed_quiet_reports",
                    {"r": r, "reports": n},
                    F(1, 3),
                    F(1, 1000 * r * n),
                )
                for r, n in [(4, 4), (8, 8), (16, 8)]
            ],
            *[
                (nx.path_graph(2), "threshold_equality", {"which": which}, F(1, 3), epsilon)
                for which, epsilon in [("publication", F(8, 5)), ("admission", F(5, 8))]
            ],
            *[
                (nx.star_graph(n), "large_star", {"leaves": n}, F(1, 1000003), F(1, 10 * n))
                for n in [256, 1024, 4096]
            ],
            *[cancellation_case(length) for length in [64, 128, 256]],
        ]:
            oracle = LocalOracle(graph)
            seed = metadata.get("seed", 0)
            answer, info = local_branch_core(oracle, seed, alpha, epsilon)
            check_acl(graph, seed, alpha, epsilon, answer)
            assert set(oracle.rows) == set(answer)
            if family == "threshold_equality":
                assert len(answer) == 1
            rows.append(
                {
                    "family": family,
                    **metadata,
                    "ambient_vertices": len(graph),
                    "alpha_lazy": str(alpha),
                    "eps_appr": str(epsilon),
                    "support_vertices": len(answer),
                    "support_volume": sum(graph.degree(i) for i in answer),
                    "oracle_counts": dict(oracle.counts),
                    "info": info,
                }
            )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.branch_core_flux",
        "arithmetic": "exact fractions; scalar heaps and dense core inverse",
        "max_n": args.max_n,
        "trace_max_n": args.trace_max_n,
        "exact_face_and_obstacle_comparisons": cases,
        "parameters_alpha_epsilon": [[str(a), str(e)] for a, e in parameters],
        "lambda": "eps_appr/2",
        "seed": "every atlas vertex; structured metadata seed, default 0",
        "random_seed": None,
        "stopping_rule": "all scalar publication queues settled and no lower gate > 11 eps d / 20",
        "counts": dict(totals),
        "audit_only_trace_counts": dict(trace_counts),
        "structured_rows": rows,
        "git_commit": subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
        ).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(
                ["git", "-C", str(repo), "status", "--porcelain"], text=True
            ).strip()
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds_including_reference": round(time.time() - started, 3),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
