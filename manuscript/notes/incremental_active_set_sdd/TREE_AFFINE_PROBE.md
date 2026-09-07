# Overnight probe: affine composition of tree responses

Date: 6 September 2026. **Proved here:** the algebra below is a proof draft.
The persistent implementation is now audited and the supplied-tree word-work
proof is in `main.tex`, Section `sec:op3-persistent-tree`.
**Open:** local discovery at the OP3 scale on arbitrary trees and arbitrary
cyclic graphs.
This is a mechanism to investigate, not an OP3 resolution.

## Why this is worth testing

The existing `spectral_balance_threshold_batch/README.md`, Section 2.3,
builds scalar tree response functions in work proportional to the sum of
subtree sizes. On deep trees that is quadratic. The scalar response curve
can instead be transformed by one affine map of its graph in the plane.
That suggests replacing explicit breakpoint lists by affine composition trees
(ACTs), with small-to-large merging.

The existing `delayed_reflection_ladder` theorem `thm:lazy-tree-response`
already gives an exact local tree algorithm with work
`O(vol(S)+log(1+Delta)*sum_{v in S} dist(seed,v))`, hence the product scale
`O_tilde(1/(rho*sqrt(alpha)))`. Its lazy streams read no descendant of an
inactive vertex but forward each event through every ancestor. The new
supplied-tree ACT theorem removes repeated curve materialization; it has not
yet removed that ancestor cost while preserving lazy local discovery.

The relevant primary source is Agarwal, Phillips and Sadri,
[*Lipschitz Unimodal and Isotonic Regression on Paths and Trees*](https://www.cs.toronto.edu/~sadri/publications/regression.pdf),
author manuscript dated 2 January 2010. Section 3, Theorem 3.1 (PDF p. 7),
supplies constant-time whole-curve affine transformations and logarithmic
evaluation, inverse evaluation, insertion and interval transformations,
provided the curve stays monotone in both coordinates. The following RPPR
adaptation is our own argument, not a theorem stated in that source.

## Supplied-tree formulation

Use the OP3 degree form

\[
\boldsymbol M=\boldsymbol D-\gamma\boldsymbol A,\quad
\gamma=1-\bar\alpha,\quad
\boldsymbol b=\boldsymbol e_v-\lambda\boldsymbol d,
\qquad
\min_{\boldsymbol u\geq0}
\tfrac12\boldsymbol u^\top\boldsymbol M\boldsymbol u-
\boldsymbol b^\top\boldsymbol u.
\]

Here the tree and its degree/grounding data are supplied. Root it at the
single positive-load vertex `v`. All other loads are `-lambda*d_i`. For a
nonroot vertex `i`, condition on its parent's degree potential `t`. Let
`u_i(t)` be its value in the optimal descendant subtree, and define

\[
\mu_i(t)=\gamma u_i(t),\qquad \nu_i(t)=t+\mu_i(t).
\]

Adding `t` makes `nu_i` strictly increasing even when `mu_i` has a flat zero
branch. Extend that initial branch to negative inputs by `nu_i(t)=t`; this is
only a data-structure extension, not a negative feasible potential.

If `i` has `k_i` children, put

\[
S_i(x)=\sum_{j\text{ child of }i}\nu_j(x),\qquad
H_i(x)=(d_i+k_i)x-b_i-S_i(x).
\]

For `x>=0`, `H_i` is the derivative of the descendant objective conditioned
on `u_i=x`. Its slopes are positive Schur diagonals, and are at least
`bar_alpha*d_i`: the local grounding term alone contributes that much to the
minimum quadratic energy with the root potential fixed to one. Thus `H_i`
is strictly increasing and piecewise affine. Its slopes decrease as more
descendants become active, because the inverse-positive response slopes
increase. Consequently `mu_i` and `nu_i` are convex.

Form `H_i` from the graph of `S_i` using the single affine map

\[
(x,y)\longmapsto
\bigl(x,(d_i+k_i)x-b_i-y\bigr).
\]

For a nonroot `i`, the positive branch obeys `H_i(u_i)=gamma*t`. Apply the
single affine map

\[
(x,y)\longmapsto
\left(y/\gamma,\ \gamma x+y/\gamma\right)
\]

to the graph of `H_i`. This gives the graph of `nu_i` above the activation
threshold

\[
t_i^0=-b_i/\gamma=\lambda d_i/\gamma.
\]

All inherited knots come from child knots at positive `x`, so their new
abscissae lie strictly above `t_i^0`. Insert `(t_i^0,t_i^0)` and replace the
left unbounded ray by `nu_i(t)=t`. Only one new knot is created at this
vertex. Both affine maps have nonzero determinant and take the relevant
curve to another strictly increasing curve.

At the seed, form `H_v` and evaluate

\[
u_v=\max\{0,H_v^{-1}(0)\}.
\]

Recover a child value by `u_i=(nu_i(u_parent)-u_parent)/gamma`. This
requires retaining each child's curve for the final traversal. The case
`gamma=0` is diagonal and handled directly.

## Work bound and the reconstruction obligation

Each curve has at most one knot per vertex in its subtree. Use the child
with the largest subtree as the accumulated curve and merge the others.
Each knot belongs to a smaller child on at most `O(log n)` ancestor merges.

There is a particularly simple ACT addition implementation here. Every
`nu_i` has the hinge representation

\[
\nu_i(t)=t+\sum_a c_a(t-t_a)_+,\qquad c_a\geq0.
\]

To add a smaller child curve, first apply the global shear adding `t` to
the ordinate. For each positive hinge, insert its abscissa if necessary and
apply the suffix shear `y += c_a*(x-t_a)` on `x>=t_a`. These operations
preserve strict monotonicity, including at the boundary of the suffix.
They cost `O((number of smaller-child knots+1)*log n)` using Theorem 3.1.
This avoids assuming that arbitrary independently transformed summands still
represent a transformed sum.

The resulting forward cost is `O(n log^2 n)` algebraic word work,
plus graph/degree input. Terminal curve evaluation costs `O(n log n)`.
**Do not silently discard child curves.** Destructive small-to-large merging
would invalidate reconstruction. The implemented remedy is a persistent
AVL tree with affine lazy tags. Each logarithmic update copies only
logarithmically many nodes, and each global affine transformation copies only
the root. This gives `O(n log^2 n)` total allocated words as well.
The authoritative proof draft is `thm:op3-persistent-tree` in the note;
the retained-version audit is described below.

Coefficient-bit growth and numerical stability are outside this exact-real
word-model claim. Unlike the generic source's tree-regression objective,
the RPPR adaptation and its support/output conversion must be audited here.

## What does not follow

1. This is a supplied-tree solver. Constructing every message by reading the
   full ambient tree is not charged by the unknown optimal support. A local,
   demand-driven construction is still needed for OP3, even on arbitrary
   rooted trees.
2. A fresh near-linear tree solve on every tiny growing face remains too
   expensive. The data structure must preserve useful state between solves
   or generate only a paid prefix of each response.
3. A sum of ACTs cannot be inverted or subjected to a general inverse-type
   affine map by transforming each summand independently. For `F(x)=x` and
   `G(x)=2x`, `(F+G)^(-1)(1)=1/3`, whereas
   `F^(-1)(1)+G^(-1)(1)=3/2`. Our construction coalesces a sum before the
   inverse-type transform. Do not import the source's tree-set operations
   outside transformations for which distributivity has been checked.
4. Cyclic separators have more than one potential parameter. Scalar
   monotone curves do not automatically extend to a compact multidimensional
   response surface. Growing attachment rank remains the principal test.

## Exact audit and next action

The registered `tree_affine_response.py` uses explicit rational curves and
compares the reconstructed vector against a separate exact obstacle solve.
All **1,152** small-tree comparisons passed: all 13 nonisomorphic trees
through six vertices, all seeds, three teleportation values, three positive
regularizers, and ordinary versus additional diagonal-grounding data.
Convexity, strict monotonicity and the zero-response branch are checked.

Eight path/star diagnostics of sizes 16--128 separate logical affine
operations from dense breakpoint materialization. On the 128-vertex path,
the reference visits 16,384 curve points for only 255 logical affine maps
and 127 zero-branch insertions. These are operation diagnostics, not a
measured fast ACT implementation. Its final support is 66 vertices, which
also illustrates the gap between a supplied tree and local discovery.

The new `persistent_affine_tree.py` implements immutable AVL nodes, affine
lazy tags, positive-hinge suffix merges, and retained child versions. Its
1,152 exact comparisons pass, as do 43,614 value/inverse round trips and
19,584 retained-version queries against separate exact obstacle solves.
`PERSISTENT_TREE_AUDIT.json` records the final source hash and all counters.
Twenty-four path/star/binary/comb diagnostics up to 512 vertices confirm that
the implementation visits and allocates tree nodes instead of repeatedly
materializing whole curves. For example, the 512-vertex path allocates
17,613 nodes, with maximum curve height nine; it still reads the whole tree
although only 66 output coordinates are positive.

Next seek a demand-driven/local construction. The adjacent cyclic probe
`LOCAL_CYCLE_PROBE.md` gives a different fully local mechanism for cycles
with unequal leaf counts, together with an exact obstruction to immediately
extending it to length-two attachments. Preserve the live-frontier accounting
in `FRONTIER_ELIMINATION_PROBE.md` as the broader cyclic baseline.
No independent proof review has yet occurred.
