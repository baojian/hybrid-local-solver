# A concrete native producer after the arithmetic floor

This is the next construction/audit target, not yet a proved theorem.
General OP3 remains Open; an inverse-cubic accuracy upper bound would be
a weaker result and should not be presented as the conjectured rate.

## Native gap-threshold push and a fully charged map

For native accuracy e in (0,1), gamma=(1-a)/(1+a) and lambda=e/2,
start with potential zero and original residual e_v. When r_i>e*d_i,
raise the potential by `(r_i-lambda*d_i)/d_i`, set r_i=lambda*d_i,
and add gamma times that increment to every original neighbor residual.

Expected proof obligations:
- All residuals remain nonnegative. Every ever-pushed vertex has residual
  at least lambda*d_i thereafter (a later self-push resets to that value;
  all other updates only increase it).
- Total residual mass starts at one and decreases by
  `bar_a*d_i*increment` at each push. Thus active original volume is
  below 1/lambda=2/e after a nonzero push, and each legal push consumes
  more than `bar_a*(e/2)*d_i` mass. Total degree-weighted updates are
  at most `2/(bar_a*e)`. No exact obstacle solve is needed for this bound.
- A comparison with the exact lambda-obstacle, if desired for additional
  support containment, is a proof object only.
- Every original row is read once, only upon first legal activation, and
  cached as pointers to stable vertex records. Repeated arithmetic on
  these cached rows still pays one unit per entry.
- Every discovered boundary label gets one degree query and one record.
  The number of such labels is at most 1+vol(active), even if some of their
  degrees are huge. Those huge outside rows are never automatically read.

A balanced map is unnecessary for the intended weak bound. Implement a
sorted dynamic array of stable record pointers, with binary lookup and
linear pointer shifting on insertion. There are O(1/e) distinct records,
so all insertion shifts cost O(1/e^2), and all first-scan lookups cost
O((1/e)log(1/e)). Allocate the array by explicit capacity doubling and
charge every new word and copied pointer. Repeated pushes use stored
neighbor pointers, not new label lookups.

Use an intrusive FIFO queue: each vertex record contains `queued` and
`next_queue`, with a queue head/tail. No queue node allocation per event.
The record also stores original degree, potential, residual, active flag
and the exact-degree-sized cached neighbor-pointer array. Record pointers
stay valid when the sorted map shifts or doubles. Enumerate final active
records using the O(1/e)-sized discovered map and allocate output once.

If these invariants hold, native work is

    O(1/(bar_a*e) + 1/e^2),

and total allocated words are O(1/e), including every map generation,
cache, record and output. This is exact-real word accounting; rational
bit lengths can grow substantially in an exact validator. No claim of a
fast numerical source or free dictionary is needed.

## A simple unconditional weak alpha-uniform composition

Use the implemented arithmetic floor with target accuracy eps,
native e=eps/2, B=4/eps and

    a_eff=max(alpha, eps^2/(16+eps^2)).

Then bar_a_eff is bounded below by a constant times eps^2. A native run
terminates with work O(eps^-3), and the paid proper/full-support arithmetic
wrapper adds at most O(eps^-1 log(1/eps)) work. It invokes no second solver.
This would give a deterministic local O(eps^-3) algorithm uniform in target
alpha in the word model, with O(eps^-1) cumulative allocated words if the
sorting/repair helpers preserve that allocation claim. Audit those helpers
rather than assuming their allocation bound from their work bound.

At target alpha>=the floor, use the same native producer and no transfer.
Its faster native mass bound still holds, but the simple uniform theorem
may just state O(eps^-3). Do not call this inverse-accuracy optimal.

## Possible checks

Exact small connected atlas graphs, several seeds and epsilon values,
alpha near one, 1/3, the floor and extremely small target alpha. Direct
full original residual scans are validators only. Check every prefix's
residual identity, active-volume lower-residual mass invariant, map and
queue structure, row-read-once property, cumulative allocation and bound
on degree-weighted updates. Include privately represented huge-hub graphs
that permit degree queries but reject outside row scans. Include a strict
threshold tie, initially empty output, a singleton positive output, full
support requiring a constant shift, and proper-support transfer.

A full run at the floor with exact rational arithmetic can become costly
on small-epsilon paths. Screen before launching larger cases, record
partial/terminated computations honestly, and do not infer bit complexity
from the abstract word budget. Meaningful longer numerical experiments
can use a separately identified fixed-precision model if required, but
must verify the original residual and never replace exact proofs with it.

## Primary-source leads already identified, not yet imported

- Friedrich and Levine, *Fast simulation of large-scale growth models*,
  arXiv:1006.1003v2 (29 March 2012), 27 pages. Primary metadata verified;
  Section 4 is the candidate approximate-odometer correction algorithm.
  Read actual runtime hypotheses before transferring anything. Author PDF:
  https://pi.math.cornell.edu/~levine/fast-simulation.pdf
- Levine, Murugan, Peres and Ugurcan, *The divisible sandpile at critical
  density*, arXiv:1501.07258v2 (13 August 2015), 34 pages, DOI
  10.1007/s00023-015-0433-x. Proposition 2.5 is a least-action lead;
  primary metadata verified but model/statement mapping still needs reading.
  Author PDF: https://pi.math.cornell.edu/~levine/divisible.pdf

The point-source residual process here has degree-scaled capacity and
killing factor gamma; do not silently equate it with a unit-capacity or
infinite-graph sandpile source. Update the literature index/topic with
checked pages and metadata when using these papers in a formal comparison.
