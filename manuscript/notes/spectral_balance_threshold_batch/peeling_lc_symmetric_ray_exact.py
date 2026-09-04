#!/usr/bin/env python3
"""Symbolic certificate for the five-vertex PeelingLC slow ray.

Run with ``uv run --with sympy python peeling_lc_symmetric_ray_exact.py``.
The script eliminates the two orbit-error coordinates exactly, checks the
implicit-function equations at ``s=0``, and derives the first nonzero series
coefficients used in DETERMINISTIC_HALO_INTEGRATION.md.
"""

from __future__ import annotations

import json

import sympy as sp


def coefficient(expression: sp.Expr, variable: sp.Symbol, degree: int) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(expression), variable)
    return sp.factor(polynomial.coeff_monomial(variable**degree))


def main() -> None:
    root, rate, freeze = sp.symbols("s lambda tau")
    leaf_error, other_error = sp.symbols("X J")
    contraction, time_scale = sp.symbols("c eta")

    diagonal = (1 + root**2) / 2
    half_walk = (1 - root**2) / 2
    operator = sp.Matrix(
        [
            [diagonal, -half_walk / 2, -half_walk / 2],
            [-3 * half_walk / 4, diagonal, -half_walk / 4],
            [-3 * half_walk / 4, -half_walk / 4, diagonal],
        ]
    )
    delta = 1 - rate
    gamma = root * (rate / (1 - root) - 1)
    moving_velocity_ratio = delta * (1 - root) / (root * rate)
    moving_increment_ratio = root * moving_velocity_ratio / (1 + root)
    source_velocity = delta / (freeze * root + gamma)
    source_increment = freeze * root * source_velocity / (1 + root)

    error = sp.Matrix([leaf_error, 1, other_error])
    increment = sp.Matrix(
        [
            moving_increment_ratio * leaf_error,
            source_increment,
            moving_increment_ratio * other_error,
        ]
    )
    # This is B a = B u + t together with u+t=(1-lambda)a.
    invariant = operator * error - operator * increment - delta * error + increment
    moving_solution = sp.solve(
        [invariant[0], invariant[2]],
        [leaf_error, other_error],
        dict=True,
        simplify=False,
    )[0]

    source_equation = sp.together(invariant[1].subs(moving_solution))
    full_trial_increment = sp.Matrix(
        [
            moving_increment_ratio * moving_solution[leaf_error],
            root * source_velocity / (1 + root),
            moving_increment_ratio * moving_solution[other_error],
        ]
    )
    freeze_equation = sp.together(
        (operator * error)[1].subs(moving_solution)
        - freeze * (operator * full_trial_increment)[1]
    )

    blow_up = {
        rate: 1 - contraction * root**2,
        freeze: time_scale * root,
    }
    source_numerator = sp.fraction(sp.together(source_equation.subs(blow_up)))[0]
    freeze_numerator = sp.fraction(sp.together(freeze_equation.subs(blow_up)))[0]
    source_lead = sp.factor(
        coefficient(source_numerator, root, 3) / (4 * (time_scale + 1))
    )
    freeze_lead = sp.factor(
        coefficient(freeze_numerator, root, 3) / (4 * (time_scale + 1))
    )
    assert sp.simplify(source_lead - 5 * (2 * contraction - 7 * time_scale - 7)) == 0
    assert sp.simplify(freeze_lead - 5 * (contraction - 7) * (time_scale + 1)) == 0, (
        freeze_lead,
        [coefficient(freeze_numerator, root, degree) for degree in range(9)],
    )

    leading = sp.Matrix([source_lead, freeze_lead])
    variables = sp.Matrix([contraction, time_scale])
    branch_point = {contraction: 7, time_scale: 1}
    jacobian = leading.jacobian(variables).subs(branch_point)
    assert jacobian.det() == 350

    source_normalized = sp.cancel(source_numerator / (4 * (time_scale + 1) * root**3))
    freeze_normalized = sp.cancel(freeze_numerator / (4 * (time_scale + 1) * root**3))
    source_next = coefficient(source_normalized, root, 1).subs(branch_point)
    freeze_next = coefficient(freeze_normalized, root, 1).subs(branch_point)
    first_derivatives = -jacobian.inv() * sp.Matrix([source_next, freeze_next])
    assert first_derivatives == sp.Matrix([-49, 2])

    first_order_branch = {
        contraction: 7 - 49 * root,
        time_scale: 1 + 2 * root,
    }
    expanded_coordinates = {
        name: sp.series(
            value.subs(blow_up).subs(first_order_branch), root, 0, 4
        ).removeO()
        for name, value in (
            ("scaled_leaf_error", moving_solution[leaf_error]),
            ("other_hub_error", moving_solution[other_error]),
        )
    }
    assert coefficient(expanded_coordinates["scaled_leaf_error"] - 1, root, 2) == -sp.Rational(
        13, 10
    )
    assert coefficient(expanded_coordinates["other_hub_error"] - 1, root, 2) == -sp.Rational(
        21, 10
    )

    print(
        json.dumps(
            {
                "source_equation_at_s_zero": str(source_lead),
                "freeze_equation_at_s_zero": str(freeze_lead),
                "branch_point": {"c": 7, "eta": 1},
                "jacobian": [[str(value) for value in row] for row in jacobian.tolist()],
                "jacobian_determinant": str(jacobian.det()),
                "c_prime_at_zero": str(first_derivatives[0]),
                "eta_prime_at_zero": str(first_derivatives[1]),
                "scaled_leaf_error_series": str(expanded_coordinates["scaled_leaf_error"]),
                "other_hub_error_series": str(expanded_coordinates["other_hub_error"]),
                "conclusion": "lambda=1-7*s^2+49*s^3+O(s^4), tau=s+2*s^2+O(s^3)",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
