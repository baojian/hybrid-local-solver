#!/usr/bin/env python3
"""Exact symbolic certificate for the zero-start two-vertex PeelingLC ray.

Run with ``uv run --with sympy python peeling_lc_two_vertex_ray_exact.py``.
The script checks the removable-limit map, the implicit-function Jacobian,
and the first terms of the analytic slow branch.
"""

from __future__ import annotations

import json

import sympy as sp


def main() -> None:
    root, momentum_zero, scaled_momentum_one = sp.symbols(
        "s p y", positive=True
    )
    diagonal = (1 + root**2) / 2
    off_diagonal = (1 - root**2) / 2
    denominator = (
        diagonal * momentum_zero
        - off_diagonal * root * scaled_momentum_one
    )
    accepted_zero = root**2 * momentum_zero / denominator
    accepted_one = root**2 * scaled_momentum_one / (1 + root)
    slack_zero = (
        root**2
        - diagonal * accepted_zero
        + off_diagonal * accepted_one
    )
    slack_one = (
        root**2
        + off_diagonal * accepted_zero
        - diagonal * accepted_one
    )
    rate = sp.factor(
        1 - root**2 - off_diagonal * (accepted_zero + accepted_one)
    )
    next_momentum_zero = sp.cancel(
        (1 - root)
        * (momentum_zero - accepted_zero + slack_zero / root)
        / rate
    )
    next_scaled_momentum_one = sp.cancel(
        (1 - root)
        * (
            root * scaled_momentum_one
            - accepted_one
            + slack_one / root
        )
        / (root * rate)
    )

    fixed_zero = sp.cancel((next_momentum_zero - momentum_zero) / root)
    fixed_one = sp.cancel(next_scaled_momentum_one - scaled_momentum_one)
    limit_equations = (
        sp.factor(fixed_zero.subs(root, 0)),
        sp.factor(fixed_one.subs(root, 0)),
    )
    branch_origin = {momentum_zero: 2, scaled_momentum_one: 4}
    jacobian = sp.Matrix(limit_equations).jacobian(
        (momentum_zero, scaled_momentum_one)
    )
    branch_jacobian = sp.simplify(jacobian.subs(branch_origin))

    upper_boundary = 4 + 8 * root / momentum_zero
    upper_next_zero = next_momentum_zero.subs(
        scaled_momentum_one, upper_boundary
    )
    upper_next_one = next_scaled_momentum_one.subs(
        scaled_momentum_one, upper_boundary
    )
    upper_inward_limit = sp.factor(
        sp.limit(
            (
                upper_next_zero * (upper_next_one - 4)
                - 8 * root
            )
            / root,
            root,
            0,
        )
    )
    upper_slack_one_limit = sp.factor(
        sp.limit(
            slack_one.subs(scaled_momentum_one, upper_boundary) / root**3,
            root,
            0,
        )
    )
    event_limits = {
        "other_initial_pressure": sp.factor(
            (diagonal * root * scaled_momentum_one - off_diagonal * momentum_zero).subs(
                root, 0
            )
        ),
        "source_final_slack_over_s2": sp.factor(
            sp.limit(slack_zero / root**2, root, 0)
        ),
        "other_slack_y_derivative_over_s2": sp.factor(
            sp.limit(
                sp.diff(slack_one, scaled_momentum_one) / root**2,
                root,
                0,
            )
        ),
        "upper_other_final_slack_over_s3": upper_slack_one_limit,
        "upper_boundary_inward": upper_inward_limit,
    }

    threshold_complement = sp.Rational(1, 2) + root
    matrix = sp.Matrix(
        [[diagonal, -off_diagonal], [-off_diagonal, diagonal]]
    )
    load = root**2 * sp.Matrix(
        [threshold_complement, -sp.Rational(1, 2) + root]
    )
    optimum = sp.Matrix([root + root**2 / 2, root - root**2 / 2])
    first_primal = sp.Matrix([load[0], 0])
    first_estimate = first_primal / root
    second_safe = sp.simplify(
        (first_primal + root * first_estimate) / (1 + root)
    )
    second_slack = sp.simplify(load - matrix * second_safe)
    second_primal = sp.simplify(second_safe + second_slack)
    second_estimate = sp.simplify(
        (1 - root) * first_estimate
        + root * second_safe
        + second_slack / root
    )
    initial_amplitude = (
        root - root**2 / 2 - 3 * root**3 / 2 + root**4
    )
    initial_momentum_zero = (
        root * threshold_complement * (1 - root) ** 2
        / initial_amplitude
    )
    initial_scaled_momentum_one = (
        root * (1 - root) * (sp.Rational(3, 2) - root)
        / initial_amplitude
    )
    zero_start_checks = {
        "second_round_exterior_residual": sp.factor(second_slack[1]),
        "symmetric_error_amplitude": initial_amplitude,
        "initial_projective_p_limit": sp.limit(
            initial_momentum_zero, root, 0
        ),
        "initial_projective_y_limit": sp.limit(
            initial_scaled_momentum_one, root, 0
        ),
        "initial_objective_gap": sp.factor((load.T * optimum)[0] / 2),
    }

    branch_zero = 2 - 4 * root + 8 * root**2
    branch_one = 4 - 8 * root + 52 * root**2
    branch = {
        momentum_zero: branch_zero,
        scaled_momentum_one: branch_one,
    }
    fixed_residual_series = (
        sp.series(fixed_zero.subs(branch), root, 0, 4),
        sp.series(fixed_one.subs(branch), root, 0, 4),
    )
    rate_series = sp.series(rate.subs(branch), root, 0, 4)
    hit_time = root * (1 + root) / denominator
    hit_time_series = sp.series(hit_time.subs(branch), root, 0, 4)
    slack_zero_series = sp.series(slack_zero.subs(branch), root, 0, 4)
    slack_one_series = sp.series(slack_one.subs(branch), root, 0, 4)

    expected = {
        "limit_equations": (-momentum_zero + scaled_momentum_one / 2, 2 - scaled_momentum_one / 2),
        "jacobian": sp.Matrix([[-1, sp.Rational(1, 2)], [0, sp.Rational(-1, 2)]]),
        "fixed_residual_orders": (3, 3),
        "rate": 1 - 4 * root**2 + 4 * root**3,
        "hit_time": root + 5 * root**2 + 11 * root**3,
        "slack_zero": 2 * root**2 - 8 * root**3,
        "slack_one": 8 * root**3,
    }
    assert all(
        sp.simplify(actual - wanted) == 0
        for actual, wanted in zip(
            limit_equations, expected["limit_equations"], strict=True
        )
    )
    assert branch_jacobian == expected["jacobian"]
    assert sp.simplify(branch_jacobian.det()) == sp.Rational(1, 2)
    assert event_limits == {
        "other_initial_pressure": -momentum_zero / 2,
        "source_final_slack_over_s2": scaled_momentum_one / 2,
        "other_slack_y_derivative_over_s2": sp.Rational(-1, 2),
        "upper_other_final_slack_over_s3": 2,
        "upper_boundary_inward": -6 * momentum_zero,
    }
    assert zero_start_checks["initial_projective_p_limit"] == sp.Rational(1, 2)
    assert zero_start_checks["initial_projective_y_limit"] == sp.Rational(3, 2)
    expected_error = sp.Matrix([initial_amplitude, initial_amplitude])
    expected_velocity = sp.Matrix(
        [
            root * threshold_complement * (1 - root) ** 2,
            root**2 * (1 - root) * (sp.Rational(3, 2) - root),
        ]
    )
    assert all(
        sp.simplify(value) == 0
        for value in optimum - second_primal - expected_error
    )
    assert all(
        sp.simplify(value) == 0
        for value in second_estimate - second_primal - expected_velocity
    )
    assert sp.simplify(
        zero_start_checks["second_round_exterior_residual"]
        - root**3 * (sp.Rational(3, 2) - root)
    ) == 0
    assert sp.simplify(
        zero_start_checks["initial_objective_gap"] - 5 * root**4 / 4
    ) == 0
    for residual, order in zip(
        fixed_residual_series, expected["fixed_residual_orders"], strict=True
    ):
        assert residual.removeO().as_leading_term(root).as_powers_dict()[root] >= order
    assert sp.expand(rate_series.removeO() - expected["rate"]) == 0
    assert sp.expand(hit_time_series.removeO() - expected["hit_time"]) == 0
    assert sp.expand(slack_zero_series.removeO() - expected["slack_zero"]) == 0
    assert sp.expand(slack_one_series.removeO() - expected["slack_one"]) == 0

    print(
        json.dumps(
            {
                "limit_fixed_equations": list(map(str, limit_equations)),
                "implicit_jacobian": [
                    list(map(str, branch_jacobian.row(index))) for index in range(2)
                ],
                "implicit_jacobian_determinant": str(branch_jacobian.det()),
                "invariant_domain_limits": {
                    key: str(value) for key, value in event_limits.items()
                },
                "zero_start_entry": {
                    key: str(value) for key, value in zero_start_checks.items()
                },
                "analytic_branch": {
                    "momentum_zero": "2 - 4*s + 8*s^2 + O(s^3)",
                    "scaled_momentum_one": "4 - 8*s + 52*s^2 + O(s^3)",
                    "rate": str(rate_series),
                    "source_hit_time": str(hit_time_series),
                    "source_final_slack": str(slack_zero_series),
                    "other_final_slack": str(slack_one_series),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
