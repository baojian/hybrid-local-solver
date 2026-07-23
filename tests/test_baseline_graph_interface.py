import numpy as np
import scipy.sparse as sp

from src.baselines import sdd_solver
from src.graphs import GraphData


def test_baseline_solver_consumes_graph_data(monkeypatch):
    adjacency = sp.csr_matrix(np.array([[0.0, 1.0], [1.0, 0.0]]))
    graph = GraphData(
        name="test-graph",
        adjacency=adjacency,
        degree=np.array([1.0, 1.0]),
    )
    solution = np.zeros(graph.n)
    solver_result = (
        solution,
        np.zeros(graph.n),
        [0.0],
        [0.0],
        0.0,
        0.0,
    )

    monkeypatch.setattr(sdd_solver, "sdd_get_opt", lambda *args: solution)
    monkeypatch.setattr(sdd_solver, "sdd_local_gd", lambda *args: solver_result)

    result = sdd_solver.single_local_sdd_solver([0.1, 1e-3, 0, graph, "gd"])

    assert result[:5] == (0.1, 1e-3, 0, "gd", "test-graph")
