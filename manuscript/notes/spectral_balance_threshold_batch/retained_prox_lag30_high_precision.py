#!/usr/bin/env python3
"""High-precision audit of the canonical one-step-domain counterexample.

The input is a 30-vertex simple connected unit graph, alpha=1/10000, and
rho=17/2000.  The script repeats the retained-prox trace at two independent
MP precisions.  It verifies a macroscopic one-step-lag lower-envelope
deficit, so the sign is separated from floating-point roundoff by many
orders of magnitude.
"""

from __future__ import annotations

import mpmath as mp

from retained_prox_experiment import LAG30_EDGES


def run(
    precision: int,
) -> tuple[
    mp.mpf,
    tuple[int, int, int],
    list[tuple[int, int]],
    list[tuple[int, ...]],
]:
    mp.mp.dps = precision
    vertex_count = 30
    neighbors = [set() for _ in range(vertex_count)]
    for left, right in LAG30_EDGES:
        neighbors[left].add(right)
        neighbors[right].add(left)
    degrees = [len(row) for row in neighbors]
    assert min(degrees) > 0 and degrees[0] == 5

    alpha = mp.mpf(1) / 10_000
    rho = mp.mpf(17) / 2_000
    sigma = alpha
    diagonal = (1 + alpha) / 2 + sigma
    coupling = (1 - alpha) / 2
    lipschitz = 1 + sigma
    shifted_gap = alpha + sigma
    root = mp.sqrt(shifted_gap / lipschitz)
    momentum = (1 - root) / (1 + root)
    auxiliary_scale = (1 - root) / root

    operator = [[mp.mpf(0) for _ in range(vertex_count)] for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        operator[vertex][vertex] = diagonal
        for neighbor in neighbors[vertex]:
            operator[vertex][neighbor] = -coupling / degrees[vertex]

    original_load = [-alpha * rho for _ in range(vertex_count)]
    original_load[0] += alpha / degrees[0]

    def apply(state: list[mp.mpf], vertex: int, face: set[int] | None = None) -> mp.mpf:
        active = range(vertex_count) if face is None else face
        return mp.fsum(operator[vertex][other] * state[other] for other in active)

    def exact_support(load: list[mp.mpf]) -> set[int]:
        face = {vertex for vertex, value in enumerate(load) if value > 0}
        while face:
            ordered = sorted(face)
            block = mp.matrix(
                [[operator[left][right] for right in ordered] for left in ordered]
            )
            solution = mp.lu_solve(block, mp.matrix([load[vertex] for vertex in ordered]))
            assert min(solution) > 0
            full = [mp.mpf(0) for _ in range(vertex_count)]
            for vertex, value in zip(ordered, solution):
                full[vertex] = value
            batch = {
                vertex
                for vertex in range(vertex_count)
                if vertex not in face and load[vertex] - apply(full, vertex) > 0
            }
            if not batch:
                return face
            face.update(batch)
        return set()

    def advance(
        face: set[int],
        shifted_load: list[mp.mpf],
        state: list[mp.mpf],
        prior: list[mp.mpf],
        envelope: list[mp.mpf],
    ) -> tuple[list[mp.mpf], list[mp.mpf], list[mp.mpf]]:
        extrapolated = [mp.mpf(0) for _ in range(vertex_count)]
        following = [mp.mpf(0) for _ in range(vertex_count)]
        for vertex in face:
            extrapolated[vertex] = state[vertex] + momentum * (
                state[vertex] - prior[vertex]
            )
        for vertex in face:
            residual = shifted_load[vertex] - apply(extrapolated, vertex, face)
            following[vertex] = extrapolated[vertex] + residual / lipschitz
        prior, state = state, following

        shift = mp.mpf(0)
        ones = [mp.mpf(1) for _ in range(vertex_count)]
        for vertex in face:
            residual = shifted_load[vertex] - apply(state, vertex, face)
            stationary = apply(ones, vertex, face)
            shift = max(shift, -residual / stationary)
        for vertex in face:
            envelope[vertex] = max(
                envelope[vertex], state[vertex] - shift, mp.mpf(0)
            )

        auxiliary = [mp.mpf(0) for _ in range(vertex_count)]
        for vertex in face:
            auxiliary[vertex] = state[vertex] + auxiliary_scale * (
                state[vertex] - prior[vertex]
            )
            state[vertex] = max(state[vertex], envelope[vertex])
            auxiliary[vertex] = max(auxiliary[vertex], envelope[vertex])
            velocity = (auxiliary[vertex] - state[vertex]) / auxiliary_scale
            prior[vertex] = state[vertex] - velocity
        return state, prior, envelope

    lower = [mp.mpf(0) for _ in range(vertex_count)]
    certified = {0}
    width = mp.mpf(1) / degrees[0] - rho
    maximum_deficit = mp.mpf(0)
    witness = (-1, -1, -1)
    event_trace: list[tuple[int, int]] = []
    support_trace: list[tuple[int, ...]] = []

    for phase in range(9):
        old_lower = lower[:]
        shifted_load = [
            original_load[vertex] + sigma * old_lower[vertex]
            for vertex in range(vertex_count)
        ]
        omniscient_face = exact_support(shifted_load)
        support_trace.append(tuple(sorted(omniscient_face)))
        requested = width / 4
        current = old_lower[:]
        previous = old_lower[:]
        omniscient_current = old_lower[:]
        omniscient_previous = old_lower[:]
        omniscient_lower = old_lower[:]
        lagged_omniscient_lower = old_lower[:]

        for iteration in range(500):
            scratch = set(certified)
            current, previous, lower = advance(
                scratch, shifted_load, current, previous, lower
            )
            omniscient_current, omniscient_previous, omniscient_lower = advance(
                omniscient_face,
                shifted_load,
                omniscient_current,
                omniscient_previous,
                omniscient_lower,
            )

            batch = {
                vertex
                for vertex in range(vertex_count)
                if vertex not in certified
                and shifted_load[vertex] - apply(lower, vertex) > 0
            }
            if batch:
                certified.update(batch)
                event_trace.append((phase, iteration + 1))

            deficits = [
                lagged_omniscient_lower[vertex] - lower[vertex]
                for vertex in range(vertex_count)
            ]
            deficit = max(deficits)
            if deficit > maximum_deficit:
                maximum_deficit = deficit
                witness = (phase, iteration + 1, deficits.index(deficit))
            lagged_omniscient_lower = omniscient_lower[:]

            residual_width = max(
                [mp.mpf(0)]
                + [
                    (shifted_load[vertex] - apply(lower, vertex)) / shifted_gap
                    for vertex in range(vertex_count)
                ]
            )
            if residual_width <= requested:
                width = width / 2 + residual_width
                break
        else:
            raise AssertionError("phase did not reach its quarter bracket")

    return maximum_deficit, witness, event_trace, support_trace


def main() -> None:
    low, low_witness, low_events, low_supports = run(80)
    high, high_witness, high_events, high_supports = run(140)
    assert low_witness == high_witness == (8, 86, 12)
    assert low_events == high_events
    assert low_supports == high_supports
    assert high > mp.mpf("0.00028")
    assert abs(low - high) < mp.mpf("1e-70")
    print("one-step lag lower dominance is false on the canonical lag30 graph")
    print("phase / iteration / vertex =", high_witness)
    print("high-precision deficit =", mp.nstr(high, 80))
    print("publication events through phase 8 =", high_events)


if __name__ == "__main__":
    main()
