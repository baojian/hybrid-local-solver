"""Local response-group bound under a global neighborhood-type promise.

The partition is used only by validators. The producer receives original
degree/row access and the seed, alpha and original ACL accuracy.
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
from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub
import networkx as nx


class PrivateDoubleStar:
    def __init__(self, leaves, remote_leaves, work):
        self.leaves, self.remote_leaves, self.work = leaves, remote_leaves, work
        self.rows, self.degrees = [], []

    def degree(self, label):
        assert 0 <= label < self.leaves + self.remote_leaves + 2
        self.work["double_star_original_degree_queries"] += 1
        self.degrees.append(label)
        return self.leaves + 1 if label == 0 else self.remote_leaves + 1 if label == 1 else 1

    def row(self, label):
        assert label != 1, "The remote high-degree hub row must remain unread."
        self.work["double_star_original_row_queries"] += 1
        self.rows.append(label)
        if label == 0:
            for other in range(1, self.leaves + 2):
                self.work["double_star_original_adjacency_entries"] += 1
                yield other
        else:
            self.work["double_star_original_adjacency_entries"] += 1
            yield 0 if label <= self.leaves + 1 else 1


def private_double_star(leaves, power, alpha, counts, aggregate):
    work = Counter()
    remote = 2**power
    oracle = PrivateDoubleStar(leaves, remote, work)
    epsilon = F(1, 8 * leaves)
    state = GroupFrontier(oracle, 0, alpha, epsilon, work)
    result = state.run()
    values = dict(result["records"])
    assert set(values) == {0} | set(range(2, leaves + 2))
    assert 1 not in oracle.rows and max(oracle.degrees) == leaves + 1
    assert len(oracle.rows) == len(set(oracle.rows)) == leaves + 1
    assert len(oracle.degrees) == len(set(oracle.degrees)) == leaves + 2
    assert state.volume == 2 * leaves + 1 < 2 / epsilon
    assert state.metrics["maximum_transient_response_groups"] == 2
    residuals = {label: F(int(label == 0)) for label in range(leaves + 2)}
    for pivot in state.history:
        vertex = pivot.vertex
        residuals[vertex.label] -= vertex.degree * vertex.value
        for neighbor in vertex.row:
            residuals[neighbor.label] += state.gamma * vertex.value
    for label, residual in residuals.items():
        degree = leaves + 1 if label == 0 else remote + 1 if label == 1 else 1
        assert 0 <= residual <= F(3, 4) * epsilon * degree
    assert epsilon * (leaves + 1) <= F(3, 16) < state.gamma / (1 + state.gamma)
    assert state.gamma * (F(1, leaves + 1) - epsilon) > epsilon
    assert 2 * (leaves + remote + 1) > 4 / epsilon
    aggregate.update(work)
    counts["private_four_type_double_star_outputs_and_mandatory_leaf_bounds"] += 1
    counts["private_double_star_original_residual_rows_checked"] += leaves + 2
    return {
        "family": "private_four_type_double_star",
        "near_leaves": leaves,
        "remote_leaves_formula": f"2^{power}",
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "mandatory_near_leaf_coordinates": leaves,
        "original_active_volume": state.volume,
        "remote_hub_row_read": False,
        "uncharted_remote_leaf_residual": "zero: no active original neighbor",
        "shared_matrix_updates": state.metrics["shared_matrix_updates"],
        "charged_units": sum(work.values()),
    }


def blow_up(quotient, sizes, clique_mask):
    """Validator input generation; no quotient data enter the producer."""
    groups, offset = [], 0
    for size in sizes:
        groups.append(list(range(offset, offset + size)))
        offset += size
    graph = nx.Graph()
    graph.add_nodes_from(range(offset))
    for t, members in enumerate(groups):
        if (clique_mask >> t) & 1:
            graph.add_edges_from((u, v) for u in members for v in members if u < v)
    for a, b in quotient.edges:
        graph.add_edges_from((u, v) for u in groups[a] for v in groups[b])
    return graph, groups


def type_validator(graph, partition, counts, dense=None):
    for members in partition:
        for i, u in enumerate(members):
            for v in members[i + 1 :]:
                assert set(graph[u]) - {v} == set(graph[v]) - {u}

    def validate(state):
        entries = audit_map(state.vertices)
        vertices = {label: vertex for label, vertex in entries}
        active = {p.vertex.label for p in state.history}
        if active:
            for members in partition:
                remaining = set(members) - active
                known = remaining & set(vertices)
                assert not known or known == remaining
                assert len({vertices[label].group for label in known}) <= 1
                counts["unsplit_type_and_simultaneous_discovery_checks"] += 1
        group, number = state.head, 0
        while group is not None:
            number += 1
            if len({vertex.degree for vertex in group.heap.data[: group.heap.size]}) > 1:
                counts["unequal_original_degrees_within_one_live_group"] += 1
            group = group.next
        assert number == state.live_count <= len(partition)
        assert state.metrics["maximum_transient_response_groups"] <= 2 * len(partition) + 1
        counts["completed_and_transient_type_count_bounds"] += 1
        if dense is not None:
            dense(state)

    return validate


def case(graph, partition, seed, alpha, epsilon, counts, aggregate, dense=False):
    work = Counter()
    oracle = LocalRows(graph, work)
    state = GroupFrontier(oracle, seed, alpha, epsilon, work)
    forward, backward = (
        prefix_validator(graph, seed, alpha, epsilon, counts) if dense else (None, None)
    )
    result = state.run(type_validator(graph, partition, counts, forward), backward)
    values = dict(result["records"])
    for i in graph:
        residual = (
            F(int(i == seed))
            - graph.degree(i) * values.get(i, F(0))
            + state.gamma * sum(values.get(j, F(0)) for j in graph[i])
        )
        assert 0 <= residual <= F(3, 4) * epsilon * graph.degree(i)
        if i in values:
            assert residual == epsilon * graph.degree(i) / 2
    assert all(
        value == state.bar * graph.degree(label) * values[label]
        for label, value in result["probabilities"]
    )
    assert result["volume"] < 2 / epsilon
    assert oracle.row_log == list(dict.fromkeys(oracle.row_log))
    assert oracle.degree_log == list(dict.fromkeys(oracle.degree_log))
    assert set(oracle.row_log) <= set(values)
    assert state.metrics["sum_squared_transient_groups_plus_one"] <= (
        len(values) * (2 * len(partition) + 2) ** 2
    )
    aggregate.update(work)
    counts["original_ACL_outputs_with_unsupplied_type_promise"] += 1
    counts["original_final_residual_rows"] += len(graph)
    counts["physical_source_choices_tested"] += 1
    counts["implemented_pivots"] += len(values)
    counts["implemented_partition_splits"] += state.metrics["original_row_partition_splits"]
    counts["implemented_shared_matrix_updates"] += state.metrics["shared_matrix_updates"]
    return {
        "seed": seed,
        "alpha": str(alpha),
        "epsilon": str(epsilon),
        "vertices": len(graph),
        "original_graph_volume": 2 * graph.number_of_edges(),
        "promised_type_count": len(partition),
        "original_active_volume": result["volume"],
        "maximum_transient_groups": state.metrics["maximum_transient_response_groups"],
        "pivots": len(values),
        "shared_matrix_updates": state.metrics["shared_matrix_updates"],
        "charged_units": sum(work.values()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    counts, work, configurations, profiles = Counter(), Counter(), [], []
    for atlas_id, quotient in enumerate(nx.graph_atlas_g()):
        k = len(quotient)
        if k < 1 or k > (4 if args.full else 3) or not nx.is_connected(quotient):
            continue
        patterns = [[1] * k, [1 + i % 3 for i in range(k)], [2 + i % 2 for i in range(k)]]
        for pattern, sizes in enumerate(patterns if args.full else patterns[1:]):
            for mask in range(2**k):
                graph, partition = blow_up(quotient, sizes, mask)
                if len(graph) < 2 or not nx.is_connected(graph):
                    continue
                configurations.append(
                    {
                        "quotient_atlas_id": atlas_id,
                        "quotient_edges": list(quotient.edges),
                        "type_sizes": sizes,
                        "clique_mask": mask,
                    }
                )
                volume = 2 * graph.number_of_edges()
                for seed in graph:
                    for alpha in [F(1), F(1, 3), F(1, 64)] if args.full else [F(1, 3), F(1, 64)]:
                        for epsilon in [F(1, 4), F(1, 2 * len(graph)), F(1, 2 * volume)]:
                            dense = (
                                seed == 0
                                and alpha == F(1, 64)
                                and epsilon == F(1, 2 * volume)
                                and mask in [0, 2**k - 1]
                                and pattern == 2
                            )
                            profile = case(
                                graph, partition, seed, alpha, epsilon, counts, work, dense
                            )
                            if dense:
                                profiles.append(
                                    {
                                        "quotient_atlas_id": atlas_id,
                                        "type_sizes": sizes,
                                        "clique_mask": mask,
                                        **profile,
                                    }
                                )
                counts["original_graph_type_configurations"] += 1
        print(
            json.dumps(
                {
                    "quotient_atlas_id": atlas_id,
                    "outputs_so_far": counts["original_ACL_outputs_with_unsupplied_type_promise"],
                }
            ),
            flush=True,
        )
    for power in [20, 128, 1024] if args.full else [20]:
        ledger = Counter()
        oracle = MassiveHub(2**power, ledger)
        state = GroupFrontier(oracle, 0, F(1, 3), F(1, 8), ledger)
        result = state.run()
        assert result["records"] == [(0, F(15, 16))]
        assert oracle.rows == [0] and state.vertices.size == 2
        assert state.live_count == 1 and state.metrics["maximum_transient_response_groups"] == 2
        work.update(ledger)
        counts["private_star_two_type_large_ambient_certificates"] += 1
    private_profiles = []
    for leaves, power in [(4, 20), (16, 128), (64, 1024)] if args.full else [(4, 20)]:
        for alpha in [F(1, 3), F(1, 64), F(1, 2**80)] if args.full else [F(1, 3)]:
            private_profiles.append(private_double_star(leaves, power, alpha, counts, work))
    result = {
        "description": __doc__,
        "full": args.full,
        "source_definition": {
            "url": "https://arxiv.org/pdf/0910.0582v2",
            "pages": [4, 12, 13],
            "scope": "Neighborhood types only; no source preprocessing or runtime import.",
        },
        "parameters": {
            "producer_randomness": "none",
            "accuracy_namespace": "original ACL eps_appr",
            "alphas": ["1", "1/3", "1/64"] if args.full else ["1/3", "1/64"],
            "epsilons": ["1/4", "1/(2*n)", "1/(2*original_volume)"],
            "seeds": "every physical vertex in every recorded configuration",
            "partition_visibility": "validator only; producer gets degree/row oracle",
        },
        "audit_only": dict(counts),
        "charged_implementation_units": dict(work),
        "graph_configurations": configurations,
        "dense_validation_profiles": profiles,
        "private_double_star_profiles": private_profiles,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in [
                "frontier_groups.py",
                "frontier_exact.py",
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
