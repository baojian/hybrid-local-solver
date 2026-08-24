# Handoff: new-agent-problem-brief

- Agent family: codex
- Role: controller
- Branch: `agent/codex/new-agent-problem-brief`
- Base commit: `706459558b2d6540a102f36fdd68980e3caaf7e9`
- Assignment state: ready_for_review
- Write scope:
  - `README.md`
  - `docs/agent-onboarding/`
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/context.toml`
  - `docs/coordination/handoffs/new-agent-problem-brief.md`
- Permitted shared files:
  - `README.md`
  - `docs/agent-onboarding/`
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/context.toml`
  - `docs/coordination/handoffs/new-agent-problem-brief.md`

## Outcome

- Requested result: Create the Markdown files needed to explain the project,
  its mathematical problem, and its unresolved research questions to a new
  agent, then consolidate the complete problem into one independently
  shareable Markdown file with no repository-internal references.
- Implemented result:
  - Added a start-here brief with project mission, vocabulary, candidate
    architecture, authority map, and contribution routes.
  - Consolidated the problem contract into one 16-section standalone file.
    It directly defines the PPR and RPPR operators, semantic output,
    certificates, accuracy namespaces, charged-work model, target complexity,
    candidate architecture, proved components, central locality gate, open
    obligations, scoped negative results, acceptance test, terminology, and
    selected paper citations. It contains no repository paths or internal
    links.
  - Added a dated research-state summary with stable facts, the
    AESP--LOCSOR promotion gate, the Round-027 boundary, six current open
    directions, and explicit non-results.
  - Added a contribution workflow and copyable assignment brief for theory,
    implementation, experiments, and read-only review.
  - Linked the package from the root repository map and included it in the
    default context manifest.
- Deliberately unchanged:
  - No mathematical definition, theorem, solver behavior, experiment,
    manuscript claim, literature metadata, or provider-owned implementation
    changed.
  - The repository-wide residual decision remains open.
  - No research direction or new coordination round was assigned to the
    incoming agent.

## Evidence

- Tests added or changed: none; this is a documentation and routing change.
- Commands run:
  - `.venv/bin/python -m tools.agent_boundaries check`
  - Markdown relative-link check over `docs/agent-onboarding/*.md`
  - Standalone-reference audit for Markdown links, URLs, parent paths, and
    repository paths in `problem-definition.md`
  - `git diff --check`
  - `make agent-audit`
  - `make test`
  - `make lint`
  - `make note-audit`
- Results:
  - All 40 remaining onboarding links resolve.
  - The standalone problem definition contains no Markdown link, URL,
    parent-relative path, or repository path.
  - Coordination records and owned paths are valid.
  - All 210 tests pass. Pytest emitted only temporary-directory cleanup
    warnings.
  - Ruff lint and format checks pass for all 89 checked files.
  - The research-note registry is consistent: 18 notes across 5 tracks.
  - Whitespace and conflict-marker checks are clean.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed:
  - `README.md`
  - `docs/agent-onboarding/`
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/context.toml`
  - `docs/coordination/handoffs/new-agent-problem-brief.md`
- Open decisions or follow-up:
  - The controller must still give the incoming agent a family identity, one
    direction or review task, a disjoint write scope, and a fresh branch.
  - The dated status summary should be reconciled whenever the controller
    broadcast or a listed direction changes materially.
  - The existing `coordination-and-offline-data` review-ready assignment was
    preserved because the current boundary-test fixture loads that record.
