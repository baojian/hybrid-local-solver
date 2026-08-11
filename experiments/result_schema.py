"""Validation and durable JSON writing for experiment result bundles.

The schema records the name of an accuracy parameter and the complete stopping
rule as provenance.  It deliberately does not interpret ``epsilon`` or define
a repository-wide residual convention.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

__all__ = ["make_result_bundle", "validate_result_bundle", "write_result_bundle"]

SCHEMA_VERSION = 1
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RESULT_STATUSES = frozenset(
    {
        "completed",
        "completed_without_target_certificate",
        "passed",
        "skipped_after_operation_budget",
        "unstable",
    }
)

_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema_version",
        "experiment",
        "created_at_utc",
        "code_version",
        "repository_dirty",
        "argv",
        "config",
        "records",
    }
)
_RECORD_FIELDS = frozenset(
    {
        "graph",
        "alpha",
        "epsilon",
        "epsilon_name",
        "random_seed",
        "stopping_rule",
        "solver",
        "solver_parameters",
        "source",
        "status",
        "work",
        "metrics",
        "code_version",
        "repository_dirty",
    }
)
_RECORD_STRING_FIELDS = (
    "graph",
    "epsilon_name",
    "stopping_rule",
    "solver",
    "status",
    "code_version",
)


def make_result_bundle(
    *,
    experiment: str,
    config: Mapping[str, Any],
    records: Iterable[Mapping[str, Any]],
    argv: Sequence[str] | None = None,
    code_version: str | None = None,
    created_at_utc: str | None = None,
    repository_dirty: bool | None = None,
) -> dict[str, Any]:
    """Build and validate a versioned experiment-result bundle.

    Missing record-level commit and dirty-worktree values are filled from the
    resolved bundle provenance.  Explicit record values are retained so that
    validation can detect a mismatch instead of silently rewriting it.
    """
    detected_version, detected_dirty = (
        _git_provenance()
        if code_version is None or repository_dirty is None
        else ("unknown", False)
    )
    resolved_version = detected_version if code_version is None else code_version
    resolved_dirty = detected_dirty if repository_dirty is None else repository_dirty
    resolved_timestamp = _utc_timestamp() if created_at_utc is None else created_at_utc
    resolved_argv = list(sys.argv if argv is None else argv)

    copied_records: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise ValueError(f"records[{index}] must be a mapping")
        copied_record = dict(record)
        copied_record.setdefault("code_version", resolved_version)
        copied_record.setdefault("repository_dirty", resolved_dirty)
        copied_records.append(copied_record)

    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "experiment": experiment,
        "created_at_utc": resolved_timestamp,
        "code_version": resolved_version,
        "repository_dirty": resolved_dirty,
        "argv": resolved_argv,
        "config": dict(config) if isinstance(config, Mapping) else config,
        "records": copied_records,
    }
    validate_result_bundle(payload)
    return payload


def validate_result_bundle(payload: object) -> None:
    """Raise ``ValueError`` unless ``payload`` satisfies schema version 1."""
    if not isinstance(payload, Mapping):
        raise ValueError("result bundle must be a mapping")

    _require_fields(payload, _TOP_LEVEL_FIELDS, "result bundle")
    if payload["schema_version"] != SCHEMA_VERSION or isinstance(payload["schema_version"], bool):
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")

    _require_nonempty_string(payload["experiment"], "experiment")
    created_at_utc = _require_nonempty_string(payload["created_at_utc"], "created_at_utc")
    _validate_utc_timestamp(created_at_utc)
    bundle_version = _require_nonempty_string(payload["code_version"], "code_version")
    bundle_dirty = payload["repository_dirty"]
    if bundle_dirty is not None and not isinstance(bundle_dirty, bool):
        raise ValueError("repository_dirty must be a boolean or null when unavailable")

    argv = payload["argv"]
    if not isinstance(argv, list):
        raise ValueError("argv must be a list")
    for index, argument in enumerate(argv):
        if not isinstance(argument, str):
            raise ValueError(f"argv[{index}] must be a string")

    if not isinstance(payload["config"], Mapping):
        raise ValueError("config must be a mapping")

    records = payload["records"]
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    if not records:
        raise ValueError("records must contain at least one result")
    for index, record in enumerate(records):
        _validate_record(record, index, bundle_version, bundle_dirty)

    try:
        json.dumps(payload, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError(f"result bundle must be JSON-serializable: {error}") from error


def write_result_bundle(path: str | os.PathLike[str], payload: object) -> None:
    """Validate and atomically replace ``path`` with formatted JSON."""
    validate_result_bundle(payload)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, allow_nan=False) + "\n"

    descriptor, temporary_name = tempfile.mkstemp(
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".tmp",
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, destination)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def _validate_record(
    record: object,
    index: int,
    bundle_version: str,
    bundle_dirty: bool | None,
) -> None:
    location = f"records[{index}]"
    if not isinstance(record, Mapping):
        raise ValueError(f"{location} must be a mapping")
    _require_fields(record, _RECORD_FIELDS, location)

    for field in _RECORD_STRING_FIELDS:
        _require_nonempty_string(record[field], f"{location}.{field}")
    alpha = _require_finite_number(record["alpha"], f"{location}.alpha")
    if not 0.0 < alpha <= 1.0:
        raise ValueError(f"{location}.alpha must lie in (0, 1]")
    epsilon = _require_finite_number(record["epsilon"], f"{location}.epsilon")
    if epsilon <= 0.0:
        raise ValueError(f"{location}.epsilon must be positive")

    random_seed = record["random_seed"]
    if not isinstance(random_seed, int) or isinstance(random_seed, bool):
        raise ValueError(f"{location}.random_seed must be an integer")

    source = record["source"]
    valid_source = (
        isinstance(source, int)
        and not isinstance(source, bool)
        and source >= 0
        or isinstance(source, str)
        and bool(source.strip())
    )
    if not valid_source:
        raise ValueError(f"{location}.source must be a nonnegative integer or nonempty string")

    if record["status"] not in RESULT_STATUSES:
        expected = ", ".join(sorted(RESULT_STATUSES))
        raise ValueError(f"{location}.status must be one of: {expected}")

    for field in ("solver_parameters", "work", "metrics"):
        if not isinstance(record[field], Mapping):
            raise ValueError(f"{location}.{field} must be a mapping")

    work = record["work"]
    _require_fields(
        work,
        frozenset(
            {
                "edge_operations",
                "local_inner_iterations",
                "outer_acceleration_iterations",
                "unit",
            }
        ),
        f"{location}.work",
    )
    _require_nonempty_string(work["unit"], f"{location}.work.unit")
    edge_operations = work["edge_operations"]
    if edge_operations is not None:
        edge_operations = _require_finite_number(
            edge_operations, f"{location}.work.edge_operations"
        )
        if edge_operations < 0.0:
            raise ValueError(f"{location}.work.edge_operations must be nonnegative")
    for field in ("local_inner_iterations", "outer_acceleration_iterations"):
        value = work[field]
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value < 0
        ):
            raise ValueError(f"{location}.work.{field} must be a nonnegative integer or null")
    if record["status"] in {"completed", "completed_without_target_certificate", "passed"}:
        if edge_operations is None:
            raise ValueError(
                f"{location}.work.edge_operations is required for status={record['status']!r}"
            )
        if not record["metrics"]:
            raise ValueError(
                f"{location}.metrics must not be empty for status={record['status']!r}"
            )
        for field in ("local_inner_iterations", "outer_acceleration_iterations"):
            if work[field] is None:
                raise ValueError(
                    f"{location}.work.{field} is required for status={record['status']!r}"
                )

    if record["code_version"] != bundle_version:
        raise ValueError(f"{location}.code_version must match bundle code_version")
    if record["repository_dirty"] is not None and not isinstance(record["repository_dirty"], bool):
        raise ValueError(f"{location}.repository_dirty must be a boolean or null")
    if record["repository_dirty"] != bundle_dirty:
        raise ValueError(f"{location}.repository_dirty must match bundle repository_dirty")


def _require_fields(payload: Mapping[str, Any], required: frozenset[str], location: str) -> None:
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError(f"{location} is missing required fields: {', '.join(missing)}")


def _require_nonempty_string(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location} must be a nonempty string")
    return value


def _require_finite_number(value: object, location: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{location} must be a finite number")
    if not math.isfinite(value):
        raise ValueError(f"{location} must be a finite number")
    return float(value)


def _validate_utc_timestamp(value: str) -> None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("created_at_utc must be an ISO 8601 timestamp") from error
    if parsed.utcoffset() != timedelta(0):
        raise ValueError("created_at_utc must use UTC")


def _git_provenance() -> tuple[str, bool | None]:
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain=v2", "--branch"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError, subprocess.SubprocessError:
        return "unknown", None

    if status.returncode != 0:
        return "unknown", None

    lines = status.stdout.splitlines()
    oid_prefix = "# branch.oid "
    version = next(
        (line.removeprefix(oid_prefix).strip() for line in lines if line.startswith(oid_prefix)),
        "unknown",
    )
    if not version or version == "(initial)":
        version = "unknown"
    dirty = any(line and not line.startswith("# ") for line in lines)
    return version, dirty


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
