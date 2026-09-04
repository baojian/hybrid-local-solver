#!/usr/bin/env python3
"""Three exact cells relaying the stopped-input-cone cover past beta=.486."""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox


BETA_0486_RELAY_VERTICES = 27
BETA_0486_RELAY_EDGES = (
    (0, 1),
    (0, 12),
    (1, 2),
    (1, 3),
    (1, 6),
    (1, 11),
    (2, 4),
    (2, 5),
    (2, 8),
    (2, 10),
    (2, 11),
    (2, 24),
    (3, 4),
    (3, 6),
    (3, 8),
    (3, 9),
    (3, 11),
    (4, 5),
    (4, 6),
    (4, 7),
    (4, 8),
    (4, 9),
    (4, 11),
    (5, 6),
    (5, 7),
    (5, 8),
    (5, 9),
    (5, 10),
    (5, 11),
    (6, 7),
    (6, 8),
    (7, 10),
    (7, 11),
    (8, 9),
    (8, 10),
    (8, 26),
    (9, 10),
    (9, 11),
    (10, 11),
    (10, 26),
    (12, 13),
    (13, 16),
    (13, 17),
    (13, 18),
    (14, 15),
    (14, 16),
    (14, 17),
    (15, 16),
    (15, 17),
    (15, 20),
    (16, 17),
    (17, 18),
    (18, 19),
    (18, 21),
    (18, 22),
    (18, 23),
    (19, 20),
    (19, 21),
    (20, 21),
    (20, 22),
    (20, 23),
    (21, 22),
    (21, 23),
    (24, 25),
)
BETA_0486_RELAY_RELATIVE_WIDTH = F(1, 1000)

# name, root, rho_scale, stop_beta, failure_vertex
BETA_0486_RELAY_CASES = (
    ("beta-0.4847-bridge", F(1, 240), F(303, 20000), F(4847, 10000), 15),
    ("beta-0.485", F(1, 320), F(3029, 200000), F(97, 200), 15),
    ("beta-0.486", F(1, 4096), F(15141, 1000000), F(243, 500), 14),
)


def main() -> None:
    neighbors, source = build_graph(
        {
            "vertices": BETA_0486_RELAY_VERTICES,
            "edges": list(BETA_0486_RELAY_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_0486_RELAY_EDGES) == len(set(BETA_0486_RELAY_EDGES)) == 64
    reports: list[dict[str, object]] = []
    previous_upper: F | None = None
    for name, root, rho_scale, stop_beta, failure_vertex in BETA_0486_RELAY_CASES:
        result = trace_retained_prox(
            neighbors,
            source=source,
            root=root,
            rho_scale=rho_scale,
            relative_width=BETA_0486_RELAY_RELATIVE_WIDTH,
            maximum_phase_products=100,
            maximum_phases=70,
            chronology="one-push-maximal",
            stop_beta=stop_beta,
        )
        assert result["status"] == "counterexample"
        assert result["total_products"] == 31
        witness = result["first_negative_active_input_residual"]
        assert (witness["phase"], witness["product"]) == (25, 8)
        assert witness["vertex"] == failure_vertex
        assert witness["input_batch"] == []
        assert witness["value"] < 0
        cell = result["same_chronology_stop_beta_interval"]
        lower = cell["lower"]
        upper = cell["upper"]
        assert lower <= stop_beta < upper
        assert F(4845, 10000) < lower < F(486, 1000)
        assert upper > F(4853, 10000)
        if previous_upper is not None:
            assert lower < previous_upper
        previous_upper = upper
        alpha = root**2 / (2 - root**2)
        reports.append(
            {
                "name": name,
                "root": root,
                "alpha": alpha,
                "rho_scale": rho_scale,
                "rho": rho_scale / len(neighbors[source]),
                "chosen_stop_beta": stop_beta,
                "same_chronology_stop_beta_interval": cell,
                "completed_products_before_failure": result["total_products"],
                "failure_phase_one_based": witness["phase"],
                "failure_product_in_phase_one_based": witness["product"],
                "failure_vertex": witness["vertex"],
                "input_batch_at_failure": witness["input_batch"],
                "failure_face": witness["face"],
                "degree_residual_over_phase_width": witness["value"]
                / witness["phase_old_width"],
                "preceding_inner_width_over_phase_width": witness[
                    "preceding_inner_width_over_old_width"
                ],
            }
        )
    assert reports[0]["same_chronology_stop_beta_interval"]["lower"] < F(
        484546, 1000000
    )
    assert reports[-1]["same_chronology_stop_beta_interval"]["upper"] > F(
        486099, 1000000
    )
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample-relay",
                    "scope": "canonical zero-start one-push-maximal chronology",
                    "vertices": BETA_0486_RELAY_VERTICES,
                    "edges": BETA_0486_RELAY_EDGES,
                    "source": source,
                    "relative_width": BETA_0486_RELAY_RELATIVE_WIDTH,
                    "cases": reports,
                    "claim": "the three exact failure cells form an overlapping relay",
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
