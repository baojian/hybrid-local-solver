# Direction status: psi_master_inequality

Last reviewed: 2026-08-29
State: proved-open
Agent family: codex
Role: controller
Branch: `agent/codex/windowed-spectral-lyapunov-7h`
Base commit: `5d4e0ffc54b5988fa2ca7aff65eef847a8b16cd0`
Allowed write scope: the registered `windowed-spectral-lyapunov-7h` scope.

## Exact question and contract

- **Question:** When is the exact one-step master form `Psi` nonpositive for
  every admissible clipped state?
- **Model:** Source-aligned RPPR and the precisely reconstructed Fable
  accelerated proximal recurrence.
- **Accuracy namespace:** A note-scoped Lyapunov absorption certificate; it is
  not identified with an unresolved global stopping rule.
- **Access and charged work:** The first task is an analytic trajectory
  inequality.  Any algorithmic corollary must separately charge graph access,
  clipping, face changes, and inverse primitives.
- **Intended result:** A theorem for a nontrivial infinite graph family, a
  verifiable structural condition, or an exact counterexample.

## Claim ledger

- **Source:** Fable's iteration-7 master identity is the starting exploratory
  claim; its finite exact decisions remain read-only evidence.
- **Proved here:** The degree-scaled recurrence and its full algebraic cap
  domain; the exact identity
  `V(h_(t+1),h_t)-(1-q)^2 V(h_t,h_(t-1))=Psi(y_t,h_t)`; the equivalent
  clip/slack decomposition; and nonpositivity for the two unmixed channels
  `y>=0` and `y<=0` under `mu_2>=2q`.  A kernel positive-association lemma
  proves `Psi<=0` under the entrywise `(HK)` condition.  The closed
  `(3D-A)^-1 D` blocks prove `(HK)` with ratios `13/36` within a part and
  `3/4` across the cut on every complete bipartite graph.  Consequently
  `sup Psi=0` on every `K_{a,b}`, `a,b>=1`, for `0<q<=1/2`.  More generally,
  a rank-one lumped-resolvent formula and an exact nonnegative
  simplex-Bernstein certificate prove `(HK)` and `sup Psi=0` on every
  complete multipartite graph `K_{n_1,...,n_k}`, with arbitrary positive
  unequal part sizes and no balance threshold.  Exact elimination of `h`
  gives a second sufficient condition `(CL)`: a zero-row-sum cross kernel
  has nonpositive off-diagonal entries.  This proves `sup Psi=0` for every
  balanced independent-set blow-up `C6[Kbar_a]`, all `a>=1` and
  `0<q<=1/4`, even though `(HK)` fails there with exact ratio
  `5211/4900>1`.  A third structural theorem pays positive cross-kernel
  entries edge by edge when the two diagonal kernels are weighted
  Laplacians and `c_ij^2<=a_ij*b_ij`.  It proves `sup Psi=0` on every
  balanced independent-set blow-up `C10[Kbar_a]` throughout
  `1/25<=q<=7/100`, where `(CL)` fails, because only adjacent cross entries
  are positive, the within-part entries are negative, and at `q=1/20` the
  exact payment ratio is
  `9190540374100260057432724000/35964609239043602890432954263<1`.
  At `q=1/20`, exact rational inversion also closes every balanced blow-up of
  `C9` and `C11`; their adjacent Young ratios are approximately `0.0490` and
  `0.4137`, respectively.  A fourth sufficient condition clips the positive
  off-diagonal cross kernel, chooses its otherwise invisible diagonal, and
  requires the resulting two-by-two operator block to be positive
  semidefinite.  Exact rational LDL certificates prove this diagonal
  completion on every balanced blow-up of `C12` and `C13` at `q=1/20`, even
  though positive off-diagonal entries in both energy kernels rule out the
  edgewise weighted-Laplacian theorem.
- **Conditional:** None yet.
- **Measured:** None yet.
- **Refuted:** `(CL)` does not cover all cycles: on `C10` at `q=1/20`, its
  adjacent kernel entry is the exact positive rational
  `6998345705403423/396849260156782400`.  This refutes the sufficient proof
  route, not `Psi<=0` itself; edgewise Young payment now closes that exact
  infinite blow-up family by a different sufficient condition.
- **Open:** Analytic nonpositivity on general graphs and on graph families
  lying beyond `(HK)`, `(CL)`, edgewise payment, and diagonal completion.

## Central blocker

The eliminated-`h` form retains clipping complementarity.  Diagonal
completion now pays positive cross entries even after the energy kernels stop
being weighted Laplacians, but only on the two additional fixed cycle
quotients currently certified.  The next advance must prove a
graph-uniform/quotient-varying completion or produce an exact admissible
positive witness.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`.
- Source/shared prerequisites: source-aligned RPPR definition.
- Context/provenance: Fable iteration-7 files are read-only exploratory evidence.
- Supplies to: safeguarded acceleration and graph-family absorption analyses.

## Resume here

- Exact file/section/lemma: `lem:psi-master-identity`,
  `thm:psi-hk-nonpositivity`, `lem:psi-eliminate-h`, and
  `thm:psi-edgewise-young`, `thm:psi-c6-blowup`, and
  `thm:psi-c10-edgewise`, `thm:psi-neighboring-cycle-edgewise`, and
  `thm:psi-c12-c13-diagonal-completion` in `main.tex` and
  `sections/diagonal_completion.tex`.
- Next concrete action: vary the cycle quotient or find the first exact
  admissible state beyond all three sufficient routes.
- Stop/go test: prove a family-wide sign inequality or produce an exact
  admissible positive witness.

## Verification

- Source pointers checked: shared problem/results summaries,
  `aesp_cd_l1_rppr`, `volume_gated_acceleration`, the acceleration/local-solver
  literature notes, and Fable iteration-6/7 evidence.
- Focused build/checks run: `make -C
  manuscript/notes/psi_master_inequality`, the independent exact-rational
  `verify_master_identity.py` audit (21/21), the exact
  `verify_complete_bipartite.py` audit (64 graphs and 5280 off-diagonal
  formulas), the exact `verify_complete_multipartite.py` certificate (45/45
  nonnegative degree-eight numerator coefficients, 10/10 nonnegative
  denominator coefficients, 493 part vectors, and 64094 off-diagonal
  checks), the exact `verify_cycle_blowup.py` audit (six rational-function
  identities, 24 eliminated-`h` checks, 36 blow-up matrices, 68796 strict
  off-diagonal checks, the exact `C10` point certificate, and 19 exact
  interval Bernstein certificates, plus fixed-`q` exact edgewise certificates
  for `C9`, `C10`, and `C11`, and exact diagonal-completion certificates with
  22/24 positive quotient LDL pivots for `C12`/`C13`),
  and `git diff --check` pass.  The edgewise theorem and its weighted
  double-counting were also independently rederived before promotion.
- Known gaps: mixed clipping beyond all four sufficient conditions, proper
  faces, finite inner residuals, and all algorithm/work consequences.

## Repository handoff

- Provider-owned paths changed: none.
- Shared paths changed: none in the direction branch.
- Assignment state: active.
