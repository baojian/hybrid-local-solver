#!/usr/bin/env python3
"""Exact finite check for the Round-019 post-reset recovery block.

The checker replays the literal q=1/5 transported-center endpoint-path
execution.  It keeps the Round-018 production, reset, and follow-up changes
separate, then accumulates only the subsequent fixed-U_4 decrease

    R_{9:k} = Psi_9 - Psi_k
            = sum_{s=9}^{k-1} (Psi_s - Psi_{s+1}).

At the canonical tight coefficient pair this reserve is still too small at
stage 12 and first pays the stage-7-to-stage-9 deficit at stage 13.  Endpoint
monotonicity extends only the stage-7-to-stage-13 comparison to the earlier
held-pair-feasible coefficient rectangle.  This is a finite exact-real block
GO, not a global or multi-admission telescope.
"""

from fractions import Fraction

from experiments.proof_audits.volume_gated_acceleration.moving_correction_stop import (
    one_step,
    residual,
    restricted_optimum,
)
from experiments.proof_audits.volume_gated_acceleration.tight_pair_local_chain import bank
from experiments.proof_audits.volume_gated_acceleration.tight_pair_schur_bank import (
    normalized_objective,
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
                    "post_delta": max(Fraction(0), max(post_residual) / alpha),
                    "post_error": max(
                        abs(value - target) for value, target in zip(padded_iterate, new_optimum)
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

    # Retain every phase boundary from the reviewed chronology.  Stages 9--13
    # are genuine consecutive fixed-U_4 held steps, not reordered snapshots.
    assert snapshots[6]["face"] == snapshots[7]["face"] == 3
    assert snapshots[6]["action"] == snapshots[7]["action"] == "hold"
    assert snapshots[8]["face"] == 3
    assert snapshots[8]["action"] == "admit"
    for stage in range(9, 14):
        assert snapshots[stage]["face"] == 4
        assert snapshots[stage]["action"] == "hold"

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
        11: (
            Fraction(5474018102528, 469488525390625),
            Fraction(78054021579111098864, 14789525645733642578125),
        ),
        12: (
            Fraction(157064386156018288, 16002516387939453125),
            Fraction(29100212066224527856, 5688279094512939453125),
        ),
        13: (
            Fraction(656143576744994256, 80012581939697265625),
            Fraction(1724650437028283454048, 369738141143341064453125),
        ),
    }
    for stage, (delta, error) in expected.items():
        assert snapshots[stage]["delta"] == delta
        assert snapshots[stage]["error"] == error

    # Exact held evidence beyond the Round-018 endpoint.  The outside row is
    # not a strong violation, while an active envelope row prevents the
    # terminal certificate at stages 11--13.
    expected_gate = {
        11: (
            Fraction(1, 625),
            Fraction(-66408660618026708057, 28441395472564697265625),
        ),
        12: (
            Fraction(492601759918033918783, 369738141143341064453125),
            Fraction(-974908390910707696, 400062909698486328125),
        ),
        13: (
            Fraction(8572706214243762091303, 9243453528583526611328125),
            Fraction(-4021680135990636848, 2000314548492431640625),
        ),
    }
    for stage, (outside, active_minimum) in expected_gate.items():
        assert snapshots[stage]["outside_residual"] == outside
        assert min(snapshots[stage]["envelope_residual"]) == active_minimum
        assert outside >= -alpha * tau
        assert active_minimum < -alpha * tau

    delta_6, error_6 = expected[6]
    delta_7, error_7 = expected[7]
    delta_9, error_9 = expected[9]
    delta_10, error_10 = expected[10]
    c_3 = (delta_7 - delta_6) / ((error_6 - error_7) / q)
    c_4 = (delta_9 - delta_10) / ((error_10 - error_9) / q)
    assert c_3 == Fraction(2978273417354, 42112483166425)
    assert c_4 == Fraction(95554102960761584, 1567701294665491845)

    optimum_drop = reset["old_value"] - reset["new_value"]
    assert optimum_drop == Fraction(175006441, 6398713140625)
    assert reset["post_delta"] == expected[8][0]
    assert reset["post_error"] == Fraction(13229, 1501825)

    banks = {
        stage: bank(delta, error, c_3 if stage <= 8 else c_4, q)
        for stage, (delta, error) in expected.items()
    }
    assert (
        banks[6]
        == banks[7]
        == Fraction(
            11198565794206524167944,
            1265364967829913056640625,
        )
    )
    assert banks[8] == Fraction(
        12539389225491032094208,
        1375396704162948974609375,
    )
    post_reset_bank = bank(reset["post_delta"], reset["post_error"], c_4, q)
    assert post_reset_bank == Fraction(
        12250921037449873344675915632,
        1177628430536760724699658203125,
    )
    assert (
        banks[9]
        == banks[10]
        == Fraction(
            8722450203325761493618137152,
            654238016964867069277587890625,
        )
    )
    assert banks[11] == Fraction(
        78123555433638913738320343552,
        5888142152683803623498291015625,
    )
    assert banks[12] == Fraction(
        57068639894967197464423352509641584,
        5017433131855686162673481231689453125,
    )
    assert banks[13] == Fraction(
        6189490926964855830995566821110704,
        643260657930216174701728363037109375,
    )
    assert banks[9] == banks[10] > banks[11] > banks[12] > banks[13] > 0

    psi = {
        stage: value * value + (optimum_drop if stage <= 8 else Fraction(0))
        for stage, value in banks.items()
    }

    # Keep the old production/reset/follow-up account exact and separate.  The
    # new reserve starts only after the positive stage-7-to-stage-9 deficit.
    psi_8_plus = post_reset_bank * post_reset_bank
    production_jump = psi[8] - psi[7]
    assert production_jump == Fraction(
        4798070852000000223973860697504672676758942656,
        1000717813631998065466639280969584524631500244140625,
    )
    assert production_jump > 0

    reset_change = psi_8_plus - psi[8]
    assert -reset_change == Fraction(
        13153352075844141929930465447315402255043873003664815010264484652155446410873317194853,
        5858303218542070115616289966440099116412997639614861194042012716938884968578815460205078125,
    )
    assert reset_change < 0

    followup_jump = psi[9] - psi_8_plus
    assert followup_jump == Fraction(
        185418883451039233414483427688468628491104384871211336448,
        2666939846939373614068372111818330675602595627307891845703125,
    )
    assert followup_jump > 0

    deficit = psi[9] - psi[7]
    assert deficit == Fraction(
        212119118576066028022993097362480113913974152962498585225695096903541477328114649390919,
        2943060211404325822565068748572471445947270419141748880957478373466923217833042144775390625,
    )
    assert deficit > 0
    assert deficit == production_jump + reset_change + followup_jump

    recovery = {}
    for stage in range(9, 14):
        recovery[stage] = psi[9] - psi[stage]
        telescoped = sum(
            (psi[index] - psi[index + 1] for index in range(9, stage)),
            Fraction(0),
        )
        assert recovery[stage] == telescoped
        assert psi[stage] - psi[7] == deficit - recovery[stage]

    assert recovery[9] == recovery[10] == 0
    assert 0 < recovery[11] < recovery[12] < recovery[13]

    # Stage 12 is the last failing endpoint and stage 13 is the first GO.
    # These exact gaps are the shortest-block certificate.
    stage_twelve_stop = psi[12] - psi[7]
    assert stage_twelve_stop == Fraction(
        7821810455784765796610400477362993713577245121092421165698554798545351057229313259270456043378499,
        330096438415373179006947743171039380514292768703056798967592936964624818773346004076302051544189453125,
    )
    assert stage_twelve_stop > 0

    stage_thirteen_slack = psi[7] - psi[13]
    assert stage_thirteen_slack == Fraction(
        12002644983985842036763876208645189025783281209947178157261192190739214790326278929352282941508109,
        916934551153814386130410397697331612539702135286268886021091491568402274370405566878616809844970703125,
    )
    assert stage_thirteen_slack > 0
    assert all(psi[stage] > psi[7] for stage in range(9, 13))
    assert psi[13] < psi[7]
    assert recovery[12] < deficit < recovery[13]

    # Rectangle extension uses endpoint monotonicity only.  The start bank is
    # increasing in c_3 and the stage-13 bank is increasing in c_4 because
    # both errors are positive.  Hence the tight pair maximizes the stage-13
    # minus stage-7 block change over c_3 >= c_3^tight and
    # 0 <= c_4 <= c_4^tight.  No rectangle-wide intermediate net sign is used.
    assert error_7 > 0
    assert expected[13][1] > 0
    for sample_c_3, sample_c_4 in (
        (c_3, c_4),
        (Fraction(1), c_4),
        (c_3, Fraction(0)),
        (Fraction(1), Fraction(0)),
    ):
        assert sample_c_3 >= c_3
        assert 0 <= sample_c_4 <= c_4
        sample_start = bank(delta_7, error_7, sample_c_3, q) ** 2 + optimum_drop
        sample_end = bank(expected[13][0], expected[13][1], sample_c_4, q) ** 2
        assert sample_end - sample_start <= psi[13] - psi[7] < 0

    assert admissions == [1, 2, 4, 8]
    assert terminal_stage == 16
    assert face_index == 4
    assert sum(degrees[: face_index + 1]) == 9
    assert swept_volume == 114

    print(
        "exact q=1/5 TightPair-Schur recovery block verified: the post-reset "
        "fixed-U_4 reserve is insufficient through stage 12 and first pays "
        "the stage-7-to-stage-9 deficit at stage 13; the 7->13 endpoint GO "
        "extends to the held-pair-feasible rectangle; J=4, T=16, "
        "nu_fin=9, swept volume=114, one terminal return"
    )


if __name__ == "__main__":
    main()
