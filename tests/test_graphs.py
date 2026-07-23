import hashlib
from io import BytesIO
from pathlib import Path

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


def test_downloads_pinned_graph_once_and_loads_it(monkeypatch, tmp_path):
    payload = _graph_payload()
    checksum = hashlib.sha256(payload).hexdigest()
    monkeypatch.setitem(graphs.GRAPH_FILES, "com-dblp", (len(payload), checksum))
    calls = []

    def fake_urlopen(request, timeout):
        calls.append((request.full_url, timeout))
        return BytesIO(payload)

    monkeypatch.setattr(graphs, "urlopen", fake_urlopen)

    path = Path(graphs.graph_path("com-dblp", cache_dir=tmp_path))
    assert path.read_bytes() == payload
    assert calls == [(graphs.graph_url("com-dblp"), 60)]
    assert graphs.HF_DATASET_REVISION in calls[0][0]

    graph = graphs.load_graph("com-dblp", cache_dir=tmp_path)
    assert isinstance(graph, graphs.GraphData)
    assert graph.name == "com-dblp"
    assert graph.n == 3
    assert graph.m == 2
    assert graph.adjacency.nnz == 4
    np.testing.assert_array_equal(graph.degree, [1.0, 2.0, 1.0])
    assert len(graph.indptr) == graph.n + 1
    assert len(graph.indices) == graph.adjacency.nnz
    assert len(calls) == 1


def test_rejects_unknown_graph_before_downloading(monkeypatch, tmp_path):
    def unexpected_download(request, timeout):
        raise AssertionError("unknown graphs must not trigger a download")

    monkeypatch.setattr(graphs, "urlopen", unexpected_download)

    with pytest.raises(ValueError, match="unknown graph"):
        graphs.graph_path("not-a-graph", cache_dir=tmp_path)


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


def test_rejects_corrupt_download(monkeypatch, tmp_path):
    payload = b"not the expected graph"
    monkeypatch.setitem(graphs.GRAPH_FILES, "com-dblp", (len(payload), "0" * 64))
    monkeypatch.setattr(graphs, "urlopen", lambda request, timeout: BytesIO(payload))

    with pytest.raises(OSError, match="SHA-256 mismatch"):
        graphs.graph_path("com-dblp", cache_dir=tmp_path)

    destination = tmp_path / graphs.HF_DATASET_SUBDIR / "com-dblp" / "com-dblp_csr-mat.npz"
    assert not destination.exists()
