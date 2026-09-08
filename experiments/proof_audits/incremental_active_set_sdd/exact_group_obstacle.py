"""Exact physical obstacle groups and dyadic canonical RPPR materialization.

The default ACL backend is unchanged. Dense obstacle and rational objective
interval calculations are validators, never numerical producer callbacks.
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
from frontier_exact import audit_map
from frontier_groups import GroupFrontier, prefix_validator
from frontier_neighborhood_types import blow_up, type_validator
from geometric_value_events import mv, obstacle
from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub
import networkx as nx


class ExactGroupObstacle(GroupFrontier):
    def __init__(self, oracle, seed, alpha, lam, work):
        assert 0 < lam < F(1, 2)
        super().__init__(oracle, seed, alpha, 2 * lam, work)
        # The base initializer has performed no eligibility query or pivot.
        self.kappa = F(0)
        work["exact_obstacle_zero_gate_initialization"] += 2


def exact_physical(oracle, seed, alpha, lam, work, validator=None, lift_validator=None):
    assert 0 < alpha <= 1 and lam > 0
    bar = 2 * alpha / (1 + alpha)
    work["exact_obstacle_dispatch_and_parameter_operations"] += 8
    if lam >= F(1, 2):
        degree = oracle.degree(seed)
        assert degree >= 1
        value = max(F(0), F(1, degree) - lam)
        assert not value or degree == 1
        work["exact_obstacle_high_penalty_degree_gate_and_output_words"] += 24
        return {
            "physical": [(seed, value)] if value else [],
            "probabilities": [(seed, bar * degree * value)] if value else [],
            "canonical_factors": [(seed, bar * value, degree)] if value else [],
            "volume": degree if value else 0,
        }, None
    state = ExactGroupObstacle(oracle, seed, alpha, lam, work)
    raw = state.run(validator, lift_validator)
    factors = [(p.vertex.label, state.bar * p.vertex.value, p.vertex.degree) for p in state.history]
    work["exact_obstacle_factored_canonical_records_and_scalar_products"] += 5 + 6 * len(factors)
    return {
        "physical": raw["records"],
        "probabilities": raw["probabilities"],
        "canonical_factors": factors,
        "volume": raw["volume"],
    }, state


def scaled_root_interval(degree, squared_mass, tolerance, work):
    """Arithmetic-only bisection; no logarithm or square-root primitive."""
    assert degree >= 1 and 0 <= squared_mass <= 1 and tolerance > 0
    lower, upper = F(0), F(1)
    work["canonical_root_interval_initialization"] += 4
    while upper - lower > tolerance:
        middle = (lower + upper) / 2
        if degree * middle * middle <= squared_mass:
            lower = middle
        else:
            upper = middle
        work["canonical_root_bisection_arithmetic_comparisons_and_temporaries"] += 13
        work["canonical_root_bisection_iterations"] += 1
    work["canonical_root_interval_final_comparison_and_return"] += 3
    return lower, upper


def inverse_root_interval(degree, tolerance, work):
    """Validator-only inverse-root enclosure, independent of the producer mass."""
    return scaled_root_interval(degree, F(1), tolerance, work)


def canonical_materialize(exact, epsilon_obj, work):
    assert epsilon_obj > 0
    delta = min(F(1), epsilon_obj)
    records, certificates = [], []
    work["canonical_output_headers_and_tolerance_operations"] += 8
    for (label, probability), (other, coefficient, degree) in zip(
        exact["probabilities"], exact["canonical_factors"]
    ):
        assert label == other and probability == degree * coefficient
        lower, upper = scaled_root_interval(degree, probability * probability, delta, work)
        if lower:
            records.append((label, lower))
        certificates.append((label, lower, upper, degree, probability))
        work["canonical_coordinate_mass_square_zero_filter_and_record_words"] += 15
    return {"records": records, "root_intervals": certificates, "delta": delta}


def canonical_objective_interval(graph, seed, alpha, lam, physical, canonical, epsilon_obj, counts):
    """Independent exact rational enclosure of the canonical objective gap."""
    x = dict(canonical["records"])
    u = dict(physical["physical"])
    gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
    energy = sum(graph.degree(i) * value * value for i, value in u.items())
    energy -= 2 * gamma * sum(u.get(i, F(0)) * u.get(j, F(0)) for i, j in graph.edges)
    optimum_objective = -alpha * bar * energy / 2
    linear = {i: alpha * value * (lam * graph.degree(i) - int(i == seed)) for i, value in x.items()}
    cross_size = (1 - alpha) * sum(x.get(i, F(0)) * x.get(j, F(0)) for i, j in graph.edges)
    slope_bound = sum(abs(value) for value in linear.values()) + cross_size
    tolerance = min(F(1), epsilon_obj) / (64 * (1 + slope_bound))
    intervals = {i: inverse_root_interval(graph.degree(i), tolerance, Counter()) for i in x}
    diagonal = (1 + alpha) * sum(value * value for value in x.values()) / 4
    lower = upper = diagonal
    for i, coefficient in linear.items():
        lo, hi = intervals[i]
        lower += coefficient * (lo if coefficient >= 0 else hi)
        upper += coefficient * (hi if coefficient >= 0 else lo)
    for i, j in graph.edges:
        coefficient = (1 - alpha) * x.get(i, F(0)) * x.get(j, F(0)) / 2
        if coefficient:
            li, hi = intervals[i]
            lj, hj = intervals[j]
            lower -= coefficient * hi * hj
            upper -= coefficient * li * lj
    assert lower <= upper and upper - optimum_objective <= epsilon_obj
    assert upper - lower <= tolerance * slope_bound
    counts["independent_rational_canonical_objective_gap_enclosures"] += 1
    return upper - optimum_objective


def check_case(graph, seed, alpha, lam, counts, aggregate, dense_prefixes=False, partition=None):
    work = Counter()
    oracle = LocalRows(graph, work)
    forward = backward = None
    if lam < F(1, 2) and dense_prefixes:
        forward, backward = prefix_validator(graph, seed, alpha, 2 * lam, counts)
    if lam < F(1, 2) and partition is not None:
        forward = type_validator(graph, partition, counts, forward)
    exact, state = exact_physical(oracle, seed, alpha, lam, work, forward, backward)
    u = dict(exact["physical"])
    labels = sorted(graph)
    gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if graph.has_edge(i, j) else F(0) for j in labels]
        for i in labels
    ]
    load = [F(int(i == seed)) - lam * graph.degree(i) for i in labels]
    reference = obstacle(matrix, load)
    assert [u.get(i, F(0)) for i in labels] == reference
    applied = mv(matrix, reference)
    for i, value, action in zip(labels, reference, applied):
        residual = F(int(i == seed)) - action
        assert 0 <= residual <= lam * graph.degree(i)
        assert not value or residual == lam * graph.degree(i)
    assert sum(p for _, p in exact["probabilities"]) <= 1
    assert all(p == bar * graph.degree(i) * u[i] for i, p in exact["probabilities"])
    assert all(
        c == bar * u[i] and degree == graph.degree(i) for i, c, degree in exact["canonical_factors"]
    )
    assert exact["volume"] < 1 / lam
    assert len(oracle.row_log) == len(set(oracle.row_log))
    assert len(oracle.degree_log) == len(set(oracle.degree_log))
    if lam >= F(1, 2):
        assert oracle.row_log == [] and oracle.degree_log == [seed]
        counts["high_penalty_degree_only_cases"] += 1
    else:
        assert state is not None
        counts["terminal_exact_zero_obstacle_gate_ties"] += sum(
            vertex.group.q == lam * vertex.degree
            for _, vertex in audit_map(state.vertices)
            if not vertex.eliminated
        )
        counts["implemented_exact_positive_pivots"] += len(state.history)
        if partition is not None:
            assert state.metrics["maximum_transient_response_groups"] <= 2 * len(partition) + 1
    counts["independent_exact_original_obstacle_outputs"] += 1
    counts["original_exact_KKT_rows"] += len(graph)
    for epsilon_obj in [F(2), F(1, 8), F(1, 2**20)]:
        canonical = canonical_materialize(exact, epsilon_obj, work)
        x = dict(canonical["records"])
        assert set(x) <= set(u) and all(value > 0 for value in x.values())
        for i, lo, hi, degree, probability in canonical["root_intervals"]:
            assert 0 <= lo <= hi <= 1
            assert degree * lo * lo <= probability * probability <= degree * hi * hi
            assert hi - lo <= canonical["delta"]
            assert lo.denominator & (lo.denominator - 1) == 0
            assert lo.denominator < 2 / canonical["delta"]
            assert x.get(i, F(0)) == lo
            counts["dyadic_canonical_precision_and_root_certificates"] += 1
        canonical_objective_interval(graph, seed, alpha, lam, exact, canonical, epsilon_obj, counts)
        counts["materialized_dyadic_canonical_RPPR_outputs"] += 1
    aggregate.update(work)
    return {
        "vertices": len(graph),
        "seed": seed,
        "alpha": str(alpha),
        "lambda_rho": str(lam),
        "original_support_volume": exact["volume"],
        "positive_coordinates": len(u),
        "original_rows_read": len(oracle.row_log),
        "charged_units": sum(work.values()),
        "maximum_transient_groups": state.metrics["maximum_transient_response_groups"]
        if state
        else 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    counts, work, profiles = Counter(), Counter(), []
    for graph in nx.graph_atlas_g():
        if len(graph) < 2 or len(graph) > (6 if args.full else 4) or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in [F(1), F(1, 3), F(1, 64)]:
                for lam in [F(1, 64), F(1, 8), F(1, 3), F(1, 2), F(3, 4), F(1), F(2)]:
                    check_case(graph, seed, alpha, lam, counts, work, dense_prefixes=lam < F(1, 2))
    for atlas_id, quotient in enumerate(nx.graph_atlas_g()):
        k = len(quotient)
        if k < 2 or k > (4 if args.full else 3) or not nx.is_connected(quotient):
            continue
        sizes = [2 + i % 2 for i in range(k)]
        for mask in [0, 2**k - 1]:
            graph, partition = blow_up(quotient, sizes, mask)
            for seed in [members[-1] for members in partition]:
                profiles.append(
                    {
                        "family": "unsupplied_mixed_quotient_types",
                        "quotient_atlas_id": atlas_id,
                        "type_sizes": sizes,
                        "clique_mask": mask,
                        **check_case(
                            graph,
                            seed,
                            F(1, 64),
                            F(1, 8 * len(graph)),
                            counts,
                            work,
                            dense_prefixes=True,
                            partition=partition,
                        ),
                    }
                )
    for power in [8, 80, 256, 1024] if args.full else [8, 80]:
        profiles.append(
            {
                "family": "tiny_alpha_two_vertex",
                **check_case(nx.path_graph(2), 0, F(1, 2**power), F(1, 8), counts, work, True),
            }
        )
        for sign in [-1, 1]:
            profile = check_case(
                nx.path_graph(2), 0, F(1, 3), F(1, 3) + sign * F(1, 2**power), counts, work, True
            )
            assert profile["positive_coordinates"] == (2 if sign < 0 else 1)
            profiles.append(
                {
                    "family": "arbitrarily_small_exact_gate",
                    "gate_side": "positive" if sign < 0 else "negative",
                    "penalty_offset_power": power,
                    **profile,
                }
            )
            counts["tiny_signed_exact_gate_stress_cases"] += 1
    for power in [20, 128, 1024] if args.full else [20]:
        ledger = Counter()
        oracle = MassiveHub(2**power, ledger)
        exact, state = exact_physical(oracle, 0, F(1, 3), F(1, 16), ledger)
        assert exact["physical"] == [(0, F(15, 16))] and oracle.rows == [0]
        assert state.vertices.size == 2 and state.volume == 1
        counts["private_huge_hub_exact_obstacle_certificates"] += 1
        work.update(ledger)
        for seed in [0, 1]:
            for lam in [F(1, 2), F(1), F(2)]:
                ledger = Counter()
                oracle = MassiveHub(2**power, ledger)
                exact, state = exact_physical(oracle, seed, F(1, 3), lam, ledger)
                assert state is None and oracle.rows == []
                assert ledger["original_degree_queries"] == 1
                assert exact["physical"] == ([(0, F(1, 2))] if seed == 0 and lam == F(1, 2) else [])
                work.update(ledger)
                counts["private_high_penalty_single_degree_no_row_cases"] += 1
    result = {
        "description": __doc__,
        "full": args.full,
        "audit_only": dict(counts),
        "parameters": {
            "producer_randomness": "none",
            "physical_penalty": "lambda=rho",
            "exact_gate": "h>0",
            "canonical_objective_targets": ["2", "1/8", "2^-20"],
            "canonical_output": "explicit dyadic coordinates; exact direct canonical bisection",
            "canonical_precision": "denominator is a power of two less than 2/min(1,epsilon_obj)",
            "factored_exact_output": "coefficient times sqrt(original_degree), stored separately",
        },
        "charged_implementation_units": dict(work),
        "profiles": profiles,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "frontier_groups.py",
                "frontier_exact.py",
                "frontier_neighborhood_types.py",
                "geometric_value_events.py",
                "small_alpha_floor.py",
                "supplied_envelope_work.py",
            ]
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
