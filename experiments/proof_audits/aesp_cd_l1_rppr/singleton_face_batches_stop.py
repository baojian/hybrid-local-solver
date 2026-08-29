#!/usr/bin/env python3
"""Exact endpoint-path STOP for face-by-face restricted restarts.

On the calibrated P8 instance, every exact restricted prefix solve exposes
exactly one new boundary vertex.  Thus even admitting every certified
positive boundary key cannot batch the serial path frontier.
"""

from __future__ import annotations

from fractions import Fraction as F

from experiments.proof_audits import note_tex_source


Matrix = list[list[F]]
Vector = list[F]


def solve(matrix: Matrix, rhs: Vector) -> Vector:
    """Solve a small rational system by exact Gauss-Jordan elimination."""
    size = len(rhs)
    work = [row[:] + [value] for row, value in zip(matrix, rhs, strict=True)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        diagonal = work[column][column]
        work[column] = [entry / diagonal for entry in work[column]]
        for row in range(size):
            if row == column:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[column], strict=True)
                ]
    return [work[row][-1] for row in range(size)]


def path_instance() -> tuple[F, F, Matrix, Vector, list[int]]:
    """Return alpha, rho, the hat-coordinate Hessian/rhs, and degrees."""
    size = 8
    q = F(1, 8)
    alpha = q * q / (1 + q * q)
    rho = F(1, 56)
    degree = [1, *([2] * (size - 2)), 1]
    seed = [1, *([0] * (size - 1))]
    hessian = [[F(0)] * size for _ in range(size)]
    for vertex in range(size):
        hessian[vertex][vertex] = (1 + alpha) * degree[vertex] / 2
    for vertex in range(size - 1):
        hessian[vertex][vertex + 1] = -(1 - alpha) / 2
        hessian[vertex + 1][vertex] = -(1 - alpha) / 2
    rhs = [
        alpha * (seed[vertex] - rho * degree[vertex])
        for vertex in range(size)
    ]
    assert alpha == F(1, 65)
    return alpha, rho, hessian, rhs, degree


def check_singleton_batches() -> None:
    _, rho, hessian, rhs, degree = path_instance()
    size = len(rhs)
    batches = []
    face_volumes = []
    minimum_coordinate = None
    for endpoint in range(size):
        face = list(range(endpoint + 1))
        restricted = [[hessian[i][j] for j in face] for i in face]
        solution = solve(restricted, [rhs[i] for i in face])
        assert all(value > 0 for value in solution)
        local_minimum = min(solution)
        minimum_coordinate = (
            local_minimum
            if minimum_coordinate is None
            else min(minimum_coordinate, local_minimum)
        )
        padded = [*solution, *([F(0)] * (size - endpoint - 1))]
        residual = [
            rhs[i] - sum(hessian[i][j] * padded[j] for j in range(size))
            for i in range(size)
        ]
        assert all(residual[i] == 0 for i in face)
        positive_exterior = tuple(
            i for i in range(endpoint + 1, size) if residual[i] > 0
        )
        expected = (endpoint + 1,) if endpoint + 1 < size else ()
        assert positive_exterior == expected
        batches.append(positive_exterior)
        face_volumes.append(sum(degree[i] for i in face))

    assert rho == F(1, 56)
    assert batches == [(1,), (2,), (3,), (4,), (5,), (6,), (7,), ()]
    assert minimum_coordinate == F(204472165, 29579630696)
    assert face_volumes == [1, 3, 5, 7, 9, 11, 13, 14]
    assert sum(face_volumes) == 63
    assert face_volumes[-1] == 14


def check_source_scope() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert "prop:aesp-cd-face-by-face-volume-stop" in source
    assert "prop:aesp-cd-geometric-face-batches" in source
    assert "volume-doubling checkpoints" in source


def main() -> None:
    check_singleton_batches()
    check_source_scope()
    print("P8 singleton face-batch STOP passed")
    print("  q=1/8, alpha=1/65, rho=1/56, endpoint seed")
    print("  exact admitted keys: 1,2,3,4,5,6,7 one at a time")
    print("  cumulative prefix volume: 63; final path volume: 14")


if __name__ == "__main__":
    main()
