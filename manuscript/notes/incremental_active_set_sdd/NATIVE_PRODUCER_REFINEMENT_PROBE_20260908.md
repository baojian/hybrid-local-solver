# Native producer refinements after the checked cubic reference

These are follow-up targets, not completed new theorems. General OP3
remains Open. Do not mistake recovering an existing quadratic accuracy
power for progress on its inverse-linear target.

## Remove the observed full-support constant mode

`NativePush` records every neighbor of every positive vertex. Therefore,
immediately after a completed push, equality of the active-record count
and discovered-record count certifies that the positive support is closed.
Connectedness then makes it the whole original graph. This uses only two
maintained counters; no ambient n or further row query is needed.

At this moment x<=u for the native lambda obstacle, by the proved push
comparison. Since every coordinate of x is positive, the exact obstacle
is fully positive and solves the unconstrained system M u=e_v-lambda*d.
All original rows are already cached and their volume is below 2/e.

Next implementation target: a charged exact LDL^T elimination on this
known whole graph, followed by the arithmetic target-alpha transfer.
Count matrix allocation, label lookup, elimination, triangular solves,
residual-state replacement and output. This is O(n^3) work and O(n^2)
live matrix words, so it retains a weak cubic accuracy bound but should
remove the 1,744-push two-vertex case. Do not use the audit's existing
dense obstacle routine as an uncharged production solver. A later
source-backed supplied solver can be substituted with its actual contract.

## A conservative native alternative

At gamma=1 residual mass no longer decreases. However, as long as support
is proper, every edge potential difference is at most one and the maximum
is at most the positive-support cardinality. The strict activation volume
bound still follows from residuals of all previously pushed coordinates.
An energy decrease of at least (e^2/8)*d_i per gap push may therefore bound
pre-closure degree work by O(e^-3), without a teleportation floor in that
part of the computation. The full-support exception requires explicit
treatment and must not be hidden in that potential bound. Prove this
before coding or claiming finite termination in the conservative case.

More precise candidate, derived after the first draft: use native accuracy
e=eps_appr and lambda=e/2. For a conservative prefix with proper support,
max(x)<=|S|<2/e follows from the superlevel flux argument without a killing
term. If the next push first closes the whole graph, its newly positive
coordinate is at most one (its prior residual is at most total mass one),
and all old values were at most n-1. Stop immediately at that first closure.
Consequently every processed prefix still has max(x)<2/e. Since each push
increases its coordinate by more than e/2,
sum_pushed d_i < (2/e)*sum_i d_i*x_i < 8/e^3.
This is a direct monotone-value budget and is stronger than the proposed
energy constant. It needs no existence of a global conservative obstacle.

If the queue empties on proper support, transfer UP to the target positive
teleportation when bar_alpha<=e^2/4: target residual equals r0-bar_alpha*A*x.
On positive coordinates, r0>=lambda*d and max(x)<2/e preserve nonnegativity;
on zero coordinates nonnegativity is direct. The upper bound only decreases.
For larger bar_alpha, use the original target-alpha gap push instead; its
mass bound already gives at most 8/e^3 degree-weighted updates.

On early full closure, all graph rows are cached with volume below 2/e.
One charged dense solve of the UNREGULARIZED target system M_alpha*y=e_v
gives exact nonnegative PageRank potential. It is not necessary to assume
the target lambda obstacle remains full after increasing teleportation.
This last distinction prevents an invalid same-support obstacle import.
The combined candidate retains O(e^-3) work, improves the volume constant
to 2/e, and uses O(e^-2) live matrix words only on full closure. It requires
a new implemented audit and proof before replacing the checked reference.

## What importing the existing OP2 theorem would actually buy

The actual proof of `active_edge_lcp`'s `thm:op2` and `thm:batch-depth`
was read, including certified face solves, safe admission, block-Cholesky
causal domination, the Chebyshev tail argument, objective projection,
and expected-work charging. No formal import has yet been made.

For native lazy parameter a and bar_a=2a/(1+a), canonical variable X and
physical variable u obey X=bar_a*D^(1/2)*u. With rho=lambda, the canonical
objective is a*bar_a times the physical obstacle objective. A canonical
objective gap t gives physical coordinate error at most
sqrt(2t/a)/bar_a because original degrees are at least one.

For native output accuracy e=eps_appr/2, take lambda=e/2 and delta=e/8.
Request t=a*bar_a^2*delta^2/2; then clip the physical approximate vector
down by delta. Its error from the full obstacle is at most 2delta and
its original residual lies between zero and (lambda+2delta)*d < e*d.
The same positive-coordinate margin proof as the significant-envelope
corollary applies. The OP2 faces lie in the rho-obstacle support, whose
original volume is at most 1/rho=4/eps_appr.

At the arithmetic floor a>=eps_appr^2/(16+eps_appr^2), the imported
expected work would be nearly O(eps_appr^-2), with target-alpha removed
even from numerical logarithms. This requires an explicit dependency edge
to `active_edge_lcp` if made into a claim, and a complete handling of its
failure flag, format caps and paid original-label conversion. Its source
SDD solver is not implemented by a dense finite audit. The quadratic
power is already available in the Wei–Yang source, so this is primarily
an interface cross-check, not the strongest next research direction.

## Source lesson

The least-action analogy supplies comparison structure; FL's fast
odometer work requires a useful approximate odometer and a paid correction
step. A productive stronger target must bound both domain discovery and
correction work. Relabelling repeated topplings or importing the initial
batched O(E+V) calculation does not resolve either obligation.
