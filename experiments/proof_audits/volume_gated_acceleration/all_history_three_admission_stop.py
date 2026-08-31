#!/usr/bin/env python3
"""Exact all-history causal-ledger STOP after three singleton admissions.

The witness replays the declared zero-start transported-center recurrence and
complete all-boundary gate.  Its causal account starts at the actual initial
state, credits all three exact restricted-optimum drops only after their
admissions, and nevertheless becomes negative at held stages 7 and 8.
"""

from fractions import Fraction

from experiments.proof_audits.volume_gated_acceleration.nonpath_causal_stop import (
    ZERO,
    degrees_from_edges,
    neighbors_from_edges,
    one_vertex_schur_data,
    replay,
    residual,
)


EDGES = ((0, 2), (0, 5), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5))
SEED = 0


def score(delta):
    """Return the observable causal score Xi=delta^2."""
    return delta * delta


def main():
    alpha = rho = tau = Fraction(1, 25)
    threshold = -alpha * tau
    degrees = degrees_from_edges(6, EDGES)
    neighbors = neighbors_from_edges(6, EDGES)
    run = replay(6, EDGES, SEED)
    assert run is not None
    snapshots = run["snapshots"]

    assert tuple(degrees) == (2, 2, 3, 3, 2, 2)
    assert run["admissions"] == [(1, (5,)), (2, (2,)), (3, (4,))]
    assert run["terminal_stage"] == 12
    assert run["active"] == (0, 5, 2, 4)
    assert run["swept_volume"] == 94
    assert {
        stage: (snapshot["action"], snapshot["admitted"]) for stage, snapshot in snapshots.items()
    } == {
        1: ("admit", (5,)),
        2: ("admit", (2,)),
        3: ("admit", (4,)),
        4: ("hold", ()),
        5: ("hold", ()),
        6: ("hold", ()),
        7: ("hold", ()),
        8: ("hold", ()),
        9: ("hold", ()),
        10: ("hold", ()),
        11: ("hold", ()),
        12: ("certify", ()),
    }

    # The zero-start state is an actual checkpoint with Xi_0=0: its only
    # active normalized residual is negative.  Projection is inactive on the
    # entire replay, so this is the literal unprojected recurrence.
    initial_residual = residual([ZERO], [SEED], SEED, neighbors, degrees, alpha, rho)
    assert initial_residual == [-Fraction(23, 1250)]
    initial_delta = max(ZERO, max(initial_residual) / alpha)
    assert initial_delta == 0
    assert min((min(snapshot["candidate"]), stage) for stage, snapshot in snapshots.items()) == (
        Fraction(122521790117, 27766447109375),
        4,
    )

    # Exact complete-gate inequalities for the three singleton admissions.
    assert snapshots[1]["outside"] == {
        2: -Fraction(21, 15625),
        5: -Fraction(44, 15625),
    }
    assert snapshots[1]["outside"][5] < threshold < snapshots[1]["outside"][2]
    assert snapshots[2]["outside"] == {
        2: -Fraction(75383, 19296875),
        4: -Fraction(3481, 19296875),
    }
    assert snapshots[2]["outside"][2] < threshold < snapshots[2]["outside"][4]
    assert snapshots[3]["outside"] == {
        1: -Fraction(350187, 10516796875),
        3: Fraction(16126501, 31550390625),
        4: -Fraction(22847009, 10516796875),
    }
    assert snapshots[3]["outside"][4] < threshold
    assert snapshots[3]["outside"][1] > threshold
    assert snapshots[3]["outside"][3] > threshold

    # Recheck the complete held/certify gate rather than relying only on the
    # stored action word.  No fourth boundary admission occurs before debt.
    for stage in range(4, 13):
        snapshot = snapshots[stage]
        assert all(value >= threshold for value in snapshot["outside"].values())
        envelope = [max(ZERO, value - snapshot["delta"]) for value in snapshot["candidate"]]
        envelope_residual = residual(
            envelope,
            list(snapshot["active"]),
            SEED,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        if stage < 12:
            assert min(envelope_residual) < threshold
        else:
            assert min(envelope_residual) >= threshold

    # Each admission is one cell.  The independently reconstructed response
    # load a_j and symmetric Schur pivot S_j give Delta_j=a_j^2/(2S_j).
    schur_data = (
        ([0], 5, Fraction(112, 8125), Fraction(266, 325)),
        ([0, 5], 2, Fraction(189, 11875), Fraction(4251, 3325)),
        ([0, 5, 2], 4, Fraction(5758, 885625), Fraction(26402, 35425)),
    )
    expected_drops = (
        Fraction(448, 3859375),
        Fraction(83349, 841343750),
        Fraction(8288641, 292278390625),
    )
    for stage, (active, new_vertex, load, pivot) in enumerate(schur_data, 1):
        assert one_vertex_schur_data(active, new_vertex, SEED, neighbors, degrees, alpha, rho) == (
            load,
            pivot,
        )
        assert snapshots[stage]["drop"] == load * load / (2 * pivot)
        assert snapshots[stage]["drop"] == expected_drops[stage - 1]
        assert snapshots[stage]["delta"] == snapshots[stage]["post_delta"] == 0
    total_drop = sum(expected_drops, ZERO)
    assert total_drop == Fraction(1305901, 5362906250)
    assert all(snapshots[stage]["drop"] == 0 for stage in range(4, 13))

    expected_delta = {
        4: Fraction(68404, 57890625),
        5: Fraction(10885816, 868359375),
        6: Fraction(7313695268, 473255859375),
        7: Fraction(4203572544, 262919921875),
        8: Fraction(185930836928, 11831396484375),
        9: Fraction(99925982336, 7098837890625),
    }
    for stage, delta in expected_delta.items():
        assert snapshots[stage]["delta"] == delta

    # Replay the causal updates in their literal order: recurrence to the
    # pre-gate candidate, then (only on admission) the realized drop and the
    # post-padding score.  At every checkpoint the update telescopes to
    # C=Xi_0+sum(Delta)-Xi with Xi_0=0.
    credit = ZERO
    old_score = score(initial_delta)
    realized_drop = ZERO
    balances = {}
    for stage, snapshot in snapshots.items():
        pre_score = score(snapshot["delta"])
        credit += old_score - pre_score
        assert credit == realized_drop - pre_score
        if snapshot["action"] == "admit":
            post_score = score(snapshot["post_delta"])
            credit += snapshot["drop"] + pre_score - post_score
            realized_drop += snapshot["drop"]
            assert credit == realized_drop - post_score
            old_score = post_score
        else:
            old_score = pre_score
        balances[stage] = credit

    assert realized_drop == total_drop
    assert all(balances[stage] > 0 for stage in range(3, 7))
    assert balances[7] == -Fraction(
        22103647843883061483647,
        1825088026185798645019531250,
    )
    assert balances[8] == -Fraction(
        12773370221603745001096343,
        3695803253026242256164550781250,
    )
    assert balances[9] == Fraction(
        60353079797207948733177433,
        1330489171089447212219238281250,
    )
    assert balances[7] < 0 and balances[8] < 0
    assert all(balances[stage] > 0 for stage in range(9, 13))

    print(
        "exact three-admission all-history STOP verified: stages 1--3 admit "
        "singletons 5,2,4; the actual zero-start causal balance is negative "
        "at held stages 7--8 and recovers at stage 9; J=3, T=12, "
        "nu_fin=9, n_fin=4, swept volume=94"
    )


if __name__ == "__main__":
    main()
