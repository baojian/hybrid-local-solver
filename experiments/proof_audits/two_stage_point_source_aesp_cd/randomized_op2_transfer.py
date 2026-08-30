#!/usr/bin/env python3
"""Exact audit of the randomized-OP2 to two-stage transfer.

The randomized SDD routine is a source primitive, so this audit does not try
to reimplement it.  Instead it checks the deterministic interface that every
residual-certified call exposes:

* an RPPR reachable face has an exact face-energy gap;
* that gap bounds omitted RPPR amplitude;
* one ordinary principal-PPR solve on the same inner face meets the claimed
  semantic error even when the face does not contain the full RPPR support;
* the threshold-batch cap produces such an inner face on exact rational path
  instances.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import ceil, log, sqrt
from random import Random

try:
    from experiments.proof_audits.two_stage_point_source_aesp_cd.two_stage_composition import (
        boundary,
        degree_unscaled_system,
        obstacle_solution,
        path_graph,
        quadratic_value,
        restricted_solution,
        solve,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from two_stage_composition import (
        boundary,
        degree_unscaled_system,
        obstacle_solution,
        path_graph,
        quadratic_value,
        restricted_solution,
        solve,
    )


def padded(values: dict[int, F], size: int) -> list[F]:
    return [values.get(vertex, F(0)) for vertex in range(size)]


def residual(hessian: list[list[F]], load: list[F], point: list[F]) -> list[F]:
    return [
        load[i] - sum(hessian[i][j] * point[j] for j in range(len(point)))
        for i in range(len(point))
    ]


def random_connected_graph(size: int, rng: Random) -> list[list[int]]:
    adjacency = [[] for _ in range(size)]
    for vertex in range(1, size):
        parent = rng.randrange(vertex)
        adjacency[vertex].append(parent)
        adjacency[parent].append(vertex)
    for left in range(size):
        for right in range(left + 1, size):
            if right in adjacency[left] or rng.random() >= F(1, 5):
                continue
            adjacency[left].append(right)
            adjacency[right].append(left)
    return adjacency


def audit_all_inner_faces() -> tuple[int, int]:
    """Exhaust every positive inner face on small random instances."""
    rng = Random(20260830)
    instances = 0
    faces = 0
    for size in range(4, 9):
        for _ in range(8):
            adjacency = random_connected_graph(size, rng)
            seed = rng.randrange(size)
            alpha = (F(1, 5), F(1, 3), F(1, 2))[rng.randrange(3)]
            degree_seed = len(adjacency[seed])
            rho = F(1, (7 + rng.randrange(5)) * degree_seed)
            degree, hessian, load = degree_unscaled_system(adjacency, alpha, rho, seed)
            ppr_load = [alpha if vertex == seed else F(0) for vertex in range(size)]
            full_ppr = solve(hessian, ppr_load)
            optimum, support, _keys = obstacle_solution(hessian, load)
            optimum_value = quadratic_value(hessian, load, optimum)

            support_tuple = tuple(sorted(support))
            for count in range(1, len(support_tuple) + 1):
                for active_tuple in combinations(support_tuple, count):
                    active = set(active_tuple)
                    if seed not in active:
                        continue
                    values = restricted_solution(hessian, load, active)
                    if any(value <= 0 for value in values.values()):
                        continue
                    face = padded(values, size)
                    gap = quadratic_value(hessian, load, face) - optimum_value
                    assert gap >= 0

                    omitted = [vertex for vertex in support if vertex not in active]
                    delta = max((optimum[vertex] for vertex in omitted), default=F(0))
                    for vertex in omitted:
                        # In degree coordinates x_i=sqrt(d_i)y_i.  Strong
                        # convexity gives alpha*||x-x*||^2 <= 2*gap.
                        assert alpha * degree[vertex] * optimum[vertex] ** 2 <= 2 * gap

                    ppr_values = restricted_solution(hessian, ppr_load, active)
                    principal_ppr = padded(ppr_values, size)
                    assert all(F(0) <= principal_ppr[i] <= full_ppr[i] for i in range(size))
                    semantic_error = max(full_ppr[i] - principal_ppr[i] for i in range(size))
                    assert semantic_error <= rho + delta
                    if semantic_error > rho:
                        assert alpha * (semantic_error - rho) ** 2 <= 2 * gap
                    faces += 1
            instances += 1
    return instances, faces


def threshold_larger_than_half(
    degree_residual: F,
    degree: int,
    threshold_squared: F,
) -> bool:
    """Compare the normalized-coordinate residual to half the threshold."""
    return degree_residual > 0 and 4 * degree_residual**2 > degree * threshold_squared


def capped_threshold_face(
    adjacency: list[list[int]],
    alpha: F,
    rho: F,
    eta: F,
    seed: int = 0,
) -> tuple[int, int, F, F]:
    """Run exact-face threshold batches using the OP2 cap and constants."""
    size = len(adjacency)
    degree, hessian, load = degree_unscaled_system(adjacency, alpha, rho, seed)
    ppr_load = [alpha if vertex == seed else F(0) for vertex in range(size)]
    full_ppr = solve(hessian, ppr_load)
    optimum = solve(hessian, load)
    assert all(value > 0 for value in optimum)
    optimum_value = quadratic_value(hessian, load, optimum)

    eps_obj = alpha * eta**2 / 2
    threshold_squared = alpha * rho * eps_obj / 64
    q_alpha = (sqrt(2 / float(alpha)) - 1) / (sqrt(2 / float(alpha)) + 1)
    phase_cap = ceil(log(64 / float(eps_obj)) / (2 * log(1 / q_alpha)))

    active = {seed}
    stopped_at_cap = False
    for phase in range(phase_cap + 1):
        values = restricted_solution(hessian, load, active)
        assert all(value > 0 for value in values.values())
        face = padded(values, size)
        if phase == phase_cap:
            stopped_at_cap = True
            break
        keys = residual(hessian, load, face)
        batch = {
            vertex
            for vertex in boundary(adjacency, active)
            if threshold_larger_than_half(
                keys[vertex],
                degree[vertex],
                threshold_squared,
            )
        }
        if not batch:
            break
        active |= batch

    face_gap = quadratic_value(hessian, load, face) - optimum_value
    assert face_gap <= eps_obj
    assert active <= set(range(size))

    ppr_values = restricted_solution(hessian, ppr_load, active)
    principal_ppr = padded(ppr_values, size)
    semantic_error = max(full_ppr[i] - principal_ppr[i] for i in range(size))
    assert semantic_error <= rho + eta
    assert all(F(0) <= principal_ppr[i] <= full_ppr[i] for i in range(size))
    assert sum(degree[vertex] for vertex in active) <= 1 / rho
    return len(active), int(stopped_at_cap), face_gap, semantic_error


def audit_incomplete_capped_paths() -> tuple[int, int, F]:
    incomplete = 0
    capped = 0
    largest_error = F(0)
    for size in (24, 32, 40, 48):
        active, stopped_at_cap, _gap, error = capped_threshold_face(
            path_graph(size),
            alpha=F(1, 2),
            rho=F(1, 10**80),
            eta=F(1, 10),
        )
        incomplete += int(active < size)
        capped += stopped_at_cap
        largest_error = max(largest_error, error)
    assert incomplete == 4
    assert capped == 4
    return incomplete, capped, largest_error


def main() -> None:
    instances, faces = audit_all_inner_faces()
    incomplete, capped, largest_error = audit_incomplete_capped_paths()
    print(f"small exact instances: {instances}")
    print(f"positive inner faces audited: {faces}")
    print(f"incomplete capped path faces: {incomplete}/{capped}")
    print(f"largest capped-path semantic error: {float(largest_error):.12g}")
    print("verdict: RPPR face energy safely transfers to an ordinary-PPR Stage II")


if __name__ == "__main__":
    main()
