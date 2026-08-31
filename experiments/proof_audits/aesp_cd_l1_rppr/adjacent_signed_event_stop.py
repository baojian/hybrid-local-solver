#!/usr/bin/env python3
"""Exact reachable S5 witness with adjacent positive Moreau corrections."""

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
    assert r"\label{eq:aesp-cd-s5-adjacent-signed-stop}" in source
    engine = load_engine(REPOSITORY_ROOT)

    size = 5
    seed = [F(0), F(1), F(0), F(0), F(0)]
    instance = engine.Inst(engine.star_graph(size), seed, F(1, 8), F(1, 16))
    assert instance.Sstar == list(range(size))

    states = [[F(0)] * size]
    events = []
    previous = current = [F(0)] * size
    for _stage in range(8):
        increment = [current[i] - previous[i] for i in range(size)]
        trial = [current[i] + instance.beta * increment[i] for i in range(size)]
        support = [i for i in range(size) if trial[i] > 0]
        delta = F(0)
        for i in support:
            residual = instance.ct[i] - sum(instance.Qt[i][j] * trial[j] for j in support)
            if residual < 0:
                delta = max(delta, -residual / (instance.alpha * instance.d[i]))
        correction = [min(instance.beta * increment[i], delta) for i in range(size)]
        cap = max(instance.beta * value for value in increment)
        kind = "N" if delta == 0 else ("F" if delta >= cap else "P")
        following = instance.obstacle_solve(
            instance.ct,
            instance.kappa,
            [trial[i] - correction[i] for i in range(size)],
            warm=support or None,
        )
        states.append(following)
        events.append((kind, correction, delta, cap))
        previous, current = current, following

    supports = [tuple(i for i, value in enumerate(point) if value > 0) for point in states]
    assert "".join(event[0] for event in events) == "NNFNNPFN"
    assert supports[:4] == [(), (0, 1), (0, 1), tuple(range(size))]
    assert all(support == tuple(range(size)) for support in supports[3:])
    assert F(1, 2) < events[5][2] / events[5][3] < F(51, 100)
    assert events[6][2] / events[6][3] > 2

    active = instance.Sstar
    matrix = [[instance.Qt[i][j] for j in active] for i in active]
    degree = [instance.d[i] for i in active]
    shifted = [
        [matrix[i][j] + (instance.kappa * degree[i] if i == j else 0) for j in range(size)]
        for i in range(size)
    ]

    def solve_d(vector):
        return engine._gauss(shifted, [degree[i] * vector[i] for i in range(size)])

    def dot_q(left, right):
        return sum(left[i] * matrix[i][j] * right[j] for i in range(size) for j in range(size))

    def dot_d(left, right):
        return sum(degree[i] * left[i] * right[i] for i in range(size))

    def bilinear(e, u, f, v):
        return instance.kappa * dot_q(e, solve_d(f)) + (
            (instance.kappa + instance.alpha) * instance.kappa * dot_d(u, solve_d(v))
        )

    def bank(e, u):
        return bilinear(e, u, e, u)

    def error(stage):
        return [instance.xstar[i] - states[stage][i] for i in active]

    theta = 1 - instance.q

    def ledger(stage):
        e_previous, e = error(stage - 1), error(stage)
        trial_error = [
            (1 + instance.beta) * e[i] - instance.beta * e_previous[i] for i in range(size)
        ]
        no_correction = [instance.kappa * value for value in solve_d(trial_error)]
        u0 = [no_correction[i] - theta * e[i] for i in range(size)]
        forcing = [instance.kappa * value for value in solve_d(events[stage][1])]
        actual = [no_correction[i] + forcing[i] for i in range(size)]
        u_actual = [u0[i] + forcing[i] for i in range(size)]
        u = [e[i] - theta * e_previous[i] for i in range(size)]
        c_input = bank(e, u)
        c0 = bank(no_correction, u0)
        cross = 2 * bilinear(no_correction, u0, forcing, forcing)
        remainder = bank(forcing, forcing)
        c_actual = bank(actual, u_actual)
        assert actual == error(stage + 1)
        assert c_actual == c0 + cross + remainder
        return c_input, c_actual, c_actual - c0

    event5 = ledger(5)
    event6 = ledger(6)
    xi5_ratio = event5[2] / event5[0]
    xi6_ratio = event6[2] / event6[0]
    two_step = event6[1] / event5[0]
    assert xi5_ratio == F(
        85415588060812730872079929,
        375540936815756872189476864,
    )
    assert xi6_ratio == F(
        18257666145580448465266605217,
        136457139588689129518317846528,
    )
    assert two_step == F(
        741880636900433781669613477769,
        683651412087706732661376548864,
    )
    assert xi5_ratio > F(1, 5) and xi6_ratio > F(1, 8) and two_step > 1

    print("S5 exact adjacent-positive-Xi STOP passed")
    print("  seed leaf 1; q=1/8, rho=1/16; S*=full")
    print("  event word NNFNNPFN; t=5 partial, t=6 full")
    print(f"  Xi5/C5={float(xi5_ratio):.12f}, Xi6/C6={float(xi6_ratio):.12f}")
    print(f"  C7/C5={float(two_step):.12f}")


if __name__ == "__main__":
    main()
