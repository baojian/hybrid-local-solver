#!/usr/bin/env python3
"""Dense audit for the literal exact-prox safe envelope.

This is a reproducible counterexample search, not a charged sparse solver.
It implements canonical single-source RPPR on finite simple unit graphs,
exact obstacle proximal calls, one-pass peeling, the positive barrier, safe
reflection, the maximal scalar ray, their coordinatewise envelope, and the
exact greatest safe box as an oracle comparator.

Only NumPy is required.  Every reported envelope iterate is checked against
the subsolution, support, monotonicity, complementarity-gap, and alpha-free
two-step identities used in the accompanying proof notes.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass

import numpy as np


Array = np.ndarray


def graph(vertex_count: int, edges: list[tuple[int, int]]) -> Array:
    adjacency = np.zeros((vertex_count, vertex_count), dtype=float)
    for left, right in edges:
        if left == right:
            raise ValueError("graphs must be simple")
        adjacency[left, right] = 1.0
        adjacency[right, left] = 1.0
    if np.any(adjacency.sum(axis=1) == 0):
        raise ValueError("graphs must have no isolated vertices")
    return adjacency


def path(vertex_count: int) -> Array:
    return graph(vertex_count, [(i, i + 1) for i in range(vertex_count - 1)])


def cycle(vertex_count: int) -> Array:
    return graph(
        vertex_count,
        [(i, (i + 1) % vertex_count) for i in range(vertex_count)],
    )


def star(leaves: int) -> Array:
    return graph(leaves + 1, [(0, i) for i in range(1, leaves + 1)])


def broom(handle: int, leaves: int) -> Array:
    # The source is endpoint zero; the leaf fan is attached at handle-1.
    edges = [(i, i + 1) for i in range(handle - 1)]
    edges.extend((handle - 1, handle + i) for i in range(leaves))
    return graph(handle + leaves, edges)


def lollipop(clique: int, tail: int) -> Array:
    edges = [(i, j) for i in range(clique) for j in range(i + 1, clique)]
    edges.append((clique - 1, clique))
    edges.extend((clique + i, clique + i + 1) for i in range(tail - 1))
    return graph(clique + tail, edges)


def barbell(clique: int, bridge: int) -> Array:
    left = list(range(clique))
    middle = list(range(clique, clique + bridge))
    right = list(range(clique + bridge, 2 * clique + bridge))
    edges = [(i, j) for p, i in enumerate(left) for j in left[p + 1 :]]
    edges.extend((i, j) for p, i in enumerate(right) for j in right[p + 1 :])
    chain = [left[-1], *middle, right[0]]
    edges.extend(zip(chain, chain[1:]))
    return graph(2 * clique + bridge, list(edges))


def binary_tree(depth: int) -> Array:
    vertex_count = 2 ** (depth + 1) - 1
    edges = []
    for parent in range(2**depth - 1):
        edges.append((parent, 2 * parent + 1))
        edges.append((parent, 2 * parent + 2))
    return graph(vertex_count, edges)


def comb(spine: int, tooth: int) -> Array:
    edges = [(i, i + 1) for i in range(spine - 1)]
    next_vertex = spine
    for root in range(spine):
        previous = root
        for _ in range(tooth):
            edges.append((previous, next_vertex))
            previous = next_vertex
            next_vertex += 1
    return graph(next_vertex, edges)


def alternating_fans(blocks: int, small: int, large: int) -> Array:
    """A path of articulation hubs with alternating leaf fans."""
    edges = [(i, i + 1) for i in range(blocks - 1)]
    next_vertex = blocks
    for hub in range(blocks):
        leaf_count = small if hub % 2 == 0 else large
        for _ in range(leaf_count):
            edges.append((hub, next_vertex))
            next_vertex += 1
    return graph(next_vertex, edges)


def direct_peeling_slow_graph() -> Array:
    """The five-vertex graph carrying the direct-gradient PeelingLC slow ray."""
    return graph(
        5,
        [(0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
    )


def random_connected(vertex_count: int, probability: float, seed: int) -> Array:
    rng = np.random.default_rng(seed)
    edges = [(i, i + 1) for i in range(vertex_count - 1)]
    present = set(edges)
    for i in range(vertex_count):
        for j in range(i + 1, vertex_count):
            if (i, j) not in present and rng.random() < probability:
                edges.append((i, j))
    return graph(vertex_count, edges)


def family(name: str, first: int, second: int, seed: int) -> Array:
    if name == "path":
        return path(first)
    if name == "cycle":
        return cycle(first)
    if name == "star":
        return star(first)
    if name == "broom":
        return broom(first, second)
    if name == "lollipop":
        return lollipop(first, second)
    if name == "barbell":
        return barbell(first, second)
    if name == "binary-tree":
        return binary_tree(first)
    if name == "comb":
        return comb(first, second)
    if name == "alternating-fans":
        return alternating_fans(first, max(1, second // 3), second)
    if name == "direct-peeling-five":
        return direct_peeling_slow_graph()
    if name == "random":
        return random_connected(first, second / 100.0, seed)
    raise ValueError(f"unknown family: {name}")


def canonical_operator(adjacency: Array, alpha: float) -> tuple[Array, Array, Array]:
    degrees = adjacency.sum(axis=1)
    roots = np.sqrt(degrees)
    normalized = adjacency / np.outer(roots, roots)
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    matrix = diagonal * np.eye(len(adjacency)) - coupling * normalized
    return matrix, degrees, roots


def obstacle_solution(matrix: Array, load: Array, tolerance: float = 1.0e-12) -> Array:
    """Monotone principal active-set solve for a Stieltjes obstacle LCP."""
    face = list(map(int, np.flatnonzero(load > tolerance)))
    solution = np.zeros(len(load))
    while face:
        solution[:] = 0.0
        block = matrix[np.ix_(face, face)]
        solution[face] = np.linalg.solve(block, load[face])
        if np.min(solution[face]) < -2.0e-9:
            raise AssertionError("active-set solution lost positivity")
        exterior = np.array(sorted(set(range(len(load))) - set(face)), dtype=int)
        if not len(exterior):
            break
        residual = load[exterior] - matrix[np.ix_(exterior, face)] @ solution[face]
        admitted = exterior[residual > tolerance]
        if not len(admitted):
            break
        face.extend(map(int, admitted))
    return solution


def objective(matrix: Array, load: Array, state: Array) -> float:
    return float(0.5 * state @ matrix @ state - load @ state)


def exact_safe_box(
    matrix: Array, load: Array, previous: Array, current: Array, theta: float
) -> tuple[Array, float]:
    trial = current + theta * (current - previous)
    support = np.flatnonzero(current > 1.0e-14)
    safe = np.zeros_like(current)
    if not len(support):
        return safe, 0.0
    block = matrix[np.ix_(support, support)]
    raw = load[support] - block @ trial[support]
    correction = obstacle_solution(block, -raw)
    safe[support] = trial[support] - correction
    slack = load[support] - block @ safe[support]
    return safe, max(0.0, float(correction @ slack))


@dataclass
class PeelResult:
    safe: Array
    gap: float
    correction: Array
    slack: Array
    freeze_times: Array
    frozen: int


def oriented_event_ledgers(
    matrix: Array,
    direction: Array,
    freeze_times: Array,
    theta: float,
    support: Array,
) -> tuple[float, float, float, float]:
    """Return gap, edge-TV, Dirichlet, and square-TV event expressions."""
    gap = 0.0
    edge_tv = 0.0
    dirichlet = 0.0
    square_tv = 0.0
    correction_time = theta - freeze_times
    indices = list(map(int, support))
    for position, left in enumerate(indices):
        for right in indices[position + 1 :]:
            if matrix[left, right] >= 0.0:
                continue
            weight = -matrix[left, right] * direction[left] * direction[right]
            difference = abs(correction_time[left] - correction_time[right])
            gap += weight * max(correction_time[left], correction_time[right]) * difference
            edge_tv += weight * difference
            dirichlet += weight * difference * difference
            square_tv += weight * abs(
                correction_time[left] ** 2 - correction_time[right] ** 2
            )
    return gap, edge_tv, dirichlet, square_tv


def peel(
    matrix: Array, load: Array, previous: Array, current: Array, theta: float
) -> PeelResult:
    trial = current + theta * (current - previous)
    support = np.flatnonzero(current > 1.0e-14)
    safe = np.zeros_like(current)
    correction_full = np.zeros_like(current)
    slack_full = np.zeros_like(current)
    freeze_full = np.full(len(current), theta)
    if not len(support):
        return PeelResult(safe, 0.0, correction_full, slack_full, freeze_full, 0)

    block = matrix[np.ix_(support, support)]
    direction = current[support] - previous[support]
    starting_slack = load[support] - block @ current[support]
    increment = np.zeros(len(support))
    moving = set(map(int, np.flatnonzero(direction > 1.0e-15)))
    elapsed = 0.0
    freeze = np.full(len(support), theta)
    scale = max(1.0, float(np.max(np.abs(starting_slack))))

    while moving and elapsed < theta - 2.0e-14:
        moving_direction = np.zeros(len(support))
        moving_indices = np.array(sorted(moving), dtype=int)
        moving_direction[moving_indices] = direction[moving_indices]
        pressure = block @ moving_direction
        slack = starting_slack - block @ increment
        candidates = [
            (elapsed + max(0.0, float(slack[index])) / float(pressure[index]), index)
            for index in moving
            if pressure[index] > 1.0e-14 * scale
        ]
        if not candidates:
            increment += (theta - elapsed) * moving_direction
            elapsed = theta
            break
        hit = min(time for time, _ in candidates)
        if hit >= theta - 2.0e-14:
            increment += (theta - elapsed) * moving_direction
            elapsed = theta
            break
        increment += (hit - elapsed) * moving_direction
        elapsed = hit
        for time, index in candidates:
            if abs(time - hit) <= 2.0e-11 * scale:
                freeze[index] = hit
                moving.discard(index)

    safe[support] = current[support] + increment
    correction = trial[support] - safe[support]
    slack = load[support] - block @ safe[support]
    correction_full[support] = correction
    slack_full[support] = slack
    freeze_full[support] = freeze
    return PeelResult(
        safe=safe,
        gap=max(0.0, float(correction @ slack)),
        correction=correction_full,
        slack=slack_full,
        freeze_times=freeze_full,
        frozen=int(np.sum(freeze < theta - 2.0e-12)),
    )


def maximal_ray(
    matrix: Array, load: Array, previous: Array, current: Array, theta: float
) -> Array:
    direction = current - previous
    pressure = matrix @ direction
    slack = load - matrix @ current
    support = current > 1.0e-14
    ratios = [
        float(slack[i] / pressure[i])
        for i in np.flatnonzero(support)
        if pressure[i] > 1.0e-15
    ]
    accepted = max(0.0, min([theta, *ratios]))
    return current + accepted * direction


def barrier(
    matrix: Array,
    load: Array,
    roots: Array,
    alpha: float,
    previous: Array,
    current: Array,
    theta: float,
) -> Array:
    trial = current + theta * (current - previous)
    violation = np.maximum(matrix @ trial - load, 0.0)
    tau = float(np.max(np.minimum(trial / roots, violation / (alpha * roots))))
    return np.maximum(current, np.maximum(trial - tau * roots, 0.0))


def safe_checks(matrix: Array, load: Array, state: Array, optimum: Array) -> None:
    support = state > 2.0e-12
    state_tolerance = 2.0e-8 * max(float(np.max(np.abs(optimum))), 1.0e-12) + 2.0e-12
    residual_tolerance = 2.0e-8 * max(
        float(np.max(np.abs(load))),
        float(np.max(np.abs(matrix @ state))),
        1.0e-12,
    ) + 2.0e-12
    if np.min(state) < -state_tolerance:
        raise AssertionError("safe state became negative")
    if np.min(optimum - state) < -state_tolerance:
        raise AssertionError("safe state exceeded the obstacle optimum")
    if np.any(support) and np.min((load - matrix @ state)[support]) < -residual_tolerance:
        raise AssertionError("safe state lost the subsolution invariant")


def run(
    adjacency: Array,
    alpha: float,
    rho_fraction: float,
    source: int,
    mode: str,
    relative_tolerance: float,
    maximum_rounds: int,
) -> dict[str, object]:
    matrix, degrees, roots = canonical_operator(adjacency, alpha)
    rho = rho_fraction / degrees[source]
    load = -alpha * rho * roots
    load[source] += alpha / roots[source]
    optimum = obstacle_solution(matrix, load)
    optimum_value = objective(matrix, load, optimum)
    initial_gap = -optimum_value
    if initial_gap <= 0.0:
        raise ValueError("the chosen threshold has empty optimum support")
    optimum_support = set(map(int, np.flatnonzero(optimum > 2.0e-12)))

    root_mu = math.sqrt(alpha / (1.0 + alpha))
    theta = (1.0 - root_mu) / (1.0 + root_mu)
    diagonal = (1.0 + alpha) / 2.0
    previous = np.zeros(len(adjacency))
    current = np.zeros(len(adjacency))
    old_center = np.zeros(len(adjacency))

    total_zeta = 0.0
    total_actual_peeling_loss = 0.0
    total_negative_credit = 0.0
    maximum_charge_ratio = 0.0
    maximum_box_distance_ratio = 0.0
    maximum_event_tv_over_response_energy = 0.0
    maximum_event_tv_over_quadratic_credits = 0.0
    total_event_dirichlet = 0.0
    total_event_square_tv = 0.0
    total_event_tv = 0.0
    total_frozen = 0
    clipping_rounds = 0
    support_changes = 0
    maximum_support_jump = 0
    branch_counts = {"peel": 0, "barrier": 0, "reflection": 0, "ties": 0}
    block_ratios: dict[str, float] = {}
    gaps = [initial_gap]

    for round_index in range(maximum_rounds):
        old_support = set(map(int, np.flatnonzero(current > 2.0e-12)))
        following = obstacle_solution(matrix + np.eye(len(matrix)), load + old_center)
        if np.min(following - current) < -2.0e-8:
            raise AssertionError("exact prox point moved backwards")
        previous, current = current, following
        safe_checks(matrix, load, current, optimum)

        residual = load - matrix @ current
        certificate = 0.5 * float(np.max(np.maximum(residual, 0.0) / roots))
        gap = objective(matrix, load, current) - optimum_value
        gaps.append(gap)
        if certificate <= relative_tolerance * initial_gap:
            rounds = round_index + 1
            break

        peeled = peel(matrix, load, previous, current, theta)
        exact_box, exact_complementarity = exact_safe_box(
            matrix, load, previous, current, theta
        )
        if exact_complementarity > 2.0e-8 * max(initial_gap, 1.0e-14) + 2.0e-13:
            raise AssertionError("exact safe-box complementarity failed")
        ray = maximal_ray(matrix, load, previous, current, theta)
        barred = barrier(matrix, load, roots, alpha, previous, current, theta)
        reflected = current + (current - old_center) / diagonal
        candidates = {
            "peel": peeled.safe,
            "barrier": barred,
            "reflection": reflected,
        }
        if np.min(peeled.safe - ray) < -2.0e-8:
            raise AssertionError("peeling failed to dominate the maximal ray")
        for candidate in [peeled.safe, exact_box, ray, barred, reflected]:
            safe_checks(matrix, load, candidate, optimum)

        if mode == "box":
            center = exact_box
        elif mode == "peel":
            center = peeled.safe
        elif mode == "envelope":
            center = np.maximum.reduce(list(candidates.values()))
            winning = [
                name
                for name, candidate in candidates.items()
                if np.any(candidate >= center - 2.0e-12)
                and np.max(center - candidate) <= 2.0e-12
            ]
            if len(winning) == 1:
                branch_counts[winning[0]] += 1
            else:
                branch_counts["ties"] += 1
        else:
            raise ValueError(f"unknown mode: {mode}")
        safe_checks(matrix, load, center, optimum)

        # Peeling identities are audited even when another envelope branch wins.
        zeta = peeled.gap
        total_zeta += zeta
        total_frozen += peeled.frozen
        clipping_rounds += int(peeled.frozen > 0)
        peeling_value = objective(matrix, load, peeled.safe)
        box_value = objective(matrix, load, exact_box)
        actual_loss = max(0.0, peeling_value - box_value)
        total_actual_peeling_loss += actual_loss
        if actual_loss > zeta + 2.0e-8 * max(initial_gap, actual_loss, 1.0e-14) + 2.0e-13:
            raise AssertionError("peeling loss exceeded its complementarity gap")

        direction = current - previous
        accepted = peeled.safe - current
        event_gap, event_tv, event_dirichlet, event_square_tv = oriented_event_ledgers(
            matrix,
            direction,
            peeled.freeze_times,
            theta,
            np.flatnonzero(current > 1.0e-14),
        )
        event_scale = max(initial_gap, zeta, 1.0e-16)
        if abs(event_gap - zeta) > 2.0e-8 * event_scale:
            raise AssertionError("oriented event formula failed")
        if abs(event_gap - 0.5 * (event_dirichlet + event_square_tv)) > 2.0e-8 * event_scale:
            raise AssertionError("freeze-time variation decomposition failed")
        accepted_slack = float(accepted @ peeled.slack)
        frozen_rows = peeled.freeze_times < theta - 2.0e-12
        frozen_accepted_slack = float(accepted[frozen_rows] @ peeled.slack[frozen_rows])
        if abs(zeta + frozen_accepted_slack - theta * event_tv) > 2.0e-8 * event_scale:
            raise AssertionError("accepted-movement/event-TV identity failed")
        total_event_dirichlet += event_dirichlet
        total_event_square_tv += event_square_tv
        total_event_tv += event_tv
        next_prox = obstacle_solution(matrix + np.eye(len(matrix)), load + peeled.safe)
        recovery = next_prox - peeled.safe
        old_value = objective(matrix, load, previous)
        next_value = objective(matrix, load, next_prox)
        two_step_decrease = old_value - next_value
        identity_tolerance = 5.0e-8 * max(
            initial_gap, abs(two_step_decrease), zeta, 1.0e-14
        ) + 5.0e-13
        if zeta > theta * two_step_decrease + identity_tolerance:
            raise AssertionError("alpha-free two-step charge failed")
        if event_tv > two_step_decrease + identity_tolerance:
            raise AssertionError("event-TV two-step charge failed")
        credit = (
            (1.0 + 1.0 / theta) * accepted_slack
            + 0.5 * float((direction + accepted) @ matrix @ (direction + accepted))
            + float(recovery @ recovery)
            + 0.5 * float(recovery @ matrix @ recovery)
        )
        response_energy = float(recovery @ recovery) + 0.5 * float(
            recovery @ matrix @ recovery
        )
        quadratic_credits = response_energy + 0.5 * float(
            (direction + accepted) @ matrix @ (direction + accepted)
        )
        if response_energy > 1.0e-30:
            maximum_event_tv_over_response_energy = max(
                maximum_event_tv_over_response_energy,
                event_tv / response_energy,
            )
        if quadratic_credits > 1.0e-30:
            maximum_event_tv_over_quadratic_credits = max(
                maximum_event_tv_over_quadratic_credits,
                event_tv / quadratic_credits,
            )
        identity_left = two_step_decrease - zeta / theta
        if abs(identity_left - credit) > 2.0e-7 * max(
            initial_gap, abs(identity_left), abs(credit), 1.0e-14
        ) + 2.0e-12:
            raise AssertionError("two-step negative-credit identity failed")
        total_negative_credit += credit
        if two_step_decrease > 1.0e-18:
            maximum_charge_ratio = max(maximum_charge_ratio, zeta / two_step_decrease)
        box_distance = 0.5 * float((exact_box - peeled.safe) @ matrix @ (exact_box - peeled.safe))
        if zeta > 1.0e-18:
            maximum_box_distance_ratio = max(maximum_box_distance_ratio, box_distance / zeta)

        new_support = set(map(int, np.flatnonzero(current > 2.0e-12)))
        jump = len(new_support - old_support)
        support_changes += int(jump > 0)
        maximum_support_jump = max(maximum_support_jump, jump)
        old_center = center
    else:
        raise RuntimeError("literal safe-prox audit exceeded its round limit")

    for multiplier in (1, 2, 4, 8):
        width = int(math.ceil(multiplier / root_mu))
        if len(gaps) > width:
            ratios = [
                gaps[end] / gaps[end - width]
                for end in range(width, len(gaps))
                if gaps[end - width] > 1.0e-14 * initial_gap
            ]
            if ratios:
                block_ratios[str(multiplier)] = float(max(ratios))

    return {
        "vertices": len(adjacency),
        "edges": int(np.sum(adjacency) // 2),
        "source": source,
        "alpha": alpha,
        "rho_fraction": rho_fraction,
        "mode": mode,
        "rounds": rounds,
        "sqrt_alpha_rounds": math.sqrt(alpha) * rounds,
        "alpha_rounds": alpha * rounds,
        "initial_gap": initial_gap,
        "final_gap": gaps[-1],
        "relative_final_gap": gaps[-1] / initial_gap,
        "optimum_support": len(optimum_support),
        "support_change_rounds": support_changes,
        "maximum_support_jump": maximum_support_jump,
        "peeling_clipping_rounds": clipping_rounds,
        "total_frozen_coordinates": total_frozen,
        "total_zeta_over_initial_gap": total_zeta / initial_gap,
        "total_actual_peeling_loss_over_initial_gap": (
            total_actual_peeling_loss / initial_gap
        ),
        "total_negative_credit_over_initial_gap": total_negative_credit / initial_gap,
        "maximum_zeta_over_two_step_decrease": maximum_charge_ratio,
        "maximum_box_distance_over_zeta": maximum_box_distance_ratio,
        "maximum_event_tv_over_response_energy": (
            maximum_event_tv_over_response_energy
        ),
        "maximum_event_tv_over_quadratic_credits": (
            maximum_event_tv_over_quadratic_credits
        ),
        "event_dirichlet_over_initial_gap": total_event_dirichlet / initial_gap,
        "event_square_tv_over_initial_gap": total_event_square_tv / initial_gap,
        "event_tv_over_initial_gap": total_event_tv / initial_gap,
        "block_ratios": block_ratios,
        "envelope_branch_counts": branch_counts,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--family",
        choices=(
            "path",
            "cycle",
            "star",
            "broom",
            "lollipop",
            "barbell",
            "binary-tree",
            "comb",
            "alternating-fans",
            "direct-peeling-five",
            "random",
        ),
        default="path",
    )
    parser.add_argument("--first", type=int, default=24)
    parser.add_argument("--second", type=int, default=6)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--source", type=int, default=0)
    parser.add_argument("--alphas", default=".03,.01,.003,.001")
    parser.add_argument("--rho-fractions", default=".05,.2,.8")
    parser.add_argument("--modes", default="box,peel,envelope")
    parser.add_argument("--relative-tolerance", type=float, default=1.0e-3)
    parser.add_argument("--maximum-rounds", type=int, default=200000)
    args = parser.parse_args()

    adjacency = family(args.family, args.first, args.second, args.seed)
    if not 0 <= args.source < len(adjacency):
        raise ValueError("source is outside the graph")
    results = []
    for alpha in map(float, args.alphas.split(",")):
        for rho_fraction in map(float, args.rho_fractions.split(",")):
            for mode in args.modes.split(","):
                results.append(
                    run(
                        adjacency,
                        alpha,
                        rho_fraction,
                        args.source,
                        mode,
                        args.relative_tolerance,
                        args.maximum_rounds,
                    )
                )
    print(
        json.dumps(
            {
                "warning": "dense deterministic audit, not a sparse-work proof",
                "family": args.family,
                "first": args.first,
                "second": args.second,
                "seed": args.seed,
                "relative_tolerance": args.relative_tolerance,
                "runs": results,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
