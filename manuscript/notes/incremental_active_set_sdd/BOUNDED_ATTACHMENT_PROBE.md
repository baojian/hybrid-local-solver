# A bounded region of changing attachments

Date: 7 September 2026. **Proved here:** the two bounds below are new proof
drafts, and the algorithm is now implemented and proof-drafted in
`thm:op3-bounded-attachments`. No independent review has occurred.
**Open:** arbitrary-graph OP3 and
attachments of unbounded size without a corresponding parameter factor.

## Attachment saturation from discounted hitting

Consider a tree component with at most `q` vertices, attached through one
edge to a cycle center of fixed potential `x`. All its loads are
`-lambda*d_i`, with actual graph degrees, and `0<gamma<1`. Write
`a=1-gamma`. For simple random walk in this component, let `tau` be the
first hit of the center and `p_i=E_i[gamma^tau]`.

The unconstrained solution inside the component is

\[
 u_i=p_i\left(x+\frac{\lambda}{a}\right)-\frac{\lambda}{a}.
\]

Indeed `p_i=gamma*sum_{j~i}p_j/d_i`, with the center fixed to one, and direct
substitution gives the negative degree loads. Starting from a child across
one rooted tree edge, the expected time to hit its parent is
`2*|descendant_subtree|-1`. Summing along the at-most-q-edge root path gives
`E_i[tau]<=q*(2q-1)<2q^2`. Convexity of `gamma^t` gives

\[
 p_i\geq\gamma^{E_i\tau}>\gamma^{2q^2}.
\]

Consequently the whole attachment is strictly positive, and its response
has reached its final affine piece, whenever

\[
 x\geq\frac{\lambda}{1-\gamma}
       \left(\gamma^{-2q^2}-1\right).
\]

This is an exact-real analysis bound. The algorithm need not form the large
power or compare approximate numbers at this threshold.

## Potential growth behind a one-sided cycle frontier

Before cycle closure, let `y_0` be the active end potential and `y_{-1}=0`
the next inactive cycle coordinate. Index consecutive active centers toward
the seed by `y_1,y_2,...`. An attached negative-load tree never has potential
greater than its center, by the maximum principle. Thus each nonseed center
equation implies

\[
 y_{k+1}+y_{k-1}\geq\frac2\gamma(y_k+\lambda).
\]

Put `w_k=y_k+lambda/(1-gamma)`. Then
`w_{k+1}>=2*w_k/gamma-w_{k-1}`, with `w_0>=w_{-1}>0`.
The first ratio is at least `1/gamma`, and induction gives
`w_k>=gamma^(-k)*lambda/(1-gamma)`. Therefore

\[
 y_k\geq\frac{\lambda}{1-\gamma}(\gamma^{-k}-1).
\]

At distance `K=2q^2` behind an active cycle end, every attachment of at most
q vertices is fully active. This strengthens the length-one settling rule
to a bounded region of possibly changing responses; it does not incorrectly
freeze the length-two witness immediately after the next admission.

## Implemented local mechanism

Promise a simple cycle with finite tree components attached through one edge
to each center, and take a cycle seed. The maximum attachment size q at
admitted centers is an analysis parameter; it is not supplied to the
algorithm. The number of attachments and cycle length are arbitrary.

- Eagerly eliminate a center at the beginning of each retained arm once its
  attachment cursor is exhausted, leaving at least the last center. Each
  center gets one fixed reverse-substitution record. The first retained
  center is therefore unsettled unless it is the only one, so the preceding
  proof bounds the retained arm by `K=2q^2` without using q to drive the rule.
- Classify the two cycle ports and attached components with bounded probes.
  Try limits 1, 2, 4, ... until exactly two ports remain. The true cycle ports
  always remain marked; an extra port is an attachment exceeding the limit.
  Stop before scanning a row whose degree exceeds the current limit. These
  probes may inspect inactive rows; their work is charged to the center.
- Build every bounded attachment's scalar response and retain its child
  curves. Sort the union of attachment knots in the center's own potential.
  Maintain its current summed affine piece and one next-knot cursor.
  Repeated builds during failed classification trials are also charged.
- The retained arms are tridiagonal. Recompute their affine responses in
  `O(K)` per event, inspect at most `2K+O(1)` center/candidate events,
  and use the exact source derivative to stop or advance.
- At closure retain both arm windows and the last center as one tridiagonal
  path between the eliminated seed-side prefixes, of size at most `2K+1`.
  Finish all remaining knots there, then recover the committed coordinates
  and evaluate the retained attachment curves once.

The proof-draft charged bound is `O_tilde(q^3*(1+vol(S)))`: at most
`O(q*vol(S))` response events, each with `O(q^2)` retained-center work,
plus bounded discovery, curve construction and terminal recovery.
Working storage is `O_tilde(q^2*(1+vol(S)))`, including cached probes.
The implementation checks the window invariant, port classification and
module-knot ties, and meters failed probes and repeated curve builds.
This gives the OP3 scale as a proof draft for each fixed q. It is not a
uniform bound as q grows and does not yet handle a seed inside an attachment.

The registered `bounded_attachment_cycle.py` passes 1,909 comparisons with
a separate exact obstacle solver and eight larger full-graph KKT checks.
It also passes 195 discounted-hitting checks through q=6. Larger tests
include cycle closure after many prefix eliminations, branching modules,
and identical local work on different ambient sizes. The final durable audit
is `BOUNDED_ATTACHMENT_AUDIT.json`. Full-graph validation is audit-only.

For q=2, increasing the cycle from 64 to 256 vertices leaves the exact
positive support at 152 vertices and the same 59 admitted centers, 159 degree
replies, 568 adjacency-entry reads and 354 retained factor rows. For q=3,
the corresponding figures are 157 positive vertices, 54 admitted centers,
168 degree replies, 1,110 entry reads and 469 retained factor rows. The
largest retained region in the eight diagnostics contains five centers.

Next audit the work proof, then investigate attachment-size dependence and
whether partial response construction can avoid reading a large inactive
attachment. The source-specific event-group question remains useful for
unbounded attachments and multiple cyclic cores; it was not resolved by this
structural theorem. These checks are not independent proof review.

## A concrete inactive-discovery obstruction

**Refuted:** the full-classification implementation has a bound independent
of attachment size merely because its final positive support is small.
Take a triangle with seed 0 and attach a q-vertex star through its center
to 0, q>=2. Use gamma=1/2 (project alpha=1/3) and lambda=1/10.
The exact obstacle optimum is `u_0=7/30` and zero elsewhere: the seed
equation holds, each cycle neighbor receives `7/60<=2/10`, and the
attached center receives `7/60<=q/10`. Other vertices receive zero.
Thus the positive support volume is always three.

The current classifier nevertheless discovers and builds the entire star.
For q=4,16,64,256 the exact audit records 6,18,66,258 exposed rows and
27,85,287,1065 adjacency-entry reads. These counts exclude the separate
full-graph KKT audit; see `INACTIVE_ATTACHMENT_AUDIT.json`.
This does not refute the stated q-dependent theorem or any uniform solver.
Indeed, checking the three initial neighbor gates before classification
already avoids this family with constant work. A broader extension must
retain that quietness principle after an asymmetric branch has activated,
when the center's future potential and old response knots still change.

The optional sharper saturation conjecture and its finite polynomial
certificates are in `DISCOUNTED_ATTACHMENT_EXTREMAL_PROBE.md`. Even a proof
would not remove the inactive-discovery issue above.
