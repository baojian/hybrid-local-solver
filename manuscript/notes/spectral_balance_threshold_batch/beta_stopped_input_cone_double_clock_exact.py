#!/usr/bin/env python3
"""Exact high-beta chronology cell for the n=27 double-clock graft."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox
from stopped_masked_input_residual_one_third_counterexample_exact import EDGES as BASE_EDGES


VERTICES = 27
EDGES = tuple(BASE_EDGES) + ((2, 24), (24, 25), (7, 26))
ROOT = F(1, 224)
RHO_SCALE = F(11, 500)
RELATIVE_WIDTH = F(1, 1000)
STOP_BETA = F(9, 20)


def main() -> None:
    neighbors, source = build_graph(
        {"vertices": VERTICES, "edges": list(EDGES), "source": 0},
        None,
    )
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=ROOT,
        rho_scale=RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["vertices"] == VERTICES
    assert result["edges"] == [list(edge) for edge in sorted(EDGES)]
    witness = result["first_negative_active_input_residual"]
    assert witness["phase"] == 19
    assert witness["product"] == 8
    assert witness["vertex"] == 16
    assert witness["input_batch"] == []
    assert witness["value"] < 0

    stopped = []
    continued = []
    for phase in result["phases"]:
        for product in phase["products"]:
            if not product["executed"]:
                continue
            record = (
                product["stop"]["inner_width_over_old_width"],
                phase["phase"],
                product["product"],
            )
            (stopped if product["stop"]["decision"] else continued).append(record)
    lower, lower_phase, lower_product = max(stopped)
    upper, upper_phase, upper_product = min(continued)
    assert (lower_phase, lower_product) == (18, 1)
    assert (upper_phase, upper_product) == (19, 3)
    assert lower <= STOP_BETA < upper
    assert F(447, 1000) < lower < F(448, 1000)
    assert F(458, 1000) < upper < F(459, 1000)
    reported_cell = result["same_chronology_stop_beta_interval"]
    assert reported_cell == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }

    failure_ratio = witness["value"] / witness["phase_old_width"]
    predecessor_ratio = witness["preceding_inner_width_over_old_width"]
    assert predecessor_ratio is not None
    assert predecessor_ratio > STOP_BETA
    failure_phase = result["phases"][-1]
    phase_clock = [
        {
            "product": product["product"],
            "ratio": product["stop"]["inner_width_over_old_width"],
            "maximum_vertex": product["stop"]["maximum_positive_residual_vertex"],
        }
        for product in failure_phase["products"]
        if product["executed"]
    ]
    assert [entry["maximum_vertex"] for entry in phase_clock] == [9, 26, 26, 25, 25, 25, 25]

    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": (
                        "canonical zero-start one-push-maximal chronology; exact "
                        "high-beta cell for a double-clock graft"
                    ),
                    "vertices": VERTICES,
                    "edges": EDGES,
                    "source": source,
                    "root": ROOT,
                    "alpha": ROOT * ROOT / (2 - ROOT * ROOT),
                    "rho_scale": RHO_SCALE,
                    "rho": RHO_SCALE / len(neighbors[source]),
                    "relative_width": RELATIVE_WIDTH,
                    "verified_stop_beta": STOP_BETA,
                    "failure_phase_one_based": witness["phase"],
                    "failure_product_one_based": witness["product"],
                    "failure_vertex": witness["vertex"],
                    "active_input_residual_over_phase_width": failure_ratio,
                    "predecessor_width_over_phase_width": predecessor_ratio,
                    "same_chronology_stop_beta_interval": reported_cell,
                    "cell_endpoint_attainment": {
                        "lower": [lower_phase, lower_product],
                        "upper": [upper_phase, upper_product],
                    },
                    "failure_phase_clock": phase_clock,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
