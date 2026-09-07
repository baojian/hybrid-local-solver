"""Exact generic relative-proximal geometry and terminal-ray normalization.

The supplied oracle is a dense rational validator. Cases include translated
capped VWFs, negative lower bounds, zero gap, affine VWFs with zero total
terminal slope, negative values at zero and extreme common energy scalings.
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

from capped_proximal_budget import capped_energy, capped_reference, dense_laplacian, instance
from diffusion_accuracy_bridge import objective, quadratic
from geometric_value_events import obstacle, solve
import networkx as nx


def multiply(matrix, x):
    return [sum(a * t for a, t in zip(row, x)) for row in matrix]


def universal_policy(kappa):
    steps, doublings = 1, 0
    while steps * steps < 256 * kappa:
        steps *= 2
        doublings += 1
    return steps, 1 / (33 * F(2**30) * kappa**3), doublings


def perturb(minimizer, relative, energy, counts):
    optimum = energy(minimizer)
    assert optimum <= 0
    if optimum == 0:
        counts["zero_normalized_model_optima"] += 1
        return minimizer, optimum
    theta = F(1, 2)
    while theta * theta > relative / (1 + relative):
        theta /= 2
        counts["reference_perturbation_scale_halvings"] += 1
    while True:
        candidate = [(1 - theta) * t for t in minimizer]
        if energy(candidate) <= optimum / (1 + relative):
            return candidate, optimum
        theta /= 2
        counts["reference_perturbation_backtracking"] += 1


class TranslatedCapped:
    def __init__(self, graph, seed, alpha, kappa, profile, scale=F(1)):
        eps = F(1, 8 * sum(dict(graph.degree()).values()))
        n, bar, ge, he, grounding, load = instance(graph, seed, alpha, eps, kappa)
        self.n, self.kappa, self.cap = n, kappa, 1 / bar
        self.ge = [(i, j, w * scale) for i, j, w in ge]
        self.he = [(i, j, w * scale) for i, j, w in he]
        self.g, self.h = dense_laplacian(n, self.ge), dense_laplacian(n, self.he)
        self.grounding, self.load = [scale * t for t in grounding], [scale * t for t in load]
        matrix = [row.copy() for row in self.g]
        for i in range(n):
            matrix[i][i] += self.grounding[i]
        optimum = obstacle(matrix, self.load)
        if profile == "zero":
            base = [F(0)] * n
        elif profile == "half_optimum":
            base = [t / 2 for t in optimum]
        elif profile == "beyond_cap":
            base = [self.cap * (3 if i % 2 else 1) for i in graph]
        elif profile == "zero_gap":
            base = optimum
        else:
            raise AssertionError(profile)
        self.base, self.lower = base, [-t for t in base]
        self.constant = -scale * F(n * (n + 1), 6)
        self.base_energy = capped_energy(self.g, self.grounding, self.cap, self.load, base)
        self.optimum = [a - b for a, b in zip(optimum, base)]
        self.upper_split = max(F(0), max(self.cap - t for t in base))
        gb = multiply(self.g, base)
        self.gradient0 = [
            v + h * min(t, self.cap) - b for v, h, t, b in zip(gb, self.grounding, base, self.load)
        ]
        self.terminal = [h * self.cap - b + v for h, b, v in zip(self.grounding, self.load, gb)]
        self.metadata = {
            "family": "translated capped VWF",
            "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
            "vertices": n,
            "physical_seed": seed,
            "alpha": str(alpha),
            "eps_appr": str(eps),
            "kappa": str(kappa),
            "base_profile": profile,
            "common_energy_scale": str(scale),
        }

    def energy(self, x):
        y = [a + b for a, b in zip(self.base, x)]
        assert all(t >= 0 for t in y)
        return (
            capped_energy(self.g, self.grounding, self.cap, self.load, y)
            - self.base_energy
            + self.constant
        )

    def oracle(self, x, relative, counts):
        physical_center = [a + b for a, b in zip(self.base, x)]
        gx, hx = multiply(self.g, physical_center), multiply(self.h, physical_center)
        load = [b + hi - gi for b, hi, gi in zip(self.load, hx, gx)]
        p = capped_reference(self.h, self.grounding, self.cap, load, counts)
        anchor = capped_energy(self.h, self.grounding, self.cap, load, self.base)

        def normalized(z):
            y = [a + b for a, b in zip(self.base, z)]
            return capped_energy(self.h, self.grounding, self.cap, load, y) - anchor

        return perturb([a - b for a, b in zip(p, self.base)], relative, normalized, counts)


class AffineVWF:
    def __init__(self, graph, kappa, zero_gap, anchor_bits, scale=F(1)):
        self.n, self.kappa = len(graph), kappa
        self.ge = [(i, j, scale * F(1 + (i + j) % 3, 3)) for i, j in graph.edges()]
        self.he = [
            (i, j, w * (1 + (kappa - 1) * F(1 + k % 3, 3))) for k, (i, j, w) in enumerate(self.ge)
        ]
        self.g, self.h = dense_laplacian(self.n, self.ge), dense_laplacian(self.n, self.he)
        target = [F(0) if zero_gap else F((i % 3) - 1) for i in graph]
        self.load = multiply(self.g, target)
        self.lower = [-F(i + 1, 3) for i in graph]
        self.optimum = self.solve(self.g, self.load)
        self.constant = -scale * F(self.n, 7)
        self.upper_split, self.gradient0 = F(0), [-t for t in self.load]
        self.terminal = self.gradient0.copy()
        self.anchor_bits = anchor_bits
        self.metadata = {
            "family": "affine VWF with zero total terminal slope",
            "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
            "vertices": self.n,
            "alpha_eps_physical_seed": "not applicable: generic supplied objective",
            "kappa": str(kappa),
            "zero_gap": zero_gap,
            "oracle_common_shift_power": anchor_bits,
            "common_energy_scale": str(scale),
        }

    def solve(self, matrix, load):
        assert sum(load) == 0
        p = [F(0)] + solve([row[1:] for row in matrix[1:]], load[1:])
        shift = max(a - b for a, b in zip(self.lower, p))
        p = [t + shift for t in p]
        assert multiply(matrix, p) == load
        return p

    def energy(self, x):
        assert all(t >= lo for t, lo in zip(x, self.lower))
        return objective(self.g, self.load, x) + self.constant

    def oracle(self, x, relative, counts):
        gx, hx = multiply(self.g, x), multiply(self.h, x)
        load = [b + hi - gi for b, hi, gi in zip(self.load, hx, gx)]
        p = self.solve(self.h, load)
        if self.anchor_bits is not None:
            p = [t + 2**self.anchor_bits for t in p]
            counts["reference_unbounded_gauge_shifts"] += 1
        counts["reference_affine_laplacian_solves"] += 1
        return perturb(p, relative, lambda z: objective(self.h, load, z), counts)


def normalize(candidate, upper, work):
    least = min(candidate)
    work["canonical_minimum_entries_scanned"] += len(candidate)
    shift = max(F(0), least - upper)
    if shift:
        work["canonical_shifted_entries_allocated"] += len(candidate)
        work["canonical_nonzero_shifts"] += 1
        return [t - shift for t in candidate]
    return candidate


def run_case(data, counts, work):
    n, kappa = data.n, data.kappa
    zero = [F(0)] * n
    start, optimum = data.energy(zero), data.energy(data.optimum)
    gap = start - optimum
    assert gap >= 0 and start == data.constant
    assert sum(data.terminal) >= 0
    assert quadratic(data.h, data.optimum) <= 2 * kappa * gap
    lower_magnitude = max(-t for t in data.lower)
    origin_radius = max(data.upper_split, lower_magnitude)
    cmin = min(w for _, _, w in data.ge)
    resistance_bound = F(n - 1) / cmin
    gradient_mass = sum(abs(t) for t in data.gradient0)
    known_gap_bound = gradient_mass * origin_radius + resistance_bound * gradient_mass**2 / 2
    assert gap <= known_gap_bound
    steps, relative, doublings = universal_policy(kappa)
    internal_absolute = gap / (2**30 * kappa)
    assert 2 * internal_absolute * F(3 * steps * (steps + 1), 2) ** 2 <= kappa * gap / 64
    y, z, previous = zero.copy(), zero.copy(), None
    work["initial_vector_entries_allocated"] += 2 * n
    work["policy_step_doublings"] += doublings
    work["input_vertex_descriptors_read"] += n
    trajectory_hash = hashlib.sha256()
    for k in range(steps):
        weight = F(k + 2, 2)
        x = [(1 - 1 / weight) * a + b / weight for a, b in zip(y, z)]
        if k:
            assert x == [a + F(k - 1, k + 2) * (a - b) for a, b in zip(y, previous)]
            counts["source_extrapolation_index_identities"] += 1
        assert quadratic(data.h, x) <= 64 * kappa**2 * gap
        counts["centers_below_shifted_lower_bound"] += any(t < lo for t, lo in zip(x, data.lower))
        raw, model_optimum = data.oracle(x, relative, counts)
        q = normalize(raw, data.upper_split, work)
        assert all(t >= lo for t, lo in zip(q, data.lower))
        assert min(q) <= data.upper_split
        counts["negative_feasible_iterates"] += min(q) < 0

        def model(v):
            d = [a - b for a, b in zip(v, x)]
            return data.energy(v) + (quadratic(data.h, d) - quadratic(data.g, d)) / 2

        model0 = start + (quadratic(data.h, x) - quadratic(data.g, x)) / 2
        raw_value, normalized_value = model(raw) - model0, model(q) - model0
        assert normalized_value <= raw_value <= model_optimum / (1 + relative)
        assert data.energy(q) <= data.energy(raw)
        assert (
            0
            <= normalized_value - model_optimum
            <= relative * (-normalized_value)
            <= internal_absolute
        )
        assert -model_optimum <= 33 * kappa**2 * gap
        energy = data.energy(q)
        if k == 0:
            assert energy <= start
        else:
            assert energy - optimum <= 8 * kappa * gap / (k + 2) ** 2
        assert energy - optimum <= 2 * kappa * gap
        difference = [a - b for a, b in zip(q, data.optimum)]
        assert quadratic(data.h, difference) <= 2 * kappa * (energy - optimum)
        assert quadratic(data.g, q) <= 12 * kappa * gap
        diameter = max(q) - min(q)
        assert diameter**2 <= resistance_bound * quadratic(data.g, q)
        excess = max(F(0), max(abs(t) for t in q) - origin_radius)
        assert (
            excess**2
            <= 12 * kappa * resistance_bound * gap
            <= 12 * kappa * resistance_bound * known_gap_bound
        )
        counts["complete_generic_proximal_geometry_steps"] += 1
        counts["zero_gap_steps"] += gap == 0
        counts["canonical_model_and_energy_inequalities"] += 1
        new_z = [a + weight * (b - c) for a, b, c in zip(z, q, x)]
        assert new_z == [weight * a - (weight - 1) * b for a, b in zip(q, y)]
        previous, y, z = y, q, new_z
        assert all(isinstance(t, F) for t in x + y + z)
        for t in y:
            for v in [t.numerator, t.denominator]:
                raw_int = abs(v).to_bytes((abs(v).bit_length() + 7) // 8, "big")
                trajectory_hash.update(bytes([v < 0]) + len(raw_int).to_bytes(8, "big") + raw_int)
        work["supplied_gradient_edge_visits"] += len(data.ge) + len(data.he)
        work["normalized_vertex_records"] += n
        work["iteration_vector_entries_allocated"] += 6 * n
        work["relative_reference_oracle_calls"] += 1
    assert data.energy(y) - optimum <= gap / 32
    counts["complete_generic_trajectories"] += 1
    counts["zero_gap_trajectories"] += gap == 0
    counts["zero_total_terminal_slope_trajectories"] += sum(data.terminal) == 0
    counts["signed_lower_domain_trajectories"] += min(data.lower) < 0
    return {
        **data.metadata,
        "steps": steps,
        "relative_tolerance": str(relative),
        "initial_gap": str(gap),
        "explicit_input_gap_upper_bound": str(known_gap_bound),
        "trajectory_fraction_bytes_sha256": trajectory_hash.hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts, work = time.monotonic(), Counter(), Counter()
    max_n = 4 if args.full else 3
    graphs = [g for g in nx.graph_atlas_g() if 2 <= len(g) <= max_n and nx.is_connected(g)]
    for graph in graphs:
        for seed in graph:
            for profile in (
                ["zero", "half_optimum", "beyond_cap"] if args.full else ["half_optimum"]
            ):
                run_case(TranslatedCapped(graph, seed, F(1, 3), F(9, 4), profile), counts, work)
        run_case(TranslatedCapped(graph, 0, F(1, 1009), F(4), "zero_gap"), counts, work)
    structured = []
    for zero_gap in [False, True]:
        for anchor in [None, 512] if args.full else [512]:
            structured.append(
                run_case(
                    AffineVWF(nx.path_graph(4 if args.full else 3), F(4), zero_gap, anchor),
                    counts,
                    work,
                )
            )
    hashes = []
    for power in [-80, 0, 80] if args.full else [-20, 20]:
        record = run_case(
            TranslatedCapped(nx.path_graph(3), 0, F(1, 1009), F(4), "beyond_cap", F(2) ** power),
            counts,
            work,
        )
        hashes.append(record["trajectory_fraction_bytes_sha256"])
        structured.append(record)
    assert len(set(hashes)) == 1
    counts["exact_common_energy_scale_invariance_checks"] += len(hashes) - 1
    result = {
        "audit": "incremental_active_set_sdd.generic_proximal_geometry",
        "arithmetic": "exact fractions",
        "random_seed": None,
        "max_n": max_n,
        "distinct_atlas_graphs": len(graphs),
        "input_family": "translated capped VWFs with signed lower domains, every physical seed through max_n; zero gap, affine zero-total-terminal-slope objectives, huge nullspace shifts and common energy scalings",
        "parameter_profiles": "atlas alpha=1/3,kappa=9/4,eps=1/(8*volume), base zero/half-optimum/beyond-cap; zero-gap alpha=1/1009,kappa=4. Structured profiles are listed explicitly.",
        "stopping_rule": "Least dyadic T with T^2>=256*kappa; universal relative tolerance 1/(33*2^30*kappa^3). Normalize each output along its common terminal ray, and certify every normalized model, gap, seminorm, diameter and input-scale bound exactly.",
        "scope": "Generic supplied-interface geometry and implemented normalization; dense exact proximal candidates and matrix checks are validators. No fast recursive oracle, preconditioner construction, bit-complexity guarantee or local OP3 solver is claimed.",
        "audit_only": dict(counts),
        "supplied_interface_counts": dict(work),
        "structured_cases": structured,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            name: hashlib.sha256(Path(__file__).with_name(name + ".py").read_bytes()).hexdigest()
            for name in [
                "capped_proximal_budget",
                "diffusion_accuracy_bridge",
                "geometric_value_events",
            ]
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
