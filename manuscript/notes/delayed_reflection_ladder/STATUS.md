# Direction status: delayed_reflection_ladder

Last reviewed: 2026-08-20
State: proved-open

## Exact question and contract

- **Question:** Can alpha-scaled delayed reflection and exact/certified response
  operations obtain product-scale local work, and what response reporter is
  still needed on arbitrary large cyclic cores?
- **Model:** The note mixes two explicitly separated objects: the shared
  unregularized PageRank quadratic for SOR/reflection, and single-seed RPPR for
  support-safe KKT homotopies and response solvers.
- **Accuracy namespace:** Unregularized sections use
  `||D^(-1/2)(b - Q x)||_infinity <= alpha * eps_ppr`. RPPR sections use
  regularization `rho` and `vol(S*(rho)) <= 1/rho`; no conversion between these
  namespaces is asserted (`main.tex:163-178`).
- **Access and charged work:** Default cost is adjacency degree-volume,
  including repeated scans. Elimination, fill, factor/response updates,
  boundary reports, sketches, checkpoints, and output must also be charged.
  Exact cleanup costs `O(vol(S))` on forests and
  `O((w+1)^2 vol(S))` under a supplied width-`w` ordering.
- **Intended result:** Prove exact/product-scale solvers on structural classes
  and isolate the weakest missing arbitrary-core finite-band response
  interface; no universal local-oracle optimality claim is made.

## Claim ledger

- **Source:** Measured exact-rung behavior comes from
  `rlsor_terminal_exact_rung`; source RPPR/FISTA conventions come from
  Fountoulakis-Martinez-Rubio; adaptive restart and AESP are motivation only
  (`main.tex:186-189,348-355`).
- **Proved here:** Exact reflection/base algebra and block debt cleanup
  (`main.tex:357-846`); output-sensitive response solvers for paths, trees,
  cycles, bounded blocks, equitable quotients, and thin radial structures
  (`main.tex:853-2479`); arbitrary-graph exact support-safe gate correctness
  (`main.tex:2570-2634`); finite-band intervals, response-energy packing,
  terminal-Schur diagonal-loss accounting, Chebyshev full checkpoints, and
  frontier whitening (`main.tex:2892-3508`).
- **Conditional:** The general unregularized matching-scale theorem assumes
  `O(1)` scans of each certified region per alpha-scaled rung and a charged
  width-`w` ordering (`main.tex:3617-3653`). An end-to-end PPR result also needs
  an explicit RPPR-to-PPR accuracy conversion when RPPR is used as a surrogate.
- **Measured:** No new campaign is run here; empirical claims are imported and
  remain measured.
- **Refuted:** Fixed ladder bases cannot preserve the no-reactivation window as
  `alpha -> 0`; self-reflection debt alone misses larger neighbor backflow
  (`main.tex:429-685`). The persistent-support spider charge is not universal
  under directed elimination (`main.tex:1445-1468`), and generic accelerated
  objective contraction fails on `P3` (`main.tex:2803-2821`).
- **Open:** Online completeness between geometric checkpoints on high-cut-rank
  nonequitable cyclic cores: the companion response note now supplies a
  product-scale fixed-face aggregate debt flush, while its singleton-path
  proposition refutes pure geometric sleep for the literal gate. An
  output-sensitive partial flush or a separately proved safe trace remains
  necessary. Unregularized threshold progress and `eps_ppr` volume
  confinement also remain open (the discussion following
  `prop:positive-resolvent-rung-ladder` and the final boundary statement).

## Central blocker

Build an output-sensitive partial flush for a high-rank large cyclic core with
no bounded-block, equitable-quotient, or thin-radial structure, or prove a
different support-safe response trace. The fixed-face aggregate flush is
already product-scale and pure geometric sleep is refuted; the reporter must
locate every required crossing without invoking a full flush or scanning the
full boundary after each light update.

## Dependencies and reusable outputs

- **Formal taxonomy dependencies:** `rlsor_terminal_exact_rung`.
- **Context/provenance:** `propagate_settle_framework` and
  `aesp_cd_l1_rppr` supply adjacent support/gate context.
  `response_preconditioned_hybrid` is the companion continuation that proves
  the low-cut-rank closure and comb obstruction; those are not local proofs or
  reverse formal edges here (`main.tex:3493-3498`).
- **Supplies to:** `adaptive_revisit_control`, `two_rung_direct_theory`,
  `propagate_settle_framework`, and the response-preconditioned program through
  structured exact responses, gate correctness, and checkpoint machinery.

## Resume here

- **Exact pointer:** Proposition `prop:positive-resolvent-rung-ladder`, its
  following checkpoint discussion, and the final boundary statement in
  `main.tex`; companion Theorem `thm:aggregate-chebyshev-debt-flush` and
  Corollary `cor:geometric-aggregate-debt-flush` in
  `response_preconditioned_hybrid/main.tex`.
- **Next action:** Instantiate one target-side output-sensitive partial flush
  between full checkpoints, or a different proved support-safe trace, and give
  its complete exposure/update/query ledger. Use the companion singleton-path
  obstruction as the regression case against pure geometric sleep.
- **Stop/go test:** Continue only if intervening reporting is packed by
  crossings; stop any schedule requiring one product-scale flush per light
  admission.

## Verification

- **Source pointers checked:** Required context/conventions; RPPR,
  adaptive-restart, AESP, and dynamic-Schur literature notes; README, full claim
  ledger, gate theorem, checkpoint additions, and open-target sections.
- **Checks last run:** Focused LaTeX build passed on 2026-08-21 (51 pages), as
  did `make note-audit`, `git diff --check`, repository lint, and all 182 tests;
  tests emitted only the known temporary-directory cleanup warnings.
- **Known gaps:** The fixed-face aggregate flush and singleton-path geometric-
  sleep obstruction are proved in the companion response note, not duplicated
  locally. This note's remaining arbitrary-core statement is intentionally
  limited to partial reporting or a different safe trace; no graph-uniform
  end-to-end theorem or RPPR-to-PPR conversion is claimed.
