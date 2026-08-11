import json

from experiments import smoke_reproduce
from experiments.result_schema import validate_result_bundle


def test_smoke_reproduction_writes_valid_verified_bundle(tmp_path, monkeypatch):
    output_path = tmp_path / "smoke.json"
    monkeypatch.setattr(
        "sys.argv",
        ["smoke_reproduce", "--output", str(output_path)],
    )

    smoke_reproduce.main()

    payload = json.loads(output_path.read_text())
    validate_result_bundle(payload)
    assert payload["experiment"] == "deterministic offline APPR hard-star reproduction smoke"
    assert len(payload["records"]) == 1

    record = payload["records"][0]
    assert record["graph"] == "star-4"
    assert record["epsilon_name"] == "eps_appr"
    assert record["status"] == "passed"
    assert record["work"]["edge_operations"] == 36.0
    assert record["metrics"]["pushes"] == 21
    assert record["metrics"]["star_lower_bound_verified"] is True
    assert record["metrics"]["appr_upper_bound_verified"] is True
    assert record["metrics"]["terminal_residual_verified"] is True
    assert record["metrics"]["mass_conservation_verified"] is True
