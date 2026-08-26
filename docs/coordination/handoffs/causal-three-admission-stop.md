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
  - Added the causal consumed-energy reserve
    `R_k=E_0+D_k-E_k`. It starts at zero, increases by exactly the energy
    consumed on executed fixed-face steps, and is unchanged by exact
    transported admissions.
  - Derived the exact finite-trace coefficient
    `lambda*=max [Xi_k-D_k]_+/R_k`. The six-vertex trace needs
    `1772625800261634289972166085525 /
    136208548497122966464402947962896 = 0.013014...`, attained at stage 7.
  - Exhausted every seed of every connected NetworkX graph-atlas
    representative through order seven at `q=1/5`: 6,780 rooted traces,
    2,847 raw-ledger insolvencies, and exact maximum
    `2786829024075210327/1036704485947225385 = 2.688161...`, already attained
    by a leaf-seeded `K_{1,5}`. Thus coefficient `3` repairs this finite atlas.
  - Proved an exact small-`q` STOP on the actual zero-start leaf-seeded
    `K_{1,4}` recurrence. The hub is admitted at stage 1, all other leaves at
    stage 2, and stage 3 holds with
    `lambda_3(q) ~ 1/(32q^3)`. Hence no constant or
    `O(polylog(1/q))` multiple of this reserve is uniformly solvent.
  - Proved that the named complete gate preserves `Xi` exactly across
    admissions. On interior traces it has sufficient coefficient
    `(1+q^2)(1-q)/q^5`, and the sharper
    `2 c_low(1-q)/q^3` under the explicit low-frequency condition
    `||r||_D^2 <= 2 c_low q^2 P`.
- Deliberately unchanged:
  - No convergence failure, objective or work lower bound, asymptotic family,
    finite-precision claim, nonpath eleven-resource vector, or class lower
    bound is asserted.
  - Structural promised-class ledgers, justified extra reserve, stronger
    observables, and different recurrences or gates remain open. In
    particular, the low-frequency condition is not claimed graph-uniform.
  - No provider-owned code, shared problem definition, dependency edge, or
    file in the user's dirty main worktree changed.

## Evidence

- Tests added or changed:
  - Added
    `volume_gated_acceleration.all_history_three_admission_stop`, an exact
    rational proof audit registered as the Round-022 mechanism.
  - Added `volume_gated_acceleration.consumed_energy_reserve`, an exact
    rational Round-023 audit. Its fast path checks the six-vertex minimum,
    actual star chronology, exact rational functions, and formal asymptotic
    coefficients; its full path enumerates the rooted graph atlas through
    order seven.
- Commands run:
  - `uv run python -m experiments.proof_audits.runner --tier full --audit volume_gated_acceleration.all_history_three_admission_stop`
  - `uv run python -m experiments.proof_audits.runner --tier full --note volume_gated_acceleration`
  - `uv run python -m experiments.proof_audits.runner --tier full --audit volume_gated_acceleration.consumed_energy_reserve`
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
  - Both new exact audits and all eleven full-tier direction audits pass; the
    existing full tier also exhausts all 3,806 connected labeled rooted graphs
    on two through five vertices for the earlier restarted-ledger pattern, and
    the new audit exhausts 6,780 rooted graph-atlas traces through order seven.
  - The note builds successfully, the 18-note inventory is consistent, the
    audit registry lists the new mechanism, and coordination checks pass.
  - All 210 tests pass, with only temporary-directory cleanup warnings.
  - Both new audits pass Ruff lint and format checks; whitespace checks pass.
  - Repository-wide `make lint` remains blocked by 1,345 pre-existing Ruff
    errors in tracked overnight research scripts already present at the base
    commit. No remaining lint error is in the new audit.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: the exact coordination record/handoff, proof-audit
  registry and new audit, and the `volume_gated_acceleration` note only.
- Open decisions or follow-up:
  - Decide whether to pursue a structural promised-class condition, an
    explicitly sourced reserve, or a stronger observable. The sharp next
    target is to prove the displayed low-frequency condition on a useful
    reachable promised class, close the `q^-3` versus `q^-5` coefficient gap,
    or find a reachable `omega(q^-3)` family.
  - The finite witness recovers at stage 9 and certifies at stage 12, so it
    must not be promoted into an asymptotic or convergence obstruction.
  - Maintaining the reserve needs the current restricted optimum and an
    active-face energy evaluation. Any uncached solve, scan, arithmetic,
    state, and validation costs must be charged.
