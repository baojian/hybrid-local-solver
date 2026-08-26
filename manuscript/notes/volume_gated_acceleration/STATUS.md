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
  and 8, and first goes at stage 9.
- **Conditional:** Full product-scale work still requires a structural or
  stronger-potential continuation/amortization theorem that bounds expansion
  debt and repeated restricted work.
- **Measured:** Floating-point path scaling tables are scaffolding only; the
  promoted finite witnesses use exact rational arithmetic.
- **Refuted:** Uniform logarithmic ordinary restarts, shock-free zero-padding,
  several pointwise or constant-coefficient correction banks, recovery of the
  restarted causal account before the next admission on every graph, and
  frontier-only admission logic. Unconditional zero-balance all-history
  solvency of the named `delta^2` account is also refuted after three
  consecutive singleton admissions. These are scoped recurrence STOPs, not
  class lower bounds.
- **Open:** A useful structural solvency condition, justified reserve, or
  stronger observable; a uniform recovery horizon if one exists; and
  graph-uniform convergence/work beyond the finite named traces.

## Central blocker

The causal score identity is face-general, but unconditional zero-balance
all-history solvency of its `delta^2` account is false for the named recurrence
and gate. The three-admission witness retains every credit from the actual
zero initialization and still becomes transiently negative. The next argument
must impose an explicit useful graph/face condition, justify additional
reserve, or replace the observable; none may infer convergence or work from
scalar solvency alone.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`.
- Source/shared prerequisites: RPPR support/KKT facts, FISTA/AESP scaffold,
  and the common charged-work convention.
- Supplies to: Safe support/volume gates, exact path response ledgers,
  correction-bank counterexamples, and the causal cross-admission credit
  identity used by mixed-response directions.

## Resume here

- Exact file/section/lemma: Start with
  `prop:three-admission-all-history-stop`, then compare the causal
  two-admission path GO and `prop:t-tree-causal-next-admission-stop`.
- Next concrete action: Prove a nontrivial structural promised-class balance
  condition, justify an explicit reserve from a stronger energy ledger, or
  design and falsify a replacement observable on all three exact traces.
- Stop/go test: Go only if the replacement survives the three-admission
  all-history trace without future borrowing and charges all restricted-
  optimum queries. Stop if a proof silently adds initial credit, conflates
  scalar solvency with convergence, or extrapolates finite enumeration into
  an asymptotic theorem.

## Verification

- Source pointers checked: `README.md`, `main.tex` and included sections,
  `registry.toml`, and shared problem/results ledgers.
- Focused checks: Ten exact `volume_gated_acceleration.*` audits cover the
  Round-013--022 mechanisms. Run them with `uv run python -m
  experiments.proof_audits.runner --tier full --note
  volume_gated_acceleration`; the full tier includes the optional small-graph
  enumeration.
- Review status: Exact rational audits reproduce the named fractions,
  chronologies, Schur drops, balances, and scope qualifications, including the
  actual zero-start causal update through the three-admission STOP.
- Known gaps: Small-graph minimality is computational scaffolding. There is no
  nonpath eleven-resource vector, structural solvency theorem, asymptotic work
  result, or finite-precision guarantee.
