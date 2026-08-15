# Research Notes

## Hybrid Local Solver

Working hypotheses, proof ideas, and experimental observations should be recorded here.

Important topics:

- Catalyst acceleration;
- AESP;
- LocSOR;
- hybrid switching rules;
- complexity bounds.

## 2026-08-14: active lower-bound ledger and first tight local hybrid

The active manuscript now separates six algorithm-specific statements under
their native accuracy conventions.

Closed statements:

- the classical APPR proof was rechecked against Andersen, Chung, and Lang
  (2007), Definition 3.3, Lemma 3.4, Algorithm 1, and Theorem 3.2. The lazy
  update, column-vector invariant, mass identity, ordering-independent star
  lower bound, and RPPR bridge are correct;
- a new numerical regression test solves the PageRank and RPPR systems
  directly and verifies `p + pr(r) = pi` for every implemented active ordering;
- full-batch RPPR ISTA retains its previously proved tight general-seed work
  `Theta((1 + log(1 / (delta * rho))) / (alpha * rho))`;
- residual-thresholded coordinate ISTA has a new ordering-independent star
  lower bound `Omega(1 / (alpha * rho))`. Together with its existing potential
  upper bound, this proves exact worst-case work
  `Theta_delta(1 / (alpha * rho))` for every fixed relative accuracy `delta`;
- the coordinate-to-batch coarse-to-fine hybrid inherits the same lower bound
  from its first phase and therefore has the same exact fixed-accuracy
  worst-case order. This is the first active-manuscript hybrid with matching
  upper and lower work bounds;
- the coarse forward-push star proof was strengthened from a scheduled-cycle
  argument to an ordering-independent flow proof, giving an explicit matching
  lower bound for Phase I;
- the full fixed-relaxation FIFO CF-Push hybrid still has only the spider lower
  bound `Omega(1 / (alpha * eps_ppr))` and the weaker energy upper bound. Its
  exact worst-case order remains open.

Scope boundary:

- these statements do not identify `eps_appr`, `rho`, `delta`, and `eps_ppr`;
- tightness is for the stated algorithms and work models, not for every local
  graph oracle;
- the graph-uniform accelerated `O_tilde(1 / (rho * sqrt(alpha)))` target
  remains open and the AESP--LOCSOR publication gate is unchanged.

## 2026-08-12: ASPR 2023 correctness and path tightness audit

Recorded as a standalone note in `manuscript/notes/aspr23_bound_audit/`.
The note reconstructs the intended exact-arithmetic ASPR theorem after
repairing the source's quadratic normalization, RPPR linear term, and the
APGD-output distance display.

Closed statements:

- the support-safety and objective-gap argument is valid for the corrected
  Stieltjes quadratic contract;
- on an endpoint-seeded RPPR path with full optimal support, every proper
  active prefix exposes exactly its next vertex;
- for sufficiently small objective-gap tolerance, literal ASPR makes exactly
  `|S*|` APGD calls and has restricted-solve work
  `Omega(|S*|^2 / sqrt(alpha))`;
- literal fresh-gradient discovery separately costs `Omega(|S*|^2)` on the
  same family;
- these bounds match the two structural products in the published ASPR upper
  bound up to logarithms;
- the quantitative scaling `alpha = |S*|^{-2}`, `rho = alpha / 100`, and
  `eps_obj = 10^{-4} alpha^2` gives
  `Omega(|S*|^3 log |S*|)` ASPR work versus
  `O(|S*|^2 log |S*|)` FISTA work at the same tolerance, while the 2026
  leaf-star lower bound gives the opposite separation when FISTA activates a
  high-degree center;
- the post-COLT official Julia repository generally plots default ASPR faster
  than its FISTA and ISTA baselines, with CASPR fastest, so those plots are not
  evidence that default ASPR is empirically slow;
- in official commit `3a169eb`, the periodic boundary-gradient option deletes
  the active-to-boundary cross block before evaluation. Its early-discovery
  flag is therefore inert on RPPR and the periodic variants only add work;
- the same implementation's in-place retraction fails to clip entries in
  `(0, delta)`, and the baseline support filter performs an `O(n)` complement
  allocation outside the stated local work model;
- a corrected early-discovery method still needs one successful event per path
  layer and `Omega(|S*|^2)` work under fresh-prefix scans, although the current
  proof does not retain the per-stage `1 / sqrt(alpha)` inner lower bound for
  that variant.

Scope boundary:

- the lower bound is for literal ASPR, not every accelerated local solver;
- the sufficiently small accuracy is an objective-gap target and is not
  identified with APPR, PPR infinity error, or the experimental proximal
  fixed-point residual;
- an algorithm-independent local-oracle lower bound remains open.

## 2026-08-13: composite AESP-CD inner oracle proved

The standalone note `manuscript/notes/aesp_cd_l1_rppr/` uses the shared RPPR
objective and analyzes a local proximal-coordinate inner method with
degree-weighted update cost.

Closed statements:

- the minimum-magnitude composite KKT map is one-Lipschitz in each untouched
  coordinate's smooth gradient;
- every exact proximal coordinate update decreases weighted KKT mass by the
  factor `2 * (alpha + kappa_A) / (1 + alpha + 2 * kappa_A)` times the updated
  violation, including zero hits and sign crossings;
- the degree-normalized KKT diagnostic divided by the shifted strong-convexity
  constant certifies degree-normalized solution error;
- both results extend to any separable `l1`-regularized Stieltjes quadratic
  `H` that admits a positive supersolution `H v >= mu v`, with coordinate
  contraction factor `(H v)_i / (H_ii v_i)`;
- thresholded sequential updates have work at most
  `C_t(z_0) / (tau_cd * eps_in)` and give an explicit objective-gap inner
  oracle; for `kappa_A = 1 - 2 * alpha`, `tau_cd = 2/3`;
- consequently, composite AESP can use this oracle from its signed
  extrapolated centers, with cumulative inner work at most
  `3 / (4 * (1 - alpha)) * sum_t C_t(y_(t-1))^2 / phi_t`;
- the raw absolute-gap functional cannot be controlled pointwise by outer
  objective error: minimum KKT mass is discontinuous when a nonzero coordinate
  approaches an `l1` kink;
- the standard composite Catalyst proximal warm start smooths this
  discontinuity, and greedy normalized-KKT coordinate selection contracts
  mass exponentially in degree work on a fixed envelope of volume `V`;
- with Catalyst's relative criterion C2, every inner stage costs
  `O_tilde(V)`, so a certified envelope gives total
  `O_tilde(V / sqrt(alpha))`; an optimal-support oracle specializes this to
  `O_tilde(1 / (rho * sqrt(alpha)))`;
- the actual full-graph heap implementation needs no support oracle and has
  trajectory-dependent work
  `O_tilde(V_exp_max / sqrt(alpha))`, where `V_exp_max` is the largest degree
  volume explored by one stage; every newly nonzero KKT key is locally exposed
  by a touched coordinate or one of its neighbors;
- if a proximal center is a certified lower solution, Stieltjes comparison
  traps its exact shifted minimizer, proximal warm start, and every greedy
  coordinate iterate below the RPPR optimum; no KKT key outside the optimal
  support activates, so that entire safe-centered call costs
  `O_tilde(1 / rho)` without a support oracle;
- any signed finite-support trial point can be converted locally into a lower
  certificate by subtracting its maximum normalized negative one-sided
  residual and clipping at zero; this makes the safe-center result directly
  applicable to accelerated trial points, but does not itself prove that
  repeated retraction preserves acceleration;
- zero-start coordinate descent for unshifted RPPR recovers the standard
  `O(1 / (alpha * eps_kkt))` degree-work scale.

Scope boundary:

- the diagnostic remains note-scoped and is not identified with the source
  proximal fixed-point residual or a repository stopping rule;
- the result closes the composite inner-locality conjecture but not the
  oracle-free graph-uniform accelerated theorem: start-mass interaction is now
  closed both on a fixed certified envelope and in terms of realized explored
  volume; safe lower centers also enforce `V_exp_max <= 1 / rho` for each
  inner call. What remains open is an accelerated outer continuation whose
  centers retain this order safety, or an amortized safeguard that corrects
  unsafe extrapolated centers without repeated acceleration restarts.

## 2026-08-12: volume-gated RPPR acceleration and expanding-subspace lemma

Recorded as a standalone note in
`manuscript/notes/volume_gated_acceleration/`. The note reconstructs the
active-volume flattening discussion and separates the spider's spectral
behavior from support-growth and repeated-scan work.

Closed statements:

- every principal restricted PageRank system has condition number at most
  `1 / alpha`; on a depth-`L` spider prefix the exact scale is
  `Theta(1 / (alpha + L^(-2)))`, so the spider obstruction is geometric
  rather than a local condition number of order `1 / alpha^2`;
- exact PPR has a degree-volume-`1 / tau` superlevel core whose Dirichlet
  restriction is `tau`-accurate in degree-normalized infinity norm;
- fixed RPPR regularization gives support volume at most `1 / rho` and PPR
  error at most `rho`;
- an arbitrary signed restricted candidate can be corrected to a safe lower
  envelope; one-sided KKT violations then admit only true-support vertices,
  and the absence of such violations certifies normalized infinity error;
- choosing `rho = tau = epsilon / 2` proves peak working volume at most
  `2 / epsilon` and final PPR error at most `epsilon`;
- an endpoint-source path forces
  `Omega(log(sqrt(alpha) / rho) / sqrt(alpha))` one-vertex expansions,
  refuting the claim that support changes can always be grouped into only
  `O(log(1 / epsilon))` ordinary restarts;
- the exact expansion gain is a Schur-complement quadratic. Its elementary
  bound is a lower bound, not the upper perturbation bound required for
  accelerated stability;
- continuous restricted re-solving costs telescope to
  `O(log(1 / epsilon) / sqrt(alpha)) + N_exp` full iterations.

Open item:

- the graph-uniform `O_tilde(1 / (rho * sqrt(alpha)))` work theorem requires
  a one-sided projected continuation lemma over safely expanding subspaces, or
  the weaker ability to charge expansion overhead only to newly admitted
  degree volume. The note does not close the separate AESP--LOCSOR promotion
  gate and does not promote the universal bound into the active manuscript.

## 2026-08-12: rigorous AESP--LocGD center-star lower bound

Recorded as a standalone note in
`manuscript/notes/aesp_locgd_star_lower_bound/`. The note reconstructs the
complete proof development for the literal AESP-PPR outer loop with the
batched LocGD inner solver and uses the AESP paper's cumulative active-volume
work measure.

Closed statements:

- on the center-seeded star `K_{1,B}`, every nonempty batched LocGD call costs
  at least `B`, and every `epsilon`-accurate output requires
  `Omega(B / sqrt(alpha))` work whenever `B * epsilon <= 1/4`;
- choosing `B = floor(1 / (4 * epsilon))` gives the unconditional lower bound
  `Omega(1 / (sqrt(alpha) * epsilon))` for this literal algorithm;
- under an edge budget `m`, the construction gives
  `Omega(min(m, 1 / epsilon) / sqrt(alpha))`;
- if unit outer-loop overhead is counted in addition to active volume, the
  first nonempty call contributes a separate
  `Omega(log(B / alpha^2) / sqrt(alpha))` delay in the small-`alpha` regime.

Proof correction and scope:

- leaf symmetry rigorously forces a full center or leaf-block scan, but it does
  not imply the proposed signed residual cone;
- the unconditional proof instead uses the first nonempty activation to bound
  every later subproblem's slow-mode error, followed by a positive
  Green-function calculation for the critically damped outer recurrence;
- the theorem does not apply to arbitrary AESP inner maps, sequential
  LocAPPR, RPPR, or every hybrid local method, and therefore does not by itself
  close the AESP--LOCSOR publication gate above;
- no polynomially larger AESP-LocGD lower bound is currently proved. A
  multiscale spider, star-of-stars, or clustered lollipop would have to force
  transient explored volume beyond the `O(1 / epsilon)` significant-output
  scale.

## 2026-08-12: black-box tradeoff and composite RPPR extension

The standalone note in `manuscript/notes/hybrid_aesp_locsor/` now includes the
latest parts of the project discussion rather than treating the 2026 RPPR paper
only as structural evidence.

New closed statements:

- for every finite handoff, total work is bounded by Phase-I work plus the
  smaller of the objective-gap and weighted-gradient-mass LOCSOR tails;
- using the direct AESP inner amortization and optimizing the objective handoff
  gives an instance-wise
  `O(R / (alpha^(3/4) * epsilon))` inner-plus-tail bound;
- this Path-I result is unconditional with respect to graph structure,
  confinement, and residual signs, but remains parameterized by the realized
  AESP ratio `R` and excludes uncharged outer initialization work;
- the RPPR unit-step proximal map is a `(1 - alpha)` contraction in
  degree-weighted infinity and one norms;
- its fixed-point residual divided by `alpha` certifies solution error;
- a finite composite Catalyst burn-in followed by full ISTA is therefore
  unconditionally convergent from every handoff.

The three proof paths are now separated explicitly:

1. black-box AESP/SOR balancing: closed and `R`-parameterized;
2. early locality/support confinement: conditionally gives
   `O_tilde(1 / (sqrt(alpha) * epsilon))`;
3. KKT-slack cumulative boundary charging: the abstract charge is proved, but
   a shifted-subproblem margin and a localized inner path-length lemma are
   still missing for AESP.

For RPPR, correctness is no longer the open point. The open point is the
`O_tilde(1 / (rho * sqrt(alpha)))` degree-work theorem from an arbitrary
accelerated warm start. Zero-start support monotonicity cannot be silently
reused after Catalyst overshoot.

## 2026-08-12: rigorous AESP--LOCSOR synthesis

Recorded as a standalone note in
`manuscript/notes/hybrid_aesp_locsor/`. The note reconstructs the project
conversation in a common PageRank normalization and separates source results,
new proofs, conditional statements, empirical observations, corrections, and
open claims.

Closed statements:

- after any finite valid AESP handoff, local SOR with fixed
  `0 < omega < 2` terminates under the final degree-normalized gradient
  certificate;
- with the proof-safe tail `omega = 1`, an objective-gap handoff
  `f(x_J)-f* <= alpha^(3/2) * eps / (1+alpha)` gives tail work
  `O(1/(sqrt(alpha) * eps))`;
- the weighted-gradient-mass handoff
  `||D^(1/2) grad f(x_J)||_1 = O(alpha^(3/2))` gives the same tail order and
  bounds every tail active-set volume;
- the complete hybrid has a trajectory-dependent bound
  `O~(Lambda_J/sqrt(alpha)) + O(1/(sqrt(alpha) * eps))`.

Corrections and open item:

- the universal signed weighted-`l1` monotone SOR range is
  `0 < omega < 1+alpha`, not all of `(0,2)`; objective descent still holds on
  `(0,2)`;
- the graph-uniform target total work follows if the early AESP locality
  factor satisfies `Lambda_J = O(1/eps)`;
- that early-locality statement is not proved for every graph. The note gives
  a support-envelope lemma and an explicit no-percolation condition under
  which it does hold, and explains why the 2026 RPPR/FISTA support results do
  not transfer automatically to unregularized AESP.

The note is intentionally not input by the active manuscript while the
repository-wide residual convention remains open.

### Publication gate

Keep `manuscript/notes/hybrid_aesp_locsor/` as a rigorous standalone research
note; do not promote its graph-uniform end-to-end complexity claim into the
active paper until one of the following is established:

1. the central early-AESP locality lemma
   \[
   \Lambda_J
   := \max_{1\leq t\leq J}
      \frac{\overline{\operatorname{vol}}(S_t)}{\gamma_t}
   = O(1/\epsilon),
   \]
   with a graph-independent hidden constant; or
2. a correct weaker structural condition or alternative burn-in work argument
   that is sufficient for the paper's stated theorem.

Until this gate is closed, paper-facing statements may use the proved
trajectory-dependent theorem and explicitly conditional confinement
corollaries, but must continue to label the universal
`O~(1/(sqrt(alpha) * epsilon))` work bound as open.

## 2026-08-02: APPR worst-case work is `Theta(1/(alpha * eps))`

Recorded in `manuscript/sections/appr_lower_bound.tex`. The classical ACL
upper bound `O(1/(alpha * eps))` is worst-case tight, witnessed by the
center-seeded star `K_{1,m}` with `m = floor(1/(8 * eps_appr))`, for every
legal active-vertex ordering. This fixes the baseline that the hybrid solver
must beat and identifies the two obstructions to attack:

1. the `1/alpha` factor, from settling only an `alpha`-fraction of pushed
   residual per push;
2. the `1/eps_appr` factor, from repeatedly rescanning a
   `Theta(1/eps_appr)`-degree vertex.

Any hybrid or accelerated method claiming a better worst-case bound must break
at least one of these; a `sqrt(alpha)`-type acceleration attacks (1) only.

Implementation status and open items:

- `src/baselines/appr.py` now provides a controlled reference implementation
  with exact degree-weighted work accounting and four legal active-vertex
  orderings. `tests/test_appr_lower_bound.py` makes the star a regression test
  and cross-checks FIFO output against the Numba kernel after repairing its
  missing self-reactivation queue step. The reproducible diagnostic entry
  point is `uv run python -m experiments.check_appr_lower_bound`; it records
  graph, `alpha`, `eps_appr`, source, random seed, stopping rule, ordering, and
  code version. Its path and long-spider rows are explicitly not theorem
  checks.
- Whether a path or long spider is tight in the coupled regime
  `L = Theta(1/eps)` with `alpha * L^2 = O(1)` is left open; the star needs no
  such coupling.
- The lower-bound checker enforces the theorem regime
  `0 < eps_appr <= 1/16`; out-of-regime values are rejected rather than
  reported as theorem checks. The figure generator validates the complete
  `(alpha, eps_appr, ordering)` grid before plotting actual or scaled work.
- The relation between `eps_appr` and the RPPR sparsity parameter `rho` is
  deliberately not asserted. Both bound support volume, and settling it is a
  prerequisite for a fair APPR-versus-RPPR work comparison.
