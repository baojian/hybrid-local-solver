# Bounded dyadic corrector: implementation and exact verification

The new `bounded_dyadic_corrector.py` implements the **exact-neighbor-sum**
variant of `bounded_dyadic_realization.md`. The original exact correctors and
continuation wrappers remain unchanged. This file does not implement a full
rounded continuation or the optional scalar-only approximate-sum rebase.

Its analytical interface requires a safe dyadic baseline below the stage
optimizer. The constructor checks nonnegativity, mass, and source bounds,
but does not independently solve an obstacle problem to certify containment.

## 1. Persistent state and actual rounded iteration

All stored X, kinetic z, scale sigma, and neighbor sums L/M are dyadic. At
the start of a step, `xi_i/w_i=sigma*X_i` and `1/2<=sigma<=1`. The exact
neighbor sums are

`L_i=sum_(j adjacent to i) X_j`, `M_i=sum_(j adjacent to i) z_j`.

The response is recovered from these sums using

\[
 ((Q-\mu I)X)_i/w_i=(q_0-\mu)X_i-cL_i/d_i,
 \qquad \mu=\theta^2.
\]

This gives the exact raw-key formula for the actual stored state; no
recursively accumulated rational response is retained. The source is
computed by scanning only the dyadic baseline support and its boundary.
The grid is chosen fine enough to contain the supplied baseline densities.

The production reporter finds the exact box/mass threshold with the same
two translated, rank-ordered breakpoint searches as the independently
audited exact reporter. It then traverses the **closed** tail

\[
 K_i\ge(\lambda/\theta+\eta+h)/\sigma.
\]

It emits exactly those coordinates whose ideal projected density is at
least h, and immediately floors that density to the h-grid. Equality at h
must be included. Sub-grid positive ideal coordinates are neither enumerated
nor scanned. Since h is smaller than the box upper bound, upper clipping
does not alter this selection equivalence.

After removing every old sparse exception, the implementation computes

\[
 \sigma'=\lfloor(1-\theta)\sigma\rfloor_h,
 \quad X_i'=\left\lfloor X_i+\theta p_i/\sigma'\right\rfloor_h
 \quad(i\in\operatorname{supp}p).
\]

It scatters the **actual** stored change `X_i'-X_i`. The selected adjacency
pass simultaneously builds the exact kinetic neighbor sums, so each emitted
row is scanned once. Source/kinetic exceptions are installed only after all
scale, vector, and response changes are complete.

If the new scale is below one half, a charged rebase floors every historical
X entry after multiplying by that scale, sets sigma to one, rebuilds neighbor
sums from the retained positive entries, and refreshes every exposed base
key, including records whose old response has vanished. Input records that
round to zero are charged, though their now-unneeded adjacency is not scanned.

These are exactly the downward perturbations in the supplied theorem:

\[
 0\le p_0-p<hw,\qquad
 0\le(1-\theta)\xi+\theta p-\xi'\le10hw.
\]

The implementation keeps the exact-sum mode. It does not silently replace
rebase scans by independent scalar rounding of neighbor sums.

## 2. Grid and fixed-block stopping certificate

The default grid is a reciprocal power of two satisfying

\[
 h\le\min\{1/8,\theta\tau/256,\theta\alpha^2r/27\}.
\]

It is also refined if necessary to represent every supplied dyadic baseline
entry. The extra `theta*alpha²*r/27` restriction ensures the support-work
condition even for a loose standalone tolerance. The prescribed continuation
tolerances already imply a sufficient restriction of this type.

The reported error floor is `Gamma<=27h/theta`. The block length is the
integer `m=1/theta`, and the number of blocks is the smallest q satisfying
`2^q>=2/tau`, found by doubling. The corrector takes exactly `m*q` steps.
After each completed block it halves its certified decay bound; no exact
product `(1-theta)^k` is retained. Between block endpoints the preceding
completed-block bound is still conservative. At completion,

\[
 \operatorname{gap}(\xi)\le2^{-q}+\Gamma<\tau.
\]

Here the initial energy bound one uses the safe-baseline interface, as in
the exact wrapper. The separate perturbed theorem then supplies
`sum vol(supp z)<=180K/r` and the rebase-count bound `4theta*K+1`.

## 3. Structural charges and arithmetic measurements

The metrics separate baseline, selected-support, and rebase adjacency
entries. Every first oracle read and every repeated cached-entry inspection
is charged. Source refreshes, emitted records, historical rebase input
records, all-exposed-key rebase passes, key changes, tree visits, projection
queries, blocks, and grid-selection halvings are also recorded.

For the exact-sum implementation, total response scans are exactly

`baseline scans + selected-support scans + rebase scans`.

Normal steps do not iterate the entire historical X, L, degree, or key maps.
Rebases deliberately do iterate historical/exposed state and pay for those
passes. The union of historical primal rows is bounded by the emitted
history, so the separately proved logarithmic number of rebases gives the
announced allowed overhead.

`ArithmeticTracker` measures reduced rational operands/results of the
explicit numerical representation and reporter, including weighted AVL
moments, threshold expressions, grid divisions, and exact comparison
cross-products. It separately measures dyadic state sizes and integers.
The tracked-rational adapter uses exact Fraction arithmetic; it does not
instrument CPython's internal gcd/division implementation or claim that
each Python operation has unit bit cost. Pure scheduling and bookkeeping
operations are structurally counted, rather than presented as a complete
interpreter trace.

The arithmetic audit `bounded_dyadic_arithmetic_audit.md` gives the common
weighted-key denominator: for `alpha=A/D`, `theta=1/T`, `h=1/H`, and
`sigma=S/H`, it divides `2DH(T+1)S`. Vertex-degree denominators cancel in
weighted moments. The old-exception removal order in this implementation
prevents moment sums from mixing successive scale denominators. No projected
coordinate's fresh exact division denominator survives its immediate floor
into the next stored vector.

## 4. Independent exact tests

All four test groups in `test_bounded_dyadic_corrector.py` passed. Results
are in `bounded_dyadic_corrector_verification.json`.

* Five deterministic dense trajectories are compared at all 292 steps
  against a separately coded rounded recurrence. They include rational alpha
  different from theta squared and a nonzero dyadic baseline.
* Every step checks the exact raw-key identity, rounded X/z/scale, both exact
  neighbor sums, both perturbed one-step energy inequalities, downward error
  bounds, feasibility, Q-error bound, and graph-entry reconciliation.
* There are 53 audited rebases, 94 genuinely nonzero scale-floor events,
  447 selected-update floor events, and 58 rebase-rounding events across the
  dense trajectories. Thus the tests exercise actual rounding, not merely
  dyadic formulas that happen to remain exact.
* Eighty-seven reporter fixtures cover exact h ties, sub-grid values, cap
  equality, binding caps, simultaneous upper clipping and mass constraints,
  and an empty reporter. A separate injected feasible binding-cap state is
  compared against one exact dense rounded step; its zero-start reachability
  is not asserted.
* A reporter coordinate of degree `2^80` has ideal projected density `h/2`
  with `h=2^-100`. It is not emitted. The exact h-tied degree-one coordinate
  is emitted. This query takes five tree visits and performs no graph scan.
* In a 1,001-vertex star, a leaf-seeded stage and all its rebases query only
  the seed/hub degrees. Only the seed adjacency is read; the degree-1,000 hub
  remains unscanned. The reference optimum is independently checked through
  its scalar KKT conditions rather than by constructing a huge dense matrix.
* A normal non-rebase step succeeds with iteration of historical X/L/degree/
  key maps explicitly prohibited by test wrappers.

For the 208-step alpha=`1/100` trajectory, h=`2^-25`. Measured rational
numerators and denominators stay within 59 bits, comparison products within
116 bits, and persistent dyadic denominators within 26 bits. The stage has
18 rebases and 36 rebase adjacency-entry inspections, all charged. This is
finite evidence for the bounded-coefficient implementation, complemented by
the separate denominator proof; it is not an empirical substitute for that
proof or a universal running-time benchmark.

No full rounded continuation has been implemented in this subtask. Its final
PG repair must still be formed from the actual candidate by an exact charged
support scan; the existing standalone PG helper provides that separate
interface.
