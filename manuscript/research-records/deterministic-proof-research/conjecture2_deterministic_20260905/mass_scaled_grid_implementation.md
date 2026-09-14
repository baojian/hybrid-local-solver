# Optional mass-scaled grid adapter

The separate prototype `mass_scaled_grid_rppr.py` uses the independently
proved mass-weighted error estimate in `mass_scaled_rounding_precision_audit.md`.
It leaves the package, default solver, fixed continuation, integer step,
reporter, scalar rebase, checkpoint implementation and terminal repair
unchanged. No timing study or runtime improvement claim is included.

## Initialization contract

For a stage with exact correction mass cap `eta`, the two comparison-energy
recurrences permit the error floor

`Gamma_eta <= 29*eta*h/theta`.

Consequently the adapter may select a dyadic grid with

`h <= min(1/8, theta*tau/(256*eta), theta*alpha^2*r/29)`

while representing the incoming repaired baseline exactly. Valid
nontrivial stages have `r <= eta <= 1`; zero and alpha-one complete-call
branches return before any mass-scaled constructor is invoked.

`MassScaledGridCorrector` inherits the existing Combined+Direct correction
MRO and overrides only its constructor and diagnostic assembly. The
constructor accepts a required `mass_cap_hint`, calls the original parent
initialization with `tau/eta`, and lets it perform all ordinary exact source
assembly and grid selection. It then verifies that the hint equals the
parent's exact `mass_cap`. A mismatch is rejected before any step. The
complete-call tolerance rules guarantee `0<tau<eta`, so the parent's
temporary tolerance remains in its existing `(0,1)` input range.

The temporary initialization tolerance is only a means of selecting the
grid. It is **not** the stopping target. Before any step or checkpoint the
adapter restores `self.tolerance=tau`, assigns
`self.gamma_bound=29*eta*h/theta` exactly once, and reconstructs all of:

- the original `E0<=1` half-block horizon;
- the source-energy half-block horizon and block count;
- the binomial target block count and target power numerator/denominator;
- the initial current block powers and half-block decay denominator.

The source statistics, their bounded-denominator upward squared sum, the
initial energy bound and the binomial block factor are reused. They remain
valid at the actual grid and do not depend on interpreting `tau/eta` as the
requested tolerance. The constructor asserts zero completed iterations,
empty checkpoint state, no accepted bound, and the initial checkpoint `T`.
No relaxed-horizon step has taken place. The inherited zero-step bound is
still `Ebar` itself, with no nonexistent rounding floor added.

The new grid preserves every incoming baseline fraction exactly. It need
not preserve an unused old grid denominator: if all retained fractions
reduce and a final target clamp permits a coarser admissible grid, the
parent may choose it. This is deliberate and safe. The grid property is
**exact baseline representation**, not strict monotonicity of grid
denominators. The independent precision audit establishes the same global
logarithmic encoding envelope for this choice.

## Fixed continuation and mass hints

`solve_rppr_mass_scaled_grid` reuses the original fixed continuation code
through its existing research-only `_continuation(factory)` mechanism.
`MassCapHintFactory` is the injected callable. Initial zero baseline has
`eta=1`. At every later construction, it uses the preceding corrector's
degree cache and grid denominator `H` to form

`mass_count = sum_i d_i * (H * baseline_density_i)`,
`eta = (H-mass_count)/H`.

All summed quantities are integers. Only the final mass hint is made into
a rational, so no degree-denominator sum or LCM occurs. The incoming
repaired coordinates already have cached degrees, including any newly
retained terminal-PG coordinates. A missing cached degree is an interface
error; the factory never replaces it by a new graph query. The parent
constructor independently rechecks the actual mass cap from its own source
assembly.

The factory holds only the immediately preceding corrector until the next
construction. It releases that extra reference before creating the new
one, and releases the final reference in the wrapper's `finally` block.
The unchanged outer continuation still has its normal temporary reference
during construction. The adapter does not retain all completed numerical
states in its result.

The outer `MassScaledGridResult` contains the unchanged inner `SolverResult`
as `result`, separate `mass_hint_metrics`, and scalar `mass_hints` records.
Convenience properties expose output, gap bound and stages. Total work is
the inner ledgers plus the mass-hint ledger. The added baseline-record and
cached-degree passes cost `O((1+|baseline|)log(N+2))` per stage, with no new
oracle calls. The stage regularizations remain exactly the existing fixed
halving schedule, including its final clamp and delta/tau/repair rules.

## Truthful setup diagnostics

All work performed by the relaxed initialization remains counted. The
actual-tolerance retargeting loops increment the existing original,
source-energy and binomial scheduling counters. Their final values are
accumulated work totals from **both** passes. The actual horizon fields
describe the actual-tolerance schedule, rather than the discarded relaxed
schedule.

`diagnostic_metrics['mass_scaled_grid']` additionally shows the actual and
relaxed tolerances, mass hint, weighted floor, discarded relaxed horizons,
relaxed setup counts, and retargeting loop counts. The retargeting counts
are explicitly identified as subsets already present in the accumulated
ordinary counters; adding them a second time would double count. One
`scalar_setup_passes` record covers the remaining constant-size validation,
operand construction and final-field setup. It is structural telemetry,
not an exact count of every scalar instruction or Python bytecode.

The research callable injection does not mutate any module globals. If
this option is later transcribed into the standalone package, its wrapper
should call the package's explicit
`_integer.solve_rppr_integer(..., corrector_class=factory)` interface rather
than adding `FunctionType` cloning to the package.

## Exact tests

Run `python3 -B test_mass_scaled_grid_rppr.py`.
`mass_scaled_grid_verification.json` records four passing groups:

- Five standalone stage fixtures, four with grids strictly coarser than
  the old choice, reaching a factor of 32. Grid selection, actual-tolerance
  original/source/binomial horizons, target powers, accumulated setup
  counters, and initial unaccepted checkpoint state are checked exactly.
- Sixty successive rounded steps, each checked against an independent
  dense weighted box projection and both exact comparison energies.
  Forty steps have nonzero downward rounding, and 28 have nonzero lazy raw
  response error. Density errors, feasibility, the one-step mass-weighted
  perturbation inequality, and the complete prefix convolution bound all
  pass using rational arithmetic.
- Two zero-step cases: exact zero initial energy and positive initial
  energy already below `tau/2`. The reported zero-step gap remains `Ebar`.
- Five complete fixed-continuation calls with 12 repaired stages. Dense
  exact KKT solutions verify the safe ordering and source interface at
  every stage. All final outputs pass independent sparse certificates.
  Eighteen added mass-hint input records/degree-cache lookups reconcile
  exactly, and all external degree/row accesses are accounted for entirely
  by the unchanged inner solver ledgers.
- A deliberately false mass-cap hint is rejected. A separate
  degree-`10^30` inactive-hub fixture uses hash-forbidden large labels and
  never reads the hub row; its independent final certificate passes.

The dense energy comparisons use the true obstacle correction for the
primal energy and a separately solved `Q^{-1}s` comparator for the
auxiliary energy. The latter may be negative; the test does not assume
nonnegativity. Neither dense solution is passed to the numerical algorithm.
Every checked kernel method remains the inherited method, with no new step
or repair implementation.

The six stable source-module hashes are unchanged before/after testing.
This prototype snapshot has SHA-256
`3b8cfa4a8f0161101147573007e5ac4cbabb4c64e348ec702f90d977a37d7d8f`.
