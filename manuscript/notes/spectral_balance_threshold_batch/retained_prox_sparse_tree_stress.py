#!/usr/bin/env python3
"""Sparse enhanced retained-prox stress on the 12,286-vertex overshoot tree.

The tree and its full canonical support certificate come from
``projected_green_overshoot_exact.py``.  This trace is floating-point
candidate evidence for the pushed lower/state comparisons, not a theorem.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np
from scipy.sparse import coo_matrix, eye

from projected_green_overshoot_exact import build_graph


def run(relative_width: float, maximum_phase_iterations: int) -> dict[str, object]:
    alpha = 1.0e-6
    rho = 1.0e-30
    n, edges, _, source, _ = build_graph()
    rows: list[int] = []
    columns: list[int] = []
    for left, right in edges:
        rows.extend((left, right))
        columns.extend((right, left))
    adjacency = coo_matrix(
        (np.ones(len(rows)), (rows, columns)), shape=(n, n)
    ).tocsr()
    degrees = np.asarray(adjacency.sum(axis=1)).ravel()
    sqrt_degrees = np.sqrt(degrees)
    normalized = adjacency.multiply(1.0 / sqrt_degrees[:, None]).multiply(
        1.0 / sqrt_degrees[None, :]
    )
    q_matrix = (1.0 + alpha) / 2.0 * eye(n, format="csr")
    q_matrix -= (1.0 - alpha) / 2.0 * normalized
    shifted_matrix = q_matrix + alpha * eye(n, format="csr")
    shifted_diagonal = (1.0 + 3.0 * alpha) / 2.0
    load = -alpha * rho * sqrt_degrees
    load[source] += alpha / sqrt_degrees[source]

    lipschitz = 1.0 + alpha
    shifted_gap = 2.0 * alpha
    root = math.sqrt(shifted_gap / lipschitz)
    momentum = (1.0 - root) / (1.0 + root)
    auxiliary_scale = (1.0 - root) / root

    lower = np.zeros(n)
    certified = np.zeros(n, dtype=bool)
    certified[source] = True
    width = 1.0 / degrees[source] - rho
    target_width = relative_width * width
    phases = 0
    total_iterations = 0
    maximum_phase_root_time = 0.0
    maximum_missing_after_closure = 0
    maximum_lower_deficit = 0.0
    maximum_primal_deficit = 0.0
    maximum_extrapolate_deficit = 0.0
    minimum_raw_momentum_margin = math.inf
    append_work = 0.0
    core_work = 0.0
    push_work = 0.0

    while width > target_width:
        old_lower = lower.copy()
        shifted_load = load + alpha * old_lower
        requested = width / 4.0
        current = old_lower.copy()
        previous = old_lower.copy()
        omniscient_current = old_lower.copy()
        omniscient_previous = old_lower.copy()
        omniscient_lower = old_lower.copy()

        for iteration in range(maximum_phase_iterations):
            active = np.flatnonzero(certified)
            starting_current = current.copy()
            starting_omniscient_current = omniscient_current.copy()

            extrapolated = np.zeros(n)
            extrapolated[active] = current[active] + momentum * (
                current[active] - previous[active]
            )
            raw_next = extrapolated + (
                shifted_load - shifted_matrix @ extrapolated
            ) / lipschitz
            next_current = np.zeros(n)
            next_current[active] = raw_next[active]
            previous, current = current, next_current
            masked_raw_next = current.copy()
            core_work += float(degrees[active].sum())

            omniscient_extrapolated = omniscient_current + momentum * (
                omniscient_current - omniscient_previous
            )
            omniscient_next = omniscient_extrapolated + (
                shifted_load - shifted_matrix @ omniscient_extrapolated
            ) / lipschitz
            omniscient_previous, omniscient_current = (
                omniscient_current,
                omniscient_next,
            )

            raw_margin = (
                2.0 * (masked_raw_next[active] - omniscient_current[active])
                - (1.0 - root)
                * (
                    starting_current[active]
                    - starting_omniscient_current[active]
                )
            )
            minimum_raw_momentum_margin = min(
                minimum_raw_momentum_margin,
                float(np.min(raw_margin, initial=math.inf)),
            )

            omniscient_residual = shifted_load - shifted_matrix @ omniscient_current
            omniscient_shift = max(
                0.0,
                float(
                    np.max(
                        -omniscient_residual
                        / (shifted_gap * sqrt_degrees)
                    )
                ),
            )
            omniscient_candidate = (
                omniscient_current - omniscient_shift * sqrt_degrees
            )
            omniscient_lower = np.maximum(
                omniscient_lower, np.maximum(omniscient_candidate, 0.0)
            )
            omniscient_auxiliary = omniscient_current + auxiliary_scale * (
                omniscient_current - omniscient_previous
            )
            omniscient_current = np.maximum(
                omniscient_current, omniscient_lower
            )
            omniscient_auxiliary = np.maximum(
                omniscient_auxiliary, omniscient_lower
            )
            omniscient_previous = omniscient_current - (
                omniscient_auxiliary - omniscient_current
            ) / auxiliary_scale

            active_residual = shifted_load - shifted_matrix @ current
            active_direction = shifted_matrix @ (
                sqrt_degrees * certified.astype(float)
            )
            ratios = np.divide(
                -active_residual[active],
                active_direction[active],
                out=np.full(len(active), -np.inf),
                where=active_direction[active] > 0.0,
            )
            shift = max(0.0, float(np.max(ratios, initial=-np.inf)))
            lower[active] = np.maximum(
                lower[active],
                np.maximum(current[active] - shift * sqrt_degrees[active], 0.0),
            )
            auxiliary = current + auxiliary_scale * (current - previous)
            current[active] = np.maximum(current[active], lower[active])
            auxiliary[active] = np.maximum(auxiliary[active], lower[active])
            previous[active] = current[active] - (
                auxiliary[active] - current[active]
            ) / auxiliary_scale

            residual = shifted_load - shifted_matrix @ lower
            positive_active = active[residual[active] > 0.0]
            increment = np.zeros(n)
            increment[positive_active] = (
                residual[positive_active] / shifted_diagonal
            )
            lower += increment
            residual -= shifted_matrix @ increment
            push_work += float(degrees[positive_active].sum())
            current[active] = np.maximum(current[active], lower[active])
            auxiliary[active] = np.maximum(auxiliary[active], lower[active])
            previous[active] = current[active] - (
                auxiliary[active] - current[active]
            ) / auxiliary_scale

            while True:
                batch = np.flatnonzero((~certified) & (residual > 0.0))
                if not len(batch):
                    break
                certified[batch] = True
                append_increment = np.zeros(n)
                append_increment[batch] = residual[batch] / shifted_diagonal
                lower += append_increment
                residual -= shifted_matrix @ append_increment
                append_work += float(degrees[batch].sum())
                current[batch] = lower[batch]
                auxiliary[batch] = lower[batch]
                previous[batch] = lower[batch]

            maximum_missing_after_closure = max(
                maximum_missing_after_closure, int((~certified).sum())
            )
            masked_extrapolate = (
                current + root * auxiliary
            ) / (1.0 + root)
            omniscient_extrapolate = (
                omniscient_current + root * omniscient_auxiliary
            ) / (1.0 + root)
            maximum_lower_deficit = max(
                maximum_lower_deficit,
                float(np.max(omniscient_lower - lower)),
            )
            maximum_primal_deficit = max(
                maximum_primal_deficit,
                float(np.max(omniscient_current - current)),
            )
            maximum_extrapolate_deficit = max(
                maximum_extrapolate_deficit,
                float(np.max(omniscient_extrapolate - masked_extrapolate)),
            )

            inner_width = float(
                np.max(
                    np.maximum(residual, 0.0)
                    / (shifted_gap * sqrt_degrees)
                )
            )
            if inner_width <= requested * (1.0 + 2.0e-10):
                break
        else:
            raise RuntimeError("sparse tree phase exceeded its iteration limit")

        phase_iterations = iteration + 1
        total_iterations += phase_iterations
        maximum_phase_root_time = max(
            maximum_phase_root_time, phase_iterations * root
        )
        width = width / 2.0 + inner_width
        phases += 1

    final_volume = float(degrees.sum())
    charged_work = core_work + push_work + append_work
    assert push_work <= core_work + 1.0e-8
    assert append_work <= final_volume + 1.0e-8
    # The exact-real comparison is expected to be nonpositive.  These loose
    # guards only reject a macroscopic floating-point regression.
    assert maximum_lower_deficit < 2.0e-9
    assert maximum_primal_deficit < 2.0e-9
    assert maximum_extrapolate_deficit < 2.0e-9
    assert minimum_raw_momentum_margin > -2.0e-9
    return {
        "warning": "sparse floating-point stress, not a theorem",
        "vertices": n,
        "edges": len(edges),
        "alpha": alpha,
        "rho": rho,
        "phases": phases,
        "total_iterations": total_iterations,
        "maximum_phase_root_time": maximum_phase_root_time,
        "maximum_missing_after_closure": maximum_missing_after_closure,
        "final_certified_vertices": int(certified.sum()),
        "maximum_lower_deficit": maximum_lower_deficit,
        "maximum_primal_deficit": maximum_primal_deficit,
        "maximum_extrapolate_deficit": maximum_extrapolate_deficit,
        "minimum_raw_momentum_margin": minimum_raw_momentum_margin,
        "core_root_work_ratio": core_work * math.sqrt(alpha) / final_volume,
        "charged_root_work_ratio": charged_work * math.sqrt(alpha) / final_volume,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--relative-width", type=float, default=1.0e-3)
    parser.add_argument("--maximum-phase-iterations", type=int, default=5000)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.relative_width, args.maximum_phase_iterations),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
