#!/usr/bin/env python3
"""Exact canonical-load stop for pushed-retraction isotonicity.

The graph, source load, retained shift, and old lower state are canonical.
Only the ordered input currents are not asserted reachable from the
prescribed zero-start NAG chronology.
"""

from fractions import Fraction as F


def main() -> None:
    alpha = F(1, 10_000)
    rho = F(1, 1_000)
    diagonal = (1 + 3 * alpha) / 2
    coupling = (1 - alpha) / 2
    matrix = ((diagonal, -coupling), (-coupling, diagonal))
    original_matrix = (
        ((1 + alpha) / 2, -coupling),
        (-coupling, (1 + alpha) / 2),
    )
    original_load = (alpha * (1 - rho), -alpha * rho)
    solution = (F(9_981, 20_000), F(9_979, 20_000))
    shave = F(3, 10) * solution[1]
    old_lower = tuple(value - shave for value in solution)
    load = tuple(
        original_load[row] + alpha * old_lower[row] for row in range(2)
    )
    omniscient = (F(494_953, 10**6), F(494_866, 10**6))
    masked = (F(645_553, 10**6), F(640_166, 10**6))
    assert all(left <= right for left, right in zip(omniscient, masked))

    def apply_with(
        operator: tuple[tuple[F, F], tuple[F, F]],
        state: tuple[F, F],
    ) -> tuple[F, F]:
        return tuple(
            sum(operator[row][column] * state[column] for column in range(2))
            for row in range(2)
        )

    assert apply_with(original_matrix, solution) == original_load
    old_product = apply_with(original_matrix, old_lower)
    assert all(
        old_product[row] <= original_load[row] for row in range(2)
    )

    def pushed_retraction(state: tuple[F, F]) -> tuple[F, F]:
        product = apply_with(matrix, state)
        residual = tuple(load[row] - product[row] for row in range(2))
        row_sum = diagonal - coupling
        shift = max(F(0), *(-value / row_sum for value in residual))
        lower = tuple(
            max(old_lower[row], state[row] - shift, F(0))
            for row in range(2)
        )
        lower_product = apply_with(matrix, lower)
        lower_residual = tuple(
            load[row] - lower_product[row] for row in range(2)
        )
        return tuple(
            lower[row] + max(F(0), lower_residual[row]) / diagonal
            for row in range(2)
        )

    omniscient_output = pushed_retraction(omniscient)
    masked_output = pushed_retraction(masked)
    assert omniscient_output == (
        F(15_673_650_477, 40_012_000_000),
        F(1_566_443, 4_000_000),
    )
    assert masked_output == (
        F(698_999_493, 2_000_600_000),
        F(698_799_433, 2_000_600_000),
    )
    deficits = tuple(
        omniscient_output[row] - masked_output[row] for row in range(2)
    )
    assert deficits == (
        F(1_693_660_617, 40_012_000_000),
        F(1_693_140_669, 40_012_000_000),
    )
    assert min(deficits) > 0

    print("pushed retraction is not an isotone operator")
    print("strict deficits =", deficits)


if __name__ == "__main__":
    main()
