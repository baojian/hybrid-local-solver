#!/usr/bin/env python3
"""Exact reachable positive-residual projection witness and finite q screen.

The primary audit replays the literal zero-start transported-center recurrence
with the complete gate at ``q=12/625``.  It proves that projection can be
active on a row whose post-step residual is positive and that the original
score has positive causal debt at that checkpoint.  ``--screen`` repeats the
same exact graph at nine nearby rational q values.  That finite screen is not
an asymptotic family.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from experiments.proof_audits.volume_gated_acceleration.consumed_energy_reserve import (
    transported_energy,
)
from experiments.proof_audits.volume_gated_acceleration.nonpath_causal_stop import (
    ZERO,
    boundary,
    degrees_from_edges,
    neighbors_from_edges,
    objective,
    residual,
    restricted_optimum,
)

ORDER = 30
SEED = 7
WITNESS_Q = Fraction(12, 625)
EDGES = (
    (0, 6),
    (0, 12),
    (1, 2),
    (1, 8),
    (1, 9),
    (1, 10),
    (1, 21),
    (1, 24),
    (2, 9),
    (2, 14),
    (2, 18),
    (2, 25),
    (2, 26),
    (2, 27),
    (3, 4),
    (3, 6),
    (3, 14),
    (3, 15),
    (3, 17),
    (3, 18),
    (3, 19),
    (3, 23),
    (3, 24),
    (3, 26),
    (3, 27),
    (4, 11),
    (4, 18),
    (4, 27),
    (4, 28),
    (4, 29),
    (5, 11),
    (5, 15),
    (5, 21),
    (5, 22),
    (5, 29),
    (6, 13),
    (6, 14),
    (6, 16),
    (6, 20),
    (6, 24),
    (6, 28),
    (7, 8),
    (7, 13),
    (7, 15),
    (8, 10),
    (8, 11),
    (9, 11),
    (9, 20),
    (10, 17),
    (10, 28),
    (11, 26),
    (11, 27),
    (12, 13),
    (12, 16),
    (12, 23),
    (12, 28),
    (13, 18),
    (14, 15),
    (14, 21),
    (14, 22),
    (15, 24),
    (15, 29),
    (16, 24),
    (16, 27),
    (17, 21),
    (17, 25),
    (18, 21),
    (19, 20),
    (20, 27),
    (21, 28),
    (22, 25),
    (24, 25),
    (24, 28),
    (25, 27),
    (25, 28),
    (25, 29),
    (27, 29),
)

EXPECTED_CHRONOLOGY = (
    (1, "admit", (8, 13, 15)),
    (2, "admit", (10, 12, 18)),
    *((stage, "hold", ()) for stage in range(3, 10)),
    (10, "admit", (0, 1, 5, 6, 11, 14, 23, 24, 29)),
    (11, "hold", ()),
    (12, "hold", ()),
    (13, "admit", (3,)),
    *((stage, "hold", ()) for stage in range(14, 25)),
    (25, "admit", (2, 4, 9, 16, 17, 21, 22, 26, 28)),
    (26, "hold", ()),
    (27, "admit", (25, 27)),
    (28, "admit", (20,)),
    (29, "admit", (19,)),
    (30, "hold", ()),
    (31, "hold", ()),
    (32, "certify", ()),
)


def projected_step(iterate, center, active, seed, neighbors, degrees, q, rho):
    """Return exact interpolation, raw/projected candidates, normal, and center."""
    alpha = q * q
    interpolation = [
        (value + q * center_value) / (1 + q) for value, center_value in zip(iterate, center)
    ]
    gradient = residual(interpolation, active, seed, neighbors, degrees, alpha, rho)
    raw = [value - derivative for value, derivative in zip(interpolation, gradient)]
    candidate = [max(ZERO, value) for value in raw]
    normal = [new - old for new, old in zip(candidate, raw)]
    center_next = [new + (1 - q) * (new - old) / q for new, old in zip(candidate, iterate)]
    return interpolation, raw, candidate, normal, center_next


def replay(q):
    """Replay the complete gate using exact rational arithmetic."""
    alpha = q * q
    rho = tau = q / 5
    degrees = degrees_from_edges(ORDER, EDGES)
    neighbors = neighbors_from_edges(ORDER, EDGES)
    active = [SEED]
    iterate = [ZERO]
    center = [ZERO]
    optimum = restricted_optimum(active, SEED, neighbors, degrees, alpha, rho)
    assert min(optimum) > 0
    initial_energy = transported_energy(
        iterate,
        center,
        active,
        optimum,
        SEED,
        neighbors,
        degrees,
        alpha,
        rho,
    )
    credit = ZERO
    chronology = []
    projected_rows = []

    for stage in range(1, 100):
        active_before = active[:]
        optimum_before = optimum[:]
        interpolation, raw, candidate, normal, center_next = projected_step(
            iterate,
            center,
            active,
            SEED,
            neighbors,
            degrees,
            q,
            rho,
        )
        active_residual = residual(
            candidate,
            active,
            SEED,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        delta = max(ZERO, max(active_residual) / alpha)
        score = delta * delta
        energy = transported_energy(
            candidate,
            center_next,
            active,
            optimum,
            SEED,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        reserve = initial_energy + credit - energy
        assert reserve > 0
        anchor = [(1 - q) * value + q * star for value, star in zip(iterate, optimum_before)]
        assert min(anchor) > 0

        for index, value in enumerate(raw):
            if value < 0:
                debt = max(ZERO, score - credit)
                projected_rows.append(
                    {
                        "stage": stage,
                        "vertex": active[index],
                        "raw": value,
                        "interpolation": interpolation[index],
                        "candidate": candidate[index],
                        "normal": normal[index],
                        "post_residual": active_residual[index],
                        "max_residual": max(active_residual),
                        "anchor": anchor[index],
                        "normal_anchor": normal[index] / anchor[index],
                        "score": score,
                        "credit": credit,
                        "debt": debt,
                        "reserve": reserve,
                        "coefficient": debt / reserve,
                        "q4_coefficient": q**4 * debt / reserve,
                    }
                )

        envelope = [max(ZERO, value - delta) for value in candidate]
        envelope_residual = residual(
            envelope,
            active,
            SEED,
            neighbors,
            degrees,
            alpha,
            rho,
        )
        position = {vertex: index for index, vertex in enumerate(active)}
        outside = {}
        for vertex in boundary(active, neighbors):
            incoming = sum(
                (envelope[position[other]] for other in neighbors[vertex] if other in position),
                ZERO,
            )
            outside[vertex] = -(1 - alpha) * incoming / (2 * degrees[vertex]) + alpha * rho
        admitted = sorted(vertex for vertex, value in outside.items() if value < -alpha * tau)
        boundary_margins = [abs(value + alpha * tau) for value in outside.values()]
        assert all(margin > 0 for margin in boundary_margins)

        if admitted:
            action = "admit"
            decision_margin = min(boundary_margins)
            old_optimum = dict(zip(active_before, optimum_before))
            old_candidate = dict(zip(active_before, candidate))
            old_center = dict(zip(active_before, center_next))
            active += admitted
            new_optimum = restricted_optimum(
                active,
                SEED,
                neighbors,
                degrees,
                alpha,
                rho,
            )
            assert min(new_optimum) > 0
            padded_optimum = [old_optimum.get(vertex, ZERO) for vertex in active]
            iterate = [old_candidate.get(vertex, ZERO) for vertex in active]
            padded_center = [old_center.get(vertex, ZERO) for vertex in active]
            center = [
                value + new - old
                for value, new, old in zip(padded_center, new_optimum, padded_optimum)
            ]
            optimum = new_optimum
            drop = objective(
                padded_optimum,
                active,
                SEED,
                neighbors,
                degrees,
                alpha,
                rho,
            ) - objective(new_optimum, active, SEED, neighbors, degrees, alpha, rho)
            assert drop > 0
            credit += drop
        elif min(envelope_residual) >= -alpha * tau:
            action = "certify"
            decision_margin = min(envelope_residual) + alpha * tau
            if boundary_margins:
                decision_margin = min(decision_margin, min(boundary_margins))
            iterate, center = candidate, center_next
        else:
            action = "hold"
            decision_margin = -alpha * tau - min(envelope_residual)
            if boundary_margins:
                decision_margin = min(decision_margin, min(boundary_margins))
            iterate, center = candidate, center_next

        assert decision_margin > 0
        chronology.append((stage, action, tuple(admitted), decision_margin))
        if action == "certify":
            break

    return chronology, projected_rows


def witness_check():
    """Verify the promoted finite reachable-projection statement."""
    chronology, projected_rows = replay(WITNESS_Q)
    assert tuple(row[:3] for row in chronology) == EXPECTED_CHRONOLOGY
    assert min(row[3] for row in chronology) > Fraction(1, 20_000_000)
    assert [(row["stage"], row["vertex"]) for row in projected_rows] == [
        (11, 23),
        (12, 23),
        (13, 23),
    ]

    before, witness, after = projected_rows
    assert before["post_residual"] < 0
    assert after["post_residual"] < 0
    assert witness["interpolation"] == witness["candidate"] == 0
    assert witness["raw"] < 0 < witness["normal"]
    assert witness["post_residual"] == witness["max_residual"] > 0
    assert witness["anchor"] > 0
    assert Fraction(55_300, 10_000) < witness["normal_anchor"] < Fraction(55_301, 10_000)
    assert witness["score"] > witness["credit"]
    assert witness["debt"] > 0 < witness["reserve"]
    assert Fraction(866, 10_000) < witness["coefficient"] < Fraction(867, 10_000)
    assert (
        Fraction(1_178, 100_000_000_000)
        < witness["q4_coefficient"]
        < Fraction(1_179, 100_000_000_000)
    )
    return witness


def finite_q_screen():
    """Run the same graph on a finite nearby rational grid, without extrapolation."""
    q_values = [Fraction(numerator, 10_000) for numerator in range(187, 196)]
    rows = []
    relevant_ratios = []
    for q in q_values:
        chronology, projected_rows = replay(q)
        relevant = [row for row in projected_rows if row["post_residual"] > 0]
        assert chronology[-1][1] == "certify"
        if q in {Fraction(187, 10_000), Fraction(195, 10_000)}:
            assert not relevant
            rows.append((q, None, ZERO))
            continue
        assert len(relevant) == 1
        witness = relevant[0]
        assert witness["stage"] == 12 and witness["vertex"] == 23
        assert Fraction(98, 1_000) < q * witness["normal_anchor"] < Fraction(111, 1_000)
        relevant_ratios.append(witness["normal_anchor"])
        if q <= Fraction(191, 10_000):
            assert witness["debt"] == 0
        else:
            assert witness["debt"] > 0
        rows.append((q, witness["normal_anchor"], witness["q4_coefficient"]))
    assert relevant_ratios == sorted(relevant_ratios)
    return rows


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--screen",
        action="store_true",
        help="also run the nine-point exact nearby-q screen",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    witness = witness_check()
    print("reachable projection witness: PASS")
    print(f"q={WITNESS_Q}, terminal_stage=32, projected_row=(12, 23)")
    print(f"normal/anchor={float(witness['normal_anchor']):.12f}")
    print(f"debt={float(witness['debt']):.12e}")
    print(f"required_coefficient={float(witness['coefficient']):.12f}")
    print(f"q^4*required_coefficient={float(witness['q4_coefficient']):.12e}")
    if args.screen:
        print("finite exact q screen (no asymptotic inference):")
        for q, ratio, scaled_coefficient in finite_q_screen():
            if ratio is None:
                print(f"q={float(q):.4f}: no clipped positive-residual row")
            else:
                print(
                    f"q={float(q):.4f}: normal/anchor={float(ratio):.9f}, "
                    f"q*ratio={float(q * ratio):.9f}, "
                    f"q^4*lambda={float(scaled_coefficient):.12e}"
                )


if __name__ == "__main__":
    main()
