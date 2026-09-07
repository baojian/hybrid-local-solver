# Local exact continuation on asymmetric cycles

Date: 7 September 2026 (Asia/Shanghai).
**Proved here** means a proof draft awaiting independent review.
The authoritative statement is `thm:op3-local-cycle` in
`sections/op3_local_cycle.tex`; `cor:op3-local-cycle-acl` gives its OP3-scale
ACL consequence. **Open:** arbitrary-graph OP3.

## What is now concrete

There is an implemented exact local obstacle solver for a promised simple
cycle with arbitrary numbers of pendant leaves, including a seed on a leaf.
The graph size, cycle ordering and future leaf counts are unknown. Only
degree replies and adjacency rows are used. Every scanned row belongs to
a vertex positive in the final optimum.

For `M=D-gamma*A`, `gamma=1-2*alpha/(1+alpha)`, the solver minimizes
`u^T M u/2 - (e_seed-lambda*d)^T u` over `u>=0`.
The output `bar_alpha*D*u` has ACL coordinate error at most `lambda*d`.
Its charged exact-real word work is `O_tilde(1+vol(support))`, and
`lambda*vol(support)<=1`; set `lambda=eps_appr` for the desired
`O_tilde(1/eps_appr)` scale on this family. Dictionary operations, degree
replies, adjacency entries, state access and final output are included.
Coefficient bits and numerical stability are separate obligations.

This is an exact obstacle solve using source-potential continuation. It does
not promise the literal intermediate trace of Wei--Yang's algorithm and
does not supply the general geometric-publication producer.

## Why two tips are enough

Increase the cycle seed's conditional potential `t` from zero. The reduced
source derivative is a continuous, strictly increasing piecewise-affine
function. At each state compare its root to the next activation event.
Only the two ends of the exposed cycle interval can introduce another cycle
vertex; all other events are known pendant-leaf groups.

A leaf group activates when its center potential reaches `lambda/gamma`.
A next one-sided cycle neighbor requires at least `2*lambda/gamma`.
Therefore every interior center has settled its leaves before the advancing
tip leaves it behind. Its elimination record is fixed thereafter. Each
record contributes two accumulated coefficients to the source derivative,
is written once, and is read once in the final reverse pass.

When the two unadmitted candidate labels match, the last inactive vertex
receives both tip loads. Its activation can precede a tip's leaf event.
Retain both tips and this last vertex in a Schur block of dimension at most
three; finish any remaining leaf groups there. This closes the exception
without rescanning the old prefixes. At most five event candidates are
inspected at any state. The only nontrivial linear systems have dimension
at most three.

For a leaf seed, eliminate its positive source response into its adjacent
cycle center first. If that center's modified load is nonpositive, return
the seed alone without reading the center's adjacency row. Otherwise use
the same algorithm with modified root diagonal and load.

## Measured evidence

The registered exact audit is `incremental_active_set_sdd.local_sun_solver`.
`LOCAL_CYCLE_AUDIT.json` records parameters, code hash and structural counters.
All **5,265** small comparisons pass against a separate exact obstacle
routine: cycles of length three through five, every ordered pattern of
leaf counts in `{0,1,2}`, cycle and leaf seeds, and nine parameter pairs.
Full-graph KKT checks also pass. They are audit work, outside solver counts.

For larger unequal leaf counts and `alpha=lambda=1/1009`:

| Cycle size | Ambient vertices | Positive output | Center rows read | Adjacency entries inspected | Degree replies |
| --- | --- | --- | --- | --- | --- |
| 128 | 380 | 158 | 55 | 213 | 160 |
| 512 | 1,533 | 158 | 55 | 213 | 160 |
| 2,048 | 6,140 | 158 | 55 | 213 | 160 |

All three outputs have support volume 316. These work counts demonstrate
local access for these instances. Elapsed diagnostic times also include
full-graph KKT verification, so they must not be advertised as local solver
runtime measurements. The asymptotic claim rests on the proof and algorithm,
not these finite examples.

## A verified limit: an attachment of length two

**Refuted:** every pendant tree has settled its response by the time its
center's next cycle neighbor activates. Take a branch `c-a-b`, with `a`
degree two, `b` degree one, and `gamma=3/4`. Its first activation is at
`u_c=8*lambda/3`, but the last leaf activates only at
`u_c=56*lambda/9`. A next cycle neighbor of degree three activates between
them at `u_c=4*lambda`. The branch's eliminated diagonal contribution
changes later from `9/32` to `9/23`.

The audit stores a full 15-vertex source-continuation witness on a 12-cycle
with a length-two branch at vertex 1 and a leaf at vertex 2. It verifies
that this late branch change occurs before the final optimum, after the
next one-sided cycle admission. See
`prop:op3-cycle-unsettled-attachment`. This rules out automatically freezing
that branch; it is not a lower bound for the larger graph class.

## Next falsifiable target and context

Try cycles with arbitrary attached paths or trees. The supplied-tree ACT
result compresses each attachment's scalar response, but it does not yet
pay for local discovery or for finding a response knot at an old cycle
center. A valid extension must handle that old event without rebuilding
every prefix or refreshing every boundary key.

The frozen notched-sun reporter in `response_preconditioned_hybrid` is
context/provenance, not a theorem dependency: it concerns a supplied frozen
face, template and constrained stream contract. The present solver concerns
an unknown graph and endogenous obstacle activations on a different family.
The primary mathematical dependencies are this note's elementary Schur and
obstacle arguments. No cross-direction proof import was introduced.

The companion `delayed_reflection_ladder` already proves
`thm:graph-scalar-homotopy` and the symmetry-based pure-cycle result
`thm:cycle-one-pass`; those ideas are prior context, not newly discovered
here. Its `thm:lazy-tree-response` pays one active-ancestor walk per event.
The two-port `prop:aesp-cd-sp-meld-hull-reduction` in `aesp_cd_l1_rppr`
isolates a relevant remaining primitive: persistent affine pullback and
melding of entire threshold hulls. Ordinary named-coordinate solves and
the new scalar ACT do not automatically implement that primitive.
