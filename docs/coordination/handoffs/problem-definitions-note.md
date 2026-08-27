# Handoff: problem-definitions-note

- Agent family: codex
- Role: direction
- Branch: `agent/codex/problem-definitions-note`
- Base commit: `b5f34cf8a02d07ab5fbca9c2e0304e815177a7c3`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/problem-definitions-note.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/problem_definitions/`
  - `manuscript/notes/registry.toml`
- Permitted shared files:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/problem-definitions-note.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`

## Outcome

- Requested result: create an independent problem-definitions note containing
  exactly the problem definitions and well-known properties of the problem.
- Implemented result: added a standalone, buildable six-page reference note
  for PPR and RPPR. It imports the shared canonical formulation, defines the
  exact sparse-output problems, translates five common formulations, and
  records source-backed spectral, positivity, normalization, residual,
  optimality, support-volume, and regularization-bias properties.
- Deliberately unchanged: algorithms, experiments, complexity targets, open
  conjectures, the implementation-wide residual decision, and all files from
  the user's original main worktree. The requested hyphenated display name is
  represented by the repository-compliant note ID `problem_definitions`.

## Evidence

- Tests added or changed: no code tests; the existing note-inventory and
  manuscript-notation tests cover the new registry entry and structural
  contract.
- Commands run: `make -C manuscript/notes/problem_definitions`,
  `make note-audit`, `make note-targets`, `make agent-audit`, `make test`,
  `make lint`, and `git diff --check`.
- Results: the note builds with resolved references; inventory, target report,
  coordination audit, diff check, Ruff code checks, and all 210 tests pass.
  `make lint` stops only because Ruff would reformat the pre-existing files
  `manuscript/notes/path_face_lock_warmup/verify_warmup.py` and
  `manuscript/notes/signed_star_acceleration/verify_star.py`, which are outside
  this assignment.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: the coordination assignment/handoff, note registry,
  and generated note index.
- Open decisions or follow-up: none inside the note. If the repository adopts
  a canonical residual later, synchronize this reference with that decision
  without turning it into an algorithm or research-claim note.
