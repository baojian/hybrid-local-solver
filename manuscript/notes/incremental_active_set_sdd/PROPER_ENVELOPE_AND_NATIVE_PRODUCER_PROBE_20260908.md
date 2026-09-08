# Next targets after the supplied-envelope and small-alpha reduction

Status at the seventh third-campaign block: General OP3 remains Open.
The supplied numerical theorem is now composed, and a supplied significant
set of volume V gives `(1+V) polylog(2+V+1/alpha+1/eps+1/p)` work. The
new conditional floor theorem needs an explicit native support-volume
contract. Continue actual active work toward the 600-new-minute minimum.

The eighth block found a simpler route to the intended parameter improvement:
`thm:op3-alpha-independent-supplied-envelope` composes same-load monotonicity
and the reserved-margin constant-shift wrapper. It makes the proposed
proper-envelope cap construction below unnecessary for that goal. Retain
the Poincare and energy ideas for native local-production bounds instead.
Read `FULL_SUPPORT_CONSTANT_SHIFT_PROBE_20260908.md` and continue target 2.

## 1. Proper supplied envelopes may admit stronger parameter bounds

This is a PROPOSED extension, not yet a theorem or audited implementation.
For a supplied proper connected component C of original volume V and
n_C vertices, every vector z supported on C satisfies a Dirichlet bound:

    sum_C d_i*z_i^2 <= V*n_C * z^T L_G z.

For each coordinate, telescope along a simple path to the first outside
zero (at most n_C edges), use Cauchy--Schwarz, then sum original degrees.
Thus the original restricted physical matrix is at least
`gamma/(V*n_C) * D_C`, even when alpha is extremely small.
The exact restricted obstacle, extended by zero, has original residual
nonnegative everywhere. The superlevel lemma bounds its maximum by
`n_C/gamma <= V/gamma`, and its energy magnitude by `V/(2*gamma)`.

A tempting cap at `Ucap=2V/gamma` has two-piece VWF scalar terms agreeing
with the original quadratics below Ucap and affine tangents above it.
The seed's terminal slope can be NEGATIVE; arbitrary boxing therefore
need not preserve the objective. Do not reuse the old componentwise
nonnegative-tail boxing proof here.

A possible repair: capped energy remains convex, and the original optimum
lies below Ucap/2, where the objectives and KKT rows agree. Hence minima
coincide. If a capped output had a coordinate above Ucap, the segment
from the common optimum to the output first hits a cap wall at distance
at least Ucap/2. On that initial segment the original quadratic lower
bound applies, giving objective gap at least

    (gamma/V^2) * (V/gamma)^2 / 2 = 1/(2*gamma).

Convexity bounds that first-hit gap by the final gap. A requested gap
`t=(gamma/V^2)*(eps/8)^2/2 < 1/(2*gamma)` would therefore force every good
output to stay inside the box, without boxing. Reject an outside-box
returned candidate on bad branches, with paid comparisons.

Check the exact source VWF requirements and complete recursion contracts
for negative individual terminal slopes. The existing recursive range
S is the SUM OF POSITIVE PARTS, not the signed sum. Here
`S <= Ucap*V + (eps/2)V`, total curvature <=V, graph weight <=V,
cap radius O(V/gamma), inverse target O(V^2/(gamma eps^2)). The original
seed gate again implies gamma>eps, so all input ranges would be polynomial
in V and 1/eps, independent of 1/alpha. Sum of terminal slopes is positive
because a proper component has at least one original cut edge. A singleton
must be handled directly before graph-edge-range formulas.

Test cap-boxing failure explicitly rather than silently asserting it.
Test exact PSD Poincare bounds and capped objective first-wall implications.
If this works, it strengthens the supplied proper-envelope theorem but
still does not discover the envelope.

## 2. Supply a simple explicit native volume contract

A possible elementary native producer is monotone coordinate pushing on
the lambda=eps_native/2 obstacle. Start at zero; if original residual
r_i > eps_native*d_i, raise x_i by

    (r_i-lambda*d_i)/d_i.

The updated residual at i becomes lambda*d_i; neighboring residuals rise
nonnegatively. Compare iterates to the exact obstacle to prove support
containment and original volume <1/lambda. Total residual mass drops by
`bar_alpha*d_i*delta_x_i`, at least
`bar_alpha*(eps_native/2)*d_i` on every push, yielding degree work
O(1/(bar_alpha*eps_native)). Charge queues, degree queries, sparse maps,
new labels, row entries, output and repeated arithmetic explicitly.

A neighbor may have enormous original degree. Query its degree before
admission or row scanning; maintaining residual on a discovered outside
label is different from paying its entire row. A paid balanced map avoids
ambient-n arrays. All encountered boundary labels count toward total
adjacency work. A zero-residual or threshold tie must terminate cleanly.
An exact obstacle is only a comparison object, not a numerical oracle.

If proved/implemented, this gives a concrete weak alpha-uniform wrapper
bound with a larger inverse-accuracy exponent. It does not establish OP3.
Read existing note/source statements before calling the routine novel.
A stronger accelerated native producer may have an appropriate volume
contract, but importing OP2 requires checking its exact theorem and model.

## 3. Literature and discovery directions

The alpha-to-zero obstacle suggests divisible-sandpile odometers and
least-action principles. Browse primary sources before asserting a link,
algorithm, or complexity result. Existing literature review of dynamic
flows is not a proof of a local event producer. Do not rerun unchanged
expensive BFS/tree/dense-core obstruction audits without a changed rule.

## 4. A possible direct weak alpha-uniform push bound (not yet proved)

For the proposed gap-threshold coordinate push at lambda=eps/2, every
activated vertex has residual at least lambda*d forever. Total residual
mass is at most one, so support volume is at most 1/lambda without invoking
an exact obstacle. On every proper-support state, the new potential cap
bounds x_seed by `2/(gamma*eps)`, hence bounds the magnitude of decreasing
obstacle energy by that quantity. Each legal update decreases energy by
at least `(eps^2/8)*d_i`. This suggests O(1/(gamma*eps^3)) degree work
before full support, where a materialized full graph has volume <=2/eps.
For gamma>=1/2 this is O(eps^-3). For gamma<1/2, the ordinary total-residual
mass argument gives O(eps^-1). Handle the final update that first fills the
whole support separately; its degree is <=2/eps and the pre-update energy
bound is the one available. Full-support detection must be maintained with
charged boundary state; no scan of all active rows after every push.

A full-support phase could use the completed supplied numerical theorem,
or perhaps an arithmetic parameter construction. This is a weak polynomial
inverse-accuracy result, not the target inverse-accuracy OP3 bound. Check
existing sources before claiming novelty.
