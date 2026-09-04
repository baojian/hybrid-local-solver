#!/usr/bin/env python3
"""Exact full comparison audit for the eight-leaf beta-0.48853 limit."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
    expected_equality_events,
)
from stopped_masked_input_residual_beta_04882_six_leaf_zero_root_limit_audit_exact import (
    BETA_04882_SIX_LEAF_ZERO_ROOT_EDGES,
    BETA_04882_SIX_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
)


BETA_04885_EIGHT_LEAF_ZERO_ROOT_VERTICES = 35
BETA_04885_EIGHT_LEAF_ZERO_ROOT_EDGES = tuple(
    sorted(set(BETA_04882_SIX_LEAF_ZERO_ROOT_EDGES) | {(1, 33), (23, 34)})
)
BETA_04885_EIGHT_LEAF_ZERO_ROOT_RHO_SCALE = F(136261, 10000000)
BETA_04885_EIGHT_LEAF_ZERO_ROOT_RELATIVE_WIDTH = (
    BETA_04882_SIX_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04885_EIGHT_LEAF_ZERO_ROOT_STOP_BETA = F(48821, 100000)
BETA_04885_EIGHT_LEAF_ZERO_ROOT_RELAY_CASES = (
    {
        "name": "entry",
        "rho_scale": F(1363, 100000),
        "stop_beta": F(2441, 5000),
    },
    {
        "name": "middle",
        "rho_scale": F(109, 8000),
        "stop_beta": F(1221, 2500),
    },
    {
        "name": "extension",
        "rho_scale": F(544839, 40000000),
        "stop_beta": F(977, 2000),
    },
)

EXPECTED_POST_CLOSURE_ZEROS = {
    (1, 1): (30, 33),
    (3, 1): (29,),
    (4, 1): (8, 14, 27, 31),
    (5, 1): (5, 15),
    (6, 1): (24,),
    (7, 1): (9,),
    (9, 1): (28,),
    (10, 1): (10,),
    (13, 1): (19, 22),
    (16, 1): (26,),
    (21, 1): (25,),
}
EXPECTED_MAXIMUM_TIES = tuple(
    (phase, 1, (27, 31)) for phase in range(23, 26)
)


def replay_case(
    neighbors: list[set[int]],
    source: int,
    case: dict[str, object],
) -> dict[str, object]:
    rho_scale = case["rho_scale"]
    stop_beta = case["stop_beta"]
    assert isinstance(rho_scale, F)
    assert isinstance(stop_beta, F)
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=rho_scale,
        relative_width=BETA_04885_EIGHT_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=stop_beta,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 32
    lower, upper = result["cell"]
    assert lower < stop_beta < upper
    assert F(48806, 100000) < lower < F(48840, 100000)
    assert F(48840, 100000) < upper < F(48870, 100000)
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
    ]
    phase_width = result["phases"][-1]["old_width"]
    normalized_failure = failure["scaled_input_residual"] / phase_width
    assert normalized_failure < -F(1, 1000)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert min(ratio_3, ratio_7) == upper
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
        rho_scale=rho_scale,
        relative_width=BETA_04885_EIGHT_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=stop_beta,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] + len(EXPECTED_MAXIMUM_TIES) == 47
    assert audit["forced_coordinate_count_per_kind"] == 17
    assert len(audit["structural_maximum_tie_certificates"]) == 3
    return {
        "name": case["name"],
        "rho_scale": rho_scale,
        "chosen_stop_beta": stop_beta,
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


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04885_EIGHT_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04885_EIGHT_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04885_EIGHT_LEAF_ZERO_ROOT_EDGES)
        == len(set(BETA_04885_EIGHT_LEAF_ZERO_ROOT_EDGES))
        == 72
    )
    cases = [replay_case(neighbors, source, case) for case in (
        BETA_04885_EIGHT_LEAF_ZERO_ROOT_RELAY_CASES
    )]
    for left, right in zip(cases, cases[1:]):
        assert (
            right["same_chronology_stop_beta_interval"]["lower"]
            < left["same_chronology_stop_beta_interval"]["upper"]
        )

    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04885_EIGHT_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04885_EIGHT_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "relative_width": BETA_04885_EIGHT_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
                    "relay_cases": cases,
                    "covered_interval": {
                        "lower": cases[0]["same_chronology_stop_beta_interval"][
                            "lower"
                        ],
                        "lower_inclusive": True,
                        "upper": cases[-1]["same_chronology_stop_beta_interval"][
                            "upper"
                        ],
                        "upper_inclusive": False,
                    },
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
