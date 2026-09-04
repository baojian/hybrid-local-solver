#!/usr/bin/env python3
"""Exact beta=.475 input-cone counterexample from one failure-side leaf."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import (
    build_graph,
    serialize,
    trace_retained_prox,
)
from stopped_masked_input_residual_high_beta_counterexample_exact import (
    BETA_0473_EDGES,
    RELATIVE_WIDTH,
    ROOT,
)


LEAF_0475_VERTICES = 28
LEAF_0475_EDGES = tuple(BETA_0473_EDGES) + ((14, 27),)
LEAF_0475_ROOT = ROOT
LEAF_0475_RHO_SCALE = F(79, 4000)
LEAF_0475_RELATIVE_WIDTH = RELATIVE_WIDTH
LEAF_0475_STOP_BETA = F(19, 40)


def main() -> None:
    """Replay the complete canonical history and verify its exact beta cell."""
    neighbors, source = build_graph(
        {
            "vertices": LEAF_0475_VERTICES,
            "edges": list(LEAF_0475_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(LEAF_0475_EDGES) == 51
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=LEAF_0475_ROOT,
        rho_scale=LEAF_0475_RHO_SCALE,
        relative_width=LEAF_0475_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=LEAF_0475_STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 28
    witness = result["first_negative_active_input_residual"]
    assert witness["phase"] == 22
    assert witness["product"] == 8
    assert witness["vertex"] == 27
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(20)) + [22, 24, 25, 26, 27]
    assert witness["value"] < 0
    predecessor_ratio = witness["preceding_inner_width_over_old_width"]
    assert predecessor_ratio is not None
    assert predecessor_ratio > LEAF_0475_STOP_BETA

    stopped: list[tuple[F, int, int]] = []
    continued: list[tuple[F, int, int]] = []
    for phase in result["phases"]:
        for product in phase["products"]:
            if not product["executed"]:
                continue
            entry = (
                product["stop"]["inner_width_over_old_width"],
                phase["phase"],
                product["product"],
            )
            (stopped if product["stop"]["decision"] else continued).append(entry)
    lower, lower_phase, lower_product = max(stopped)
    upper, upper_phase, upper_product = min(continued)
    assert (lower_phase, lower_product) == (21, 1)
    assert (upper_phase, upper_product) == (22, 3)
    assert F(472, 1000) < lower < F(473, 1000)
    assert F(476, 1000) < upper < F(477, 1000)
    assert lower <= LEAF_0475_STOP_BETA < upper
    reported_cell = result["same_chronology_stop_beta_interval"]
    assert reported_cell == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }

    failure_phase = result["phases"][-1]
    phase_clock = [
        {
            "product": product["product"],
            "ratio": product["stop"]["inner_width_over_old_width"],
            "maximum_vertex": product["stop"]["maximum_positive_residual_vertex"],
        }
        for product in failure_phase["products"]
        if product["executed"]
    ]
    assert [entry["maximum_vertex"] for entry in phase_clock] == [
        26,
        26,
        26,
        25,
        25,
        25,
        25,
    ]

    leaf_publications = []
    for phase in result["phases"]:
        for product in phase["products"]:
            if 27 in product["input_frontier"]["positive"]:
                leaf_publications.append(
                    (phase["phase"], product["product"], "input-frontier")
                )
            for closure in product.get("post_product_admissions", []):
                if 27 in closure["admitted"]:
                    leaf_publications.append(
                        (phase["phase"], product["product"], "append-closure")
                    )
    assert leaf_publications == [(4, 1, "append-closure")]

    # In degree coordinates the pendant row has degree one.  Its complete
    # input residual is therefore this scalar port-forcing identity.  The
    # exact negative sign comes from the leaf's positive retained velocity,
    # not from a missing exterior contribution.
    alpha = LEAF_0475_ROOT * LEAF_0475_ROOT / (
        2 - LEAF_0475_ROOT * LEAF_0475_ROOT
    )
    shifted_diagonal = (1 + 3 * alpha) / 2
    coupling = (1 - alpha) / 2
    active_input_residuals = dict(witness["active_input_residuals"])
    leaf_formula = (
        witness["shifted_load"][27]
        - shifted_diagonal * witness["input_extrapolate"][27]
        + coupling * witness["input_extrapolate"][14]
    )
    assert leaf_formula == active_input_residuals[27] == witness["value"]
    assert witness["current"][27] > witness["previous"][27]

    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": (
                        "canonical zero-start one-push-maximal chronology; "
                        "exact beta=.475 cell from one failure-side leaf"
                    ),
                    "vertices": LEAF_0475_VERTICES,
                    "edges": LEAF_0475_EDGES,
                    "source": source,
                    "root": LEAF_0475_ROOT,
                    "alpha": alpha,
                    "rho_scale": LEAF_0475_RHO_SCALE,
                    "rho": LEAF_0475_RHO_SCALE / len(neighbors[source]),
                    "relative_width": LEAF_0475_RELATIVE_WIDTH,
                    "verified_stop_beta": LEAF_0475_STOP_BETA,
                    "failure_phase_one_based": witness["phase"],
                    "failure_product_one_based": witness["product"],
                    "failure_vertex": witness["vertex"],
                    "failure_face": witness["face"],
                    "active_input_residual_over_phase_width": (
                        witness["value"] / witness["phase_old_width"]
                    ),
                    "predecessor_width_over_phase_width": predecessor_ratio,
                    "same_chronology_stop_beta_interval": reported_cell,
                    "cell_endpoint_attainment": {
                        "lower": [lower_phase, lower_product],
                        "upper": [upper_phase, upper_product],
                    },
                    "failure_phase_clock": phase_clock,
                    "leaf_publication_history": leaf_publications,
                    "leaf_failure_identity": {
                        "formula": "h_27-b*q_27+c*q_14",
                        "shifted_load_h_27": witness["shifted_load"][27],
                        "input_q_27": witness["input_extrapolate"][27],
                        "input_q_14": witness["input_extrapolate"][14],
                        "value": leaf_formula,
                    },
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
