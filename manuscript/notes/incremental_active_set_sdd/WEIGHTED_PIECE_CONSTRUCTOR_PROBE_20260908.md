# Weighted constructor: replace component stretch by rooted-piece stretch

**Open proof-development target, 8 September 2026.** The complete supplied
constructor remains Conditional. This probe records the next argument to
verify and implement; none of its uncompleted steps is a source import.

## A stronger source obstruction than the earlier display mismatch

CPW arXiv:2105.14629v2, PDF p.23, Definition 5.7 sums the local stretch
of **all** original edges over each entire forest component. Lemma 5.9
claims a forest with at most j roots and maximum such component stretch
`O(m*log(n)*loglog(n)/j)`. The page was rendered and checked. The arXiv
metadata still lists v2 (3 June 2021) as current on 8 September 2026.

**Candidate elementary obstruction to the literal lemma:** on an m-leaf
unit star, every spanning forest with at most j components deletes at
most j-1 edges. The center component retains at least m-j+1 tree edges.
Each retained forest edge has local stretch one by Definition 5.4's
first case, so the component total is at least m-j+1. Take j about
sqrt(m); this exceeds any fixed constant times m*log(n)*loglog(n)/j
eventually. Verify exact finite forest enumerations and the asymptotic
quantifiers before promoting the obstruction to a proved note statement.
It concerns the printed intermediate quantity, **not** the final spectral
constructor theorem: on a star the original tree itself is an exact
preconditioner.

The proof on PDF p.27 says that a forest component lies within one
decomposition piece. Pieces sharing a boundary root can remain in the
same component. This suggests repairing the proof with edge-disjoint
rooted pieces that may meet at roots, rather than bounding whole-component
stretch. The earlier reversed cases in Claim 5.14 remain a separate issue.

## Proposed repair, to prove and audit

Let a refined tree decomposition have connected edge-disjoint pieces,
at most two shared boundary vertices each. Cut a minimum-congestion edge
between the two boundaries of every two-boundary piece. Keep each
resulting part as a separate rooted piece, even when it shares its root
with several other parts. Their union is a forest with one root per
component. Every original edge's canonical route uses at most two rooted
pieces and one core edge; a same-root route may cross the common root.

For each rooted piece B, bound
`sum_e c_e * resistance(P_F(e) intersect B) <= kappa`.
Different pieces have disjoint forest edges. This is the quantity needed
by Cauchy–Schwarz; it need not bound an entire component.

**Candidate direct quadratic comparison:** let H0 consist of forest edges
scaled by kappa>=1, plus canonical core edges of original conductance,
aggregated by root pair. Splitting each original edge difference over its
at most three route segments suggests `G <= 3*H0`. For the reverse bound,
each core root difference splits into the original edge difference and
its two forest endpoint segments. Summing suggests
`E_core <= 3*E_G + 3*kappa*E_F`, hence
`H0 <= 7*kappa*G`. Thus `Q=3*H0` would satisfy
`G <= Q <= 21*kappa*G`. Check same-root edges, cancellations, tree edges,
singleton roots and all parallel-edge aggregation explicitly.

## Congestion and weighted decomposition details

CPW's proof also writes the global corridor congestion as the congestion
of edges assigned to that piece. Edges with both endpoints outside can
traverse the complete two-boundary corridor. Their contribution is a
common additive constant at every corridor edge, so it should not change
the minimizer. Prove this common-offset statement rather than using the
displayed equality. The corrected Claim 5.14 cases then suggest local
stretch at most twice the piece's assigned original tree-stretch load.

An independent positive-weight decomposition may avoid all weight-ratio
questions. Let `w_v=sum_{e incident v} stretch_T(e)`; total vertex load
is `2*W`, with `W=sum_e stretch_T(e)`. Assign every vertex to exactly
one piece containing it, and assign each original edge to its endpoint
owner pieces. Each piece's assigned edge load is then at most its owned
vertex load.

Proposed DFS construction at threshold theta:

- Child remainders are connected and have owned load below theta. Merge
  their edge lists at the parent, flushing a connected piece once load
  reaches theta. Light parent load belongs to only the first relevant
  piece. Each nontrivial flushed piece has owned load below 2*theta.
- A vertex with load at least theta receives a singleton owner piece;
  its load is not charged again in incident nontrivial pieces.
- Keep only the connector vertex after a flush, with no second ownership.
  The final root remainder is the only extra subthreshold piece.
- There are at most `2*W/theta+1` pieces before refinement. Use linked
  lists for child remainder edge/owner lists; do not repeatedly copy
  an entire subtree. Total memberships should be O(n+number_of_pieces).

Refine each piece by its shared boundary vertices and branching vertices
of their Steiner tree. Partition maximal corridors and hanging branches
into pieces with at most two boundaries. Original vertex ownership must
be reassigned to exactly one refined piece that contains it, so no
piece gains more than its parent's owned load. Bound the number of new
pieces using the bipartite incidence tree of old pieces and shared
vertices: total boundary incidences is at most twice the old piece count.
Choose a conservative theta, e.g. a sufficiently large constant times W/j,
and handle small j with one piece and an arbitrary root. Derive explicit
constants only after the actual refinement algorithm and counts are fixed.

Tree distances, original edge stretches and congestion can be computed
with rooted-tree preprocessing and LCA path additions in O(m log n) word
work. Sorting root-pair records costs O(m log m) and charges every copy.
These are within the supplied near-linear polylog allowance; no local
discovery claim is made. The arbitrary-positive-weight low-stretch-tree
and fixed-accuracy sparsifier imports still require their exact source
contracts and confidence accounting.

## Next falsifiable checks

1. Exact star enumeration for the literal component-stretch obstruction.
2. Exhaustive small weighted tree decompositions/routings: component versus
   rooted-piece loads, common congestion offset, and both quadratic bounds.
3. Implement DFS ownership and refinement with all allocations/copies
   charged, including high-degree stars and zero/one/two-boundary pieces.
4. Only then compose with the source low-stretch tree and core sparsifier.
   General OP3 still requires local discovery after any supplied result.
