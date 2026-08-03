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

from src.baselines.appr import APPR_ORDERINGS, approximate_pagerank
from src.synthetic_graphs import path_graph, spider_graph, star_graph

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STOPPING_RULE = "terminate when r[u] < eps_appr * d[u] for every vertex u"
APPR_LOWER_BOUND_MAX_EPS = 1.0 / 16.0
GRAPH_KINDS = ("star", "path", "spider")


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
    _validate_check_parameters(alphas, eps_values, orderings, spider_length, graph_kinds)
    records = []
    version = code_version()
    for eps_appr in eps_values:
        leaf_count = math.floor(1.0 / (8.0 * eps_appr))
        cases = [_build_case(graph_kind, leaf_count, spider_length) for graph_kind in graph_kinds]
        for alpha in alphas:
            for graph_kind, graph, source, lower_bound_applies in cases:
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


def _validate_check_parameters(
    alphas: list[float],
    eps_values: list[float],
    orderings: list[str],
    spider_length: int,
    graph_kinds: tuple[str, ...],
) -> None:
    if not alphas:
        raise ValueError("at least one alpha value is required")
    if not eps_values:
        raise ValueError("at least one eps_appr value is required")
    if not orderings:
        raise ValueError("at least one ordering is required")
    if not graph_kinds:
        raise ValueError("at least one graph kind is required")
    if spider_length < 1:
        raise ValueError(f"spider_length must be positive, got {spider_length}")

    invalid_alphas = [alpha for alpha in alphas if not math.isfinite(alpha) or not 0 < alpha <= 1]
    if invalid_alphas:
        raise ValueError(f"alpha values must lie in (0, 1], got {invalid_alphas}")
    invalid_eps = [
        eps_appr
        for eps_appr in eps_values
        if not math.isfinite(eps_appr) or not 0 < eps_appr <= APPR_LOWER_BOUND_MAX_EPS
    ]
    if invalid_eps:
        raise ValueError(
            f"eps_appr values must lie in the proved regime (0, 1/16], got {invalid_eps}"
        )

    unknown_orderings = set(orderings).difference(APPR_ORDERINGS)
    if unknown_orderings:
        raise ValueError(f"unknown orderings: {', '.join(sorted(unknown_orderings))}")
    unknown_graph_kinds = set(graph_kinds).difference(GRAPH_KINDS)
    if unknown_graph_kinds:
        raise ValueError(f"unknown graph kinds: {', '.join(sorted(unknown_graph_kinds))}")
    if len(set(graph_kinds)) != len(graph_kinds):
        raise ValueError("graph_kinds must not contain duplicates")


def _build_case(graph_kind: str, leaf_count: int, spider_length: int):
    if graph_kind == "star":
        return "star", star_graph(leaf_count), 0, True
    if graph_kind == "path":
        return "path", path_graph(2 * leaf_count + 1), leaf_count, False
    if graph_kind == "spider":
        return (
            "spider",
            spider_graph(leaf_count, spider_length),
            0,
            spider_length == 1,
        )
    raise AssertionError(f"validated graph kind unexpectedly missing: {graph_kind}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alphas", default="1,0.5,0.1")
    parser.add_argument("--eps", default="0.0625,0.03125,0.015625")
    parser.add_argument("--orderings", default=",".join(APPR_ORDERINGS))
    parser.add_argument("--random-seed", type=int, default=17)
    parser.add_argument("--spider-length", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        alphas = [float(value) for value in args.alphas.split(",") if value]
        eps_values = [float(value) for value in args.eps.split(",") if value]
        orderings = [value for value in args.orderings.split(",") if value]
        records = run_checks(
            alphas,
            eps_values,
            orderings,
            random_seed=args.random_seed,
            spider_length=args.spider_length,
        )
    except ValueError as error:
        parser.error(str(error))
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
