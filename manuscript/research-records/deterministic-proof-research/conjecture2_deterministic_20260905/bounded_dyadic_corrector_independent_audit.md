# Independent implementation audit: bounded dyadic corrector

Audited the current `bounded_dyadic_corrector.py` without modifying it,
including the weighted AVL operations it imports from fresh task files.
This is a stage-corrector audit; the file does not implement the final PG
repair, outer continuation, or optional approximate-sum rebase.

## Result

No correctness or locality defect was found in the stage implementation.
Its stored-state updates realize the exact-sum version of the bounded
dyadic proof. There is one important limitation of the diagnostic bit
counters: reduced rational sizes are not the maximum sizes of every
integer formed inside Fraction arithmetic. The file's tracker docstring
already distinguishes them. The limitation does not invalidate the
bounded-bit theorem, but it must be preserved when reporting measurements.

The independently added diagnostic is
`audit_bounded_dyadic_corrector.py`; its exact result is in
`bounded_dyadic_independent_verification.json`. It passed 52 stage steps,
208 independently reconstructed raw identities, and 632 full tree audits
following key updates. Those audits checked 2,522 tree nodes, including
their actual common-denominator divisibility, subtree moments, counts,
heights, and AVL balance.

## Concrete code checks

### Parameters and source normalization

Lines 225–254 enforce reciprocal-power-of-two momentum, the correct
`mu<=alpha<4mu` relation, dyadic baseline densities, and a grid fine enough
to represent every baseline value exactly. The additional grid ceiling
`theta*alpha^2*rho/27` correctly preserves the work bound even when a
standalone caller requests a loose objective tolerance.

Lines 279–291 form the source density

    alpha*1_seed/d_i - q0*baseline_i + c*sum_adj baseline_j/d_i

and check its bounds and exact degree-weighted mass identity. Every
nonzero source location is in the union of baseline support, its exposed
neighbors, and the seed. Other vertices have source zero, so no global
source scan is missing. Baseline containment below the true optimizer is
an analytical caller precondition, explicitly documented at lines 217–219;
the constructor does not purport to certify that precondition itself.

### Exact reporter and grid ties

The strict tails in `box_mass` correctly compute the clipped mass and the
right-hand affine slope. The two sorted breakpoint searches at lines
155–173 retain the exact root bracket. Equality returns before a flat
interval could cause division by zero. The selected affine root uses an
exact positive degree sum, without a numerical-margin stopping rule.

Lines 188–194 implement a closed tail. Lines 202–206 use precisely the
threshold `(shift+eta+h)/sigma` and floor only emitted ideal values.
Consequently ties at one grid unit are retained, and discarded positive
sub-grid coordinates are not enumerated first. The upper cap is applied
before grid flooring. Projection's ideal mass is evaluated through
moments before rounding, as required by the perturbation theorem.

### State transition and neighbor sums

Lines 390–392 remove every old exception before any primal mutation or
scale change. Lines 401–406 floor the new normalized X and record the
actual stored difference, rather than the intended increment. Lines
410–418 scan each emitted kinetic row once, simultaneously constructing
the exact next kinetic neighbor sums and scattering actual X changes.

The scale changes only after the old exceptions have been removed. At an
ordinary step, all changed own-coordinate and neighbor response keys are
refreshed, then the new sparse kinetic/source exceptions are installed.
An old kinetic exception which disappears is therefore restored to its
base key rather than left with a stale scale denominator.

The response at lines 338–343 uses `(q0-mu)X_i-c L_i/d_i`, including the
essential destination-degree denominator. The independently reconstructed
raw identities use the full y/Q formula and match the implementation,
including nonsquare alpha and a nonzero dyadic baseline.

### Rebase and full charge

Lines 369–377 floor every currently stored X, discard resulting zeros,
and rebuild exact neighbor sums from the surviving stored state. It is
valid to scan only those surviving rows: the entire former scalar X map
has already been visited, and the old response map is replaced outright.
Lines 380–382 refresh every exposed key, including records whose old
response has become zero. Thus no stale base key survives a rebase.

`_row` charges first exposure separately from every cached adjacency read.
The independent fixture used a seed adjacent to three hubs of respective
degrees 1,000,003, 1,000,033, and 1,000,037, with a nonzero seed baseline.
Only the seed's adjacency list was ever queried. It incurred exactly
3 baseline, 156 selected, and 51 rebase adjacency-entry reads. All 17
rebases refreshed the four exposed records without scanning a hub row.

These large pairwise-coprime boundary degrees also exercise the dangerous
denominator case: individual keys contain unrelated degree factors, but
their stored weighted moments cancel those factors exactly. At every
key-update checkpoint each weighted key and subtree moment denominator
divided `2*den(alpha)*H*(T+1)*S`, with `h=1/H`, `theta=1/T`,
and `sigma=S/H` at that checkpoint.

### Certificate and output

The block schedule uses `block_size=1/theta` and a dyadically decaying
upper bound once per complete block. It does not retain an exact power
of a at each iteration. The objective certificate is valid between
blocks as a conservative bound as well as at the prescribed endpoint.
The output represents the actual `baseline+sigma X` in degree densities,
with three charged output words per nonzero coordinate. It is not yet the
safe, clipped terminal output of the outer algorithm; that is intentionally
outside this component's API.

## What the bit counters actually prove

`Tracked` wraps explicit reporter operations and records reduced Fraction
operands/results. Its comparisons additionally measure the two integer
cross-products. It does not inspect the unreduced integers formed by
Fraction addition, multiplication, division, or gcd reduction. Some
parameter-setup expressions also execute as ordinary Fraction arithmetic
before their final values are measured.

A direct exact counterexample to interpreting the reduced counters as
all-intermediate counters is

    10402/10403 + 1/20604 = 21011/21012.

The existing tracker records a maximum numerator and denominator length
of 15 bits. Independently tracing Fraction's addition on this operation
observes the pre-reduction integer `2122111`, which has 22 bits. The new
diagnostic confirms both measurements. The implementation's measured
59-bit values in the sibling suite must therefore be described as
reduced rational numerator/denominator sizes.

There is a simple rigorous replacement for an exact internal trace. If
every operand numerator and denominator of one binary rational operation
has at most b bits, forming unreduced products needs at most 2b bits, and
adding or subtracting the two cross-products needs at most 2b+1 bits.
Gcd remainders and exact divisions do not increase that bound. Thus
`2b+1` is a conservative internal-integer envelope for that operation.
Applying it globally requires an operand bound which also covers setup
arithmetic; the bounded-coefficient proof supplies such a bound. A future
instrumented implementation can record this envelope operation by
operation, separately from the reduced-rational measurements.

In the new local fixture, the reduced numerator/denominator maxima were
35/48 bits, and explicitly measured comparison products reached 81 bits.
Those distinct numbers already illustrate why a single reduced-size
counter should not be called an all-arithmetic word size.

## Remaining implementation scope

The component still uses Python dictionaries and sets for point maps.
Integer-key iteration is deterministic for this usage and no randomized
numerical algorithm is called, but hash-table operations do not establish
the theorem's worst-case balanced-map cost. That replacement is separate
from the correctly balanced projection reporter. Structural metrics count
specified operations rather than every interpreter instruction.

No change to the production corrector was needed for this audit. Safe
continuation, terminal repair, and scalar-only rebasing should be checked
as separate implementations when added; the present exact-sum tests do
not certify those absent components.
