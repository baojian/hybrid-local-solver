#!/usr/bin/env python3
"""Exact P3 reachable witness with positive signed Moreau correction Xi."""

from __future__ import annotations

import importlib.util
from fractions import Fraction as F
from pathlib import Path

from experiments.proof_audits import REPOSITORY_ROOT, note_tex_source


def load_engine(repo: Path):
    path = repo / "manuscript/claude-overnight-2026-08-24/w7_windowed/engine.py"
    spec = importlib.util.spec_from_file_location("window_engine", path)
    engine = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(engine)
    return engine


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-p3-positive-signed-event}" in source
    engine = load_engine(REPOSITORY_ROOT)

    # Legal source: nonnegative endpoint seed of mass one.
    inst = engine.Inst(engine.path_graph(3), [F(1), F(0), F(0)], F(1, 8), F(1, 16))
    assert (inst.alpha, inst.kappa, inst.beta, inst.mu) == (
        F(1, 65),
        F(63, 65),
        F(7, 9),
        F(63, 4160),
    )
    assert inst.Sstar == [0, 1, 2]

    states = [[F(0)] * 3]
    events = []
    previous = current = [F(0)] * 3
    for _stage in range(5):
        increment = [current[i] - previous[i] for i in range(3)]
        trial = [current[i] + inst.beta * increment[i] for i in range(3)]
        support = [i for i in range(3) if trial[i] > 0]
        delta = F(0)
        for i in support:
            residual = inst.ct[i] - sum(inst.Qt[i][j] * trial[j] for j in support)
            if residual < 0:
                delta = max(delta, -residual / (inst.alpha * inst.d[i]))
        correction = [min(inst.beta * increment[i], delta) for i in range(3)]
        cap = max(inst.beta * value for value in increment)
        kind = "N" if delta == 0 else ("F" if delta >= cap else "P")
        following = inst.obstacle_solve(
            inst.ct, inst.kappa, [trial[i] - correction[i] for i in range(3)], warm=support or None
        )
        states.append(following)
        events.append((kind, correction, delta, cap))
        previous, current = current, following

    assert "".join(event[0] for event in events) == "NNNFN"
    assert [tuple(i for i, value in enumerate(x) if value > 0) for x in states[:5]] == [
        (),
        (0, 1),
        (0, 1, 2),
        (0, 1, 2),
        (0, 1, 2),
    ]
    assert states[2] == [F(9641, 417792), F(633, 139264), F(361, 417792)]
    assert states[3] == [F(703225, 20054016), F(23659, 2228224), F(78137, 20054016)]
    assert events[3][1] == [F(1683199, 180486144), F(94717, 20054016), F(25039, 10616832)]
    assert events[3][2] == F(34349, 940032)
    assert events[3][3] == F(1683199, 180486144)
    assert events[3][2] / events[3][3] == F(134592, 34351) > 1

    # Rational hat-coordinate form of the normalized Moreau bank.
    S = inst.Sstar
    size = len(S)
    matrix = [[inst.Qt[i][j] for j in S] for i in S]
    degree = [inst.d[i] for i in S]
    shifted = [
        [matrix[i][j] + (inst.kappa * degree[i] if i == j else 0) for j in range(size)]
        for i in range(size)
    ]

    def solve_d(vector):
        return engine._gauss(shifted, [degree[i] * vector[i] for i in range(size)])

    def dot_q(left, right):
        return sum(left[i] * matrix[i][j] * right[j] for i in range(size) for j in range(size))

    def dot_d(left, right):
        return sum(degree[i] * left[i] * right[i] for i in range(size))

    def bilinear(e, u, f, v):
        return inst.kappa * dot_q(e, solve_d(f)) + (inst.kappa + inst.alpha) * inst.kappa * dot_d(
            u, solve_d(v)
        )

    def bank(e, u):
        return bilinear(e, u, e, u)

    def error(stage):
        return [inst.xstar[i] - states[stage][i] for i in S]

    # Stage convention: event t=3 consumes (x_2,x_3) and produces x_4.
    theta = 1 - inst.q
    e_previous, e = error(2), error(3)
    trial_error = [(1 + inst.beta) * e[i] - inst.beta * e_previous[i] for i in range(size)]
    no_correction = [inst.kappa * value for value in solve_d(trial_error)]
    u0 = [no_correction[i] - theta * e[i] for i in range(size)]
    correction = events[3][1]
    forcing = [inst.kappa * value for value in solve_d(correction)]
    actual = [no_correction[i] + forcing[i] for i in range(size)]
    u_actual = [u0[i] + forcing[i] for i in range(size)]
    u = [e[i] - theta * e_previous[i] for i in range(size)]

    c_input = bank(e, u)
    c0 = bank(no_correction, u0)
    cross = 2 * bilinear(no_correction, u0, forcing, forcing)
    remainder = bank(forcing, forcing)
    c_actual = bank(actual, u_actual)
    xi = c_actual - c0

    assert actual == error(4)
    assert c_actual == c0 + cross + remainder
    assert c_input == F(394678245312256474541, 142546604927741853696000)
    assert c0 == F(3047152388139462633779, 1282919444349676683264000)
    assert cross == F(36349377234988775587, 57417373733132383027200)
    assert remainder == F(370064583419113289, 3162742910313478225920)
    assert xi == F(22050631447194911121799, 29397695351363780109926400)
    assert c_actual == F(7298971801335701915991269, 2335483575136122530955264000)
    assert xi / c_input == F(938073510129372371755, 3462704548150418915328) > F(1, 4)
    assert xi / (inst.q * c_input) > 2
    assert c_actual / c_input > 1

    print("P3 exact positive-Xi STOP passed")
    print("  legal endpoint seed; support word: () -> 01 -> 012")
    print("  event word NNNFN; t=3 consumes (x2,x3) and produces x4")
    print(f"  Xi/C = {xi / c_input} = {float(xi / c_input):.15f}")
    print(f"  Xi/(qC) = {float(xi / (inst.q * c_input)):.15f}")
    print(f"  C+/C = {float(c_actual / c_input):.15f}")


if __name__ == "__main__":
    main()
