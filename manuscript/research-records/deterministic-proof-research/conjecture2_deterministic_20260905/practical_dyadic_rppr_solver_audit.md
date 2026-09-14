# Practical dyadic corrector and monotone continuation

The standalone implementation is `practical_dyadic_rppr_solver.py`. Its public
entry points are:

* `PracticalDyadicCorrector(oracle, seed, alpha, theta, rho, tolerance,
  baseline=None, grid=None)` for one fixed-block stage.
* `solve_rppr_practical(oracle, seed, alpha, rho, epsilon)` for complete
  continuation and a final safe-output certificate.

The oracle supplies only `degree(vertex)` and `neighbors(vertex)`. Returned
triples encode exact degree densities and degrees, as in the existing
wrappers. Stage summaries additionally expose the dyadic grid, projection
mass cap, separate projected-gradient charges, scalar-neighbor rebase
counts, grid-repair counts, and baseline-preservation counts.

The original exact-sum dyadic corrector and all original wrappers are
unchanged and remain available. This variant is a bounded exact-rational
prototype; it is not unchecked floating point or a benchmark-based claim
of universal speed.

## 1. Scalar-only rebases and their certified error

Normal selected updates are inherited from the exact-sum implementation:
scatter the actual rounded change in X, and build the current kinetic
neighbor sums exactly during the same selected-row scan. Only the rebase is
different. At its triggering scale `sigma<1/2`, independently set

\[
 X'_i=\lfloor\sigma X_i\rfloor_h,\qquad
 L'_i=\lfloor\sigma L_i\rfloor_h,\qquad \sigma'=1.
\]

The implementation performs scalar passes over X, L, and the exposed keys.
It refreshes every exposed base key. It does not scatter either rebase
change through the graph, and does not alter the exact current-kinetic sums
or the fixed baseline source. Old sparse key exceptions have already been
removed by the inherited step before this rebase starts.

Let `E_i=L_i-sum_(j adjacent to i)X_j`. Normal updates preserve E. At a
rebase, writing both downward rounding losses gives

\[
 E'_i=\sigma E_i+\sum_{j\sim i}\ell_{X,j}-\ell_{L,i}.
\]

Starting from zero, `|E_i|/d_i<=4h` follows by induction because each
triggering scale is below one half. The induced raw-density error is

\[
 u_i/w_i=\frac{\sigma c E_i}{\theta(1+\theta)d_i},
 \qquad |u_i|/w_i\le2h/\theta.
\]

The kinetic and primal rounding bounds remain h and 10h. The independently
audited perturbation theorem consequently gives `Gamma<=29h/theta` and the
conservative total kinetic volume bound `360K/r`. These claims, including
the error recurrence, are audited in section 6 of
`bounded_dyadic_realization_audit_localization.md`, using
`perturbed_q_metric_kinetic_work.md`.

The grid is a reciprocal power of two with
`h<=min(1/8,theta*tolerance/256,theta*alpha²*r/29)` and is further refined
to represent the dyadic baseline. The original fixed-block schedule is
retained. The resulting final stage gap is strictly below its tolerance.

The approximate L is never used for end-stage certification or repair:
projected gradient is recomputed exactly from the actual full candidate.

## 2. Exact remaining-mass cap

The source is evaluated exactly from the safe baseline. The known cap is

\[
 \eta=\frac{w^Ts}{\alpha}=1-w^T\bar x.
\]

`SourceMassReporter` uses this exact scalar in place of the unit correction
mass cap. The ordered tree and closed-tail grid reporter are otherwise
unchanged; the already-built tree root is transferred without rebuilding or
scanning its records. Both the analytical comparator `Q^{-1}s` and the true
correction have mass at most eta. On the mass face, the Q-normal contribution
is `multiplier*(alpha*eta-mass(s))=0`, so the same comparison proof applies.

All stored corrections and kinetic vectors remain in the eta-capped box.
Consequently the **full** candidate `baseline+correction` has mass at most
one. The code does not approximate eta or silently replace a negative source
by zero. The exact cap and its sector justification are independently audited
in `mass_deficit_cap_and_monotone_repair_audit.md`.

The sharper exact-trajectory constant in that note is not substituted into
this perturbed implementation: the wrapper conservatively records `360K/r`.

## 3. Exact projected gradient, grid repair, and a monotone baseline

The wrapper follows the existing regularization schedule and chooses delta
as before, with additional final halvings until `2delta²/r<=epsilon`. Its
stage tolerance is

\[
 \tau=\alpha\delta^2/8.
\]

After the rounded stage, it uses the separately verified
`projected_gradient_truncate` helper. This scans only the actual candidate
support, forms the exact PG values at affected neighbors, and subtracts
delta before any newly positive PG adjacency could be scanned. It reuses
cached candidate rows where available, while charging the repeated entries.

The positive clipped values are rounded down to the current grid. Finally,
`round_and_preserve_baseline` computes

\[
 \bar x_{\rm new}=\max\left(\bar x_{\rm old},
           w\left\lfloor[y/w-\delta]_+\right\rfloor_h\right).
\]

The tolerance and grid guarantee that the rounded candidate is below the
true optimizer, has `Qbar<=b`, and has density error at most `2delta`.
Nonnegative Stieltjes subsolutions are closed under coordinatewise maximum:
at a row choosing one vector's diagonal coordinate, all other coordinates
only increase and their off-diagonal coefficients are nonpositive. Thus the
maximum remains a subsolution and lies below the optimizer. Its coordinate
error is no larger than the repaired candidate's error.

One then reapplies the same coordinate-error/support argument, rather than
assuming monotonicity of a Q-norm, to obtain

\[
 \bar x_{\rm old}\le\bar x_{\rm new}\le x^*_r,\qquad
 0\le b-Q\bar x_{\rm new}\le2\alpha r w,
 \qquad J_r(\bar x_{\rm new})-J_r(x^*_r)\le2\delta^2/r.
\]

The next source interface is restored, baseline densities and support are
monotone, and their exact mass deficits are nonincreasing. The final output
retains the stated epsilon certificate. The cap/max audit cited above proves
these facts; no true support or optimizer is an algorithmic input.

## 4. Charges and numerical-size interpretation

Every selected-row scatter, baseline source scan, and final PG scan is
charged. Rebase adjacency cost is identically zero in this variant. Scalar
rebases still pay for every X/L record and exposed-key refresh; these full
passes are not presented as free operations. Grid repair and the maximum
with the old baseline have separate scalar-record counters.

The implementation continues to use Python point maps and exact Fraction
arithmetic. The projection tree itself is deterministic AVL. A fully
comparison-balanced point-map implementation is a separate integration
task; the fresh `deterministic_avl_containers.py` component is available for
that purpose. No claim about worst-case Python hash-table time is made.

ArithmeticTracker reports **reduced rational** numerator and denominator
sizes. Those are not the sizes of every unreduced temporary inside Fraction.
For explicit measured rational arithmetic with operands of at most b bits,
addition/subtraction need at most `2b+1` bits for unreduced numerators and
products; multiplication/division need at most `2b`. The diagnostic field
`fraction_internal_arithmetic_bits_bound` records the conservative `2b+1`
envelope using the largest measured rational/integer size, including the
stage-setup operands. It is a derived upper bound for that measured
arithmetic, not an interpreter trace or a claim to instrument every internal
operation of the reused end-stage PG helper. Comparison cross-products are
recorded separately as actual integer products.

The separate common-denominator analysis establishes bounded coefficients
independently of these finite measurements. The scalar-only rebase leaves
all stored X/L/M values dyadic and does not propagate projected-coordinate
division denominators into the next stored state.

## 5. Independent exact verification

All five groups in `test_practical_dyadic_rppr_solver.py` passed. Results are
saved in `practical_dyadic_rppr_solver_verification.json`.

* Four dense scalar-state trajectories compare 258 rounded steps exactly.
  They check X, L, z, scale, raw reporter values, both perturbed energy
  inequalities, feasibility, and graph-entry charges.
* The tests include 43 scalar rebases, nine steps with a genuinely nonzero
  neighbor-sum discrepancy, and eight with genuinely nonzero raw error.
  The uniform `4h` and `2h/theta` bounds hold in every checked coordinate.
* Seven full deterministic cases, with 13 stages and 1,452 correction
  iterations, are compared against an independent exhaustive dense KKT
  oracle. Every candidate gap, PG/grid/max repair, source interface, support
  bound, monotone baseline, and final certificate passes.
* Full candidate mass is checked after every recorded wrapper step and is
  always at most one. An additional feasible injected state makes the
  source-mass cap `eta=15/16` bind exactly. This is an arithmetic fixture,
  not a zero-start reachability assertion.
* A separate valid-baseline fixture starts with the exact dyadic optimum on
  a two-vertex graph. The maximum repair actually preserves two old positive
  coordinates that truncation alone would reduce; the result remains the
  exact optimum. Thus the preservation branch is exercised explicitly.
* A degree-1,000 inactive hub remains adjacency-unscanned through the scalar
  rebases. Every full-wrapper rebase adjacency counter is exactly zero.
  Final PG entry counts equal the actual candidate support volume.

Across the full-wrapper fixtures, measured reduced rational maxima are 90
numerator bits and 92 denominator bits. The standalone 208-step small-alpha
fixture uses at most 59 bits for either reduced component, with derived
arithmetic envelope 119 bits. These are finite diagnostics, not a universal
benchmark or a replacement for the arithmetic-size proof.

No unbounded benchmark was run in this subtask. Original solver files were
not modified.
