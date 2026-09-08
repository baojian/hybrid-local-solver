# Implementing the exact live-frontier elimination baseline

**Completed as a proof draft and implemented reference.** Read
`sec:op3-exact-frontier`, `frontier_exact.py`, and
`FRONTIER_EXACT_AUDIT.json`. The audit passes 7,305 original outputs and
12,986 prefix states. The fill-dependent cost and cubic star-and-tail
obstruction are now proved; general OP3 remains Open.

The following implementation plan is retained as provenance.

Originally the next constructive target. The algebraic predecessor is
`FRONTIER_ELIMINATION_PROBE.md`; no implementation was found under its
live-frontier/elimination anchors. Preserve its star-fill obstruction.
General OP3 remains Open. The point here is an actual paid baseline and
a measured fill/reporting ledger, not a claimed improvement over the
known quadratic source rate.

## Input and invariant

Use original M=D-gamma*A, gamma=(1-alpha)/(1+alpha), alpha in (0,1],
lambda=eps_appr/2, kappa=lambda/2. After eliminating admitted A,
an exposed unadmitted vertex i has exact transformed load

h_i = b_i - M_iA M_AA^-1 b_A = r_i^A-lambda*d_i,

exact Schur diagonal s_i, and nonnegative effective conductances to
other unadmitted labels. Admit only if h_i>kappa*d_i. True h values
only increase under legal positive pivots, so an intrusive queue needs
one insertion per admitted label. At termination, the exact face solution
has active residual lambda*d and all outside residual at most
(lambda+kappa)*d=3eps_appr*d/4. Unseen labels have no admitted neighbor.

Every admitted face is safe for the original lambda obstacle, so its
original degree volume is below 1/lambda even on full support at positive
alpha. Hence there are O(1/eps_appr) admissions and discovered labels,
and total original queried-row degree is O(1/eps_appr). A newly discovered
huge degree is one word/reply; its adjacency is not allocated or read
unless the mathematical admission gate succeeds. Before each original
row buffer, check the active-volume cap as an invariant.

## Exact update and final reconstruction

On admission i, first expose its original row once. Add gamma to its
conductance with each still-unadmitted original neighbor. Original neighbors
already eliminated are skipped: their effect is already in s_i, h_i and
the retained fill. This avoids reading any unadmitted original row and
avoids double-counting an original edge. Newly encountered labels get one
degree query and initial h_j=-lambda*d_j (plus source at the seed), s_j=d_j.

Gather current positive effective neighbors j, with weights w_ij. Let
z_i=h_i/s_i>0 and store z_i and coefficients w_ij/s_i for final lifting.
Then update, for all current neighbors and unordered neighbor pairs,

s_j -= w_ij^2/s_i,
h_j += w_ij*z_i,
w_jk += w_ij*w_ik/s_i.

Check each changed h_j gate, then unlink the incident edges of i.
After discovery finishes, reverse the elimination records and set
x_i=z_i+sum_j (w_ij/s_i)*x_j, with never-admitted coordinates zero.
Only this final pass materializes the active potentials. Emit the original
probabilities bar_alpha*d_i*x_i in a paid pass. No dense inverse oracle or
repeated full face solution is part of the producer.

## Data structures and accounting to implement

Use deterministic AVL maps with explicit charged comparisons, rotations
and node allocation. One map indexes original vertex labels; a second
indexes unordered pairs of stable internal vertex indices. Each pair
record holds its exact weight and intrusive links in both endpoint
adjacency lists. On elimination, unlink each incident pair in constant
work per endpoint. The pair-map key can remain as inactive history:
an eliminated endpoint is never reused, so no AVL deletion is needed.
All historical pair records remain charged, and there are at most
O(V^2) distinct pairs. Do not hide an uncharged Python dictionary or a
linear scan of all known labels in the production path.

For p_i live effective neighbors at elimination, target the honest bound

O((1+V+sum_i(p_i+1)^2)*log(2+V))

for work and total allocated words, including map insertions, all pair
updates, queues, input/degree/row access, failed gates, saved coefficients
and final output. This is at most O(V^3 log(2+V)), with live state
O(V^2), and it has no target-alpha arithmetic dependence. All bit/precision
claims remain separate. It is a weak general reference; the important
measured parameter is the actual fill sum and number of load publications.

## Audit plan

Use independent dense exact face/Schur/obstacle checks only as validators
on small graphs. Check each prefix h, s, fill, queue and active-volume
invariant, then every original final residual row. Include paths, cycles,
trees, complete and sparse cyclic graphs, alpha through very small dyadic
values, exact threshold ties, arbitrary labels and a private huge hub whose
row must not be read. A star with a long tail gives a large ambient graph
and a dense live clique after the center pivot; count cubic pair work
without turning it into a universal lower bound. Keep graph reads,
fill generation, h updates, failed gates and reconstruction separately.

After this baseline, useful targets are implicit clique/rank compression
with a real threshold reporter, or controlled original-residual refinement.
The source random approximate-elimination order is not automatically a
legal positive-pivot order, and its spectral factor product need not have
the M-matrix signs. Those shortcuts were explicitly ruled out above.
