#!/usr/bin/env python3
"""Exact finite check for the Round-021 nonpath causal-ledger STOP.

The primary check replays the canonical transported-center recurrence on the
six-vertex asymmetric T tree from ``prop:t-tree-causal-next-admission-stop``.
It uses exact ``Fraction`` arithmetic throughout.  With ``--enumerate`` it
also exhausts every connected labeled graph on at most five vertices and
every seed, a finite computational minimality audit rather than a theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations


ZERO = Fraction(0)


def degrees_from_edges(order, edges):
    """Return ambient degrees for a simple graph on ``range(order)``."""
    degrees = [0] * order
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1
    return degrees


def neighbors_from_edges(order, edges):
    """Return sorted adjacency lists."""
    neighbors = [[] for _ in range(order)]
    for left, right in edges:
        neighbors[left].append(right)
        neighbors[right].append(left)
    for row in neighbors:
        row.sort()
    return neighbors


def solve_fraction(matrix, right_hand_side):
    """Solve a nonsingular exact rational system by Gauss--Jordan elimination."""
    size = len(right_hand_side)
    augmented = [row[:] + [value] for row, value in zip(matrix, right_hand_side)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(size)]


def apply_h(values, active, neighbors, degrees, alpha):
    """Apply ``D^{-1/2} Q D^{1/2}`` on an induced active face."""
    eta = (1 - alpha) / 2
    diagonal = (1 + alpha) / 2
    position = {vertex: index for index, vertex in enumerate(active)}
    result = []
    for index, vertex in enumerate(active):
        neighbor_sum = sum(
            (values[position[other]] for other in neighbors[vertex] if other in position),
            ZERO,
        )
        result.append(diagonal * values[index] - eta * neighbor_sum / degrees[vertex])
    return result


def load(active, seed, degrees, alpha, rho):
    """Return the normalized RPPR load on an active face."""
    return [
        alpha * ((Fraction(1, degrees[seed]) if vertex == seed else ZERO) - rho)
        for vertex in active
    ]


def residual(values, active, seed, neighbors, degrees, alpha, rho):
    return [
        left - right
        for left, right in zip(
            apply_h(values, active, neighbors, degrees, alpha),
            load(active, seed, degrees, alpha, rho),
        )
    ]


def restricted_optimum(active, seed, neighbors, degrees, alpha, rho):
    """Solve the normalized restricted RPPR stationarity system exactly."""
    eta = (1 - alpha) / 2
    diagonal = (1 + alpha) / 2
    position = {vertex: index for index, vertex in enumerate(active)}
    matrix = [[ZERO for _ in active] for _ in active]
    for row, vertex in enumerate(active):
        matrix[row][row] = diagonal
        for other in neighbors[vertex]:
            if other in position:
                matrix[row][position[other]] = -eta / degrees[vertex]
    return solve_fraction(matrix, load(active, seed, degrees, alpha, rho))


def objective(values, active, seed, neighbors, degrees, alpha, rho):
    """Evaluate the exact normalized RPPR objective on one face."""
    applied = apply_h(values, active, neighbors, degrees, alpha)
    loads = load(active, seed, degrees, alpha, rho)
    return sum(
        (
            Fraction(degrees[vertex]) * (Fraction(1, 2) * value * image - load_value * value)
            for vertex, value, image, load_value in zip(active, values, applied, loads)
        ),
        ZERO,
    )


def one_vertex_schur_data(active, new_vertex, seed, neighbors, degrees, alpha, rho):
    """Return the positive load and symmetric Schur pivot for one admission."""
    enlarged = active + [new_vertex]
    old_optimum = restricted_optimum(active, seed, neighbors, degrees, alpha, rho)
    padded = old_optimum + [ZERO]
    normalized_residual = residual(
        padded,
        enlarged,
        seed,
        neighbors,
        degrees,
        alpha,
        rho,
    )[-1]
    response_load = -degrees[new_vertex] * normalized_residual

    size = len(enlarged)
    normalized_matrix = []
    for column in range(size):
        basis = [ZERO] * size
        basis[column] = Fraction(1)
        normalized_matrix.append(apply_h(basis, enlarged, neighbors, degrees, alpha))
    normalized_matrix = [list(row) for row in zip(*normalized_matrix)]
    symmetric_matrix = [
        [degrees[vertex] * value for value in row]
        for vertex, row in zip(enlarged, normalized_matrix)
    ]
    old_block = [row[:-1] for row in symmetric_matrix[:-1]]
    old_to_new = [row[-1] for row in symmetric_matrix[:-1]]
    new_to_old = symmetric_matrix[-1][:-1]
    response = solve_fraction(old_block, old_to_new)
    schur_pivot = symmetric_matrix[-1][-1] - sum(
        (left * right for left, right in zip(new_to_old, response)),
        ZERO,
    )
    return response_load, schur_pivot


def one_step(iterate, center, active, seed, neighbors, degrees, q, rho):
    """One exact fixed-face transported-center accelerated step."""
    alpha = q * q
    interpolation = [
        (value + q * center_value) / (1 + q) for value, center_value in zip(iterate, center)
    ]
    gradient = residual(
        interpolation,
        active,
        seed,
        neighbors,
        degrees,
        alpha,
        rho,
    )
    candidate = [value - derivative for value, derivative in zip(interpolation, gradient)]
    if min(candidate) <= 0:
        return None
    center_next = [new + (1 - q) * (new - old) / q for new, old in zip(candidate, iterate)]
    return candidate, center_next


def boundary(active, neighbors):
    active_set = set(active)
    return sorted(
        {other for vertex in active for other in neighbors[vertex] if other not in active_set}
    )


def replay(order, edges, seed, max_stages=200):
    """Replay the complete all-boundary gate, returning exact checkpoints."""
    q = Fraction(1, 5)
    alpha = q * q
    rho = tau = q / 5
    degrees = degrees_from_edges(order, edges)
    neighbors = neighbors_from_edges(order, edges)
    active = [seed]
    iterate = [ZERO]
    center = [ZERO]
    optimum = restricted_optimum(active, seed, neighbors, degrees, alpha, rho)
    snapshots = {}
    admissions = []
    swept_volume = 0

    for stage in range(1, max_stages + 1):
        active_before = active[:]
        optimum_before = optimum[:]
        swept_volume += sum(degrees[vertex] for vertex in active)
        stepped = one_step(
            iterate,
            center,
            active,
            seed,
            neighbors,
            degrees,
            q,
            rho,
        )
        if stepped is None:
            return None
        candidate, center_next = stepped
        active_residual = residual(
            candidate,
            active,
            seed,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        delta = max(ZERO, max(active_residual) / alpha)
        envelope = [max(ZERO, value - delta) for value in candidate]
        envelope_residual = residual(
            envelope,
            active,
            seed,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        position = {vertex: index for index, vertex in enumerate(active)}
        outside_residual = {}
        for vertex in boundary(active, neighbors):
            incoming = sum(
                (envelope[position[other]] for other in neighbors[vertex] if other in position),
                ZERO,
            )
            outside_residual[vertex] = -(1 - alpha) * incoming / (2 * degrees[vertex]) + alpha * rho
        admitted = sorted(
            vertex for vertex, value in outside_residual.items() if value < -alpha * tau
        )
        drop = ZERO
        post_delta = delta
        if admitted:
            action = "admit"
            admissions.append((stage, tuple(admitted)))
            active = active + admitted
            new_optimum = restricted_optimum(
                active,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            )
            old_by_vertex = dict(zip(active_before, optimum_before))
            candidate_by_vertex = dict(zip(active_before, candidate))
            center_by_vertex = dict(zip(active_before, center_next))
            padded_optimum = [old_by_vertex.get(vertex, ZERO) for vertex in active]
            padded_candidate = [candidate_by_vertex.get(vertex, ZERO) for vertex in active]
            padded_center = [center_by_vertex.get(vertex, ZERO) for vertex in active]
            displacement = [new - old for new, old in zip(new_optimum, padded_optimum)]
            center = [value + shift for value, shift in zip(padded_center, displacement)]
            iterate = padded_candidate
            optimum = new_optimum
            drop = objective(
                padded_optimum,
                active,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            ) - objective(
                new_optimum,
                active,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            )
            post_residual = residual(
                padded_candidate,
                active,
                seed,
                neighbors,
                degrees,
                alpha,
                rho,
            )
            post_delta = max(ZERO, max(post_residual) / alpha)
        elif min(envelope_residual) >= -alpha * tau:
            action = "certify"
            iterate, center = candidate, center_next
        else:
            action = "hold"
            iterate, center = candidate, center_next

        snapshots[stage] = {
            "active": tuple(active_before),
            "action": action,
            "admitted": tuple(admitted),
            "candidate": tuple(candidate),
            "delta": delta,
            "post_delta": post_delta,
            "outside": outside_residual,
            "drop": drop,
        }
        if action == "certify":
            return {
                "snapshots": snapshots,
                "admissions": admissions,
                "terminal_stage": stage,
                "active": tuple(active),
                "degrees": tuple(degrees),
                "swept_volume": swept_volume,
            }
    return None


def causal_balances(run, origin_stage):
    """Restart Xi=delta^2 at ``origin_stage`` and audit later checkpoints."""
    snapshots = run["snapshots"]
    origin_score = snapshots[origin_stage]["delta"] ** 2
    realized_drops = ZERO
    balances = {}
    pre_admission = {}
    for stage in range(origin_stage + 1, run["terminal_stage"] + 1):
        score = snapshots[stage]["delta"] ** 2
        pre_admission[stage] = origin_score + realized_drops - score
        realized_drops += snapshots[stage]["drop"]
        balances[stage] = origin_score + realized_drops - snapshots[stage]["post_delta"] ** 2
    return pre_admission, balances


def named_tree_check():
    edges = ((0, 1), (1, 2), (2, 3), (2, 4), (4, 5))
    run = replay(6, edges, 0)
    assert run is not None
    snapshots = run["snapshots"]
    expected_actions = {
        1: ("admit", (1,)),
        2: ("admit", (2,)),
        3: ("hold", ()),
        4: ("admit", (3,)),
        5: ("hold", ()),
        6: ("hold", ()),
        7: ("hold", ()),
        8: ("hold", ()),
        9: ("admit", (4,)),
        10: ("hold", ()),
        11: ("hold", ()),
        12: ("hold", ()),
        13: ("hold", ()),
        14: ("hold", ()),
        15: ("admit", (5,)),
        16: ("hold", ()),
        17: ("certify", ()),
    }
    assert {
        stage: (snapshot["action"], snapshot["admitted"]) for stage, snapshot in snapshots.items()
    } == expected_actions
    assert run["degrees"] == (1, 2, 3, 1, 2, 1)
    assert run["admissions"] == [(1, (1,)), (2, (2,)), (4, (3,)), (9, (4,)), (15, (5,))]
    assert run["terminal_stage"] == 17
    assert run["active"] == (0, 1, 2, 3, 4, 5)
    assert run["swept_volume"] == 125

    threshold = -Fraction(1, 625)
    assert snapshots[4]["outside"][3] == -Fraction(734335307, 179791015625)
    assert snapshots[4]["outside"][4] == -Fraction(223334841, 179791015625)
    assert snapshots[4]["outside"][3] < threshold < snapshots[4]["outside"][4]
    assert snapshots[9]["outside"][4] == -Fraction(
        8110851051223533,
        4315546221923828125,
    )
    assert snapshots[9]["outside"][4] < threshold

    load_4, pivot_4 = one_vertex_schur_data(
        [0, 1, 2],
        3,
        0,
        neighbors_from_edges(6, edges),
        list(run["degrees"]),
        Fraction(1, 25),
        Fraction(1, 25),
    )
    load_9, pivot_9 = one_vertex_schur_data(
        [0, 1, 2, 3],
        4,
        0,
        neighbors_from_edges(6, edges),
        list(run["degrees"]),
        Fraction(1, 25),
        Fraction(1, 25),
    )
    assert (load_4, pivot_4) == (Fraction(167, 23725), Fraction(7681, 23725))
    assert (load_9, pivot_9) == (
        Fraction(46594, 4800625),
        Fraction(139178, 192025),
    )
    assert snapshots[4]["drop"] == Fraction(27889, 364463450)
    assert snapshots[9]["drop"] == Fraction(542750209, 8351767328125)
    assert snapshots[4]["drop"] == load_4 * load_4 / (2 * pivot_4)
    assert snapshots[9]["drop"] == load_9 * load_9 / (2 * pivot_9)
    assert all(min(snapshot["candidate"]) > 0 for snapshot in snapshots.values())

    pre_admission, balances = causal_balances(run, 3)
    assert balances[5] == -Fraction(
        8829125916972234811,
        272095189292297363281250,
    )
    assert pre_admission[9] == -Fraction(
        68219046926175800933507563,
        310358575286526679992675781250,
    )
    assert balances[9] == -Fraction(
        33486740471411901479718569,
        216293380225071907043457031250,
    )
    assert balances[13] < 0
    assert balances[14] == Fraction(
        1413547795978281227785235568281109142219549159,
        20440374468970319043095709057524800300598144531250,
    )
    assert all(balances[stage] < 0 for stage in range(5, 14))
    assert balances[14] > 0

    print(
        "exact q=1/5 asymmetric-T STOP verified: debt survives the stage-9 "
        "admission; stage 13 is the last local STOP and stage 14 the first "
        "local GO; J=5, T=17, nu_fin=10, n_fin=6, swept volume=125"
    )


def connected(order, edges):
    neighbors = neighbors_from_edges(order, edges)
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for other in neighbors[vertex]:
            if other not in reached:
                reached.add(other)
                frontier.append(other)
    return len(reached) == order


def has_next_admission_stop(run):
    """Test the reviewed finite pattern from every held restart checkpoint."""
    snapshots = run["snapshots"]
    held_stages = [stage for stage, snap in snapshots.items() if snap["action"] == "hold"]
    for origin in held_stages:
        later_admissions = [
            stage
            for stage in range(origin + 1, run["terminal_stage"] + 1)
            if snapshots[stage]["action"] == "admit"
        ]
        if len(later_admissions) < 2:
            continue
        _pre, balances = causal_balances(run, origin)
        if balances[later_admissions[1]] < 0:
            return True
    return False


def enumerate_small_graphs():
    rooted_cases = 0
    for order in range(2, 6):
        possible_edges = list(combinations(range(order), 2))
        for mask in range(1 << len(possible_edges)):
            edges = tuple(edge for index, edge in enumerate(possible_edges) if mask & (1 << index))
            if not connected(order, edges):
                continue
            for seed in range(order):
                rooted_cases += 1
                run = replay(order, edges, seed)
                assert run is not None
                assert not has_next_admission_stop(run), (order, edges, seed)
    assert rooted_cases == 3806
    print(
        "computational audit verified: no reviewed next-admission STOP among "
        "all 3806 connected labeled rooted graphs on 2--5 vertices"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--enumerate",
        action="store_true",
        help="also exhaust all connected labeled rooted graphs on 2--5 vertices",
    )
    arguments = parser.parse_args()
    named_tree_check()
    if arguments.enumerate:
        enumerate_small_graphs()


if __name__ == "__main__":
    main()
