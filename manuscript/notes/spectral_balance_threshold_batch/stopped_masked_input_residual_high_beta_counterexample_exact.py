#!/usr/bin/env python3
"""Exact canonical counterexample on a high interval of stopping constants."""

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
    (2, 6),
    (2, 8),
    (2, 10),
    (2, 11),
    (3, 4),
    (3, 5),
    (3, 11),
    (4, 5),
    (4, 6),
    (4, 8),
    (5, 6),
    (5, 7),
    (5, 9),
    (5, 10),
    (6, 7),
    (7, 8),
    (7, 11),
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
    (16, 17),
    (16, 20),
    (17, 18),
    (18, 19),
    (18, 20),
    (18, 21),
    (18, 22),
    (18, 23),
    (19, 20),
    (20, 21),
    (20, 23),
    (22, 23),
)
ROOT = F(1, 224)
RHO_SCALE = F(201, 10000)
RELATIVE_WIDTH = F(1, 1000)
STOP_BETA = F(221393, 500000)
MIDDLE_STOP_BETA = F(419, 1000)

# A nearby search lineage gives a cell bridging the earlier two-fifths
# witness to the two cells above.
BRIDGE_EDGES = (
    (0, 1),
    (0, 12),
    (1, 2),
    (1, 5),
    (1, 6),
    (1, 11),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 8),
    (2, 10),
    (2, 11),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 9),
    (3, 11),
    (4, 5),
    (4, 6),
    (4, 8),
    (5, 6),
    (5, 7),
    (5, 9),
    (5, 10),
    (6, 7),
    (6, 11),
    (7, 10),
    (7, 11),
    (8, 9),
    (8, 10),
    (9, 10),
    (10, 11),
    (12, 13),
    (13, 14),
    (13, 17),
    (13, 18),
    (14, 15),
    (14, 17),
    (15, 16),
    (15, 17),
    (16, 17),
    (16, 20),
    (17, 18),
    (18, 19),
    (18, 20),
    (18, 21),
    (18, 22),
    (18, 23),
    (19, 20),
    (20, 23),
    (22, 23),
)
BRIDGE_RHO_SCALE = F(12, 625)
BRIDGE_STOP_BETA = F(417, 1000)

# A denser member of the same two-lobe family crosses beta=0.45.
DENSE_EDGES = (
    (0, 1),
    (0, 12),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 6),
    (1, 7),
    (1, 11),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 8),
    (2, 10),
    (2, 11),
    (3, 4),
    (3, 6),
    (3, 7),
    (3, 11),
    (4, 5),
    (4, 6),
    (4, 7),
    (4, 8),
    (5, 6),
    (5, 9),
    (5, 11),
    (6, 7),
    (6, 8),
    (6, 9),
    (6, 10),
    (6, 11),
    (7, 8),
    (7, 10),
    (7, 11),
    (8, 9),
    (8, 10),
    (8, 11),
    (9, 10),
    (10, 11),
    (12, 13),
    (13, 14),
    (13, 15),
    (13, 17),
    (13, 18),
    (14, 15),
    (14, 16),
    (14, 17),
    (15, 17),
    (16, 17),
    (16, 18),
    (16, 20),
    (17, 18),
    (18, 19),
    (18, 20),
    (18, 21),
    (18, 22),
    (18, 23),
    (19, 20),
    (20, 21),
    (20, 22),
    (20, 23),
    (21, 22),
    (22, 23),
)
DENSE_RHO_SCALE = F(77, 5000)
DENSE_STOP_BETA = F(9, 20)

# A sparse three-leaf augmentation of the original 24-vertex graph extends
# the exact cover farther toward 1/2 than the dense search witness.
STRUCTURED_VERTICES = 27
STRUCTURED_EDGES = (
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
    (2, 24),
    (3, 4),
    (3, 5),
    (4, 5),
    (4, 6),
    (4, 8),
    (5, 6),
    (5, 9),
    (6, 7),
    (7, 8),
    (7, 26),
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
    (24, 25),
)
STRUCTURED_RHO_SCALE = F(11, 500)
STRUCTURED_STOP_BETA = F(9, 20)

# One chord addition and two deletions retime the structured graph enough to
# cross beta=0.46 while retaining a connected 46-edge graph.
NEAR_HALF_EDGES = tuple(
    sorted((set(STRUCTURED_EDGES) - {(16, 20), (21, 22)}) | {(3, 8)})
)
NEAR_HALF_RHO_SCALE = F(109, 5000)
NEAR_HALF_STOP_BETA = F(23, 50)
NEAR_HALF_047_RHO_SCALE = F(21509, 1000000)
NEAR_HALF_047_STOP_BETA = F(47, 100)

BETA_0473_EDGES = (
    (0, 1),
    (0, 12),
    (1, 2),
    (1, 3),
    (1, 6),
    (1, 11),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 8),
    (2, 10),
    (2, 11),
    (2, 24),
    (3, 4),
    (3, 5),
    (3, 8),
    (4, 5),
    (4, 6),
    (4, 9),
    (4, 10),
    (5, 6),
    (5, 7),
    (5, 9),
    (6, 7),
    (7, 8),
    (7, 26),
    (8, 9),
    (8, 10),
    (9, 10),
    (10, 11),
    (12, 13),
    (13, 14),
    (13, 17),
    (13, 18),
    (14, 16),
    (14, 17),
    (15, 17),
    (15, 20),
    (15, 21),
    (16, 17),
    (17, 18),
    (18, 19),
    (18, 20),
    (18, 22),
    (18, 23),
    (19, 20),
    (20, 21),
    (20, 23),
    (22, 23),
    (24, 25),
)
BETA_0473_RHO_SCALE = F(393, 20000)
BETA_0473_STOP_BETA = F(473, 1000)

BETA_0477_EDGES = (
    (0, 1),
    (0, 12),
    (1, 2),
    (1, 3),
    (1, 6),
    (1, 11),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 8),
    (2, 10),
    (2, 11),
    (2, 24),
    (3, 4),
    (3, 5),
    (3, 8),
    (3, 11),
    (4, 5),
    (4, 6),
    (4, 8),
    (4, 10),
    (5, 6),
    (5, 7),
    (5, 9),
    (6, 7),
    (7, 8),
    (7, 10),
    (7, 26),
    (8, 9),
    (8, 10),
    (9, 10),
    (10, 11),
    (12, 13),
    (13, 14),
    (13, 16),
    (13, 17),
    (13, 18),
    (14, 16),
    (14, 17),
    (15, 16),
    (15, 17),
    (15, 20),
    (16, 17),
    (17, 18),
    (18, 19),
    (18, 22),
    (18, 23),
    (19, 20),
    (19, 21),
    (20, 21),
    (20, 23),
    (21, 22),
    (22, 23),
    (24, 25),
)
BETA_0477_RHO_SCALE = F(187, 10000)
BETA_0477_STOP_BETA = F(477, 1000)

# One dormant-boundary edge retimes the same two-clock relay.  Vertex 21 is
# still outside the certified face at the failing phase start.
BETA_0478_EDGES = tuple(sorted(set(BETA_0477_EDGES) | {(18, 21)}))
BETA_0478_RHO_SCALE = BETA_0477_RHO_SCALE
BETA_0478_STOP_BETA = BETA_0477_STOP_BETA


def chronology_cell(result: dict[str, object]) -> tuple[F, int, int, F, int, int]:
    """Independently reconstruct the exact beta cell from product decisions."""
    stopped: list[tuple[F, int, int]] = []
    continued: list[tuple[F, int, int]] = []
    for phase in result["phases"]:
        for product in phase["products"]:
            stop = product.get("stop")
            if stop is None:
                continue
            entry = (stop["inner_width_over_old_width"], phase["phase"], product["product"])
            (stopped if stop["decision"] else continued).append(entry)
    lower, lower_phase, lower_product = max(stopped)
    upper, upper_phase, upper_product = min(continued)
    assert result["same_chronology_stop_beta_interval"] == {
        "lower": lower,
        "lower_inclusive": True,
        "upper": upper,
        "upper_inclusive": False,
    }
    return lower, lower_phase, lower_product, upper, upper_phase, upper_product


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
    assert result["total_products"] == 23
    witness = result["first_negative_active_input_residual"]
    assert witness["phase"] == 18
    assert witness["product"] == 7
    assert witness["vertex"] == 16
    assert witness["input_batch"] == []
    assert witness["face"] == list(range(19))
    assert witness["value"] < 0

    cell_lower, lower_phase, lower_product, cell_upper, upper_phase, upper_product = (
        chronology_cell(result)
    )
    assert cell_lower <= STOP_BETA < cell_upper
    assert (lower_phase, lower_product) == (17, 1)
    assert (upper_phase, upper_product) == (18, 6)
    assert witness["preceding_inner_width_over_old_width"] == cell_upper
    reported_cell = result["same_chronology_stop_beta_interval"]

    middle_result = trace_retained_prox(
        neighbors,
        source=source,
        root=ROOT,
        rho_scale=RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=MIDDLE_STOP_BETA,
    )
    assert middle_result["status"] == "counterexample"
    assert middle_result["total_products"] == 25
    middle_witness = middle_result["first_negative_active_input_residual"]
    assert middle_witness["phase"] == 18
    assert middle_witness["product"] == 8
    assert middle_witness["vertex"] == 15
    assert middle_witness["input_batch"] == []
    assert middle_witness["face"] == list(range(19))
    assert middle_witness["value"] < 0
    (
        middle_lower,
        middle_lower_phase,
        middle_lower_product,
        middle_upper,
        middle_upper_phase,
        middle_upper_product,
    ) = chronology_cell(middle_result)
    middle_reported_cell = middle_result["same_chronology_stop_beta_interval"]
    assert (middle_lower_phase, middle_lower_product) == (17, 2)
    assert (middle_upper_phase, middle_upper_product) == (17, 1)
    assert middle_lower <= MIDDLE_STOP_BETA < middle_upper
    assert middle_upper == cell_lower
    middle_degree_ratio = middle_witness["value"] / middle_witness["phase_old_width"]

    bridge_neighbors, bridge_source = build_graph(
        {"vertices": VERTICES, "edges": list(BRIDGE_EDGES), "source": 0},
        None,
    )
    bridge_result = trace_retained_prox(
        bridge_neighbors,
        source=bridge_source,
        root=ROOT,
        rho_scale=BRIDGE_RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=BRIDGE_STOP_BETA,
    )
    assert bridge_result["status"] == "counterexample"
    assert bridge_result["total_products"] == 23
    bridge_witness = bridge_result["first_negative_active_input_residual"]
    assert (bridge_witness["phase"], bridge_witness["product"]) == (18, 7)
    assert bridge_witness["vertex"] == 16
    assert bridge_witness["input_batch"] == []
    assert bridge_witness["value"] < 0
    bridge_cell = chronology_cell(bridge_result)
    assert bridge_cell[0] <= BRIDGE_STOP_BETA < bridge_cell[3]
    assert bridge_cell[0] < F(415111, 1000000)
    assert bridge_cell[3] > middle_lower

    dense_neighbors, dense_source = build_graph(
        {"vertices": VERTICES, "edges": list(DENSE_EDGES), "source": 0},
        None,
    )
    dense_result = trace_retained_prox(
        dense_neighbors,
        source=dense_source,
        root=ROOT,
        rho_scale=DENSE_RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=DENSE_STOP_BETA,
    )
    assert dense_result["status"] == "counterexample"
    assert dense_result["total_products"] == 24
    dense_witness = dense_result["first_negative_active_input_residual"]
    assert (dense_witness["phase"], dense_witness["product"]) == (18, 8)
    assert dense_witness["vertex"] == 14
    assert dense_witness["input_batch"] == []
    assert dense_witness["value"] < 0
    dense_cell = chronology_cell(dense_result)
    assert dense_cell[0] <= DENSE_STOP_BETA < dense_cell[3]
    assert dense_cell[0] < bridge_cell[3]
    assert dense_cell[3] > F(4533, 10000)

    structured_neighbors, structured_source = build_graph(
        {
            "vertices": STRUCTURED_VERTICES,
            "edges": list(STRUCTURED_EDGES),
            "source": 0,
        },
        None,
    )
    structured_result = trace_retained_prox(
        structured_neighbors,
        source=structured_source,
        root=ROOT,
        rho_scale=STRUCTURED_RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=STRUCTURED_STOP_BETA,
    )
    assert structured_result["status"] == "counterexample"
    assert structured_result["total_products"] == 25
    structured_witness = structured_result["first_negative_active_input_residual"]
    assert (structured_witness["phase"], structured_witness["product"]) == (19, 8)
    assert structured_witness["vertex"] == 16
    assert structured_witness["input_batch"] == []
    assert structured_witness["value"] < 0
    structured_cell = chronology_cell(structured_result)
    assert structured_cell[0] <= STRUCTURED_STOP_BETA < structured_cell[3]
    assert structured_cell[0] < dense_cell[3]
    assert structured_cell[3] > F(4589, 10000)

    near_half_neighbors, near_half_source = build_graph(
        {
            "vertices": STRUCTURED_VERTICES,
            "edges": list(NEAR_HALF_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(NEAR_HALF_EDGES) == 46
    near_half_result = trace_retained_prox(
        near_half_neighbors,
        source=near_half_source,
        root=ROOT,
        rho_scale=NEAR_HALF_RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=NEAR_HALF_STOP_BETA,
    )
    assert near_half_result["status"] == "counterexample"
    assert near_half_result["total_products"] == 27
    near_half_witness = near_half_result["first_negative_active_input_residual"]
    assert (near_half_witness["phase"], near_half_witness["product"]) == (22, 7)
    assert near_half_witness["vertex"] == 16
    assert near_half_witness["input_batch"] == []
    assert near_half_witness["value"] < 0
    near_half_cell = chronology_cell(near_half_result)
    assert near_half_cell[0] <= NEAR_HALF_STOP_BETA < near_half_cell[3]
    assert near_half_cell[0] < structured_cell[3]
    assert near_half_cell[3] > F(4661, 10000)

    near_half_047_result = trace_retained_prox(
        near_half_neighbors,
        source=near_half_source,
        root=ROOT,
        rho_scale=NEAR_HALF_047_RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=NEAR_HALF_047_STOP_BETA,
    )
    assert near_half_047_result["status"] == "counterexample"
    assert near_half_047_result["total_products"] == 26
    near_half_047_witness = near_half_047_result[
        "first_negative_active_input_residual"
    ]
    assert (near_half_047_witness["phase"], near_half_047_witness["product"]) == (
        21,
        7,
    )
    assert near_half_047_witness["vertex"] == 16
    assert near_half_047_witness["input_batch"] == []
    assert near_half_047_witness["value"] < 0
    near_half_047_cell = chronology_cell(near_half_047_result)
    assert near_half_047_cell[0] <= NEAR_HALF_047_STOP_BETA < near_half_047_cell[3]
    assert near_half_047_cell[0] < near_half_cell[3]
    assert near_half_047_cell[3] > F(4703, 10000)

    beta_0473_neighbors, beta_0473_source = build_graph(
        {
            "vertices": STRUCTURED_VERTICES,
            "edges": list(BETA_0473_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_0473_EDGES) == 50
    beta_0473_result = trace_retained_prox(
        beta_0473_neighbors,
        source=beta_0473_source,
        root=ROOT,
        rho_scale=BETA_0473_RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=BETA_0473_STOP_BETA,
    )
    assert beta_0473_result["status"] == "counterexample"
    assert beta_0473_result["total_products"] == 27
    beta_0473_witness = beta_0473_result["first_negative_active_input_residual"]
    assert (beta_0473_witness["phase"], beta_0473_witness["product"]) == (21, 8)
    assert beta_0473_witness["vertex"] == 16
    assert beta_0473_witness["input_batch"] == []
    assert beta_0473_witness["value"] < 0
    beta_0473_cell = chronology_cell(beta_0473_result)
    assert beta_0473_cell[0] <= BETA_0473_STOP_BETA < beta_0473_cell[3]
    assert beta_0473_cell[0] < near_half_047_cell[3]
    assert beta_0473_cell[3] > F(4735, 10000)

    beta_0477_neighbors, beta_0477_source = build_graph(
        {
            "vertices": STRUCTURED_VERTICES,
            "edges": list(BETA_0477_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_0477_EDGES) == 54
    beta_0477_result = trace_retained_prox(
        beta_0477_neighbors,
        source=beta_0477_source,
        root=ROOT,
        rho_scale=BETA_0477_RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=BETA_0477_STOP_BETA,
    )
    assert beta_0477_result["status"] == "counterexample"
    assert beta_0477_result["total_products"] == 31
    beta_0477_witness = beta_0477_result["first_negative_active_input_residual"]
    assert (beta_0477_witness["phase"], beta_0477_witness["product"]) == (25, 8)
    assert beta_0477_witness["vertex"] == 15
    assert beta_0477_witness["input_batch"] == []
    assert beta_0477_witness["value"] < 0
    beta_0477_cell = chronology_cell(beta_0477_result)
    assert beta_0477_cell[0] <= BETA_0477_STOP_BETA < beta_0477_cell[3]
    assert beta_0477_cell[0] < beta_0473_cell[3]
    assert beta_0477_cell[3] > F(477, 1000)

    beta_0478_neighbors, beta_0478_source = build_graph(
        {
            "vertices": STRUCTURED_VERTICES,
            "edges": list(BETA_0478_EDGES),
            "source": 0,
        },
        None,
    )
    assert len(BETA_0478_EDGES) == 55
    beta_0478_result = trace_retained_prox(
        beta_0478_neighbors,
        source=beta_0478_source,
        root=ROOT,
        rho_scale=BETA_0478_RHO_SCALE,
        relative_width=RELATIVE_WIDTH,
        maximum_phase_products=100,
        maximum_phases=50,
        chronology="one-push-maximal",
        stop_beta=BETA_0478_STOP_BETA,
    )
    assert beta_0478_result["status"] == "counterexample"
    assert beta_0478_result["total_products"] == 31
    beta_0478_witness = beta_0478_result["first_negative_active_input_residual"]
    assert (beta_0478_witness["phase"], beta_0478_witness["product"]) == (25, 8)
    assert beta_0478_witness["vertex"] == 15
    assert beta_0478_witness["input_batch"] == []
    assert beta_0478_witness["value"] < 0
    beta_0478_cell = chronology_cell(beta_0478_result)
    assert beta_0478_cell[0] <= BETA_0478_STOP_BETA < beta_0478_cell[3]
    assert beta_0478_cell[0] < beta_0477_cell[3]
    assert beta_0478_cell[3] > F(4784, 10000)

    degree_ratio = witness["value"] / witness["phase_old_width"]
    alpha = ROOT * ROOT / (2 - ROOT * ROOT)
    rho = RHO_SCALE / len(neighbors[0])
    print(
        json.dumps(
            serialize(
                {
                    "status": "counterexample",
                    "scope": (
                        "canonical zero-start one-push-maximal chronology on "
                        "an exact half-open interval of stopping constants"
                    ),
                    "vertices": VERTICES,
                    "edges": EDGES,
                    "source": source,
                    "root": ROOT,
                    "alpha": alpha,
                    "rho_scale": RHO_SCALE,
                    "rho": rho,
                    "relative_width": RELATIVE_WIDTH,
                    "chosen_stop_beta": STOP_BETA,
                    "same_chronology_stop_beta_interval": reported_cell,
                    "chronology_cell_attainment": {
                        "lower_attained_at": [lower_phase, lower_product],
                        "upper_attained_at": [upper_phase, upper_product],
                    },
                    "adjacent_middle_counterexample": {
                        "chosen_stop_beta": MIDDLE_STOP_BETA,
                        "same_chronology_stop_beta_interval": middle_reported_cell,
                        "chronology_cell_attainment": {
                            "lower_attained_at": [
                                middle_lower_phase,
                                middle_lower_product,
                            ],
                            "upper_attained_at": [
                                middle_upper_phase,
                                middle_upper_product,
                            ],
                        },
                        "completed_products_before_failure": middle_result["total_products"],
                        "failure_phase_one_based": middle_witness["phase"],
                        "failure_product_in_phase_one_based": middle_witness["product"],
                        "failure_vertex": middle_witness["vertex"],
                        "degree_residual_over_phase_width": middle_degree_ratio,
                    },
                    "bridge_counterexample": {
                        "edges": BRIDGE_EDGES,
                        "rho_scale": BRIDGE_RHO_SCALE,
                        "rho": BRIDGE_RHO_SCALE / len(bridge_neighbors[0]),
                        "chosen_stop_beta": BRIDGE_STOP_BETA,
                        "same_chronology_stop_beta_interval": bridge_result[
                            "same_chronology_stop_beta_interval"
                        ],
                        "completed_products_before_failure": bridge_result["total_products"],
                        "failure_phase_one_based": bridge_witness["phase"],
                        "failure_product_in_phase_one_based": bridge_witness["product"],
                        "failure_vertex": bridge_witness["vertex"],
                        "degree_residual_over_phase_width": bridge_witness["value"]
                        / bridge_witness["phase_old_width"],
                    },
                    "beta_045_counterexample": {
                        "edges": DENSE_EDGES,
                        "rho_scale": DENSE_RHO_SCALE,
                        "rho": DENSE_RHO_SCALE / len(dense_neighbors[0]),
                        "chosen_stop_beta": DENSE_STOP_BETA,
                        "same_chronology_stop_beta_interval": dense_result[
                            "same_chronology_stop_beta_interval"
                        ],
                        "completed_products_before_failure": dense_result["total_products"],
                        "failure_phase_one_based": dense_witness["phase"],
                        "failure_product_in_phase_one_based": dense_witness["product"],
                        "failure_vertex": dense_witness["vertex"],
                        "degree_residual_over_phase_width": dense_witness["value"]
                        / dense_witness["phase_old_width"],
                    },
                    "structured_beta_045_counterexample": {
                        "vertices": STRUCTURED_VERTICES,
                        "edges": STRUCTURED_EDGES,
                        "rho_scale": STRUCTURED_RHO_SCALE,
                        "rho": STRUCTURED_RHO_SCALE
                        / len(structured_neighbors[structured_source]),
                        "chosen_stop_beta": STRUCTURED_STOP_BETA,
                        "same_chronology_stop_beta_interval": structured_result[
                            "same_chronology_stop_beta_interval"
                        ],
                        "completed_products_before_failure": structured_result[
                            "total_products"
                        ],
                        "failure_phase_one_based": structured_witness["phase"],
                        "failure_product_in_phase_one_based": structured_witness[
                            "product"
                        ],
                        "failure_vertex": structured_witness["vertex"],
                        "degree_residual_over_phase_width": structured_witness["value"]
                        / structured_witness["phase_old_width"],
                    },
                    "near_half_counterexample": {
                        "vertices": STRUCTURED_VERTICES,
                        "edges": NEAR_HALF_EDGES,
                        "rho_scale": NEAR_HALF_RHO_SCALE,
                        "rho": NEAR_HALF_RHO_SCALE
                        / len(near_half_neighbors[near_half_source]),
                        "chosen_stop_beta": NEAR_HALF_STOP_BETA,
                        "same_chronology_stop_beta_interval": near_half_result[
                            "same_chronology_stop_beta_interval"
                        ],
                        "completed_products_before_failure": near_half_result[
                            "total_products"
                        ],
                        "failure_phase_one_based": near_half_witness["phase"],
                        "failure_product_in_phase_one_based": near_half_witness[
                            "product"
                        ],
                        "failure_vertex": near_half_witness["vertex"],
                        "degree_residual_over_phase_width": near_half_witness["value"]
                        / near_half_witness["phase_old_width"],
                        "preceding_inner_width_over_phase_width": near_half_witness[
                            "preceding_inner_width_over_old_width"
                        ],
                    },
                    "beta_047_counterexample": {
                        "vertices": STRUCTURED_VERTICES,
                        "edges": NEAR_HALF_EDGES,
                        "rho_scale": NEAR_HALF_047_RHO_SCALE,
                        "rho": NEAR_HALF_047_RHO_SCALE
                        / len(near_half_neighbors[near_half_source]),
                        "chosen_stop_beta": NEAR_HALF_047_STOP_BETA,
                        "same_chronology_stop_beta_interval": near_half_047_result[
                            "same_chronology_stop_beta_interval"
                        ],
                        "completed_products_before_failure": near_half_047_result[
                            "total_products"
                        ],
                        "failure_phase_one_based": near_half_047_witness["phase"],
                        "failure_product_in_phase_one_based": near_half_047_witness[
                            "product"
                        ],
                        "failure_vertex": near_half_047_witness["vertex"],
                        "degree_residual_over_phase_width": near_half_047_witness[
                            "value"
                        ]
                        / near_half_047_witness["phase_old_width"],
                        "preceding_inner_width_over_phase_width": near_half_047_witness[
                            "preceding_inner_width_over_old_width"
                        ],
                    },
                    "beta_0473_counterexample": {
                        "vertices": STRUCTURED_VERTICES,
                        "edges": BETA_0473_EDGES,
                        "rho_scale": BETA_0473_RHO_SCALE,
                        "rho": BETA_0473_RHO_SCALE
                        / len(beta_0473_neighbors[beta_0473_source]),
                        "chosen_stop_beta": BETA_0473_STOP_BETA,
                        "same_chronology_stop_beta_interval": beta_0473_result[
                            "same_chronology_stop_beta_interval"
                        ],
                        "completed_products_before_failure": beta_0473_result[
                            "total_products"
                        ],
                        "failure_phase_one_based": beta_0473_witness["phase"],
                        "failure_product_in_phase_one_based": beta_0473_witness[
                            "product"
                        ],
                        "failure_vertex": beta_0473_witness["vertex"],
                        "degree_residual_over_phase_width": beta_0473_witness["value"]
                        / beta_0473_witness["phase_old_width"],
                        "preceding_inner_width_over_phase_width": beta_0473_witness[
                            "preceding_inner_width_over_old_width"
                        ],
                    },
                    "beta_0477_counterexample": {
                        "vertices": STRUCTURED_VERTICES,
                        "edges": BETA_0477_EDGES,
                        "rho_scale": BETA_0477_RHO_SCALE,
                        "rho": BETA_0477_RHO_SCALE
                        / len(beta_0477_neighbors[beta_0477_source]),
                        "chosen_stop_beta": BETA_0477_STOP_BETA,
                        "same_chronology_stop_beta_interval": beta_0477_result[
                            "same_chronology_stop_beta_interval"
                        ],
                        "completed_products_before_failure": beta_0477_result[
                            "total_products"
                        ],
                        "failure_phase_one_based": beta_0477_witness["phase"],
                        "failure_product_in_phase_one_based": beta_0477_witness[
                            "product"
                        ],
                        "failure_vertex": beta_0477_witness["vertex"],
                        "input_batch_at_failure": beta_0477_witness["input_batch"],
                        "failure_face": beta_0477_witness["face"],
                        "degree_residual_over_phase_width": beta_0477_witness[
                            "value"
                        ]
                        / beta_0477_witness["phase_old_width"],
                        "preceding_inner_width_over_phase_width": beta_0477_witness[
                            "preceding_inner_width_over_old_width"
                        ],
                    },
                    "beta_0478_counterexample": {
                        "vertices": STRUCTURED_VERTICES,
                        "edges": BETA_0478_EDGES,
                        "rho_scale": BETA_0478_RHO_SCALE,
                        "rho": BETA_0478_RHO_SCALE
                        / len(beta_0478_neighbors[beta_0478_source]),
                        "chosen_stop_beta": BETA_0478_STOP_BETA,
                        "same_chronology_stop_beta_interval": beta_0478_result[
                            "same_chronology_stop_beta_interval"
                        ],
                        "completed_products_before_failure": beta_0478_result[
                            "total_products"
                        ],
                        "failure_phase_one_based": beta_0478_witness["phase"],
                        "failure_product_in_phase_one_based": beta_0478_witness[
                            "product"
                        ],
                        "failure_vertex": beta_0478_witness["vertex"],
                        "input_batch_at_failure": beta_0478_witness["input_batch"],
                        "failure_face": beta_0478_witness["face"],
                        "degree_residual_over_phase_width": beta_0478_witness[
                            "value"
                        ]
                        / beta_0478_witness["phase_old_width"],
                        "preceding_inner_width_over_phase_width": beta_0478_witness[
                            "preceding_inner_width_over_old_width"
                        ],
                    },
                    "completed_products_before_failure": result["total_products"],
                    "failure_phase_one_based": witness["phase"],
                    "failure_product_in_phase_one_based": witness["product"],
                    "failure_vertex": witness["vertex"],
                    "input_batch_at_failure": witness["input_batch"],
                    "failure_face": witness["face"],
                    "degree_coordinate_input_residual": witness["value"],
                    "degree_residual_over_phase_width": degree_ratio,
                    "preceding_inner_width_over_phase_width": witness[
                        "preceding_inner_width_over_old_width"
                    ],
                    "claim": (
                        "each reported strict chronology is a counterexample "
                        "throughout its exact half-open beta cell"
                    ),
                }
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
