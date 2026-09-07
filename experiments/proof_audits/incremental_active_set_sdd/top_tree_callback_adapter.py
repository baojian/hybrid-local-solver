"""Exact audit of the top-tree application callback contract for local trees.

The adapter implements only constant-size application callbacks and delegates
all hull work to the persistent backend. The exhaustive driver below supplies
hierarchies and metadata. It is NOT the source paper's balancing algorithm.
Reference enumeration, dense solves, and original cluster sets are audit-only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

from geometric_value_events import solve
import networkx as nx
from path_cluster_reporter import Backend
from projective_hull_rope import Arena, cartesian, size, static_upper


@dataclass(frozen=True, slots=True)
class Snapshot:
    ports: tuple
    contains_seed: bool
    summary: object
    children: tuple = ()
    edge: tuple | None = None


class Adapter:
    """Application state; no scans of represented cluster vertices or rows."""

    def __init__(self, seed, depth, original, gamma):
        self.seed, self.depth = seed, depth
        self.backend = Backend(original, gamma)
        self.counts = Counter()

    def ordered(self, ports):
        assert len(ports) <= 2
        return tuple(sorted(ports, key=self.depth.__getitem__))

    def create(self, edge, ports, rows):
        self.counts["base_callbacks"] += 1
        ports = self.ordered(ports)
        contains = self.seed in edge
        if contains and self.seed not in ports:
            self.counts["unavailable_base_records"] += 1
            return Snapshot(ports, contains, None, edge=edge)
        assert ports
        parent, child = self.ordered(edge)
        summary = self.backend.edge(parent, child, rows)
        if len(ports) == 1:
            assert ports == (parent,)
            summary = self.backend.forget(summary)
            self.counts["one_port_base_records"] += 1
        assert summary.ports == ports
        return Snapshot(ports, contains, summary, edge=edge)

    def join(self, a, b, ports):
        self.counts["join_callbacks"] += 1
        ports = self.ordered(ports)
        contains = a.contains_seed or b.contains_seed
        shape = f"{min(len(a.ports), len(b.ports))}+{max(len(a.ports), len(b.ports))}->{len(ports)}"
        self.counts[f"shape_{shape}"] += 1
        if contains and self.seed not in ports:
            self.counts["unavailable_join_records"] += 1
            return Snapshot(ports, contains, None, children=(a, b))
        assert ports and a.summary is not None and b.summary is not None
        left, right = a.summary, b.summary
        if len(left.ports) == len(right.ports) == 2:
            if left.ports[1] != right.ports[0]:
                left, right = right, left
            assert left.ports[1] == right.ports[0]
            summary = self.backend.compress(left, right)
        else:
            if len(left.ports) != 1:
                left, right = right, left
            assert len(left.ports) == 1
            summary = self.backend.rake(left, right)
            if len(summary.ports) > len(ports):
                assert len(ports) == 1 and ports[0] == summary.ports[0]
                summary = self.backend.forget(summary)
                self.counts["rake_then_forget_records"] += 1
        assert summary.ports == ports
        return Snapshot(ports, contains, summary, children=(a, b))

    def split(self, snapshot):
        self.counts["split_callbacks"] += 1
        assert len(snapshot.children) == 2
        return snapshot.children


class AuditCase:
    """Canonical positive tree face plus wholly separate exhaustive metadata."""

    def __init__(self, tree, seed, alpha, counts):
        self.tree, self.seed, self.alpha, self.counts = tree, seed, alpha, counts
        self.n = len(tree)
        self.gamma, self.bar = (1 - alpha) / (1 + alpha), 2 * alpha / (1 + alpha)
        self.lam = self.bar / (12 * (2 * self.n) ** self.n)
        self.parent, self.depth = {seed: None}, {seed: 0}
        order = [seed]
        for i in order:
            for j in sorted(tree[i]):
                if j != self.parent[i]:
                    self.parent[j], self.depth[j] = i, self.depth[i] + 1
                    order.append(j)
        self.edges = [(self.parent[i], i) for i in order[1:]]
        self.full = (1 << len(self.edges)) - 1
        # One inactive report with private leaves at every core vertex.
        self.original = {
            i: (F(tree.degree(i) + 1), F(i == seed) - self.lam * (tree.degree(i) + 1)) for i in tree
        }
        base_degree = -((-2 / (self.bar * self.lam)).__floor__())
        self.report_degrees = {i: base_degree * (1 + (i * 3) % 5) for i in tree}
        self.rows = {i: (self.lam * self.report_degrees[i] / self.gamma, self.n + i) for i in tree}
        root_home = min(tree[seed])
        self.home = {
            i: next(k for k, edge in enumerate(self.edges) if edge == (self.parent[i], i))
            for i in tree
            if i != seed
        }
        self.home[seed] = next(k for k, edge in enumerate(self.edges) if edge == (seed, root_home))
        self.payload = {
            k: [(i, *self.rows[i]) for i in tree if self.home[i] == k]
            for k in range(len(self.edges))
        }
        matrix = [
            [
                self.original[i][0] if i == j else -self.gamma if j in tree[i] else F(0)
                for j in range(self.n)
            ]
            for i in range(self.n)
        ]
        self.values = solve(matrix, [self.original[i][1] for i in range(self.n)])
        assert min(self.values) > 0
        assert all(self.gamma * self.values[i] < self.lam * self.report_degrees[i] for i in tree)
        self.adapter = Adapter(seed, self.depth, self.original, self.gamma)
        self.meta, self.oracle_cache, self.masks = {}, {}, {}
        for mask in range(1, self.full + 1):
            edges = [edge for k, edge in enumerate(self.edges) if mask & (1 << k)]
            vertices = {i for edge in edges for i in edge}
            if len(vertices) != len(edges) + 1:
                continue
            degree = Counter(i for edge in edges for i in edge)
            ordinary = {i for i in vertices if degree[i] < tree.degree(i)}
            self.masks[mask] = (vertices, ordinary)

    def ports(self, mask, exposed):
        vertices, ordinary = self.masks[mask]
        ports = ordinary | ({self.seed} if exposed and self.seed in vertices else set())
        return tuple(sorted(ports, key=self.depth.__getitem__))

    def register(self, snapshot, mask):
        self.meta[id(snapshot)] = mask
        return snapshot

    def oracle(self, mask, ports):
        key = mask, ports
        if key in self.oracle_cache:
            return self.oracle_cache[key]
        vertices = self.masks[mask][0]
        interior = sorted(vertices - set(ports))
        assert self.seed not in interior
        selected = {frozenset(edge) for k, edge in enumerate(self.edges) if mask & (1 << k)}

        def entry(i, j):
            return (
                self.original[i][0]
                if i == j
                else -self.gamma
                if frozenset((i, j)) in selected
                else F(0)
            )

        inner = [[entry(i, j) for j in interior] for i in interior]
        offset = dict(zip(interior, solve(inner, [self.original[i][1] for i in interior])))
        coefficients = {i: [] for i in vertices}
        for p in ports:
            col = solve(inner, [-entry(i, p) for i in interior])
            for i, value in zip(interior, col):
                coefficients[i].append(value)
        for k, p in enumerate(ports):
            coefficients[p] = [F(k == j) for j in range(len(ports))]
            offset[p] = F(0)
        matrix = tuple(
            tuple(
                entry(i, j) + sum(entry(i, h) * coefficients[h][k] for h in interior)
                for k, j in enumerate(ports)
            )
            for i in ports
        )
        rhs = tuple(
            self.original[i][1] - sum(entry(i, h) * offset[h] for h in interior) for i in ports
        )
        raw = []
        for k, rows in self.payload.items():
            if not mask & (1 << k):
                continue
            for home, threshold, label in rows:
                aa = coefficients[home]
                cc = offset[home] - threshold
                assert min(aa) >= 0 and sum(aa) > 0 and cc < 0
                raw.append((aa[0], cc, sum(aa), label) if len(ports) == 2 else (-cc / aa[0], label))
        result = matrix, rhs, raw
        self.oracle_cache[key] = result
        self.counts["independent_schur_oracles"] += 1
        self.counts["independent_owned_rows"] += len(raw)
        return result

    def check(self, snapshot, mask, exposed):
        ports = self.ports(mask, exposed)
        assert snapshot.ports == ports
        contains = self.seed in self.masks[mask][0]
        assert snapshot.contains_seed == contains
        invalid = contains and self.seed not in ports
        assert (snapshot.summary is None) == invalid
        self.counts["availability_checks"] += 1
        if invalid:
            return
        assert 1 <= len(ports) <= 2
        if len(ports) == 2:
            parent, child = ports
            at = child
            while self.depth[at] > self.depth[parent]:
                at = self.parent[at]
            assert at == parent
            self.counts["rooted_port_comparability_checks"] += 1
        matrix, rhs, raw = self.oracle(mask, ports)
        state = snapshot.summary
        assert state.matrix == matrix and state.load == rhs
        if len(ports) == 2:
            observer = Arena()
            actual = [cartesian(observer.get(state.hull, k))[:2] for k in range(size(state.hull))]
            expected = [cartesian(p)[:2] for p in static_upper(raw)]
            assert actual == expected
            for values in [
                (self.values[ports[0]], self.values[ports[1]]),
                (F(0), F(0)),
                (F(13, 7), F(17, 9)),
            ]:
                got = self.adapter.backend.arena.query(state.hull, values)
                direct = {
                    p[3]: (p[0] * values[0] + (p[2] - p[0]) * values[1] + p[1]) / p[2] for p in raw
                }
                assert (got is None) == (not direct)
                if direct:
                    assert got[0] == max(direct.values()) and direct[got[1]] == got[0]
                self.counts["exact_two_port_queries"] += 1
        else:
            assert (state.threshold is None) == (not raw)
            if raw:
                assert state.threshold[0] == min(x[0] for x in raw) and state.threshold in raw
            self.counts["exact_one_port_queries"] += 1
        got = self.adapter.backend.recover(state, [self.values[p] for p in ports])
        assert got == {i: self.values[i] for i in self.masks[mask][0]}
        self.counts["recovered_original_coordinates"] += len(got)
        self.counts["valid_summary_comparisons"] += 1

    def enumerate(self, exposed):
        roots = {}
        retained = []
        for mask in sorted(self.masks, key=lambda m: (m.bit_count(), m)):
            ports = self.ports(mask, exposed)
            if len(ports) > 2:
                continue
            if mask.bit_count() == 1:
                k = mask.bit_length() - 1
                out = self.register(
                    self.adapter.create(self.edges[k], ports, self.payload[k]), mask
                )
                self.check(out, mask, exposed)
                roots[mask] = out
                retained.append(out)
                continue
            bit = mask & -mask
            left = (mask - 1) & mask
            found = 0
            while left:
                right = mask ^ left
                if left & bit and left in roots and right in roots:
                    out = self.register(self.adapter.join(roots[left], roots[right], ports), mask)
                    self.check(out, mask, exposed)
                    roots[mask] = out
                    found += 1
                    self.counts["all_legal_binary_joins"] += 1
                left = (left - 1) & mask
            assert found, (mask, ports)
            retained.append(roots[mask])
        assert self.full in roots
        for old in retained:
            self.check(old, self.meta[id(old)], exposed)
            self.counts["retained_version_comparisons"] += 1
        return roots[self.full]

    def expose(self, old):
        frontier = []

        def split_invalid(node):
            mask = self.meta[id(node)]
            if node.summary is not None:
                assert node.ports == self.ports(mask, True)
                frontier.append(node)
                self.counts["exposure_reused_roots"] += 1
            elif node.children:
                for child in self.adapter.split(node):
                    split_invalid(child)
            else:
                k = mask.bit_length() - 1
                out = self.register(
                    self.adapter.create(self.edges[k], self.ports(mask, True), self.payload[k]),
                    mask,
                )
                frontier.append(out)
                self.counts["exposure_recreated_base_edges"] += 1

        split_invalid(old)
        seen = 0
        for node in frontier:
            mask = self.meta[id(node)]
            assert not seen & mask
            seen |= mask
        assert seen == self.full
        while len(frontier) > 1:
            point = next(i for i, node in enumerate(frontier) if len(node.ports) == 1)
            a = frontier.pop(point)
            shared = a.ports[0]
            neighbor = next(i for i, node in enumerate(frontier) if shared in node.ports)
            b = frontier.pop(neighbor)
            mask = self.meta[id(a)] | self.meta[id(b)]
            out = self.register(self.adapter.join(a, b, self.ports(mask, True)), mask)
            self.check(out, mask, True)
            frontier.append(out)
        out = frontier[0]
        self.check(out, self.full, True)
        assert out.ports == (self.seed,)
        assert out.summary.load[0] / out.summary.matrix[0][0] == self.values[self.seed]
        self.counts["complete_exposure_transitions"] += 1
        return out

    def payload_refresh(self, root, edge_index):
        """Algebraic intermediate payload update, not an admission or stop query."""
        old_payload = self.payload[edge_index]
        self.payload[edge_index] = [
            (i, threshold * F(11, 7), label) for i, threshold, label in old_payload
        ]
        self.oracle_cache.clear()
        visits = 0

        def refresh(node):
            nonlocal visits
            mask = self.meta[id(node)]
            if not mask & (1 << edge_index):
                return node
            visits += 1
            if not node.children:
                return self.register(
                    self.adapter.create(node.edge, node.ports, self.payload[edge_index]), mask
                )
            a, b = node.children
            return self.register(self.adapter.join(refresh(a), refresh(b), node.ports), mask)

        new = refresh(root)
        self.check(new, self.full, True)
        self.counts["payload_path_recomputed_records"] += visits
        self.counts["intermediate_payload_refreshes"] += 1
        self.payload[edge_index] = old_payload
        self.oracle_cache.clear()
        self.check(root, self.full, True)
        self.counts["payload_old_root_rechecks"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, callbacks, backend, hull = Counter(), Counter(), Counter(), Counter()
    parameters = [F(1, 3), F(1, 1009)]
    for n in range(2, args.max_n + 1):
        for tree0 in nx.nonisomorphic_trees(n):
            tree = nx.convert_node_labels_to_integers(tree0, ordering="sorted")
            for seed in tree:
                for alpha in parameters:
                    case = AuditCase(tree, seed, alpha, counts)
                    unexposed = case.enumerate(False)
                    exposed = case.enumerate(True)
                    transitioned = case.expose(unexposed)
                    for k in sorted({0, len(case.edges) - 1}):
                        case.payload_refresh(transitioned, k)
                    case.check(exposed, case.full, True)
                    callbacks.update(case.adapter.counts)
                    backend.update(case.adapter.backend.counts)
                    hull.update(case.adapter.backend.arena.counts)
                    counts["canonical_positive_faces"] += 1
        print(
            json.dumps(
                {
                    "through_n": n,
                    "faces": counts["canonical_positive_faces"],
                    "joins": counts["all_legal_binary_joins"],
                }
            ),
            flush=True,
        )
    result = {
        "audit": "incremental_active_set_sdd.top_tree_callback_adapter",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph": "all nonisomorphic core trees through max_n, with one inactive private-star report at every core vertex",
        "seed": "every core vertex",
        "max_n": args.max_n,
        "alpha_lazy": [str(a) for a in parameters],
        "lambda_rule": "bar_alpha / (12*(2*n)^n)",
        "eps_appr": "2*lambda",
        "report_degree_rule": "ceil(2/(bar_alpha*lambda))*(1+(3*i)%5)",
        "stopping_rule": "canonical core face positive and every original report gate quiet; callback/intermediate-payload audits do not make stopping decisions",
        "scope": "application callbacks implemented; exhaustive supplied hierarchies and metadata are reference-only; published online balancing algorithm not implemented",
        "audit_only": dict(counts),
        "adapter_counts": dict(callbacks),
        "backend_counts": dict(backend),
        "hull_counts": dict(hull),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["path_cluster_reporter", "projective_hull_rope"]
        },
        "elapsed_seconds_including_reference": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
