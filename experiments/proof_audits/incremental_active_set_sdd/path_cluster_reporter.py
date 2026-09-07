"""Exact two-port tree-cluster algebra with persistent projective reporters.

The cluster operations below use constant-size Schur state and the implemented
persistent hull rope. The driver supplies tree faces and rebuilds their cluster
hierarchies as an audit. It is NOT an online local tree-hierarchy implementation.
Audit-only vertex/edge sets and dense oracles are kept outside cluster state.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import subprocess
import time

from geometric_value_events import obstacle, point, solve
import networkx as nx
from projective_hull_rope import Arena, cartesian, port_map, size, static_upper


@dataclass(frozen=True, slots=True)
class Cluster:
    ports: tuple
    matrix: tuple
    load: tuple
    hull: object = None
    threshold: tuple | None = None
    kind: str = "edge"
    children: tuple = ()
    recovery: tuple = ()


class Backend:
    def __init__(self, original, gamma):
        self.original, self.gamma = original, gamma
        self.arena = Arena()
        self.counts = Counter()

    def edge(self, parent, child, rows):
        self.counts["edge_records"] += 1
        self.counts["initial_boundary_rows"] += len(rows)
        hull = None
        for home, threshold, label in sorted(rows, key=lambda x: x[0] == parent):
            x = F(home == parent)
            row = (x, -threshold, F(1), label)
            hull = self.arena.merge(hull, self.arena.node(row))
        dp, bp = self.original[parent]
        dc, bc = self.original[child]
        return Cluster((parent, child), ((dp, -self.gamma), (-self.gamma, dc)), (bp, bc), hull)

    def compress(self, left, right):
        a, m = left.ports
        mm, b = right.ports
        assert m == mm and a != b
        self.counts["compress_records"] += 1
        dm, bm = self.original[m]
        delta = left.matrix[1][1] + right.matrix[0][0] - dm
        load = left.load[1] + right.load[0] - bm
        wl, wr = -left.matrix[0][1], -right.matrix[0][1]
        assert delta > 0 and wl > 0 and wr > 0 and load < 0
        eta, zeta, shift = wl / delta, wr / delta, load / delta
        tl = port_map(((F(1), F(0)), (eta, zeta)), (F(0), shift))
        tr = port_map(((eta, zeta), (F(0), F(1))), (shift, F(0)))
        hull = self.arena.merge(self.arena.apply(right.hull, tr), self.arena.apply(left.hull, tl))
        matrix = (
            (left.matrix[0][0] - wl * eta, -wl * zeta),
            (-wr * eta, right.matrix[1][1] - wr * zeta),
        )
        rhs = (left.load[0] + wl * shift, right.load[1] + wr * shift)
        return Cluster(
            (a, b),
            matrix,
            rhs,
            hull,
            kind="compress",
            children=(left, right),
            recovery=(m, eta, zeta, shift),
        )

    def rake(self, side, path):
        assert len(side.ports) == 1 and side.ports[0] in path.ports
        self.counts["rake_records"] += 1
        v = side.ports[0]
        i = path.ports.index(v)
        dv, bv = self.original[v]
        matrix = [list(row) for row in path.matrix]
        rhs = list(path.load)
        matrix[i][i] += side.matrix[0][0] - dv
        rhs[i] += side.load[0] - bv
        if len(path.ports) == 1:
            candidates = [t for t in [side.threshold, path.threshold] if t is not None]
            threshold = min(candidates) if candidates else None
            return Cluster(
                path.ports,
                tuple(tuple(row) for row in matrix),
                tuple(rhs),
                threshold=threshold,
                kind="rake",
                children=(side, path),
            )
        hull = path.hull
        if side.threshold is not None:
            threshold, label = side.threshold
            row = self.arena.node((F(i == 0), -threshold, F(1), label))
            hull = self.arena.merge(hull, row) if i == 0 else self.arena.merge(row, hull)
        return Cluster(
            path.ports,
            tuple(tuple(row) for row in matrix),
            tuple(rhs),
            hull,
            kind="rake",
            children=(side, path),
        )

    def forget(self, cluster):
        assert len(cluster.ports) == 2
        a, b = cluster.ports
        delta = cluster.matrix[1][1]
        load = cluster.load[1]
        weight = -cluster.matrix[0][1]
        assert delta > 0 and weight > 0 and load < 0
        eta, shift = weight / delta, load / delta
        threshold = self.arena.one_port(cluster.hull, (F(1), eta), (F(0), shift))
        self.counts["forget_records"] += 1
        return Cluster(
            (a,),
            ((cluster.matrix[0][0] - weight * eta,),),
            (cluster.load[0] + weight * shift,),
            threshold=threshold,
            kind="forget",
            children=(cluster,),
            recovery=(b, eta, shift),
        )

    def recover(self, root, port_values):
        self.counts["recovery_calls"] += 1
        values = {}
        stack = [(root, dict(zip(root.ports, port_values)))]
        while stack:
            cluster, known = stack.pop()
            self.counts["recovery_cluster_visits"] += 1
            if cluster.kind == "edge":
                for i in cluster.ports:
                    if i in values:
                        assert values[i] == known[i]
                    else:
                        values[i] = known[i]
                        self.counts["output_words"] += 1
            elif cluster.kind == "compress":
                m, eta, zeta, shift = cluster.recovery
                known[m] = eta * known[cluster.ports[0]] + zeta * known[cluster.ports[1]] + shift
                stack.extend(
                    (child, {p: known[p] for p in child.ports}) for child in cluster.children
                )
            elif cluster.kind == "rake":
                stack.extend(
                    (child, {p: known[p] for p in child.ports}) for child in cluster.children
                )
            elif cluster.kind == "forget":
                b, eta, shift = cluster.recovery
                known[b] = eta * known[cluster.ports[0]] + shift
                stack.append((cluster.children[0], known))
            else:
                raise AssertionError("unknown record")
        return values


class Case:
    """All full-graph access and metadata in this class are audit-only."""

    def __init__(self, graph, seed, alpha, epsilon, labels, counts):
        self.graph, self.seed, self.alpha, self.epsilon = graph, seed, alpha, epsilon
        self.gamma, self.lam = (1 - alpha) / (1 + alpha), epsilon / 2
        self.labels = set(labels)
        self.counts = counts
        self.original = {
            i: (F(graph.degree(i)), F(i == seed) - self.lam * graph.degree(i)) for i in labels
        }
        self.parent = {seed: None}
        order = [seed]
        for i in order:
            for j in graph[i]:
                if j in labels and j != self.parent[i]:
                    self.parent[j] = i
                    order.append(j)
        assert set(order) == self.labels
        self.boundary = {j: i for i in labels for j in graph[i] if j not in labels}
        self.local = {}
        for i in labels:
            candidates = [
                (self.lam * graph.degree(j) / self.gamma, j)
                for j, p in self.boundary.items()
                if p == i
            ]
            self.local[i] = min(candidates) if candidates else None
        self.root_home = min(j for j in graph[seed] if j in labels)
        self.backend = Backend(self.original, self.gamma)
        self.meta = {}

    def register(self, c, vertices, edges):
        self.meta[id(c)] = (set(vertices), set(edges))
        return c

    def edge(self, p, i):
        rows = []
        if self.local[i] is not None:
            rows.append((i, *self.local[i]))
        if p == self.seed and i == self.root_home and self.local[p] is not None:
            rows.append((p, *self.local[p]))
        return self.register(self.backend.edge(p, i, rows), {p, i}, {(p, i)})

    def rake(self, a, b):
        av, ae = self.meta[id(a)]
        bv, be = self.meta[id(b)]
        assert av & bv == set(a.ports) and not ae & be
        return self.register(self.backend.rake(a, b), av | bv, ae | be)

    def compress(self, a, b):
        av, ae = self.meta[id(a)]
        bv, be = self.meta[id(b)]
        assert av & bv == {a.ports[1]} and not ae & be
        return self.register(self.backend.compress(a, b), av | bv, ae | be)

    def forget(self, a):
        return self.register(self.backend.forget(a), *self.meta[id(a)])

    def side(self, i):
        out = self.edge(self.parent[i], i)
        for j in sorted(self.graph[i]):
            if j in self.labels and self.parent.get(j) == i:
                out = self.rake(self.side(j), out)
        return self.forget(out)

    def build(self, tip, style):
        path = [tip]
        while path[-1] != self.seed:
            path.append(self.parent[path[-1]])
        path.reverse()
        edges = [self.edge(a, b) for a, b in zip(path, path[1:])]
        for k, i in enumerate(path):
            for j in sorted(self.graph[i]):
                if j in self.labels and self.parent.get(j) == i and j not in path:
                    target = 0 if k == 0 else k - 1
                    if style == "right" and k < len(edges):
                        target = k
                    edges[target] = self.rake(self.side(j), edges[target])

        def join(items):
            if len(items) == 1:
                return items[0]
            split = (
                1 if style == "right" else len(items) - 1 if style == "left" else len(items) // 2
            )
            return self.compress(join(items[:split]), join(items[split:]))

        return join(edges)

    def check(self, cluster, actual_values):
        ports = cluster.ports
        vertices, edges = self.meta[id(cluster)]
        assert vertices == self.labels
        internal = sorted(vertices - set(ports))
        gamma = self.gamma

        def entry(i, j):
            return (
                self.original[i][0]
                if i == j
                else -gamma
                if (i, j) in edges or (j, i) in edges
                else F(0)
            )

        he = [[entry(i, j) for j in internal] for i in internal]
        offsets = dict(zip(internal, solve(he, [self.original[i][1] for i in internal])))
        coefficients = {i: [] for i in vertices}
        for p in ports:
            col = solve(he, [-entry(i, p) for i in internal])
            for i, value in zip(internal, col):
                coefficients[i].append(value)
        for k, p in enumerate(ports):
            coefficients[p] = [F(i == k) for i in range(len(ports))]
            offsets[p] = F(0)
        matrix = tuple(
            tuple(
                entry(i, j) + sum(entry(i, k) * coefficients[k][column] for k in internal)
                for column, j in enumerate(ports)
            )
            for i in ports
        )
        rhs = tuple(
            self.original[i][1] - sum(entry(i, k) * offsets[k] for k in internal) for i in ports
        )
        assert matrix == cluster.matrix and rhs == cluster.load
        raw = []
        for j, parent in self.boundary.items():
            aa = [gamma * x for x in coefficients[parent]]
            cc = gamma * offsets[parent] - self.lam * self.graph.degree(j)
            assert min(aa) >= 0 and sum(aa) > 0 and cc < 0
            if len(ports) == 2:
                raw.append((aa[0], cc, sum(aa), j))
            else:
                raw.append((-cc / aa[0], j))
        if len(ports) == 2:
            observer = Arena()
            got = [cartesian(observer.get(cluster.hull, k))[:2] for k in range(size(cluster.hull))]
            want = [cartesian(p)[:2] for p in static_upper(raw)]
            assert got == want
            for u, v in [
                (actual_values[ports[0]], actual_values[ports[1]]),
                (F(0), F(0)),
                (F(13, 7), F(17, 9)),
            ]:
                out = self.backend.arena.query(cluster.hull, (u, v))
                vals = {p[3]: (p[0] * u + (p[2] - p[0]) * v + p[1]) / p[2] for p in raw}
                assert (out is None) == (not vals)
                if vals:
                    assert out[0] == max(vals.values()) and vals[out[1]] == out[0]
                self.counts["exact_two_port_gate_queries"] += 1
        else:
            assert (cluster.threshold is None) == (not raw)
            if raw:
                assert cluster.threshold[0] == min(x for x, _ in raw)
                assert cluster.threshold in raw
            self.counts["exact_one_port_gate_checks"] += 1
        recovered = self.backend.recover(cluster, [actual_values[p] for p in ports])
        assert recovered == {i: actual_values[i] for i in vertices}
        self.counts["recovered_original_coordinates"] += len(vertices)
        self.counts["independent_full_schur_checks"] += 1
        self.counts["independent_boundary_rows"] += len(raw)


class ImplicitReportPath:
    """A finite unweighted path with private inactive stars, never materialized."""

    def __init__(self, degrees):
        self.n = len(degrees)
        self.report_degrees = degrees

    def degree(self, vertex):
        if vertex < self.n:
            return 2 if vertex in {0, self.n - 1} else 3
        return self.report_degrees[vertex - self.n]

    def __getitem__(self, vertex):
        assert vertex < self.n, "inactive report adjacency must not be scanned"
        return [i for i in [vertex - 1, vertex + 1] if 0 <= i < self.n] + [self.n + vertex]


def tridiagonal(diagonal, gamma, rhs):
    if not diagonal:
        return []
    pivots, load = list(diagonal), list(rhs)
    for i in range(1, len(pivots)):
        pivots[i] -= gamma * gamma / pivots[i - 1]
        load[i] += gamma * load[i - 1] / pivots[i - 1]
    out = [F(0)] * len(pivots)
    out[-1] = load[-1] / pivots[-1]
    for i in reversed(range(len(out) - 1)):
        out[i] = (load[i] + gamma * out[i + 1]) / pivots[i]
    return out


def structured_path(n):
    alpha, bar = F(1, 1009), F(1, 505)
    gamma, lam = 1 - bar, bar / (12 * 64**n)
    diagonal = [F(2)] + [F(3)] * (n - 2) + [F(2)]
    interior = diagonal[1:-1]
    left_rhs = [F(0)] * (n - 2)
    right_rhs = left_rhs[:]
    if interior:
        left_rhs[0] = gamma
        right_rhs[-1] = gamma
    left = [F(1)] + tridiagonal(interior, gamma, left_rhs) + [F(0)]
    right = [F(0)] + tridiagonal(interior, gamma, right_rhs) + [F(1)]
    offset = [F(0)] + tridiagonal(interior, gamma, [-lam * d for d in interior]) + [F(0)]
    reports = []
    raw = []
    scale = 2 / bar
    for i in range(n):
        total = gamma * (left[i] + right[i])
        x = left[i] / (left[i] + right[i])
        target = (gamma * offset[i] + scale * (1 + x * x) * total) / lam
        degree = -((-target).__floor__())
        assert degree >= 1
        reports.append(degree)
        raw.append((gamma * left[i], gamma * offset[i] - lam * degree, total, n + i))
    graph = ImplicitReportPath(reports)
    values = tridiagonal(diagonal, gamma, [F(i == 0) - lam * diagonal[i] for i in range(n)])
    assert min(values) > 0
    assert all(gamma * values[i] < lam * reports[i] for i in range(n))
    expected = static_upper(raw)
    assert len(expected) == n
    counts = Counter()
    case = Case(graph, 0, alpha, 2 * lam, set(range(n)), counts)
    schur = (
        (diagonal[0] - gamma * left[1], -gamma * right[1]),
        (-gamma * left[-2], diagonal[-1] - gamma * right[-2]),
    )
    rhs = (F(1) - lam * diagonal[0] + gamma * offset[1], -lam * diagonal[-1] + gamma * offset[-2])
    styles = []
    versions = []
    for style in ["balanced", "left", "right"]:
        old_counts = case.backend.arena.counts.copy()
        cluster = case.build(n - 1, style)
        assert cluster.matrix == schur and cluster.load == rhs
        observer = Arena()
        got = [cartesian(observer.get(cluster.hull, k))[:2] for k in range(size(cluster.hull))]
        assert got == [cartesian(p)[:2] for p in expected]
        for ports in [
            (values[0], values[-1]),
            (F(0), F(0)),
            (scale, scale),
            (3 * scale, F(0)),
            (F(0), 3 * scale),
        ]:
            out = case.backend.arena.query(cluster.hull, ports)
            direct = {p[3]: (p[0] * ports[0] + (p[2] - p[0]) * ports[1] + p[1]) / p[2] for p in raw}
            assert out[0] == max(direct.values()) and direct[out[1]] == out[0]
            counts["structured_extreme_queries"] += 1
        one = case.forget(cluster)
        assert one.load[0] / one.matrix[0][0] == values[0]
        eta, shift = -schur[0][1] / schur[1][1], rhs[1] / schur[1][1]
        thresholds = [
            (
                (lam * reports[i] / gamma - offset[i] - right[i] * shift)
                / (left[i] + right[i] * eta),
                n + i,
            )
            for i in range(n)
        ]
        assert one.threshold[0] == min(t for t, _ in thresholds) and one.threshold in thresholds
        recovered = case.backend.recover(one, (values[0],))
        assert recovered == dict(enumerate(values))
        versions.append(cluster)
        delta = case.backend.arena.counts - old_counts
        styles.append(
            {"style": style, "hull_vertices": size(cluster.hull), "hull_counts": dict(delta)}
        )
    for cluster in versions:
        observer = Arena()
        assert [cartesian(observer.get(cluster.hull, k))[:2] for k in range(n)] == [
            cartesian(p)[:2] for p in expected
        ]
    return {
        "positive_vertices": n,
        "support_volume": int(sum(diagonal)),
        "ambient_vertices": n + sum(reports),
        "alpha_lazy": str(alpha),
        "eps_appr": str(2 * lam),
        "lambda": str(lam),
        "boundary_degree_rule": "ceil((gamma*z_i+(2/bar_alpha)*(1+x_i^2)*gamma*(hL_i+hR_i))/lambda)",
        "all_boundary_rows_retained": True,
        "styles": styles,
        "backend_counts": dict(case.backend.counts),
        "audit_only": dict(counts),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--structured", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    counts, backend_counts, hull_counts = Counter(), Counter(), Counter()
    parameters = [(F(1, 3), F(1, 5)), (F(1, 7), F(1, 20)), (F(1, 1009), F(1, 50))]
    rng = random.Random(20260908)
    for n in range(2, args.max_n + 1):
        for graph0 in nx.nonisomorphic_trees(n):
            graph = nx.convert_node_labels_to_integers(graph0, ordering="sorted")
            for seed in graph:
                for alpha, epsilon in parameters:
                    gamma = (1 - alpha) / (1 + alpha)
                    lam = epsilon / 2
                    matrix = [
                        [
                            F(graph.degree(i)) if i == j else -gamma if j in graph[i] else F(0)
                            for j in range(n)
                        ]
                        for i in range(n)
                    ]
                    load = [F(i == seed) - lam * graph.degree(i) for i in range(n)]
                    optimum = obstacle(matrix, load)
                    labels = {seed}
                    counts["source_instances"] += 1
                    if not optimum[seed]:
                        continue
                    while True:
                        values = point(matrix, load, labels)
                        assert all(values[i] > 0 for i in labels)
                        boundary = sorted({j for i in labels for j in graph[i] if j not in labels})
                        if len(labels) >= 2:
                            case = Case(graph, seed, alpha, epsilon, labels, counts)
                            tips = sorted(labels - {seed})
                            selected = tips if n <= 5 else [rng.choice(tips)]
                            versions = []
                            for tip in selected:
                                for style in ["balanced", "left", "right"]:
                                    tree = case.build(tip, style)
                                    case.check(tree, values)
                                    one = case.forget(tree)
                                    case.check(one, values)
                                    assert one.load[0] / one.matrix[0][0] == values[seed]
                                    versions.append(tree)
                            for old in versions:
                                case.check(old, values)
                                counts["retained_reparenthesized_versions"] += 1
                            sides = [case.side(j) for j in sorted(graph[seed]) if j in labels]
                            for ordered in [sides, list(reversed(sides))]:
                                one = ordered[0]
                                for side in ordered[1:]:
                                    one = case.rake(side, one)
                                    counts["one_port_to_one_port_rakes"] += 1
                                case.check(one, values)
                                assert one.load[0] / one.matrix[0][0] == values[seed]
                            backend_counts.update(case.backend.counts)
                            hull_counts.update(case.backend.arena.counts)
                            counts["positive_faces"] += 1
                        due = [
                            j
                            for j in boundary
                            if -sum(matrix[j][i] * values[i] for i in labels) + load[j] > 0
                        ]
                        if not due:
                            assert values == optimum
                            break
                        labels.add(min(due))
                        counts["legal_admissions"] += 1
        print(
            json.dumps(
                {
                    "through_n": n,
                    "faces": counts["positive_faces"],
                    "schur_checks": counts["independent_full_schur_checks"],
                }
            ),
            flush=True,
        )
    result = {
        "audit": "incremental_active_set_sdd.path_cluster_reporter",
        "arithmetic": "exact fractions",
        "random_seed": 20260908,
        "seed": "every vertex",
        "graph": "all nonisomorphic trees through max_n",
        "max_n": args.max_n,
        "parameters_alpha_epsilon": [[str(a), str(e)] for a, e in parameters],
        "stopping_rule": "exact positive source face sequence; all-quiet obstacle stop",
        "scope": "cluster backend implemented; supplied hierarchy rebuilds are audit-only, no online local solver claimed",
        "audit_only": dict(counts),
        "backend_counts": dict(backend_counts),
        "hull_counts": dict(hull_counts),
        "structured_cases": [structured_path(n) for n in [8, 16, 32, 64, 128]]
        if args.structured
        else [],
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "hull_backend_sha256": hashlib.sha256(
            Path(__file__).with_name("projective_hull_rope.py").read_bytes()
        ).hexdigest(),
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
