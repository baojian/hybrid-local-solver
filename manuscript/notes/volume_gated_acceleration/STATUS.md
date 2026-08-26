# Direction status: volume_gated_acceleration

Last reviewed: 2026-08-27
State: proved-open

## Exact question and contract

- **Question:** Can safe RPPR support gates preserve accelerated progress
  across certified subspace additions without a full restart or old-face scan
  per admission?
- **Model:** Shared PPR plus RPPR safe-support gates. Exact path audits use the
  declared zero-start transported-center recurrence and complete
  all-violations gate; the nonpath audits use two named six-vertex graphs and
  the same causal scalar ledger.
- **Accuracy namespace:** The final PPR target is
  `||D^-1/2(x_hat-x0)||_infinity <= eps_ppr`; `rho` is RPPR regularization and
  `tau` the one-sided gate, with the main conversion
  `rho=tau=eps_ppr/2`.
- **Access and charged work:** Restricted steps cost `vol(U)`; admission
  scans, response/recurrence calls, state writes, validation, materialization,
  and output are charged in the shared eleven-resource order.
- **Intended result:** Peak volume `O(1/eps_ppr)` and graph-uniform
  `O_tilde(1/(rho*sqrt(alpha)))` work.

## Claim ledger

- **Source:** RPPR/FISTA support and confinement facts, the classical
  bad-star phenomenon, LocCH, and AESP are source ingredients identified in
  the note.
- **Proved here:** Principal conditioning, spider geometry, the exact-PPR
  core, RPPR support/error conversion, safe lower-envelope admission, the
  exact peak-volume gate, transported-center/Schur ledgers, and append-only
  path response. Exact finite audits then delimit correction/error banks,
  isolate reset and follow-up effects, and prove a causal credit ledger. On
  the `q=1/5` path, old credit survives two admissions; restarting at stage 7
  stops through stage 11 and first goes at stage 12. On the asymmetric T tree,
  the restarted balance remains negative through the next admission, stops
  through stage 13, and first goes at stage 14. On the second six-vertex
  graph, the account begins at the actual zero initialization, retains all
  credit from three consecutive singleton admissions, stops at held stages 7
  and 8, and first goes at stage 9. The causal reserve
  `R_k=E_0+D_k-E_k` is exactly the transported-center energy consumed by
  already executed fixed-face contractions and is unchanged across exact
  transported admissions. Its exact finite-trace minimum coefficient repairs
  the six-vertex witness with `lambda*=0.013014...`; coefficient `3` repairs
  every rooted connected graph-atlas trace through order seven at `q=1/5`.
  A reachable zero-start `K_{2,3}`-plus-seed-leaf family requires
  `lambda(q) ~ 49/(3884q^4)` while remaining projection-inactive through the
  reviewed stage. Together with the proved quartic upper coefficients, this
  closes the graph-uniform order at `Theta(q^-4)` for the support-aware ledger
  and the inactive-original subclass. More generally, the exact leading
  `K_{2,r}`-plus-seed-leaf coefficient tends to `1/15`, so every
  graph-uniform repair has `liminf q^4 lambda(q) >= 1/15` along that family.
  On a separate explicit 30-vertex point-seed graph at `q=12/625`, the exact
  zero-start complete-gate trace first clips vertex 23 benignly at stage 11,
  then reaches `p_23=0<r_23(p)` at stage 12 with
  `n_23/b_23=5.530040...` and positive causal debt. The exact required
  coefficient is `0.086694...`, with
  `q^4 lambda=1.178144...e-8`, and the run later certifies at stage 32. An
  exact nine-point rational screen of the same fixed graph is finite evidence
  only: the relevant row appears for `q=0.0188,...,0.0194` and disappears at
  both adjacent screened endpoints. For the declared point-seed parameters
  `rho=tau=q/5` with an interior initial singleton, the first boundary
  admission forces
  `E_0>c_0(q)q^5`, where
  `c_0(q)=4(1+q^2)/(5(1-q^2)(3+q^2))`; hence the consumed reserve is already
  larger than `c_0(q)q^6`. This floor pays every later clipped-zero residual,
  while the projected decrement pays the positive-support rows. Therefore
  the original all-coordinate score, with arbitrary projection, is solvent
  with `(1-q^2)/q^4`. Together with the `K_{2,r}` family, this closes its
  graph-uniform coefficient order at `Theta(q^-4)` as well. Separately, the
  same transported recurrence has the graph-uniform total-energy cap
  `E_0+D_k <= q^2`. Direct residual-to-envelope control at the sharpened
  threshold `4q^10/(25(1+q^2)(1+3q^2)^2)` then forces the complete gate
  to admit or certify within `O(q^-1 log(1/q))` consecutive steps per face.
  Hence every finite execution terminates with PPR error at most `2q/5`,
  `T=O(q^-2 log(1/q))`, and swept active volume
  `O(q^-3 log(1/q))`. A dense incremental exact-real response charges all
  optimum shifts in the same arithmetic order with `O(q^-2)` storage.
  On any fixed-gap 3-regular `n`-vertex spectral-expander family at `q=1/(2n)`, the
  normalized RPPR optimum is strictly above `tau=q/5` at every vertex.
  Terminal certification therefore forces the named execution to reach the
  full face.  Linear treewidth and strict Stieltjes fill force every explicit
  original-basis scalar Cholesky/LDL response to store `Omega(q^-2)` scalars
  and perform `Omega(q^-3)` ordinary pivot arithmetic, even with the best
  offline ordering and final support supplied.
  If a control policy instead gates directly on each fully materialized exact
  restricted optimum, its safe-envelope correction is zero.  It invokes the
  same complete gate once per face, uses `O(q^-2)` cumulative scans, and
  removes the hold logarithm from the dense fallback, whose factor/solve work
  becomes `O(q^-3)`.  This is an exact active-set comparator, not a log-free
  chronology theorem for the named fixed-step recurrence.
- **Conditional:** The named complete gate preserves `Xi` exactly across
  admissions. For interior visited restricted optima, the baseline coefficient
  `(1+q^2)(1-q)/q^5` remains valid, and the exact projection-normal identity
  gives the step-local refinement `(C_n+1-q^2)/q^4` when every clipped
  positive-residual row obeys `n_i <= C_n((1-q)z_i+qz_i*)`; inactivity has
  `C_n=0`. A modified safe positive-support envelope has coefficient
  `(1-q^2)/q^4` under arbitrary projection; its gate
  chronology may differ and clipped-zero rows remain in admission and terminal
  scans. Under the declared low-frequency residual condition
  `||r||_D^2 <= 2 c_low q^2 P`, coefficient
  `2 c_low(1-q)/q^3` suffices. Full product-scale work still requires a
  structural or stronger-potential continuation/amortization theorem that
  bounds expansion debt and repeated restricted work.
- **Measured:** Floating-point path scaling tables are scaffolding only. The
  graph-atlas reserve sweep is exact finite evidence at `q=1/5`, not a
  graph-uniform extrapolation; all promoted witness values use exact rational
  arithmetic.
- **Refuted:** Uniform logarithmic ordinary restarts, shock-free zero-padding,
  several pointwise or constant-coefficient correction banks, recovery of the
  restarted causal account before the next admission on every graph, and
  frontier-only admission logic. Unconditional zero-balance all-history
  solvency of the named `delta^2` account is also refuted after three
  consecutive singleton admissions. On an actual zero-start leaf-seeded
  `K_{1,4}` family, the consumed-energy repair needs
  `lambda(q) ~ 1/(32q^3)`, so no constant or `O(polylog(1/q))` multiplier is
  uniform. Its reviewed candidates are strictly positive, so this lower order
  also applies to the support-aware modification. An exact projection-active
  three-vertex state refutes extending the original-score `2/q^4` decrement
  to arbitrary algebraic states; that three-vertex state itself has no
  zero-start reachability claim.
  The stronger reachable quartic family refutes every `o(q^-4)` coefficient
  for both reviewed ledgers. These are scoped recurrence/ledger STOPs, not
  convergence or work lower bounds. The 30-vertex trace also refutes the
  possible shortcut that every reachable clipped row has nonpositive
  post-step residual, but it gives no asymptotic coefficient lower bound. The
  threshold-tuned endpoint-path route
  also stops on the registered finite instances: the gate certifies two
  vertices before the intended full face and projection remains inactive.
- **Refuted (representation-specific):** Sparse ordering or ordinary
  multifrontal organization cannot make the dense fallback product-scale on
  the full-support expander family.  This STOP applies only to exact
  original-basis explicit scalar Cholesky/LDL Schur updates.  It is not a
  recurrence or information lower bound, does not cover compressed,
  matrix-free, iterative, approximate, or fast-matrix-multiplication
  responses, and says nothing about whether the per-face logarithm is
  necessary.
- **Open:** Identify useful narrower classes where the low-frequency condition
  holds; remove the logarithm for the named candidate-envelope recurrence or
  prove it necessary; and bypass explicit scalar Cholesky with a charged
  response that improves the `O(q^-3)` exact-optimum comparator to desired product-scale
  `O_tilde(q^-2)` work. Finite precision, bit complexity, stability, and
  non-Cholesky response costs remain open.

## Central blocker

The causal score identity is face-general, but unconditional zero-balance
all-history solvency of its `delta^2` account is false for the named recurrence
and gate. The justified consumed-energy reserve repairs all finite `q=1/5`
atlas traces with coefficient `3`, and the reachable quartic family supplies
the matching lower order. The first-admission energy floor closes both the
support-aware and original all-coordinate coefficient orders at
  `Theta(q^-4)`, including arbitrary projection in the theorem's interior
  point-seed scope. The exact normal identity and 30-vertex trace remain useful local
diagnostics, but their ratio no longer blocks scalar all-history solvency.
The scalar quartic statement itself still may not be promoted into a
convergence conclusion. The separate total-energy argument now supplies a
graph-uniform terminal horizon and a dense exact-real fallback, but not the
desired product-scale work theorem.  The expander STOP now shows that sparse
ordering cannot repair the explicit scalar Cholesky fallback; the remaining
representation target must be compressed, matrix-free, iterative,
approximate, or otherwise outside that class.  The per-face logarithm remains
independently open.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`.
- Source/shared prerequisites: RPPR support/KKT facts, FISTA/AESP scaffold,
  and the common charged-work convention.
- Context/provenance: the companion `propagate_settle_framework` note proves
  a related quadratic-storage obstruction for explicit multifrontal
  responses at a different parameter scaling.  The local expander STOP
  includes its own support-margin, separator, strict-fill, and scalar-work
  proof and therefore adds no formal registry dependency.
  The companion `incremental_active_set_sdd` note develops the general exact
  solve-and-boundary interface and a linear path realization.  It is likewise
  comparator context rather than a formal dependency of the local proofs.
- Supplies to: Safe support/volume gates, exact path response ledgers,
  correction-bank counterexamples, and the causal cross-admission credit
  identity used by mixed-response directions.

## Resume here

- Exact file/section/lemma: Start with
  `prop:consumed-energy-structural-solvency` and
  `prop:consumed-reserve-quartic-projection` and
  `thm:original-score-projected-quartic` and
  `thm:complete-gate-soft-horizon` and
  `cor:complete-gate-dense-fallback` and
  `cor:complete-gate-exact-optimum-comparator` and
  `prop:complete-gate-explicit-cholesky-expander-stop` and
  `prop:original-score-normal-anchor` and
  `prop:reachable-positive-residual-projection`, then
  `prop:consumed-energy-quartic-lower` and
  `prop:consumed-energy-star-stop`, then compare
  `prop:three-admission-all-history-stop`.
- Next concrete action: sharpen the graph-uniform soft horizon by removing
  its per-face logarithm or replace explicit scalar Cholesky transport with a
  compressed, matrix-free, iterative, approximate, or otherwise non-Cholesky
  charged response whose total work is `O_tilde(q^-2)`. The scalar reserve and
  normal-anchor diagnostics are not needed for the proved horizon.
- Stop/go test: Go only if the replacement survives the reachable quartic
  family, star asymptotic, and three-admission all-history trace without future
  borrowing and charges all
  restricted-optimum/energy queries. Stop if a proof silently adds initial
  credit, conflates scalar solvency with convergence, or extrapolates finite
  enumeration into an asymptotic theorem.

## Verification

- Source pointers checked: `README.md`, `main.tex` and included sections,
  `registry.toml`, and shared problem/results ledgers.
- Focused checks: Fourteen exact `volume_gated_acceleration.*` audits cover the
  Round-013--026 mechanisms. Run them with `uv run python -m
  experiments.proof_audits.runner --tier full --note
  volume_gated_acceleration`; the full tier includes both optional small-graph
  enumerations.
- Review status: Exact rational audits reproduce the named fractions,
  chronologies, Schur drops, balances, reserve identities, atlas maximum, star
  rational functions/asymptotics, tensor Bernstein determinant certificate,
  projection-active STOP, reachable quartic formal series and exact replay
  grid, exact leading `K_{2,r}` formulas, projection-normal identities, finite
  critical-path gate failures, candidate inactivity checks, the reachable
  positive-residual projection chronology and debt, the exact first-admission
  quartic constants, the terminal-energy cap and envelope threshold, and
  scope qualifications.  The expander audit checks the exact resolvent
  normalization, RPPR margin, product-scale conversion, clique-storage count,
  and scalar Schur-update sum; expansion and treewidth remain theorem proof,
  not finite computational evidence.
- Known gaps: Small-graph enumeration is computational scaffolding. The
  low-frequency promised-class condition has not been derived from graph
  geometry. Exact support tests require finite-precision margins in an
  implementation. There is no product-scale nonpath eleven-resource vector,
  sparse-response theorem, finite-precision guarantee, or bit-complexity
  bound.  The named candidate-envelope fallback is exact-real and
  `O(q^-3 log(1/q))`; the changed-policy exact-optimum comparator is
  `O(q^-3)`.
