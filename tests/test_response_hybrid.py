import numpy as np
import pytest

from experiments import explore_response_hybrid
from experiments.result_schema import make_result_bundle
from src.hybrid_solver_codex.evolving_cg import pagerank_matrix, pagerank_rhs
from src.hybrid_solver_codex.response_hybrid import (
    DenseNestedResponse,
    dense_response_frontier_hybrid,
)
from src.synthetic_graphs import graph_from_edges, path_graph


def test_bordered_response_updates_match_direct_principal_inverses():
    graph = path_graph(9)
    matrix = pagerank_matrix(graph, alpha=0.07).toarray()
    response = DenseNestedResponse(matrix)

    for batch in ([4], [3, 5], [2, 6], [1, 7]):
        update = response.expand(batch)
        vertices = response.vertices
        direct_inverse = np.linalg.inv(matrix[np.ix_(vertices, vertices)])

        assert update.anchor_size_after == vertices.size
        assert update.schur_min_eigenvalue > 0.0
        assert update.dense_flop_estimate > 0.0
        np.testing.assert_allclose(response.inverse, direct_inverse, rtol=1.0e-11, atol=1.0e-12)


def test_frontier_schur_cg_matches_direct_principal_solve_and_warm_starts():
    graph = path_graph(7)
    alpha = 0.1
    matrix = pagerank_matrix(graph, alpha).toarray()
    right_hand_side = pagerank_rhs(graph, alpha, source=0)
    response = DenseNestedResponse(matrix)
    response.expand([0, 1])
    frontier = np.array([2, 3])

    first = response.solve_with_frontier(
        right_hand_side,
        frontier,
        graph.degree,
        tolerance=1.0e-13,
    )
    active = np.array([0, 1, 2, 3])
    direct = np.linalg.solve(
        matrix[np.ix_(active, active)],
        right_hand_side[active],
    )

    assert first.converged
    assert first.iterations <= frontier.size
    assert not first.warm_started
    np.testing.assert_allclose(first.solution[active], direct, rtol=1.0e-11, atol=1.0e-12)

    second = response.solve_with_frontier(
        right_hand_side,
        frontier,
        graph.degree,
        tolerance=1.0e-13,
        initial_solution=first.solution,
    )
    assert second.converged
    assert second.warm_started
    assert second.iterations == 0
    np.testing.assert_allclose(second.solution, first.solution, rtol=1.0e-11, atol=1.0e-12)


@pytest.mark.parametrize("rebuild_volume_factor", [1.0, 2.0, np.inf])
def test_response_frontier_endpoints_and_hybrid_certify(rebuild_volume_factor):
    graph = path_graph(33)
    alpha = 0.05
    eps_ppr = 1.0e-9
    result = dense_response_frontier_hybrid(
        graph,
        alpha=alpha,
        source=16,
        eps_ppr=eps_ppr,
        rebuild_volume_factor=rebuild_volume_factor,
        probe_frontier_before_rebuild=False,
    )
    direct = np.linalg.solve(
        pagerank_matrix(graph, alpha).toarray(),
        pagerank_rhs(graph, alpha, source=16),
    )

    assert result.certified
    assert result.termination_reason == "verified_residual_certificate"
    assert len(result.trace.anchor_size) == len(result.trace.frontier_size)
    assert len(result.trace.anchor_size) == len(result.trace.response_rebuilt)
    assert result.work.boundary_coordinate_reads == graph.n * len(result.trace.anchor_size)
    assert result.work.active_materialization_writes >= result.work.final_output_writes
    assert result.work.response_update_dense_flops > 0.0
    np.testing.assert_allclose(result.solution, direct, rtol=1.0e-7, atol=1.0e-9)

    if rebuild_volume_factor == 1.0:
        assert result.work.response_updates > 1
        assert result.work.frontier_cg_iterations == 0
    elif np.isinf(rebuild_volume_factor):
        assert result.work.response_updates == 1
        assert result.work.frontier_cg_iterations > 0
    else:
        assert result.work.response_updates > 1
        assert result.work.frontier_cg_iterations > 0


def test_zero_frontier_budget_stops_before_using_inaccurate_boundary_values():
    graph = path_graph(17)
    result = dense_response_frontier_hybrid(
        graph,
        alpha=0.05,
        source=8,
        eps_ppr=1.0e-9,
        rebuild_volume_factor=np.inf,
        max_frontier_iterations=0,
    )

    assert not result.certified
    assert result.termination_reason == "frontier_iteration_limit"
    assert result.work.response_updates == 1
    assert result.work.frontier_cg_iterations == 0


def test_probe_first_policy_avoids_dense_rebuild_on_easy_heavy_star_batch():
    from src.synthetic_graphs import star_graph

    graph = star_graph(64)
    immediate = dense_response_frontier_hybrid(
        graph,
        alpha=0.05,
        source=0,
        eps_ppr=1.0e-7,
        rebuild_volume_factor=2.0,
        probe_frontier_before_rebuild=False,
    )
    probe_first = dense_response_frontier_hybrid(
        graph,
        alpha=0.05,
        source=0,
        eps_ppr=1.0e-7,
        rebuild_volume_factor=2.0,
        probe_frontier_before_rebuild=True,
    )

    assert immediate.certified and probe_first.certified
    assert immediate.work.response_updates == 2
    assert probe_first.work.response_updates == 1
    assert probe_first.work.frontier_cg_iterations == 1
    assert probe_first.work.response_update_dense_flops < immediate.work.response_update_dense_flops


def test_dense_response_rejects_duplicate_or_overlapping_vertices():
    graph = path_graph(5)
    response = DenseNestedResponse(pagerank_matrix(graph, alpha=0.1).toarray())

    with pytest.raises(ValueError, match="duplicates"):
        response.expand([0, 0])
    response.expand([0])
    with pytest.raises(ValueError, match="disjoint"):
        response.expand([0, 1])


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"rebuild_volume_factor": 0.9}, "rebuild_volume_factor"),
        ({"inner_tolerance_fraction": 1.0}, "inner_tolerance_fraction"),
        ({"max_frontier_iterations": -1}, "max_frontier_iterations"),
        ({"probe_frontier_before_rebuild": 1}, "probe_frontier_before_rebuild"),
    ],
)
def test_response_frontier_hybrid_validates_controller_parameters(kwargs, message):
    with pytest.raises(ValueError, match=message):
        dense_response_frontier_hybrid(
            graph_from_edges("edge", 2, [(0, 1)]),
            alpha=0.1,
            source=0,
            eps_ppr=1.0e-4,
            **kwargs,
        )


def test_response_experiment_emits_schema_valid_endpoint_records(monkeypatch):
    graph = path_graph(9)
    monkeypatch.setattr(
        explore_response_hybrid,
        "synthetic_cases",
        lambda _seed: [(graph, 4, "small test path")],
    )
    config, records = explore_response_hybrid.run_exploration(
        alpha=0.1,
        eps_ppr=1.0e-6,
        random_seed=3,
    )
    payload = make_result_bundle(
        experiment="response hybrid unit test",
        config=config,
        records=records,
        argv=[],
        code_version="test-version",
        created_at_utc="2026-08-20T00:00:00Z",
        repository_dirty=False,
    )

    assert len(payload["records"]) == 3
    assert {record["solver"] for record in payload["records"]} == {
        "dense_response_every_batch",
        "dense_response_frontier_hybrid",
        "dense_anchor_iterative_frontier",
    }
    assert all(record["metrics"]["certified"] for record in payload["records"])
