# Composition of cached certificates and binomial block scheduling

The composition is sound. The separately named final prototype is
`combined_certified_dyadic_rppr.py`, exporting `CombinedDyadicCorrector` and
`solve_rppr_combined`. No existing implementation or package file was edited.
The implementation composes the two stable classes through cooperative
inheritance and uses the unchanged integer continuation/repair body with an
isolated corrector-class binding.

## 1. Method resolution is verified, not assumed

The actual C3 method-resolution order is

    CombinedDyadicCorrector
    EarlyStopSourceEnergyCorrector
    BinomialBlockDyadicCorrector
    SourceEnergyDyadicCorrector
    IntegerDyadicCorrector
    object.

This order is asserted in the exact test suite. Its consequences are:

* Initialization runs Integer, SourceEnergy, and Binomial initialization
  before EarlyStop installs its checkpoint state. Therefore the checkpoint
  horizon is already the tighter binomial target, and all binomial fields
  exist before an objective property can be used by the completed object.
* `run()` is the EarlyStop method. Its `self.target_iterations` is the
  binomial horizon. It checks only T,2T,4T,... strictly before that horizon.
* `step()` first executes EarlyStop's accepted-bound invalidation, then
  Binomial's method. The latter executes the unchanged integer recurrence
  and updates its power on each newly completed block before returning.
* With no accepted independent bound, EarlyStop's `super()` objective
  property resolves directly to the Binomial property. It cannot silently
  fall back to the older half-block certificate. After acceptance the bound
  is the independently recomputed current-candidate certificate instead.
* Diagnostic properties follow the same chain, retaining source statistics,
  binomial powers/schedule data, and the full checkpoint ledger together.

The classes' `super()` calls are cooperative at each of these points. There
is no explicit ancestor-method call that bypasses the intended method order.
The relevant parent code snapshots were confirmed stable before composition.

## 2. Numerical trajectory and fallback correctness

Initialization, source formation, exact mass cap, integer state updates,
scalar rebases, and projection queries are those of the binomial corrector.
A checkpoint reads vectors and caches but does not alter them. Rejected
certificate state and materialized candidates are discarded before the next
step. Therefore, on identical stage input, the combined numerical state is
exactly the binomial state at every executed prefix.

The audited binomial fallback gives, with c=floor(k/T),

    original objective gap <= E_k
      <=Ebar*beta^c+Gamma          when k>0,
    original objective gap <=Ebar when k=0.

The prescribed horizon K=Tq satisfies Ebar*beta^q<=tau/2 and Gamma<tau/8.
Thus every fallback return satisfies gap<tau. Zero-step and zero-energy
stages use Ebar without a fictitious rounding term. The code's completed
power update occurs before any checkpoint or caller reads the bound.

A checkpoint instead materializes the actual full candidate, independently
recomputes its exact sparse subgradient, and uses the upward-rounded bound

    gap <= ||subgradient||^2_upper/(2alpha).

This certificate is derived from strong convexity of the nonnegative
obstacle objective. It does not depend on an accelerated energy identity,
monotonicity, approximate neighbor sums, or the fallback schedule. The
candidate's dyadic denominators divide H^2, satisfying the independent
checker's common-density-denominator contract. The checker uses a common
integer denominator and upward squared divisions, so it introduces no
aggregation of coprime degree denominators.

Acceptance requires this freshly computed bound to be **strictly less**
than tau. Its scalar and iteration number are retained, and that already
materialized candidate is returned. If a caller subsequently invokes
`step()`, the accepted bound is cleared before the state changes. The next
bound then comes from the binomial power. Re-running may accept a fresh
certificate or reach the still-valid fallback. A previous iterate's bound
is never applied to the new iterate.

For the same baseline and other stage inputs, the combined return iteration
is at most either separate variant's return iteration: before the binomial
horizon it performs the identical geometric checks as the early-only
variant, and otherwise it returns at that earlier fallback horizon. At a
checkpoint exactly equal to the binomial horizon it uses the fallback,
with no additional norm check. This stagewise statement does not assert
monotonicity of total work across complete continuations whose later
baselines differ.

## 3. Terminal repair and continuation remain valid

Every return path supplies a nonnegative actual candidate with original
objective gap below the same tau=alpha*delta^2/8 used by the unchanged
repair. The exact terminal PG pass ignores the approximate L state and
scans the actual candidate. Downward clipping/grid rounding and the maximum
with the old safe baseline then give the established safe order, monotone
baseline, and source bounds. The next stage consequently has its required
source in [0,4*alpha*r*w].

The final returned objective certificate remains 2*delta^2/rho<=epsilon.
An early certificate may replace the stage certificate, but it never
replaces the final repair argument. The zero-solution and alpha=1 direct
branches still bypass the corrector entirely. No new optimum/support oracle
or graph-wide input is introduced.

## 4. Checkpoints are cache-only and fully charged

Every positive candidate coordinate lies in the old baseline or a previously
emitted kinetic support. Baseline rows are scanned during source setup;
emitted rows are scanned during their updates, even when an individual
rounded primal increment is zero. Each scan exposes neighboring degrees.
Therefore every candidate row and every degree needed by the independent
checker is already cached.

`CacheOnlyOracle` holds references to the stage's degree and adjacency maps.
Scalar rebases replace only X/L, so those cache references remain valid.
Missing cache data causes an assertion; it never triggers an external oracle
call. Tests verify no new degree or row replies at every actual checkpoint.
The helper's separate temporary AVL maps/sets are cleared on both success
and failure. Only an accepted scalar bound and iteration persist.

Let V_k be candidate support volume and W_k cumulative kinetic volume.
The same prefix theorem gives

    V_k <=V_baseline+W_k <=(1+360k)/r.

At geometric checkpoints k_j=T*2^j before an actual return at k_actual,

    sum_j k_j <2*k_actual,
    sum_j V_(k_j) =O((k_actual+1)/r).

Each checkpoint pays for materialization, cached adjacency reads, cached
degree/row lookups, deterministic checker map requests, squared-statistic
arithmetic, and temporary-state disposal. A balanced-map logarithm gives
O((k_actual+1)log(N+2)/r) added arithmetic/word work. The final PG reread is
charged again; it is not hidden by the preceding checkpoint scan. If
k_actual=0, there is no checkpoint, while initialization and terminal work
remain charged.

These checks preserve the cubic-log arithmetic and conservative bit bounds
of `integer_source_complexity_corollary.md`. The binomial horizon is no
larger than the original fixed horizon, and the vectors remain a valid
prefix. Checkpoint common denominators and binomial powers both fit the
same O(B)-bit envelope. The public continuation calls `run()` once per
stage; additional caller-requested materializations or manual continuation
steps are extra work, with semantic invalidation behavior tested separately.

## 5. Exact composition tests

`test_combined_certified_dyadic_rppr.py` passes six groups. Results are saved
in `combined_certified_dyadic_verification.json`.

* The MRO, selected run method, fallback property, and combined metadata are
  checked explicitly.
* Eighteen complete stages across four exact finite-graph cases execute
  816 state steps. Every step exactly matches a separately instantiated
  binomial corrector with the same baseline/grid and has a valid complete
  acceleration-energy prefix bound.
* Fifty-one genuine independent checkpoints are audited: sixteen accept and
  thirty-five reject. Each bound is compared with an exhaustive dense KKT
  objective gap, and its threshold decision is checked exactly. All cached
  checks leave external oracle histories unchanged and release their
  temporary checker containers.
* A genuine fallback stage remains after rejected checkpoints. Its returned
  bound equals the corresponding binomial-reference bound. Early returned
  bounds equal the retained independent certificate. Every repaired output
  satisfies dense optimum containment, baseline monotonicity, source bounds,
  and the final objective certificate.
* Zero-step continuation, an exact-zero-energy baseline, alpha=1, and the
  zero-solution equality branch are covered.
* After a successful early return, a manual step clears the bound, advances
  the binomial power correctly, and exposes the valid fallback bound. A
  subsequent run returns another valid certificate. Explicit missing-cache
  requests assert without calling the external graph oracle.
* An implicit billion-degree star boundary is queried only for its degree;
  all scanned rows are the seed leaf. Its one-coordinate optimum is checked
  analytically, and its final output also passes the independent sparse
  certificate. Checkpoints record no cache miss or hub-row scan.

All graph counts reconcile with the corrector, checkpoint, and terminal
ledgers. The tests do not use randomized graph generation or arithmetic.

## 6. Four-variant bounded study

`study_combined_certified_dyadic.py` runs source-energy only, early-check
only, binomial-only, and combined variants in symmetric order
source/early/binomial/combined/combined/binomial/early/source. Each has two
samples per fixture. The timed interval includes the counting oracle,
checkpoint metering/materialization/checking/disposal, and terminal repair.
Graph construction, serialization, hashing, and a fresh independent final
certificate are outside that interval and reported separately.

`combined_certified_dyadic_study.json` retains all twenty-four complete
answers, including every output, stage, continuation metric, and checkpoint
metric; it also records source SHA-256 hashes, CPU/wall measurements, oracle
counts, and independent final certificates. Each backend reproduced its
own exact result and metrics. All twenty-four final sparse certificates
meet the requested epsilon.

| Fixture / variant | Iterations | Total adjacency entries | Median CPU s | Median wall s |
|---|---:|---:|---:|---:|
| Billion-vertex path: source | 1,344 | 7,811 | 0.7936 | 0.8026 |
| Path: early | 528 | 4,947 | 0.4836 | 0.4934 |
| Path: binomial | 912 | 5,235 | 0.5239 | 0.5250 |
| Path: combined | 400 | 3,526 | 0.3268 | 0.3274 |
| Two bridged 8-cliques: source | 340 | 10,193 | 0.5205 | 0.5275 |
| Bridged cliques: early | 72 | 3,558 | 0.1462 | 0.1481 |
| Bridged cliques: binomial | 208 | 6,269 | 0.3103 | 0.3123 |
| Bridged cliques: combined | 72 | 3,558 | 0.1509 | 0.1515 |
| Billion-degree star boundary: source | 2,032 | 2,031 | 0.4543 | 0.4574 |
| Star boundary: early | 112 | 118 | 0.0305 | 0.0305 |
| Star boundary: binomial | 1,408 | 1,407 | 0.3098 | 0.3109 |
| Star boundary: combined | 112 | 118 | 0.0317 | 0.0317 |

The path uses alpha=1/100,rho=1/16,epsilon=1e-6; the bridged cliques use
alpha=13/97,rho=1/128,epsilon=1e-6; the star uses alpha=1/100,rho=1/64,
epsilon=1e-8 and a leaf seed. Combined checkpoint reads are respectively
83,441,7, all included in the table's total adjacency count.

The path benefits from both refinements. On the other two fixtures the
combined variant matches early-only graph work, with a small extra scalar
setup cost visible in these timings. This is a bounded comparison, not a
claim that the composition always reduces wall time or every complete
continuation's graph work. Its guaranteed property is exact certified
stopping with a tighter fallback and fully paid local checks.

Only clocks use floating values. Every solver computation and stopping
decision is exact and deterministic. The reusable star runs have been
handed to the independent larger study to avoid duplicate measurements.
