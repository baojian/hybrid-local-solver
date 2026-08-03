import math

import numpy as np
import pytest
import scipy.sparse as sp

from src.baselines.appr import APPR_ORDERINGS, approximate_pagerank
from src.baselines.sdd_solver import sdd_local_appr
from src.graphs import GraphData


def _graph_from_edges(name: str, node_count: int, edges: list[tuple[int, int]]) -> GraphData:
    first = np.fromiter((u for u, _ in edges), dtype=int)
    second = np.fromiter((v for _, v in edges), dtype=int)
    rows = np.concatenate((first, second))
    columns = np.concatenate((second, first))
    adjacency = sp.csr_matrix(
        (np.ones(len(rows)), (rows, columns)),
        shape=(node_count, node_count),
    )
    degree = np.asarray(adjacency.sum(axis=1)).ravel()
    return GraphData(name=name, adjacency=adjacency, degree=degree)


def _star(leaf_count: int) -> GraphData:
    return _graph_from_edges(
        f"star-{leaf_count}",
        leaf_count + 1,
        [(0, leaf) for leaf in range(1, leaf_count + 1)],
    )


def _path(node_count: int) -> GraphData:
    return _graph_from_edges(
        f"path-{node_count}",
        node_count,
        [(u, u + 1) for u in range(node_count - 1)],
    )


def _spider(arm_count: int, arm_length: int) -> GraphData:
    edges = []
    for arm in range(arm_count):
        previous = 0
        for depth in range(arm_length):
            node = 1 + arm * arm_length + depth
            edges.append((previous, node))
            previous = node
    return _graph_from_edges(
        f"spider-{arm_count}x{arm_length}",
        1 + arm_count * arm_length,
        edges,
    )


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
        _star(leaf_count),
        0,
        alpha=alpha,
        eps_appr=eps_appr,
        ordering=ordering,
        random_seed=17,
    )

    assert np.all(result.residual < eps_appr * _star(leaf_count).degree)
    assert result.estimate.sum() + result.residual.sum() == pytest.approx(1.0)
    assert result.work > 3.0 / (128.0 * alpha * eps_appr)
    assert result.work <= 1.0 / (alpha * eps_appr)


@pytest.mark.parametrize(
    "graph,seed",
    [
        (_path(9), 4),
        (_spider(4, 1), 0),
        (_spider(4, 3), 0),
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


def test_reference_fifo_matches_existing_numba_appr_kernel():
    graph = _star(4)
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
    graph = _star(100)
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
    graph = _spider(5, 3)
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
        approximate_pagerank(_path(3), 1, **kwargs)
