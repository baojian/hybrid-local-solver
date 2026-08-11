import json
import subprocess
from copy import deepcopy

import pytest

from experiments import result_schema


def _record(**overrides):
    record = {
        "graph": "tiny-path",
        "alpha": 0.15,
        "epsilon": 1.0e-4,
        "epsilon_name": "eps_appr",
        "random_seed": 17,
        "stopping_rule": "active while r[u] >= eps_appr * d[u]",
        "solver": "appr",
        "solver_parameters": {"ordering": "fifo"},
        "source": 0,
        "status": "completed",
        "work": {
            "edge_operations": 12,
            "local_inner_iterations": 4,
            "outer_acceleration_iterations": 0,
            "unit": "degree-weighted adjacency-list entries scanned",
        },
        "metrics": {"residual_mass": 0.001},
    }
    record.update(overrides)
    return record


def _bundle(**overrides):
    bundle = result_schema.make_result_bundle(
        experiment="schema test",
        config={"purpose": "unit-test"},
        records=[_record()],
        argv=["python", "-m", "experiments.smoke_reproduce"],
        code_version="abc123",
        created_at_utc="2026-08-12T01:02:03Z",
        repository_dirty=True,
    )
    bundle.update(overrides)
    return bundle


def test_make_result_bundle_stamps_complete_provenance_without_mutating_record():
    record = _record()

    bundle = result_schema.make_result_bundle(
        experiment="schema test",
        config={"purpose": "unit-test"},
        records=[record],
        argv=["experiment", "--tiny"],
        code_version="abc123",
        created_at_utc="2026-08-12T01:02:03Z",
        repository_dirty=True,
    )

    assert bundle == {
        "schema_version": 1,
        "experiment": "schema test",
        "created_at_utc": "2026-08-12T01:02:03Z",
        "code_version": "abc123",
        "repository_dirty": True,
        "argv": ["experiment", "--tiny"],
        "config": {"purpose": "unit-test"},
        "records": [
            {
                **record,
                "code_version": "abc123",
                "repository_dirty": True,
            }
        ],
    }
    assert "code_version" not in record
    assert "repository_dirty" not in record


def test_make_result_bundle_uses_safe_git_fallback(monkeypatch):
    def unavailable(*args, **kwargs):
        raise OSError("git unavailable")

    monkeypatch.setattr(result_schema.subprocess, "run", unavailable)

    bundle = result_schema.make_result_bundle(
        experiment="schema test",
        config={},
        records=[_record()],
        argv=["experiment"],
        created_at_utc="2026-08-12T01:02:03Z",
    )

    assert bundle["code_version"] == "unknown"
    assert bundle["repository_dirty"] is None
    assert bundle["records"][0]["code_version"] == "unknown"
    assert bundle["records"][0]["repository_dirty"] is None


def test_make_result_bundle_reads_commit_and_dirty_state_from_one_git_snapshot(monkeypatch):
    calls = []

    def git_status(*args, **kwargs):
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(
            args[0],
            0,
            stdout="# branch.oid abc123\n# branch.head main\n1 .M N... file.py\n",
            stderr="",
        )

    monkeypatch.setattr(result_schema.subprocess, "run", git_status)

    bundle = result_schema.make_result_bundle(
        experiment="schema test",
        config={},
        records=[_record()],
        argv=["experiment"],
        created_at_utc="2026-08-12T01:02:03Z",
    )

    assert len(calls) == 1
    assert bundle["code_version"] == "abc123"
    assert bundle["repository_dirty"] is True


def test_validate_accepts_explicit_unknown_dirty_state():
    bundle = _bundle(repository_dirty=None)
    bundle["records"][0]["repository_dirty"] = None

    result_schema.validate_result_bundle(bundle)


@pytest.mark.parametrize("missing", sorted(result_schema._TOP_LEVEL_FIELDS))
def test_validate_rejects_missing_top_level_fields(missing):
    bundle = _bundle()
    del bundle[missing]

    with pytest.raises(ValueError, match="missing required fields"):
        result_schema.validate_result_bundle(bundle)


@pytest.mark.parametrize("missing", sorted(result_schema._RECORD_FIELDS))
def test_validate_rejects_missing_record_fields(missing):
    bundle = _bundle()
    del bundle["records"][0][missing]

    with pytest.raises(ValueError, match="missing required fields"):
        result_schema.validate_result_bundle(bundle)


@pytest.mark.parametrize("field", ["alpha", "epsilon"])
@pytest.mark.parametrize("value", [True, "0.1", float("nan"), float("inf"), float("-inf")])
def test_validate_rejects_non_numeric_or_nonfinite_accuracy_values(field, value):
    bundle = _bundle()
    bundle["records"][0][field] = value

    with pytest.raises(ValueError, match=rf"{field} must be a finite number"):
        result_schema.validate_result_bundle(bundle)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("alpha", 0.0, "must lie in"),
        ("alpha", 1.01, "must lie in"),
        ("epsilon", 0.0, "must be positive"),
        ("epsilon", -1.0e-4, "must be positive"),
    ],
)
def test_validate_rejects_out_of_domain_accuracy_values(field, value, message):
    bundle = _bundle()
    bundle["records"][0][field] = value

    with pytest.raises(ValueError, match=message):
        result_schema.validate_result_bundle(bundle)


@pytest.mark.parametrize("source", [-1, True, "", [], {}])
def test_validate_rejects_invalid_sources(source):
    bundle = _bundle()
    bundle["records"][0]["source"] = source

    with pytest.raises(ValueError, match="source must be"):
        result_schema.validate_result_bundle(bundle)


def test_validate_rejects_empty_record_list():
    bundle = _bundle(records=[])

    with pytest.raises(ValueError, match="at least one result"):
        result_schema.validate_result_bundle(bundle)


def test_validate_rejects_unknown_status():
    bundle = _bundle()
    bundle["records"][0]["status"] = "maybe"

    with pytest.raises(ValueError, match="status must be one of"):
        result_schema.validate_result_bundle(bundle)


@pytest.mark.parametrize("edge_operations", [-1, float("inf"), "twelve"])
def test_validate_rejects_invalid_edge_work(edge_operations):
    bundle = _bundle()
    bundle["records"][0]["work"]["edge_operations"] = edge_operations

    with pytest.raises(ValueError, match="edge_operations"):
        result_schema.validate_result_bundle(bundle)


def test_validate_requires_work_and_metrics_for_completed_records():
    missing_work = _bundle()
    missing_work["records"][0]["work"]["edge_operations"] = None
    with pytest.raises(ValueError, match="edge_operations is required"):
        result_schema.validate_result_bundle(missing_work)

    missing_metrics = _bundle()
    missing_metrics["records"][0]["metrics"] = {}
    with pytest.raises(ValueError, match="metrics must not be empty"):
        result_schema.validate_result_bundle(missing_metrics)


@pytest.mark.parametrize(
    "created_at_utc",
    ["not-a-date", "2026-08-12T01:02:03", "2026-08-12T01:02:03+08:00"],
)
def test_validate_rejects_invalid_or_non_utc_timestamp(created_at_utc):
    bundle = _bundle(created_at_utc=created_at_utc)

    with pytest.raises(ValueError, match="created_at_utc"):
        result_schema.validate_result_bundle(bundle)


@pytest.mark.parametrize(
    ("target", "field"),
    [
        ("bundle", "experiment"),
        ("bundle", "created_at_utc"),
        ("bundle", "code_version"),
        ("record", "graph"),
        ("record", "epsilon_name"),
        ("record", "stopping_rule"),
        ("record", "solver"),
        ("record", "status"),
    ],
)
def test_validate_rejects_empty_required_strings(target, field):
    bundle = _bundle()
    location = bundle if target == "bundle" else bundle["records"][0]
    location[field] = "   "

    with pytest.raises(ValueError, match="must be a nonempty string"):
        result_schema.validate_result_bundle(bundle)


def test_validate_rejects_record_provenance_mismatches():
    version_mismatch = _bundle()
    version_mismatch["records"][0]["code_version"] = "different"
    with pytest.raises(ValueError, match="must match bundle code_version"):
        result_schema.validate_result_bundle(version_mismatch)

    dirty_mismatch = _bundle()
    dirty_mismatch["records"][0]["repository_dirty"] = False
    with pytest.raises(ValueError, match="must match bundle repository_dirty"):
        result_schema.validate_result_bundle(dirty_mismatch)


def test_validate_rejects_nested_non_json_values():
    bundle = _bundle()
    bundle["records"][0]["metrics"]["bad"] = {1, 2}

    with pytest.raises(ValueError, match="must be JSON-serializable"):
        result_schema.validate_result_bundle(bundle)


def test_write_result_bundle_creates_parents_and_round_trips_json(tmp_path):
    bundle = _bundle()
    destination = tmp_path / "nested" / "results.json"

    result_schema.write_result_bundle(destination, bundle)

    assert json.loads(destination.read_text()) == bundle
    assert destination.read_text().endswith("\n")
    assert list(destination.parent.glob(f".{destination.name}.*.tmp")) == []


def test_invalid_bundle_does_not_replace_existing_file(tmp_path):
    destination = tmp_path / "results.json"
    destination.write_text("existing\n")
    invalid = deepcopy(_bundle())
    invalid["records"][0]["code_version"] = "different"

    with pytest.raises(ValueError, match="must match bundle code_version"):
        result_schema.write_result_bundle(destination, invalid)

    assert destination.read_text() == "existing\n"
