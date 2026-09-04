#!/usr/bin/env python3
"""Exact beta-0.4865 clock-boundary rewire counterexample."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox
from stopped_masked_input_residual_beta_0486_relay_exact import (
    BETA_0486_RELAY_EDGES,
    BETA_0486_RELAY_RELATIVE_WIDTH,
    BETA_0486_RELAY_VERTICES,
)


BETA_04857_CLOCK_BOUNDARY_VERTICES = BETA_0486_RELAY_VERTICES
BETA_04857_CLOCK_BOUNDARY_EDGES = tuple(
    sorted(
        (
            set(BETA_0486_RELAY_EDGES)
            - {(5, 8), (4, 8), (1, 11), (10, 11)}
        )
        | {(4, 10), (3, 5), (1, 4), (5, 26)}
    )
)
BETA_04857_CLOCK_BOUNDARY_ROOT = F(1, 4096)
BETA_04857_CLOCK_BOUNDARY_RHO_SCALE = F(75706471, 5000000000)
BETA_04857_CLOCK_BOUNDARY_RELATIVE_WIDTH = BETA_0486_RELAY_RELATIVE_WIDTH
BETA_04857_CLOCK_BOUNDARY_STOP_BETA = F(973, 2000)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04857_CLOCK_BOUNDARY_VERTICES,
            "edges": list(BETA_04857_CLOCK_BOUNDARY_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04857_CLOCK_BOUNDARY_EDGES)
        == len(set(BETA_04857_CLOCK_BOUNDARY_EDGES))
        == 64
    )
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=BETA_04857_CLOCK_BOUNDARY_ROOT,
        rho_scale=BETA_04857_CLOCK_BOUNDARY_RHO_SCALE,
        relative_width=BETA_04857_CLOCK_BOUNDARY_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=BETA_04857_CLOCK_BOUNDARY_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 31
    witness = result["first_negative_active_input_residual"]
    assert (witness["phase"], witness["product"], witness["vertex"]) == (25, 8, 14)
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(20)) + [22, 23, 24, 25, 26]
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
    assert (lower_phase, lower_product, lower_vertex) == (24, 1, 7)
    assert (upper_phase, upper_product, upper_vertex) == (25, 3, 26)
    assert F(48640, 100000) < lower < F(48641, 100000)
    assert F(48658, 100000) < upper < F(48659, 100000)
    assert lower <= BETA_04857_CLOCK_BOUNDARY_STOP_BETA < upper
    assert result["same_chronology_stop_beta_interval"] == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }

    failure_phase_clock = [
        {
            "product": product["product"],
            "ratio": product["stop"]["inner_width_over_old_width"],
            "maximum_vertex": product["stop"]["maximum_positive_residual_vertex"],
        }
        for product in result["phases"][-1]["products"]
        if product.get("stop") is not None
    ]
    assert [entry["maximum_vertex"] for entry in failure_phase_clock] == [
        26,
        26,
        26,
        25,
        25,
        25,
        25,
    ]
    assert failure_phase_clock[2]["ratio"] == upper
    equioscillation_gap = (
        failure_phase_clock[6]["ratio"] - failure_phase_clock[2]["ratio"]
    )
    assert 0 < equioscillation_gap < F(1, 100000000)

    alpha = BETA_04857_CLOCK_BOUNDARY_ROOT**2 / (
        2 - BETA_04857_CLOCK_BOUNDARY_ROOT**2
    )
    rho = BETA_04857_CLOCK_BOUNDARY_RHO_SCALE / len(neighbors[source])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_04857_CLOCK_BOUNDARY_VERTICES,
                    "edges": BETA_04857_CLOCK_BOUNDARY_EDGES,
                    "source": source,
                    "root": BETA_04857_CLOCK_BOUNDARY_ROOT,
                    "alpha": alpha,
                    "rho_scale": BETA_04857_CLOCK_BOUNDARY_RHO_SCALE,
                    "rho": rho,
                    "relative_width": BETA_04857_CLOCK_BOUNDARY_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_04857_CLOCK_BOUNDARY_STOP_BETA,
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
                    "failure_phase_clock": failure_phase_clock,
                    "product_7_minus_product_3_ratio": equioscillation_gap,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
