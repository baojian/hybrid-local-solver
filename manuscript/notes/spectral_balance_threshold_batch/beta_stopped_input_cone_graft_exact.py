#!/usr/bin/env python3
"""Exact beta-stop chronology cell for the two-leaf n=26 graft."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox
from stopped_masked_input_residual_one_third_counterexample_exact import EDGES as BASE_EDGES


VERTICES = 26
EDGES = tuple(BASE_EDGES) + ((2, 24), (2, 25))
ROOT = F(1, 224)
RHO_SCALE = F(173, 8000)
RELATIVE_WIDTH = F(1, 1000)
STOP_BETA = F(21, 50)


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
    witness = result["first_negative_active_input_residual"]
    assert witness["phase"] == 16
    assert witness["product"] == 7
    assert witness["vertex"] == 16
    assert witness["value"] < 0

    stopped_lower = (F(0), None)
    continued_upper = (F(1), None)
    for phase in result["phases"]:
        for product in phase["products"]:
            if not product["executed"]:
                continue
            ratio = product["stop"]["inner_width_over_old_width"]
            location = (phase["phase"], product["product"])
            if product["stop"]["decision"] and ratio > stopped_lower[0]:
                stopped_lower = (ratio, location)
            if not product["stop"]["decision"] and ratio < continued_upper[0]:
                continued_upper = (ratio, location)

    lower, lower_location = stopped_lower
    upper, upper_location = continued_upper
    assert lower_location == (15, 1)
    assert upper_location == (16, 6)
    assert lower <= STOP_BETA < upper
    assert F(416, 1000) < lower < F(417, 1000)
    assert F(432, 1000) < upper < F(433, 1000)

    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": (
                        "canonical zero-start one-push-maximal chronology; exact "
                        "beta cell for the n=26 two-leaf clock graft"
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
                    "active_input_residual": witness["value"],
                    "active_input_residual_over_phase_width": (
                        witness["value"] / witness["phase_old_width"]
                    ),
                    "same_chronology_beta_cell": {
                        "interval": "[lower, upper)",
                        "lower": lower,
                        "lower_attained_at_phase_product": lower_location,
                        "upper": upper,
                        "upper_attained_at_phase_product": upper_location,
                    },
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
