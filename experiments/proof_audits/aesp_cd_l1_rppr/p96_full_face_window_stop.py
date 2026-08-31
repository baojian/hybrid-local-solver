#!/usr/bin/env python3
"""Exact P96 fixed-full Moreau-window half-contraction STOP."""

from __future__ import annotations

import importlib.util
from fractions import Fraction as F

from experiments.proof_audits import REPOSITORY_ROOT, note_tex_source


def load_engine():
    path = REPOSITORY_ROOT / "manuscript/claude-overnight-2026-08-24/w7_windowed/engine.py"
    spec = importlib.util.spec_from_file_location("p96_window_engine", path)
    assert spec is not None and spec.loader is not None
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    return engine


def make_path_instance(engine):
    class PathInstance(engine.Inst):
        """Exact active-set semantics with block Thomas restricted solves."""

        def _restricted_solve(self, rhs, kappa, active):
            solution = [F(0)] * self.n
            blocks = []
            ordered = sorted(active)
            if ordered:
                low = high = ordered[0]
                for value in ordered[1:]:
                    if value == high + 1:
                        high = value
                    else:
                        blocks.append((low, high))
                        low = high = value
                blocks.append((low, high))

            for low, high in blocks:
                length = high - low + 1
                upper = [F(0)] * length
                transformed = [F(0)] * length
                diagonal = self.Qt[low][low] + kappa * self.d[low]
                if length > 1:
                    upper[0] = self.Qt[low][low + 1] / diagonal
                transformed[0] = rhs[low] / diagonal
                for offset in range(1, length):
                    vertex = low + offset
                    lower = self.Qt[vertex][vertex - 1]
                    denominator = (
                        self.Qt[vertex][vertex] + kappa * self.d[vertex] - lower * upper[offset - 1]
                    )
                    if offset + 1 < length:
                        upper[offset] = self.Qt[vertex][vertex + 1] / denominator
                    transformed[offset] = (
                        rhs[vertex] - lower * transformed[offset - 1]
                    ) / denominator
                solution[high] = transformed[-1]
                for offset in range(length - 2, -1, -1):
                    solution[low + offset] = (
                        transformed[offset] - upper[offset] * solution[low + offset + 1]
                    )
            return solution

        def obstacle_solve(self, ct, kappa, center, warm=None):
            rhs = [ct[i] + kappa * self.d[i] * center[i] for i in range(self.n)]
            active = set(warm) if warm is not None else {i for i in range(self.n) if rhs[i] > 0}
            if not active:
                active = {i for i in range(self.n) if rhs[i] > 0}
            for _ in range(4 * self.n + 8):
                solution = self._restricted_solve(rhs, kappa, active)
                negative = [i for i in active if solution[i] < 0]
                if negative:
                    active.difference_update(negative)
                    continue
                violated = []
                for i in range(self.n):
                    if i in active:
                        continue
                    gradient = -rhs[i] + self.Qt[i][i] * solution[i]
                    if i:
                        gradient += self.Qt[i][i - 1] * solution[i - 1]
                    if i + 1 < self.n:
                        gradient += self.Qt[i][i + 1] * solution[i + 1]
                    if gradient < 0:
                        violated.append(i)
                if not violated:
                    return solution
                active.update(violated)
            raise RuntimeError("active set stalled")

    return PathInstance


def main() -> None:
    engine = load_engine()
    path_instance = make_path_instance(engine)
    size = 96
    seed = [F(1, 2), F(1, 2)] + [F(0)] * (size - 2)
    instance = path_instance(engine.path_graph(size), seed, F(1, 128), F(1, 380))
    assert instance.Sstar == list(range(size))

    states = [[F(0)] * size]
    events = []
    previous = current = [F(0)] * size
    for _stage in range(370):
        displacement = [current[i] - previous[i] for i in range(size)]
        assert all(value >= 0 for value in displacement)
        trial = [current[i] + instance.beta * displacement[i] for i in range(size)]
        support = [i for i, value in enumerate(trial) if value > 0]
        delta = F(0)
        for i in support:
            residual = instance.ct[i] - instance.Qt[i][i] * trial[i]
            if i:
                residual -= instance.Qt[i][i - 1] * trial[i - 1]
            if i + 1 < size:
                residual -= instance.Qt[i][i + 1] * trial[i + 1]
            if residual < 0:
                delta = max(delta, -residual / (instance.alpha * instance.d[i]))
        cap_vector = [instance.beta * value for value in displacement]
        cap = max(cap_vector)
        correction = [min(value, delta) for value in cap_vector]
        kind = "N" if delta == 0 else ("F" if delta >= cap else "P")
        center = [trial[i] - correction[i] for i in range(size)]
        assert all(center[i] >= current[i] for i in range(size))
        following = instance.obstacle_solve(
            instance.ct,
            instance.kappa,
            center,
        )
        assert all(following[i] >= current[i] for i in range(size))
        assert all(following[i] <= instance.xstar[i] for i in range(size))
        states.append(following)
        events.append((kind, delta, cap))
        previous, current = current, following

    assert all(value > 0 for value in states[195])
    assert all(all(value > 0 for value in state) for state in states[195:])

    def msolve(vector):
        rhs = [instance.kappa * instance.d[i] * vector[i] for i in range(size)]
        return instance._restricted_solve(rhs, instance.kappa, set(range(size)))

    def dot_q(left, right):
        total = F(0)
        for i in range(size):
            total += left[i] * instance.Qt[i][i] * right[i]
            if i + 1 < size:
                total += left[i] * instance.Qt[i][i + 1] * right[i + 1]
                total += left[i + 1] * instance.Qt[i + 1][i] * right[i]
        return total

    def dot_d(left, right):
        return sum(instance.d[i] * left[i] * right[i] for i in range(size))

    theta = 1 - instance.q
    volume = sum(instance.d)

    def bank(stage):
        error = [instance.xstar[i] - states[stage][i] for i in range(size)]
        old_error = [instance.xstar[i] - states[stage - 1][i] for i in range(size)]
        velocity = [error[i] - theta * old_error[i] for i in range(size)]
        mapped_error, mapped_velocity = msolve(error), msolve(velocity)
        total = dot_q(error, mapped_error) + (instance.kappa + instance.alpha) * dot_d(
            velocity, mapped_velocity
        )
        mean_error = dot_d([F(1)] * size, error) / volume
        mean_velocity = dot_d([F(1)] * size, velocity) / volume
        low = (
            instance.kappa
            * volume
            * (instance.q * instance.q * mean_error * mean_error + mean_velocity * mean_velocity)
        )
        return total, low, total - low

    # The scanner's label is one below the mathematical input bank.  Events
    # 242,...,330 give 89 transitions from C_242 to C_331; 128 transitions
    # end at C_370.
    start = bank(242)
    end_89 = bank(331)
    end_128 = bank(370)
    ratio_89 = end_89[0] / start[0]
    ratio_128 = end_128[0] / start[0]
    low_ratio_128 = end_128[1] / start[1]
    offsets = [i for i in range(89) if events[242 + i][0] != "N"]
    assert offsets == [0, 1, 14, 16, 19, 21, 23, 24, 26, 28, 29, 31, 34, 52, 64]
    assert all(events[242 + i][0] == "P" for i in offsets)
    assert ratio_89 > F(77, 100)
    assert ratio_128 > F(54, 100) > F(1, 2)
    assert low_ratio_128 > F(2, 3)
    assert "cor:aesp-cd-observable-two-scale-window" in note_tex_source("aesp_cd_l1_rppr")

    print("P96 exact fixed-full Moreau-window STOP passed")
    print("  full support from x195; event window t=242..330")
    print(f"  partial offsets={offsets}")
    print(f"  C331/C242={float(ratio_89):.12f} > 77/100")
    print(f"  C370/C242={float(ratio_128):.12f} > 54/100")
    print(f"  C370_low/C242_low={float(low_ratio_128):.12f} > 2/3")


if __name__ == "__main__":
    main()
