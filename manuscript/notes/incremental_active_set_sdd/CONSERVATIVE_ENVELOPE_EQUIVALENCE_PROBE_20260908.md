# A sharper remaining target: conservative significant-envelope discovery

This is a concrete proof/implementation probe, not an established equivalence.
General OP3 remains Open. Its literal nested-reuse requirement is stronger
than merely producing ACL output; keep that distinction in any reduction.

## First discharge small whole graphs at the desired scale

Develop a deterministic local component exploration with budget B=4/eps_appr.
Maintain original degrees of discovered distinct labels and query each row
at most once. If their known degree sum exceeds B, return a witnessed
lower bound vol(G)>B before allocating or reading an offending large row.
If the exploration closes, the complete original graph has volume <=B.
Use a charged balanced search tree for labels: the existing sorted dynamic
array can take quadratic insertion work and is not enough for this gate.
Every inspected incidence, comparison, queue operation, allocation and
degree reply must fit O((1+B) log(2+B)). A partially consumed row may be
charged in full before starting it; the sum of such started row degrees
must still be <=B. Test a private huge hub and a long path without known n.

On a complete small graph, the already proved alpha-independent supplied
envelope theorem applies to U=G. Its source-backed capped solve gives
the required ACL output in the desired inverse-accuracy work. Thus the
remaining large-graph case may assume vol(G)>4/eps_appr, with the initial
gate's work paid. The gate does not claim that its partial BFS labels form
an envelope; the earlier BFS obstruction remains valid.

## The conservative obstacle is then well posed and proper

Set e=eps_appr, lambda=e/2, delta=e/8, and b=e_v-lambda*d.
Let u0 minimize (1/2)u^T L u-b^T u over u>=0 at gamma=1.
Because lambda*vol(G)>2, the existing conservative existence proposition
gives a unique minimizer. It must have proper support S0: full-support
stationarity would have 0=sum(b)<0. Its original residual is nonnegative,
equals lambda*d on S0, and has a positive cut residual outside whenever
S0 is nonempty. Hence V0=vol(S0)<1/lambda=2/e and max(u0)<=|S0|<=V0.

Candidate target: produce U containing {i:u0_i>delta}, with original
volume O(1/e) and fully charged work (1/e) polylog(1/e,1/p), using no
ambient preprocessing. The output may omit smaller positive coordinates.
This problem contains no teleportation parameter.

## Forward reduction to original positive-alpha ACL

For target M_alpha=L+bar_alpha*A, same-load monotonicity should give
u_alpha<=u0. The proof uses the positive-target maximum principle, so
it remains valid when its upper comparison obstacle is conservative.
Thus U contains every target obstacle coordinate above the same delta.
Invoke the existing alpha-independent supplied-envelope theorem, with
its original load, confidence and degree-volume caps preserved.
This would reduce general ACL output to the conservative finder, after
the small-component gate. Source solvers remain explicit imports, not
implemented by a dense finite audit.

## Reverse reduction from a hypothetical fast ACL producer

This direction needs the standard original output-volume guarantee,
not merely an upper bound on the number of emitted labels. It may help
show that the conservative target captures the algorithmic ACL problem.

Let w solve L[S0,S0] w=d[S0], with zero values outside S0. A superlevel
flux argument with total source V0 should bound every edge difference
by V0 and then max(w)<=V0*|S0|<=V0^2. This is an existence/comparison
calculation; S0 and this inverse are not given to either algorithm.

For t=bar_a>0, let ut be the obstacle for M_t=L+t*A, with the SAME
load b. Its support lies in S0 by monotonicity. On S0,
L(u0-ut)<=t*A*ut<=t*d*max(u0). The positive Dirichlet inverse would give
0<=u0-ut<=t*max(u0)*w, so
||u0-ut||_infinity < 8*t/e^3.

Take t=e^4/128, corresponding to lazy a=t/(2-t). Then this error is
below e/16=delta/2. A hypothetical ACL solver at this a and residual
accuracy lambda=e/2 returns x>=ut by the least-nonnegative-supersolution
property, because M_t*x>=e_v-lambda*d. Therefore supp(x) contains every
conservative coordinate above delta. Its standard O(1/lambda) original
volume becomes the desired envelope volume; its log(1/a) factors are
only O(log(1/e)). Handle failure, output format and volume caps explicitly.

Needed exact audit: conservative KKT existence and proper support,
Dirichlet torsion bounds, same-load parameter comparison, the quantitative
gap at t=e^4/128, and support containment from genuine ACL outputs.
Do not let dense full-graph validators stand in for a local finder.

## The lower-bound scale survives large ambient graphs

A center-seeded star with m=floor(1/(8e)) degree-one leaves can have
an arbitrarily long path attached to its center. For alpha<=1/3 and
e<=1/16, d_center=m+1 and gamma>=1/2. Any original ACL output must have
x_center>=1/d_center-e. Omitting any degree-one leaf would require
gamma*x_center<=e, contradicting e*d_center<=1/8+e<1/3.
Thus all m=Omega(1/e) leaves must still be emitted, even when vol(G)
is above the component gate's budget. This is a residual-certificate
lower bound: its tiny-alpha semantic output may behave differently.
Prove and audit this directly rather than claiming the source's semantic
star formula transfers unchanged after appending the path.
