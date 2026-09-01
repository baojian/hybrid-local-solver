#!/usr/bin/env python3
"""Stress the reachable masked ``no-shave`` cone from an arbitrary phase residual.

This isolates a fixed active face.  Starting from a certified lower point with
arbitrary nonnegative active residual, it executes the enhanced retained-prox
updates (one diagonal residual push per product) and reports the smallest raw
current residual before retraction.  A negative value is an exact obstruction
to the tempting claim that the masked retraction is always inactive.

The experiment is only a counterexample search; a nonnegative result is not a
proof of the source-history invariant.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np


def trial(
    rng: np.random.Generator,
    vertices: int,
    alpha: float,
    products: int,
    residual_push_rounds: int,
    quarter_stop: bool,
):
    adjacency = np.zeros((vertices, vertices))
    # A path guarantees connectivity; extra edges randomize the averaging map.
    for i in range(vertices - 1):
        adjacency[i, i + 1] = adjacency[i + 1, i] = 1.0
    for i in range(vertices):
        for j in range(i + 2, vertices):
            if rng.random() < 0.22:
                adjacency[i, j] = adjacency[j, i] = 1.0
    degrees = adjacency.sum(axis=1)
    transition = adjacency / degrees[:, None]
    coupling = (1.0 - alpha) / 2.0
    diagonal = (1.0 + 3.0 * alpha) / 2.0
    lipschitz = 1.0 + alpha
    root = math.sqrt(2.0 * alpha / (1.0 + alpha))
    momentum = (1.0 - root) / (1.0 + root)
    auxiliary_scale = (1.0 - root) / root
    matrix = diagonal * np.eye(vertices) - coupling * transition

    residual0 = np.exp(rng.uniform(-12.0, 12.0, size=vertices))
    residual0 /= residual0.max()
    load = residual0.copy()
    lower = np.zeros(vertices)
    current = lower.copy()
    previous = lower.copy()
    omniscient_lower = lower.copy()
    omniscient_current = lower.copy()
    omniscient_previous = lower.copy()
    smallest = math.inf
    witness = {}
    smallest_lead = math.inf
    lead_witness = {}
    smallest_nonterminal_lead = math.inf
    nonterminal_lead_witness = {}
    smallest_same_time_gap = math.inf
    same_time_gap_witness = {}
    smallest_lower_over_omniscient_extrapolate_gap = math.inf
    lower_over_omniscient_extrapolate_witness = {}
    smallest_same_time_extrapolate_gap = math.inf
    same_time_extrapolate_witness = {}
    maximum_predecessor_residual_at_lead_failure = -math.inf
    lead_failure_residual_witness = {}
    predecessor_residual_maximum = math.inf
    for product in range(1, products + 1):
        starting_lower = lower.copy()
        extrapolate = current + momentum * (current - previous)
        following = extrapolate + (load - matrix @ extrapolate) / lipschitz
        previous, current = current, following
        raw_residual = load - matrix @ current
        raw_min = float(raw_residual.min())
        if raw_min < smallest:
            smallest = raw_min
            witness = {
                "product": product,
                "vertex": int(np.argmin(raw_residual)),
                "raw_residual": raw_min,
                "initial_residual": residual0.tolist(),
                "edges": np.argwhere(np.triu(adjacency) > 0).tolist(),
            }

        omniscient_extrapolate = omniscient_current + momentum * (
            omniscient_current - omniscient_previous
        )
        omniscient_following = (
            omniscient_extrapolate + (load - matrix @ omniscient_extrapolate) / lipschitz
        )
        omniscient_previous, omniscient_current = (
            omniscient_current,
            omniscient_following,
        )
        omniscient_raw_residual = load - matrix @ omniscient_current
        direction = matrix @ np.ones(vertices)
        omniscient_shift = max(0.0, float(np.max(-omniscient_raw_residual / direction)))
        omniscient_candidate = omniscient_current - omniscient_shift
        omniscient_lower = np.maximum(omniscient_lower, np.maximum(omniscient_candidate, 0.0))
        omniscient_auxiliary = omniscient_current + auxiliary_scale * (
            omniscient_current - omniscient_previous
        )
        omniscient_current = np.maximum(omniscient_current, omniscient_lower)
        omniscient_auxiliary = np.maximum(omniscient_auxiliary, omniscient_lower)
        omniscient_previous = (
            omniscient_current - (omniscient_auxiliary - omniscient_current) / auxiliary_scale
        )
        pending_lead = None
        pending_lead_witness = {}
        if product > 1:
            lead = float(np.min(starting_lower - omniscient_lower))
            pending_lead = lead
            pending_lead_witness = {
                "product": product,
                "vertex": int(np.argmin(starting_lower - omniscient_lower)),
                "lead": lead,
                "initial_residual": residual0.tolist(),
                "edges": np.argwhere(np.triu(adjacency) > 0).tolist(),
            }
            if lead < smallest_lead:
                smallest_lead = lead
                lead_witness = pending_lead_witness
            if (
                lead < 0.0
                and predecessor_residual_maximum > maximum_predecessor_residual_at_lead_failure
            ):
                maximum_predecessor_residual_at_lead_failure = predecessor_residual_maximum
                lead_failure_residual_witness = {
                    **pending_lead_witness,
                    "predecessor_residual_maximum": (predecessor_residual_maximum),
                }

        # Retraction exactly as in the retained-prox experiment.
        direction = matrix @ np.ones(vertices)
        shift = max(0.0, float(np.max(-raw_residual / direction)))
        candidate = current - shift
        lower = np.maximum(lower, np.maximum(candidate, 0.0))
        auxiliary = current + auxiliary_scale * (current - previous)
        current = np.maximum(current, lower)
        auxiliary = np.maximum(auxiliary, lower)
        previous = current - (auxiliary - current) / auxiliary_scale

        for _ in range(residual_push_rounds):
            residual = load - matrix @ lower
            increment = np.maximum(residual, 0.0) / diagonal
            lower += increment
            current = np.maximum(current, lower)
            auxiliary = np.maximum(auxiliary, lower)
            previous = current - (auxiliary - current) / auxiliary_scale
        same_time_gap = float(np.min(lower - omniscient_lower))
        if same_time_gap < smallest_same_time_gap:
            smallest_same_time_gap = same_time_gap
            same_time_gap_witness = {
                "product": product,
                "vertex": int(np.argmin(lower - omniscient_lower)),
                "gap": same_time_gap,
                "initial_residual": residual0.tolist(),
                "edges": np.argwhere(np.triu(adjacency) > 0).tolist(),
            }
        omniscient_output_extrapolate = (omniscient_current + root * omniscient_auxiliary) / (
            1.0 + root
        )
        masked_output_extrapolate = (current + root * auxiliary) / (1.0 + root)
        same_time_extrapolate_gap = float(
            np.min(masked_output_extrapolate - omniscient_output_extrapolate)
        )
        if same_time_extrapolate_gap < smallest_same_time_extrapolate_gap:
            smallest_same_time_extrapolate_gap = same_time_extrapolate_gap
            same_time_extrapolate_witness = {
                "product": product,
                "vertex": int(np.argmin(masked_output_extrapolate - omniscient_output_extrapolate)),
                "gap": same_time_extrapolate_gap,
                "initial_residual": residual0.tolist(),
                "edges": np.argwhere(np.triu(adjacency) > 0).tolist(),
            }
        lower_over_extrapolate = float(np.min(lower - omniscient_output_extrapolate))
        if lower_over_extrapolate < smallest_lower_over_omniscient_extrapolate_gap:
            smallest_lower_over_omniscient_extrapolate_gap = lower_over_extrapolate
            lower_over_omniscient_extrapolate_witness = {
                "product": product,
                "vertex": int(np.argmin(lower - omniscient_output_extrapolate)),
                "gap": lower_over_extrapolate,
                "initial_residual": residual0.tolist(),
                "edges": np.argwhere(np.triu(adjacency) > 0).tolist(),
            }
        post_push_residual = load - matrix @ lower
        predecessor_residual_maximum = max(0.0, float(post_push_residual.max()))
        stopped = predecessor_residual_maximum <= 0.25
        if pending_lead is not None and not stopped:
            if pending_lead < smallest_nonterminal_lead:
                smallest_nonterminal_lead = pending_lead
                nonterminal_lead_witness = pending_lead_witness
        if quarter_stop and stopped:
            break
    return (
        smallest,
        witness,
        smallest_lead,
        lead_witness,
        smallest_nonterminal_lead,
        nonterminal_lead_witness,
        smallest_same_time_gap,
        same_time_gap_witness,
        smallest_lower_over_omniscient_extrapolate_gap,
        lower_over_omniscient_extrapolate_witness,
        smallest_same_time_extrapolate_gap,
        same_time_extrapolate_witness,
        maximum_predecessor_residual_at_lead_failure,
        lead_failure_residual_witness,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=12)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--products", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20260901)
    parser.add_argument("--residual-push-rounds", type=int, default=1)
    parser.add_argument("--quarter-stop", action="store_true")
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    best = math.inf
    best_record = {}
    best_lead = math.inf
    best_lead_record = {}
    best_nonterminal_lead = math.inf
    best_nonterminal_lead_record = {}
    best_same_time_gap = math.inf
    best_same_time_gap_record = {}
    best_lower_over_omniscient_extrapolate_gap = math.inf
    best_lower_over_omniscient_extrapolate_record = {}
    best_same_time_extrapolate_gap = math.inf
    best_same_time_extrapolate_record = {}
    maximum_failure_predecessor_residual = -math.inf
    maximum_failure_predecessor_residual_record = {}
    for _ in range(args.trials):
        alpha = math.exp(rng.uniform(math.log(1.0e-6), math.log(0.99)))
        (
            value,
            witness,
            lead,
            lead_witness,
            nonterminal_lead,
            nonterminal_lead_witness,
            same_time_gap,
            same_time_gap_witness,
            lower_over_omniscient_extrapolate_gap,
            lower_over_omniscient_extrapolate_witness,
            same_time_extrapolate_gap,
            same_time_extrapolate_witness,
            failure_predecessor_residual,
            lead_failure_residual_witness,
        ) = trial(
            rng,
            args.vertices,
            alpha,
            args.products,
            args.residual_push_rounds,
            args.quarter_stop,
        )
        if value < best:
            best = value
            best_record = {"alpha": alpha, **witness}
        if lead < best_lead:
            best_lead = lead
            best_lead_record = {"alpha": alpha, **lead_witness}
        if nonterminal_lead < best_nonterminal_lead:
            best_nonterminal_lead = nonterminal_lead
            best_nonterminal_lead_record = {
                "alpha": alpha,
                **nonterminal_lead_witness,
            }
        if same_time_gap < best_same_time_gap:
            best_same_time_gap = same_time_gap
            best_same_time_gap_record = {
                "alpha": alpha,
                **same_time_gap_witness,
            }
        if lower_over_omniscient_extrapolate_gap < best_lower_over_omniscient_extrapolate_gap:
            best_lower_over_omniscient_extrapolate_gap = lower_over_omniscient_extrapolate_gap
            best_lower_over_omniscient_extrapolate_record = {
                "alpha": alpha,
                **lower_over_omniscient_extrapolate_witness,
            }
        if same_time_extrapolate_gap < best_same_time_extrapolate_gap:
            best_same_time_extrapolate_gap = same_time_extrapolate_gap
            best_same_time_extrapolate_record = {
                "alpha": alpha,
                **same_time_extrapolate_witness,
            }
        if failure_predecessor_residual > maximum_failure_predecessor_residual:
            maximum_failure_predecessor_residual = failure_predecessor_residual
            maximum_failure_predecessor_residual_record = {
                "alpha": alpha,
                **lead_failure_residual_witness,
            }
    print(
        json.dumps(
            {
                "warning": "finite floating-point counterexample search",
                "trials": args.trials,
                "vertices": args.vertices,
                "products": args.products,
                "residual_push_rounds": args.residual_push_rounds,
                "quarter_stop": args.quarter_stop,
                "minimum_raw_residual": best,
                "witness": best_record,
                "minimum_pushed_one_step_lead": best_lead,
                "lead_witness": best_lead_record,
                "minimum_nonterminal_pushed_one_step_lead": (best_nonterminal_lead),
                "nonterminal_lead_witness": best_nonterminal_lead_record,
                "minimum_same_time_pushed_gap": best_same_time_gap,
                "same_time_gap_witness": best_same_time_gap_record,
                "minimum_lower_over_omniscient_extrapolate_gap": (
                    best_lower_over_omniscient_extrapolate_gap
                ),
                "lower_over_omniscient_extrapolate_witness": (
                    best_lower_over_omniscient_extrapolate_record
                ),
                "minimum_same_time_extrapolate_gap": (best_same_time_extrapolate_gap),
                "same_time_extrapolate_witness": (best_same_time_extrapolate_record),
                "maximum_predecessor_residual_at_lead_failure": (
                    maximum_failure_predecessor_residual
                ),
                "lead_failure_residual_witness": (maximum_failure_predecessor_residual_record),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
