# Direction status: aspr23_bound_audit

Last reviewed: 2026-08-20
State: proved-open

## Exact question and contract

- **Question:** Is the published literal COLT-2023 ASPR proof correct after all
  restricted-solve and discovery work is charged, and is its repeated-prefix
  factor intrinsic to that algorithm?
- **Model:** Exact-arithmetic nonnegative Stieltjes quadratic programming; for RPPR, H=Q, strong convexity alpha, smoothness 1, and the literal COLT-2023 ASPR restricted-APGD/retraction/discovery algorithm.
- **Accuracy namespace:** eps_obj is objective gap for each restricted solve. It is not eps_ppr, eps_appr, or a KKT residual.
- **Access and charged work:** One restricted APGD step charges stored restricted-Hessian nonzeros; discovery charges incident nonzeros. Repeated work on old active prefixes is charged.
- **Intended result:** Audit the published correctness and complexity proof, repair it where possible, and decide whether the extra optimal-support factor is intrinsic to literal ASPR.

## Claim ledger

- **Source:** The ASPR algorithm and published upper-bound ingredients are restated with source pointers in main.tex:75-86.
- **Proved here:** Three proof repairs and the support/objective theorem (main.tex:235-351); exact endpoint-path calls and one-layer discovery (main.tex:535-689); lower bounds Omega(s^2/sqrt(alpha)) for restricted solves and Omega(s^2) for fresh discovery (main.tex:691-752); and a factor-s separation from the support-free advertised scale (main.tex:754-861).
- **Conditional:** Linear memory requires sorted adjacency lists and a streaming merge implementation (main.tex:374-386).
- **Measured:** The source paper's reported experiments favor its default ASPR over its included FISTA/ISTA baselines and report CASPR fastest; this is source measurement, not a project theorem (main.tex:391-419).
- **Refuted:** Literal repeated restricted solves are not harmless: the endpoint path rules out a support-free interpretation of the default ASPR bound. The official periodic-discovery and retraction arguments also fail as written (main.tex:421-529).
- **Open:** A broader lower bound against stronger local-response oracles, and an expanding-face accelerated method that avoids repeated-prefix work (main.tex:917-966).

## Central blocker

The audit itself is closed. The successor falsifiable target is an expanding-face estimate-sequence lemma that preserves a certified old-face state across support additions and charges only newly admitted volume; otherwise seek an oracle-separated lower bound.

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Source/shared prerequisites: the shared RPPR/Stieltjes model and the cited
  COLT-2023 source.
- Supplies to: local_solver_oracle_hierarchy (algorithm-specific lower-bound rung), and the repeated-prefix warnings used by volume_gated_acceleration and aesp_cd_l1_rppr.

## Resume here

- Exact file/section/lemma: main.tex, “What is and is not tight” and “Consequences and next targets,” especially lines 917-966.
- Next concrete action: State the admissible old-face response primitive and prove or falsify the one-expansion amortization inequality there.
- Stop/go test: Go only if the proof charges every old-face response application and new adjacency exposure; stop if it silently assumes the future support or a free restricted solve.

## Verification

- Source pointers checked: README.md, registry.toml, main.tex status table/proofs, shared problem/results ledgers, and docs/literature/acceleration.md were cross-read on 2026-08-20.
- Focused build/checks run: Manual claim and line-pointer audit completed; make note-audit passed on 2026-08-20 (18 notes across 5 tracks).
- Known gaps: No material README/main claim-status inconsistency was found. Do not propagate the endpoint-path bound as a lower bound for all local solvers, or the source plots as evidence that ASPR is universally slow.
