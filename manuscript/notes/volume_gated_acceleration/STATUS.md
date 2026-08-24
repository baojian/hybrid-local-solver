# Direction status: volume_gated_acceleration

Last reviewed: 2026-08-24
State: proved-open

## Exact question and contract

- **Question:** Can safe RPPR support gates preserve accelerated progress
  across certified subspace additions without a full restart or old-face scan
  per admission?
- **Model:** Shared PPR plus RPPR safe-support gates. Exact path audits use the
  declared zero-start transported-center recurrence and complete
  all-violations gate; the nonpath audit uses the named asymmetric six-vertex
  T tree and the same causal scalar ledger.
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
  through stage 13, and first goes at stage 14.
- **Conditional:** Full product-scale work still requires an all-history
  continuation/amortization theorem or a structural condition that bounds
  expansion debt and repeated restricted work.
- **Measured:** Floating-point path scaling tables are scaffolding only; the
  promoted finite witnesses use exact rational arithmetic.
- **Refuted:** Uniform logarithmic ordinary restarts, shock-free zero-padding,
  several pointwise or constant-coefficient correction banks, recovery of the
  restarted causal account before the next admission on every graph, and
  frontier-only admission logic. These are scoped recurrence STOPs, not class
  lower bounds.
- **Open:** All-history causal solvency or a useful weaker structural
  condition, a uniform recovery horizon if one exists, and graph-uniform
  convergence/work beyond the finite named traces.

## Central blocker

The causal score identity is face-general, but the available solvency proofs
are finite and trajectory-specific. The nonpath witness rules out a
recovery-before-next-admission invariant for the named recurrence and gate;
it does not refute carrying older credit indefinitely. The next argument must
either prove all-history solvency under an explicit structure condition or
exhibit debt that survives enough admissions to invalidate that route.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`.
- Source/shared prerequisites: RPPR support/KKT facts, FISTA/AESP scaffold,
  and the common charged-work convention.
- Supplies to: Safe support/volume gates, exact path response ledgers,
  correction-bank counterexamples, and the causal cross-admission credit
  identity used by mixed-response directions.

## Resume here

- Exact file/section/lemma: Start with the causal two-admission path result and
  `prop:t-tree-causal-next-admission-stop`, together with their exact gate and
  Schur-drop definitions.
- Next concrete action: Search a family with three or more relevant
  admissions, or prove a structural all-history balance bound that survives
  the asymmetric-T chronology.
- Stop/go test: Go if the declared causal ledger remains nonnegative without
  future borrowing and all restricted-optimum queries are charged. Stop if a
  proof resets credit silently, conflates scalar solvency with convergence, or
  extrapolates finite enumeration into an asymptotic theorem.

## Verification

- Source pointers checked: `README.md`, `main.tex` and included sections,
  `registry.toml`, and shared problem/results ledgers.
- Focused checks: Nine exact `volume_gated_acceleration.*` audits cover the
  Round-013--021 mechanisms. Run them with `uv run python -m
  experiments.proof_audits.runner --tier full --note
  volume_gated_acceleration`; the full tier includes the optional small-graph
  enumeration.
- Review status: Prior independent audits reproduced the named fractions,
  chronology, Schur drops, balances, and scope qualifications. This
  reorganization changes no theorem, equation, or evidence classification.
- Known gaps: Small-graph minimality is computational scaffolding. There is no
  nonpath eleven-resource vector, all-admission theorem, asymptotic work
  result, or finite-precision guarantee.
