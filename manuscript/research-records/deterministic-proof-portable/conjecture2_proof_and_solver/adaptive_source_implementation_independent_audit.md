# Independent audit of the optional adaptive continuation prototype

Audited `adaptive_source_continuation_rppr.py`, its supplied test module and
verification JSON, and the new `app:adaptive` TeX subsection. The independent
mathematical derivation is in `adaptive_source_schedule_independent_audit.md`.
No implementation, stable package, numerical core, or TeX file was changed.

**Conclusion:** no correctness or locality defect found. The separately
versioned prototype is consistent with the proved adaptive schedule and
the unchanged numerical core. The audited source hash is
`af33cb41872eb834aeabb14f5ec5cc1a45cda7400482884da5576e0358c633ea`.

## Schedule, repair, and state lifecycle

The corrector subclass changes no method and resolves to the already
audited Combined/Direct recurrence. The wrapper retains the same per-stage
momentum, tolerance, grid, objective certificate, terminal PG/grid/maximum
repair, and final gap bound. It changes only regularization parameters.
The exact current source maximum is divided by `4*alpha`, clamped to the
target, and checked against the repaired-source range. The initial scalar
comes directly from the queried seed degree. The final stage performs no
unnecessary maximum computation. Zero/direct branches and zero-iteration
terminal repair are preserved.

Crucially, the nonfinal call passes the **new repaired output** and its
actual grid denominator to `source_maximum`. It does not reuse the old
fixed source, the approximate primal neighbor record, or an old source
maximum. The next corrector is constructed from that repaired baseline.
The source pass uses the completed corrector's graph caches only; no
numeric state or reporter query follows it. This matters because generic
cache additions are not installed into that completed reporter. The helper
documents this non-resumption contract, and the wrapper obeys it.

## Source assembly and maxima outside the support

The helper starts with the seed numerator, subtracts each retained diagonal
contribution, and adds each retained neighbor contribution. Its affected
set is exactly the seed union baseline support union immediate boundary;
all omitted source values are zero. Every numerator is checked, including
inactive boundary coordinates. The maximum is computed over all affected
records by exact integer cross products, with one final rational
construction. It is not restricted to the retained support or the seed.

For a maximizing vertex, the resulting unclamped parameter equals
`N_i/(8*A*H*d_i)`, matching the independent bounded-denominator derivation.
Non-dyadic proposed and chosen stage parameters are therefore supported;
the baseline remains on the separately selected dyadic grid.

## Access and temporary-state ledger

The helper checks/updates only retained rows and the degrees of affected
vertices. A fresh row has a counted oracle request, first entries, cache
write, and subsequent numeric traversal. A cached row still has its counted
request/lookup and full numeric traversal. Thus the first-entry and scanned-
entry counters describe distinct paid accesses; callers must retain both
when aggregating all low-level reads. No boundary row is recursively read.

The prototype retains all probe operations in `adaptive_metrics` and each
schedule record. It does not retroactively change correction or repair
counters. Total work is explicitly the inner result ledgers plus these
adaptive ledgers. Subsequent fresh corrector initialization incurs its
ordinary repeated source/row costs again. The two temporary AVL maps are
cleared in `finally`, and their records are included in reclamation counts.
The counters are logical records/operations, not a claim to instrument
every Python instruction or integer temporary.

There is an additional useful invariant for the actual certified wrapper.
The candidate and its PG point each have Euclidean error at most `delta/2`.
If the candidate coordinate is zero, then the PG coordinate is at most
`delta`, hence its density is at most `delta/w_i<=delta`. Truncation removes
it. Therefore the repaired support is contained in the candidate support,
whose rows and boundary degrees were already cached. The actual adaptive
passes should require no new graph accesses, although all cached scans
remain paid. The helper's fresh/partial-cache branches are still legitimate
general helper cases and must remain charged; the implementation does not
depend on using this stronger cache fact for its work guarantee.

## Independent exact tests

The separate checker `audit_adaptive_source_implementation.py` passes all
three groups. Results are in
`adaptive_source_independent_implementation_verification.json`:

- 38 source-helper cases, including empty baseline and a strict maximum
  outside the baseline support;
- 36 independently assembled dense source maxima with fresh, partial,
  and complete caches, covering 51 fresh and 48 cached retained rows;
- exact checks of every principal cache/source ledger formula, including
  degree replies, first and repeated entries, source updates, maximum
  comparisons, and temporary reclamation;
- two full adaptive cases and five stage optima checked by independent
  exhaustive dense KKT solves;
- three noninitial repaired-source probes and three non-dyadic parameters,
  with exact numerator/degree cancellation checks;
- a near-zero target case exercising a zero-iteration final stage;
- exact reconciliation of all external graph accesses and final objective
  gaps. The actual three noninitial probes added no graph cache records,
  as the stronger support-containment argument predicts.

These checks are additional to the author's inspected eight tiny calls,
24 stage comparisons, four stage replays, 16 source passes, high-degree
boundary fixture, and direct/zero-step tests. No timing experiment was run
by this independent audit, and no uniform performance improvement is
inferred from correctness or from fewer possible stages.

## TeX transcription

`app:adaptive` correctly transcribes the repaired-source range, the special
initial quarter step, factor-two-to-four **nonfinal** decrease, terminal
clamp qualification, current-stage invariants, and geometric reciprocal
sum. It pays source formation, repeated initialization, zero-iteration
repair, and first/cached row work. The factor-four deficit reference and
the exact proposed-parameter encoding agree with the independently proved
formulas. It preserves direct branches and makes no universal elapsed-time
claim. No correction is required.
