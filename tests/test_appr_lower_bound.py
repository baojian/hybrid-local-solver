import math

import numpy as np
import pytest

from experiments import check_appr_lower_bound
from src.baselines.appr import APPR_ORDERINGS, approximate_pagerank
from src.baselines.sdd_solver import sdd_local_appr
from src.synthetic_graphs import path_graph, spider_graph, star_graph


@pytest.mark.parametrize("ordering", APPR_ORDERINGS)
@pytest.mark.parametrize(
    ("alpha", "eps_appr"),
    [
        (0.1, 1.0 / 32.0),
        (0.5, 1.0 / 64.0),
        (1.0, 1.0 / 16.0),
    ],
)
def test_hard_star_obeys_two_sided_work_bound_for_every_ordering(ordering, alpha, eps_appr):
    leaf_count = math.floor(1.0 / (8.0 * eps_appr))
    result = approximate_pagerank(
        star_graph(leaf_count),
        0,
        alpha=alpha,
        eps_appr=eps_appr,
        ordering=ordering,
        random_seed=17,
    )

    assert np.all(result.residual < eps_appr * star_graph(leaf_count).degree)
    assert result.estimate.sum() + result.residual.sum() == pytest.approx(1.0)
    assert result.work > 3.0 / (128.0 * alpha * eps_appr)
    assert result.work <= 1.0 / (alpha * eps_appr)


@pytest.mark.parametrize(
    "graph,seed",
    [
        (path_graph(9), 4),
        (spider_graph(4, 1), 0),
        (spider_graph(4, 3), 0),
    ],
)
@pytest.mark.parametrize("ordering", APPR_ORDERINGS)
def test_path_and_spider_diagnostics_terminate_with_valid_mass_and_work(graph, seed, ordering):
    alpha = 0.2
    eps_appr = 1.0 / 32.0
    result = approximate_pagerank(
        graph,
        seed,
        alpha=alpha,
        eps_appr=eps_appr,
        ordering=ordering,
        random_seed=17,
    )

    assert np.all(result.residual < eps_appr * graph.degree)
    assert result.estimate.sum() + result.residual.sum() == pytest.approx(1.0)
    assert result.work <= 1.0 / (alpha * eps_appr)


@pytest.mark.parametrize("ordering", APPR_ORDERINGS)
def test_reference_appr_satisfies_pagerank_invariant_and_rppr_bridge(ordering):
    graph = spider_graph(3, 2)
    source = 0
    alpha = 0.2
    eps_appr = 1.0 / 64.0
    result = approximate_pagerank(
        graph,
        source,
        alpha=alpha,
        eps_appr=eps_appr,
        ordering=ordering,
        random_seed=17,
    )

    adjacency = np.zeros((graph.n, graph.n), dtype=np.float64)
    for u in range(graph.n):
        start, stop = graph.indptr[u], graph.indptr[u + 1]
        adjacency[u, graph.indices[start:stop]] = 1.0
    transition = adjacency @ np.diag(1.0 / graph.degree)
    lazy_walk = 0.5 * (np.eye(graph.n) + transition)
    pagerank_system = np.eye(graph.n) - (1.0 - alpha) * lazy_walk
    seed = np.zeros(graph.n)
    seed[source] = 1.0
    exact_pagerank = np.linalg.solve(pagerank_system, alpha * seed)
    residual_pagerank = np.linalg.solve(pagerank_system, alpha * result.residual)

    np.testing.assert_allclose(result.estimate + residual_pagerank, exact_pagerank)
    assert np.linalg.norm(exact_pagerank - result.estimate, ord=1) == pytest.approx(
        result.residual.sum()
    )

    inv_sqrt_degree = np.diag(1.0 / np.sqrt(graph.degree))
    normalized_adjacency = inv_sqrt_degree @ adjacency @ inv_sqrt_degree
    q_matrix = 0.5 * (1.0 + alpha) * np.eye(graph.n) - 0.5 * (1.0 - alpha) * normalized_adjacency
    rppr_solution = np.linalg.solve(q_matrix, alpha * inv_sqrt_degree @ seed)
    np.testing.assert_allclose(np.sqrt(graph.degree) * rppr_solution, exact_pagerank)


def test_reference_fifo_matches_existing_numba_appr_kernel():
    graph = star_graph(4)
    alpha = 0.2
    eps_appr = 1.0 / 32.0
    expected = approximate_pagerank(
        graph,
        0,
        alpha=alpha,
        eps_appr=eps_appr,
        ordering="fifo",
    )
    seed = np.zeros(graph.n)
    seed[0] = 1.0

    estimate, residual, _, work_by_round, _, _ = sdd_local_appr(
        graph.n,
        graph.indptr,
        graph.indices,
        graph.degree,
        seed,
        alpha,
        eps_appr,
    )

    np.testing.assert_allclose(estimate, expected.estimate)
    np.testing.assert_allclose(residual, expected.residual)
    assert sum(work_by_round) == expected.work


def test_numba_kernel_does_not_stop_with_reactivated_seed_missing_from_queue():
    graph = star_graph(100)
    alpha = 0.2
    eps_appr = 0.01
    source = 1
    expected = approximate_pagerank(
        graph,
        source,
        alpha=alpha,
        eps_appr=eps_appr,
        ordering="fifo",
    )
    seed = np.zeros(graph.n)
    seed[source] = 1.0

    estimate, residual, _, work_by_round, _, _ = sdd_local_appr(
        graph.n,
        graph.indptr,
        graph.indices,
        graph.degree,
        seed,
        alpha,
        eps_appr,
    )

    assert np.all(residual < eps_appr * graph.degree)
    np.testing.assert_allclose(estimate, expected.estimate)
    np.testing.assert_allclose(residual, expected.residual)
    assert sum(work_by_round) == expected.work


def test_random_ordering_is_reproducible_when_trace_is_requested():
    graph = spider_graph(5, 3)
    kwargs = {
        "alpha": 0.1,
        "eps_appr": 1.0 / 64.0,
        "ordering": "random",
        "random_seed": 23,
        "record_trace": True,
    }

    first = approximate_pagerank(graph, 0, **kwargs)
    second = approximate_pagerank(graph, 0, **kwargs)

    assert first.push_trace == second.push_trace
    np.testing.assert_allclose(first.estimate, second.estimate)


@pytest.mark.parametrize(
    "kwargs,match",
    [
        ({"alpha": 0.0, "eps_appr": 0.1}, "alpha"),
        ({"alpha": 0.1, "eps_appr": 0.0}, "eps_appr"),
        ({"alpha": 0.1, "eps_appr": 0.1, "ordering": "unknown"}, "ordering"),
    ],
)
def test_rejects_invalid_parameters(kwargs, match):
    with pytest.raises(ValueError, match=match):
        approximate_pagerank(path_graph(3), 1, **kwargs)


@pytest.mark.parametrize("eps_appr", [0.0, -0.1, 0.0625001, 0.1, float("inf")])
def test_lower_bound_checker_rejects_eps_outside_theorem_regime(eps_appr):
    with pytest.raises(ValueError, match=r"proved regime \(0, 1/16\]"):
        check_appr_lower_bound.run_checks(
            [0.25],
            [eps_appr],
            ["fifo"],
            random_seed=17,
            spider_length=3,
            graph_kinds=("star",),
        )


def test_star_only_check_does_not_construct_unrequested_graphs(monkeypatch):
    def unexpected_graph(*args, **kwargs):
        raise AssertionError("unrequested graph construction must remain lazy")

    monkeypatch.setattr(check_appr_lower_bound, "path_graph", unexpected_graph)
    monkeypatch.setattr(check_appr_lower_bound, "spider_graph", unexpected_graph)

    records = check_appr_lower_bound.run_checks(
        [0.25],
        [1.0 / 16.0],
        ["fifo"],
        random_seed=17,
        spider_length=3,
        graph_kinds=("star",),
    )

    assert len(records) == 1
    assert records[0]["graph_kind"] == "star"
