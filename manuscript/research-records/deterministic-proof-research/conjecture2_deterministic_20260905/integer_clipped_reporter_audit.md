# Integer-moment two-tree clipped reporter

The separate module `integer_clipped_reporter.py` implements only the
ordered clipped-projection reporter. It changes neither the package nor
the existing reporter. Source-numerator formulas and solver-state updates
are caller obligations, audited separately. No random procedure is used.

## API and represented quantities

Construct `IntegerClippedReporter()`. Its public update operations are

    set_base(vertex, numerator, degree)
    set_exception(vertex, numerator, degree)
    remove(vertex)
    discard(vertex)
    clear()

The vertex and numerator are integers and the degree is a positive
integer. Calling either setter replaces the vertex's old record, including
moving it out of the other tree. A deterministic AVL vertex registry
therefore enforces disjointness. No label hashing is needed. A no-op setter
does not delete and reinsert an identical record.

At projection time the caller supplies positive integers S and G. A base
record `(b,d,i)` represents raw density

    S*b/(G*d) - shift,

whereas an exception `(n,d,i)` represents

    n/(G*d) - shift.

An exception's numerator is the **full** numerator, not an additive
exception layered on top of a simultaneously stored base record. For the
intended source formulas, this means `n_i=S*b_i+H*e_i`. The reporter does
not derive or validate those graph-specific formulas.

Use

    result = reporter.project_counts(
        base_scale=S, common_denominator=G,
        shift=shift, upper=U, cap=M, grid=h)

where h is positive dyadic and at most U. The result has fields
`entries`, `multiplier`, and `cap_active`. Each entry is
`(vertex, positive_integer_grid_count, degree)`; its density is count*h.
Entries are emitted in base-tree key order followed by exception-tree
key order, with vertex ID breaking equal-key ties inside each tree.
This deterministic order need not be sorted by vertex ID.

Only projection root/setup arithmetic uses Fractions. Point updates use
integer comparisons, integer moments, and the integer-key AVL registry.
Even emitted floors return integer counts without constructing a Fraction
per emitted coordinate.

## Integer tree invariants

Each component tree is ordered by `numerator/degree`; comparison uses the
integer cross-products `n_1*d_2` and `n_2*d_1`, followed by the integer
vertex ID if the ratios tie. Each subtree stores

    height, count, sum(degree), sum(numerator).

Rotations recompute these integer fields exactly. The positive global
scale S leaves the base tree's ordering unchanged. Individual degrees
never enter a stored rational denominator, and weighted subtree moments
are literally integer sums rather than fractions whose denominators must
later cancel.

Each point operation costs `O(log(N+1))` integer comparisons in the worst
case, including the registry lookup and any move between the two trees.
Clearing a nonempty reporter has O(N) node-reclamation cost, recorded as
cleared records; dropping a root is not described as free destruction.
The metrics are structural diagnostics rather than an exhaustive count
of every registry operation or machine instruction.

## Scaled waterfill and four breakpoint sequences

The implementation searches the scaled threshold

    q = (gamma + shift)*G,
    W = U*G, target = M*G,

instead of repeatedly constructing physical raw densities. For one
component with scale c in `{S,1}`, the strict tail at q is found by the
integer comparison

    n_i*q_den > q_num*d_i/c,

implemented without division as
`n_i*(q_den*c) > q_num*d_i`. Its degree and numerator sums are combined
with those of the other tree, scaling base numerator sums by S.

Let `(D_l,N_l)` be the combined degree and scaled numerator sums above q,
and `(D_h,N_h)` their counterparts above `q+W`. Then G times the clipped
mass is exactly

    Phi(q) = (N_l-N_h) - q*(D_l-D_h) + W*D_h.

Its right derivative has magnitude `D_l-D_h`. The strict-tail convention
includes an upper-bound equality in the right derivative's free set and
excludes a zero equality, as required.

First evaluate Phi at `q0=shift*G`. If it is at most target, gamma is zero.
Otherwise the root lies between q0 and the maximum scaled key. Cap zero
is handled immediately by that maximum. In the remaining case, binary
search each of the four sorted sequences

    S*b_i/d_i, S*b_i/d_i-W,
    n_i/d_i,   n_i/d_i-W.

For a candidate breakpoint, the exact clipped mass determines which side
retains the root. Exact equality returns immediately, including a plateau
target. After one sequence's search there is no breakpoint from it in
the interior of the remaining bracket. Later searches only shrink that
bracket, so the property is preserved. After all four searches its
interior contains no breakpoint at all.

The lower endpoint has mass strictly above target. Therefore the final
affine interval has positive free-degree sum, and one exact division
gives

    q_root = q_low + (Phi(q_low)-target)/(D_l-D_h).

The returned physical multiplier is `q_root/G-shift`. All queries are
exact rank/tail comparisons, with no tolerance loop or smallest-margin
assumption. Each of the four binary searches makes O(log N) candidates;
each rank and combined tail query costs O(log N). Thus root discovery
costs O(log^2(N+2)) tree work and exact rational operations of bounded
coefficient size.

## Inclusive emission and integer flooring

A rounded coordinate is positive exactly when its ideal projected density
is at least h. In scaled coordinates the reporter therefore queries the
inclusive tail

    c*n_i/d_i >= q_root + h*G.

Equality is included. Only these tails are traversed; all positive ideal
coordinates below h remain unenumerated. Upper clipping does not change
this equivalence because `h<=U`.

Write `q_root=A/B` and `h=h_n/h_d`. For an emitted record set

    numerator = c*n_i*B - A*d_i,
    denominator = G*d_i*B.

The returned count is computed entirely with integers:

    min(floor(U/h),
        floor(numerator*h_d/(denominator*h_n))).

This equals `floor(min(U, raw_i-gamma)/h)`, including upper ties. The
global upper count and cutoff are computed once per query. The emission
phase costs O(log(N+2)+k) tree visits and O(k) integer floor calculations
for k returned records. It performs no Fraction construction per record.

Root fractions can contain one breakpoint degree or one free-degree sum,
but those denominators never enter a tree moment or the next emitted
integer count. The reporter itself accumulates no denominator history.

## Independent verification

`test_integer_clipped_reporter.py` passed all four groups. Its independent
dense oracle constructs all physical raw values, enumerates all clipped
breakpoints, and finds the root by a dense piecewise-linear scan. It does
not call the reporter's moment or threshold routines.

- 3,946 exact projections were compared, including 2,033 active mass caps
  and 879 cases with an upper-bound coordinate.
- Tests cover empty components, empty reporters, zero cap, plateau
  targets, repeated ratio keys, exact grid ties, negative raw values,
  negative shifts, both tree assignments, disparate coprime degrees, and
  huge signed integer labels that reject hashing.
- 2,400 mutation states and 9,000 nodes were checked for order, heights,
  balance, counts, degree sums, numerator sums, ranks, and registry/tree
  disjointness. The reporter's Fraction constructor alias was disabled
  during these insertion/update/move/removal tests.
- A locality fixture had 8,192 positive ideal values below the grid and
  one retained value exactly at the grid threshold. It emitted only that
  one record in 44 tree visits.

Results are recorded in `integer_clipped_reporter_verification.json`.
The component is ready for a separately audited solver integration; these
tests do not themselves certify that a caller supplies the right graph
source numerators or updates them at the right scale transition.
