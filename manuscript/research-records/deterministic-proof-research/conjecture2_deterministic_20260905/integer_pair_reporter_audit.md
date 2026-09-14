# Integer-pair clipped reporter: implementation, proof, and bounded study

The separate `integer_pair_clipped_reporter.py` implements the same exact projection as the stable integer-moment reporter, with unreduced integer pairs throughout the root searches. It inherits the existing deterministic AVL point updates without changing the stable reporter, solver, or package. `integer_pair_dyadic_rppr.py` provides isolated solver bindings for equivalence checks; enabling them in a deliverable remains a separate integration decision.

## Shared denominator lifting

Let the old common denominator be G and the four rational globals be shift, upper U, cap C, and grid h. For each reduced denominator d, form `d/gcd(d,G)` and take their least common multiple M. Then each of `shift*G*M`, `U*G*M`, `C*G*M`, and `h*G*M` is an integer. This uses only four shared denominators; no vertex degree is included in the least common multiple.

Set `G'=G*M`, base scale `S'=S*M`, exception scale `M`, and integer globals `initial=shift*G'`, `width=U*G'`, `target=C*G'`, `step=h*G'`. For each record the transformed ratio divided by G' is exactly its original physical ratio divided by G. The projection is therefore unchanged. The implementation accepts the same positive dyadic grids as the stable reporter, including dyadic grids whose numerator is greater than one.

## Integer mass queries and root

Represent q by `(qn,qd)` with `qd>0`, without reduction. The strict lower and upper tails use thresholds `(qn,qd*scale)` and `(qn+width*qd,qd*scale)`. If their combined weighted moments are `(Dl,Nl)` and `(Dh,Nh)`, then

`mass(q)*qd = (Nl-Nh+width*Dh)*qd - qn*(Dl-Dh)`.

Thus comparison against the scaled target uses `target*qd` entirely in integers. The right slope is `Dl-Dh`. Strict upper tails are correct at equality: a record exactly at q+width contributes width through the lower tail rather than the upper tail and belongs to the derivative for increasing q.

The four sorted breakpoint sequences are `(scale*n-translation*d,d)` for the two trees and translations zero and width. Integer cross multiplication supplies their exact order and all bracket comparisons. The same four binary searches as the existing proof remove every breakpoint from the bracket's interior. At a detected equality, the breakpoint itself is a valid multiplier; this includes plateau endpoints. When the cap is zero, the maximum ratio gives a zero-mass solution. If the cap is inactive, the initial threshold is returned.

In the remaining affine interval let `intercept=Nl-Nh+width*Dh` and `slope=Dl-Dh>0`. The final root is constructed directly as

`q=(intercept-target,slope)`.

It is deliberately not computed by repeated arithmetic on the old pair. The direct construction discards its previous denominator and prevents denominator growth with search length. The exact root is checked against both bracket endpoints.

## Closed-tail emission and integer grid counts

The rounded density is positive exactly when `scale*n/d >= q+step`. The inherited inclusive tail query uses `(qn+step*qd,qd*scale)`, retaining exact grid ties while leaving sub-grid positives unmaterialized. For every emitted record the returned count is

`min(width//step, (scale*n*qd-qn*d)//(step*d*qd))`.

All terms are integers. `width//step=floor(U/h)`, so the formula remains correct when U is not a grid multiple. The only returned Fraction is the interface multiplier

`(qn-initial*qd)/(qd*G')`.

Scalar input normalization also uses Fractions. There is no Fraction construction, rational arithmetic, or gcd inside breakpoint or mass searches or per-entry floors.

## Complexity and bit sizes

The query retains O(log^2(N+2)) tree-search work and O((k+1)log(N+2)) charged emission work for k retained records. Point insertion/removal/moves retain deterministic AVL bounds. Tree layout, selected records, and all existing structural metrics are unchanged by the pair representation.

The lifting integer has at most the sum of the four scalar denominator bit lengths. Every breakpoint pair has denominator one or a single degree; the affine root has denominator at most the total exposed degree. Weighted integer moments have only an additional O(log N) bit factor beyond the largest record numerator/degree. All pair comparisons and mass calculations use a constant number of products and sums of these quantities. Thus intermediate bit lengths are O(encoded scalar bits + grid/state bits + log N + log maximum degree), with a constant factor for unreduced products. They do not grow linearly with the number of root-search iterations or accumulate degree least-common-multiples. This is a derived bound; the standard metrics do not trace every integer multiplication.

For the integer solver's particular globals, grid and cap denominators divide the grid-based G already. Any additional lift is controlled by the stage regularization denominator. The generic four-global lifting rule still handles arbitrary valid rational shift/upper/cap inputs.

## Exact tests

`test_integer_pair_clipped_reporter.py` and `integer_pair_reporter_verification.json` record six passing test groups:

- The existing 3,946 independent dense projection cases, including caps, upper clipping, ties, empty trees, plateaus, moves, and coprime degrees.
- All 2,400 mutation states and the 8,192-record sub-grid rejection fixture from the stable suite; the latter still visits only 44 tree nodes to emit its one retained record.
- 192 additional exact comparisons with the original reporter, including full returned multipliers and all structural metric fields, positive/negative shifts, nontrivial shared denominator lifting, and huge integer labels/degrees.
- Four direct root searches with both Fraction construction and gcd explicitly forbidden during the search.
- 503 checks that every queried pair denominator is bounded by the exposed degree sum.

The dense oracle computes the weighted box projection by an independent explicit breakpoint scan. The tests include grid `3/64`, so they do not rely on reciprocal-power-of-two grids alone.

`study_integer_pair_reporter.py` and `integer_pair_solver_study.json` add 48 exact recurrence-step comparisons, including 31 steps with nonzero scalar neighbor-sum error, and six complete continuation comparisons. These cover both the original and source-energy stage schedules, an asymmetric barbell, and a star with 101-bit vertex labels. Outputs, certificates, all stage fields, and diagnostic/local-work fields match exactly. The adapter uses private copies of fixed-size function namespaces; it does not mutate existing module globals. The source-energy adapter's method-resolution order runs the pair reporter's constructor before applying the unchanged energy schedule.

## Performance interpretation

No other timing job ran concurrently. These are small ABBA studies, not a broad or statistically powered performance claim.

On the actual implicit billion-vertex path with `alpha=1/100`, `rho=1/16`, and `epsilon=10^-6`, both backends took 2,016 iterations and returned identical signatures. Median CPU time was 0.9751 seconds for the existing reporter and 0.9660 for the pair reporter. Median wall time was 0.9811 versus 0.9875 seconds. This is essentially no observed end-to-end change on that fixture.

`benchmark_integer_pair_queries.py` and `integer_pair_query_benchmark.json` isolate 256 binding-cap projections over the same two prebuilt trees with 2,048 records. Each timed run traversed exactly 238,184 tree nodes and returned identical exact results. Median CPU time fell from 0.2044 to 0.1333 seconds; wall time fell from 0.2087 to 0.1362 seconds, about a 1.53 ratio. This synthetic query benchmark shows reduced search arithmetic overhead when searches are substantial. It does not establish that this regime is reached by a particular RPPR trajectory, nor override the flat actual-solver result.

The optimization is mathematically equivalent and has a useful search-level effect, but its practical value depends on the proportion of time spent in binding-cap root queries. Keeping it optional is reasonable until broader representative solver measurements justify integration.
