#!/usr/bin/env python3
"""Exact scalar audit for the explicit-Cholesky expander STOP.

The theorem uses a spectral-expander family and a standard treewidth argument.
This script checks its normalization, margin constants, and exact clique
storage/pivot-update counts on a deterministic rational grid.  It is a
regression check, not a computational proof of graph expansion.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb


def audit_scale(n: int, gamma: Fraction) -> int:
    """Check one exact ``q=1/(2n)`` specialization."""
    assert n >= 2
    assert 0 < gamma <= 1
    q = Fraction(1, 2 * n)
    rho = tau = q / 5
    alpha = q * q
    beta = (1 - alpha) / (1 + alpha)

    assert 1 - beta == 2 * alpha / (1 + alpha)
    spectral_multiplier = (1 - beta) / (1 - beta * (1 - gamma))
    assert spectral_multiplier <= 2 * alpha / gamma

    ppr_floor = 2 * q - 2 * q * q / gamma
    normalized_rppr_floor = ppr_floor / 3 - rho
    margin = normalized_rppr_floor - tau
    assert margin == 4 * q / 15 - 2 * q * q / (3 * gamma)
    assert q < 2 * gamma / 5
    assert margin > 0

    assert alpha * (Fraction(1, 3) - rho) > 0
    product_scale = 1 / (rho * q)
    assert product_scale == 5 / (q * q) == 20 * n * n

    # A filled clique of order k stores binom(k,2) off-diagonals.  Ordinary
    # scalar Schur elimination performs sum_{j<k} binom(j,2)=binom(k,3)
    # pair updates inside that clique.
    k = max(3, n // 10)
    storage = comb(k, 2)
    pivot_updates = sum(comb(j, 2) for j in range(1, k))
    assert storage == k * (k - 1) // 2
    assert pivot_updates == comb(k, 3)
    return 1


def main() -> None:
    gamma_values = (Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1, 1))
    cells = 0
    for gamma in gamma_values:
        # This choice is strictly inside q < 2 gamma / 5 for every cell.
        first_n = 2 + 5 // (4 * gamma)
        for offset in (0, 1, 7, 31, 127):
            cells += audit_scale(first_n + offset, gamma)
    print(f"explicit-Cholesky expander STOP scalar audit: PASS ({cells} cells)")


if __name__ == "__main__":
    main()
