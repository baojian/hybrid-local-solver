#!/usr/bin/env python3
"""Exact finite check for the Round-015 correction--error-bank STOP.

The checker replays the same literal q=1/5 transported-center path execution
as Round 014.  It verifies that the bank delta_t + e_t/q absorbs the reviewed
stage-6--7 correction increase, then fails on the earliest later pair of
consecutive gate-held steps, stages 9--10 on U_4.  This is a finite identity,
not an asymptotic lower bound.
"""

from fractions import Fraction

from experiments.proof_audits.volume_gated_acceleration.moving_correction_stop import (
    one_step,
    residual,
    restricted_optimum,
)


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
    held = []
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
        bank = delta + error_inf / q
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
            held.append(stage)
            iterate, center = iterate_next, center_next

        snapshots[stage] = {
            "face": face_before,
            "action": action,
            "delta": delta,
            "error_inf": error_inf,
            "bank": bank,
            "envelope_residual": envelope_residual,
            "outside_residual": outside_residual,
            "envelope_clipped": min(iterate_next) < delta,
        }
        if action == "certify":
            break
    else:
        raise AssertionError("the exact q=1/5 run did not terminate")

    expected_bank = {
        6: Fraction(46753974625596, 1024161048828125),
        7: Fraction(77233034131696, 5120805244140625),
        9: Fraction(18730043949735496616, 591581025829345703125),
        10: Fraction(105427397282315325168, 2957905129146728515625),
    }
    for stage, value in expected_bank.items():
        assert snapshots[stage]["bank"] == value

    assert snapshots[6]["face"] == snapshots[7]["face"] == 3
    assert snapshots[6]["action"] == snapshots[7]["action"] == "hold"
    assert snapshots[7]["bank"] - snapshots[6]["bank"] == -Fraction(
        156536838996284, 5120805244140625
    )

    assert snapshots[9]["face"] == snapshots[10]["face"] == 4
    assert snapshots[9]["action"] == snapshots[10]["action"] == "hold"
    assert snapshots[9]["delta"] == Fraction(228031410368, 18779541015625)
    assert snapshots[9]["error_inf"] == Fraction(
        2309349016903925448,
        591581025829345703125,
    )
    assert snapshots[10]["delta"] == Fraction(1115890388544, 93897705078125)
    assert snapshots[10]["error_inf"] == Fraction(
        14055067155984414192,
        2957905129146728515625,
    )
    assert snapshots[10]["delta"] - snapshots[9]["delta"] == -Fraction(24266663296, 93897705078125)
    assert snapshots[10]["bank"] - snapshots[9]["bank"] == Fraction(
        11777177533637842088, 2957905129146728515625
    )

    assert snapshots[9]["envelope_clipped"]
    assert snapshots[10]["envelope_clipped"]
    assert snapshots[9]["outside_residual"] == Fraction(1, 625)
    assert snapshots[10]["outside_residual"] == Fraction(1, 625)
    assert snapshots[9]["envelope_residual"][3] == -Fraction(
        5807889226569967,
        2169506475830078125,
    )
    assert snapshots[10]["envelope_residual"][4] == -Fraction(
        135334265006654209513,
        73947628228668212890625,
    )
    assert snapshots[9]["envelope_residual"][3] < -alpha * tau
    assert snapshots[10]["envelope_residual"][4] < -alpha * tau

    held_pairs = [
        (stage, stage + 1)
        for stage in held
        if stage + 1 in held and snapshots[stage]["face"] == snapshots[stage + 1]["face"]
    ]
    first_failure = next(
        pair for pair in held_pairs if snapshots[pair[1]]["bank"] > snapshots[pair[0]]["bank"]
    )
    assert first_failure == (9, 10)

    assert admissions == [1, 2, 4, 8]
    assert terminal_stage == 16
    assert face_index == 4
    assert sum(degrees[: face_index + 1]) == 9
    assert swept_volume == 114

    print(
        "exact q=1/5 bank STOP verified: Phi_7 < Phi_6, but "
        "Phi_10 > Phi_9 on consecutive held U_4 steps; "
        "J=4, T=16, nu_fin=9, swept volume=114, one terminal return"
    )


if __name__ == "__main__":
    main()
