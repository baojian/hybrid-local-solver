# Handoff: problem-definitions-layout

- Agent family: codex
- Role: direction
- Branch: `agent/codex/problem-definitions-layout`
- Base commit: `5d4e0ffc54b5988fa2ca7aff65eef847a8b16cd0`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/problem-definitions-layout.md`
  - `manuscript/notes/AGENTS.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/WORKFLOW.md`
  - `manuscript/notes/problem_definitions/`
  - `manuscript/notes/tools/note_inventory.py`
  - `tests/test_note_inventory_tool.py`
- Permitted shared files:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/problem-definitions-layout.md`
  - `manuscript/notes/AGENTS.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/WORKFLOW.md`
  - `manuscript/notes/tools/note_inventory.py`
  - `tests/test_note_inventory_tool.py`

## Outcome

- Requested result: reduce `manuscript/notes/problem_definitions/` to
  `README.md`, `Makefile`, and `main.tex` by combining `README.md` and
  `STATUS.md`.
- Implemented result: preserved the full operational status handoff inside
  `README.md`, removed `STATUS.md`, and taught the note inventory to accept
  either a separate status file or an explicitly titled README-embedded
  handoff.
- Deliberately unchanged: every other note retains its separate `STATUS.md`;
  no mathematical content in `main.tex` changed.

## Evidence

- Tests added or changed: extended `tests/test_note_inventory_tool.py` to
  exercise README-embedded status handoffs while retaining coverage for the
  separate-file form.
- Commands run: `make -C manuscript/notes/problem_definitions`,
  `uv run pytest tests/test_note_inventory_tool.py`, `make note-audit`,
  `make agent-audit`, `make test`, and `make lint`.
- Results: the note built as a six-page PDF; the inventory audited 27 notes;
  all 211 tests passed; agent auditing, Ruff checks, and Ruff formatting checks
  passed. Pytest emitted 15 non-failing temporary-directory cleanup warnings.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: note workflow documentation, the inventory validator,
  its focused tests, and the coordination assignment/handoff.
- Open decisions or follow-up: none. The inventory continues to prefer
  `STATUS.md` when both forms are present, so existing notes are unaffected.
