"""Check APPR work on the star, path, and spider constructions.

The star (equivalently, a depth-one spider) is the proved hard instance. Paths
and longer spiders are diagnostics only; the manuscript makes no matching
lower-bound claim for them.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import scipy.sparse as sp

from src.baselines.appr import APPR_ORDERINGS, approximate_pagerank
from src.graphs import GraphData

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STOPPING_RULE = "terminate when r[u] < eps_appr * d[u] for every vertex u"


def graph_from_edges(name: str, node_count: int, edges: list[tuple[int, int]]) -> GraphData:
    first = np.fromiter((u for u, _ in edges), dtype=int)
    second = np.fromiter((v for _, v in edges), dtype=int)
    rows = np.concatenate((first, second))
    columns = np.concatenate((second, first))
    adjacency = sp.csr_matrix(
        (np.ones(len(rows)), (rows, columns)),
        shape=(node_count, node_count),
    )
    degree = np.asarray(adjacency.sum(axis=1)).ravel()
    return GraphData(name=name, adjacency=adjacency, degree=degree)


def star_graph(leaf_count: int) -> GraphData:
    return graph_from_edges(
        f"star-{leaf_count}",
        leaf_count + 1,
        [(0, leaf) for leaf in range(1, leaf_count + 1)],
    )


def path_graph(node_count: int) -> GraphData:
    return graph_from_edges(
        f"path-{node_count}",
        node_count,
        [(u, u + 1) for u in range(node_count - 1)],
    )


def spider_graph(arm_count: int, arm_length: int) -> GraphData:
    edges = []
    for arm in range(arm_count):
        previous = 0
        for depth in range(arm_length):
            node = 1 + arm * arm_length + depth
            edges.append((previous, node))
            previous = node
    return graph_from_edges(
        f"spider-{arm_count}x{arm_length}",
        1 + arm_count * arm_length,
        edges,
    )


def code_version() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return "unknown"
    version = completed.stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if status.returncode == 0 and status.stdout:
        version += "-dirty"
    return version


def run_checks(
    alphas: list[float],
    eps_values: list[float],
    orderings: list[str],
    *,
    random_seed: int,
    spider_length: int,
    graph_kinds: tuple[str, ...] = ("star", "path", "spider"),
) -> list[dict[str, object]]:
    records = []
    version = code_version()
    for eps_appr in eps_values:
        leaf_count = math.floor(1.0 / (8.0 * eps_appr))
        cases = [
            ("star", star_graph(leaf_count), 0, True),
            ("path", path_graph(2 * leaf_count + 1), leaf_count, False),
            (
                "spider",
                spider_graph(leaf_count, spider_length),
                0,
                spider_length == 1,
            ),
        ]
        for alpha in alphas:
            for graph_kind, graph, source, lower_bound_applies in cases:
                if graph_kind not in graph_kinds:
                    continue
                for ordering in orderings:
                    result = approximate_pagerank(
                        graph,
                        source,
                        alpha=alpha,
                        eps_appr=eps_appr,
                        ordering=ordering,
                        random_seed=random_seed,
                    )
                    lower_bound = 3.0 / (128.0 * alpha * eps_appr)
                    upper_bound = 1.0 / (alpha * eps_appr)
                    work = float(result.work)
                    records.append(
                        {
                            "graph": graph.name,
                            "graph_kind": graph_kind,
                            "nodes": graph.n,
                            "edges": graph.m,
                            "source": source,
                            "alpha": alpha,
                            "eps_appr": eps_appr,
                            "random_seed": random_seed,
                            "ordering": ordering,
                            "stopping_rule": STOPPING_RULE,
                            "max_pushes": None,
                            "code_version": version,
                            "pushes": int(result.pushes),
                            "work": work,
                            "scaled_work": float(alpha * eps_appr * work),
                            "upper_bound": upper_bound,
                            "upper_bound_verified": bool(work <= upper_bound),
                            "star_lower_bound": lower_bound,
                            "lower_bound_applies": lower_bound_applies,
                            "lower_bound_verified": (
                                bool(work > lower_bound) if lower_bound_applies else None
                            ),
                        }
                    )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alphas", default="1,0.5,0.1")
    parser.add_argument("--eps", default="0.0625,0.03125,0.015625")
    parser.add_argument("--orderings", default=",".join(APPR_ORDERINGS))
    parser.add_argument("--random-seed", type=int, default=17)
    parser.add_argument("--spider-length", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    alphas = [float(value) for value in args.alphas.split(",")]
    eps_values = [float(value) for value in args.eps.split(",")]
    orderings = [value for value in args.orderings.split(",") if value]
    if args.spider_length < 1:
        parser.error("--spider-length must be positive")
    unknown = set(orderings).difference(APPR_ORDERINGS)
    if unknown:
        parser.error(f"unknown orderings: {', '.join(sorted(unknown))}")

    records = run_checks(
        alphas,
        eps_values,
        orderings,
        random_seed=args.random_seed,
        spider_length=args.spider_length,
    )
    payload = json.dumps(records, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")

    proved = [record for record in records if record["lower_bound_applies"]]
    diagnostics = [record for record in records if not record["lower_bound_applies"]]
    print(
        f"verified star lower bound in {sum(r['lower_bound_verified'] for r in proved)}"
        f"/{len(proved)} runs; verified APPR upper bound in "
        f"{sum(r['upper_bound_verified'] for r in records)}/{len(records)} runs"
    )
    print("graph            alpha   eps_appr ordering     work alpha*eps*work lower-bound")
    for record in records:
        if not record["lower_bound_applies"]:
            lower_status = "n/a"
        elif record["lower_bound_verified"]:
            lower_status = "pass"
        else:
            lower_status = "FAIL"
        print(
            f"{record['graph']:<16} {record['alpha']:>5g} {record['eps_appr']:>10g} "
            f"{record['ordering']:<10} {record['work']:>8.0f} "
            f"{record['scaled_work']:>14.6f} {lower_status:>11}"
        )
    if diagnostics:
        print("path and long-spider rows are diagnostics; no star lower bound is asserted for them")


if __name__ == "__main__":
    main()
