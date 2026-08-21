# Direction status: aesp_cd_l1_rppr

Last reviewed: 2026-08-21
State: proved-open

## Exact question and contract

- **Question:** Can exact proximal coordinate solves inside AESP achieve the
  graph-uniform product scale after every support correction and rekey is
  charged?
- **Model:** Shared RPPR objective F_rho=f+alpha*rho*||D^(1/2)x||_1 with alpha in (0,1/2), wrapped in Catalyst/AESP shifted subproblems with kappa_A=1-2*alpha and solved by exact proximal coordinate updates.
- **Accuracy namespace:** The terminal requirement is R_KKT,rho(x)/alpha <= eps_kkt. eps_kkt is a composite KKT diagnostic, not eps_ppr, eps_obj, or rho.
- **Access and charged work:** Updating coordinate i and rekeying affected neighbors costs d_i; all envelope growth, retractions, KKT scans, and repeated updates are charged.
- **Intended result:** An implementable, oracle-free O_tilde(1/(rho*sqrt(alpha))) local-work theorem.

## Claim ledger

- **Source:** RPPR support/KKT facts and the Catalyst/AESP scaffold are source ingredients, separated in the source map and the opening formulation section of `main.tex`.
- **Proved here:** Weighted KKT contraction and solution certificate (`lem:aesp-cd-kkt-error`, `thm:aesp-cd-mass`, and `thm:aesp-cd-stieltjes`); the threshold inner-oracle interface (`thm:aesp-cd-inner-work` and `thm:aesp-cd-relative-oracle`); safe retraction, safe lower centers, order-safe support, and the safeguarded outer ledger (`lem:aesp-cd-lower-retraction`, `thm:aesp-cd-safe-center`, and `thm:aesp-cd-safe-outer-ledger`); the exact defect/collapse and multiplicative log-inflation ledger (`lem:aesp-cd-estimate-defect` and `lem:aesp-cd-multiplicative-ledger`); a per-round upper bound on `log max(1,gamma_t)` using normalized collateral clipping, which may overcharge a benign collateral round and has the exact collapse amplitude for `t>=2` (`lem:aesp-cd-collateral-charge`); an exact single-edge family with singleton support, one full correction every other stage, raw correction count N_T=floor((T-1)/2), and zero normalized log-inflation (`prop:aesp-cd-singleton-corrections`); and an exact full-support single-edge family whose stage-two harmful collateral charge is Theta(q) while both its same-step and prefix Euclidean log-progress are Theta(q^2) (`prop:aesp-cd-euclidean-packing-fails`).
- **Conditional:** The final accelerated work bound holds if the positive cumulative normalized log-inflation is controlled at accelerated scale; the local certified-envelope solve itself is already proved by `thm:aesp-cd-safe-center`.
- **Measured:** None; this note is proof/algorithm analysis.
- **Refuted:** Raw objective gap does not control KKT error at the l1 kink (`lem:aesp-cd-center-cancel`); pointwise momentum nonexpansion fails on P3 (`prop:aesp-cd-momentum-expansion`); the number of nonzero correction calls cannot be charged only to support additions or bounded independently of terminal accuracy, even on a singleton support (`prop:aesp-cd-singleton-corrections`); and no `o(1/q)` coefficient (in particular, no alpha-independent or polylogarithmic one) packs `C_t^col` solely by the monotone Euclidean log-error decrease, either pointwise or on the first two-stage prefix (`prop:aesp-cd-euclidean-packing-fails`). The singleton corrections are benign for I_T, while the Euclidean-packing counterexample has a positive defect; neither refutes every cumulative normalized-inflation potential.
- **Open:** Pack the cumulative normalized collateral charges from `eq:aesp-cd-collateral-cumulative` at accelerated scale using genuinely multistep collapse information or another potential, or derive a locally checkable one-sided surrogate. The proved charge is a posteriori because `B_t^col` uses the unknown optimum; it is not a local certificate. Raw correction counting and Euclidean log-error normalization are both too coarse.

## Central blocker

The remaining lemma is not safe-center preservation, a raw correction count, a per-round positive-inflation estimate, or a direct normalization by Euclidean log-progress: all four are settled at their stated scopes. It is a cumulative packing bound for the normalized collateral fractions in `eq:aesp-cd-collateral-cumulative` using additional collapse history or a different potential, while still charging every correction/rekey call separately.

## Dependencies and reusable outputs

- Formal taxonomy dependencies: none.
- Source/shared prerequisites: shared RPPR support/KKT facts and
  Catalyst/AESP source machinery.
- Supplies to: volume_gated_acceleration, hybrid_local_solver_synthesis, response_preconditioned_hybrid, and any direction needing safe lower centers or local KKT admission.

## Resume here

- Exact file/section/lemma: start at `lem:aesp-cd-collateral-charge` and `prop:aesp-cd-euclidean-packing-fails`; compare the singleton family's zero charge with the full-support family's Theta(q) harmful charge and only Theta(q^2) Euclidean progress.
- Next concrete action: Test a multiscale potential that retains the exact collapse ratio across several stages, or upper-bound the unknown collateral set by a locally checkable one-sided quantity. Do not normalize the existing Euclidean telescope into a logarithm and do not replace the fractions by the number of nonzero corrections.
- Stop/go test: Go if `sum_t C_t^col` is bounded at accelerated scale while all correction/rekey work remains explicit, or if a computable surrogate provably dominates it with such a budget; stop if the argument treats the a posteriori charge as locally computable, uses an alpha-independent Euclidean log-error charge contradicted by `prop:aesp-cd-euclidean-packing-fails`, counts support additions, treats benign corrections as harmful, restarts Catalyst, or scans the full envelope per correction.

## Verification

- Source pointers checked: README.md, taxonomy.toml, main.tex, docs/research_notes.md, docs/literature/acceleration.md, and the shared ledgers were cross-read on 2026-08-21.
- Focused build/checks run: Round 002 checked the collateral inequality numerically on five path regimes. An independent read-only audit verified the factors, index range, singleton/P3 consequences, and exact-collapse formula, and required the benign-overcharge and `t>=2` wording now used here. Round 003 symbolically checked the exact two-vertex recurrence and all displayed limits in `prop:aesp-cd-euclidean-packing-fails`; a second independent audit verified the KKT solution, retraction schedule, collateral/defect signs, all four limits, and the `o(1/q)` scope. The direction was rebuilt and the workspace inventory and diff checks were rerun on 2026-08-21.
- Known gaps: The taxonomy, manifest, research ledger, and acceleration
  literature note now name correction log-inflation as the live target.
  The README has also been reconciled so its `V_exp` paragraph is historical
  setup rather than a second live blocker. Read `_shared/results/README.md` as
  saying continuation cost is open, not safe-center correctness. The new
  collateral charge is analytical and uses the unknown optimum. The direct
  Euclidean log-error packing is now refuted, but cumulative packing by a
  different potential and a locally checkable surrogate remain open.
