#!/usr/bin/env python3
"""Exact fixed-branch p3/p7 equioscillation on the E22 zero-root graph."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
)
from stopped_masked_input_residual_beta_04898_twenty_two_leaf_zero_root_limit_audit_exact import (
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES,
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_VERTICES,
    EXPECTED_INHERITED_ZEROS,
    EXPECTED_MAXIMUM_TIES,
    EXPECTED_POST_CLOSURE_ZEROS,
)


BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_VERTICES = BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_VERTICES
BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_EDGES = BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES
BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RHO_SCALE = F(
    987676041359525989145724568491697235274655264942305031603363997399106787905678745966289710398522604268442509928835973405774451141084474777106887665457391325872941966579538923101636232285464805220864234147,
    84487002648146815751370354040123617020211222433873978417690221069038367485793385409793636205662385170169830103530578726117948355591456003276239355669579769263869771628089515966624311726719266205928842532251,
)
BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RELATIVE_WIDTH = (
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_STOP_BETA = F(48979, 100000)


def audit_zero_equioscillation(
    neighbors: list[set[int]],
    source: int,
) -> dict[str, object]:
    """Run the reusable full comparison audit on the zero-root branch."""
    audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RHO_SCALE,
        relative_width=BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RELATIVE_WIDTH,
        stop_beta=BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_inherited_zeros=EXPECTED_INHERITED_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["grouped_equality_event_count"] == 41
    assert audit["forced_coordinate_counts_by_kind"] == {
        "post_closure_active": 28,
        "active_input": 26,
        "raw_velocity": 26,
        "lower_clamp": 26,
    }
    assert len(audit["structural_maximum_tie_certificates"]) == 8
    assert all(value > 0 for value in audit["minimum_strict_margins"].values())
    return audit


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_VERTICES,
            "edges": list(BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_EDGES)
        == len(set(BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_EDGES))
        == 86
    )
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RHO_SCALE,
        relative_width=BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RELATIVE_WIDTH,
        stop_beta=BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 33
    lower, upper = result["cell"]
    assert F(48869, 100000) < lower < F(48870, 100000)
    assert F(4897917, 10000000) < upper < F(4897918, 10000000)
    assert lower < BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_STOP_BETA < upper

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
    upper_attainments = tuple(
        (phase, product, vertex) for ratio, phase, product, vertex in continued if ratio == upper
    )
    assert upper_attainments == ((27, 3, 41), (27, 7, 25))

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_3 == ratio_7 == upper

    audit = audit_zero_equioscillation(neighbors, source)
    assert audit["failure"] == failure

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_VERTICES,
                    "edges": BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_EDGES,
                    "source": source,
                    "rho_scale": (BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RHO_SCALE),
                    "relative_width": (BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RELATIVE_WIDTH),
                    "chosen_stop_beta": (BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_STOP_BETA),
                    "same_chronology_stop_beta_interval": {
                        "lower": lower,
                        "lower_inclusive": True,
                        "upper": upper,
                        "upper_inclusive": False,
                    },
                    "chronology_cell_attainment": {
                        "lower_attained_at": [26, 1, 27],
                        "upper_attained_at": [
                            [27, 3, 41],
                            [27, 7, 25],
                        ],
                    },
                    "designed_cross_product_equioscillation": {
                        "left": [27, 3, 41],
                        "right": [27, 7, 25],
                        "common_ratio": upper,
                        "algorithmic_branch_tie": False,
                        "reason": (
                            "the equal ratios occur at distinct products; every "
                            "non-structurally-forced within-product maximum and "
                            "stop comparison remains strict"
                        ),
                    },
                    "failure_residual_over_phase_width": normalized_failure,
                    "comparison_audit": audit,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
