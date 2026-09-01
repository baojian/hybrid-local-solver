#!/usr/bin/env python3
"""Exact stop: reachable clamping/pushing need not preserve MomentumFlux.

Both paired states use the true NAG raw-auxiliary formula.  Raw current,
raw extrapolate, and retracted lower are ordered, and the two-coordinate
momentum-flux cone is strict before clamping.  The reachable clamp preserves
current/extrapolate order, but reverses one flux margin to -1/6.  A common
retained-form Stieltjes matrix/load makes both lowers certified; one legal
masked diagonal push still leaves the margin negative at -2/15.

The states are not asserted reachable from the canonical zero-start source
chronology, so this scopes the remaining history theorem rather than refuting
the enhanced algorithm.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


def raw_auxiliary(root: F, old_current: F, raw_current: F) -> F:
    return (raw_current - (1 - root) * old_current) / root


def main() -> None:
    root = F(1, 2)
    coupling = F(1, 8)

    omniscient_old_lower = (F(0), F(2))
    omniscient_old_current = (F(0), F(5))
    omniscient_raw_current = (F(3), F(0))
    omniscient_fresh_candidate = (F(0), F(-1))

    masked_old_lower = (F(4), F(5, 2))
    masked_old_current = (F(6), F(4))
    masked_raw_current = (F(5), F(3))
    masked_fresh_candidate = (F(9, 2), F(2))

    def build(
        old_lower: tuple[F, F],
        old_current: tuple[F, F],
        current: tuple[F, F],
        candidate: tuple[F, F],
    ) -> dict[str, tuple[F, F]]:
        assert all(c >= ell >= 0 for c, ell in zip(old_current, old_lower))
        assert all(v <= c for v, c in zip(candidate, current))
        auxiliary = tuple(
            raw_auxiliary(root, old_current[i], current[i]) for i in range(2)
        )
        lower = tuple(
            max(old_lower[i], candidate[i], F(0)) for i in range(2)
        )
        extrapolate = tuple(
            (current[i] + root * auxiliary[i]) / (1 + root)
            for i in range(2)
        )
        clamped_current = tuple(max(current[i], lower[i]) for i in range(2))
        clamped_auxiliary = tuple(
            max(auxiliary[i], lower[i]) for i in range(2)
        )
        clamped_extrapolate = tuple(
            (clamped_current[i] + root * clamped_auxiliary[i]) / (1 + root)
            for i in range(2)
        )
        return {
            "raw_current": current,
            "raw_auxiliary": auxiliary,
            "lower": lower,
            "raw_extrapolate": extrapolate,
            "clamped_current": clamped_current,
            "clamped_auxiliary": clamped_auxiliary,
            "clamped_extrapolate": clamped_extrapolate,
        }

    omniscient = build(
        omniscient_old_lower,
        omniscient_old_current,
        omniscient_raw_current,
        omniscient_fresh_candidate,
    )
    masked = build(
        masked_old_lower,
        masked_old_current,
        masked_raw_current,
        masked_fresh_candidate,
    )

    def gaps(prefix: str) -> tuple[tuple[F, F], tuple[F, F], tuple[F, F]]:
        current = tuple(
            masked[f"{prefix}current"][i] - omniscient[f"{prefix}current"][i]
            for i in range(2)
        )
        auxiliary = tuple(
            masked[f"{prefix}auxiliary"][i]
            - omniscient[f"{prefix}auxiliary"][i]
            for i in range(2)
        )
        extrapolate = tuple(
            masked[f"{prefix}extrapolate"][i]
            - omniscient[f"{prefix}extrapolate"][i]
            for i in range(2)
        )
        return current, auxiliary, extrapolate

    raw_current_gap, raw_auxiliary_gap, raw_extrapolate_gap = gaps("raw_")
    clamp_current_gap, clamp_auxiliary_gap, clamp_extrapolate_gap = gaps(
        "clamped_"
    )
    lower_gap = tuple(
        masked["lower"][i] - omniscient["lower"][i] for i in range(2)
    )

    def flux(auxiliary_gap: tuple[F, F], extrapolate_gap: tuple[F, F]) -> tuple[F, F]:
        return tuple(
            root * (1 - root) * auxiliary_gap[i]
            + 2 * coupling * extrapolate_gap[1 - i]
            for i in range(2)
        )

    raw_flux = flux(raw_auxiliary_gap, raw_extrapolate_gap)
    clamped_flux = flux(clamp_auxiliary_gap, clamp_extrapolate_gap)

    assert min(raw_current_gap) >= 0
    assert min(raw_extrapolate_gap) >= 0
    assert min(lower_gap) >= 0
    assert raw_flux == (F(7, 12), F(23, 12))
    assert min(clamp_current_gap) >= 0
    assert min(clamp_extrapolate_gap) >= 0
    assert clamped_flux == (F(-1, 6), F(1, 3))

    # This is B=L(I-R) for s=1/2, L=8/7, diagonal R=3/8, and
    # K_12=K_21=1/8.  The off-diagonal -1/7 is a canonical normalized
    # principal coupling for adjacent ambient-degree-three vertices.
    matrix = ((F(5, 7), F(-1, 7)), (F(-1, 7), F(5, 7)))

    def matvec(vector: tuple[F, F]) -> tuple[F, F]:
        return tuple(
            sum(matrix[i][j] * vector[j] for j in range(2))
            for i in range(2)
        )

    masked_residual = (F(0), F(2, 7))
    load = tuple(
        matvec(masked["lower"])[i] + masked_residual[i] for i in range(2)
    )
    omniscient_residual = tuple(
        load[i] - matvec(omniscient["lower"])[i] for i in range(2)
    )
    assert omniscient_residual == (F(22, 7), F(0))
    assert min(masked_residual) >= 0 and min(omniscient_residual) >= 0

    pushed_lower = tuple(
        masked["lower"][i] + masked_residual[i] / matrix[i][i]
        for i in range(2)
    )
    pushed_current = tuple(
        max(masked["clamped_current"][i], pushed_lower[i]) for i in range(2)
    )
    pushed_auxiliary = tuple(
        max(masked["clamped_auxiliary"][i], pushed_lower[i]) for i in range(2)
    )
    pushed_extrapolate = tuple(
        (pushed_current[i] + root * pushed_auxiliary[i]) / (1 + root)
        for i in range(2)
    )
    pushed_auxiliary_gap = tuple(
        pushed_auxiliary[i] - omniscient["clamped_auxiliary"][i]
        for i in range(2)
    )
    pushed_extrapolate_gap = tuple(
        pushed_extrapolate[i] - omniscient["clamped_extrapolate"][i]
        for i in range(2)
    )
    pushed_flux = flux(pushed_auxiliary_gap, pushed_extrapolate_gap)
    assert pushed_lower == (F(9, 2), F(29, 10))
    assert min(pushed_extrapolate_gap) >= 0
    assert pushed_flux == (F(-2, 15), F(13, 30))

    def strings(values: tuple[F, F]) -> list[str]:
        return [str(value) for value in values]

    print(
        json.dumps(
            {
                "root": str(root),
                "off_diagonal_K": str(coupling),
                "raw_current_gap": strings(raw_current_gap),
                "raw_extrapolate_gap": strings(raw_extrapolate_gap),
                "lower_gap": strings(lower_gap),
                "raw_flux": strings(raw_flux),
                "clamped_current_gap": strings(clamp_current_gap),
                "clamped_extrapolate_gap": strings(clamp_extrapolate_gap),
                "clamped_flux": strings(clamped_flux),
                "retained_matrix": [
                    [str(value) for value in row] for row in matrix
                ],
                "common_load": strings(load),
                "omniscient_lower_residual": strings(omniscient_residual),
                "masked_lower_residual": strings(masked_residual),
                "pushed_lower": strings(pushed_lower),
                "pushed_extrapolate_gap": strings(pushed_extrapolate_gap),
                "pushed_flux": strings(pushed_flux),
                "conclusion": (
                    "reachable clamp and one certified diagonal push preserve "
                    "current/extrapolate order but do not generically preserve "
                    "MomentumFlux"
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
