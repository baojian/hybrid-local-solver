#!/usr/bin/env python3
"""Exact beta=.48 stopped-input-cone counterexample on a unit graph."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)
from stopped_masked_input_residual_high_beta_counterexample_exact import (
    RELATIVE_WIDTH,
    ROOT,
)


BETA_048_VERTICES = 27
BETA_048_EDGES = (
    (0, 1),
    (0, 12),
    (1, 2),
    (1, 3),
    (1, 6),
    (1, 11),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 8),
    (2, 10),
    (2, 11),
    (2, 24),
    (3, 4),
    (3, 5),
    (3, 8),
    (4, 5),
    (4, 6),
    (4, 8),
    (4, 11),
    (5, 6),
    (5, 7),
    (5, 9),
    (5, 11),
    (6, 7),
    (6, 8),
    (7, 8),
    (7, 10),
    (7, 26),
    (8, 9),
    (8, 10),
    (9, 10),
    (9, 11),
    (10, 11),
    (12, 13),
    (13, 14),
    (13, 16),
    (13, 17),
    (13, 18),
    (14, 15),
    (14, 16),
    (14, 17),
    (15, 16),
    (15, 17),
    (15, 20),
    (16, 17),
    (17, 18),
    (18, 19),
    (18, 21),
    (18, 22),
    (18, 23),
    (19, 20),
    (19, 21),
    (20, 21),
    (20, 23),
    (21, 22),
    (21, 23),
    (22, 23),
    (24, 25),
)
BETA_048_ROOT = ROOT
BETA_048_RHO_SCALE = F(171, 10000)
BETA_048_RELATIVE_WIDTH = RELATIVE_WIDTH
BETA_048_STOP_BETA = F(12, 25)


def main() -> None:
    """Replay the full chronology and independently reconstruct its beta cell."""
    neighbors, source = build_graph(
        {
            "vertices": BETA_048_VERTICES,
            "edges": list(BETA_048_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_048_EDGES) == len(set(BETA_048_EDGES)) == 59
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=BETA_048_ROOT,
        rho_scale=BETA_048_RHO_SCALE,
        relative_width=BETA_048_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=BETA_048_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 28
    witness = result["first_negative_active_input_residual"]
    assert (witness["phase"], witness["product"], witness["vertex"]) == (22, 8, 15)
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(19)) + [24, 25, 26]
    assert witness["value"] < 0
    assert witness["preceding_inner_width_over_old_width"] > BETA_048_STOP_BETA

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
    assert (lower_phase, lower_product) == (21, 1)
    assert (upper_phase, upper_product) == (22, 7)
    assert F(4769, 10000) < lower < F(477, 1000)
    assert F(4812, 10000) < upper < F(4813, 10000)
    assert lower <= BETA_048_STOP_BETA < upper
    reported_cell = result["same_chronology_stop_beta_interval"]
    assert reported_cell == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }

    failure_phase = result["phases"][-1]
    phase_clock = [
        {
            "product": product["product"],
            "ratio": product["stop"]["inner_width_over_old_width"],
            "maximum_vertex": product["stop"]["maximum_positive_residual_vertex"],
        }
        for product in failure_phase["products"]
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
    assert phase_clock[-1]["ratio"] == upper

    alpha = BETA_048_ROOT * BETA_048_ROOT / (2 - BETA_048_ROOT * BETA_048_ROOT)
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": (
                        "canonical zero-start one-push-maximal chronology; "
                        "exact beta=.48 cell on a simple connected unit graph"
                    ),
                    "vertices": BETA_048_VERTICES,
                    "edges": BETA_048_EDGES,
                    "source": source,
                    "root": BETA_048_ROOT,
                    "alpha": alpha,
                    "rho_scale": BETA_048_RHO_SCALE,
                    "rho": BETA_048_RHO_SCALE / len(neighbors[source]),
                    "relative_width": BETA_048_RELATIVE_WIDTH,
                    "verified_stop_beta": BETA_048_STOP_BETA,
                    "failure_phase_one_based": witness["phase"],
                    "failure_product_one_based": witness["product"],
                    "failure_vertex": witness["vertex"],
                    "failure_face": witness["face"],
                    "active_input_residual_over_phase_width": (
                        witness["value"] / witness["phase_old_width"]
                    ),
                    "predecessor_width_over_phase_width": witness[
                        "preceding_inner_width_over_old_width"
                    ],
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
