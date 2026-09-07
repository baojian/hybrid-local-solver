"""Local ACL with grouped physical-flux events and current-degree core peeling.

Every positive admission is temporarily retained. A nonseed retained vertex
with at most two reduced neighbors is eliminated, possibly moving one flux
group. Dense inverse entries use stable original labels; deleting a core
vertex restricts that inverse without reindexing saved recovery equations.
The maximum simultaneous core size remains an explicit work parameter.
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
from branch_core_flux import (
    check_acl,
    face_reference,
    subdivided_core,
    mixed_quiet_reports,
    cancellation_case,
)
from geometric_value_events import solve
import networkx as nx


@dataclass
class Core:
    diagonal: F
    load: F
    value: F
    edges: dict = field(default_factory=dict)
    groups: dict = field(default_factory=dict)
    heap: list = field(default_factory=list)


@dataclass
class Boundary:
    degree: int
    diagonal: F
    groups: dict = field(default_factory=dict)
    lower: F = F(0)
    queued: bool = False


@dataclass
class Group:
    core: int
    target: int
    slope: F
    intercept: F
    incidences: int
    lower: F
    live: bool = True
    publications: int = 0


def local_peeling(oracle, seed, alpha, epsilon, audit=None, policy="fifo"):
    gamma, lam = (1 - alpha) / (1 + alpha), epsilon / 2
    assert 0 < gamma < 1 and epsilon > 0 and policy in {"fifo", "lifo"}
    floor, ratio, gate = epsilon / 16, F(5, 4), 11 * epsilon / 20
    degree = oracle.degree(seed)
    if lam * degree >= 1:
        return {}, {"admissions": 0, "peak_core_size": 0, "final_core_size": 0}
    cores = {seed: Core(F(degree), 1 - lam * degree, (1 - lam * degree) / degree)}
    inverse = {seed: {seed: F(1, degree)}}
    active, boundary, groups, records, seen_edges = {seed}, {}, [], [], set()
    ready, peeling = deque(), deque()
    counts = Counter(admissions=1, core_births=1, inverse_entry_allocations=1, peak_core_size=1)

    def ensure(label):
        counts["boundary_record_accesses"] += 1
        if label not in boundary:
            d = oracle.degree(label)
            boundary[label] = Boundary(d, F(d))
            counts["boundary_creations"] += 1
        return boundary[label]

    def retire(identifier):
        group = groups[identifier]
        assert group.live
        group.live = False
        del cores[group.core].groups[group.target]
        candidate = boundary[group.target]
        del candidate.groups[group.core]
        candidate.lower -= group.lower
        counts["group_retirements"] += 1

    def add_group(c, j, a, b, k=1, lower=F(0), parents=(), endpoint=None):
        candidate = ensure(j)
        old = candidate.groups.get(c)
        if old is not None:
            previous = groups[old]
            a += previous.slope
            b += previous.intercept
            k += previous.incidences
            lower += previous.lower
            parents = (*parents, old)
            retire(old)
            counts["group_coalescences"] += 1
        assert a > 0 and b <= 0 and k > 0
        group = Group(c, j, a, b, k, lower)
        identifier = len(groups)
        groups.append(group)
        candidate.groups[c] = identifier
        cores[c].groups[j] = identifier
        candidate.lower += lower
        threshold = (ratio * lower + k * floor - b) / a
        heapq.heappush(cores[c].heap, (threshold, identifier))
        counts["group_creations"] += 1
        counts["heap_pushes"] += 1
        if audit:
            audit.new_group(identifier, parents, endpoint, j)

    def new_edges(label):
        for other in oracle.row(label):
            counts["original_edge_checks"] += 1
            edge = tuple(sorted((label, other)))
            if edge in seen_edges:
                continue
            seen_edges.add(edge)
            assert other not in active
            yield other

    def peel():
        while peeling:
            i = peeling.popleft()
            counts["peeling_eligibility_checks"] += 1
            if i == seed or i not in cores:
                continue
            row = cores[i]
            if len(row.edges) + len(row.groups) > 2:
                continue
            assert 1 <= len(row.edges) <= 2 and len(row.groups) <= 1
            delta, load = row.diagonal, row.load
            assert delta > 0 and load < 0
            neighbors = tuple(row.edges.items())
            outside = tuple((j, groups[g].slope) for j, g in row.groups.items())
            records.append((i, delta, load, neighbors, outside))
            counts["reverse_records_stored"] += 1
            for c, w in neighbors:
                target = cores[c]
                del target.edges[i]
                target.diagonal -= w * w / delta
                target.load += w * load / delta
                peeling.append(c)
                counts["reduced_core_scalar_updates"] += 2
                counts["reduced_edge_deletions"] += 1
            if len(neighbors) == 2:
                (c, wc), (d, wd) = neighbors
                value = wc * wd / delta
                cores[c].edges[d] = cores[c].edges.get(d, F(0)) + value
                cores[d].edges[c] = cores[d].edges.get(c, F(0)) + value
                counts["reduced_edge_additions"] += 2
            if row.groups:
                assert len(neighbors) == 1
                j, identifier = next(iter(row.groups.items()))
                group = groups[identifier]
                old_lower = boundary[j].lower
                a, b, k, lower = group.slope, group.intercept, group.incidences, group.lower
                retire(identifier)
                boundary[j].diagonal -= a * a / delta
                c, w = neighbors[0]
                add_group(c, j, a * w / delta, b + a * load / delta, k, lower, (identifier,))
                assert boundary[j].lower == old_lower
                counts["moved_flux_groups"] += 1
                counts["boundary_diagonal_updates"] += 1
            for c in cores:
                if c != i:
                    del inverse[c][i]
                    counts["inverse_entry_deletions"] += 1
            counts["inverse_entry_deletions"] += len(inverse[i])
            del inverse[i]
            counts["discarded_heap_entries"] += len(row.heap)
            del cores[i]
            counts["core_removals"] += 1

    for j in new_edges(seed):
        add_group(seed, j, gamma, F(0), endpoint=seed)
    while True:
        counts["event_rounds"] += 1
        for row in cores.values():
            counts["core_queue_visits"] += 1
            while row.heap:
                counts["heap_top_checks"] += 1
                threshold, identifier = row.heap[0]
                group = groups[identifier]
                if not group.live:
                    heapq.heappop(row.heap)
                    counts["heap_pops"] += 1
                    counts["stale_heap_pops"] += 1
                    continue
                if row.value <= threshold:
                    break
                heapq.heappop(row.heap)
                counts["heap_pops"] += 1
                flux = group.slope * row.value + group.intercept
                assert flux > ratio * group.lower + group.incidences * floor
                candidate = boundary[group.target]
                candidate.lower += flux - group.lower
                group.lower = flux
                group.publications += 1
                counts["publications"] += 1
                if candidate.lower > gate * candidate.degree and not candidate.queued:
                    candidate.queued = True
                    ready.append(group.target)
                    counts["ready_pushes"] += 1
                threshold = (
                    ratio * flux + group.incidences * floor - group.intercept
                ) / group.slope
                heapq.heappush(row.heap, (threshold, identifier))
                counts["heap_pushes"] += 1
        if audit:
            audit.check(active, cores, inverse, boundary, groups, records)
        if not ready:
            counts["quiet_certificates"] += 1
            break
        label = ready.popleft() if policy == "fifo" else ready.pop()
        counts["ready_pops"] += 1
        candidate = boundary[label]
        assert candidate.lower > gate * candidate.degree
        coupling, load = {}, -lam * candidate.degree
        for c, identifier in tuple(candidate.groups.items()):
            group = groups[identifier]
            coupling[c] = group.slope
            load += group.intercept
            retire(identifier)
            counts["admitted_group_reads"] += 1
        del boundary[label]
        surplus = load + sum(w * cores[c].value for c, w in coupling.items())
        response = {c: sum(inverse[c][d] * w for d, w in coupling.items()) for c in cores}
        pivot = candidate.diagonal - sum(w * response[c] for c, w in coupling.items())
        assert surplus > 0 and pivot > 0
        value = surplus / pivot
        counts["inverse_vector_terms"] += len(cores) * len(coupling)
        for c in cores:
            cores[c].value += response[c] * value
            counts["core_value_updates"] += 1
            for d in cores:
                inverse[c][d] += response[c] * response[d] / pivot
                counts["inverse_entry_updates"] += 1
            inverse[c][label] = response[c] / pivot
        inverse[label] = {c: response[c] / pivot for c in cores}
        inverse[label][label] = 1 / pivot
        counts["inverse_entry_allocations"] += 2 * len(cores) + 1
        cores[label] = Core(candidate.diagonal, load, value, edges=coupling)
        for c, w in coupling.items():
            cores[c].edges[label] = w
            counts["reduced_edge_additions"] += 2
        active.add(label)
        counts["admissions"] += 1
        counts["core_births"] += 1
        counts["peak_core_size"] = max(counts["peak_core_size"], len(cores))
        for j in new_edges(label):
            add_group(label, j, gamma, F(0), endpoint=label)
        peeling.append(label)
        peel()
    answer = {i: row.value for i, row in cores.items()}
    for i, diagonal, load, neighbors, outside in reversed(records):
        assert i not in answer
        answer[i] = (
            load
            + sum(w * answer[j] for j, w in neighbors)
            + sum(w * answer.get(j, F(0)) for j, w in outside)
        ) / diagonal
        assert answer[i] > 0
        counts["reverse_records_read"] += 1
    counts["output_words"] += len(answer)
    counts["final_core_size"] = len(cores)
    counts["maximum_group_incidences"] = max((g.incidences for g in groups), default=0)
    counts["maximum_group_publications"] = max((g.publications for g in groups), default=0)
    return answer, dict(counts)


class TraceAudit:
    """Expensive independent physical-membership and full-face checks, audit-only."""

    def __init__(self, graph, seed, alpha, epsilon, counts):
        self.graph, self.seed, self.alpha, self.epsilon = graph, seed, alpha, epsilon
        self.counts, self.members, self.previous = counts, {}, {}

    def new_group(self, identifier, parents, endpoint, target):
        members = set()
        if endpoint is not None:
            members.add((endpoint, target))
        for parent in parents:
            assert members.isdisjoint(self.members[parent])
            members.update(self.members[parent])
            self.counts["membership_copies"] += len(self.members[parent])
        self.members[identifier] = members

    def check(self, active, cores, inverse, boundary, groups, records):
        graph = self.graph
        gamma = (1 - self.alpha) / (1 + self.alpha)
        exact = face_reference(graph, self.seed, self.alpha, self.epsilon, active)
        assert all(exact[i] > 0 and exact[i] >= self.previous.get(i, F(0)) for i in exact)
        assert all(exact[i] == row.value for i, row in cores.items())
        assert all(
            i == self.seed or len(row.edges) + len(row.groups) > 2 for i, row in cores.items()
        )
        for i, row in cores.items():
            assert row.diagonal > 0
            assert (
                row.diagonal * row.value - sum(w * cores[j].value for j, w in row.edges.items())
                == row.load
            )
            assert all(cores[j].edges[i] == w > 0 for j, w in row.edges.items())
            self.counts["reduced_core_equation_checks"] += 1
        labels = sorted(active)
        matrix = [
            [
                F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0)
                for j in labels
            ]
            for i in labels
        ]
        for c in cores:
            column = dict(zip(labels, solve(matrix, [F(int(i == c)) for i in labels])))
            assert all(inverse[d][c] == column[d] for d in cores)
            self.counts["inverse_entry_checks"] += len(cores)
        partition = set()
        for identifier, group in enumerate(groups):
            if not group.live:
                continue
            members = self.members[identifier]
            assert len(members) == group.incidences and partition.isdisjoint(members)
            partition.update(members)
            assert all(j == group.target and i in active for i, j in members)
            flux = gamma * sum(exact[i] for i, _ in members)
            assert flux == group.slope * cores[group.core].value + group.intercept
            assert group.lower <= flux <= 5 * group.lower / 4 + group.incidences * self.epsilon / 16
            self.counts["physical_group_checks"] += 1
        assert partition == {(i, j) for i in active for j in graph[i] if j not in active}
        for j, candidate in boundary.items():
            assert candidate.lower == sum(groups[k].lower for k in candidate.groups.values())
            self.counts["shared_gate_checks"] += 1
        recovered = {i: row.value for i, row in cores.items()}
        for i, delta, load, neighbors, outside in reversed(records):
            assert i not in recovered
            recovered[i] = (
                load
                + sum(w * recovered[j] for j, w in neighbors)
                + sum(w * recovered.get(j, F(0)) for j, w in outside)
            ) / delta
        assert recovered == exact
        self.previous = exact
        self.counts["full_trace_faces"] += 1


def grouped_parallel_report(n):
    graph = nx.Graph([(0, 1)])
    graph.add_node(2)
    for i in range(n):
        previous = 1
        for _ in range(1 + i % 2):
            label = len(graph)
            graph.add_edge(previous, label)
            previous = label
        graph.add_edge(previous, 2)
    for _ in range(10 * n * n):
        graph.add_edge(2, len(graph))
    return graph


def comb(n, length, cyclic=False):
    graph = nx.cycle_graph(n) if cyclic else nx.path_graph(n)
    for i in range(n):
        previous = i
        for _ in range(length + (i % 3 == 0)):
            label = len(graph)
            graph.add_edge(previous, label)
            previous = label
    return graph


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--trace-max-n", type=int, default=4)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.time()
    cases, totals, traces, rows = 0, Counter(), Counter(), []
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
                for policy in ["fifo", "lifo"]:
                    oracle = LocalOracle(graph)
                    audit = (
                        TraceAudit(graph, seed, alpha, epsilon, traces)
                        if len(graph) <= args.trace_max_n
                        else None
                    )
                    answer, info = local_peeling(oracle, seed, alpha, epsilon, audit, policy)
                    check_acl(graph, seed, alpha, epsilon, answer)
                    assert answer == face_reference(graph, seed, alpha, epsilon, answer)
                    optimum = exact_reference(graph, seed, alpha, epsilon / 2)
                    assert all(0 < x <= optimum[i] for i, x in answer.items())
                    assert set(oracle.rows) == set(answer)
                    for k, v in info.items():
                        if k.startswith(("maximum_", "peak_")):
                            totals[k] = max(totals[k], v)
                        else:
                            totals[k] += v
                    totals.update(oracle.counts)
                    cases += 1
    if args.structured:
        instances = [
            *[
                (subdivided_core(r, 8), "subdivided_core", {"r": r}, F(1, 1000003), F(1, 1000003))
                for r in [4, 8, 16]
            ],
            *[
                (
                    mixed_quiet_reports(r, n),
                    "shared_quiet_reports",
                    {"r": r, "reports": n},
                    F(1, 3),
                    F(1, 1000 * r * n),
                )
                for r, n in [(4, 4), (8, 8), (16, 8)]
            ],
            *[cancellation_case(length) for length in [64, 128, 256]],
            *[
                (
                    nx.balanced_tree(2, h),
                    "balanced_tree",
                    {"height": h},
                    F(1, 1009),
                    F(1, 10090 * 6**h),
                )
                for h in [3, 4, 5, 6]
            ],
            *[
                (
                    grouped_parallel_report(n),
                    "grouped_parallel_report",
                    {"paths": n},
                    F(1, 3),
                    F(1, 50 * n * n),
                )
                for n in [4, 8, 32, 64]
            ],
            *[
                (
                    comb(n, length, cyclic),
                    "asymmetric_comb",
                    {"centers": n, "branch_length": length, "cyclic": cyclic},
                    F(1, 1009),
                    F(1, 10000),
                )
                for n in [32, 128]
                for length in [1, 2]
                for cyclic in [False, True]
            ],
        ]
        for graph, family, metadata, alpha, epsilon in instances:
            for policy in ["fifo", "lifo"]:
                seed = metadata.get("seed", 0)
                oracle = LocalOracle(graph)
                extra_audit = (
                    TraceAudit(graph, seed, alpha, epsilon, traces)
                    if family == "grouped_parallel_report" and metadata["paths"] <= 8
                    else None
                )
                answer, info = local_peeling(
                    oracle, seed, alpha, epsilon, audit=extra_audit, policy=policy
                )
                check_acl(graph, seed, alpha, epsilon, answer)
                assert set(oracle.rows) == set(answer)
                rows.append(
                    {
                        "family": family,
                        **metadata,
                        "policy": policy,
                        "ambient_vertices": len(graph),
                        "positive_vertices": len(answer),
                        "support_volume": sum(graph.degree(i) for i in answer),
                        "alpha_lazy": str(alpha),
                        "eps_appr": str(epsilon),
                        "counts": info,
                        "oracle_counts": dict(oracle.counts),
                    }
                )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.live_core_peeling",
        "arithmetic": "exact fractions",
        "max_n": args.max_n,
        "trace_max_n": args.trace_max_n,
        "exact_comparisons": cases,
        "parameters_alpha_epsilon": [[str(a), str(e)] for a, e in parameters],
        "lambda": "eps_appr/2",
        "seed": "every atlas vertex; structured metadata seed, default 0",
        "random_seed": None,
        "policies": ["fifo", "lifo"],
        "stopping_rule": "all grouped flux queues settled; no lower gate > 11 eps d / 20",
        "counts": dict(totals),
        "audit_only_trace_counts": dict(traces),
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
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
