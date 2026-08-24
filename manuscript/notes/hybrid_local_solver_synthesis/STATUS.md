# Direction status: hybrid_local_solver_synthesis

Last reviewed: 2026-08-20

State: synthesis

## Exact question and contract

- **Question:** How do the PPR and RPPR directions fit together, which gaps block
  promotion, and where should the controller route the next proof or experiment?
- **Model:** Unregularized track: connected graph, single seed, `0<alpha<1/2`, source-aligned `Q`, AESP burn-in, then momentum-free LocSOR. RPPR track: shared composite `F_rho`, finite Catalyst burn-in, then momentum-free proximal cleanup (`sections/02_problem_and_normalizations.tex:4-10`; `sections/04_hybrid_algorithm.tex:1-33`; `sections/08a_composite_rppr_hybrid.tex`).
- **Accuracy namespace:** PPR uses `||D^(-1/2) grad f(x)||_infinity < alpha eps_ppr`, implying degree-normalized solution error `< eps_ppr`. RPPR uses fixed-point residual `R_fp,alpha,rho`; solution error is at most `||R_fp||/alpha`, so the stopping threshold is `alpha eps_sol` (`sections/02_problem_and_normalizations.tex:12-38`; `sections/08a_composite_rppr_hybrid.tex:100-132`).
- **Access and charged work:** Charge `d_u` for every coordinate adjacency scan, `vol(S_k)` per simultaneous active-set iteration, and `sum_k vol(S_t^(k))` for AESP inner work; wall time is secondary (`sections/02_problem_and_normalizations.tex:88-107`). The `R`-parameterized black-box result is inner-plus-tail only and charges outer initialization separately (`sections/06a_black_box_tradeoff.tex`; `sections/C_claim_audit.tex:29-35`).
- **Intended result:** Unregularized `O_tilde(1/(sqrt(alpha) eps_ppr))` end-to-end work and RPPR `O_tilde(1/(rho sqrt(alpha)))` work, each with every burn-in/cleanup scan charged (`sections/01_scope_and_status.tex:54-77`).

## Claim ledger

- **Source:** Locally evolving sets, AESP, Catalyst, and classical-FISTA RPPR results are imported with native assumptions (`sections/01_scope_and_status.tex:4-16`; `sections/03_source_frameworks.tex`).
- **Proved here:** Finite-handoff AESP--LocSOR convergence; objective-gap tail and master handoff inequality; the run-dependent `O(R/(alpha^(3/4) eps_ppr))` inner-plus-tail tradeoff; corrected one-coordinate SOR range; RPPR proximal contraction/residual certificate and convergence after any finite Catalyst handoff (`sections/01_scope_and_status.tex:91-128`).
- **Conditional:** The full PPR product bound requires early locality `Lambda_t=O(1/eps_ppr)` or the displayed confinement/no-percolation envelope; no graph-uniform bound on `R` is proved (`sections/01_scope_and_status.tex:104-117,141-148`).
- **Measured:** Bell-shaped active volumes and early AESP advantage are empirical motivation only; this note adds no graph-uniform measured claim (`sections/C_claim_audit.tex:100-103`).
- **Refuted:** Full-range one-coordinate SOR mass contraction; support volume alone implies AESP locality; Catalyst compatibility alone implies local RPPR work; and zero-start RPPR support monotonicity survives an arbitrary Catalyst handoff (`sections/C_claim_audit.tex:15-61,83-87`).
- **Open:** Prove or refute FIFO early AESP locality, preferably via the boundary-sensitive target, and prove arbitrary-warm-start RPPR locality (`sections/11_open_problems.tex:10-39,106-121`).

## Central blocker

Primary: settle `prob:early-locality` for the current FIFO AESP trace or give a counterexample. Secondary and independent: establish a locally charged RPPR cleanup from a signed/overshooting Catalyst point. These must remain separate accuracy/work theorems (`sections/11_open_problems.tex:10-39,106-121`).

## Dependencies and reusable outputs

- Formal registry dependencies: `hybrid_aesp_locsor` and
  `aesp_cd_l1_rppr`.
- Supplies to: The broad controller synthesis, active-manuscript claim audit, experimental/TB design, and downstream work using the handoff, SOR correction, or RPPR fixed-point certificate.
- Ownership boundary: This directory owns the controller-facing integration,
  comparison, promotion-gate, and gap map. Proof-bearing derivations and archive
  history remain with `hybrid_local_solver_complete_note` or the focused
  direction cited as proof owner.

## Resume here

- Exact file/section/lemma: `sections/11_open_problems.tex:10-39`, Problem `prob:early-locality`; for RPPR, `sections/11_open_problems.tex:106-121` and `sections/08a_composite_rppr_hybrid.tex:200-225`.
- Next concrete action: Run the FIFO early-locality inequality against one adversarial graph family and either prove a queue-inflation bound relative to a certified envelope or record a counterexample with fully charged active-volume work.
- Stop/go test: Go to an end-to-end PPR theorem only if burn-in initialization and every inner active volume are charged; go to RPPR work only if warm-start support/boundary scans are bounded. Convergence alone is not sufficient.

## Verification

- Source pointers checked: `README.md`; `main.tex`; the listed section files; and the note's entry in `registry.toml`.
- Focused build/checks run: No TeX source changed; repository `make note-audit` is the required post-edit check.
- Known gaps: The main status table now says the RPPR work theorem remains
  open and Catalyst compatibility alone is insufficient, consistent with
  `sections/C_claim_audit.tex:56-61`. The README also qualifies the
  `O(R/(alpha^(3/4) epsilon))` result as inner-plus-tail work. This broad
  synthesis integrates `hybrid_local_solver_complete_note` as a proof-bearing
  source but does not own or duplicate that note's derivations. Its README
  remains high-level rather than a substitute for this resume card.
