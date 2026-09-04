#!/usr/bin/env python3
"""Exact canonical counterexample to the quarter-stopped input-cone claim."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox


VERTICES = 16
EDGES = (
    (0, 1),
    (0, 10),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (7, 12),
    (8, 9),
    (9, 10),
    (9, 11),
    (10, 15),
    (11, 12),
    (12, 13),
    (12, 14),
    (13, 14),
    (14, 15),
)
ROOT = F(1, 224)
RHO_SCALE = F(481, 8000)
RELATIVE_WIDTH = F(1, 1000)


def main() -> None:
    neighbors, source = build_graph(
        {"vertices": VERTICES, "edges": list(EDGES), "source": 0},
        None,
    )
    result = trace_retained_prox(
        neighbors,
        source=source,
        root=ROOT,
        rho_scale=RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 47
    witness = result["first_negative_active_input_residual"]
    assert witness["phase"] == 20
    assert witness["product"] == 10
    assert witness["vertex"] == 11
    assert witness["input_batch"] == []
    assert witness["face"] == [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        8,
        9,
        10,
        11,
        12,
        14,
        15,
    ]
    assert witness["value"] < 0
    preceding_ratio = witness["preceding_inner_width_over_old_width"]
    assert preceding_ratio is not None
    assert preceding_ratio > F(1, 4)
    beta_cell = result["same_chronology_stop_beta_interval"]
    assert beta_cell["lower"] <= F(1, 4) < beta_cell["upper"]
    degree_ratio = witness["value"] / witness["phase_old_width"]
    alpha = ROOT * ROOT / (2 - ROOT * ROOT)
    rho = RHO_SCALE / len(neighbors[0])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": (
                        "canonical zero-start one-push-maximal chronology with "
                        "the quarter inner stopping rule"
                    ),
                    "vertices": VERTICES,
                    "edges": EDGES,
                    "source": 0,
                    "root": ROOT,
                    "alpha": alpha,
                    "rho_scale": RHO_SCALE,
                    "rho": rho,
                    "relative_width": RELATIVE_WIDTH,
                    "completed_products_before_failure": result["total_products"],
                    "failure_phase_one_based": witness["phase"],
                    "failure_product_in_phase_one_based": witness["product"],
                    "failure_vertex": witness["vertex"],
                    "input_batch_at_failure": witness["input_batch"],
                    "failure_face": witness["face"],
                    "degree_coordinate_input_residual": witness["value"],
                    "degree_residual_over_phase_width": degree_ratio,
                    "preceding_inner_width_over_phase_width": preceding_ratio,
                    "same_chronology_stop_beta_interval": beta_cell,
                    "quarter_stop_would_execute_failure_product": True,
                    "scope_warning": (
                        "the witness refutes every beta in the reported "
                        "half-open chronology interval; outside that interval "
                        "the outer history changes and must be re-audited"
                    ),
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
