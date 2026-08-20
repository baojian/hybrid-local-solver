"""Shared synthetic graph constructions used by tests and experiments."""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from src.graphs import GraphData


def graph_from_edges(name: str, node_count: int, edges: list[tuple[int, int]]) -> GraphData:
    """Build a symmetric, unweighted graph from undirected edges."""
    if node_count < 1:
        raise ValueError(f"node_count must be positive, got {node_count}")

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


def star_graph(leaf_count: int) -> GraphData:
    """Return the star with center vertex zero and ``leaf_count`` leaves."""
    if leaf_count < 1:
        raise ValueError(f"leaf_count must be positive, got {leaf_count}")
    return graph_from_edges(
        f"star-{leaf_count}",
        leaf_count + 1,
        [(0, leaf) for leaf in range(1, leaf_count + 1)],
    )


def path_graph(node_count: int) -> GraphData:
    """Return a path whose vertices are numbered consecutively from zero."""
    if node_count < 2:
        raise ValueError(f"node_count must be at least two, got {node_count}")
    return graph_from_edges(
        f"path-{node_count}",
        node_count,
        [(u, u + 1) for u in range(node_count - 1)],
    )


def spider_graph(arm_count: int, arm_length: int) -> GraphData:
    """Return a spider with center zero and equal-length vertex-disjoint arms."""
    if arm_count < 1:
        raise ValueError(f"arm_count must be positive, got {arm_count}")
    if arm_length < 1:
        raise ValueError(f"arm_length must be positive, got {arm_length}")

    edges = []
    for arm in range(arm_count):
        previous = 0
        for depth in range(arm_length):
            node = 1 + arm * arm_length + depth
            edges.append((previous, node))
            previous = node
    return graph_from_edges(
        f"spider-{arm_count}x{arm_length}",
        1 + arm_count * arm_length,
        edges,
    )


def decoy_hub_graph(hub_degree: int) -> GraphData:
    """Return the high-degree halo-overshoot obstruction.

    Vertex zero is the seed, vertex one is a degree-three branch, vertex two
    is its low-degree violating leaf, and vertex three is a decoy hub with
    ``hub_degree - 1`` private leaves.  The construction has ``hub_degree + 3``
    vertices and no isolated vertices.
    """
    if hub_degree < 1:
        raise ValueError(f"hub_degree must be positive, got {hub_degree}")
    edges = [(0, 1), (1, 2), (1, 3)]
    edges.extend((3, leaf) for leaf in range(4, hub_degree + 3))
    return graph_from_edges(
        f"decoy-hub-{hub_degree}",
        hub_degree + 3,
        edges,
    )
