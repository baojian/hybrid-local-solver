# Handoff: coordination-and-offline-data

- Agent family: codex
- Role: controller
- Branch: `agent/codex/coordination-and-offline-data`
- Base commit: `f04938ee68f0f74f333ce8b7386f6834c774d083`
- Assignment state: ready_for_review
- Write scope: the paths recorded in `../active_assignments.toml`
- Permitted shared files: the paths recorded in `../active_assignments.toml`

## Outcome

- Requested result: implement the nine repository-organization changes while
  keeping the project scope concise and separating agent-family work.
- Implemented result: added the canonical scope and context manifests,
  explicit data preparation, local-only graph loading, provider contracts and
  directories, branch/worktree assignments, ownership checks, review routing,
  CI enforcement, and structured implementation provenance.
- Deliberately unchanged: mathematical definitions, solver recurrences,
  reported experiment records, source-paper files, archived manuscripts,
  immutable round records, and the Claude-owned source package.

## Evidence

- Tests added or changed: graph loading, data acquisition, solver contract,
  coordination boundaries, provider entry points, and sweep CLI coverage.
- Commands run: `make agent-audit`, `make test`, `make lint`,
  `make note-audit`, `make research-audit-fast`, and the focused
  `frontier_adaptive_ladder` LaTeX build.
- Results: 210 tests passed; lint and formatting passed; 18-note registry
  passed; seven representative proof checks passed; the changed note built to
  a five-page PDF.

## Review notes

- Provider-owned paths changed: Codex experiment drivers and their tests moved
  under matching provider directories; solver implementation behavior did not
  change.
- Shared paths changed: repository policy, graph/data interfaces,
  coordination tools, CI, documentation, neutral contracts, and provenance
  records.
- Open decision: enable the documented default-branch review rule in repository
  hosting settings if it is not already active.
