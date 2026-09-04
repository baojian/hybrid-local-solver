#!/usr/bin/env python3
"""Exact full comparison audit for the twenty-two-leaf beta-0.48951 limit."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
)
from stopped_masked_input_residual_beta_04896_twenty_leaf_zero_root_limit_audit_exact import (
    BETA_04896_TWENTY_LEAF_ZERO_ROOT_EDGES,
    BETA_04896_TWENTY_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
)


BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_VERTICES = 49
BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES = tuple(
    sorted(set(BETA_04896_TWENTY_LEAF_ZERO_ROOT_EDGES) | {(5, 47), (19, 48)})
)
BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RHO_SCALE = F(1169, 100000)
BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RELATIVE_WIDTH = (
    BETA_04896_TWENTY_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_STOP_BETA = F(48951, 100000)

EXPECTED_POST_CLOSURE_ZEROS = {
    (1, 1): (2, 30, 33, 37),
    (2, 1): (4, 18),
    (4, 1): (8, 14, 27, 29, 31, 35, 39, 43, 44, 45),
    (5, 1): (15, 36, 46),
    (7, 1): (24,),
    (8, 1): (28,),
    (10, 1): (10,),
    (14, 1): (41, 47),
    (15, 1): (26,),
    (21, 1): (25,),
    # Unlike the earlier events, this batch is followed by another product
    # in the same phase.  Carried velocities at its neighboring active rows
    # change the next extrapolate, so the zero is not inherited at product 8.
    (27, 7): (22, 23),
}
EXPECTED_INHERITED_ZEROS = {
    (2, 1): (2, 30, 33, 37),
    (3, 1): (4, 18),
    (5, 1): (8, 14, 27, 29, 31, 35, 39, 43, 44, 45),
    (6, 1): (15, 36, 46),
    (8, 1): (24,),
    (9, 1): (28,),
    (11, 1): (10,),
    (15, 1): (41, 47),
    (16, 1): (26,),
    (22, 1): (25,),
}
EXPECTED_MAXIMUM_TIES = (
    (22, 1, (33, 37)),
    (23, 1, (33, 37)),
    (24, 1, (33, 37)),
    (25, 1, (27, 31, 35, 43)),
    (26, 1, (27, 31, 35, 43)),
    (27, 1, (41, 47)),
    (27, 2, (41, 47)),
    (27, 3, (41, 47)),
)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES)
        == len(set(BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES))
        == 86
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 33
    lower, upper = result["cell"]
    assert F(48870, 100000) < lower < F(48872, 100000)
    assert F(48978, 100000) < upper < F(48979, 100000)
    assert lower < BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_STOP_BETA < upper

    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (
        27,
        8,
        28,
    )
    assert failure["input_batch"] == []
    assert failure["face"] == list(range(19)) + [
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
        43,
        44,
        45,
        46,
        47,
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
    assert min(continued) == (upper, 27, 7, 25)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_7 == upper < ratio_3
    assert ratio_3 - ratio_7 > F(1, 100000)

    audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RHO_SCALE,
        relative_width=BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_inherited_zeros=EXPECTED_INHERITED_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] == 41
    assert audit["forced_coordinate_counts_by_kind"] == {
        "post_closure_active": 28,
        "active_input": 26,
        "raw_velocity": 26,
        "lower_clamp": 26,
    }
    assert len(audit["structural_maximum_tie_certificates"]) == 8
    terminal_zero_certificate = audit["structural_zero_certificates"][-1]
    assert terminal_zero_certificate == {
        "phase": 27,
        "product": 7,
        "zero_vertices": (22, 23),
        "closure_batches": [(22, 23)],
        "reason": "direct diagonal cancellation and no same/later pushed neighbor",
    }

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "rho_scale": BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RHO_SCALE,
                    "relative_width": (
                        BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RELATIVE_WIDTH
                    ),
                    "chosen_stop_beta": (
                        BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_STOP_BETA
                    ),
                    "same_chronology_stop_beta_interval": {
                        "lower": lower,
                        "lower_inclusive": True,
                        "upper": upper,
                        "upper_inclusive": False,
                    },
                    "chronology_cell_attainment": {
                        "lower_attained_at": [26, 1, 27],
                        "upper_attained_at": [27, 7, 25],
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
