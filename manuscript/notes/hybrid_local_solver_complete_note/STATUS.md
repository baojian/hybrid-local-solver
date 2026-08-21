# Direction status: hybrid_local_solver_complete_note

Last reviewed: 2026-08-20

State: synthesis

## Exact question and contract

- **Question:** Can the archived safeguarded RPPR theorem attempt pay for
  accelerated warmup and restarts locally, and which proved obstructions delimit
  that attempt?
- **Model:** Source-aligned RPPR with `0<alpha<1/2`, orthant objective `F_rho^+`, weight `w=D^(1/2)1`, and note-scoped KKT residual `kappa_rho(x)=b-Qx-alpha rho w`. The proposed algorithm accelerates at `bar_rho=(1+sqrt(alpha))rho`, retracts to a certified lower point, discards momentum, and runs an `omega=1` coordinate tail (`sections/problem.tex:3-59`; `sections/hybrid.tex:1-24`).
- **Accuracy namespace:** `rho` is a regularization/locality scale, not identified with global `eps_ppr`. The tail stops on the note-scoped KKT threshold `zeta=alpha rho`; the persistent-support lower bound asks `||D^(-1/2)(x-x*_rho)||_infinity <= rho` (and also treats a stated objective gap) (`sections/convergence.tex:13-86`; `sections/lower_bound.tex:105-121`).
- **Access and charged work:** Scanning coordinate `i` costs `d_i`; a batched active set costs `vol(S)` and trajectory work is `sum_t vol(S_t)` (`sections/problem.tex:61-77`). The intended hybrid target is `O_tilde(1/(rho sqrt(alpha)))` (`sections/scope.tex:3-14`).
- **Intended result:** Safeguarded accelerated epochs plus a monotone lower shadow with `Work_total = O_tilde(1/(rho sqrt(alpha)) + N_rst/rho)`, followed by a theorem paying for `N_rst` or exposing it instance-adaptively (`sections/open.tex:35-72`).

## Claim ledger

- **Source:** APPR, locally evolving sets, Catalyst/AESP, sparse ASPR, and the classical-FISTA locality obstruction are used with their native models (`sections/frameworks.tex:1-59`).
- **Proved here:** One-sided tail and over-regularized handoff; activation-tax and its exact face defect; lower-certificate Euclidean centers; cumulative active-volume/flux identity; exact radial obstacle recurrence and limiting period-11 wave; and `Omega(1/(rho sqrt(alpha)))` for persistent-support one-hop methods (`sections/scope.tex:75-99`, with proof files named there).
- **Conditional:** Bounded-core, controlled-face, and flux-dependent hybrid work bounds (`sections/euclidean.tex:92-135`; `sections/flux.tex:121-154`).
- **Measured:** Finite rooted-tree flux values are computational observations for the exact radial recurrence, not an asymptotic proof (`sections/tree_wave.tex:80-135,214-237`).
- **Refuted:** Uniform exponent-two matched-Bregman acceleration; using the unguarded `Phi_T=O(alpha T)` flux law as a graph-uniform proof hypothesis (`sections/bregman.tex:136-241`; `sections/flux.tex:156-192`).
- **Open:** Unconditional graph-uniform warmup, restart amortization, lower-shadow accuracy, finite-tree excitation transfer, moving-frontier lower bounds, and residual reconciliation (`sections/open.tex:26-105`).

## Central blocker

Prove restart amortization for the two-state safeguarded algorithm while preserving lower-shadow accuracy; independently finish finite-tree excitation if a formal zero-start counterexample is needed. The warmup must be charged locally rather than inferred from convergence or final support (`sections/open.tex:35-105`).

## Dependencies and reusable outputs

- Formal taxonomy dependencies: `hybrid_aesp_locsor`.
- Source/shared prerequisites: the frameworks recorded in
  `sections/frameworks.tex`.
- Supplies to: The controller's historical proof ledger, safeguarded-acceleration directions, oracle-lower-bound scoping, and any synthesis that cites the tail, face-change defect, or tree-wave obstruction.
- Ownership boundary: This directory owns the proof-bearing consolidated theorem
  attempt, derivations, counterexamples, and historical archive.
  `hybrid_local_solver_synthesis` may integrate its conclusions and gaps but
  cites this note rather than duplicating its proofs.

## Resume here

- Exact file/section/lemma: `sections/open.tex:35-105`, especially Restart amortization and Lower-shadow accuracy; for the obstruction route, `sections/tree_wave.tex:214-237`.
- Next concrete action: State one epoch potential that pays a wave-triggered restart by objective decrease or newly certified KKT slack, and prove the lower shadow retains the prior `1/sqrt(alpha)` progress.
- Stop/go test: Go if the restart charge yields the displayed `N_rst/rho` ledger without assuming monotone accelerated support. Stop or narrow if restart count merely renames the unknown number of face phases.

## Verification

- Source pointers checked: `README.md:1-23`; `main.tex:14-72`; `sections/scope.tex`, `problem.tex`, `frameworks.tex`, `convergence.tex`, `bregman.tex`, `euclidean.tex`, `flux.tex`, `lower_bound.tex`, `tree_wave.tex`, and `open.tex`; `taxonomy.toml:61-68`.
- Focused build/checks run: No TeX source changed; repository `make note-audit` is the required post-edit check.
- Known gaps: The abstract now matches the precise ledger: unconditional
  inertial-warmup locality is unproved, the proposed uniform-flux route is
  invalid, and zero-start finite-tree asymptotic transfer remains open
  (`sections/scope.tex:93-96`; `sections/tree_wave.tex:227-237`). The
  finite-tree table still has no checked-in generator/data record or
  commit/dirty-tree metadata. The README is a good history summary but omits
  the exact model, target accuracy, central resume lemma, dependencies, and
  this important narrowing.
