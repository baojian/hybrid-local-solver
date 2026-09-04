#!/usr/bin/env python3
"""Exact finite-root twenty-two-leaf counterexample at beta=.48951."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
)
from stopped_masked_input_residual_beta_04898_twenty_two_leaf_zero_root_limit_audit_exact import (
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES,
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RHO_SCALE,
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_STOP_BETA,
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_VERTICES,
    EXPECTED_INHERITED_ZEROS,
    EXPECTED_MAXIMUM_TIES,
    EXPECTED_POST_CLOSURE_ZEROS,
)


BETA_04898_TWENTY_TWO_LEAF_VERTICES = (
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_VERTICES
)
BETA_04898_TWENTY_TWO_LEAF_EDGES = BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_EDGES
BETA_04898_TWENTY_TWO_LEAF_ROOT = F(1, 65536)
BETA_04898_TWENTY_TWO_LEAF_RHO_SCALE = (
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RHO_SCALE
)
BETA_04898_TWENTY_TWO_LEAF_RELATIVE_WIDTH = (
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04898_TWENTY_TWO_LEAF_STOP_BETA = (
    BETA_04898_TWENTY_TWO_LEAF_ZERO_ROOT_STOP_BETA
)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04898_TWENTY_TWO_LEAF_VERTICES,
            "edges": list(BETA_04898_TWENTY_TWO_LEAF_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04898_TWENTY_TWO_LEAF_EDGES)
        == len(set(BETA_04898_TWENTY_TWO_LEAF_EDGES))
        == 86
    )
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=BETA_04898_TWENTY_TWO_LEAF_ROOT,
        rho_scale=BETA_04898_TWENTY_TWO_LEAF_RHO_SCALE,
        relative_width=BETA_04898_TWENTY_TWO_LEAF_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=BETA_04898_TWENTY_TWO_LEAF_STOP_BETA,
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
    assert witness["face"] == list(range(19)) + [
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
    assert witness["value"] < 0
    normalized_failure = witness["value"] / witness["phase_old_width"]
    assert normalized_failure < -F(1, 100000000000000)

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
    assert (upper_phase, upper_product, upper_vertex) == (27, 7, 25)
    assert F(48870, 100000) < lower < F(48872, 100000)
    assert F(48978, 100000) < upper < F(48979, 100000)
    assert lower < BETA_04898_TWENTY_TWO_LEAF_STOP_BETA < upper
    assert result["same_chronology_stop_beta_interval"] == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["stop"]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["stop"]["inner_width_over_old_width"]
    assert ratio_7 == upper < ratio_3
    assert ratio_3 - ratio_7 > F(1, 100000)

    # The shared full-comparison auditor evaluates the exact s=0 limiting
    # branch.  Calling it here couples this finite witness to the separately
    # proved strict limiting chronology without mislabeling it as a
    # finite-root comparison audit.
    limit_audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=BETA_04898_TWENTY_TWO_LEAF_RHO_SCALE,
        relative_width=BETA_04898_TWENTY_TWO_LEAF_RELATIVE_WIDTH,
        stop_beta=BETA_04898_TWENTY_TWO_LEAF_STOP_BETA,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_inherited_zeros=EXPECTED_INHERITED_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert limit_audit["grouped_equality_event_count"] == 41
    assert limit_audit["forced_coordinate_counts_by_kind"] == {
        "post_closure_active": 28,
        "active_input": 26,
        "raw_velocity": 26,
        "lower_clamp": 26,
    }
    assert len(limit_audit["structural_maximum_tie_certificates"]) == 8

    alpha = BETA_04898_TWENTY_TWO_LEAF_ROOT**2 / (
        2 - BETA_04898_TWENTY_TWO_LEAF_ROOT**2
    )
    assert alpha == F(1, 8589934591)
    rho = BETA_04898_TWENTY_TWO_LEAF_RHO_SCALE / len(neighbors[source])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_04898_TWENTY_TWO_LEAF_VERTICES,
                    "edges": BETA_04898_TWENTY_TWO_LEAF_EDGES,
                    "source": source,
                    "root": BETA_04898_TWENTY_TWO_LEAF_ROOT,
                    "alpha": alpha,
                    "rho_scale": BETA_04898_TWENTY_TWO_LEAF_RHO_SCALE,
                    "rho": rho,
                    "relative_width": BETA_04898_TWENTY_TWO_LEAF_RELATIVE_WIDTH,
                    "chosen_stop_beta": BETA_04898_TWENTY_TWO_LEAF_STOP_BETA,
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
                    "degree_residual_over_phase_width": normalized_failure,
                    "product_3_minus_product_7_ratio": ratio_3 - ratio_7,
                    "zero_root_comparison_audit": limit_audit,
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
