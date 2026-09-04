#!/usr/bin/env python3
"""Exact full comparison audit for the six-leaf beta-0.4882 limit."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
    expected_equality_events,
)
from stopped_masked_input_residual_beta_04865_branch_boundary_exact import (
    BETA_04865_BRANCH_BOUNDARY_EDGES,
    BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH,
)


BETA_04882_SIX_LEAF_ZERO_ROOT_VERTICES = 33
BETA_04882_SIX_LEAF_ZERO_ROOT_EDGES = tuple(
    sorted(
        set(BETA_04865_BRANCH_BOUNDARY_EDGES)
        | {(2, 29), (4, 27), (4, 31), (13, 30), (15, 28), (21, 32)}
    )
)
BETA_04882_SIX_LEAF_ZERO_ROOT_RHO_SCALE = F(6943, 500000)
BETA_04882_SIX_LEAF_ZERO_ROOT_RELATIVE_WIDTH = (
    BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH
)
BETA_04882_SIX_LEAF_ZERO_ROOT_STOP_BETA = F(4881, 10000)

EXPECTED_POST_CLOSURE_ZEROS = {
    (1, 1): (18, 30),
    (3, 1): (29,),
    (4, 1): (5, 8, 14, 27, 31),
    (5, 1): (7, 15, 24),
    (6, 1): (11,),
    (7, 1): (9,),
    (9, 1): (10, 28),
    (14, 1): (19, 22, 23),
    (15, 1): (26,),
    (20, 1): (25,),
}
EXPECTED_MAXIMUM_TIES = tuple(
    (phase, 1, (27, 31)) for phase in range(21, 25)
)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04882_SIX_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04882_SIX_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04882_SIX_LEAF_ZERO_ROOT_EDGES)
        == len(set(BETA_04882_SIX_LEAF_ZERO_ROOT_EDGES))
        == 70
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04882_SIX_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04882_SIX_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04882_SIX_LEAF_ZERO_ROOT_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 31
    lower, upper = result["cell"]
    assert F(48729, 100000) < lower < F(48730, 100000)
    assert F(48821, 100000) < upper < F(48822, 100000)
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (25, 8, 28)
    assert failure["input_batch"] == []
    assert failure["face"] == list(range(20)) + list(range(22, 32))
    phase_width = result["phases"][-1]["old_width"]
    normalized_failure = failure["scaled_input_residual"] / phase_width
    assert normalized_failure < -F(1, 1000)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_7 == upper
    assert 0 < ratio_3 - ratio_7 < F(1, 100000)
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
        rho_scale=BETA_04882_SIX_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04882_SIX_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04882_SIX_LEAF_ZERO_ROOT_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] + len(EXPECTED_MAXIMUM_TIES) == 44
    assert audit["forced_coordinate_count_per_kind"] == 20
    assert len(audit["structural_maximum_tie_certificates"]) == 4

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04882_SIX_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04882_SIX_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "rho_scale": BETA_04882_SIX_LEAF_ZERO_ROOT_RHO_SCALE,
                    "relative_width": BETA_04882_SIX_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_04882_SIX_LEAF_ZERO_ROOT_STOP_BETA,
                    "same_chronology_stop_beta_interval": {
                        "lower": lower,
                        "lower_inclusive": True,
                        "upper": upper,
                        "upper_inclusive": False,
                    },
                    "failure_residual_over_phase_width": normalized_failure,
                    "product_3_minus_product_7_ratio": ratio_3 - ratio_7,
                    "comparison_audit": audit,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
