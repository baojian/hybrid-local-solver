#!/usr/bin/env python3
"""Exact scalar stop for a bare pushed-state order induction.

The example is a legal fixed-face NAG state, but it is not claimed to be
reachable from the canonical single-source zero initialization.
"""

from fractions import Fraction as F


def extrapolate(current: F, auxiliary: F, root: F) -> F:
    return (current + root * auxiliary) / (1 + root)


def main() -> None:
    root = F(1, 2)
    # B/L=1/2 and h/L=2, so the scalar exact solution is 4 and the
    # normalized gradient map is T(q)=q+(2-q/2).
    matrix_over_lipschitz = F(1, 2)
    load_over_lipschitz = F(2)
    exact_solution = load_over_lipschitz / matrix_over_lipschitz

    omniscient_current = F(8)
    omniscient_auxiliary = F(14)
    masked_current = F(9)
    masked_auxiliary = F(12)
    lower = F(0)

    omniscient_input = extrapolate(
        omniscient_current, omniscient_auxiliary, root
    )
    masked_input = extrapolate(masked_current, masked_auxiliary, root)
    assert masked_current > omniscient_current
    assert masked_input == omniscient_input == 10
    assert lower <= min(omniscient_current, masked_current)

    following = omniscient_input + (
        load_over_lipschitz
        - matrix_over_lipschitz * omniscient_input
    )
    assert following == 7

    # With auxiliary_scale=(1-root)/root=1, the next auxiliary is
    # following+(following-current).  Retraction of following=7 produces
    # the exact certified lower value 4, below both new auxiliaries, so the
    # dual-dominance clamp changes neither of them.
    omniscient_next_auxiliary = 2 * following - omniscient_current
    masked_next_auxiliary = 2 * following - masked_current
    retracted_lower = min(following, exact_solution)
    assert retracted_lower == 4
    assert omniscient_next_auxiliary == 6 > retracted_lower
    assert masked_next_auxiliary == 5 > retracted_lower

    omniscient_next_input = extrapolate(
        following, omniscient_next_auxiliary, root
    )
    masked_next_input = extrapolate(
        following, masked_next_auxiliary, root
    )
    assert omniscient_next_input == F(20, 3)
    assert masked_next_input == F(19, 3)
    assert omniscient_next_input - masked_next_input == F(1, 3)

    print("bare current/extrapolate order induction fails exactly")
    print("next extrapolate deficit =", omniscient_next_input - masked_next_input)


if __name__ == "__main__":
    main()
