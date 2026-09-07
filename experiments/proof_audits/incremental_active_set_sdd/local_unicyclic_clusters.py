"""Exact local unicyclic state-machine audit with rebuilt reference hierarchies.

Admissions use only original degree/row access, local heaps, cluster reporters,
and at most two named-coordinate queries per checkpoint. The hierarchy builder
and its parent index are deliberately rebuilt and separately charged: this is a
correctness driver, not an implementation of the published online top tree.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import heapq
import json
from pathlib import Path
import subprocess
import time

from cluster_point_queries import audit_index, point_query
from geometric_value_events import obstacle, point, solve
from local_sun_solver import Oracle
import networkx as nx
from shifted_tree_clusters import ShiftedBackend
from top_tree_callback_adapter import Adapter


class ReferenceHierarchy:
    """Cached active edges only; full reconstruction is explicitly audit-only."""

    def __init__(self, state):
        self.state = state
        self.counts = state.builder_counts
        self.counts["full_hierarchy_rebuilds"] += 1
        self.adapter = Adapter(state.anchor, state.depth, state.original, state.gamma)
        self.adapter.backend = ShiftedBackend(state.original, state.gamma, state.shift)
        self.children = {i: [] for i in state.active}
        for i, parent in state.parent.items():
            self.counts["active_parent_entries_read"] += 1
            if parent is not None:
                self.children[parent].append(i)
        for children in self.children.values():
            children.sort()
        self.root_home = self.children[state.anchor][0]
        self.minimum = {i: state.minimum(i, self.counts) for i in state.active}
        self.counts["rebuilt_home_payloads"] += len(state.active)

    def edge(self, parent, child, ports):
        rows = []
        if self.minimum[child] is not None:
            rows.append((child, *self.minimum[child]))
        if parent == self.state.anchor and child == self.root_home:
            if self.minimum[parent] is not None:
                rows.append((parent, *self.minimum[parent]))
        return self.adapter.create((parent, child), ports, rows)

    def branch(self, parent, child):
        children = self.children[child]
        if not children:
            return self.edge(parent, child, (parent,))
        out = self.edge(parent, child, (parent, child))
        for k, grandchild in enumerate(children):
            side = self.branch(child, grandchild)
            ports = (parent,) if k == len(children) - 1 else (parent, child)
            out = self.adapter.join(side, out, ports)
        return out

    def build(self):
        state = self.state
        if state.extra is None:
            items = [self.branch(state.anchor, child) for child in self.children[state.anchor]]
            while len(items) > 1:
                items = [
                    self.adapter.join(items[k], items[k + 1], (state.anchor,))
                    if k + 1 < len(items)
                    else items[k]
                    for k in range(0, len(items), 2)
                ]
            return items[0]
        tip = state.extra[1]
        path = [tip]
        while path[-1] != state.anchor:
            path.append(state.parent[path[-1]])
        path.reverse()
        path_vertices = set(path)
        items = [self.edge(a, b, (a, b)) for a, b in zip(path, path[1:])]
        for k, vertex in enumerate(path):
            target = max(0, k - 1)
            for child in self.children[vertex]:
                if child not in path_vertices:
                    items[target] = self.adapter.join(
                        self.branch(vertex, child), items[target], items[target].ports
                    )
        while len(items) > 1:
            items = [
                self.adapter.join(
                    items[k], items[k + 1], (items[k].ports[0], items[k + 1].ports[-1])
                )
                if k + 1 < len(items)
                else items[k]
                for k in range(0, len(items), 2)
            ]
        assert items[0].ports == state.extra
        return items[0]


class LocalState:
    def __init__(self, oracle, seed, alpha, lam, extra_first=False):
        self.oracle, self.seed, self.alpha, self.lam = oracle, seed, alpha, lam
        self.gamma, self.bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        self.shift = 1 / self.bar
        self.active, self.boundary, self.heaps = set(), {}, {}
        self.parent, self.depth, self.original, self.tree = {}, {}, {}, {}
        self.anchor, self.extra, self.exception = seed, None, None
        self.extra_first = extra_first
        self.counts, self.builder_counts, self.query_counts = Counter(), Counter(), Counter()
        self.backend_counts, self.hull_counts, self.callback_counts = (
            Counter(),
            Counter(),
            Counter(),
        )
        self.history, self.admissions = [], []

    def minimum(self, parent, ledger=None):
        ledger = self.counts if ledger is None else ledger
        heap = self.heaps[parent]
        ledger["heap_minimum_calls"] += 1
        while heap:
            threshold, label = heap[0]
            ledger["heap_validity_dictionary_reads"] += 1
            if self.boundary.get(label) == (parent,):
                return threshold, label
            heapq.heappop(heap)
            ledger["lazy_heap_deletions"] += 1
        return None

    def admit(self, vertex):
        parents = self.boundary.pop(vertex) if self.active else ()
        assert len(parents) <= 2
        closing = len(parents) == 2
        if closing:
            assert self.extra is None and self.exception == vertex
            self.exception = None
            if self.extra_first:
                parents = (parents[1], parents[0])
        self.active.add(vertex)
        self.heaps[vertex], self.tree[vertex] = [], []
        degree = self.oracle.degree(vertex)
        self.original[vertex] = (
            F(degree),
            F(vertex == self.seed) - self.lam * degree - self.shift * degree,
        )
        self.parent[vertex] = parents[0] if parents else None
        self.depth[vertex] = self.depth[parents[0]] + 1 if parents else 0
        if parents:
            parent = parents[0]
            self.tree[parent].append(vertex)
            self.tree[vertex].append(parent)
        active_neighbors = []
        changed = set(parents)
        for neighbor in self.oracle.row(vertex):
            self.counts["active_membership_reads"] += 1
            if neighbor in self.active:
                active_neighbors.append(neighbor)
                continue
            neighbor_degree = self.oracle.degree(neighbor)
            old = self.boundary.get(neighbor, ())
            self.counts["boundary_incidence_dictionary_reads"] += 1
            assert len(old) <= 1
            self.boundary[neighbor] = old + (vertex,)
            self.counts["boundary_incidence_writes"] += 1
            if old:
                assert self.extra is None and not closing and self.exception is None
                self.exception = neighbor
                changed.add(old[0])
                self.counts["exception_discoveries"] += 1
            else:
                heapq.heappush(
                    self.heaps[vertex],
                    (self.lam * neighbor_degree / self.gamma - self.shift, neighbor),
                )
                self.counts["heap_insertions"] += 1
        assert set(active_neighbors) == set(parents)
        assert len(changed) <= 2
        self.counts["changed_old_home_payloads"] += len(changed)
        if closing:
            self.extra = (parents[1], vertex)
            self.anchor = parents[1]
            self.parent, self.depth = {self.anchor: None}, {self.anchor: 0}
            order = [self.anchor]
            for i in order:
                self.counts["reroot_vertex_reads"] += 1
                for j in self.tree[i]:
                    self.counts["reroot_cached_edge_reads"] += 1
                    if j != self.parent[i]:
                        self.parent[j], self.depth[j] = i, self.depth[i] + 1
                        order.append(j)
            assert set(order) == self.active
            self.counts["cycle_closures"] += 1
            self.counts["reroot_rehomed_payloads"] += len(self.active)
        elif self.extra is not None:
            self.counts["postclosure_leaf_admissions"] += 1
        self.admissions.append(vertex)
        self.counts["admissions"] += 1

    def checkpoint(self):
        self.counts["root_solves"] += 1
        if len(self.active) == 1:
            value = (1 - self.lam * self.oracle.degree(self.seed)) / self.oracle.degree(self.seed)
            minimum = self.minimum(self.seed)
            ordinary = (value - self.shift - minimum[0], minimum[1]) if minimum else None
            assert self.exception is None
            return ordinary, None, {self.seed: value}, None
        builder = ReferenceHierarchy(self)
        snapshot = builder.build()
        root = snapshot.summary
        matrix = [list(row) for row in root.matrix]
        load = list(root.load)
        if self.extra is not None:
            assert root.ports == self.extra and self.exception is None
            matrix[0][1] -= self.gamma
            matrix[1][0] -= self.gamma
            load = [value + self.gamma * self.shift for value in load]
            self.counts["two_port_cycle_corrections"] += 1
        values = solve(matrix, load)
        backend = builder.adapter.backend
        if len(root.ports) == 1:
            ordinary = (
                (values[0] - root.threshold[0], root.threshold[1]) if root.threshold else None
            )
        else:
            ordinary = backend.arena.query(root.hull, values)
        self.counts["ordinary_root_queries"] += 1
        exceptional = None
        if self.exception is not None:
            parents, leaves = audit_index(root, self.builder_counts)
            pp, qq = self.boundary[self.exception]
            aa, bb = (
                point_query(
                    i, leaves[i], lambda node: parents[id(node)], root, values, self.query_counts
                )
                + self.shift
                for i in (pp, qq)
            )
            gate = self.gamma * (aa + bb) - self.lam * self.oracle.degree(self.exception)
            exceptional = gate, self.exception
            self.counts["exceptional_queries"] += 1
            self.counts["quiet_exceptional_queries"] += gate <= 0
        self.history.append((backend, root, tuple(values)))
        self.callback_counts.update(builder.adapter.counts)
        self.backend_counts.update(backend.counts)
        self.hull_counts.update(backend.arena.counts)
        return ordinary, exceptional, None, (backend, root, tuple(values))

    def run(self, validator=None, prefer_exception=False):
        if self.lam * self.oracle.degree(self.seed) >= 1:
            self.counts["trivial_stops"] += 1
            return {}
        self.admit(self.seed)
        while True:
            ordinary, exceptional, singleton, record = self.checkpoint()
            if validator is not None:
                validator(self, ordinary, exceptional, singleton, record)
            choices = [exceptional, ordinary] if prefer_exception else [ordinary, exceptional]
            chosen = next((item for item in choices if item is not None and item[0] > 0), None)
            if chosen is None:
                self.counts["failed_final_gate_queries"] += 1
                if singleton is not None:
                    self.counts["final_output_words"] += 1
                    return singleton
                backend, root, values = record
                before = backend.counts["recovery_cluster_visits"]
                out = {i: value + self.shift for i, value in backend.recover(root, values).items()}
                self.counts["final_recovery_cluster_visits"] += (
                    backend.counts["recovery_cluster_visits"] - before
                )
                self.counts["final_output_words"] += len(out)
                return out
            self.admit(chosen[1])


def check_case(graph, seed, alpha, lam, prefer_exception, counts):
    n = len(graph)
    gamma, bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
    matrix = [
        [F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0) for j in range(n)]
        for i in range(n)
    ]
    load = [F(i == seed) - lam * graph.degree(i) for i in range(n)]
    optimum = obstacle(matrix, load)
    previous = [F(0)] * n

    def validate(state, ordinary, exceptional, singleton, record):
        nonlocal previous
        exact = point(matrix, load, state.active)
        counts["independent_face_solves"] += 1
        assert all(previous[i] <= exact[i] <= optimum[i] for i in range(n))
        assert all(exact[i] > 0 for i in state.active)
        if singleton is None:
            backend, root, ports = record
            got = backend.recover(root, ports)
            counts["audit_only_full_recoveries"] += 1
            assert all(value + state.shift == exact[i] for i, value in got.items())
        else:
            assert all(value == exact[i] for i, value in singleton.items())
        boundary = {
            j: tuple(i for i in graph[j] if i in state.active)
            for j in graph
            if j not in state.active and any(i in state.active for i in graph[j])
        }
        assert set(boundary) == set(state.boundary)
        assert all(set(ps) == set(state.boundary[j]) for j, ps in boundary.items())
        ordinary_positive, exceptional_positive = False, False
        for j, parents in boundary.items():
            gate = gamma * sum(exact[i] for i in parents) - lam * graph.degree(j)
            if len(parents) == 2:
                assert state.exception == j and exceptional == (gate, j)
                exceptional_positive |= gate > 0
            else:
                assert len(parents) == 1
                ordinary_positive |= gate > 0
            counts["independent_original_gate_checks"] += 1
        assert ordinary_positive == (ordinary is not None and ordinary[0] > 0)
        assert exceptional_positive == (exceptional is not None and exceptional[0] > 0)
        for item in [ordinary, exceptional]:
            if item is not None and item[0] > 0:
                j = item[1]
                assert gamma * sum(exact[i] for i in boundary[j]) - lam * graph.degree(j) > 0
        if state.extra is not None:
            tree_matrix = [row[:] for row in matrix]
            c, t = state.extra
            tree_matrix[c][t] = tree_matrix[t][c] = F(0)
            uncorrected = point(tree_matrix, load, state.active)
            counts["negative_uncorrected_tree_faces"] += any(
                uncorrected[i] < 0 for i in state.active
            )
            counts["physical_seed_interior_cycle_faces"] += seed not in state.extra
        previous = exact

    state = LocalState(Oracle(graph), seed, alpha, lam, extra_first=prefer_exception)
    got = state.run(validate, prefer_exception)
    assert [got.get(i, F(0)) for i in range(n)] == optimum
    assert state.oracle.rows == set(got)
    volume = sum(graph.degree(i) for i in got)
    assert not got or lam * volume < 1
    assert state.oracle.counts["adjacency_entries_inspected"] == volume
    residual = [
        F(i == seed) - sum(matrix[i][j] * got.get(j, F(0)) for j in range(n)) for i in range(n)
    ]
    assert all(0 <= residual[i] <= lam * graph.degree(i) for i in range(n))
    assert all(bar * graph.degree(i) * got.get(i, F(0)) >= 0 for i in range(n))
    counts["exact_obstacle_acl_comparisons"] += 1
    counts["stops_before_cycle_closure"] += state.extra is None
    counts["stops_with_quiet_exception"] += state.exception is not None
    # Old roots remain usable after later rebuilt versions and re-rooting.
    for backend, root, ports in state.history[:: max(1, len(state.history) // 3)]:
        parents, leaves = audit_index(root, counts)
        recovered = backend.recover(root, ports)
        for i, leaf in leaves.items():
            assert (
                point_query(i, leaf, lambda node: parents[id(node)], root, ports, counts)
                == recovered[i]
            )
        counts["retained_old_root_rechecks"] += 1
    return state


class ImplicitPrivateStars:
    """Finite unweighted graph; quiet hub rows are forbidden during this audit."""

    def __init__(self, core, hub_degree):
        self.core, self.n, self.hub_degree = core, len(core), hub_degree

    def degree(self, vertex):
        if vertex < self.n:
            return self.core.degree(vertex) + 1
        assert vertex < 2 * self.n
        return self.hub_degree * (1 + vertex % 3)

    def __getitem__(self, vertex):
        assert vertex < self.n, "An inactive private-star hub row was scanned."
        return list(self.core[vertex]) + [self.n + vertex]


def structured_cases(counts):
    records = []
    families = []
    for path_size in [8, 16]:
        core = nx.path_graph(path_size)
        core.add_edges_from([(2, path_size), (path_size, 3)])
        families.append(core)
    core = nx.balanced_tree(2, 3)
    core.add_edge(7, 8)
    families.append(core)
    core = nx.cycle_graph(8)
    for i in range(4):
        core.add_edges_from([(i, 8 + 2 * i), (8 + 2 * i, 9 + 2 * i)])
    families.append(core)
    for core in families:
        n = len(core)
        for seed in sorted({0, n - 1}):
            for alpha, lam in [(F(1, 3), F(1, 1000)), (F(1, 1009), F(1, 10000))]:
                state = check_case(core, seed, alpha, lam, True, counts)
                records.append(
                    {
                        "kind": "explicit changing attachments",
                        "edges": sorted(core.edges),
                        "seed": seed,
                        "alpha_lazy": str(alpha),
                        "lambda": str(lam),
                        "eps_appr": str(2 * lam),
                        "admission_order": state.admissions,
                        "state_machine_counts": dict(state.counts),
                        "original_graph_access": dict(state.oracle.counts),
                    }
                )
        # A fully positive core with enormous, finite, wholly unscanned stars.
        alpha, seed = F(1, 1009), n - 1
        bar, gamma = 2 * alpha / (1 + alpha), (1 - alpha) / (1 + alpha)
        lam = bar / (12 * (2 * n) ** n)
        hub_degree = -((-2 / (bar * lam)).__floor__())
        graph = ImplicitPrivateStars(core, hub_degree)
        matrix = [
            [F(graph.degree(i)) if i == j else -gamma if j in core[i] else F(0) for j in core]
            for i in core
        ]
        exact = solve(matrix, [F(i == seed) - lam * graph.degree(i) for i in core])
        assert min(exact) > 0
        assert all(gamma * exact[i] < lam * graph.degree(n + i) for i in core)
        state = LocalState(Oracle(graph), seed, alpha, lam)
        got = state.run(prefer_exception=True)
        assert [got.get(i, F(0)) for i in core] == exact
        assert state.oracle.rows == set(core)
        volume = sum(graph.degree(i) for i in core)
        assert state.oracle.counts["adjacency_entries_inspected"] == volume
        counts["implicit_private_star_exact_comparisons"] += 1
        records.append(
            {
                "kind": "implicit finite private stars",
                "core_edges": sorted(core.edges),
                "seed": seed,
                "alpha_lazy": str(alpha),
                "lambda": str(lam),
                "eps_appr": str(2 * lam),
                "core_vertices": n,
                "ambient_vertices": n + sum(graph.degree(n + i) for i in core),
                "minimum_hub_degree": hub_degree,
                "active_volume": volume,
                "admission_order": state.admissions,
                "state_machine_counts": dict(state.counts),
                "original_graph_access": dict(state.oracle.counts),
                "audit_only_hierarchy_builder_counts": dict(state.builder_counts),
                "inactive_hub_rows_scanned": 0,
            }
        )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, operations, queries, builders, backends, hulls, callbacks, access = (
        Counter() for _ in range(8)
    )
    parameters = [
        (F(1, 3), F(1, 20)),
        (F(1, 7), F(1, 100)),
        (F(1, 1009), F(1, 100)),
        (F(1, 3), F(1, 4)),
    ]
    graphs = [
        g
        for g in nx.graph_atlas_g()
        if 2 <= len(g) <= args.max_n and nx.is_connected(g) and len(g.edges) <= len(g)
    ]
    for graph in graphs:
        for seed in graph:
            for alpha, lam in parameters:
                for preference in [False, True]:
                    state = check_case(graph, seed, alpha, lam, preference, counts)
                    operations.update(state.counts)
                    maximum = state.query_counts.pop("maximum_backend_parent_height", 0)
                    queries.update(state.query_counts)
                    queries["maximum_backend_parent_height"] = max(
                        queries["maximum_backend_parent_height"], maximum
                    )
                    builders.update(state.builder_counts)
                    backends.update(state.backend_counts)
                    hulls.update(state.hull_counts)
                    callbacks.update(state.callback_counts)
                    access.update(state.oracle.counts)
        print(
            json.dumps(
                {
                    "graph_n": len(graph),
                    "edges": len(graph.edges),
                    "cases": counts["exact_obstacle_acl_comparisons"],
                }
            ),
            flush=True,
        )
    structured = structured_cases(counts) if args.structured else []
    result = {
        "audit": "incremental_active_set_sdd.local_unicyclic_clusters",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all connected simple tree and unicyclic atlas graphs through max_n",
        "max_n": args.max_n,
        "graph_count": len(graphs),
        "seed": "every vertex",
        "parameters_alpha_lambda": [[str(a), str(lam)] for a, lam in parameters],
        "eps_appr": "2*lambda",
        "policies": [
            "ordinary reporter first; second-discovered cycle edge retained as extra",
            "exceptional gate first; first-discovered cycle edge retained as extra",
        ],
        "stopping_rule": "all ordinary and exceptional original gates nonpositive; strict positive admissions only",
        "scope": "local state machine and application algebra implemented; complete hierarchy rebuilt each checkpoint with separately counted construction; published fast online hierarchy not implemented",
        "state_machine_counts": dict(operations),
        "original_graph_access": dict(access),
        "named_query_counts": dict(queries),
        "audit_only_hierarchy_builder_counts": dict(builders),
        "rebuilt_callback_counts": dict(callbacks),
        "rebuilt_backend_counts": dict(backends),
        "rebuilt_hull_counts": dict(hulls),
        "audit_only": dict(counts),
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "cluster_point_queries",
                "shifted_tree_clusters",
                "top_tree_callback_adapter",
                "path_cluster_reporter",
                "projective_hull_rope",
                "local_sun_solver",
            ]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
