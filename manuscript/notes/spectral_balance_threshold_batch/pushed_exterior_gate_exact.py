#!/usr/bin/env python3
"""Exact arithmetic certificate for the retained-prox exterior gate.

This verifies the only parameter inequality used by the BoundaryFluxGate
lemma.  It is not a verifier that the boundary-flux premise holds along every
canonical history; that premise remains the open part.
"""

from __future__ import annotations

import json
from fractions import Fraction


def certificate(alpha: Fraction) -> dict[str, str]:
    if not 0 < alpha <= 1:
        raise ValueError("the retained PPR range is 0 < alpha <= 1")

    lipschitz = 1 + alpha
    diagonal = (1 + 3 * alpha) / 2
    root_squared = 2 * alpha / (1 + alpha)

    # The extrapolate produced on a zero-history exterior row is
    # 2c/(1+s).  A diagonal append p=r/B_ii with r>=Lc dominates it iff
    # s >= 2 alpha/(1+alpha).  Both sides are nonnegative, and the exact
    # squared slack factors as follows.
    root_threshold = 2 * alpha / (1 + alpha)
    squared_slack = root_squared - root_threshold * root_threshold
    factored_squared_slack = 2 * alpha * (1 - alpha) / (1 + alpha) ** 2
    assert squared_slack == factored_squared_slack
    assert squared_slack >= 0

    # It also dominates the raw current because B_ii<=L.
    diagonal_slack = lipschitz - diagonal
    assert diagonal_slack == (1 - alpha) / 2
    assert diagonal_slack >= 0

    return {
        "alpha": str(alpha),
        "L": str(lipschitz),
        "B_ii": str(diagonal),
        "L_minus_B_ii": str(diagonal_slack),
        "s_squared": str(root_squared),
        "required_lower_bound_on_s": str(root_threshold),
        "squared_slack": str(squared_slack),
        "squared_slack_factorization": "2*alpha*(1-alpha)/(1+alpha)^2",
        "conclusion": (
            "if r_i(u)>=L*c_i^o>0 on a zero-history exterior row, "
            "then p_i=r_i(u)/B_ii dominates both c_i^o and "
            "2*c_i^o/(1+s)"
        ),
    }


def main() -> None:
    samples = (
        Fraction(1, 1),
        Fraction(1, 100),
        Fraction(1, 10_000),
        Fraction(1, 1_000_000),
    )
    print(json.dumps([certificate(alpha) for alpha in samples], indent=2))


if __name__ == "__main__":
    main()
