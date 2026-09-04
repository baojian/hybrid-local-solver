#!/usr/bin/env python3
"""Exact retimed extension of the beta-0.4865 branch-boundary cell."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox
from stopped_masked_input_residual_beta_04865_branch_boundary_exact import (
    BETA_04865_BRANCH_BOUNDARY_EDGES,
    BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH,
    BETA_04865_BRANCH_BOUNDARY_RHO_SCALE,
    BETA_04865_BRANCH_BOUNDARY_ROOT,
    BETA_04865_BRANCH_BOUNDARY_STOP_BETA,
    BETA_04865_BRANCH_BOUNDARY_VERTICES,
)


BETA_04865_BRANCH_BOUNDARY_RETIMED_ROOT = F(1, 262144)
BETA_04865_BRANCH_BOUNDARY_RETIMED_RHO_SCALE = F(756368731, 50000000000)
BETA_04865_BRANCH_BOUNDARY_RETIMED_STOP_BETA = F(973, 2000)
BETA_04865_BRANCH_BOUNDARY_RELAY_CASES = (
    (
        "bridge",
        BETA_04865_BRANCH_BOUNDARY_ROOT,
        BETA_04865_BRANCH_BOUNDARY_RHO_SCALE,
        BETA_04865_BRANCH_BOUNDARY_STOP_BETA,
    ),
    (
        "retimed_extension",
        BETA_04865_BRANCH_BOUNDARY_RETIMED_ROOT,
        BETA_04865_BRANCH_BOUNDARY_RETIMED_RHO_SCALE,
        BETA_04865_BRANCH_BOUNDARY_RETIMED_STOP_BETA,
    ),
)


def trace_case(neighbors, source, root: F, rho_scale: F, stop_beta: F) -> dict:
    return trace_retained_prox(
        neighbors,
        source=source,
        root=root,
        rho_scale=rho_scale,
        relative_width=BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=70,
        chronology="one-push-maximal",
        stop_beta=stop_beta,
    )


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_04865_BRANCH_BOUNDARY_VERTICES,
            "edges": list(BETA_04865_BRANCH_BOUNDARY_EDGES),
            "source": 0,
        },
        None,
    )
    assert (
        len(BETA_04865_BRANCH_BOUNDARY_EDGES)
        == len(set(BETA_04865_BRANCH_BOUNDARY_EDGES))
        == 64
    )

    summaries = []
    for name, root, rho_scale, stop_beta in BETA_04865_BRANCH_BOUNDARY_RELAY_CASES:
        result = trace_case(neighbors, source, root, rho_scale, stop_beta)
        assert result["status"] == "counterexample"
        assert result["total_products"] == 31
        witness = result["first_negative_active_input_residual"]
        assert (witness["phase"], witness["product"], witness["vertex"]) == (
            25,
            8,
            14,
        )
        assert witness["input_batch"] == []
        assert witness["face"] == list(range(20)) + [22, 23, 24, 25, 26]
        assert witness["value"] < 0

        cell = result["same_chronology_stop_beta_interval"]
        lower = cell["lower"]
        upper = cell["upper"]
        assert lower <= stop_beta < upper
        summaries.append(
            {
                "name": name,
                "root": root,
                "alpha": root**2 / (2 - root**2),
                "rho_scale": rho_scale,
                "rho": rho_scale / len(neighbors[source]),
                "chosen_stop_beta": stop_beta,
                "same_chronology_stop_beta_interval": cell,
                "degree_residual_over_phase_width": witness["value"]
                / witness["phase_old_width"],
                "preceding_inner_width_over_phase_width": witness[
                    "preceding_inner_width_over_old_width"
                ],
            }
        )

    first_cell = summaries[0]["same_chronology_stop_beta_interval"]
    second_cell = summaries[1]["same_chronology_stop_beta_interval"]
    assert F(48639, 100000) < first_cell["lower"] < F(48640, 100000)
    assert F(48650, 100000) < first_cell["upper"] < F(48651, 100000)
    assert F(48649, 100000) < second_cell["lower"] < F(48650, 100000)
    assert F(48658, 100000) < second_cell["upper"] < F(48659, 100000)
    assert second_cell["lower"] < first_cell["upper"]

    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample_relay",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_04865_BRANCH_BOUNDARY_VERTICES,
                    "edges": BETA_04865_BRANCH_BOUNDARY_EDGES,
                    "source": source,
                    "relative_width": BETA_04865_BRANCH_BOUNDARY_RELATIVE_WIDTH,
                    "cases": summaries,
                    "strict_cell_overlap": first_cell["upper"]
                    - second_cell["lower"],
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
