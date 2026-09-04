#!/usr/bin/env python3
"""Exact full comparison audit for the sixteen-leaf beta-0.48905 limit."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
)
from stopped_masked_input_residual_beta_04891_fourteen_leaf_zero_root_relay_exact import (
    BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_EDGES,
    BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
)


BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_VERTICES = 43
BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES = tuple(
    sorted(set(BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_EDGES) | {(5, 41), (22, 42)})
)
BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RHO_SCALE = F(6243, 500000)
BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH = (
    BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_STOP_BETA = F(9781, 20000)

EXPECTED_POST_CLOSURE_ZEROS = {
    (1, 1): (2, 18, 30, 33, 37),
    (2, 1): (4,),
    (4, 1): (8, 14, 27, 29, 31, 35, 39),
    (5, 1): (15, 36),
    (7, 1): (11, 24),
    (8, 1): (9, 28),
    (11, 1): (10,),
    (14, 1): (41,),
    (16, 1): (26,),
    (22, 1): (25,),
}
EXPECTED_MAXIMUM_TIES = (
    (22, 1, (33, 37)),
    (23, 1, (33, 37)),
    (24, 1, (27, 31, 35)),
    (25, 1, (27, 31, 35)),
    (26, 1, (27, 31, 35)),
)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES)
        == len(set(BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES))
        == 80
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 33
    lower, upper = result["cell"]
    assert F(48897, 100000) < lower < F(48898, 100000)
    assert F(48913, 100000) < upper < F(48914, 100000)
    assert lower < BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_STOP_BETA < upper
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (
        27,
        8,
        28,
    )
    assert failure["input_batch"] == []
    assert failure["face"] == list(range(20)) + [
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        33,
        35,
        36,
        37,
        39,
        41,
    ]
    phase_width = result["phases"][-1]["old_width"]
    normalized_failure = failure["scaled_input_residual"] / phase_width
    assert normalized_failure < -F(1, 1000)

    stopped: list[tuple[F, int, int, int]] = []
    continued: list[tuple[F, int, int, int]] = []
    for phase in result["phases"]:
        for product in phase["products"]:
            if not product.get("executed"):
                continue
            entry = (
                product["inner_width_over_old_width"],
                phase["phase"],
                product["product"],
                product["maximum_vertex"],
            )
            (stopped if product["stop"] else continued).append(entry)
    assert max(stopped) == (lower, 26, 1, 27)
    assert min(continued) == (upper, 27, 3, 26)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_3 == upper < ratio_7
    assert ratio_7 - ratio_3 > F(1, 10000)

    audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] == 40
    assert audit["forced_coordinate_count_per_kind"] == 23
    assert len(audit["structural_maximum_tie_certificates"]) == 5

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "rho_scale": BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RHO_SCALE,
                    "relative_width": (
                        BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH
                    ),
                    "chosen_stop_beta": BETA_04892_SIXTEEN_LEAF_ZERO_ROOT_STOP_BETA,
                    "same_chronology_stop_beta_interval": {
                        "lower": lower,
                        "lower_inclusive": True,
                        "upper": upper,
                        "upper_inclusive": False,
                    },
                    "chronology_cell_attainment": {
                        "lower_attained_at": [26, 1, 27],
                        "upper_attained_at": [27, 3, 26],
                    },
                    "failure_residual_over_phase_width": normalized_failure,
                    "product_7_minus_product_3_ratio": ratio_7 - ratio_3,
                    "comparison_audit": audit,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
