#!/usr/bin/env python3
"""Exact full comparison audit for the stronger beta-0.48662 limit graph."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04865_branch_boundary_exact import (
    BETA_04865_BRANCH_BOUNDARY_EDGES,
    BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH,
    BETA_04865_BRANCH_BOUNDARY_VERTICES,
)


BETA_04862_ZERO_ROOT_VERTICES = BETA_04865_BRANCH_BOUNDARY_VERTICES
BETA_04862_ZERO_ROOT_EDGES = tuple(
    sorted((set(BETA_04865_BRANCH_BOUNDARY_EDGES) - {(3, 11), (10, 11)}) | {(5, 26), (6, 11)})
)
BETA_04862_ZERO_ROOT_RHO_SCALE = F(15138865594, 1000000000000)
BETA_04862_ZERO_ROOT_RELATIVE_WIDTH = BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH
BETA_04862_ZERO_ROOT_STOP_BETA = F(48659, 100000)
BETA_04862_ZERO_ROOT_ALTERNATIVE_EDGES = tuple(
    sorted((set(BETA_04865_BRANCH_BOUNDARY_EDGES) - {(8, 9), (10, 11)}) | {(5, 26), (7, 8)})
)
# This permutation fixes the source and the entire failure-side module.
BETA_04862_ZERO_ROOT_ISOMORPHISM = (
    0,
    1,
    2,
    6,
    4,
    5,
    3,
    9,
    8,
    7,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
)

EXPECTED_POST_CLOSURE_ZEROS = {
    (4, 1): (8, 15),
    (5, 1): (24,),
    (6, 1): (7, 9),
    (9, 1): (10,),
    (15, 1): (19, 22, 23, 26),
    (20, 1): (25,),
}
EXPECTED_INHERITED_ZEROS = {
    (phase + 1, product): vertices
    for (phase, product), vertices in EXPECTED_POST_CLOSURE_ZEROS.items()
}


def minimum(current: F | None, value: F) -> F:
    return value if current is None or value < current else current


def audit_comparisons(
    neighbors: list[set[int]],
    source: int,
    *,
    rho_scale: F = BETA_04862_ZERO_ROOT_RHO_SCALE,
    relative_width: F = BETA_04862_ZERO_ROOT_RELATIVE_WIDTH,
    stop_beta: F = BETA_04862_ZERO_ROOT_STOP_BETA,
    expected_post_closure_zeros: dict[tuple[int, int], tuple[int, ...]] = (
        EXPECTED_POST_CLOSURE_ZEROS
    ),
    expected_inherited_zeros: dict[tuple[int, int], tuple[int, ...]] | None = None,
    expected_maximum_ties: tuple[tuple[int, int, tuple[int, ...]], ...] = (),
) -> dict[str, object]:
    """Replay every limiting comparison and classify every equality."""
    vertex_count = len(neighbors)
    vertices = set(range(vertex_count))
    degrees = [len(row) for row in neighbors]
    rho = rho_scale / degrees[source]
    if expected_inherited_zeros is None:
        expected_inherited_zeros = {
            (phase + 1, product): vertices
            for (phase, product), vertices in expected_post_closure_zeros.items()
        }
    zero = F(0)

    def apply_limit(state: list[F], vertex: int) -> F:
        return state[vertex] / 2 - sum(
            (state[neighbor] for neighbor in neighbors[vertex]),
            zero,
        ) / (2 * degrees[vertex])

    def residual(load: list[F], state: list[F]) -> list[F]:
        return [load[v] - apply_limit(state, v) for v in range(vertex_count)]

    strict_margins: dict[str, F | None] = {
        "active_input": None,
        "exterior_input": None,
        "raw_velocity": None,
        "lower_clamp": None,
        "pre_push": None,
        "closure_test": None,
        "post_closure_active": None,
        "unique_maximum": None,
        "maximum_to_next_distinct": None,
        "stop": None,
    }

    def record(name: str, value: F) -> None:
        assert value > 0
        strict_margins[name] = minimum(strict_margins[name], value)

    load = [-rho for _ in range(vertex_count)]
    load[source] += F(1, degrees[source])
    lower = [zero for _ in range(vertex_count)]
    certified = {source}
    width = F(1, degrees[source]) - rho
    target_width = relative_width * width
    total_products = 0
    active_input_zeros: dict[tuple[int, int], tuple[int, ...]] = {}
    raw_velocity_zeros: dict[tuple[int, int], tuple[int, ...]] = {}
    lower_clamp_ties: dict[tuple[int, int], tuple[int, ...]] = {}
    post_closure_zeros: dict[tuple[int, int], tuple[int, ...]] = {}
    zero_exterior_inputs: list[tuple[int, int, int]] = []
    zero_pre_push: list[tuple[int, int, int]] = []
    zero_closure_tests: list[tuple[int, int, int, int]] = []
    maximum_ties: list[tuple[int, int, tuple[int, ...]]] = []
    maximum_tie_certificates: list[dict[str, object]] = []
    stop_ties: list[tuple[int, int]] = []
    structural_certificates: list[dict[str, object]] = []
    failure = None
    phase = 0

    while width > target_width and failure is None:
        phase += 1
        old_width = width
        current = lower[:]
        velocity = [zero for _ in range(vertex_count)]
        for product in range(1, 101):
            extrapolate = [zero for _ in range(vertex_count)]
            for vertex in certified:
                extrapolate[vertex] = current[vertex] + velocity[vertex]
            input_residual = residual(load, extrapolate)

            active_zeros = tuple(sorted(v for v in certified if input_residual[v] == 0))
            if active_zeros:
                active_input_zeros[(phase, product)] = active_zeros
            for vertex in certified:
                if input_residual[vertex] != 0:
                    record("active_input", abs(input_residual[vertex]))
            outside = vertices - certified
            for vertex in outside:
                if input_residual[vertex] == 0:
                    zero_exterior_inputs.append((phase, product, vertex))
                else:
                    record("exterior_input", abs(input_residual[vertex]))

            input_batch = sorted(v for v in outside if input_residual[v] > 0)
            certified.update(input_batch)
            face = sorted(certified)
            negative_active = [v for v in face if input_residual[v] < 0]
            if negative_active:
                vertex = min(negative_active, key=lambda v: input_residual[v])
                failure = {
                    "phase": phase,
                    "product": product,
                    "vertex": vertex,
                    "scaled_input_residual": input_residual[vertex],
                    "input_batch": input_batch,
                    "face": face,
                }
                break

            old_current = current
            following = [zero for _ in range(vertex_count)]
            for vertex in face:
                following[vertex] = extrapolate[vertex] + input_residual[vertex]
            raw_velocity = [following[v] - old_current[v] for v in range(vertex_count)]
            raw_zeros = tuple(sorted(v for v in face if raw_velocity[v] == 0))
            if raw_zeros:
                raw_velocity_zeros[(phase, product)] = raw_zeros
            clamp_ties = []
            for vertex in face:
                if raw_velocity[vertex] != 0:
                    record("raw_velocity", abs(raw_velocity[vertex]))
                arguments = (lower[vertex], following[vertex], zero)
                maximum = max(arguments)
                if sum(argument == maximum for argument in arguments) > 1:
                    clamp_ties.append(vertex)
                    assert lower[vertex] == following[vertex] > 0
                else:
                    ordered_arguments = sorted(arguments, reverse=True)
                    record("lower_clamp", ordered_arguments[0] - ordered_arguments[1])
                lower[vertex] = maximum
                current[vertex] = lower[vertex]
                velocity[vertex] = max(raw_velocity[vertex], zero)
            if clamp_ties:
                lower_clamp_ties[(phase, product)] = tuple(clamp_ties)

            full_residual = residual(load, lower)
            active_push = [v for v in face if full_residual[v] > 0]
            for vertex, value in enumerate(full_residual):
                if value == 0:
                    zero_pre_push.append((phase, product, vertex))
                else:
                    record("pre_push", abs(value))
            for vertex in active_push:
                lower[vertex] += 2 * full_residual[vertex]
                current[vertex] = lower[vertex]
            full_residual = residual(load, lower)

            closure_batches: list[tuple[int, ...]] = []
            closure_round = 0
            while True:
                outside = vertices - certified
                for vertex in outside:
                    if full_residual[vertex] == 0:
                        zero_closure_tests.append((phase, product, closure_round, vertex))
                    else:
                        record("closure_test", abs(full_residual[vertex]))
                batch = tuple(sorted(v for v in outside if full_residual[v] > 0))
                if not batch:
                    break
                closure_batches.append(batch)
                for vertex in batch:
                    lower[vertex] += 2 * full_residual[vertex]
                    current[vertex] = lower[vertex]
                    velocity[vertex] = zero
                certified.update(batch)
                full_residual = residual(load, lower)
                closure_round += 1

            post_zeros = tuple(v for v in sorted(certified) if full_residual[v] == 0)
            if post_zeros:
                post_closure_zeros[(phase, product)] = post_zeros
                pushed_at = {
                    vertex: index for index, batch in enumerate(closure_batches) for vertex in batch
                }
                for vertex in post_zeros:
                    assert vertex in pushed_at
                    index = pushed_at[vertex]
                    same_or_later = set().union(*closure_batches[index:]) - {vertex}
                    assert neighbors[vertex].isdisjoint(same_or_later)
                structural_certificates.append(
                    {
                        "phase": phase,
                        "product": product,
                        "zero_vertices": post_zeros,
                        "closure_batches": closure_batches,
                        "reason": (
                            "direct diagonal cancellation and no same/later pushed neighbor"
                        ),
                    }
                )
            for vertex in certified:
                if full_residual[vertex] != 0:
                    record("post_closure_active", abs(full_residual[vertex]))
            assert all(full_residual[v] >= 0 for v in certified)
            assert all(full_residual[v] < 0 for v in vertices - certified)

            ordered = sorted(
                ((value, vertex) for vertex, value in enumerate(full_residual)),
                reverse=True,
            )
            maximum_value = ordered[0][0]
            maximizers = tuple(
                sorted(vertex for value, vertex in ordered if value == maximum_value)
            )
            if len(maximizers) > 1:
                maximum_ties.append((phase, product, maximizers))
                reference = maximizers[0]
                assert reference != source
                assert all(
                    vertex != source and neighbors[vertex] == neighbors[reference]
                    for vertex in maximizers[1:]
                )
                maximum_tie_certificates.append(
                    {
                        "phase": phase,
                        "product": product,
                        "vertices": maximizers,
                        "common_neighbors": tuple(sorted(neighbors[reference])),
                        "reason": "source-preserving graph twins have identical residuals",
                    }
                )
            else:
                record("unique_maximum", maximum_value - ordered[1][0])
            distinct_values = sorted({value for value, _ in ordered}, reverse=True)
            assert len(distinct_values) >= 2
            record(
                "maximum_to_next_distinct",
                distinct_values[0] - distinct_values[1],
            )
            inner_width = max(maximum_value, zero) / 2
            ratio = inner_width / old_width
            if ratio == stop_beta:
                stop_ties.append((phase, product))
            else:
                record("stop", abs(ratio - stop_beta))
            total_products += 1
            if ratio <= stop_beta:
                width = old_width / 2 + inner_width
                break
        else:
            raise AssertionError("unexpected product limit")

    assert failure is not None
    assert active_input_zeros == expected_inherited_zeros
    assert raw_velocity_zeros == expected_inherited_zeros
    assert lower_clamp_ties == expected_inherited_zeros
    assert post_closure_zeros == expected_post_closure_zeros
    assert not zero_exterior_inputs
    assert not zero_pre_push
    assert not zero_closure_tests
    assert tuple(maximum_ties) == expected_maximum_ties
    assert not stop_ties
    forced_post_closure_coordinate_count = sum(len(row) for row in post_closure_zeros.values())
    forced_inherited_coordinate_count = sum(len(row) for row in active_input_zeros.values())
    assert sum(len(row) for row in raw_velocity_zeros.values()) == forced_inherited_coordinate_count
    assert sum(len(row) for row in lower_clamp_ties.values()) == forced_inherited_coordinate_count
    assert strict_margins["unique_maximum"] > 0
    assert strict_margins["maximum_to_next_distinct"] > 0
    assert strict_margins["stop"] > 0
    assert failure["scaled_input_residual"] < 0

    return {
        "failure": failure,
        "total_products": total_products,
        "grouped_equality_event_count": (
            len(expected_post_closure_zeros) + 3 * len(expected_inherited_zeros)
        ),
        # Kept for backward compatibility with witnesses where every
        # post-closure zero is inherited after a stopped product.
        "forced_coordinate_count_per_kind": forced_post_closure_coordinate_count,
        "forced_coordinate_counts_by_kind": {
            "post_closure_active": forced_post_closure_coordinate_count,
            "active_input": forced_inherited_coordinate_count,
            "raw_velocity": forced_inherited_coordinate_count,
            "lower_clamp": forced_inherited_coordinate_count,
        },
        "forced_post_closure_zeros": post_closure_zeros,
        "forced_next_phase_active_input_zeros": active_input_zeros,
        "forced_next_phase_raw_velocity_zeros": raw_velocity_zeros,
        "forced_next_phase_lower_clamp_ties": lower_clamp_ties,
        "structural_zero_certificates": structural_certificates,
        "zero_exterior_input_comparisons": zero_exterior_inputs,
        "zero_pre_push_comparisons": zero_pre_push,
        "zero_closure_comparisons": zero_closure_tests,
        "maximum_ties": maximum_ties,
        "structural_maximum_tie_certificates": maximum_tie_certificates,
        "stop_ties": stop_ties,
        "minimum_strict_margins": strict_margins,
    }


def expected_equality_events(
    post_closure_zeros: dict[tuple[int, int], tuple[int, ...]] = (EXPECTED_POST_CLOSURE_ZEROS),
) -> list[dict[str, object]]:
    events = []
    for (phase, product), vertices in post_closure_zeros.items():
        events.append(
            {
                "kind": "final_active_residual",
                "phase": phase,
                "product": product,
                "vertices": list(vertices),
            }
        )
        inherited_phase = phase + 1
        for kind in (
            "active_input_residual",
            "raw_velocity",
            "lower_clamp_argument",
        ):
            events.append(
                {
                    "kind": kind,
                    "phase": inherited_phase,
                    "product": product,
                    "vertices": list(vertices),
                }
            )
    return events


def expected_complete_equality_events(
    post_closure_zeros: dict[tuple[int, int], tuple[int, ...]],
    maximum_ties: tuple[tuple[int, int, tuple[int, ...]], ...],
) -> list[dict[str, object]]:
    """Merge forced zero/clamp events and maximum ties in trace order."""
    staged: list[tuple[int, int, int, dict[str, object]]] = []
    stage = {
        "active_input_residual": 1,
        "raw_velocity": 2,
        "lower_clamp_argument": 3,
        "final_active_residual": 4,
        "maximum_residual": 5,
    }
    for event in expected_equality_events(post_closure_zeros):
        staged.append(
            (
                int(event["phase"]),
                int(event["product"]),
                stage[str(event["kind"])],
                event,
            )
        )
    for phase, product, vertices in maximum_ties:
        event = {
            "kind": "maximum_residual",
            "phase": phase,
            "product": product,
            "vertices": list(vertices),
        }
        staged.append((phase, product, stage["maximum_residual"], event))
    return [event for _, _, _, event in sorted(staged, key=lambda item: item[:3])]


def main() -> None:
    relabeled_edges = {
        tuple(
            sorted(
                (BETA_04862_ZERO_ROOT_ISOMORPHISM[left], BETA_04862_ZERO_ROOT_ISOMORPHISM[right])
            )
        )
        for left, right in BETA_04862_ZERO_ROOT_EDGES
    }
    assert relabeled_edges == set(BETA_04862_ZERO_ROOT_ALTERNATIVE_EDGES)
    assert BETA_04862_ZERO_ROOT_ISOMORPHISM[0] == 0
    neighbors, source = build_graph(
        {
            "vertices": BETA_04862_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04862_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_04862_ZERO_ROOT_EDGES) == len(set(BETA_04862_ZERO_ROOT_EDGES)) == 64
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04862_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04862_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04862_ZERO_ROOT_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 31
    lower, upper = result["cell"]
    assert F(48652, 100000) < lower < F(48654, 100000)
    assert F(48662, 100000) < upper < F(48663, 100000)
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (25, 8, 14)
    assert failure["input_batch"] == []
    assert failure["face"] == list(range(20)) + [22, 23, 24, 25, 26]
    assert failure["scaled_input_residual"] < -F(1, 1000000)

    phase_25 = result["phases"][-1]["products"]
    ratio_3 = phase_25[2]["inner_width_over_old_width"]
    ratio_7 = phase_25[6]["inner_width_over_old_width"]
    assert ratio_7 == upper
    assert 0 < ratio_3 - ratio_7 < F(1, 10000000000)
    expected_events = expected_equality_events()
    assert result["equality_events"] == expected_events

    audit = audit_comparisons(neighbors, source)
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] == len(expected_events)
    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04862_ZERO_ROOT_VERTICES,
                    "edges": BETA_04862_ZERO_ROOT_EDGES,
                    "source": source,
                    "rho_scale": BETA_04862_ZERO_ROOT_RHO_SCALE,
                    "relative_width": BETA_04862_ZERO_ROOT_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_04862_ZERO_ROOT_STOP_BETA,
                    "same_chronology_stop_beta_interval": {
                        "lower": lower,
                        "lower_inclusive": True,
                        "upper": upper,
                        "upper_inclusive": False,
                    },
                    "product_3_minus_product_7_ratio": ratio_3 - ratio_7,
                    "isomorphic_alternative": {
                        "edges": BETA_04862_ZERO_ROOT_ALTERNATIVE_EDGES,
                        "source_preserving_vertex_map": (BETA_04862_ZERO_ROOT_ISOMORPHISM),
                    },
                    "comparison_audit": audit,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
