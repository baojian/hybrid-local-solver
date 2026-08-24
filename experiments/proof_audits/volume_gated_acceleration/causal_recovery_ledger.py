#!/usr/bin/env python3
"""Exact finite check for the Round-020 causal recovery ledger.

The checker replays the literal q=1/5 transported-center endpoint-path
execution and audits two consecutive canonical admissions, at stages 4 and 8.
For the observable face score A=delta^2, it maintains the causal credit

    C^+ = C^- + Delta + A^- - A^+,

where Delta is zero on a fixed-face transition and is the exact realized
restricted-optimum drop on an admission.  The update is evaluated only after
the new score and any Schur drop are available.  Positive score decreases are
credited, score increases are debited, and no future decrease is borrowed.

The two-admission ledger stays solvent.  If the unused stage-4 credit is
discarded and the stage-8 block is restarted from stage 7, the local account
is negative through stage 11 and first becomes nonnegative at stage 12.  This
is a finite exact-real GO/STOP, not a global recovery-horizon theorem.
"""

from fractions import Fraction

from experiments.proof_audits.volume_gated_acceleration.moving_correction_stop import (
    one_step,
    residual,
    restricted_optimum,
)
from experiments.proof_audits.volume_gated_acceleration.tight_pair_schur_bank import (
    normalized_objective,
)


def score(delta):
    """Observable squared global-correction score."""
    return delta * delta


def update_credit(credit, old_score, new_score, realized_drop=Fraction(0)):
    """Apply one causal transition and expose its decrease/rise split."""
    decrease = max(Fraction(0), old_score - new_score)
    increase = max(Fraction(0), new_score - old_score)
    updated = credit + realized_drop + decrease - increase
    assert updated == credit + realized_drop + old_score - new_score
    return updated, decrease, increase


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
    resets = {}

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
            post_residual = residual(
                padded_iterate,
                degrees[: face_index + 2],
                alpha,
                rho,
            )
            resets[stage] = {
                "pre_delta": delta,
                "post_delta": max(Fraction(0), max(post_residual) / alpha),
                "drop": normalized_objective(
                    old_optimum + [Fraction(0)],
                    degrees[: face_index + 2],
                    alpha,
                    rho,
                )
                - normalized_objective(
                    new_optimum,
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
            "outside_residual": outside_residual,
            "envelope_residual": envelope_residual,
        }
        if action == "certify":
            break
    else:
        raise AssertionError("the exact q=1/5 run did not terminate")

    expected_delta = {
        3: Fraction(0),
        4: Fraction(0),
        5: Fraction(0),
        6: Fraction(14898928, 2462890625),
        7: Fraction(6291729688, 751181640625),
        8: Fraction(28990137728, 3755908203125),
        9: Fraction(228031410368, 18779541015625),
        10: Fraction(1115890388544, 93897705078125),
        11: Fraction(5474018102528, 469488525390625),
        12: Fraction(157064386156018288, 16002516387939453125),
    }
    for stage, delta in expected_delta.items():
        assert snapshots[stage]["delta"] == delta

    # These are consecutive canonical admissions in the reviewed trace.
    assert snapshots[3]["face"] == snapshots[4]["face"] == 2
    assert snapshots[3]["action"] == "hold"
    assert snapshots[4]["action"] == "admit"
    assert snapshots[5]["face"] == snapshots[7]["face"] == 3
    assert all(snapshots[stage]["action"] == "hold" for stage in range(5, 8))
    assert snapshots[8]["face"] == 3
    assert snapshots[8]["action"] == "admit"
    assert all(
        snapshots[stage]["face"] == 4 and snapshots[stage]["action"] == "hold"
        for stage in range(9, 13)
    )

    drop_4 = resets[4]["drop"]
    drop_8 = resets[8]["drop"]
    assert drop_4 == Fraction(858637, 6497453125)
    assert drop_8 == Fraction(175006441, 6398713140625)
    assert resets[4]["pre_delta"] == resets[4]["post_delta"] == 0
    assert resets[8]["pre_delta"] == resets[8]["post_delta"] == expected_delta[8]

    scores = {stage: score(delta) for stage, delta in expected_delta.items()}
    scores["4+"] = score(resets[4]["post_delta"])
    scores["8+"] = score(resets[8]["post_delta"])

    # Face-general causal ledger across both admissions.  Start at the held
    # stage-3 checkpoint, credit each exact drop only at its reset, and debit
    # every subsequent score increase.  No future state enters an update.
    transitions = (
        (4, Fraction(0)),
        ("4+", drop_4),
        (5, Fraction(0)),
        (6, Fraction(0)),
        (7, Fraction(0)),
        (8, Fraction(0)),
        ("8+", drop_8),
        (9, Fraction(0)),
        (10, Fraction(0)),
        (11, Fraction(0)),
        (12, Fraction(0)),
    )
    credit = Fraction(0)
    old_score = scores[3]
    credits = {3: credit}
    realized_drop_sum = Fraction(0)
    for checkpoint, realized_drop in transitions:
        credit, _decrease, _increase = update_credit(
            credit,
            old_score,
            scores[checkpoint],
            realized_drop,
        )
        realized_drop_sum += realized_drop
        assert credit == scores[3] + realized_drop_sum - scores[checkpoint]
        credits[checkpoint] = credit
        old_score = scores[checkpoint]

    # The first admission is an immediate reset GO: production and first
    # follow-up leave A=0, while its exact Schur drop is realized at 4- -> 4+.
    assert scores[3] == scores[4] == scores["4+"] == scores[5] == 0
    assert credits["4+"] == credits[5] == drop_4 > 0

    # The carried ledger is solvent at every checkpoint.  Its narrowest
    # positive margin after the first admission occurs immediately after the
    # second admission's follow-up, at stage 9.
    assert all(credits[checkpoint] >= 0 for checkpoint, _ in transitions)
    post_first_credits = [credits[checkpoint] for checkpoint, _ in transitions[1:]]
    assert min(post_first_credits) == credits[9]
    assert credits[9] == Fraction(
        19651905005344050452901946,
        1629693433860599994659423828125,
    )
    assert credits[9] > 0

    # Restarting the same causal account at stage 7 deliberately discards the
    # unused stage-4 credit.  Keep production, reset, and follow-up separate.
    local_credit = Fraction(0)
    local_credit, production_decrease, production_increase = update_credit(
        local_credit,
        scores[7],
        scores[8],
    )
    assert production_decrease > 0
    assert production_increase == 0
    local_credit, reset_decrease, reset_increase = update_credit(
        local_credit,
        scores[8],
        scores["8+"],
        drop_8,
    )
    assert reset_decrease == reset_increase == 0
    local_credit, followup_decrease, followup_increase = update_credit(
        local_credit,
        scores["8+"],
        scores[9],
    )
    assert followup_decrease == 0
    assert followup_increase > 0
    local_credits = {9: local_credit}
    old_score = scores[9]
    for stage in range(10, 13):
        local_credit, decrease, increase = update_credit(
            local_credit,
            old_score,
            scores[stage],
        )
        assert decrease > 0
        assert increase == 0
        local_credits[stage] = local_credit
        old_score = scores[stage]

    deficit = scores[9] - (scores[7] + drop_8)
    assert deficit == Fraction(
        554786577946334102644597007243,
        11109620138627710163593292236328125,
    )
    assert deficit > 0
    assert local_credits[9] == -deficit

    recovery_11 = scores[9] - scores[11]
    recovery_12 = scores[9] - scores[12]
    assert recovery_11 < deficit < recovery_12
    assert local_credits[11] == -Fraction(
        266914703353796147278415896540763,
        6943512586642318852245807647705078125,
    )
    assert local_credits[12] == Fraction(
        1384575499982769519202601001412515901,
        1183348132578517190393991768360137939453125,
    )
    assert all(local_credits[stage] < 0 for stage in range(9, 12))
    assert local_credits[12] > 0

    # The exact cross-state cancellation: credit left after the earlier block
    # is larger than the restarted stage-8 deficit and makes stage 9 solvent.
    prior_credit_at_7 = drop_4 - scores[7]
    assert prior_credit_at_7 == credits[7] > 0
    assert credits[9] == prior_credit_at_7 + local_credits[9] > 0

    # Preserve the complete literal execution and the quantities underlying
    # its already reviewed eleven-coordinate vector.
    assert admissions == [1, 2, 4, 8]
    assert terminal_stage == 16
    assert face_index == 4
    assert sum(degrees[: face_index + 1]) == 9
    assert face_index + 1 == 5
    assert swept_volume == 114

    print(
        "exact q=1/5 causal delta^2 recovery ledger verified: the stage-4 "
        "Schur credit stays solvent across the second canonical admission at "
        "stage 8; without that carry, stage 11 is the last local STOP and "
        "stage 12 the first local GO; J=4, T=16, nu_fin=9, swept volume=114, "
        "one terminal return"
    )


if __name__ == "__main__":
    main()
