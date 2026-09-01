#!/usr/bin/env python3
"""Symbolic audit of the partial-gradient NAG potential contraction.

The support-safety and sign of the omitted exterior-gradient term are proved
order-theoretically in README.md.  This script verifies the remaining scalar
estimate-sequence cancellation exactly.
"""

from __future__ import annotations

import json

import sympy as sp


def main() -> None:
    root, strong, q_error, displacement, gradient = sp.symbols("s mu b d g", positive=True)
    old_objective_gap = sp.symbols("F", nonnegative=True)
    lipschitz = strong / root**2

    # q_error=q-x*, displacement=x-q, and therefore z-x*=q_error-d/s.
    old_estimate_error = q_error - displacement / root

    # Convexity at x and strong convexity at x* are combined with weights
    # 1-s and s; smooth descent contributes -g^2/(2L).
    next_objective_upper = (
        (1 - root) * old_objective_gap
        - (1 - root) * gradient * displacement
        + root * gradient * q_error
        - root * strong * q_error**2 / 2
        - gradient**2 / (2 * lipschitz)
    )
    next_estimate_error = q_error - (1 - root) * displacement / root - root * gradient / strong
    old_potential = old_objective_gap + strong * old_estimate_error**2 / 2
    next_potential_upper = next_objective_upper + strong * next_estimate_error**2 / 2
    remainder = sp.factor(sp.expand(next_potential_upper - (1 - root) * old_potential))
    expected = -(1 - root) * strong * displacement**2 / (2 * root)
    assert sp.simplify(remainder - expected) == 0

    print(
        json.dumps(
            {
                "identity": str(remainder),
                "conclusion": (
                    "for 0<s<=1 and mu>0, the active partial-gradient "
                    "NAG potential contracts by 1-s, with the displayed "
                    "nonpositive remainder"
                ),
                "scope": (
                    "requires the omitted exterior gradient inner product with x* to be nonnegative"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
