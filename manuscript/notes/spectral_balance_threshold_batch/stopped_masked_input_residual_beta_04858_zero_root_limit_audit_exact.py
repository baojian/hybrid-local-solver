#!/usr/bin/env python3
"""Exact branch-comparison audit for the beta-0.48658 zero-root limit."""

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


ZERO_ROOT_RHO_SCALE = F(756368559, 50000000000)
ZERO_ROOT_STOP_BETA = F(48657, 100000)

EXPECTED_POST_CLOSURE_ZEROS = {
    (4, 1): (5, 8, 15),
    (5, 1): (7, 24),
    (6, 1): (11,),
    (7, 1): (9,),
    (9, 1): (10,),
    (15, 1): (19, 22, 23),
    (16, 1): (26,),
    (20, 1): (25,),
}
EXPECTED_INHERITED_ZEROS = {
    (phase + 1, product): vertices
    for (phase, product), vertices in EXPECTED_POST_CLOSURE_ZEROS.items()
}


def minimum(current: F | None, value: F) -> F:
    return value if current is None or value < current else current


def audit_comparisons(neighbors: list[set[int]], source: int) -> dict[str, object]:
    """Replay the limit recurrence and classify every exact zero or tie."""
    vertex_count = len(neighbors)
    vertices = set(range(vertex_count))
    degrees = [len(row) for row in neighbors]
    rho = ZERO_ROOT_RHO_SCALE / degrees[source]
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
        "pre_push": None,
        "closure_test": None,
        "unique_maximum": None,
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
    target_width = BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH * width
    total_products = 0
    active_input_zeros: dict[tuple[int, int], tuple[int, ...]] = {}
    raw_velocity_zeros: dict[tuple[int, int], tuple[int, ...]] = {}
    post_closure_zeros: dict[tuple[int, int], tuple[int, ...]] = {}
    zero_exterior_inputs: list[tuple[int, int, int]] = []
    zero_pre_push: list[tuple[int, int, int]] = []
    zero_closure_tests: list[tuple[int, int, int, int]] = []
    maximum_ties: list[tuple[int, int, tuple[int, ...]]] = []
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

            active_zeros = tuple(
                sorted(v for v in certified if input_residual[v] == 0)
            )
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
            for vertex in face:
                if raw_velocity[vertex] != 0:
                    record("raw_velocity", abs(raw_velocity[vertex]))
                lower[vertex] = max(lower[vertex], following[vertex], zero)
                current[vertex] = lower[vertex]
                velocity[vertex] = max(raw_velocity[vertex], zero)

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
                        zero_closure_tests.append(
                            (phase, product, closure_round, vertex)
                        )
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
                    vertex: index
                    for index, batch in enumerate(closure_batches)
                    for vertex in batch
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
                        "reason": "direct diagonal cancellation and no same/later pushed neighbor",
                    }
                )
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
            else:
                record("unique_maximum", maximum_value - ordered[1][0])
            inner_width = max(maximum_value, zero) / 2
            ratio = inner_width / old_width
            if ratio == ZERO_ROOT_STOP_BETA:
                stop_ties.append((phase, product))
            else:
                record("stop", abs(ratio - ZERO_ROOT_STOP_BETA))
            total_products += 1
            if ratio <= ZERO_ROOT_STOP_BETA:
                width = old_width / 2 + inner_width
                break
        else:
            raise AssertionError("unexpected product limit")

    assert failure is not None
    assert active_input_zeros == EXPECTED_INHERITED_ZEROS
    assert raw_velocity_zeros == EXPECTED_INHERITED_ZEROS
    assert post_closure_zeros == EXPECTED_POST_CLOSURE_ZEROS
    assert not zero_exterior_inputs
    assert not zero_pre_push
    assert not zero_closure_tests
    assert not maximum_ties
    assert not stop_ties
    assert sum(len(row) for row in post_closure_zeros.values()) == 13
    assert sum(len(row) for row in active_input_zeros.values()) == 13
    assert sum(len(row) for row in raw_velocity_zeros.values()) == 13
    assert strict_margins["unique_maximum"] > F(4, 100000000)
    assert strict_margins["stop"] > F(1, 100000)
    assert failure["scaled_input_residual"] < -F(1, 1000000)

    return {
        "failure": failure,
        "total_products": total_products,
        "zero_comparison_count": 39,
        "forced_post_closure_zeros": post_closure_zeros,
        "forced_next_phase_active_input_zeros": active_input_zeros,
        "forced_next_phase_raw_velocity_zeros": raw_velocity_zeros,
        "structural_zero_certificates": structural_certificates,
        "zero_exterior_input_comparisons": zero_exterior_inputs,
        "zero_pre_push_comparisons": zero_pre_push,
        "zero_closure_comparisons": zero_closure_tests,
        "maximum_ties": maximum_ties,
        "stop_ties": stop_ties,
        "minimum_strict_margins": strict_margins,
    }


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04865_BRANCH_BOUNDARY_VERTICES,
            "edges": list(BETA_04865_BRANCH_BOUNDARY_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04865_BRANCH_BOUNDARY_EDGES)
        == len(set(BETA_04865_BRANCH_BOUNDARY_EDGES))
        == 64
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH,
        stop_beta=ZERO_ROOT_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 31
    lower, upper = result["cell"]
    assert F(48649, 100000) < lower < F(48650, 100000)
    assert F(48658, 100000) < upper < F(48659, 100000)
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (25, 8, 14)
    assert failure["input_batch"] == []
    assert failure["face"] == list(range(20)) + [22, 23, 24, 25, 26]
    assert failure["scaled_input_residual"] < -F(1, 1000000)

    phase_25 = result["phases"][-1]["products"]
    ratio_3 = phase_25[2]["inner_width_over_old_width"]
    ratio_7 = phase_25[6]["inner_width_over_old_width"]
    assert ratio_3 == upper
    assert 0 < ratio_7 - ratio_3 < F(1, 10000000000)

    audit = audit_comparisons(neighbors, source)
    assert audit["failure"] == failure
    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_zeros",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04865_BRANCH_BOUNDARY_VERTICES,
                    "edges": BETA_04865_BRANCH_BOUNDARY_EDGES,
                    "source": source,
                    "rho_scale": ZERO_ROOT_RHO_SCALE,
                    "relative_width": BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH,
                    "chosen_stop_beta": ZERO_ROOT_STOP_BETA,
                    "same_chronology_stop_beta_interval": {
                        "lower": lower,
                        "lower_inclusive": True,
                        "upper": upper,
                        "upper_inclusive": False,
                    },
                    "product_7_minus_product_3_ratio": ratio_7 - ratio_3,
                    "comparison_audit": audit,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
