# Handoff: causal-three-admission-stop

- Agent family: codex
- Role: direction
- Branch: `agent/codex/causal-three-admission-stop`
- Base commit: `71764c15c5bc2bb92f01d9d807942acf61e4be85`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/causal-three-admission-stop.md`
  - `experiments/proof_audits/registry.toml`
  - `experiments/proof_audits/volume_gated_acceleration/`
  - `manuscript/notes/volume_gated_acceleration/`
- Permitted shared files: same as the complete write scope above.

## Outcome

- Requested result: Resolve the note's all-history causal-solvency target by
  proving a structural theorem or finding an exact debt obstruction across at
  least three admissions, then record the result without touching the dirty
  main worktree.
- Implemented result:
  - Added an exact six-vertex zero-start execution with three consecutive
    singleton admissions at stages 1, 2, and 3.
  - Proved that all three realized restricted-optimum drops total
    `1305901/5362906250`, yet the all-history `Xi=delta^2` balance is negative
    at held stages 7 and 8 before recovering at stage 9.
  - Replayed the causal update in chronological order from the actual zero
    initialization, including separate pre-gate and post-admission checkpoints,
    exact complete-gate inequalities, Schur loads/pivots, positivity margins,
    and the terminal certificate.
  - Promoted the result as a finite algorithm-specific Refuted route and
    updated the abstract, scope, implications, proof sequence, claim ledger,
    README, and STATUS resume target.
- Deliberately unchanged:
  - No convergence failure, objective or work lower bound, asymptotic family,
    finite-precision claim, nonpath eleven-resource vector, or class lower
    bound is asserted.
  - Structural promised-class ledgers, justified extra reserve, stronger
    observables, and different recurrences or gates remain open.
  - No provider-owned code, shared problem definition, dependency edge, or
    file in the user's dirty main worktree changed.

## Evidence

- Tests added or changed:
  - Added
    `volume_gated_acceleration.all_history_three_admission_stop`, an exact
    rational proof audit registered as the Round-022 mechanism.
- Commands run:
  - `uv run python -m experiments.proof_audits.runner --tier full --audit volume_gated_acceleration.all_history_three_admission_stop`
  - `uv run python -m experiments.proof_audits.runner --tier full --note volume_gated_acceleration`
  - `make -C manuscript/notes/volume_gated_acceleration`
  - `make note-audit`
  - `make research-audit-list`
  - `make agent-audit`
  - `uv run python -m tools.agent_boundaries check-worktree --branch agent/codex/causal-three-admission-stop`
  - `make test`
  - `uv run ruff check experiments/proof_audits/volume_gated_acceleration/all_history_three_admission_stop.py`
  - `uv run ruff format --check experiments/proof_audits/volume_gated_acceleration/all_history_three_admission_stop.py`
  - `make lint`
  - `git diff --check`
- Results:
  - The new exact audit and all ten full-tier direction audits pass; the
    existing full tier also exhausts all 3,806 connected labeled rooted graphs
    on two through five vertices for the earlier restarted-ledger pattern.
  - The note builds successfully, the 18-note inventory is consistent, the
    audit registry lists the new mechanism, and coordination checks pass.
  - All 210 tests pass, with only temporary-directory cleanup warnings.
  - The new audit passes Ruff lint and format checks; whitespace checks pass.
  - Repository-wide `make lint` remains blocked by 1,345 pre-existing Ruff
    errors in tracked overnight research scripts already present at the base
    commit. No remaining lint error is in the new audit.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: the exact coordination record/handoff, proof-audit
  registry and new audit, and the `volume_gated_acceleration` note only.
- Open decisions or follow-up:
  - Decide whether to pursue a structural promised-class condition, an
    explicitly sourced reserve, or a stronger observable. Any replacement
    must survive the path two-admission GO, asymmetric-T restarted STOP, and
    this zero-start three-admission all-history STOP.
  - The finite witness recovers at stage 9 and certifies at stage 12, so it
    must not be promoted into an asymptotic or convergence obstruction.
