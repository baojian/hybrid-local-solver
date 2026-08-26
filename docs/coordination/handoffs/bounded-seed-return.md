# Handoff: bounded-seed-return

- Agent family: codex
- Role: direction
- Branch: `agent/codex/bounded-seed-return`
- Base commit: `a02b39a2bb12e8e9d528ae1f011f8f041f98bed3`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/bounded-seed-return.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/bounded_seed_return/`
- Permitted shared files:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/bounded-seed-return.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`

## Outcome

- Requested result: decide whether bounded ordinary seed degree can coexist
  with `vol(S_eps_ppr) = Theta(1/eps_ppr)` and
  `pi_v/gamma_alpha = Theta(1/alpha)`, and preserve the result as a standalone
  rigorous direction.
- Implemented result: proved the local spectral-measure envelope
  `F_v(t) <= 4 d_v sqrt(t)`, integrated it with explicit constants to bound
  the discounted seed diagonal, ruled out the simultaneous bounded-degree
  scalings in the joint local limit, and derived the exact necessary-degree
  lower bound `Omega(1/(eps_ppr + sqrt(alpha)))`.  The note records that the
  stronger `Omega(1/eps_ppr)` conclusion needs
  `alpha = O(eps_ppr^2)`, supplies exact formulas for paths, caterpillars, hub
  ladders, and regular trees, and includes a deterministic verifier.
- Deliberately unchanged: the dirty main worktree, the separately owned
  `class_separation_ladder` direction, shared mathematical conventions, and
  every solver implementation.  The note does not claim an algorithmic upper
  bound or exclude a distributed signed-relaxation lower bound.

## Evidence

- Tests added or changed: added the standalone deterministic
  `manuscript/notes/bounded_seed_return/verify.py`; no repository test file was
  modified.
- Commands run:
  - `make -C manuscript/notes/bounded_seed_return`
  - `uv run python manuscript/notes/bounded_seed_return/verify.py`
  - `make note-audit`
  - `make note-report`
  - `make agent-audit`
  - `make test`
  - `make lint`
  - `uv run ruff check manuscript/notes/bounded_seed_return/verify.py`
- Results: eight-page warning-free PDF; 20-note inventory consistent; 4,176
  rooted spectral/resolvent cells and all family/formula checks pass;
  coordination audit passes; 210 repository tests pass with 15 temporary-file
  cleanup warnings; focused Ruff passes.  Repository-wide lint reports 1,345
  pre-existing findings under `manuscript/claude-overnight-2026-08-24/`, all
  outside the assignment scope.

## Review notes

- Provider-owned paths changed: new
  `manuscript/notes/bounded_seed_return/` direction.
- Shared paths changed: `docs/coordination/active_assignments.toml`, this
  handoff, `manuscript/notes/README.md`, and
  `manuscript/notes/registry.toml`.
- Open decisions or follow-up: integrate the theorem into the separately
  owned class-separation ladder after review.  Any continued lower-bound
  search should target distributed charged work rather than another
  bounded-degree seed-return witness.
