"""Paid heavy-path cycle updates for a supplied positive-weight graph/tree.

This realizes the basic KOSZ cycle solver with O(log^2 n) tree operations
and capped fair-bit sampling. Low-stretch tree selection is a separate
source import. Dense solves and explicit paths below are validators only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fair_bit_categorical import Categorical
from geometric_value_events import solve
from spectral_preconditioner_floor import laplacian
from weighted_corridor_routing import TreeIndex
import networkx as nx


class HeavyFlow:
    def __init__(self, index, initial, work):
        self.index, self.work = index, work
        n = index.n
        sizes, heavy = [1] * n, [-1] * n
        for vertex in reversed(index.order):
            for child, _ in index.adjacency[vertex]:
                work["heavy_child_incidence_reads"] += 1
                if index.parent[child] != vertex:
                    continue
                sizes[vertex] += sizes[child]
                if heavy[vertex] == -1 or sizes[child] > sizes[heavy[vertex]]:
                    heavy[vertex] = child
                work["heavy_child_size_and_comparison_operations"] += 6
        self.root = index.order[0]
        self.head, self.position, self.vertex_at = [-1] * n, [-1] * n, []
        starts = [self.root]
        while starts:
            start = starts.pop()
            vertex = start
            while vertex != -1:
                self.head[vertex], self.position[vertex] = start, len(self.vertex_at)
                self.vertex_at.append(vertex)
                for child, _ in index.adjacency[vertex]:
                    work["heavy_order_incidence_reads"] += 1
                    if index.parent[child] == vertex and child != heavy[vertex]:
                        starts.append(child)
                        work["light_chain_stack_words_and_copy_budget"] += 3
                vertex = heavy[vertex]
                work["heavy_chain_position_operations"] += 8
        self.width = 1
        while self.width < n:
            self.width *= 2
            work["segment_width_doublings"] += 1
        self.resistance, self.weighted, self.lazy = [[F(0)] * (2 * self.width) for _ in range(3)]
        work["heavy_index_and_segment_array_words"] += 7 * n + 6 * self.width
        for vertex in range(n):
            leaf = self.width + self.position[vertex]
            resistance = (
                F(0) if vertex == self.root else index.resistance[index.parent_edge[vertex]]
            )
            self.resistance[leaf] = resistance
            self.weighted[leaf] = resistance * initial[vertex]
            work["segment_leaf_initialization_operations"] += 7
        for node in reversed(range(1, self.width)):
            self.resistance[node] = self.resistance[2 * node] + self.resistance[2 * node + 1]
            self.weighted[node] = self.weighted[2 * node] + self.weighted[2 * node + 1]
            work["segment_build_operations"] += 8
        work["released_heavy_selection_words"] += 2 * n

    def add_range(self, left, right, value, node=1, start=0, stop=None):
        stop = self.width if stop is None else stop
        self.work["segment_update_call_frame_and_interval_operations"] += 12
        if left <= start and stop <= right:
            self.lazy[node] += value
            self.weighted[node] += value * self.resistance[node]
            self.work["segment_lazy_update_operations"] += 7
            return
        middle = (start + stop) // 2
        if left < middle:
            self.add_range(left, right, value, 2 * node, start, middle)
        if right > middle:
            self.add_range(left, right, value, 2 * node + 1, middle, stop)
        self.weighted[node] = (
            self.weighted[2 * node]
            + self.weighted[2 * node + 1]
            + self.lazy[node] * self.resistance[node]
        )
        self.work["segment_partial_reconstruction_operations"] += 8

    def query_range(self, left, right, node=1, start=0, stop=None, carry=F(0)):
        stop = self.width if stop is None else stop
        self.work["segment_query_call_frame_and_interval_operations"] += 12
        if left <= start and stop <= right:
            self.work["segment_complete_query_operations"] += 4
            return self.weighted[node] + carry * self.resistance[node]
        middle, carry = (start + stop) // 2, carry + self.lazy[node]
        result = F(0)
        if left < middle:
            result += self.query_range(left, right, 2 * node, start, middle, carry)
        if right > middle:
            result += self.query_range(left, right, 2 * node + 1, middle, stop, carry)
        self.work["segment_partial_query_operations"] += 6
        return result

    def segments(self, vertex):
        fragments = 0
        while vertex != self.root:
            head = self.head[vertex]
            left = self.position[head] + (head == self.root)
            right = self.position[vertex] + 1
            assert left < right
            yield left, right
            vertex = self.root if head == self.root else self.index.parent[head]
            fragments += 1
            self.work["heavy_path_fragment_reads_and_state_operations"] += 9
        assert fragments <= self.index.n.bit_length()

    def potential(self, vertex):
        return sum((self.query_range(left, right) for left, right in self.segments(vertex)), F(0))

    def add_path(self, vertex, value):
        for left, right in self.segments(vertex):
            self.add_range(left, right, value)

    def materialize(self):
        n, flows, stack = self.index.n, [F(0)] * self.index.n, [(1, F(0))]
        while stack:
            node, carry = stack.pop()
            self.work["flow_materialization_stack_frame_operations"] += 8
            if node >= self.width:
                position = node - self.width
                if position < n:
                    vertex = self.vertex_at[position]
                    if vertex != self.root:
                        flows[vertex] = self.weighted[node] / self.resistance[node] + carry
                        self.work["materialized_flow_reads_and_arithmetic"] += 6
            else:
                carry += self.lazy[node]
                stack.append((2 * node, carry))
                stack.append((2 * node + 1, carry))
                self.work["materialization_stack_words_and_copy_budget"] += 10
        potentials = [F(0)] * n
        for vertex in self.index.order[1:]:
            potentials[vertex] = (
                potentials[self.index.parent[vertex]]
                + self.index.resistance[self.index.parent_edge[vertex]] * flows[vertex]
            )
            self.work["final_tree_potential_and_order_copy_operations"] += 8
        self.work["materialized_flow_and_potential_output_words"] += 2 * n
        return flows, potentials


class CyclePreparation:
    def __init__(self, n, original, tree_ids, root, work):
        self.work, self.original, self.tree_ids = work, original, tree_ids
        self.index = TreeIndex(n, original, tree_ids, root, work)
        self.in_tree = [False] * len(original)
        for edge in tree_ids:
            self.in_tree[edge] = True
        self.off_tree, self.cycle_resistance, weights = [], [], []
        for edge, (_, _, c) in enumerate(original):
            if not self.in_tree[edge]:
                self.off_tree.append(edge)
                weights.append(1 + self.index.stretches[edge])
                self.cycle_resistance.append(weights[-1] / c)
            work["off_tree_cycle_setup_operations_and_words"] += 12
        self.tau = sum(weights, F(0))
        self.sampler = Categorical(weights, work) if weights else None
        work["tree_flag_and_cycle_weight_sum_operations"] += len(original) + len(weights)
        assert self.tau == self.index.total_stretch + len(original) - 2 * n + 2

    def state(self, demand):
        return CycleState(self, demand)

    def budget(self, eta, delta):
        assert 0 < eta <= 1 and 0 < delta < 1
        if self.tau == 0:
            return 0, 0
        tau_upper = 1
        while tau_upper < self.tau:
            tau_upper *= 2
            self.work["iteration_tau_upper_doubling_operations"] += 3
        target = 2 * self.tau * self.index.total_stretch / (delta * eta * eta)
        exponent, scale = 0, 1
        while scale < target:
            exponent += 1
            scale *= 2
            self.work["iteration_log_upper_doubling_operations"] += 4
        steps = tau_upper * exponent
        self.work["iteration_budget_arithmetic_operations"] += 8
        cap = self.sampler.cap(steps, delta / 2)
        return steps, cap

    def solve(self, demand, eta, delta, fair_bit):
        state = self.state(demand)
        self.work["zero_demand_checks"] += len(demand)
        steps, cap = (0, 0) if all(value == 0 for value in demand) else self.budget(eta, delta)
        for iteration in range(steps):
            draw = self.sampler.draw(fair_bit, cap)
            if draw.category is None:
                return None, {
                    "completed_updates": iteration,
                    "prescribed_updates": steps,
                    "cap": cap,
                }
            state.update(draw.category)
        flows, potentials = state.tree.materialize()
        self.work["released_final_flow_reference_words"] += len(flows)
        return potentials, {"completed_updates": steps, "prescribed_updates": steps, "cap": cap}


class CycleState:
    def __init__(self, preparation, demand):
        self.preparation, self.work = preparation, preparation.work
        index = preparation.index
        assert len(demand) == index.n and sum(demand) == 0
        initial = list(demand)
        for vertex in reversed(index.order[1:]):
            initial[index.parent[vertex]] += initial[vertex]
            self.work["initial_demand_tree_flow_operations_and_order_copy"] += 5
        assert initial[index.order[0]] == 0
        self.tree = HeavyFlow(index, initial, self.work)
        self.off_flow = [F(0)] * len(preparation.off_tree)
        self.work["demand_validation_initial_flow_and_off_flow_words"] += 3 * index.n + len(
            self.off_flow
        )

    def update(self, selected):
        preparation = self.preparation
        u, v, c = preparation.original[preparation.off_tree[selected]]
        delta = self.off_flow[selected] / c - (self.tree.potential(u) - self.tree.potential(v))
        adjustment = delta / preparation.cycle_resistance[selected]
        self.off_flow[selected] -= adjustment
        self.tree.add_path(u, adjustment)
        self.tree.add_path(v, -adjustment)
        self.work["cycle_update_original_reads_and_scalar_operations"] += 15
        self.work["cycle_updates"] += 1
        return delta


def dense_reference(n, original, demand):
    matrix = laplacian(n, original)
    if n == 1:
        return [F(0)]
    return [F(0), *solve([row[1:] for row in matrix[1:]], demand[1:])]


def energy(original, potential):
    return sum((c * (potential[u] - potential[v]) ** 2 for u, v, c in original), F(0))


def state_checks(state, demand, optimum, counts):
    prep, index = state.preparation, state.preparation.index
    tree_flow, potential = state.tree.materialize()
    all_flow, divergence = [F(0)] * len(prep.original), [F(0)] * index.n
    for vertex in index.order[1:]:
        edge = prep.tree_ids[index.parent_edge[vertex]]
        u, _, _ = prep.original[edge]
        all_flow[edge] = tree_flow[vertex] if u == vertex else -tree_flow[vertex]
    for k, edge in enumerate(prep.off_tree):
        all_flow[edge] = state.off_flow[k]
    primal = F(0)
    for (u, v, c), flow in zip(prep.original, all_flow):
        divergence[u] += flow
        divergence[v] -= flow
        primal += flow * flow / c
    assert divergence == demand
    optimum_energy = energy(prep.original, optimum)
    gap = (
        primal
        - 2 * sum((x * b for x, b in zip(potential, demand)), F(0))
        + energy(prep.original, potential)
    )
    expected_decrease = F(0)
    for k, edge in enumerate(prep.off_tree):
        u, v, c = prep.original[edge]
        residual = all_flow[edge] / c - potential[u] + potential[v]
        expected_decrease += c * residual * residual / prep.tau
    if prep.tau:
        assert expected_decrease == gap / prep.tau
        assert expected_decrease <= primal - optimum_energy
    else:
        assert primal == optimum_energy and gap == 0
    error = energy(prep.original, [x - y for x, y in zip(potential, optimum)])
    assert error <= prep.tau * (primal - optimum_energy)
    for vertex in range(index.n):
        assert state.tree.potential(vertex) == potential[vertex]
    counts["exact_divergence_energy_gap_and_voltage_checks"] += 1
    counts["exact_tree_potential_queries"] += index.n
    return primal, potential


def audit_states(graph, weights, root, rng, counts, work, steps):
    n, edges = len(graph), list(graph.edges())
    original = [(u, v, c) for (u, v), c in zip(edges, weights)]
    weighted = graph.copy()
    for (u, v), c in zip(edges, weights):
        weighted[u][v]["weight"] = c
    tree = nx.maximum_spanning_tree(weighted)
    ids = [i for i, (u, v) in enumerate(edges) if tree.has_edge(u, v)]
    prep = CyclePreparation(n, original, ids, root, work)
    demand = [F(rng.randrange(-3, 4)) for _ in range(n)]
    demand[root] -= sum(demand)
    optimum = dense_reference(n, original, demand)
    state = prep.state(demand)
    old_energy, _ = state_checks(state, demand, optimum, counts)
    assert old_energy <= prep.index.total_stretch * energy(original, optimum)
    counts["initial_tree_flow_stretch_bounds"] += 1
    for _ in range(steps if prep.off_tree else 0):
        selected = rng.randrange(len(prep.off_tree))
        residual = state.update(selected)
        new_energy, potential = state_checks(state, demand, optimum, counts)
        assert old_energy - new_energy == residual * residual / prep.cycle_resistance[selected]
        u, v, c = original[prep.off_tree[selected]]
        assert state.off_flow[selected] / c - potential[u] + potential[v] == 0
        old_energy = new_energy
        counts["exact_sampled_cycle_energy_identities"] += 1
    counts["supplied_cycle_state_cases"] += 1


def audit_heavy_paths(tree, root, rng, counts, work, steps):
    n, edges = len(tree), list(tree.edges())
    original = [(u, v, F(2) ** ([-80, 80, 0, 1][e % 4])) for e, (u, v) in enumerate(edges)]
    index = TreeIndex(n, original, list(range(n - 1)), root, work)
    raw = [F(rng.randrange(-5, 6), 3) for _ in range(n)]
    raw[root] = F(0)
    backend = HeavyFlow(index, raw, work)
    for iteration in range(steps):
        vertex, value = rng.randrange(n), F(rng.randrange(-7, 8), 5)
        before = sum(work.values())
        backend.add_path(vertex, value)
        node = vertex
        while node != root:
            raw[node] += value
            node = index.parent[node]
            counts["validator_explicit_tree_flow_updates"] += 1
        queried = rng.randrange(n)
        actual = backend.potential(queried)
        expected, node = F(0), queried
        while node != root:
            expected += raw[node] * index.resistance[index.parent_edge[node]]
            node = index.parent[node]
            counts["validator_explicit_tree_path_terms"] += 1
        assert actual == expected
        assert sum(work.values()) - before <= 1000 * (n.bit_length() + 1) ** 2
        counts["heavy_path_update_query_and_work_checks"] += 1
        if iteration % 16 == 0 or iteration == steps - 1:
            before = sum(work.values())
            materialized, _ = backend.materialize()
            assert materialized == raw
            assert sum(work.values()) - before <= 200 * n
            counts["linear_work_flow_materializations"] += 1
    counts["large_heavy_path_tree_cases"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work, rng = time.monotonic(), Counter(), Counter(), random.Random(908045)
    for exponent in [-80, 0, 80] if args.full else [0]:
        original = [(0, 1, F(1)), (1, 2, F(1)), (0, 2, F(2) ** exponent)]
        prep = CyclePreparation(3, original, [0, 1], 0, work)
        for eta in [F(1), F(1, 8), F(1, 2**100)]:
            for delta in [F(1, 2), F(1, 8), F(1, 2**200)]:
                steps, cap = prep.budget(eta, delta)
                tau_upper = 1
                while tau_upper < prep.tau:
                    tau_upper *= 2
                exponent_bound = steps // tau_upper
                assert steps == tau_upper * exponent_bound and prep.tau <= tau_upper < 2 * prep.tau
                target = 2 * prep.tau * prep.index.total_stretch / (delta * eta * eta)
                assert 2 ** (exponent_bound - 1) < target <= 2**exponent_bound
                assert F(max(0, len(prep.off_tree) - 1) * steps, 2**cap) <= delta / 2
                counts["exact_accuracy_failure_iteration_budget_checks"] += 1
    for graph in nx.graph_atlas_g():
        n = len(graph)
        if not 1 <= n <= (5 if args.full else 4) or not nx.is_connected(graph):
            continue
        profiles = [[F(1)] * len(graph.edges())]
        if args.full:
            profiles.append([F(2) ** ([-20, 20, 0, 1][e % 4]) for e in range(len(graph.edges()))])
        for weights in profiles:
            for root in range(n) if args.full else [0]:
                audit_states(graph, weights, root, rng, counts, work, 16 if args.full else 5)
    for n in [3, 4, 5] if args.full else [3, 4]:
        graph = nx.complete_graph(n)
        edges = list(graph.edges())
        original = [(u, v, F(1)) for u, v in edges]
        ids = [i for i, (u, _) in enumerate(edges) if u == 0]
        prep = CyclePreparation(n, original, ids, 0, work)
        for seed in range(3 if args.full else 1):
            demand = [F(0)] * n
            demand[0], demand[-1] = F(1), F(-1)
            eta, delta = F(1, 8), F(1, 8)
            local_rng = random.Random(908100 + 10 * n + seed)
            answer, outcome = prep.solve(demand, eta, delta, lambda: local_rng.getrandbits(1))
            assert answer is not None
            exact = dense_reference(n, original, demand)
            error = energy(original, [x - y for x, y in zip(answer, exact)])
            assert error <= eta * eta * energy(original, exact)
            assert outcome["completed_updates"] == outcome["prescribed_updates"]
            counts["fixed_budget_end_to_end_solves"] += 1
            counts["fixed_budget_completed_updates"] += outcome["completed_updates"]
        if n == 4:
            # The first off-tree CDF boundary is 1/3. Its binary expansion
            # stays ambiguous at every finite depth and forces a clean abort.
            bit_index = 0

            def boundary_bit():
                nonlocal bit_index
                result = bit_index % 2
                bit_index += 1
                return result

            answer, outcome = prep.solve(demand, eta, delta, boundary_bit)
            assert answer is None and outcome["completed_updates"] == 0
            assert bit_index == outcome["cap"]
            counts["forced_capped_sampler_aborts"] += 1
        answer, outcome = prep.solve([F(0)] * n, eta, delta, lambda: rng.getrandbits(1))
        assert answer == [F(0)] * n and outcome["completed_updates"] == 0
        counts["zero_demand_exact_solves"] += 1
    for n in [1, 2, 17] if args.full else [1, 2]:
        original = [(v - 1, v, F(v + 1)) for v in range(1, n)]
        prep = CyclePreparation(n, original, list(range(n - 1)), n - 1, work)
        demand = [F(1)] * n
        demand[0] -= n
        answer, outcome = prep.solve(demand, F(1, 8), F(1, 8), lambda: rng.getrandbits(1))
        exact = dense_reference(n, original, demand)
        assert energy(original, [x - y for x, y in zip(answer, exact)]) == 0
        assert outcome["completed_updates"] == 0
        counts["pure_tree_exact_solves"] += 1
    for n in [32, 128, 512] if args.full else [16]:
        for shape in ("star", "path", "random"):
            tree = (
                nx.star_graph(n - 1)
                if shape == "star"
                else nx.path_graph(n)
                if shape == "path"
                else nx.from_prufer_sequence([rng.randrange(n) for _ in range(n - 2)])
            )
            for root in [0, n // 2, n - 1]:
                audit_heavy_paths(tree, root, rng, counts, work, 128 if args.full else 16)
    result = {
        "audit": "incremental_active_set_sdd.weighted_cycle_solver",
        "scope": "Implemented supplied-tree heavy-path KOSZ cycle updates and capped fair-bit fixed-budget solves; low-stretch tree selection remains a source primitive. Dense grounded solves and explicit energies are validators. No local OP3 theorem.",
        "arithmetic": "exact fractions; exact-real word work, not bit complexity",
        "work_scope": "Charges all audited backend API operations, including additional calls requested by state validators; dense reference solves and explicit reference paths are outside this counter.",
        "audit_only": dict(counts),
        "charged_cycle_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "fair_bit_categorical.py",
                "weighted_corridor_routing.py",
                "geometric_value_events.py",
                "spectral_preconditioner_floor.py",
            ]
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
