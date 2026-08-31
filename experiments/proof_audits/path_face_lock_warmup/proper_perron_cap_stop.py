#!/usr/bin/env python3
"""Exact P3 proper-face Perron/common-cap STOP certificate."""

from __future__ import annotations

import importlib.util
from fractions import Fraction as F

from experiments.proof_audits import REPOSITORY_ROOT, note_tex_source


def add_surd(left, right):
    return left[0] + right[0], left[1] + right[1]


def scale_surd(scalar, value):
    return scalar * value[0], scalar * value[1]


def multiply_surd(left, right):
    return left[0] * right[0] + 2 * left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def sign_surd(value):
    rational, radical = value
    if rational >= 0 and radical >= 0:
        return 1 if rational or radical else 0
    if rational <= 0 and radical <= 0:
        return -1
    if rational >= 0:
        return 1 if rational * rational > 2 * radical * radical else -1
    return 1 if 2 * radical * radical > rational * rational else -1


def load_engine():
    path = REPOSITORY_ROOT / "manuscript/claude-overnight-2026-08-24/w7_windowed/engine.py"
    spec = importlib.util.spec_from_file_location("proper_perron_engine", path)
    assert spec is not None and spec.loader is not None
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    return engine


def main() -> None:
    engine = load_engine()
    instance = engine.Inst(
        engine.path_graph(3),
        [F(1, 2), F(1, 2), F(0)],
        F(1, 4),
        F(1, 4),
    )
    assert instance.d == [1, 2, 1]
    assert instance.alpha == F(1, 17)
    assert instance.kappa == F(15, 17)
    assert instance.beta == F(3, 5)
    assert instance.Sstar == [0, 1]
    assert instance.xstar == [F(9, 196), F(1, 49), 0]
    assert instance.Qt == [
        [F(9, 17), F(-8, 17), 0],
        [F(-8, 17), F(18, 17), F(-8, 17)],
        [0, F(-8, 17), F(9, 17)],
    ]

    # On A={0,1}, Q_A=D_A^{-1}(Qt)_AA has minimum/Perron eigenpair
    # lambda=(9-4*sqrt(2))/17 and phi=(sqrt(2),1).
    eigenvalue = (F(9, 17), F(-4, 17))
    perron = [(F(0), F(1)), (F(1), F(0))]
    operator = [[F(9, 17), F(-8, 17)], [F(-4, 17), F(9, 17)]]
    for i in range(2):
        image = add_surd(
            scale_surd(operator[i][0], perron[0]),
            scale_surd(operator[i][1], perron[1]),
        )
        assert image == multiply_surd(eigenvalue, perron[i])
    assert sign_surd(eigenvalue) > 0

    previous = current = [F(0)] * 3
    states = [current]
    word = []
    records = []
    for _stage in range(6):
        displacement = [current[i] - previous[i] for i in range(3)]
        assert all(value >= 0 for value in displacement)
        trial = [current[i] + instance.beta * displacement[i] for i in range(3)]
        support = [i for i, value in enumerate(trial) if value > 0]
        delta = F(0)
        for i in support:
            residual = instance.ct[i] - sum(instance.Qt[i][j] * trial[j] for j in support)
            if residual < 0:
                delta = max(delta, -residual / (instance.alpha * instance.d[i]))
        cap_vector = [instance.beta * value for value in displacement]
        cap = max(cap_vector)
        correction = [min(value, delta) for value in cap_vector]
        center = [trial[i] - correction[i] for i in range(3)]
        assert all(center[i] >= current[i] for i in range(3))
        following = instance.obstacle_solve(instance.ct, instance.kappa, center)
        kind = "N" if delta == 0 else ("F" if delta >= cap else "P")
        word.append(kind)
        records.append((delta, cap, correction))
        states.append(following)
        previous, current = current, following

    assert "".join(word) == "NNNNPN"
    assert [tuple(i for i, value in enumerate(state) if value > 0) for state in states] == [
        (),
        (0, 1),
        (0, 1),
        (0, 1),
        (0, 1),
        (0, 1),
        (0, 1),
    ]
    delta, cap, correction = records[4]
    assert delta == F(137457, 53453440)
    assert cap == F(53541, 13363360)
    assert correction == [delta, delta, 0]
    assert 0 < delta < cap
    # In Perron coordinates the active entries are delta/sqrt(2), delta.
    transformed = [(F(0), delta / 2), (delta, F(0))]
    assert transformed[0] != transformed[1]

    perron_map = (F(90, 136), F(15, 136))
    global_m0 = F(15, 16)
    assert sign_surd(add_surd((global_m0, 0), scale_surd(-1, perron_map))) > 0
    old_scalar = scalar = (F(1), F(0))
    trials = []
    for _stage in range(6):
        trial = add_surd(
            scale_surd(1 + instance.beta, scalar),
            scale_surd(-instance.beta, old_scalar),
        )
        trials.append(trial)
        old_scalar, scalar = scalar, multiply_surd(perron_map, trial)
    assert all(sign_surd(value) > 0 for value in trials[:5])
    assert trials[5] == (F(-3977667, 227177120), F(1608417, 227177120))
    assert sign_surd(trials[5]) < 0
    source = note_tex_source("path_face_lock_warmup")
    assert "prop:proper-face-perron-split-window" in source
    assert "prop:p3-proper-perron-cap-stop" in source

    print("P3 proper-face Perron/common-cap STOP passed")
    print("  support chronology: empty, then A={0,1} through the certificate")
    print(f"  word t=0..5: {''.join(word)}")
    print("  stage-4 Perron cap spread: sqrt(2), not one")
    print("  pure-Perron global-beta first negative trial: t=5")


if __name__ == "__main__":
    main()
