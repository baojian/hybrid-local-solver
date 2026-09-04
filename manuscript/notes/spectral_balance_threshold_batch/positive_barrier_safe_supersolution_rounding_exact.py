"""Exact checks for positive-barrier SafeSupersolution rounding examples."""

from fractions import Fraction


def matvec(
    matrix: tuple[tuple[Fraction, ...], ...],
    vector: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    """Multiply a rational matrix and vector."""
    return tuple(
        sum((entry * value for entry, value in zip(row, vector, strict=True)), Fraction())
        for row in matrix
    )


def add(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    """Add rational vectors."""
    return tuple(a + b for a, b in zip(left, right, strict=True))


def subtract(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    """Subtract rational vectors."""
    return tuple(a - b for a, b in zip(left, right, strict=True))


def dot(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
) -> Fraction:
    """Take a rational inner product."""
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction())


def residual(
    matrix: tuple[tuple[Fraction, ...], ...],
    offset: tuple[Fraction, ...],
    vector: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    """Evaluate the affine LCP residual."""
    return add(offset, matvec(matrix, vector))


def check_slow_mode_sensitivity() -> None:
    """Check that raw residual repair has the sharp inverse-alpha scale."""
    alpha = Fraction(1, 11)
    delta = Fraction(2, 7)
    diagonal = (1 + alpha) / 2
    off_diagonal = -(1 - alpha) / 2
    matrix = ((diagonal, off_diagonal), (off_diagonal, diagonal))
    h = (Fraction(1), Fraction(1))
    endpoint = h
    exact = h
    offset = tuple(-alpha * value for value in h)
    approximate = tuple((1 - delta) * value for value in h)

    assert matvec(matrix, h) == tuple(alpha * value for value in h)
    assert residual(matrix, offset, exact) == (Fraction(), Fraction())
    assert residual(matrix, offset, approximate) == tuple(-alpha * delta * value for value in h)

    gamma = max(
        Fraction(),
        *(max(-value / weight, Fraction()) for value, weight in zip(approximate, h, strict=True)),
        *(
            max(-value / (alpha * weight), Fraction())
            for value, weight in zip(residual(matrix, offset, approximate), h, strict=True)
        ),
    )
    assert gamma == delta
    repaired = tuple(
        min(cap, value + gamma * weight)
        for cap, value, weight in zip(endpoint, approximate, h, strict=True)
    )
    assert repaired == exact


def check_safe_cap_gap_increase() -> None:
    """Check that a supersolution cap is safe but can increase e^T F(e)."""
    matrix = (
        (Fraction(2, 3), Fraction(-1, 3)),
        (Fraction(-1, 3), Fraction(2, 3)),
    )
    offset = (Fraction(), Fraction(1))
    endpoint = (Fraction(3), Fraction())
    supersolution = (Fraction(3), Fraction(1))
    clipped = tuple(min(a, b) for a, b in zip(endpoint, supersolution, strict=True))

    endpoint_residual = residual(matrix, offset, endpoint)
    supersolution_residual = residual(matrix, offset, supersolution)
    clipped_residual = residual(matrix, offset, clipped)

    assert endpoint_residual == (Fraction(2), Fraction())
    assert supersolution_residual == (Fraction(5, 3), Fraction(2, 3))
    assert clipped == endpoint
    assert min(clipped_residual) >= 0
    assert dot(supersolution, supersolution_residual) == Fraction(17, 3)
    assert dot(clipped, clipped_residual) == Fraction(6)
    assert dot(clipped, clipped_residual) > dot(supersolution, supersolution_residual)


def check_augmented_ground_gap() -> None:
    """Check the signed extraction identity and augmented objective gap."""
    matrix = (
        (Fraction(2, 3), Fraction(-1, 3)),
        (Fraction(-1, 3), Fraction(2, 3)),
    )
    grounding = (Fraction(1, 3), Fraction(1, 3))
    offset = (Fraction(-2, 3), Fraction(4, 3))
    exact = (Fraction(1), Fraction())
    endpoint = (Fraction(2), Fraction(1))
    tau = Fraction(1, 5)
    ground_linear = dot(grounding, endpoint) + tau
    ground_laplacian = (
        (Fraction(2, 3), Fraction(-1, 3), Fraction(-1, 3)),
        (Fraction(-1, 3), Fraction(2, 3), Fraction(-1, 3)),
        (Fraction(-1, 3), Fraction(-1, 3), Fraction(2, 3)),
    )
    potential = (Fraction(1, 4), Fraction(3, 4))
    ground = Fraction(1, 2)
    signed = tuple(value - ground for value in potential)

    assert matvec(matrix, (Fraction(1), Fraction(1))) == grounding
    assert residual(matrix, offset, exact) == (Fraction(), Fraction(1))
    assert min(residual(matrix, offset, endpoint)) >= 0

    augmented = potential + (ground,)
    objective_augmented = (
        dot(augmented, matvec(ground_laplacian, augmented)) / 2
        + dot(offset, potential)
        + ground_linear * ground
    )
    objective_signed = dot(signed, matvec(matrix, signed)) / 2 + dot(offset, signed)
    split = objective_signed + ground * (sum(offset) + ground_linear)
    assert objective_augmented == split

    objective_exact = dot(exact, matvec(matrix, exact)) / 2 + dot(offset, exact)
    signed_error = subtract(signed, exact)
    energy_error = dot(signed_error, matvec(matrix, signed_error)) / 2
    assert objective_augmented - objective_exact >= energy_error + tau * ground


def check_zero_input_barrier_fails_abox_stop() -> None:
    """Check that BarrierCap needs an accurate input, even on one unit edge."""
    s = Fraction(1, 10)
    alpha = s * s
    rho = Fraction(1, 4)
    delta = s**4
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    matrix = ((diagonal, -coupling), (-coupling, diagonal))
    h = (Fraction(1), Fraction(1))
    load = (alpha * (1 - rho), -alpha * rho)
    original_optimum = (diagonal - rho, coupling - rho)

    exact_correction = (delta, Fraction())
    exact_residual = (Fraction(), delta)
    endpoint = (2 * delta, delta)
    inverse_residual = (s * s * coupling, s * s * diagonal)
    current = tuple(
        value - shift - delta
        for value, shift in zip(original_optimum, inverse_residual, strict=True)
    )
    trial = add(current, endpoint)
    estimate = add(current, tuple((1 + s) * value / s for value in endpoint))
    offset = subtract(load, matvec(matrix, trial))

    assert min(current) > 0
    assert min(subtract(estimate, current)) > 0
    assert matvec(matrix, original_optimum) == load
    assert offset == subtract(exact_residual, matvec(matrix, exact_correction))
    assert residual(matrix, offset, exact_correction) == exact_residual
    assert min(residual(matrix, offset, endpoint)) >= 0

    barrier = matvec(matrix, h)
    assert barrier == (alpha, alpha)
    approximate = (Fraction(), Fraction())
    approximate_residual = residual(matrix, offset, approximate)
    assert 2 * coupling * coupling - diagonal * diagonal == (1 - 6 * alpha + alpha * alpha) / 4
    assert coupling - diagonal * diagonal == (1 - 4 * alpha - alpha * alpha) / 4
    assert 2 * coupling * coupling > diagonal * diagonal
    assert coupling > diagonal * diagonal
    lower_ratio = coupling / diagonal
    upper_ratio = diagonal / coupling
    test_ratios = (
        (2 * lower_ratio + upper_ratio) / 3,
        (lower_ratio + 2 * upper_ratio) / 3,
    )
    for ratio_h in test_ratios:
        directional_barrier = matvec(matrix, (Fraction(1), ratio_h))
        assert min(directional_barrier) > 0
        directional_gamma = -approximate_residual[0] / directional_barrier[0]
        assert directional_gamma >= endpoint[0]
        assert directional_gamma * ratio_h >= endpoint[1]
    gamma = max(
        Fraction(),
        *(
            max(-value / weight, Fraction())
            for value, weight in zip(approximate_residual, barrier, strict=True)
        ),
    )
    assert gamma == diagonal * delta / alpha
    assert gamma >= max(endpoint)
    repaired = tuple(
        min(cap, value + gamma * weight)
        for cap, value, weight in zip(endpoint, approximate, h, strict=True)
    )
    assert repaired == endpoint

    repaired_residual = residual(matrix, offset, repaired)
    zeta = dot(repaired, repaired_residual)
    estimate_minus_repaired_point = subtract(estimate, current)
    allowance = (
        s
        * alpha
        * dot(
            estimate_minus_repaired_point,
            estimate_minus_repaired_point,
        )
        / 2
    )
    ratio = (1 + s) * zeta / allowance
    assert zeta == s**8 * (1 + 3 * s * s)
    assert allowance == Fraction(5, 2) * s**9 * (1 + s) ** 2
    assert ratio == 2 * (1 + 3 * s * s) / (5 * s * (1 + s))
    assert ratio > 1


def check_unsafe_prox_center_accuracy_floor() -> None:
    """Check the full-face gap between an unsafe prox and every safe output."""
    s = Fraction(1, 10)
    alpha = s * s
    theta = (1 - s) / (1 + s)
    rho = Fraction(1, 4)
    epsilon = Fraction(1, 1000)
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    matrix = ((diagonal, -coupling), (-coupling, diagonal))
    proximal_matrix = (
        (diagonal + 1, -coupling),
        (-coupling, diagonal + 1),
    )
    h = (Fraction(1), Fraction(1))
    load = (alpha * (1 - rho), -alpha * rho)
    optimum = (diagonal - rho, coupling - rho)
    displacement = 2 * epsilon / theta
    current = tuple(value - epsilon for value in optimum)
    previous = tuple(value - epsilon - displacement for value in optimum)
    raw_center = add(current, tuple(theta * (x - y) for x, y in zip(current, previous)))
    raw_prox = tuple(value + epsilon / (1 + alpha) for value in optimum)

    assert min(previous) > 0
    assert all(value <= 0 for value in residual(matrix, tuple(-value for value in load), previous))
    assert all(value <= 0 for value in residual(matrix, tuple(-value for value in load), current))
    assert raw_center == tuple(value + epsilon for value in optimum)
    assert matvec(proximal_matrix, raw_prox) == add(load, raw_center)
    assert min(subtract(raw_prox, optimum)) > 0

    prox_error = subtract(optimum, raw_prox)
    objective_floor = dot(prox_error, matvec(proximal_matrix, prox_error)) / 2
    expected_floor = epsilon * epsilon * dot(h, h) / (2 * (1 + alpha))
    assert objective_floor == expected_floor


def main() -> None:
    """Run all exact checks."""
    check_slow_mode_sensitivity()
    check_safe_cap_gap_increase()
    check_augmented_ground_gap()
    check_zero_input_barrier_fails_abox_stop()
    check_unsafe_prox_center_accuracy_floor()
    print("positive-barrier SafeSupersolution rounding exact checks passed")


if __name__ == "__main__":
    main()
