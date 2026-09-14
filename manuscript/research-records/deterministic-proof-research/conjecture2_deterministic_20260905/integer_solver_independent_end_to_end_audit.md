# Independent end-to-end audit of the integer solver

Status: passed on the audited snapshot. No discrepancy was found between
the implementation and the bounded scalar-rebase theorem under its stated
graph and safe-baseline contracts. This audit did not alter implementation
files. Its separate checker and exact evidence are
`audit_integer_solver_independent.py` and
`integer_solver_independent_audit_results.json`.

Audited SHA-256 snapshots:

- `integer_dyadic_rppr_solver.py`:
  `fd81d6a246f05e1f92f520179a19f9171baaf058ea2535b6b1561d0bbbad4d44`
- `integer_clipped_reporter.py`:
  `ef51b8ba9eca62ee6e6570a315051f67f28507130befc77cc706dd2c9c37f794`
- `deterministic_avl_containers.py`:
  `f737e7e8f6e2fc837ca9888463788fa6741d964fc53fa07c1a59fc77c6d0acef`

## 1. Formula and stage audit

`IntegerDyadicCorrector` implements the integers in
`integer_two_tree_reporter_audit.md`. Its `G=2*D*H^2*(T+1)` is the common
physical denominator `H*C0`; `_base` is exactly the proposed base numerator.
`_install_exceptions` uses the positive kinetic expression and the exact
source numerator, then multiplies the base by the current S and the
exception by H. The resulting raw density is correct for the actual
represented primal neighbor records, including their certified rebase error.

The initial source numerator equals

    2*A*H*1_seed-(D+A)*d_i*P_i+(D-A)*B_i.

Its implemented upper-bound comparison is exactly the density condition
`s_i/w_i<=4*alpha*r`. The check
`sum(source_numerators)==2*A*cap_count` is precisely the weighted source
mass identity. Thus `mass_cap=cap_count/H` is the exact source-mass cap,
not an approximate estimate. Baselines are placed on a common dyadic grid:
the chosen reciprocal power-of-two grid represents every supplied baseline
density exactly.

The scale update `(T-1)*S//T` is `floor_h(a*sigma)`. The normalized X-count
increment `H*count//(T*new_S)` is exactly the required floor of the kinetic
addition; its old normalized count is already an integer. Actual integer
increments, rather than intended unfloored increments, are scattered to L.
The current kinetic neighbor map M is rebuilt exactly from the newly emitted
kinetic counts.

The grid ceiling provides both `Gamma<tau/8` and `Gamma<=alpha^2*r`. Its
extra `theta*alpha^2*r/29` ceiling makes the latter true even for a direct
stage call with a larger allowed tolerance. It also keeps the raw error
within the selected residual margin. The fixed block schedule supplies
`a^K<=tau/2`, and the certificate `2^(-completed_blocks)+Gamma` is valid
throughout a block as a conservative decay bound.

## 2. Exceptions and scalar rebases

Every old exception is moved into the base tree before S changes. The
primal update then changes only touched base records; a rebase rebuilds
all exposed base records. Finally all new exceptions, including static
source exceptions, are installed using the final new S. Therefore no stale
exception numerator or old exception ordering survives a scale change.
The registry gives exactly one owner per exposed vertex.

The rebase computes new X and L maps independently from their old values,
using integer floors. It does not scatter rebased X differences, and it
does not scale current-kinetic or baseline neighbor sums. This is precisely
the audited recurrence with `|L_i-sum_neighbor X|<=4h*d_i`. Its exposed-key
rebuild is explicit and counted; no assumption that rounded keys retain
their old order is made. No adjacency method is called in `_rebase`.

## 3. Reporter audit

The two trees store integer ratio numerators, degrees, labels, and integer
weighted subtree sums. Ratio comparison is by integer cross multiplication.
Insertions, removals, successor replacement, rotations, and moment refresh
maintain the disjoint ordered AVL invariants.

`_scaled_mass` is exactly the difference of the two positive tails. Its
returned slope uses the right derivative: a coordinate at an upper-box
breakpoint is included in the free slope, while a zero breakpoint is
excluded. This is the correct convention for solving from the lower end of
the final affine interval.

`_threshold` searches the four ordered breakpoint sequences separately.
Each binary-search iteration performs one O(log N) rank access and at most
one O(log N) mass query, so the full cost is O(log^2 N). Every discarded
rank interval lies outside the current root bracket; subsequent bracket
shrinking preserves that fact for previously searched sequences. After
all four passes, no breakpoint lies in the open bracket, justifying the
single affine root solve. Equal masses, empty trees, exact ratio ties, and
zero mass cap are handled explicitly.

Emission uses the closed threshold `q+grid*G`, then performs integer floor
division. Thus equality at one grid unit is retained, and sub-grid ideal
projection entries are never enumerated. The two output tails are disjoint.
No per-emitted-coordinate Fraction construction is needed.

## 4. Wrapper and exact terminal repair

The wrapper's stage regularizations and deltas match the theorem. Every
stage requests `tau=alpha*delta^2/8`; its grid is checked against
`delta/2` and `alpha*r/4`. The terminal incoming numerator is exactly

    alpha*1_seed+c*d_i*f_i+c*sum_neighbor f,

so dividing by d_i and subtracting `alpha*r` gives one exact projected-
gradient step from the actual full candidate. It does not reuse approximate
L as an exact gradient. The code scans only candidate rows, computes all
affected PG values, and clips before inspecting any newly positive PG row.
The retained density is floored to the stage grid and maximized with the
old baseline on that same grid.

The safe-source, containment, and `2*delta` repair conclusions therefore
apply. The next source satisfies the factor-four stage interface, and the
final reported bound `2*delta^2/r` is at most epsilon. The zero-regime and
alpha-one shortcuts are algebraically correct and use no adjacency scan.

## 5. Access and arithmetic accounting

Only baseline rows and newly emitted kinetic rows are scanned during a
stage. Each row is cached after its first oracle read. Repeated cached
entries are counted separately, with selected-entry count exactly equal to
the cumulative kinetic degree-volume. Source neighbors require only degree
queries and sparse records. Scalar rebase work is charged by exposed-record
counts and reporter point operations. Final materialization and PG are
charged to the baseline/kinetic history.

The degree-query count reconciles with one wrapper query, all stage queries,
and terminal repair queries. First adjacency entries reconcile with the
independent oracle. First oracle returns and cached entry scans are separate
metrics; summing both gives the corresponding two physical traversals when a
new row is first materialized and then consumed.

The correction, neighbor, source, baseline, scale, and per-vertex reporter
records are integers throughout iteration. Fractions remain in fixed scalar
parameters, the scalar waterfill search, certificates, and the one terminal
materialization/repair. This is the advertised scope of integer-only point
updates; it is not an assertion that the entire program contains no Fraction.

Reporter comparison/tree-visit counters do not instrument the additional
registry and point-map AVL lookups. They are structural telemetry, not a
literal count of every machine or mathematical operation. Those lookups
have the proved O(log N) worst-case implementation and fit the same charged
loop bounds. No bit-size maximum is silently measured on every iteration.

## 6. Independent executable evidence

Six full wrapper fixtures (path, star, cycle, barbell, grid, tree-clique)
covered 15 stages and 1,370 iterations. The checker used its own exhaustive
rational KKT oracle and edge-form objective, rather than the implementation's
reference trajectory. It verified:

- 2,740 individual energy inequalities: both E and B at every step;
- the actual squared Q-error bound at every step;
- exact raw recomputation, including the primal-neighbor error, followed by
  an independently enumerated dense clipped projection;
- 1,385 integer-state/feasibility checks and 4,556 reporter-record checks;
- all source/cap identities, integer AVL moments and balance, and disjoint
  base/exception ownership;
- 401 scalar rebases, their neighbor-error invariant, and zero rebase
  adjacency accesses;
- exact final objective gap, containment, monotone repaired baselines,
  mass-deficit repair bounds, and graph-access reconciliation.

A dynamic guard on Fraction arithmetic and comparison methods passed all
1,370 steps: none occurred in iterative point updates outside the scalar
projection query. The largest inspected stored integer was 83 bits on these
fixtures. This is an observation about stored state, not a bound on every
temporary or all future inputs.

None of these six warm trajectories bound the mass cap. To keep that scope
honest, a separate 16-case generic reporter audit exercised 15 binding roots,
zero cap, mixed tree ownership, changes of scale, and exact closed-tail/ratio
ties. These are reporter-contract fixtures, not claims of reachability from
zero in the full solver.

The audit confirms this fixed-block integer implementation. A different
source-energy schedule or a packaged transcription requires its own audit;
their correctness is not inferred from these tests.
