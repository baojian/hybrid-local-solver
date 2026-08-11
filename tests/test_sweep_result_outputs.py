import json

import numpy as np

from experiments import run_eps_sweep, run_omega_sweep
from experiments.result_schema import validate_result_bundle
from src.synthetic_graphs import star_graph


def test_epsilon_sweep_persists_provisional_certificate_and_work(tmp_path, monkeypatch):
    graph = star_graph(4)
    output_path = tmp_path / "eps.json"

    monkeypatch.setattr(run_eps_sweep, "load_graph", lambda _name: graph)
    monkeypatch.setattr(run_eps_sweep, "sdd_get_opt", lambda *args: np.zeros(graph.n))

    def fake_run_one(*args):
        result = (
            np.zeros(graph.n),
            np.zeros(graph.n),
            [0.125],
            [4.0, 2.0],
            0.01,
            0.0,
        )
        return result, result[0]

    monkeypatch.setattr(run_eps_sweep, "run_one", fake_run_one)
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_eps_sweep",
            "--dataset",
            "tiny-star",
            "--alpha",
            "0.25",
            "--num-sources",
            "1",
            "--algos",
            "gd",
            "--mults",
            "1",
            "--output",
            str(output_path),
        ],
    )

    run_eps_sweep.main()

    payload = json.loads(output_path.read_text())
    validate_result_bundle(payload)
    record = payload["records"][0]
    assert record["solver"] == "gd"
    assert record["epsilon_name"] == "eps_gradient_residual"
    assert "eps * alpha * d[v]" in record["stopping_rule"]
    assert record["metrics"]["target_certificate_achieved"] is True
    assert record["work"]["edge_operations"] == 6.0
    assert record["work"]["local_inner_iterations"] == 2
    assert record["work"]["outer_acceleration_iterations"] == 0
    assert record["metrics"]["comparison_status"].startswith("exploratory")


def test_omega_sweep_persists_each_source_run(tmp_path, monkeypatch):
    graph = star_graph(4)
    output_path = tmp_path / "omega.json"

    monkeypatch.setattr(run_omega_sweep, "load_graph", lambda _name: graph)
    monkeypatch.setattr(run_omega_sweep, "sdd_get_opt", lambda *args: np.zeros(graph.n))

    def fake_local_sor(*args):
        return (
            np.zeros(graph.n),
            np.zeros(graph.n),
            [0.25],
            [3.0, 2.0],
            0.02,
            0.0,
        )

    monkeypatch.setattr(run_omega_sweep, "sdd_local_sor", fake_local_sor)
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_omega_sweep",
            "--dataset",
            "tiny-star",
            "--alpha",
            "0.25",
            "--num-sources",
            "1",
            "--mults",
            "1",
            "--omega-lo",
            "1.0",
            "--omega-hi",
            "1.0",
            "--omega-step",
            "1.0",
            "--output",
            str(output_path),
        ],
    )

    run_omega_sweep.main()

    payload = json.loads(output_path.read_text())
    validate_result_bundle(payload)
    assert len(payload["records"]) == 1
    record = payload["records"][0]
    assert record["solver"] == "sor"
    assert record["solver_parameters"]["omega"] == 1.0
    assert record["epsilon_name"] == "eps_gradient_residual"
    assert "abs(r[v])" in record["stopping_rule"]
    assert record["metrics"]["target_certificate_achieved"] is True
    assert record["work"]["edge_operations"] == 5.0
    assert record["status"] == "completed"


def test_sor_queue_empty_does_not_imply_target_residual_certificate():
    graph = star_graph(30)
    alpha = 0.1
    eps = 0.01
    source = 0
    b = np.zeros(graph.n)
    b[source] = 2.0 * alpha / ((1.0 + alpha) * np.sqrt(graph.degree[source]))

    result = run_omega_sweep.sdd_local_sor(
        graph.n,
        graph.indptr,
        graph.indices,
        graph.degree,
        b,
        alpha,
        eps,
        1.95,
        np.zeros(graph.n),
    )
    achieved, max_normalized_residual = run_omega_sweep._certificate_metrics(
        np.asarray(result[1]),
        graph.degree,
        alpha=alpha,
        eps=eps,
    )

    assert achieved is False
    assert max_normalized_residual > 1.0
