# Optional independent early stopping with fully charged cached checks

`early_stop_source_energy_rppr.py` adds independent certificates at geometric checkpoints to the stable source-energy solver. No original recurrence, source-energy schedule, checker, terminal repair, or package file was edited. The prescribed source-energy horizon remains a fallback. The separate exact tests pass, and the bounded timing study shows useful reductions on all three tested fixtures after including checkpoint costs.

## Certificate and stopping rule

Let `f` be the current full candidate density, so its normalized vector is `x_i=sqrt(d_i)*f_i`. Independently recompute the gradient of the original nonnegative obstacle objective:

`g_i/sqrt(d_i) = ((1+alpha)/2)*f_i - ((1-alpha)/2)*sum_{j~i} f_j/d_i - alpha*1_{i=seed}/d_i + alpha*r`.

At positive coordinates take the full gradient; at zero coordinates take its negative part. This is a valid subgradient of the quadratic objective plus the nonnegative-orthant indicator. It has no contribution outside the closed neighborhood of the candidate and the seed. Strong convexity gives `F(x)-F(x*)<=||g_selected||^2/(2alpha)` for every nonnegative candidate. No monotonicity of the accelerated objective or relation to a previous certificate is used.

The imported `certify_sparse_output` reconstructs that norm using integer numerators and an upward squared-sum bound. Its conclusion is independent of the accelerated trajectory. The current candidate densities are dyadic with denominators dividing H^2: the primal is `(S/H)*(X/H)` and the baseline is already on the grid. Hence the checker's largest-reduced-denominator contract holds, and its upward arithmetic is applicable. It may overestimate the true error, which can only prevent an early stop.

For prescribed horizon K and `T=1/theta`, check at `T,2T,4T,...` only while the checkpoint is strictly below K. Stop exactly when the freshly computed bound is **strictly less than tau**. On rejection, destroy the certificate and materialized candidate before the next step. On acceptance, retain only its scalar bound and iteration number, and return that already materialized candidate. The unchanged terminal PG/grid repair then uses the required original-objective gap below tau, exactly as in the fixed schedule.

The accepted scalar is invalidated before any subsequent manually requested step. At zero-step stages and when no earlier checkpoint succeeds, the original energy certificate remains the fallback. Certificates from earlier iterates are never applied to later iterates.

## Why no new graph exposure is required

The full candidate's support is contained in the baseline support and the union of previously emitted positive kinetic coordinates. Every baseline row is scanned during initialization. Every positive kinetic coordinate has its row scanned in the same update that uses it, even if its rounded primal increment is zero. Scanning a row exposes all adjacent degrees. Therefore:

- Every positive candidate row already exists in the adjacency cache.
- Every candidate degree and every affected-neighbor degree already exists in the degree cache.
- The seed degree has been exposed at initialization.

`CacheOnlyOracle` reads those maps directly. A missing row or degree raises an assertion, rather than falling through to the external graph oracle. It counts one logical cached degree lookup, cached row lookup, and every visited cached adjacency entry. Tests reconcile external oracle histories before and after all actual checkpoints and find no new exposure.

## Added-work bound

Let `V_k` be candidate support volume at iteration k, and let `W_k` be cumulative emitted kinetic volume through k. The previous source-energy/perturbed selected-flow theorem applies to every prefix, so `W_k<=360k/r`. Baseline volume is at most `1/r`. Consequently

`V_k <= vol(baseline)+W_k <= (1+360k)/r`.

This counts the whole current candidate; it does not silently ignore old positive primal coordinates or assume their support is kinetic support. Rebased-away coordinates can only reduce the candidate support.

A single checkpoint materializes O(V_k) words/records, scans exactly V_k cached adjacency entries, and touches at most `2V_k+1` affected vertices. Its deterministic AVL point accesses take O(log(N+2)) work each. Integer accumulation, norm construction, and disposal require O(V_k+1) additional scalar/record work up to the established bit costs.

If the completed checkpoints are `k_j=T*2^j`, and `k_actual` is the actual stopping iteration (whether early or at fallback), then `sum_j k_j<2k_actual`. The number of checkpoints is also O(k_actual+1). Thus

`sum_j V_{k_j} <= (J+360*sum_j k_j)/r = O((k_actual+1)/r)`.

After the existing logarithmic factors, this is the proposed added-work bound. The source-energy algorithm still has its separate baseline initialization and stage-final terms. If `k_actual=0`, no checkpoint runs; the adapter adds only fixed-size scalar setup. No charge to a nonexistent zero-step kinetic budget is needed.

The underlying state trajectory is unchanged up to whichever checkpoint accepts. Rejected checks only read state and caches. Hence the prefix energy and selected-flow lemmas remain valid without modification, and the original worst-case OP2 bound survives. Later stage baselines can differ from the fixed schedule because early endpoints differ; the usual safe repair supplies their required interface.

## Operational accounting

The implementation separately reports:

- Candidate materialization input records, returned records/words, three point lookups per emitted full candidate record, union-state reclamation, and total candidate volume.
- Cached degree/row lookups and every cached adjacency entry read.
- Independent checker AVL point lookups, writes, and iterated records, plus affected/output/subgradient records and integer accumulation updates.
- All six temporary checker AVL containers and their reclaimed record counts.
- Failed candidate words/records and discarded certificate scalar fields.

The metered checker reuses the independent checker's exact code with private AVL class bindings in a copied fixed-size namespace. It neither changes the original checker globals nor any graph-state container. Temporary maps are explicitly cleared after each check, including a `finally` path on error. The temporary output support union made by materialization is separately charged as O(number of candidate records) reclamation.

These counters count logical AVL requests and record operations. Tree comparisons, rotations, and scalar arithmetic have the usual constant or logarithmic factor per recorded operation; the counters are not advertised as a literal trace of every Python instruction. Fixed scalar setup and the fixed-size namespace/class construction are O(1) in graph size. The norm's squared statistic uses one common parameter/grid denominator and upward integer divisions, so there is no new degree-denominator least-common-multiple growth.

## Exact tests and branch coverage

`test_early_stop_source_energy_rppr.py` writes `early_stop_source_energy_verification.json`. Four groups pass:

- 52 actual checkpoints, comprising 16 accepted and 36 rejected checks.
- Four complete exact finite graph cases and 18 stages, with dense rational KKT optimum, candidate objective-gap, repaired containment, monotone baseline maximum, and repaired source-interface checks.
- One genuine fallback stage after five failed independent checkpoints, and one zero-step stage.
- Complete reconciliation of external degree/adjacency replies, zero checkpoint cache misses, temporary-state reclamation, and the geometric checkpoint-volume charge.
- A successful bound invalidated before manual stepping, and explicit missing-cache assertions that make no external oracle calls.

The fallback case is not obtained by forcing an artificially loose certificate: it occurs in the five-vertex path with alpha=1/100 and the actual independent norm bound. The tests also cover nonsquare alpha and an asymmetric cyclic graph. No random test generation is used.

## Bounded practical comparison

`study_early_stop_source_energy.py` and `early_stop_source_energy_study.json` contain a sequential ABBA study with two samples per backend/fixture. CPU and wall clocks include the solve, its counting oracle, all checkpoint metering/materialization/checking/discard work, and terminal repair. Graph setup, result serialization, and an additional independent final-output check are excluded. No other timing job ran concurrently. The comparison uses stable source-energy scheduling, not the separate binomial-schedule refinement.

| Fixture | Fixed / early iterations | Fixed / early total adjacency entries | Fixed CPU / wall (s) | Early CPU / wall (s) |
|---|---:|---:|---:|---:|
| Billion-vertex path, alpha=1/100, rho=1/16, epsilon=1e-6 | 1344 / 528 | 7811 / 4947 | 0.660 / 0.667 | 0.393 / 0.400 |
| Two bridged 8-cliques, alpha=13/97, rho=1/128, epsilon=1e-6 | 340 / 72 | 10193 / 3558 | 0.411 / 0.415 | 0.118 / 0.118 |
| Billion-degree star boundary, leaf seed, alpha=1/100, rho=1/64, epsilon=1e-8 | 2032 / 112 | 2031 / 118 | 0.347 / 0.348 | 0.027 / 0.027 |

The early totals include 96, 441, and 7 added checkpoint adjacency entries, respectively. In the hub case, only leaf rows were scanned: the maximum degree queried was one billion, but the maximum degree scanned was one. Thus checkpoint checking preserved the locality distinction between a boundary degree reply and an adjacency scan.

All repeated runs were deterministic within each backend. Different backends need not return identical approximate vectors. After timing, every final output in this study was independently certified again by the sparse subgradient checker, and its independent bound met the requested epsilon. This is stronger accuracy evidence than merely checking the repaired source interval. The finite dense tests additionally verify support containment; the independent subgradient bound alone does not establish containment.

The measured median CPU ratios are about 1.68, 3.49, and 12.95. They are illustrative results for these three fixtures, not a general performance guarantee. The guaranteed statement is safe stopping with the fixed fallback and the added-work bound proved above.
