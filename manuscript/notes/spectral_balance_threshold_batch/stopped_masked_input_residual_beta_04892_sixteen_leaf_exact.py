#!/usr/bin/env python3
"""Exact finite-root sixteen-leaf counterexample at beta=.48905."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)
from stopped_masked_input_residual_beta_04892_sixteen_leaf_zero_root_limit_audit_exact import (
    BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES,
    BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
    BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RHO_SCALE,
    BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_STOP_BETA,
    BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_VERTICES,
)


BETA_04892_SIXTEEN_LEAF_VERTICES = BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_VERTICES
BETA_04892_SIXTEEN_LEAF_EDGES = BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES
BETA_04892_SIXTEEN_LEAF_ROOT = F(1, 4096)
BETA_04892_SIXTEEN_LEAF_RHO_SCALE = BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RHO_SCALE
BETA_04892_SIXTEEN_LEAF_RELATIVE_WIDTH = (
    BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04892_SIXTEEN_LEAF_STOP_BETA = BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_STOP_BETA


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04892_SIXTEEN_LEAF_VERTICES,
            "edges": list(BETA_04892_SIXTEEN_LEAF_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04892_SIXTEEN_LEAF_EDGES)
        == len(set(BETA_04892_SIXTEEN_LEAF_EDGES))
        == 80
    )
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=BETA_04892_SIXTEEN_LEAF_ROOT,
        rho_scale=BETA_04892_SIXTEEN_LEAF_RHO_SCALE,
        relative_width=BETA_04892_SIXTEEN_LEAF_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=BETA_04892_SIXTEEN_LEAF_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 33
    witness = result["first_negative_active_input_residual"]
    assert (witness["phase"], witness["product"], witness["vertex"]) == (
        27,
        8,
        28,
    )
    assert witness["input_batch"] == []
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
    assert (lower_phase, lower_product, lower_vertex) == (26, 1, 27)
    assert (upper_phase, upper_product, upper_vertex) == (27, 3, 26)
    assert F(48897, 100000) < lower < F(48898, 100000)
    assert F(48913, 100000) < upper < F(48914, 100000)
    assert lower < BETA_04892_SIXTEEN_LEAF_STOP_BETA < upper
    assert result["same_chronology_stop_beta_interval"] == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }

    alpha = BETA_04892_SIXTEEN_LEAF_ROOT**2 / (
        2 - BETA_04892_SIXTEEN_LEAF_ROOT**2
    )
    rho = BETA_04892_SIXTEEN_LEAF_RHO_SCALE / len(neighbors[source])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_04892_SIXTEEN_LEAF_VERTICES,
                    "edges": BETA_04892_SIXTEEN_LEAF_EDGES,
                    "source": source,
                    "root": BETA_04892_SIXTEEN_LEAF_ROOT,
                    "alpha": alpha,
                    "rho_scale": BETA_04892_SIXTEEN_LEAF_RHO_SCALE,
                    "rho": rho,
                    "relative_width": BETA_04892_SIXTEEN_LEAF_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_04892_SIXTEEN_LEAF_STOP_BETA,
                    "same_chronology_stop_beta_interval": result[
                        "same_chronology_stop_beta_interval"
                    ],
                    "chronology_cell_attainment": {
                        "lower_attained_at": [lower_phase, lower_product, lower_vertex],
                        "upper_attained_at": [upper_phase, upper_product, upper_vertex],
                    },
                    "completed_products_before_failure": result["total_products"],
                    "failure_phase_one_based": witness["phase"],
                    "failure_product_in_phase_one_based": witness["product"],
                    "failure_vertex": witness["vertex"],
                    "input_batch_at_failure": witness["input_batch"],
                    "failure_face": witness["face"],
                    "degree_residual_over_phase_width": witness["value"]
                    / witness["phase_old_width"],
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
