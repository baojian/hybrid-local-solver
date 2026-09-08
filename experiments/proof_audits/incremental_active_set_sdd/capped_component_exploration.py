"""A charged local whole-component gate with an explicit AVL label map.

Return the entire graph if its original volume fits the supplied budget,
or witness a larger original volume using distinct queried degrees.
Partial exploration is never declared a significant-potential envelope.
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

from small_alpha_floor import LocalRows
from supplied_envelope_work import MassiveHub
import networkx as nx


class Node:
    __slots__ = ("label", "degree", "left", "right", "height", "next", "row", "complete")

    def __init__(self, label, degree):
        self.label, self.degree = label, degree
        self.left, self.right, self.next, self.row = None, None, None, None
        self.height, self.complete = 1, False


class AVLRecords:
    def __init__(self, oracle, work):
        self.oracle, self.work, self.root = oracle, work, None
        self.head, self.tail = None, None
        self.size, self.volume = 0, 0
        work["gate_record_words_reserved"] += 10
        work["gate_map_header_initialization"] += 10

    def height(self, node):
        self.work["gate_avl_height_reads"] += 2
        return 0 if node is None else node.height

    def fix(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        self.work["gate_avl_height_comparison_and_write"] += 4

    def left(self, node):
        other = node.right
        node.right, other.left = other.left, node
        self.fix(node)
        self.fix(other)
        self.work["gate_avl_rotation_pointer_operations"] += 6
        return other

    def right(self, node):
        other = node.left
        node.left, other.right = other.right, node
        self.fix(node)
        self.fix(other)
        self.work["gate_avl_rotation_pointer_operations"] += 6
        return other

    def insert(self, node, label):
        self.work["gate_avl_call_frame_and_branch_operations"] += 6
        if node is None:
            degree = self.oracle.degree(label)
            assert degree >= 1
            record = Node(label, degree)
            self.size += 1
            self.volume += degree
            if self.tail is None:
                self.head = record
            else:
                self.tail.next = record
            self.tail = record
            self.work["gate_record_words_reserved"] += 8
            self.work["gate_new_record_degree_volume_and_queue_updates"] += 20
            return record, record, True
        self.work["gate_avl_label_comparisons"] += 2
        if label == node.label:
            return node, node, False
        if label < node.label:
            node.left, record, fresh = self.insert(node.left, label)
        else:
            node.right, record, fresh = self.insert(node.right, label)
        self.work["gate_avl_child_pointer_return_operations"] += 4
        if fresh:
            self.fix(node)
            balance = self.height(node.left) - self.height(node.right)
            self.work["gate_avl_balance_arithmetic_and_comparisons"] += 4
            if balance > 1:
                if self.height(node.left.left) < self.height(node.left.right):
                    node.left = self.left(node.left)
                node = self.right(node)
            elif balance < -1:
                if self.height(node.right.right) < self.height(node.right.left):
                    node.right = self.right(node.right)
                node = self.left(node)
        return node, record, fresh

    def ensure(self, label):
        self.root, record, _ = self.insert(self.root, label)
        self.work["gate_avl_root_and_return_operations"] += 4
        return record

    def ordered(self):
        output, stack = [None] * self.size, [None] * self.root.height
        self.work["gate_terminal_array_words_reserved"] += self.size + self.root.height + 4
        self.work["gate_terminal_array_initialization"] += self.size + self.root.height + 4
        node, depth, position = self.root, 0, 0
        while node is not None or depth:
            while node is not None:
                stack[depth] = node
                depth += 1
                node = node.left
                self.work["gate_terminal_tree_descent_operations"] += 5
            depth -= 1
            node = stack[depth]
            output[position] = node
            position += 1
            node = node.right
            self.work["gate_terminal_tree_output_operations"] += 7
        assert position == self.size
        return output


def explore(oracle, seed, budget, work):
    assert budget >= 1
    records = AVLRecords(oracle, work)
    records.ensure(seed)
    started_volume = 0

    def report(complete):
        work["gate_terminal_report_fields"] += 8
        return {
            "complete": complete,
            "records": records.ordered(),
            "known_volume": records.volume,
            "started_row_volume": started_volume,
            "map": records,
        }

    work["gate_known_volume_comparisons"] += 1
    if records.volume > budget:
        return report(False)
    while records.head is not None:
        record = records.head
        records.head = record.next
        if records.head is None:
            records.tail = None
        record.next = None
        started_volume += record.degree
        assert started_volume <= records.volume <= budget
        # Charge the whole row before reading its first entry, even if
        # the new-degree witness later stops in the middle of this row.
        work["gate_full_original_row_degree_charged"] += record.degree
        record.row = [None] * record.degree
        work["gate_row_buffer_words_reserved"] += record.degree
        work["gate_row_initialization_and_queue_pop"] += record.degree + 12
        number = 0
        for label in oracle.row(record.label):
            assert number < record.degree
            neighbor = records.ensure(label)
            record.row[number] = neighbor
            number += 1
            work["gate_incidence_pointer_and_volume_check"] += 5
            if records.volume > budget:
                return report(False)
        assert number == record.degree
        record.complete = True
        work["gate_completed_row_flag_and_check"] += 3
    return report(True)


def validate_avl(records, counts):
    seen = []

    def visit(node, lo, hi):
        if node is None:
            return 0, 0
        assert (lo is None or lo < node.label) and (hi is None or node.label < hi)
        left, nl = visit(node.left, lo, node.label)
        seen.append(node)
        right, nr = visit(node.right, node.label, hi)
        assert abs(left - right) <= 1 and node.height == 1 + max(left, right)
        return node.height, 1 + nl + nr

    height, size = visit(records.root, None, None)
    assert size == records.size and height <= 1 + 2 * (size + 1).bit_length()
    assert sum(node.degree for node in seen) == records.volume
    counts["exact_AVL_balance_order_height_and_volume_checks"] += 1
    return seen


def audit_case(graph, seed, budget, counts, work):
    access = LocalRows(graph, work)
    before = sum(work.values())
    result = explore(access, seed, budget, work)
    records = result["records"]
    assert records == validate_avl(result["map"], counts)
    labels = {node.label for node in records}
    assert len(labels) == len(records) <= budget + 1
    assert set(access.degree_log) == labels and len(access.degree_log) == len(labels)
    assert len(set(access.row_log)) == len(access.row_log)
    assert sum(graph.degree(i) for i in access.row_log) == result["started_row_volume"] <= budget
    assert result["known_volume"] == sum(graph.degree(i) for i in labels)
    assert result["complete"] == (sum(dict(graph.degree()).values()) <= budget)
    if result["complete"]:
        assert labels == set(graph) and set(access.row_log) == labels
        for node in records:
            assert node.complete and {r.label for r in node.row} == set(graph[node.label])
        counts["complete_original_component_certificates"] += 1
    else:
        assert result["known_volume"] > budget
        counts["distinct_degree_large_component_witnesses"] += 1
    bound = 1000 * (1 + budget) * (2 + int(budget + 1).bit_length())
    assert sum(work.values()) - before <= bound
    counts["component_gate_cases"] += 1
    counts["one_time_degree_queries"] += len(access.degree_log)
    counts["one_time_started_rows"] += len(access.row_log)
    counts["full_row_degree_charged_even_on_partial_stop"] += result["started_row_volume"]


class PrivatePath:
    def __init__(self, size, work):
        self.size, self.work, self.rows = size, work, []

    def degree(self, label):
        assert 0 <= label < self.size
        self.work["original_degree_queries"] += 1
        return 1 if label in (0, self.size - 1) else 2

    def row(self, label):
        self.rows.append(label)
        self.work["original_row_queries"] += 1
        if label > 0:
            self.work["original_adjacency_entries"] += 1
            yield label - 1
        if label + 1 < self.size:
            self.work["original_adjacency_entries"] += 1
            yield label + 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    for graph in nx.graph_atlas_g():
        if not 2 <= len(graph) <= (6 if args.full else 3) or not nx.is_connected(graph):
            continue
        volume = 2 * graph.number_of_edges()
        for seed in graph:
            for budget in [1, F(volume - 1, 2), volume - 1, volume, volume + 1]:
                audit_case(graph, seed, max(F(1), budget), counts, work)
    for size in [31, 257, 4096] if args.full else [31]:
        graph = nx.path_graph(size)
        for budget in [16, 2 * size - 3, 2 * size - 2]:
            audit_case(graph, 0, budget, counts, work)
    rng = random.Random(20260908)
    for _ in range(32 if args.full else 3):
        labels = list(range(17))
        rng.shuffle(labels)
        graph = nx.relabel_nodes(nx.path_graph(17), {i: labels[i] * 2**80 for i in range(17)})
        audit_case(graph, labels[0] * 2**80, 32, counts, work)
        counts["permuted_large_label_AVL_cases"] += 1
    for size in [2**20, 2**80, 2**1024]:
        access = PrivatePath(size, work)
        result = explore(access, 0, 64, work)
        assert not result["complete"] and result["known_volume"] == 65
        assert result["started_row_volume"] == 63 and max(access.rows) == 31
        counts["private_huge_path_bounded_explorations"] += 1
        access = MassiveHub(size, work)
        result = explore(access, 0, 64, work)
        assert not result["complete"] and access.rows == [0]
        assert result["started_row_volume"] == 1
        counts["private_huge_hub_witnesses_before_hub_row"] += 1
    result = {
        "audit": "incremental_active_set_sdd.capped_component_exploration",
        "scope": "Implemented AVL map, one-time original degree/row access, capped queue and original-volume witness. No envelope is inferred from a partial exploration.",
        "parameters": {
            "full": args.full,
            "alpha": "not used",
            "epsilon": "budget B=4/eps_appr in reduction",
            "random_seed": 20260908,
        },
        "audit_only": dict(counts),
        "charged_work": dict(work),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in ["small_alpha_floor.py", "supplied_envelope_work.py"]
        },
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        ),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"audit_only": dict(counts), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
