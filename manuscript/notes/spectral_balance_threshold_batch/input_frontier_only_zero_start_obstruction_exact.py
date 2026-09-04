#!/usr/bin/env python3
"""Exact zero-start obstruction for input-frontier admission without pushes.

The arithmetic is Fraction-exact in random-walk degree coordinates.  This is
the input-frontier-only retained-prox chronology: it performs the lower
retraction and exact-positive admission, but neither the active residual push
nor the immediate diagonal push of newly appended rows.
"""

from __future__ import annotations

import json
from fractions import Fraction as F


VERTICES = 20
EDGES = [(vertex, vertex + 1) for vertex in range(VERTICES - 1)] + [(14, 18)]
ROOT = F(1, 224)
RHO = F(1067, 40000)
RELATIVE_WIDTH = F(1, 1000)


def fraction_record(value: F) -> dict[str, str]:
    """Return an exact representation plus a display-only decimal."""
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": f"{float(value):.17g}",
    }


def main() -> None:
    neighbors = [set() for _ in range(VERTICES)]
    for left, right in EDGES:
        neighbors[left].add(right)
        neighbors[right].add(left)
    degrees = list(map(len, neighbors))
    assert min(degrees) > 0

    root_squared = ROOT * ROOT
    alpha = root_squared / (2 - root_squared)
    diagonal = (1 + root_squared) / 2
    coupling = (1 - root_squared) / 2
    momentum = (1 - ROOT) / (1 + ROOT)
    auxiliary_scale = (1 - ROOT) / ROOT

    def shifted_operator(vector: list[F], face: set[int] | None = None) -> list[F]:
        if face is None:
            face = set(range(VERTICES))
        return [
            diagonal * vector[vertex]
            - coupling
            * sum(
                (vector[neighbor] for neighbor in neighbors[vertex] if neighbor in face),
                F(0),
            )
            / degrees[vertex]
            for vertex in range(VERTICES)
        ]

    width = 1 - RHO
    initial_width = width
    lower = [F(0) for _ in range(VERTICES)]
    certified = {0}
    phase = 0
    products = 0

    while width > RELATIVE_WIDTH * initial_width:
        old_lower = lower.copy()
        shifted_load = [
            root_squared
            / 2
            * (F(vertex == 0, degrees[0]) - RHO + old_lower[vertex])
            for vertex in range(VERTICES)
        ]
        current = old_lower.copy()
        previous = old_lower.copy()
        preceding_inner_width: F | None = None

        for iteration in range(20_000):
            extrapolate = [F(0) for _ in range(VERTICES)]
            for vertex in certified:
                extrapolate[vertex] = current[vertex] + momentum * (
                    current[vertex] - previous[vertex]
                )
            full_input_residual = [
                shifted_load[vertex] - value
                for vertex, value in enumerate(shifted_operator(extrapolate))
            ]
            input_batch = {
                vertex
                for vertex in range(VERTICES)
                if vertex not in certified and full_input_residual[vertex] > 0
            }
            certified.update(input_batch)

            extrapolate = [F(0) for _ in range(VERTICES)]
            for vertex in certified:
                extrapolate[vertex] = current[vertex] + momentum * (
                    current[vertex] - previous[vertex]
                )
            masked_operator = shifted_operator(extrapolate, certified)
            input_residual = [
                shifted_load[vertex] - masked_operator[vertex]
                for vertex in range(VERTICES)
            ]
            failing_vertex = min(certified, key=input_residual.__getitem__)
            if input_residual[failing_vertex] < 0:
                assert phase == 18
                assert iteration + 1 == 4
                assert products == 143
                assert failing_vertex == 18
                assert certified == set(range(16)) | {18}
                assert preceding_inner_width is not None
                assert preceding_inner_width > width / 4
                failure = input_residual[failing_vertex]
                print(
                    json.dumps(
                        {
                            "status": "counterexample",
                            "scope": (
                                "canonical zero-start input-frontier-only chronology; "
                                "active and append diagonal pushes are disabled"
                            ),
                            "vertices": VERTICES,
                            "edges": EDGES,
                            "source": 0,
                            "root": str(ROOT),
                            "alpha": str(alpha),
                            "rho": str(RHO),
                            "relative_width": str(RELATIVE_WIDTH),
                            "failure_phase_zero_based": phase,
                            "failure_product_in_phase_one_based": iteration + 1,
                            "products_before_failure": products,
                            "failure_vertex": failing_vertex,
                            "failure_face": sorted(certified),
                            "degree_coordinate_input_residual": fraction_record(failure),
                            "degree_residual_over_width": fraction_record(failure / width),
                            "preceding_inner_width_over_width": fraction_record(
                                preceding_inner_width / width
                            ),
                            "quarter_stop_would_execute_failure_product": True,
                        },
                        indent=2,
                        sort_keys=True,
                    )
                )
                return
            assert all(input_residual[vertex] >= 0 for vertex in certified)

            next_current = [F(0) for _ in range(VERTICES)]
            for vertex in certified:
                next_current[vertex] = extrapolate[vertex] + input_residual[vertex]
            previous, current = current, next_current

            active_operator = shifted_operator(current, certified)
            active_residual = [
                shifted_load[vertex] - active_operator[vertex]
                for vertex in range(VERTICES)
            ]
            face_indicator = [
                F(1) if vertex in certified else F(0) for vertex in range(VERTICES)
            ]
            constant_direction = shifted_operator(face_indicator, certified)
            shift = max(
                [F(0)]
                + [
                    -active_residual[vertex] / constant_direction[vertex]
                    for vertex in certified
                    if constant_direction[vertex] > 0
                ]
            )
            for vertex in certified:
                lower[vertex] = max(
                    lower[vertex], current[vertex] - shift, F(0)
                )

            auxiliary = [
                current[vertex]
                + auxiliary_scale * (current[vertex] - previous[vertex])
                for vertex in range(VERTICES)
            ]
            for vertex in certified:
                current[vertex] = max(current[vertex], lower[vertex])
                auxiliary[vertex] = max(auxiliary[vertex], lower[vertex])
                previous[vertex] = current[vertex] - (
                    auxiliary[vertex] - current[vertex]
                ) / auxiliary_scale

            full_lower_residual = [
                shifted_load[vertex] - value
                for vertex, value in enumerate(shifted_operator(lower))
            ]
            output_batch = {
                vertex
                for vertex in range(VERTICES)
                if vertex not in certified and full_lower_residual[vertex] > 0
            }
            certified.update(output_batch)
            inner_width = max(
                [F(0)]
                + [value / root_squared for value in full_lower_residual]
            )
            preceding_inner_width = inner_width
            products += 1
            if inner_width <= width / 4:
                break
        else:
            raise AssertionError("exact phase exceeded its product limit")

        width = width / 2 + inner_width
        phase += 1

    raise AssertionError("the expected exact counterexample was not reached")


if __name__ == "__main__":
    main()
