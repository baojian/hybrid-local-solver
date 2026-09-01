#!/usr/bin/env python3
"""Exact Q(sqrt(10)) audit of the 40-vertex Green-band stress trace.

The witness has several root-scale publication gaps.  It rigorously rejects
large constants in two tempting local charges (packet-energy fraction and
global remaining-Green/face-growth progress) without refuting the overall
shared-clock conjecture.
"""

from __future__ import annotations

from decimal import getcontext
from fractions import Fraction as F

from exact_delayed_clock import K, maximum, solve_fraction
from two_mask_experiments import green_band_stress_graph


def main() -> None:
    getcontext().prec = 60
    adjacency = green_band_stress_graph()
    vertex_count = len(adjacency)
    neighbors = [set(map(int, adjacency[vertex].nonzero()[0])) for vertex in range(vertex_count)]
    degrees = [len(row) for row in neighbors]
    edges = [
        (left, right)
        for left in range(vertex_count)
        for right in neighbors[left]
        if left < right
    ]
    assert vertex_count == 40 and len(edges) == 55 and degrees[0] == 7

    alpha = F(1, 1000)
    rho_scale = F(16_294_035_977_595_616, 10**22)
    rho = rho_scale / degrees[0]
    objective_tolerance = F(1, 10**20)
    publication_threshold_squared = alpha * rho * objective_tolerance / 256
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    beta = K(F(1001, 999), F(-20, 999))
    auxiliary_scale = K(F(-1), F(10))

    conjugated_load = [F(-alpha * rho) for _ in range(vertex_count)]
    conjugated_load[0] += alpha / degrees[0]

    full_matrix = [[F(0) for _ in range(vertex_count)] for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        full_matrix[vertex][vertex] = diagonal * degrees[vertex]
    for left, right in edges:
        full_matrix[left][right] = -coupling
        full_matrix[right][left] = -coupling

    load = [degrees[vertex] * conjugated_load[vertex] for vertex in range(vertex_count)]
    full_center = solve_fraction(full_matrix, load)
    assert all(coordinate > 0 for coordinate in full_center)
    full_green = solve_fraction(
        full_matrix,
        [alpha if vertex == 0 else F(0) for vertex in range(vertex_count)],
    )
    assert sum(degrees[vertex] * full_green[vertex] for vertex in range(vertex_count)) == 1
    assert all(
        any(full_green[neighbor] > full_green[vertex] for neighbor in neighbors[vertex])
        for vertex in range(1, vertex_count)
    )

    scratch = {0}
    certified = {0}
    current = [K() for _ in range(vertex_count)]
    previous = [K() for _ in range(vertex_count)]
    lower = [K() for _ in range(vertex_count)]
    events: list[tuple[int, tuple[int, ...]]] = []

    def h_apply(state: list[K], vertex: int) -> K:
        return diagonal * degrees[vertex] * state[vertex] - coupling * sum(
            (state[neighbor] for neighbor in neighbors[vertex]),
            K(),
        )

    for iteration in range(110):
        extrapolated = [K() for _ in range(vertex_count)]
        next_iterate = [K() for _ in range(vertex_count)]
        for vertex in scratch:
            extrapolated[vertex] = current[vertex] + beta * (
                current[vertex] - previous[vertex]
            )
        for vertex in scratch:
            neighbor_sum = sum(
                (
                    extrapolated[neighbor]
                    for neighbor in neighbors[vertex]
                    if neighbor in scratch
                ),
                K(),
            )
            next_iterate[vertex] = coupling * (
                extrapolated[vertex] + neighbor_sum / degrees[vertex]
            ) + conjugated_load[vertex]
        previous, current = current, next_iterate

        ratios: list[K] = []
        for vertex in scratch:
            active_residual = degrees[vertex] * conjugated_load[vertex] - h_apply(
                current,
                vertex,
            )
            stationary = diagonal * degrees[vertex] - coupling * len(
                neighbors[vertex] & scratch
            )
            ratios.append((-active_residual) / stationary)
        shift = maximum([K()] + ratios)
        for vertex in scratch:
            candidate = current[vertex] - shift
            if candidate > lower[vertex]:
                lower[vertex] = candidate

        auxiliary = [K() for _ in range(vertex_count)]
        for vertex in scratch:
            auxiliary[vertex] = current[vertex] + auxiliary_scale * (
                current[vertex] - previous[vertex]
            )
            if current[vertex] < lower[vertex]:
                current[vertex] = lower[vertex]
            if auxiliary[vertex] < lower[vertex]:
                auxiliary[vertex] = lower[vertex]
            velocity = (auxiliary[vertex] - current[vertex]) / auxiliary_scale
            previous[vertex] = current[vertex] - velocity

        outside = sorted(set(range(vertex_count)) - certified)
        residuals = {
            vertex: degrees[vertex] * conjugated_load[vertex] - h_apply(lower, vertex)
            for vertex in outside
        }
        batch = tuple(vertex for vertex in outside if residuals[vertex] > 0)
        if batch:
            # At this explicit objective accuracy, the manuscript's finite
            # publication threshold selects exactly the same positive batch.
            assert all(
                residuals[vertex] * residuals[vertex]
                > degrees[vertex] * publication_threshold_squared
                for vertex in batch
            )
            events.append((iteration, batch))
            scratch.update(batch)
            certified.update(batch)

    expected = [
        (0, (1, 2, 10, 11, 23, 24, 38)),
        (1, (3, 5, 6, 8, 9, 17, 19, 30, 31, 34, 39)),
        (2, (4, 7, 12, 13, 14, 15, 18, 20, 21, 25, 27, 28, 29, 32, 37)),
        (41, (16,)),
        (91, (26,)),
        (92, (22, 35, 36)),
        (109, (33,)),
    ]
    assert events == expected and len(certified) == vertex_count

    faces = [{0}]
    for _, batch in events:
        faces.append(faces[-1] | set(batch))

    # The complements of nested source-rooted faces form a laminar component
    # forest.  Each component's Green maximum is an entrance vertex whose
    # strictly higher Green neighbor already belongs to the face.
    previous_components: list[set[int]] | None = None
    for face in faces[:-1]:
        unseen = set(range(vertex_count)) - face
        components: list[set[int]] = []
        while unseen:
            seed = next(iter(unseen))
            component = {seed}
            stack = [seed]
            unseen.remove(seed)
            while stack:
                vertex = stack.pop()
                for neighbor in neighbors[vertex] & unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
            components.append(component)
        if previous_components is not None:
            assert all(
                sum(component <= parent for parent in previous_components) == 1
                for component in components
            )
        for component in components:
            component_maximum = max(full_green[vertex] for vertex in component)
            maximizers = [
                vertex
                for vertex in component
                if full_green[vertex] == component_maximum
            ]
            assert all(
                any(
                    neighbor in face
                    and full_green[neighbor] > full_green[vertex]
                    for neighbor in neighbors[vertex]
                )
                for vertex in maximizers
            )
            solution_maximum = max(full_center[vertex] for vertex in component)
            solution_maximizers = [
                vertex
                for vertex in component
                if full_center[vertex] == solution_maximum
            ]
            assert all(
                any(
                    neighbor in face
                    and full_center[neighbor] > full_center[vertex]
                    for neighbor in neighbors[vertex]
                )
                for vertex in solution_maximizers
            )
        previous_components = components

    centers: list[list[F]] = []
    for face in faces:
        ordered = sorted(face)
        center_on_face = solve_fraction(
            [[full_matrix[left][right] for right in ordered] for left in ordered],
            [load[vertex] for vertex in ordered],
        )
        center = [F(0) for _ in range(vertex_count)]
        for vertex, value in zip(ordered, center_on_face):
            center[vertex] = value
        centers.append(center)

    packet_energies: list[F] = []
    for old, new in zip(centers, centers[1:]):
        packet = [new[index] - old[index] for index in range(vertex_count)]
        energy = sum(
            packet[left] * full_matrix[left][right] * packet[right]
            for left in range(vertex_count)
            for right in range(vertex_count)
        )
        packet_energies.append(energy)

    remaining_energy = [
        sum(packet_energies[index:], F(0)) for index in range(len(packet_energies))
    ]
    delayed_release = packet_energies[3] / remaining_energy[3]
    assert delayed_release < F(1, 30)

    face_before_41 = faces[3]
    face_after_41 = faces[4]
    face_before_91 = faces[4]
    face_after_91 = faces[5]
    volume = lambda face: sum(degrees[vertex] for vertex in face)
    assert F(volume(face_after_41), volume(face_before_41)) == F(26, 25)
    assert F(volume(face_after_91), volume(face_before_91)) == F(105, 104)

    def remaining_max(face: set[int]) -> F:
        return max(full_green[vertex] for vertex in set(range(vertex_count)) - face)

    def remaining_solution_max(face: set[int]) -> F:
        return max(full_center[vertex] for vertex in set(range(vertex_count)) - face)

    assert remaining_max(face_before_41) == remaining_max(face_after_41)
    assert remaining_max(face_before_91) == remaining_max(face_after_91)
    assert remaining_solution_max(face_before_41) == remaining_solution_max(face_after_41)
    assert remaining_solution_max(face_before_91) == remaining_solution_max(face_after_91)

    print("exact_field=Q(sqrt(10)) comparisons=pass")
    print("eps_obj=1e-20 thresholded_batches=same")
    print("events=", events)
    print("delayed_release_fraction_less_than=1/30")
    print("delayed_release_decimal=", float(delayed_release))
    print("event41_volume_growth=26/25 remaining_Green_max_ratio=1")
    print("event91_volume_growth=105/104 remaining_Green_max_ratio=1")
    print("event41_and_event91_remaining_solution_max_ratio=1")
    print("complement_component_forest_and_Green_solution_port_maxima=pass")
    print("overall_shared_clock_not_refuted=true")


if __name__ == "__main__":
    main()
