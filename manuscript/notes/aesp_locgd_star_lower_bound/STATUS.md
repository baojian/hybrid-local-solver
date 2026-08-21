# Direction status: aesp_locgd_star_lower_bound

Last reviewed: 2026-08-20
State: proved-open

## Exact question and contract

- **Question:** What is the exact center-star cost of literal batched
  AESP--LocGD, and can its lower bound extend to a precisely wider inner-map
  class?
- **Model:** The literal source AESP-PPR schedule, momentum, and activation threshold, with batched LocGD inner calls, on center-seeded stars; alpha is in (0,1/2).
- **Accuracy namespace:** eps_ppr means ||D^(-1)(pi_hat-pi)||_infinity in the note's shared normalization.
- **Access and charged work:** Each outer call charges the degree volume of its active set; empty calls have zero source work, and total work is cumulative active volume.
- **Intended result:** Determine the exact star cost of literal batched AESP-LocGD and whether it already matches or exceeds the desired product scale.

## Claim ledger

- **Source:** The AESP parameter schedule, threshold rule, and LocGD map are source facts recorded at main.tex:58-83.
- **Proved here:** Symmetry reduces the star dynamics to a scalar batched minimum (main.tex:177-269); an unconditional activation/error/Green-function argument (372-581) yields the literal-star lower bound Omega(1/(sqrt(alpha)*eps_ppr)) in its stated regime (618-677), with a matching incident-edge budget calculation (707-726) and an augmented outer-delay statement (732-766).
- **Conditional:** The earlier residual-cone proof route is valid only under an extra cone invariant (main.tex:271-354); the final proof does not need it.
- **Measured:** None.
- **Refuted:** Star symmetry alone does not imply the residual cone used by the abandoned proof route (main.tex:271-354).
- **Open:** A multiscale spider/star-of-stars/lollipop that forces transient volume asymptotically larger than output, or an extension from batched LocGD to sequential LocAPPR or a wider inner-oracle class (main.tex:768-803).

## Central blocker

The present lower bound is algorithm-specific and already tight at the product scale. The next falsifiable target must create a genuine transient-volume separation, not re-prove the center-star output cost.

## Dependencies and reusable outputs

- Formal taxonomy dependencies: none.
- Source/shared prerequisites: the exact source AESP schedule and shared PPR
  certificate.
- Supplies to: local_solver_oracle_hierarchy as an iterative-method lower-bound rung, and stress tests for hybrid_aesp_locsor and other early-locality conjectures.

## Resume here

- Exact file/section/lemma: main.tex:768-803, “Refinements and next falsifiable targets.”
- Next concrete action: Specify one multiscale graph family and derive its literal activation chronology before attempting an asymptotic work bound.
- Stop/go test: Go only if the construction separates cumulative active volume from required output volume; stop if it merely reproduces the center-star Omega(1/(sqrt(alpha)*eps_ppr)) cost.

## Verification

- Source pointers checked: README.md, taxonomy.toml, main.tex proof branches, AESP literature notes, and shared ledgers were cross-read on 2026-08-20.
- Focused build/checks run: Manual claim and line-pointer audit completed; make note-audit passed on 2026-08-20 (18 notes across 5 tracks).
- Known gaps: No material README/main claim-status inconsistency was found. taxonomy.toml's next_target is a scope guard rather than the current constructive target. Never generalize this result from literal batched LocGD to arbitrary AESP inners, hybrids, or persistent-response solvers.
