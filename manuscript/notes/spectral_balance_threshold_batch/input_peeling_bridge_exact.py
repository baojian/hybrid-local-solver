#!/usr/bin/env python3
"""Symbolic identities for inserting a peeling safeguard before local NAG.

The identities isolate two different quantities which must not be conflated:

* changing the physical estimate state to realize the safe input can increase
  the ordinary NAG estimate potential; and
* the complementarity error of a one-pass (rather than exact) safe-box
  projection is paid by two-step objective progress with no alpha loss.

The order and positivity hypotheses needed to turn the identities into
inequalities are proved in the companion README.
"""

from __future__ import annotations

import json

import sympy as sp


def main() -> None:
    root, lipschitz = sp.symbols("s L", positive=True)
    error, accepted, correction = sp.symbols("X u e", nonnegative=True)
    strong = root**2 * lipschitz
    estimate_scale = (1 + root) / root

    # q_raw-x = u+e, q_safe-x=u.  The estimate state is reset by
    # z_safe=z_raw-kappa*e, and X=x*-x.
    old_estimate_error = estimate_scale * (accepted + correction) - error
    safe_estimate_error = estimate_scale * accepted - error
    potential_debit = sp.factor(
        strong * (safe_estimate_error**2 - old_estimate_error**2) / 2
    )
    expected_debit = sp.factor(
        root * lipschitz * (1 + root) * correction * error
        - lipschitz
        * (1 + root) ** 2
        * (correction * accepted + correction**2 / 2)
    )
    assert sp.simplify(potential_debit - expected_debit) == 0

    # Scalar audit of the direct-gradient two-step charge.  Here delta is
    # x-x_old, u=q_safe-x, t is the safe residual, and the raw momentum is
    # theta*delta=u+e.  The matrix quadratic terms are represented by
    # nonnegative symbols because the vector identity is obtained by exact
    # quadratic expansion.
    theta, delta, safe_residual = sp.symbols("theta d t", positive=True)
    path_energy, gradient_descent = sp.symbols("E_path E_grad", nonnegative=True)
    correction_from_box = theta * delta - accepted
    peeling_gap = correction_from_box * safe_residual
    objective_decrease = (
        safe_residual * (delta + accepted) + path_energy + gradient_descent
    )
    charge_remainder = sp.factor(objective_decrease - peeling_gap / theta)
    expected_charge_remainder = sp.factor(
        (1 + 1 / theta) * accepted * safe_residual + path_energy + gradient_descent
    )
    assert sp.simplify(charge_remainder - expected_charge_remainder) == 0

    print(
        json.dumps(
            {
                "estimate_potential_debit_identity": str(potential_debit),
                "two_step_charge_remainder": str(charge_remainder),
                "conclusions": [
                    "the exact safe-input reset has a potentially positive comparator cross term",
                    "the one-pass projection complementarity gap is at most theta times two-step objective decrease",
                ],
                "scope": "symbolic scalar coefficients; vector forms use Euclidean inner products and quadratic norms",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
