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


def test_note_inventory_audit_passes() -> None:
    tool = _load_tool()
    assert tool.audit_inventory(REPOSITORY) == []


def test_note_inventory_reports_the_two_organized_research_targets() -> None:
    tool = _load_tool()
    _, taxonomy = tool.load_inventory(REPOSITORY)
    report = tool.markdown_report(taxonomy)
    targets = tool.markdown_targets(taxonomy)
    graph = tool.mermaid_graph(taxonomy)

    assert "`response_preconditioned_hybrid`" in report
    assert "`local_solver_oracle_hierarchy`" in report
    assert "`response_preconditioned_hybrid`" in targets
    assert "`local_solver_oracle_hierarchy`" in targets
    assert "incremental_active_set_sdd --> response_preconditioned_hybrid" in graph
