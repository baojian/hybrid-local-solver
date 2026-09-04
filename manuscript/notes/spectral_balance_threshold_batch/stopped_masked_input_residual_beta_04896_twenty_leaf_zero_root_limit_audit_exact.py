#!/usr/bin/env python3
"""Exact full comparison audit for the twenty-leaf beta-0.48935 limit."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
)
from stopped_masked_input_residual_beta_04894_eighteen_leaf_zero_root_limit_audit_exact import (
    BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_EDGES,
    BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
)


BETA_04896_TWENTY_LEAF_ZERO_ROOT_VERTICES = 47
BETA_04896_TWENTY_LEAF_ZERO_ROOT_EDGES = tuple(
    sorted(set(BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_EDGES) | {(2, 45), (18, 46)})
)
BETA_04896_TWENTY_LEAF_ZERO_ROOT_RHO_SCALE = F(11781, 1000000)
BETA_04896_TWENTY_LEAF_ZERO_ROOT_RELATIVE_WIDTH = (
    BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04896_TWENTY_LEAF_ZERO_ROOT_STOP_BETA = F(9787, 20000)

EXPECTED_POST_CLOSURE_ZEROS = {
    (1, 1): (2, 30, 33, 37),
    (2, 1): (4, 18),
    (4, 1): (8, 14, 29, 39, 44, 45),
    (5, 1): (5, 15, 27, 31, 35, 36, 43, 46),
    (6, 1): (7,),
    (8, 1): (24, 28),
    (10, 1): (10,),
    (13, 1): (41,),
    (15, 1): (26,),
    (20, 1): (25,),
}
EXPECTED_MAXIMUM_TIES = (
    (21, 1, (33, 37)),
    (22, 1, (33, 37)),
    (23, 1, (33, 37)),
    (24, 1, (27, 31, 35, 43)),
    (25, 1, (27, 31, 35, 43)),
    (26, 1, (27, 31, 35, 43)),
)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04896_TWENTY_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04896_TWENTY_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04896_TWENTY_LEAF_ZERO_ROOT_EDGES)
        == len(set(BETA_04896_TWENTY_LEAF_ZERO_ROOT_EDGES))
        == 84
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04896_TWENTY_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04896_TWENTY_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04896_TWENTY_LEAF_ZERO_ROOT_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 32
    lower, upper = result["cell"]
    assert F(48907, 100000) < lower < F(48909, 100000)
    assert F(48951, 100000) < upper < F(48952, 100000)
    assert lower < BETA_04896_TWENTY_LEAF_ZERO_ROOT_STOP_BETA < upper
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (
        26,
        8,
        28,
    )
    assert failure["input_batch"] == []
    assert failure["face"] == list(range(19)) + [
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
        43,
        44,
        45,
        46,
    ]
    phase_width = result["phases"][-1]["old_width"]
    normalized_failure = failure["scaled_input_residual"] / phase_width
    assert normalized_failure < -F(1, 100000)

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
    assert max(stopped) == (lower, 25, 1, 27)
    assert min(continued) == (upper, 26, 3, 26)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_3 == upper < ratio_7
    assert ratio_7 - ratio_3 > F(1, 10000)

    audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=BETA_04896_TWENTY_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04896_TWENTY_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04896_TWENTY_LEAF_ZERO_ROOT_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] == 40
    assert audit["forced_coordinate_count_per_kind"] == 27
    assert len(audit["structural_maximum_tie_certificates"]) == 6

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04896_TWENTY_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04896_TWENTY_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "rho_scale": BETA_04896_TWENTY_LEAF_ZERO_ROOT_RHO_SCALE,
                    "relative_width": (
                        BETA_04896_TWENTY_LEAF_ZERO_ROOT_RELATIVE_WIDTH
                    ),
                    "chosen_stop_beta": BETA_04896_TWENTY_LEAF_ZERO_ROOT_STOP_BETA,
                    "same_chronology_stop_beta_interval": {
                        "lower": lower,
                        "lower_inclusive": True,
                        "upper": upper,
                        "upper_inclusive": False,
                    },
                    "chronology_cell_attainment": {
                        "lower_attained_at": [25, 1, 27],
                        "upper_attained_at": [26, 3, 26],
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
