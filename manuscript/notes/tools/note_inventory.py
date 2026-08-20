"""Audit and report the standalone research-note inventory.

The manifest records buildable documents. The taxonomy records research roles,
backend families, dependencies, and next proof targets. This tool keeps those
two views synchronized without generating or rewriting either source file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


TRACKS = {"iterative", "response", "mixed", "synthesis", "models"}
SUPPORT_EVOLUTION = {"fixed-or-nested", "nested", "not-applicable", "trajectory-dependent"}
EVIDENCE = {"conditional", "measured", "model-proposal", "proved-open", "synthesis"}
REQUIRED_TAXONOMY_FIELDS = {
    "id",
    "track",
    "primitive",
    "support_evolution",
    "evidence",
    "role",
    "next_target",
    "depends_on",
}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def load_inventory(root: Path | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = root or repository_root()
    notes = root / "manuscript" / "notes"
    manifest = _load_toml(notes / "manifest.toml")
    taxonomy = _load_toml(notes / "taxonomy.toml")
    return manifest.get("note", []), taxonomy.get("entry", [])


def _duplicate_values(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def _makefile_note_ids(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"^NOTES\s*:=\s*\\\n(?P<body>.*?)(?:\n\n|\n\.PHONY:)", text, re.MULTILINE | re.DOTALL
    )
    if match is None:
        return set()
    ids: set[str] = set()
    for line in match.group("body").splitlines():
        token = line.strip().removesuffix("\\").strip()
        if token:
            ids.add(token)
    return ids


def _dependency_cycles(entries: dict[str, dict[str, Any]]) -> list[list[str]]:
    state: dict[str, int] = {}
    stack: list[str] = []
    cycles: list[list[str]] = []

    def visit(note_id: str) -> None:
        marker = state.get(note_id, 0)
        if marker == 2:
            return
        if marker == 1:
            start = stack.index(note_id)
            cycles.append([*stack[start:], note_id])
            return
        state[note_id] = 1
        stack.append(note_id)
        for dependency in entries[note_id].get("depends_on", []):
            if dependency in entries:
                visit(dependency)
        stack.pop()
        state[note_id] = 2

    for note_id in sorted(entries):
        visit(note_id)
    return cycles


def audit_inventory(root: Path | None = None) -> list[str]:
    root = root or repository_root()
    notes = root / "manuscript" / "notes"
    errors: list[str] = []

    manifest_data = _load_toml(notes / "manifest.toml")
    taxonomy_data = _load_toml(notes / "taxonomy.toml")
    if manifest_data.get("schema_version") != 1:
        errors.append("manifest.toml must use schema_version = 1")
    if taxonomy_data.get("schema_version") != 1:
        errors.append("taxonomy.toml must use schema_version = 1")

    manifest = manifest_data.get("note", [])
    taxonomy = taxonomy_data.get("entry", [])
    manifest_ids = [record.get("id", "") for record in manifest]
    taxonomy_ids = [record.get("id", "") for record in taxonomy]

    for duplicate in sorted(_duplicate_values(manifest_ids)):
        errors.append(f"duplicate manifest id: {duplicate}")
    for duplicate in sorted(_duplicate_values(taxonomy_ids)):
        errors.append(f"duplicate taxonomy id: {duplicate}")

    manifest_set = set(manifest_ids)
    taxonomy_set = set(taxonomy_ids)
    for note_id in sorted(manifest_set - taxonomy_set):
        errors.append(f"manifest note missing from taxonomy: {note_id}")
    for note_id in sorted(taxonomy_set - manifest_set):
        errors.append(f"taxonomy note missing from manifest: {note_id}")

    manifest_by_id = {record["id"]: record for record in manifest if record.get("id")}
    taxonomy_by_id = {record["id"]: record for record in taxonomy if record.get("id")}

    readme = (notes / "README.md").read_text(encoding="utf-8")
    for note_id, record in sorted(manifest_by_id.items()):
        entrypoint = record.get("entrypoint")
        expected_entrypoint = f"{note_id}/main.tex"
        if entrypoint != expected_entrypoint:
            errors.append(
                f"{note_id}: entrypoint must be {expected_entrypoint}, found {entrypoint!r}"
            )
        note_directory = notes / note_id
        for filename in ("main.tex", "README.md", "Makefile"):
            if not (note_directory / filename).is_file():
                errors.append(f"{note_id}: missing {filename}")
        makefile = note_directory / "Makefile"
        if makefile.is_file() and "include ../note.mk" not in makefile.read_text(encoding="utf-8"):
            errors.append(f"{note_id}: Makefile must include ../note.mk")
        if f"| `{note_id}` |" not in readme:
            errors.append(f"{note_id}: missing row in manuscript/notes/README.md")

    for note_id, record in sorted(taxonomy_by_id.items()):
        missing = REQUIRED_TAXONOMY_FIELDS - set(record)
        if missing:
            errors.append(f"{note_id}: missing taxonomy fields {sorted(missing)}")
        if record.get("track") not in TRACKS:
            errors.append(f"{note_id}: invalid track {record.get('track')!r}")
        if record.get("support_evolution") not in SUPPORT_EVOLUTION:
            errors.append(
                f"{note_id}: invalid support_evolution {record.get('support_evolution')!r}"
            )
        if record.get("evidence") not in EVIDENCE:
            errors.append(f"{note_id}: invalid evidence {record.get('evidence')!r}")
        dependencies = record.get("depends_on", [])
        if not isinstance(dependencies, list) or not all(
            isinstance(dependency, str) for dependency in dependencies
        ):
            errors.append(f"{note_id}: depends_on must be a list of note ids")
            continue
        if note_id in dependencies:
            errors.append(f"{note_id}: a note cannot depend on itself")
        for dependency in dependencies:
            if dependency not in taxonomy_by_id:
                errors.append(f"{note_id}: unknown dependency {dependency}")

    for cycle in _dependency_cycles(taxonomy_by_id):
        errors.append(f"taxonomy dependency cycle: {' -> '.join(cycle)}")

    makefile_ids = _makefile_note_ids(notes / "Makefile")
    for note_id in sorted(manifest_set - makefile_ids):
        errors.append(f"manifest note missing from manuscript/notes/Makefile: {note_id}")
    for note_id in sorted(makefile_ids - manifest_set):
        errors.append(f"Makefile note missing from manifest: {note_id}")

    return errors


def markdown_report(entries: list[dict[str, Any]]) -> str:
    lines = [
        "| Note | Track | Primitive | Support | Evidence | Next target |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for record in sorted(entries, key=lambda item: (item["track"], item["id"])):
        fields = [
            f"`{record['id']}`",
            record["track"],
            record["primitive"],
            record["support_evolution"],
            record["evidence"],
            record["next_target"],
        ]
        lines.append("| " + " | ".join(field.replace("|", "\\|") for field in fields) + " |")
    return "\n".join(lines)


def markdown_targets(entries: list[dict[str, Any]]) -> str:
    lines = [
        "| Note | Track | Evidence | Next proof or experiment target |",
        "| --- | --- | --- | --- |",
    ]
    for record in sorted(entries, key=lambda item: (item["track"], item["id"])):
        fields = [
            f"`{record['id']}`",
            record["track"],
            record["evidence"],
            record["next_target"],
        ]
        lines.append("| " + " | ".join(field.replace("|", "\\|") for field in fields) + " |")
    return "\n".join(lines)


def mermaid_graph(entries: list[dict[str, Any]]) -> str:
    by_id = {record["id"]: record for record in entries}
    lines = ["flowchart LR"]
    for note_id, record in sorted(by_id.items()):
        node = note_id.replace("-", "_")
        label = f"{note_id} ({record['track']})".replace('"', "'")
        lines.append(f'    {node}["{label}"]')
    for note_id, record in sorted(by_id.items()):
        node = note_id.replace("-", "_")
        for dependency in sorted(record["depends_on"]):
            parent = dependency.replace("-", "_")
            lines.append(f"    {parent} --> {node}")
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="validate manifest, taxonomy, files, and dependencies")

    report = subparsers.add_parser("report", help="print the current taxonomy")
    report.add_argument("--format", choices=("json", "markdown"), default="markdown")

    targets = subparsers.add_parser("targets", help="print the next target for every note")
    targets.add_argument("--format", choices=("json", "markdown"), default="markdown")

    graph = subparsers.add_parser("graph", help="print the note dependency graph")
    graph.add_argument("--format", choices=("json", "mermaid"), default="mermaid")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    manifest, taxonomy = load_inventory()

    if args.command == "check":
        errors = audit_inventory()
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(f"note inventory is consistent: {len(manifest)} notes across {len(TRACKS)} tracks")
        return 0

    if args.command == "report":
        if args.format == "json":
            print(json.dumps(taxonomy, indent=2, sort_keys=True))
        else:
            print(markdown_report(taxonomy))
        return 0

    if args.command == "targets":
        if args.format == "json":
            targets = [
                {
                    "id": record["id"],
                    "track": record["track"],
                    "evidence": record["evidence"],
                    "next_target": record["next_target"],
                }
                for record in taxonomy
            ]
            print(json.dumps(targets, indent=2, sort_keys=True))
        else:
            print(markdown_targets(taxonomy))
        return 0

    if args.command == "graph":
        if args.format == "json":
            graph = {record["id"]: sorted(record["depends_on"]) for record in taxonomy}
            print(json.dumps(graph, indent=2, sort_keys=True))
        else:
            print(mermaid_graph(taxonomy))
        return 0

    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
