#!/usr/bin/env python3
"""Fraction-exact atlas covering a continuous interval of beta stops.

Each representative trace is a canonical point-source, zero-start,
one-push-maximal execution.  The general tracer returns the exact half-open
interval of stopping constants which preserve all of that trace's earlier
stop/nonstop decisions.  This wrapper verifies that every trace fails and
that the cells overlap from beta=0 to the reported right endpoint.
"""

from __future__ import annotations

import json
from fractions import Fraction as F

from retained_prox_input_cone_trace_exact import build_graph, serialize, trace_retained_prox
from stopped_masked_input_residual_beta_048_counterexample_exact import (
    BETA_048_EDGES,
    BETA_048_RHO_SCALE,
    BETA_048_STOP_BETA,
    BETA_048_VERTICES,
)
from stopped_masked_input_residual_beta_0482_retimed_exact import (
    BETA_0482_RETIMED_EDGES,
    BETA_0482_RETIMED_RHO_SCALE,
    BETA_0482_RETIMED_STOP_BETA,
    BETA_0482_RETIMED_VERTICES,
)
from stopped_masked_input_residual_beta_0484_counterexample_exact import (
    BETA_0484_EDGES,
    BETA_0484_RHO_SCALE,
    BETA_0484_ROOT,
    BETA_0484_STOP_BETA,
    BETA_0484_VERTICES,
)
from stopped_masked_input_residual_beta_04845_bridge_exact import (
    BETA_04845_BRIDGE_EDGES,
    BETA_04845_BRIDGE_RHO_SCALE,
    BETA_04845_BRIDGE_ROOT,
    BETA_04845_BRIDGE_STOP_BETA,
    BETA_04845_BRIDGE_VERTICES,
)
from stopped_masked_input_residual_beta_0486_relay_exact import (
    BETA_0486_RELAY_CASES,
    BETA_0486_RELAY_EDGES,
    BETA_0486_RELAY_VERTICES,
)
from stopped_masked_input_residual_beta_0486_clock_swap_exact import (
    BETA_0486_CLOCK_SWAP_EDGES,
    BETA_0486_CLOCK_SWAP_RHO_SCALE,
    BETA_0486_CLOCK_SWAP_ROOT,
    BETA_0486_CLOCK_SWAP_STOP_BETA,
    BETA_0486_CLOCK_SWAP_VERTICES,
)
from stopped_masked_input_residual_beta_04864_clock_rewire_exact import (
    BETA_04864_CLOCK_REWIRE_EDGES,
    BETA_04864_CLOCK_REWIRE_RHO_SCALE,
    BETA_04864_CLOCK_REWIRE_ROOT,
    BETA_04864_CLOCK_REWIRE_STOP_BETA,
    BETA_04864_CLOCK_REWIRE_VERTICES,
)
from stopped_masked_input_residual_beta_04865_branch_boundary_exact import (
    BETA_04865_BRANCH_BOUNDARY_EDGES,
    BETA_04865_BRANCH_BOUNDARY_RHO_SCALE,
    BETA_04865_BRANCH_BOUNDARY_ROOT,
    BETA_04865_BRANCH_BOUNDARY_STOP_BETA,
    BETA_04865_BRANCH_BOUNDARY_VERTICES,
)
from stopped_masked_input_residual_beta_04865_branch_boundary_retimed_exact import (
    BETA_04865_BRANCH_BOUNDARY_RETIMED_RHO_SCALE,
    BETA_04865_BRANCH_BOUNDARY_RETIMED_ROOT,
    BETA_04865_BRANCH_BOUNDARY_RETIMED_STOP_BETA,
)
from stopped_masked_input_residual_beta_048659_two_leaf_exact import (
    BETA_048659_TWO_LEAF_EDGES,
    BETA_048659_TWO_LEAF_RHO_SCALE,
    BETA_048659_TWO_LEAF_ROOT,
    BETA_048659_TWO_LEAF_STOP_BETA,
    BETA_048659_TWO_LEAF_VERTICES,
)
from stopped_masked_input_residual_beta_04877_four_leaf_exact import (
    BETA_04877_FOUR_LEAF_EDGES,
    BETA_04877_FOUR_LEAF_RHO_SCALE,
    BETA_04877_FOUR_LEAF_ROOT,
    BETA_04877_FOUR_LEAF_STOP_BETA,
    BETA_04877_FOUR_LEAF_VERTICES,
)
from stopped_masked_input_residual_beta_04881_six_leaf_exact import (
    BETA_04881_SIX_LEAF_EDGES,
    BETA_04881_SIX_LEAF_RHO_SCALE,
    BETA_04881_SIX_LEAF_ROOT,
    BETA_04881_SIX_LEAF_STOP_BETA,
    BETA_04881_SIX_LEAF_VERTICES,
)
from stopped_masked_input_residual_beta_04882_eight_leaf_exact import (
    BETA_04882_EIGHT_LEAF_EDGES,
    BETA_04882_EIGHT_LEAF_RELAY_CASES,
    BETA_04882_EIGHT_LEAF_ROOT,
    BETA_04882_EIGHT_LEAF_VERTICES,
)
from stopped_masked_input_residual_beta_04890_twelve_leaf_exact import (
    BETA_04890_TWELVE_LEAF_EDGES,
    BETA_04890_TWELVE_LEAF_RHO_SCALE,
    BETA_04890_TWELVE_LEAF_ROOT,
    BETA_04890_TWELVE_LEAF_STOP_BETA,
    BETA_04890_TWELVE_LEAF_VERTICES,
)
from stopped_masked_input_residual_beta_04891_fourteen_leaf_exact import (
    BETA_04891_FOURTEEN_LEAF_EDGES,
    BETA_04891_FOURTEEN_LEAF_RELAY_CASES,
    BETA_04891_FOURTEEN_LEAF_ROOT,
    BETA_04891_FOURTEEN_LEAF_VERTICES,
)
from stopped_masked_input_residual_beta_04892_sixteen_leaf_exact import (
    BETA_04892_SIXTEEN_LEAF_EDGES,
    BETA_04892_SIXTEEN_LEAF_RHO_SCALE,
    BETA_04892_SIXTEEN_LEAF_ROOT,
    BETA_04892_SIXTEEN_LEAF_STOP_BETA,
    BETA_04892_SIXTEEN_LEAF_VERTICES,
)
from stopped_masked_input_residual_beta_04894_eighteen_leaf_retimed_exact import (
    BETA_04894_EIGHTEEN_LEAF_RETIMED_RHO_SCALE,
    BETA_04894_EIGHTEEN_LEAF_RETIMED_ROOT,
    BETA_04894_EIGHTEEN_LEAF_RETIMED_STOP_BETA,
    BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_EDGES,
    BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_VERTICES,
)
from stopped_masked_input_residual_beta_04896_twenty_leaf_exact import (
    BETA_04896_TWENTY_LEAF_EDGES,
    BETA_04896_TWENTY_LEAF_RHO_SCALE,
    BETA_04896_TWENTY_LEAF_ROOT,
    BETA_04896_TWENTY_LEAF_STOP_BETA,
    BETA_04896_TWENTY_LEAF_VERTICES,
)
from stopped_masked_input_residual_beta_04898_twenty_two_leaf_equioscillation_exact import (
    BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_ROOT,
)
from stopped_masked_input_residual_beta_04898_twenty_two_leaf_zero_root_equioscillation_exact import (
    BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_EDGES,
    BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RHO_SCALE,
    BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_STOP_BETA,
    BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_VERTICES,
)
from stopped_masked_input_residual_high_beta_counterexample_exact import (
    BETA_0473_EDGES,
    BETA_0473_RHO_SCALE,
    BETA_0473_STOP_BETA,
    BETA_0477_EDGES,
    BETA_0477_RHO_SCALE,
    BETA_0477_STOP_BETA,
    BETA_0478_EDGES,
    BETA_0478_RHO_SCALE,
    BETA_0478_STOP_BETA,
    BRIDGE_EDGES,
    BRIDGE_RHO_SCALE,
    BRIDGE_STOP_BETA,
    DENSE_EDGES,
    DENSE_RHO_SCALE,
    DENSE_STOP_BETA,
    EDGES as HIGH_EDGES,
    NEAR_HALF_EDGES,
    NEAR_HALF_047_RHO_SCALE,
    NEAR_HALF_047_STOP_BETA,
    NEAR_HALF_RHO_SCALE,
    NEAR_HALF_STOP_BETA,
    RELATIVE_WIDTH,
    RHO_SCALE as HIGH_RHO_SCALE,
    ROOT,
    STRUCTURED_EDGES,
    STRUCTURED_RHO_SCALE,
    STRUCTURED_STOP_BETA,
    STRUCTURED_VERTICES,
    VERTICES,
)
from stopped_masked_input_residual_one_third_counterexample_exact import (
    EDGES as BASE_EDGES,
    RHO_SCALE as BASE_RHO_SCALE,
)
from stopped_masked_input_residual_triple_clock_counterexample_exact import (
    TRIPLE_CLOCK_EDGES,
    TRIPLE_CLOCK_RHO_SCALE,
    TRIPLE_CLOCK_STOP_BETA,
    TRIPLE_CLOCK_VERTICES,
)


Case = tuple[str, int, tuple[tuple[int, int], ...], F, F, F]


CASES: tuple[Case, ...] = (
    ("anchor-first-phase", VERTICES, HIGH_EDGES, ROOT, HIGH_RHO_SCALE, F(1, 100)),
    ("anchor-low", VERTICES, HIGH_EDGES, ROOT, HIGH_RHO_SCALE, F(9, 50)),
    ("base-1/5", VERTICES, BASE_EDGES, ROOT, BASE_RHO_SCALE, F(1, 5)),
    ("base-6/25", VERTICES, BASE_EDGES, ROOT, BASE_RHO_SCALE, F(6, 25)),
    ("anchor-6/25", VERTICES, HIGH_EDGES, ROOT, HIGH_RHO_SCALE, F(6, 25)),
    ("base-7/25", VERTICES, BASE_EDGES, ROOT, BASE_RHO_SCALE, F(7, 25)),
    ("anchor-31/100", VERTICES, HIGH_EDGES, ROOT, HIGH_RHO_SCALE, F(31, 100)),
    ("base-one-third", VERTICES, BASE_EDGES, ROOT, BASE_RHO_SCALE, F(1, 3)),
    ("anchor-3/8", VERTICES, HIGH_EDGES, ROOT, HIGH_RHO_SCALE, F(3, 8)),
    ("anchor-77/200", VERTICES, HIGH_EDGES, ROOT, HIGH_RHO_SCALE, F(77, 200)),
    ("base-two-fifths", VERTICES, BASE_EDGES, ROOT, BASE_RHO_SCALE, F(2, 5)),
    ("bridge", VERTICES, BRIDGE_EDGES, ROOT, BRIDGE_RHO_SCALE, BRIDGE_STOP_BETA),
    ("dense", VERTICES, DENSE_EDGES, ROOT, DENSE_RHO_SCALE, DENSE_STOP_BETA),
    (
        "structured",
        STRUCTURED_VERTICES,
        STRUCTURED_EDGES,
        ROOT,
        STRUCTURED_RHO_SCALE,
        STRUCTURED_STOP_BETA,
    ),
    (
        "triple-clock",
        TRIPLE_CLOCK_VERTICES,
        TRIPLE_CLOCK_EDGES,
        ROOT,
        TRIPLE_CLOCK_RHO_SCALE,
        TRIPLE_CLOCK_STOP_BETA,
    ),
    (
        "near-half-retimed",
        STRUCTURED_VERTICES,
        NEAR_HALF_EDGES,
        ROOT,
        NEAR_HALF_RHO_SCALE,
        NEAR_HALF_STOP_BETA,
    ),
    (
        "near-half-rho-0.47",
        STRUCTURED_VERTICES,
        NEAR_HALF_EDGES,
        ROOT,
        NEAR_HALF_047_RHO_SCALE,
        NEAR_HALF_047_STOP_BETA,
    ),
    (
        "beta-0.473",
        STRUCTURED_VERTICES,
        BETA_0473_EDGES,
        ROOT,
        BETA_0473_RHO_SCALE,
        BETA_0473_STOP_BETA,
    ),
    (
        "beta-0.477",
        STRUCTURED_VERTICES,
        BETA_0477_EDGES,
        ROOT,
        BETA_0477_RHO_SCALE,
        BETA_0477_STOP_BETA,
    ),
    (
        "beta-0.478-dormant-edge",
        STRUCTURED_VERTICES,
        BETA_0478_EDGES,
        ROOT,
        BETA_0478_RHO_SCALE,
        BETA_0478_STOP_BETA,
    ),
    (
        "beta-0.48",
        BETA_048_VERTICES,
        BETA_048_EDGES,
        ROOT,
        BETA_048_RHO_SCALE,
        BETA_048_STOP_BETA,
    ),
    (
        "beta-0.482-retimed",
        BETA_0482_RETIMED_VERTICES,
        BETA_0482_RETIMED_EDGES,
        ROOT,
        BETA_0482_RETIMED_RHO_SCALE,
        BETA_0482_RETIMED_STOP_BETA,
    ),
    (
        "beta-0.484-small-root",
        BETA_0484_VERTICES,
        BETA_0484_EDGES,
        BETA_0484_ROOT,
        BETA_0484_RHO_SCALE,
        BETA_0484_STOP_BETA,
    ),
    (
        "beta-0.4845-bridge",
        BETA_04845_BRIDGE_VERTICES,
        BETA_04845_BRIDGE_EDGES,
        BETA_04845_BRIDGE_ROOT,
        BETA_04845_BRIDGE_RHO_SCALE,
        BETA_04845_BRIDGE_STOP_BETA,
    ),
    *(
        (name, BETA_0486_RELAY_VERTICES, BETA_0486_RELAY_EDGES, root, rho, beta)
        for name, root, rho, beta, _failure_vertex in BETA_0486_RELAY_CASES
    ),
    (
        "beta-0.486-clock-swap",
        BETA_0486_CLOCK_SWAP_VERTICES,
        BETA_0486_CLOCK_SWAP_EDGES,
        BETA_0486_CLOCK_SWAP_ROOT,
        BETA_0486_CLOCK_SWAP_RHO_SCALE,
        BETA_0486_CLOCK_SWAP_STOP_BETA,
    ),
    (
        "beta-0.4864-clock-rewire",
        BETA_04864_CLOCK_REWIRE_VERTICES,
        BETA_04864_CLOCK_REWIRE_EDGES,
        BETA_04864_CLOCK_REWIRE_ROOT,
        BETA_04864_CLOCK_REWIRE_RHO_SCALE,
        BETA_04864_CLOCK_REWIRE_STOP_BETA,
    ),
    (
        "beta-0.4865-branch-boundary",
        BETA_04865_BRANCH_BOUNDARY_VERTICES,
        BETA_04865_BRANCH_BOUNDARY_EDGES,
        BETA_04865_BRANCH_BOUNDARY_ROOT,
        BETA_04865_BRANCH_BOUNDARY_RHO_SCALE,
        BETA_04865_BRANCH_BOUNDARY_STOP_BETA,
    ),
    (
        "beta-0.4865-boundary-retimed",
        BETA_04865_BRANCH_BOUNDARY_VERTICES,
        BETA_04865_BRANCH_BOUNDARY_EDGES,
        BETA_04865_BRANCH_BOUNDARY_RETIMED_ROOT,
        BETA_04865_BRANCH_BOUNDARY_RETIMED_RHO_SCALE,
        BETA_04865_BRANCH_BOUNDARY_RETIMED_STOP_BETA,
    ),
    (
        "beta-0.487-two-leaf",
        BETA_048659_TWO_LEAF_VERTICES,
        BETA_048659_TWO_LEAF_EDGES,
        BETA_048659_TWO_LEAF_ROOT,
        BETA_048659_TWO_LEAF_RHO_SCALE,
        BETA_048659_TWO_LEAF_STOP_BETA,
    ),
    (
        "beta-0.4875-four-leaf",
        BETA_04877_FOUR_LEAF_VERTICES,
        BETA_04877_FOUR_LEAF_EDGES,
        BETA_04877_FOUR_LEAF_ROOT,
        BETA_04877_FOUR_LEAF_RHO_SCALE,
        BETA_04877_FOUR_LEAF_STOP_BETA,
    ),
    (
        "beta-0.4881-six-leaf",
        BETA_04881_SIX_LEAF_VERTICES,
        BETA_04881_SIX_LEAF_EDGES,
        BETA_04881_SIX_LEAF_ROOT,
        BETA_04881_SIX_LEAF_RHO_SCALE,
        BETA_04881_SIX_LEAF_STOP_BETA,
    ),
    *(
        (
            f"beta-0.488-eight-leaf-{case['name']}",
            BETA_04882_EIGHT_LEAF_VERTICES,
            BETA_04882_EIGHT_LEAF_EDGES,
            BETA_04882_EIGHT_LEAF_ROOT,
            case["rho_scale"],
            case["stop_beta"],
        )
        for case in BETA_04882_EIGHT_LEAF_RELAY_CASES
    ),
    (
        "beta-0.4889-twelve-leaf",
        BETA_04890_TWELVE_LEAF_VERTICES,
        BETA_04890_TWELVE_LEAF_EDGES,
        BETA_04890_TWELVE_LEAF_ROOT,
        BETA_04890_TWELVE_LEAF_RHO_SCALE,
        BETA_04890_TWELVE_LEAF_STOP_BETA,
    ),
    *(
        (
            f"beta-0.489-fourteen-leaf-{case['name']}",
            BETA_04891_FOURTEEN_LEAF_VERTICES,
            BETA_04891_FOURTEEN_LEAF_EDGES,
            BETA_04891_FOURTEEN_LEAF_ROOT,
            case["rho_scale"],
            case["stop_beta"],
        )
        for case in BETA_04891_FOURTEEN_LEAF_RELAY_CASES
    ),
    (
        "beta-0.48905-sixteen-leaf",
        BETA_04892_SIXTEEN_LEAF_VERTICES,
        BETA_04892_SIXTEEN_LEAF_EDGES,
        BETA_04892_SIXTEEN_LEAF_ROOT,
        BETA_04892_SIXTEEN_LEAF_RHO_SCALE,
        BETA_04892_SIXTEEN_LEAF_STOP_BETA,
    ),
    (
        "beta-0.48935-eighteen-leaf-retimed",
        BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_VERTICES,
        BETA_04894_EIGHTEEN_LEAF_ZERO_ROOT_EDGES,
        BETA_04894_EIGHTEEN_LEAF_RETIMED_ROOT,
        BETA_04894_EIGHTEEN_LEAF_RETIMED_RHO_SCALE,
        BETA_04894_EIGHTEEN_LEAF_RETIMED_STOP_BETA,
    ),
    (
        "beta-0.48935-twenty-leaf",
        BETA_04896_TWENTY_LEAF_VERTICES,
        BETA_04896_TWENTY_LEAF_EDGES,
        BETA_04896_TWENTY_LEAF_ROOT,
        BETA_04896_TWENTY_LEAF_RHO_SCALE,
        BETA_04896_TWENTY_LEAF_STOP_BETA,
    ),
    (
        "beta-0.48979-twenty-two-leaf-equioscillation",
        BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_VERTICES,
        BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_EDGES,
        BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_ROOT,
        BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_RHO_SCALE,
        BETA_04898_TWENTY_TWO_LEAF_EQUILIBRATED_STOP_BETA,
    ),
)


def main() -> None:
    assert len(CASES) == 44
    assert CASES[-1][0] == "beta-0.48979-twenty-two-leaf-equioscillation"
    cells: list[dict[str, object]] = []
    covered_upper = F(0)
    for name, vertices, edges, root, rho_scale, stop_beta in CASES:
        neighbors, source = build_graph(
            {"vertices": vertices, "edges": list(edges), "source": 0},
            None,
        )
        result = trace_retained_prox(
            neighbors,
            source=source,
            root=root,
            rho_scale=rho_scale,
            relative_width=RELATIVE_WIDTH,
            maximum_phase_products=100,
            maximum_phases=50,
            chronology="one-push-maximal",
            stop_beta=stop_beta,
        )
        assert result["status"] == "counterexample"
        witness = result["first_negative_active_input_residual"]
        assert witness["value"] < 0
        cell = result["same_chronology_stop_beta_interval"]
        lower = cell["lower"]
        upper = cell["upper"]
        assert lower <= stop_beta < upper
        assert lower <= covered_upper, (name, lower, covered_upper)
        covered_upper = max(covered_upper, upper)
        cells.append(
            {
                "name": name,
                "vertices": vertices,
                "edges": len(edges),
                "root": root,
                "rho_scale": rho_scale,
                "representative_beta": stop_beta,
                "cell": cell,
                "failure_phase": witness["phase"],
                "failure_product": witness["product"],
                "failure_vertex": witness["vertex"],
                "failure_residual_over_phase_width": (
                    witness["value"] / witness["phase_old_width"]
                ),
            }
        )

    assert cells[0]["cell"]["lower"] == 0
    result = {
        "status": "counterexample-cell-cover",
        "scope": (
            "every beta in the open interval (0, covered_upper) is refuted "
            "by at least one exact canonical zero-start chronology cell"
        ),
        "roots": sorted({case[3] for case in CASES}),
        "relative_width": RELATIVE_WIDTH,
        "covered_interval": {
            "lower": F(0),
            "lower_inclusive_in_beta_domain": False,
            "upper": covered_upper,
            "upper_inclusive": False,
        },
        "cells": cells,
    }
    print(json.dumps(serialize(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
