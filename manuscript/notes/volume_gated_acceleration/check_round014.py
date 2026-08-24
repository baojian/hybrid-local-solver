#!/usr/bin/env python3
"""Exact finite check for the Round-014 moving-correction STOP.

This is an exact replay at q=1/5.  It proves only the two finite pointwise
failures recorded in ``prop:path-monotone-correction-potential-fails``; it is
not evidence for or against an asymptotic chronology bound.
"""

from fractions import Fraction


def apply_h(z, degrees, alpha):
    """Apply D^{-1/2} Q D^{1/2} on the represented ambient-degree prefix."""
    eta = (1 - alpha) / 2
    diagonal = (1 + alpha) / 2
    out = []
    for i, value in enumerate(z):
        neighbor_sum = Fraction(0)
        if i:
            neighbor_sum += z[i - 1]
        if i + 1 < len(z):
            neighbor_sum += z[i + 1]
        out.append(diagonal * value - eta * neighbor_sum / degrees[i])
    return out


def cbar(length, alpha, rho):
    load = [-alpha * rho for _ in range(length)]
    load[0] += alpha
    return load


def residual(z, degrees, alpha, rho):
    return [
        left - right for left, right in zip(apply_h(z, degrees, alpha), cbar(len(z), alpha, rho))
    ]


def restricted_optimum(length, degrees, alpha, rho):
    """Exact Thomas solve for the normalized restricted optimum."""
    eta = (1 - alpha) / 2
    diagonal_value = (1 + alpha) / 2
    right_hand_side = cbar(length, alpha, rho)
    diagonal = [diagonal_value for _ in range(length)]
    upper = [-eta / degrees[i] for i in range(length - 1)]
    lower = [-eta / degrees[i] for i in range(1, length)]
    for i in range(1, length):
        multiplier = lower[i - 1] / diagonal[i - 1]
        diagonal[i] -= multiplier * upper[i - 1]
        right_hand_side[i] -= multiplier * right_hand_side[i - 1]
    answer = [Fraction(0) for _ in range(length)]
    answer[-1] = right_hand_side[-1] / diagonal[-1]
    for i in range(length - 2, -1, -1):
        answer[i] = (right_hand_side[i] - upper[i] * answer[i + 1]) / diagonal[i]
    return answer


def one_step(p, center, degrees, q, rho):
    alpha = q * q
    y = [(value + q * center_value) / (1 + q) for value, center_value in zip(p, center)]
    gradient = residual(y, degrees, alpha, rho)
    raw = [value - grad for value, grad in zip(y, gradient)]
    assert min(raw) > 0, "the actual q=1/5 proximal candidate clipped"
    center_next = [
        value_next + (1 - q) * (value_next - value) / q for value_next, value in zip(raw, p)
    ]
    return raw, center_next


def main():
    q = Fraction(1, 5)
    alpha = q * q
    rho = tau = q / 5
    degrees = [Fraction(1)] + [Fraction(2)] * 16

    p = [Fraction(0)]
    center = [Fraction(0)]
    optimum = restricted_optimum(1, degrees, alpha, rho)
    admissions = []
    held = []
    snapshots = {}
    swept_volume = Fraction(0)
    face_index = 0

    for stage in range(1, 100):
        face_before = face_index
        swept_volume += sum(degrees[: face_index + 1])
        p_next, center_next = one_step(p, center, degrees[: face_index + 1], q, rho)
        active_residual = residual(p_next, degrees[: face_index + 1], alpha, rho)
        delta = max(Fraction(0), max(active_residual) / alpha)
        envelope = [max(Fraction(0), value - delta) for value in p_next]
        envelope_residual = residual(envelope, degrees[: face_index + 1], alpha, rho)
        outside_residual = -((1 - alpha) / 2) * envelope[-1] / degrees[face_index + 1] + alpha * rho

        if stage in (6, 7):
            error = [value - target for value, target in zip(p_next, optimum)]
            snapshots[stage] = {
                "face": face_before,
                "delta": delta,
                "residual": active_residual,
                "error": error,
                "error_inf": max(abs(value) for value in error),
                "envelope_margin": min(p_next) - delta,
            }

        if outside_residual < -alpha * tau:
            admissions.append(stage)
            new_optimum = restricted_optimum(face_index + 2, degrees, alpha, rho)
            displacement = [new - old for new, old in zip(new_optimum, optimum + [Fraction(0)])]
            p = p_next + [Fraction(0)]
            center = [
                value + shift for value, shift in zip(center_next + [Fraction(0)], displacement)
            ]
            optimum = new_optimum
            face_index += 1
            continue

        if min(envelope_residual) >= -alpha * tau:
            terminal_stage = stage
            break

        held.append(stage)
        p, center = p_next, center_next
    else:
        raise AssertionError("the exact q=1/5 run did not terminate")

    stage6 = snapshots[6]
    stage7 = snapshots[7]
    expected_delta6 = Fraction(14898928, 2462890625)
    expected_delta7 = Fraction(6291729688, 751181640625)
    expected_residual7 = [
        Fraction(6291729688, 18779541015625),
        Fraction(229902132, 3755908203125),
        -Fraction(19945416, 61572265625),
        -Fraction(5682971052, 18779541015625),
    ]
    expected_error7 = Fraction(1373692513944, 1024161048828125)

    assert stage6["face"] == stage7["face"] == 3
    assert 6 in held and 7 in held
    assert stage6["delta"] == expected_delta6
    assert stage7["delta"] == expected_delta7
    assert stage7["delta"] - stage6["delta"] == Fraction(1747556648, 751181640625)
    assert stage7["residual"] == expected_residual7
    assert stage7["error_inf"] == expected_error7
    assert stage7["delta"] / stage7["error_inf"] == Fraction(5361340160387, 858557821215)
    assert stage7["delta"] > stage7["error_inf"] / q
    assert stage7["envelope_margin"] == Fraction(51347070933121, 5120805244140625)

    assert admissions == [1, 2, 4, 8]
    assert terminal_stage == 16
    assert face_index == 4
    assert sum(degrees[: face_index + 1]) == 9
    assert swept_volume == 114

    print(
        "exact q=1/5 STOP verified: delta_7 > delta_6, "
        "delta_7/e_7 > 1/q; J=4, T=16, nu_fin=9, "
        "swept volume=114, one terminal return"
    )


if __name__ == "__main__":
    main()
