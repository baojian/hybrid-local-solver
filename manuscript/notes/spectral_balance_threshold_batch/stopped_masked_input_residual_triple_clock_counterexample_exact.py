#!/usr/bin/env python3
"""Exact high-beta input-cone counterexample with three clock grafts."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)


TRIPLE_CLOCK_VERTICES = 28
TRIPLE_CLOCK_EDGES = (
    (0, 1),
    (0, 12),
    (1, 2),
    (1, 6),
    (1, 11),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 8),
    (2, 10),
    (2, 11),
    (2, 24),
    (2, 27),
    (3, 4),
    (3, 5),
    (4, 5),
    (4, 6),
    (4, 8),
    (5, 6),
    (5, 9),
    (6, 7),
    (7, 8),
    (7, 26),
    (8, 9),
    (8, 10),
    (9, 10),
    (10, 11),
    (12, 13),
    (13, 14),
    (13, 17),
    (13, 18),
    (14, 15),
    (15, 16),
    (15, 17),
    (15, 20),
    (16, 17),
    (16, 20),
    (17, 18),
    (18, 19),
    (18, 20),
    (18, 22),
    (18, 23),
    (19, 20),
    (20, 21),
    (20, 23),
    (21, 22),
    (22, 23),
    (24, 25),
)
TRIPLE_CLOCK_ROOT = F(1, 224)
TRIPLE_CLOCK_RHO_SCALE = F(21, 1000)
TRIPLE_CLOCK_RELATIVE_WIDTH = F(1, 1000)
TRIPLE_CLOCK_STOP_BETA = F(23, 50)


def main() -> None:
    """Replay the canonical history and assert its exact half-open beta cell."""
    neighbors, source = build_graph(
        {
            "vertices": TRIPLE_CLOCK_VERTICES,
            "edges": list(TRIPLE_CLOCK_EDGES),
            "source": 0,
        },
        None,
    )
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=TRIPLE_CLOCK_ROOT,
        rho_scale=TRIPLE_CLOCK_RHO_SCALE,
        relative_width=TRIPLE_CLOCK_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=60,
        chronology="one-push-maximal",
        stop_beta=TRIPLE_CLOCK_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 25
    witness = result["first_negative_active_input_residual"]
    assert witness["phase"] == 19
    assert witness["product"] == 8
    assert witness["vertex"] == 16
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(19)) + [24, 25, 26, 27]
    assert witness["value"] < 0
    predecessor_ratio = witness["preceding_inner_width_over_old_width"]
    assert predecessor_ratio is not None
    assert predecessor_ratio > TRIPLE_CLOCK_STOP_BETA

    stopped: list[tuple[F, int, int]] = []
    continued: list[tuple[F, int, int]] = []
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
    assert F(458, 1000) < lower < F(459, 1000)
    assert F(462, 1000) < upper < F(463, 1000)
    assert lower <= TRIPLE_CLOCK_STOP_BETA < upper
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
                        "exact high-beta cell for three clock grafts"
                    ),
                    "vertices": TRIPLE_CLOCK_VERTICES,
                    "edges": TRIPLE_CLOCK_EDGES,
                    "source": source,
                    "root": TRIPLE_CLOCK_ROOT,
                    "alpha": (
                        TRIPLE_CLOCK_ROOT * TRIPLE_CLOCK_ROOT
                        / (2 - TRIPLE_CLOCK_ROOT * TRIPLE_CLOCK_ROOT)
                    ),
                    "rho_scale": TRIPLE_CLOCK_RHO_SCALE,
                    "rho": TRIPLE_CLOCK_RHO_SCALE / len(neighbors[source]),
                    "relative_width": TRIPLE_CLOCK_RELATIVE_WIDTH,
                    "verified_stop_beta": TRIPLE_CLOCK_STOP_BETA,
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
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
