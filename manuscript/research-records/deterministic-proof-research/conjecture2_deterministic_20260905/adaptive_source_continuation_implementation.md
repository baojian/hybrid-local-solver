# Optional adaptive source continuation prototype

`adaptive_source_continuation_rppr.py` adds a separate research prototype.
It does not modify the standalone package, its default solver, or any
existing numerical module. Its complete mathematical interface is
independently audited in `adaptive_source_schedule_audit.md`. No timing
study has been run and no runtime improvement is claimed from the tests.

## API and unchanged numerical core

Call `solve_rppr_adaptive(oracle, seed, alpha, rho, epsilon)`. Its
`AdaptiveContinuationResult` contains:

- `result`: the existing `SolverResult` type, with the usual output,
  certificate, stage summaries, and continuation/repair metrics;
- `adaptive_metrics`: a separate additive source/scheduling ledger;
- `schedule`: the exact source maximum, maximizing vertex, old/proposed/
  chosen regularization and source-pass metrics for every stage.

Convenience properties expose `output`, `objective_gap_bound`, and `stages`.
**Total work includes both `result`'s existing ledgers and
`adaptive_metrics`.** It is incorrect to report only the inner result's
counts. Each stage summary remains the existing `PracticalStageSummary`.

`AdaptiveFastCorrector` has the unchanged cooperative Combined+Direct MRO:
early checkpoint -> binomial block -> source energy -> direct exception
transition -> integer correction. It has no method override. The wrapper
calls the original `_terminal_repair` directly. All momentum, grid,
delta/tolerance rules, actual correction steps, early certificates, repairs,
and final certificate `2*delta^2/rho` are unchanged at a given stage.
Changing stage regularizations can of course change the overall trajectory
and output from a dyadic continuation; equality to the old full call is
neither expected nor used as a correctness criterion.

## Schedule and source assembly

The direct zero and alpha-one branches still use only the initial seed
degree. Otherwise, initialize `old_r=1/d_seed`, baseline zero, and the exact
maximum `M=alpha/d_seed`. This obtains the first stage
`max(rho,1/(4*d_seed))` without an initial row scan.

At every stage choose `max(rho,M/(4*alpha))`. The already audited bounds
`alpha*old_r <= M <= 2*alpha*old_r` are checked explicitly. The proposed
value lies in `[old_r/4,old_r/2]`; a final target clamp can be closer to
`old_r`. The schedule records the distinction. A nonfinal repaired output
is then passed to `source_maximum`; a final output skips this unnecessary
pass. A zero-iteration stage still executes the ordinary terminal repair.

For dyadic densities `count_i/H`, `alpha=A/D`, the helper assembles

`N_i = 2*A*H*[i=seed] - (D+A)*d_i*count_i
       + (D-A)*sum_(j adjacent i) count_j`.

Its physical source density is `N_i/(2*D*H*d_i)`. Only the seed, retained
baseline, and its immediate boundary receive records; every omitted source
is exactly zero. The helper checks nonnegative source numerators and takes
the maximum by integer cross-products `N_i*d_max > N_max*d_i`. It constructs
one final rational maximum per pass. It never sums source densities with
different degree denominators, and it never uses approximate lazy neighbor
responses. The next nonclamped regularization is equivalently
`N_max/(8*A*H*d_max)`, so no historical denominator product is accumulated.

## Locality and work accounting

The helper reuses the **completed** corrector's AVL degree and adjacency
caches. It scans only retained baseline rows. If terminal repair retained
a coordinate whose row has never been read, that row may be loaded; its
entries, row request, cache write, and any new boundary degree replies are
all charged to the separate adaptive ledger. Every cached row traversal is
also charged. No inactive boundary row is read merely because its source
is evaluated.

**The corrector must not be resumed after this source pass.** Newly cached
vertices are deliberately not inserted into its now-unused reporter. The
wrapper never steps or queries that reporter afterward. The saved numeric
diagnostic snapshot is obtained before the pass; adaptive accesses are not
retroactively attributed to the earlier correction. The next stage uses
the unchanged fresh corrector setup, and any repeated baseline reads are
still counted there.

The two temporary graph maps, baseline counts and source numerators, are
AVL maps. They are explicitly cleared in a `finally` block, with their
record reclamation counted. Other extra records are constant-size scalars
and a charged row buffer/cache entry. There is no vertex-keyed hash table,
sorting oracle, or randomized balancing. Fixed-name diagnostic dictionaries
come only from the existing dataclass metrics interfaces.

The ledger distinguishes input records/volume, retained row requests,
cached hits, fresh entries, all scanned entries, degree/cache lookups and
writes, source integer updates, maximum comparisons, rational maximum
construction, temporary reclamation, and scheduling operations. These are
logical counters; the remaining validation, bookkeeping and integer
arithmetic have constant cost per counted record or entry, before the
usual AVL and bit-cost factors.

Each extra source pass costs
`O((1+volume(retained baseline))*log(N+2))` deterministic word work and
`O(volume(retained baseline))` adjacency inspections. The pass uses the
old stage's safe output, of volume at most `1/old_r`. The independently
proved geometric stage sum is less than `3/rho`, so these additions fit
the existing total local bound. The same source audit establishes the
unchanged rational bit envelope: all source maxima and proposed parameters
are rebuilt from bounded dyadic counts and one degree denominator.

## Exact verification

Run `python3 -B test_adaptive_source_continuation.py`.
`adaptive_source_continuation_verification.json` records five passing groups:

- Eight tiny complete calls and 24 stages, each compared with an independent
  exhaustive-support rational KKT solve. Every repaired stage is below the
  exact optimum, preserves the old baseline, obeys the repaired-source
  interval, and satisfies its advertised objective error.
- Four non-dyadic rational stage jumps, eight target clamps, and one actual
  zero-iteration stage that still performs terminal repair. The stage
  reciprocal sum and exact source maximum are independently recomputed.
- Sixteen noninitial scheduling passes, with 73 retained-row entries, and
  exact reconciliation of external oracle accesses with correction,
  terminal repair, and adaptive ledgers.
- Four full independent corrector/repair replays at the adaptive stage
  parameters, reproducing the stage output and every numerical diagnostic.
- A fresh-cache source pass and an entirely cached repetition on a virtual
  two-spoke graph. The true maximum occurs at an inactive boundary vertex;
  another boundary has degree above `2^181`. Only the seed row is read.
- Direct zero/alpha-one branches and a separate degree-`10^30` hub example
  with hash-forbidden large labels. The hub's row is forbidden and never
  requested. All eight tiny final outputs and the separate hub output pass
  independent sparse subgradient certificates.

Core-module hashes are recorded before and after the tests and are
unchanged. The prototype source hash at this snapshot is
`af33cb41872eb834aeabb14f5ec5cc1a45cda7400482884da5576e0358c633ea`.
