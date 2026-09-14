# Exact degree-two elimination: an OP2 extension to partial 2-tree supports

Status: a proved deterministic structural extension. This note does not
prove general OP2. It concerns exact principal solves, not a transformation
of the obstacle problem into a different preconditioned obstacle problem.
Only the permitted definitions and fresh current-task work are used.

## 1. Local matrix and elimination algorithm

For the currently admitted safe set S, materialize its induced matrix

    H=alpha*D+c*diag(d-d_S)+c*L(G[S]),
    c=(1-alpha)/2.

Write it as `diag(g)+L(C)`, with positive grounding
`g_i=alpha*d_i+c*(d_i-d_S(i))` and nonnegative edge conductances. Full
degrees and induced edges come from the charged active adjacency scans.
Nothing about unseen adjacency lists or the final support is required.

Maintain the current weighted off-diagonal graph using deterministic
balanced maps. Initialize a deterministic queue of its vertices of degree
at most two. When an eligible vertex v is removed, its pivot is

    kappa_v=g_v+sum_(u adjacent v)c_vu>0.

Save that pivot and the at most two neighbor coefficients for subsequent
forward and backward substitution. For each surviving neighbor u, update

    g_u <- g_u+c_uv*g_v/kappa_v.

If v has two distinct neighbors u,w, insert or increase their conductance by

    c_uw <- c_uw+c_uv*c_vw/kappa_v.

Remove the edges incident to v. These formulas are exactly its Schur
complement, expressed as positive grounding plus a weighted Laplacian.
In particular grounding remains strictly positive. Equivalently, the
ordinary matrix formulas are

    H_ij <- H_ij-H_iv*H_vj/kappa_v,
    h_i <- h_i-H_iv*h_v/kappa_v.

The latter RHS updates give a direct solve for one RHS. Storing the
elimination factors instead gives linear-time applications to later RHSs.
Back substitution uses the saved equation at each removed vertex.

Degrees never increase in a degree-at-most-two elimination. A degree-two
neighbor loses its edge to v and gains at most one edge to the other
neighbor; if that edge already existed, its degree decreases. Thus a queue
and explicitly charged stale-entry checks suffice; a priority heap is not
necessary. Each elimination inserts at most one new edge and affects at
most two surviving vertices.

There are O(|S|) fill insertions and O(|S|) elimination records. Including
initial graph construction, map operations, degree bookkeeping, RHS
updates, and substitutions, the total is

    O(vol(S)*log(vol(S)+2))

exact-real logical work if the queue exhausts the matrix.

## 2. Why this always exhausts a graph of treewidth at most two

Here is a self-contained graph argument; the solver does not need a tree
decomposition as input.

A tree decomposition of width at most two has bags of size at most three,
every graph edge is in a bag, and the bags containing any fixed vertex form
a connected subtree. Remove any leaf bag contained in its neighboring bag,
repeatedly. If one bag remains, every vertex has degree at most two. Otherwise
take a leaf bag B and a vertex v in B absent from its neighboring bag. The
connected-subtree property implies that v occurs in no other bag. Every
neighbor of v is therefore in B, and v has degree at most two. This proves
that every nonempty graph of treewidth at most two has an eligible vertex.

Such decompositions are preserved under graph minors. For a vertex deletion,
remove its label from the bags. For contraction of an edge uv, replace u and
v by one label. The union of their bag subtrees is connected because some
bag contains both endpoints; bag sizes do not increase.

Removing a vertex v of degree two and adding the edge between its neighbors
is precisely a graph minor: contract one incident edge, retaining the label
of that neighbor. If the neighbors were already adjacent, the duplicate
edge is merged. Removing a vertex of degree zero or one is also a minor.
The positive Schur conductance formulas create exactly this adjacency
pattern; there is no cancellation creating an extra edge.

Consequently every intermediate filled graph still has treewidth at most
two and, if nonempty, still has an eligible vertex. Arbitrary deterministic
choices among eligible vertices therefore exhaust it. These graphs are also
called partial 2-trees; no particular series-parallel terminal structure is
needed for the proof.

## 3. Fully charged local consequence

Suppose the unknown optimal induced support graph G[S*] has treewidth at
most two. Safe all-violations admission gives `S_t subseteq S*`, so every
G[S_t] is also of treewidth at most two. The procedure above solves each
principal system in `O(vol(S_t)*log(vol(S_t)+2))` work. The algorithm does
not receive S* or a decomposition; successful elimination certifies each
current solve directly.

Combining `vol(S_t)<=1/rho` with the already proved accelerated exact-batch
stage bound yields

    tilde O(1/rho *
       [1+alpha^(-1/2)*log_+(2alpha/epsilon)]).

This includes examples with cyclomatic number Theta(1/rho), such as many
triangles joined at articulation vertices. It is therefore strictly more
general than a constant/polylogarithmic cycle-rank guarantee. It remains a
structural theorem, not a general-graph OP2 proof.

## 4. What remains on an arbitrary graph

When the queue empties early, the remaining Schur graph has minimum degree
at least three. Call it the **minimum-degree-three Schur core**. It is not
the usual graph 3-core: subdividing every edge of K4 makes the ordinary
3-core empty, whereas degree-two elimination reconstructs a K4 Schur core.

The remaining matrix is again strictly grounded SDD with nonpositive
off-diagonals. If C is its vertex set, the original normalized spectral
bounds also survive:

    alpha*D_C <= H_core <= D_C.

For the lower bound, use the variational characterization of a Schur
complement and `H>=alpha*D`; minimize over eliminated coordinates. For the
upper bound, take those coordinates to be zero and use `H_CC<=D_C`.

One may solve this smaller matrix by exact PCG, then back substitute. A
forest preconditioner built from its *updated* grounding and *updated*
weighted conductances again differs from the core by a PSD chord update
of rank at most its cycle rank, so the same r_core+1 exact iteration bound
applies. Forest factor/application cost is linear in the core representation.
The constant-c/original-degree implementation must not be used verbatim on
this weighted Schur matrix; its matvec and factor inputs must be generalized
to the updated weights and grounding.

Thus a fully charged fallback has per-stage cost

    O(vol(S)*log(vol(S)+2)
       +(r_core+1)*(|C|+|E_core|)*log(vol(S)+2)).

The eliminated paths and trees are paid for once per stage, rather than
once per core PCG iteration. No general amortized bound for the core term
has been proved here. This note specifies and proves the extension but
does not add a separate implementation to the existing prototype.
