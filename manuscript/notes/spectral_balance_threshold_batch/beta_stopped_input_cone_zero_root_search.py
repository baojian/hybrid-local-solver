#!/usr/bin/env python3
"""Fast floating search in the removable ``s=0`` retained-prox limit.

This unregistered helper uses the scaled-state recurrence certified by
``retained_prox_input_cone_zero_root_limit_exact.py``.  Unlike a tiny-alpha
floating trace, its residuals stay order one, so cancellation does not hide
the strict input-cone sign.  Candidates remain heuristic until replayed by
the Fraction-exact limit tracer and then lifted at a positive rational root.
"""

from __future__ import annotations

import math

import numpy as np
from numba import njit


@njit(cache=True)
def evaluate_zero_root(
    adjacency: np.ndarray,
    rho_scale: float,
    beta: float,
    maximum_phases: int = 70,
    maximum_products: int = 100,
) -> tuple[int, float, int, int, int, float, float, int, int]:
    """Return status, failure data, and the true chronology-cell bounds."""
    vertices = adjacency.shape[0]
    degrees = np.empty(vertices)
    for vertex in range(vertices):
        degrees[vertex] = np.sum(adjacency[vertex])
        if degrees[vertex] <= 0.0:
            return -1, math.inf, -1, -1, -1, 0.0, 0.5, 0, 0

    matrix = np.zeros((vertices, vertices))
    for left in range(vertices):
        matrix[left, left] = 0.5
        for right in range(vertices):
            if adjacency[left, right] != 0.0:
                matrix[left, right] = -0.5 / degrees[left]

    rho = rho_scale / degrees[0]
    load = np.full(vertices, -rho)
    load[0] += 1.0 / degrees[0]
    lower = np.zeros(vertices)
    certified = np.zeros(vertices, dtype=np.bool_)
    certified[0] = True
    width = 1.0 / degrees[0] - rho
    initial_width = width
    chronology_lower = 0.0
    chronology_upper = 0.5
    total_products = 0
    tolerance = 1.0e-13

    for phase in range(1, maximum_phases + 1):
        if width <= 1.0e-3 * initial_width:
            return (
                0,
                math.inf,
                -1,
                -1,
                -1,
                chronology_lower,
                chronology_upper,
                total_products,
                phase - 1,
            )
        old_width = width
        current = lower.copy()
        velocity = np.zeros(vertices)

        for product in range(1, maximum_products + 1):
            extrapolate = np.zeros(vertices)
            for vertex in range(vertices):
                if certified[vertex]:
                    extrapolate[vertex] = current[vertex] + velocity[vertex]
            input_residual = load - matrix @ extrapolate
            for vertex in range(vertices):
                if not certified[vertex] and input_residual[vertex] > tolerance:
                    certified[vertex] = True

            input_vertex = -1
            input_value = math.inf
            for vertex in range(vertices):
                if certified[vertex] and input_residual[vertex] < input_value:
                    input_vertex = vertex
                    input_value = input_residual[vertex]
            if input_value < -tolerance:
                return (
                    1,
                    input_value / old_width,
                    phase,
                    product,
                    input_vertex,
                    chronology_lower,
                    chronology_upper,
                    total_products,
                    phase - 1,
                )

            old_current = current.copy()
            following = np.zeros(vertices)
            for vertex in range(vertices):
                if certified[vertex]:
                    following[vertex] = extrapolate[vertex] + input_residual[vertex]
            for vertex in range(vertices):
                if certified[vertex]:
                    raw_velocity = following[vertex] - old_current[vertex]
                    lower[vertex] = max(lower[vertex], following[vertex], 0.0)
                    current[vertex] = lower[vertex]
                    velocity[vertex] = max(raw_velocity, 0.0)

            residual = load - matrix @ lower
            for vertex in range(vertices):
                if certified[vertex] and residual[vertex] > tolerance:
                    lower[vertex] += 2.0 * residual[vertex]
                    current[vertex] = lower[vertex]
            residual = load - matrix @ lower

            while True:
                admitted = False
                for vertex in range(vertices):
                    if not certified[vertex] and residual[vertex] > tolerance:
                        certified[vertex] = True
                        lower[vertex] += 2.0 * residual[vertex]
                        current[vertex] = lower[vertex]
                        velocity[vertex] = 0.0
                        admitted = True
                if not admitted:
                    break
                residual = load - matrix @ lower

            maximum = 0.0
            for vertex in range(vertices):
                if residual[vertex] > maximum:
                    maximum = residual[vertex]
            ratio = maximum / (2.0 * old_width)
            total_products += 1
            if ratio <= beta:
                chronology_lower = max(chronology_lower, ratio)
                width = old_width / 2.0 + maximum / 2.0
                break
            chronology_upper = min(chronology_upper, ratio)
        else:
            return (
                -2,
                math.inf,
                phase,
                maximum_products,
                -1,
                chronology_lower,
                chronology_upper,
                total_products,
                phase,
            )

    return (
        -3,
        math.inf,
        maximum_phases,
        -1,
        -1,
        chronology_lower,
        chronology_upper,
        total_products,
        maximum_phases,
    )

