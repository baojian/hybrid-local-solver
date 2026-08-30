#!/usr/bin/env python3
"""100-digit audit of the threshold-batch Cholesky theorem.

The proof is in ``main.tex``. This dependency-free Decimal audit checks the
factor ordering, inverse ordering, singular-value bounds, causal forcing,
face-gap identity, and theorem bound on small canonical paths and stars. It
complements the broader double-precision grid in ``verify_batch_depth.py``.
"""

from __future__ import annotations

from decimal import Decimal, getcontext


getcontext().prec = 100
D = Decimal
TOL = D("1e-70")


def zeros(rows: int, columns: int) -> list[list[Decimal]]:
    return [[D(0) for _ in range(columns)] for _ in range(rows)]


def transpose(matrix: list[list[Decimal]]) -> list[list[Decimal]]:
    return [list(column) for column in zip(*matrix, strict=True)]


def matmul(left: list[list[Decimal]], right: list[list[Decimal]]) -> list[list[Decimal]]:
    right_transpose = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in right_transpose]
        for row in left
    ]


def matvec(matrix: list[list[Decimal]], vector: list[Decimal]) -> list[Decimal]:
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix]


def solve(matrix: list[list[Decimal]], vector: list[Decimal]) -> list[Decimal]:
    size = len(vector)
    augmented = [row[:] + [value] for row, value in zip(matrix, vector, strict=True)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        assert abs(augmented[pivot][column]) > TOL
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        for entry in range(column, size + 1):
            augmented[column][entry] /= pivot_value
        for row in range(size):
            if row == column:
                continue
            multiplier = augmented[row][column]
            for entry in range(column, size + 1):
                augmented[row][entry] -= multiplier * augmented[column][entry]
    return [augmented[row][-1] for row in range(size)]


def inverse(matrix: list[list[Decimal]]) -> list[list[Decimal]]:
    size = len(matrix)
    columns = []
    for index in range(size):
        unit = [D(0) for _ in range(size)]
        unit[index] = D(1)
        columns.append(solve(matrix, unit))
    return transpose(columns)


def cholesky(matrix: list[list[Decimal]]) -> list[list[Decimal]]:
    size = len(matrix)
    factor = zeros(size, size)
    for row in range(size):
        for column in range(row + 1):
            value = matrix[row][column] - sum(
                factor[row][index] * factor[column][index] for index in range(column)
            )
            if row == column:
                assert value > 0
                factor[row][column] = value.sqrt()
            else:
                factor[row][column] = value / factor[column][column]
    return factor


def symmetric_eigenvalues(matrix: list[list[Decimal]]) -> list[Decimal]:
    """Jacobi eigenvalues, used only as a high-precision falsification check."""

    work = [row[:] for row in matrix]
    size = len(work)
    for _ in range(200 * size * size):
        row, column = max(
            ((i, j) for i in range(size) for j in range(i + 1, size)),
            key=lambda pair: abs(work[pair[0]][pair[1]]),
            default=(0, 0),
        )
        if row == column or abs(work[row][column]) < TOL:
            break
        off = work[row][column]
        tau = (work[column][column] - work[row][row]) / (2 * off)
        sign = D(1) if tau >= 0 else D(-1)
        tangent = sign / (abs(tau) + (1 + tau * tau).sqrt())
        cosine = 1 / (1 + tangent * tangent).sqrt()
        sine = tangent * cosine
        old_row = work[row][row]
        old_column = work[column][column]
        work[row][row] = old_row - tangent * off
        work[column][column] = old_column + tangent * off
        work[row][column] = work[column][row] = D(0)
        for index in range(size):
            if index in (row, column):
                continue
            row_value = work[row][index]
            column_value = work[column][index]
            work[row][index] = work[index][row] = cosine * row_value - sine * column_value
            work[column][index] = work[index][column] = sine * row_value + cosine * column_value
    return sorted(work[index][index] for index in range(size))


def path_graph(vertices: int) -> list[list[Decimal]]:
    adjacency = zeros(vertices, vertices)
    for vertex in range(vertices - 1):
        adjacency[vertex][vertex + 1] = D(1)
        adjacency[vertex + 1][vertex] = D(1)
    return adjacency


def star_graph(vertices: int) -> list[list[Decimal]]:
    adjacency = zeros(vertices, vertices)
    for vertex in range(1, vertices):
        adjacency[0][vertex] = D(1)
        adjacency[vertex][0] = D(1)
    return adjacency


def pagerank_lcp(
    adjacency: list[list[Decimal]], alpha: Decimal, rho: Decimal, seed: int
) -> tuple[list[list[Decimal]], list[Decimal], list[Decimal]]:
    vertices = len(adjacency)
    degrees = [sum(row) for row in adjacency]
    matrix = zeros(vertices, vertices)
    for row in range(vertices):
        matrix[row][row] = (1 + alpha) / 2
        for column in range(vertices):
            if adjacency[row][column]:
                matrix[row][column] -= (
                    ((1 - alpha) / 2)
                    * adjacency[row][column]
                    / (degrees[row] * degrees[column]).sqrt()
                )
    linear = [-alpha * rho * degree.sqrt() for degree in degrees]
    linear[seed] += alpha / degrees[seed].sqrt()
    return matrix, linear, degrees


def principal(
    matrix: list[list[Decimal]], rows: list[int], columns: list[int]
) -> list[list[Decimal]]:
    return [[matrix[row][column] for column in columns] for row in rows]


def face_solution(
    matrix: list[list[Decimal]], linear: list[Decimal], active: list[int]
) -> list[Decimal]:
    point = [D(0) for _ in linear]
    solution = solve(principal(matrix, active, active), [linear[index] for index in active])
    for position, index in enumerate(active):
        point[index] = solution[position]
    return point


def residual(
    matrix: list[list[Decimal]], linear: list[Decimal], point: list[Decimal]
) -> list[Decimal]:
    return [a - b for a, b in zip(linear, matvec(matrix, point), strict=True)]


def threshold_partition(
    matrix: list[list[Decimal]],
    linear: list[Decimal],
    seed: int,
    threshold: Decimal,
) -> tuple[list[list[int]], list[list[Decimal]], int]:
    blocks = [[seed]]
    active = [seed]
    faces = [face_solution(matrix, linear, active)]
    while True:
        current = residual(matrix, linear, faces[-1])
        new = [
            index
            for index in range(len(linear))
            if index not in active and current[index] > threshold
        ]
        if not new:
            break
        blocks.append(new)
        active.extend(new)
        faces.append(face_solution(matrix, linear, active))
    declared_faces = len(faces)
    while True:
        current = residual(matrix, linear, faces[-1])
        new = [
            index for index in range(len(linear)) if index not in active and current[index] > TOL
        ]
        if not new:
            break
        blocks.append(new)
        active.extend(new)
        faces.append(face_solution(matrix, linear, active))
    return blocks, faces, declared_faces


def block_ranges(blocks: list[list[int]]) -> list[range]:
    ranges = []
    start = 0
    for block in blocks:
        ranges.append(range(start, start + len(block)))
        start += len(block)
    return ranges


def audit_instance(
    adjacency: list[list[Decimal]],
    alpha: Decimal,
    rho: Decimal,
    seed: int,
    threshold: Decimal,
) -> tuple[Decimal, int]:
    matrix, linear, _ = pagerank_lcp(adjacency, alpha, rho, seed)
    blocks, faces, declared_faces = threshold_partition(matrix, linear, seed, threshold)
    support = [index for block in blocks for index in block]
    ranges = block_ranges(blocks)
    q_support = principal(matrix, support, support)
    rhs = [linear[index] for index in support]
    factor = cholesky(q_support)
    for row in range(len(factor)):
        for column in range(row):
            assert factor[row][column] <= TOL

    bidiagonal = zeros(len(factor), len(factor))
    for block_index, current in enumerate(ranges):
        for row in current:
            for column in current:
                bidiagonal[row][column] = factor[row][column]
        if block_index:
            for row in current:
                for column in ranges[block_index - 1]:
                    bidiagonal[row][column] = factor[row][column]

    inverse_full = inverse(factor)
    inverse_bidiagonal = inverse(bidiagonal)
    for row in range(len(factor)):
        for column in range(len(factor)):
            assert inverse_bidiagonal[row][column] >= -TOL
            assert inverse_bidiagonal[row][column] <= inverse_full[row][column] + TOL

    gram = matmul(transpose(bidiagonal), bidiagonal)
    eigenvalues = symmetric_eigenvalues(gram)
    assert eigenvalues[0] >= alpha - TOL
    assert eigenvalues[-1] <= D(2) + TOL

    transformed = solve(factor, rhs)
    assert min(transformed) >= -TOL
    forcing = matvec(bidiagonal, transformed)
    for coordinate in ranges[0]:
        assert abs(forcing[coordinate] - rhs[coordinate]) <= TOL
    for current in ranges[1:]:
        assert max(forcing[coordinate] for coordinate in current) <= threshold + TOL

    q_alpha = ((2 / alpha).sqrt() - 1) / ((2 / alpha).sqrt() + 1)
    optimum = faces[-1]
    maximum_ratio = D(0)
    for block_index, face in enumerate(faces[:declared_faces]):
        error = [a - b for a, b in zip(optimum, face, strict=True)]
        gap = sum(a * b for a, b in zip(error, matvec(matrix, error), strict=True)) / 2
        tail = sum(
            (
                transformed[coordinate] ** 2
                for current in ranges[block_index + 1 :]
                for coordinate in current
            ),
            D(0),
        ) / D(2)
        assert abs(gap - tail) <= TOL
        bound = 8 * q_alpha ** (2 * block_index) + threshold**2 / (alpha * rho)
        assert gap <= bound + TOL
        maximum_ratio = max(maximum_ratio, gap / bound)
    return maximum_ratio, len(blocks)


def main() -> None:
    cases = 0
    largest_ratio = D(0)
    largest_blocks = 0
    for vertices in (4, 7, 10):
        for adjacency, seeds in (
            (path_graph(vertices), (0, vertices // 2)),
            (star_graph(vertices), (0, vertices - 1)),
        ):
            for seed in seeds:
                degree = sum(adjacency[seed])
                for alpha in map(D, ("0.03", "0.2", "0.7")):
                    for rho_fraction in map(D, ("0.02", "0.2", "0.6")):
                        rho = rho_fraction / degree
                        for threshold_fraction in map(D, ("0", "0.001")):
                            ratio, blocks = audit_instance(
                                adjacency,
                                alpha,
                                rho,
                                seed,
                                threshold_fraction * alpha,
                            )
                            cases += 1
                            largest_ratio = max(largest_ratio, ratio)
                            largest_blocks = max(largest_blocks, blocks)
    print(f"100-digit path/star cases checked: {cases}")
    print(f"largest admission-block count: {largest_blocks}")
    print(f"largest exact-gap/theorem-bound ratio: {largest_ratio:.18g}")
    print("verdict: all high-precision factor, forcing, gap, and bound checks passed")


if __name__ == "__main__":
    main()
