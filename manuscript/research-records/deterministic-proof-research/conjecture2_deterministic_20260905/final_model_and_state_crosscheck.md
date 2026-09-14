# Final cross-check of model, stored state and access assumptions

This final read-only review concerns the completed proof and its current
implementation. It changes no theorem, numerical code, output or archive.
It examines the points at which an implementation detail could otherwise
silently strengthen the source's model.

## What the main theorem assumes

The authorized OP2 uses a finite connected simple unweighted undirected
graph with positive integer degrees, a point seed, `0<alpha<=1`, positive
regularization, and positive additive objective tolerance. The substantive
regime is `rho<1/d_seed`. In particular `d_i>=1` is used in the safe repair:
an ordinary Euclidean error bound also bounds each degree density error.
This reasoning is not being extended to arbitrarily small weighted degrees.

The exact-real theorem uses only scalar field arithmetic, comparisons,
ordered records and graph-oracle words. The momentum parameter is chosen
by halving; the stopping bound is maintained by repeated multiplication.
Projection locates an interval among finitely many ordered breakpoints and
solves one affine equation. It does not require numerical bisection to an
unknown activation margin, a logarithm primitive, or a floor of an
arbitrary input real. Symbolic output triples represent
`density*sqrt(degree)` without approximating that coordinate.

The bounded-dyadic package is a separate rational-input realization.
Its integer quotient/remainder operations and encoded arithmetic have their
own explicit treatment. The conservative bit bound includes integer
arithmetic and gcd costs. That statement is distinct from the main
arbitrary-real algebraic theorem and does not establish ordinary unchecked
floating-point correctness.

## Why degree denominators do not accumulate

All stored dyadic vectors use counts on a common stage grid. In the two-tree
reporter, a key is represented as an integer numerator divided by a common
stage factor and one vertex degree. Multiplication by its degree cancels
that individual denominator. Thus a subtree's degree-weighted numerator
sum is an integer accumulation; it is not a sum whose denominator is the
least common multiple of all exposed degrees.

Root reconstruction introduces a degree sum, whose bit length is bounded
by the exposed-record count and largest exposed degree. The ideal projected
coordinate is then rounded directly onto the stage grid. Its temporary
root denominator is not propagated into the next stored vector. Similarly,
the upward square sums in source-energy and output certificates retain a
common denominator instead of accumulating individual degree denominators.

The scalar scale is stored as `S/H` and periodically reset. Its update is
an integer multiply/divide followed by downward rounding. No denominator
of the form `(1-theta)^k` is retained in the bounded realization. At an
iteration boundary `sigma>=1/2`, so a feasible correction density at most
`U=4r` gives `X/H<=2U`. Before a rebase the temporary scale remains
positive and the explicitly proved larger constant bound applies. Lazy
neighbor sums add only degree-encoding length and the controlled rounding
error. The source and kinetic neighbor sums remain exact.

The adaptive parameter is rebuilt from the current dyadic baseline and the
original alpha. Its representation therefore contains the current grid,
one maximizing degree and original scalar encodings, rather than a product
of previous stage parameter denominators. Stage tolerances stay above the
global parameter/accuracy lower bound. Optional mass-scaled grids preserve
all incoming baseline fractions exactly, and their lower-grid induction
retains the old logarithmic encoding envelope even when unused precision
can be discarded at the final clamp.

## Why local exposure suffices

Every positive stored correction or kinetic coordinate has already exposed
its entire adjacency row. An unexposed coordinate therefore has zero own
state, source and neighbor response and a negative raw thresholded value.
The projection cannot activate an unknown coordinate. This is the reason
the reporter can omit the rest of the graph; no global support oracle is
implicit in the projection formula.

The core comparison set is analytical. The signed-flow proof charges the
full degree of every emitted coordinate on every iteration. It permits
temporary overshoot and support changes. Downward primal error enters the
response bound for the actual current state; downward mirror rounding has
the correct selected-flow sign. Neither a monotonically decreasing primal
objective nor monotone intermediate support is assumed.

The terminal gradient uses the actual candidate and cached real adjacency
rows. The approximate lazy neighbor sum is not treated as an exact gradient.
Newly positive projected-gradient neighbors are clipped before any new row
scan. Degrees for all candidate/boundary records are already exposed.
The safe repaired vector and old-baseline maximum retain support contained
in the true optimum and the certified density error. Componentwise ordering
is used with a Euclidean error bound; no unsupported componentwise
monotonicity of a `Q` norm is invoked.

All source refreshes, old and new reporter exceptions, repeated cached
accesses, materializations, rebase passes, unsuccessful certificates,
temporary-state disposal and output are charged explicitly. Fixed source
records occupy at most the baseline volume plus its boundary and seed.
In the nontrivial regime `eta/r>=1`, so constant setup and zero-step work
fit the same ledger. No whole-graph validation of the user's oracle is
included: the oracle is assumed to represent the stated graph, and any
computation internal to a user-supplied oracle has its own cost.

## Outcome

No additional model assumption or uncharged graph operation was found.
The original exact-real theorem and the separate encoded-integer extension
retain the qualifications stated in the completed PDF. The final portable
archive is unchanged by this review. Its independent integrity report,
the main proof audits, exact integration records, and final public tests
remain the relevant frozen evidence; this cross-check adds no solver runs
or performance measurement.
