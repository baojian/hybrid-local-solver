# Adaptive response groups for exact frontier elimination

**Completed as a proved draft and implemented reference.** Read
`sec:op3-frontier-response-groups`, `frontier_groups.py` and
`FRONTIER_GROUPS_AUDIT.json`; 7,311 outputs and 5,700 reverse aggregate
checks pass. The following original plan is retained as provenance.
The structural continuation is `FRONTIER_GROUP_STRUCTURE_PROBE_20260908.md`. General OP3
remains Open. The paid explicit reference and its cubic fill obstruction
are now complete in `sec:op3-exact-frontier` and `FRONTIER_EXACT_AUDIT.json`.
This proposal compresses vertices that share their current response to
the admitted set. It does not assume a supplied graph partition.

## Exact state to implement

After eliminating admitted S, partition known unadmitted labels into groups
whose original adjacency columns into S coincide. Do not group by degree:
retain each individual original degree d_j. For group t, maintain q_t and
a symmetric matrix C on groups so that each member j in t has

    h_j = -lambda*d_j + q_t,
    s_j = d_j - C_tt,
    fill(j,k) = C_tu,  j in t, k in u, j != k.

Handle the initial source by a singleton seed group with q=1 and C=0.
After its first admission all unadmitted source terms are zero. A group
may contain different original degrees and unrelated unread outside rows.
Its minimum original degree determines whether any member satisfies the
strict gate q_t > (lambda+kappa)*d_j. A binary heap per group with stable
vertex positions supports insertion and arbitrary removal in logarithmic
work. Scanning all current groups for an eligible minimum costs O(B),
not O(number of member vertices), and is charged explicitly.

On removing eligible i from group p, save

    sigma = d_i-C_pp, z_i=(-lambda*d_i+q_p)/sigma.

Read its original row once, with the same pre-row volume guard as the
explicit reference. Every still-unadmitted old neighbor moves to a new
child of its existing group, one child per parent in this row. Moving
exactly the encountered neighbors refines each old group into original
neighbors and nonneighbors of i. The row itself pays for all membership
moves; no scan of the other members is allowed. Newly discovered labels
form one new group with previous q=0 and C=0. Mark these neighbor groups
for the current pivot. Empty parent groups can be retired after their
response values have served the current update.

Cloning group t copies its q and its C interactions with every current
group, costing O(B) matrix operations. The child-child self term is C_tt;
old and cloned interactions agree until the next Schur update. For each
remaining group t, the effective coupling from the removed pivot is

    w_t = C_pt + gamma*(t was made from an original neighbor of i).

The exact update is one scalar per group and one entry per group pair:

    q_t += w_t*z_i,
    C_tu += w_t*w_u/sigma, including t=u.

Original edges between unadmitted vertices remain unread, just as in the
explicit reference. Only the newly exposed pivot row adds their coupling.
No degree-sized buffer for an unadmitted huge outside hub is permitted.

## Reconstruction without expanding group membership

Save z_i and one coefficient w_t/sigma for each current group, rather
than one coefficient per member. Also save the chronological group-split,
new-group, group-retirement and pivot-removal records. Start the final
reverse replay with zero sums for all final unadmitted groups. At a reversed
pivot, the sums refer to the sets immediately after its forward partition
refinement and removal. Compute

    x_i = z_i + sum_t (w_t/sigma)*sum_of_values_in_group_t.

Undo the splits by adding each child's sum to its old parent; discard a
fresh discovery group's aggregate, since those labels did not occur in
earlier frontier responses. Their individual output values remain saved.
Finally reinsert x_i into its pre-removal parent's aggregate. Retired
empty groups are restored with zero aggregate when necessary. This order
must be checked against an independent full back substitution; a forward
group name alone is not a persistent membership snapshot.

## Intended honest bound and falsifiable tests

Let B_i count nonempty groups around pivot i, including newly split groups,
and k_i the number of newly created groups. The target bound is

    O((1+V + sum_i (B_i+1)^2 + sum_i k_i*(B_i+1))*log(2+V))

for work and total allocated words. The group count and total new groups
are O(1+V): every split has an original neighbor incidence to pay for it.
Thus the general worst case is still cubic. Do not claim a universal small
group count. Stable label lookup, heap swaps/positions, all matrix lookups
and clones, failed group gates, reverse aggregates and output must be paid.
Historical matrix entries may remain in an insertion-only AVL map and are
charged. Total heap insertions/moves are O(1+V), because they are paid by
one-time original row entries; no small-to-large assumption is needed.

First tests: compare every h, s and fill coefficient with exact face Schur
systems on small graphs; compare every final original residual and lifted
coordinate. Include exact gate ties, multiple groups splitting in one row,
an entire group moving, empty parents, unequal degrees, arbitrary labels,
tiny alpha, and private huge hubs. On the star-with-tail family, the leaf
clique should remain one group until the leaves are removed, turning cubic
pair work into a linear number of group updates plus heap costs. Explore
where response diversity itself grows on sparse graphs before making any
broader structural claim. Existing fast tree and multipartite algorithms
remain prior context, not new achievements of this representation.
