"""Validate and run the research-note proof-audit registry."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path


AUDIT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = AUDIT_ROOT.parents[1]
REGISTRY_PATH = AUDIT_ROOT / "registry.toml"
NOTE_REGISTRY_PATH = REPOSITORY_ROOT / "manuscript" / "notes" / "registry.toml"
KINDS = {"exact", "numerical"}


@dataclass(frozen=True)
class Audit:
    """One registered proof audit."""

    id: str
    note: str
    script: str
    provenance_round: int | None
    kind: str
    fast: bool
    full_args: tuple[str, ...]
    provenance_date: str | None = None

    @property
    def module(self) -> str:
        path = Path(self.script).with_suffix("")
        return ".".join(("experiments", "proof_audits", *path.parts))


def _toml(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def load_audits(path: Path = REGISTRY_PATH) -> list[Audit]:
    """Load the proof-audit registry without running any audit."""

    data = _toml(path)
    records = data.get("audit", [])
    if not isinstance(records, list):
        return []
    audits: list[Audit] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        try:
            audits.append(
                Audit(
                    id=str(record["id"]),
                    note=str(record["note"]),
                    script=str(record["script"]),
                    provenance_round=(
                        int(record["provenance_round"]) if "provenance_round" in record else None
                    ),
                    kind=str(record["kind"]),
                    fast=bool(record["fast"]),
                    full_args=tuple(str(value) for value in record["full_args"]),
                    provenance_date=record.get("provenance_date"),
                )
            )
        except KeyError, TypeError, ValueError:
            continue
    return audits


def audit_registry(path: Path = REGISTRY_PATH) -> list[str]:
    """Return structural errors in the proof-audit registry."""

    errors: list[str] = []
    data = _toml(path)
    if data.get("schema_version") != 1:
        errors.append("proof-audit registry must use schema_version = 1")

    raw_records = data.get("audit", [])
    if not isinstance(raw_records, list):
        return [*errors, "proof-audit registry field 'audit' must be an array"]

    required = {
        "id",
        "note",
        "script",
        "kind",
        "fast",
        "full_args",
    }
    note_data = _toml(NOTE_REGISTRY_PATH)
    note_ids = {
        record.get("id") for record in note_data.get("note", []) if isinstance(record, dict)
    }
    ids: list[str] = []
    scripts: list[str] = []
    fast_notes: set[str] = set()

    for index, record in enumerate(raw_records):
        label = f"audit record {index + 1}"
        if not isinstance(record, dict):
            errors.append(f"{label}: expected a TOML table")
            continue
        missing = required - set(record)
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}")
            continue

        audit_id = record["id"]
        note_id = record["note"]
        script = record["script"]
        label = str(audit_id)
        if not isinstance(audit_id, str) or audit_id.count(".") != 1:
            errors.append(f"{label}: id must have form '<note>.<audit>'")
        elif not audit_id.startswith(f"{note_id}."):
            errors.append(f"{label}: id prefix must match note {note_id!r}")
        else:
            ids.append(audit_id)

        if note_id not in note_ids:
            errors.append(f"{label}: unknown note {note_id!r}")
        if record["kind"] not in KINDS:
            errors.append(f"{label}: kind must be one of {sorted(KINDS)}")
        if not isinstance(record["fast"], bool):
            errors.append(f"{label}: fast must be Boolean")
        elif record["fast"]:
            fast_notes.add(str(note_id))
        has_round = "provenance_round" in record
        has_date = "provenance_date" in record
        if has_round == has_date:
            errors.append(f"{label}: specify exactly one provenance_round or provenance_date")
        elif has_round:
            if not isinstance(record["provenance_round"], int) or record["provenance_round"] <= 0:
                errors.append(f"{label}: provenance_round must be a positive integer")
        else:
            try:
                date.fromisoformat(record["provenance_date"])
            except TypeError, ValueError:
                errors.append(f"{label}: provenance_date must be an ISO calendar date")
        if not isinstance(record["full_args"], list) or not all(
            isinstance(value, str) for value in record["full_args"]
        ):
            errors.append(f"{label}: full_args must be a list of strings")

        if not isinstance(script, str):
            errors.append(f"{label}: script must be a string")
            continue
        scripts.append(script)
        relative = Path(script)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"{label}: script must stay under experiments/proof_audits")
            continue
        if not relative.parts or relative.parts[0] != note_id or relative.suffix != ".py":
            errors.append(f"{label}: script path must be '<note>/<name>.py'")
        elif not (AUDIT_ROOT / relative).is_file():
            errors.append(f"{label}: missing script {script}")

    for duplicate in sorted({value for value in ids if ids.count(value) > 1}):
        errors.append(f"duplicate proof-audit id: {duplicate}")
    for duplicate in sorted({value for value in scripts if scripts.count(value) > 1}):
        errors.append(f"duplicate proof-audit script: {duplicate}")

    disk_scripts = {
        str(path.relative_to(AUDIT_ROOT))
        for path in AUDIT_ROOT.glob("*/*.py")
        if path.name != "__init__.py"
    }
    registered_scripts = set(scripts)
    for script in sorted(disk_scripts - registered_scripts):
        errors.append(f"unregistered proof-audit script: {script}")
    for script in sorted(registered_scripts - disk_scripts):
        errors.append(f"registered proof-audit script missing from disk: {script}")

    audited_notes = {str(record.get("note")) for record in raw_records if isinstance(record, dict)}
    for note_id in sorted(audited_notes - fast_notes):
        errors.append(f"{note_id}: no representative fast proof audit")
    return errors


def _selected_audits(
    audits: list[Audit], tier: str, notes: set[str], audit_ids: set[str]
) -> list[Audit]:
    selected = [audit for audit in audits if tier == "full" or audit.fast]
    if notes:
        selected = [audit for audit in selected if audit.note in notes]
    if audit_ids:
        selected = [audit for audit in selected if audit.id in audit_ids]
    return selected


def _print_registry(audits: list[Audit]) -> None:
    print("audit\tkind\tfast\tprovenance\tscript")
    for audit in audits:
        print(
            f"{audit.id}\t{audit.kind}\t{'yes' if audit.fast else 'no'}\t"
            f"{audit.provenance_date or f'{audit.provenance_round:03d}'}\t{audit.script}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=("fast", "full"), default="fast")
    parser.add_argument("--note", action="append", default=[], help="limit to a note id")
    parser.add_argument("--audit", action="append", default=[], help="limit to an audit id")
    parser.add_argument("--check", action="store_true", help="validate the registry and exit")
    parser.add_argument("--list", action="store_true", help="print the registry and exit")
    arguments = parser.parse_args()

    errors = audit_registry()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    audits = load_audits()
    if arguments.check:
        print(f"proof-audit registry is consistent: {len(audits)} audits")
        return 0
    if arguments.list:
        _print_registry(audits)
        return 0

    selected = _selected_audits(audits, arguments.tier, set(arguments.note), set(arguments.audit))
    if not selected:
        print("ERROR: no proof audits match the requested selection", file=sys.stderr)
        return 2

    started = time.monotonic()
    for position, audit in enumerate(selected, start=1):
        extra_args = audit.full_args if arguments.tier == "full" else ()
        command = [sys.executable, "-m", audit.module, *extra_args]
        print(f"[{position}/{len(selected)}] {audit.id}", flush=True)
        result = subprocess.run(command, cwd=REPOSITORY_ROOT, check=False)
        if result.returncode:
            print(f"FAILED: {audit.id} (exit {result.returncode})", file=sys.stderr)
            return result.returncode

    elapsed = time.monotonic() - started
    print(f"proof audits passed: {len(selected)} ({arguments.tier} tier, {elapsed:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
