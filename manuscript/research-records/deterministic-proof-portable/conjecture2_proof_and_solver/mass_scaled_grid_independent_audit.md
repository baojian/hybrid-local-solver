# Independent audit of the optional mass-scaled grid adapter

Status: passed; no correctness defect or requested implementation change.
Audited source: mass_scaled_grid_rppr.py, SHA-256
3b8cfa4a8f0161101147573007e5ac4cbabb4c64e348ec702f90d977a37d7d8f.

The mathematical reference is mass_scaled_rounding_precision_audit.md.
Only current-team artifacts were inspected. No stable core, package, or
other implementation was edited. The author's verification JSON was read;
its full suite and larger studies were not rerun.

## 1. Initialization and restoration

The method resolution order is

    MassScaledGrid -> Combined -> EarlyStop -> Binomial -> SourceEnergy
                   -> DirectExceptionInteger -> Integer -> object.

Calling the inherited constructor with tau/eta selects the relaxed grid,
assembles the exact source and mass cap, and computes source statistics on
that actual grid. It performs no numerical step or checkpoint. The hint is
then checked against the assembled cap, so a false external hint cannot
silently produce a valid returned corrector.

The adapter restores the actual tau and the floor
Gamma_eta=29*eta*h/theta before returning. It recomputes the original
unit-initial-energy horizon, the source half-block horizon, and the
binomial horizon against this tau. It also resets all initial decay/power
fields to one, and retains the untouched empty checkpoint state.
The source-energy bound needs no second statistical pass: it depends on
the actual initialized source/grid, alpha, mu, rho, and eta, not on tau.
The binomial constant likewise depends only on T.

This is sufficient for all inherited certificate paths. At zero steps the
bound is Ebar, at ordinary prefixes it is the binomial contraction bound
plus Gamma_eta, and accepted checkpoints use the unchanged independent
original-objective certificate against actual tau. The fallback endpoint
satisfies Ebar*beta^q<=tau/2 and Gamma_eta<tau/8.

The valid wrapper always has 0<tau<eta and eta>=rho>0, so the explicit
initialization guards neither divide by zero nor exclude a valid
nontrivial stage. The zero-solution and alpha=1 branches bypass the factory.

## 2. Work counters and reference lifetime

The inherited relaxed initialization work is genuinely performed.
The retargeting loop updates are added to its ordinary accumulated
schedule counters. Each displayed RetargetingWork field is a subset of
those totals, not an additional charge. The diagnostic counter contract
states this explicitly. The separate scalar_setup_passes=1 records one
constant-size setup/validation pass; it is not a claimed exact count of
Python scalar operations or bytecodes.

MassCapHintFactory uses only the previous corrector's cached degrees and
the incoming baseline fractions. All their denominators divide the old
grid denominator. Its integer degree-weighted count sum therefore yields
eta exactly without degree-denominator aggregation or graph queries.
The new constructor independently verifies the same cap through source
assembly. Baseline record visits, cached lookups, count conversions,
integer mass updates, and hint setup are separate additional ledgers.
They must be added to the inner result's ordinary work; the retargeting
subsets must not be added again.

The factory releases its old-corrector reference before constructing the
next one, and releases the final reference in a finally block. The
unchanged outer continuation can still own its normal preceding
temporary during the next constructor call, so this is a constant number
of simultaneous correctors, not a claim that all old memory disappears
before every allocation. Hint records retain only scalar summaries.
A weak-reference test, with no outer continuation owner, confirms actual
reclamation before the new constructor and after final release.

## 3. Exact representation and unchanged recurrence

The parent constructor imposes the reciprocal of each reduced baseline
denominator as a ceiling. This represents the baseline exactly but may
allow coarsening when its fractions reduce. That is the weaker, sufficient
condition proved in the mathematical audit; retaining unused old grid bits
is unnecessary. The default bit bound follows from

    h_new >= min(h_old, largest_dyadic<=theta*tau_new/(256*eta_new)).

For actual continuation tau is nonincreasing, so the existing
h_new>theta*tau_new/512 envelope remains valid.
A bounded valid-interface fixture with nonincreasing tolerances confirms
a factor-two coarsening while preserving the exact baseline. Its supplied
baseline is an exact old optimum, chosen to isolate representation and
cache handling; this fixture does not claim that a particular preceding
rounded run produced that exact optimum.

Method identity checks verify unchanged step, run, and scalar-rebase
methods against the existing combined/direct class. The factory-bound
continuation has exactly the integer wrapper's code object. The reporter
and terminal repair implementations are inherited unchanged.

External oracle call sequences match the unmodified combined/direct
corrector when supplied the same new grid and manually extended test
stopping guard, for every checked prefix. This is a same-trajectory
statement. Different grid choices may change actual support decisions,
and no equality of graph work with the old default grid is claimed.

## 4. Independent bounded exact evidence

Saved checker: audit_mass_scaled_grid_independent.py.
Saved results: mass_scaled_grid_independent_verification.json.

All four test groups pass:

- 52 separately constructed dense rounded steps, each matching the
  integer primal, approximate neighbor, kinetic, and exact kinetic-neighbor
  states. The dense projection uses its own complete breakpoint list and
  affine mass interpolation, not the production reporter.
- 208 weighted energy inequalities and 52 Q-response bounds, evaluated on
  the actual rounded states against independent dense exact KKT solutions
  and exact Q-inverse comparators. Fifty auxiliary-energy prefixes are
  negative, so their validity is not being inferred from positivity.
- 37 steps with nonzero approximate-neighbor raw error and 19 scalar
  rebases; the raw error, neighbor discrepancy, downward state errors,
  mass caps, and zero rebase-adjacency count all satisfy their interfaces.
- 52 matching external-oracle prefixes against the unchanged same-grid
  core; exact schedule minima, power fields, and accumulated/subset
  counter identities are checked at every construction.
- Both zero-energy and positive-energy zero-step stages retain their
  correct Ebar certificate.
- Two complete continuations, seven repaired stages, non-dyadic final
  parameters, exact safe-order/source checks, and final objective gaps
  below the requested tolerance. Every external degree reply and
  adjacency entry reconciles with the inner ledgers; hint generation adds
  no graph accesses.
- Cached-hint generation, exact coarsening, and prior/final reference
  release pass their separate checks.

The author's saved results additionally report 60 dense prefix comparisons,
a grid enlargement up to 32, twelve repaired stages, zero/direct branches,
and an unscanned boundary with degree 10^30. These are author-supplied
evidence, not counted as new independently executed tests above.

All seven audited source hashes remained unchanged during this audit.
The tests are finite validation of the implementation; the uniform
convergence, locality, and bit guarantees depend on the proved stage
interface and the mass-scaled lemma.

