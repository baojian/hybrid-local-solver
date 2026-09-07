# Fixed-lambda root thresholds: results and remaining representation

Date: 7 September 2026. The algebra and finite witnesses below are **Proved
here** as drafts awaiting independent review. General OP3 remains **Open**.
Proof authority is `sections/op3_root_threshold_groups.tex`; the next
constructive target is `ORDERED_PATH_CLUSTER_PROBE.md`.

## The exact update is now identified

On a current connected positive tree face U, retain the source potential t
and eliminate E=U without the source. Write the old potentials as
`u_i(t)=h_i t+z_i`, with h_source=1 and z_source=0. For a frontier child j,
its gate is `a_j t+b_j`, where a_j>0 and b_j<0; set tau_j=-b_j/a_j.

Define root-path resistance by summing `1/(gamma h_parent h_child)` along
the active path. The harmonic diagonal change turns the interior matrix
into a grounded weighted-tree Laplacian. Consequently

`G_px = h_p h_x R_LCA(p,x)`.

For admission of w with parent x, let
`delta=d_w-gamma^2 G_xx>0` and `kappa=gamma^2 h_x^2/delta`.
A surviving frontier j, grouped by ell=LCA(parent(j),x), obeys

`tau'_j = tau_w + (tau_j-tau_w)/(1+kappa R_ell)`.

Thus each group has a positive affine threshold map and preserves its
internal order. Different ancestor groups have different maps. Old active
harmonic and resistance coordinates also have explicit updates:

`h'_p=h_p(1+kappa R_ell)` and
`R'_p=R_ell/(1+kappa R_ell)+(R_p-R_ell)/(1+kappa R_ell)^2`.

See `lem:op3-root-resistance-transform` and
`cor:op3-root-coordinate-update`. These identities do not charge group
identification, membership changes or searches; they are not a data structure.

## Refuted shortcuts, with their exact scopes

- **Refuted: a stale global threshold order suffices for exact quietness.**
  The nine-vertex tree with edges `01,05,12,23,34,56,58,67`, source 0,
  alpha=1/7 and lambda=1/40 has FIFO prefix `0,1,5,2,6,8`. Before 8,
  only 8 is positive; thresholds 3 and 7 are respectively 88/135 and 31/45.
  After 8 they are 88/135 and 43/72. Rechecking only old minimum 3 finds
  a negative gate, while 7 has positive gate 373/142880. Its original
  residual still meets the looser ACL tolerance; this witness alone does
  not refute ACL stopping. See `prop:op3-tree-fixed-threshold-order`.
- **Refuted: minimum-threshold admission restores exact order/quietness.**
  A different nine-vertex tree, edges `01,06,12,14,15,23,67,78`, source 0,
  alpha=1/7, lambda=1/31, follows minimum-threshold prefix `0,6,1,7,4,5`.
  After 5, the old minimum 8 remains negative, at -35/115847, while 2
  becomes positive, at 215/115847. Every selected minimum and previous
  gate is checked at that fixed lambda. See
  `prop:op3-tree-minimum-policy-order`.
- **Refuted: stale-minimum validation certifies ACL for every legal trace.**
  A fifteen-vertex canonical tree at alpha=1/1009 and lambda=2/51 has
  legal prefix `0,1,2,3,4,5,6,7`. Before 7 it is the only positive
  frontier candidate. Afterward old minimum 8 remains quiet, while the
  original residual at 9 exceeds its ACL tolerance by a factor
  `194118268149174442122/182466278813571685633`, approximately 1.0638583.
  The graph, all coefficients and each positive prefix gate are saved in
  `ROOT_THRESHOLD_WITNESSES_AUDIT.json` and the proof is
  `prop:op3-tree-stale-minimum-acl`. This prefix is a legal selected order,
  not a claim about the minimum-threshold policy.

None of these statements refutes the implemented physical-flux queues or
lower-bounds local algorithms. The distinct policy and stopping scopes matter.

## Exact audits

`ROOT_THRESHOLD_ORDER_AUDIT.json` records 22,440 traces on all nonisomorphic
trees through nine vertices, every seed, six parameter pairs and five
policies: exact minimum, FIFO, LIFO, and physical-band FIFO/LIFO. It verifies
110,542 legal admissions, 115,237 Schur row updates, 46,912 same-ancestor
factor comparisons, and 406,131 Green/resistance and coordinate-update
checks. Every final result satisfies original ACL residual bounds; the
13,464 exact-stop traces agree with an independent obstacle solve.
All full solves, frontier scans, parent/LCA construction and cache operations
are audit-only reference work.

`MINIMUM_ROOT_THRESHOLD_AUDIT.json` explores the exact minimum policy without
an epsilon grid. For each current face, a frontier gate is positive iff
`lambda < c_j`, where
`c_j=gamma q_parent/(d_j+gamma y_parent)`,
`q=M_UU^-1 e_source` and `y=M_UU^-1 d_U`.
Minimum root threshold is maximum c_j, independently of lambda until stop.
Intersecting the previous admission bounds with quiet/positive requirements
gives exact valid intervals. The audit covers all trees through eleven
vertices, every seed, and alpha=1/3,1/7,1/1009: 13,179 parameter-independent
sequences, 122,388 symbolic admissions, 33 strict quiet-order reversals and
39 stale-minimum missed-positive intervals. Saved witnesses are rechecked
by independent dense solves and actual minimum choices. No minimum-policy
ACL miss was found in this finite family; a general guarantee remains Open.

`ROOT_THRESHOLD_WITNESSES_AUDIT.json` also checks four implicit tree families
with backbone lengths 4,8,16,32. The quiet reports at different ancestors
have distinct maps. Through length 32 the explicit per-group method would
perform 496 nonidentity maps, although support volume is 96. The construction
uses exponentially small epsilon, so this is not work exceeding 1/epsilon.
It demonstrates the ancestor-group cost and leaves room for stronger quietness
certificates. See `prop:op3-tree-many-threshold-groups`.

## Distinguish these results from existing notes

The AESP--CD result `prop:aesp-cd-point-source-homotopy-reorder` varies rho
on a cyclic six-vertex graph. Its projective pullback lemma already handles
a common two-port map, and its separated-slope meld handles disjoint slope
ranges. Its alternating external fan is a different obstruction. The
adaptive-revisit caterpillar reporter assumes a backbone-first phase and
uses fixed row factors. These are useful context/provenance; none is silently
imported as a new local complexity theorem here.

## Resume

Test the adjacent-path separation and projective convex-chain primitive in
`ORDERED_PATH_CLUSTER_PROBE.md`. The root-resistance formulas narrow the
question, but paying one operation per ancestor still gives the old radius
factor. A complete local hierarchy, exact due-event search, quietness and
recovery must be accounted for before stating a new tree work theorem.
