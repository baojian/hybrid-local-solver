#!/usr/bin/env python3
"""Exact two-leaf stopped-input-cone counterexample at beta=.487."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)
from stopped_masked_input_residual_beta_04864_clock_rewire_exact import (
    BETA_04864_CLOCK_REWIRE_EDGES,
    BETA_04864_CLOCK_REWIRE_RELATIVE_WIDTH,
)

BETA_048659_TWO_LEAF_VERTICES = 29
BETA_048659_TWO_LEAF_EDGES = tuple(
    sorted(
        (set(BETA_04864_CLOCK_REWIRE_EDGES) - {(1, 11)})
        | {(1, 4), (4, 27), (15, 28)}
    )
)
BETA_048659_TWO_LEAF_ROOT = F(1, 65536)
BETA_048659_TWO_LEAF_RHO_SCALE = F(367530301, 25000000000)
BETA_048659_TWO_LEAF_RELATIVE_WIDTH = BETA_04864_CLOCK_REWIRE_RELATIVE_WIDTH
BETA_048659_TWO_LEAF_STOP_BETA = F(487, 1000)


def main() -> None:
    """Replay the full exact chronology and reconstruct its beta cell."""
    neighbors, source = build_graph(
        {
            "vertices": BETA_048659_TWO_LEAF_VERTICES,
            "edges": list(BETA_048659_TWO_LEAF_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_048659_TWO_LEAF_EDGES) == 66
    assert len(BETA_048659_TWO_LEAF_EDGES) == len(set(BETA_048659_TWO_LEAF_EDGES))
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=BETA_048659_TWO_LEAF_ROOT,
        rho_scale=BETA_048659_TWO_LEAF_RHO_SCALE,
        relative_width=BETA_048659_TWO_LEAF_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=BETA_048659_TWO_LEAF_STOP_BETA,
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
    assert witness["face"] == list(range(20)) + list(range(22, 29))
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
    assert (upper_phase, upper_product, upper_vertex) == (24, 7, 25)
    assert F(48618, 100000) < lower < F(48620, 100000)
    assert F(48702, 100000) < upper < F(48703, 100000)
    assert lower <= BETA_048659_TWO_LEAF_STOP_BETA < upper
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
            "maximum_vertex": product["stop"]["maximum_positive_residual_vertex"],
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
    assert phase_clock[6]["ratio"] == upper
    assert witness["preceding_inner_width_over_old_width"] == upper

    alpha = BETA_048659_TWO_LEAF_ROOT**2 / (2 - BETA_048659_TWO_LEAF_ROOT**2)
    rho = BETA_048659_TWO_LEAF_RHO_SCALE / len(neighbors[source])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_048659_TWO_LEAF_VERTICES,
                    "edges": BETA_048659_TWO_LEAF_EDGES,
                    "source": source,
                    "root": BETA_048659_TWO_LEAF_ROOT,
                    "alpha": alpha,
                    "rho_scale": BETA_048659_TWO_LEAF_RHO_SCALE,
                    "rho": rho,
                    "relative_width": BETA_048659_TWO_LEAF_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_048659_TWO_LEAF_STOP_BETA,
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
