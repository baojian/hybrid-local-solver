import numpy as np
import pytest

from src.synthetic_graphs import decoy_hub_graph, path_graph, spider_graph, star_graph


def test_star_path_and_spider_have_expected_degrees_and_edges():
    star = star_graph(4)
    assert (star.n, star.m) == (5, 4)
    np.testing.assert_array_equal(star.degree, [4, 1, 1, 1, 1])

    path = path_graph(5)
    assert (path.n, path.m) == (5, 4)
    np.testing.assert_array_equal(path.degree, [1, 2, 2, 2, 1])

    spider = spider_graph(3, 2)
    assert (spider.n, spider.m) == (7, 6)
    np.testing.assert_array_equal(spider.degree, [3, 2, 1, 2, 1, 2, 1])

    decoy = decoy_hub_graph(4)
    assert (decoy.n, decoy.m) == (7, 6)
    np.testing.assert_array_equal(decoy.degree, [1, 3, 1, 4, 1, 1, 1])


@pytest.mark.parametrize(
    "builder,args,match",
    [
        (star_graph, (0,), "leaf_count"),
        (path_graph, (1,), "node_count"),
        (spider_graph, (0, 2), "arm_count"),
        (spider_graph, (2, 0), "arm_length"),
        (decoy_hub_graph, (0,), "hub_degree"),
    ],
)
def test_synthetic_graphs_reject_isolated_or_empty_constructions(builder, args, match):
    with pytest.raises(ValueError, match=match):
        builder(*args)
