# Direction status: incremental_active_set_sdd

Last reviewed: 2026-08-20

State: proved-open

## Exact question and contract

- **Question:** Can the Wei--Yang growing-active-set method reuse exact old-face
  state without repeated materialization or global boundary refresh on arbitrary
  graphs?
- **Model:** Map the shared lazy system to Wei--Yang's degree form by `bar_alpha = 2 alpha/(1+alpha)`, `x = D^(1/2) z`, with `rho` unchanged. For `M = D-(1-bar_alpha)A`, residue `r(z)=s-bar_alpha^(-1)Mz`, and exact restricted state `z[U]`, admit `v` when `r(z[U])_v > (lambda+kappa)d_v` (`main.tex:98-152`).
- **Accuracy namespace:** With `lambda=kappa=epsilon/2`, the exact path gate returns a deterministic ACL `epsilon`-approximation. With `lambda=rho` and `kappa <= min(rho,xi/bar_alpha)`, it returns RPPR objective gap at most `bar_alpha kappa <= xi` and ACL error `rho+kappa` (`main.tex:417-455`). These are source/native namespaces, not the repository's final `eps_ppr` convention.
- **Access and charged work:** Charge one word per materialized coordinate, degree work for every adjacency scan, all updates and violation queries, and one final output. The path algorithm costs `O(cvol(U_J)+d_next)`; the general interface costs `O(I(U_K)+cvol(U_K))` (`main.tex:51-56,361-415,471-501`).
- **Intended result:** A high-probability arbitrary-graph `Violations`/`Expand`/`Finalize` data structure with total `O_tilde(cvol(S*)/sqrt(alpha) polylog(1/(rho xi delta)))`; the stronger output-linear bound remains open (`main.tex:541-555`).

## Claim ledger

- **Source:** Wei--Yang arXiv:2608.16339v1 gives ACL work `O_tilde(1/epsilon^2)` and RPPR work `O_tilde(|S*| vol(S*))`, and explicitly leaves incremental reuse open (`main.tex:154-182,591-597`).
- **Proved here:** Exact block-Schur correction and energy telescoping; the endpoint-path materialization barrier; append-only path `LDL^T` gates plus one reverse materialization; and preservation of the source ACL/RPPR guarantees on paths (`main.tex:184-276,280-455`).
- **Conditional:** Any interface satisfying the source-safe error margins and charging all update/query/output work removes the round factor, with total `O(I(U_K)+cvol(U_K))` (`main.tex:471-517`).
- **Measured:** None.
- **Refuted:** An ordinary warm start followed by full active-matrix passes or full vector materialization does not remove repeated-prefix work; endpoint paths force quadratic writes in that representation (`main.tex:73-80,280-340`).
- **Open:** Graph-uniform implicit continuation on arbitrary cyclic graphs; energy telescoping alone does not pay for dense old-coordinate transport or repeated boundary-key refresh (`main.tex:519-560`).

## Central blocker

Support complete boundary-violation reporting under dense implicit Schur corrections without materializing the old solution or refreshing every boundary key. The next falsifiable target is `conj:aggregate`; every proposed oracle should first be tested on broad old-face transport and repeated boundary-key refresh (`main.tex:519-560,585-589`).

## Dependencies and reusable outputs

- Formal taxonomy dependencies: none.
- Source/shared prerequisites: the shared PageRank/RPPR model and the
  Wei--Yang 2026 source.
- Supplies to: `response_preconditioned_hybrid` (block correction and implicit interface), `local_solver_oracle_hierarchy` (path representation separation), and the controller's persistent-response track.

## Resume here

- Exact file/section/lemma: `main.tex:471-517`, `def:interface` and `thm:conditional-interface`; then `main.tex:519-555`, `conj:aggregate`.
- Next concrete action: Extend the scalar path record to one explicitly charged low-rank separator and determine whether all affected boundary keys can be located once rather than refreshed globally.
- Stop/go test: Go if every eliminated incidence, separator update, violation query, and final word is charged near-linearly in final exposed volume. Stop or qualify if dense transport or rekeying forces repeated-prefix work.

## Verification

- Source pointers checked: `README.md:1-23`; `main.tex:46-182,184-276,280-455,465-589`; `taxonomy.toml:131-138`; shared related-work/results/broadcast ledgers dated 2026-08-20.
- Focused build/checks run: No TeX source changed; repository `make note-audit` is the required post-edit check.
- Known gaps: `cvol` is now defined locally in the scope section, removing the
  dependence on `propagate_settle_framework` for the basic work unit. The short
  README still omits the alpha/variable mapping, native accuracy parameters,
  interface details, dependencies, and exact next lemma; this `STATUS.md`
  remains the operational resume card.
