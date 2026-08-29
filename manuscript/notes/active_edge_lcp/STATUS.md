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
- **Intended result:** A margin-free aggregate continuation and reporter with
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

## Central blocker

Prove the margin-free aggregate continuation bound in Definition 6.1 of
`main.tex`: over all nested true-support faces, charge changing-face solve
state, warm starts, boundary-key updates and queries, sign refinement,
materialization, and output within
`O_tilde(E sqrt(kappa(Q)) log(1 / eps_obj))`, where explored incidence volume
`E=O_tilde(vol(S*))`.  The difficult interface is a dense positive correction
on the old face coupled to complete reporting of newly negative active-edge
keys.

Terminal volume does not close this gap.  On endpoint paths the exact safe
faces can be all prefixes, so a full face solve, materialization, or boundary
refresh at every pivot costs `Theta(s^2)` for terminal volume `Theta(s)`.

## Claim ledger

- **Source:** canonical nonnegative optimum/support-volume facts; standard CG
  rate; Wei--Yang true-support activation and repeated-face work; the audited
  global LCP, bound-QP, SDD, and obstacle theorems.
- **Proved here:** exact obstacle/LCP signs and scaling; supplied-support CG
  work; safe batched pivots; boundary-only discovery; objective certificate;
  path cumulative-volume obstruction; four-vertex rational CG overshoot.
- **Conditional:** the fully charged active-edge contract implies OP2 work
  `O_tilde(1 / (rho sqrt(alpha)))` with logarithmic objective accuracy.
- **Measured:** none.
- **Refuted:** terminal support volume as a cumulative ledger; the invariant
  `0 <= x_k <= x*_rho` for ordinary or orthant-projected face CG.  Neither is
  a class lower bound.
- **Open:** arbitrary-graph dynamic principal response plus complete
  boundary reporting without a supplied support or hidden sign margin.

## Literature verdict

- Wei--Yang 2026 is the closest local theorem, but solves every nested SDD
  system from scratch and scans a current boundary per round.
- Foniok et al. give at most `n` K-LCP pivots from zero, but their vertex
  oracle evaluates a global principal basis and all `n` cube orientations.
- Schmelzer--Stoll expose the `sqrt(kappa)` face-CG factor, but retain a global
  free-set loop, an outer-step factor, and a trajectory-wide decision margin.
- Koutis--Miller--Peng is usable for a supplied principal SDD matrix; its
  preprocessing is global and not changing-face support discovery.
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
- The focused note build, note registry, coordination audit, and all 213 tests
  pass.  The owned Python script passes Ruff lint and format checks.  The full
  repository format check still reports nine pre-existing files in the
  separately owned `aesp_cd_l1_rppr` proof-audit direction; exact details are
  recorded in the coordination handoff.

## Resume here

- Exact target: `main.tex`, Definition `def:active-edge-contract`, especially
  the aggregate bound `eq:aggregate-contract`.
- First test: a single block expansion `U -> U union J` with implicit Schur
  response; attempt to report every newly negative boundary key while charging
  only the new incidences and `sqrt(kappa)` numerical work.
- Stop/qualify if a dense old-coordinate correction forces replay of all old
  cut edges or if sign correctness assumes an undeclared minimum margin.
