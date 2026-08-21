import math

import numpy as np
import pytest

from src.hybrid_solver_codex.evolving_cg import (
    CGTrace,
    EvolvingCGTrace,
    frontier_sparse_cg,
    geometric_envelope_cg,
    pagerank_matrix,
    pagerank_rhs,
    restarted_evolving_set_cg,
)
from src.synthetic_graphs import decoy_hub_graph, path_graph, star_graph


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


def test_geometric_envelope_cg_doubles_volume_and_reduces_path_restarts():
    graph = path_graph(129)
    parameters = {"alpha": 0.02, "source": 64, "eps_ppr": 1.0e-7}
    literal = restarted_evolving_set_cg(graph, **parameters)
    geometric = geometric_envelope_cg(
        graph,
        volume_growth_factor=2.0,
        **parameters,
    )

    assert isinstance(geometric.trace, EvolvingCGTrace)
    assert geometric.certified
    assert geometric.outer_restarts < literal.outer_restarts
    assert geometric.edge_operations < literal.edge_operations
    assert sum(geometric.trace.discovery_edge_operations) > 0.0
    assert max(geometric.trace.objective_value) <= 1.0e-15
    assert sum(geometric.trace.active_volume) <= 3.0 * geometric.trace.active_volume[-1]
    assert geometric.outer_restarts <= 1 + math.ceil(
        math.log2(geometric.trace.active_volume[-1] / geometric.trace.active_volume[0])
    )
    maximum_inner_iterations = max(geometric.trace.inner_iterations)
    assert (
        geometric.edge_operations
        <= (3.0 * maximum_inner_iterations + 10.0) * geometric.trace.active_volume[-1]
    )
    for current, following, target_reached in zip(
        geometric.trace.active_volume,
        geometric.trace.active_volume[1:],
        geometric.trace.growth_target_reached,
        strict=False,
    ):
        if target_reached:
            assert following >= 2.0 * current


def test_geometric_envelope_cg_exhausts_only_the_seed_component():
    from src.synthetic_graphs import graph_from_edges

    graph = graph_from_edges(
        "two-path-components",
        8,
        [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7)],
    )
    result = geometric_envelope_cg(
        graph,
        alpha=0.05,
        source=0,
        eps_ppr=1.0e-9,
        volume_growth_factor=100.0,
    )

    assert isinstance(result.trace, EvolvingCGTrace)
    assert result.certified
    np.testing.assert_array_equal(result.explored_vertices, np.arange(4))
    assert not all(result.trace.growth_target_reached)


def test_geometric_envelope_cg_does_not_scan_an_already_full_graph_for_halo():
    graph = star_graph(16)
    result = geometric_envelope_cg(
        graph,
        alpha=0.05,
        source=0,
        eps_ppr=1.0e-9,
        volume_growth_factor=4.0,
    )

    assert isinstance(result.trace, EvolvingCGTrace)
    assert result.certified
    assert result.trace.discovery_edge_operations == (0.0, 0.0)
    assert result.trace.growth_target_reached == (False, True)


@pytest.mark.parametrize("hub_degree", [16, 64, 256])
def test_nonviolating_decoy_hub_forces_unbounded_geometric_overshoot(hub_degree):
    graph = decoy_hub_graph(hub_degree)
    parameters = {"alpha": 0.01, "source": 0, "eps_ppr": 0.25}
    literal = restarted_evolving_set_cg(graph, **parameters)
    geometric = geometric_envelope_cg(graph, **parameters)

    assert literal.certified
    assert geometric.certified
    np.testing.assert_array_equal(literal.explored_vertices, [0, 1, 2])
    np.testing.assert_array_equal(geometric.explored_vertices, [0, 1, 2, 3])
    assert np.sum(graph.degree[literal.explored_vertices]) == 5.0
    assert np.sum(graph.degree[geometric.explored_vertices]) == hub_degree + 5.0
    assert literal.edge_operations == 33.0
    assert geometric.edge_operations == 4.0 * hub_degree + 37.0
    assert geometric.trace.violating_size == (1, 1, 0)
    assert geometric.trace.added_size == (1, 2, 0)


def test_decoy_hub_boundary_residuals_match_the_closed_form_proof():
    alpha = 0.13
    hub_degree = 64
    graph = decoy_hub_graph(hub_degree)
    matrix = pagerank_matrix(graph, alpha).toarray()
    right_hand_side = pagerank_rhs(graph, alpha, source=0)

    def exact_principal_residual(active_vertices):
        active_vertices = np.asarray(active_vertices)
        solution = np.zeros(graph.n)
        principal = matrix[np.ix_(active_vertices, active_vertices)]
        solution[active_vertices] = np.linalg.solve(principal, right_hand_side[active_vertices])
        return right_hand_side - matrix @ solution

    first_residual = exact_principal_residual([0])
    second_residual = exact_principal_residual([0, 1])
    terminal_residual = exact_principal_residual([0, 1, 2])
    first_ratio = (1.0 - alpha) / (3.0 * (1.0 + alpha))
    leaf_ratio = (1.0 - alpha) ** 2 / (3.0 * (1.0 + alpha) ** 2 - (1.0 - alpha) ** 2)
    terminal_hub_ratio = (1.0 - alpha) ** 2 / (
        hub_degree * (3.0 * (1.0 + alpha) ** 2 - 2.0 * (1.0 - alpha) ** 2)
    )

    np.testing.assert_allclose(first_residual[1] / np.sqrt(3.0) / alpha, first_ratio)
    np.testing.assert_allclose(second_residual[2] / alpha, leaf_ratio)
    np.testing.assert_allclose(
        second_residual[3] / np.sqrt(hub_degree) / alpha,
        leaf_ratio / hub_degree,
    )
    np.testing.assert_allclose(
        terminal_residual[3] / np.sqrt(hub_degree) / alpha,
        terminal_hub_ratio,
    )


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


@pytest.mark.parametrize("growth_factor", [1.0, 0.5, np.inf])
def test_geometric_envelope_cg_validates_growth_factor(growth_factor):
    with pytest.raises(ValueError, match="volume_growth_factor"):
        geometric_envelope_cg(
            path_graph(4),
            alpha=0.1,
            source=0,
            eps_ppr=1.0e-4,
            volume_growth_factor=growth_factor,
        )
