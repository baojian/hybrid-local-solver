#!/usr/bin/env python3
"""Exact comparison audit for the stronger eighteen-leaf rho retiming."""

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
    BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_VERTICES,
    EXPECTED_MAXIMUM_TIES,
    EXPECTED_POST_CLOSURE_ZEROS,
)


BETA_04894_EIGHTEEN_LEAF_RETIMED_RHO_SCALE = F(6120857, 500000000)
BETA_04894_EIGHTEEN_LEAF_RETIMED_STOP_BETA = F(9787, 20000)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04894_EIGHTEEN_LEAF_RETIMED_RHO_SCALE,
        relative_width=BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04894_EIGHTEEN_LEAF_RETIMED_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 33
    lower, upper = result["cell"]
    assert F(48846, 100000) < lower < F(48848, 100000)
    assert F(48938, 100000) < upper < F(48939, 100000)
    assert lower < BETA_04894_EIGHTEEN_LEAF_RETIMED_STOP_BETA < upper
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (
        27,
        8,
        28,
    )
    assert failure["input_batch"] == [19, 22, 23]
    phase_width = result["phases"][-1]["old_width"]
    normalized_failure = failure["scaled_input_residual"] / phase_width
    assert normalized_failure < -F(1, 1000)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_3 == upper < ratio_7
    assert 0 < ratio_7 - ratio_3 < F(1, 10000000)

    audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=BETA_04894_EIGHTEEN_LEAF_RETIMED_RHO_SCALE,
        relative_width=BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04894_EIGHTEEN_LEAF_RETIMED_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "rho_scale": BETA_04894_EIGHTEEN_LEAF_RETIMED_RHO_SCALE,
                    "relative_width": (
                        BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH
                    ),
                    "chosen_stop_beta": BETA_04894_EIGHTEEN_LEAF_RETIMED_STOP_BETA,
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
