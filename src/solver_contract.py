"""Implementation-neutral request and result contracts for local solvers."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

import numpy as np

from src.graphs import GraphData


@dataclass(frozen=True, slots=True)
class SolverRequest:
    """Inputs and reproducibility metadata required for a solver run."""

    graph: GraphData
    source: int
    alpha: float
    epsilon: float
    epsilon_name: str
    random_seed: int
    stopping_rule: str
    solver_parameters: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0 <= self.source < self.graph.n:
            raise ValueError(f"source must be in [0, {self.graph.n}), got {self.source}")
        if not math.isfinite(self.alpha) or not 0.0 < self.alpha <= 1.0:
            raise ValueError(f"alpha must be finite and in (0, 1], got {self.alpha}")
        if not math.isfinite(self.epsilon) or self.epsilon <= 0.0:
            raise ValueError(f"epsilon must be finite and positive, got {self.epsilon}")
        if not self.epsilon_name.strip():
            raise ValueError("epsilon_name must be nonempty")
        if not self.stopping_rule.strip():
            raise ValueError("stopping_rule must be nonempty")


@dataclass(frozen=True, slots=True)
class WorkRecord:
    """Comparable work counters, with the unit stated explicitly."""

    edge_operations: float
    local_inner_iterations: int
    outer_acceleration_iterations: int
    runtime_seconds: float
    unit: str

    def __post_init__(self) -> None:
        numeric_values = {
            "edge_operations": self.edge_operations,
            "local_inner_iterations": self.local_inner_iterations,
            "outer_acceleration_iterations": self.outer_acceleration_iterations,
            "runtime_seconds": self.runtime_seconds,
        }
        for field_name, value in numeric_values.items():
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{field_name} must be finite and nonnegative, got {value}")
        if not self.unit.strip():
            raise ValueError("work unit must be nonempty")


@dataclass(frozen=True, slots=True)
class SolverResult:
    """Provider-neutral result returned by a solver adapter."""

    provider_id: str
    solver_id: str
    solution: np.ndarray
    coordinate_system: str
    work: WorkRecord
    metrics: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.provider_id.strip():
            raise ValueError("provider_id must be nonempty")
        if not self.solver_id.strip():
            raise ValueError("solver_id must be nonempty")
        if self.solution.ndim != 1:
            raise ValueError(f"solution must be one-dimensional, got {self.solution.shape}")
        if not self.coordinate_system.strip():
            raise ValueError("coordinate_system must be nonempty")


@runtime_checkable
class SolverBackend(Protocol):
    """Stable adapter boundary implemented inside a provider-owned package."""

    provider_id: str
    solver_id: str

    def solve(self, request: SolverRequest) -> SolverResult:
        """Run the solver without changing the request's declared conventions."""
        ...
