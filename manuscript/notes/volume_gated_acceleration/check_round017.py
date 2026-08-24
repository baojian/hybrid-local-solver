#!/usr/bin/env python3
"""Exact finite check for the Round-017 tight-pair Schur bank.

The checker replays the literal q=1/5 transported-center endpoint-path
execution.  It uses the unique tight endpoints of the two held-pair
coefficient half-lines, freezes the stage-8 candidate while the face optimum
and coefficient are switched, and verifies that the *squared* scalar-bank
jump is strictly smaller than the exact Schur/optimum-drop shock.

This is a finite reset-charge identity.  It is not a global stagewise
potential, an asymptotic chronology result, or a logarithm-removal claim.
"""

from fractions import Fraction

from check_round014 import apply_h, cbar, one_step, residual, restricted_optimum


def normalized_objective(z, degrees, alpha, rho):
    """Evaluate G(sqrt(D) z) using exact normalized path coordinates."""
    h_z = apply_h(z, degrees, alpha)
    load = cbar(len(z), alpha, rho)
    return sum(
        degree * (Fraction(1, 2) * value * h_value - load_value * value)
        for degree, value, h_value, load_value in zip(degrees, z, h_z, load)
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
            new_optimum = restricted_optimum(face_index + 2, degrees, alpha, rho)
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
                post_delta = max(Fraction(0), max(post_residual) / alpha)
                post_error_inf = max(
                    abs(value - target) for value, target in zip(padded_iterate, new_optimum)
                )
                stage_eight_reset = {
                    "old_optimum": old_optimum,
                    "new_optimum": new_optimum,
                    "displacement": displacement,
                    "iterate": padded_iterate,
                    "pre_delta": delta,
                    "post_delta": post_delta,
                    "pre_error_inf": error_inf,
                    "post_error_inf": post_error_inf,
                    "old_optimum_value": normalized_objective(
                        old_optimum + [Fraction(0)],
                        degrees[: face_index + 2],
                        alpha,
                        rho,
                    ),
                    "new_optimum_value": normalized_objective(
                        new_optimum,
                        degrees[: face_index + 2],
                        alpha,
                        rho,
                    ),
                    "old_optimum_padded_residual": residual(
                        old_optimum + [Fraction(0)],
                        degrees[: face_index + 2],
                        alpha,
                        rho,
                    ),
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
            "error_inf": error_inf,
            "outside_residual": outside_residual,
            "envelope_residual": envelope_residual,
            "envelope_clipped": min(iterate_next) < delta,
        }
        if action == "certify":
            break
    else:
        raise AssertionError("the exact q=1/5 run did not terminate")

    assert stage_eight_reset is not None
    reset = stage_eight_reset

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

    # Literal chronology and gate facts surrounding the two held pairs and
    # the intervening stage-8 admission/reset.
    assert snapshots[6]["face"] == snapshots[7]["face"] == 3
    assert snapshots[6]["action"] == snapshots[7]["action"] == "hold"
    assert not snapshots[6]["envelope_clipped"]
    assert not snapshots[7]["envelope_clipped"]
    assert snapshots[8]["face"] == 3
    assert snapshots[8]["action"] == "admit"
    assert snapshots[8]["outside_residual"] == -Fraction(
        1054129838748409,
        640100655517578125,
    )
    assert snapshots[8]["outside_residual"] < -alpha * tau
    assert snapshots[9]["face"] == snapshots[10]["face"] == 4
    assert snapshots[9]["action"] == snapshots[10]["action"] == "hold"
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

    # The Round-016 half-line endpoints are canonical here: c_3 is the
    # smallest U_3-feasible coefficient and c_4 is the largest
    # nonnegative U_4-feasible coefficient.
    delta_6, error_6 = expected_components[6]
    delta_7, error_7 = expected_components[7]
    delta_9, error_9 = expected_components[9]
    delta_10, error_10 = expected_components[10]
    c_3 = (delta_7 - delta_6) / ((error_6 - error_7) / q)
    c_4 = (delta_9 - delta_10) / ((error_10 - error_9) / q)
    assert c_3 == Fraction(2978273417354, 42112483166425)
    assert c_4 == Fraction(95554102960761584, 1567701294665491845)
    assert c_3 > c_4 >= 0

    def bank(delta, error, coefficient):
        return delta + coefficient * error / q

    bank_6 = bank(delta_6, error_6, c_3)
    bank_7 = bank(delta_7, error_7, c_3)
    bank_9 = bank(delta_9, error_9, c_4)
    bank_10 = bank(delta_10, error_10, c_4)
    assert (
        bank_6
        == bank_7
        == Fraction(
            11198565794206524167944,
            1265364967829913056640625,
        )
    )
    assert (
        bank_9
        == bank_10
        == Fraction(
            8722450203325761493618137152,
            654238016964867069277587890625,
        )
    )

    # Freeze the actual stage-8 candidate.  The primal point is merely
    # zero-padded at admission; the estimate center is transported, the
    # restricted optimum is reset, and the face coefficient is switched.
    assert (
        reset["pre_delta"]
        == reset["post_delta"]
        == Fraction(
            28990137728,
            3755908203125,
        )
    )
    assert reset["pre_error_inf"] == Fraction(
        101253632777792,
        25604026220703125,
    )
    assert reset["post_error_inf"] == Fraction(13229, 1501825)
    assert reset["displacement"][-1] == Fraction(13229, 1501825)

    bank_before = bank(reset["pre_delta"], reset["pre_error_inf"], c_3)
    bank_after = bank(reset["post_delta"], reset["post_error_inf"], c_4)
    assert bank_before == Fraction(
        12539389225491032094208,
        1375396704162948974609375,
    )
    assert bank_after == Fraction(
        12250921037449873344675915632,
        1177628430536760724699658203125,
    )

    # Recover the one-coordinate Schur pivot from the old-optimum KKT row
    # and the new-coordinate optimum displacement.  In normalized path
    # coordinates the objective gain is d_4 * h_bar^2 / (2 S_4), d_4=2.
    old_optimum_residual = reset["old_optimum_padded_residual"]
    assert old_optimum_residual[:-1] == [Fraction(0)] * 4
    normalized_shock_gradient = old_optimum_residual[-1]
    assert normalized_shock_gradient == -Fraction(13229, 4260625)
    schur_pivot = -normalized_shock_gradient / reset["displacement"][-1]
    assert schur_pivot == Fraction(60073, 170425)
    optimum_drop = reset["old_optimum_value"] - reset["new_optimum_value"]
    assert optimum_drop == Fraction(175006441, 6398713140625)
    assert optimum_drop == (
        degrees[4] * normalized_shock_gradient * normalized_shock_gradient / (2 * schur_pivot)
    )

    # A raw linear bank has the wrong units for a unit objective-shock
    # charge and fails it on this reset.  Squaring the bank gives the
    # dimension-consistent TightPair-Schur switch rule, which succeeds.
    linear_jump = bank_after - bank_before
    assert linear_jump == Fraction(
        554628881140200492346173398318847940688,
        431242238758981116922282085156980224609375,
    )
    assert linear_jump - optimum_drop == Fraction(
        17100016937884852092375537225532271095508966741,
        13584715716625901120427549219234435097360107421875,
    )
    assert linear_jump > optimum_drop

    squared_jump = bank_after * bank_after - bank_before * bank_before
    assert squared_jump == Fraction(
        4668774724025881375281773213362190705316645416162821813856742543440531613604096,
        185969868489858075498661532785400296133687118291915525862648162012159824371337890625,
    )
    switch_slack = optimum_drop - squared_jump
    assert switch_slack == Fraction(
        13153352075844141929930465447315402255043873003664815010264484652155446410873317194853,
        5858303218542070115616289966440099116412997639614861194042012716938884968578815460205078125,
    )
    assert switch_slack > 0

    # With remaining optimum-drop reserve H_3=Delta_8 and H_4=0, the
    # charged potential bank^2+H strictly decreases at the frozen reset.
    reserve_before = optimum_drop
    reserve_after = Fraction(0)
    assert (bank_after * bank_after + reserve_after) - (
        bank_before * bank_before + reserve_before
    ) == -switch_slack

    # Because both banks are nonnegative, the tight endpoints maximize the
    # reset jump over every locally feasible pair c_3' >= c_3 and
    # 0 <= c_4' <= c_4.  Thus the verified endpoint inequality is the
    # worst-case reset audit for that whole feasible rectangle.
    assert bank_before > 0
    assert bank_after > 0

    assert admissions == [1, 2, 4, 8]
    assert terminal_stage == 16
    assert face_index == 4
    assert sum(degrees[: face_index + 1]) == 9
    assert swept_volume == 114

    print(
        "exact q=1/5 TightPair-Schur reset verified: both named held pairs "
        "are flat; the raw linear switch exceeds the optimum drop, but the "
        "squared switch is strictly paid by Delta_8=175006441/6398713140625; "
        "J=4, T=16, nu_fin=9, swept volume=114, one terminal return"
    )


if __name__ == "__main__":
    main()
