#!/usr/bin/env python3
"""Exact-trajectory/rational-interval P24 certificate for the 6/5 STOP.

It uses the explicit normalized-path cosine basis,
Machin's formula with alternating rational remainders for pi, and outward
rounding to a 10^-28 rational grid.  No floating-point spectral computation
enters the asserted inequalities.
"""

from __future__ import annotations

import importlib.util
import math
from fractions import Fraction as F
from pathlib import Path

from experiments.proof_audits import REPOSITORY_ROOT, note_tex_source


SCALE = 10**28
ZERO = (F(0), F(0))


def floor_grid(x: F) -> F:
    return F(x.numerator * SCALE // x.denominator, SCALE)


def ceil_grid(x: F) -> F:
    return -floor_grid(-x)


def outward(interval: tuple[F, F]) -> tuple[F, F]:
    return floor_grid(interval[0]), ceil_grid(interval[1])


def enclose(x: F) -> tuple[F, F]:
    return floor_grid(x), ceil_grid(x)


def add(a, b):
    return outward((a[0] + b[0], a[1] + b[1]))


def sub(a, b):
    return outward((a[0] - b[1], a[1] - b[0]))


def mul(a, b):
    products = tuple(a[i] * b[j] for i in (0, 1) for j in (0, 1))
    return outward((min(products), max(products)))


def inv(a):
    assert a[0] > 0
    return outward((1 / a[1], 1 / a[0]))


def div(a, b):
    return mul(a, inv(b))


def scale(c: F, a):
    return mul(enclose(c), a)


def square(a):
    if a[0] <= 0 <= a[1]:
        return outward((F(0), max(a[0] ** 2, a[1] ** 2)))
    return outward((min(a[0] ** 2, a[1] ** 2), max(a[0] ** 2, a[1] ** 2)))


def atan_bounds(inverse_denominator: int, terms: int = 30):
    z = F(1, inverse_denominator)
    partial = sum(
        ((-1 if j % 2 else 1) * z ** (2 * j + 1) / F(2 * j + 1) for j in range(terms)), F(0)
    )
    next_term = z ** (2 * terms + 1) / F(2 * terms + 1)
    # Odd partial sums are upper bounds, even partial sums lower bounds.
    return (partial, partial + next_term) if terms % 2 == 0 else (partial - next_term, partial)


def cosine_table(size: int):
    atan_5 = atan_bounds(5)
    atan_239 = atan_bounds(239)
    pi_interval = (16 * atan_5[0] - 4 * atan_239[1], 16 * atan_5[1] - 4 * atan_239[0])

    def cosine(k: int, terms: int = 30):
        x_interval = (F(k, size - 1) * pi_interval[0], F(k, size - 1) * pi_interval[1])
        midpoint = (x_interval[0] + x_interval[1]) / 2
        radius = (x_interval[1] - x_interval[0]) / 2
        partial = term = F(1)
        for j in range(1, terms + 1):
            term *= -midpoint * midpoint / F((2 * j - 1) * (2 * j))
            partial += term
        # Taylor theorem plus |cos x-cos y| <= |x-y|.
        remainder = abs(midpoint) ** (2 * terms + 1) / F(math.factorial(2 * terms + 1))
        return outward((partial - remainder - radius, partial + remainder + radius))

    return [cosine(k) for k in range(size)]


def load_engine(repo: Path):
    path = repo / "manuscript/claude-overnight-2026-08-24/w7_windowed/engine.py"
    spec = importlib.util.spec_from_file_location("window_engine", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-p24-low-start-stop}" in source
    engine = load_engine(REPOSITORY_ROOT)

    n = 24
    adjacency = engine.path_graph(n)
    instance = engine.Inst(adjacency, [F(1)] + [F(0)] * (n - 1), F(1, 24), F(1, 92))
    states = [[F(0)] * n]
    corrections = []
    previous = current = [F(0)] * n
    for _stage in range(94):
        increment = [current[i] - previous[i] for i in range(n)]
        trial = [current[i] + instance.beta * increment[i] for i in range(n)]
        support = [i for i in range(n) if trial[i] > 0]
        delta = F(0)
        for i in support:
            residual = instance.ct[i] - sum(instance.Qt[i][j] * trial[j] for j in support)
            if residual < 0:
                delta = max(delta, -residual / (instance.alpha * instance.d[i]))
        correction = [min(instance.beta * increment[i], delta) for i in range(n)]
        cap = max(instance.beta * value for value in increment)
        kind = "N" if delta == 0 else ("F" if delta >= cap else "P")
        shifted = [trial[i] - correction[i] for i in range(n)]
        following = instance.obstacle_solve(
            instance.ct, instance.kappa, shifted, warm=support or None
        )
        corrections.append((kind, correction, delta, cap))
        states.append(following)
        previous, current = current, following

    assert len(instance.Sstar) == 24
    assert all(all(value > 0 for value in states[t]) for t in range(56, 94))
    assert "".join(corrections[t][0] for t in range(57, 93)) == "P" + "N" * 35
    assert F(4, 5) < corrections[57][2] / corrections[57][3] < F(9, 10)

    degrees = [len(row) for row in adjacency]
    cosines = cosine_table(n)

    def cosine_ik(i: int, k: int):
        residue = (i * k) % (2 * (n - 1))
        residue = min(residue, 2 * (n - 1) - residue)
        return cosines[residue]

    eigenvalues = [
        sub(enclose((1 + instance.alpha) / 2), scale((1 - instance.alpha) / 2, cosines[k]))
        for k in range(n)
    ]
    cutoff = F(instance.kappa) / (instance.beta * (2 + instance.beta))
    assert eigenvalues[9][1] < cutoff < eigenvalues[10][0]

    def error(stage: int):
        return [instance.xstar[i] - states[stage][i] for i in range(n)]

    def coefficient_square(vector, mode: int):
        coefficient = ZERO
        for i, value in enumerate(vector):
            coefficient = add(coefficient, mul(enclose(F(degrees[i]) * value), cosine_ik(i, mode)))
        norm_square = 2 * (n - 1) if mode in (0, n - 1) else n - 1
        return scale(F(1, norm_square), square(coefficient))

    def low_bank(stage: int):
        now, before = error(stage), error(stage - 1)
        velocity = [now[i] - F(23, 24) * before[i] for i in range(n)]
        answer = ZERO
        for k in range(10):
            answer = add(
                answer,
                add(
                    coefficient_square(now, k),
                    div(
                        scale(instance.kappa + instance.alpha, coefficient_square(velocity, k)),
                        eigenvalues[k],
                    ),
                ),
            )
        return answer

    def high_energy(stage: int):
        now = error(stage)
        answer = ZERO
        for k in range(10, n):
            answer = add(answer, mul(eigenvalues[k], coefficient_square(now, k)))
        return answer

    def low_payment():
        answer = ZERO
        kappa = enclose(instance.kappa)
        c = enclose(instance.kappa + instance.alpha)
        for stage in range(57, 93):
            for k in range(10):
                mode = div(kappa, add(eigenvalues[k], kappa))
                weight = mul(square(mode), add(enclose(F(1)), div(c, eigenvalues[k])))
                answer = add(answer, mul(weight, coefficient_square(corrections[stage][1], k)))
        return mul(enclose(instance.mu), answer)

    payment = low_payment()
    high_drop = sub(high_energy(56), high_energy(92))
    low_start = mul(enclose(instance.mu), low_bank(56))
    assert payment[0] - high_drop[1] > 0
    assert low_start[0] > 0
    required = div(sub(payment, high_drop), low_start)

    # Simple durable rational outer bounds, deliberately much looser than
    # the 10^-28 interval evaluation.
    assert payment[0] > F(181_459_359, 10**15)
    assert high_drop[1] < F(2_016_735, 10**17)
    assert low_start[1] < F(1_503_275, 10**13)
    certified = F(3_628_783_833, 3_006_550_000)
    assert required[0] > certified > F(6, 5)

    print("P24 rational-interval 6/5 STOP passed")
    print("  exact word: P + 35 N; full support 24")
    print(f"  required coefficient >= {certified} = {float(certified):.15f}")
    print(f"  excess over 6/5 = {certified - F(6, 5)}")


if __name__ == "__main__":
    main()
