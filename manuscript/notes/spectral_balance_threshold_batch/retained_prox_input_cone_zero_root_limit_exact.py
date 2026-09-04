#!/usr/bin/env python3
"""Fraction-exact ``s -> 0`` limit of the stopped input-cone trace.

This is an unregistered research companion.  It evaluates the removable
small-root limit proved in ``BETA_STOP_CLOCK_GLUING_AUDIT.md``.  States and
residuals are divided by ``alpha`` before taking the limit.  The apparently
singular auxiliary coefficient is represented by the surviving positive
velocity ``max(current - previous, 0)``.

The routine is useful only when all branch comparisons in the returned
finite prefix are strict.  It is not a substitute for a positive-root exact
certificate; rather, it computes the rational endpoint to which such
certificates converge on a fixed chronology branch.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    fraction,
    load_json_argument,
    serialize,
)


def trace_zero_root_limit(
    neighbors: list[set[int]],
    *,
    source: int,
    rho_scale: F,
    relative_width: F,
    stop_beta: F,
    maximum_phase_products: int = 100,
    maximum_phases: int = 70,
) -> dict[str, object]:
    """Run the exact scaled-state chronology at retained root ``s=0``."""
    if not 0 < rho_scale < 1:
        raise ValueError("rho_scale must lie in (0,1)")
    if not 0 < relative_width < 1:
        raise ValueError("relative_width must lie in (0,1)")
    if not 0 < stop_beta < F(1, 2):
        raise ValueError("stop_beta must lie in (0,1/2)")

    vertex_count = len(neighbors)
    degrees = [len(row) for row in neighbors]
    rho = rho_scale / degrees[source]
    half = F(1, 2)
    zero = F(0)

    def apply_limit(state: list[F], vertex: int) -> F:
        return half * state[vertex] - half / degrees[vertex] * sum(
            (state[neighbor] for neighbor in neighbors[vertex]),
            zero,
        )

    def residual(load: list[F], state: list[F]) -> list[F]:
        return [load[v] - apply_limit(state, v) for v in range(vertex_count)]

    # This is lim_(alpha->0) original_load / alpha.
    load = [-rho for _ in range(vertex_count)]
    load[source] += F(1, degrees[source])
    lower = [zero for _ in range(vertex_count)]
    certified = {source}
    width = F(1, degrees[source]) - rho
    target_width = relative_width * width
    chronology_lower = zero
    chronology_upper = half
    total_products = 0
    phases: list[dict[str, object]] = []
    # Exact equality events are the only places where a branch of the
    # limiting recurrence need not persist automatically for positive root.
    # Keep a compact ledger so a claimed small-root continuation can classify
    # every tie as either algebraically forced or requiring higher order.
    equality_events: list[dict[str, object]] = []

    def record_zeros(
        kind: str,
        values: list[F],
        vertices: list[int],
        *,
        phase: int,
        product: int,
        closure_round: int | None = None,
    ) -> None:
        zeros = [vertex for vertex in vertices if values[vertex] == 0]
        if zeros:
            event: dict[str, object] = {
                "kind": kind,
                "phase": phase,
                "product": product,
                "vertices": zeros,
            }
            if closure_round is not None:
                event["closure_round"] = closure_round
            equality_events.append(event)

    while width > target_width:
        if len(phases) >= maximum_phases:
            return {
                "status": "phase_limit",
                "phases": phases,
                "total_products": total_products,
                "cell": [chronology_lower, chronology_upper],
            }
        old_width = width
        current = lower[:]
        velocity = [zero for _ in range(vertex_count)]
        phase_products: list[dict[str, object]] = []

        for product in range(1, maximum_phase_products + 1):
            extrapolate = [zero for _ in range(vertex_count)]
            for vertex in certified:
                extrapolate[vertex] = current[vertex] + velocity[vertex]
            input_residual = residual(load, extrapolate)
            outside_before_input = [
                vertex for vertex in range(vertex_count) if vertex not in certified
            ]
            record_zeros(
                "input_frontier_residual",
                input_residual,
                outside_before_input,
                phase=len(phases) + 1,
                product=product,
            )
            input_batch = [
                vertex
                for vertex in range(vertex_count)
                if vertex not in certified and input_residual[vertex] > 0
            ]
            certified.update(input_batch)
            face = sorted(certified)
            input_vertex = min(face, key=lambda vertex: input_residual[vertex])
            input_value = input_residual[input_vertex]
            record_zeros(
                "active_input_residual",
                input_residual,
                face,
                phase=len(phases) + 1,
                product=product,
            )
            if input_value < 0:
                phase_products.append(
                    {
                        "product": product,
                        "executed": False,
                        "input_vertex": input_vertex,
                        "input_residual": input_value,
                        "input_batch": input_batch,
                    }
                )
                phases.append(
                    {
                        "phase": len(phases) + 1,
                        "old_width": old_width,
                        "products": phase_products,
                        "stopped": False,
                    }
                )
                return {
                    "status": "counterexample",
                    "phases": phases,
                    "total_products": total_products,
                    "cell": [chronology_lower, chronology_upper],
                    "failure": {
                        "phase": len(phases),
                        "product": product,
                        "vertex": input_vertex,
                        "scaled_input_residual": input_value,
                        "input_batch": input_batch,
                        "face": face,
                    },
                    "equality_events": equality_events,
                }

            old_current = current
            following = [zero for _ in range(vertex_count)]
            for vertex in face:
                following[vertex] = extrapolate[vertex] + input_residual[vertex]
            raw_velocity = [
                following[vertex] - old_current[vertex]
                for vertex in range(vertex_count)
            ]
            record_zeros(
                "raw_velocity",
                raw_velocity,
                face,
                phase=len(phases) + 1,
                product=product,
            )
            lower_before_clamp = lower[:]
            lower_ties = []
            for vertex in face:
                clamp_arguments = (
                    lower_before_clamp[vertex],
                    following[vertex],
                    zero,
                )
                clamp_maximum = max(clamp_arguments)
                if sum(value == clamp_maximum for value in clamp_arguments) > 1:
                    lower_ties.append(vertex)
            if lower_ties:
                equality_events.append(
                    {
                        "kind": "lower_clamp_argument",
                        "phase": len(phases) + 1,
                        "product": product,
                        "vertices": lower_ties,
                    }
                )
            for vertex in face:
                lower[vertex] = max(lower[vertex], following[vertex], zero)
                current[vertex] = lower[vertex]
                velocity[vertex] = max(raw_velocity[vertex], zero)

            full_residual = residual(load, lower)
            record_zeros(
                "pre_push_residual",
                full_residual,
                face,
                phase=len(phases) + 1,
                product=product,
            )
            active_push = [vertex for vertex in face if full_residual[vertex] > 0]
            for vertex in active_push:
                lower[vertex] += 2 * full_residual[vertex]
                current[vertex] = lower[vertex]
            full_residual = residual(load, lower)
            closure_round = 0
            closure_batches: list[list[int]] = []
            while True:
                closure_round += 1
                outside_before_closure = [
                    vertex for vertex in range(vertex_count) if vertex not in certified
                ]
                record_zeros(
                    "closure_residual",
                    full_residual,
                    outside_before_closure,
                    phase=len(phases) + 1,
                    product=product,
                    closure_round=closure_round,
                )
                batch = [
                    vertex
                    for vertex in range(vertex_count)
                    if vertex not in certified and full_residual[vertex] > 0
                ]
                if not batch:
                    break
                closure_batches.append(batch)
                for vertex in batch:
                    lower[vertex] += 2 * full_residual[vertex]
                    current[vertex] = lower[vertex]
                    velocity[vertex] = zero
                certified.update(batch)
                full_residual = residual(load, lower)

            assert all(full_residual[vertex] >= 0 for vertex in certified)
            assert all(
                full_residual[vertex] <= 0
                for vertex in set(range(vertex_count)) - certified
            )
            record_zeros(
                "final_active_residual",
                full_residual,
                sorted(certified),
                phase=len(phases) + 1,
                product=product,
            )
            record_zeros(
                "final_exterior_residual",
                full_residual,
                sorted(set(range(vertex_count)) - certified),
                phase=len(phases) + 1,
                product=product,
            )
            maximum_vertex = max(
                range(vertex_count),
                key=lambda vertex: full_residual[vertex],
            )
            maximum_residual = max(full_residual[maximum_vertex], zero)
            maximum_ties = [
                vertex
                for vertex, value in enumerate(full_residual)
                if value == maximum_residual
            ]
            if len(maximum_ties) > 1:
                equality_events.append(
                    {
                        "kind": "maximum_residual",
                        "phase": len(phases) + 1,
                        "product": product,
                        "vertices": maximum_ties,
                    }
                )
            inner_width = maximum_residual / 2
            ratio = inner_width / old_width
            stop = ratio <= stop_beta
            if ratio == stop_beta:
                equality_events.append(
                    {
                        "kind": "stop_threshold",
                        "phase": len(phases) + 1,
                        "product": product,
                        "vertices": [maximum_vertex],
                    }
                )
            if stop:
                chronology_lower = max(chronology_lower, ratio)
            else:
                chronology_upper = min(chronology_upper, ratio)
            phase_products.append(
                {
                    "product": product,
                    "executed": True,
                    "input_vertex": input_vertex,
                    "input_residual": input_value,
                    "input_batch": input_batch,
                    "active_push": active_push,
                    "closure_batches": closure_batches,
                    "maximum_vertex": maximum_vertex,
                    "inner_width_over_old_width": ratio,
                    "stop": stop,
                }
            )
            total_products += 1
            if stop:
                width = old_width / 2 + inner_width
                phases.append(
                    {
                        "phase": len(phases) + 1,
                        "old_width": old_width,
                        "new_width": width,
                        "products": phase_products,
                        "stopped": True,
                    }
                )
                break
        else:
            return {
                "status": "product_limit",
                "phases": phases,
                "total_products": total_products,
                "cell": [chronology_lower, chronology_upper],
            }

    return {
        "status": "pass",
        "phases": phases,
        "total_products": total_products,
        "cell": [chronology_lower, chronology_upper],
        "equality_events": equality_events,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", required=True, type=load_json_argument)
    parser.add_argument("--source", type=int)
    parser.add_argument("--rho-scale", required=True, type=fraction)
    parser.add_argument("--relative-width", type=fraction, default=F(1, 1000))
    parser.add_argument("--stop-beta", required=True, type=fraction)
    args = parser.parse_args()
    neighbors, source = build_graph(args.graph, args.source)
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=args.rho_scale,
        relative_width=args.relative_width,
        stop_beta=args.stop_beta,
    )
    print(json.dumps(serialize(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
