# Contribution workflow for a new agent

This workflow turns the formal problem into a bounded, reviewable
assignment. The root [`AGENTS.md`](../../AGENTS.md) and
[`docs/coordination/policy.md`](../coordination/policy.md) are authoritative
if this summary differs.

## Before writing

1. Read [`README.md`](README.md),
   [`problem-definition.md`](problem-definition.md), and
   [`research-status.md`](research-status.md).
2. Obtain a task identifier, agent family, role, base commit, disjoint write
   scope, and permitted shared files from the controller.
3. Register the assignment in
   [`active_assignments.toml`](../coordination/active_assignments.toml).
4. Use a dedicated clean worktree on a branch named
   `agent/<family>/<task>`.
5. Load the default files declared by
   [`context.toml`](../coordination/context.toml), then load only the
   direction, provider code, literature source, or history explicitly needed
   by the assignment.
6. Run `make agent-audit` before the first substantive edit.

Active assignments must have disjoint write scopes. A shared file may be
changed only when it is listed in both the assignment's write scope and its
permitted shared files.

## If the assignment changes theory or algorithms

Read all of the following before editing:

- [`docs/research-context.md`](../research-context.md);
- [`docs/mathematical-conventions.md`](../mathematical-conventions.md);
- the relevant file under [`docs/literature/`](../literature/);
- [`docs/decisions/residual-convention.md`](../decisions/residual-convention.md)
  when a residual, normalization, or stopping rule is involved;
- [`manuscript/notes/AGENTS.md`](../../manuscript/notes/AGENTS.md);
- the assigned direction's `README.md`, `STATUS.md`, source note, and formal
  dependencies in
  [`manuscript/notes/registry.toml`](../../manuscript/notes/registry.toml).

A source paper is evidence for its own result. The repository documentation
is authoritative for this project's notation and conventions. Verify an
imported theorem or equation against the source PDF and record a page or
section pointer in the relevant literature note.

## If the assignment changes code or experiments

Before source changes, read [`src/AGENTS.md`](../../src/AGENTS.md) and
[`src/README.md`](../../src/README.md). Solver implementations are owned by
agent family. Write only in the provider directories assigned to that
family; compare implementations through
[`src/solver_contract.py`](../../src/solver_contract.py), tests, and
experiment records.

Before experiment changes, read
[`experiments/README.md`](../../experiments/README.md). Every recorded run
must include:

- graph and seed;
- `alpha` and every accuracy or regularization parameter;
- random seed;
- actual stopping rule and certificate;
- solver parameters;
- Git commit and dirty-worktree state;
- local-work measurements appropriate to the problem contract.

Never edit a generated figure manually.

## Claim discipline

Every research note separates these evidence classes:

- **Source:** imported from a cited source with an exact pointer;
- **Proved:** derived in the owning note under stated assumptions;
- **Conditional:** valid only if named missing assumptions or lemmas hold;
- **Measured:** observed in a reproducible computation;
- **Open:** not established;
- **Refuted:** a precisely scoped claim stopped by proof or counterexample.

Do not use measured evidence as proof, import a conditional result as
unconditional, or broaden a scoped stop into a class lower bound. Preserve
failed proof paths when they rule out a reusable mechanism.

## Recommended first contribution

A good first assignment is narrow enough to have one falsifiable output:

- rederive one named lemma and audit every assumption;
- test one proposed invariant on the smallest exact graph family that can
  invalidate it;
- formalize one missing conversion between an RPPR certificate and the PPR
  semantic target;
- add one exact or reproducible proof audit for an already stated claim; or
- review one direction's current “Resume here” target and return a scoped go
  or stop result.

Do not begin by rewriting the active manuscript or by combining several open
directions into one new narrative.

## Copyable assignment brief

Use this block when handing work to another agent:

```markdown
# Assignment: <short task name>

- Agent family: <family>
- Role: <direction | implementer | reviewer | controller>
- Branch: agent/<family>/<task>
- Base commit: <40-character commit>
- Write scope: <complete disjoint path list>
- Permitted shared files: <exact shared path list>

## Question

<One falsifiable mathematical or implementation question.>

## Contract

- Graph, seed, and parameter regime:
- Accuracy namespace and terminal certificate:
- Access model and charged work:
- Allowed support and inverse primitives:
- Deterministic or probabilistic guarantee:

## Required context

- Direction STATUS and exact resume pointer:
- Formal dependencies:
- Relevant literature note and source pointers:
- Existing result or counterexample that must be preserved:

## Deliverable and stop/go test

- Required artifact:
- Go condition:
- Stop condition:
- Explicitly out of scope:

## Verification

- Focused proof audit, test, or build:
- Repository checks:
```

## Before handoff

1. Reconcile changed definitions with project conventions and accepted
   decisions.
2. Update the direction `STATUS.md`, shared ledgers, or literature pointers
   only when the assignment owns those paths and the evidence requires it.
3. Run the focused check for the changed artifact.
4. Run:

   ```bash
   make agent-audit
   make test
   make lint
   ```

5. Run `make reproduce` before changing reported experimental results.
6. Complete a handoff based on
   [`handoff-template.md`](../coordination/handoff-template.md) and mark the
   assignment `ready_for_review`.

The handoff must name all modified shared files, commands run, results, and
remaining open decisions. Review readiness does not itself authorize a merge.
