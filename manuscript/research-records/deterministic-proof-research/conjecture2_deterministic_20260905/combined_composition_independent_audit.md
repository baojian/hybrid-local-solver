# Independent audit of the combined certified corrector

Inspected `combined_certified_dyadic_rppr.py` and the completed
`combined_certified_dyadic_audit.md`, together with the two previously
independently audited parent implementations. The combined source SHA-256
is `0bdc7425c424c4c16b957d07f2fd4c9551e293c2b1b5465b55ea6fef9a503122`.
No implementation was changed.

**Finding: the composition is sound; no correction is requested.**

## Dispatch and certificate ownership

The actual MRO is Combined, EarlyStop, Binomial, SourceEnergy, Integer.
Initialization therefore computes the source and binomial horizon before
installing checkpoint state. The checkpoint run loop uses that tighter
horizon. A step first invalidates any accepted independent bound, executes
the unchanged integer recurrence once, and updates the binomial block power
before returning. The fallback property dispatches from EarlyStop directly
to Binomial, so it cannot accidentally report the older half-block bound.
All diagnostic layers are retained.

An accepted independent scalar belongs to the current full candidate and
iteration. The candidate is returned unchanged and supplies the objective
gap needed by the unchanged terminal PG/grid/max repair. After manual
stepping the scalar is cleared, and the valid binomial prefix certificate
becomes visible. The independent scalar need not bound the full accelerated
energy; the underlying energy theorem continues to hold separately and is
the premise used by the locality proof.

Zero-step stages use the source initial bound without a fictitious
perturbation term. Rejected checks cannot prevent the fixed binomial
fallback from returning with gap below tau. The unchanged continuation body
also preserves the alpha=1 and zero-solution direct branches. Its isolated
class-binding copy is verified to reuse the identical wrapper code object.

## Work and encoded arithmetic

For identical stage inputs, every numerical state and graph access is a
prefix of the binomial parent's trajectory. Checks only read caches, whose
completeness follows from past baseline/emitted-row scans. They leave the
recurrence, source, reporter, and counters controlling the horizon intact.
Temporary checker maps are reclaimed after each check.

The prior prefix ledger gives candidate volume at k at most `(1+360k)/r`.
Restricting checkpoints to `T,2T,4T,...` below the binomial horizon retains
`sum k_j<2*k_actual`; added materialization/check/disposal work remains
`O((k_actual+1)log(N+2)/r)`. Initialization and final PG work are paid even
at zero steps. All inherited repeated scalar-rebase and source-setup
charges remain present. Thus the composition preserves the existing
cubic-log arithmetic and conservative bit bounds.

Binomial powers use at most `16q+1` bits. Candidate density denominators
divide H^2; checker integer accumulation uses one common denominator and
upward per-degree divisions, never a degree LCM. Both refinements therefore
fit the established O(B)-bit envelope simultaneously. Neither failed
certificate denominators nor earlier block powers enter the stored vectors.

The source note's same-input stagewise return-time comparison is valid:
the combination makes the same geometric checks as the early-only parent
until the earlier binomial endpoint, where fallback can terminate it. This
does not imply lower total work for every complete continuation, because
later repaired baselines can differ. The note makes that distinction.

## Independent bounded evidence

`audit_combined_composition_independent.py` adapts the independent cached
checkpoint audit to a separately instantiated binomial reference.
`combined_composition_independent_audit_results.json` records all passes:

- 794 exact reference-state and complete-energy prefixes, including scalar
  block powers and their bit bounds.
- Four complete cases and seventeen stages, with exact KKT optima, final
  objective gaps, monotone repairs, and repaired source bounds.
- 44 checkpoints: 17 accepted and 27 rejected. Every check runs with the
  external oracle locked to raise; all 264 temporary maps are reclaimed.
- A genuine fallback following failed checks, a zero-step stage, manual
  accepted-bound invalidation/resumption, and two exact direct branches.
- Explicit MRO, wrapper code identity, isolated class binding, combined
  diagnostic fields, and the current-state certificate selected on every
  returned path.

Parent-specific manual checkpoint skipping and exception cleanup were
already independently tested in `early_stop_independent_audit.md`; this
bounded composition run does not claim to repeat those cases. No practical
timing claim is inferred from these correctness tests.
