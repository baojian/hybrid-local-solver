# Handoff: aesp-cd-two-stage-8h

- Agent family: codex
- Role: direction
- Branch: `agent/codex/aesp-cd-two-stage-8h`
- Base commit: `6b4f44a0780f529cff03991626a537caafd16ac1`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/aesp-cd-two-stage-8h.md`
  - `experiments/proof_audits/registry.toml`
  - `experiments/proof_audits/two_stage_point_source_aesp_cd/`
  - `experiments/two_stage_point_source_aesp_cd/`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/two_stage_point_source_aesp_cd/`
- Permitted shared files:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/aesp-cd-two-stage-8h.md`
  - `experiments/proof_audits/registry.toml`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`

## Outcome

- Requested result: develop a point-source, at-most-two-stage hybrid around
  AESP-CD/SOR/APPR, identify or certify a useful Stage-I set with charged
  local work, restart once, shorten the long manuscript, and preserve exact
  theorem boundaries.
- Implemented result:
  - A standalone 36-page proof note, 10-page short paper, and 4-page strict
    theorem core.
  - A proved composition interface: a certified RPPR envelope `E` followed
    by one ordinary principal-PPR solve gives total charged work
    `W_disc + O_tilde(vol(E)/sqrt(alpha))`; exact structural completion uses
    `rho=epsilon` and no unused terminal half-budget.
  - An at-most-two-stage algorithm: numerical certificates return early;
    lower-safe AESP mass states complete by APPR/SOR; genuinely set-only
    screens discard all changing-face history and solve once.
  - Concrete Stage-I lanes: hard-capped Green balls, direct PPR leakage,
    APPR snapshot plus exact-face verification, positive-residual SOR/AESP,
    exact positive batches, and exact point-source tree threshold messages.
  - A fair race with direct APPR, so every speculative failure has a
    constant-factor fallback.
  - Executable tree/unicyclic factors reused for both RPPR and ordinary-PPR
    right-hand sides.
  - A residual-interval exact-face verifier; exhaustive randomized checking
    rejected every false face among 8,096 candidates on 36 small structural
    systems and certified all 36 exact supports.
  - A claim-to-evidence index and an explicit 100-page-to-4/10-page reduction
    plan.
- Deliberately unchanged:
  - No arbitrary-graph accelerated Stage-I reporter is claimed.
  - The point-source result is not promoted to the desired additive
    `nnz(s)` sparse-source theorem.
  - The long `aesp_cd_l1_rppr` provider note remains the companion proof
    audit; no provider-owned theorem source was edited.
  - Existing repository-wide formatting and note-inventory debt is not
    repaired outside this assignment.

## Evidence

- Tests added or changed:
  - Registered exact audit
    `two_stage_point_source_aesp_cd.two_stage_composition`.
  - Registered saved-result/numerical audit
    `two_stage_point_source_aesp_cd.saved_results_consistency`.
  - Exact Fraction checks include obstacle comparison, sparse-source linear
    superposition, the multi-source RPPR obstruction, all 192 subsets in
    three envelope instances, fixed-envelope completion, leakage, mass, fair
    races, and structural tails.
  - Numerical checks include semantic error for every saved finite output,
    reusable factors on three named and 80 randomized tree/unicyclic systems,
    and 8,096 exhaustive randomized verifier candidates.
- Commands run:
  - `make experiments`
  - `make figures`
  - `make paper`
  - all three local `latexmk` entrypoints
  - targeted proof-audit runner and registry consistency
  - complete 90-row APPR and SOR reruns to temporary outputs
  - scoped Ruff and `git diff --check`
  - repository tests, note inventory, lint, and agent-boundary checks during
    final integration
- Results:
  - Main/short/strict PDFs build as 36/10/4 pages.
  - Targeted proof audits pass 2/2.
  - APPR sweep remains 28 certified, literal fresh/reused fair wins 2/2.
  - SOR sweep remains 75 certified, literal fresh/reused fair wins 5/5.
  - Exact-batch fresh/reused fair wins are 8/9; tree messages 14; structural
    Green 35.
  - `make experiments`, `make figures`, and `make paper` pass.
  - Scoped Ruff and diff checks pass.
  - `make agent-audit` passes.
  - Repository Pytest: 207 passed, 3 failed.  All three failures are
    pre-existing and outside this assignment: the provider note's `r_\rho`
    semantic alias plus its 1,237-line `06b` and 4,361-line `06d` inventory
    violations.
  - Repository `ruff check` passes.  Scoped format checking passes; global
    format checking still lists 14 pre-existing files under
    `experiments/proof_audits/aesp_cd_l1_rppr/`.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: assignment registry, proof-audit registry, note
  registry, and note README only.
- Open decisions or follow-up:
  - The key remaining theorem is an adjacency-local arbitrary-graph set
    reporter producing a certified `O_tilde(1/epsilon)` envelope in
    `O_tilde(1/(epsilon sqrt(alpha)))` charged work before APPR finishes.
  - Current APPR/SOR/AESP numerical proposal lanes often already meet the
    semantic target; a forced second solve is therefore deliberately not the
    default execution.
  - Repository-wide tests retain pre-existing failures in provider notation,
    provider section-length inventory, and unrelated formatting checks; see
    the final command transcript rather than attributing them to this branch.
