#!/usr/bin/env python3
"""Exact finite audit of the reachable NAG clamp identity.

The accompanying proof is algebraic and valid for every 0<s<=1.  This script
checks the identity and its order consequence on a finite rational grid.  The
restriction that the auxiliary is generated from an old current above the old
lower is essential; arbitrary triples do not have this property.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


def reachable_state(
    root: F, old_lower: F, old_current: F, raw_current: F, fresh_candidate: F
) -> tuple[F, F, F, F]:
    assert 0 < root <= 1
    assert old_current >= old_lower >= 0
    assert fresh_candidate <= raw_current
    raw_auxiliary = (raw_current - (1 - root) * old_current) / root
    lower = max(old_lower, fresh_candidate, F(0))
    raw_extrapolate = (raw_current + root * raw_auxiliary) / (1 + root)
    clamped_extrapolate = (
        max(raw_current, lower) + root * max(raw_auxiliary, lower)
    ) / (1 + root)
    formula = max(
        raw_extrapolate,
        lower,
        (raw_current + root * lower) / (1 + root),
    )
    assert clamped_extrapolate == formula
    return raw_current, raw_extrapolate, lower, clamped_extrapolate


def main() -> None:
    roots = (F(1, 4), F(1, 2), F(3, 4), F(1))
    grid = tuple(F(value, 2) for value in range(-4, 9))
    checked_states = 0
    checked_ordered_pairs = 0

    for root in roots:
        states: list[tuple[F, F, F, F]] = []
        for old_lower in (F(0), F(1, 2), F(1), F(2)):
            for old_current in (F(0), F(1, 2), F(1), F(2), F(3)):
                if old_current < old_lower:
                    continue
                for raw_current in grid:
                    for shave in (F(0), F(1, 2), F(2)):
                        fresh_candidate = raw_current - shave
                        states.append(
                            reachable_state(
                                root,
                                old_lower,
                                old_current,
                                raw_current,
                                fresh_candidate,
                            )
                        )
                        checked_states += 1

        for omniscient in states:
            for masked in states:
                if (
                    masked[0] >= omniscient[0]
                    and masked[1] >= omniscient[1]
                    and masked[2] >= omniscient[2]
                ):
                    assert masked[3] >= omniscient[3]
                    checked_ordered_pairs += 1

    print(
        json.dumps(
            {
                "roots": [str(root) for root in roots],
                "checked_reachable_states": checked_states,
                "checked_ordered_pairs": checked_ordered_pairs,
                "identity": (
                    "q_clamped=max(q_raw,l,(c_raw+s*l)/(1+s))"
                ),
                "conclusion": (
                    "raw-current, raw-extrapolate, and retracted-lower order "
                    "imply post-clamp current and extrapolate order"
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
