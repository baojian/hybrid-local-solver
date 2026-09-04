#!/usr/bin/env python3
"""Exact positive-root four-leaf counterexample at beta=.4875."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)
from stopped_masked_input_residual_beta_04865_branch_boundary_exact import (
    BETA_04865_BRANCH_BOUNDARY_EDGES,
    BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH,
)


BETA_04877_FOUR_LEAF_VERTICES = 31
BETA_04877_FOUR_LEAF_EDGES = tuple(
    sorted(
        set(BETA_04865_BRANCH_BOUNDARY_EDGES)
        | {(4, 27), (15, 28), (2, 29), (13, 30)}
    )
)
BETA_04877_FOUR_LEAF_ROOT = F(1, 1048576)
BETA_04877_FOUR_LEAF_RHO_SCALE = F(7053, 500000)
BETA_04877_FOUR_LEAF_RELATIVE_WIDTH = BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH
BETA_04877_FOUR_LEAF_STOP_BETA = F(39, 80)


def main() -> None:
    """Replay the exact chronology and reconstruct its beta cell."""
    neighbors, source = build_graph(
        {
            "vertices": BETA_04877_FOUR_LEAF_VERTICES,
            "edges": list(BETA_04877_FOUR_LEAF_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_04877_FOUR_LEAF_EDGES) == 68
    assert len(BETA_04877_FOUR_LEAF_EDGES) == len(
        set(BETA_04877_FOUR_LEAF_EDGES)
    )
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=BETA_04877_FOUR_LEAF_ROOT,
        rho_scale=BETA_04877_FOUR_LEAF_RHO_SCALE,
        relative_width=BETA_04877_FOUR_LEAF_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=BETA_04877_FOUR_LEAF_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 30
    witness = result["first_negative_active_input_residual"]
    assert (witness["phase"], witness["product"], witness["vertex"]) == (
        24,
        8,
        28,
    )
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(20)) + list(range(22, 31))
    assert witness["value"] < 0

    stopped: list[tuple[F, int, int, int]] = []
    continued: list[tuple[F, int, int, int]] = []
    for phase in result["phases"]:
        for product in phase["products"]:
            stop = product.get("stop")
            if stop is None:
                continue
            entry = (
                stop["inner_width_over_old_width"],
                phase["phase"],
                product["product"],
                stop["maximum_positive_residual_vertex"],
            )
            (stopped if stop["decision"] else continued).append(entry)
    lower, lower_phase, lower_product, lower_vertex = max(stopped)
    upper, upper_phase, upper_product, upper_vertex = min(continued)
    assert (lower_phase, lower_product, lower_vertex) == (23, 1, 7)
    assert (upper_phase, upper_product, upper_vertex) == (24, 3, 26)
    assert F(48688, 100000) < lower < F(48689, 100000)
    assert F(48767, 100000) < upper < F(48768, 100000)
    assert lower <= BETA_04877_FOUR_LEAF_STOP_BETA < upper
    assert result["same_chronology_stop_beta_interval"] == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }

    phase_clock = [
        {
            "product": product["product"],
            "ratio": product["stop"]["inner_width_over_old_width"],
            "maximum_vertex": product["stop"][
                "maximum_positive_residual_vertex"
            ],
        }
        for product in result["phases"][-1]["products"]
        if product.get("stop") is not None
    ]
    assert [entry["maximum_vertex"] for entry in phase_clock] == [
        26,
        26,
        26,
        25,
        25,
        25,
        25,
    ]
    assert phase_clock[2]["ratio"] == upper
    assert phase_clock[6]["ratio"] > upper

    alpha = BETA_04877_FOUR_LEAF_ROOT**2 / (2 - BETA_04877_FOUR_LEAF_ROOT**2)
    rho = BETA_04877_FOUR_LEAF_RHO_SCALE / len(neighbors[source])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_04877_FOUR_LEAF_VERTICES,
                    "edges": BETA_04877_FOUR_LEAF_EDGES,
                    "source": source,
                    "root": BETA_04877_FOUR_LEAF_ROOT,
                    "alpha": alpha,
                    "rho_scale": BETA_04877_FOUR_LEAF_RHO_SCALE,
                    "rho": rho,
                    "relative_width": BETA_04877_FOUR_LEAF_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_04877_FOUR_LEAF_STOP_BETA,
                    "same_chronology_stop_beta_interval": result[
                        "same_chronology_stop_beta_interval"
                    ],
                    "chronology_cell_attainment": {
                        "lower_attained_at": [
                            lower_phase,
                            lower_product,
                            lower_vertex,
                        ],
                        "upper_attained_at": [
                            upper_phase,
                            upper_product,
                            upper_vertex,
                        ],
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
                    "failure_phase_clock": phase_clock,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
