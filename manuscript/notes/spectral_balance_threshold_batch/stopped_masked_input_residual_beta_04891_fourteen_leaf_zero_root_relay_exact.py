#!/usr/bin/env python3
"""Exact two-rho zero-root relay for the fourteen-leaf extension."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize
from retained_prox_input_cone_zero_root_limit_exact import trace_zero_root_limit
from stopped_masked_input_residual_beta_04862_zero_root_limit_audit_exact import (
    audit_comparisons,
)
from stopped_masked_input_residual_beta_04890_twelve_leaf_zero_root_limit_audit_exact import (
    BETA_04890_TWELVE_LEAF_ZERO_ROOT_EDGES,
    BETA_04890_TWELVE_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
)


BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_VERTICES = 41
BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_EDGES = tuple(
    sorted(set(BETA_04890_TWELVE_LEAF_ZERO_ROOT_EDGES) | {(2, 39), (20, 40)})
)
BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH = (
    BETA_04890_TWELVE_LEAF_ZERO_ROOT_RELATIVE_WIDTH
)
BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_RELAY_CASES = (
    {
        "name": "entry",
        "rho_scale": F(1260037, 100000000),
        "stop_beta": F(244449, 500000),
    },
    {
        "name": "extension",
        "rho_scale": F(629919, 50000000),
        "stop_beta": F(489, 1000),
    },
)

EXPECTED_POST_CLOSURE_ZEROS = {
    (1, 1): (2, 30, 33, 37),
    (2, 1): (4, 18),
    (4, 1): (14, 29, 39),
    (5, 1): (5, 8, 15, 27, 31, 35, 36),
    (6, 1): (7,),
    (7, 1): (11, 24),
    (8, 1): (9, 28),
    (10, 1): (10,),
    (13, 1): (22,),
    (15, 1): (26,),
    (21, 1): (25,),
}
EXPECTED_MAXIMUM_TIES = (
    (21, 1, (33, 37)),
    (22, 1, (33, 37)),
    (23, 1, (27, 31, 35)),
    (24, 1, (27, 31, 35)),
    (25, 1, (27, 31, 35)),
    (26, 1, (27, 31, 35)),
)


def replay_case(
    neighbors: list[set[int]], source: int, case: dict[str, object]
) -> dict[str, object]:
    rho_scale = case["rho_scale"]
    stop_beta = case["stop_beta"]
    assert isinstance(rho_scale, F)
    assert isinstance(stop_beta, F)
    result = trace_zero_root_limit(
        neighbors,
        source=source,
        rho_scale=rho_scale,
        relative_width=BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=stop_beta,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 32
    lower, upper = result["cell"]
    assert lower < stop_beta < upper
    failure = result["failure"]
    assert (failure["phase"], failure["product"], failure["vertex"]) == (
        26,
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
    assert max(stopped) == (lower, 25, 1, 27)
    assert min(continued) == (upper, 26, 3, 26)

    failure_phase = result["phases"][-1]["products"]
    ratio_3 = failure_phase[2]["inner_width_over_old_width"]
    ratio_7 = failure_phase[6]["inner_width_over_old_width"]
    assert ratio_3 == upper < ratio_7

    audit = audit_comparisons(
        neighbors,
        source,
        rho_scale=rho_scale,
        relative_width=BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH,
        stop_beta=stop_beta,
        expected_post_closure_zeros=EXPECTED_POST_CLOSURE_ZEROS,
        expected_maximum_ties=EXPECTED_MAXIMUM_TIES,
    )
    assert audit["failure"] == failure
    assert audit["grouped_equality_event_count"] == 44
    assert audit["forced_coordinate_count_per_kind"] == 25
    assert len(audit["structural_maximum_tie_certificates"]) == 6
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
        "chronology_cell_attainment": {
            "lower_attained_at": [25, 1, 27],
            "upper_attained_at": [26, 3, 26],
        },
        "failure_residual_over_phase_width": normalized_failure,
        "product_7_minus_product_3_ratio": ratio_7 - ratio_3,
        "comparison_audit": audit,
    }


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_VERTICES,
            "edges": list(BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_EDGES)
        == len(set(BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_EDGES))
        == 78
    )
    cases = [
        replay_case(neighbors, source, case)
        for case in BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_RELAY_CASES
    ]
    assert (
        cases[1]["same_chronology_stop_beta_interval"]["lower"]
        < cases[0]["same_chronology_stop_beta_interval"]["upper"]
    )
    print(
        json.dumps(
            serialize(
                {
                    "status": "strict_modulo_structurally_forced_equalities",
                    "scope": "canonical zero-start one-push-maximal s=0 limit",
                    "vertices": BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_VERTICES,
                    "edges": BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_EDGES,
                    "source": source,
                    "relative_width": (
                        BETA_04891_FOURTEEN_LEAF_ZERO_ROOT_RELATIVE_WIDTH
                    ),
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
