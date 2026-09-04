#!/usr/bin/env python3
"""Exact beta=.482 stopped-input-cone counterexample on a unit graph."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)
from stopped_masked_input_residual_beta_048_counterexample_exact import (
    BETA_048_EDGES,
    BETA_048_RELATIVE_WIDTH,
    BETA_048_ROOT,
    BETA_048_VERTICES,
)


BETA_0482_VERTICES = BETA_048_VERTICES
BETA_0482_EDGES = tuple(
    sorted((set(BETA_048_EDGES) - {(13, 17)}) | {(3, 9), (4, 9)})
)
BETA_0482_ROOT = BETA_048_ROOT
BETA_0482_RHO_SCALE = F(3297, 200000)
BETA_0482_RELATIVE_WIDTH = BETA_048_RELATIVE_WIDTH
BETA_0482_STOP_BETA = F(241, 500)


def main() -> None:
    """Replay the full chronology and independently reconstruct its beta cell."""
    neighbors, source = build_graph(
        {
            "vertices": BETA_0482_VERTICES,
            "edges": list(BETA_0482_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_0482_EDGES) == len(set(BETA_0482_EDGES)) == 60
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=BETA_0482_ROOT,
        rho_scale=BETA_0482_RHO_SCALE,
        relative_width=BETA_0482_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=BETA_0482_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 29
    witness = result["first_negative_active_input_residual"]
    assert (witness["phase"], witness["product"], witness["vertex"]) == (23, 8, 15)
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(19)) + [24, 25, 26]
    assert witness["value"] < 0
    assert witness["preceding_inner_width_over_old_width"] > BETA_0482_STOP_BETA

    stopped: list[tuple[F, int, int]] = []
    continued: list[tuple[F, int, int]] = []
    for phase in result["phases"]:
        for product in phase["products"]:
            stop = product.get("stop")
            if stop is None:
                continue
            entry = (
                stop["inner_width_over_old_width"],
                phase["phase"],
                product["product"],
            )
            (stopped if stop["decision"] else continued).append(entry)
    lower, lower_phase, lower_product = max(stopped)
    upper, upper_phase, upper_product = min(continued)
    assert (lower_phase, lower_product) == (22, 1)
    assert (upper_phase, upper_product) == (23, 7)
    assert F(4799, 10000) < lower < F(4800, 10000)
    assert F(4824, 10000) < upper < F(4825, 10000)
    assert lower <= BETA_0482_STOP_BETA < upper
    reported_cell = result["same_chronology_stop_beta_interval"]
    assert reported_cell == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }

    alpha = BETA_0482_ROOT * BETA_0482_ROOT / (2 - BETA_0482_ROOT**2)
    rho = BETA_0482_RHO_SCALE / len(neighbors[source])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_0482_VERTICES,
                    "edges": BETA_0482_EDGES,
                    "source": source,
                    "root": BETA_0482_ROOT,
                    "alpha": alpha,
                    "rho_scale": BETA_0482_RHO_SCALE,
                    "rho": rho,
                    "relative_width": BETA_0482_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_0482_STOP_BETA,
                    "same_chronology_stop_beta_interval": reported_cell,
                    "chronology_cell_attainment": {
                        "lower_attained_at": [lower_phase, lower_product],
                        "upper_attained_at": [upper_phase, upper_product],
                    },
                    "completed_products_before_failure": result["total_products"],
                    "failure_phase_one_based": witness["phase"],
                    "failure_product_in_phase_one_based": witness["product"],
                    "failure_vertex": witness["vertex"],
                    "input_batch_at_failure": witness["input_batch"],
                    "failure_face": witness["face"],
                    "degree_residual_over_phase_width": witness["value"]
                    / witness["phase_old_width"],
                    "preceding_inner_width_over_phase_width": witness[
                        "preceding_inner_width_over_old_width"
                    ],
                    "claim": (
                        "the strict counterexample persists throughout the exact "
                        "half-open beta cell"
                    ),
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
