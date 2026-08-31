#!/usr/bin/env python3
"""Exact reachable S5 audit of the sharp Moreau face-shock constants."""

from __future__ import annotations

import importlib.util
from fractions import Fraction as F

from experiments.proof_audits import REPOSITORY_ROOT, note_tex_source


def load_engine():
    path = (
        REPOSITORY_ROOT
        / "manuscript/claude-overnight-2026-08-24/w7_windowed/engine.py"
    )
    spec = importlib.util.spec_from_file_location("s5_face_shock_engine", path)
    assert spec is not None and spec.loader is not None
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    return engine


def face_data(instance, point, face, engine):
    """Return restricted optimum, optimum value, error, and restart bank."""
    matrix = [[instance.Qt[i][j] for j in face] for i in face]
    rhs = [instance.ct[i] for i in face]
    optimum = engine._gauss(matrix, rhs)
    optimum_value = -F(1, 2) * sum(
        rhs[i] * optimum[i] for i in range(len(face))
    )
    error = [optimum[i] - point[face[i]] for i in range(len(face))]
    degree = [instance.d[i] for i in face]
    shifted = [
        [
            matrix[i][j] + (instance.kappa * degree[i] if i == j else 0)
            for j in range(len(face))
        ]
        for i in range(len(face))
    ]
    moreau_error = engine._gauss(
        shifted,
        [instance.kappa * degree[i] * error[i] for i in range(len(face))],
    )
    restart_bank = sum(
        error[i]
        * sum(matrix[i][j] * moreau_error[j] for j in range(len(face)))
        for i in range(len(face))
    ) + (instance.kappa + instance.alpha) * instance.q**2 * sum(
        degree[i] * error[i] * moreau_error[i] for i in range(len(face))
    )
    return optimum, optimum_value, error, restart_bank


def check_reachable_face_shock() -> None:
    engine = load_engine()
    instance = engine.Inst(
        engine.star_graph(5),
        [F(1), F(0), F(0), F(0), F(0)],
        F(1, 128),
        F(1, 16),
    )
    assert instance.Sstar == list(range(5))
    assert instance.alpha == F(1, 16385)
    assert instance.kappa == F(16383, 16385)
    assert instance.beta == F(127, 129)

    zero = [F(0)] * 5
    point = instance.obstacle_solve(instance.ct, instance.kappa, zero)
    assert point == [F(1, 131072), F(0), F(0), F(0), F(0)]
    next_point = instance.obstacle_solve(
        instance.ct,
        instance.kappa,
        [(1 + instance.beta) * value for value in point],
    )
    assert all(value > 0 for value in next_point)
    records = instance.run(3)
    assert [(row["t"], row["cls"], row["supp"]) for row in records] == [
        (0, "N", ()),
        (1, "N", (0,)),
        (2, "N", (0, 1, 2, 3, 4)),
    ]

    old = face_data(instance, point, [0], engine)
    new = face_data(instance, point, list(range(5)), engine)
    face_gain = old[1] - new[1]
    old_bank = old[3]
    new_bank = new[3]
    assert old[0] == [F(1, 43696)]
    assert new[0] == [F(16387, 262160), *([F(16383, 262160)] * 4)]
    assert face_gain == F(89467563, 93847900476800)
    assert old_bank == F(667240645080557, 2149857405379555371253760)
    assert new_bank == F(
        2361075135253227577341,
        619083363355948774064128000,
    )
    ratio = new_bank / (old_bank + face_gain)
    assert ratio == F(590484979685064105981, 147649028343669402280)
    assert F(399, 100) < ratio < 4

    # Rationally certify sqrt(C_new) < sqrt(C_old) + 2 sqrt(face_gain).
    excess = new_bank - old_bank - 4 * face_gain
    assert excess > 0
    assert excess**2 < 16 * old_bank * face_gain


def check_sharp_constant_mode_family() -> None:
    """The empty-to-full constant mode has exact energy ratio 4(1-q^2)."""
    previous = F(0)
    for denominator in (8, 16, 32, 64, 128, 256, 512):
        q = F(1, denominator)
        alpha = q * q / (1 + q * q)
        kappa = 1 - 2 * alpha
        m0 = kappa / (kappa + alpha)
        volume = F(8)
        scale = F(1)
        face_gain = alpha * scale**2 * volume / 2
        restart_bank = 2 * alpha * m0 * scale**2 * volume
        ratio = restart_bank / face_gain
        assert m0 == 1 - q * q
        assert ratio == 4 * m0 == 4 - 4 * q * q
        assert previous < ratio < 4
        previous = ratio
    assert previous > F(3999, 1000)


def check_source_scope() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert "prop:aesp-cd-moreau-face-shock-sharp" in source
    assert "eq:aesp-cd-moreau-face-shock-coefficient" in source
    assert "4m_0\\Delta" in source


def main() -> None:
    check_reachable_face_shock()
    check_sharp_constant_mode_family()
    check_source_scope()
    print("S5 sharp Moreau face-shock audit passed")
    print("  reachable center-to-full admission: energy ratio >3.99 and <4")
    print("  coefficient-2 root transfer certified by exact rational squares")
    print("  constant-mode family: exact ratio 4(1-q^2) tends to four")


if __name__ == "__main__":
    main()
