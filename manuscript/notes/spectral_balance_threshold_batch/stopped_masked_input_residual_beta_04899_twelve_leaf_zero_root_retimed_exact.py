#!/usr/bin/env python3
"""Exact audited zero-root rho retiming on the twelve-leaf graph."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
    expected_complete_equality_events,
)
from stopped_masked_input_residual_beta_04890_twelve_leaf_zero_root_limit_audit_exact import (
    BETA_04890_TWELVE_LEAF_ZERO_ROOT_EDGES,
    BETA_04890_TWELVE_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
    BETA_04890_TWELVE_LEAF_ZERO_ROOT_VERTICES,
    EXPECTED_MAXIMUM_TIES,
    EXPECTED_POST_CLOSURE_ZEROS,
)


BETA_04899_TWELVE_LEAF_ZERO_ROOT_RETIMED_RHO_SCALE = F(26191, 2000000)
BETA_04899_TWELVE_LEAF_ZERO_ROOT_RETIMED_STOP_BETA = F(4889, 10000)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04890_TWELVE_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04890_TWELVE_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04899_TWELVE_LEAF_ZERO_ROOT_RETIMED_RHO_SCALE,
        relative_width=BETA_04890_TWELVE_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04899_TWELVE_LEAF_ZERO_ROOT_RETIMED_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 33
    lower, upper = result["cell"]
    assert F(488769, 1000000) < lower < F(488770, 1000000)
    assert F(488986, 1000000) < upper < F(488987, 1000000)
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (27, 8, 28)
    assert failure["input_batch"] == []
    normalized_failure = failure["scaled_input_residual"] / result["phases"][-1][
        "old_width"
    ]
    assert normalized_failure < -F(2, 1000)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_3 == upper < ratio_7
    assert result["equality_events"] == expected_complete_equality_events(
        EXPECTED_POST_CLOSURE_ZEROS,
        EXPECTED_MAXIMUM_TIES,
    )

    audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=BETA_04899_TWELVE_LEAF_ZERO_ROOT_RETIMED_RHO_SCALE,
        relative_width=BETA_04890_TWELVE_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04899_TWELVE_LEAF_ZERO_ROOT_RETIMED_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] == 44
    assert audit["forced_coordinate_count_per_kind"] == 22
    assert len(audit["structural_maximum_tie_certificates"]) == 6

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04890_TWELVE_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04890_TWELVE_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "rho_scale": (
                        BETA_04899_TWELVE_LEAF_ZERO_ROOT_RETIMED_RHO_SCALE
                    ),
                    "relative_width": (
                        BETA_04890_TWELVE_LEAF_ZERO_ROOT_RELATIVE_WIDTH
                    ),
                    "chosen_stop_beta": (
                        BETA_04899_TWELVE_LEAF_ZERO_ROOT_RETIMED_STOP_BETA
                    ),
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
