#!/usr/bin/env python3
"""Exact canonical counterexample to the one-third-stopped input-cone claim."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox


VERTICES = 24
EDGES = (
    (0, 1),
    (0, 12),
    (1, 2),
    (1, 6),
    (1, 11),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 8),
    (2, 10),
    (2, 11),
    (3, 4),
    (3, 5),
    (4, 5),
    (4, 6),
    (4, 8),
    (5, 6),
    (5, 9),
    (6, 7),
    (7, 8),
    (8, 9),
    (8, 10),
    (9, 10),
    (10, 11),
    (12, 13),
    (13, 14),
    (13, 17),
    (13, 18),
    (14, 15),
    (15, 16),
    (15, 17),
    (15, 20),
    (16, 17),
    (16, 20),
    (17, 18),
    (18, 19),
    (18, 20),
    (18, 22),
    (18, 23),
    (19, 20),
    (20, 21),
    (20, 23),
    (21, 22),
    (22, 23),
)
ROOT = F(1, 224)
RHO_SCALE = F(173, 8000)
RELATIVE_WIDTH = F(1, 1000)
STOP_BETA = F(1, 3)


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
        stop_beta=STOP_BETA,
    )
    assert result["status"] == "counterexample"
    assert result["total_products"] == 18
    witness = result["first_negative_active_input_residual"]
    assert witness["phase"] == 13
    assert witness["product"] == 7
    assert witness["vertex"] == 16
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(19))
    assert witness["value"] < 0
    preceding_ratio = witness["preceding_inner_width_over_old_width"]
    assert preceding_ratio is not None
    assert preceding_ratio > STOP_BETA
    beta_cell = result["same_chronology_stop_beta_interval"]
    assert beta_cell["lower"] <= STOP_BETA < beta_cell["upper"]
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
                        "the one-third inner stopping rule"
                    ),
                    "vertices": VERTICES,
                    "edges": EDGES,
                    "source": 0,
                    "root": ROOT,
                    "alpha": alpha,
                    "rho_scale": RHO_SCALE,
                    "rho": rho,
                    "relative_width": RELATIVE_WIDTH,
                    "stop_beta": STOP_BETA,
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
                    "one_third_stop_would_execute_failure_product": True,
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
