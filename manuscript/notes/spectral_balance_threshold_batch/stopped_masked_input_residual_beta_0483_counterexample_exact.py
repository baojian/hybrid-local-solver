#!/usr/bin/env python3
"""Exact beta=.483 stopped-input-cone counterexample."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox
from stopped_masked_input_residual_beta_0482_retimed_exact import (
    BETA_0482_RETIMED_EDGES,
    BETA_0482_RETIMED_RELATIVE_WIDTH,
    BETA_0482_RETIMED_ROOT,
    BETA_0482_RETIMED_VERTICES,
)


BETA_0483_VERTICES = BETA_0482_RETIMED_VERTICES
BETA_0483_EDGES = tuple(sorted(set(BETA_0482_RETIMED_EDGES) | {(8, 11)}))
BETA_0483_ROOT = BETA_0482_RETIMED_ROOT
BETA_0483_RHO_SCALE = F(633, 40000)
BETA_0483_RELATIVE_WIDTH = BETA_0482_RETIMED_RELATIVE_WIDTH
BETA_0483_STOP_BETA = F(483, 1000)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_0483_VERTICES,
            "edges": list(BETA_0483_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_0483_EDGES) == len(set(BETA_0483_EDGES)) == 63
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=BETA_0483_ROOT,
        rho_scale=BETA_0483_RHO_SCALE,
        relative_width=BETA_0483_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=BETA_0483_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 29
    witness = result["first_negative_active_input_residual"]
    assert (witness["phase"], witness["product"], witness["vertex"]) == (23, 8, 15)
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(19)) + [24, 25, 26]
    assert witness["value"] < 0

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
    assert (upper_phase, upper_product) == (23, 3)
    assert F(4786, 10000) < lower < F(4787, 10000)
    assert F(4830, 10000) < upper < F(4831, 10000)
    assert lower <= BETA_0483_STOP_BETA < upper
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
    assert phase_clock[2]["ratio"] == upper
    assert phase_clock[6]["ratio"] > upper

    alpha = BETA_0483_ROOT**2 / (2 - BETA_0483_ROOT**2)
    rho = BETA_0483_RHO_SCALE / len(neighbors[source])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_0483_VERTICES,
                    "edges": BETA_0483_EDGES,
                    "source": source,
                    "root": BETA_0483_ROOT,
                    "alpha": alpha,
                    "rho_scale": BETA_0483_RHO_SCALE,
                    "rho": rho,
                    "relative_width": BETA_0483_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_0483_STOP_BETA,
                    "same_chronology_stop_beta_interval": result[
                        "same_chronology_stop_beta_interval"
                    ],
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
                    "failure_phase_clock": phase_clock,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
