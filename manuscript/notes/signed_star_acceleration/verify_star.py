"""Exact-rational audit for the signed-star acceleration note.

This script is deliberately independent of NumPy/SciPy.  It verifies the
reduced dynamics and closed forms; the LaTeX proofs remain authoritative.
"""

from __future__ import annotations

from fractions import Fraction


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def check_cell(t: Fraction, eps: Fraction) -> None:
    alpha = t * t
    c_alpha = (1 - alpha) / (1 + alpha)
    gamma_alpha = 1 - c_alpha
    lam = (1 - t) / (1 + t)
    omega = 1 + lam * lam
    m = floor_fraction(1 / (8 * eps))
    k_stop = ceil_fraction(2 / t)

    assert m >= 1 / (16 * eps)
    assert 1 - omega == -(lam * lam)
    assert c_alpha * omega == 2 * lam
    assert 1 - c_alpha * lam == 2 * t / (1 + t * t)
    assert 1 + c_alpha == 2 / (1 + t * t)

    # The squared fast-mode displacement cap from the energy proof.
    phi0 = alpha / (2 * m)
    mu_fast = 1 + c_alpha
    cap_squared_from_energy = 16 * m * phi0 / mu_fast
    assert cap_squared_from_energy == 4 * alpha * (1 + alpha)

    # Exact reduced full-state simulation.
    center = gamma_alpha
    leaves = Fraction(0)
    for k in range(k_stop + 1):
        denom = 1 - c_alpha * c_alpha
        center_error = (center + c_alpha * leaves) / denom
        leaf_error_sum = (leaves + c_alpha * center) / denom
        semantic_error = max(abs(center_error), abs(leaf_error_sum)) / m
        closed_form = lam**k * (1 + t * t + 2 * t * k) / (2 * m)
        assert semantic_error == closed_form

        if k >= 1:
            positive_layer = gamma_alpha * (k + 1) * lam**k
            negative_layer = -gamma_alpha * k * lam ** (k + 1)
            assert sorted((center, leaves)) == sorted((positive_layer, negative_layer))

        if k == k_stop:
            assert semantic_error <= eps
            break

        if k % 2 == 0:  # center block
            old_center = center
            center = (1 - omega) * old_center
            leaves += c_alpha * omega * old_center
        else:  # all-leaves block
            old_leaves = leaves
            leaves = (1 - omega) * old_leaves
            center += c_alpha * omega * old_leaves


def main() -> None:
    cells = 0
    for inv_t in (2, 3, 4, 8, 16, 32, 64):
        t = Fraction(1, inv_t)
        for inv_eps in (16, 32, 128, 512):
            check_cell(t, Fraction(1, inv_eps))
            cells += 1
    print(f"exact signed-star checks passed: {cells} parameter cells")


if __name__ == "__main__":
    main()
