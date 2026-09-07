"""Exact spectral checks for a paid preconditioner edge-floor wrapper.

Only the preconditioner is changed. Dense PSD and cut checks are validators.
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
import time

import networkx as nx


def prune(n, original, supplied, counts):
    """Input spectral order is a contract, not verified by this linear scan."""
    assert n >= 2 and original and supplied
    floor = None
    for v, w, c in original:
        assert 0 <= v < n and 0 <= w < n and v != w and c > 0
        floor = c if floor is None else min(floor, c)
        counts["original_edge_floor_records_scanned"] += 1
    tau = floor / (2 * len(supplied) * (n - 1))
    retained, deleted = [], []
    for v, w, c in supplied:
        assert 0 <= v < n and 0 <= w < n and v != w and c > 0
        counts["supplied_edge_threshold_checks"] += 1
        if c < tau:
            deleted.append((v, w, c))
            counts["deleted_edge_records_allocated"] += 1
        else:
            retained.append((v, w, 2 * c))
            counts["retained_edge_records_allocated"] += 1
            counts["retained_edge_weight_scalings"] += 1
            counts["exact_threshold_ties_retained"] += c == tau
    counts["new_record_words_allocated"] += 3 * (len(retained) + len(deleted)) + 2
    return retained, deleted, tau


def laplacian(n, edges):
    matrix = [[F(0)] * n for _ in range(n)]
    for v, w, c in edges:
        matrix[v][v] += c
        matrix[w][w] += c
        matrix[v][w] -= c
        matrix[w][v] -= c
    return matrix


def difference(a, b, scale=F(1)):
    return [[x - scale * y for x, y in zip(row, other)] for row, other in zip(a, b)]


def certify_psd(matrix, counts):
    """Exact symmetric elimination, including singular zero-pivot columns."""
    a = [row.copy() for row in matrix]
    n = len(a)
    counts["reference_PSD_matrix_words_allocated"] += n * n
    for i in range(n):
        assert a[i][i] >= 0
        if a[i][i] == 0:
            assert all(a[j][i] == 0 == a[i][j] for j in range(i, n))
            counts["reference_PSD_zero_columns"] += 1
            continue
        for j in range(i + 1, n):
            for k in range(j, n):
                a[j][k] -= a[j][i] * a[i][k] / a[i][i]
                a[k][j] = a[j][k]
                counts["reference_PSD_Schur_entries_updated"] += 1
    counts["complete_exact_PSD_certificates"] += 1


def audit_case(n, original, supplied, kappa, roots, counts, work):
    g, h = laplacian(n, original), laplacian(n, supplied)
    certify_psd(difference(h, g), counts)
    certify_psd(difference(g, h, 1 / kappa), counts)
    output, deleted, tau = prune(n, original, supplied, work)
    new, removed = laplacian(n, output), laplacian(n, deleted)
    certify_psd(difference(g, removed, F(2)), counts)
    certify_psd(difference(new, g), counts)
    certify_psd(difference(g, new, 1 / (2 * kappa)), counts)
    floor = min(c for _, _, c in original)
    assert all(c >= floor / (len(supplied) * (n - 1)) for _, _, c in output)
    assert sum(c for _, _, c in deleted) <= floor / (2 * (n - 1))
    assert sum(c for _, _, c in output) <= 2 * kappa * sum(c for _, _, c in original)
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from((v, w) for v, w, _ in output)
    assert nx.is_connected(graph)
    old = nx.Graph()
    old.add_nodes_from(range(n))
    old.add_edges_from((v, w) for v, w, _ in supplied)
    weights = {(min(v, w), max(v, w)): c for v, w, c in supplied}
    for v, w in nx.bridges(old):
        c = weights[min(v, w), max(v, w)]
        assert c >= floor and graph.has_edge(v, w)
        counts["original_bridge_cut_and_retention_certificates"] += 1
    if roots is not None:
        assert nx.is_connected(graph.subgraph(roots))
        assert all(v in roots and w in roots for v, w, _ in deleted)
        forest = old.copy()
        forest.remove_edges_from([(v, w) for v, w in old.edges() if v in roots and w in roots])
        assert nx.is_forest(forest)
        assert all(len(set(c) & set(roots)) == 1 for c in nx.connected_components(forest))
        counts["valid_forest_core_decompositions_preserved"] += 1
    # Complete cut identities are independent of the PSD elimination.
    for bits in range(1, 1 << (n - 1)):

        def crossing(v, w):
            return bool(bits & (1 << v)) != bool(bits & (1 << w))

        a = sum(c for v, w, c in original if crossing(v, w))
        b = sum(c for v, w, c in output if crossing(v, w))
        assert 0 < a <= b <= 2 * kappa * a
        counts["complete_nontrivial_cut_certificates"] += 1
    counts["complete_preconditioner_floor_cases"] += 1
    counts["cases_with_deleted_edges"] += bool(deleted)
    return {
        "n": n,
        "original_edges": len(original),
        "supplied_edges": len(supplied),
        "deleted_edges": len(deleted),
        "quality_before": str(kappa),
        "threshold": str(tau),
        "retained_minimum": str(min(c for _, _, c in output)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, rng = time.monotonic(), random.Random(80313)
    counts, work, cases = Counter(), Counter(), []
    scales = [F(1, 2**80), F(1), F(2**80)] if args.full else [F(1)]
    for n in range(3, 10 if args.full else 5):
        for scale in scales:
            for factor in [F(1, 2), F(1), F(2)]:
                original = [(v, w, scale) for v in range(n) for w in range(v)]
                tau = scale / (2 * n * (n - 1))
                supplied = [(0, v, n * scale) for v in range(1, n)]
                supplied.append((1, 2, factor * tau))
                cases.append(audit_case(n, original, supplied, F(n + 1), [0, 1, 2], counts, work))
    for graph in nx.graph_atlas_g():
        if not 3 <= len(graph) <= (5 if args.full else 4) or not nx.is_connected(graph):
            continue
        n = len(graph)
        original = [(v, w, F(rng.randrange(1, 8), rng.randrange(1, 5))) for v, w in graph.edges()]
        floor = min(c for _, _, c in original)
        for scale in scales:
            g = [(v, w, scale * c) for v, w, c in original]
            supplied = [(v, w, 2 * c) for v, w, c in g]
            missing = next(
                ((v, w) for v in range(n) for w in range(v) if not graph.has_edge(v, w)), None
            )
            extra = F(0)
            if missing:
                extra = scale * floor / (4 * (len(supplied) + 1) * (n - 1))
                supplied.append((*missing, extra))
            kappa = 2 + (n - 1) * extra / (scale * floor)
            cases.append(audit_case(n, g, supplied, kappa, None, counts, work))
    assert counts["cases_with_deleted_edges"] and work["exact_threshold_ties_retained"]
    result = {
        "audit": "incremental_active_set_sdd.spectral_preconditioner_floor",
        "arithmetic": "exact fractions",
        "random_seed": 80313,
        "input_family": "Complete graph versus scaled star with threshold-adjacent core edge; weighted connected atlas graphs; common scales 2^-80,1,2^80",
        "alpha_eps_physical_seed": "not applicable: supplied graph/preconditioner interface",
        "stopping_rule": "One complete original/supplied edge scan; delete weights strictly below threshold and double retained weights",
        "scope": "Implemented paid spectral edge-floor wrapper; all input/output PSD, bridge and cut checks are validators. No preconditioner constructor, fast coarse solver or local OP3 theorem.",
        "audit_only": dict(counts),
        "algorithm_counts": dict(work),
        "cases": cases,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
