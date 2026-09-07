"""Exact supplied-graph audit of an explicit original-capped APG tolerance.

Sparse state/instance construction is counted separately from the dense
piece-enumeration reference oracle. This does not implement a fast diffusion
oracle, a preconditioner constructor, or unknown-support graph discovery.
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

from diffusion_accuracy_bridge import objective, quadratic
from geometric_value_events import obstacle, solve
import networkx as nx


def policy(bar, eps, kappa, edges, gap_floor=None):
    assert bar > 0 and eps > 0 and kappa >= 1 and edges >= 1
    steps, doublings = 1, 0
    while steps * steps < 256 * kappa:
        steps *= 2
        doublings += 1
    radius = kappa / (bar * (eps / 2))
    floor = eps / 8 if gap_floor is None else gap_floor
    assert floor > 0
    absolute = floor / (2**30 * kappa**4)
    scale = 9 * kappa * edges * radius**2 / 2 + 1 / (2 * bar)
    return steps, radius, absolute, absolute / scale, scale, doublings


def dense_laplacian(n, edges):
    matrix = [[F(0)] * n for _ in range(n)]
    for i, j, weight in edges:
        matrix[i][i] += weight
        matrix[j][j] += weight
        matrix[i][j] -= weight
        matrix[j][i] -= weight
    return matrix


def sparse_mv(n, edges, vector, work):
    result = [F(0)] * n
    for i, j, weight in edges:
        flow = weight * (vector[i] - vector[j])
        result[i] += flow
        result[j] -= flow
        work["supplied_edge_gradient_visits"] += 1
    return result


def capped_energy(laplacian, grounding, cap, load, x):
    return quadratic(laplacian, x) / 2 + sum(
        h * (t * t - max(F(0), t - cap) ** 2) / 2 - b * t for h, b, t in zip(grounding, load, x)
    )


def capped_reference(laplacian, grounding, cap, load, counts):
    """Exact convex KKT validator, with exhaustive piece fallback."""
    n = len(load)
    matrix = [row.copy() for row in laplacian]
    for i in range(n):
        matrix[i][i] += grounding[i]
    candidate = obstacle(matrix, load)
    counts["reference_uncapped_obstacle_solves"] += 1
    if max(candidate) <= cap:
        counts["reference_uncapped_KKT_successes"] += 1
        return candidate
    guess = tuple(0 if t == 0 else 1 if t <= cap else 2 for t in candidate)
    for state in itertools.chain([guess], itertools.product(range(3), repeat=n)):
        active = [i for i, status in enumerate(state) if status]
        if len(active) == n and all(status == 2 for status in state):
            continue  # Pure Laplacian: positive total terminal slope forbids an optimum.
        principal = [[laplacian[i][j] for j in active] for i in active]
        rhs = [load[i] - (grounding[i] * cap if state[i] == 2 else 0) for i in active]
        for k, i in enumerate(active):
            if state[i] == 1:
                principal[k][k] += grounding[i]
        values = solve(principal, rhs)
        candidate = [F(0)] * n
        for i, t in zip(active, values):
            candidate[i] = t
        counts["reference_piece_linear_systems"] += 1
        if any(
            (status == 1 and not 0 <= t <= cap) or (status == 2 and t < cap)
            for status, t in zip(state, candidate)
        ):
            continue
        slack = [
            sum(a * t for a, t in zip(row, candidate)) + h * min(cap, x) - b
            for row, h, x, b in zip(laplacian, grounding, candidate, load)
        ]
        if all(s == 0 if t > 0 else s >= 0 for s, t in zip(slack, candidate)):
            counts["reference_capped_KKT_successes"] += 1
            counts["reference_optimum_coordinates_beyond_cap"] += sum(t > cap for t in candidate)
            return candidate
    raise AssertionError("No exact capped KKT piece found")


def inexact_reference(laplacian, grounding, cap, load, relative, absolute, mode, counts):
    p = capped_reference(laplacian, grounding, cap, load, counts)
    optimum = capped_energy(laplacian, grounding, cap, load, p)
    assert optimum <= 0
    if optimum == 0:
        return p, optimum, F(0)
    fraction = F(1, 2)
    budget = relative / (1 + relative) if mode == "relative" else absolute / max(F(1), -optimum)
    while fraction * fraction > budget:
        fraction /= 2
        counts["reference_perturbation_scale_halvings"] += 1
    while True:
        q = [(1 - fraction) * t for t in p]
        energy = capped_energy(laplacian, grounding, cap, load, q)
        if (
            (energy <= optimum / (1 + relative))
            if mode == "relative"
            else (energy - optimum <= absolute)
        ):
            break
        fraction /= 2
        counts["reference_objective_backtracking_halvings"] += 1
    assert optimum <= energy <= 0
    counts["nonexact_reference_candidates"] += energy > optimum
    return q, optimum, energy - optimum


def instance(graph, seed, alpha, eps, kappa):
    n = len(graph)
    gamma = (1 - alpha) / (1 + alpha)
    bar = 1 - gamma
    original_edges = [(i, j, gamma) for i, j in graph.edges()]
    preconditioned_edges = [
        (i, j, gamma * (1 + (kappa - 1) * F(1 + index % 3, 3)))
        for index, (i, j) in enumerate(graph.edges())
    ]
    assert all(
        g <= h <= kappa * g for (_, _, g), (_, _, h) in zip(original_edges, preconditioned_edges)
    )
    grounding = [bar * graph.degree(i) for i in graph]
    load = [F(i == seed) - eps * graph.degree(i) / 2 for i in graph]
    return n, bar, original_edges, preconditioned_edges, grounding, load


def trajectory(graph, seed, alpha, eps, kappa, mode, counts, work, initial=None, gap_floor=None):
    n, bar, original_edges, preconditioned_edges, grounding, load = instance(
        graph, seed, alpha, eps, kappa
    )
    g = dense_laplacian(n, original_edges)
    h = dense_laplacian(n, preconditioned_edges)
    matrix = [row.copy() for row in g]
    for i in range(n):
        matrix[i][i] += grounding[i]
    cap = 1 / bar
    exact = obstacle(matrix, load)
    minimum = objective(matrix, load, exact)
    assert eps / 8 < -minimum <= 1 / (2 * bar)
    assert capped_energy(g, grounding, cap, load, exact) == minimum
    assert initial is None or gap_floor is not None
    initial = [F(0)] * n if initial is None else initial
    initial_energy = capped_energy(g, grounding, cap, load, initial)
    gap0 = initial_energy - minimum
    assert initial_energy <= 0 and gap0 > 0
    assert (eps / 8 if gap_floor is None else gap_floor) <= gap0
    initial_error = [a - b for a, b in zip(initial, exact)]
    assert quadratic(h, initial_error) <= 2 * kappa * gap0
    steps, radius, absolute, relative, scale, doublings = policy(
        bar, eps, kappa, len(original_edges), gap_floor
    )
    assert 256 * kappa <= steps**2 < 1024 * kappa
    assert 2 * absolute * F(3 * steps * (steps + 1), 2) ** 2 <= kappa * gap0 / 64
    work["step_count_doublings"] += doublings
    work["explicit_vector_entries_allocated"] += 2 * n
    y, z, previous_y = initial.copy(), initial.copy(), None
    maximum_bits = 0
    for k in range(steps):
        alpha_step = F(k + 2, 2)
        tau = 1 / alpha_step
        x = [(1 - tau) * a + tau * b for a, b in zip(y, z)]
        if k:
            assert x == [a + F(k - 1, k + 2) * (a - b) for a, b in zip(y, previous_y)]
            counts["exact_extrapolation_index_identities"] += 1
        assert all(-radius <= t <= 2 * radius for t in x)
        counts["infeasible_accelerated_centers"] += min(x) < 0
        assert quadratic(h, x) <= 9 * kappa * len(original_edges) * radius**2
        gx = sparse_mv(n, original_edges, x, work)
        hx = sparse_mv(n, preconditioned_edges, x, work)
        shifted = [b + hi - gi for b, hi, gi in zip(load, hx, gx)]
        assert sum(shifted) == sum(load)
        q, prox_minimum, error = inexact_reference(
            h, grounding, cap, shifted, relative, absolute, mode, counts
        )
        model0 = (quadratic(h, x) - quadratic(g, x)) / 2
        original_at_q = capped_energy(g, grounding, cap, load, q)
        normalized_at_q = capped_energy(h, grounding, cap, shifted, q)
        difference = [a - b for a, b in zip(q, x)]
        direct_model = original_at_q + (quadratic(h, difference) - quadratic(g, difference)) / 2
        assert normalized_at_q == direct_model - model0
        assert direct_model >= original_at_q >= minimum
        assert -normalized_at_q <= -prox_minimum <= scale
        if mode == "relative":
            assert normalized_at_q <= prox_minimum / (1 + relative)
            assert error <= relative * (-normalized_at_q) <= absolute
            counts["normalized_relative_to_absolute_certificates"] += 1
        else:
            assert error <= absolute
            counts["absolute_error_stress_certificates"] += 1
        assert error >= 0
        if k == 0:
            assert original_at_q <= initial_energy + absolute
        else:
            assert original_at_q - minimum <= 8 * kappa * gap0 / (k + 2) ** 2
        assert original_at_q - minimum <= 2 * kappa * gap0
        assert original_at_q >= eps * sum(q) / 2 - 1 / (2 * bar)
        assert all(0 <= t <= radius for t in q)
        counts["complete_proximal_model_and_sublevel_certificates"] += 1
        new_z = [a + alpha_step * (b - c) for a, b, c in zip(z, q, x)]
        assert new_z == [alpha_step * a - (alpha_step - 1) * b for a, b in zip(q, y)]
        previous_y, y, z = y, q, new_z
        assert all(isinstance(t, F) for t in x + y + z)
        work["explicit_vector_entries_allocated"] += 6 * n
        work["normalized_VWF_vertex_records"] += n
        work["normalized_VWF_piece_descriptors"] += 2 * n
        work["relative_or_absolute_reference_oracle_calls"] += 1
        maximum_bits = max(maximum_bits, *(t.denominator.bit_length() for t in y))
    assert capped_energy(g, grounding, cap, load, y) - minimum <= gap0 / 32
    counts["complete_accelerated_trajectories"] += 1
    counts["nonzero_restart_trajectories"] += any(initial)
    work["final_output_entries"] += n
    return y, {
        "vertices": n,
        "edges": len(original_edges),
        "physical_seed": seed,
        "alpha": str(alpha),
        "eps_appr": str(eps),
        "kappa": str(kappa),
        "oracle_mode": mode,
        "steps": steps,
        "known_radius": str(radius),
        "known_absolute_error": str(absolute),
        "known_relative_error": str(relative),
        "maximum_validator_denominator_bits": maximum_bits,
    }


def standalone_centers(graph, counts):
    n, bar, ge, he, grounding, load = instance(graph, 0, F(1, 3), F(1, 2 * graph.degree(0)), F(4))
    g, h, cap = dense_laplacian(n, ge), dense_laplacian(n, he), 1 / bar
    for profile in range(4):
        x = [
            cap * ((-3 if (i + profile) % 2 else 4) if profile < 2 else -3 if profile == 2 else 4)
            for i in graph
        ]
        shifted = [
            b + sum((hi - gi) * t for hi, gi, t in zip(hr, gr, x)) for b, hr, gr in zip(load, h, g)
        ]
        p = capped_reference(h, grounding, cap, shifted, counts)
        energy = capped_energy(h, grounding, cap, shifted, p)
        model0 = (quadratic(h, x) - quadratic(g, x)) / 2
        d = [a - b for a, b in zip(p, x)]
        assert (
            energy
            == capped_energy(g, grounding, cap, load, p)
            + (quadratic(h, d) - quadratic(g, d)) / 2
            - model0
        )
        counts["negative_individual_proximal_tail_slopes"] += sum(
            hh * cap - b < 0 for hh, b in zip(grounding, shifted)
        )
        counts["standalone_infeasible_center_model_certificates"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    max_n = 5 if args.full else 3
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed in graph:
            profiles = [
                (F(1, 3), F(9, 4), F(1, 2 * graph.degree(seed))),
                (F(1, 1009), F(4), F(1, 8 * sum(dict(graph.degree()).values()))),
                (F(1008, 1009), F(1), F(1, 2 * graph.degree(seed))),
            ]
            for alpha, kappa, eps in profiles if args.full else profiles[:1]:
                trajectory(graph, seed, alpha, eps, kappa, "relative", counts, work)
        if len(graph) <= 4:
            standalone_centers(graph, counts)
    structured = []
    for graph in (
        [nx.path_graph(5), nx.star_graph(4), nx.cycle_graph(5)] if args.full else [nx.path_graph(3)]
    ):
        structured.append(
            trajectory(
                graph,
                0,
                F(1, 3),
                F(1, 8 * sum(dict(graph.degree()).values())),
                F(16),
                "absolute",
                counts,
                work,
            )[1]
        )
    result = {
        "audit": "incremental_active_set_sdd.capped_proximal_budget",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "graph_family": "connected atlas through max_n, every physical seed, explicit paired parameter profiles; path/star/cycle absolute-error stress and standalone infeasible centers",
        "max_n": max_n,
        "distinct_atlas_graphs": len(graphs),
        "parameter_profiles": "(alpha,kappa,eps)=(1/3,9/4,1/(2*d_seed)),(1/1009,4,1/(8*volume)),(1008/1009,1,1/(2*d_seed)); fast uses first profile",
        "stopping_rule": "Least dyadic T with T^2>=256*kappa; relative oracle tolerance a/B, a=eps/(8*2^30*kappa^4), B=9*kappa*m*R^2/2+1/(2*bar), R=kappa/(bar*lambda). Verify every normalized model, absolute error, original sublevel, extrapolation index and final 1/32 gap contraction.",
        "scope": "Explicit tolerance and sparse supplied-instance state construction. Dense obstacle/piece enumeration and perturbed oracle candidates are validators; no fast oracle, preconditioner constructor, recursive numerical theorem or local OP3 solver is implemented.",
        "audit_only": dict(counts),
        "supplied_algorithm_counts": dict(work),
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in ["diffusion_accuracy_bridge", "geometric_value_events"]
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
