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
  - Sharpened the original-score upper coefficient to `2/q^4` whenever the
    nonnegativity projection is inactive. The proof uses a one-mode quadratic
    PSD certificate whose determinant has an exact nonnegative tensor
    Bernstein expansion of degrees `(10,5)`.
  - Added an exact projection-active three-vertex RPPR state where the
    original all-coordinate residual violates the `2(E-E+)` decrement even
    though the standard energy contraction is strict. This is an algebraic
    state STOP, not a zero-start reachability claim.
  - Added the safe positive-support envelope and score. A Stieltjes
    subsolution comparison proves envelope safety, and the exact projected
    prox slack gives sufficient coefficient `(1-q^2)/q^4` under arbitrary
    projection. This modified gate can have a different chronology and still
    must inspect clipped-zero rows for admission and termination.
  - Verified that the six-vertex trace, all 6,780 atlas traces, and the
    reviewed stages of the small-`q` `K_{1,4}` family have inactive candidate
    projection. Hence the star's `Omega(q^-3)` lower requirement also applies
    to the support-aware ledger.
  - Closed that gap with an actual zero-start reachable family on a
    `K_{2,3}` plus one seed leaf. Stages 1 and 2 admit the first hub and all
    three middle vertices; stages 3 and 4 hold with strictly positive
    candidates. At stage 4,
    `Xi=49/4096-1141q/10240+O(q^2)` and
    `R=(971/1024)q^4+(52493/15360)q^5+O(q^6)`, so every solvent coefficient
    satisfies `lambda(q) >= 49/(3884q^4)+O(q^-3)`. This proves sharp
    graph-uniform `Theta(q^-4)` order for the support-aware ledger and the
    inactive original-score subclass.
  - Extended the leading-order replay to every fixed `K_{2,r}` plus seed leaf,
    `r >= 3`. Its exact scaled lower constant is
    `(s-1)(s^2-2s-1)^2 /
    {s(15s^4-15s^3+2s^2+s-3)}`, where `s=r+1`, and tends to `1/15` as
    `r` grows. Thus every graph-uniform coefficient has
    `liminf q^4 lambda(q) >= 1/15` along this family.
  - Retained the exact projection normal
    `n=r(y)-(y-p)` instead of dropping it. With
    `b=(1-q)z+qz*`, the fixed-step decrement contains
    `<n,b>_D` and the post residual is `n+(I-H)g`. Therefore the original
    all-coordinate ledger has coefficient `(C_n+1-q^2)/q^4` whenever every
    clipped positive-residual row obeys `n_i <= C_n b_i`; inactive projection
    is the exact case `C_n=0`.
  - Proved the point-seed clipped-row dichotomy: a clipped seed row has
    negative post residual, while a clipped nonseed row has post residual at
    most `q^3/5`. If the interpolation is nonnegative, its projection normal
    is also at most `q^3/5`. These bounds alone do not supply a consumed-reserve
    baseline, so the unconditional `q^-4` conclusion remains open.
  - Stopped the direct critical endpoint-path construction. For the longest
    full path with positive terminal restricted optimum, exact zero-start
    replays at `q=1/8,1/12,1/16` certify on prefixes of sizes `8,12,17`
    instead of the intended sizes `10,14,19`; every raw candidate is positive.
- Deliberately unchanged:
  - No convergence failure, objective or work lower bound, finite-precision
    claim, nonpath eleven-resource vector, or solver-class lower bound is
    asserted.
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
    coefficients. It now also verifies the exact Bernstein determinant table,
    strict candidate positivity through the star's reviewed stages, and the
    projection-active original-score STOP. It additionally performs a formal
    exact first-order series replay of the quartic family and exact rational
    replays at `q=1/20,...,1/640`, including the later stage-15 admission and
    stage-4 worst checkpoint. Its full path enumerates the rooted graph atlas
    through order seven. The fast path also checks the exact leading scaled
    recurrence and closed-form debt/reserve constant for
    `r=3,4,5,7,10,30` in the `K_{2,r}` extension.
    It now also checks the projection-normal decomposition, exact normal
    slack, the algebraic ratio `11929/50`, and the three finite critical-path
    gate failures.
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
  - `uv run ruff check experiments/proof_audits/volume_gated_acceleration/consumed_energy_reserve.py`
  - `uv run ruff format --check experiments/proof_audits/volume_gated_acceleration/consumed_energy_reserve.py`
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
    scalar target is now only the original all-coordinate score under
    arbitrary projection: its reachable lower order is `q^-4` and its general
    upper coefficient remains `O(q^-5)`. The exact next target is now a
    graph-uniform bound on the normal-anchor ratio, or a reachable family on
    which that ratio creates superquartic debt. The displayed low-frequency condition
    can apply only on a narrower promised class, not all reachable traces.
  - The finite witness recovers at stage 9 and certifies at stage 12, so it
    must not be promoted into an asymptotic or convergence obstruction.
  - Maintaining the reserve needs the current restricted optimum and an
    active-face energy evaluation. Any uncached solve, scan, arithmetic,
    state, and validation costs must be charged.
  - Exact support membership also needs a numerical margin and validation;
    the support-aware scalar score does not remove clipped-zero rows from
    boundary or terminal gate scans.
