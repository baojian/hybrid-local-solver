# Direction status: two_stage_revisited_20260906

Last reviewed: 2026-09-06
State: proved-open

## Exact question and contract

- **Question:** Which changes to the older two-stage attempts become provable
  using the newer randomized and deterministic RPPR results?
- **Model:** Finite connected simple unit graph, original positive degrees,
  local degree and adjacency access, no preprocessing. Point-source results
  and explicit sparse-source extensions are distinguished.
- **Accuracy namespace:** `eps_ppr` is normalized semantic PPR error;
  `eps_obj` is independent RPPR objective error; `eps_kkt` is the older
  note's normalized minimum-subgradient diagnostic. ACL residual claims
  require the explicitly stated separate certificates.
- **Access and charged work:** Input reads, degree replies, first and repeated
  incidences, source-key refreshes, scalar/tree operations, threshold reports,
  materialization, face construction, and output are all charged. Exact-real
  operations and separately rounded bounded arithmetic have separate proofs.
  Dense references and radial quotients are offline verification only.
- **Intended result:** Resumable proofs and reproducible audits of new
  deterministic and randomized two-stage constructions, with the unchanged
  old algorithms' open questions kept distinct.

## Claim ledger

- **Source:** Accelerated comparison identity from
  `deterministic_op2_20260905`; RPPR order, mass and bias facts; the exact
  face/residual contract of randomized threshold batching from
  `two_stage_point_source_aesp_cd`; the scoped ranked-SOR obstruction in
  `two_rung_direct_theory`.
- **Proved here:** Orthant-only cooling bank, moving-comparator signed flow,
  `44 sum 1/r` kinetic work, lazy reporter, direct OP1/OP2 completion,
  directed rounding with constant 60, and fixed degree pruning. General
  sparse sources have additive input work, including recovery of the
  original RPPR objective on an approximate support. Certified randomized
  faces admit a coarse GS handoff. A signed residual-excess potential gives
  a deterministic accelerated-prefix / coordinate-tail construction with
  exact incidence work `O((1+log(2/alpha))/(eps_ppr sqrt(alpha)))`.
  The separated-front graph limit and linear cascade also prove that no
  universal constant bounds the new ramp's error by its current regularizer.
  Separately, the ideal exact-inner AESP recurrence has unbounded normalized
  weighted residual mass over finite unit trees and stages at fixed alpha.
  Its proof does not cover the actual thresholded inner solver.
- **Measured:** The exact, sparse-state, rounded, interface and numerical
  checks are enumerated in `VERIFICATION.md` and `COVERAGE.json`. The new
  deterministic early-handoff audit has 1,096 actual runs, 1,025 nonempty
  tails, and 12 separately labelled external signed-tail witnesses.
  A later 512-run extension checks four alpha values that are not dyadic
  squares, with 438 nonempty tails and the additional endpoint/interfaces.
  The randomized SDD primitive itself is imported, not implemented or timed.
- **Refuted:** Intermediate monotonicity, lower order to PPR/current RPPR,
  nonnegative PPR residual, and every graph-uniform constant ramp-tracking
  bound for this particular recurrence. The asymptotic conclusion uses a
  proof beyond the finite counterexamples. It is not a work lower bound.
  Also refuted is an all-stage, graph-independent constant residual-mass
  bound for ideal exact-inner AESP; the thresholded implementation remains
  outside that obstruction's scope.
- **Conditional:** Applying the new tail potential to unchanged AESP yields
  an instance-wise handoff bound; an accelerated end-to-end AESP claim would
  still require an accelerated prefix-work theorem up to that certificate.
- **Open:** Independent proof review; practical comparisons under a common
  work contract; unchanged AESP/FISTA/SOR-specific locality claims. No
  unmodified-algorithm theorem follows from the new constructions.

## Central blocker

No missing lemma has been identified in the written new constructions or
in the separated-front obstruction. These are research proofs awaiting
independent review, not machine-checked theorems. Finite audits do not
replace their asymptotic arguments.

For the user's original AESP route, the remaining problem is still prefix
work. The new, falsifiable alternative to bounding `Lambda_J` is to reach
`sum_i sqrt(d_i)(|b-Qx|_i-alpha rho sqrt(d_i))_+ <= alpha theta`
with accelerated charged prefix work. The signed tail needs no lower-order
assumption at handoff. Its final clipping supplies lower RPPR order at
`eps_ppr/3` and nonnegative PPR residual, while meeting the semantic target.

Exact primal supports are nested; kinetic supports vary. Rounded primal
coordinates may disappear, and the charged stored history remains nested.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `deterministic_op2_20260905`,
  `two_rung_direct_theory`, `two_stage_point_source_aesp_cd`.
- **Context/provenance:** The three user-named older notes, the independent
  deterministic proof, and the active manuscript. They are not all formal
  imports. Existing manuscript changes were preserved; another task committed
  them as `7e1b4e77351b361e0c700ce3186c1534d2023f0e` during this session.
- **Reusable outputs:** `main.tex` and its sections, the matching dated audit
  directory, and the verification manifest. Start with
  `thm:revisit-deterministic-gs`, `lem:revisit-gap-to-excess`,
  `thm:revisit-cooling-bank`, `lem:revisit-weighted-flow`,
  `thm:revisit-volume`, `thm:revisit-general-rppr`,
  `thm:revisit-randomized-gs`, and `thm:revisit-front-limit`.
  The additional ideal-AESP obstruction is `thm:revisit-exact-aesp-mass`.

## Verification

See `VERIFICATION.md` for exact coverage, source-snapshot qualifications,
reproduction commands, repository-check failures and PDF inspection.
The all-seed atlas audit through seven vertices passed all 27,120 cases on
995 connected graph representatives and checked 2,461,140 exact steps.
The 1,096-case deterministic early-handoff extension and its 12 signed-tail
witnesses also passed, as did the later 512-case extension to four alpha
values that are not dyadic squares. The corresponding directed-rounding
sweep passed 1,114 cases and four implicit stars.

The focused audit runner passed all 12 registered fast audits. A dedicated
deterministic-handoff run checks the strengthened output order
and the corrected alpha=1 and zero-output branches. Focused style checks
passed. The latest repository
reproduction check has 231 passes and the same three pre-existing failures
(one old notation alias and two oversized note-source checks). Full lint
has two unrelated pre-existing findings. The agent-boundary audit passed.

## Resume here

The investigation and all planned audits are complete. Final review was
2026-09-06 09:06:34 UTC, after 6 hours, 16 minutes, 45 seconds from the
02:49:49 UTC start. The requested six-hour minimum was met.

Start independent review with `lem:revisit-signed-excess`,
`lem:revisit-gap-to-excess`, and `thm:revisit-deterministic-gs`, then trace
the prefix back to the cooling bank and moving-flow lemma. Review the
two graph-limit arguments separately; neither is needed by the positive
algorithm theorem.

The next AESP-specific falsifiable target is accelerated charged prefix
work up to the observable excess certificate. Test the actual thresholded
inner policy; do not substitute the ideal exact-inner recurrence or infer
its locality from a bounded ordinary residual mass. Preserve the active
paper and older notes during that follow-up.

## Repository handoff

- **Provider-owned paths changed:** none. New proof-audit modules are under
  `experiments/proof_audits/two_stage_revisited_20260906/`.
- **Shared paths changed:** the note README/registry, the proof-audit
  README/registry, and the runner's date-provenance support.
- **Supplies to:** the three older hybrid directions and the newer
  deterministic/randomized RPPR proofs, after independent review.
- **Accepted shared snapshots:** the older controller broadcast is a frozen
  accepted-review record. This dated note is indexed for review and does
  not replace that snapshot or announce a new coordinated round.
- **Assignment state:** ready_for_review.
