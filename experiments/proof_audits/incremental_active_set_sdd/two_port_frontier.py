"""Local exact obstacle elimination with at most two retained branch vertices.

Keep the seed and the first admitted nonseed vertex of degree >=3. Every
other admitted vertex has degree <=2 and is eliminated immediately. Stable
frontier inequalities become points queried by a dynamic planar upper hull.
Stop with PortLimit before admitting a second nonseed branching vertex.
No inactive adjacency row or ambient graph size is supplied to the solver.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

from bounded_attachment_cycle import LocalOracle, exact_reference
from dynamic_upper_hull import DynamicUpperHull
from local_sun_solver import check_solution
import networkx as nx


class PortLimit(Exception):
    pass


@dataclass
class FrontierRow:
    diagonal: F
    load: F
    coupling: list = field(default_factory=lambda: [F(0), F(0)])


def local_two_port(oracle, seed, alpha, lam):
    gamma = (1 - alpha) / (1 + alpha)
    assert 0 < gamma < 1 and lam > 0
    degree = oracle.degree(seed)
    if lam * degree >= 1:
        return {}, {"admissions": 0, "cores": [], "hull_counts": {}}
    core = {seed: 0}
    active = {seed}
    boundary = {}
    seen_edges = set()
    records = []
    hull = DynamicUpperHull()
    matrix = [[F(degree), F(0)], [F(0), F(1)]]
    load = [1 - lam * degree, F(0)]
    counts = Counter(admissions=1)

    def ensure(label):
        counts["frontier_record_accesses"] += 1
        if label not in boundary:
            d = oracle.degree(label)
            boundary[label] = FrontierRow(F(d), -lam * d)
            counts["frontier_exposures"] += 1
            counts["maximum_frontier_records"] = max(
                counts["maximum_frontier_records"], len(boundary)
            )
        return boundary[label]

    def publish(label):
        row = boundary[label]
        assert row.diagonal > 0 and row.load < 0 and min(row.coupling) >= 0
        hull.set(label, tuple(a / -row.load for a in row.coupling))
        counts["individual_frontier_rekeys"] += 1

    def new_edges(label):
        for other in oracle.row(label):
            counts["original_edge_dictionary_checks"] += 1
            edge = tuple(sorted((label, other)))
            if edge in seen_edges:
                continue
            seen_edges.add(edge)
            assert other not in active
            yield other

    def expose_core(label):
        slot = core[label]
        for other in new_edges(label):
            row = ensure(other)
            row.coupling[slot] += gamma
            publish(other)

    expose_core(seed)
    previous = [F(0), F(0)]
    while True:
        counts["core_solves"] += 1
        if len(core) == 1:
            values = [load[0] / matrix[0][0], F(0)]
        else:
            determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2
            assert determinant > 0
            values = [
                (load[0] * matrix[1][1] - matrix[0][1] * load[1]) / determinant,
                (load[1] * matrix[0][0] - matrix[0][1] * load[0]) / determinant,
            ]
        assert all(x >= y for x, y in zip(values, previous))
        previous = values
        found = hull.extreme(values)
        if found is None or found[1] <= 1:
            counts["quiet_certificates"] += 1
            break
        label = found[0]
        row = boundary[label]
        assert row.load + sum(a * x for a, x in zip(row.coupling, values)) > 0
        d = oracle.degree(label)
        if d >= 3 and len(core) == 2:
            raise PortLimit((label, tuple(core), dict(counts)))
        del boundary[label]
        hull.delete(label)
        active.add(label)
        counts["admissions"] += 1
        if d >= 3:
            assert row.coupling[1] == 0
            core[label] = 1
            matrix[1][1] = row.diagonal
            matrix[0][1] = matrix[1][0] = -row.coupling[0]
            load[1] = row.load
            expose_core(label)
            continue
        successors = list(new_edges(label))
        assert len(successors) <= 1
        diagonal, b, coupling = row.diagonal, row.load, tuple(row.coupling)
        for i in range(2):
            load[i] += coupling[i] * b / diagonal
            for j in range(2):
                matrix[i][j] -= coupling[i] * coupling[j] / diagonal
                counts["core_schur_entries"] += 1
        for other in successors:
            successor = ensure(other)
            successor.diagonal -= gamma * gamma / diagonal
            successor.load += gamma * b / diagonal
            for i in range(2):
                successor.coupling[i] += gamma * coupling[i] / diagonal
            publish(other)
        records.append((label, diagonal, b, coupling, successors))
        counts["reverse_records_stored"] += 1
    answer = {label: values[slot] for label, slot in core.items()}
    for label, diagonal, b, coupling, successors in reversed(records):
        answer[label] = (
            b
            + sum(a * x for a, x in zip(coupling, values))
            + gamma * sum(answer.get(other, F(0)) for other in successors)
        ) / diagonal
        assert answer[label] > 0
        counts["reverse_records_read"] += 1
    counts["output_words"] += len(answer)
    counts["final_boundary_records"] = len(boundary)
    return answer, {**dict(counts), "cores": list(core), "hull_counts": dict(hull.counts)}


def unequal_bundle(lengths):
    graph = nx.Graph()
    graph.add_nodes_from([0, 1])
    for length in lengths:
        previous = 0
        for _ in range(length - 1):
            label = len(graph)
            graph.add_edge(previous, label)
            previous = label
        graph.add_edge(previous, 1)
    return graph


def inactive_descendant(q):
    graph = nx.cycle_graph(7)
    graph.add_edges_from([(3, 7), (7, 8), (8, 9)])
    graph.add_edges_from((9, i) for i in range(10, q + 9))
    return graph


def shared_quiet_reports(n):
    graph = nx.Graph([(0, 1)])
    for i in range(n):
        report = len(graph)
        graph.add_node(report)
        for core in [0, 1]:
            previous = core
            for _ in range(1 + (i + core) % 2):
                relay = len(graph)
                graph.add_edge(previous, relay)
                previous = relay
            graph.add_edge(previous, report)
        for _ in range(64 * n + i):
            graph.add_edge(report, len(graph))
    return graph


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.time()
    cases = skipped = 0
    totals = Counter()
    rows = []
    parameters = [
        (F(1, 3), F(1, 10)),
        (F(1, 1009), F(1, 1009)),
        (F(1, 7), F(1, 100)),
        (F(1, 1000003), F(1, 1000003)),
    ]
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha, lam in parameters:
                expected = {i: x for i, x in exact_reference(graph, seed, alpha, lam).items() if x}
                eligible = sum(graph.degree(i) >= 3 for i in expected if i != seed) <= 1
                oracle = LocalOracle(graph)
                try:
                    answer, info = local_two_port(oracle, seed, alpha, lam)
                except PortLimit:
                    assert not eligible
                    skipped += 1
                    continue
                assert eligible and answer == expected
                check_solution(graph, seed, alpha, lam, answer)
                assert set(oracle.rows) == set(answer)
                cases += 1
                totals.update(oracle.counts)
                totals.update(info["hull_counts"])
    if args.structured:
        for graph, family, metadata in [
            *[
                (shared_quiet_reports(n), "shared_quiet_reports", {"reports": n})
                for n in [4, 16, 32]
            ],
            *[(inactive_descendant(q), "inactive_descendant", {"q": q}) for q in [64, 256, 1024]],
            *[
                (
                    unequal_bundle([2 + (i * i + 3 * i) % 17 for i in range(n)]),
                    "unequal_path_bundle",
                    {"paths": n},
                )
                for n in [8, 32, 128]
            ],
        ]:
            alpha, lam = (
                (F(1, 3), F(1, 1000))
                if family == "inactive_descendant"
                else (F(1, 1009), F(1, 10000))
            )
            if family == "shared_quiet_reports":
                alpha, lam = F(1, 3), F(1, 100 * metadata["reports"] ** 2)
            oracle = LocalOracle(graph)
            answer, info = local_two_port(oracle, 0, alpha, lam)
            check_solution(graph, 0, alpha, lam, answer)
            assert set(oracle.rows) == set(answer)
            assert sum(graph.degree(i) for i in answer) <= 1 / lam
            rows.append(
                {
                    "family": family,
                    **metadata,
                    "ambient_vertices": len(graph),
                    "alpha_lazy": str(alpha),
                    "lambda": str(lam),
                    "support_vertices": len(answer),
                    "support_volume": sum(graph.degree(i) for i in answer),
                    "counts": dict(oracle.counts),
                    "info": info,
                }
            )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.two_port_frontier",
        "arithmetic": "exact fractions; actual persistent AVL upper-hull backend",
        "max_n": args.max_n,
        "exact_reference_comparisons": cases,
        "correctly_detected_port_limit": skipped,
        "parameters": [[str(a), str(lam)] for a, lam in parameters],
        "seed": "every vertex on atlas; vertex 0 on structured cases",
        "random_seed": None,
        "stopping_rule": "strict positive boundary surplus; extreme maximum <= 1 certifies KKT",
        "counts": dict(totals),
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
        "hull_sha256": hashlib.sha256(
            Path(__file__).with_name("dynamic_upper_hull.py").read_bytes()
        ).hexdigest(),
        "elapsed_seconds_including_reference": round(time.time() - started, 3),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
