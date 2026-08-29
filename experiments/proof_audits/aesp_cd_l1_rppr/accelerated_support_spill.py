#!/usr/bin/env python3
"""Exact two-coordinate support spill under projected Nesterov acceleration."""

from __future__ import annotations

from fractions import Fraction as F

from experiments.proof_audits import note_tex_source


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum(entry * value for entry, value in zip(row, vector, strict=True)) for row in matrix]


def projected_step(hessian: list[list[F]], rhs: list[F], point: list[F]) -> list[F]:
    gradient = [value - target for value, target in zip(matvec(hessian, point), rhs, strict=True)]
    return [max(point[i] - gradient[i], F(0)) for i in range(len(point))]


def exact_spill() -> None:
    # Rotate diag(1,1/4) by the rational orthogonal pair (12/13,5/13).
    # Thus L=1, mu=1/4, and critical strongly-convex momentum is beta=1/3.
    hessian = [[F(601, 676), F(-45, 169)], [F(-45, 169), F(61, 169)]]
    rhs = [F(1), F(-1, 3)]
    exact = [F(676, 601), F(0)]
    assert matvec(hessian, exact)[0] == rhs[0]
    assert matvec(hessian, exact)[1] - rhs[1] == F(61, 1803) > 0

    zero = [F(0), F(0)]
    first = projected_step(hessian, rhs, zero)
    assert first == [F(1), F(0)]
    assert first[0] < exact[0]

    beta = F(1, 3)
    extrapolated = [first[i] + beta * (first[i] - zero[i]) for i in range(2)]
    assert extrapolated == [F(4, 3), F(0)]
    second = projected_step(hessian, rhs, extrapolated)
    assert second == [F(194, 169), F(11, 507)]
    assert second[0] > exact[0]
    assert second[1] > 0 == exact[1]


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-accelerated-support-spill}" in source
    exact_spill()
    print("PASS projected-acceleration support spill")
    print("  spectrum={1,1/4}, beta=1/3")
    print("  true support={0}, second projected support={0,1}")
    print("  scope: sparse scratch containment STOP, not an acceleration lower bound")


if __name__ == "__main__":
    main()
