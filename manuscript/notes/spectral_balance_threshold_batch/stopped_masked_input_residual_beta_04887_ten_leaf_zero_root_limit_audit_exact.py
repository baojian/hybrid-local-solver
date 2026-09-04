#!/usr/bin/env python3
"""Exact full comparison audit for the ten-leaf beta-0.48866 limit."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
    expected_equality_events,
)
from stopped_masked_input_residual_beta_04885_eight_leaf_zero_root_limit_audit_exact import (
    BETA_04885_EIGHT_LEAF_ZERO_ROOT_EDGES,
    BETA_04885_EIGHT_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
)


BETA_04887_TEN_LEAF_ZERO_ROOT_VERTICES = 37
BETA_04887_TEN_LEAF_ZERO_ROOT_EDGES = tuple(
    sorted(set(BETA_04885_EIGHT_LEAF_ZERO_ROOT_EDGES) | {(4, 35), (18, 36)})
)
BETA_04887_TEN_LEAF_ZERO_ROOT_RHO_SCALE = F(133419, 10000000)
BETA_04887_TEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH = (
    BETA_04885_EIGHT_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04887_TEN_LEAF_ZERO_ROOT_STOP_BETA = F(977, 2000)

EXPECTED_POST_CLOSURE_ZEROS = {
    (1, 1): (4, 30, 33),
    (2, 1): (18,),
    (3, 1): (29,),
    (4, 1): (8, 14, 27, 31, 35),
    (5, 1): (5, 15, 36),
    (6, 1): (11, 24),
    (8, 1): (9,),
    (9, 1): (28,),
    (10, 1): (10,),
    (16, 1): (26,),
    (17, 1): (19, 22),
    (21, 1): (25,),
}
EXPECTED_MAXIMUM_TIES = tuple(
    (phase, 1, (27, 31, 35)) for phase in range(23, 27)
)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04887_TEN_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04887_TEN_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04887_TEN_LEAF_ZERO_ROOT_EDGES)
        == len(set(BETA_04887_TEN_LEAF_ZERO_ROOT_EDGES))
        == 74
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04887_TEN_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04887_TEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04887_TEN_LEAF_ZERO_ROOT_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 32
    lower, upper = result["cell"]
    assert F(48809, 100000) < lower < F(48810, 100000)
    assert F(48865, 100000) < upper < F(48866, 100000)
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (26, 8, 28)
    assert failure["input_batch"] == []
    assert failure["face"] == list(range(20)) + [
        22,
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
    ]
    phase_width = result["phases"][-1]["old_width"]
    normalized_failure = failure["scaled_input_residual"] / phase_width
    assert normalized_failure < -F(1, 1000)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_3 == upper
    assert 0 < ratio_7 - ratio_3 < F(1, 100000)
    expected_events = expected_equality_events(EXPECTED_POST_CLOSURE_ZEROS)
    expected_events.extend(
        {
            "kind": "maximum_residual",
            "phase": phase,
            "product": product,
            "vertices": list(vertices),
        }
        for phase, product, vertices in EXPECTED_MAXIMUM_TIES
    )
    assert result["equality_events"] == expected_events

    audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=BETA_04887_TEN_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04887_TEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04887_TEN_LEAF_ZERO_ROOT_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] + len(EXPECTED_MAXIMUM_TIES) == 52
    assert audit["forced_coordinate_count_per_kind"] == 22
    assert len(audit["structural_maximum_tie_certificates"]) == 4

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04887_TEN_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04887_TEN_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "rho_scale": BETA_04887_TEN_LEAF_ZERO_ROOT_RHO_SCALE,
                    "relative_width": BETA_04887_TEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_04887_TEN_LEAF_ZERO_ROOT_STOP_BETA,
                    "same_chronology_stop_beta_interval": {
                        "lower": lower,
                        "lower_inclusive": True,
                        "upper": upper,
                        "upper_inclusive": False,
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
