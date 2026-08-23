# Direction status: aesp_cd_l1_rppr

Last reviewed: 2026-08-23
State: proved-open

## Exact question and contract

- **Question:** Can the actual finite-inner safeguarded recurrence satisfy a
  net accelerated exponent after every residual, retraction, rekey, and
  terminal-gate charge is included?
- **Model:** Shared RPPR objective F_rho=f+alpha*rho*||D^(1/2)x||_1 on the full range 0<alpha<=1.  The shifted Catalyst/AESP analysis uses alpha<1/2 and kappa_A=1-2*alpha (the frozen accelerated arm uses alpha<1/4); the unshifted zero-start fallback covers 1/4<=alpha<=1.
- **Accuracy namespace:** The terminal requirement is R_KKT,rho(x)/alpha <= eps_kkt. eps_kkt is a composite KKT diagnostic, not eps_ppr, eps_obj, or rho.
- **Access and charged work:** Updating coordinate i and rekeying affected neighbors costs d_i; all envelope growth, retractions, KKT scans, and repeated updates are charged.
- **Intended result:** An implementable, oracle-free O_tilde(1/(rho*sqrt(alpha))) local-work theorem.

## Claim ledger

- **Source:** RPPR support/KKT facts and the Catalyst/AESP scaffold are source ingredients, separated in the source map and the opening formulation section of `main.tex`.
- **Proved here:** Weighted KKT contraction and solution certificate (`lem:aesp-cd-kkt-error`, `thm:aesp-cd-mass`, and `thm:aesp-cd-stieltjes`); the relative inner-oracle interface (`thm:aesp-cd-relative-oracle`); safe retraction, order-safe support, and the exact safeguarded outer ledger (`lem:aesp-cd-lower-retraction`, `thm:aesp-cd-safe-center`, and `thm:aesp-cd-safe-outer-ledger`); the exact defect and log-inflation ledgers (`lem:aesp-cd-estimate-defect` and `lem:aesp-cd-multiplicative-ledger`); the collateral-clipping upper bound (`lem:aesp-cd-collateral-charge`); the singleton correction-count obstruction (`prop:aesp-cd-singleton-corrections`); the Euclidean-normalization obstruction (`prop:aesp-cd-euclidean-packing-fails`); the abstract scalar-ledger obstruction (`prop:aesp-cd-ledger-only-insufficient`); and the finite `P4`/`P7` exact traces.  Round 023 adds the exact fixed-`P4` invariant cone (`prop:aesp-cd-p4-infinite-inflation`), finite-inner residual identities (`lem:aesp-cd-finite-inner-identities`), the scalar C2 residual obstruction (`prop:aesp-cd-c2-residual-stop`), and dual C2-plus-absolute polish (`cor:aesp-cd-dual-inner-stop`).  Round 024 proves exact support-entry discontinuity and sharp fixed-support factor `1+1/alpha` for the raw lower retraction (`prop:aesp-cd-retraction-shadowing-stop`), exact separation of full corrections plus a residual-only adjacent finite bound (`lem:aesp-cd-full-correction-separation`), and a direct finite-error accelerated gate/vector on the a-posteriori structural class `theta_A>=c0*q` (`thm:aesp-cd-high-dirichlet-branch`).  Round 025 proves that actual support entries are shielded by the previous finite end residual (`lem:aesp-cd-support-entry-shield`), bounds finite-created same-state correction excess one-sidedly by the C2-plus-absolute polish (`lem:aesp-cd-one-sided-correction-excess`), gives the affordable pre-gate entry-inflation ledger (`cor:aesp-cd-entry-inflation-ledger`), and identifies the exact local two-stage post-full high-pass filter and its mixed-mode `K8` limit (`prop:aesp-cd-post-full-high-pass`).  Round 026 gives the actual-finite persistent-controller L1 and windowed square-energy telescopes (`lem:aesp-cd-persistent-square-ledger`), proves separate windowed `Q`-energy bounds for the common correction and surviving momentum (`lem:aesp-cd-truncation-q-energy`), realizes the mixed event as the exact dense-seed word `N N P0 F N^infinity` (`prop:aesp-cd-k8-reachable-pulse`), and gives the small-`q` reachable raw-bank separation (`prop:aesp-cd-k8-q-bank-stop`).  Round 027 proves the exact actual-finite lagged Euclidean reserve and its graph-uniform `q^2` drift (`lem:aesp-cd-q-weighted-euclidean-reserve`), then gives a two-family stagewise STOP for the lagged unsplit `q^(-1)Q`-energy bank together with an exact `K8` high-band compatibility limit (`prop:aesp-cd-unsplit-q-energy-stagewise-stop`).
- **Conditional:** If the actual finite trajectory satisfies `J_T^fin <= (1-c)qT+B`, then computable `T` and `xi` give the terminal potential threshold (`cor:aesp-cd-conditional-finite-acceptance`).  The displayed accelerated eleven-resource vector in `cor:aesp-cd-frozen-conditional-contract` additionally specializes to `alpha<1/4`, absolute `c>=c_0>0`, and `B=polylog(alpha^(-1),epsilon^(-1),nnz(s)+2/epsilon)`.  The fresh gate, RPPR bias bridge, and cached-row accounting do not themselves depend on packing.  For `1/4<=alpha<=1`, the zero-start fallback closes the gate unconditionally in at most `5/epsilon` degree work and satisfies the same vector with `W_epsilon=nnz(s)+O(1/epsilon)`.
- **Measured:** None; this note is proof/algorithm analysis.
- **Refuted:** Raw objective gap does not control KKT error at the l1 kink (`lem:aesp-cd-center-cancel`); pointwise momentum nonexpansion fails on `P3` (`prop:aesp-cd-momentum-expansion`); correction calls cannot be charged only to support additions (`prop:aesp-cd-singleton-corrections`); no `o(1/q)` coefficient packs the collateral charge solely by monotone Euclidean log-error (`prop:aesp-cd-euclidean-packing-fails`); and the scalar ledgers alone cannot prove accelerated packing (`prop:aesp-cd-ledger-only-insufficient`).  The fixed-objective `P4` theorem refutes every horizon-uniform, fixed-support/fixed-parameter, or transient-only bound on `I_T`, but not an accuracy-logarithmic allowance or net exponent.  Round 024 additionally refutes ambient-norm black-box exact-to-finite shadowing through the lower retraction: its map is support-entry discontinuous and has sharp fixed-support amplification `1+1/alpha`.  Round 026 refutes an alpha-independent direct payment of the raw Euclidean correction defect by the same-window unsplit `Q`-energy drop: the reachable `K8` family needs `Omega(q^(-3))=Omega(alpha^(-3/2))`; even after the `mu_E` weight, that same direct payment needs `Omega(q^(-1))`.  Round 027 further refutes a uniform one-step `1-cq` contraction for the lagged unsplit bank `Phi_t+(A/q)E_(t-1)^Q` when the same coefficient is large enough to pay that `K8` pulse: a reachable low-mode `K2` trajectory has only `O(q^2)` relative decrease.  This does **not** refute a spectrally split, windowed, nonlinear, or differently normalized `q^(-1)`-weighted bank, an additive polylogarithmic term, direct finite-sequence packing, the net exponent, or the solver.
- **Open:** Prove `J_T^fin <= (1-c)qT+B` (or an equivalent direct rate) for the actual C2-plus-absolute finite recurrence on low-Dirichlet optimal supports `theta_A=o(q)`.  The high-Dirichlet class is closed structurally by `thm:aesp-cd-high-dirichlet-branch`; its condition uses the unknown optimal face and is not an algorithmic certificate.  Round 025 removes entry-dominated stages from the blocker at arbitrarily small `delta*q*T` cost.  Round 026 supplies cumulative persistent-controller and truncation `Q`-energy charges.  Round 027 shows that the exact Euclidean reserve has only `q^2` drift and that the simplest lagged unsplit `q^(-1)Q` reserve cannot contract stagewise at rate `cq`; its `K2` witness still has accelerated global decay with only logarithmic startup loss.  A windowed spectral or nonlinear transfer remains open, and neither reachable family is an additive-resistant counterexample.

## Central blocker

The old target of making normalized inflation horizon-uniform is false on an
actual fixed RPPR objective, and Round 024 shows that ambient Lipschitz
shadowing is not a viable finite transfer.  The remaining graph-uniform lemma
is a **net** exponent or a structure-aware direct rate for low-Dirichlet
optimal faces.  Entry rows and finite-created one-sided correction excess are
now explicitly charged.  Persistent-row controller squares, correction
energy, and surviving-momentum energy are also charged in `Q`-energy.  The
exact lagged Euclidean reserve absorbs the collateral defect but has only
`q^2` graph-uniform drift, while the lagged unsplit `q^(-1)Q` reserve cannot
simultaneously pay the reachable `K8` pulse and contract every stage at rate
`cq`.  The remaining analytical blocker is a windowed spectral or nonlinear
transfer that controls the Euclidean collateral cross term with an
accelerated graph-uniform constant, while retaining every retraction/rekey,
the finite residuals, and the fact that coordinatewise positive part does
not commute with spectral projectors.

## Dependencies and reusable outputs

- Formal taxonomy dependencies: none.
- Source/shared prerequisites: shared RPPR support/KKT facts and
  Catalyst/AESP source machinery.
- Supplies to: volume_gated_acceleration, hybrid_local_solver_synthesis, response_preconditioned_hybrid, and any direction needing safe lower centers or local KKT admission.

## Resume here

- Exact file/section/lemma: start at `lem:aesp-cd-persistent-square-ledger`, `lem:aesp-cd-truncation-q-energy`, `prop:aesp-cd-k8-q-bank-stop`, `lem:aesp-cd-q-weighted-euclidean-reserve`, `prop:aesp-cd-unsplit-q-energy-stagewise-stop`, and `cor:aesp-cd-conditional-finite-acceptance`.
- Next concrete action: Seek a spectrally split, windowed, nonlinear, or differently normalized `q^(-1)`-weighted Lyapunov that pairs persistent high-energy decay with the Euclidean collateral term while preserving accelerated low modes.  It must survive the fixed reachable pulse, the small-`q` same-drop STOP, the lagged unsplit-bank stagewise STOP, partial corrections, and current-residual suppression.  In particular, do not assume coordinatewise positive part commutes with spectral projectors, iterate ambient retraction Lipschitzness, target horizon-uniform `I_T`, erase `a_t`, or pay the defect from a single unsplit local drop.
- Stop/go test: Go if the actual finite sequence admits `J_T^fin <= (1-c)qT+B` with declared graph-uniform constants and the residual charges fit the dual absolute polish; stop if the proof erases `a_t`, uses unknown `x*` as an algorithmic certificate, or claims the conditional resource vector unconditionally.

## Verification

- Source pointers checked: README.md, taxonomy.toml, main.tex, docs/research_notes.md, docs/literature/acceleration.md, and the shared ledgers were cross-read through 2026-08-22.
- Focused build/checks run: Round 002 checked the collateral inequality numerically on five path regimes. An independent read-only audit verified the factors, index range, singleton/P3 consequences, and exact-collapse formula. Round 003 symbolically checked the exact two-vertex recurrence and all displayed limits in `prop:aesp-cd-euclidean-packing-fails`. Round 022 added `check_round022.py`: exact rational audits pass for the abstract identities at `q=1/100,1/20,1/10`; the exact P4 audit passes through `T=500` with 135 corrections, 44 positive stages, `I_500=1.023645592839495300681440396`, and `log(Phi_0/Phi_500)=348.258172221020140783...`. The optional exact P7 audit passes through `T=800` with 122 corrections, 39 positive stages, `I_800=7.294522704368255655469798574`, and progress `521.468182347257868782...`. These corrected high-precision logarithms replace earlier truncated-mantissa scratch values. An independent Round-022 mathematics-and-scope audit rederived the countermodel and both traces, adjudicated the logarithms from exact rational states, and returned CLEAN after the P4 display was wrapped.
- Round 023 adds `check_round023.py`.  It exactly replays the prefix, derives
  the active map and retraction matrix, checks every phase inequality on all
  four invariant-cone rays, verifies the word map and cone image, and bounds
  the harmful defect and potential by exact rational monomial intervals.  Two
  independent read-only audits separately reconstructed the phase indexing,
  cone, defect, potential, finite-inner identities, dual stop, and conditional
  acceptance constants.  `check_round023.py` and the Round-022 regression
  checker pass; Ruff format/check passes; the focused LaTeX build produces a
  clean 34-page PDF with no undefined references or layout warnings.
- Round 024 adds `check_round024.py`.  It uses exact rational arithmetic for
  the `P2` discontinuity and sharp amplification, a fixed-face separation
  instance and finite residual bound, and the high-Dirichlet contraction.
  Two independent read-only audits rederived every displayed constant and
  returned CLEAN after the settled-face, graph-uniform-scope, and eigenvalue
  wording repairs.  The Round-024 checker and Round-022/023 regressions pass;
  Ruff format/check and `git diff --check` pass; the focused LaTeX build
  produces a clean 37-page PDF with no warnings, undefined references, or
  overfull boxes.
- Round 025 adds `check_round025.py`.  It exactly checks the new-row residual
  shield, the one-sided same-state correction excess and momentum constants,
  the `4*delta*q` pre-gate charge, the post-full scalar filter, and the exact
  mixed-mode `K8` fractions.  An independent read-only audit rederived every
  index, maximum split, gate/potential constant, work logarithm, filter
  factor, and scope exclusion and returned CLEAN after notation and source
  hygiene repairs.  The Round-022--025 regression checkers pass; Ruff
  format/check and `git diff --check` pass; the focused LaTeX build produces
  a clean 41-page PDF with no warnings, undefined references, or overfull
  boxes.
- Round 026 adds `check_round026.py`.  It uses exact rational arithmetic to
  check the actual-finite persistent-row driver and its windowed square-energy
  telescope, both boundary-aware truncation bounds, the reachable dense-seed
  `K8` word `N,N,P0,F,N^infinity` including the all-time modal tail, and the
  small-`q` same-drop separation with raw ratio `Omega(q^(-3))` and
  `mu_E`-weighted ratio `Omega(q^(-1))`.  Independent exact replays checked
  the degree normalization, phase indexing, positive defects, pre-gate
  inequalities, and tail certificate.  A final independent read-only audit
  returned CLEAN after the later-trial index and exact `5/6` envelope
  guardrail were made explicit.  The Round-022--026 regression checkers pass;
  Ruff format/check and `git diff --check` pass; the focused LaTeX build
  produces a clean 48-page PDF with no warnings, undefined references, or
  overfull boxes.
- Round 027 adds `check_round027.py`.  It uses exact rational arithmetic to
  check the finite lagged Euclidean reserve, the reachable uniform-seed `K2`
  recurrence and fresh gate at `ell_t`, the lagged unsplit-bank coefficient
  floor and `O(q^2)` one-step STOP, the global non-obstruction, and the exact
  `K8` high-band payment fractions and limit.  Two independent exact replays
  and read-only source audits returned CLEAN after the lagged-bank and genuine
  persistent-stage indices were repaired.  The Round-022--027 regression
  checkers pass; Ruff format/check and `git diff --check` pass; the focused
  LaTeX build produces a clean 51-page PDF with no warnings, undefined
  references, or overfull boxes.
- Known gaps: The taxonomy, manifest, research ledger, and acceleration
  literature note now name correction log-inflation as the live target.
  The README has also been reconciled so its `V_exp` paragraph is historical
  setup rather than a second live blocker. Read `_shared/results/README.md` as
  saying continuation cost is open, not safe-center correctness. The new
  collateral charge is analytical and uses the unknown optimum. The abstract
  countermodel has no fixed objective or prox map.  The infinite `P4` theorem
  is an exact-solve, fixed-`q` result and has no finite-inner or end-to-end
  resource conclusion.  Round 025 controls support-entry and finite-created
  one-sided excess, but persistent-row positive-part mixing remains open; the
  displayed accelerated resource vector is explicitly conditional on a net
  packing theorem outside the proved a-posteriori high-Dirichlet structural
  class.  Round 026 now charges persistent controllers and both truncation
  pieces in windowed `Q`-energy, but its reachable small-`q` family rules out
  alpha-independent direct payment of the raw defect by that same unsplit
  drop (and still needs `Omega(q^(-1))` after `mu_E` weighting).  Round 027
  rules out uniform one-step accelerated contraction for the corresponding
  lagged unsplit additive bank, but its low-mode witness decays globally and
  the fixed `K8` pulse is payable by its high band.  The surviving target is
  a spectrally split, windowed, nonlinear, or differently normalized
  `q^(-1)`-weighted finite-sequence Lyapunov that closes the net exponent
  without erasing any residual, retraction, rekey, gate, or output charge.
