import hashlib
from io import BytesIO

import pytest

from experiments.data_acquisition import fetch_graphs
from src import graphs


def _pin_test_payload(monkeypatch, payload: bytes) -> None:
    monkeypatch.setitem(
        graphs.GRAPH_FILES,
        "com-dblp",
        (len(payload), hashlib.sha256(payload).hexdigest()),
    )


def test_fetches_revision_pinned_graph_once(monkeypatch, tmp_path):
    payload = b"small graph fixture"
    _pin_test_payload(monkeypatch, payload)
    calls = []

    def open_url(request, timeout):
        calls.append((request.full_url, timeout))
        return BytesIO(payload)

    first = fetch_graphs.fetch_graph("com-dblp", data_dir=tmp_path, opener=open_url)
    second = fetch_graphs.fetch_graph(
        "com-dblp",
        data_dir=tmp_path,
        opener=lambda *_args, **_kwargs: pytest.fail("valid local file should be reused"),
    )

    assert first == second
    assert first.read_bytes() == payload
    assert calls == [(fetch_graphs.graph_url("com-dblp"), 60)]
    assert fetch_graphs.DATASET_REVISION in calls[0][0]


def test_rejects_invalid_download_and_removes_partial_file(monkeypatch, tmp_path):
    payload = b"unexpected bytes"
    monkeypatch.setitem(graphs.GRAPH_FILES, "com-dblp", (len(payload), "0" * 64))

    with pytest.raises(OSError, match="SHA-256 mismatch"):
        fetch_graphs.fetch_graph(
            "com-dblp",
            data_dir=tmp_path,
            opener=lambda _request, timeout: BytesIO(payload),
        )

    graph_dir = tmp_path / "com-dblp"
    assert not (graph_dir / "com-dblp_csr-mat.npz").exists()
    assert list(graph_dir.glob("*.part")) == []


def test_existing_invalid_file_requires_force(monkeypatch, tmp_path):
    payload = b"expected bytes"
    _pin_test_payload(monkeypatch, payload)
    destination = tmp_path / "com-dblp" / "com-dblp_csr-mat.npz"
    destination.parent.mkdir(parents=True)
    destination.write_bytes(b"wrong")

    with pytest.raises(OSError, match="pass --force"):
        fetch_graphs.fetch_graph("com-dblp", data_dir=tmp_path)


def test_cli_requires_explicit_destination_and_selection():
    with pytest.raises(SystemExit):
        fetch_graphs.main([])
