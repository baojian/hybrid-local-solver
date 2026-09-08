"""Exact rooted-piece routing and the literal component-stretch obstruction.

Forests, roots and path tables are supplied exhaustive validator inputs.
This audit does not implement low-stretch discovery or the weighted tree
decomposition. It independently checks the proposed quadratic comparison.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from spectral_preconditioner_floor import certify_psd, difference, laplacian
import networkx as nx


def edge_key(u, v):
    return min(u, v), max(u, v)


def forest_subsets(graph, counts):
    edges = list(graph.edges())
    for size in range(len(graph)):
        for selected in itertools.combinations(edges, size):
            forest = nx.Graph()
            forest.add_nodes_from(graph)
            forest.add_edges_from(selected)
            counts["validator_forest_candidates"] += 1
            if nx.is_forest(forest):
                components = [sorted(component) for component in nx.connected_components(forest)]
                paths = dict(nx.all_pairs_shortest_path(forest))
                counts["validator_path_words"] += sum(
                    len(path) for table in paths.values() for path in table.values()
                )
                yield forest, components, paths


def comparison(graph, weights, forest, components, paths, roots, counts):
    n = len(graph)
    root_of = {v: root for component, root in zip(components, roots) for v in component}
    part_of = {}
    # Each branch incident to a root is a separate edge-disjoint piece.
    # Pieces can share a root while belonging to the same forest component.
    for u, v in forest.edges():
        root = root_of[u]
        endpoint = u if len(paths[root][u]) > len(paths[root][v]) else v
        first_child = paths[root][endpoint][1]
        part_of[edge_key(u, v)] = root, first_child
    parts, component_stretch = defaultdict(F), defaultdict(F)
    core = defaultdict(F)
    core_records = 0
    for u, v in graph.edges():
        original = edge_key(u, v)
        if forest.has_edge(u, v):
            nodes = [u, v]
            route = [original]
            counts["retained_forest_edge_routes"] += 1
        elif root_of[u] == root_of[v]:
            nodes = paths[u][v]
            route = [edge_key(a, b) for a, b in zip(nodes, nodes[1:])]
            counts["same_root_nonforest_routes"] += 1
        else:
            left, right = paths[u][root_of[u]], paths[root_of[v]][v]
            route = [edge_key(a, b) for nodes in (left, right) for a, b in zip(nodes, nodes[1:])]
            key = edge_key(root_of[u], root_of[v])
            core[key] += weights[original]
            core_records += 1
            counts["cross_root_core_routes"] += 1
        blocks = [key for key, _ in itertools.groupby(part_of[e] for e in route)]
        assert len(blocks) <= 2 and len(blocks) == len(set(blocks))
        counts["at_most_two_piece_route_certificates"] += 1
        for edge in route:
            stretch = weights[original] / weights[edge]
            parts[part_of[edge]] += stretch
            component_stretch[root_of[edge[0]]] += stretch
            counts["validator_local_stretch_terms"] += 1
    kappa = max([F(1), *parts.values()])
    forest_edges = [(u, v, weights[edge_key(u, v)]) for u, v in forest.edges()]
    original_edges = [(u, v, weights[edge_key(u, v)]) for u, v in graph.edges()]
    core_edges = [(u, v, weight) for (u, v), weight in core.items()]
    g, f, c = laplacian(n, original_edges), laplacian(n, forest_edges), laplacian(n, core_edges)
    h = [[kappa * f[i][j] + c[i][j] for j in range(n)] for i in range(n)]
    q = [[3 * value for value in row] for row in h]
    certify_psd(difference(q, g), counts)
    certify_psd(difference(g, q, F(1, 21) / kappa), counts)
    # Independently check the stronger intermediate reverse-core inequality.
    reverse_core = [
        [3 * g[i][j] + 3 * kappa * f[i][j] - c[i][j] for j in range(n)] for i in range(n)
    ]
    certify_psd(reverse_core, counts)
    counts["rooted_piece_comparison_cases"] += 1
    counts["parallel_core_records_aggregated"] += core_records - len(core)
    counts["empty_envelope_cases"] += not len(forest.edges())
    counts["singleton_core_cases"] += len(roots) == 1
    counts["shared_root_piece_pairs"] += sum(
        max(0, sum(part_root == root for part_root, _ in parts) - 1) for root in roots
    )
    counts["nonunit_weight_cases"] += any(weight != 1 for weight in weights.values())
    max_component = max([F(0), *component_stretch.values()])
    return max_component / kappa


def star_obstruction(full, counts):
    for leaves in range(2, 10 if full else 5):
        graph = nx.star_graph(leaves)
        for forest, components, paths in forest_subsets(graph, counts):
            center_component = next(component for component in components if 0 in component)
            kept = len(center_component) - 1
            component_count = len(components)
            assert kept == leaves - component_count + 1
            for center_root in center_component:
                root_of = {i: center_root if i in center_component else i for i in graph}
                center_stretch = F(0)
                for leaf in range(1, leaves + 1):
                    if forest.has_edge(0, leaf):
                        center_stretch += 1
                    else:
                        center_stretch += len(paths[0][root_of[0]]) - 1
                assert center_stretch >= leaves - component_count + 1
                if center_root == 0:
                    assert center_stretch == kept
                counts["literal_component_star_certificates"] += 1
    asymptotic = []
    for k in list(range(4, 65)) + [128, 256, 512, 1024] if full else [4, 8, 16]:
        leaves, roots = 2 ** (2 * k), 2**k
        minimum = leaves - roots + 1
        # log2(n) < 2*k+1, and log2(log2(n)) < 2*k+1.
        conservative_denominator = F(leaves * (2 * k + 1) ** 2, roots)
        ratio = F(minimum) / conservative_denominator
        assert 2 * minimum >= leaves
        assert ratio >= F(roots, 2 * (2 * k + 1) ** 2)
        counts["asymptotic_component_star_certificates"] += 1
        asymptotic.append(
            {
                "k": k,
                "leaves": leaves,
                "root_budget": roots,
                "component_stretch_lower_bound": minimum,
                "ratio_to_conservative_m_logs_over_j": str(ratio),
            }
        )
    return asymptotic


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts = time.monotonic(), Counter()
    asymptotic = star_obstruction(args.full, counts)
    maximum_ratio = F(0)
    for graph in nx.graph_atlas_g():
        if not 1 <= len(graph) <= (5 if args.full else 3) or not nx.is_connected(graph):
            continue
        edges = list(graph.edges())
        profiles = [dict.fromkeys((edge_key(u, v) for u, v in edges), F(1))]
        if args.full:
            profiles.extend(
                [
                    {
                        edge_key(u, v): F(2) ** (((3 * i + 5) % 7) - 3)
                        for i, (u, v) in enumerate(edges)
                    },
                    {
                        edge_key(u, v): F(2) ** ([-80, 80, 0, 1][i % 4])
                        for i, (u, v) in enumerate(edges)
                    },
                ]
            )
        for forest, components, paths in forest_subsets(graph, counts):
            for roots in itertools.product(*components):
                for weights in profiles:
                    ratio = comparison(graph, weights, forest, components, paths, roots, counts)
                    maximum_ratio = max(maximum_ratio, ratio)
        counts["connected_atlas_graphs"] += 1
    result = {
        "audit": "incremental_active_set_sdd.rooted_piece_spectral_comparison",
        "arithmetic": "exact fractions and exact singular PSD elimination",
        "scope": "Supplied-forest validator for rooted-piece routing, G<=3*H0<=21*kappa*G, and an obstruction to the literal whole-component local-stretch lemma. Does not refute the final source spectral theorem, implement a weighted decomposition, or solve OP3.",
        "source_under_review": "CPW arXiv:2105.14629v2, Definitions 5.4/5.7 and Lemma 5.9, PDF pp.22-23",
        "input_family": "All connected atlas graphs through five vertices, all spanning forests, every choice of one root per component, three positive-weight profiles; all small star forests and asymptotic star certificates",
        "audit_only": dict(counts),
        "max_component_to_piece_stretch_ratio": str(maximum_ratio),
        "asymptotic_star_cases": asymptotic,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "spectral_preconditioner_floor.py": hashlib.sha256(
                Path(__file__).with_name("spectral_preconditioner_floor.py").read_bytes()
            ).hexdigest()
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
