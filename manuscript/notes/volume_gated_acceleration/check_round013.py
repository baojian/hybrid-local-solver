#!/usr/bin/env python3
"""Finite exact scaffolding for the withdrawn Round-013 path candidate.

These checks cover only m=2,4,8 and do not prove an asymptotic terminal-face
lower bound.
"""

from fractions import Fraction
from math import comb


def apply_h(z, degrees, alpha):
    """Apply D^{-1/2} Q D^{1/2} on the represented prefix."""
    eta = (1 - alpha) / 2
    a = (1 + alpha) / 2
    out = []
    for i, value in enumerate(z):
        neighbor_sum = Fraction(0)
        if i:
            neighbor_sum += z[i - 1]
        if i + 1 < len(z):
            neighbor_sum += z[i + 1]
        out.append(a * value - eta * neighbor_sum / degrees[i])
    return out


def cbar(length, alpha, rho):
    out = [-alpha * rho for _ in range(length)]
    out[0] += alpha
    return out


def residual(z, degrees, alpha, rho):
    return [u - v for u, v in zip(apply_h(z, degrees, alpha), cbar(len(z), alpha, rho))]


def restricted_optimum(length, degrees, alpha, rho):
    """Rational Thomas solve for the normalized restricted optimum."""
    eta = (1 - alpha) / 2
    a = (1 + alpha) / 2
    rhs = cbar(length, alpha, rho)
    diag = [a for _ in range(length)]
    upper = [-eta / degrees[i] for i in range(length - 1)]
    lower = [-eta / degrees[i] for i in range(1, length)]
    for i in range(1, length):
        multiplier = lower[i - 1] / diag[i - 1]
        diag[i] -= multiplier * upper[i - 1]
        rhs[i] -= multiplier * rhs[i - 1]
    answer = [Fraction(0) for _ in range(length)]
    answer[-1] = rhs[-1] / diag[-1]
    for i in range(length - 2, -1, -1):
        answer[i] = (rhs[i] - upper[i] * answer[i + 1]) / diag[i]
    return answer


def one_step(p, v, degrees, q, rho):
    alpha = q * q
    y = [(x + q * center) / (1 + q) for x, center in zip(p, v)]
    grad = residual(y, degrees, alpha, rho)
    raw = [x - g for x, g in zip(y, grad)]
    assert min(raw) >= 0, "the nonnegativity projection unexpectedly activated"
    p_next = raw
    v_next = [x_next + (1 - q) * (x_next - x) / q for x_next, x in zip(p_next, p)]
    return p_next, v_next


def check_family(n):
    assert n % 16 == 0
    q = Fraction(1, n)
    alpha = q * q
    rho = tau = q / 5
    edge_count = n // 16
    degrees = [Fraction(1)] + [Fraction(2)] * (edge_count - 1) + [Fraction(1)]

    p = [Fraction(0)]
    v = [Fraction(0)]
    for face_size in range(1, edge_count + 1):
        p_next, v_next = one_step(p, v, degrees[:face_size], q, rho)
        r_active = residual(p_next, degrees[:face_size], alpha, rho)
        delta = max(Fraction(0), max(r_active) / alpha)
        assert delta == 0, "the rapid-front exact envelope correction is nonzero"
        ell = [max(Fraction(0), x - delta) for x in p_next]
        next_index = face_size
        next_residual = -((1 - alpha) / 2) * ell[-1] / degrees[next_index] + alpha * rho
        assert next_residual < -alpha * tau, "the next singleton is not strongly admitted"

        old_optimum = restricted_optimum(face_size, degrees, alpha, rho)
        new_optimum = restricted_optimum(face_size + 1, degrees, alpha, rho)
        p = p_next + [Fraction(0)]
        v = [
            old_v + new_x - old_x
            for old_v, new_x, old_x in zip(
                v_next + [Fraction(0)],
                new_optimum,
                old_optimum + [Fraction(0)],
            )
        ]

    full_residual = residual(p, degrees, alpha, rho)
    middle = edge_count // 2
    packet_floor = (
        alpha * (1 - q) ** edge_count * Fraction(comb(edge_count, middle), 4 * (2**edge_count))
    )
    assert -full_residual[middle] >= packet_floor

    # Check the conditional full-face residual recurrence, the actual
    # unclipped global correction, and non-certification for a finite prefix.
    for _ in range(n // 2):
        r_p = residual(p, degrees, alpha, rho)
        r_v = residual(v, degrees, alpha, rho)
        p_next, v_next = one_step(p, v, degrees, q, rho)
        r_next = residual(p_next, degrees, alpha, rho)
        mixed = [(x + q * y) / (1 + q) for x, y in zip(r_p, r_v)]
        predicted = [x - y for x, y in zip(mixed, apply_h(mixed, degrees, alpha))]
        assert r_next == predicted

        delta = max(Fraction(0), max(r_next) / alpha)
        assert min(p_next) > delta, "the terminal safe-envelope subtraction clipped"
        assert min(p_next) - delta >= alpha / 8
        ell = [x - delta for x in p_next]
        r_ell = residual(ell, degrees, alpha, rho)
        assert r_ell == [x - alpha * delta for x in r_next]
        assert min(r_ell) < -alpha * tau, "the terminal face certified too early"
        p, v = p_next, v_next

    return edge_count, max(x.numerator.bit_length() for x in p)


def main():
    for n in (32, 64, 128):
        edge_count, numerator_bits = check_family(n)
        print(
            f"n={n}: exact q=1/{n}, edges={edge_count}, "
            f"finite admissions and {n // 2} terminal steps verified "
            f"(max numerator bits={numerator_bits})"
        )


if __name__ == "__main__":
    main()
