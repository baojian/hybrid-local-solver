# Repository coordination policy

This policy separates implementation ownership from shared mathematical work.
The root `AGENTS.md` remains authoritative for research practice; this file
defines the mechanics used when more than one agent family contributes.

## One assignment, one branch, one worktree

Each writing assignment uses a dedicated branch and a dedicated clean
worktree. Agent branches follow `agent/<family>/<task>`, for example
`agent/codex/local-loader`. Two active writers must never share a dirty
worktree. Human review and read-only comparison may use any worktree.

Before editing, the controller adds an entry to `active_assignments.toml` with
the agent family, branch, base commit, role, complete write scope, explicitly
permitted shared files, and current state. Scopes must not overlap between
active assignments. The controller removes the entry after merge or
abandonment; durable outcomes belong in the commit history or the appropriate
research-note handoff.

## Ownership and shared interfaces

Provider-owned implementation paths are declared in `ownership.toml` and
reviewed through `.github/CODEOWNERS`. An agent may read and test every
implementation but writes only within its own provider paths. A new provider
gets new directories under `src/`, `experiments/providers/`, and
`tests/providers/`; an existing provider directory is never repurposed.

Shared code exposes neutral contracts. Cross-provider comparisons use
`src/solver_contract.py`, experiment records, and tests. They do not copy or
rewrite another provider's implementation. Changes to shared mathematical
definitions still require the documentation and verification described in the
root `AGENTS.md`.

## Shared-file changes

An assignment may change a shared file only when that exact file or directory
is listed in both its write scope and its permitted shared files. Shared changes
should be limited to interfaces, orchestration, documentation, tests, and
coordination records needed by the task. A reviewer confirms these paths before
merge.

Run the repository checks before handoff:

```bash
make agent-audit
make test
make lint
```

The default branch should require a pull request, passing checks, and owner
review. Repository hosting settings are managed outside this worktree; the
checked-in workflow and CODEOWNERS file express the expected rule.

## Context loading

`context.toml` is the canonical context manifest. Agent products translate it
to their own include/exclude controls. Provider implementations, source-paper
files, archived manuscripts, immutable round history, generated output, and
host-provided agent packages are excluded from default context and loaded only
for a named task. A provider assignment loads only its matching provider paths;
cross-provider review is explicitly read-only.

Host-provided agent packages belong outside the versioned worktree. If a host
mounts them at `.agents/` for a paper-import task, the mount remains ignored by
Git and excluded from normal project context.

## Handoff

Use `handoff-template.md`. A handoff names the branch and base commit, describes
every modified scope, identifies shared files, records checks, and states any
open decisions. A review-ready handoff changes the assignment state to
`ready_for_review`; it does not merge its own provider-owned work without the
required review.
