from __future__ import annotations

import importlib.util
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
TOOL_PATH = REPOSITORY / "manuscript" / "notes" / "tools" / "note_inventory.py"


def _load_tool():
    specification = importlib.util.spec_from_file_location("note_inventory", TOOL_PATH)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _valid_status_text(note_id: str = "example") -> str:
    return f"""# Direction status: {note_id}

Last reviewed: 2026-08-21
State: proved-open

## Exact question and contract

- **Question:** Is the target true?
- **Model:** A declared model.
- **Accuracy namespace:** A declared tolerance.
- **Access and charged work:** Every operation is charged.
- **Intended result:** A falsifiable theorem.

## Claim ledger

- **Source:** A cited source.
- **Proved here:** One local lemma.
- **Conditional:** One conditional statement.
- **Measured:** No measurements.
- **Refuted:** No refuted claims.
- **Open:** One open target.

## Central blocker

One missing lemma.

## Dependencies and reusable outputs

- **Formal registry dependencies:** none.
- **Source/shared prerequisites:** `source_only`.
- **Context/provenance:** `provenance_only`.
- **Supplies to:** one output.

## Resume here

Resume at the missing lemma.

## Verification

The focused checks passed.
"""


def _valid_round_text() -> str:
    sections = {
        "## Assignments": "One assignment.",
        "## Direction handoffs": "Pending evidence.",
        "## Controller adjudication": "No promotion yet.",
        "## Redistribution messages": "No verified message yet.",
        "## Metadata and shared-state changes": "No metadata change.",
        "## Validation": "Audit pending.",
        "## Next round queue": "One next target.",
    }
    body = "\n\n".join(f"{heading}\n\n{value}" for heading, value in sections.items())
    return f"# Research round 007: example\n\nDate: 2026-08-21\nRound state: active\n\n{body}\n"


def test_note_inventory_audit_passes() -> None:
    tool = _load_tool()
    assert tool.audit_inventory(REPOSITORY) == []


def test_note_sources_stay_within_reviewable_size_limits() -> None:
    tool = _load_tool()
    for record in tool.load_registry(REPOSITORY):
        note = REPOSITORY / "manuscript" / "notes" / record["id"]
        assert len((note / "main.tex").read_text(encoding="utf-8").splitlines()) <= (
            tool.MAX_ENTRYPOINT_LINES
        )
        for section in (note / "sections" / "body").glob("*.tex"):
            assert len(section.read_text(encoding="utf-8").splitlines()) <= (
                tool.MAX_EXTRACTED_SECTION_LINES
            )


def test_round_named_proof_programs_do_not_live_inside_notes() -> None:
    notes = REPOSITORY / "manuscript" / "notes"
    assert list(notes.glob("*/check_round*.py")) == []


def test_every_note_has_a_complete_status_handoff() -> None:
    tool = _load_tool()
    registry = tool.load_registry(REPOSITORY)

    for record in registry:
        note = REPOSITORY / "manuscript" / "notes" / record["id"]
        status = tool.status_handoff_file(note, record["id"])
        assert status is not None
        text = status.read_text(encoding="utf-8")
        assert (
            tool.audit_status_handoff(
                record["id"],
                text,
                embedded=status.name == "README.md",
            )
            == []
        )


def test_status_handoff_can_be_embedded_in_readme() -> None:
    tool = _load_tool()
    text = "# Example note\n\nOverview.\n\n" + _valid_status_text()

    assert tool.audit_status_handoff("example", text, embedded=True) == []


def test_status_handoff_rejects_empty_fields_and_non_enum_state() -> None:
    tool = _load_tool()
    text = _valid_status_text().replace("State: proved-open", "State: proved-open; refuted")
    text = text.replace("Last reviewed: 2026-08-21", "Last reviewed: 2026-99-99")
    text = text.replace("- **Question:** Is the target true?", "- **Question:**")
    text = text.replace("- **Measured:** No measurements.", "- **Measured:**")

    errors = tool.audit_status_handoff("example", text)

    assert any("invalid STATUS.md state" in error for error in errors)
    assert "example: STATUS.md Last reviewed must be an ISO date" in errors
    assert "example: STATUS.md field 'Question' must not be empty" in errors
    assert "example: STATUS.md field 'Measured' must not be empty" in errors


def test_status_handoff_rejects_an_empty_heading_skeleton() -> None:
    tool = _load_tool()
    skeleton = "\n\n".join(
        [
            "# Direction status: example\n\nState: proved-open",
            *sorted(tool.REQUIRED_STATUS_HEADINGS),
        ]
    )

    errors = tool.audit_status_handoff("example", skeleton)

    assert errors
    assert any("required field 'Question'" in error for error in errors)
    assert "example: STATUS.md central blocker must not be empty" in errors


def test_status_registry_dependencies_match_wrapped_code_quoted_ids() -> None:
    tool = _load_tool()
    text = _valid_status_text().replace(
        "- **Formal registry dependencies:** none.",
        "- **Formal registry dependencies:** `parent_one` and\n  `parent_two`.",
    )

    assert (
        tool.audit_status_registry_dependencies("example", text, ["parent_one", "parent_two"]) == []
    )


def test_status_registry_dependencies_report_missing_and_extra_edges() -> None:
    tool = _load_tool()
    text = _valid_status_text().replace(
        "- **Formal registry dependencies:** none.",
        "- **Formal registry dependencies:** `present_parent` and `extra_parent`.",
    )

    errors = tool.audit_status_registry_dependencies(
        "example", text, ["present_parent", "missing_parent"]
    )

    assert len(errors) == 1
    assert "missing from STATUS.md: ['missing_parent']" in errors[0]
    assert "extra in STATUS.md: ['extra_parent']" in errors[0]


def test_status_registry_dependencies_accept_none() -> None:
    tool = _load_tool()

    assert tool.audit_status_registry_dependencies("example", _valid_status_text(), []) == []


def test_status_registry_dependencies_ignore_provenance_and_prerequisites() -> None:
    tool = _load_tool()
    text = _valid_status_text()

    assert "`source_only`" in text
    assert "`provenance_only`" in text
    assert tool.audit_status_registry_dependencies("example", text, []) == []


def test_status_registry_dependencies_require_exactly_one_formal_field() -> None:
    tool = _load_tool()
    valid = _valid_status_text()
    missing = valid.replace("- **Formal registry dependencies:** none.\n", "")
    repeated = valid.replace(
        "- **Formal registry dependencies:** none.",
        "- **Formal registry dependencies:** none.\n- Formal registry dependencies: none.",
    )

    assert tool.audit_status_registry_dependencies("example", missing, []) == [
        "example: STATUS.md missing required field 'Formal registry dependencies'"
    ]
    assert tool.audit_status_registry_dependencies("example", repeated, []) == [
        "example: STATUS.md repeats required field 'Formal registry dependencies'"
    ]


def test_shared_controller_layer_is_complete() -> None:
    tool = _load_tool()
    notes = REPOSITORY / "manuscript" / "notes"

    assert all((notes / relative_path).is_file() for relative_path in tool.REQUIRED_SHARED_FILES)
    assert {"README.md", "WORKFLOW.md"} <= tool.REQUIRED_SHARED_FILES


def test_controller_link_audit_checks_local_targets_only(tmp_path: Path) -> None:
    tool = _load_tool()
    document = tmp_path / "README.md"
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    document.write_text(
        "[present](target.md) [missing](missing.md) "
        "[section](#local) [remote](https://example.com)\n",
        encoding="utf-8",
    )

    assert tool.broken_local_markdown_links(document) == ["missing.md"]


def test_round_record_contract_and_state_are_enforced() -> None:
    tool = _load_tool()
    valid = _valid_round_text()

    assert tool.audit_round_record("2026-08-21-round-007.md", valid) == []

    invalid = valid.replace("Round state: active", "Round state: done")
    invalid = invalid.replace(
        "## Controller adjudication\n\nNo promotion yet.", "## Controller adjudication"
    )
    errors = tool.audit_round_record("2026-08-21-round-007.md", invalid)
    assert any("invalid round state" in error for error in errors)
    assert any(
        "Controller adjudication" in error and "must not be empty" in error for error in errors
    )


def test_every_round_record_is_valid_and_indexed_once() -> None:
    tool = _load_tool()
    rounds = REPOSITORY / "manuscript" / "notes" / "_shared" / "coordination" / "rounds"
    index = (rounds / "README.md").read_text(encoding="utf-8")

    for round_file in sorted(rounds.glob("*.md")):
        if round_file.name == "README.md":
            continue
        assert (
            tool.audit_round_record(round_file.name, round_file.read_text(encoding="utf-8")) == []
        )
        assert index.count(f"]({round_file.name})") == 1


def test_readme_note_rows_are_counted_exactly() -> None:
    tool = _load_tool()
    readme = (
        "| [`one`](one/) | iterative |\n"
        "| [`two`](two/) | response |\n"
        "| [`one`](one/) | duplicate |\n"
    )

    assert tool._readme_note_row_count(readme, "one") == 2
    assert tool._readme_note_row_count(readme, "two") == 1
    assert tool._readme_note_row_count(readme, "missing") == 0


def test_note_inventory_reports_the_two_organized_research_targets() -> None:
    tool = _load_tool()
    registry = tool.load_registry(REPOSITORY)
    report = tool.markdown_report(registry)
    targets = tool.markdown_targets(registry)
    graph = tool.mermaid_graph(registry)

    assert "`response_preconditioned_hybrid`" in report
    assert "`local_solver_oracle_hierarchy`" in report
    assert "`response_preconditioned_hybrid`" in targets
    assert "`local_solver_oracle_hierarchy`" in targets
    assert "incremental_active_set_sdd --> response_preconditioned_hybrid" in graph
