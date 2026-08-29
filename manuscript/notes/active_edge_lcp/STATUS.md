# Direction status: active_edge_lcp

Last reviewed: 2026-08-29

State: proved-open

## Exact question and contract

- **Question:** Can the exact RPPR obstacle LCP be solved by a graph-uniform
  local active-edge method without a supplied support or repeated-prefix work?
- **Model:** `c=b-alpha rho D^(1/2)1`, `x>=0`, `w=Qx-c>=0`, and
  `x_i w_i=0`, with `alpha I <= Q <= I`, point seed, and
  `vol(S*)<=1/rho` in the canonical nonzero regime.
- **Accuracy namespace:** Return feasible `xhat` with RPPR objective gap at
  most `eps_obj`.  The sufficient local stop is
  `||g_KKT(xhat)||_2 <= sqrt(2 alpha eps_obj)`; no residual namespace is
  silently substituted.
- **Access and charged work:** Charge seed and degree queries, adjacency
  entries, false activations, repeated scans, changing-face updates, numerical
  solves, boundary certificates, state traffic, materialization, and output.
- **Intended result:** A margin-free aggregate continuation and known-threshold reporter with
  total `O_tilde(vol(S*) sqrt(kappa(Q)) log(1/eps_obj))` work, implying
  `O_tilde(1/(rho sqrt(alpha)))` for OP2.

## Strongest proved result

In the exact RPPR obstacle LCP, every negative outside slack of a reachable
exact face belongs to the unknown optimum support.  Batched negative-slack
pivots preserve strict positivity, increase all old coordinates, require no
deletions, and terminate in at most `|S*|` activations.  Violations are
boundary-only.  This closes support soundness at the mathematical outer-loop
level without an oracle.

A supplied exact support can be solved by ordinary CG plus one final orthant
projection in
`O(vol(S*) / sqrt(alpha) log(1 / eps_obj))` charged row work.  A one-scan
minimum-norm KKT subgradient certifies objective gap.

The hidden sign-margin issue is closed.  For an approximate face solve with
residual norm `delta`, any approximate boundary slack below
`-delta/alpha` is negative on the exact face and is therefore support-safe.
If no key crosses that threshold and
`delta/alpha <= sqrt(2 alpha eps_obj)/(1+2 sqrt(|boundary U|))`, orthant
projection already satisfies the objective target.  The reporter need not
resolve all exact negative signs.

The finite-precision interface has overlapping thresholds: a certified slack
interval of predetermined width below twice the residual error either proves
a safe pivot or proves the projected objective stop.  Refinement therefore
depends only on the requested objective tolerance, not on key separation.

Across exact nested faces, the total squared correction energy and the total
squared full-slack motion are at most `alpha`.  This is a rigorous heavy-change
budget, but it does not pay for touching many small boundary-key changes or
for applying an implicit dense correction.

On a promised endpoint-seeded path, append-only scalar `LDL^T` state tests
each successive boundary in constant arithmetic and materializes once.  This
gives an exact-real, fully charged `O(vol(S*))` structural solver with no
global preprocessing.

## Central blocker

Prove the threshold-certified aggregate continuation bound in Definition
`def:active-edge-contract` of `main.tex`: over all nested true-support faces,
charge changing-face solve
state, warm starts, boundary-key updates and queries, interval error,
materialization, and output within
`O_tilde(E sqrt(kappa(Q)) log(1 / eps_obj))`, where explored incidence volume
`E=O_tilde(vol(S*))`.  The difficult interface is a dense positive correction
on the old face coupled to certifying whether any approximate active-edge key
crossed the known residual-derived threshold.

Terminal volume does not close this gap.  On endpoint paths the exact safe
faces can be all prefixes, so a full face solve, materialization, or boundary
refresh at every pivot costs `Theta(s^2)` for terminal volume `Theta(s)`.

## Claim ledger

- **Source:** canonical nonnegative optimum/support-volume facts; standard CG
  rate; Wei--Yang true-support activation and repeated-face work; the audited
  global LCP, bound-QP, SDD, and obstacle theorems.
- **Proved here:** exact obstacle/LCP signs and scaling; supplied-support CG
  work; safe batched pivots; boundary-only discovery; objective certificate;
  the margin-free approximate-face dichotomy and overlapping interval
  thresholds; the exact energy/slack-motion telescope; path cumulative-volume
  obstruction; exact linear-work endpoint-path continuation; four-vertex
  rational CG overshoot.
- **Conditional:** the fully charged active-edge contract implies OP2 work
  `O_tilde(1 / (rho sqrt(alpha)))` with logarithmic objective accuracy.
- **Measured:** none.
- **Refuted:** terminal support volume as a cumulative ledger; the invariant
  `0 <= x_k <= x*_rho` for ordinary or orthant-projected face CG.  Neither is
  a class lower bound.
- **Open:** arbitrary-graph dynamic principal response plus complete
  known-threshold boundary reporting without a supplied support.

## Literature verdict

- Wei--Yang 2026 is the closest local theorem, but solves every nested SDD
  system from scratch and scans a current boundary per round.
- Foniok et al. give at most `n` K-LCP pivots from zero, but their vertex
  oracle evaluates a global principal basis and all `n` cube orientations.
- Schmelzer--Stoll expose the `sqrt(kappa)` face-CG factor, but retain a global
  free-set loop, an outer-step factor, and a trajectory-wide decision margin.
- Koutis--Miller--Peng is usable for a supplied principal SDD matrix; its
  preprocessing is global and not changing-face support discovery.
- Durfee--Gao--Goranci--Peng support dynamic terminal additions and coordinate
  Laplacian queries, but only after full-graph preprocessing, with ambient
  sublinear time and polynomial accuracy dependence.
- van den Brand--Nanongkai--Saranurak maintain dense inverses dynamically, but
  use `O(n^omega)` preprocessing and ambient-polynomial update/query work.
- Bokanowski--Maroso--Zidani give at most linearly many Howard obstacle
  policies, but each iteration is a global system solve and policy test.
- Classical projected-CG, MPRGP, block-pivot, and monotone-multigrid results
  are global-only or rely on FEM hierarchy/strict-complementarity assumptions.

Exact theorem/page pointers are in `docs/literature/lcp-solvers.md`.

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Canonical authority: `manuscript/notes/problem_definitions/` and shared
  mathematical conventions, read-only.
- Read-only cross-checks: `evolving_support_cg`,
  `incremental_active_set_sdd`, `aspr23_bound_audit`, `aesp_cd_l1_rppr`,
  `delayed_reflection_ladder`, and `local_solver_oracle_hierarchy`.
- No material is promoted to the active manuscript.

## Verification

- `python3 verify_counterexample.py` uses only exact `Fraction` arithmetic and
  checks every iterate, step size, energy decrease, conjugacy, and overshoot.
- `python3 verify_threshold_dichotomy.py` checks 720 exact rational cases and
  exercises both the support-safe interval report and objective-stop branches,
  plus 36 exact energy/slack telescopes.
- `python3 verify_path_ldl.py` checks 580 exact canonical path instances,
  including full 30-vertex support, against direct principal solves and KKT.
- The focused note build, note registry, coordination audit, and all 213 tests
  pass.  The owned Python script passes Ruff lint and format checks.  The full
  repository format check still reports nine pre-existing files in the
  separately owned `aesp_cd_l1_rppr` proof-audit direction; exact details are
  recorded in the coordination handoff.

## Resume here

- Exact target: `main.tex`, Definition `def:active-edge-contract`, especially
  the aggregate bound `eq:aggregate-contract`.
- First test: a single block expansion `U -> U union J` with implicit Schur
  response; return one approximate key below `-delta/alpha` or certify none,
  while charging only new incidences and `sqrt(kappa)` numerical work.
- Stop/qualify if a dense old-coordinate correction forces replay of all old
  cut edges.  Do not reintroduce exact-sign refinement: the threshold theorem
  has already removed that requirement.
