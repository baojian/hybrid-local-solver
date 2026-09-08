"""Paid resistance sketches using ordinary energy-approximate solves.

The production path uses the supplied-tree cycle backend. Dense solves,
complete sign enumeration and deliberately nonlinear providers are named
validators; none is hidden in the production work or solver contract.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from local_gap_certificate import sort_records
from weighted_cycle_solver import CyclePreparation, dense_reference, energy
import networkx as nx

ROWS = 512
SQRT_FACTOR = F(257, 256)


def ceiling_log2(value, work):
    scale, exponent = 1, 0
    while scale < value:
        scale *= 2
        exponent += 1
        work["sketch_log_budget_doubling_operations"] += 4
    return exponent


def sqrt_upper(value, work):
    """Eight rational bisections after a paid dyadic bracket; value >= 1."""
    assert value >= 1
    upper = F(1)
    work["sqrt_bracket_setup_operations"] += 2
    while upper * upper < value:
        upper *= 2
        work["sqrt_bracket_doubling_comparison_operations"] += 4
    lower = upper / 2
    for _ in range(8):
        middle = (lower + upper) / 2
        if middle * middle >= value:
            upper = middle
        else:
            lower = middle
        work["sqrt_bisection_operations_and_scalar_words"] += 7
    return upper


class ResistancePreparation:
    def __init__(self, n, original, tree_ids, root, work, validator_factory=None):
        self.n, self.original, self.work = n, original, work
        self.m = len(original)
        if n == 1:
            assert not original
            self.minimum, self.normalized, self.scales, self.provider = F(1), [], [], None
            return
        assert original and 0 <= root < n
        self.minimum = original[0][2]
        for u, v, c in original:
            assert 0 <= u < n and 0 <= v < n and u != v and c > 0
            self.minimum = min(self.minimum, c)
            work["normalization_input_reads_checks_and_minimum_operations"] += 9
        self.normalized, self.scales = [], []
        for u, v, c in original:
            value = c / self.minimum
            self.normalized.append((u, v, value))
            self.scales.append(sqrt_upper(value, work))
            work["normalized_edge_and_scale_words_with_copy_budget"] += 13
        self.eta, self.solve_delta = F(1, 128 * self.m), F(1, 16 * ROWS)
        self.provider = (
            CyclePreparation(n, self.normalized, tree_ids, root, work)
            if validator_factory is None
            else validator_factory(n, self.normalized)
        )

    def group(self, fair_bit):
        """One full prescribed group, streaming rows and charging each solve."""
        sums = [F(0)] * self.m
        self.work["group_accumulator_words"] += self.m
        for _ in range(ROWS):
            demand = [F(0)] * self.n
            self.work["sketch_rhs_words_allocated"] += self.n
            for (u, v, _), scale in zip(self.normalized, self.scales):
                bit = fair_bit()
                assert bit in (0, 1)
                signed = scale if bit else -scale
                demand[u] += signed
                demand[v] -= signed
                self.work["sketch_independent_Rademacher_bits"] += 1
                self.work["sketch_rhs_input_reads_and_arithmetic"] += 9
            answer, _ = self.provider.solve(demand, self.eta, self.solve_delta, fair_bit)
            self.work["ordinary_solver_calls"] += 1
            if answer is None:
                self.work["aborted_group_zero_output_words"] += self.m
                return [F(0)] * self.m, False
            assert len(answer) == self.n
            for edge, (u, v, _) in enumerate(self.normalized):
                difference = answer[u] - answer[v]
                sums[edge] += difference * difference
                self.work["edge_sketch_difference_and_accumulation_operations"] += 8
        result = [value / ROWS for value in sums]
        self.work["completed_group_output_words_and_divisions"] += 2 * self.m
        return result, True

    def estimate(self, delta, fair_bit):
        assert 0 < delta < 1
        if self.n == 1:
            return [], {"groups": 0, "rows_per_group": ROWS, "aborted_groups": 0}
        groups = 32 * ceiling_log2(4 * self.m / delta, self.work) + 1
        vectors, aborted = [], 0
        for _ in range(groups):
            values, success = self.group(fair_bit)
            vectors.append(values)
            aborted += not success
            self.work["group_vector_references_and_copy_budget"] += 3
        result = []
        for edge in range(self.m):
            records = [(vector[edge],) for vector in vectors]
            self.work["median_input_reads_records_and_copy_budget"] += 4 * groups
            ordered = sort_records(records, self.work)
            result.append(ordered[groups // 2][0] / self.minimum)
            self.work["rescaled_median_output_operations_and_words"] += 5
        return result, {"groups": groups, "rows_per_group": ROWS, "aborted_groups": aborted}


class NonlinearReference:
    """Dense validator with admissible, RHS-dependent nonlinear error."""

    def __init__(self, n, original, counts, fail_every=0):
        self.n, self.original, self.counts = n, original, counts
        self.calls, self.fail_every = 0, fail_every

    def solve(self, demand, eta, delta, fair_bit):
        del delta, fair_bit
        self.calls += 1
        if self.fail_every and self.calls % self.fail_every == 0:
            self.counts["validator_injected_group_failures"] += 1
            return None, {}
        exact = dense_reference(self.n, self.original, demand)
        factor = 1 + eta if demand[0] >= 0 else 1 - eta
        answer = [factor * value for value in exact]
        assert energy(self.original, [x - y for x, y in zip(answer, exact)]) <= eta * eta * energy(
            self.original, exact
        )
        self.counts["validator_dense_nonlinear_solve_energy_certificates"] += 1
        return answer, {}


def exact_resistances(n, edges, counts):
    output = []
    for u, v, _ in edges:
        demand = [F((i == u) - (i == v)) for i in range(n)]
        solution = dense_reference(n, edges, demand)
        output.append(solution[u] - solution[v])
        counts["validator_dense_effective_resistance_solves"] += 1
    assert sum((c * r for (_, _, c), r in zip(edges, output)), F(0)) == n - 1
    counts["validator_exact_leverage_sum_identities"] += 1
    return output


def moment_case(n, edges, counts, work):
    minimum = min(c for _, _, c in edges)
    normalized = [(u, v, c / minimum) for u, v, c in edges]
    scales = [sqrt_upper(c, work) for _, _, c in normalized]
    h, m = SQRT_FACTOR, len(edges)
    eta = F(1, 128 * m)
    nonlinear = NonlinearReference(n, normalized, counts)
    for u, v, _ in edges:
        demand = [F((i == u) - (i == v)) for i in range(n)]
        voltage = dense_reference(n, normalized, demand)
        resistance = voltage[u] - voltage[v]
        coefficients = [s * (voltage[a] - voltage[b]) for (a, b, _), s in zip(edges, scales)]
        second = sum((c * c for c in coefficients), F(0))
        fourth_formula = 3 * second * second - 2 * sum((c**4 for c in coefficients), F(0))
        assert resistance <= second <= h * h * resistance
        second_sum, fourth_sum = F(0), F(0)
        for signs in itertools.product((-1, 1), repeat=m):
            value = sum((a * c for a, c in zip(signs, coefficients)), F(0))
            second_sum += value * value
            fourth_sum += value**4
            counts["validator_enumerated_edge_Rademacher_rows"] += 1
        assert second_sum / (2**m) == second
        assert fourth_sum / (2**m) == fourth_formula <= 3 * second * second
        counts["exact_Rademacher_second_fourth_moment_identities"] += 1
    # All rows independently verify the energy perturbation bound. The
    # nonlinear validator need not be representable by one fixed matrix.
    exact_r = exact_resistances(n, normalized, counts)
    for signs in itertools.product((-1, 1), repeat=m):
        demand = [F(0)] * n
        for (u, v, _), s, a in zip(edges, scales, signs):
            demand[u] += s * a
            demand[v] -= s * a
        exact = dense_reference(n, normalized, demand)
        exact_energy = energy(normalized, exact)
        assert exact_energy <= h * h * m
        answer, _ = nonlinear.solve(demand, eta, F(1, 8192), lambda: 0)
        error = [x - y for x, y in zip(answer, exact)]
        for (u, v, _), resistance in zip(edges, exact_r):
            assert (error[u] - error[v]) ** 2 <= eta * eta * h * h * m * resistance
            counts["ordinary_nonlinear_edge_error_bounds"] += 1
        counts["exact_sketch_rhs_energy_bounds"] += 1
    demand = [F(0)] * n
    demand[0], demand[-1] = F(1), F(-1)
    positive, _ = nonlinear.solve(demand, eta, F(1, 8192), lambda: 0)
    negative, _ = nonlinear.solve([-b for b in demand], eta, F(1, 8192), lambda: 0)
    assert positive != [-v for v in negative]
    counts["nonlinear_provider_not_a_fixed_linear_operator"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    h = SQRT_FACTOR
    assert (F(7, 8) - h / 128) ** 2 >= F(3, 4)
    assert h * h * (F(17, 16) + F(1, 128)) ** 2 <= F(5, 4)
    assert F(2, ROWS) / F(1, 8) ** 2 == F(1, 4)
    assert ROWS * F(1, 16 * ROWS) == F(1, 16)
    assert F(55, 64) <= F(7, 8)
    counts["exact_sketch_perturbation_and_failure_constants"] += 5
    for exponent in range(0, 1025, 16) if args.full else range(0, 81, 16):
        for factor in [F(1), F(257, 256), F(2), F(4) - F(1, 2**40)]:
            value = F(2) ** exponent * factor
            before = sum(work.values())
            upper = sqrt_upper(value, work)
            assert value <= upper * upper <= h * h * value
            assert sum(work.values()) - before <= 60 + 4 * (exponent + 2)
            counts["dyadic_square_root_bracket_and_work_checks"] += 1
    for m in [1, 2, 3, 100, 10**9]:
        for delta in [F(1, 2), F(1, 16), F(1, 2**100)]:
            logarithm = ceiling_log2(4 * m / delta, work)
            groups = 32 * logarithm + 1
            # Exact bound stronger than the exponential bound used in text.
            assert F(55, 64) ** groups * m * m <= delta * delta
            counts["exact_joint_median_confidence_budgets"] += 1
    graphs = [
        g
        for g in nx.graph_atlas_g()
        if 2 <= len(g) <= (4 if args.full else 3) and nx.is_connected(g)
    ]
    for graph in graphs:
        n = len(graph)
        for profile in range(2 if args.full else 1):
            edges = [
                (u, v, F(2) ** ((e % 3) * 2 - 2) if profile else F(1))
                for e, (u, v) in enumerate(graph.edges())
            ]
            moment_case(n, edges, counts, work)
    if args.full:
        for n, edges in [
            (2, [(0, 1, F(2) ** -80), (0, 1, F(1)), (0, 1, F(2) ** 80)]),
            (3, [(0, 1, F(2) ** -80), (1, 2, F(1)), (0, 2, F(2) ** 80)]),
        ]:
            moment_case(n, edges, counts, work)
            counts["extreme_relative_weight_moment_fixtures"] += 1
    # Full prescribed groups with the actual cycle backend, including a
    # nontrivial cycle. No dense solve supplies these output vectors.
    fixtures = [
        (1, [], []),
        (2, [(0, 1, F(1, 2**80))], [0]),
        (3, [(0, 1, F(1)), (1, 2, F(4))], [0, 1]),
        (3, [(0, 1, F(1)), (1, 2, F(2)), (0, 2, F(4))], [0, 1]),
        (3, [(0, 1, F(2) ** -40), (1, 2, F(1)), (0, 2, F(2) ** 40)], [1, 2]),
    ]
    for fixture_id, (n, edges, tree_ids) in enumerate(fixtures if args.full else fixtures[:2]):
        prep = ResistancePreparation(n, edges, tree_ids, n - 1, work)
        rng = random.Random(908500 + fixture_id)
        actual, outcome = prep.estimate(F(1, 4), lambda: rng.getrandbits(1))
        exact = exact_resistances(n, edges, counts)
        assert all(F(3, 4) * r <= a <= F(5, 4) * r for a, r in zip(actual, exact))
        counts["actual_cycle_backend_complete_resistance_estimates"] += 1
        counts["actual_cycle_backend_prescribed_groups"] += outcome["groups"]
        counts["actual_cycle_backend_estimated_edges"] += len(edges)
    # Complete estimator with an explicitly labelled dense nonlinear provider.
    graph = nx.complete_graph(4)
    edges = [(u, v, F(1 + i % 3)) for i, (u, v) in enumerate(graph.edges())]
    prep = ResistancePreparation(
        4,
        edges,
        [],
        0,
        work,
        validator_factory=lambda n, original: NonlinearReference(n, original, counts),
    )
    rng = random.Random(908511)
    if args.full:
        actual, outcome = prep.estimate(F(1, 4), lambda: rng.getrandbits(1))
        exact = exact_resistances(4, edges, counts)
        assert all(F(3, 4) * r <= a <= F(5, 4) * r for a, r in zip(actual, exact))
        counts["validator_nonlinear_complete_resistance_estimates"] += 1
        counts["validator_nonlinear_prescribed_groups"] += outcome["groups"]
    failing = ResistancePreparation(
        4,
        edges,
        [],
        0,
        work,
        validator_factory=lambda n, original: NonlinearReference(n, original, counts, fail_every=1),
    )
    before = work["ordinary_solver_calls"]
    values, success = failing.group(lambda: rng.getrandbits(1))
    assert not success and values == [F(0)] * len(edges)
    assert work["ordinary_solver_calls"] - before == 1
    counts["capped_solve_failure_group_short_circuits"] += 1
    result = {
        "audit": "incremental_active_set_sdd.ordinary_solve_resistances",
        "scope": "Implemented median-of-means resistance estimates with ordinary cycle solves and charged fair bits; low-stretch tree is supplied. Dense moment checks and nonlinear providers are labelled validators. No local OP3 algorithm.",
        "arithmetic": "exact fractions in reference; exact-real word work, not bit complexity",
        "parameters": {
            "rows_per_group": ROWS,
            "group_rule": "32*ceil_log2(4*m/delta)+1",
            "solve_eta": "1/(128*m)",
            "solve_delta": "1/8192",
            "seed_base": 908500,
            "full": args.full,
        },
        "audit_only": dict(counts),
        "charged_sketch_and_cycle_work": dict(work),
        "work_scope": "All sketch-side operations and actual cycle backend calls; the explicitly labelled dense nonlinear provider work is validator-only.",
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "weighted_cycle_solver.py",
                "fair_bit_categorical.py",
                "local_gap_certificate.py",
                "geometric_value_events.py",
                "spectral_preconditioner_floor.py",
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
    print(
        json.dumps(
            {"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}, indent=2
        )
    )


if __name__ == "__main__":
    main()
