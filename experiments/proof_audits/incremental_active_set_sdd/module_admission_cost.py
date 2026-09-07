"""Legal two-star admissions, genuine curve costs and residual-mass budgets.

This is a supplied-family diagnostic, not a local solver or a general
amortization theorem. Original degrees include all future core vertices.
Reference curve construction and KKT validation are charged separately
from the three explicitly executed union-update alternatives.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from module_curve_removal import RemovalArena, certify, remove_response
from persistent_affine_tree import Arena, size
from persistent_module_response import PersistentModules, add_zero_left_response
from recursive_module_response import supplied_decomposition
import networkx as nx


def family(k, future, profile):
    # Universal 0, centers 1 and 2, k old leaves on each side, then twins.
    old_a = list(range(3, 3 + k))
    old_b = list(range(3 + k, 3 + 2 * k))
    twins = list(range(3 + 2 * k, 3 + 2 * k + future))
    core = nx.Graph()
    core.add_nodes_from(range(3 + 2 * k + future))
    core.add_edges_from((0, i) for i in core if i)
    core.add_edges_from((1, i) for i in old_a + twins)
    core.add_edges_from((2, i) for i in old_b)
    q = dict.fromkeys(core, 0)
    for r, i in enumerate(old_a):
        q[i] = r + 1 if profile == "unequal" else 1
    for r, i in enumerate(old_b):
        q[i] = 2 * r + 1 if profile == "unequal" else 1
    degrees = {i: core.degree(i) + q[i] for i in core}
    return core, q, degrees, {1, *old_a, *twins}, {2, *old_b}, old_a, twins


def response(core, vertices, degrees, q, seed, alpha, lam, references):
    if not vertices:
        return None, {}
    graph = core.subgraph(vertices)
    nodes, _ = supplied_decomposition(graph)
    state = PersistentModules(
        nodes, {i: degrees[i] for i in vertices}, {i: q[i] for i in vertices}, seed, alpha, lam
    )
    values = state.recover()
    references.update(state.arena.counts)
    return state.curves[-1], values


def validate_original(core, q, degrees, seed, gamma, lam, values, counts):
    """Direct full original KKT equations, including every pendant coordinate."""
    residual_mass = physical_mass = F(0)
    residuals = {}
    for i in core:
        u = values.get(i, F(0))
        leaf = max(F(0), gamma * u - lam)
        residual = F(i == seed) - degrees[i] * u
        residual += gamma * (sum(values.get(j, F(0)) for j in core[i]) + q[i] * leaf)
        assert residual >= 0
        if u:
            assert residual == lam * degrees[i]
        elif i in values:
            assert residual <= lam * degrees[i]
        leaf_residual = gamma * u - leaf
        assert leaf_residual == lam if leaf else 0 <= leaf_residual <= lam
        residual_mass += residual + q[i] * leaf_residual
        physical_mass += degrees[i] * u + q[i] * leaf
        residuals[i] = residual
        counts["original_core_and_group_KKT_checks"] += 1
    assert residual_mass == 1 - (1 - gamma) * physical_mass <= 1
    counts["original_residual_mass_identities"] += 1
    return residuals


def union_alternatives(old_a, new_a, b, counts):
    """Execute all available routes, with no stale knots or large-curve scans."""
    rows = []
    for route in ["remove_then_add", "new_a_plus_b", "b_plus_new_a"]:
        arena = RemovalArena()
        a0, a1, other = [c.with_arena(arena) for c in [old_a, new_a, b]]
        if route == "remove_then_add":
            # Old state is supplied; its initialization is not a new update.
            init = Arena()
            old_sum = add_zero_left_response(old_a.with_arena(init), b.with_arena(init))
            result = remove_response(old_sum.with_arena(arena), a0)
            result = add_zero_left_response(result, a1)
        elif route == "new_a_plus_b":
            result = add_zero_left_response(a1, other)
        else:
            result = add_zero_left_response(other, a1)
        ref = Arena()
        expected = add_zero_left_response(new_a.with_arena(ref), b.with_arena(ref))
        certify(result, expected, counts)
        streamed = arena.counts["merged_light_knots"] + arena.counts["removed_child_knots_streamed"]
        rows.append(
            {
                "route": route,
                "streamed_knots": streamed,
                "allocated_nodes": arena.counts["node_allocations"],
                "counts": dict(arena.counts),
            }
        )
    assert [r["streamed_knots"] for r in rows] == [
        size(old_a.root) + size(new_a.root),
        size(b.root),
        size(new_a.root),
    ]
    return rows


def trajectory(k, future, profile, seed, alpha, scale, priority, counts, references):
    core, q, degrees, side_a, side_b, old_a, twins = family(k, future, profile)
    volume = sum(degrees.values()) + sum(q.values())
    lam = F(1, scale * volume)
    gamma = (1 - alpha) / (1 + alpha)
    reached = {seed}
    values = {seed: F(1, degrees[seed]) - lam}
    assert values[seed] > 0
    order = [seed]
    updates = []
    residuals = validate_original(core, q, degrees, seed, gamma, lam, values, counts)
    while True:
        positive = [i for i in core if i not in reached and residuals[i] > lam * degrees[i]]
        counts["reference_candidate_scans"] += len(core)
        if not positive:
            break
        if priority == "old_first":
            j = min(positive, key=lambda i: (i in twins, -q[i], i))
        else:
            j = min(positive, key=lambda i: (i not in twins, i))
        assert residuals[j] - lam * degrees[j] > 0
        before_values = values
        before_a = reached & side_a
        reached = reached | {j}
        _, values = response(core, reached, degrees, q, seed, alpha, lam, references)
        assert all(values[i] > 0 for i in reached)
        assert all(values[i] >= before_values[i] for i in before_values)
        order.append(j)
        counts["strict_original_core_admissions"] += 1
        # Core-kernel construction includes all its ordinary private leaves.
        # It does not assert that those rows were separately admitted/read.
        if j in twins and before_a and reached & side_b:
            a0, _ = response(core, before_a, degrees, q, seed, alpha, lam, references)
            a1, _ = response(core, reached & side_a, degrees, q, seed, alpha, lam, references)
            b, _ = response(core, reached & side_b, degrees, q, seed, alpha, lam, references)
            routes = union_alternatives(a0, a1, b, counts)
            known_q = [q[i] for i in old_a if i in before_values and before_values[i] > 0]
            residual_twin = gamma * (before_values.get(0, F(0)) + before_values.get(1, F(0)))
            missing = sum(i not in before_values for i in twins)
            assert missing * residual_twin <= 1
            assert size(a1.root) <= 2 * len(known_q) + 2
            if known_q:
                largest_q = max(known_q)
                assert largest_q >= len(known_q)
                assert residual_twin > lam * (2 + largest_q)
                assert missing * lam * (2 + largest_q) < 1
                counts["degree_two_twin_residual_budgets"] += 1
                assert size(a1.root) < 2 / (lam * missing)
            else:
                largest_q = None
            counts["genuine_event_cardinality_bounds"] += 1
            updates.append(
                {
                    "admitted": j,
                    "original_degree": degrees[j],
                    "old_a_events": size(a0.root),
                    "new_a_events": size(a1.root),
                    "b_events": size(b.root),
                    "cheapest_streamed_knots": min(r["streamed_knots"] for r in routes),
                    "missing_twins_before": missing,
                    "largest_positive_old_a_pendant_count": largest_q,
                    "twin_residual_before": str(residual_twin),
                    "routes": routes,
                }
            )
        residuals = validate_original(core, q, degrees, seed, gamma, lam, values, counts)
    assert all(residuals[i] <= lam * degrees[i] for i in core if i not in reached)
    positive_volume = sum(degrees[i] for i in reached)
    positive_volume += sum(q[i] for i in reached if gamma * values[i] > lam)
    assert lam * positive_volume < 1
    counts["complete_legal_admission_trajectories"] += 1
    measured = len(updates)
    harmonic = sum((F(1, j) for j in range(1, measured + 1)), F(0))
    streamed = sum(r["cheapest_streamed_knots"] for r in updates)
    assert streamed <= 2 * measured + 2 * harmonic / lam
    counts["cumulative_harmonic_stream_bounds"] += 1
    return {
        "k": k,
        "future_twins": future,
        "pendant_profile": profile,
        "physical_seed": seed,
        "alpha": str(alpha),
        "lambda": str(lam),
        "priority": priority,
        "original_total_volume": volume,
        "final_positive_volume": positive_volume,
        "core_admission_order": order,
        "measured_union_updates": len(updates),
        "total_cheapest_streamed_knots": streamed,
        "harmonic_stream_upper_bound": str(2 * measured + 2 * harmonic / lam),
        "maximum_cheapest_knots_per_degree": str(
            max(
                (F(r["cheapest_streamed_knots"], r["original_degree"]) for r in updates),
                default=F(0),
            )
        ),
        "updates": updates,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    counts, references = Counter(), Counter()
    records = []
    sizes = [2, 4, 8, 12] if args.full else [2, 4]
    for k in sizes:
        future = k * k
        _, q, degrees, *_ = family(k, future, "unequal")
        volume = sum(degrees.values()) + sum(q.values())
        alphas = (
            [F(1, 3), F(1, 1 + 8 * volume), F(1, 1 + volume * volume)]
            if args.full
            else [F(1, 1 + 8 * volume)]
        )
        for alpha, scale, priority, seed in itertools.product(
            alphas, [2, 8], ["old_first", "twins_first"], [0, 1]
        ):
            records.append(
                trajectory(k, future, "unequal", seed, alpha, scale, priority, counts, references)
            )
    result = {
        "audit": "incremental_active_set_sdd.module_admission_cost",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph_family": "universal core vertex joined to two stars, unequal private leaves, k^2 degree-two future twins in star A",
        "stopping_rule": "every unknown core original gate <= lambda*d; all reached cores positive, private leaves recovered through exact kernels",
        "scope": "Supplied-family legal-trajectory diagnostic. Three explicit union-update routes and residual budget; no local algorithm, general upper bound or lower bound.",
        "audit_only": dict(counts),
        "reference_curve_construction_counts": dict(references),
        "trajectories": records,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "module_curve_removal",
                "persistent_affine_tree",
                "persistent_module_response",
                "recursive_module_response",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
