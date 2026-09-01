#!/usr/bin/env python3
"""Fraction-exact small-graph audit of the enhanced retained-prox history.

At alpha=1/7 the retained NAG root is exactly 1/2.  In degree coordinates
all graph, load, retraction, publication, and diagonal-push arithmetic is
rational.  This script enumerates connected labelled simple unit graphs and
checks the pushed-domain and three local history clauses without floating
point.  It is a finite audit, not a graph-uniform proof.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction as F


ALPHA = F(1, 7)
SIGMA = ALPHA
ORIGINAL_DIAGONAL = F(4, 7)
SHIFTED_DIAGONAL = F(5, 7)
COUPLING = F(3, 7)
LIPSCHITZ = F(8, 7)
SHIFTED_GAP = F(2, 7)
ROOT = F(1, 2)
MOMENTUM = F(1, 3)
AUXILIARY_SCALE = F(1)


def configure(root: F) -> None:
    global ALPHA, SIGMA, ORIGINAL_DIAGONAL, SHIFTED_DIAGONAL
    global COUPLING, LIPSCHITZ, SHIFTED_GAP, ROOT, MOMENTUM
    global AUXILIARY_SCALE
    if not 0 < root <= 1:
        raise ValueError("root must lie in (0,1]")
    ROOT = root
    ALPHA = root * root / (2 - root * root)
    SIGMA = ALPHA
    ORIGINAL_DIAGONAL = (1 + ALPHA) / 2
    SHIFTED_DIAGONAL = (1 + 3 * ALPHA) / 2
    COUPLING = (1 - ALPHA) / 2
    LIPSCHITZ = 1 + ALPHA
    SHIFTED_GAP = 2 * ALPHA
    MOMENTUM = (1 - root) / (1 + root)
    AUXILIARY_SCALE = (1 - root) / root
    assert SHIFTED_GAP / LIPSCHITZ == root * root


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    size = len(rhs)
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    left - factor * right for left, right in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(size)]


def connected(neighbors: list[set[int]]) -> bool:
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in neighbors[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(neighbors)


def minimum_update(
    record: dict[str, object] | None,
    value: F,
    witness: dict[str, object],
) -> dict[str, object]:
    if record is None or value < record["value"]:
        return {"value": value, **witness}
    return record


def audit_graph(
    neighbors: list[set[int]],
    rho_fraction: F,
    relative_width: F,
    post_append_residual_push: bool,
    input_residual_append: bool,
) -> dict[str, object]:
    vertex_count = len(neighbors)
    degrees = [len(row) for row in neighbors]
    rho = rho_fraction / degrees[0]
    operator = [[F(0) for _ in range(vertex_count)] for _ in range(vertex_count)]
    original_operator = [[F(0) for _ in range(vertex_count)] for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        operator[vertex][vertex] = SHIFTED_DIAGONAL
        original_operator[vertex][vertex] = ORIGINAL_DIAGONAL
        for neighbor in neighbors[vertex]:
            operator[vertex][neighbor] = -COUPLING / degrees[vertex]
            original_operator[vertex][neighbor] = -COUPLING / degrees[vertex]

    def apply(state: list[F], vertex: int, face: set[int] | None = None) -> F:
        active = range(vertex_count) if face is None else face
        return sum(operator[vertex][other] * state[other] for other in active)

    def residual(load: list[F], state: list[F]) -> list[F]:
        return [load[i] - apply(state, i) for i in range(vertex_count)]

    def exact_solution(load: list[F], matrix: list[list[F]] = operator) -> tuple[set[int], list[F]]:
        face = {vertex for vertex, value in enumerate(load) if value > 0}
        full = [F(0) for _ in range(vertex_count)]
        while face:
            ordered = sorted(face)
            block = [[matrix[left][right] for right in ordered] for left in ordered]
            values = solve(block, [load[vertex] for vertex in ordered])
            assert min(values) >= 0
            full = [F(0) for _ in range(vertex_count)]
            for vertex, value in zip(ordered, values):
                full[vertex] = value
            batch = {
                vertex
                for vertex in range(vertex_count)
                if vertex not in face
                and load[vertex] - sum(matrix[vertex][other] * full[other] for other in face) > 0
            }
            if not batch:
                return face, full
            face.update(batch)
        return set(), full

    original_load = [-ALPHA * rho for _ in range(vertex_count)]
    original_load[0] += ALPHA / degrees[0]
    final_face, final_solution = exact_solution(original_load, original_operator)
    assert 0 in final_face

    lower = [F(0) for _ in range(vertex_count)]
    certified = {0}
    initial_width = F(1, degrees[0]) - rho
    width = initial_width
    target = relative_width * initial_width
    extrema: dict[str, dict[str, object] | None] = {
        "pushed_lower_gap": None,
        "pre_push_lower_gap": None,
        "starting_lower_one_step_gap": None,
        "relevant_starting_lower_one_step_gap": None,
        "starting_current_one_step_gap": None,
        "starting_auxiliary_one_step_gap": None,
        "starting_extrapolate_one_step_gap": None,
        "current_gap": None,
        "extrapolate_gap": None,
        "momentum_flux": None,
        "boundary_flux": None,
        "boundary_layer": None,
        "exterior_current_zero_margin": None,
        "shadow_cover_margin": None,
        "masked_raw_residual_margin": None,
        "masked_input_residual_margin": None,
        "two_jacobi_cap_margin": None,
    }
    phases = 0
    products = 0
    maximum_phase_products = 0
    events = 0

    while width > target:
        if phases >= 60:
            raise AssertionError("too many exact outer phases")
        old_lower = lower[:]
        old_width = width
        shifted_load = [original_load[i] + SIGMA * old_lower[i] for i in range(vertex_count)]
        omniscient_face, exact_prox = exact_solution(shifted_load)
        assert certified.issubset(final_face)
        assert all(exact_prox[i] >= old_lower[i] for i in range(vertex_count))

        current = old_lower[:]
        previous = old_lower[:]
        auxiliary = old_lower[:]
        omniscient_current = old_lower[:]
        omniscient_previous = old_lower[:]
        omniscient_auxiliary = old_lower[:]
        omniscient_lower = old_lower[:]

        def advance(
            face: set[int],
            state: list[F],
            prior: list[F],
            envelope: list[F],
        ) -> tuple[list[F], list[F], list[F], list[F], list[F], F, F]:
            input_extrapolate = [F(0) for _ in range(vertex_count)]
            following = [F(0) for _ in range(vertex_count)]
            for vertex in face:
                input_extrapolate[vertex] = state[vertex] + MOMENTUM * (
                    state[vertex] - prior[vertex]
                )
            input_residuals = {
                vertex: shifted_load[vertex] - apply(input_extrapolate, vertex, face)
                for vertex in face
            }
            for vertex in face:
                following[vertex] = input_extrapolate[vertex] + input_residuals[vertex] / LIPSCHITZ
            prior, state = state, following

            shifts = [F(0)]
            minimum_row_residual: F | None = None
            ones = [F(1) for _ in range(vertex_count)]
            for vertex in face:
                row_residual = shifted_load[vertex] - apply(state, vertex, face)
                if minimum_row_residual is None or row_residual < minimum_row_residual:
                    minimum_row_residual = row_residual
                direction = apply(ones, vertex, face)
                assert direction > 0
                shifts.append(-row_residual / direction)
            shift = max(shifts)
            for vertex in face:
                candidate = state[vertex] - shift
                envelope[vertex] = max(envelope[vertex], candidate, F(0))

            next_auxiliary = [F(0) for _ in range(vertex_count)]
            for vertex in face:
                next_auxiliary[vertex] = state[vertex] + AUXILIARY_SCALE * (
                    state[vertex] - prior[vertex]
                )
                state[vertex] = max(state[vertex], envelope[vertex])
                next_auxiliary[vertex] = max(next_auxiliary[vertex], envelope[vertex])
                prior[vertex] = (
                    state[vertex] - (next_auxiliary[vertex] - state[vertex]) / AUXILIARY_SCALE
                )
            return (
                state,
                prior,
                envelope,
                next_auxiliary,
                input_extrapolate,
                minimum_row_residual if minimum_row_residual is not None else F(0),
                min(input_residuals.values(), default=F(0)),
            )

        for iteration in range(100):
            old_face = set(certified)
            starting_masked_lower = lower[:]
            starting_masked_current = current[:]
            starting_masked_auxiliary = auxiliary[:]
            starting_masked_extrapolate = [
                (starting_masked_current[i] + ROOT * starting_masked_auxiliary[i]) / (1 + ROOT)
                for i in range(vertex_count)
            ]
            if input_residual_append:
                full_input_residual = residual(shifted_load, starting_masked_extrapolate)
                input_batch = {
                    vertex
                    for vertex in range(vertex_count)
                    if vertex not in certified and full_input_residual[vertex] > 0
                }
                if input_batch:
                    assert input_batch.issubset(omniscient_face)
                    certified.update(input_batch)
                    old_face = set(certified)
                    events += 1
            starting_omniscient_current = omniscient_current[:]
            starting_omniscient_previous = omniscient_previous[:]
            starting_omniscient_lower = omniscient_lower[:]
            starting_omniscient_residual = residual(shifted_load, starting_omniscient_lower)
            omniscient_jacobi_one = [
                starting_omniscient_lower[i]
                + max(starting_omniscient_residual[i], F(0)) / SHIFTED_DIAGONAL
                for i in range(vertex_count)
            ]
            jacobi_one_residual = residual(shifted_load, omniscient_jacobi_one)
            omniscient_jacobi_two = [
                omniscient_jacobi_one[i] + max(jacobi_one_residual[i], F(0)) / SHIFTED_DIAGONAL
                for i in range(vertex_count)
            ]
            (
                current,
                previous,
                lower,
                auxiliary,
                _,
                masked_raw_residual_margin,
                masked_input_residual_margin,
            ) = advance(old_face, current, previous, lower)
            (
                omniscient_current,
                omniscient_previous,
                omniscient_lower,
                omniscient_auxiliary,
                omniscient_input_extrapolate,
                _,
                _,
            ) = advance(
                omniscient_face,
                omniscient_current,
                omniscient_previous,
                omniscient_lower,
            )
            products += 1

            for vertex in omniscient_face:
                extrema["two_jacobi_cap_margin"] = minimum_update(
                    extrema["two_jacobi_cap_margin"],
                    omniscient_jacobi_two[vertex] - omniscient_lower[vertex],
                    {
                        "phase": phases,
                        "product": iteration + 1,
                        "vertex": vertex,
                    },
                )

            extrema["masked_raw_residual_margin"] = minimum_update(
                extrema["masked_raw_residual_margin"],
                masked_raw_residual_margin,
                {
                    "phase": phases,
                    "product": iteration + 1,
                },
            )
            extrema["masked_input_residual_margin"] = minimum_update(
                extrema["masked_input_residual_margin"],
                masked_input_residual_margin,
                {
                    "phase": phases,
                    "product": iteration + 1,
                },
            )

            if iteration > 0:
                for vertex in range(vertex_count):
                    extrema["starting_lower_one_step_gap"] = minimum_update(
                        extrema["starting_lower_one_step_gap"],
                        starting_masked_lower[vertex] - omniscient_lower[vertex],
                        {
                            "phase": phases,
                            "product": iteration + 1,
                            "vertex": vertex,
                        },
                    )
                    if omniscient_lower[vertex] > starting_omniscient_lower[vertex]:
                        extrema["relevant_starting_lower_one_step_gap"] = minimum_update(
                            extrema["relevant_starting_lower_one_step_gap"],
                            starting_masked_lower[vertex] - omniscient_lower[vertex],
                            {
                                "phase": phases,
                                "product": iteration + 1,
                                "vertex": vertex,
                                "starting_masked_lower": starting_masked_lower[vertex],
                                "starting_omniscient_lower": starting_omniscient_lower[vertex],
                                "new_omniscient_lower": omniscient_lower[vertex],
                                "starting_masked_current": starting_masked_current[vertex],
                                "starting_masked_auxiliary": starting_masked_auxiliary[vertex],
                                "new_omniscient_current": omniscient_current[vertex],
                                "new_omniscient_auxiliary": omniscient_auxiliary[vertex],
                            },
                        )
                    omniscient_output_extrapolate = (
                        omniscient_current[vertex] + ROOT * omniscient_auxiliary[vertex]
                    ) / (1 + ROOT)
                    one_step_witness = {
                        "phase": phases,
                        "product": iteration + 1,
                        "vertex": vertex,
                    }
                    extrema["starting_current_one_step_gap"] = minimum_update(
                        extrema["starting_current_one_step_gap"],
                        starting_masked_current[vertex] - omniscient_current[vertex],
                        one_step_witness,
                    )
                    extrema["starting_auxiliary_one_step_gap"] = minimum_update(
                        extrema["starting_auxiliary_one_step_gap"],
                        starting_masked_auxiliary[vertex] - omniscient_auxiliary[vertex],
                        one_step_witness,
                    )
                    extrema["starting_extrapolate_one_step_gap"] = minimum_update(
                        extrema["starting_extrapolate_one_step_gap"],
                        starting_masked_extrapolate[vertex] - omniscient_output_extrapolate,
                        one_step_witness,
                    )

            pre_push_lower = lower[:]
            pre_push_residual = residual(shifted_load, pre_push_lower)
            for vertex in range(vertex_count):
                witness = {
                    "phase": phases,
                    "product": iteration + 1,
                    "vertex": vertex,
                }
                extrema["pre_push_lower_gap"] = minimum_update(
                    extrema["pre_push_lower_gap"],
                    pre_push_lower[vertex] - omniscient_lower[vertex],
                    witness,
                )
                delta = omniscient_lower[vertex] - pre_push_lower[vertex]
                if delta > 0:
                    cover = max(pre_push_residual[vertex], F(0)) - (SHIFTED_DIAGONAL * delta)
                    extrema["shadow_cover_margin"] = minimum_update(
                        extrema["shadow_cover_margin"], cover, witness
                    )

            old_exterior = omniscient_face - old_face
            for vertex in old_exterior:
                assert starting_omniscient_current[vertex] == 0
                assert starting_omniscient_previous[vertex] == 0
                active_neighbors = neighbors[vertex] & old_face
                if not active_neighbors:
                    continue
                cq = (
                    COUPLING
                    / degrees[vertex]
                    * sum(omniscient_input_extrapolate[neighbor] for neighbor in neighbors[vertex])
                )
                cu = (
                    COUPLING
                    / degrees[vertex]
                    * sum(pre_push_lower[neighbor] for neighbor in neighbors[vertex])
                )
                witness = {
                    "phase": phases,
                    "product": iteration + 1,
                    "vertex": vertex,
                }
                extrema["boundary_flux"] = minimum_update(
                    extrema["boundary_flux"], cu - cq, witness
                )
                for neighbor in active_neighbors:
                    extrema["boundary_layer"] = minimum_update(
                        extrema["boundary_layer"],
                        pre_push_lower[neighbor] - omniscient_input_extrapolate[neighbor],
                        {**witness, "vertex": neighbor},
                    )

            # One simultaneous positive-residual push on the old face.
            increment = [F(0) for _ in range(vertex_count)]
            for vertex in old_face:
                if pre_push_residual[vertex] > 0:
                    increment[vertex] = pre_push_residual[vertex] / SHIFTED_DIAGONAL
            for vertex in old_face:
                lower[vertex] += increment[vertex]
            full_residual = residual(shifted_load, lower)
            for vertex in old_face:
                current[vertex] = max(current[vertex], lower[vertex])
                auxiliary[vertex] = max(auxiliary[vertex], lower[vertex])
                previous[vertex] = (
                    current[vertex] - (auxiliary[vertex] - current[vertex]) / AUXILIARY_SCALE
                )

            # Maximal exact-positive append closure.
            while True:
                batch = {
                    vertex
                    for vertex in range(vertex_count)
                    if vertex not in certified and full_residual[vertex] > 0
                }
                if not batch:
                    break
                events += 1
                batch_increment = [F(0) for _ in range(vertex_count)]
                for vertex in batch:
                    batch_increment[vertex] = full_residual[vertex] / SHIFTED_DIAGONAL
                for vertex in batch:
                    lower[vertex] += batch_increment[vertex]
                    current[vertex] = lower[vertex]
                    auxiliary[vertex] = lower[vertex]
                    previous[vertex] = lower[vertex]
                certified.update(batch)
                full_residual = residual(shifted_load, lower)

            if post_append_residual_push:
                cleanup_increment = [F(0) for _ in range(vertex_count)]
                for vertex in certified:
                    if full_residual[vertex] > 0:
                        cleanup_increment[vertex] = full_residual[vertex] / SHIFTED_DIAGONAL
                for vertex in certified:
                    lower[vertex] += cleanup_increment[vertex]
                    current[vertex] = max(current[vertex], lower[vertex])
                    auxiliary[vertex] = max(auxiliary[vertex], lower[vertex])
                    previous[vertex] = (
                        current[vertex] - (auxiliary[vertex] - current[vertex]) / AUXILIARY_SCALE
                    )
                full_residual = residual(shifted_load, lower)
                while True:
                    batch = {
                        vertex
                        for vertex in range(vertex_count)
                        if vertex not in certified and full_residual[vertex] > 0
                    }
                    if not batch:
                        break
                    events += 1
                    for vertex in batch:
                        lower[vertex] += full_residual[vertex] / SHIFTED_DIAGONAL
                        current[vertex] = lower[vertex]
                        auxiliary[vertex] = lower[vertex]
                        previous[vertex] = lower[vertex]
                    certified.update(batch)
                    full_residual = residual(shifted_load, lower)

            masked_extrapolate = [
                (current[i] + ROOT * auxiliary[i]) / (1 + ROOT) for i in range(vertex_count)
            ]
            omniscient_extrapolate = [
                (omniscient_current[i] + ROOT * omniscient_auxiliary[i]) / (1 + ROOT)
                for i in range(vertex_count)
            ]

            for vertex in range(vertex_count):
                witness = {
                    "phase": phases,
                    "product": iteration + 1,
                    "vertex": vertex,
                }
                extrema["pushed_lower_gap"] = minimum_update(
                    extrema["pushed_lower_gap"],
                    lower[vertex] - omniscient_lower[vertex],
                    witness,
                )
                extrema["current_gap"] = minimum_update(
                    extrema["current_gap"],
                    current[vertex] - omniscient_current[vertex],
                    witness,
                )
                extrema["extrapolate_gap"] = minimum_update(
                    extrema["extrapolate_gap"],
                    masked_extrapolate[vertex] - omniscient_extrapolate[vertex],
                    witness,
                )

            for vertex in certified & omniscient_face:
                auxiliary_gap = auxiliary[vertex] - omniscient_auxiliary[vertex]
                neighbor_flux = (
                    COUPLING
                    / (LIPSCHITZ * degrees[vertex])
                    * sum(
                        masked_extrapolate[neighbor] - omniscient_extrapolate[neighbor]
                        for neighbor in neighbors[vertex]
                    )
                )
                flux = ROOT * (1 - ROOT) * auxiliary_gap + 2 * neighbor_flux
                extrema["momentum_flux"] = minimum_update(
                    extrema["momentum_flux"],
                    flux,
                    {
                        "phase": phases,
                        "product": iteration + 1,
                        "vertex": vertex,
                    },
                )

            for vertex in omniscient_face - certified:
                zero_margin = -max(
                    omniscient_current[vertex],
                    omniscient_auxiliary[vertex],
                    omniscient_extrapolate[vertex],
                )
                extrema["exterior_current_zero_margin"] = minimum_update(
                    extrema["exterior_current_zero_margin"],
                    zero_margin,
                    {
                        "phase": phases,
                        "product": iteration + 1,
                        "vertex": vertex,
                    },
                )

            inner_width = max([F(0)] + [value / SHIFTED_GAP for value in full_residual])
            if inner_width <= old_width / 4:
                width = old_width / 2 + inner_width
                maximum_phase_products = max(maximum_phase_products, iteration + 1)
                break
        else:
            raise AssertionError("exact phase exceeded 100 products")
        phases += 1

    asserted_nonnegative = [
        "pushed_lower_gap",
        "pre_push_lower_gap",
        "starting_lower_one_step_gap",
        "relevant_starting_lower_one_step_gap",
        "current_gap",
        "extrapolate_gap",
        "momentum_flux",
        "boundary_flux",
        "boundary_layer",
        "exterior_current_zero_margin",
        "masked_raw_residual_margin",
    ]
    if not post_append_residual_push:
        asserted_nonnegative.append("masked_input_residual_margin")
    for name in asserted_nonnegative:
        record = extrema[name]
        if record is not None:
            assert record["value"] >= 0, (name, record)
    if extrema["shadow_cover_margin"] is not None:
        assert extrema["shadow_cover_margin"]["value"] >= 0
    assert certified.issubset(final_face)
    assert all(final_solution[i] >= lower[i] for i in range(vertex_count))

    return {
        "phases": phases,
        "products": products,
        "maximum_phase_products": maximum_phase_products,
        "events": events,
        "final_support_size": len(final_face),
        "extrema": extrema,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=4, choices=(2, 3, 4, 5))
    parser.add_argument("--root", default="1/2")
    parser.add_argument("--rho-fractions", default="1/10,1/2,9/10")
    parser.add_argument("--relative-width", default="1/64")
    parser.add_argument("--post-append-residual-push", action="store_true")
    parser.add_argument("--input-residual-append", action="store_true")
    args = parser.parse_args()
    configure(F(args.root))
    rho_fractions = tuple(F(value) for value in args.rho_fractions.split(","))
    relative_width = F(args.relative_width)
    pairs = list(itertools.combinations(range(args.vertices), 2))

    graph_count = 0
    run_count = 0
    global_extrema: dict[str, dict[str, object] | None] = {}
    maximum_products = 0
    maximum_phases = 0
    maximum_events = 0
    maximum_phase_products = 0

    for mask in range(1 << len(pairs)):
        neighbors = [set() for _ in range(args.vertices)]
        edges = []
        for index, (left, right) in enumerate(pairs):
            if mask >> index & 1:
                neighbors[left].add(right)
                neighbors[right].add(left)
                edges.append([left, right])
        if min(map(len, neighbors), default=0) == 0 or not connected(neighbors):
            continue
        graph_count += 1
        for rho_fraction in rho_fractions:
            result = audit_graph(
                neighbors,
                rho_fraction,
                relative_width,
                args.post_append_residual_push,
                args.input_residual_append,
            )
            run_count += 1
            maximum_products = max(maximum_products, int(result["products"]))
            maximum_phases = max(maximum_phases, int(result["phases"]))
            maximum_events = max(maximum_events, int(result["events"]))
            maximum_phase_products = max(
                maximum_phase_products,
                int(result["maximum_phase_products"]),
            )
            for name, record in result["extrema"].items():
                if record is None:
                    continue
                value = record["value"]
                previous = global_extrema.get(name)
                if previous is None or value < previous["value"]:
                    global_extrema[name] = {
                        **record,
                        "rho_fraction": rho_fraction,
                        "edges": edges,
                    }

    def serialize(value: object) -> object:
        if isinstance(value, F):
            return str(value)
        if isinstance(value, dict):
            return {key: serialize(item) for key, item in value.items()}
        if isinstance(value, list):
            return [serialize(item) for item in value]
        return value

    print(
        json.dumps(
            serialize(
                {
                    "warning": "finite fraction-exact audit, not a theorem",
                    "vertices": args.vertices,
                    "connected_graphs": graph_count,
                    "runs": run_count,
                    "alpha": ALPHA,
                    "retained_root": ROOT,
                    "rho_fractions": list(rho_fractions),
                    "relative_width": relative_width,
                    "post_append_residual_push": args.post_append_residual_push,
                    "input_residual_append": args.input_residual_append,
                    "maximum_phases": maximum_phases,
                    "maximum_products": maximum_products,
                    "maximum_phase_products": maximum_phase_products,
                    "maximum_events": maximum_events,
                    "minimum_exact_margins": global_extrema,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
