import numpy as np
import pytest
import scipy.sparse as sp

from src.graphs import GraphData
from src.solver_contract import SolverBackend, SolverRequest, SolverResult, WorkRecord


def _request() -> SolverRequest:
    adjacency = sp.csr_matrix(np.array([[0.0, 1.0], [1.0, 0.0]]))
    graph = GraphData("edge", adjacency, np.array([1.0, 1.0]))
    return SolverRequest(
        graph=graph,
        source=0,
        alpha=0.1,
        epsilon=1e-4,
        epsilon_name="eps_test",
        random_seed=17,
        stopping_rule="declared test rule",
    )


class _Backend:
    provider_id = "fixture"
    solver_id = "zero"

    def solve(self, request: SolverRequest) -> SolverResult:
        return SolverResult(
            provider_id=self.provider_id,
            solver_id=self.solver_id,
            solution=np.zeros(request.graph.n),
            coordinate_system="x",
            work=WorkRecord(0.0, 0, 0, 0.0, "fixture operations"),
        )


def test_backend_satisfies_neutral_contract():
    backend = _Backend()
    result = backend.solve(_request())

    assert isinstance(backend, SolverBackend)
    assert result.provider_id == "fixture"
    assert result.solution.shape == (2,)


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"source": 2}, "source must be"),
        ({"alpha": 0.0}, "alpha must be"),
        ({"epsilon": 0.0}, "epsilon must be"),
        ({"epsilon_name": ""}, "epsilon_name"),
        ({"stopping_rule": ""}, "stopping_rule"),
    ],
)
def test_request_rejects_incomplete_or_invalid_contract(changes, message):
    values = {
        "graph": _request().graph,
        "source": 0,
        "alpha": 0.1,
        "epsilon": 1e-4,
        "epsilon_name": "eps_test",
        "random_seed": 17,
        "stopping_rule": "declared test rule",
    }
    values.update(changes)

    with pytest.raises(ValueError, match=message):
        SolverRequest(**values)


def test_work_record_rejects_negative_counters():
    with pytest.raises(ValueError, match="edge_operations"):
        WorkRecord(-1.0, 0, 0, 0.0, "fixture operations")
