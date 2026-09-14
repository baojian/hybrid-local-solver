# Independent audit of geometric cached certificate checkpoints

Inspected code: `early_stop_source_energy_rppr.py`, SHA-256
`48d45c16eb084b4e84b7663038208191e52ad0f3911fc4db52c0786576a5f1cb`.
The independent auditor also read `early_stop_source_energy_audit.md`, the
fresh certificate implementation, the inherited corrector/repair, and the
deterministic AVL operations used by the metering adapter. No code was
changed. No randomized algorithm or test is used.

**Finding: the current-state stopping rule, cached realization, and stated
added-work bound are valid. No implementation correction is requested.**

## 1. The accepted bound belongs to the current full iterate

The candidate passed to the independent checker is the full vector
`baseline + sigma*X`, materialized after a completed accelerated step. Its
coordinates are nonnegative. The checker recomputes a valid subgradient of
the original weighted-absolute-value objective: on zero coordinates the
Stieltjes signs place the selected zero/negative endpoint inside the
original subgradient interval. The bound is therefore valid for the
original objective, without an acceleration-energy assumption and without
requiring the candidate to be a safe lower solution.

The code accepts only when the newly returned upper bound is strictly
smaller than the stage tolerance. It stores that scalar together with the
current iteration and returns precisely the already checked candidate.
There is no state mutation between certificate calculation and return.
The unchanged terminal PG/grid/max repair requires this objective-gap
bound, rather than a bound on the full accelerated energy or on its kinetic
term. Thus a successful independent check supplies exactly the repair's
needed interface. The ordinary continuation source and containment
invariants follow from that repair as before.

At a positive rejected checkpoint no accepted scalar survives. The
prescribed source-energy horizon and its valid prefix certificate remain
unchanged. No conclusion is drawn from a failed sufficient certificate.

## 2. Zero steps, fallback, and explicit manual operations

The run loop checks only positive times `T,2T,4T,...` strictly below the
fixed horizon. A zero-step stage performs no checkpoint and uses the
inherited initial-energy certificate. At the fixed horizon, the ordinary
certificate gives the required strict gap bound and the code returns its
current output without needing an independent check to succeed.

If an accepted stage is explicitly stepped again, the accepted scalar and
iteration are cleared before the next step. The fallback prefix energy
certificate then applies to the changed state. Calling run after manual
prefix steps skips scheduled checkpoints at or before the current time;
future checks remain on the original geometric sequence. Repeated run on
an accepted, unmodified state returns its current output with the same
valid scalar. Its extra materialization is an explicit caller action, not
an uncounted operation in a default wrapper run. Arbitrary direct state
mutation and arbitrarily repeated calls to the private checkpoint method
are not part of the wrapper complexity claim.

## 3. Cache completeness and unchanged recurrence

Every positive primal count was created at a previously emitted kinetic
coordinate. All emitted kinetic rows are scanned, including coordinates
whose primal increment rounds to zero. Baseline rows are scanned during
initialization. Consequently every positive full-candidate row is already
cached, and every neighbor's degree was exposed when that row was scanned.
The seed degree is exposed at initialization.

The cache adapter holds the corrector's persistent degree and adjacency
maps. Scalar rebasing replaces X/L maps, not these two cache maps. The
adapter has no fallback path to the external oracle: a missing entry raises
an assertion. It is therefore impossible for a successful check to create
new graph exposure through this adapter.

Candidate materialization, certificate computation, and temporary-map
cleanup do not change any recurrence state, reporter key, source value,
cache record, or iteration count. The core state trajectory is exactly a
prefix of the source-energy trajectory with the same stage input. Stopping
earlier can change a later repaired baseline, which is covered by the
repair theorem rather than a claim of identical entire continuations.

## 4. Work, temporary state, and reclamation

At prefix k, candidate volume satisfies

    V_k <= vol(baseline)+sum_{t<=k}vol(supp z_t)
        <= (1+360k)/r.

The actual whole candidate is paid for. The proof neither identifies its
support with current kinetic support nor silently discards old positive
coordinates. Materialization visits the union of positive X and baseline
records. Those counts are positive and sigma>0, so this union has exactly
the number of returned candidate records. Its allocation, point lookups,
and reclamation cost O(V_k log(N+2)).

The independent checker reads V_k cached adjacency entries and at most
`2V_k+1` affected degrees. All six temporary AVL maps (including the set's
backing map) are retained in a local tracking list and explicitly cleared
in a finally block. Clearing a root may reclaim linearly many nodes; the
code records the size before clear, and the proof pays that work. The list
is then cleared. Failed candidates are released before the next step, and
only a constant-size accepted certificate survives a successful check.
On an exception the same finally block reclaims constructed checker maps;
the exception is propagated rather than silently accepted.

Logical metering uses the exact certificate function with private AVL class
bindings. Inherited `get` and `contains` operations reach the metered item
lookup; iteration reaches the metered item iterator. Metering does not
claim to count every rotation/comparison or Python instruction individually.
Those operations receive their proved deterministic logarithmic factor.
The fixed-size namespace copy and class/function setup are O(1) in graph
size. The code does not modify the original checker's globals.

For the subset of geometric checks that actually occur before termination,
`sum k_j < 2*k_actual`. Hence

    sum V_(k_j) <= (number_of_checks+360*sum k_j)/r
                 = O((k_actual+1)/r).

There is no extra logarithmic number-of-checks multiplier on the volume
term. Added checker work is O((k_actual+1)log(N+2)/r), with the established
encoded-arithmetic factors if charged in bits. The original initialization,
state-rebase, final materialization, and terminal repair costs remain
separate. Temporary storage at any one check is O(V_k+1); failed checker
histories do not accumulate. These terms preserve the existing worst-case
operation and storage bounds.

## 5. H-squared candidates and bit precision

If the current grid denominator is H, candidate densities are

    (S*X_i + H*baseline_i)/H^2.

All reduced denominators are powers of two dividing H^2. Therefore their
largest reduced denominator is a valid common denominator for the exact
checker; the denominator contract is satisfied even when reductions differ
coordinatewise. This must use H^2 in the analysis rather than assuming the
unrepaired candidate lies on the original H grid.

Candidate mass is at most one. With a common denominator Hc<=H^2, integer
counts have O(log H) bits in addition to local degree/parameter encoding.
The residual denominator is `C=2*den(alpha)*Hc*den(r)`. The integer
neighbor sums and upward terms `ceil(V_i^2/d_i)` avoid a graph-degree LCM.
The final squared denominator is C^2; its bit length is a fixed multiple
of the existing parameter/grid lengths. Combining a fixed number of such
scalars with alpha still gives O(B)-bit numerators, denominators, and
temporaries in the previous encoded-input bound. Neither the number of
checkpoints nor previous certificate denominators enters future arithmetic.

## 6. Independent exact evidence

The separate checker `audit_early_stop_independent.py` records results in
`early_stop_independent_audit_results.json`. All checks passed:

- Four complete graph/parameter cases and seventeen stages, with exact
  support-enumeration KKT optima and independent edge-form objective gaps.
  Every stage's repair is monotone, below its true optimum, and has the
  required source interval; each final gap is within its certificate.
- 943 exact state comparisons with an independent source-energy corrector,
  including reporter registries and ordered degree/adjacency query histories.
- 48 actual checkpoints: 18 accepted and 30 rejected. At every check the
  external oracle is locked to raise on any call. Independent exact density
  gradients and actual gaps verify the freshly computed certificate.
- All 288 checker containers are reclaimed. Reclaimed node totals agree
  with container sizes measured immediately before return. Full checkpoint
  volumes, affected/update counts, and geometric work sums reconcile.
- One genuine fallback after failed independent checks, one zero-step
  stage, accepted-bound invalidation followed by resumption, and manual
  stepping past optional checkpoints.
- An injected exception after all six checker maps have been created
  confirms finally-path cleanup and absence of an accepted stale bound.

The source note's measured speedups remain finite-instance observations.
This independent audit establishes the validity and charged realization of
the optional stopping rule, not a universal practical speedup guarantee.
