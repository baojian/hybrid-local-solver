#!/usr/bin/env python3
"""Exact finite check for the Round-018 TightPair-Schur local chain.

The checker replays the literal q=1/5 transported-center endpoint-path
execution and separates four states around the stage-8 admission: held stage
7, the stage-8 pre-reset candidate on U_3, the same zero-padded candidate after
the U_4 reset, and held stage 9.  It verifies the squared-bank-plus-reserve
change on the production step, reset, and follow-up step separately.

This is a finite exact-real local-chain STOP.  It is not a global stagewise
potential, a multi-admission result, or an asymptotic chronology claim.
"""

from fractions import Fraction

from check_round014 import one_step, residual, restricted_optimum
from check_round017 import normalized_objective


def bank(delta, error, coefficient, q):
    """Return delta + coefficient * q^{-1} * error."""
    return delta + coefficient * error / q


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
    stage_eight_reset = None

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
        error_inf = max(abs(value - target) for value, target in zip(iterate_next, optimum))
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
            old_optimum = optimum
            new_optimum = restricted_optimum(
                face_index + 2,
                degrees,
                alpha,
                rho,
            )
            displacement = [new - old for new, old in zip(new_optimum, old_optimum + [Fraction(0)])]
            padded_iterate = iterate_next + [Fraction(0)]
            padded_center = center_next + [Fraction(0)]
            transported_center = [
                value + shift for value, shift in zip(padded_center, displacement)
            ]

            if stage == 8:
                post_residual = residual(
                    padded_iterate,
                    degrees[: face_index + 2],
                    alpha,
                    rho,
                )
                stage_eight_reset = {
                    "old_optimum": old_optimum,
                    "new_optimum": new_optimum,
                    "pre_delta": delta,
                    "post_delta": max(Fraction(0), max(post_residual) / alpha),
                    "pre_error": error_inf,
                    "post_error": max(
                        abs(value - target) for value, target in zip(padded_iterate, new_optimum)
                    ),
                    "old_value": normalized_objective(
                        old_optimum + [Fraction(0)],
                        degrees[: face_index + 2],
                        alpha,
                        rho,
                    ),
                    "new_value": normalized_objective(
                        new_optimum,
                        degrees[: face_index + 2],
                        alpha,
                        rho,
                    ),
                    "padded_iterate": padded_iterate,
                    "transported_center": transported_center,
                }

            iterate = padded_iterate
            center = transported_center
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
            "error": error_inf,
            "outside_residual": outside_residual,
            "envelope_residual": envelope_residual,
        }
        if action == "certify":
            break
    else:
        raise AssertionError("the exact q=1/5 run did not terminate")

    assert stage_eight_reset is not None
    reset = stage_eight_reset

    # Literal chronology: stage 7 is held on U_3; one more U_3 recurrence
    # produces the stage-8 candidate before the gate admits; the reset merely
    # zero-pads that candidate and transports the center; stage 9 is the first
    # subsequent U_4 recurrence and is held.
    assert snapshots[6]["face"] == snapshots[7]["face"] == 3
    assert snapshots[6]["action"] == snapshots[7]["action"] == "hold"
    assert snapshots[8]["face"] == 3
    assert snapshots[8]["action"] == "admit"
    assert snapshots[8]["outside_residual"] == -Fraction(
        1054129838748409,
        640100655517578125,
    )
    assert snapshots[8]["outside_residual"] < -alpha * tau
    assert snapshots[9]["face"] == snapshots[10]["face"] == 4
    assert snapshots[9]["action"] == snapshots[10]["action"] == "hold"
    assert len(reset["padded_iterate"]) == len(reset["transported_center"]) == 5

    expected = {
        6: (
            Fraction(14898928, 2462890625),
            Fraction(623976140044, 78781619140625),
        ),
        7: (
            Fraction(6291729688, 751181640625),
            Fraction(1373692513944, 1024161048828125),
        ),
        8: (
            Fraction(28990137728, 3755908203125),
            Fraction(101253632777792, 25604026220703125),
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
    for stage, (delta, error) in expected.items():
        assert snapshots[stage]["delta"] == delta
        assert snapshots[stage]["error"] == error

    delta_6, error_6 = expected[6]
    delta_7, error_7 = expected[7]
    delta_8, error_8_minus = expected[8]
    delta_9, error_9 = expected[9]
    delta_10, error_10 = expected[10]
    assert reset["pre_delta"] == reset["post_delta"] == delta_8
    error_8_plus = reset["post_error"]
    assert reset["pre_error"] == error_8_minus
    assert error_8_plus == Fraction(13229, 1501825)

    # The same canonical coefficients are the endpoints of the two held-pair
    # half-lines.  They make 6->7 and 9->10 exactly flat.
    c_3 = (delta_7 - delta_6) / ((error_6 - error_7) / q)
    c_4 = (delta_9 - delta_10) / ((error_10 - error_9) / q)
    assert c_3 == Fraction(2978273417354, 42112483166425)
    assert c_4 == Fraction(95554102960761584, 1567701294665491845)

    b_6 = bank(delta_6, error_6, c_3, q)
    b_7 = bank(delta_7, error_7, c_3, q)
    b_8_minus = bank(delta_8, error_8_minus, c_3, q)
    b_8_plus = bank(delta_8, error_8_plus, c_4, q)
    b_9 = bank(delta_9, error_9, c_4, q)
    b_10 = bank(delta_10, error_10, c_4, q)
    assert (
        b_6
        == b_7
        == Fraction(
            11198565794206524167944,
            1265364967829913056640625,
        )
    )
    assert b_8_minus == Fraction(
        12539389225491032094208,
        1375396704162948974609375,
    )
    assert b_8_plus == Fraction(
        12250921037449873344675915632,
        1177628430536760724699658203125,
    )
    assert (
        b_9
        == b_10
        == Fraction(
            8722450203325761493618137152,
            654238016964867069277587890625,
        )
    )

    optimum_drop = reset["old_value"] - reset["new_value"]
    assert optimum_drop == Fraction(175006441, 6398713140625)

    # Reserve H_3=Delta_8 is unchanged during the U_3 production step.  The
    # first local-chain comparison therefore fails before the reset.
    psi_7 = b_7 * b_7 + optimum_drop
    psi_8_minus = b_8_minus * b_8_minus + optimum_drop
    production_jump = psi_8_minus - psi_7
    assert production_jump == Fraction(
        4798070852000000223973860697504672676758942656,
        1000717813631998065466639280969584524631500244140625,
    )
    assert production_jump > 0

    # The reset consumes the reserve and remains a strict GO, exactly as in
    # Round 017.
    psi_8_plus = b_8_plus * b_8_plus
    reset_change = psi_8_plus - psi_8_minus
    switch_slack = -reset_change
    assert switch_slack == Fraction(
        13153352075844141929930465447315402255043873003664815010264484652155446410873317194853,
        5858303218542070115616289966440099116412997639614861194042012716938884968578815460205078125,
    )
    assert reset_change < 0

    # With no reserve left on U_4, the first post-reset fixed-face step also
    # rises.  The complete stage-7-to-stage-9 chain has positive net change.
    psi_9 = b_9 * b_9
    followup_jump = psi_9 - psi_8_plus
    assert followup_jump == Fraction(
        185418883451039233414483427688468628491104384871211336448,
        2666939846939373614068372111818330675602595627307891845703125,
    )
    assert followup_jump > 0
    net_jump = psi_9 - psi_7
    assert net_jump == Fraction(
        212119118576066028022993097362480113913974152962498585225695096903541477328114649390919,
        2943060211404325822565068748572471445947270419141748880957478373466923217833042144775390625,
    )
    assert net_jump > 0

    # Feasible-coefficient scope.  Since all banks are nonnegative, squared
    # nonincrease is equivalent to scalar-bank nonincrease.  The production
    # step would require c_3 below this cap, contradicting held-pair
    # feasibility c_3 >= c_3^tight.  The follow-up would require c_4 above
    # this floor, contradicting 0 <= c_4 <= c_4^tight.
    production_cap = (delta_7 - delta_8) / ((error_8_minus - error_7) / q)
    assert production_cap == Fraction(2103479690463, 41819574955745)
    assert c_3 - production_cap == Fraction(
        7193475072039691470138791,
        352225229270171965368972325,
    )
    followup_floor = (delta_9 - delta_8) / ((error_8_plus - error_9) / q)
    assert followup_floor == Fraction(
        2617155474971384896,
        14508305905763575885,
    )
    assert followup_floor - c_4 == Fraction(
        543317974029592451788763102773474256,
        4548937990373711847606538687901231565,
    )
    assert production_cap < c_3
    assert followup_floor > c_4 >= 0

    assert admissions == [1, 2, 4, 8]
    assert terminal_stage == 16
    assert face_index == 4
    assert sum(degrees[: face_index + 1]) == 9
    assert swept_volume == 114

    print(
        "exact q=1/5 TightPair-Schur local chain verified: 6->7 and 9->10 "
        "are flat; 7->8- is the first positive squared-bank-plus-reserve "
        "STOP, the reserve-paid reset decreases, and 8+->9 rises again; "
        "J=4, T=16, nu_fin=9, swept volume=114, one terminal return"
    )


if __name__ == "__main__":
    main()
