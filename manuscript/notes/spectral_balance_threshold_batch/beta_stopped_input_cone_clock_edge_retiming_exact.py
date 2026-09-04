#!/usr/bin/env python3
"""Exact beta=0.475 witness from one clock-branch edge retiming."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)
from stopped_masked_input_residual_high_beta_counterexample_exact import (
    BETA_0473_EDGES,
    RELATIVE_WIDTH,
    ROOT,
)


VERTICES = 27
DELETED_EDGE = (7, 8)
ADDED_EDGE = (5, 8)
EDGES = tuple(sorted((set(BETA_0473_EDGES) - {DELETED_EDGE}) | {ADDED_EDGE}))
RHO_SCALE = F(979, 50000)
STOP_BETA = F(19, 40)


def main() -> None:
    neighbors, source = build_graph(
        {"vertices": VERTICES, "edges": list(EDGES), "source": 0},
        None,
    )
    assert DELETED_EDGE not in EDGES
    assert ADDED_EDGE in EDGES
    assert len(EDGES) == len(BETA_0473_EDGES)

    result = trace_retained_prox(
        neighbors,
        source=source,
        root=ROOT,
        rho_scale=RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=60,
        chronology="one-push-maximal",
        stop_beta=STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 27
    witness = result["first_negative_active_input_residual"]
    assert (witness["phase"], witness["product"], witness["vertex"]) == (21, 8, 15)
    assert witness["input_batch"] == []
    assert witness["value"] < 0
    predecessor_ratio = witness["preceding_inner_width_over_old_width"]
    assert predecessor_ratio is not None
    assert predecessor_ratio > STOP_BETA

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
    assert (lower_phase, lower_product) == (20, 1)
    assert (upper_phase, upper_product) == (21, 3)
    assert lower <= STOP_BETA < upper
    assert F(4722, 10000) < lower < F(4723, 10000)
    assert F(4763, 10000) < upper < F(4764, 10000)
    reported_cell = result["same_chronology_stop_beta_interval"]
    assert reported_cell == {
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
        if product["executed"]
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

    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": (
                        "canonical zero-start one-push-maximal chronology; "
                        "exact clock-branch edge retiming"
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
                    "active_input_residual_over_phase_width": (
                        witness["value"] / witness["phase_old_width"]
                    ),
                    "predecessor_width_over_phase_width": predecessor_ratio,
                    "same_chronology_stop_beta_interval": reported_cell,
                    "cell_endpoint_attainment": {
                        "lower": [lower_phase, lower_product],
                        "upper": [upper_phase, upper_product],
                    },
                    "failure_phase_clock": phase_clock,
                    "retiming": {
                        "deleted_edge": DELETED_EDGE,
                        "added_edge": ADDED_EDGE,
                    },
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
