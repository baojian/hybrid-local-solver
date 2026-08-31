# Handoff: OP2 randomized two-stage transfer

- Agent family: codex
- Role: direction
- Branch: `agent/codex/op2-randomized-transfer-6h`
- Base commit: `6231a1c2ffed37eecef3e265f6d415bd2caaeaa8`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/op2-randomized-two-stage-transfer-6h.md`
  - `experiments/proof_audits/registry.toml`
  - `experiments/proof_audits/two_stage_point_source_aesp_cd/`
  - `experiments/two_stage_point_source_aesp_cd/`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/two_stage_point_source_aesp_cd/`

## Outcome

- Requested result: audit the repository note claiming a randomized complete
  solution of OP2 and determine whether its techniques close the point-source
  two-stage AESP-CD/RPPR Stage-I problem.
- Source verdict: `active_edge_lcp` does prove OP2 in the canonical exact-real
  randomized word model.  Its threshold-batch theorem rebuilds only
  `O_tilde(alpha^(-1/2) log(1/eps_obj))` safe exposed faces.  Each face uses a
  fresh randomized nearly-linear SDD solve, an exact active-residual
  acceptance scan, capped independent retries, and a complete thresholded
  boundary batch.  Block-Cholesky/Chebyshev decay, rather than persistent
  dynamic response, supplies the square-root phase count.
- New transfer proved here: Stage I need not find or contain all of `S*`.  If
  a safe inner face `U` has RPPR objective gap `Gamma_U`, then

  ```text
  max_{i outside U} x*_rho(i)/sqrt(d_i) <= sqrt(2 Gamma_U/alpha),
  PPR_error(Q_U^(-1)b_U) <= rho + sqrt(2 Gamma_U/alpha).
  ```

  This follows from strong convexity plus the existing approximate-envelope
  linearization lemma.
- Literal two-stage result: set `eps_obj=alpha eta^2/2`, retain only the final
  threshold-batch face, discard every numerical/randomized Stage-I state, and
  solve ordinary PPR independently on that face to error `tau`, with
  `rho+eta+tau<=eps_ppr`.  The expected fully charged work is
  `O_tilde(1/(eps_ppr sqrt(alpha)))` on every graph, with declared failure
  probability.
- Shortest execution: with `rho=eps_ppr/2` and
  `eps_obj=alpha eps_ppr^2/8`, the certified numerical RPPR point returned by
  OP2 is already a valid PPR output, so Stage II is optional.
- AESP-CD verdict: the threshold, safe-admission, hard-cap, certification, and
  restart mechanisms transfer as a new active-set portfolio lane.  This does
  not prove that the original AESP-CD momentum recurrence survives changing
  faces.
- Remaining scope: deterministic finite-precision/coefficient-bit complexity,
  a practical local KMP-style SDD realization, and persistent response reuse
  remain open.  The point-source result is not promoted to an additive
  `nnz(s)` theorem for general sparse sources.

## Manuscript reduction

- The full note now contains the complete imported-source ledger, the new
  inner-face lemma, the literal two-stage theorem, direct-return corollary,
  Las Vegas wrapper, and exact scope boundary.
- The same two-page theorem core is shared by the short and strict papers.
  Current compiled sizes are 40 pages for the full audit, 12 pages for the
  short paper, and 6 pages for the strict support-first paper.
- Stale claims that arbitrary-graph discovery was wholly open were corrected
  throughout the abstracts, scope, reduction plan, status, registry, README,
  and claim-to-evidence map.  The stronger exact-support/containing-envelope
  reporter remains an optional deterministic/persistent target.

## Evidence

- New registered exact audit
  `two_stage_point_source_aesp_cd.randomized_op2_transfer`:
  - 40 exact rational graph instances;
  - 171 positive inner faces;
  - four paths that deliberately reach the batch cap with incomplete support;
  - exact checks of strong-convexity amplitude transfer, principal-PPR
    linearization, support volume, and semantic error.
- New 67-case numerical prototype:
  - seven graph families over three alpha values and three target accuracies;
  - four tiny-rho strict-inner-face cap exits;
  - both Stage I and Stage II receive randomly shaped errors that pass their
    exact residual acceptance tests;
  - all direct and literal Stage-II outputs meet the PPR target;
  - largest direct/Stage-II semantic ratios are `0.500010/0.462166`.
- The existing saved-result consistency audit now checks the new CSV and its
  residual, objective-gap, incomplete-face, and semantic-error columns.
- Source note audits rechecked: 720 exact threshold cases, 36 exact
  telescopes, 580 exact paths, 1,152 batch-depth cases, and 216 independent
  100-digit cases.
- Koutis--Miller--Peng's source contract was rechecked: constant-success chain
  construction is amplified here only by exact residual certification and
  capped independent retries; no unsupported arbitrary failure interface is
  attributed to the source theorem.

## Checks

- Full/short/strict LaTeX builds pass as 40/12/6 pages with resolved
  references and citations and no overfull-box diagnostics.
- All three registered two-stage fast audits pass.
- Proof-audit registry consistency passes: 65 audits.
- Experiment smoke reproduction passes.
- Scoped Ruff check/format and `git diff --check` pass.
- Agent-boundary audit passes after this assignment moves to
  `ready_for_review`.
- Repository Pytest reports 210 passed and three pre-existing provider
  failures outside this scope: one `r_rho` semantic alias and the
  1,237/4,361-line provider-section inventory limits.  The earlier
  active-assignment overlap disappears after this assignment's review
  transition.
- Global Ruff has one pre-existing unused import in
  `manuscript/notes/problem_definitions/verify_exact_batch_cholesky.py`;
  neither that file nor the provider failures were modified.

## Review notes

- Provider-owned theorem sources changed: none.  `active_edge_lcp` was read
  and independently audited but not edited.
- The numerical prototype is not a KMP implementation; it tests the exact
  post-solver interface using adversarially shaped accepted errors.
- The new proof materially changes the project verdict: the arbitrary-graph
  existence question is solved in the exact-real randomized word model, but
  not yet as a deterministic floating-point implementation.
- The commit containing this handoff is the review-ready transfer commit.
