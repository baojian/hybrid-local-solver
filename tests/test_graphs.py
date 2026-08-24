import hashlib
from io import BytesIO

import numpy as np
import pytest
import scipy.sparse as sp

from src import graphs


def _graph_payload():
    adjacency = sp.csr_matrix(
        np.array(
            [
                [0.0, 2.0, 0.0],
                [2.0, 0.0, 3.0],
                [0.0, 3.0, 0.0],
            ],
            dtype=np.float32,
        )
    )
    output = BytesIO()
    sp.save_npz(output, adjacency)
    return output.getvalue()


def _write_catalogued_graph(monkeypatch, data_dir):
    graph_name = "com-dblp"
    file_path = data_dir / graph_name / f"{graph_name}_csr-mat.npz"
    file_path.parent.mkdir(parents=True)
    file_payload = _graph_payload()
    file_path.write_bytes(file_payload)
    monkeypatch.setitem(
        graphs.GRAPH_FILES,
        graph_name,
        (len(file_payload), hashlib.sha256(file_payload).hexdigest()),
    )
    return graph_name, file_path


def test_resolves_explicit_local_path_and_loads_graph(monkeypatch, tmp_path):
    graph_name, file_path = _write_catalogued_graph(monkeypatch, tmp_path)

    assert graphs.graph_path(graph_name, data_dir=tmp_path) == file_path
    graph = graphs.load_graph(graph_name, data_dir=tmp_path)

    assert isinstance(graph, graphs.GraphData)
    assert graph.name == graph_name
    assert graph.n == 3
    assert graph.m == 2
    assert graph.adjacency.nnz == 4
    np.testing.assert_array_equal(graph.degree, [1.0, 2.0, 1.0])
    assert len(graph.indptr) == graph.n + 1
    assert len(graph.indices) == graph.adjacency.nnz


def test_rejects_unknown_graph(tmp_path):
    with pytest.raises(ValueError, match="unknown graph"):
        graphs.graph_path("not-a-graph", data_dir=tmp_path)


def test_missing_graph_has_explicit_acquisition_guidance(tmp_path):
    with pytest.raises(FileNotFoundError, match="explicit data-acquisition command"):
        graphs.graph_path("com-dblp", data_dir=tmp_path)


def test_validates_size_and_optional_digest(monkeypatch, tmp_path):
    graph_name, file_path = _write_catalogued_graph(monkeypatch, tmp_path)

    assert graphs.validate_graph_file(graph_name, file_path, check_sha256=True) == file_path

    monkeypatch.setitem(graphs.GRAPH_FILES, graph_name, (file_path.stat().st_size, "0" * 64))
    with pytest.raises(OSError, match="SHA-256 mismatch"):
        graphs.validate_graph_file(graph_name, file_path, check_sha256=True)


def test_source_sampling_is_reproducible_sorted_and_degree_filtered():
    adjacency = sp.csr_matrix(
        np.array(
            [
                [0, 1, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0],
                [0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 0],
                [0, 0, 0, 1, 0, 1],
                [0, 0, 0, 0, 1, 0],
            ]
        )
    )
    degree = np.asarray(adjacency.sum(1)).ravel()
    graph = graphs.GraphData(name="path", adjacency=adjacency, degree=degree)

    first = graph.sample_sources(count=3, seed=17, min_degree=2)
    second = graph.sample_sources(count=3, seed=17, min_degree=2)

    assert first == second
    assert first == sorted(first)
    assert len(first) == 3
    assert all(graph.degree[node] >= 2 for node in first)
    assert graph.sample_sources(count=10, seed=17, min_degree=2) == [1, 2, 3, 4]

    with pytest.raises(ValueError, match="count must be nonnegative"):
        graph.sample_sources(count=-1, seed=17)
