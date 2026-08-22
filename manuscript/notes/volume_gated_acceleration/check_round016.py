#!/usr/bin/env python3
"""Exact finite check for the Round-016 no-constant-bank STOP.

The checker replays the literal q=1/5 transported-center path execution and
derives the complete coefficient constraints for

    Phi_t(c; U) = delta_t + c * e_t(U) / q,  c >= 0.

The held U_3 pair 6--7 imposes a lower bound on c, whereas the held U_4 pair
9--10 imposes a strictly smaller upper bound.  This exact finite
incompatibility is not an asymptotic lower bound.
"""

from fractions import Fraction

from check_round014 import one_step, residual, restricted_optimum


def main():
    q = Fraction(1, 5)
    alpha = q * q
    rho = tau = q / 5
    degrees = [Fraction(1)] + [Fraction(2)] * 16

    iterate = [Fraction(0)]
    center = [Fraction(0)]
    optimum = restricted_optimum(1, degrees, alpha, rho)
    face_index = 0
    swept_volume = Fraction(0)
    admissions = []
    snapshots = {}

    for stage in range(1, 100):
        face_before = face_index
        swept_volume += sum(degrees[: face_index + 1])
        iterate_next, center_next = one_step(
            iterate,
            center,
            degrees[: face_index + 1],
            q,
            rho,
        )
        active_residual = residual(
            iterate_next,
            degrees[: face_index + 1],
            alpha,
            rho,
        )
        delta = max(Fraction(0), max(active_residual) / alpha)
        error = [value - target for value, target in zip(iterate_next, optimum)]
        error_inf = max(abs(value) for value in error)
        envelope = [max(Fraction(0), value - delta) for value in iterate_next]
        envelope_residual = residual(
            envelope,
            degrees[: face_index + 1],
            alpha,
            rho,
        )
        outside_residual = -((1 - alpha) / 2) * envelope[-1] / degrees[face_index + 1] + alpha * rho

        if outside_residual < -alpha * tau:
            action = "admit"
            admissions.append(stage)
            new_optimum = restricted_optimum(face_index + 2, degrees, alpha, rho)
            displacement = [new - old for new, old in zip(new_optimum, optimum + [Fraction(0)])]
            iterate = iterate_next + [Fraction(0)]
            center = [
                value + shift for value, shift in zip(center_next + [Fraction(0)], displacement)
            ]
            optimum = new_optimum
            face_index += 1
        elif min(envelope_residual) >= -alpha * tau:
            action = "certify"
            terminal_stage = stage
            iterate, center = iterate_next, center_next
        else:
            action = "hold"
            iterate, center = iterate_next, center_next

        snapshots[stage] = {
            "face": face_before,
            "action": action,
            "delta": delta,
            "error_inf": error_inf,
            "envelope_residual": envelope_residual,
            "outside_residual": outside_residual,
            "envelope_clipped": min(iterate_next) < delta,
            "minimum_minus_delta": min(iterate_next) - delta,
        }
        if action == "certify":
            break
    else:
        raise AssertionError("the exact q=1/5 run did not terminate")

    expected_components = {
        6: (
            Fraction(14898928, 2462890625),
            Fraction(623976140044, 78781619140625),
        ),
        7: (
            Fraction(6291729688, 751181640625),
            Fraction(1373692513944, 1024161048828125),
        ),
        9: (
            Fraction(228031410368, 18779541015625),
            Fraction(2309349016903925448, 591581025829345703125),
        ),
        10: (
            Fraction(1115890388544, 93897705078125),
            Fraction(14055067155984414192, 2957905129146728515625),
        ),
    }
    for stage, (delta, error_inf) in expected_components.items():
        assert snapshots[stage]["delta"] == delta
        assert snapshots[stage]["error_inf"] == error_inf

    assert snapshots[6]["face"] == snapshots[7]["face"] == 3
    assert snapshots[6]["action"] == snapshots[7]["action"] == "hold"
    assert not snapshots[6]["envelope_clipped"]
    assert not snapshots[7]["envelope_clipped"]
    assert snapshots[6]["minimum_minus_delta"] == Fraction(7887224114511, 1024161048828125)
    assert snapshots[7]["minimum_minus_delta"] == Fraction(51347070933121, 5120805244140625)
    assert snapshots[6]["minimum_minus_delta"] > 0
    assert snapshots[7]["minimum_minus_delta"] > 0
    assert snapshots[6]["outside_residual"] == -Fraction(6356902733941, 25604026220703125)
    assert snapshots[7]["outside_residual"] == -Fraction(103250215833101, 128020131103515625)
    assert snapshots[6]["outside_residual"] >= -alpha * tau
    assert snapshots[7]["outside_residual"] >= -alpha * tau
    assert min(snapshots[6]["envelope_residual"]) == -Fraction(174663082, 61572265625)
    assert min(snapshots[7]["envelope_residual"]) == -Fraction(49725078868, 18779541015625)
    assert min(snapshots[6]["envelope_residual"]) < -alpha * tau
    assert min(snapshots[7]["envelope_residual"]) < -alpha * tau

    assert snapshots[8]["face"] == 3
    assert snapshots[8]["action"] == "admit"
    assert snapshots[8]["outside_residual"] == -Fraction(1054129838748409, 640100655517578125)
    assert snapshots[8]["outside_residual"] < -alpha * tau

    assert snapshots[9]["face"] == snapshots[10]["face"] == 4
    assert snapshots[9]["action"] == snapshots[10]["action"] == "hold"
    assert snapshots[9]["envelope_clipped"]
    assert snapshots[10]["envelope_clipped"]
    assert snapshots[9]["minimum_minus_delta"] == -Fraction(
        4281637684063154199, 591581025829345703125
    )
    assert snapshots[10]["minimum_minus_delta"] == -Fraction(
        2062732844064099169, 591581025829345703125
    )
    assert snapshots[9]["outside_residual"] == Fraction(1, 625)
    assert snapshots[10]["outside_residual"] == Fraction(1, 625)
    assert snapshots[9]["envelope_residual"][3] == -Fraction(5807889226569967, 2169506475830078125)
    assert snapshots[10]["envelope_residual"][4] == -Fraction(
        135334265006654209513, 73947628228668212890625
    )
    assert snapshots[9]["envelope_residual"][3] < -alpha * tau
    assert snapshots[10]["envelope_residual"][4] < -alpha * tau

    delta_6, error_6 = expected_components[6]
    delta_7, error_7 = expected_components[7]
    delta_9, error_9 = expected_components[9]
    delta_10, error_10 = expected_components[10]

    correction_rise_67 = delta_7 - delta_6
    error_drop_slope_67 = (error_6 - error_7) / q
    correction_drop_910 = delta_9 - delta_10
    error_rise_slope_910 = (error_10 - error_9) / q
    assert correction_rise_67 == Fraction(1747556648, 751181640625)
    assert error_drop_slope_67 == Fraction(6737997306628, 204832209765625)
    assert correction_drop_910 == Fraction(24266663296, 93897705078125)
    assert error_rise_slope_910 == Fraction(2508322071464786952, 591581025829345703125)

    lower_coefficient = correction_rise_67 / error_drop_slope_67
    upper_coefficient = correction_drop_910 / error_rise_slope_910
    assert lower_coefficient == Fraction(2978273417354, 42112483166425)
    assert upper_coefficient == Fraction(95554102960761584, 1567701294665491845)
    assert lower_coefficient - upper_coefficient == Fraction(
        129004507967154213801509972186,
        13203958876316640794781123060825,
    )
    assert lower_coefficient > upper_coefficient >= 0

    # Exact endpoint checks for the two affine half-line constraints.
    assert correction_rise_67 - lower_coefficient * error_drop_slope_67 == 0
    assert -correction_drop_910 + upper_coefficient * error_rise_slope_910 == 0
    # Therefore pair 6--7 is nonincreasing iff c >= lower_coefficient, while
    # pair 9--10 is nonincreasing iff c <= upper_coefficient.  Their exact
    # feasible intervals are disjoint, so no c >= 0 satisfies both.

    assert admissions == [1, 2, 4, 8]
    assert terminal_stage == 16
    assert face_index == 4
    assert sum(degrees[: face_index + 1]) == 9
    assert swept_volume == 114

    print(
        "exact q=1/5 no-constant-bank STOP verified: held pair 6--7 "
        "requires c >= 2978273417354/42112483166425, while held pair "
        "9--10 requires c <= 95554102960761584/1567701294665491845; "
        "the intervals are disjoint; J=4, T=16, nu_fin=9, swept "
        "volume=114, one terminal return"
    )


if __name__ == "__main__":
    main()
