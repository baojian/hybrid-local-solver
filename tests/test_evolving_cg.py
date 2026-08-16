import numpy as np
import pytest

from src.hybrid_solver_codex.evolving_cg import (
    CGTrace,
    EvolvingCGTrace,
    frontier_sparse_cg,
    pagerank_matrix,
    pagerank_rhs,
    restarted_evolving_set_cg,
)
from src.synthetic_graphs import path_graph, star_graph


def test_frontier_sparse_cg_propagates_one_path_hop_per_iteration():
    graph = path_graph(21)
    result = frontier_sparse_cg(
        graph,
        alpha=0.05,
        source=10,
        eps_ppr=1.0e-30,
        max_iterations=4,
    )

    assert isinstance(result.trace, CGTrace)
    assert result.trace.direction_support_size == (1, 3, 5, 7)
    assert result.trace.direction_volume == (2.0, 6.0, 10.0, 14.0)
    np.testing.assert_array_equal(result.explored_vertices, np.arange(7, 14))
    assert result.termination_reason == "iteration_limit"
    assert not result.certified


@pytest.mark.parametrize(
    ("graph", "source"),
    [
        (path_graph(25), 12),
        (star_graph(24), 0),
    ],
)
def test_frontier_sparse_cg_matches_direct_solution_and_certificate(graph, source):
    alpha = 0.05
    eps_ppr = 1.0e-7
    result = frontier_sparse_cg(
        graph,
        alpha=alpha,
        source=source,
        eps_ppr=eps_ppr,
    )
    direct = np.linalg.solve(
        pagerank_matrix(graph, alpha).toarray(),
        pagerank_rhs(graph, alpha, source),
    )

    assert result.certified
    assert result.termination_reason == "verified_residual_certificate"
    assert np.max(np.abs(result.residual) / np.sqrt(graph.degree)) <= alpha * eps_ppr
    assert np.max(np.abs(result.solution - direct) / np.sqrt(graph.degree)) <= eps_ppr


def test_restarted_evolving_cg_uses_nested_batch_expansions_and_certifies():
    graph = path_graph(17)
    alpha = 0.1
    eps_ppr = 1.0e-5
    result = restarted_evolving_set_cg(
        graph,
        alpha=alpha,
        source=8,
        eps_ppr=eps_ppr,
    )

    assert isinstance(result.trace, EvolvingCGTrace)
    assert result.certified
    assert result.trace.active_size[0] == 1
    for current, added, following in zip(
        result.trace.active_size,
        result.trace.added_size,
        result.trace.active_size[1:],
        strict=False,
    ):
        assert following == current + added
    assert result.trace.added_size[-1] == 0
    assert result.outer_restarts == len(result.trace.active_size) - 1
    assert np.max(np.abs(result.residual) / np.sqrt(graph.degree)) <= alpha * eps_ppr


def test_exact_principal_solution_has_only_nonnegative_boundary_residual():
    graph = path_graph(8)
    alpha = 0.1
    source = 0
    matrix = pagerank_matrix(graph, alpha).toarray()
    right_hand_side = pagerank_rhs(graph, alpha, source)
    active = np.array([0, 1, 2])
    solution = np.zeros(graph.n)
    solution[active] = np.linalg.solve(
        matrix[np.ix_(active, active)],
        right_hand_side[active],
    )
    residual = right_hand_side - matrix @ solution

    np.testing.assert_allclose(residual[active], 0.0, atol=1.0e-14)
    assert residual[3] > 0.0
    np.testing.assert_allclose(residual[4:], 0.0, atol=1.0e-14)


def test_masking_a_cg_direction_breaks_q_conjugacy_on_three_node_path():
    matrix = np.array(
        [
            [2.0, -1.0, 0.0],
            [-1.0, 2.0, -1.0],
            [0.0, -1.0, 2.0],
        ]
    )
    first = np.array([1.0, 0.0, 0.0])
    masked_second = np.array([0.0, 1.0, 0.0])
    reorthogonalized_second = np.array([0.5, 1.0, 0.0])

    assert first @ matrix @ masked_second == -1.0
    assert first @ matrix @ reorthogonalized_second == 0.0


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"alpha": 0.0, "eps_ppr": 1.0e-4}, "alpha"),
        ({"alpha": 0.1, "eps_ppr": 0.0}, "eps_ppr"),
    ],
)
def test_frontier_sparse_cg_validates_accuracy_parameters(kwargs, message):
    with pytest.raises(ValueError, match=message):
        frontier_sparse_cg(path_graph(4), source=0, **kwargs)
