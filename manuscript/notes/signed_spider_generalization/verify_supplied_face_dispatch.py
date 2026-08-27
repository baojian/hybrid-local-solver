"""Exact audits for the supplied-face CG/Chebyshev dispatch."""

from __future__ import annotations

from fractions import Fraction

Matrix = list[list[Fraction]]


def identity(size: int) -> Matrix:
    """Return an exact identity matrix."""
    return [[Fraction(row == column) for column in range(size)] for row in range(size)]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    """Multiply two exact matrices."""
    rows = len(left)
    inner = len(right)
    columns = len(right[0])
    return [
        [
            sum((left[row][index] * right[index][column] for index in range(inner)), Fraction())
            for column in range(columns)
        ]
        for row in range(rows)
    ]


def matvec(matrix: Matrix, vector: list[Fraction]) -> list[Fraction]:
    """Multiply an exact matrix and vector."""
    return [
        sum((entry * vector[column] for column, entry in enumerate(row)), Fraction())
        for row in matrix
    ]


def inverse(matrix: Matrix) -> Matrix:
    """Invert an exact nonsingular matrix by Gauss--Jordan elimination."""
    size = len(matrix)
    augmented = [row[:] + unit[:] for row, unit in zip(matrix, identity(size), strict=True)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(augmented[row], augmented[column], strict=True)
            ]
    return [row[size:] for row in augmented]


def chebyshev(degree: int, value: Fraction) -> Fraction:
    """Evaluate T_degree(value) exactly by its three-term recurrence."""
    if degree == 0:
        return Fraction(1)
    previous = Fraction(1)
    current = value
    for _ in range(1, degree):
        previous, current = current, 2 * value * current - previous
    return current


def check_chebyshev_identity() -> int:
    """Check the exact denominator identity at rational square roots of alpha."""
    cells = 0
    for root_alpha in (Fraction(1, 2), Fraction(1, 3), Fraction(1, 5), Fraction(2, 7)):
        alpha = root_alpha * root_alpha
        outside = (1 + alpha) / (1 - alpha)
        chi = (1 - root_alpha) / (1 + root_alpha)
        for degree in range(0, 13):
            inverse_denominator = 1 / chebyshev(degree, outside)
            closed_form = 2 * chi**degree / (1 + chi ** (2 * degree))
            assert inverse_denominator == closed_form
            assert inverse_denominator <= 2 * chi**degree
            cells += 1
    return cells


def check_load_bound() -> int:
    """Audit the single-seed shifted-load bound under rho*vol(U)<=1."""
    cells = 0
    for seed_degree in range(1, 8):
        for volume in range(seed_degree, 25):
            for denominator in range(volume, 2 * volume + 1):
                rho = Fraction(1, denominator)
                scaled_norm_sq = (1 - rho * seed_degree) ** 2 / seed_degree
                scaled_norm_sq += rho * rho * (volume - seed_degree)
                assert rho * volume <= 1
                assert scaled_norm_sq <= 1 + rho <= 2
                cells += 1
    return cells


def check_semantic_inverse_bound() -> int:
    """Check the M-matrix row-sum certificate on principal cycle faces."""
    cells = 0
    for alpha in (Fraction(1, 9), Fraction(1, 4), Fraction(4, 9)):
        diagonal = (1 + alpha) / 2
        off_diagonal = -(1 - alpha) / 4
        # Three consecutive vertices of a degree-two cycle, with Dirichlet
        # edges at the two ends.  D is scalar, so row and symmetric coordinates agree.
        operator = [
            [diagonal, off_diagonal, Fraction()],
            [off_diagonal, diagonal, off_diagonal],
            [Fraction(), off_diagonal, diagonal],
        ]
        operator_inverse = inverse(operator)
        assert all(entry >= 0 for row in operator_inverse for entry in row)
        row_sums = [sum(row, Fraction()) for row in operator_inverse]
        assert max(row_sums) <= 1 / alpha
        for residual in (
            [Fraction(1), Fraction(-1), Fraction(2)],
            [alpha, -alpha, alpha],
            [Fraction(-2), Fraction(), Fraction(1)],
        ):
            error = matvec(operator_inverse, residual)
            assert max(map(abs, error)) <= max(map(abs, residual)) / alpha
            cells += 1
    return cells


def check_annihilator_off_by_one() -> int:
    """Check degree-n error annihilation and degree-(n-1) solution interpolation."""
    eigenvalues = (Fraction(1, 3), Fraction(2, 3), Fraction(5, 6))
    operator: Matrix = [
        [Fraction(1, 2), Fraction(-1, 6), Fraction()],
        [Fraction(-1, 6), Fraction(1, 2), Fraction()],
        [Fraction(), Fraction(), Fraction(5, 6)],
    ]
    annihilator = identity(3)
    coefficients = [Fraction(1)]
    for eigenvalue in eigenvalues:
        factor = identity(3)
        for row in range(3):
            for column in range(3):
                factor[row][column] -= operator[row][column] / eigenvalue
        annihilator = matmul(annihilator, factor)
        following = [Fraction() for _ in range(len(coefficients) + 1)]
        for degree, coefficient in enumerate(coefficients):
            following[degree] += coefficient
            following[degree + 1] -= coefficient / eigenvalue
        coefficients = following
    assert annihilator == [[Fraction() for _ in range(3)] for _ in range(3)]

    # q_2(Q)b = Q^{-1}b follows from I-a_3(Q)=Q q_2(Q).
    right_hand_side = [Fraction(2), Fraction(-1), Fraction(3)]
    exact_solution = matvec(inverse(operator), right_hand_side)
    quotient = [-coefficient for coefficient in coefficients[1:]]
    # Horner evaluation of q_2(Q)b uses powers through Q^2 only.
    recovered = [Fraction() for _ in right_hand_side]
    for coefficient in reversed(quotient):
        recovered = matvec(operator, recovered)
        recovered = [
            value + coefficient * entry
            for value, entry in zip(recovered, right_hand_side, strict=True)
        ]
    assert recovered == exact_solution
    # The explicit check above locks the iteration off-by-one: three error
    # factors, but a solution polynomial of degree at most two.
    return 2


def main() -> None:
    """Run all exact supplied-face audits."""
    chebyshev_cells = check_chebyshev_identity()
    load_cells = check_load_bound()
    semantic_cells = check_semantic_inverse_bound()
    annihilator_cells = check_annihilator_off_by_one()
    print(
        "supplied_face_dispatch=pass "
        f"chebyshev_cells={chebyshev_cells} load_cells={load_cells} "
        f"semantic_cells={semantic_cells} annihilator_cells={annihilator_cells}"
    )


if __name__ == "__main__":
    main()
