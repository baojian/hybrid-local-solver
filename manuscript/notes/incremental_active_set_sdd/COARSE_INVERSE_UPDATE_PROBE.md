# Next probe: maintained coarse inverse and paid port promotion

Date: 7 September 2026. **Completed proof draft and exact audit.**
The prospective transaction below is preserved. Its completed proof is
`sec:op3-maintained-inverse`, with full results in
`MAINTAINED_COARSE_INVERSE_AUDIT.json`. The r^2 work bound is Proved here
as a draft awaiting independent review. The next Open target is
`COARSE_PUBLICATION_PROBE.md`.

Original prospective status: **Open end-to-end construction.** The selected
conditional Green query and block identities are **Proved here**, as drafts
awaiting independent review, in `sec:op3-cluster-green`. The existing complete
cycle-rank theorem is `thm:op3-local-cycle-rank`, with work

`O(1 + V*((1+r)*L^4 + (1+r)^3 + q*L^2))`, `L=log(2+V)`.

Do not lower its cubic exponent merely because a rank-one inverse identity
exists. Implement and audit the following full transaction first.

## Completed selected Green primitive

`cluster_green_queries.py` extends a named affine parent walk by accumulating
the eliminated scalar variances. If an eliminated port m has current row
coefficient c and pivot delta, add c^2/delta. Optionally retain the pair
(c,1/delta), keyed by that current elimination record. A completed-square
factorization makes these scalar residuals independent.

The walk returns the at-most-two root coefficients a_i, shifted offset z_i,
and conditional variance G_ii. It takes O(log n) work on the imported
height-bounded hierarchy. Keeping traces uses O(log n) temporary words;
matching two traces gives conditional G_ij in O(log^2 n) conservative
dictionary work. Different tree pieces have conditional cross term zero
given their shared coarse ports. Do not infer zero covariance between
arbitrary records just because their root identities differ.

If J=(M_UU^{-1})_PP is the current retained-port inverse, the full entry is

`Green(i,j) = G_cond(i,j) + a_i^T J a_j`.

For physical coordinates use
`u_i = z_i + a_i^T (u_P-C*1) + C`.
The rows a_i have at most two nonzero positions in the full port namespace.

## Ordinary one-parent admission

Before changing the current source hierarchy, query its parent i to obtain
a_i, G_cond(i,i), and u_i. Set

`z = J*a_i`,
`variance = G_cond(i,i) + a_i^T*z`,
`delta = d_j - gamma^2*variance`,
`u_new_j = (gamma*u_i - lambda*d_j)/delta`.

The numerator is strictly positive from the admitted original gate, and
delta >= bar_alpha*d_j > 0 by the original principal-matrix energy bound.
With P unchanged, update

`J_new = J + (gamma^2/delta)*z*z^T`,
`u_P_new = u_P + gamma*z*u_new_j`.

This is O(|P|^2) actual inverse writes plus O(|P|) vector arithmetic; every
read, copy and overwrite must be charged. Then append the leaf to its
parent's home tree piece, update changed ordinary heap payloads, and restore
the affected source exposures before another gate check.

## Cycle birth: old-port promotion, one border, possible restriction

Suppose j has a>=2 active parents. The existing partition algorithm keeps
one insertion-tree parent, adds a-1 extra edges and computes a new retained
set P_new from the old seed and all extra-edge endpoints plus Steiner
junctions. Its permanent retained set is monotone: marks grow and a degree-
three vertex of the marked Steiner subtree can never cease to be branching.

1. Preserve the **old current** component roots, port values, inverse and
   home-component map until all promotion queries finish. The new row may
   be scanned after its gate is certified, and the new partition may be
   computed from cached edges, but do not mix noise traces from different
   source hierarchy versions. Full map copies at a cycle birth are allowed
   only with their existing paid O(V) rebuild charge.
2. Promote every old vertex in P_new\P and every active parent of j that is
   not yet retained. At most one parent can be an extra temporary port: the
   chosen insertion-tree parent. All other parents are endpoints of new
   extra edges and therefore belong to P_new. Obtain each promoted vertex's
   old conditional response and trace from its old home piece.
3. Using the old J as a fixed baseline, fill the augmented inverse with
   `G_cond(i,j)+a_i^T J a_j`. Cross terms with old ports need at most two
   columns of J; cross terms between promoted interiors use trace matching
   only when they came from the same old piece. Append their physical means
   from their old exact conditional responses. Charge every matrix copy.
4. All active parents are now retained. Let s be their indicator in this
   augmented port set. Compute z=J_aug*s and
   `delta=d_j-gamma^2*s^T*z`. Border j using

   `J_border = [[J_aug + gamma^2*z*z^T/delta, gamma*z/delta],
                [gamma*z^T/delta,                 1/delta]]`.

   Its physical value is the full original gate divided by delta; increase
   old retained values by gamma*z*u_new_j. Include every active edge of j.
5. If the insertion-tree parent was only a temporary port, restrict the
   **inverse** to the principal submatrix indexed by P_new (including j).
   This is the inverse of the Schur system after that port is eliminated;
   it is not the principal submatrix of the original coarse matrix. Charge
   the dense restriction copy. Rebuild the new component hierarchies and
   home-component map exactly as in the existing cycle-rank algorithm.

This temporary-port option keeps the original partition algorithm and its
|P|<=4r bound unchanged. Retaining all parents permanently is another valid
candidate but enlarges the marked set and requires a different bound; do
not mix those variants silently.

## Candidate total ledger

There are O(r) permanent promotions, plus at most one transient promotion
per cycle-birth event, hence O(r) promotion occurrences overall. Capturing
their traces costs O(r log^2 V); all pairs of promoted points cost at most
O(r^2 log^2 V). Even a simple implementation that copies an O(r)-square
matrix once per promoted coordinate costs O(r^3), which is covered by
O(V*r^2), since r<=V. Ordinary and cycle-birth border updates each cost
O((1+r)^2), and there are at most |U| admissions.

Together with the already paid partition rebuilds and exceptional queries,
the candidate improved bound is

`O(1 + V*((1+r)*L^4 + (1+r)^2 + q*L^2))`.

This would give O_tilde((1+r^2+q)/rho) exact RPPR and the analogous ACL bound.
It still does not resolve general OP3. In particular, dense inverse writes
are a real r^2 cost, and repeated quiet exceptional gates still cost q per
checkpoint in this representation.

Space must state which histories are retained: all cluster/hull versions
and historical one/two-port solutions may be saved within
O((1+r)*V*L^3), while only the **current coarse inverse** is kept, in
O((1+r)^2) words. Retaining every dense inverse version would incur another
V*r^2 term; do not claim it within the smaller space bound.

## Required audit and rejection criteria

- Run actual source-driven admissions on all small connected graphs, both
  parent/admission policies, and the existing structured multi-cycle families.
- Independently assemble the current coarse Schur matrix from the full
  original active matrix; verify J*K=I exactly and every retained physical
  mean against a separate full-face solve. Matrix multiplication is an
  independent inverse certificate, not another use of the update formula.
- Exercise simultaneous cycle births, many promoted junctions, a temporary
  insertion parent subsequently dropped, no new old ports, and repeated
  admissions after a fixed cycle core has formed.
- Compare every ordinary and exceptional gate, final obstacle solution and
  original ACL residual. Include the finite implicit private-star families
  with no inactive hub scans and alpha=1/1009.
- Count original accesses, conditional parent walks, covariance matches,
  inverse entry writes, matrix copies/restrictions, partition rebuilds,
  failed reports, all historical cluster state and final output separately.
- Preserve the old version until promotion is complete. A mismatch between
  old means, old conditional traces and the current inverse is a correctness
  failure even if a dense rebuild could hide it.

Only after these checks and a full work proof should the r^3 term in the
previous theorem be replaced by r^2 for this maintained-inverse variant.

## Exact first transaction to reproduce

Triangle edges {0,1},{1,2},{0,2}, physical seed 0, alpha=1/3, lambda=1/20.
On legal old face U={0,1}, retain only P={0}. Then
J00=8/15 and the physical old values are (7/15,1/15). Choosing 1 as the
insertion parent when 2 is admitted makes the extra edge {0,2}; permanent
new ports are {0,2}, so 1 is a transient promoted parent.

The old conditional response of 1 has coefficient 1/4 and conditional
variance 1/2, giving promoted inverse
`[[8/15,2/15],[2/15,8/15]]` on {0,1}.
For the two-parent border, z=(2/3,2/3), delta=5/3, gate=1/6 and u2=1/10.
The full triangle inverse has diagonal 3/5 and off-diagonal 1/5, while its
physical means become (1/2,1/10,1/10). Restricting that inverse to {0,2}
gives `[[3/5,1/5],[1/5,3/5]]`; the corresponding independently assembled
coarse matrix is `[[15/8,-5/8],[-5/8,15/8]]`. Their product is the identity.
This transaction checks both temporary promotion and its later removal.
