# Direction status: active_edge_lcp

Last reviewed: 2026-08-30

State: proved-open

## Exact question and contract

- **Question:** Can the exact RPPR obstacle LCP be solved by a graph-uniform
  local algorithm without a supplied support, global preprocessing, or
  uncharged repeated-prefix work?
- **Model:** `c=b-alpha*rho*D^(1/2)1`, `x>=0`, `w=Qx-c>=0`, and
  `x_i w_i=0`, with `alpha I <= Q <= I`, a point seed, and
  `vol(S*)<=1/rho` in the canonical nonzero regime.
- **Accuracy namespace:** Return feasible `xhat` with RPPR objective gap at most
  `eps_obj`; dependence on `1/eps_obj` is polylogarithmic.
- **Access and charged work:** Seed and degree queries, adjacency entries,
  candidate creation, false activations, repeated scans, face construction,
  numerical solves, solver state, boundary accumulation and decisions,
  materialization, projection, and output are all charged.
- **Intended result:** Theorem `thm:op2` proves randomized high-probability correctness
  with fully charged expected work
  `O_tilde(1/(rho*sqrt(alpha)) log(1/eps_obj))` and no supplied support or
  ambient preprocessing.

## Strongest proved result

The threshold-batch energy-depth theorem (`thm:batch-depth`) orders the true
support by safe admission batches and block-factorizes `Q[S*,S*]`.  Removing
all Cholesky blocks except the diagonal and first block subdiagonal produces a
block-bidiagonal M-matrix `C_hat` satisfying

```text
||C_hat^(-1)||_2 <= 1/sqrt(alpha),
||C_hat||_2 <= sqrt(2).
```

Chebyshev inverse decay on `C_hat C_hat^T` and the batch-causality inequality
give

```text
F(x^U_J)-F(x*) <= 8 q_alpha^(2J) + threshold^2/(alpha*rho),
q_alpha = (sqrt(2/alpha)-1)/(sqrt(2/alpha)+1).
```

The distributed threshold term charges every delayed or ambiguous vertex
once, when its eventual pivot block is eliminated.  It removes the earlier
positive-`rho` Krylov-containment gap.

Algorithm `alg:threshold-batch` chooses
`threshold=(1/8)*sqrt(alpha*rho*eps_obj)` and caps the number of phases at
`O(alpha^(-1/2) log(1/eps_obj))`.  Each phase solves the exposed
degree-coordinate SDD face to relative energy error
`(1/32)*sqrt(alpha*rho*eps_obj)`.  An exact active residual test certifies
absolute face-energy error, and capped independent retries give the requested
success probability.  The accepted face is scanned and all boundary residuals
above half the threshold are admitted.  Approximation error makes every pivot
strictly safe and leaves every unreported exact residual below the declared
threshold.  Orthant projection of the last face accounts for the remaining
numerical error.

Every face is contained in `S*`, so its volume is at most `1/rho`.  Multiplying
this by the proved phase bound yields OP2 while charging every item in the
resource ledger.

## Claim ledger

- **Source:** Canonical nonnegative optimum/support-volume facts; standard CG
  and Chebyshev estimates; Koutis--Miller--Peng's nearly-linear SDD solve on a
  supplied exposed matrix; audited global LCP/obstacle/bound-QP comparisons.
- **Proved here:** Exact obstacle/LCP scaling; safe batched pivots;
  boundary-only discovery; supplied-support CG; local KKT certificate;
  margin-free threshold and interval dichotomies; exact energy/slack
  telescope; threshold-batch Cholesky decay; the fully charged graph-uniform
  OP2 algorithm; path cumulative-volume obstruction; exact activation-once
  endpoint-path continuation; and the four-vertex projected-CG obstruction.
- **Conditional:** The persistent active-edge contract remains a stronger
  changing-face implementation route, but it is not used by the proved OP2
  theorem.
- **Measured:** The new batch-depth theorem passed a 1,152-case floating-point
  grid and an independent 216-case, 100-digit Decimal audit.  These are
  falsification checks, not proof.  The older threshold, path, and CG scripts
  use exact rational arithmetic where stated.
- **Refuted:** Terminal support volume alone as a cumulative-work ledger; and
  `0<=x_k<=x*_rho` for ordinary or orthant-projected face CG.  Neither is a
  class lower bound.
- **Open:** Deterministic finite-precision/bit-complexity guarantees and a
  persistent response implementation sharper than the proved fresh-batch
  solver.

## Central blocker

There is no remaining blocker for OP2 in the repository's exact-real
randomized word model.  The note remains `proved-open` because deterministic
coefficient-bit complexity and a persistent changing-face implementation are
strictly stronger targets.  The next falsifiable target is a certified
finite-precision realization whose bit and adjacency work remains
polylogarithmic in the requested objective accuracy; this is not needed by
`thm:op2`.

## Literature verdict

- Koutis--Miller--Peng supplies the only algorithmic black box used by the new
  theorem: a nearly-linear solve for each explicitly exposed SDD face.
- Wei--Yang remains the closest prior local active-set theorem, but its stated
  work retains an outer support factor; the batch-depth theorem is new here.
- Foniok et al., Bokanowski--Maroso--Zidani, Schmelzer--Stoll, classical
  block-pivot/bound-QP methods, and monotone multigrid do not state the OP2
  local access and work theorem.
- Dynamic Laplacian/inverse sources require global preprocessing or ambient
  polynomial work and are not used.

Exact theorem and page pointers are in `docs/literature/lcp-solvers.md`.

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Canonical authority: `manuscript/notes/problem_definitions/` and shared
  mathematical conventions, read-only.
- Algorithmic source primitive: the cited nearly-linear SDD theorem.
- Read-only cross-checks: `evolving_support_cg`,
  `incremental_active_set_sdd`, `aspr23_bound_audit`, `aesp_cd_l1_rppr`,
  `delayed_reflection_ladder`, and `local_solver_oracle_hierarchy`.
- The obstacle reduction, safe-pivot invariant, threshold-batch depth theorem,
  and fully charged OP2 algorithm are promoted in condensed form to the active
  manuscript.  Deterministic bit complexity and persistent response remain in
  this note as stronger open directions.

## Verification

- `verify_counterexample.py`: exact rational CG overshoot audit.
- `verify_threshold_dichotomy.py`: 720 exact rational threshold cases and 36
  exact energy/slack telescopes.
- `verify_path_ldl.py`: 580 exact canonical path cases.
- `verify_batch_depth.py`: randomized structured falsification audit of the
  block factor, inverse ordering, causal forcing, and stated tail bound.
- `verify_batch_depth_high_precision.py`: dependency-free 100-digit Decimal
  audit on 216 canonical path/star instances, including singular-value and
  inverse-ordering checks.
- Focused note build passed: 24 pages with resolved references/citations and no
  fatal, undefined-reference, or overfull-box diagnostics; all pages were
  rendered and visually inspected without clipping, overlap, or broken
  equations/tables.
- The promoted manuscript builds to 20 pages with resolved citations and
  references; `git diff --check`, `make agent-audit`, both batch-depth audits,
  and `make research-audit-fast` pass.
- The current repository-wide `make test` passes 210/213 tests.  Its three
  failures are pre-existing AESP-CD note-maintenance issues: one semantic
  alias match and two reports of the same 1,237-line extracted section.
  `make lint` is likewise red on one pre-existing unused import in the
  `problem_definitions` note.  None of those files is modified by this
  manuscript promotion.

## Independent audit verdict

- A hostile proof audit found no fatal defect in the block Cholesky theorem
  after the `J=0`, two-face chronology, inverse-ordering, and polynomial-tail
  wording repairs.
- A separate end-to-end audit found no fatal defect after adding exact
  active-residual certification, capped constant-success SDD retries, and the
  unconditional batch-exposure charge.
- A source-contract audit verified the canonical signs/scaling and corrected
  the degree-scaled SDD application and KMP probability interface.
- Do not promote automatically; manuscript promotion remains a separate
  controller decision.

## Resume here

- Proof authority: `sections/body/note_part1.tex` for `thm:batch-depth` and
  `sections/body/note_part2.tex` for `alg:threshold-batch` and `thm:op2`.
- For review, recheck the block-Cholesky inverse ordering, two-face causal
  forcing, certified SDD retry wrapper, and unconditional exposure ledger.
- The only next research extension is deterministic finite precision or a
  sharper persistent-response backend; neither should weaken or relabel the
  proved exact-real OP2 theorem.
