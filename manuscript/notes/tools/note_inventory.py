"""Audit and report the standalone research-note inventory and handoffs.

The manifest records buildable documents. The taxonomy records research roles,
backend families, dependencies, and next proof targets. Each direction also
has a concise operational status card, while the controller-owned shared layer
holds the common problem, literature, results, and broadcast. This tool keeps
those views synchronized without generating or rewriting their source files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from datetime import date
from pathlib import Path
from typing import Any


TRACKS = {"iterative", "response", "mixed", "synthesis", "models"}
SUPPORT_EVOLUTION = {"fixed-or-nested", "nested", "not-applicable", "trajectory-dependent"}
EVIDENCE = {"conditional", "measured", "model-proposal", "proved-open", "synthesis"}
STATUS_STATES = {"source", "proved-open", "conditional", "measured", "synthesis", "refuted"}
ROUND_STATES = {"active", "reviewed", "redistributed"}
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
REQUIRED_STATUS_HEADINGS = {
    "## Exact question and contract",
    "## Claim ledger",
    "## Central blocker",
    "## Dependencies and reusable outputs",
    "## Resume here",
    "## Verification",
}
REQUIRED_STATUS_CONTRACT_FIELDS = (
    "Question",
    "Model",
    "Accuracy namespace",
    "Access and charged work",
    "Intended result",
)
REQUIRED_STATUS_CLAIM_CLASSES = (
    "Source",
    "Proved here",
    "Conditional",
    "Measured",
    "Refuted",
    "Open",
)
REQUIRED_ROUND_HEADINGS = {
    "## Assignments",
    "## Direction handoffs",
    "## Controller adjudication",
    "## Redistribution messages",
    "## Metadata and shared-state changes",
    "## Validation",
    "## Next round queue",
}
REQUIRED_SHARED_FILES = {
    "AGENTS.md",
    "README.md",
    "WORKFLOW.md",
    "_shared/README.md",
    "_shared/problem_definition/README.md",
    "_shared/related_work/README.md",
    "_shared/results/README.md",
    "_shared/coordination/README.md",
    "_shared/coordination/BROADCAST.md",
    "_shared/coordination/ROUND_TEMPLATE.md",
    "_shared/coordination/STATUS_TEMPLATE.md",
    "_shared/coordination/rounds/README.md",
}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\((?P<target><[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)")
ROUND_FILENAME = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})-round-(?P<number>\d{3})\.md")
NOTE_ID = re.compile(r"[a-z][a-z0-9_]*")
FORMAL_TAXONOMY_DEPENDENCIES = "Formal taxonomy dependencies"


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


def _section_text(text: str, heading: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return ""
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    return "\n".join(lines[start:end])


def _labeled_values(section: str, label: str) -> list[str]:
    escaped = re.escape(label)
    pattern = re.compile(
        rf"^- (?:\*\*{escaped}:\*\*|{escaped}:)[ \t]*(?P<value>.*)$",
        re.MULTILINE,
    )
    return [match.group("value").strip() for match in pattern.finditer(section)]


def _labeled_blocks(section: str, label: str) -> list[str]:
    """Return complete top-level list items carrying ``label``.

    Unlike ``_labeled_values``, this includes wrapped continuation lines.  It
    deliberately stops at the next top-level list item so neighboring
    provenance and source-prerequisite fields cannot become dependency edges.
    """

    markers = (f"- **{label}:**", f"- {label}:")
    lines = section.splitlines()
    blocks: list[str] = []
    for index, line in enumerate(lines):
        marker = next((candidate for candidate in markers if line.startswith(candidate)), None)
        if marker is None:
            continue
        value_lines = [line[len(marker) :].strip()]
        for continuation in lines[index + 1 :]:
            if continuation.startswith("- "):
                break
            value_lines.append(continuation.strip())
        blocks.append(" ".join(value for value in value_lines if value))
    return blocks


def audit_status_taxonomy_dependencies(
    note_id: str, text: str, expected_dependencies: list[str]
) -> list[str]:
    """Require the STATUS formal dependency field to mirror taxonomy exactly."""

    section = _section_text(text, "## Dependencies and reusable outputs")
    declarations = _labeled_blocks(section, FORMAL_TAXONOMY_DEPENDENCIES)
    if not declarations:
        return [f"{note_id}: STATUS.md missing required field {FORMAL_TAXONOMY_DEPENDENCIES!r}"]
    if len(declarations) > 1:
        return [f"{note_id}: STATUS.md repeats required field {FORMAL_TAXONOMY_DEPENDENCIES!r}"]

    declaration = declarations[0]
    if re.fullmatch(r"none\.?", declaration, re.IGNORECASE):
        declared_dependencies: set[str] = set()
    else:
        declared_dependencies = {
            token for token in re.findall(r"`([^`\n]+)`", declaration) if NOTE_ID.fullmatch(token)
        }
        if not declared_dependencies:
            return [
                f"{note_id}: STATUS.md field {FORMAL_TAXONOMY_DEPENDENCIES!r} "
                "must contain code-quoted note ids or 'none'"
            ]

    expected = set(expected_dependencies)
    if declared_dependencies == expected:
        return []

    differences: list[str] = []
    missing = sorted(expected - declared_dependencies)
    extra = sorted(declared_dependencies - expected)
    if missing:
        differences.append(f"missing from STATUS.md: {missing}")
    if extra:
        differences.append(f"extra in STATUS.md: {extra}")
    return [
        f"{note_id}: STATUS.md formal taxonomy dependencies must exactly match "
        f"taxonomy depends_on ({'; '.join(differences)})"
    ]


def audit_status_handoff(note_id: str, text: str) -> list[str]:
    errors: list[str] = []
    lines = text.splitlines()
    expected_title = f"# Direction status: {note_id}"
    if not lines or lines[0] != expected_title:
        errors.append(f"{note_id}: STATUS.md must start with {expected_title!r}")

    reviewed_matches = re.findall(r"^Last reviewed:[ \t]*(.*)$", text, re.MULTILINE)
    if len(reviewed_matches) != 1:
        errors.append(f"{note_id}: STATUS.md must contain exactly one Last reviewed line")
    else:
        try:
            date.fromisoformat(reviewed_matches[0].strip())
        except ValueError:
            errors.append(f"{note_id}: STATUS.md Last reviewed must be an ISO date")

    state_matches = re.findall(r"^State:[ \t]*(.*)$", text, re.MULTILINE)
    if len(state_matches) != 1:
        errors.append(f"{note_id}: STATUS.md must contain exactly one State line")
    elif state_matches[0].strip() not in STATUS_STATES:
        errors.append(
            f"{note_id}: invalid STATUS.md state {state_matches[0].strip()!r}; "
            f"expected one of {sorted(STATUS_STATES)}"
        )

    status_lines = set(lines)
    for heading in sorted(REQUIRED_STATUS_HEADINGS):
        if heading not in status_lines:
            errors.append(f"{note_id}: STATUS.md missing heading {heading!r}")

    required_sections = {
        "## Exact question and contract": REQUIRED_STATUS_CONTRACT_FIELDS,
        "## Claim ledger": REQUIRED_STATUS_CLAIM_CLASSES,
    }
    for heading, labels in required_sections.items():
        if heading not in status_lines:
            continue
        section = _section_text(text, heading)
        for label in labels:
            values = _labeled_values(section, label)
            if not values:
                errors.append(f"{note_id}: STATUS.md missing required field {label!r}")
            elif len(values) > 1:
                errors.append(f"{note_id}: STATUS.md repeats required field {label!r}")
            elif not values[0]:
                errors.append(f"{note_id}: STATUS.md field {label!r} must not be empty")

    if not _section_text(text, "## Central blocker").strip():
        errors.append(f"{note_id}: STATUS.md central blocker must not be empty")
    return errors


def audit_round_record(filename: str, text: str) -> list[str]:
    errors: list[str] = []
    match = ROUND_FILENAME.fullmatch(filename)
    if match is None:
        return [f"invalid research-round filename: {filename}"]

    lines = text.splitlines()
    title_prefix = f"# Research round {match.group('number')}: "
    if not lines or not lines[0].startswith(title_prefix) or lines[0] == title_prefix:
        errors.append(f"{filename}: round title must start with {title_prefix!r}")

    date_matches = re.findall(r"^Date:[ \t]*(.*)$", text, re.MULTILINE)
    if date_matches != [match.group("date")]:
        errors.append(f"{filename}: Date must occur once and match the filename")

    state_matches = re.findall(r"^Round state:[ \t]*(.*)$", text, re.MULTILINE)
    if len(state_matches) != 1:
        errors.append(f"{filename}: must contain exactly one Round state line")
    elif state_matches[0].strip() not in ROUND_STATES:
        errors.append(
            f"{filename}: invalid round state {state_matches[0].strip()!r}; "
            f"expected one of {sorted(ROUND_STATES)}"
        )

    round_lines = set(lines)
    for heading in sorted(REQUIRED_ROUND_HEADINGS):
        if heading not in round_lines:
            errors.append(f"{filename}: missing heading {heading!r}")
        elif not _section_text(text, heading).strip():
            errors.append(f"{filename}: section {heading!r} must not be empty")
    return errors


def broken_local_markdown_links(path: Path) -> list[str]:
    broken: set[str] = set()
    text = path.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK.finditer(text):
        target = match.group("target").strip("<>")
        if target.startswith("#") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
            continue
        local_path = target.split("#", 1)[0]
        if not local_path:
            continue
        resolved = Path(local_path)
        if not resolved.is_absolute():
            resolved = path.parent / resolved
        if not resolved.exists():
            broken.add(target)
    return sorted(broken)


def _readme_note_row_count(text: str, note_id: str) -> int:
    return text.count(f"| `{note_id}` |")


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

    for relative_path in sorted(REQUIRED_SHARED_FILES):
        control_file = notes / relative_path
        if not control_file.is_file():
            errors.append(f"missing shared control file: manuscript/notes/{relative_path}")
            continue
        for target in broken_local_markdown_links(control_file):
            errors.append(
                f"broken local Markdown link in manuscript/notes/{relative_path}: {target}"
            )

    rounds_directory = notes / "_shared" / "coordination" / "rounds"
    rounds_index_file = rounds_directory / "README.md"
    rounds_index = (
        rounds_index_file.read_text(encoding="utf-8") if rounds_index_file.is_file() else ""
    )
    if rounds_directory.is_dir():
        for round_file in sorted(rounds_directory.glob("*.md")):
            if round_file.name == "README.md":
                continue
            round_text = round_file.read_text(encoding="utf-8")
            errors.extend(audit_round_record(round_file.name, round_text))
            for target in broken_local_markdown_links(round_file):
                errors.append(
                    "broken local Markdown link in "
                    f"manuscript/notes/_shared/coordination/rounds/{round_file.name}: {target}"
                )
            index_occurrences = rounds_index.count(f"]({round_file.name})")
            if index_occurrences != 1:
                errors.append(
                    f"{round_file.name}: expected exactly one link in rounds/README.md, "
                    f"found {index_occurrences}"
                )

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
    disk_note_ids = {
        directory.name
        for directory in notes.iterdir()
        if directory.is_dir()
        and not directory.name.startswith("_")
        and (directory / "main.tex").is_file()
    }
    for note_id in sorted(manifest_set - taxonomy_set):
        errors.append(f"manifest note missing from taxonomy: {note_id}")
    for note_id in sorted(taxonomy_set - manifest_set):
        errors.append(f"taxonomy note missing from manifest: {note_id}")
    for note_id in sorted(disk_note_ids - manifest_set):
        errors.append(f"direction directory missing from manifest: {note_id}")
    for note_id in sorted(manifest_set - disk_note_ids):
        errors.append(f"manifest note missing direction directory: {note_id}")

    manifest_by_id = {record["id"]: record for record in manifest if record.get("id")}
    taxonomy_by_id = {record["id"]: record for record in taxonomy if record.get("id")}

    readme_file = notes / "README.md"
    readme = readme_file.read_text(encoding="utf-8") if readme_file.is_file() else ""
    for note_id, record in sorted(manifest_by_id.items()):
        entrypoint = record.get("entrypoint")
        expected_entrypoint = f"{note_id}/main.tex"
        if entrypoint != expected_entrypoint:
            errors.append(
                f"{note_id}: entrypoint must be {expected_entrypoint}, found {entrypoint!r}"
            )
        note_directory = notes / note_id
        for filename in ("main.tex", "README.md", "STATUS.md", "Makefile"):
            if not (note_directory / filename).is_file():
                errors.append(f"{note_id}: missing {filename}")
        status_file = note_directory / "STATUS.md"
        if status_file.is_file():
            status_text = status_file.read_text(encoding="utf-8")
            errors.extend(audit_status_handoff(note_id, status_text))
        makefile = note_directory / "Makefile"
        if makefile.is_file() and "include ../note.mk" not in makefile.read_text(encoding="utf-8"):
            errors.append(f"{note_id}: Makefile must include ../note.mk")
        readme_occurrences = _readme_note_row_count(readme, note_id)
        if readme_occurrences == 0:
            errors.append(f"{note_id}: missing row in manuscript/notes/README.md")
        elif readme_occurrences != 1:
            errors.append(
                f"{note_id}: expected exactly one row in manuscript/notes/README.md, "
                f"found {readme_occurrences}"
            )

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
        status_file = notes / note_id / "STATUS.md"
        if status_file.is_file():
            errors.extend(
                audit_status_taxonomy_dependencies(
                    note_id,
                    status_file.read_text(encoding="utf-8"),
                    dependencies,
                )
            )

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
