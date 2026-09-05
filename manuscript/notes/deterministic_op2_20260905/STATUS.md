# Direction status: deterministic_op2_20260905

Last reviewed: 2026-09-06
State: proved-open
Agent family: codex
Role: reviewer
Branch: `main`
Base commit: `e83d996e7e61534ba5f3724ea3df3e25778a7ba9`
Allowed write scope: this note directory and its mechanical registry/index registration.

## Exact question and contract

- **Question:** Deterministically solve canonical point-source RPPR with the
  OP2 root-condition-number locality bound.
- **Model:** Finite simple connected undirected graph, unit edges, at least
  two vertices, one seed vertex, original degrees, `0 < alpha <= 1`.
- **Accuracy namespace:** `eps_obj` is additive gap for `F_rho`; `eps_ppr` is
  degree-normalized PPR solution error and has a separate conversion.
- **Access and charged work:** Local degree and adjacency-list access;
  every first/repeated incidence, scalar operation, comparison, state access,
  response update, threshold query, certificate, materialization, and output
  is charged. No ambient preprocessing or supplied optimal support.
- **Intended result:** `O_tilde(1/(rho*sqrt(alpha)))` exact-real algebraic word
  work, with only polylogarithmic objective-accuracy dependence. A bounded
  rational implementation includes input/label encoding lengths in bit costs.

## Claim ledger

- **Source:** Canonical RPPR facts from `problem_definitions`; continuation
  and two-energy argument from the parallel task **Prove conjecture 2
  deterministically**, restated and independently checked in the archived
  proof audit. The core proof's origin is not attributed to this task.
- **Proved here:** Audit-supported extension to a fixed degree-pruned
  principal matrix; boundary-forest spectral certificate; bounded certified
  component/pilot refinements; early PG checkpoints; rational coordinate
  conversion; fixed-size exact obstacle shortcut. The full audited argument
  yields the stated deterministic OP2 bound for this algorithm.
- **Conditional:** No unproved trajectory/confinement assumption is invoked
  for that bound. Extensions beyond the stated graph/seed model require their
  own proofs. This record is not an external or machine-checked verification.
- **Measured:** Original verification totals and structured exact-arithmetic
  timings are in `VERIFICATION.md`; 17 portable tests accompany the code.
  All research runs were deterministic; no random seed was used.
- **Refuted:** Earlier cyclic-dual-averaging support containment and uniform
  signed-Chebyshev mass arguments have recorded counterexamples. These do
  not refute the different continuation algorithm.
- **Open:** General accelerated rate for the earlier score-repair candidate;
  optional global-pivot implementation; matched practical comparison against
  optimized FISTA/AESP; weighted and general-seed extensions; external review.

## Central blocker

No unresolved lemma was found in the completed audit of the stated OP2
algorithm. The main remaining practical question is falsifiable: does an
implementation with controlled numerical error beat optimized FISTA at the
same certified objective accuracy, including all state and graph costs?

## Dependencies and reusable outputs

- **Formal registry dependencies:** `problem_definitions`.
- **Source/shared prerequisites:** shared source-aligned RPPR model, Stieltjes
  positivity, original-degree volume and support bounds.
- **Context/provenance:** The external parallel task supplied the core proof;
  earlier manuscript directions motivated checks and are compared in
  `research-notes/prior-obstructions-vs-complete-proof.md`. Those comparisons
  are not additional formal imports or newly validated algorithms.
- **Supplies to:** Future independent review and practical implementation.
  No automatic promotion into the active manuscript is made.

## Resume here

- **Exact file/section/lemma:** `main.tex` and its section files, especially
  `thm:det-op2-stage` (accelerated rate), `thm:det-op2-volume` (repeated local
  volume), `lem:det-op2-repair` (safe continuation), `alg:det-op2` (pseudocode),
  and `thm:det-op2-total` (fully charged work).
  The original `proof-audit.pdf` contains sections “One continuation
  stage,” “The second energy and the cumulative work theorem,” and “A realizable
  local ledger and bounded arithmetic.” Original TeX is in both source archives.
  The portable package's `PROOF_TO_CODE.md` maps claims to code.
- **Next concrete action:** Independently review the standalone proof and
  design a matched objective-accuracy benchmark. The extracted portable
  package's 17 tests have already been rerun successfully during this save.
- **Stop/go test:** Require measured end-to-end time and scanned incidences
  at a common certified accuracy; a lower iteration count alone is insufficient.

## Verification

- **Source pointers checked:** FM26 v2, Theorems 4.3--4.4 and Proposition 4.7;
  WY26 v1, Theorems 1.2--1.3 and deterministic-solver remark; AESP Theorem 3.6
  and its discussion of the parameter R. Comparison recorded in `DISCUSSION.md`.
- **Focused build/checks run:** Original proof/code checks are retained in
  `VERIFICATION.md`. Repository-copy checks are recorded in `SAVE_VERIFICATION.md`.
- **Known gaps:** No claim of practical superiority, machine verification,
  weighted/general-seed theorem, or OP3 persistent inverse result.

## Repository handoff

- Provider-owned paths changed: none; executable code is a preserved archive.
- Shared paths changed: note registry and generated note-index row only.
- Assignment state: ready_for_review.
- No private exploration was sent to another task; this is a saved local handoff.
